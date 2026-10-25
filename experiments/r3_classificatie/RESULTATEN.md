# R3 – A6 Classificatie-Monte-Carlo en signaalketen (FASE 2)

A6 · 2026-10-25 · EUR 2026 excl. btw · aannames **[A]**
Draaien vanuit repo-root: `python3 experiments/r3_classificatie/mc.py` (~15 s, seed 20261025, 30 000 ledigingen × 100 zakken per scenario). Gebruik `--fast` voor een snelle controle.
Uitvoer: `mc_results.json` (voor A7), `mc_container.csv`, `mc_inworp.csv`, `mc_meta.json`, `fig_concepten_recall_valsalarm.png` (deck), `fig_recall_vs_meldingen.png`, `fig_inworp.png`, `fig_vermeden_schade.png`.

> **Status: FASE 2. Alle modellen zijn echt.** K1/K2: A2 `r3_inductie/sensor_model_K1/K2.json` in de **in_bag**-modus, door A2 aanbevolen:
> - een Li-loze zak geeft `clutter_bag.p_out_given_n_metal`;
> - een zak met Li geeft het maximum over de Li-items van `p_out_given_item_in_bag`, met superpositie gesimuleerd door A2.
>
> K3: A3 (independent_or met masking). K4 en B1: A4. Brandkans: A1 `risk.p_fire_from_wheq`. Geen placeholders meer (zie `mc_meta.json`).
>
> **Voor A7:** `mc_results.json` bevat per concept K1–K5, B0, B1, perfect en random de reeksen [laag, basis, hoog] voor `recall_energy`, `recall_risk`, `alarms_per_1000_emptyings`, `avoided_fire_fraction`, `fires_per_1000_containers_year`, `ppv_container_ge75` en `eur_avoided_per_container_month`.

## Methode
1. **Zakken.** Items uit `params.ITEMS` (NB/Poisson), Wh per item uit een driehoeksverdeling. Li-items worden geschaald met het scenario en met een latente containerfactor Gamma(k = 2) **[A]**. Die factor staat voor verschillen tussen buurten.
2. **Sensor per zak.** Uitkomst {geen, cel, pakket}, waarbij pakket = ≥ 20 Wh-eq (`PACK_WHEQ`). Voor K1/K2 geldt de in_bag-modus van A2. Voor K3 geldt independent-or: elk object triggert zelfstandig, de zak krijgt de hoogste uitkomst, en Li krijgt een extra miskans bij ander metaal.
3. **Bayes-score.** Per uitkomst wordt E[Wh-eq van de zak | uitkomst] gekalibreerd op een aparte trekking. De containerscore is de som sinds de laatste lediging. Daarnaast de varianten "teller" (de oorspronkelijke K1) en "pakket-teller".
4. **Beslisregels.**
   - **budget**: rangorde, met oranje = top 20 per 1 000 ledigingen (2,5 per wagen per dag bij 125 containers per dag **[A]**) en rood = 1 per wagen per week.
   - **budget5 / budget50**: varianten met 5 en 50 meldingen per 1 000 ledigingen.
   - **A1-R3**: oranje bij een container ≥ 75 of een inworp ≥ 50 Wh-eq, rood bij ≥ 150 of een inworp ≥ 75.
   - **A1-R3+pakket**: daarbovenop maakt elke pakket-uitkomst de container oranje.
5. **Effect.** P(brand) per lediging komt uit A1. De actie verlaagt die: oranje (laatste in de route, niet extra persen) met 30 % **[A]**, rood (apart legen, niet persen) met 80 % **[A]**. Wagenbranden zijn omgerekend naar EUR met `ECON`.
6. **Event-kanalen.**
   - K4: λ containerbrand (A4: 2/5/10 e-4 per container per jaar) × P(detectie binnen 60 min, regel E) × 50 % minder schade **[A]**. Meldingen = A4 "vlag actief bij lediging".
   - B1: wagenbranden × vermeden EUR per wagenbrand (A4).
   - K5 = K2-rangorde + K4.

## Resultaten

