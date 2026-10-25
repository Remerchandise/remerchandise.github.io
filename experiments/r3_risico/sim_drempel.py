"""A1 R3 – gevoeligheidsanalyse drempels (bovengrens: sensor ziet alleen Li-items, geen clutter).

Draait vanuit repo-root: python3 experiments/r3_risico/sim_drempel.py
Output: fig_risico_vs_drempel.png, fig_pareto.png, fig_brandkans_container.png, resultaten.json
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import risk  # noqa: E402
from risk import ITEMS, params  # noqa: E402

SEED = 20261025
N_EMPT = 40_000          # ledigingen per scenario
BAGS = 100               # zakken (= inworpen) per lediging [A] params basis
LI = [c for c, it in ITEMS.items() if it["li"]]
SIGMAS = [0.0, 0.3, 0.5, 1.0]
T_THROW = np.array([5, 7.5, 10, 15, 20, 30, 50, 75, 100])
T_CONT = np.array([20, 30, 50, 75, 100, 150, 200, 300])


def tri(rng, lo, mid, hi, n):
    if hi <= lo:
        return np.full(n, mid, float)
    return rng.triangular(lo, mid, hi, n)


def simulate(scale, rng):
    """Trek Li-items: return arrays (emptying_idx, bag_idx, cls_idx, wheq)."""
    E, B, C, W = [], [], [], []
    for ci, c in enumerate(LI):
        it = ITEMS[c]
        n = rng.poisson(it["mean"] * scale * BAGS, N_EMPT)
        tot = n.sum()
        E.append(np.repeat(np.arange(N_EMPT), n))
        B.append(rng.integers(0, BAGS, tot))
        C.append(np.full(tot, ci))
        wh = tri(rng, *it["wh"], tot)
        W.append(wh * it["w_chem"] * it["w_state"])
    return (np.concatenate(E), np.concatenate(B), np.concatenate(C), np.concatenate(W))


def analyse(sim, sigma, rng):
    e, b, c, w = sim
    est = w * (np.exp(rng.normal(0, sigma, w.size)) if sigma > 0 else 1.0)
    key = e * BAGS + b
    uk, inv = np.unique(key, return_inverse=True)
    bag_true = np.bincount(inv, weights=w)
    bag_est = np.bincount(inv, weights=est)
    bag_emp = uk // BAGS
    cont_true = np.bincount(e, weights=w, minlength=N_EMPT)
    cont_est = np.bincount(e, weights=est, minlength=N_EMPT)
    tot = w.sum()
    out = {"throw": [], "cont": []}
    for t in T_THROW:
        f = bag_est >= t
        rec = bag_true[f].sum() / tot
        alarms_emp = np.unique(bag_emp[f]).size / N_EMPT * 1000     # ledigingen met >=1 melding
        throws = f.sum() / N_EMPT * 1000                             # meldingen (inworpen) per 1000 ledigingen
        out["throw"].append(dict(T=float(t), recall=float(rec), alarms_per_1000=float(throws),
                                 containers_flagged_per_1000=float(alarms_emp)))
    for t in T_CONT:
        f = cont_est >= t
        out["cont"].append(dict(T=float(t), recall=float(cont_true[f].sum() / tot),
                                alarms_per_1000=float(f.sum() / N_EMPT * 1000)))
    return out, cont_true


def main():
    rng = np.random.default_rng(SEED)
    res = {"meta": dict(seed=SEED, n_emptyings=N_EMPT, bags=BAGS,
                        note="Bovengrens: alleen Li-items, perfecte detectie; sigma = lognormale Wh-schattingsfout per item")}
    sims = {}
    for sc, scale in params.SCENARIOS.items():
        sims[sc] = simulate(scale, rng)
        res[sc] = {}
        for s in SIGMAS:
            res[sc][f"sigma_{s}"], ct = analyse(sims[sc], s, rng)
        # brandkans per container (verdeling)
        res[sc]["wheq_per_emptying"] = dict(mean=float(ct.mean()), p50=float(np.median(ct)),
                                            p90=float(np.percentile(ct, 90)), p99=float(np.percentile(ct, 99)),
                                            share_ge1_li=float((np.bincount(sims[sc][0], minlength=N_EMPT) > 0).mean()))
        res[sc]["P_fire_per_emptying_mean"] = {k: float(risk.p_fire_from_wheq(ct, k).mean()) for k in ("laag", "basis", "hoog")}
        res[sc]["fires_per_1000_containers_yr_paramsK"] = {k: float(v * 52 * 1000) for k, v in res[sc]["P_fire_per_emptying_mean"].items()}
    res["fires_per_1000_calibrated"] = {c: risk.expected_fires_per_1000(c) for c in ("laag", "basis", "hoog")}

    # ---- fig_risico_vs_drempel
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    cols = {0.0: "#1f4e79", 0.3: "#2e86c1", 0.5: "#e67e22", 1.0: "#c0392b"}
    for s in SIGMAS:
        d = res["basis"][f"sigma_{s}"]
        ax[0].plot([x["alarms_per_1000"] for x in d["throw"]], [x["recall"] for x in d["throw"]], "o-", c=cols[s], label=f"σ={s}")
        for x in d["throw"]:
            if s == 0.0:
                ax[0].annotate(f'{x["T"]:g}', (x["alarms_per_1000"], x["recall"]), fontsize=7, xytext=(3, 3), textcoords="offset points")
        d2 = d["cont"]
        ax[1].plot([x["alarms_per_1000"] for x in d2], [x["recall"] for x in d2], "o-", c=cols[s], label=f"σ={s}")
        if s == 0.0:
            for x in d2:
                ax[1].annotate(f'{x["T"]:g}', (x["alarms_per_1000"], x["recall"]), fontsize=7, xytext=(3, 3), textcoords="offset points")
    ax[0].set(xscale="log", xlabel="meldingen (inworpen ≥ T) per 1.000 ledigingen", ylabel="energiegewogen recall",
              title="Per inworp, T = 5–100 Wh-eq (basis)")
    ax[1].set(xscale="log", xlabel="containers ≥ T per 1.000 ledigingen", ylabel="energiegewogen recall",
              title="Per container, T = 20–300 Wh-eq (basis)")
    for a in ax:
        a.grid(alpha=.3); a.legend(); a.set_ylim(0, 1)
    fig.suptitle("Bovengrens recall vs alarmlast (perfecte Li-sensor, alleen Wh-fout σ)", fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_risico_vs_drempel.png"), dpi=130); plt.close(fig)

    # ---- fig_pareto
    e, b, c, w = sims["basis"]
    order = np.argsort(-w)
    cumw = np.cumsum(w[order]) / w.sum()
    cumn = np.arange(1, w.size + 1) / w.size
    share_w = np.array([w[c == i].sum() for i in range(len(LI))]) / w.sum()
    share_n = np.array([(c == i).sum() for i in range(len(LI))]) / w.size
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    ax[0].plot(cumn, cumw, c="#1f4e79"); ax[0].plot([0, 1], [0, 1], "--", c="grey", lw=.8)
    for q in (0.05, 0.10, 0.20):
        ax[0].axvline(q, c="grey", lw=.5); ax[0].annotate(f"{q:.0%} → {np.interp(q, cumn, cumw):.0%}", (q, np.interp(q, cumn, cumw)), fontsize=8, xytext=(4, -12), textcoords="offset points")
    ax[0].set(xlabel="aandeel Li-items (gesorteerd op Wh-eq)", ylabel="aandeel risico (Wh-eq)", title="Pareto Li-items (basis)"); ax[0].grid(alpha=.3)
    x = np.arange(len(LI))
    ax[1].bar(x - .2, share_n, .4, label="aandeel items", color="#95a5a6")
    ax[1].bar(x + .2, share_w, .4, label="aandeel Wh-eq (risico)", color="#c0392b")
    ax[1].set_xticks(x, LI, rotation=35, ha="right", fontsize=8); ax[1].legend(); ax[1].set_title("Per itemklasse")
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_pareto.png"), dpi=130); plt.close(fig)
    res["pareto_basis"] = {LI[i]: dict(share_items=float(share_n[i]), share_wheq=float(share_w[i])) for i in range(len(LI))}
    res["pareto_basis"]["_top10pct_items_share_wheq"] = float(np.interp(0.10, cumn, cumw))
    big = np.isin(c, [LI.index(k) for k in ("powerbank", "laptop_gereedschap", "ebike_step")])
    res["pareto_basis"]["_ge_powerbank_share_items"] = float(big.mean())
    res["pareto_basis"]["_ge_powerbank_share_wheq"] = float(w[big].sum() / w.sum())
    pk = w >= params.PACK_WHEQ
    res["pareto_basis"]["_ge50wheq_share_items"] = float(pk.mean())
    res["pareto_basis"]["_ge50wheq_share_wheq"] = float(w[pk].sum() / w.sum())

    # ---- fig_brandkans_container: P_brand vs Wh-eq en containerverdeling
    r = np.logspace(0, 3, 200)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for k, col in zip(("laag", "basis", "hoog"), ("#27ae60", "#2e86c1", "#c0392b")):
        ax.loglog(r, risk.p_fire_from_wheq(r, k), c=col, label=f"k {k} = {params.K_PER_WHEQ[k]:.1e}")
    for t, lab in ((50, "oranje"), (150, "rood")):
        ax.axvline(t, ls="--", c="grey"); ax.text(t * 1.05, 2e-7, lab, fontsize=8)
    ax.axvline(res["basis"]["wheq_per_emptying"]["mean"], c="k", lw=.8); ax.text(res["basis"]["wheq_per_emptying"]["mean"] * 1.05, 1e-3, "gem. lediging", fontsize=8)
    ax.set(xlabel="Wh-eq in container (sinds lediging)", ylabel="P_brand per ketenpassage", title="Brandkans per container = 1 − exp(−k·ΣWh-eq)")
    ax.grid(alpha=.3, which="both"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_brandkans_container.png"), dpi=130); plt.close(fig)

    with open(os.path.join(HERE, "resultaten.json"), "w") as f:
        json.dump(res, f, indent=1)
    # korte console-samenvatting
    for sc in params.SCENARIOS:
        print(sc, res[sc]["wheq_per_emptying"], res[sc]["fires_per_1000_containers_yr_paramsK"])
    print("calibrated", res["fires_per_1000_calibrated"])
    print("pareto", {k: v for k, v in res["pareto_basis"].items() if k.startswith("_")})
    for s in SIGMAS:
        print("sigma", s)
        for x in res["basis"][f"sigma_{s}"]["throw"]:
            print("  throw", x)
        for x in res["basis"][f"sigma_{s}"]["cont"]:
            print("  cont ", x)


if __name__ == "__main__":
    main()
