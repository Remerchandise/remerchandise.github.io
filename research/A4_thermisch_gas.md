# A4 – Thermisch, gas & continue monitoring (Ronde 0 research)

Agent 4 · peildatum 2026-10 · EUR 2026 excl. btw · aannames **[A]** · "NG" = niet gevonden / niet geverifieerd

## 0. Kernbevindingen (TL;DR)

1. **Een cel die in de container "rustig" ligt, geeft vrijwel geen meetbaar signaal tot de vent opent.** Vóór venting: alleen lokale opwarming in de cel; afval isoleert extreem (thermische diffusiviteit ~1–2·10⁻⁷ m²/s → 0,1 m afval ≈ 18 h, 0,5 m ≈ 19 dagen geleidingstijd). Een temperatuursensor op de deksel ziet een begraven cel **pas als er brand/rookpluim is**.
2. **Waarschuwingsvenster off-gas → thermal runaway (TR) is abuse-afhankelijk:** oververhitting/overladen: ~5–30 min (Li-ion Tamer: 6,4 min bij DNV-GL; 9–25 min in andere tests – leveranciersbron). Crush/penetratie (vuilniswagen): **seconden, geen venster**. Latente interne kortsluiting na valschade: onbekend (minuten–uren, intermitterend) – **NG** voor afvalcontext.
3. **Gas bereikt de sensor niet snel genoeg bij een zak onderin**: zuivere diffusie door 1 m afval ≈ 1 dag; alleen een warme pluim (= al TR/smeulen) brengt gas in minuten naar boven. Vent-damp vóór TR (≈ 0,05–0,3 L elektrolytdamp per 18650 **[A]**) verdunt in ~2 m³ kopruimte tot 25–150 ppm *als* het al aankomt.
4. **Na ontsteking is detectie wél makkelijk en goedkoop** (CO, H₂, VOC, dT/dt, IR): orde minuten. Realistische waarde van continue monitoring = **vroege branddetectie in de container + "NIET LEGEN"-vlag** voor de chauffeur (voorkomt dat een smeulende container in de wagen wordt gestort), niet "voorspellen vóór TR".
5. **Vals alarm:** rottend restafval produceert zelf CO₂ (0,1–5 %), CO (tientallen–honderden ppm in compost), H₂ (anaerobe fermentatie), H₂S, NH₃, ethanol/esters en warmte (+5–20 K **[A]**). H₂ en CO zijn dus **niet uniek**. Onderscheid moet komen uit **snelheid** (dC/dt, dT/dt in minuten vs. uren–dagen) en combinatie (CO + H₂ + VOC + T tegelijk).
6. **Vocht dempt het risico:** Chen et al. 2025 (PolyU) – één 18650 kon bij ≥30 % vocht in afval geen smeulbrand starten; min. 50 % SOC nodig in droog afval. NL-restafval is vaak 25–40 % vocht **[A]** → container zelf is een minder waarschijnlijke brandhaard dan de wagen (consistent met kickoff).
7. **Markt:** vulgraadsensoren (Sensoneo, Nordsense, Ecube) hebben al een temperatuursensor/"fire alarm" als optie → een temperatuur-brandalarm is **commodity**; onderscheidend vermogen moet uit gas-/inworpcombinatie komen.

## 1. Fases van thermal runaway

