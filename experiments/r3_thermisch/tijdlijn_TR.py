"""Detectievenster vóór thermal runaway per mechanisme (literatuur -> tabel + tijdlijnfiguur).

Bronnen: research/A4_thermisch_gas.md §1 (Li-ion Tamer/DNV-GL 6,4 min; Honeywell 9-25 min;
Cai 2020/2021; UN GTR 20 5 min; Koch/Birke). Waarden met [A] zijn aannames.
Uitvoer: fig_tijdlijn_TR.png, tijdlijn_TR.csv
"""
import os, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

# venster = tijd tussen eerste detecteerbaar extern signaal (1e venting) en TR-onset, in s (laag, basis, hoog)
MECH = [
    # naam, stap in keten, venster (l,b,h) s, voorafgaande latentie (l,b,h) s, bron
    ("Extern oververhitten (zon/compost >> 60 °C)", "3 container", (300, 600, 1800), (3600, 6 * 3600, 48 * 3600),
     "Li-ion Tamer: 6,4 min (DNV-GL), 9–25 min (Honeywell); onwaarschijnlijk in container (compost < 50 °C) [A]"),
    ("Latente interne short na valschade", "2→3 container", (0, 60, 900), (60, 6 * 3600, 7 * 86400),
     "NG; soft short kan minuten–uren zelf verwarmen [A]; venster na venting ≈ crush-achtig"),
    ("Crush/penetratie persplaat", "5 wagen", (0, 5, 30), (0, 2, 60),
     "nail/crush: TR binnen seconden (algemene lit.) – geen venster"),
    ("Doorboring shredder/grijper", "6–7 verwerking", (0, 5, 30), (0, 5, 600), "idem crush"),
    ("Overladen (BESS, referentie)", "n.v.t.", (300, 900, 1800), (600, 1800, 7200), "Li-ion Tamer 9–25 min; ref. UN GTR 20 eist 5 min"),
]

# latentie detectiekanaal na TR / brand (s) (l,b,h) – uit warmte_gas.py / b1_laadbak.py
CHANNELS = [
    ("K4 CO-cel kopruimte (cel bovenin ≤0,3 m)", (90, 180, 600)),
    ("K4 CO-cel (cel 1 m diep, smeulen)", (300, 1200, 7200)),
    ("K4 IR 8×8 (cel bovenin)", (30, 120, 600)),
    ("B1 thermische camera laadbak (TR in zicht)", (1, 3, 10)),
    ("Li-ion Tamer (vóór TR, BESS-rek)", (-1500, -400, -380)),
]


def main():
    with open(os.path.join(HERE, "tijdlijn_TR.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["mechanisme", "stap", "venster_l_s", "venster_b_s", "venster_h_s", "latentie_b_s", "bron"])
        for n, s, v, lat, b in MECH:
            w.writerow([n, s, *v, lat[1], b])

    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(10, 7.5), gridspec_kw={"height_ratios": [5, 3]})
    for i, (n, s, v, lat, b) in enumerate(MECH):
        y = len(MECH) - 1 - i
        ax.barh(y, -max(v[2], 1), left=0, color="#f2c14e", alpha=0.35, height=0.6)
        ax.barh(y, -max(v[1], 1), left=0, color="#e07a1f", height=0.6, label="venster venting→TR (basis; licht = hoog)" if i == 0 else None)
        ax.barh(y, 1800, left=0, color="#b22222", height=0.6, label="TR → brand/smeulen" if i == 0 else None)
        ax.text(-3500, y, f"{n}\n[{s}]", va="center", ha="right", fontsize=8)
        ax.text(1900, y, f"{v[1]/60:.1f} min (l {v[0]/60:.1f} – h {v[2]/60:.0f})", va="center", fontsize=8)
    ax.axvline(0, color="k", lw=1)
    ax.set_xlim(-3600, 5000)
    ax.set_yticks([])
    ax.set_xlabel("tijd t.o.v. TR-onset (s)")
    ax.set_title("Detectievenster vóór thermal runaway per mechanisme (literatuur + [A])")
    ax.legend(loc="lower right", fontsize=8)

    for i, (n, lat) in enumerate(CHANNELS):
        y = len(CHANNELS) - 1 - i
        ax2.plot([lat[0], lat[2]], [y, y], color="#1f5fa8", lw=6, alpha=0.4)
        ax2.plot(lat[1], y, "o", color="#1f5fa8")
        ax2.text(-3500, y, n, va="center", ha="right", fontsize=8)
    ax2.axvline(0, color="k", lw=1)
    ax2.set_xlim(-3600, 8000)
    ax2.set_yticks([])
    ax2.set_xlabel("detectielatentie t.o.v. TR-onset (s)  (negatief = vóór TR)")
    ax2.set_title("Latentie per detectiekanaal (bol = basis, balk = laag–hoog)")
    fig.subplots_adjust(left=0.36, hspace=0.45, right=0.97, top=0.94, bottom=0.08)
    fig.savefig(os.path.join(HERE, "fig_tijdlijn_TR.png"), dpi=130)
    for n, s, v, lat, b in MECH:
        print(f"{n:45s} venster {v[0]:>5}/{v[1]:>5}/{v[2]:>5} s  | {b}")


if __name__ == "__main__":
    main()
