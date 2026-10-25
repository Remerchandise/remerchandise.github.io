"""A2 Ronde 3 – inductiesimulatie K1 (VLF 3 freq, 1 lus) en K2 (PI, 2 lussen, ferro-kanaal).

Draaien: python3 experiments/r3_inductie/sim_inductie.py   (vanuit repo-root; seed vast)
Output: sensor_model_K1.json, sensor_model_K2.json, resultaten.json, fig_*.png in deze map.
"""
import json, os, sys, time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import params  # noqa
from objects import make, pad, MAXM  # noqa

T0 = time.time()
RNG = np.random.default_rng(20261025)
ITEMS = params.ITEMS
LI_ITEMS = [k for k, v in ITEMS.items() if v["li"]]
PACK_ITEMS = ["powerbank", "laptop_gereedschap", "ebike_step"]  # Orchestrator: pakket = powerbank en groter
CLUTTER = [k for k, v in ITEMS.items() if not v["li"] and v["metal"] != "none"]

# ---------------------------------------------------------------- geometrie
L = 0.40          # trommel 40x40x40 cm; lus T in z=0 (opening), lus B in z=-0.40 (bodem)
BOX = dict(x=(-0.17, 0.17), y=(-0.17, 0.17), z=(-0.37, -0.03))


def loop_field(P, z0, n=60):
    """Biot-Savart (per A) van vierkante lus LxL in vlak z=z0, punten P (N,3)."""
    h = L / 2
    c = np.array([[-h, -h], [h, -h], [h, h], [-h, h], [-h, -h]])
    B = np.zeros_like(P)
    for i in range(4):
        a = np.r_[c[i], z0]; b = np.r_[c[i + 1], z0]
        t = (np.arange(n) + 0.5) / n
        mids = a + np.outer(t, b - a); seg = (b - a) / n
        r = P[:, None, :] - mids[None]
        rn = np.linalg.norm(r, axis=2)[..., None]
        B += np.sum(np.cross(seg[None, None, :], r) / rn ** 3, axis=1)
    return 1e-7 * B


B0 = np.linalg.norm(loop_field(np.zeros((1, 3)), 0.0))


from scipy.interpolate import RegularGridInterpolator
_G = [np.linspace(BOX[a][0], BOX[a][1], 29) for a in "xyz"]
_GP = np.stack(np.meshgrid(*_G, indexing="ij"), -1).reshape(-1, 3)
_FT = (loop_field(_GP, 0.0) / B0).reshape(29, 29, 29, 3)
_FB = (loop_field(_GP, -L) / B0).reshape(29, 29, 29, 3)
_IT = RegularGridInterpolator(_G, _FT); _IB = RegularGridInterpolator(_G, _FB)


def fields(P):
    """Veld per A van lus T (opening) en B (bodem), genormaliseerd op lusmidden T; grid-interpolatie."""
    return _IT(P), _IB(P)


# ---------------------------------------------------------------- ruis/achtergrond [A]
# eenheden: cm^3-equivalent polariseerbaarheid in het centrum van lus T
NOISE = {  # laag / basis / hoog / ideaal (index 3: vrijwel ruisloos -> alleen clutter beperkt)
    "sig_w_1ms": (0.6, 2.0, 6.0, 0.01),   # witte ruis per 1 ms meting
    "sig_drift": (0.1, 0.3, 1.0, 0.01),   # 1/f + temperatuurdrift-vloer na vóór/na-verschil
    "sig_bg": (0.5, 2.0, 20.0, 0.0),     # restsignaal RVS-trommel/stalen zuil (meedraaiende spoel); niet meedraaiend: ~200+
}
T_MEAS = 2.0  # s stilstand (opdrachtgever: 1-10 s)


def sigma_tot(T, lvl=1, bg=True):
    w = NOISE["sig_w_1ms"][lvl] / np.sqrt(T * 1000)
    return np.sqrt(w ** 2 + NOISE["sig_drift"][lvl] ** 2 + (NOISE["sig_bg"][lvl] ** 2 if bg else 0))


