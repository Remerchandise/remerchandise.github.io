# R3 – A6 Classificatie-Monte-Carlo en signaalketen (FASE 1)

A6 · 2026-10-25 · EUR 2026 excl. btw · aannames **[A]**
Draaien vanuit repo-root: `python3 experiments/r3_classificatie/mc.py` (~15 s, seed 20261025, 30 000 ledigingen × 100 zakken per scenario). Gebruik `--fast` voor een snelle controle.
Uitvoer: `mc_container.csv`, `mc_inworp.csv`, `mc_meta.json` (welke modellen zijn gebruikt), `fig_recall_vs_meldingen.png`, `fig_inworp.png`, `fig_vermeden_schade.png`.

> **Status van de modellen.** K3 (A3) en K4/B1 (A4) zijn al de echte modellen. Voor K1 en K2 zijn het nog **placeholders [A]** (`placeholders/sensor_model_K1/K2.json`), omdat A2 nog geen JSON heeft geleverd. Figuren met placeholders dragen een label in de titel.

**FASE 2:** zodra `experiments/r3_inductie/sensor_model_K1.json` en `sensor_model_K2.json` bestaan, gebruikt mc.py die automatisch. Opnieuw draaien is dan genoeg. Dit wordt automatisch opgepikt:
- K3 uit `r3_rontgen/`;
- K4 (A4-formaat `formaat_A6`, regel E; meldingen = "vlag actief bij lediging");
- B1 (`b1_resultaten.json`);
- brandkans via A1 `risk.p_fire_from_wheq`.

## Methode
1. **Zakken.** Per zak worden de items getrokken uit `params.ITEMS`:
   - NB- of Poisson-verdeling;
   - Wh per item uit een driehoeksverdeling (laag/basis/hoog);
   - Li-items geschaald met het scenario en met een latente containerfactor Gamma(k = 2) **[A]**. Die factor staat voor verschillen tussen buurten; zonder zo'n factor valt er geen rangorde te maken.
2. **Sensor per zak.** Elk object geeft een uitkomst {geen, cel, pakket} volgens `p_out_given_item` (independent-or). De zak krijgt de hoogste uitkomst. Li-objecten hebben een extra kans gemist te worden als er ander metaal in de zak zit (`masking`). Pakket = ≥ 20 Wh-eq (`params.PACK_WHEQ`).
3. **Bayes-score.** Per uitkomst wordt E[Wh-eq van de zak | uitkomst] gekalibreerd op een aparte trekking. De containerscore is de som daarvan sinds de laatste lediging. Daarnaast tellen we twee varianten: de "teller" (aantal geflagde zakken, de oorspronkelijke K1) en de "pakket-teller".
4. **Beslisregels.** Er zijn drie regels:
   - **budget**: rangorde, met oranje = top 2 % (2,5 per wagen per dag bij 125 containers per wagen per dag **[A]**) en rood = top 0,16 % (1 per wagen per week);
   - **A1-R3**: oranje bij een container ≥ 75 of een inworp ≥ 50 Wh-eq, rood bij ≥ 150 of een inworp ≥ 75;
   - **A1-R3+pakket**: daarbovenop maakt elke pakket-uitkomst de container oranje.
5. **Effect.** Brandkans per lediging = `risk.p_fire_from_wheq(som Wh-eq, k)`. De actie verlaagt die kans: oranje (laatste in de route, niet extra persen) met 30 % **[A]**, rood (apart legen, niet persen) met 80 % **[A]**. Vermeden schade = vermeden wagenbranden × `ECON.fire_cost_truck_eur`.
6. **Event-kanalen.**
   - K4: containerbranden per jaar (A4: λ = 2/5/10 e-4) × P(detectie binnen 60 min) × 50 % minder schade **[A]** × `fire_cost_container`.
   - B1: wagenbranden × vermeden EUR per wagenbrand (A4).
   - K5 = K2-rangorde + K4-event.

## Resultaten

### Basisgetal
Wagenbranden per 1 000 containers per jaar: **0,07 / 1,26 / 48** (laag / basis / hoog). Het hoge scenario combineert 2,5× zoveel Li met een 15× hogere k (A1) en is een extreme bovengrens.

### Per inworp (scenario basis) – `fig_inworp.png`

| Sensor | Zakken geflagd | PPV Li bij flag | Recall Li-zak | PPV pakket | Recall pakket |
|---|---|---|---|---|---|
| K1 VLF *(placeholder)* | 77 % | 0,03 | 0,85 | 0,004 | 0,50 |
| K2 PI *(placeholder)* | 53 % | 0,04 | 0,67 | 0,009 | 0,60 |
| K3 röntgen (A3) | 21 % | 0,10 (laag 0,05 / hoog 0,22) | 0,72 | 0,17 (0,10 / 0,31) | 0,77 |
| Perfect | 2,9 % | 1 | 1 | 1 | 1 |

