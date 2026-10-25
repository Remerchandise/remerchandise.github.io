"""Ronde 3 – A7 business model: unit economics, TCO 6 jaar, prijs, business case, betalers.

Draai:  python3 experiments/r3_business/business.py
Output: experiments/r3_business/{results.json, tables.md, fig_unit_economics.png, fig_business_case.png}

PARAMETRISEERBAAR (FASE 2):
  * BOM van A5: product/BOM_<concept>.csv  -> overschrijft hw (laag/basis/hoog) van dat concept.
    Ondersteunde CSV-vormen (kolomnamen hoofdletterongevoelig):
      (a) rijen met kolommen 'laag','basis','hoog' (of 'prijs_laag', 'eur_basis', ...) -> kolomsom
      (b) één rij met 'totaal'/'total' in de eerste kolom -> die rij
  * MC van A6: experiments/r3_classificatie/mc_results.json (of r3_business/mc_input.json) met per concept
      {"K2": {"recall_energy": [l,b,h], "alarms_per_1000_emptyings": [l,b,h],
              "avoided_fire_fraction": [l,b,h] (optioneel; overschrijft recall*eff),
              "fires_per_1000_containers_year": [l,b,h] (optioneel; overschrijft A1-basis)}}
  * Alle andere parameters: dict CONCEPTS / GLOBAL hieronder, of run(overrides={...}).
Alle bedragen EUR 2026 excl. btw. [A] = aanname, zie RESULTATEN.md.
"""
import csv, json, os, sys, copy
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "experiments", "common"))
try:
    import params as P
    ECON = P.ECON
except Exception:  # fallback
    ECON = {"fire_cost_truck_eur": (10_000, 25_000, 50_000), "fire_cost_container_eur": (3_000, 8_000, 15_000)}

S = ["laag", "basis", "hoog"]
SCALES = [100, 1000, 10000]

GLOBAL = {
    "life_y": 6,                                   # TCO-horizon en afschrijving [A]
    "gross_margin": 0.40,                          # brutomarge leverancier [A]
    "emptyings_per_year": 52,
    # incidenten in de keten per 1.000 containers per jaar (A1 R0: 1,7; 0,3–15)
    "fires_per_1000_cy": (0.3, 1.7, 15.0),
    # schade per incident per schakel [A]; truck/container uit params.ECON
    "dmg_truck": ECON["fire_cost_truck_eur"],
    "dmg_container": ECON["fire_cost_container_eur"],
    "p_container_start": (0.1, 0.2, 0.3),          # deel incidenten dat al in de container begint [A]
    "dmg_processor": (5_000, 25_000, 75_000),       # verwachte AVI/overslag-schade per incident (kans x 1-5 mln) [A]
    # vaste kosten leverancier per jaar (support, dashboard, accountmanagement), per schaal
    "support_fixed_y": {100: 10_000, 1000: 30_000, 10000: 100_000},   # platform/accountmanagement [A]
    "support_per_unit_y": {"container": 6, "pool": 150, "wagen": 300},  # helpdesk + veldsupport per eenheid [A]
    # klanten per schaal en CAC per klant
    "customers": {100: 1, 1000: 5, 10000: 30},
    "cac_per_customer": (15_000, 30_000, 50_000),
    "hw_scale": {100: 1.0, 1000: 0.8, 10000: 0.65},  # volumekorting hardware
    "cloud_pm": (0.15, 0.30, 0.60),                 # per eenheid per maand bij 10k; x3 bij 100, x1,5 bij 1000
    "cost_per_alarm": (10, 40, 150),                # actie per melding (oranje = laatst in route; rood = apart legen) [A]
}

