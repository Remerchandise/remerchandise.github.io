"""Deck-grafieken (Orchestrator). Leest uitsluitend resultaten uit experiments/ en product/.

Draai vanuit repo-root: python3 deck/charts.py  ->  deck/charts/*.png
Eén stijl voor alle grafieken: grijs = context, ember = boodschap.
"""
import csv, json, math, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "deck", "charts")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(ROOT, "experiments", "common"))
import params  # noqa: E402

INK, MUTED, GRID = "#1F2328", "#5F646A", "#E3E5E8"
GRAY, GRAY_D = "#B9BEC4", "#7D848B"
EMBER, EMBER_L = "#D9481C", "#F2A07F"
TEAL = "#1F7A6D"
GOOD, WARN, CRIT = "#2E8B57", "#E39B00", "#C8312F"

plt.rcParams.update({
    "font.family": "Carlito", "font.size": 13, "axes.edgecolor": GRID,
    "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "axes.axisbelow": True, "figure.dpi": 200, "savefig.bbox": "tight",
    "savefig.pad_inches": 0.08, "axes.titlesize": 14, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "axes.titlelocation": "left", "legend.frameon": False,
})


def J(path):
    return json.load(open(os.path.join(ROOT, path)))


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


NL = {"knoopcel": "Knoopcel", "vape": "Vape", "li_klein_overig": "Oortjes/watch",
      "cel_18650": "Losse 18650", "telefoon": "Telefoon", "powerbank": "Powerbank",
      "laptop_gereedschap": "Laptop/gereedschap", "ebike_step": "E-bike/step",
      "blik": "Blikje", "folie": "Aluminiumfolie", "sleutel_klein_metaal": "Sleutels/klein metaal",
      "pan_gereedschap": "Pan/gereedschap", "alkaline": "Alkaline AA/AAA",
      "elektronica_zonder_accu": "Elektronica zonder accu"}


# 1. Pareto: aandeel items vs aandeel risico ------------------------------------
def c_pareto():
    p = J("experiments/r3_risico/resultaten.json")["pareto_basis"]
    keys = [k for k in NL if k in p]
    keys.sort(key=lambda k: p[k]["share_wheq"])
    y = np.arange(len(keys))
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.barh(y + 0.2, [p[k]["share_items"] * 100 for k in keys], 0.38, color=GRAY, label="aandeel Li-items")
    ax.barh(y - 0.2, [p[k]["share_wheq"] * 100 for k in keys], 0.38, color=EMBER, label="aandeel risico (Wh-eq)")
    ax.set_yticks(y, [NL[k] for k in keys])
    ax.set_xlabel("% van alle Li-items in restafval (basis)")
    ax.grid(axis="y", visible=False)
    for i, k in enumerate(keys):
        ax.text(p[k]["share_wheq"] * 100 + 0.6, i - 0.2, f"{p[k]['share_wheq']*100:.0f}%", va="center", color=INK, fontsize=11)
    ax.legend(loc="lower right")
    save(fig, "c01_pareto.png")


# 2. Brandkans per container vs Wh-eq, met drempels ------------------------------
def c_brandkans():
    R = np.logspace(0, 3, 200)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    th = params.THRESH_CONTAINER
    ax.axvspan(1, th["oranje"], color=GOOD, alpha=0.08)
    ax.axvspan(th["oranje"], th["rood"], color=WARN, alpha=0.10)
    ax.axvspan(th["rood"], 1000, color=CRIT, alpha=0.08)
    for lab, col, ls in [("hoog", EMBER, "-"), ("basis", INK, "-"), ("laag", GRAY_D, "--")]:
        k = params.K_PER_WHEQ[lab]
        ax.plot(R, (1 - np.exp(-k * R)) * 1e3, color=col, lw=2, ls=ls, label=f"k {lab}")
    ax.axvline(15.7, color=MUTED, lw=1, ls=":")
    ax.text(16.5, 7, "gemiddelde\nlediging\n≈ 16 Wh-eq", color=MUTED, fontsize=10, va="top")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(1, 1000); ax.set_ylim(1e-4, 30)
    ax.set_xlabel("Risico-energie in container sinds lediging (Wh-eq, log)")
    ax.set_ylabel("Brandkans per lediging (‰, log)")
    for x, t, c in [(7, "groen", GOOD), (85, "oranje", WARN), (380, "rood", CRIT)]:
        ax.text(x, 15, t, color=c, fontsize=12, fontweight="bold", ha="center")
    ax.legend(loc="lower right")
    save(fig, "c02_brandkans.png")


