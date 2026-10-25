"""Warmte- en gastransport van een falende cel door afval naar de sensoren van K4.

(a) Temperatuur op afstand r na TR-warmtepuls (18650 / powerbank / vape) en bij continu smeulen.
(b) Tijd tot ΔT >= 5 K aan het afvaloppervlak vs. diepte.
(c) Aankomsttijd gas in kopruimte: koud ventgas (diffusie) vs. warm rookgas (Darcy-pluim).
(d) Kans dat ventgas vóór TR de kopruimte bereikt (pre-TR detectie), MC over diepte en venster.
Uitvoer: fig_warmte_diffusie.png, warmte_gas_resultaten.json
"""
import os, sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model_a4 as M

RNG = np.random.default_rng(42)
F_HEAT = {"laag": 1.5, "basis": 2.5, "hoog": 4.0}   # warmte TR / elektrische Wh (incl. deel verbranding) [A]
CELLS = {"vape 2 Wh": 2.0, "18650 11 Wh": 11.0, "powerbank 37 Wh": 37.0}
SMOLDER_W = {"laag": 50.0, "basis": 200.0, "hoog": 1000.0}  # vermogen smeulnest [A]
DELAY_MEAN_H = {"laag": 72.0, "basis": 6.0, "hoog": 0.5}    # tijd inworp -> falen (hoog = snel = ondiep = gunstig voor detectie)


def depth_samples(n, delay_mean_h):
    delay_d = RNG.exponential(delay_mean_h, n) / 24.0
    return np.minimum(M.RISE_M_PER_DAY * delay_d + RNG.uniform(0, 0.15, n), 2.0)