FREQS = np.array([5e3, 15e3, 40e3])            # K1
GATES = np.array([10, 30, 90, 270, 810]) * 1e-6  # K2 PI-vensters
TG0 = 10e-6
BG_MODES = [(2, 1.0, 260e-6), (1, 1.0, 5e-3)]  # RVS-trommel (eddy) + verzinkte zuil (ferro), genormaliseerd


def vlf(kind, p, tau, f):
    w = 2 * np.pi * f
    jwt = 1j * w * tau
    return np.where(kind == 1, p / (1 + jwt), np.where(kind == 2, -p * jwt / (1 + jwt), 0))


def pi_g(kind, p, tau, t):
    return np.where(kind > 0, p * (TG0 / tau) * np.exp(-t / tau), 0.0)


def bg_vec():
    k = np.array([m[0] for m in BG_MODES]); p = np.array([m[1] for m in BG_MODES]); t = np.array([m[2] for m in BG_MODES])
    v1 = np.concatenate([[vlf(k, p, t, f).sum().real, vlf(k, p, t, f).sum().imag] for f in FREQS])
    v2 = np.array([pi_g(k, p, t, g).sum() for g in GATES])
    return v1 / np.abs(v1).max(), v2 / np.abs(v2).max()


BG1, BG2 = bg_vec()

# ---------------------------------------------------------------- objecten trekken
def tri(rng, lo, mid, hi):
    return lo if hi <= lo else rng.triangular(lo, mid, hi)


def draw_obj(item, rng, wh=None):
    if isinstance(item, tuple):
        item, wh = item
    wh = tri(rng, *ITEMS[item]["wh"]) if wh is None else wh
    kind, D, tau = pad(make(item, rng, wh))
    return kind, D, tau, wh


def draw_clutter_counts(rng, mode="bag", n=None):
    """'bag': realistische zak volgens params; 'fixed': precies n metaalobjecten (samenstelling ∝ mean)."""
    if mode == "bag":
        out = []
        for k in CLUTTER:
            v = ITEMS[k]; m = v["mean"]
            if v["dist"][0] == "nb":
                r = v["dist"][1]; c = rng.negative_binomial(r, r / (r + m))
            else:
                c = rng.poisson(m)
            out += [k] * c
        return out
    w = np.array([ITEMS[k]["mean"] for k in CLUTTER]); w /= w.sum()
    return list(rng.choice(CLUTTER, size=n, p=w))


def measure(bags, lvl=1, T=T_MEAS, rng=RNG):
    """bags: lijst van lijsten itemnamen. Geeft features K1 (6), K2 (17) + hulpgrootheden."""
    flat = [(bi, it) for bi, b in enumerate(bags) for it in b]
    nb = len(bags)
    F1 = np.zeros((nb, 2 * len(FREQS))); F2 = np.zeros((nb, 3 * len(GATES) + 2))
    if flat:
        idx = np.array([f[0] for f in flat])
        N = len(flat)
        kinds = np.zeros((N, MAXM), int); Ds = np.zeros((N, MAXM, 3)); taus = np.ones((N, MAXM))
        for i, (_, it) in enumerate(flat):
            kinds[i], Ds[i], taus[i], _ = draw_obj(it, rng)
        P = np.column_stack([rng.uniform(*BOX[a], N) for a in "xyz"])
        R = Rotation.random(N, random_state=rng.integers(1 << 31)).as_matrix()
        hT, hB = fields(P)
        uT = np.einsum("nij,ni->nj", R, hT); uB = np.einsum("nij,ni->nj", R, hB)  # R^T h
        pTT = np.einsum("nj,nmj,nj->nm", uT, Ds, uT)
        pBB = np.einsum("nj,nmj,nj->nm", uB, Ds, uB)
        pTB = np.einsum("nj,nmj,nj->nm", uT, Ds, uB)
        for fi, f in enumerate(FREQS):
            z = vlf(kinds, pTT, taus, f).sum(1)
            F1[:, 2 * fi] += np.bincount(idx, z.real, nb); F1[:, 2 * fi + 1] += np.bincount(idx, z.imag, nb)
        for ci, pc in enumerate([pTT, pBB, pTB]):
            for gi, g in enumerate(GATES):
                F2[:, ci * len(GATES) + gi] += np.bincount(idx, pi_g(kinds, pc, taus, g).sum(1), nb)
        for ci, pc in enumerate([pTT, pBB]):  # ferro-kanaal: Re alpha bij 1 kHz
            F2[:, 15 + ci] += np.bincount(idx, vlf(kinds, pc, taus, 1e3).sum(1).real, nb)
    s = sigma_tot(T, lvl, bg=False)
    sbg = NOISE["sig_bg"][lvl]
    F1 += rng.normal(0, s, F1.shape) + rng.normal(0, sbg, (nb, 1)) * BG1
    bg2 = np.concatenate([BG2, BG2, BG2 * 0.3, [1.0, 1.0]])
    F2 += rng.normal(0, s, F2.shape) + rng.normal(0, sbg, (nb, 1)) * bg2
    return F1, F2