# unit: 'container' (1 per container), 'wagen' (1 per containers_per_unit), 'pool' (rouleert), 'gemeente'
# kosten: laag=goedkoop ; prestaties: laag=pessimistisch
CONCEPTS = {
    "K1": dict(name="Strandmetaaldetector (VLF) in trommel", unit="container", cpu=(1, 1, 1),
               hw=(35, 50, 80), install=(25, 40, 60), conn_pm=(0.4, 0.9, 1.5), maint_rate=(0.05, 0.08, 0.12),
               maint_cost=(60, 100, 150), cac_factor=1.0,
               recall=(0.10, 0.25, 0.40), eff={"truck": (0.3, 0.5, 0.7), "proc": (0.1, 0.2, 0.4), "cont": (0, 0, 0)},
               alarms=(80, 40, 20)),   # meldingen per 1.000 ledigingen (pessimistisch = veel)
    "K2": dict(name="Pakketwachter (PI, OEM pas-zuil)", unit="container", cpu=(1, 1, 1),
               hw=(15, 25, 40), install=(20, 40, 60), conn_pm=(0.2, 0.5, 1.0),   # = OEM-fee i.p.v. eigen modem
               maint_rate=(0.03, 0.05, 0.08), maint_cost=(40, 60, 100), cac_factor=0.5, support_factor=0.7,
               recall=(0.25, 0.45, 0.65), eff={"truck": (0.3, 0.5, 0.7), "proc": (0.1, 0.2, 0.4), "cont": (0, 0, 0)},
               alarms=(30, 15, 8)),
    "K3a": dict(name="Röntgen schaduwdoos vast per zuil", unit="container", cpu=(1, 1, 1),
                hw=(900, 2000, 4500), install=(200, 400, 800), conn_pm=(0.4, 0.9, 1.5),
                maint_rate=(0.08, 0.12, 0.20), maint_cost=(150, 250, 400), cac_factor=1.0,
                recall=(0.60, 0.80, 0.90), eff={"truck": (0.3, 0.5, 0.7), "proc": (0.1, 0.2, 0.4), "cont": (0, 0, 0)},
                alarms=(10, 6, 4)),
    "K3b": dict(name="Röntgen ijkpaal rouleert (1 per 35)", unit="pool", cpu=(20, 35, 50),
                hw=(2000, 3500, 7000), install=(150, 250, 400), conn_pm=(0.9, 0.9, 1.5),
                maint_rate=(0.08, 0.12, 0.20), maint_cost=(150, 250, 400), cac_factor=1.0,
                moves_per_y=(4, 6, 12), move_cost=(150, 250, 400),
                recall=(0.60, 0.80, 0.90), eff={"truck": (0.3, 0.5, 0.7), "proc": (0.1, 0.2, 0.4), "cont": (0, 0, 0)},
                alarms=(10, 6, 4), coverage_is_fraction=True),   # beschermt alleen 1/cpu van de containers tegelijk
    "K4": dict(name="Deksel-eventmodule (IR 8x8 + CO)", unit="container", cpu=(1, 1, 1),
               hw=(45, 70, 110), install=(20, 35, 60), conn_pm=(0.4, 0.9, 1.5),
               maint_rate=(0.05, 0.08, 0.12), maint_cost=(60, 100, 150), cac_factor=1.0,
               recall=(0.6, 0.8, 0.9), event_only=True,      # alleen incidenten die in container starten
               # FASE 2: A6 rekent 0 wagenbranden; A7 laat 'niet legen' bij container-start beperkt meetellen [A]
               eff={"truck": (0.0, 0.3, 0.6), "proc": (0.0, 0.3, 0.6), "cont": (0.2, 0.4, 0.6)},
               alarms=(3, 1, 0.5)),
    "K5": dict(name="Hybride K2+K4 + actieprotocol", unit="container", cpu=(1, 1, 1),
               hw=(55, 90, 140), install=(35, 60, 100), conn_pm=(0.3, 0.7, 1.2),
               maint_rate=(0.05, 0.08, 0.12), maint_cost=(60, 100, 150), cac_factor=0.6,
               recall=(0.25, 0.45, 0.65), eff={"truck": (0.3, 0.5, 0.7), "proc": (0.1, 0.2, 0.4), "cont": (0, 0, 0)},
               combine_with="K4", alarms=(30, 15, 8)),
    "B1": dict(name="Thermische camera laadbak (per wagen)", unit="wagen", cpu=(200, 400, 800),
               hw=(3000, 5000, 8000), install=(500, 1000, 2000), conn_pm=(5, 10, 20),
               maint_rate=(0.05, 0.10, 0.15), maint_cost=(300, 500, 800), cac_factor=1.0,
               recall=(0.8, 0.9, 0.95),            # detectie van brand in de laadbak
               eff={"truck": (0.4, 0.6, 0.8), "proc": (0.1, 0.2, 0.4), "cont": (0, 0, 0)}, proc_factor=0.5,  # schadebeperking
               alarms=(0.5, 0.3, 0.2)),
    # FASE 2 varianten voor betaalmodel (niet in A5-BOM; afgeleid) [A]
    "K4add": dict(name="K4 als add-on op bestaande vulgraad-/zuilmodule", unit="container", cpu=(1, 1, 1),
               hw=(27, 40, 57),                       # alleen sensoren uit BOM_K4 (IR 8x8 + CO + NTC/RH)
               install=(0, 10, 20), conn_pm=(0.05, 0.1, 0.2), cloud_included=True, maint_y=(2, 4, 8),
               maint_rate=(0, 0, 0), maint_cost=(0, 0, 0), nre=(15000, 25000, 40000),
               cac_factor=0.1, support_factor=0.2,       # verkocht door vulgraad-/zuilleverancier
               recall=(0.6, 0.8, 0.9), event_only=True,
               eff={"truck": (0.0, 0.3, 0.6), "proc": (0.0, 0.3, 0.6), "cont": (0.2, 0.4, 0.6)},
               alarms=(3, 1, 0.5)),
    "B1oem": dict(name="B1 als fabrieksoptie in voertuigaanbesteding", unit="wagen", cpu=(500, 300, 200),
               hw=(700, 2050, 4800), install=(100, 200, 400), conn_pm=(5, 10, 20), cloud_included=True,
               maint_y=(100, 200, 400), maint_rate=(0, 0, 0), maint_cost=(0, 0, 0), nre=(5000, 15000, 30000),
               cac_factor=0.1, support_factor=0.3, proc_factor=0.5,
               recall=(0.8, 0.9, 0.95), eff={"truck": (0.4, 0.6, 0.8), "proc": (0.1, 0.2, 0.4), "cont": (0, 0, 0)},
               alarms=(0.5, 0.3, 0.2)),
    "B0": dict(name="Accu-brievenbus + steekproefsortering", unit="container", cpu=(1, 1, 1),
               hw=(50, 100, 200), install=(20, 40, 80), conn_pm=(0, 0, 0),
               maint_rate=(0.05, 0.10, 0.15), maint_cost=(30, 50, 80), cac_factor=0.5,
               opex_y=(20, 40, 80),                 # legen brievenbus per jaar (via OPEN-inzamelnet) [A]
               sorting_y_per_customer=(10_000, 20_000, 50_000),
               prevalence_reduction=(0.03, 0.08, 0.15),   # deel Li-energie dat uit restafval verdwijnt [A]
               alarms=(0, 0, 0)),
}