def main():
    res = {}
    fig, axs = plt.subplots(2, 2, figsize=(11, 8.5))
    a = M.ALPHA["basis"]

    # (a) puls 18650
    t = np.logspace(1, 7, 400)
    ax = axs[0, 0]
    Q = CELLS["18650 11 Wh"] * 3600 * F_HEAT["basis"]
    for r in [0.05, 0.1, 0.2, 0.3, 0.5]:
        ax.loglog(t / 3600, np.maximum(M.dT_pulse(Q, r, t, a), 1e-3), label=f"r = {r:.2f} m")
    ax.axhline(5, color="k", ls="--", lw=0.8)
    ax.text(2e-3, 6, "detectie ΔT = 5 K", fontsize=8)
    ax.set_ylim(1e-2, 1e3)
    ax.set_xlabel("tijd na TR (h)")
    ax.set_ylabel("ΔT (K)")
    ax.set_title("(a) TR-puls 18650 (11 Wh × 2,5 = 99 kJ) in afval, α=1,5e-7")
    ax.legend(fontsize=7)
    peak = {}
    for name, wh in CELLS.items():
        Qc = wh * 3600 * F_HEAT["basis"]
        peak[name] = {}
        for r in [0.05, 0.1, 0.2, 0.3, 0.5]:
            tt = r ** 2 / (6 * a)
            peak[name][f"{r}"] = {"dTmax_K": float(M.dT_pulse(Qc, r, tt, a)), "t_peak_h": tt / 3600}
    res["puls_piek"] = peak

    # (b) tijd tot ΔT 5 K aan oppervlak vs diepte, puls en continu
    ax = axs[0, 1]
    depths = np.linspace(0.02, 1.5, 150)
    tgrid = np.logspace(0, 7.5, 3000)
    out_b = {}
    for lab, P in SMOLDER_W.items():
        tt = []
        for d in depths:
            dT = M.dT_continuous(P, d, tgrid, a)
            idx = np.argmax(dT >= 5)
            tt.append(tgrid[idx] / 3600 if dT[idx] >= 5 else np.nan)
        tt = np.array(tt)
        ax.semilogy(depths, tt, label=f"smeulen {P:.0f} W (geleiding)")
        out_b[f"smeulen_{lab}"] = {f"{d:.2f}": (None if np.isnan(x) else float(x)) for d, x in zip(depths[::15], tt[::15])}
    for name, wh in CELLS.items():
        Qc = wh * 3600 * F_HEAT["basis"]
        tt = []
        for d in depths:
            dT = M.dT_pulse(Qc, d, tgrid, a)
            idx = np.argmax(dT >= 5)
            tt.append(tgrid[idx] / 3600 if dT[idx] >= 5 else np.nan)
        ax.semilogy(depths, tt, ls=":", label=f"puls {name}")
        tt = np.array(tt)
        dmax = depths[~np.isnan(tt)].max() if np.any(~np.isnan(tt)) else 0
        out_b[f"puls_{name}_max_diepte_m"] = float(dmax)
    ax.set_xlabel("diepte cel onder afvaloppervlak (m)")
    ax.set_ylabel("tijd tot ΔT ≥ 5 K aan oppervlak (h)")
    ax.set_title("(b) Thermisch zichtbaar aan oppervlak (alleen geleiding)")
    ax.legend(fontsize=7)
    res["tijd_tot_5K_oppervlak_h"] = out_b

    # (c) gas aankomsttijd
    ax = axs[1, 0]
    for lab, D in M.D_GAS_EFF.items():
        ax.semilogy(depths, M.t_diffusion(depths, D) / 60, color="#888", ls=["--", "-", ":"][list(M.D_GAS_EFF).index(lab)],
                    label=f"koud ventgas, diffusie D={D:g}")
    for lab, k in M.PERM.items():
        v = M.darcy_velocity(k)
        ax.semilogy(depths, depths / v / 60, color="#b22222", ls=["--", "-", ":"][list(M.PERM).index(lab)],
                    label=f"warm rookgas, Darcy κ={k:g} (v={v*100:.2f} cm/s)")
    ax.axhspan(1, 10, color="#e07a1f", alpha=0.2)
    ax.text(0.05, 2, "venster venting→TR\n(1–10 min, basis)", fontsize=7)
    ax.set_xlabel("diepte (m)")
    ax.set_ylabel("aankomsttijd kopruimte (min)")
    ax.set_title("(c) Gastransport naar kopruimte")
    ax.legend(fontsize=6.5)
    res["darcy_v_cm_s"] = {lab: float(M.darcy_velocity(k) * 100) for lab, k in M.PERM.items()}

    # (d) MC pre-TR detectie (ventgas bereikt kopruimte vóór TR) en post-TR gas-detectie binnen 10/30 min
    n = 20000
    out_d = {}
    for lab in ["laag", "basis", "hoog"]:
        d = depth_samples(n, DELAY_MEAN_H[lab])
        win = RNG.lognormal(np.log(60), 1.2, n)  # latente short: mediaan 1 min [A]
        Dg = M.D_GAS_EFF[lab]
        p_pre = float(np.mean(M.t_diffusion(d, Dg) < win))
        v = M.darcy_velocity(M.PERM[lab])
        t_post = d / v
        out_d[{"laag": "pessimistisch", "basis": "basis", "hoog": "optimistisch"}[lab]] = {
            "diepte_mediaan_m": float(np.median(d)), "P_diepte_lt_0.3m": float(np.mean(d < 0.3)),
            "P_ventgas_voor_TR": p_pre,
            "P_rookgas_kopruimte_10min": float(np.mean(t_post < 600)),
            "P_rookgas_kopruimte_30min": float(np.mean(t_post < 1800)),
        }
    res["MC_detectievenster"] = out_d
    ax = axs[1, 1]
    for lab, c in zip(["laag", "basis", "hoog"], ["#1f5fa8", "#e07a1f", "#2a9d8f"]):
        d = np.sort(depth_samples(n, DELAY_MEAN_H[lab]))
        ax.plot(d, np.linspace(0, 1, n), color=c, label=f"vertraging inworp→falen gem. {DELAY_MEAN_H[lab]:g} h")
    ax.axvline(0.3, color="k", ls="--", lw=0.8)
    ax.text(0.32, 0.1, "0,3 m: grens\nIR/ventgas", fontsize=7)
    ax.set_xlabel("diepte cel bij falen (m)")
    ax.set_ylabel("cumulatieve kans")
    ax.set_title("(d) Diepte bij falen (stijging 0,28 m/dag)")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_warmte_diffusie.png"), dpi=130)
    with open(os.path.join(HERE, "warmte_gas_resultaten.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps({k: res[k] for k in ["MC_detectievenster", "darcy_v_cm_s"]}, indent=1))
    print("puls-piek 18650:", {r: round(v["dTmax_K"], 1) for r, v in peak["18650 11 Wh"].items()})
    print("max diepte puls zichtbaar (m):", {k: v for k, v in out_b.items() if "max" in k})
    print("smeulen basis tijd tot 5K (h):", out_b["smeulen_basis"])


if __name__ == "__main__":
    main()