Ook röntgen haalt per inworp geen PPV ≥ 50 % (checklist B1). De oorzaak is alkaline: 39 % van de K3-flags is een zak met alkaline en zonder Li. Alarmeren per zak valt daarmee af voor alle concepten.

### Per container, regel "budget" (≤ 20 meldingen per 1 000 ledigingen, 1 rood per wagen per week) – `fig_recall_vs_meldingen.png`

| Concept | Risicorecall basis (laag–hoog) | Vermeden branden | EUR/container/maand basis (laag–hoog) |
|---|---|---|---|
| Willekeurig (referentie) | 0,018 | 0,6 % | 0,016 |
| K1 VLF-teller *(ph)* | 0,024 | 0,9 % | 0,023 (0,0004–1,8) |
| K2 pakketwachter *(ph)* | 0,029 | 1,0 % | 0,027 (0,0006–2,1) |
| B0 risicokaart (geen sensor, ruis σ = 0,7 **[A]**) | 0,041 | 1,4 % | 0,037 (0,0008–3,4) |
| K3 röntgen | 0,093 (0,11–0,087) | 3,3 % | 0,086 (0,002–6,2) |
| **Perfecte sensor (bovengrens)** | **0,16 (0,21–0,11)** | **5,8 %** | **0,15 (0,005–7,7)** |

**Kernresultaat.** Ook een perfecte zuilsensor vangt binnen de werkbaarheidsgrens hooguit ~16 % van het brandrisico. Dat komt doordat het risico verspreid zit over veel containers met elk een paar kleine items. De top 2 % containers bevat dus maar een klein deel ervan. Vermeden schade is dan **≤ EUR 0,15 per container per maand** (basis). Dat ligt een orde onder de kostprijs van EUR 8–23 (A7).

### Per container, A1-R3-drempels (los van het budget)

| Concept | Meldingen per 1 000 ledigingen | Rood per wagen per week | Risicorecall | EUR/c/m basis |
|---|---|---|---|---|
| Perfect | 77 (laag 22 / hoog 246) | 7,6 | 0,52 | 0,76 |
| Perfect + pakket | 134 | 7,6 | 0,67 | 0,88 |
| K3 röntgen | 4,4 | 0 | 0,03 | 0,02 |
| K3 + pakket | 304 | 0 | 0,69 | 0,54 |
| K2 *(ph)* + pakket | ~1 000 (elke container) | 0 | 1 | 0,79 |

De A1-drempels liggen bij een perfecte sensor al **3–4× boven de werkbaarheidsgrens** (77 tegenover 20 per 1 000). Elke pakket-uitkomst als oranje tellen is met echte sensoren onwerkbaar, omdat pakket-flags door ander metaal in vrijwel elke lediging voorkomen. Een Bayes-score van een sensor met veel vals-positieven blijft onder de 75 Wh-eq. Hij komt daar alleen overheen bij 2,5× zoveel Li (scenario hoog).

### Event-kanalen en benchmark (EUR per container per maand)

| Concept | Meldingen | EUR/c/m (laag / basis / hoog) |
|---|---|---|
| K4 deksel-event (regel E) | 0,29 / 1,06 / 2,41 vlaggen per wagen per week | 0,012 / 0,17 / 0,63 |
| K5 = K2 + K4 | budget + 1,06 per week | 0,013 / 0,19 / 2,7 |
| **B1 thermische camera in de wagen** | n.v.t. (A4) | 0,006 / **0,90** / 129 |

## Conclusies
1. **Uitgangspunt 2 (risicodrempel) klopt wel, maar de drempel moet in meldingen per wagen worden uitgedrukt, niet in Wh-eq.** Bij een vaste Wh-eq-drempel bepaalt de base rate de alarmlast.
2. **Uitgangspunt 3 (metaaldetector):** de K1/K2-placeholders presteren nauwelijks beter dan willekeurig (0,024–0,029 tegenover 0,018). Wachten op A2 voor de echte cijfers. Om er iets aan te hebben moet K2 de PPV voor pakket per inworp naar ≥ 0,1–0,2 brengen (röntgenniveau).
3. Een **zuilsensor kan het meeste risico niet bereiken.** De bovengrens is ~6 % vermeden branden bij een werkbaar aantal meldingen. **B1 (wagen) levert in het basisscenario ~6× meer op dan een perfecte zuilsensor.** K4 voegt een eigen waarde toe via containerbranden.
4. Het nut van een sensor in de zuil zit dus vooral in **data en preventie** (B0, rangorde voor campagnes, de Li-prevalentie omlaag brengen), niet in het voorkomen van branden.

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
