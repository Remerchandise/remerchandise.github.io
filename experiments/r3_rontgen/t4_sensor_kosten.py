"""T4 – sensor_model_K3.json (formaat experiments/common/params.py) + kosten K3a (vast per zuil) vs K3b (rouleerende ijkpaal).
Output: sensor_model_K3.json, fig_kosten.png, t4_resultaten.txt"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'experiments', 'common'))
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import params as P
rng = np.random.default_rng(42)
PACK = P.PACK_WHEQ
W_STATE_ASSUMED = 0.8   # sensor kent SOC/chemie niet -> Wh-eq_est = Wh_est * 0,8 [A]
SIG = 0.35              # [A] lognormale fout Wh-schatting (celtelling ok, capaciteit/cel + vergroting onzeker)
P_HEAVY_FAIL = 0.03     # [A] fractie zakken > ~11 g/cm2 waar 30 kV/4 W/5 s SNR<5 haalt (t2) -> gemist
# p_det = kans dat object als 'accu-achtig' (cel/pakket) wordt gesegmenteerd; wh_fac = (mediaan geschatte Wh / echte Wh of vaste Wh)
DET = {  # [A] onderbouwing in RESULTATEN.md (T1: opaak/vorm; T2: SNR)
    'blik': dict(p_det=0.010, wh=('fix', 8.0)),             # spuitbus/blikrand als cilinder
    'folie': dict(p_det=0.002, wh=('fix', 5.0)),            # transparant (T~0,9)
    'sleutel_klein_metaal': dict(p_det=0.040, wh=('fix', 5.0)),  # bouten, magneten, stiften: opaak + cilindrisch
    'pan_gereedschap': dict(p_det=0.10, wh=('fix', 25.0)),  # massief blok/motor lijkt op pack
    'alkaline': dict(p_det=0.85, wh=('fac', 1.8)),          # zelfde vorm als Li-cel; AA-volume ~0,5x 18650 -> ~5,5 Wh geschat
    'knoopcel': dict(p_det=0.35, wh=('fac', 1.0)),          # lijkt op munt
    'elektronica_zonder_accu': dict(p_det=0.08, wh=('fix', 10.0)),  # elco's/motortjes cilindrisch
    'vape': dict(p_det=0.80, wh=('fac', 1.0)),              # opake kern in semitransparante Al-huls
    'li_klein_overig': dict(p_det=0.45, wh=('fac', 1.0)),
    'cel_18650': dict(p_det=0.93, wh=('fac', 1.0)),
    'telefoon': dict(p_det=0.95, wh=('fac', 1.0)),
    'powerbank': dict(p_det=0.95, wh=('fac', 1.0)),
    'laptop_gereedschap': dict(p_det=0.95, wh=('fac', 1.0)),
    'ebike_step': dict(p_det=0.97, wh=('fac', 1.0)),
}
def tri(lo, mid, hi, n):
    return rng.triangular(lo, mid, hi if hi > lo else lo + 1e-9, n) if hi > lo else np.full(n, mid)
pout = {}; whest = {}
n = 200_000
for k, it in P.ITEMS.items():
    d = DET[k]; pdet = d['p_det'] * ((1 - P_HEAVY_FAIL) if it['li'] else 1)
    if d['wh'][0] == 'fac':
        wtrue = tri(*it['wh'], n); est = wtrue * d['wh'][1] * np.exp(rng.normal(0, SIG, n))
        if k == 'alkaline': est = 3.0 * d['wh'][1] * np.exp(rng.normal(0, SIG, n))
    else:
        est = d['wh'][1] * np.exp(rng.normal(0, 0.6, n))
    ppack = np.mean(est * W_STATE_ASSUMED >= PACK)
    pout[k] = [round(float(1 - pdet), 4), round(float(pdet * (1 - ppack)), 4), round(float(pdet * ppack), 4)]
    whest[k] = [round(float(np.median(est)), 2), SIG if d['wh'][0] == 'fac' else 0.6]
model = {
    "concept": "K3",
    "variant": "K3a (vast per zuil) en K3b (ijkpaal) gebruiken dezelfde sensor; K3b meet alleen tijdens campagne",
    "classes": P.OUT_CLASSES,
    "p_out_given_item": pout,
    "wh_est_given_item": {"note": "[mediaan geschatte Wh, sigma lognormaal] per gedetecteerd object; A6: tel Wh_est*0,8 van alle 'cel'-objecten in één inworp op -> >= PACK_WHEQ = pakket (vangt bundels alkaline/losse cellen)", **whest},
    "clutter": {"model": "independent_or", "note": "elk niet-Li object triggert zelfstandig met p_out_given_item; Al-blik/folie/glas zijn (half)transparant (T1) en triggeren vrijwel nooit"},
    "masking": {"p_miss_li_given_n_metal": [0.0, 0.006, 0.012, 0.03],
                "note": "2D-overlap met opaak metaal: ~3 %/opaak object x 50 % mis bij overlap; ~40 % van metaalobjecten opaak [A]"},
    "chemie": "Li-ion vs alkaline NIET te onderscheiden (T1: R 18650=1,19 vs AA=1,20 zelfs bij 80 kV; bij 30 kV beide opaak)",
    "meettijd_s": {"laag": 0.2, "basis": 5, "hoog": 15, "note": "4/3-camera+GOS, 30 kV 4 W; t2_resultaten.txt"},
    "basis": "experiments/r3_rontgen: t1 (Beer-Lambert/contrast), t2 (fotonstatistiek), p_det [A] expertschatting vorm-herkenning; PACK_WHEQ=%d, sigma Wh %.2f, P_heavy_fail %.2f" % (PACK, SIG, P_HEAVY_FAIL),
}
json.dump(model, open(os.path.join(HERE, 'sensor_model_K3.json'), 'w'), indent=1, ensure_ascii=False)
out = ['p_out_given_item [geen, cel, pakket]  (PACK_WHEQ=%d)' % PACK] + [f'  {k:24s} {v}' for k, v in pout.items()]

# ---------------- kosten ----------------
# (laag, basis, hoog) EUR 2026 excl. btw [A]; bron research/A3_rontgen.md §8, A5 R2 (verhuizing EUR 300–600)
HW = {'bron 30 kV + HV + kV-begrenzing': (400, 1200, 3000), 'GOS + 4/3"-camera + lens': (600, 1200, 2000),
      'afscherming/interlocks/PE-vensters': (300, 600, 1500), 'MCU+NPU (STM32N6) + modem': (60, 120, 250),
      'PV 10 Wp + LiFePO4 50 Wh': (100, 200, 400)}
INSTALL = (300, 600, 1200)       # montage + meetrapport stralingsdeskundige per installatie
OPEX_Y = (100, 200, 400)         # jaarlijkse interlock-/dosimetriecontrole + data
YEARS = 6
hw = np.array([sum(v[i] for v in HW.values()) for i in range(3)])
k3a = (hw + np.array(INSTALL) + np.array(OPEX_Y) * YEARS) / (YEARS * 12)
# K3b: unit + frame; campagnes van 3 mnd -> 4 campagnes/unit/jaar [A]; per campagne verhuizing + stralingsmeting + analyse
unit = hw + 200
camp = np.array([300, 600, 600]) + np.array([200, 300, 600]) + np.array([500, 1000, 2000])
per_unit_year = unit / YEARS + 4 * camp + np.array(OPEX_Y)
cov = np.array([50, 35, 20])   # (i) netwerk: 1 unit per 20–50 containers, continu rouleren
k3b = per_unit_year / cov / 12
# (ii) validatie-/ijkcampagne per gemeente: 5 units x 1 jaar (20 zuil-campagnes) voor 1 000 containers [A]
k3b_val = 5 * per_unit_year / 1000 / 12
out.append(f'\nHW per zuil (laag/basis/hoog): {hw.tolist()} EUR')
out.append(f'K3a vast per zuil, TCO {YEARS} jr: {np.round(k3a,1).tolist()} EUR/container/maand')
out.append(f'K3b ijkpaal: kosten per unit-jaar {np.round(per_unit_year).tolist()} EUR; per campagne {camp.tolist()} EUR;'
           f' (i) netwerk 1 per {cov.tolist()} containers: {np.round(k3b,1).tolist()} EUR/container/maand')
out.append(f'K3b (ii) ijkcampagne 5 units x 1 jaar voor gemeente met 1 000 containers: {np.round(5*per_unit_year).tolist()} EUR/jaar = {np.round(k3b_val,2).tolist()} EUR/container/maand')
out.append('Vermeden schade (A7): ~3 EUR/container/maand (basis)')
fig, ax = plt.subplots(figsize=(7, 4.2))
x = np.arange(3); lab = ['K3a vast per zuil', 'K3b netwerk\n(1 per 20–50)', 'K3b ijkcampagne\n(5 units/1000 cont.)']
V = [k3a, k3b, k3b_val]; basis = [v[1] for v in V]; err = [[v[1]-v[0] for v in V], [v[2]-v[1] for v in V]]
ax.bar(x, basis, yerr=err, capsize=6, color=['C3', 'C0', 'C2']); ax.axhline(3, color='k', ls='--'); ax.text(-0.4, 3.6, 'vermeden schade ~€3/container/mnd (A7)', fontsize=8)
ax.set_xticks(x, lab); ax.set_ylabel('EUR per container per maand (TCO 6 jr)'); ax.set_title('Kosten K3a vs K3b (laag–basis–hoog)')
for i, b in enumerate(basis): ax.text(i, b + 1, f'€{b:.1f}', ha='center')
plt.tight_layout(); plt.savefig(os.path.join(HERE, 'fig_kosten.png'), dpi=130)
open(os.path.join(HERE, 't4_resultaten.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