| Fase | Celtemp. | Wat gebeurt er | Gas / signaal | Detecteerbaar van buiten de cel? |
|---|---|---|---|---|
| 0 Latent defect | omgeving | Deuk, Li-plating, soft short | geen | Nee |
| 1 SEI-decompositie | ~80–120 °C (start 60–90) | Exotherme SEI-afbraak, zelfverhitting mW–W | intern CO₂, C₂H₄ (nog in cel) | Alleen T aan celoppervlak |
| 2 Separator smelt / druk stijgt | 130 °C (PE), 165 °C (PP) | Interne druk ↑, CID/vent opent bij ~1–2 MPa (18650) | **1e venting**: elektrolytdamp (DMC, EMC, DEC, EC), CO₂, sporen H₂ | Ja – "off-gas" (Li-ion Tamer-principe), hoorbaar "plop/sis" **[A]** |
| 3 Kathode-decompositie → TR | 150–250 °C onset, piek 500–900 °C | O₂ uit kathode (NMC/NCA), dT/dt > 1 K/s, vlam/vonken | Hoofdgas: CO₂ ~20–45 %, CO ~10–30 %, H₂ ~15–30 %, CH₄, C₂H₄, C₂H₆; HF (≈20–200 mg/Wh, Larsson 2017) | Ja, zeer duidelijk (rook, CO, H₂, IR, druk) |
| 4 Brand omgeving | – | Ontsteking karton/plastic; smeulen in afval | CO hoog, rook, VOC | Ja, minuten |

Gasvolume TR: orde **0,5–2 L per Ah** (NMC, 100 % SOC) **[A, literatuurbandbreedte; Koch et al. 2018 Batteries 4(2):16 – exacte waarden niet geverifieerd]** → 18650 (3 Ah, 11 Wh): ~2–6 L; vape-cel (0,3–0,5 Ah): ~0,2–1 L; powerbank 10 Ah: 5–20 L.
Gassamenstelling: soortgelijke species over studies, concentraties variëren sterk (review Baird et al. 2020); HSE-studie max CO 16,9 vol%, CH₄ 7,6 %, C₂H₄ 7,9 % (gasmet.com samenvatting).

### Tijdvensters (detectie vóór TR)

| Mechanisme | Venster 1e venting → TR | Bron / status |
|---|---|---|
| Extern oververhitten | 5–30 min | Li-ion Tamer 6,4 min (DNV-GL), 9–25 min (Honeywell artikel); "tot 30 min" (trade) – leverancier |
| Overladen (BESS) | minuten–tientallen min | idem; niet relevant in container |
| Nail/crush (wagen) | 0–10 s | algemene literatuur; geen bruikbaar venster |
| Latente soft short na val | **NG**; vermoedelijk meeste cellen falen direct of nooit **[A]** | nader onderzoek |
| Regelgeving | UN GTR 20 (EV): 5 min waarschuwing vóór gevaar | via Cai dissertatie (UMich 2021) |

Cai et al. (UMich, 2020 arXiv 2010.13519; dissertatie 2021): CO₂ via NDIR is beste doelgas voor venting-detectie; plus krachtsensor voor zwelling. Gas-sensoren reageren in 1–8 s (Amphenol, vendor). Koch/Birke (genoemd in ICMIE 2022): gassensor detecteerde TR het snelst van alle sensortypen.

## 2. Wat gebeurt er in een container?

| Parameter | Waarde laag / basis / hoog | Opmerking |
|---|---|---|
| Volume ondergrondse container | 3 / 5 / 5 m³ | kickoff |
| Vrije kopruimte (half vol) | 0,5 / 2 / 3,5 m³ | **[A]** |
| Poriënvolume tussen zakken | 30 / 50 / 70 % | **[A]**; maar zakken zijn dicht → gas blijft deels in zak |
| Massa afval vol | 300 / 500 / 800 kg | **[A]** ~100–160 kg/m³ |
| Thermische diffusiviteit afval | 1 / 1,5 / 3 ·10⁻⁷ m²/s | **[A]** (vergelijk droog stro/grond) |
| Geleidingstijd t≈L²/α tot 0,1 / 0,3 / 0,5 m | 18 h / 7 d / 19 d | berekend (α=1,5·10⁻⁷) |
| Bulk-ΔT 50 kg afval door 11 Wh | 0,4 K | berekend → bulktemp. nutteloos |
| Diffusietijd gas (D=10⁻⁵ m²/s) 0,3 / 1 / 2 m | 2,5 / 28 / 111 h | berekend; convectie/pluim kan 100–1000× sneller |
| Verdunning in 2 m³: 0,05 / 0,3 / 1,3 L gas | 25 / 150 / 650 ppm | 1,3 L ≈ H₂ uit TR 18650 |
| Drukpuls 3 L in 2 m³ (afgesloten) | ~150 Pa | in praktijk lekt deksel/trommel → transiënt < 10–50 Pa **[A]** |
| Temperatuur ondergronds binnencontainer | 8 / 15 / 25 °C | grond/betonput buffert **[A]** |
| Temp. onder deksel minicontainer/bovengrondse bak (zomer, zon) | 35 / 50 / 65 °C | **[A]**, opdrachtgever noemt 50–60 °C |
| Compostwarmte restafval (gesloten zakken, 1–2 wk) | +2 / +8 / +20 K | **[A]** zuurstofgelimiteerd; grote hopen halen 60–70 °C, container niet |
| Vocht restafval NL | 20 / 30 / 45 % | **[A]**; Chen 2025: ≥30 % → 1 cel start geen smeulbrand |

