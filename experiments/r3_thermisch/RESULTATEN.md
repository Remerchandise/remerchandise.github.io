# R3 – A4 resultaten: thermisch, gas, K4 en B1

Agent 4 · 2026-10 · EUR 2026 excl. btw · **[A]** = aanname. Bandbreedtes: laag / basis / hoog. Bij detectie betekent "laag" het pessimistische scenario.

Draaien vanuit de repo-root (deterministisch, totaal < 20 s):
```
python3 experiments/r3_thermisch/warmte_gas.py     # fig_warmte_diffusie.png, warmte_gas_resultaten.json
python3 experiments/r3_thermisch/valsalarm_mc.py   # fig_valsalarm.png, event_model_K4.json
python3 experiments/r3_thermisch/b1_laadbak.py     # fig_b1_laadbak.png, b1_resultaten.json
python3 experiments/r3_thermisch/tijdlijn_TR.py    # fig_tijdlijn_TR.png, tijdlijn_TR.csv
```
Gedeelde fysica staat in `model_a4.py`.

## Samenvatting

| Grootheid | Laag | Basis | Hoog | Bron |
|---|---|---|---|---|
| Venster venting → TR, latente short (container) | 0 s | 1 min | 15 min | lit. + [A] (tijdlijn) |
| Venster crush (wagen) | 0 s | 5 s | 30 s | lit. |
| P(ventgas bereikt kopruimte vóór TR), zelfs met VOC-sensor | 0,3 % | 4 % | 24 % | warmte_gas (d) |
| P(K4 detecteert vóór TR) | 0 | 0 | ≤ 5 % | geen VOC-kanaal |
| Max. diepte waarop een TR-puls ≥ 5 K aan het oppervlak geeft (vape / 18650 / powerbank) | – | 0,13 / 0,23 / 0,35 m | – | warmte_gas (b) |
| Snelheid rookgaspluim (Darcy) | 0,11 cm/s | 1,1 cm/s | 11 cm/s | [A] permeabiliteit 1e-8…1e-6 m² |
| K4 regel E: P(detectie smeulbrand ≤ 10 min) | 0,22 | 1,0 | 1,0 | valsalarm_mc |
| K4 regel E: P(detectie smeulbrand ≤ 60 min) | 0,48 | 1,0 | 1,0 | idem |
| K4 regel D: P(detectie ≤ 60 min) | 0,78 | 1,0 | 1,0 | idem |
| K4 hinderalarm (rotting, zon, zakken, uitlaatgas) per container-jaar, regel E | 0 | 0 | 0,03 | idem (model; zie beperkingen) |
| K4 alarm door heet object (as, peuk, vuurwerk) per container-jaar | 0,5 | 1,9 | 4,2 | idem; aanname 0,5/2/5 per jaar |
| "Niet legen"-vlag actief op het moment van lediging, per 1.000 containers per jaar | 24 | 88 | 201 | idem; ≈ 0,5 / 1,7 / 3,9 per week |
| P(vlag terecht): accubrand / brand ongeacht oorzaak / brand of heet object | 0,0001 / 0,0001 / 0,99 | 0,0003 / 0,0013 / 1,0 | 0,002 / 0,01 / 1,0 | idem |
| B1 camera laadbak: P(detectie Li-brand in wagen) | 0,19 | 0,49 | 0,76 | b1_laadbak |
| B1 reactietijd (mediaan / p90) | 1 s / – | 1 s / 81 s | 1 s / 47 s | idem |
| B1 kosten per container per maand | 0,07 | 0,21 | 0,56 | €3–8k per wagen, 300–800 UGC |
| Waarde van K4 (vermeden containerschade) per container per maand | 0,02 | 0,67 | 3,75 | idem [A] |

## Test 1 – Detectievenster vóór TR per mechanisme (`tijdlijn_TR.py`, `fig_tijdlijn_TR.png`)
- **Vraag:** hoeveel tijd zit er tussen het eerste externe signaal en de TR, en welk kanaal haalt dat?
- **Methode:** literatuur in een tabel (Li-ion Tamer: 6,4 min bij DNV-GL en 9–25 min volgens Honeywell; UN GTR 20: 5 min; crush: seconden) en de kanaallatenties uit test 3 en test 5.
- **Resultaat:** alleen extern oververhitten en overladen geven 5–30 min. Die mechanismen zijn in een container zeldzaam: compost blijft onder 50 °C [A]. Een latente short geeft 0–15 min (NG, [A]). Persen en shredder geven 0–30 s.
- **Conclusie:** een venster vóór TR bestaat praktisch niet voor de relevante mechanismen. Alle zuil- en containerconcepten moeten na TR detecteren.