# 3. Inductie: detectiekans in een echte zak per itemklasse ----------------------
def c_inductie():
    m = J("experiments/r3_inductie/sensor_model_K1.json")["p_out_given_item_in_bag"]
    keys = [k for k in NL if k in m]
    val = {k: (m[k][1] + m[k][2]) * 100 for k in keys}
    keys.sort(key=lambda k: val[k])
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    cols = [EMBER if params.ITEMS[k]["li"] else GRAY for k in keys]
    ax.barh(range(len(keys)), [val[k] for k in keys], color=cols, height=0.65)
    ax.set_yticks(range(len(keys)), [NL[k] for k in keys])
    ax.grid(axis="y", visible=False)
    for i, k in enumerate(keys):
        ax.text(val[k] + 0.8, i, f"{val[k]:.0f}%", va="center", fontsize=10.5, color=INK)
    clutter = J("experiments/r3_inductie/sensor_model_K1.json").get("clutter_bag", {}).get("p_out")
    if clutter:
        fa = (clutter[1] + clutter[2]) * 100
        ax.axvline(fa, color=INK, lw=1.2, ls="--")
        ax.text(fa + 0.8, 0.2, f"vals alarm zak\nzonder Li: {fa:.0f}%", fontsize=10, color=INK)
    ax.set_xlabel("Kans op melding 'cel/pakket' als item in een gewone zak zit (K1, VLF)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=EMBER, label="lithium"), Patch(color=GRAY, label="geen lithium")], loc="lower right")
    save(fig, "c03_inductie.png")


# 4. Röntgen: transmissie per object -------------------------------------------
def c_rontgen():
    objs = [("18650", 7.1e-13, True), ("AA alkaline", 2.4e-13, False), ("Sleutel messing", 7.4e-11, False),
            ("Vape", 1.0e-7, True), ("Telefoon (pouch)", 2.6e-4, True), ("Staalblik", 2.2e-2, False),
            ("Glazen fles", 8.6e-2, False), ("Al-blikje", 0.90, False), ("Al-folieprop", 0.93, False)]
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    y = np.arange(len(objs))[::-1]
    ax.barh(y, [o[1] for o in objs], color=[EMBER if o[2] else GRAY for o in objs], height=0.62, left=1e-14)
    ax.set_xscale("log"); ax.set_xlim(1e-14, 2)
    ax.set_yticks(y, [o[0] for o in objs]); ax.grid(axis="y", visible=False)
    ax.axvline(1e-4, color=INK, lw=1, ls="--")
    ax.text(1.3e-4, 8.3, "≈ zwart", fontsize=10, color=INK)
    ax.set_xlabel("Relatieve transmissie achter zak van 10 g/cm² bij 30 kV (log)")
    save(fig, "c04_rontgen_transmissie.png")


def c_rontgen_tijd():
    dens = [2, 5, 10, 13]
    series = {"Goedkoop: RPi-camera, 4 W": [0.58, 4.48, 30, 30],
              "Lijnarray CsI, 4 W": [0.12, 0.77, 10.78, 30],
              "4/3\"-camera f/0,95, 4 W": [0.10, 0.18, 2.50, 14.44]}
    cols = [EMBER, GRAY_D, INK]
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    for (lab, v), c in zip(series.items(), cols):
        ax.plot(dens, v, "-o", color=c, lw=2, ms=7, label=lab)
    ax.axhline(30, color=MUTED, lw=1, ls=":")
    ax.text(2.1, 22, "> 30 s: niet haalbaar\nin de trommel", color=MUTED, fontsize=10)
    ax.set_yscale("log"); ax.set_ylim(0.08, 45)
    ax.set_xlabel("Massa van de zak per oppervlak (g/cm²)")
    ax.set_ylabel("Benodigde stilstand (s, log)")
    ax.legend(loc="lower right", fontsize=11)
    save(fig, "c05_rontgen_tijd.png")


# 5. Tijdlijn: waarschuwingsvenster vóór thermal runaway -----------------------
def c_tijdlijn():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "experiments/r3_thermisch/tijdlijn_TR.csv"))))
    lab = {"Extern oververhitten (zon/compost >> 60 °C)": "Oververhitting (zon/compost)",
           "Latente interne short na valschade": "Latente short na val in zuil",
           "Crush/penetratie persplaat": "Persplaat vuilniswagen",
           "Doorboring shredder/grijper": "Shredder / grijper verwerker",
           "Overladen (BESS, referentie)": "Referentie: overladen (BESS)"}
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    for i, r in enumerate(rows[::-1]):
        lo, b, hi = (float(r[k]) / 60 for k in ("venster_l_s", "venster_b_s", "venster_h_s"))
        c = EMBER if "wagen" in r["stap"] or "verwerking" in r["stap"] else GRAY_D
        ax.plot([lo, hi], [i, i], color=c, lw=7, solid_capstyle="round", alpha=0.45)
        ax.plot(b, i, "o", color=c, ms=9)
        ax.text(hi + 0.6, i, f"{b:.0f} min" if b >= 1 else f"{b*60:.0f} s", va="center", fontsize=10.5, color=INK)
    ax.set_yticks(range(len(rows)), [lab.get(r["mechanisme"], r["mechanisme"]) for r in rows[::-1]])
    ax.grid(axis="y", visible=False)
    ax.set_xlim(-0.5, 34)
    ax.set_xlabel("Waarschuwingstijd tussen eerste meetbaar signaal en thermal runaway (min)")
    save(fig, "c06_tijdlijn.png")