**Consequenties:**
- Cel onderin onder 0,5–2 m afval: thermisch en qua gas **onzichtbaar tot echte brand**. Cel bovenop (net ingeworpen): T en gas wél binnen minuten zichtbaar.
- Gas van TR is heet → stijgt op als pluim door poriën; H₂ is licht → snelle opstijging. Detectie in kopruimte van **rook/CO/H₂ binnen 1–10 min na TR** is plausibel **[A, te modelleren R3]**.
- Ventilatie: ondergrondse containers zijn semi-gesloten (inworptrommel, kieren deksel) → luchtwisseling 0,5–5 /h **[A]** → gasconcentratie piekt en daalt over tientallen minuten; continu meten met interval ≤ 1–2 min nodig rond event.

### Vals-alarmbronnen (rotting / omgeving)

| Bron | CO₂ | CO | H₂ | VOC | H₂S/NH₃ | T | Tijdschaal |
|---|---|---|---|---|---|---|---|
| Aerobe afbraak | 0,1–5 % | 0–50 ppm | ~0 | ethanol, terpenen, esters | NH₃ | +2–20 K | uren–dagen |
| Anaerobe zone (natte zakken) | ↑ | tot 100+ ppm **[A]** | 1–100+ ppm **[A]** | zuren, mercaptanen | H₂S ppm | – | dagen |
| Zon op deksel | – | – | – | VOC uit plastic ↑ | – | +20–40 K | dagelijkse cyclus |
| Sigarettenpeuk / as in bak | ↑ | 10–500 ppm | sporen | rook | – | lokaal | minuten → **echte brand, terecht alarm** |
| Vuurwerk (jaarwisseling) | | ↑ | | rook | | ↑ | minuten |
| Vape (intact) | – | – | – | PG/VG + aroma | – | – | constant |
| Li-ion TR | ↑↑ | ↑↑ (100–10k ppm lokaal) | ↑↑ | carbonaten | sporen HF | ↑↑ lokaal | **seconden–minuten** |

Onderscheid = **tempo + coïncidentie**: TR geeft gelijktijdige sprong in CO, H₂, VOC (en T als dichtbij) binnen < 5 min; rotting is traag (uren) en H₂ zonder CO-sprong.

## 3. Sensoren (prijzen 2026, excl. btw, volume ~1k tenzij anders)