## Test 2 – Warmte- en gastransport (`warmte_gas.py`, `fig_warmte_diffusie.png`)
- **Methode:** analytische puntbron (puls en continu) in afval met α = 1,5e-7 m²/s en spiegelfactor 2 voor het oppervlak. Gas met koude diffusie (D_eff 3e-6…1e-5) of als warme Darcy-pluim. MC over de diepte bij falen: de afvalstapel stijgt 0,28 m/dag, de vertraging van inworp tot falen is exponentieel met gemiddeld 72 / 6 / 0,5 h [A].
- **Resultaat:**
  - Een 18650-puls (99 kJ) geeft maximaal 518 / 65 / 8 / 2,4 K op 5 / 10 / 20 / 30 cm. De piek op 30 cm komt pas na ~28 h.
  - Een smeulnest van 200 W is via geleiding aan het oppervlak zichtbaar na 2,4 h vanaf 0,17 m en na 41 h vanaf 0,62 m.
  - De rookgaspluim bereikt de kopruimte vanaf 1 m diepte in 9 s tot 15 min.
  - Koud ventgas doet over 1 m 14–46 h.
- **Conclusie:**
  1. IR werkt alleen voor de bovenste ~0,3 m. CO via de warme pluim werkt ook dieper.
  2. Als cellen vooral kort na de inworp falen (basis), liggen ze ondiep: mediaan 0,14 m, en 95 % ligt hoger dan 0,3 m. Daarmee is detectie na TR goed.
  3. Onbekend is hoe de vertraging van inworp tot falen verdeeld is. Dat is de grootste onzekerheid.

## Test 3 – Vals alarm en detectie K4 (`valsalarm_mc.py`, `fig_valsalarm.png`, `event_model_K4.json`)
- **Methode:** 120 container-jaren per scenario met stappen van 5 min.
  - Achtergrond: seizoen en dag, zon (bovengronds), compost +0–12 K per week, verse zakken van 18–40 °C, CO-basis (lognormaal, mediaan 3 ppm), fermentatie-episodes (0,15–0,6 per week, 20–50 ppm, inclusief H₂-kruisgevoeligheid), uitlaatgas bij lediging en vuurwerk. Warme as of peuk zonder brand: 0,5 / 2 / 5 per jaar [A].
  - Brand: 4.000 events per scenario, Darcy-pluim plus kopruimtemodel (V 0,5–3,5 m³, ACH 0,5–5/h). TGS5042 met t90 = 60 s (Figaro-datasheet).
  - Regels: A CO > 50 ppm · B dCO > 30 ppm per 10 min · C IR > 45 °C én > 20 K boven de mediaan · D 2-van-3 · E B∧C of B∧CO > 150 ppm.
- **Resultaat:**
  - Alleen een absolute CO-drempel (A) geeft 2 / 10 / 36 hinderalarmen per container-jaar. Die regel is onbruikbaar.
  - Een stijgsnelheid plus coïncidentie (D, E) maakt de hinder in het model ≈ 0.
  - Wat overblijft zijn hete objecten. Voor "niet legen" zijn die terecht, want hete as in de wagen is ook een brandoorzaak, maar het zijn geen accu's.
  - De vlag wordt zelden door een accu veroorzaakt (PPV voor accu 0,01–0,2 %).
- **Conclusie:**
  - K4 is een **brand- en heet-objectdetector** met een terechte vlag (≈ 100 % brand of heet object) en een acceptabele last (≤ 4 actieve vlaggen per week per 1.000 containers, ruim binnen B2).
  - K4 is **geen accudetector**.
  - Advies: regel D voor ondergrondse containers (hogere detectie bij diepe cellen), regel E voor bovengrondse bakken (minder zon- en CO-hinder: 0,03 tegen 6,4 per jaar).

## Test 4 – Energie en sensorspecificaties (afgeleid, geen script)
- TGS5042 werkt passief (~0 W) in −10…+60 °C (datasheet 11/12). Onder een bovengrondse deksel in de zon (tot 65 °C, [A]) valt hij buiten de specificatie.
- 8×8 IR elke 5 min: ~5 mA × 3,3 V × 0,5 s / 300 s ≈ 0,03 mW ≈ 0,25 Wh/jaar. Past ruim in 25 mWh/dag (A5).

