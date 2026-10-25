"""Ronde 4 – gewogen scorekaart (Orchestrator).

Scores 1–5 per criterium, onderbouwd met de Ronde 3-resultaten (zie toelichting
in debate/R4_scorekaart.md). Draai: python3 experiments/r4_scorekaart/scorekaart.py
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
W = {"detectie": 0.25, "kosten": 0.20, "eenvoud": 0.15,
     "inpasbaarheid": 0.15, "juridisch": 0.10, "waarde": 0.15}

# concept: (naam, scores, knock-out of None, betrouwbaarheid)
C = {
    "K1": ("Strandmetaaldetector (VLF) in trommel",
           dict(detectie=1, kosten=3, eenvoud=4, inpasbaarheid=3, juridisch=5, waarde=1),
           "Discriminatie fysiek onvoldoende: PPV 5 %, recall Li-zak 5 %; abonnement > vermeden schade", "hoog"),
    "K2": ("Pakketwachter (PI, OEM pas-zuil)",
           dict(detectie=1.5, kosten=3, eenvoud=3, inpasbaarheid=3, juridisch=5, waarde=1),
           "Vals alarm onwerkbaar (PPV pakket 4–7 %); niet beter dan B0 zonder sensor; abonnement EUR 10,7 vs schade EUR 0,08/mnd", "middel"),
    "K3a": ("Röntgen ≤30 kV vast per zuil",
            dict(detectie=3, kosten=1, eenvoud=2, inpasbaarheid=1, juridisch=3, waarde=2),
            "Prijs EUR 90/mnd ≫ schade; 1,2–5,5 Wh/dag niet off-grid op batterij", "middel"),
    "K3b": ("Röntgen-ijkpaal (rouleert)",
            dict(detectie=3, kosten=2, eenvoud=2, inpasbaarheid=3, juridisch=3, waarde=2),
            "Als abonnement EUR 26,7/mnd vs schade ~0; alleen zinvol als eenmalig validatie-instrument", "middel"),
    "K4": ("Deksel-eventmodule (IR + CO)",
           dict(detectie=2, kosten=4, eenvoud=4, inpasbaarheid=4, juridisch=5, waarde=2),
           "Geen accudetector (PPV accu ≤ 0,2 %); als losse module abonnement EUR 13,9 > schade", "middel"),
    "K4add": ("K4 als add-on op bestaande vulgraadsensor (hotspots)",
              dict(detectie=2, kosten=5, eenvoud=4, inpasbaarheid=5, juridisch=5, waarde=2),
              None, "laag"),
    "K5": ("Hybride K2 + K4 + protocol",
           dict(detectie=1.5, kosten=2, eenvoud=2, inpasbaarheid=3, juridisch=4, waarde=2),
           "Erft vals-alarm K2; abonnement EUR 18,6 vs schade EUR 0,3/mnd", "middel"),
    "B1": ("Thermische camera laadbak, als abonnement",
           dict(detectie=4, kosten=3, eenvoud=4, inpasbaarheid=4, juridisch=4, waarde=3),
           "Abonnement EUR 8,4/mnd vs schade EUR 1,4/mnd bij 1.000 containers", "middel"),
    "B1oem": ("Thermische camera laadbak, fabrieksoptie wagen (benchmark)",
              dict(detectie=4, kosten=4, eenvoud=4, inpasbaarheid=4, juridisch=4, waarde=4),
              None, "middel"),
    "B0": ("Accu-brievenbus aan zuil, betaald door PRO (geen sensor)",
           dict(detectie=2, kosten=3, eenvoud=5, inpasbaarheid=4, juridisch=5, waarde=3),
           None, "laag"),
}

rows = []
for k, (naam, s, ko, betr) in C.items():
    tot = round(sum(W[c] * v for c, v in s.items()), 2)
    # AANBEVOLEN vereist >= 3,5 en geen knock-out; geen enkel concept haalt in het
    # basisscenario abonnement <= vermeden schade, dus maximaal CONDITIONEEL
    # (voorwaarden: debate/R4_scorekaart.md).
    if ko:
        oordeel = "NIET AANBEVOLEN (knock-out)"
    else:
        oordeel = "CONDITIONEEL"
    rows.append(dict(id=k, naam=naam, **s, gewogen=tot, knockout=ko or "", oordeel=oordeel, betrouwbaarheid=betr))

with open(os.path.join(HERE, "scorekaart.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
json.dump({"gewichten": W, "concepten": rows}, open(os.path.join(HERE, "scorekaart.json"), "w"), indent=1, ensure_ascii=False)
for r in rows:
    print(f"{r['id']:4s} {r['gewogen']:.2f}  {r['oordeel']}")