| Sensor | Meet | Prijs EUR (l/b/h) | Vermogen | Drift/levensduur | Opmerking |
|---|---|---|---|---|---|
| NTC 10k (glas) | T punt | 0,05 / 0,2 / 0,5 | µW (gepulst) | stabiel | string van 8 in RVS-kabel: 5 / 10 / 20 |
| DS18B20 / SHT4x | T (+RV) | 1 / 2 / 3 | µW–µA | SHT4x: RV-drift bij condens | standaard in vulgraadsensoren |
| Lineaire thermokabel (digitaal, 68–88 °C) | T-drempel langs lijn | 3 / 5 / 8 per m | 0 (passief) | jaren | brandmeldtechniek (Protectowire-type) **[A prijs]** |
| Glasvezel DTS | T over lengte | > 5 000 systeem | W | – | **niet haalbaar** per container |
| MLX90614 | IR 1 pixel (FOV 35–90°) | 6 / 10 / 15 | 1–2 mA cont.; gepulst µW gem. | ±0,5 K | ziet alleen oppervlak |
| Panasonic AMG8833 Grid-EYE | IR 8×8 | 12 / 18 / 25 **[A]** | 4,5 mA | – | |
| MLX90641 | IR 16×12 | 12 / 16 / 22 **[A]** | ~20 mA | – | |
| MLX90640 | IR 32×24 | 25 / 28 / 33 | ~20 mA, frame < 1 s | – | DigiKey $35,32 (1 st) / $28,40 (100) |
| Heimann HTPA32x32d | IR 32×32 | 40 / 60 / 90 **[A, NG]** | ~10 mA | – | |
| FLIR Lepton 3.5 | IR 160×120 radiometrisch | 120 / 135 / 150 | ~150 mW | – | GroupGets $149,99; DigiKey $140 |
| Sensirion SGP41 | VOC/NOx index (MOX) | 4 / 5 / 7 **[A]** | ~3 mA @3,3 V ≈ 10 mW tijdens meting; algoritme wil 1 Hz | baseline-adaptief (relatief, geen ppm) | index past zich aan → traag lek "verdwijnt" |
| Bosch BME688 | VOC/VSC/H₂/CO-klassen via heaterprofielen + AI, T/RV/p | 5 / 6 / 8 | ULP ~0,1 mA gem. (≈0,3 mW), heater pulsen | drift, vochtgevoelig | DigiKey $8,65 / $5,76 (3k); BME AI-Studio trainbaar (vape/elektrolyt/compost?) |
| Figaro TGS5042 | CO elektrochemisch | 10 / 15 / 22 **[A]** | ~0 (geen heater) | 7–10 jr | ideaal batterijgevoed; reageert ook op H₂ (kruisgevoelig) |
| Alphasense CO-A4/CO-AF | CO elektrochemisch, ppb | 35 / 50 / 70 **[A]** + AFE 20 | µW | 2–3 jr | overkill |
| Figaro TGS2615-E00 | H₂ MOX | 8 / 10 / 14 **[A]** | heater ~50–300 mW **[A]** | vochtdrift | alleen gepulst; slecht voor batterijvoeding |
| Sensirion STC42A (2026) / STC31 | H₂ (of CO₂) via thermische geleiding | 12 / 20 / 30 **[A]**; eval-kit €51,80 | mW-orde **[A]** | factory-gekalibreerd, AEC-Q100 | persbericht 16-06-2026 "TR detection"; %-bereik → ongevoelig voor ppm-niveaus in container |
| NDIR/PA CO₂ (SCD41, Senseair Sunrise) | CO₂ ppm | 15 / 22 / 35 | SCD41 low-power ~0,5 mA gem.; Sunrise µA-orde | ABC-kalibratie faalt in afval (nooit 400 ppm) | compost-CO₂ maakt CO₂ nutteloos als enige gas |
| Optische rookmelder-kamer | rook | 3 / 6 / 10 | µA | stof/condens → vals | goedkoop, robuust indien beschermd |
| Honeywell Li-ion Tamer GEN3 | elektrolytdamp ppm | 250 / 500 / 900 **[A, NG]** | netvoeding 12–24 V | – | voor BESS; te duur en net-gevoed |
| MEMS-microfoon (wake-on-sound) | akoestiek (vent-"plop") | 0,5 / 1 / 2 | ~10 µW wake-mode | – | onconventioneel |
| Barometer BMP390 | drukpuls | 2 / 3 / 4 | µA | – | wind/deksel geeft ruis |

**Energie:** budget batterijgevoed device (bv. 2× Li-SOCl₂ D, ~2×19 Wh = 38 Wh, 10 jr) ≈ **10 mWh/dag ≈ 0,4 mW gemiddeld** **[A]**. Continue MOX (10 mW) = 88 Wh/jaar → onhaalbaar; gepulste BME688/TGS5042/NTC/1-pixel IR elke 1–5 min past ruim. MLX90640 elke 10 min: ~20 mA·3,3 V·1 s/600 s ≈ 0,1 mW → OK.