# ------------------------------------------------------------------ inlezen FASE 2

def _num(x):
    try:
        return float(str(x).replace("€", "").replace(",", ".").strip())
    except ValueError:
        return None


def load_bom(concepts, bom_dir=os.path.join(ROOT, "product")):
    """FASE 2: lees A5-BOM. Voorkeur product/BOM_samenvatting.csv (kolommen hw_*, installatie_*, per_maand_*,
    per_jaar_*, eenmalig_*, containers_per_unit_*); anders TOTAAL_*-rijen in product/BOM_<ID>.csv.
    Zet hw, install, conn_pm (= connectiviteit + cloud), maint_y, nre en cpu. Retourneert ingelezen ID's."""
    used = []
    def apply(cid, d, src):
        c = concepts[cid]
        if "hw" in d: c["hw"] = d["hw"]
        if "installatie" in d: c["install"] = d["installatie"]
        if "per_maand" in d: c["conn_pm"] = d["per_maand"]; c["cloud_included"] = True
        if "per_jaar" in d: c["maint_y"] = d["per_jaar"]
        if "eenmalig" in d: c["nre"] = d["eenmalig"]
        if "containers_per_unit" in d and c["unit"] != "container":
            c["cpu"] = d["containers_per_unit"]
        c["hw_source"] = src
        used.append(cid)
    p = os.path.join(bom_dir, "BOM_samenvatting.csv")
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding="utf-8")):
            cid = r["concept"].strip()
            if cid not in concepts: continue
            d = {}
            for k in ("hw", "installatie", "per_maand", "per_jaar", "eenmalig", "containers_per_unit"):
                vals = [_num(r.get(f"{k}_{s}", "")) for s in S]
                if all(v is not None for v in vals): d[k] = tuple(vals)
            apply(cid, d, "product/BOM_samenvatting.csv")
    for cid in concepts:
        if cid in used: continue
        p = os.path.join(bom_dir, f"BOM_{cid}.csv")
        if not os.path.exists(p): continue
        d = {}
        for r in csv.DictReader(open(p, encoding="utf-8")):
            post = r.get("post", "")
            if post.startswith("TOTAAL_"):
                k = post[len("TOTAAL_"):]
                k = {"hw": "hw", "installatie": "installatie", "per_maand": "per_maand", "per_jaar": "per_jaar", "eenmalig": "eenmalig"}.get(k)
                if k: d[k] = tuple(_num(r[s]) for s in S)
            if post.lower().startswith("containers per unit"):
                d["containers_per_unit"] = tuple(_num(r[s]) for s in S)
        if d: apply(cid, d, p.replace(ROOT + "/", ""))
    return used


