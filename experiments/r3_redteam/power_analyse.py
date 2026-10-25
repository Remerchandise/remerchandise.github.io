"""A8 Ronde 3 - power-analyses voor labtests en veldtest.

Draai vanuit repo-root: python3 experiments/r3_redteam/power_analyse.py
Gebruikt experiments/common/params.py. Deterministisch (seed 8).
Output: tabellen op stdout + results.json + fig_power_veldtest.png, fig_power_cluster.png,
fig_power_brand.png in experiments/r3_redteam/.
"""
import json, math, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import params  # noqa: E402

rng = np.random.default_rng(8)
Z = stats.norm.ppf(0.975)
out = {}

# ---------- 1. Prevalentie per zak uit params ----------
def li_mean_per_bag(scale=1.0, min_wheq=0.0):
    m = 0.0
    for k, it in params.ITEMS.items():
        if not it["li"]:
            continue
        wheq = it["wh"][1] * it["w_chem"] * it["w_state"]
        if wheq >= min_wheq:
            m += it["mean"] * scale
    return m

prev = {}
for sc, f in params.SCENARIOS.items():
    lam_li = li_mean_per_bag(f)
    lam_pak = li_mean_per_bag(f, params.PACK_WHEQ)
    lam_10 = li_mean_per_bag(f, params.THRESH_THROW["oranje"])
    prev[sc] = dict(p_li=1 - math.exp(-lam_li), p_ge10=1 - math.exp(-lam_10), p_pakket=1 - math.exp(-lam_pak))
out["prevalentie_per_zak"] = prev

# ---------- 2. Veldtest: zakken sorteren om recall +-10 % (95 %) te meten ----------
def n_pos_needed(recall, halfwidth):
    """Wilson-benadering ~ normaal; aantal positieve zakken."""
    return math.ceil(Z**2 * recall * (1 - recall) / halfwidth**2)

veld = {}
kg = params.BAG["mass_kg_median"]
for target, key in [("Li-item (alle)", "p_li"), ("Li >= 10 Wh-eq", "p_ge10"), ("pakket >= 50 Wh-eq", "p_pakket")]:  # NB params: alleen ebike_step >= 50 Wh-eq (laptop 48)
    veld[target] = {}
    for sc in params.SCENARIOS:
        p = prev[sc][key]
        row = {}
        for rec in (0.5, 0.8):
            npos = n_pos_needed(rec, 0.10)
            nbags = math.ceil(npos / p)
            row[f"recall{rec}"] = dict(n_pos=npos, n_zakken=nbags, ton=round(nbags * kg / 1000, 1))
        veld[target][sc] = row
out["veldtest_natuurlijk"] = veld

# PPV-meting: aantal alarmen nodig voor PPV +-10 %
out["ppv_meting_alarmen_nodig"] = {f"ppv{p}": n_pos_needed(p, 0.10) for p in (0.1, 0.27, 0.5)}

# Spiking (blind toegevoegde testzakken): positieven worden niet meer door prevalentie beperkt
spike = {}
for rec in (0.5, 0.8, 0.95):
    spike[f"recall{rec}"] = dict(hw10=n_pos_needed(rec, 0.10), hw05=n_pos_needed(rec, 0.05))
out["spiking_per_klasse"] = spike

# Simulatiecheck: dekking 95%-CI bij 62 positieven, recall 0.8
sims = rng.binomial(62, 0.8, 20000) / 62
out["sim_check_halfbreedte_95_n62"] = round(float(np.percentile(np.abs(sims - 0.8), 95)), 3)

# ---------- 3. Labtest inductie: AUC-precisie (Hanley-McNeil) ----------
def auc_se(auc, n1, n0):
    q1 = auc / (2 - auc); q2 = 2 * auc**2 / (1 + auc)
    return math.sqrt((auc*(1-auc) + (n1-1)*(q1-auc**2) + (n0-1)*(q2-auc**2)) / (n1*n0))

lab = {}
for auc in (0.7, 0.8, 0.9):
    for n in (20, 50, 100, 200):
        lab[f"AUC{auc}_n{n}per_klasse"] = round(Z * auc_se(auc, n, n), 3)
out["lab_inductie_auc_halfbreedte"] = lab

# ---------- 4. Steekproef-cluster: hoeveel kg om 2x verschil in Li/t te zien ----------
def power_poisson_ratio(lam_t, ratio, tonnes, n_sim=4000):
    """Twee clusters, elk 'tonnes' gesorteerd; conditionele binomiale toets (eenzijdig 5 %)."""
    a = rng.poisson(lam_t * tonnes, n_sim)
    b = rng.poisson(lam_t * ratio * tonnes, n_sim)
    tot = a + b
    p_hat = ratio / (1 + ratio)
    pv = stats.binom.sf(b - 1, tot, 0.5)
    pv[tot == 0] = 1
    return float(np.mean(pv < 0.05))