**Kalibratie/vocht:** RV in container 80–100 % met condens **[A]** → membraan (ePTFE), sensor in kopruimte bovenin, niet in afval. MOX-baseline drift: werken met relatieve sprongen (Δ binnen 5 min) i.p.v. absolute ppm.

## 4. Bestaande producten met temperatuur/brandalarm

| Product | Wat | Brand-functie | Bron |
|---|---|---|---|
| Sensoneo Single/Quatro Sensor | ultrasoon vulgraad, NB-IoT/LTE-M/Sigfox | T-meting + "fire alarm" optioneel; claim: overleefde brand ondergrondse bak oudejaarsnacht | sensoneo.com (z.d., geraadpleegd 2026-10) |
| Nordsense | laser vulgraad, T, accelerometer, elke 15 min | T-meting; brandalarm **NG** | nordsense.com |
| Ecube Labs CleanCAP/CleanCUBE | vulgraad / perscompactorbak | "fire detection sensor" (werking NG) | Ecube brochure |
| Smartsensor (AU) | vulgraad + T | alerts bij plotselinge T-stijging | startus-insights |
| Enevo, BrighterBins, Bigbelly | vulgraad (BigBelly compactor) | T/brand **NG** in deze ronde | – |
| Honeywell Li-ion Tamer | off-gas BESS | 6,4–25 min vóór TR | honeywell.com |

→ **Implicatie:** gemeenten met vulgraadsensoren hebben vaak al een T-alarm "gratis". Ons continu-monitoringdeel moet (a) combineren met inworpdetectie en (b) beter scoren op snelheid en vals alarm (multi-gas).

## 5. Context NL

- NVRD (NOS, 2023): ≥3×/maand brand in vuilniswagen, tientallen per jaar, vooral Li-ion/vapes. Vereniging Afvalbedrijven: ~10 branden/maand (inzamelplaatsen + wagens) ≈ 120/jr.
- Containerbranden zelf: vaak vuurwerk/brandstichting/peuken **[A]**; aandeel Li-ion **NG**.

## 6. Niet gevonden / open

- Exacte Koch 2018 gasvolumes per Ah; Li-ion Tamer GEN3 prijs; Heimann prijs; SGP41/TGS5042 actuele distributeursprijs.
- Gemeten temperatuur- en gasprofielen (CO, H₂) in NL-ondergrondse restafvalcontainers over 1–2 weken → **meetcampagne voorstellen** (1 container, BME688 + TGS5042 + NTC, €100, 4 weken).
- Kans op vertraagde TR (uren–dagen) na valschade.

## Bronnen (datum)