def load_mc(concepts, glob):
    """Neem recall, meldingen en vermeden-brandfractie over uit A6-MC als die er is."""
    for p in (os.path.join(ROOT, "experiments", "r3_classificatie", "mc_results.json"),
              os.path.join(OUT, "mc_input.json")):
        if os.path.exists(p):
            try:
                mc = json.load(open(p))
            except Exception:
                continue
            used = []
            items = []
            for cid, d in mc.items():
                if not isinstance(d, dict) or cid.startswith("_"): continue
                if cid == "K3": items += [("K3a", d), ("K3b", d)]
                elif cid == "B1": items += [("B1", d), ("B1oem", d)]
                else: items.append((cid, d))
            for cid, d in items:
                if cid not in concepts or cid in ("B0",):   # B0 = preventie, eigen model (zie RESULTATEN)
                    continue
                c = concepts[cid]
                if cid == "K4":   # A6: 0 wagenbranden; A7 houdt event-model voor container-starts aan
                    if "fires_per_1000_containers_year" in d: glob["fires_per_1000_cy"] = tuple(d["fires_per_1000_containers_year"])
                    c["mc_source"] = p.replace(ROOT + "/", ""); c["mc_note"] = "A6 avoided=0 (wagen); A7 event-model"; used.append(cid)
                    continue
                if d.get("recall_energy") and None not in d["recall_energy"]: c["recall"] = tuple(d["recall_energy"])
                if d.get("alarms_per_1000_emptyings") and None not in d["alarms_per_1000_emptyings"]:
                    c["alarms"] = tuple(d["alarms_per_1000_emptyings"])
                if "avoided_fire_fraction" in d:
                    af = tuple(d["avoided_fire_fraction"])
                    if cid == "K3b": af = tuple(a / c["cpu"][1] for a in af)   # rouleert: dekt 1/cpu tegelijk
                    c["avoided_fraction"] = af
                if "fires_per_1000_containers_year" in d: glob["fires_per_1000_cy"] = tuple(d["fires_per_1000_containers_year"])
                c["mc_source"] = p.replace(ROOT + "/", "")
                used.append(cid)
            return used
    return []

# ------------------------------------------------------------------ kosten

def cost_pm(c, n, s, g=GLOBAL):
    """Kostprijs leverancier per container per maand, uitgesplitst. n = aantal containers bij klant(en)."""
    i = S.index(s)
    L = g["life_y"]
    cpu = c["cpu"][1] if c["unit"] in ("wagen", "pool") else 1     # containers per eenheid (basis)
    units = max(1.0, n / cpu)
    sc = g["hw_scale"][n]
    hw = c["hw"][i] * sc
    inst = c["install"][i] * (1.0 if n == 100 else 0.85)
    per_unit_y = {
        "hardware": hw / L,
        "installatie": inst / L,
        "connectiviteit": c["conn_pm"][i] * 12,
        "cloud": 0.0 if c.get("cloud_included") else g["cloud_pm"][i] * {100: 3, 1000: 1.5, 10000: 1}[n] * 12,
        "onderhoud": c["maint_y"][i] if "maint_y" in c else c["maint_rate"][i] * c["maint_cost"][i],
    }
    if "moves_per_y" in c and "maint_y" not in c:
        per_unit_y["onderhoud"] += c["moves_per_y"][i] * c["move_cost"][i]
    if "opex_y" in c and "maint_y" not in c:
        per_unit_y["onderhoud"] += c["opex_y"][i]
    out = {k: v * units / n / 12 for k, v in per_unit_y.items()}
    fixed = (g["support_fixed_y"][n] + g["support_per_unit_y"][c["unit"]] * units) * [0.7, 1, 1.4][i] * c.get("support_factor", 1.0)
    if c.get("unit") == "container" and "sorting_y_per_customer" in c:
        fixed = 0.5 * fixed + g["customers"][n] * c["sorting_y_per_customer"][i]
    out["support"] = fixed / n / 12
    out["NRE"] = c.get("nre", (0, 0, 0))[i] / L / n / 12          # eenmalig (certificering/OEM-adapter), verdeeld over installed base n
    out["CAC"] = g["customers"][n] * g["cac_per_customer"][i] * c["cac_factor"] / L / n / 12
    if c.get("combine_with"):
        out["support"] *= 1.3   # K5: K4-hardware zit al in hw/install; twee kanalen = 30 % meer support [A]
    out["kostprijs"] = sum(out.values())
    return out