cluster = {}
ton_grid = np.array([0.1, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0])
fig, ax = plt.subplots(figsize=(6.5, 4))
for sc, col in zip(params.SCENARIOS, ["#7aa6c2", "#1f5f8b", "#0b2e4a"]):
    lam_t = li_mean_per_bag(params.SCENARIOS[sc]) / kg * 1000  # Li-items per ton
    pw = [power_poisson_ratio(lam_t, 2.0, t) for t in ton_grid]
    t80 = next((float(t) for t, p in zip(ton_grid, pw) if p >= 0.8), None)
    cluster[sc] = dict(li_per_ton=round(lam_t, 2), ton_per_cluster_power80=t80,
                       steekproeven_100kg=None if t80 is None else math.ceil(t80 / 0.1))
    ax.plot(ton_grid, pw, "o-", color=col, label=f"{sc} ({lam_t:.1f} Li/t)")
# proxy: alle batterijen incl. alkaline (Eureco-methode, ~28 losse + ~8 in apparaten per t)
for lam_all, lab_ in [(36.0, "alle batterijen (~36/t, proxy)")]:
    pw = [power_poisson_ratio(lam_all, 2.0, t) for t in ton_grid]
    t80 = next((float(t) for t, p in zip(ton_grid, pw) if p >= 0.8), None)
    cluster["proxy_alle_batterijen"] = dict(per_ton=lam_all, ton_per_cluster_power80=t80,
                                          steekproeven_100kg=None if t80 is None else math.ceil(t80 / 0.1))
    ax.plot(ton_grid, pw, "s--", color="#c46a1b", label=lab_)
ax.axhline(0.8, ls="--", c="grey")
ax.set_xlabel("gesorteerd per cluster (t)"); ax.set_ylabel("power (2x verschil, alpha 5 %)")
ax.set_title("Steekproefsortering: tonnage om 2x verschil Li/t te zien")
ax.legend(); fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_power_cluster.png"), dpi=120)
out["cluster_steekproef"] = cluster

# ---------- 5. Brand als uitkomst: containerjaren voor 30 % daling ----------
def containerjaren_needed(rate_per_cj, reduction, power=0.8):
    # twee-arm Poisson, normaalbenadering op log-rate ratio
    za, zb = Z, stats.norm.ppf(power)
    rr = 1 - reduction
    # var(log RR) ~ 1/E1 + 1/E2 ; E1 = rate*N, E2 = rate*rr*N
    n = (za + zb) ** 2 * (1 + 1 / rr) / (rate_per_cj * math.log(rr) ** 2)
    return n

brand = {}
p_fire_lediging = {"laag": 7e-6, "basis": 3e-5, "hoog": 7e-5}  # A1
for sc, p in p_fire_lediging.items():
    rate = p * params.CONTAINER["emptyings_per_year"]
    brand[sc] = {f"daling{int(r*100)}%": int(containerjaren_needed(rate, r)) for r in (0.3, 0.5)}
out["brand_uitkomst_containerjaren_per_arm"] = brand
fig, ax = plt.subplots(figsize=(6.5, 4))
reds = np.linspace(0.1, 0.8, 30)
for sc, col in zip(p_fire_lediging, ["#7aa6c2", "#1f5f8b", "#0b2e4a"]):
    rate = p_fire_lediging[sc] * 52
    ax.semilogy(reds * 100, [containerjaren_needed(rate, r) for r in reds], color=col, label=sc)
ax.axhline(1000, ls=":", c="grey"); ax.text(12, 1150, "gemeente 1.000 containers, 1 jaar", fontsize=8)
ax.set_xlabel("te detecteren brandreductie (%)"); ax.set_ylabel("containerjaren per arm")
ax.set_title("Branden als uitkomstmaat: benodigde omvang"); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_power_brand.png"), dpi=120)

# ---------- figuur veldtest ----------
fig, ax = plt.subplots(figsize=(6.5, 4))
labels = list(veld.keys())
x = np.arange(len(labels))
for i, sc in enumerate(params.SCENARIOS):
    vals = [veld[l][sc]["recall0.8"]["ton"] for l in labels]
    ax.bar(x + (i - 1) * 0.27, vals, 0.27, label=sc)
ax.set_yscale("log"); ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8)
ax.set_ylabel("te sorteren restafval (t)"); ax.set_title("Veldtest zonder spiking: recall 0,8 +-0,10 (95 %)")
ax.legend(); fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_power_veldtest.png"), dpi=120)

with open(os.path.join(HERE, "results.json"), "w") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