def feat(F):
    return np.arcsinh(F / 1.0)


# ---------------------------------------------------------------- datasets
def label(item):
    if item in PACK_ITEMS: return 2
    if ITEMS[item]["li"]: return 1
    return 0


def build(n_per, rng, clutter="bag", nfix=None, items=None):
    items = items or list(ITEMS)
    bags, y, tgt = [], [], []
    for it in items:
        for _ in range(n_per):
            c = draw_clutter_counts(rng, clutter, nfix) if clutter else []
            bags.append([it] + c); y.append(label(it)); tgt.append(it)
    return bags, np.array(y), np.array(tgt)


class KNN:
    def __init__(self, X, y, k=31):
        self.mu = np.median(X, 0); self.sd = np.percentile(X, 75, 0) - np.percentile(X, 25, 0) + 1e-3
        self.t = cKDTree((X - self.mu) / self.sd); self.y = y; self.k = k
        self.w = np.array([1.0 / max(1, (y == c).sum()) for c in range(3)])

    def proba(self, X):
        _, I = self.t.query((X - self.mu) / self.sd, k=self.k, workers=-1)
        Y = self.y[I]
        P = np.stack([(Y == c).sum(1) * self.w[c] for c in range(3)], 1)
        return P / P.sum(1, keepdims=True)