# 6. Recall vs meldingen per concept --------------------------------------------
def c_recall():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "experiments/r3_classificatie/mc_container.csv"))))
    want = [("perfect (bovengrens)", "Perfecte sensor", INK, "-"), ("K3 rontgen", "K3 röntgen", TEAL, "-"),
            ("K2 pakketwachter", "K2 pakketwachter", GRAY_D, "-"), ("B0 risicokaart", "B0 geen sensor", GRAY, "--"),
            ("K1 VLF teller", "K1 strandmetaaldetector", EMBER, "-"), ("willekeurig", "Willekeurig melden", GRAY, ":")]
    xs = {"budget5": 5, "budget": 20, "budget50": 50}
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.axvspan(0, 20, color=GOOD, alpha=0.06)
    ax.text(1, 31.5, "werkbaar voor\nophaaldienst", color=GOOD, fontsize=10.5)
    for key, lab, col, ls in want:
        pts = sorted((xs[r["regel"]], float(r["energierecall"]) * 100) for r in rows
                     if r["scenario"] == "basis" and r["concept"] == key and r["regel"] in xs)
        if not pts:
            continue
        x, y = zip(*pts)
        ax.plot(x, y, ls, marker="o", color=col, lw=2.2, ms=7)
        ax.text(51.5, y[-1], lab, va="center", fontsize=11, color=INK)
    ax.set_xlim(0, 75); ax.set_ylim(0, 35)
    ax.set_xticks([5, 20, 50])
    ax.set_xlabel("Meldingen per 1.000 ledigingen (drempelkeuze)")
    ax.set_ylabel("Afgevangen risico-energie (%)")
    save(fig, "c07_recall_meldingen.png")