### Basisgetal
Wagenbranden per 1 000 containers per jaar: **0,07 / 1,27 / 48** (laag / basis / hoog). Het hoge scenario combineert 2,5× zoveel Li met een 15× hogere k (A1) en is een extreme bovengrens.

### Per inworp (scenario basis) – `fig_inworp.png`

| Sensor | Zakken geflagd | PPV Li bij flag (laag–hoog) | Recall Li-zak | Energierecall per zak | PPV pakket | Recall pakket |
|---|---|---|---|---|---|---|
| K1 VLF (A2) | 2,0 % | 0,07 (0,04–0,17) | 0,05 | 0,26 | 0,08 | 0,12 |
| K2 PI pakketwachter (A2) | 2,4 % | 0,05 (0,02–0,11) | 0,04 | 0,27 | 0,04 | 0,08 |
| K3 röntgen (A3) | 15 % | 0,12 (0,06–0,26) | 0,65 | 0,88 | 0,34 (0,20–0,53) | 0,82 |
| Perfect | 2,9 % | 1 | 1 | 1 | 1 | 1 |

Bij A2's werkpunt (2 % vals per zak) zijn K1 en K2 vooral **blind**: ze vinden 4–5 % van de Li-zakken en 8–12 % van de pakketten. Per zak haalt geen enkel concept een PPV ≥ 50 % (checklist B1). Bij röntgen is 62 % van de flags een zak met alkaline en zonder Li.

### Per container bij de werkbare drempel: ≤ 20 meldingen per 1 000 ledigingen en 1 rood per wagen per week
Figuren: `fig_concepten_recall_valsalarm.png` (deckfiguur, ook met 5 en 50 per 1 000) en `fig_recall_vs_meldingen.png`.

| Concept | Energierecall (laag / basis / hoog) | PPV cont ≥ 75 (basis) | Vals-alarmratio (basis) | Vermeden wagenbranden (basis) | EUR/c/m (laag / basis / hoog) |
|---|---|---|---|---|---|
| Willekeurig | 0,021 / 0,015 / 0,019 | 0,01 | 0,020 | 0,5 % | 0,0004 / 0,014 / 1,3 |
| K1 VLF-teller | 0,027 / 0,036 / 0,036 | 0,05 | 0,019 | 1,4 % | 0,0006 / 0,036 / 2,6 |
| K2 pakketwachter | 0,046 / 0,044 / 0,052 | 0,07 | 0,019 | 1,5 % | 0,0009 / 0,041 / 3,9 |
| B0 risicokaart (geen sensor) | 0,050 / 0,044 / 0,048 | 0,09 | 0,019 | 1,5 % | 0,0010 / 0,041 / 3,4 |
| K3 röntgen | 0,104 / 0,093 / 0,092 | 0,28 | 0,015 | 3,5 % | 0,0023 / 0,092 / 6,7 |
| **Perfecte sensor** | **0,21 / 0,15 / 0,11** | 0,67 | 0,007 | **5,8 %** | 0,005 / **0,15** / 8,2 |
| K4 deksel-event | n.v.t. (0,5 / 1,7 / 3,9 vlaggen per 1 000 ledigingen) | – | – | 0 (containerbrand) | 0,012 / 0,17 / 0,63 |
| K5 = K2 + K4 | 0,046 / 0,044 / 0,052 (21,7 meldingen per 1 000) | 0,07 | 0,019 | 1,5 % | 0,013 / 0,21 / 4,5 |
| **B1 camera in de wagen** | n.v.t. | – | – | 10 / 34 / 64 % (schade-eq.) | 0,006 / **0,90** / 129 |

Varianten (basis, energierecall bij 5 / 20 / 50 meldingen per 1 000):
- K2: 0,015 / 0,044 / 0,092
- K3: 0,031 / 0,093 / 0,19
- perfect: 0,050 / 0,15 / 0,30
- willekeurig: 0,004 / 0,015 / 0,046

Bij 50 per 1 000 is de vals-alarmratio voor alle concepten ~4–5 %.

### A1-R3-drempels (los van het budget, basis)

