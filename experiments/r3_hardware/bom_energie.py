"""A5 Ronde 3: BOM per concept (product/BOM_*.csv), energiebudget (fig_energie.png) en tabellen.
Draai vanuit repo-root: python3 experiments/r3_hardware/bom_energie.py
EUR 2026 excl. btw, @1 000 st. Aannames [A] toegelicht in RESULTATEN.md en research/A5_hardware.md."""
import csv, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "experiments", "common"))
import params  # noqa: E402

OUT = os.path.join(ROOT, "experiments", "r3_hardware")
PROD = os.path.join(ROOT, "product")
os.makedirs(PROD, exist_ok=True)

# ---------------------------------------------------------------- BOM
# categorie: hw (per unit), installatie (per unit), eenmalig (totaal programma), per_maand (per unit),
#            per_jaar (per unit), dekking (containers per unit)
H, I, E, M, J, D = "hw", "installatie", "eenmalig", "per_maand", "per_jaar", "dekking"

COMMON_LINER = ("Kunststof (PE-UHMW) trommelliner + bevestiging", H, 15, 30, 60, "[A] maatwerk per trommeltype; spoel erachter (R2 A3#6)")

BOM = {
 "K1": [  # VLF strandmetaaldetector, standalone, elektronica in zuilkop (A5-C2b)
  ("DD-spoel gewikkeld + gegoten", H, 8, 12, 20, "[A] 2 spoelen Cu 0,5 mm, epoxy"),
  COMMON_LINER,
  ("VLF front-end 2-3 freq (DDS, eindtrap, lock-in ADC 24 bit)", H, 6, 10, 16, "[A] AD9833/ADS1220-klasse"),
  ("nRF9151 SiP (MCU + LTE-M/NB-IoT)", H, 12, 14, 16, "Farnell 2026: 15,57 @250"),
  ("Antenne LTE + kabel naar kunststof kap", H, 2, 3, 6, "[A]"),
  ("SIM 10 jaar (1NCE)", H, 10, 10, 15, "1NCE FAQ: EUR 10/10 j"),
  ("Li-SOCl2 LS33600 + HLC/supercap-buffer", H, 15, 20, 28, "TME 2026: 11-18,6/cel; buffer [A]"),
  ("PCB + passieven + assemblage", H, 6, 9, 14, "[A]"),
  ("Behuizing IP67/IK10 + potting + RVS-bevestiging", H, 8, 14, 22, "[A]"),
  ("Robot-flexkabel spoel-zuilkop + connector", H, 6, 10, 18, "[A] >=300k buigcycli"),
  ("Test, kalibratie, verpakking", H, 3, 5, 8, "[A]"),
  ("Installatie (liner + spoel + kop), 45-90 min + reis", I, 40, 60, 90, "[A]"),
  ("Certificering RED/CE/EMC + veldvalidatie", E, 20000, 30000, 45000, "[A]"),
  ("Connectiviteit + cloud", M, 0.1, 0.5, 1.5, "1NCE in HW; hosting [A]"),
  ("Onderhoud: celwissel /6 j + uitval 2 %/j", J, 3, 6, 12, "[A]"),
  ("Containers per unit", D, 1, 1, 1, ""),
 ],
 "K2": [  # Pakketwachter OEM-module op pas-zuil (A5-C1b)
  ("2 PI-lussen in liner (boven/onder)", H, 8, 12, 20, "[A]"),
  COMMON_LINER,
  ("PI front-end multi-gate + ferro-kanaal", H, 6, 9, 14, "[A] MOSFET, snelle opamp, 1 MS/s ADC"),
  ("STM32U5 MCU (DSP + classifier)", H, 3, 4, 6, "[A]"),
  ("OEM-interface (RS485/UART, galv. scheiding) + DC-DC 12 V", H, 3, 5, 8, "[A]; fail-open, geen slotsturing"),
  ("PCB + passieven + assemblage", H, 5, 8, 12, "[A]"),
  ("Behuizing in zuilkop IP67 + potting", H, 5, 8, 14, "[A] zuilkop beschermt al (IK)"),
  ("Robot-flexkabel lussen-zuilkop + connector", H, 6, 10, 18, "[A]"),
  ("Test, kalibratie, verpakking", H, 3, 5, 8, "[A]"),
  ("Installatie (meeliften op service toegangscontrole)", I, 30, 45, 75, "[A]"),
  ("Certificering EMC (geen radio) + OEM-integratie NRE", E, 60000, 100000, 160000, "[A] EMC 10-20k + NRE 50-150k/OEM (A7)"),
  ("Connectiviteit (meeliften op OEM-modem) + cloud", M, 0.05, 0.2, 0.5, "[A]"),
  ("Onderhoud: uitval 2 %/j, geen eigen batterij", J, 1, 2, 4, "[A]"),
  ("Containers per unit", D, 1, 1, 1, ""),
  ("OPTIE standalone: nRF9151 + SIM + antenne + LS33600 + buffer", "optie_hw", 39, 47, 65, "zie K1-regels"),
 ],
 "K3a": [  # Röntgen-schaduwdoos vast per zuil
  ("Mini-röntgenbuis <=30 kV + HV-voeding", H, 300, 700, 1500, "A3 R1 [A]"),
  ("GOS-scherm 35x43 cm", H, 80, 150, 300, "[A]"),
  ("Camera 12 MP + optiek/spiegel", H, 40, 80, 150, "[A]"),
  ("Compute (STM32N6 of CM5) i.p.v. RPi", H, 15, 40, 80, "[A]"),
  ("Afscherming + interlock (veiligheids-PLC-relais)", H, 100, 250, 600, "[A]"),
  ("PE/CFRP-vensters in dubbele RVS-trommel", H, 40, 80, 150, "[A] R2a A5"),
  ("Energie: LiFePO4 200 Wh verwarmd + 30-50 Wp + laadregelaar", H, 120, 185, 305, "[A]"),
  ("LTE-M modem + antenne + SIM", H, 25, 30, 40, "[A]"),
  ("Behuizing/mechaniek IP67", H, 80, 150, 300, "[A]"),
  ("Assemblage + test", H, 60, 120, 250, "[A]"),
  ("Installatie + stralingsmeting oplevering", I, 400, 650, 1100, "[A]"),
  ("Certificering (RED/EMC, LVD, Bbs-dossier/typekeur)", E, 40000, 80000, 150000, "[A]"),
  ("Connectiviteit + cloud (beelden)", M, 1, 2, 4, "[A]"),
  ("Onderhoud: jaarlijkse dosiscontrole, accu /5 j, buis /8 j", J, 120, 220, 400, "[A]"),
  ("Containers per unit", D, 1, 1, 1, ""),
 ],
 "K4": [  # Deksel-eventmodule aan de container (eigen batterij)
  ("Thermopile-array 8x8 (AMG8833-klasse)", H, 15, 22, 30, "[A]"),
  ("Elektrochemische CO-cel (TGS5042-klasse) + bias", H, 10, 15, 22, "[A]"),
  ("2x NTC (binnen/buiten) + RH-sensor", H, 2, 3, 5, "[A]"),
  ("Radio+MCU: STM32WL LoRaWAN (basis) / nRF9151 (hoog)", H, 6, 8, 16, "[A]"),
  ("Antenne in dekselnaad", H, 2, 3, 6, "[A]"),
  ("Li-SOCl2 LS33600 + buffer", H, 14, 18, 26, "TME 2026"),
  ("PCB + passieven + assemblage", H, 5, 8, 12, "[A]"),
  ("Behuizing IP68/IK10 met IR-venster (HDPE/Ge) + vent", H, 10, 16, 25, "[A]"),
  ("RVS-beugel onder deksel, schokdempers", H, 3, 5, 8, "[A]"),
  ("Test, kalibratie, verpakking", H, 3, 5, 8, "[A]"),
  ("Installatie (bij lediging, 20-30 min)", I, 20, 30, 50, "[A]"),
  ("Certificering RED/CE/EMC", E, 15000, 25000, 40000, "[A]"),
  ("Connectiviteit (KPN LoRaWAN of 1NCE) + cloud", M, 0.3, 0.8, 1.5, "[A]"),
  ("Onderhoud: CO-cel + batterij /6 j, uitval 2 %/j", J, 4, 7, 12, "[A] CO-cel 5-7 j"),
  ("Containers per unit", D, 1, 1, 1, ""),
 ],
 "B1": [  # Thermische camera boven laadbak vuilniswagen
  ("Radiometrische thermische camera IP67 (160x120-320x240)", H, 400, 1200, 3000, "[A] Seek/FLIR/Hikmicro-klasse"),
  ("Edge-computer + cabinedisplay/zoemer", H, 150, 400, 800, "[A]"),
  ("Koppeling container-ID (RFID/boordcomputer)", H, 0, 100, 300, "[A] RFID vaak aanwezig"),
  ("Beschermkap, lensreiniging, beugel, bekabeling", H, 100, 250, 500, "[A]"),
  ("4G-router", H, 50, 100, 200, "[A]"),
  ("Installatie op wagen", I, 300, 600, 1200, "[A]"),
  ("Certificering/E-markering voertuig", E, 5000, 15000, 30000, "[A]"),
  ("Connectiviteit + cloud", M, 5, 10, 20, "[A]"),
  ("Onderhoud (lens, kalibratie, schade)", J, 100, 200, 400, "[A]"),
  ("Containers per unit", D, 500, 300, 200, "A7/A1: 200-500 containers per wagen"),
 ],
 "B0": [  # Accu-brievenbus aan zuil, geen elektronica
  ("Stibat-inzamelbuis + RVS-houder + sticker/QR", H, 25, 40, 60, "A6-C4 [A]"),
  ("Installatie", I, 20, 40, 60, "[A]"),
  ("Lediging buis (Stibat/inzamelaar)", J, 10, 25, 50, "[A] 4-12x/j"),
  ("Containers per unit", D, 1, 1, 1, ""),
 ],
}
# K3b: zelfde unit, rouleert 1 per 20-50 containers, met verhuiskosten
BOM["K3b"] = [r for r in BOM["K3a"] if r[1] != D] + [
  ("Verhuizing tussen zuilen (4-12x/j x 300-600)", J, 1200, 3600, 7200, "[A] R2a A5"),
  ("Containers per unit", D, 50, 35, 20, "A3-C4"),
]
# K5 = K2 (zuil) + K4-lite (container, BLE naar zuilmodule i.p.v. eigen WAN)
k4lite = []
for r in BOM["K4"]:
    n = r[0]
    if n.startswith("Radio+MCU"):
        r = ("Radio+MCU: nRF52 BLE naar zuilmodule (geen eigen WAN)", H, 3, 4, 6, "[A]")
    elif n.startswith("Antenne"):
        r = ("Antenne BLE (PCB)", H, 0.5, 1, 2, "[A]")
    elif n.startswith("Connectiviteit"):
        continue
    elif n.startswith("Certificering"):
        r = ("Certificering RED (BLE, pre-gecert. module)", E, 5000, 10000, 20000, "[A]")
    elif n.startswith("Containers"):
        continue
    k4lite.append(("K4-lite: " + r[0], *r[1:]))