# ------------------------------------------------------------------ waarde

def damage_profile(s, g):
    i = S.index(s)
    return dict(rate=g["fires_per_1000_cy"][i] / 1000.0, truck=g["dmg_truck"][i], proc=g["dmg_processor"][i],
                cont=g["dmg_container"][i], pcs=g["p_container_start"][i])


def avoided_y(c, s, g, cid=None):
    """Vermeden schade per container per jaar, per drager (gemeente/eigenaar container, inzamelaar, verwerker)."""
    i = S.index(s)
    d = damage_profile(s, g)
    gross = {"container": d["rate"] * d["pcs"] * d["cont"],
             "inzamelaar": d["rate"] * d["truck"],
             "verwerker": d["rate"] * d["proc"]}
    if "prevalence_reduction" in c:                        # B0
        f = c["prevalence_reduction"][i]
        return {k: v * f for k, v in gross.items()}, gross
    if "avoided_fraction" in c:                            # direct uit MC (fractie wagenbranden vermeden)
        f = c["avoided_fraction"][i]
        pf = c.get("proc_factor", 1.0)                     # zelfde fractie bij verwerker (zuil: container apart) [A]
        return {"container": 0.0, "inzamelaar": gross["inzamelaar"] * f, "verwerker": gross["verwerker"] * f * pf}, gross
    r = c["recall"][i]
    if c.get("coverage_is_fraction"):
        r = r / c["cpu"][1]
    eff = c["eff"]
    share = d["pcs"] if c.get("event_only") else 1.0
    av = {"container": gross["container"] / max(d["pcs"], 1e-9) * share * r * eff["cont"][i] if c.get("event_only") else 0.0,
          "inzamelaar": gross["inzamelaar"] * share * r * eff["truck"][i],
          "verwerker": gross["verwerker"] * share * r * eff["proc"][i]}
    if c.get("event_only"):
        av["container"] = gross["container"] * r * eff["cont"][i]
    if c.get("combine_with"):
        a2, _ = avoided_y(CONCEPTS_CUR[c["combine_with"]], s, g)
        av = {k: av[k] + a2[k] * (1 - r) for k in av}      # K4 vangt deel dat K2 mist
    return av, gross


def alarm_cost_y(c, s, g):
    i = S.index(s)
    return c["alarms"][i] / 1000.0 * g["emptyings_per_year"] * g["cost_per_alarm"][i]

# ------------------------------------------------------------------ run

CONCEPTS_CUR = CONCEPTS