## Test 5 – B1 thermische camera laadbak (`b1_laadbak.py`, `fig_b1_laadbak.png`)
- **Methode:** de TR-vertraging na crush is lognormaal met mediaan 20 s; 10–25 % is laat (10 min – 5 h) [A]. Zichtvenster in de laadbak 20–600 s, zichtbaarheid 30–70 %, plus een pluim bij een diepte van 0,3–0,8 m. Alarm bij 93 °C (Seek Thermal, pilot Goodyear AZ; SWANA-award 2025).
- **Resultaat:** P_det 0,19 / 0,49 / 0,76 met reactie in ~1 s. Kosten €0,07–0,56 per container per maand. Met een "hot load dump" vermijdt elke gedetecteerde wagenbrand gemiddeld €1k / 8,5k / 32k [A].
- **Conclusie:** **B1 domineert K4 voor het hoofdrisico (stap 5)**. Het is goedkoper per container, grijpt in waar het risico zit en is bewezen in de praktijk. K4 voegt alleen bescherming van de container zelf toe (stap 3) en voorkomt dat een smeulende container in de wagen wordt gestort. De waarde daarvan, €0,02–3,75 per container per maand, rechtvaardigt K4 alleen als goedkope add-on op een bestaande vulgraad- of zuilmodule, niet als eigen device.

## Beperkingen (eerlijk)
- Het hinderalarm van IR (≈ 0) volgt uit de aanname dat geen object zonder brand boven 45 °C komt met 20 K boven de mediaan, behalve as en vuurwerk. Dat moet in het veld gemeten worden.
- De permeabiliteit van losse zakken (1e-8…1e-6 m²), de fractie gas die de kopruimte bereikt en de verdeling van de vertraging tussen inworp en falen zijn niet gemeten [A]. Die bepalen het verschil tussen P_det 0,48 en 1,0.
- Het aantal hete-objectevents per container-jaar (0,5–5) is een aanname. Het bepaalt de vlaglast lineair.
- Het percentage containerbranden door accu's (A7: 0,02–0,1 % per UGC per jaar) is niet gevonden.

## Alleen met prototype te bevestigen – labtestontwerp

| # | Opstelling | Testobjecten | Protocol | Meet / succescriterium |
|---|---|---|---|---|
| L1 Gaspluim | Stalen kist van 1 m³ (of afgedankte UGC) met 60 echte, dichtgeknoopte restafvalzakken; K4-prototype en referentie-CO-meter (elektrochemisch, ppm-log 10 s) onder de deksel | Warmtebron 200 W met CO-tracer (1–5 L CO/H₂-mengsel 1 %) op 0,2 / 0,5 / 1,0 m diepte; koude injectie als controle | 3 diepten × 2 (warm/koud) × 5 herhalingen = 30 runs; ACH meten met CO₂-afvaltest | Aankomsttijd en piek-ppm → kalibreer permeabiliteit en f_reach. Succes: warme bron op 1 m binnen 15 min > 30 ppm |
| L2 Brandproef | Oefenterrein van de brandweer, UGC met afval, IR 8×8 + CO + thermokoppels | 18650 (100 % SOC), vape, powerbank via nagel of verwarmingsdraad op 0,1 / 0,5 / 1 m | 3 × 3 × 2 herhalingen = 18 runs, video + gasanalyse (FTIR optioneel) | Detectietijd per regel D/E. Succes: ≥ 80 % binnen 30 min |
| L3 Veldachtergrond | 3 containers (2 ondergronds, 1 bovengronds, waarvan 1 bij horeca/station), 8 weken in juni–aug | K4-prototype + referentie-CO + T-logger, inworp- en ledigingslog van de zuil | 1-min logging, ruwe data, regels offline | Hinderalarmen per container-jaar (doel < 0,1), CO-fermentatieprofielen, IR-heterogeniteit |
| L4 Sensoroverleving | Klimaatkast 60 °C / 95 % RV en H₂S 5–20 ppm | 5× TGS5042, 3× AMG8833 met hydrofoob venster | 1.000 h, wekelijks ijken met 100 ppm CO | Gevoeligheidsdrift < 20 %, venster niet beslagen |
| L5 B1-referentie | Meerijden met een Seek-/Lepton-camera boven de laadbak, 4 wagens × 3 maanden | – | Log hotspots > 93 °C en incidenten | Aantal alarmen per wagen per maand en terechtheid |

## Bestanden
- `experiments/r3_thermisch/event_model_K4.json`: P(detectie brand binnen 10/30/60 min) per regel en scenario, vals alarm per container-jaar (totaal / hinder / heet object), P(vlag terecht), vlaggen actief bij lediging, formaat voor A6 (apart event-kanaal, geen p_out_given_item)
- Figuren: `fig_tijdlijn_TR.png`, `fig_warmte_diffusie.png`, `fig_valsalarm.png`, `fig_b1_laadbak.png`

Bronnen: zie research/A4_thermisch_gas.md, en daarnaast Figaro TGS5042 productinformatie (rev09, t90 ≤ 60 s): https://www.figarosensor.com/product/tgs5042_product%20information%28fusa%29_rev09.pdf · Goodyear AZ / Seek Thermal (hoodline 2025-09): https://hoodline.com/2025/09/goodyear-wins-2025-best-safety-innovation-award-for-revolutionary-trash-truck-fire-detection-technology/