- Honeywell, "National lab testing demonstrates value in early detection" (z.d., geraadpleegd 2026-10): https://www.honeywell.com/us/en/insights/articles/national-lab-testing-demonstrates-value-in-early-detection
- Solar Builder, "Li-ion Tamer: preventing thermal runaway before it begins" (z.d.): https://solarbuildermag.com/news/li-ion-tamer-preventing-thermal-runaway-before-it-begins/
- Cai, Mohtat, Stefanopoulou, Siegel, "Li-ion battery fault detection in large packs using force and gas sensors", arXiv 2010.13519 (2020-10): https://www.arxiv.org/abs/2010.13519
- T. Cai, dissertatie "Detection of Lithium-ion Battery Failure and Thermal Runaway", UMich (2021): https://deepblue.lib.umich.edu/handle/2027.42/169734
- Koch, Fill, Birke, "Comprehensive gas analysis on large scale automotive Li-ion cells in thermal runaway", Batteries 4(2):16 (2018) – waarden niet geverifieerd
- Gasmet, "Composition and explosibility of gas emissions from Li-ion batteries undergoing TR" (HSE-studie): https://www.gasmet.com/applications/safety/safety-research/composition-and-explosibility-of-gas-emissions-from-lithium-ion-batteries-undergoing-thermal-runaway/
- Larsson et al., "Toxic fluoride gas emissions from lithium-ion battery fires", Sci. Rep. 7 (2017-08)
- Chen et al., "Underground fires induced by disposed Li-ion battery in peatland and landfill", PSEP (2025): https://research.polyu.edu.hk/en/publications/underground-fires-induced-by-disposed-li-ion-battery-in-peatland-/
- Gausden & Cerik, "Single-use vape batteries … ignition sources in waste", Batteries (2024-07): https://dspace.lib.cranfield.ac.uk/items/30829f9b-1b57-42f8-aced-a213a6c93b4a
- Sensirion persbericht STC42A (2026-06-16): https://sensirion.com/company/news/press-releases-and-news/article/sensirion-announces-global-availability-of-the-stc42a-automotive-h2-sensor-for-thermal-runaway-detection
- DigiKey MLX90640 / BME688 productpagina's (geraadpleegd 2026-10): https://www.digikey.com/en/products/detail/melexis-technologies-nv/MLX90640ESF-BAB-000-SP/8638466 , https://azcus.digikey.com/en/products/detail/bosch-sensortec/BME688/13681261
- GroupGets Lepton 3.5 (geraadpleegd 2026-10): https://groupgets.com/products/flir-lepton-3-5
- Sensoneo productpagina's (geraadpleegd 2026-10): https://www.sensoneo.com/en-us/products/smart-fill-level-sensors-dumpsters-containers/ ; https://partners.sigfox.com/products/quatro-sensor-868
- Nordsense platform: https://nordsense.com/ns-platform/ ; Ecube brochure: https://ecubelabs.com/data/market/Ecube_brochure_EN.pdf ; StartUs Insights smart bins: https://www.startus-insights.com/innovators-guide/5-top-smart-bin-solutions-impacting-smart-cities/
- NOS, "Jaarlijks tientallen branden in vuilniswagens door batterijen en accu's" (2023): https://nos.nl/l/2485439

## 7. Plan Ronde 3 (experiments/A4_*)

| # | Experiment | Methode | Output / beslisvraag |
|---|---|---|---|
| E1 | Warmtetransport cel → sensor | 2D/axisymmetrische FD-geleiding (scipy) cel (11 Wh, TR-piek 600 °C) in afvalmatrix, diepte 0–2 m; sensor op deksel, wand-NTC-string, IR op oppervlak | Tijd tot ΔT>5 K bij sensor per diepte; vanaf welke diepte is T-detectie zinloos |
| E2 | Gastransport | 1D diffusie + buoyante Darcy-advectie door poreuze afvalkolom; bron: venting 0,05–0,3 L (pre-TR) en TR 2–6 L (18650) / 0,2–1 L (vape); kopruimte 0,5–3,5 m³, ACH 0,5–5/h | ppm CO/H₂/VOC bij sensor vs. tijd; **detectievenster vóór TR** per diepte |
| E3 | Detectievenster per mechanisme | tabel + Monte Carlo: oververhitting (5–30 min), latente short (verdeling **[A]**), crush (0 s) × transportvertraging E1/E2 | Kans dat alarm vóór TR komt; verwacht: ~0 % voor zak onderin, 30–60 % voor bovenste laag **[A]** |
| E4 | Vals-alarm | synthetische 14-daagse tijdreeksen rotting (CO₂, CO, H₂, VOC-index, T dagcyclus, zomer 60 °C deksel) + TR-events; regels: drempel, dC/dt, coïncidentie 2-uit-3 | ROC; vals alarm per container per jaar (doel < 0,1) |
| E5 | Energiebudget | duty-cycle per sensorset | Wh/jr vs. 38 Wh/10 jr |
| E6 (optioneel, fysiek) | BME688 neus-test | compostzak, vape (intact/lek), DMC-druppel, peuk in doos | haalbaarheid "vape-neus" en elektrolytsignatuur |