def run(overrides=None, write=True):
    global CONCEPTS_CUR
    concepts = copy.deepcopy(CONCEPTS)
    g = copy.deepcopy(GLOBAL)
    bom_used = load_bom(concepts)
    mc_used = load_mc(concepts, g)
    if overrides:
        for k, v in overrides.items():
            if k in concepts: concepts[k].update(v)
            else: g[k] = v
    CONCEPTS_CUR = concepts
    res = {"bom_used": bom_used, "mc_used": mc_used, "concepts": {}}
    for cid, c in concepts.items():
        r = {"name": c["name"], "cost_pm": {}, "price_pm": {}, "avoided_y": {}, "alarm_cost_y": {}, "tco6_per_1000": {}}
        for n in SCALES:
            r["cost_pm"][n] = {s: cost_pm(c, n, s, g) for s in S}
            r["price_pm"][n] = {s: r["cost_pm"][n][s]["kostprijs"] / (1 - g["gross_margin"]) for s in S}
        for s in S:
            av, gross = avoided_y(c, s, g)
            r["avoided_y"][s] = av
            r["gross_y"] = gross if s == "basis" else r.get("gross_y")
            r["alarm_cost_y"][s] = alarm_cost_y(c, s, g)
        # TCO 6 jaar voor klant met 1.000 containers (prijs incl. marge + kosten vervolgacties)
        for s in S:
            r["tco6_per_1000"][s] = (r["price_pm"][1000][s] * 12 + r["alarm_cost_y"][s]) * g["life_y"] * 1000
        # business case per container per jaar: pessimistisch = hoge kosten + lage waarde
        def bc(cost_s, val_s):
            cost = r["price_pm"][1000][cost_s] * 12 + r["alarm_cost_y"][cost_s]
            val = sum(r["avoided_y"][val_s].values())
            return dict(cost_y=cost, avoided_y=val, net_y=val - cost, ratio=val / cost if cost else float("inf"))
        # break-even: max abonnementsprijs (per container per maand) en benodigde brandfrequentie
        r["max_price_pm_basis"] = max(0.0, (sum(r["avoided_y"]["basis"].values()) - r["alarm_cost_y"]["basis"]) / 12)
        rate_b = g["fires_per_1000_cy"][1]
        cost_b = r["price_pm"][1000]["basis"] * 12 + r["alarm_cost_y"]["basis"]
        av_b = sum(r["avoided_y"]["basis"].values())
        r["breakeven_fires_per_1000_cy"] = (cost_b / av_b * rate_b) if av_b > 0 else float("inf")
        if c["unit"] in ("wagen", "pool"):
            r["price_per_unit_pm_1000"] = {s_: r["price_pm"][1000][s_] * c["cpu"][1] for s_ in S}
        r["business_case_1000"] = {"pessimistisch": bc("hoog", "laag"), "basis": bc("basis", "basis"),
                                   "optimistisch": bc("laag", "hoog")}
        res["concepts"][cid] = r
    res["global"] = {k: (v if not isinstance(v, dict) else {str(a): b for a, b in v.items()}) for k, v in g.items()}
    if write:
        _write(res, concepts, g)
    return res

# ------------------------------------------------------------------ output

def payers_table(res):
    """Per betaler: welk deel van de vermeden schade (basis) valt bij hem, en ROI als hij het hele abonnement betaalt."""
    rows = []
    for cid, r in res["concepts"].items():
        av = r["avoided_y"]["basis"]; tot = sum(av.values())
        cost = r["price_pm"][1000]["basis"] * 12 + r["alarm_cost_y"]["basis"]
        rows.append((cid, av["container"], av["inzamelaar"], av["verwerker"], tot, cost))
    return rows