def c_inworp():
    rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "experiments/r3_classificatie/mc_inworp.csv")))
            if r["scenario"] == "basis" and r["sensor"] in ("K1", "K2", "K3")]
    lab = {"K1": "K1 VLF", "K2": "K2 PI", "K3": "K3 röntgen"}
    x = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    rec = [float(r["recall_li_zak"]) * 100 for r in rows]
    ppv = [float(r["ppv_li_bij_flag"]) * 100 for r in rows]
    ax.bar(x - 0.2, rec, 0.38, color=GRAY_D, label="recall: % Li-zakken gemeld")
    ax.bar(x + 0.2, ppv, 0.38, color=EMBER, label="PPV: % meldingen met Li")
    for i in range(len(rows)):
        ax.text(x[i] - 0.2, rec[i] + 1.2, f"{rec[i]:.0f}%", ha="center", fontsize=11)
        ax.text(x[i] + 0.2, ppv[i] + 1.2, f"{ppv[i]:.0f}%", ha="center", fontsize=11)
    ax.set_xticks(x, [lab[r["sensor"]] for r in rows]); ax.grid(axis="x", visible=False)
    ax.set_ylim(0, 80); ax.set_ylabel("%")
    ax.legend(loc="upper left")
    save(fig, "c08_inworp.png")


# 7. Scorekaart ------------------------------------------------------------------
def c_scores():
    rows = J("experiments/r4_scorekaart/scorekaart.json")["concepten"]
    rows.sort(key=lambda r: r["gewogen"])
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    cols = [TEAL if r["oordeel"].startswith("CONDITIONEEL") else GRAY for r in rows]
    ax.barh(range(len(rows)), [r["gewogen"] for r in rows], color=cols, height=0.62)
    ax.set_yticks(range(len(rows)), [f"{r['id']}  {r['naam'][:34]}" for r in rows], fontsize=11)
    ax.axvline(3.5, color=INK, lw=1.2, ls="--")
    ax.text(3.53, len(rows) - 0.6, "drempel\nAANBEVOLEN 3,5", fontsize=10, color=INK, va="top")
    for i, r in enumerate(rows):
        t = f"{r['gewogen']:.2f}".replace(".", ",") + ("  KO" if r["knockout"] else "")
        ax.text(r["gewogen"] + 0.05, i, t, va="center", fontsize=10.5, color=INK)
    ax.set_xlim(1, 5); ax.grid(axis="y", visible=False)
    ax.set_xlabel("Gewogen score (1–5)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=TEAL, label="conditioneel"), Patch(color=GRAY, label="niet aanbevolen")],
              loc="lower right")
    save(fig, "c09_scores.png")


# 8. Prijs per container vs vermeden schade ------------------------------------
def c_prijs_schade():
    d = J("experiments/r3_business/results.json")["concepts"]
    order = ["K3a", "K3b", "B0", "K5", "K1", "K4", "K2", "B1", "K4add", "B1oem"]
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    for i, k in enumerate(order):
        pr = d[k]["price_pm"]["1000"]
        av = {s: sum(d[k]["avoided_y"][s].values()) / 12 for s in ("laag", "basis", "hoog")}
        ax.plot([pr["laag"], pr["hoog"]], [i, i], color=EMBER_L, lw=5, solid_capstyle="round")
        ax.plot(pr["basis"], i, "o", color=EMBER, ms=9)
        ax.plot([max(av["laag"], 0.01), av["hoog"]], [i + 0.0, i + 0.0], color=GRAY, lw=1.5)
        ax.plot(max(av["basis"], 0.01), i, "D", color=INK, ms=7)
    ax.set_yticks(range(len(order)), order); ax.grid(axis="y", visible=False)
    ax.set_xscale("log"); ax.set_xlim(0.01, 300)
    ax.set_xlabel("EUR per container per maand (log), klant met 1.000 containers")
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([], [], marker="o", color=EMBER, ls="", ms=9, label="abonnementsprijs (basis, band)"),
                       Line2D([], [], marker="D", color=INK, ls="", ms=7, label="vermeden schade (basis; lijn = laag–hoog)")],
              loc="lower right", fontsize=10.5)
    save(fig, "c10_prijs_vs_schade.png")


