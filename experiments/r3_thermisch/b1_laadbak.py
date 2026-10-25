"""Benchmark B1: thermische camera boven de laadbak (Seek Thermal 'Fire Detection', pilot Goodyear AZ,
alarm bij 200 °F = 93 °C; SWANA Safety Innovation Award 2025). Detectiekans en reactietijd bij een
Li-brand in de wagen, plus kosten per container. Vergelijking met K4 (alleen containerbrand).
Uitvoer: fig_b1_laadbak.png, b1_resultaten.json
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(11)
N = 50000
SC = {  # [A] pessimistisch/basis/optimistisch -> P_det laag/basis/hoog
    "laag":  dict(view_s=(20, 120), p_vis=0.3, p_late=0.25, plume_s=(60, 300), d_plume=0.3),
    "basis": dict(view_s=(30, 300), p_vis=0.5, p_late=0.15, plume_s=(30, 180), d_plume=0.5),
    "hoog":  dict(view_s=(60, 600), p_vis=0.7, p_late=0.10, plume_s=(15, 90), d_plume=0.8),
}
COST = {"capex_eur": (3000, 5000, 8000), "install_eur": (300, 600, 1000), "opex_eur_jr": (150, 300, 500),
        "ugc_per_wagen": (800, 500, 300), "jaren": 6}
# Schade per wagenbrand (params.ECON) en reductie door 'hot load dump' [A]
DAMAGE = (10_000, 25_000, 50_000)
DUMP_REDUCTION = (0.5, 0.7, 0.85)


def simulate(p):
    # TR-vertraging na crush: 85 % snel (lognormaal mediaan 20 s), rest laat (10 min - 5 h) [A]
    late = rng.random(N) < p["p_late"]
    t_tr = np.where(late, rng.uniform(600, 5 * 3600, N), rng.lognormal(np.log(20), 1.0, N))
    view = rng.uniform(*p["view_s"], N)
    vis = rng.random(N) < p["p_vis"]
    depth = rng.uniform(0, 1.5, N)
    t_plume = rng.uniform(*p["plume_s"], N)
    # zichtbaar: direct (bovenop) of via pluim als diepte < d_plume
    t_seen = np.where(vis, t_tr + 1.0, np.where(depth < p["d_plume"], t_tr + t_plume, np.inf))
    det = t_seen <= view
    return det, np.where(det, t_seen - t_tr, np.nan)


def main():
    res = {"bronnen": ["Goodyear AZ / Seek Thermal pilot, alarm 93 °C (goodyearaz.gov, hoodline 2025-09)", "A8 checklist D3: EUR 3–8k per wagen"]}
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for lab, c in zip(SC, ["#1f5fa8", "#e07a1f", "#2a9d8f"]):
        det, lat = simulate(SC[lab])
        res[lab] = {"P_det": float(det.mean()), "reactietijd_mediaan_s": float(np.nanmedian(lat)), "reactietijd_p90_s": float(np.nanpercentile(lat, 90))}
        x = np.sort(lat[~np.isnan(lat)])
        ax[0].plot(x, np.linspace(0, det.mean(), len(x)), color=c, label=f"{lab}: P_det={det.mean():.2f}")
    ax[0].set_xscale("log"); ax[0].set_xlabel("reactietijd na TR (s)"); ax[0].set_ylabel("cumulatieve P(detectie)")
    ax[0].set_title("B1: thermische camera laadbak"); ax[0].legend(fontsize=8)
    # kosten per container per maand
    cpm = []
    for i in range(3):
        tot = COST["capex_eur"][i] + COST["install_eur"][i] + COST["opex_eur_jr"][i] * COST["jaren"]
        cpm.append(tot / COST["jaren"] / 12 / COST["ugc_per_wagen"][i])
    res["kosten_eur_per_container_maand_l_b_h"] = cpm
    # vermeden schade per wagenbrand
    av = [res[l]["P_det"] * DAMAGE[i] * DUMP_REDUCTION[i] for i, l in enumerate(["laag", "basis", "hoog"])]
    res["vermeden_schade_per_wagenbrand_eur_l_b_h"] = av
    # K4-vergelijking: waarde containerbrand (alle oorzaken) per container per maand
    lam_all = np.array([2e-4, 5e-4, 1e-3]) * 5
    cost_cont = np.array([3000, 8000, 15000])
    pdet_k4 = np.array([0.47, 1.0, 1.0])
    red = np.array([0.2, 0.4, 0.6])   # schadereductie door vroege melding containerbrand [A]
    res["K4_waarde_eur_per_container_maand_l_b_h"] = list(lam_all * cost_cont * pdet_k4 * red / 12)
    ax[1].bar([0, 1], [cpm[1], res["K4_waarde_eur_per_container_maand_l_b_h"][1]], yerr=[[cpm[1] - cpm[0], res["K4_waarde_eur_per_container_maand_l_b_h"][1] - res["K4_waarde_eur_per_container_maand_l_b_h"][0]],
                                                                                         [cpm[2] - cpm[1], res["K4_waarde_eur_per_container_maand_l_b_h"][2] - res["K4_waarde_eur_per_container_maand_l_b_h"][1]]],
              color=["#b22222", "#2a9d8f"], capsize=4)
    ax[1].set_xticks([0, 1]); ax[1].set_xticklabels(["B1 kosten / container", "K4 vermeden containerschade"])
    ax[1].set_ylabel("EUR per container per maand"); ax[1].set_title("Orde van grootte (basis, balk = l–h)")
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_b1_laadbak.png"), dpi=130)
    with open(os.path.join(HERE, "b1_resultaten.json"), "w") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