BOM["K5"] = [("K2: " + r[0], *r[1:]) for r in BOM["K2"] if r[1] not in (D, "optie_hw")] + k4lite + [
  ("Software-integratie actieprotocol (boordcomputer/AMCS)", E, 20000, 40000, 80000, "[A] A6"),
  ("Containers per unit", D, 1, 1, 1, ""),
]

def totals(rows):
    t = {}
    for r in rows:
        if r[1] in (H, I, E, M, J, D):
            t.setdefault(r[1], np.zeros(3))
            if r[1] == D:
                t[D] = np.array(r[2:5], float)
            else:
                t[r[1]] += np.array(r[2:5], float)
    return t

summary = []
for k, rows in BOM.items():
    with open(os.path.join(PROD, f"BOM_{k}.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["concept", "post", "categorie", "laag", "basis", "hoog", "bron_aanname"])
        for r in rows:
            w.writerow([k, *r])
        t = totals(rows)
        for c in (H, I, E, M, J):
            if c in t:
                w.writerow([k, f"TOTAAL_{c}", f"totaal_{c}", *np.round(t[c], 2), "som"])
    t = totals(rows)
    cov = t.get(D, np.ones(3))
    # per-container 10-jaars TCO excl. eenmalig, uitgaande van unit-dekking
    tco10 = (t.get(H, 0) + t.get(I, 0) + 120 * t.get(M, 0) + 10 * t.get(J, 0)) / cov
    summary.append([k, *np.round(t.get(H, np.zeros(3)), 0), *np.round(t.get(I, np.zeros(3)), 0),
                    *np.round(t.get(M, np.zeros(3)), 2), *np.round(t.get(J, np.zeros(3)), 0),
                    *np.round(t.get(E, np.zeros(3)), 0), *cov.astype(int), *np.round(tco10, 0),
                    *np.round(tco10 / 120, 2)])
hdr = ["concept"] + [f"{c}_{s}" for c in ("hw", "installatie", "per_maand", "per_jaar", "eenmalig",
       "containers_per_unit", "tco10j_per_container", "tco_per_container_per_maand")
       for s in ("laag", "basis", "hoog")]
with open(os.path.join(PROD, "BOM_samenvatting.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(summary)

# ---------------------------------------------------------------- ENERGIE
V = 3.6
THROWS = params.CONTAINER["throws_per_day"]  # (30, 80, 150)
# (mWh per inworp l/b/h, vaste mWh/dag l/b/h) – vaste last = slaap + continu + communicatie
E_MODEL = {
 #           per inworp (mWh)          vast per dag (mWh)              toelichting
 "K1":   ((0.04, 0.08, 0.15), (2.4, 6.3, 14.3)),   # VLF 40 mW+MCU 15 mW x 2-10 s; slaap 5-50 uA + 1-4 LTE-M + alarmen
 "K2":   ((0.06, 0.16, 0.30), (0.5, 1.5, 4.0)),    # 2 lussen PI ~100 mW x 2-10 s; geen eigen modem (OEM)
 "K3a":  ((20, 36, 70), (24, 72, 240)),            # buis 0,03 Wh + compute; standby 1-10 W? -> 1-10 mW*24h... zie RESULTATEN
 "K4":   ((0, 0, 0), (6, 12, 25)),                 # IR 8x8 elke 10 min (15 mW x 10-15 s), CO-bias, LoRa/NB-IoT
 "K5c":  ((0, 0, 0), (5, 10, 21)),                 # K5 containerdeel = K4-lite (BLE i.p.v. WAN: -1..-4 mWh/dag); zuildeel = K2
}
CAP = {  # bruikbare energie
 "1x LS33600 (43 Wh)": 43_000,
 "2x LS33600 (86 Wh)": 86_000,
}
ZUIL_ACCU_MARGE_MWH_DAG = (20, 50, 150)   # [A] extra last die zuil-accu/paneel zonder aanpassing draagt
SOLAR_DEC_MWH_DAG_PER_WP = (60, 150, 300)  # [A] dec NL, verticaal/schaduw ... horizontaal (0,5 kWh/m2/d, PR 0,6)

rows = []
for k, (pt, fx) in E_MODEL.items():
    for i, lab in enumerate(("laag", "basis", "hoog")):
        for n in THROWS:
            d = n * pt[i] + fx[i]
            rows.append((k, lab, n, round(d, 1)))
with open(os.path.join(OUT, "energie_tabel.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["concept", "scenario", "inworpen_per_dag", "mWh_per_dag"]); w.writerows(rows)

def day(k, n, i=1):
    pt, fx = E_MODEL[k]; return n * pt[i] + fx[i]

print("Energie mWh/dag (basis) @30/80/150:")
for k in E_MODEL:
    vals = [day(k, n) for n in THROWS]
    yrs = [43_000 / v / 365 for v in vals]
    print(f"  {k:4s}", " / ".join(f"{v:7.1f}" for v in vals), "| jaren op 1x LS33600:", " / ".join(f"{y:5.1f}" for y in yrs))
print("B1: voeding uit wagen (24 V), ~15 W x 8-10 h = 120-150 Wh/dag, niet beperkend")

# figuur
fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
n = np.linspace(10, 200, 100)
cols = {"K1": "#1f77b4", "K2": "#2ca02c", "K4": "#9467bd", "K5c": "#ff7f0e", "K3a": "#d62728"}
for k, c in cols.items():
    lo = np.array([day(k, x, 0) for x in n]); ba = np.array([day(k, x, 1) for x in n]); hi = np.array([day(k, x, 2) for x in n])
    ax[0].plot(n, ba, color=c, label=k); ax[0].fill_between(n, lo, hi, color=c, alpha=0.15)
ax[0].set_yscale("log"); ax[0].set_xlabel("inworpen per dag"); ax[0].set_ylabel("mWh per dag (band = laag-hoog)")
for lab, cap in (("1x LS33600, 5 j", 43_000 / (5 * 365)), ("1x LS33600, 10 j", 43_000 / (10 * 365))):
    ax[0].axhline(cap, ls="--", color="k", lw=0.8); ax[0].text(12, cap * 1.08, lab, fontsize=8)
ax[0].axhline(5 * 150, ls=":", color="orange", lw=1); ax[0].text(12, 5 * 150 * 1.08, "5 Wp paneel dec (basis)", fontsize=8, color="orange")
ax[0].axhspan(ZUIL_ACCU_MARGE_MWH_DAG[0], ZUIL_ACCU_MARGE_MWH_DAG[2], color="grey", alpha=0.12)
ax[0].text(140, 25, "marge pas-zuil-accu [A]", fontsize=8, color="grey")
for x in THROWS: ax[0].axvline(x, color="grey", lw=0.4)
ax[0].legend(fontsize=8, loc="center right"); ax[0].set_title("Energie per dag vs. off-grid capaciteit")
# levensduur
ks = ["K1", "K2 (standalone-optie)", "K4", "K5c (K4-lite)"]
real = ["K1", "K2", "K4", "K5c"]
x = np.arange(len(ks)); wdt = 0.25
for j, nn in enumerate(THROWS):
    yrs = [min(43_000 / day(k, nn) / 365, 30) for k in real]
    ax[1].bar(x + (j - 1) * wdt, yrs, wdt, label=f"{nn} inworpen/dag")
ax[1].axhline(5, color="k", ls="--", lw=0.8); ax[1].text(-0.4, 5.3, "bestekeis batterij >= 5 j", fontsize=8)
ax[1].axhline(10, color="k", ls=":", lw=0.8); ax[1].text(-0.4, 10.3, "levensduur elektronica 10 j", fontsize=8)
ax[1].set_xticks(x); ax[1].set_xticklabels(ks); ax[1].set_ylabel("jaar op 1x LS33600 (43 Wh), basis, max 30")
ax[1].set_title("Batterijlevensduur (K2/K5-zuildeel draait normaal op zuil-accu)"); ax[1].legend(fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_energie.png"), dpi=130); plt.close(fig)

# ---------------------------------------------------------------- BLOKSCHEMA
def box(a, x, y, w, h, txt, fc):
    a.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec="k", lw=1)); a.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=8)
def arr(a, x1, y1, x2, y2, t=""):
    a.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="->", lw=1))
    if t: a.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.12, t, fontsize=7, ha="center")
fig, a = plt.subplots(figsize=(12, 6)); a.set_xlim(0, 12); a.set_ylim(0, 7); a.axis("off")
a.add_patch(plt.Rectangle((0.2, 3.3), 7.4, 3.5, fc="none", ec="#2ca02c", ls="--")); a.text(0.3, 6.55, "INWORPZUIL (K2-module in zuilkop + lussen in trommelliner)", fontsize=9, color="#2ca02c")
box(a, 0.5, 4.8, 1.6, 1.2, "2 PI-lussen\nachter PE-liner\n(meedraaiend)", "#e8f5e9")
box(a, 2.6, 4.8, 1.8, 1.2, "PI front-end\nmulti-gate +\nferro-kanaal", "#e8f5e9")
box(a, 4.9, 4.8, 1.6, 1.2, "STM32U5\nnulmeting, features,\nklasse 0/1/2", "#e8f5e9")
box(a, 4.9, 3.5, 1.6, 0.9, "BLE-ontvanger\n(van K4-lite)", "#fff3e0")
box(a, 8.2, 4.8, 1.8, 1.2, "OEM toegangs-\ncontroller\n(pas, slot)", "#eeeeee")
box(a, 8.2, 3.3, 1.8, 1.0, "OEM-modem\nLTE-M/4G", "#eeeeee")
box(a, 10.4, 4.8, 1.4, 1.2, "12 V accu\n(+ zonnepaneel)", "#eeeeee")
box(a, 10.4, 3.3, 1.4, 1.0, "Cloud / Bayes-hub\n(A6) → boord-\ncomputer", "#e3f2fd")
arr(a, 2.1, 5.4, 2.6, 5.4); arr(a, 4.4, 5.4, 4.9, 5.4)
arr(a, 6.5, 5.6, 8.2, 5.6, "RS485/UART, gal. gescheiden"); arr(a, 8.2, 5.1, 6.5, 5.1, "pas-/trommel-event (trigger)")
arr(a, 10.4, 5.4, 10.0, 5.4, ""); a.text(10.0, 6.15, "12 V → DC-DC (fail-open)", fontsize=7)
arr(a, 9.1, 4.8, 9.1, 4.3); arr(a, 10.0, 3.8, 10.4, 3.8)
a.add_patch(plt.Rectangle((0.2, 0.3), 7.4, 2.6, fc="none", ec="#9467bd", ls="--")); a.text(0.3, 2.65, "ONDERGRONDSE CONTAINER (K4-lite onder deksel, eigen LS33600)", fontsize=9, color="#9467bd")
box(a, 0.5, 0.7, 1.6, 1.4, "IR 8x8 +\nCO-cel +\n2x NTC", "#f3e5f5")
box(a, 2.6, 0.7, 1.8, 1.4, "nRF52 BLE\n(event: dT/dt,\nCO-trend)", "#f3e5f5")
box(a, 4.9, 0.7, 1.6, 1.4, "LS33600\n43 Wh bruikbaar\n6-10 j", "#f3e5f5")
arr(a, 2.1, 1.4, 2.6, 1.4); arr(a, 4.9, 1.4, 4.4, 1.4); arr(a, 3.5, 2.1, 5.3, 3.5, "BLE ~1-3 m")
a.text(8.2, 1.5, "K5 = K2 + K4-lite + actieprotocol\nOranje (rangorde) = laatst in route\nRood (pakket + event) = apart/niet persen\nGeen eigen SIM, geen eigen accu in de zuil", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(PROD, "blokschema.png"), dpi=130); plt.close(fig)

# ---------------------------------------------------------------- MONTAGESCHETS (doorsnede)
fig, a = plt.subplots(figsize=(8, 9)); a.set_xlim(-1, 7); a.set_ylim(-5.5, 3.5); a.set_aspect("equal"); a.axis("off")
a.add_patch(plt.Rectangle((-1, -0.1), 8, 0.1, fc="#999")); a.text(5.3, 0.1, "maaiveld / platform", fontsize=8)
a.add_patch(plt.Rectangle((1.5, 0), 3, 2.6, fc="#cfd8dc", ec="k")); a.text(1.6, 2.35, "zuil 3 mm staal", fontsize=8)
a.add_patch(plt.Rectangle((1.5, 2.6), 3, 0.5, fc="#90a4ae", ec="k")); a.text(1.6, 2.75, "zuilkop: K2-module + OEM-elektronica", fontsize=7)
c = plt.Circle((3, 1.3), 0.95, fc="#eceff1", ec="k", lw=2); a.add_patch(c); a.text(3, 2.35, "RVS-trommel 60 L", fontsize=7, ha="center")
a.add_patch(matplotlib.patches.Arc((3, 1.3), 1.7, 1.7, theta1=200, theta2=340, color="#2ca02c", lw=4)); a.text(3, 0.2, "PE-liner + 2 PI-lussen", fontsize=7, ha="center", color="#2ca02c")
a.add_patch(plt.Rectangle((2.5, 0.9), 1.0, 0.6, fc="#a1887f", ec="k")); a.text(3, 1.2, "zak", fontsize=7, ha="center")
a.plot([3.9, 4.2, 4.2], [0.8, 0.8, 2.7], color="#2ca02c", lw=1.5); a.text(4.25, 1.6, "flexkabel", fontsize=7, color="#2ca02c")
a.add_patch(plt.Rectangle((0.3, -5.2), 5.4, 5.0, fc="#eeeeee", ec="k")); a.text(0.4, -5.0, "betonput + container 3-5 m³", fontsize=8)
a.add_patch(plt.Rectangle((0.6, -0.9), 4.8, 0.3, fc="#bdbdbd", ec="k")); a.text(0.7, -0.8, "containerkop (wordt bij lediging opgetild)", fontsize=7)
a.add_patch(plt.Rectangle((4.3, -1.3), 0.8, 0.4, fc="#9467bd", ec="k")); a.text(5.15, -1.25, "K4-lite\n(IR+CO, BLE)", fontsize=7, color="#9467bd")
a.plot([4.7, 3.8], [-1.3, -3.2], color="#9467bd", ls=":"); a.plot([4.7, 5.4], [-1.3, -3.2], color="#9467bd", ls=":")
a.add_patch(plt.Rectangle((0.8, -4.9), 4.4, 1.8, fc="#d7ccc8", ec="k")); a.text(3, -4.0, "afval", fontsize=8, ha="center")
a.annotate("", (3, -0.6), (3, 0.3), arrowprops=dict(arrowstyle="->")); a.text(3.1, -0.2, "valschacht", fontsize=7)
fig.tight_layout(); fig.savefig(os.path.join(PROD, "montage.png"), dpi=130); plt.close(fig)

print("\nBOM samenvatting (hw basis | tco/container/maand l/b/h):")
for s in summary:
    print(f"  {s[0]:4s} hw {s[2]:7.0f} | tco/mnd {s[-3]:.2f} / {s[-2]:.2f} / {s[-1]:.2f}")
