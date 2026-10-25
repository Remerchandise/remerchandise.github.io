#!/usr/bin/env python3
"""A6 – Classificatie-Monte-Carlo (Ronde 3).

Draaien vanuit repo-root:  python3 experiments/r3_classificatie/mc.py [--n 20000] [--fast]

Keten: zakinhoud (params.ITEMS, scenario) -> sensormodel per concept (sensor_model_K*.json)
-> zak-output {geen, cel, pakket} -> Bayes-score per container (posterior E[Wh-eq | output],
gekalibreerd op een aparte kalibratierun) -> beslisregel (A1-drempels of rangorde-budget)
-> recall (aantal, energie, risico), vals-alarmratio, PPV, meldingen per wagen, vermeden branden.

Sensormodellen worden gezocht in deze volgorde (FASE 2 = echte modellen neerzetten, verder niets):
  experiments/r3_inductie/sensor_model_K1.json, sensor_model_K2.json
  experiments/r3_rontgen/sensor_model_K3.json
  experiments/r3_thermisch/event_model_K4.json  (+ event_model_B1.json of "B1"-blok erin)
  anders: experiments/r3_classificatie/placeholders/*.json   (gemarkeerd [A] in de output)
Brandkans: experiments/r3_risico/risk.py als die `p_fire_wheq(wheq, k)` of `p_fire(items)` levert,
anders eigen implementatie 1 - exp(-k * sum(Wh-eq)) (params.K_PER_WHEQ).
"""
import argparse, json, os, sys, csv
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "experiments", "common"))
import params as P  # noqa: E402

ITEM_NAMES = list(P.ITEMS.keys())
NI = len(ITEM_NAMES)
IS_LI = np.array([P.ITEMS[n]["li"] for n in ITEM_NAMES])
IS_METAL_NONLI = np.array([(P.ITEMS[n]["metal"] != "none") and not P.ITEMS[n]["li"] for n in ITEM_NAMES])
WHEQ_FACTOR = np.array([P.ITEMS[n]["w_chem"] * P.ITEMS[n]["w_state"] for n in ITEM_NAMES])

# ---- operationele aannames [A] -------------------------------------------------------
OPS = {
    "containers_per_truck_day": 125,     # [A] A8: 100-150
    "truck_days_per_week": 5,
    "budget_oranje_per_truck_day": 2.5,  # [A] checklist B2: <= 2-3 actiegerichte meldingen/wagen/dag
    "budget_rood_per_truck_week": 1.0,   # [A] R2: <= 1 rood per wagen per week
    "eff_oranje": 0.3,                   # [A] laatste van de route / niet extra persen
    "eff_rood": 0.8,                     # [A] apart legen, niet persen
    "latent_gamma_shape": 2.0,           # [A] spreiding tussen containers (buurten): CV = 0.71
    "b0_score_noise_sigma": 0.7,         # [A] lognormale ruis op risicokaart (steekproefsortering)
    "bags_per_emptying": P.CONTAINER["bags_per_emptying"][1],
}
SCEN_INDEX = {"laag": 0, "basis": 1, "hoog": 2}
# A1-drempels R3 (Orchestrator-bericht 2026-10-25; params.THRESH_* nog op R1-waarden)
A1_R3 = {"throw_oranje": 50, "throw_rood": 75, "cont_oranje": 75, "cont_rood": 150}


