"""Vals alarm door rotting/zomer en detectie van brand-events voor K4 (deksel-eventmodule:
8x8 IR + passieve elektrochemische CO-cel), Monte Carlo.

Achtergrond (per container-jaar, stap 5 min): temperatuur afvaloppervlak (seizoen, dag, zon bij
bovengrondse bak, compostwarmte, verse zakken), CO (basislijn, fermentatie-episodes incl.
H2-kruisgevoeligheid, uitlaatgas bij lediging, vuurwerk), warme as/peuken zonder brand.
Brand-events: TR van cel op diepte d (diepteverdeling uit warmte_gas.py) + smeulnest; gas via
Darcy-pluim naar kopruimte; IR-hotspot via pluim-uitlaat en opwaarts smeulfront.
Regels: A CO>50 ppm, B dCO>30 ppm/10 min, C IR-hotspot, D 2-van-3, E coïncidentie (aanbevolen).
Uitvoer: fig_valsalarm.png, event_model_K4.json
"""
import os, sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model_a4 as M

SEED = 7
DT_MIN = 5
N_STEPS = 365 * 24 * 60 // DT_MIN
N_CONT = 120            # container-jaren per scenario
REFRACT = 6 * 60 // DT_MIN

# Achtergrondscenario's (vals-alarmlast laag/basis/hoog) [A]
BG = {
    "laag":  dict(type="ondergronds", ferm_p_week=0.15, ferm_med_ppm=20, ash_per_yr=0.5, firework_p=0.15, exhaust_max=10),
    "basis": dict(type="ondergronds", ferm_p_week=0.30, ferm_med_ppm=30, ash_per_yr=2.0, firework_p=0.30, exhaust_max=25),
    "hoog":  dict(type="bovengronds", ferm_p_week=0.60, ferm_med_ppm=50, ash_per_yr=5.0, firework_p=0.50, exhaust_max=40),
}
# Brand-detectiescenario's (pessimistisch/basis/optimistisch -> P_det laag/basis/hoog) [A]
FIRE = {
    "laag":  dict(perm=M.PERM["laag"], delay_h=72.0, smolder_W=(30, 150), f_reach=(0.2, 0.5), V=3.5, ach=5.0, lam=(0.1, 0.4), vfront_cm_min=(0.05, 0.3)),
    "basis": dict(perm=M.PERM["basis"], delay_h=6.0, smolder_W=(50, 500), f_reach=(0.3, 0.8), V=2.0, ach=2.0, lam=(0.2, 0.8), vfront_cm_min=(0.1, 1.0)),
    "hoog":  dict(perm=M.PERM["hoog"], delay_h=0.5, smolder_W=(100, 1000), f_reach=(0.5, 1.0), V=0.5, ach=0.5, lam=(0.4, 1.2), vfront_cm_min=(0.3, 2.0)),
}
P_SUSTAIN = {"laag": 0.3, "basis": 0.5, "hoog": 0.7}   # kans dat TR doorgaat in smeulen (Chen 2025: vocht dempt) [A]
LAMBDA_FIRE_LI = {"laag": 2e-4, "basis": 5e-4, "hoog": 1e-3}   # containerbrand door accu per UGC-jaar (A7 [A])
ALLCAUSE_FACTOR = 5.0   # alle oorzaken (vuurwerk, as, peuken, brandstichting) / accu [A]

TH = dict(co_abs=50.0, co_rise=30.0, ir_abs=45.0, ir_excess=20.0, co_big=150.0)