| Concept | Meldingen per 1 000 | Rood per wagen per week | Energierecall | EUR/c/m |
|---|---|---|---|---|
| Perfect | 77 (laag 22 / hoog 246) | 7,7 | 0,52 | 0,76 |
| K3 röntgen | 1,4 | 0 | 0,01 | 0,01 |
| K3 + pakket | 304 | 0 | 0,69 | 0,55 |
| K2 + pakket | 253 | 0 | 0,39 | 0,31 |
| K1 + pakket | 203 | 0 | 0,34 | 0,27 |

## Conclusies
1. **K1 en K2 (inductie) zijn nauwelijks beter dan willekeurig.** Hun energierecall is 0,036–0,044, tegenover 0,015 willekeurig en 0,044 voor B0 zonder sensor. **K2 voegt dus niets toe ten opzichte van een sensorloze risicokaart (B0).** Uitgangspunt 3 (de metaaldetector als Li-detector) vervalt.
2. **Röntgen (K3) haalt ~60 % van de perfecte bovengrens**, maar is per zuil te duur (A7: EUR 36 per container per maand).
3. Een **zuilsensor kan het meeste risico niet bereiken.** Zelfs perfect vermijdt hij binnen de werkbaarheidsgrens ~6 % van de wagenbranden, wat neerkomt op ≤ EUR 0,15 per container per maand (basis). **B1 (wagen) levert ~6× meer op dan een perfecte zuilsensor** en ~20× meer dan K2. K4 levert een eigen bijdrage via containerbranden (EUR 0,17).
4. **Uitgangspunt 2 (risicodrempel) is nodig, maar moet in meldingen per wagen worden uitgedrukt.** Met de A1-Wh-drempels geeft zelfs een perfecte sensor 3–4× te veel meldingen. Met echte sensoren plus de pakketregel worden het er 200–300 per 1 000.
5. Waar een zuilsensor wel waarde heeft: **data en preventie** (rangorde voor campagnes, B0, gedrag), en K4 als vangnet voor containerbranden.

## Alleen met een prototype te bevestigen
- **Sensor per object en bij opeenstapeling** (K1/K2): zie het labtestontwerp van A8. A6 heeft daaruit nodig: `p_out_given_item` per itemklasse en `p_miss_li_given_n_metal`, gemeten op ≥ 300 synthetische zakken met een realistische metaalmix (2,5 blikjes + 3 folie gemiddeld).
- **Spreiding tussen containers** (Gamma k = 2 **[A]**): bepaalt hoeveel een rangorde kan opleveren. Te meten met steekproefsortering van ≥ 30 containers × 3 ledigingen (zie A8 power_analyse), en daarbij de variatiecoëfficiënt van Li per ton tussen containers schatten.
- **Effectiviteit van de acties** (30 % / 80 % **[A]**): veldproef met chauffeurs, waarbij "niet persen" wordt gekoppeld aan het aantal branden in de bunker en de overslag.

---

# r3_signaal – codeskelet

| Bestand | Inhoud |
|---|---|
| `experiments/r3_signaal/firmware_skeleton.py` | MicroPython-stijl, draait ook als zelftest. Keten: meting → klasse → Bayes-containerscore → niveau → **13-byte LoRaWAN-payload** (byte-indeling in de docstring) of MQTT-JSON. Downlinks: geleegd, posteriortabel, drempels. Verstuurt alleen bij escalatie, plus periodiek elke 6 uur. |
| `experiments/r3_signaal/ttn_decoder.js` | TTN/KPN-payloadformatter (`decodeUplink`, `encodeDownlink`). Round-trip getest met node. |
| `experiments/r3_signaal/dashboard_mock.html` | Statische mock: tegels, schematische kaart, tabel met filter en sortering, meldingen voor de chauffeur met terugkoppelknoppen (labels). Twee kanalen (rangorde / event). Geen persoonsgegevens. |

Voorbeeldpayload (oranje, 86 inworpen, 25 cel, 1 pakket): `124100070056043819011e0ea1` (13 B). Die past in SF12, waar maximaal 51 B mag.