# ---- modellen laden -------------------------------------------------------------------
def _first(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def load_sensor(concept):
    real = {"K1": "r3_inductie", "K2": "r3_inductie", "K3": "r3_rontgen"}[concept]
    p = _first([os.path.join(ROOT, "experiments", real, f"sensor_model_{concept}.json"),
                os.path.join(HERE, "placeholders", f"sensor_model_{concept}.json")])
    m = json.load(open(p))
    placeholder = "placeholders" in p
    pm = np.zeros((NI, 3))
    for i, n in enumerate(ITEM_NAMES):
        v = m["p_out_given_item"].get(n)
        if v is None:  # ontbrekende klasse: metaal-loos = geen, anders conservatief als 'blik'
            v = [1, 0, 0] if P.ITEMS[n]["metal"] == "none" else m["p_out_given_item"].get("blik", [1, 0, 0])
        v = np.asarray(v, float)
        pm[i] = v / v.sum()
    mask = np.asarray(m.get("masking", {}).get("p_miss_li_given_n_metal", [0, 0, 0, 0]), float)
    return dict(concept=concept, p=pm, mask=mask, path=os.path.relpath(p, ROOT), placeholder=placeholder)


def load_event(name):
    p = _first([os.path.join(ROOT, "experiments", "r3_thermisch", f"event_model_{name}.json"),
                os.path.join(HERE, "placeholders", f"event_model_{name}.json")])
    m = json.load(open(p))
    if name == "B1" and "B1" in m:
        m = m["B1"]
    m["_path"] = os.path.relpath(p, ROOT)
    m["_placeholder"] = "placeholders" in p
    return m


def load_risk():
    rp = os.path.join(ROOT, "experiments", "r3_risico", "risk.py")
    if os.path.exists(rp):
        sys.path.insert(0, os.path.dirname(rp))
        try:
            import risk  # noqa
            for fn in ("p_fire_from_wheq", "p_fire_wheq"):
                if hasattr(risk, fn):
                    f = getattr(risk, fn)
                    return (lambda wheq, k, f=f: np.asarray(f(wheq, k), float)), f"A1 risk.{fn} (experiments/r3_risico/risk.py)"
        except Exception as e:  # pragma: no cover
            print("risk.py niet bruikbaar:", e)
    return (lambda wheq, k: -np.expm1(-k * wheq)), "eigen: 1-exp(-k*Wh-eq) (params.K_PER_WHEQ)"


# ---- zakken trekken -------------------------------------------------------------------
def sample_bags(rng, n_cont, n_bags, scen):
    """Return counts (n_cont*n_bags, NI) int16, wheq per zak, n_metal per zak, container-id."""
    s = P.SCENARIOS[scen]
    nb = n_cont * n_bags
    latent = rng.gamma(OPS["latent_gamma_shape"], 1 / OPS["latent_gamma_shape"], n_cont)
    lat_b = np.repeat(latent, n_bags)
    counts = np.zeros((nb, NI), np.int16)
    wheq = np.zeros(nb)
    si = SCEN_INDEX[scen]
    for i, n in enumerate(ITEM_NAMES):
        it = P.ITEMS[n]
        mu = it["mean"] * (s * lat_b if it["li"] else np.ones(nb))
        if it["dist"][0] == "nb":
            r = it["dist"][1]
            lam = rng.gamma(r, mu / r, nb)  # NB als gamma-Poisson-mengsel
            c = rng.poisson(lam)
        else:
            c = rng.poisson(mu, nb)
        counts[:, i] = c
        if WHEQ_FACTOR[i] > 0:
            idx = np.nonzero(c)[0]
            if idx.size:
                reps = np.repeat(idx, c[idx])
                lo, mid, hi = it["wh"]
                # Wh per item: driehoek(laag, basis, hoog) – scenario-band als vorm
                wh = rng.triangular(lo, mid, hi, reps.size) if hi > lo else np.full(reps.size, mid)
                np.add.at(wheq, reps, wh * WHEQ_FACTOR[i])
    n_metal = (counts[:, IS_METAL_NONLI]).sum(1)
    return counts, wheq, n_metal, latent


def sensor_output(rng, counts, n_metal, model):
    """Zak-output = max over objecten (independent_or). Li-objecten krijgen extra miskans door ander metaal."""
    p = model["p"]
    F0, F1 = p[:, 0], p[:, 0] + p[:, 1]
    bucket = np.minimum(n_metal, 3)
    pm = model["mask"][bucket]  # per zak
    logP0 = np.zeros(counts.shape[0])
    logP1 = np.zeros(counts.shape[0])
    cl = lambda x: np.log(np.clip(x, 1e-15, 1.0))
    for i in range(NI):
        c = counts[:, i]
        if not c.any():
            continue
        if IS_LI[i]:
            f0 = (1 - pm) * F0[i] + pm
            f1 = (1 - pm) * F1[i] + pm
            logP0 += c * cl(f0)
            logP1 += c * cl(f1)
        else:
            logP0 += c * cl(F0[i])
            logP1 += c * cl(F1[i])
    u = rng.random(counts.shape[0])
    out = np.where(u < np.exp(logP0), 0, np.where(u < np.exp(logP1), 1, 2)).astype(np.int8)
    return out


def perfect_output(wheq):
    return np.where(wheq >= P.PACK_WHEQ, 2, np.where(wheq > 0, 1, 0)).astype(np.int8)


# ---- metrieken ------------------------------------------------------------------------
def bag_metrics(out, counts, wheq):
    li = (counts[:, IS_LI].sum(1) > 0)
    alk = counts[:, ITEM_NAMES.index("alkaline")] > 0
    pos_pack = wheq >= P.PACK_WHEQ
    flag = out >= 1
    pk = out == 2
    sd = lambda a, b: float(a.sum() / b.sum()) if b.sum() else float("nan")
    return {
        "frac_li_zak": float(li.mean()),
        "frac_flag(cel|pakket)": float(flag.mean()),
        "recall_li_zak": sd(flag & li, li),
        "ppv_li_bij_flag": sd(flag & li, flag),
        "frac_flag_met_alkaline_zonder_li": sd(flag & alk & ~li, flag),
        "frac_pakket": float(pk.mean()),
        "recall_pakket(>=PACK_WHEQ)": sd(pk & pos_pack, pos_pack),
        "ppv_pakket": sd(pk & pos_pack, pk),
        "energierecall_flag": float(wheq[flag].sum() / wheq.sum()),
    }


def calibrate_posterior(out, wheq):
    """Bayes: E[Wh-eq van zak | output-klasse] uit kalibratierun."""
    return np.array([wheq[out == k].mean() if (out == k).any() else 0.0 for k in range(3)])


def container_eval(score, cont_wheq, pfire, rule_q=None, thr=None, bagmax=None, pakket_any=None):
    """Beslisregel: rangorde (quantiles) of absolute drempels. Geeft alarm-niveau per container."""
    lvl = np.zeros(score.size, np.int8)
    if rule_q is not None:
        qo, qr = rule_q
        to = np.quantile(score, 1 - qo) if qo > 0 else np.inf
        tr = np.quantile(score, 1 - qr) if qr > 0 else np.inf
        # bij ties (bv. tellers) niet meer dan budget: strikte >, aangevuld met random tie-break
        jitter = score + 1e-9 * np.random.default_rng(1).random(score.size)
        to = np.quantile(jitter, 1 - qo) if qo > 0 else np.inf
        tr = np.quantile(jitter, 1 - qr) if qr > 0 else np.inf
        lvl[jitter >= to] = 1
        lvl[jitter >= tr] = 2
    else:  # A1-R3: container-score of hoogste inworp-score; optioneel elke 'pakket'-output = oranje
        o = score >= thr["cont_oranje"]
        r = score >= thr["cont_rood"]
        if bagmax is not None:
            o |= bagmax >= thr["throw_oranje"]
            r |= bagmax >= thr["throw_rood"]
        if pakket_any is not None:
            o |= pakket_any
        lvl[o] = 1
        lvl[r] = 2
    return lvl


def summarize(lvl, cont_wheq, pfire, eff):
    pos_o = cont_wheq >= A1_R3["cont_oranje"]
    pos_r = cont_wheq >= A1_R3["cont_rood"]
    alarm = lvl >= 1
    red = lvl == 2
    e = np.where(lvl == 2, eff[1], np.where(lvl == 1, eff[0], 0.0))
    sd = lambda a, b: float(a.sum() / b.sum()) if b.sum() else float("nan")
    cpd = OPS["containers_per_truck_day"]
    return {
        "frac_oranje+": float(alarm.mean()), "frac_rood": float(red.mean()),
        "meld_oranje+_per_wagen_dag": float(alarm.mean() * cpd),
        "meld_rood_per_wagen_week": float(red.mean() * cpd * OPS["truck_days_per_week"]),
        "meld_per_1000_ledigingen": float(alarm.mean() * 1000),
        "recall_cont>=75": sd(alarm & pos_o, pos_o), "ppv_cont>=75": sd(alarm & pos_o, alarm),
        "far_cont<75": sd(alarm & ~pos_o, ~pos_o),
        "recall_rood_cont>=150": sd(red & pos_r, pos_r), "ppv_rood_cont>=150": sd(red & pos_r, red),
        "energierecall": float(cont_wheq[alarm].sum() / cont_wheq.sum()),
        "risicorecall": float(pfire[alarm].sum() / pfire.sum()),
        "frac_branden_vermeden": float((pfire * e).sum() / pfire.sum()),
        "branden_per_1000c_jr": float(pfire.mean() * 1000 * P.CONTAINER["emptyings_per_year"]),
        "vermeden_per_1000c_jr": float((pfire * e).mean() * 1000 * P.CONTAINER["emptyings_per_year"]),
    }


# ---- hoofdrun -------------------------------------------------------------------------
def run(n_cont, seed, scenarios, outdir):
    p_fire_fn, risk_src = load_risk()
    sensors = {k: load_sensor(k) for k in ("K1", "K2", "K3")}
    ev_k4, ev_b1 = load_event("K4"), load_event("B1")
    nbag = OPS["bags_per_emptying"]
    cpd, tdw = OPS["containers_per_truck_day"], OPS["truck_days_per_week"]
    q_o = OPS["budget_oranje_per_truck_day"] / cpd
    q_r = OPS["budget_rood_per_truck_week"] / (cpd * tdw)
    eff = (OPS["eff_oranje"], OPS["eff_rood"])
    results, curves, bagres = [], {}, {}
    for scen in scenarios:
        k = P.K_PER_WHEQ[scen]
        rng = np.random.default_rng(seed + SCEN_INDEX[scen])
        # kalibratie (aparte trekking) voor posterior E[Wh-eq|output]
        cc, cw, cm, _ = sample_bags(rng, max(2000, n_cont // 5), nbag, scen)
        post = {}
        for name, sm in sensors.items():
            post[name] = calibrate_posterior(sensor_output(rng, cc, cm, sm), cw)
        post["perfect"] = calibrate_posterior(perfect_output(cw), cw)
        # evaluatie
        counts, wheq, nmet, latent = sample_bags(rng, n_cont, nbag, scen)
        cont_wheq = wheq.reshape(n_cont, nbag).sum(1)
        pfire = p_fire_fn(cont_wheq, k)
        outs = {name: sensor_output(rng, counts, nmet, sm) for name, sm in sensors.items()}
        outs["perfect"] = perfect_output(wheq)
        scores, bagmax, pakany = {}, {}, {}
        for name, o in outs.items():
            bagres[(scen, name)] = bag_metrics(o, counts, wheq)
            oc = o.reshape(n_cont, nbag)
            scores[name + "_bayes"] = post[name][oc].sum(1)
            scores[name + "_teller"] = (oc >= 1).sum(1).astype(float)
            scores[name + "_pakket"] = (oc == 2).sum(1) + 1e-3 * scores[name + "_bayes"]
            bagmax[name + "_bayes"] = (wheq.reshape(n_cont, nbag).max(1) if name == "perfect" else post[name][oc].max(1))
            pakany[name + "_bayes"] = (oc == 2).any(1)
        scores["B0_risicokaart"] = latent * np.exp(OPS["b0_score_noise_sigma"] * rng.standard_normal(n_cont))
        scores["random"] = rng.random(n_cont)
        concepts = {  # concept -> scorefunctie (zie RESULTATEN.md)
            "K1 VLF teller": "K1_teller", "K1 VLF bayes": "K1_bayes",
            "K2 pakketwachter": "K2_bayes", "K2 pakket-teller": "K2_pakket", "K3 rontgen": "K3_bayes",
            "B0 risicokaart": "B0_risicokaart", "perfect (bovengrens)": "perfect_bayes", "willekeurig": "random",
        }
        for cname, skey in concepts.items():
            sc = scores[skey]
            rules = [("budget", dict(rule_q=(q_o, q_r)))]
            if skey.endswith("bayes"):  # absolute Wh-eq-drempel alleen zinvol voor gekalibreerde Bayes-score
                rules += [("A1-R3", dict(thr=A1_R3, bagmax=bagmax[skey])),
                          ("A1-R3+pakket", dict(thr=A1_R3, bagmax=bagmax[skey], pakket_any=pakany[skey]))]
            for rule, kw in rules:
                lvl = container_eval(sc, cont_wheq, pfire, **kw)
                r = summarize(lvl, cont_wheq, pfire, eff)
                r.update(scenario=scen, concept=cname, regel=rule)
                results.append(r)
            # curve: risicorecall vs meldingen/wagen/week (rangorde)
            qs = np.logspace(-3.3, -0.3, 30)
            order = np.argsort(-(sc + 1e-9 * np.random.default_rng(2).random(n_cont)))
            cum_p = np.cumsum(pfire[order]) / pfire.sum()
            cum_e = np.cumsum(cont_wheq[order]) / cont_wheq.sum()
            idx = np.clip((qs * n_cont).astype(int) - 1, 0, n_cont - 1)
            curves[(scen, cname)] = (qs * cpd * tdw, cum_p[idx], cum_e[idx])
        # K5 = K2-rangorde + K4-eventkanaal; B1 = camera wagen; K4 alleen
        base_k2 = [r for r in results if r["scenario"] == scen and r["concept"] == "K2 pakketwachter" and r["regel"] == "budget"][0]
        fires_truck = base_k2["branden_per_1000c_jr"]
        cf = ev_k4["container_fire_rate_per_container_year"] * 1000
        k4_cont_avoided = cf * ev_k4["p_detect_container_fire"] * ev_k4["damage_reduction_if_detected"]
        k4_fa_week = ev_k4["false_alarms_per_container_year"] * cpd * tdw / 52
        b1_eq = fires_truck * ev_b1["p_detect_truck_fire"] * ev_b1["damage_reduction_if_detected"]
        for cname, extra in (("K4 deksel-event", dict(src=None)), ("K5 hybride (K2+K4)", dict(src=base_k2)),
                             ("B1 camera wagen", dict(src=None))):
            r = {kk: (float("nan") if isinstance(vv, float) else vv) for kk, vv in base_k2.items()}
            r.update(scenario=scen, concept=cname, regel="budget+event", branden_per_1000c_jr=fires_truck)
            if cname.startswith("K4"):
                r.update({"meld_rood_per_wagen_week": k4_fa_week, "vermeden_per_1000c_jr": 0.0, "frac_branden_vermeden": 0.0,
                          "containerbranden_schade_eq_vermeden_per_1000c_jr": k4_cont_avoided})
            elif cname.startswith("K5"):
                r.update({kk: base_k2[kk] for kk in base_k2 if kk not in ("concept", "regel")})
                r["meld_rood_per_wagen_week"] = base_k2["meld_rood_per_wagen_week"] + k4_fa_week
                r["containerbranden_schade_eq_vermeden_per_1000c_jr"] = k4_cont_avoided
            else:
                r.update({"meld_rood_per_wagen_week": ev_b1.get("false_alarms_per_truck_week", float("nan")),
                          "vermeden_per_1000c_jr": 0.0, "frac_branden_vermeden": 0.0,
                          "wagenbranden_schade_eq_vermeden_per_1000c_jr": b1_eq})
            r["concept"], r["scenario"] = cname, scen
            results.append(r)
    # economie per container per maand (vermeden schade-equivalent)
    ct, cc_ = P.ECON["fire_cost_truck_eur"], P.ECON["fire_cost_container_eur"]
    for r in results:
        si = SCEN_INDEX[r["scenario"]]
        eq = (np.nan_to_num(r.get("vermeden_per_1000c_jr", 0.0))
              + np.nan_to_num(r.get("wagenbranden_schade_eq_vermeden_per_1000c_jr", 0.0))) * ct[si] \
            + np.nan_to_num(r.get("containerbranden_schade_eq_vermeden_per_1000c_jr", 0.0)) * cc_[si]
        r["vermeden_schade_eur_per_container_maand"] = float(eq / 1000 / 12)
    meta = dict(n_containers=n_cont, bags=nbag, seed=seed, risk=risk_src, ops=OPS,
                sensors={k: dict(path=v["path"], placeholder=v["placeholder"]) for k, v in sensors.items()},
                events={"K4": ev_k4["_path"], "B1": ev_b1["_path"]},
                placeholder_any=any(v["placeholder"] for v in sensors.values()) or ev_k4["_placeholder"] or ev_b1["_placeholder"])
    write_outputs(outdir, results, bagres, curves, meta)
    return results, bagres, curves, meta


def write_outputs(outdir, results, bagres, curves, meta):
    os.makedirs(outdir, exist_ok=True)
    keys = ["scenario", "concept", "regel"] + sorted({k for r in results for k in r} - {"scenario", "concept", "regel"})
    with open(os.path.join(outdir, "mc_container.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in results:
            w.writerow({k: (f"{r[k]:.4g}" if isinstance(r.get(k), float) else r.get(k, "")) for k in keys})
    bk = sorted({k for v in bagres.values() for k in v})
    with open(os.path.join(outdir, "mc_inworp.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "sensor"] + bk)
        for (s, n), v in bagres.items():
            w.writerow([s, n] + [f"{v[k]:.4g}" for k in bk])
    json.dump(meta, open(os.path.join(outdir, "mc_meta.json"), "w"), indent=1)
    plot(outdir, results, bagres, curves, meta)


def plot(outdir, results, bagres, curves, meta):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, ink2, grid = "#0b0b0b", "#52514e", "#e4e3df"
    col = {"K1 VLF teller": "#2a78d6", "K1 VLF bayes": "#eb6834", "K2 pakketwachter": "#1baf7a",
           "K3 rontgen": "#eda100", "K2 pakket-teller": "#e87ba4", "B0 risicokaart": "#6250d6", "perfect (bovengrens)": "#52514e", "willekeurig": "#a9a8a2"}
    tag = "  [PLACEHOLDER-sensormodellen]" if meta["placeholder_any"] else ""
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": grid, "axes.labelcolor": ink2,
                         "xtick.color": ink2, "ytick.color": ink2, "axes.spines.top": False, "axes.spines.right": False})
    # Fig 1: risicorecall vs meldingen per wagen per week (basis)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4), sharey=True)
    for ax, which, lab in ((axes[0], 1, "risicorecall (aandeel brandkans in gemelde containers)"),
                           (axes[1], 2, "energierecall (aandeel Wh-eq)")):
        for (s, c), v in curves.items():
            if s != "basis":
                continue
            ls = "--" if c in ("perfect (bovengrens)", "willekeurig") else "-"
            ax.plot(v[0], v[which], ls, color=col[c], lw=2, label=c)
        b_o = OPS["budget_oranje_per_truck_day"] * OPS["truck_days_per_week"]
        b_r = OPS["budget_rood_per_truck_week"]
        for b, t in ((b_r, "budget rood\n1/wagen/wk"), (b_o, "budget oranje\n2,5/wagen/dag")):
            ax.axvline(b, color=ink2, lw=0.8, ls=":")
            ax.text(b * 1.08, 0.86, t, color=ink2, fontsize=7)
        ax.set_xscale("log")
        ax.set_xlabel("gemelde containers per wagen per week (rangorde)")
        ax.set_title(lab, fontsize=9, color=ink, loc="left")
        ax.grid(True, color=grid, lw=0.6)
        ax.set_ylim(0, 1)
    axes[0].set_ylabel("recall")
    axes[1].legend(frameon=False, fontsize=7, loc="upper left", bbox_to_anchor=(1.01, 1))
    fig.suptitle("Container-rangorde: recall vs alarmlast (scenario basis)" + tag, fontsize=10, color=ink, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "fig_recall_vs_meldingen.png"), dpi=150)
    plt.close(fig)
    # Fig 2: per-inworp PPV en recall (basis)
    sens = ["K1", "K2", "K3", "perfect"]
    mets = [("ppv_li_bij_flag", "PPV Li | flag"), ("recall_li_zak", "recall Li-zak"),
            ("ppv_pakket", "PPV pakket"), ("recall_pakket(>=PACK_WHEQ)", "recall pakket"), ("frac_flag(cel|pakket)", "aandeel zakken geflagd")]
    fig, ax = plt.subplots(figsize=(10, 3.6))
    x = np.arange(len(mets))
    wbar = 0.2
    cs = ["#2a78d6", "#1baf7a", "#eda100", "#52514e"]
    for j, s in enumerate(sens):
        v = [bagres[("basis", s)][m] for m, _ in mets]
        bars = ax.bar(x + (j - 1.5) * wbar, v, wbar * 0.9, color=cs[j], label=s)
        for xi, vi in zip(x + (j - 1.5) * wbar, v):
            ax.text(xi, vi + 0.01, f"{vi:.2f}", ha="center", fontsize=6, color=ink2)
    ax.set_xticks(x, [l for _, l in mets])
    ax.set_ylim(0, 1.1)
    ax.legend(frameon=False, ncol=4, fontsize=7)
    ax.grid(True, axis="y", color=grid, lw=0.6)
    ax.set_title("Per inworp (zak), scenario basis" + tag, fontsize=10, color=ink, loc="left")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "fig_inworp.png"), dpi=150)
    plt.close(fig)
    # Fig 3: vermeden schade EUR/container/maand per scenario, budgetregel
    cn = ["K1 VLF teller", "K2 pakketwachter", "K3 rontgen", "K5 hybride (K2+K4)", "B1 camera wagen", "B0 risicokaart", "perfect (bovengrens)"]
    fig, ax = plt.subplots(figsize=(10, 3.6))
    x = np.arange(len(cn))
    for j, s in enumerate(("laag", "basis", "hoog")):
        v = []
        for c in cn:
            rr = [r for r in results if r["scenario"] == s and r["concept"] == c and r["regel"].startswith("budget")]
            v.append(rr[0]["vermeden_schade_eur_per_container_maand"] if rr else 0)
        ax.bar(x + (j - 1) * 0.27, v, 0.25, color=["#a9cdf3", "#2a78d6", "#123f75"][j], label=s)
    ax.set_yscale("log")
    ax.set_xticks(x, cn, fontsize=7)
    ax.set_ylabel("EUR / container / maand")
    ax.legend(frameon=False, title="scenario", fontsize=7)
    ax.grid(True, axis="y", color=grid, lw=0.6)
    ax.set_title("Vermeden schade(-equivalent) bij budgetregel" + tag, fontsize=10, color=ink, loc="left")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "fig_vermeden_schade.png"), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=30000, help="aantal containerledigingen per scenario")
    ap.add_argument("--seed", type=int, default=20261025)
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--out", default=HERE)
    a = ap.parse_args()
    n = 3000 if a.fast else a.n
    res, bag, cur, meta = run(n, a.seed, ["laag", "basis", "hoog"], a.out)
    print("risico:", meta["risk"], "| placeholders:", meta["placeholder_any"])
    for r in res:
        if True:
            print(f'{r["scenario"]:5s} {r["concept"]:22s} {r["regel"]:12s} '
                  f'or/dag={r.get("meld_oranje+_per_wagen_dag", float("nan")):6.2f} rood/wk={r["meld_rood_per_wagen_week"]:6.2f} '
                  f'risrec={r.get("risicorecall", float("nan")):.2f} verm={r.get("frac_branden_vermeden", float("nan")):.3f} '
                  f'EUR/c/m={r["vermeden_schade_eur_per_container_maand"]:.3f}')