def background(rng, sc, n, ash=True, fireworks=True):
    p = dict(BG[sc])
    if not ash:
        p["ash_per_yr"] = 0.0
    if not fireworks:
        p["firework_p"] = 0.0
    t = np.arange(N_STEPS) * DT_MIN / 60.0             # uur
    day = t / 24.0
    season = np.sin(2 * np.pi * (day - 110) / 365)
    diurnal = np.sin(2 * np.pi * (t % 24 - 9) / 24)
    if p["type"] == "ondergronds":
        Tmed = 12 + 4 * season + 0.5 * diurnal
        Tmed = np.broadcast_to(Tmed, (n, N_STEPS)).copy()
    else:
        Tamb = 11 + 8 * season + 5 * diurnal
        sun_day = rng.uniform(0, 1, (n, 366))[:, day.astype(int)] * 30 * np.clip(season + 0.3, 0, None)
        Tmed = Tamb + sun_day * np.clip(diurnal, 0, None)
    # compostwarmte per weekcyclus
    week = (day // 7).astype(int)
    A = rng.uniform(0, 12, (n, 53))[:, week] * (1 + 0.5 * season)
    tin = (day % 7)
    Tmed = Tmed + A * (1 - np.exp(-tin / 2.0))
    # hotspot-excess: heterogeniteit + verse zakken (stap naar T_bag, verval 2 h)
    excess = np.abs(rng.normal(0, 1.5, (n, N_STEPS))) + 0.3 * A * (1 - np.exp(-tin / 2.0))
    n_bag = rng.poisson(80 * 365 / 4, n)   # ~1 op 4 inworpen landt in beeld als 'max pixel'
    for i in range(n):
        idx = rng.integers(0, N_STEPS, n_bag[i])
        Tbag = np.where(rng.random(n_bag[i]) < 0.02, rng.uniform(30, 40, n_bag[i]), rng.uniform(18, 25, n_bag[i]))
        jump = np.clip(Tbag - Tmed[i, idx], 0, None)
        for k in range(4):  # verval over ~20 min -> 2 h (benadering: eerste 4 stappen)
            j = np.minimum(idx + k, N_STEPS - 1)
            excess[i, j] = np.maximum(excess[i, j], jump * np.exp(-k * DT_MIN / 120))
    # CO
    base = rng.lognormal(np.log(3), 0.7, (n, 1)) * np.ones((n, N_STEPS))
    co = base.copy()
    ferm_on = rng.random((n, 53)) < p["ferm_p_week"] * (1 + 0.6 * np.clip(np.sin(2 * np.pi * (np.arange(53) * 7 - 110) / 365), 0, None))
    ferm_amp = rng.lognormal(np.log(p["ferm_med_ppm"]), 0.6, (n, 53))
    ramp = rng.uniform(12, 48, (n, 53))
    co += (ferm_on * ferm_amp)[:, week] * np.clip(tin * 24 / ramp[:, week], 0, 1)
    # lediging: uitlaatgas-piek 10 min op dag 0 van de week (om 8:00)
    emp_idx = (np.arange(53) * 7 * 24 + 8) * 60 // DT_MIN
    emp_idx = emp_idx[emp_idx < N_STEPS - 2]
    co[:, emp_idx] += rng.uniform(0, p["exhaust_max"], (n, len(emp_idx)))
    # vuurwerk 31-12 / 1-1
    ny = (364 * 24 + 23) * 60 // DT_MIN
    hit = rng.random(n) < p["firework_p"]
    k = np.arange(0, N_STEPS - ny)
    for i in np.where(hit)[0]:
        amp = rng.uniform(30, 300)
        co[i, ny:] += amp * np.exp(-k * DT_MIN / 60)
        if rng.random() < 0.3:
            excess[i, ny:ny + 6] += rng.uniform(40, 200)
    # warme as / peuk zonder brand
    for i in range(n):
        m = rng.poisson(p["ash_per_yr"])
        for _ in range(m):
            s = rng.integers(0, N_STEPS - 40)
            tau = rng.uniform(30, 120)
            kk = np.arange(40)
            excess[i, s:s + 40] += rng.uniform(30, 250) * np.exp(-kk * DT_MIN / tau)
            co[i, s:s + 40] += rng.uniform(10, 100) * np.exp(-kk * DT_MIN / (2 * tau))
    co += rng.normal(0, 2, co.shape)
    return Tmed, excess, co


def rules(Tmed, excess, co):
    lag = 10 // DT_MIN
    dco = np.zeros_like(co)
    dco[:, lag:] = co[:, lag:] - co[:, :-lag]
    tmax = Tmed + excess
    A = co > TH["co_abs"]
    B = dco > TH["co_rise"]
    ir_now = (tmax > TH["ir_abs"]) & (excess > TH["ir_excess"])
    C = ir_now.copy()
    C[:, 1:] = ir_now[:, 1:] & ir_now[:, :-1]          # 2 opeenvolgende frames (10 min)
    # B en C hoeven niet in exact dezelfde stap: venster 30 min
    def widen(X, w=30 // DT_MIN):
        Y = X.copy()
        for s in range(1, w + 1):
            Y[:, s:] |= X[:, :-s]
        return Y
    D = (A.astype(int) + B + C) >= 2
    E = (widen(B) & C) | (widen(B) & (co > TH["co_big"]))
    return dict(A=A, B=B, C=C, D=D, E=E)


def count_alarms(X):
    """Aantal alarm-episodes (opgaande flank, refractair 6 h) per container."""
    out = []
    for row in X:
        idx = np.flatnonzero(row)
        if len(idx) == 0:
            out.append(0); continue
        c, last = 1, idx[0]
        for j in idx[1:]:
            if j - last > REFRACT:
                c += 1
            last = j
        out.append(c)
    return np.array(out)


def fire_events(rng, sc, n, co_bg, sustain_p):
    """Simuleer n events (30 s stap, 2 h). Retourneer detectietijd (min, inf = niet) per regel + type."""
    f = FIRE[sc]
    dt = 30.0
    t = np.arange(0, 2 * 3600, dt)
    delay_d = rng.exponential(f["delay_h"], n) / 24
    d = np.minimum(M.RISE_M_PER_DAY * delay_d + rng.uniform(0, 0.15, n), 2.0)
    v = M.darcy_velocity(f["perm"]) * rng.lognormal(0, 0.5, n)
    t_arr = d / v
    sustain = rng.random(n) < sustain_p
    P = rng.uniform(*f["smolder_W"], n) * sustain
    yco = rng.uniform(0.1, 0.3, n)
    freach = rng.uniform(*f["f_reach"], n)
    Gco = P / 15e6 * 1000 * yco / 1.145 * freach       # L/s CO
    wh = rng.choice([2.0, 11.0, 15.0, 37.0], n, p=[0.6, 0.15, 0.15, 0.1])
    Vpulse = wh * 0.11 * freach                         # L CO uit TR-puls [A] (~6 L gas/11 Wh, 20 % CO)
    n_ = f["ach"] / 3600
    tt = t[None, :] - t_arr[:, None]
    on = tt > 0
    # puls: toevoer verspreid over 180 s
    pulse_rate = np.where(on & (tt < 180), Vpulse[:, None] / 180, 0.0)
    smold_rate = np.where(on, Gco[:, None] * np.clip(tt / 600, 0, 1), 0.0)   # smeulnest groeit in 10 min
    Gtot = pulse_rate + smold_rate
    C = np.zeros_like(tt)
    y = np.zeros(n)
    for i in range(len(t)):
        y = y + dt * (Gtot[:, i] / 1000 / f["V"] * 1e6 - n_ * y)
        C[:, i] = y
    # sensor t90 60 s
    C = M.sensor_first_order(C, dt, 60.0)
    co = C + co_bg[:, None] + rng.normal(0, 2, C.shape)
    lam = rng.uniform(*f["lam"], n)
    vfront = rng.uniform(*f["vfront_cm_min"], n) / 100 / 60
    exit_ex = np.where(on, 200 * np.exp(-d / lam)[:, None] * (sustain[:, None] | (tt < 600)), 0.0)
    front = np.where(sustain[:, None] & (t[None, :] > d[:, None] / vfront[:, None]), 300.0, 0.0)
    # TR-puls zelf bovenin (d<0.2 m): direct hete plek
    surf = np.where(on & (d[:, None] < 0.2), M.dT_pulse(wh[:, None] * 3600 * 2.5, np.maximum(d[:, None], 0.03), np.maximum(tt, 1), M.ALPHA["basis"]), 0.0)
    excess = np.maximum.reduce([exit_ex, front, surf])
    Tmed = 15.0
    lag = int(600 / dt)
    dco = np.zeros_like(co); dco[:, lag:] = co[:, lag:] - co[:, :-lag]
    dco[:, :lag] = co[:, :lag] - co_bg[:, None]   # historie vóór TR = achtergrond
    A = co > TH["co_abs"]; B = dco > TH["co_rise"]
    irn = ((Tmed + excess) > TH["ir_abs"]) & (excess > TH["ir_excess"])
    Cc = irn.copy(); Cc[:, 2:] = irn[:, 2:] & irn[:, 1:-1] & irn[:, :-2]
    w = int(1800 / dt)
    Bw = B.copy()
    for s in range(1, w + 1):
        Bw[:, s:] |= B[:, :-s]
    R = dict(A=A, B=B, C=Cc, D=(A.astype(int) + B + Cc) >= 2, E=(Bw & Cc) | (Bw & (co > TH["co_big"])))
    tdet = {}
    for k, X in R.items():
        hit = X.any(axis=1)
        first = np.where(hit, t[np.argmax(X, axis=1)], np.inf)
        tdet[k] = np.where(hit, t[np.argmax(X, axis=1)] / 60.0, np.inf)
    return tdet, sustain, d


def main():
    rng = np.random.default_rng(SEED)
    res = {"concept": "K4", "regels": {"A": "CO > 50 ppm", "B": "dCO > 30 ppm / 10 min", "C": "IR max > 45 °C én > 20 K boven mediaan, 2 frames",
                                         "D": "2-van-3 (A,B,C)", "E": "coïncidentie: B (±30 min) ∧ C, of B ∧ CO > 150 ppm (aanbevolen)"}}
    fa = {}
    example = None
    co_pool = []
    for sc in ["laag", "basis", "hoog"]:
        Tmed, excess, co = background(rng, sc, N_CONT)
        R = rules(Tmed, excess, co)
        fa[sc] = {k: float(count_alarms(X).mean()) for k, X in R.items()}
        co_pool.append(co[:, ::12].ravel())
        if sc == "basis":
            example = (Tmed[0], excess[0], co[0])
        print("FA/container-jaar", sc, {k: round(v, 3) for k, v in fa[sc].items()})
    res["vals_alarm_per_container_jaar"] = fa
    # bronontleding: hinder (rotting/zon/zakken/uitlaat) vs. 'hete objecten' (as/peuk/vuurwerk, terecht voor niet-legen)
    decomp = {}
    for sc in ["laag", "basis", "hoog"]:
        Tm_, ex_, co_ = background(np.random.default_rng(SEED + 1), sc, N_CONT, ash=False, fireworks=False)
        R_ = rules(Tm_, ex_, co_)
        decomp[sc] = {k: float(count_alarms(X).mean()) for k, X in R_.items()}
        print("FA hinder-only", sc, {k: round(v, 3) for k, v in decomp[sc].items()})
    res["vals_alarm_hinder_per_container_jaar"] = decomp
    res["hete_object_alarmen_per_container_jaar"] = {sc: {k: max(fa[sc][k] - decomp[sc][k], 0.0) for k in fa[sc]} for sc in fa}
    co_pool = np.concatenate(co_pool)

    det = {}
    curves = {}
    tgrid = np.arange(0, 121, 1)
    n_ev = 4000
    for sc in ["laag", "basis", "hoog"]:
        co_bg = rng.choice(co_pool, n_ev)
        tdet, sustain, d = fire_events(rng, sc, n_ev, co_bg, P_SUSTAIN[sc])
        det[sc] = {}
        for k, td in tdet.items():
            det[sc][k] = {
                "brand_P_det_10min": float(np.mean(td[sustain] <= 10)),
                "brand_P_det_30min": float(np.mean(td[sustain] <= 30)),
                "brand_P_det_60min": float(np.mean(td[sustain] <= 60)),
                "TR_zonder_brand_P_det_60min": float(np.mean(td[~sustain] <= 60)) if (~sustain).any() else None,
                "mediaan_detectietijd_brand_min": float(np.median(td[sustain])),
            }
            curves[(sc, k)] = [np.mean(td[sustain] <= x) for x in tgrid]
        print("detectie", sc, {k: (round(v["brand_P_det_10min"], 2), round(v["brand_P_det_60min"], 2)) for k, v in det[sc].items()})
    res["detectie_na_TR"] = det
    # gevoeligheid: basis-transport, maar cel diep (vertraging 72 h)
    FIRE["basis_diep"] = dict(FIRE["basis"], delay_h=72.0)
    tdet, sustain, d = fire_events(rng, "basis_diep", n_ev, rng.choice(co_pool, n_ev), P_SUSTAIN["basis"])
    res["detectie_gevoeligheid_basis_diep72h"] = {k: {"P10": float(np.mean(td[sustain] <= 10)), "P60": float(np.mean(td[sustain] <= 60)),
                                                     "diepte_mediaan_m": float(np.median(d))} for k, td in tdet.items()}
    print("basis diep", {k: (round(v["P10"], 2), round(v["P60"], 2)) for k, v in res["detectie_gevoeligheid_basis_diep72h"].items()})
    # vlag actief op moment van lediging: hold 6 h na laatste trigger, alarmduur ~2 h [A]
    res["vlag_actief_bij_lediging_per_container_jaar"] = {sc: {k: v * (2 + 6) / 168 for k, v in fa[sc].items()} for sc in fa}
    res["detectie_voor_TR"] = {"P": [0.0, 0.0, 0.05], "toelichting": "K4 heeft geen VOC-kanaal; ventgas vóór TR bevat weinig CO. Zelfs een VOC-sensor: P(ventgas in kopruimte vóór TR) 0,3 % / 4 % / 24 % (warmte_gas.py)."}

    # PPV 'niet legen'
    ppv = {}
    combos = {"laag": ("hoog", "laag", "laag"), "basis": ("basis", "basis", "basis"), "hoog": ("laag", "hoog", "hoog")}
    for lab, (fa_sc, det_sc, lam_sc) in combos.items():
        ppv[lab] = {}
        for k in ["A", "B", "C", "D", "E"]:
            pdet = det[det_sc][k]["brand_P_det_60min"]
            lam_li = LAMBDA_FIRE_LI[lam_sc]
            lam_all = lam_li * ALLCAUSE_FACTOR
            F = fa[fa_sc][k]
            Fh = decomp[fa_sc][k]
            Hot = max(F - Fh, 0.0)
            ppv[lab][k] = {"PPV_accubrand": lam_li * pdet / (lam_li * pdet + F + 1e-12),
                           "PPV_brand_alle_oorzaken": lam_all * pdet / (lam_all * pdet + F + 1e-12),
                           "PPV_brand_of_heet_object": (lam_all * pdet + Hot) / (lam_all * pdet + F + 1e-12),
                           "vlaggen_per_1000_containers_jaar": 1000 * (F + lam_all * pdet),
                           "hindervlaggen_per_1000_containers_jaar": 1000 * Fh}
    res["P_vlag_niet_legen_terecht"] = ppv
    res["aannames"] = {"BG": BG, "FIRE": {k: {kk: (list(vv) if isinstance(vv, tuple) else vv) for kk, vv in v.items()} for k, v in FIRE.items()},
                       "P_sustain": P_SUSTAIN, "lambda_fire_li_per_UGC_jaar": LAMBDA_FIRE_LI, "allcause_factor": ALLCAUSE_FACTOR,
                       "drempels": TH, "container_jaren_per_scenario": N_CONT, "events_per_scenario": n_ev}
    res["formaat_A6"] = {
        "classes": ["geen", "cel", "pakket"],
        "p_out_given_item": "n.v.t. – K4 detecteert geen items, alleen events; gebruik als apart event-kanaal",
        "event_kanaal": {"rood_niet_legen": "regel E", "kans_detectie_brand_60min_l_b_h": [det[s]["E"]["brand_P_det_60min"] for s in ["laag", "basis", "hoog"]],
                         "vals_alarm_per_container_jaar_l_b_h": [fa[s]["E"] for s in ["laag", "basis", "hoog"]]},
    }
    with open(os.path.join(HERE, "event_model_K4.json"), "w") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)

    # ---- figuur
    fig, axs = plt.subplots(2, 2, figsize=(12, 8.5))
    Tm, ex, co = example
    s0 = 160 * 24 * 60 // DT_MIN
    sl = slice(s0, s0 + 14 * 24 * 60 // DT_MIN)
    th = np.arange(sl.stop - sl.start) * DT_MIN / 60 / 24
    ax = axs[0, 0]
    ax.plot(th, co[sl], color="#555", lw=0.8, label="CO (ppm)")
    ax.plot(th, (Tm + ex)[sl], color="#e07a1f", lw=0.8, label="IR max-pixel (°C)")
    ax.plot(th, Tm[sl], color="#1f5fa8", lw=0.8, label="IR mediaan (°C)")
    ax.axhline(TH["co_abs"], color="#555", ls="--", lw=0.6)
    ax.axhline(TH["ir_abs"], color="#e07a1f", ls="--", lw=0.6)
    ax.set_xlabel("dag (juni, ondergronds, basis)")
    ax.set_title("(a) Achtergrond 14 dagen: fermentatie-CO, compost, verse zakken")
    ax.legend(fontsize=7)
    ax = axs[0, 1]
    ks = ["A", "B", "C", "D", "E"]
    x = np.arange(len(ks))
    for j, sc in enumerate(["laag", "basis", "hoog"]):
        ax.bar(x + (j - 1) * 0.27, [fa[sc][k] for k in ks], 0.27, label=f"achtergrond {sc} ({BG[sc]['type']})")
    ax.set_xticks(x); ax.set_xticklabels(["A CO>50", "B dCO>30", "C IR", "D 2v3", "E coïnc."])
    ax.set_yscale("symlog", linthresh=0.01)
    ax.axhline(0.1, color="k", ls="--", lw=0.8); ax.text(3.6, 0.12, "doel 0,1", fontsize=7)
    ax.set_ylabel("vals alarm per container-jaar")
    ax.set_title("(b) Vals alarm per regel")
    ax.legend(fontsize=7)
    ax = axs[1, 0]
    for k, c in zip(ks, ["#999", "#555", "#e07a1f", "#2a9d8f", "#b22222"]):
        ax.plot(tgrid, curves[("basis", k)], color=c, label=f"regel {k} (basis)")
        ax.fill_between(tgrid, curves[("laag", k)], curves[("hoog", k)], color=c, alpha=0.08)
    ax.set_xlabel("minuten na TR-onset")
    ax.set_ylabel("P(detectie | smeulbrand)")
    ax.set_title("(c) Detectie brand-event (band = pessimistisch–optimistisch)")
    ax.legend(fontsize=7)
    ax = axs[1, 1]
    for lab, mk in zip(["laag", "basis", "hoog"], ["v", "o", "^"]):
        ax.scatter([ppv[lab][k]["vlaggen_per_1000_containers_jaar"] for k in ks], [ppv[lab][k]["PPV_brand_of_heet_object"] for k in ks], marker=mk, label=f"scenario {lab}")
        for k in ks:
            ax.annotate(k, (ppv[lab][k]["vlaggen_per_1000_containers_jaar"], ppv[lab][k]["PPV_brand_of_heet_object"]), fontsize=7)
    ax.set_xscale("log")
    ax.set_xlabel("'niet legen'-vlaggen per 1.000 containers per jaar")
    ax.set_ylabel("P(vlag terecht) – brand of heet object (as/vuurwerk)")
    ax.set_title("(d) Terechtheid vlag vs. alarmlast")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_valsalarm.png"), dpi=130)
    print(json.dumps(ppv["basis"], indent=1))


if __name__ == "__main__":
    main()