def _write(res, concepts, g):
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=float)
    L = []
    L.append(f"BOM uit A5 gebruikt voor: {res['bom_used'] or 'geen (eigen schattingen)'}; MC uit A6 gebruikt voor: {res['mc_used'] or 'geen (placeholders)'}\n")
    L.append("## Kostprijs en prijs per container per maand (EUR, basis; [laag–hoog])\n")
    L.append("| Concept | kost 100 | kost 1.000 | kost 10.000 | prijs 1.000 (40 % marge) | prijs 10.000 |")
    L.append("|---|---|---|---|---|---|")
    for cid, r in res["concepts"].items():
        cp = r["cost_pm"]; pp = r["price_pm"]
        f = lambda d: f"{d['basis']['kostprijs']:.2f} [{d['laag']['kostprijs']:.1f}–{d['hoog']['kostprijs']:.1f}]"
        L.append(f"| {cid} {r['name']} | {f(cp[100])} | {f(cp[1000])} | {f(cp[10000])} | "
                 f"{pp[1000]['basis']:.2f} [{pp[1000]['laag']:.1f}–{pp[1000]['hoog']:.1f}] | {pp[10000]['basis']:.2f} |")
    L.append("\n## Opbouw kostprijs bij 1.000 containers (basis, EUR/container/maand)\n")
    keys = ["hardware", "installatie", "connectiviteit", "cloud", "onderhoud", "support", "NRE", "CAC", "kostprijs"]
    L.append("| Concept | " + " | ".join(keys) + " |"); L.append("|---" * (len(keys) + 1) + "|")
    for cid, r in res["concepts"].items():
        L.append(f"| {cid} | " + " | ".join(f"{r['cost_pm'][1000]['basis'][k]:.2f}" for k in keys) + " |")
    L.append("\n## Business case per container per jaar, klant met 1.000 containers (EUR)\n")
    L.append("| Concept | abonnement + vervolgacties (basis) | vermeden schade laag / basis / hoog | ratio basis | ratio pessimistisch / optimistisch | TCO 6 jr per 1.000 (basis) | knock-out (ratio basis < 1) |")
    L.append("|---|---|---|---|---|---|---|")
    for cid, r in res["concepts"].items():
        b = r["business_case_1000"]
        av = [sum(r["avoided_y"][s].values()) for s in S]
        L.append(f"| {cid} | {b['basis']['cost_y']:.0f} | {av[0]:.1f} / {av[1]:.1f} / {av[2]:.0f} | {b['basis']['ratio']:.2f} | "
                 f"{b['pessimistisch']['ratio']:.3f} / {b['optimistisch']['ratio']:.2f} | {r['tco6_per_1000']['basis']/1e3:.0f}k | {'JA' if b['basis']['ratio'] < 1 else 'nee'} |")
    L.append("\n## Break-even (basis)\n")
    L.append("| Concept | max. prijs die vermeden schade dekt (EUR/container/mnd) | idem zonder kosten vervolgacties | kosten vervolgacties EUR/container/jr | benodigde brandfrequentie voor ratio 1 (per 1.000 containerjaar; gebruikt: " + " / ".join(f"{v:.2f}" for v in g["fires_per_1000_cy"]) + ") |")
    L.append("|---|---|---|---|---|")
    for cid, r in res["concepts"].items():
        extra = f" (prijs per eenheid {r['price_per_unit_pm_1000']['basis']:.0f} EUR/mnd)" if "price_per_unit_pm_1000" in r else ""
        L.append(f"| {cid}{extra} | {r['max_price_pm_basis']:.2f} | {sum(r['avoided_y']['basis'].values())/12:.2f} | {r['alarm_cost_y']['basis']:.1f} | {r['breakeven_fires_per_1000_cy']:.0f} |")
    L.append("\n## Wie heeft de baat? (basis, EUR per container per jaar vermeden)\n")
    L.append("| Concept | gemeente/eigenaar container | inzamelaar (wagen) | verwerker/verzekeraar (AVI) | totaal | kosten | aandeel verwerker |")
    L.append("|---|---|---|---|---|---|---|")
    for cid, a, b_, c_, t, cost in payers_table(res):
        L.append(f"| {cid} | {a:.2f} | {b_:.2f} | {c_:.2f} | {t:.2f} | {cost:.0f} | {c_/t*100 if t else 0:.0f} % |")
    open(os.path.join(OUT, "tables.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))
    _figs(res)
    _figs_deck(res)


def _figs(res):
    ids = list(res["concepts"].keys())
    # fig 1: kostprijs per container per maand vs schaal, plus vermeden schade-band
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    x = np.arange(len(ids)); w = 0.26
    for j, n in enumerate(SCALES):
        b = [res["concepts"][c]["cost_pm"][n]["basis"]["kostprijs"] for c in ids]
        lo = [res["concepts"][c]["cost_pm"][n]["laag"]["kostprijs"] for c in ids]
        hi = [res["concepts"][c]["cost_pm"][n]["hoog"]["kostprijs"] for c in ids]
        ax[0].bar(x + (j - 1) * w, b, w, yerr=[np.subtract(b, lo), np.subtract(hi, b)], capsize=2, label=f"{n} containers")
    av = [sum(res["concepts"][c]["avoided_y"]["basis"].values()) / 12 for c in ids]
    ax[0].scatter(x, av, marker="D", color="k", zorder=5, label="vermeden schade (basis) /mnd")
    ax[0].set_yscale("log"); ax[0].set_xticks(x); ax[0].set_xticklabels(ids)
    ax[0].set_ylabel("EUR per container per maand (log)"); ax[0].set_title("Kostprijs leverancier vs vermeden schade")
    ax[0].legend(fontsize=8)
    keys = ["hardware", "installatie", "connectiviteit", "cloud", "onderhoud", "support", "NRE", "CAC"]
    bottom = np.zeros(len(ids))
    for k in keys:
        v = np.array([res["concepts"][c]["cost_pm"][1000]["basis"][k] for c in ids])
        ax[1].bar(x, v, 0.6, bottom=bottom, label=k); bottom += v
    ax[1].set_yscale("symlog", linthresh=1); ax[1].set_xticks(x); ax[1].set_xticklabels(ids)
    ax[1].set_title("Opbouw kostprijs bij 1.000 containers (basis)"); ax[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_unit_economics.png"), dpi=130); plt.close(fig)
    # fig 2: business case ratio en baat per drager
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    for j, sc in enumerate(["pessimistisch", "basis", "optimistisch"]):
        ax[0].bar(x + (j - 1) * w, [res["concepts"][c]["business_case_1000"][sc]["ratio"] for c in ids], w, label=sc)
    ax[0].axhline(1, color="k", ls="--", lw=1); ax[0].set_yscale("log")
    ax[0].set_xticks(x); ax[0].set_xticklabels(ids); ax[0].set_ylabel("vermeden schade / (abonnement + acties)")
    ax[0].set_title("Business case (klant 1.000 containers)"); ax[0].legend(fontsize=8)
    bottom = np.zeros(len(ids))
    for k, lab in [("container", "gemeente/eigenaar"), ("inzamelaar", "inzamelaar"), ("verwerker", "verwerker/verzekeraar")]:
        v = np.array([res["concepts"][c]["avoided_y"]["basis"][k] for c in ids])
        ax[1].bar(x, v, 0.6, bottom=bottom, label=lab); bottom += v
    ax[1].set_xticks(x); ax[1].set_xticklabels(ids); ax[1].set_ylabel("EUR per container per jaar")
    ax[1].set_title("Wie heeft de vermeden schade? (basis)"); ax[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_business_case.png"), dpi=130); plt.close(fig)


def _figs_deck(res):
    ids = list(res["concepts"].keys())
    x = np.arange(len(ids))
    # fig_prijs_vs_schade: abonnementsprijs (1.000 containers, basis, band laag-hoog) vs vermeden schade per maand
    fig, ax = plt.subplots(figsize=(10, 5))
    pb = np.array([res["concepts"][c]["price_pm"][1000]["basis"] for c in ids])
    pl = np.array([res["concepts"][c]["price_pm"][1000]["laag"] for c in ids])
    ph = np.array([res["concepts"][c]["price_pm"][1000]["hoog"] for c in ids])
    ax.errorbar(x - 0.12, pb, yerr=[pb - pl, ph - pb], fmt="s", ms=8, capsize=4, color="#c0392b", label="abonnementsprijs (1.000 containers, 40 % marge)")
    ab = np.array([sum(res["concepts"][c]["avoided_y"]["basis"].values()) / 12 for c in ids])
    al = np.array([sum(res["concepts"][c]["avoided_y"]["laag"].values()) / 12 for c in ids])
    ah = np.array([sum(res["concepts"][c]["avoided_y"]["hoog"].values()) / 12 for c in ids])
    ax.errorbar(x + 0.12, np.maximum(ab, 1e-4), yerr=[np.maximum(ab, 1e-4) - np.maximum(al, 1e-5), ah - ab], fmt="o", ms=8, capsize=4,
                color="#27ae60", label="vermeden schade (laag–basis–hoog brandkans)")
    ax.set_yscale("log"); ax.set_xticks(x); ax.set_xticklabels(ids)
    ax.set_ylabel("EUR per container per maand (log)")
    ax.set_title("Abonnementsprijs vs vermeden schade per container")
    ax.grid(axis="y", which="both", alpha=0.3); ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_prijs_vs_schade.png"), dpi=140); plt.close(fig)
    # fig_schaal: kostprijs en marge bij 100/1.000/10.000
    fig, ax = plt.subplots(figsize=(11, 5))
    w = 0.26
    for j, n in enumerate(SCALES):
        cost = np.array([res["concepts"][c]["cost_pm"][n]["basis"]["kostprijs"] for c in ids])
        price = np.array([res["concepts"][c]["price_pm"][n]["basis"] for c in ids])
        ax.bar(x + (j - 1) * w, cost, w, color=f"C{j}", label=f"kostprijs {n}")
        ax.bar(x + (j - 1) * w, price - cost, w, bottom=cost, color=f"C{j}", alpha=0.35, hatch="//", label=f"marge {n}")
    ax.set_yscale("log"); ax.set_xticks(x); ax.set_xticklabels(ids)
    ax.set_ylim(0.3, None); ax.set_ylabel("EUR per container per maand (log)"); ax.set_title("Schaaleffect: kostprijs + marge bij 100 / 1.000 / 10.000 containers")
    ax.legend(ncol=3, fontsize=8); ax.grid(axis="y", which="both", alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_schaal.png"), dpi=140); plt.close(fig)


if __name__ == "__main__":
    run()
