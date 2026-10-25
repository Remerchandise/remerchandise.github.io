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
               eff={"truck": (0.5, 0.7, 0.9), "proc": (0.5, 0.7, 0.9), "cont": (0.2, 0.4, 0.6)},
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
               eff={"truck": (0.4, 0.6, 0.8), "proc": (0.1, 0.2, 0.4), "cont": (0, 0, 0)},   # schadebeperking
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
    """Overschrijf hw met A5-BOM als product/BOM_<ID>.csv bestaat. Retourneert lijst van ingelezen ID's."""
    used = []
    for cid, c in concepts.items():
        for fn in (f"BOM_{cid}.csv", f"BOM_{cid.lower()}.csv"):
            p = os.path.join(bom_dir, fn)
            if not os.path.exists(p):
                continue
            with open(p, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f, delimiter=";" if ";" in f.readline() else ","))
            if not rows:
                continue
            keys = {k: k.lower() for k in rows[0].keys() if k}
            cols = {}
            for s in S:
                cand = [k for k, kl in keys.items() if kl == s or kl.endswith("_" + s) or kl.startswith(s + "_")
                        or kl == f"eur_{s}" or kl == f"prijs_{s}"]
                if cand:
                    cols[s] = cand[0]
            if len(cols) < 3:
                continue
            first = list(rows[0].keys())[0]
            tot = [r for r in rows if str(r.get(first, "")).strip().lower() in ("totaal", "total", "som")]
            if tot:
                vals = tuple(_num(tot[0][cols[s]]) for s in S)
            else:
                qty_col = next((k for k, kl in keys.items() if kl in ("aantal", "qty", "n")), None)
                vals = []
                for s in S:
                    t = 0.0
                    for r in rows:
                        v = _num(r[cols[s]])
                        q = _num(r[qty_col]) if qty_col and _num(r[qty_col]) is not None else 1.0
                        t += (v or 0) * q
                    vals.append(t)
                vals = tuple(vals)
            if all(v is not None and v > 0 for v in vals):
                c["hw"] = vals
                c["hw_source"] = p.replace(ROOT + "/", "")
                used.append(cid)
                break
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
            for cid, d in mc.items():
                if cid not in concepts or not isinstance(d, dict):
                    continue
                c = concepts[cid]
                if "recall_energy" in d: c["recall"] = tuple(d["recall_energy"])
                if "alarms_per_1000_emptyings" in d: c["alarms"] = tuple(d["alarms_per_1000_emptyings"])
                if "avoided_fire_fraction" in d: c["avoided_fraction"] = tuple(d["avoided_fire_fraction"])
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
        "cloud": g["cloud_pm"][i] * {100: 3, 1000: 1.5, 10000: 1}[n] * 12,
        "onderhoud": c["maint_rate"][i] * c["maint_cost"][i],
    }
    if "moves_per_y" in c:
        per_unit_y["onderhoud"] += c["moves_per_y"][i] * c["move_cost"][i]
    if "opex_y" in c:
        per_unit_y["onderhoud"] += c["opex_y"][i]
    out = {k: v * units / n / 12 for k, v in per_unit_y.items()}
    fixed = (g["support_fixed_y"][n] + g["support_per_unit_y"][c["unit"]] * units) * [0.7, 1, 1.4][i] * c.get("support_factor", 1.0)
    if c.get("unit") == "container" and "sorting_y_per_customer" in c:
        fixed = 0.5 * fixed + g["customers"][n] * c["sorting_y_per_customer"][i]
    out["support"] = fixed / n / 12
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
    if "avoided_fraction" in c:                            # direct uit MC
        f = c["avoided_fraction"][i]
        return {k: v * f for k, v in gross.items()}, gross
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
    keys = ["hardware", "installatie", "connectiviteit", "cloud", "onderhoud", "support", "CAC", "kostprijs"]
    L.append("| Concept | " + " | ".join(keys) + " |"); L.append("|---" * (len(keys) + 1) + "|")
    for cid, r in res["concepts"].items():
        L.append(f"| {cid} | " + " | ".join(f"{r['cost_pm'][1000]['basis'][k]:.2f}" for k in keys) + " |")
    L.append("\n## Business case per container per jaar, klant met 1.000 containers (EUR)\n")
    L.append("| Concept | abonnement + vervolgacties (basis) | vermeden schade laag / basis / hoog | ratio basis | ratio pessimistisch / optimistisch | TCO 6 jr per 1.000 (basis) |")
    L.append("|---|---|---|---|---|---|")
    for cid, r in res["concepts"].items():
        b = r["business_case_1000"]
        av = [sum(r["avoided_y"][s].values()) for s in S]
        L.append(f"| {cid} | {b['basis']['cost_y']:.0f} | {av[0]:.1f} / {av[1]:.1f} / {av[2]:.0f} | {b['basis']['ratio']:.2f} | "
                 f"{b['pessimistisch']['ratio']:.3f} / {b['optimistisch']['ratio']:.2f} | {r['tco6_per_1000']['basis']/1e3:.0f}k |")
    L.append("\n## Break-even (basis)\n")
    L.append("| Concept | max. prijs die vermeden schade dekt (EUR/container/mnd) | idem zonder kosten vervolgacties | kosten vervolgacties EUR/container/jr | benodigde brandfrequentie voor ratio 1 (per 1.000 containerjaar; A1: 0,3 / 1,7 / 15) |")
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
    keys = ["hardware", "installatie", "connectiviteit", "cloud", "onderhoud", "support", "CAC"]
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


if __name__ == "__main__":
    run()