def c_schaal():
    d = J("experiments/r3_business/results.json")["concepts"]
    n = [100, 1000, 10000]
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    for k, lab, c in [("K2", "K2 pakketwachter", GRAY_D), ("K5", "K5 hybride", GRAY),
                      ("K4add", "K4 add-on", TEAL), ("B1oem", "B1 camera wagen (OEM)", EMBER)]:
        p = [d[k]["price_pm"][str(x)]["basis"] for x in n]
        ax.plot(n, p, "-o", color=c, lw=2.2, ms=7)
        ax.text(11500, p[-1], lab, va="center", fontsize=11, color=INK)
    sch = sum(d["B1oem"]["avoided_y"]["basis"].values()) / 12
    ax.axhline(sch, color=INK, lw=1.2, ls="--")
    ax.text(110, sch * 1.12, f"vermeden schade B1 ≈ EUR {sch:.2f}".replace(".", ","), fontsize=10.5, color=INK)
    sch2 = sum(d["K2"]["avoided_y"]["basis"].values()) / 12
    ax.axhline(sch2, color=GRAY_D, lw=1, ls=":")
    ax.text(110, sch2 * 1.15, f"vermeden schade K2 ≈ EUR {sch2:.2f}".replace(".", ","), fontsize=10.5, color=GRAY_D)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(80, 60000)
    ax.set_xticks(n, ["100", "1.000", "10.000"])
    ax.set_xlabel("Aantal containers onder contract")
    ax.set_ylabel("Abonnementsprijs EUR/container/mnd (log)")
    save(fig, "c11_schaal.png")


# 9. Energie --------------------------------------------------------------------
def c_energie():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "experiments/r3_hardware/energie_tabel.csv"))))
    keys = ["K4", "K2", "K1", "K3a"]
    lab = {"K1": "K1 VLF", "K2": "K2 PI", "K3a": "K3a röntgen", "K4": "K4 IR+CO"}
    v = {k: float(next(r["mWh_per_dag"] for r in rows if r["concept"] == k and r["scenario"] == "basis"
                       and r["inworpen_per_dag"] == "80")) for k in keys}
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.barh(range(len(keys)), [v[k] for k in keys], color=[EMBER if k == "K3a" else GRAY_D for k in keys], height=0.6)
    ax.set_yticks(range(len(keys)), [lab[k] for k in keys]); ax.grid(axis="y", visible=False)
    ax.set_xscale("log"); ax.set_xlim(1, 30000)
    for i, k in enumerate(keys):
        ax.text(v[k] * 1.15, i, f"{v[k]:,.0f}".replace(",", "."), va="center", fontsize=11)
    for x, t in [(23.6, "D-cel, 5 jaar"), (750, "5 Wp paneel, dec.")]:
        ax.axvline(x, color=INK, lw=1, ls="--")
        ax.text(x * 1.1, 3.45, t, fontsize=10, color=INK)
    ax.set_xlabel("mWh per dag bij 80 inworpen (log)")
    save(fig, "c12_energie.png")


# 10. Wie heeft de baat ---------------------------------------------------------
def c_baat():
    d = J("experiments/r3_business/results.json")["concepts"]
    ks = [("B1oem", "B1 camera wagen"), ("K4add", "K4 add-on"), ("B0", "B0 preventie"), ("K2", "K2 pakketwachter")]
    parts = [("container", "gemeente (container)", TEAL), ("inzamelaar", "inzamelaar (wagen)", EMBER),
             ("verwerker", "verwerker / verzekeraar", GRAY_D)]
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    for i, (k, lab) in enumerate(ks):
        a = d[k]["avoided_y"]["basis"]; tot = sum(a.values()) or 1
        left = 0
        for key, plab, c in parts:
            w = a[key] / tot * 100
            ax.barh(i, w, left=left, color=c, height=0.6, edgecolor="white", linewidth=2, label=plab if i == 0 else None)
            if w > 8:
                ax.text(left + w / 2, i, f"{w:.0f}%", ha="center", va="center", color="white", fontsize=11, fontweight="bold")
            left += w
    ax.set_yticks(range(len(ks)), [l for _, l in ks]); ax.grid(visible=False)
    ax.set_xlim(0, 100); ax.set_xlabel("Aandeel van de vermeden schade (%)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=3, fontsize=10.5)
    save(fig, "c13_baat.png")


if __name__ == "__main__":
    for f in [c_pareto, c_brandkans, c_inductie, c_rontgen, c_rontgen_tijd, c_tijdlijn, c_recall,
              c_inworp, c_scores, c_prijs_schade, c_schaal, c_energie, c_baat]:
        f()
        print("ok", f.__name__)
