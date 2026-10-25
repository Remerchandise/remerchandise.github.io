"""Gedeelde parameters voor alle Ronde 3-experimenten (Orchestrator).

Bronnen: research/A1_risicobenchmark.md (energie per type, w-factoren, k),
research/A6_software.md §2.2 (zakinhoud). Alles met [A] is aanname.
Gebruik: from experiments.common.params import ITEMS, BAG, SCENARIOS
of: sys.path.insert(0, 'experiments/common'); import params
"""

# Zak en container [A]
BAG = {
    "mass_kg_median": 5.0, "mass_kg_low": 3.0, "mass_kg_high": 9.0,
    "volume_l": (30, 60),
}
CONTAINER = {
    "bags_per_emptying": (80, 100, 120),   # laag/basis/hoog [A]
    "throws_per_day": (30, 80, 150),       # inworpen per dag [A]
    "emptyings_per_year": 52,              # 1x/week basis [A]
}

# Itemklassen per zak.
#   mean: gemiddeld aantal per zak (basis), band (laag, hoog)
#   dist: 'nb' (negatief binomiaal, r) of 'poisson'
#   wh: energie (laag, basis, hoog) in Wh
#   li: True als lithium (ion of metaal)
#   w_chem: weging chemie; w_state: weging toestand/SOC (basis) -> Wh-eq = wh*w_chem*w_state
#   metal: 'ferro' | 'nonferro' | 'mixed' | 'none' (voor inductie)
ITEMS = {
    "blik":            dict(mean=2.5,   band=(1, 5),        dist=("nb", 1.5), wh=(0, 0, 0),       li=False, w_chem=0,   w_state=0,   metal="mixed"),
    "folie":           dict(mean=3.0,   band=(1, 6),        dist=("nb", 1.0), wh=(0, 0, 0),       li=False, w_chem=0,   w_state=0,   metal="nonferro"),
    "sleutel_klein_metaal": dict(mean=0.15, band=(0.05, 0.3), dist=("poisson",), wh=(0, 0, 0),   li=False, w_chem=0,   w_state=0,   metal="mixed"),
    "pan_gereedschap": dict(mean=0.02,  band=(0.01, 0.05),  dist=("poisson",), wh=(0, 0, 0),     li=False, w_chem=0,   w_state=0,   metal="ferro"),   # [A] groot ferro-object
    "alkaline":        dict(mean=0.14,  band=(0.10, 0.20),  dist=("nb", 0.3), wh=(2.5, 3.0, 3.9), li=False, w_chem=0.0, w_state=0,   metal="ferro"),
    "knoopcel":        dict(mean=0.01,  band=(0.005, 0.02), dist=("poisson",), wh=(0.6, 0.7, 0.7), li=True, w_chem=0.3, w_state=1.0, metal="ferro"),
    "elektronica_zonder_accu": dict(mean=0.10, band=(0.05, 0.2), dist=("poisson",), wh=(0, 0, 0), li=False, w_chem=0, w_state=0, metal="mixed"),
    "vape":            dict(mean=0.010, band=(0.005, 0.02), dist=("poisson",), wh=(1.0, 2.0, 3.7), li=True, w_chem=1.0, w_state=1.5, metal="nonferro"),  # Al-huls + pouch/13350
    "li_klein_overig": dict(mean=0.005, band=(0.003, 0.01), dist=("poisson",), wh=(0.15, 0.5, 1.5), li=True, w_chem=1.0, w_state=1.0, metal="nonferro"),  # oortjes, watch
    "cel_18650":       dict(mean=0.0015, band=(0.0008, 0.003), dist=("poisson",), wh=(9, 11, 12.6), li=True, w_chem=1.0, w_state=0.7, metal="ferro"),
    "telefoon":        dict(mean=0.0015, band=(0.0008, 0.004), dist=("poisson",), wh=(11.5, 15, 19), li=True, w_chem=1.0, w_state=0.7, metal="mixed"),
    "powerbank":       dict(mean=0.0010, band=(0.0005, 0.003), dist=("poisson",), wh=(18, 37, 74), li=True, w_chem=1.0, w_state=0.8, metal="ferro"),  # meestal 18650-array
    "laptop_gereedschap": dict(mean=0.0004, band=(0.0002, 0.0015), dist=("poisson",), wh=(40, 60, 100), li=True, w_chem=1.0, w_state=0.8, metal="ferro"),
    "ebike_step":      dict(mean=0.0001, band=(0.00003, 0.0005), dist=("poisson",), wh=(250, 450, 720), li=True, w_chem=1.0, w_state=0.8, metal="ferro"),
}
# Controle: Li-items per zak basis ~0.030 -> ~6 Li-items/ton bij 5 kg/zak (A1 basis); ~3 per lediging van 100 zakken.
# Scenario's schalen alle Li-items samen.
SCENARIOS = {"laag": 0.5, "basis": 1.0, "hoog": 2.5}

# Risico (A1 §7.3): p_brand per item per ketenpassage = 1 - exp(-k * Wh_eq)
K_PER_WHEQ = {"laag": 1.7e-7, "basis": 1.5e-6, "hoog": 2.3e-5}

# Drempels (A1)
THRESH_THROW = {"oranje": 10, "rood": 50}       # Wh-eq per inworp
THRESH_CONTAINER = {"oranje": 50, "rood": 150}  # Wh-eq per container sinds lediging
PACK_WHEQ = 20  # sensorklasse "pakket" = powerbank en groter (Orchestrator-besluit R3: met params-Wh valt bij 50 alleen e-bike erboven; A8/A1 Pareto: >=powerbank = ~58 % risico)

# Sensor-uitgangsklassen (gemeenschappelijk formaat voor A2/A3/A4 -> A6)
# Per concept levert een agent experiments/<map>/sensor_model_<concept>.json:
# {
#   "concept": "K2",
#   "classes": ["geen", "cel", "pakket"],
#   "p_out_given_item": {"<itemklasse>": [p_geen, p_cel, p_pakket], ...},   # één item alleen in zak
#   "clutter": {"model": "independent_or", "note": "elk niet-Li metaalobject kan zelfstandig een output triggeren met p_out_given_item"},
#   "masking": {"p_miss_li_given_n_metal": [p0, p1, p2, p3plus]},   # extra miskans Li door ander metaal
#   "basis": "korte toelichting + verwijzing naar simulatie"
# }
OUT_CLASSES = ["geen", "cel", "pakket"]

ECON = {  # prijspeil 2026 excl. btw [A]
    "fire_cost_truck_eur": (10_000, 25_000, 50_000),   # gemiddelde schade per wagenbrand-incident (A7)
    "fire_cost_container_eur": (3_000, 8_000, 15_000),
    "price_level": "EUR 2026 excl. btw",
}