def run_concept(name, lvl=1, T=T_MEAS, n_train=2500, n_eval=600, verbose=True):
    rng = np.random.default_rng(1000 + lvl * 10 + (name == "K2"))
    col = 0 if name == "K1" else 1
    # training: 70 % realistische zak-clutter, 30 % alleen
    b1, y1, _ = build(int(n_train * 0.7), rng, "bag")
    b0, y0, _ = build(int(n_train * 0.3), rng, None)
    btr = b1 + b0; ytr = np.r_[y1, y0]
    btr += [draw_clutter_counts(rng) for _ in range(n_train * 3)]; ytr = np.r_[ytr, np.zeros(n_train * 3, int)]
    Xtr = feat(measure(btr, lvl, T, rng)[col])
    clf = KNN(Xtr, ytr)
    # drempels op realistische clutter-zakken zonder Li
    bval = [draw_clutter_counts(rng) for _ in range(20000)]
    Pv = clf.proba(feat(measure(bval, lvl, T, rng)[col]))
    t_pak = np.quantile(Pv[:, 2], 1 - 0.002)
    t_li = np.quantile(Pv[:, 1] + Pv[:, 2], 1 - 0.02)

    def decide(P):
        out = np.zeros(len(P), int)
        out[(P[:, 1] + P[:, 2]) >= t_li] = 1
        out[P[:, 2] >= t_pak] = 2
        return out

    res = {"t_pak": float(t_pak), "t_li": float(t_li)}
    # p_out_given_item (alleen in zak)
    be, ye, te = build(n_eval, rng, None)
    oe = decide(clf.proba(feat(measure(be, lvl, T, rng)[col])))
    pout = {it: [float(np.mean(oe[te == it] == c)) for c in range(3)] for it in ITEMS}
    res["p_out_given_item"] = pout
    # met realistische clutter
    bc, yc, tc = build(n_eval, rng, "bag")
    oc = decide(clf.proba(feat(measure(bc, lvl, T, rng)[col])))
    res["p_out_given_item_in_bag"] = {it: [float(np.mean(oc[tc == it] == c)) for c in range(3)] for it in ITEMS}
    # clutter-only zakken: realistische valse-uitvoer per zak
    bq = [draw_clutter_counts(rng) for _ in range(8000)]
    oq = decide(clf.proba(feat(measure(bq, lvl, T, rng)[col])))
    nq = np.array([len(b) for b in bq])
    res["clutter_bag"] = {"p_out": [float(np.mean(oq == c)) for c in range(3)],
                          "p_out_given_n_metal": {str(n): [float(np.mean(oq[(nq == n) if n < 3 else (nq >= 3)] == c)) for c in range(3)] for n in range(4)},
                          "frac_bags_n_metal": [float(np.mean(nq == n)) for n in range(3)] + [float(np.mean(nq >= 3))]}
    # masking: Li-item + n clutter
    wli = np.array([ITEMS[i]["mean"] * ITEMS[i]["wh"][1] * ITEMS[i]["w_chem"] * ITEMS[i]["w_state"] for i in LI_ITEMS])
    det = {}
    for n in range(4):
        if n < 3:
            bm, ym, tm = build(n_eval // 2, rng, "fixed" if n else None, n, LI_ITEMS)
        else:
            bm, tm = [], []
            for it in LI_ITEMS:
                k = 0
                while k < n_eval // 2:
                    c = draw_clutter_counts(rng)
                    if len(c) >= 3:
                        bm.append([it] + c); tm.append(it); k += 1
            tm = np.array(tm)
        om = decide(clf.proba(feat(measure(bm, lvl, T, rng)[col])))
        det[n] = {it: (float(np.mean(om[tm == it] >= 1)), float(np.mean(om[tm == it] == 2))) for it in LI_ITEMS}
    d0 = np.array([det[0][i][0] for i in LI_ITEMS])
    pm = []
    for n in range(4):
        dn = np.array([det[n][i][0] for i in LI_ITEMS])
        pm.append(float(max(0.0, 1 - (wli * dn).sum() / max(1e-9, (wli * d0).sum()))))
    res["p_miss_li_given_n_metal"] = pm
    res["det_per_item_by_n"] = {str(n): det[n] for n in range(4)}
    # energiegewogen recall in realistische zak
    wpak = np.array([ITEMS[i]["mean"] * ITEMS[i]["wh"][1] for i in PACK_ITEMS])
    res["recall_pakket_items_in_bag"] = float(sum(ITEMS[i]["mean"] * ITEMS[i]["wh"][1] * res["p_out_given_item_in_bag"][i][2] for i in PACK_ITEMS) / wpak.sum())
    res["recall_any_li_energy_in_bag"] = float((wli * np.array([1 - res["p_out_given_item_in_bag"][i][0] for i in LI_ITEMS])).sum() / wli.sum())
    res["_clf"] = clf; res["_decide"] = decide
    if verbose:
        print(f"{name} lvl{lvl} T={T}: recall pakket(in zak)={res['recall_pakket_items_in_bag']:.2f}, "
              f"Li-energie≥cel={res['recall_any_li_energy_in_bag']:.2f}, vals≥cel/zak={1-res['clutter_bag']['p_out'][0]:.3f}  ({time.time()-T0:.0f}s)")
    return res


def auc(a, b):
    """AUC dat score a > score b."""
    s = np.r_[a, b]; r = s.argsort().argsort() + 1
    return float((r[:len(a)].sum() - len(a) * (len(a) + 1) / 2) / (len(a) * len(b)))


def fisher(Xa, Xb):
    m = Xa.mean(0) - Xb.mean(0); S = np.cov(Xa.T) + np.cov(Xb.T) + 1e-6 * np.eye(Xa.shape[1])
    w = np.linalg.solve(S, m)
    return float(w @ m), w


# ================================================================= MAIN
if __name__ == "__main__":
    out = {}
    # ---------- fig_spectra + fig_decay (canonieke objecten, oriëntatie-gemiddeld = trace/3, positie centrum)
    canon = ["cel_18650", "alkaline", "telefoon", "vape", "powerbank", "laptop_gereedschap", "blik", "folie",
             "sleutel_klein_metaal", "pan_gereedschap", "elektronica_zonder_accu"]
    rng = np.random.default_rng(7)
    f = np.logspace(2.5, 5.3, 200); t = np.logspace(-5.3, -2.5, 200)
    fig, ax = plt.subplots(1, 2, figsize=(13, 5)); fig2, ax2 = plt.subplots(figsize=(7, 5))
    cmap = plt.get_cmap("tab20")
    for i, it in enumerate(canon):
        kind, D, tau, wh = draw_obj(it, rng)
        p = D.mean(1)
        z = np.array([vlf(kind, p, tau, ff).sum() for ff in f])
        g = np.array([pi_g(kind, p, tau, tt).sum() for tt in t])
        ls = "-" if ITEMS[it]["li"] else "--"
        ax[0].semilogx(f, z.real, ls, color=cmap(i), label=it); ax[1].semilogx(f, -z.imag, ls, color=cmap(i))
        ax2.loglog(t * 1e6, np.abs(g), ls, color=cmap(i), label=it)
    ax[0].set(xlabel="f [Hz]", ylabel="Re α [cm³] (+ = ferro)", title="VLF in-fase (I)"); ax[0].set_yscale("symlog", linthresh=1)
    ax[1].set(xlabel="f [Hz]", ylabel="−Im α [cm³]", title="VLF kwadratuur (Q)"); ax[1].set_yscale("symlog", linthresh=1)
    for fq in FREQS: ax[0].axvline(fq, color="grey", lw=0.5); ax[1].axvline(fq, color="grey", lw=0.5)
    ax[0].legend(fontsize=7); fig.suptitle("Polariseerbaarheidsspectra (oriëntatie-gemiddeld, 1 trekking per klasse; doorgetrokken = Li)")
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_spectra.png"), dpi=120)
    for gt in GATES: ax2.axvline(gt * 1e6, color="grey", lw=0.5)
    ax2.set(xlabel="t na uitschakelen [µs]", ylabel="|g(t)| [cm³-eq]", title="PI-vervalcurven (K2), grijze lijnen = vensters", ylim=(1e-3, 1e5))
    ax2.legend(fontsize=7); fig2.tight_layout(); fig2.savefig(os.path.join(HERE, "fig_decay.png"), dpi=120)

    # ---------- positie-effect + meettijd
    rng = np.random.default_rng(8)
    Nn = 4000
    P = np.column_stack([rng.uniform(*BOX[a], Nn) for a in "xyz"])
    hT, hB = fields(P)
    resp = np.sum(hT ** 2, 1)  # isotroop object: respons ∝ |h|^2
    out["positie_spreiding"] = {"p01": float(np.percentile(resp, 1)), "p50": float(np.median(resp)), "p99": float(np.percentile(resp, 99)),
                                "ratio_p99_p01": float(np.percentile(resp, 99) / np.percentile(resp, 1))}
    resp2 = np.sqrt(np.sum(hT ** 2, 1) * np.sum(hB ** 2, 1))
    est = np.sqrt(resp / resp2)  # demo: verhouding T/B geeft diepte -> correctiefactor
    Ts = np.logspace(-2, 1.5, 60)
    cell_M = 37.0  # cm3, oriëntatie-gemiddelde 18650 ferro-respons (zie objects)
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    for lvl, nm in enumerate(["laag", "basis", "hoog"]):
        for q, ls in [(50, "-"), (5, ":")]:
            r = np.percentile(resp, q)
            ax[0].loglog(Ts, cell_M * r / sigma_tot(Ts, lvl), ls, color=["g", "b", "r"][lvl], label=f"ruis {nm}, positie P{q}")
    ax[0].loglog(Ts, cell_M * np.percentile(resp, 5) / sigma_tot(Ts, 1, bg=False), "k--", label="basis zonder trommel-rest (ideaal)")
    ax[0].axhline(5, color="grey", lw=0.8); ax[0].set(xlabel="meettijd T [s]", ylabel="SNR 18650", title="SNR vs meettijd (√N tot drift/achtergrond-vloer)")
    ax[0].legend(fontsize=7)
    im = ax[1].hist(np.log10(resp), 60, color="tab:blue"); ax[1].set(xlabel="log10 relatieve respons (1 = lusmidden)", ylabel="aantal", title=f"Positie-effect in 40×40×40 cm: P99/P1 = {out['positie_spreiding']['ratio_p99_p01']:.0f}×")
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_meettijd.png"), dpi=120)
    out["meettijd"] = {nm: {"SNR_P5_T0.1": float(cell_M * np.percentile(resp, 5) / sigma_tot(0.1, l)), "SNR_P5_T2": float(cell_M * np.percentile(resp, 5) / sigma_tot(2, l)),
                            "SNR_P5_T10": float(cell_M * np.percentile(resp, 5) / sigma_tot(10, l)),
                            "T_95pct_vloer_s": float(Ts[np.argmax(sigma_tot(Ts, l) < 1.05 * sigma_tot(1e3, l))])} for l, nm in enumerate(["laag", "basis", "hoog"])}

    # ---------- concepten basis + gevoeligheid
    R = {}
    for name in ["K1", "K2"]:
        R[name] = {lvl: run_concept(name, lvl, n_train=(2500 if lvl == 1 else 1200), n_eval=(600 if lvl == 1 else 300)) for lvl in (1, 0, 2)}
    for name in ["K1", "K2"]:
        rr = run_concept(name, 3, n_train=1200, n_eval=300)
        out[name + "_ideaal_ruisloos"] = {k: v for k, v in rr.items() if not k.startswith("_")}
    for name in ["K1", "K2"]:
        out[name] = {nm: {k: v for k, v in R[name][l].items() if not k.startswith("_")} for l, nm in [(0, "laag"), (1, "basis"), (2, "hoog")]}

    # ---------- feature-space + scheidbaarheid (alleen-object, basis ruis)
    rng = np.random.default_rng(9)
    pairs = {}
    nS = 1500
    data = {}
    for it in ["cel_18650", "alkaline", "telefoon", "sleutel_klein_metaal", "powerbank", "pan_gereedschap", "blik", "vape", "folie"]:
        F1, F2 = measure([[it]] * nS, 1, T_MEAS, rng)
        data[it] = (feat(F1), feat(F2), F1, F2)
    for a, b in [("cel_18650", "alkaline"), ("telefoon", "sleutel_klein_metaal"), ("powerbank", "pan_gereedschap"), ("vape", "blik"), ("vape", "folie")]:
        fa1, wa1 = fisher(data[a][0], data[b][0]); fa2, wa2 = fisher(data[a][1], data[b][1])
        pairs[f"{a}_vs_{b}"] = {"K1_fisher_J": fa1, "K1_AUC_LDA": auc(data[a][0] @ wa1, data[b][0] @ wa1),
                                "K2_fisher_J": fa2, "K2_AUC_LDA": auc(data[a][1] @ wa2, data[b][1] @ wa2)}
    out["scheidbaarheid_alleen"] = pairs
    # schaal-invariant kenmerk K2: verval-helling en ferro-verhouding
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    for i, it in enumerate(data):
        F1, F2 = data[it][2], data[it][3]
        ph = np.degrees(np.arctan2(-F1[:, 3], F1[:, 2]))       # fase bij 15 kHz (Q/I)
        amp = np.log10(np.abs(F1[:, 2] + 1j * F1[:, 3]) + 1e-3)
        ax[0].scatter(ph, amp, s=3, alpha=0.35, color=cmap(i), label=it)
        g = np.abs(F2[:, :5]) + 0.05
        slope = np.log10(g[:, 3] / g[:, 1])
        ferro = np.arcsinh(F2[:, 15] / (g[:, 0] + 1))
        ax[1].scatter(slope, ferro, s=3, alpha=0.35, color=cmap(i), label=it)
    ax[0].set(xlabel="fase 15 kHz [°] (I>0 = ferro)", ylabel="log10 |α| meting [cm³]", title="K1: fase vs amplitude (alleen-object, basisruis)")
    ax[1].set(xlabel="log10 g(270µs)/g(30µs) (verval-helling)", ylabel="asinh(ferro / g(10µs))", title="K2: schaal-invariante kenmerken")
    ax[0].legend(markerscale=4, fontsize=7); fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_feature_space.png"), dpi=120)

    # ---------- ROC Li vs geen in realistische zak, K1 vs K2
    fig, ax = plt.subplots(figsize=(6, 5))
    for name, colr in [("K1", "tab:orange"), ("K2", "tab:blue")]:
        clf = R[name][1]["_clf"]; c = 0 if name == "K1" else 1
        rng = np.random.default_rng(11)
        bp = [[it] + draw_clutter_counts(rng) for it in PACK_ITEMS for _ in range(500)]
        bn = [draw_clutter_counts(rng) for _ in range(6000)]
        bl = [[it] + draw_clutter_counts(rng) for it in ["cel_18650", "telefoon", "vape"] for _ in range(500)]
        sp = clf.proba(feat(measure(bp, 1, T_MEAS, rng)[c]))[:, 2]; sn = clf.proba(feat(measure(bn, 1, T_MEAS, rng)[c]))
        sl = clf.proba(feat(measure(bl, 1, T_MEAS, rng)[c]))
        th = np.unique(np.r_[sn[:, 2], 2])
        ax.plot([np.mean(sn[:, 2] >= x) for x in th], [np.mean(sp >= x) for x in th], color=colr, label=f"{name} pakket vs clutter (AUC {auc(sp, sn[:,2]):.2f})")
        sll = sl[:, 1] + sl[:, 2]; snl = sn[:, 1] + sn[:, 2]; th = np.unique(np.r_[snl, 2])
        ax.plot([np.mean(snl >= x) for x in th], [np.mean(sll >= x) for x in th], "--", color=colr, label=f"{name} 18650/telefoon/vape vs clutter (AUC {auc(sll, snl):.2f})")
        out.setdefault("AUC_in_zak", {})[name] = {"pakket": auc(sp, sn[:, 2]), "cel_tel_vape": auc(sll, snl)}
    ax.plot([0, 1], [0, 1], "k:", lw=0.6); ax.set_xscale("log"); ax.set_xlim(1e-3, 1)
    ax.set(xlabel="vals-positief per zak (clutter zonder Li)", ylabel="recall", title="ROC in realistische zak (basisruis, T=2 s)")
    ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_roc.png"), dpi=120)

    # ---------- Wh-schatting K2 (lineaire regressie log Wh op features), Li-items
    rng = np.random.default_rng(12)
    for mode in ["alleen", "zak"]:
        bags, whs = [], []
        for it in ["cel_18650", "telefoon", "powerbank", "laptop_gereedschap"]:
            for _ in range(800):
                rr = np.random.default_rng(rng.integers(1 << 31))
                wh = tri(rr, *ITEMS[it]["wh"]); whs.append(wh)
                bags.append([(it, wh)] + (draw_clutter_counts(rng) if mode == "zak" else []))
        # meet met dezelfde wh: hertrek via vaste seed is complex -> benadering: gebruik item-mediane Wh-spreiding
        X = feat(measure(bags, 1, T_MEAS, rng)[1]); y = np.log(np.array(whs))
        Xa = np.c_[X, np.ones(len(X))]; n2 = len(X) // 2; perm = rng.permutation(len(X))
        tr, te = perm[:n2], perm[n2:]
        coef, *_ = np.linalg.lstsq(Xa[tr], y[tr], rcond=None)
        out.setdefault("Wh_schatting_K2", {})[mode] = {"sigma_ln": float(np.std(Xa[te] @ coef - y[te])), "sigma_log10": float(np.std(Xa[te] @ coef - y[te]) / np.log(10)), "note": "lineaire regressie ln(Wh) op K2-features; 18650/telefoon/powerbank/laptop-gereedschap"}

    # ---------- JSON voor A6
    for name in ["K1", "K2"]:
        b = R[name][1]
        js = {"concept": name,
              "classes": params.OUT_CLASSES,
              "p_out_given_item": b["p_out_given_item"],
              "clutter": {"model": "independent_or",
                          "note": "p_out_given_item = object alléén in zak. Realistischer: gebruik clutter_bag.p_out (valse uitvoer per Li-loze zak met realistische metaalinhoud, superpositie gesimuleerd) en p_out_given_item_in_bag (Li-item + realistische clutter)."},
              "masking": {"p_miss_li_given_n_metal": b["p_miss_li_given_n_metal"],
                          "definitie": "P(detectie>=cel | Li + n metaalobjecten) = P(detectie | alleen) * (1 - p_miss[n]); energiegewogen over Li-items; index 3 = 3+ (realistische zakken met >=3 metaalobjecten)"},
              "clutter_bag": b["clutter_bag"],
              "p_out_given_item_in_bag": b["p_out_given_item_in_bag"],
              "operating_point": {"vals_pakket_per_clutterzak": 0.002, "vals_cel_of_pakket_per_clutterzak": 0.02, "meettijd_s": T_MEAS, "ruisniveau": "basis"},
              "gevoeligheid": {nm: {"recall_pakket_items_in_bag": R[name][l]["recall_pakket_items_in_bag"],
                                    "recall_any_li_energy_in_bag": R[name][l]["recall_any_li_energy_in_bag"]} for l, nm in [(0, "laag"), (1, "basis"), (2, "hoog")]},
              "basis": ("A2 R3 simulatie experiments/r3_inductie/sim_inductie.py: dipool-polariseerbaarheid per object (multi-exponentiële eddy-modes + ferro-term), "
                        "Biot-Savart 40x40 cm lus(sen), willekeurige positie/oriëntatie, superpositie clutter uit params.ITEMS, ruis+RVS-trommelrest [A], kNN-classifier. "
                        + ("K1 = 1 lus, VLF 5/15/40 kHz I/Q." if name == "K1" else "K2 = 2 lussen (opening+bodem), PI 5 vensters x 3 kanalen + ferro-kanaal 1 kHz.")
                        + " Pakket = powerbank, laptop/gereedschap, e-bike (PACK_WHEQ=20, Orchestrator).")}
        with open(os.path.join(HERE, f"sensor_model_{name}.json"), "w") as fh:
            json.dump(js, fh, indent=1)
    with open(os.path.join(HERE, "resultaten.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    print(json.dumps({k: out[k] for k in ["positie_spreiding", "meettijd", "scheidbaarheid_alleen", "AUC_in_zak", "Wh_schatting_K2"]}, indent=1))
    print(f"klaar in {time.time()-T0:.0f}s")
