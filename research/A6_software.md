# A6 – Software, signaal & dashboard (Ronde 0 research)

Agent 6 · peildatum 2026-10-25 · EUR 2026 excl. btw · aannames = **[A]**

## 0. Kern in vijf punten

1. **De basisfrequentie bepaalt alles.** Met 28 losse batterijen/ton restafval (Eureco/St. OPEN, apr 2026) plus batterijen in apparaten (~7/ton) en ~2 vapes/ton zit er in **elke lediging van een ondergrondse container (~80–120 zakken) vrijwel zeker ≥ 1 batterij** en in 60–100 % van de ledigingen ≥ 1 Li-houdend item (§2.3). Een ja/nee-alarm per container is dus waardeloos: de drempel moet op **risico-score (Wh, aantal cellen, Li-ion, schade)** of **relatieve rangorde** liggen.
2. **Metaal zit in bijna elke zak** (ferro 2,0 % + non-ferro 1,6 % ≈ 3,6 % gewicht → ~200 g metaal per zak van 6 kg). Bij 3 % Li-zakken geeft een detector met recall 0,9 en vals-positief 30 % een precisie (PPV) van **8,5 %**; pas bij FPR ≤ 1 % wordt PPV > 70 %. → A2 moet FPR per zak < ~3 % halen, anders alleen als "ruwe prior" bruikbaar.
3. **Bayesiaanse accumulatie per container** (log-odds optellen per inworp, verval bij lediging) is de natuurlijke logica; ze is robuust tegen ruis van één meting en past op een microcontroller (< 1 kB RAM).
4. **Signaalketen is opgelost terrein:** LoRaWAN (51 B bij SF10–12) volstaat ruim voor een 11-byte bericht; koppeling via de bestaande **ContainerDevice-/vulgraad-API's** (HVC, OAuth2) en STOSAG-achtige pas-/containerdata. Er is **geen actieve open standaard** voor sensorevents (STOSAG 1.0 in 2018 als verouderd beoordeeld).
5. **AVG:** container-niveau-alarm = geen persoonsgegeven. Koppeling aan de pashouder = profilering met handhavingseffect → DPIA verplicht, proportionaliteit zwak (Arnhem-zaak AP 2017). Advies: **standaard ontkoppeld**, alleen geaggregeerde feedback.

## 1. Detectielogica

| Laag | Methode | Input | Rekenlast | Geschikt voor | Opmerking |
|------|---------|-------|-----------|---------------|-----------|
| L0 | Vaste drempel | 1 feature (bv. ΔL inductie, piek-amplitude) | triviaal | MVP, A2-C "strandmetaaldetector" | Hoge FPR door blikjes/folie |
| L1 | Twee-drempel + hysterese + duur | feature + stilstandtijd in trommel | triviaal | elk concept | "Langer meten" (uitgangspunt 1) verlaagt ruis ∝ 1/√t, maar **niet** de verwisseling blik↔cel (systematisch, geen ruis) |
| L2 | Logistische regressie / naive Bayes | 3–8 features (amplitude, fase/tijdconstante → geleidbaarheid, multi-frequentie ratio, gewicht zak, temp) | ~20 MAC | edge (Cortex-M0+) | Interpreteerbaar; coëfficiënten OTA te updaten via downlink (51 B) |
| L3 | kNN (k=5) op ~500 referentievectoren | idem | 500×8 = 4 k ops, 4 kB flash | edge | Goed bij weinig trainingsdata; slecht bij drift |
| L4 | Tiny 1D-CNN (TFLite Micro / Edge Impulse) | ruwe pulsrespons (PI-detector, 64–256 samples) of multi-freq sweep | 10–50 k MAC, 20–60 kB flash | Cortex-M4F (nRF52840, STM32L4) | Vereist ≥ 1 000 gelabelde inworpen per klasse **[A]**; labelen = lastig (zak openen) |
| L5 | Bayesiaanse accumulatie per container | per-inworp likelihood-ratio LRᵢ | 1 optelling | altijd, bovenop L0–L4 | `S = Σ log LRᵢ`; reset bij lediging (vulgraad-sprong of route-event); alarm als S > θ of P(≥1 hoog-risico) > p* |
| L6 | Fusie per-inworp + continu (A4) | LR inworp × LR temp/gas | triviaal | container-niveau | Continue meting (temp/CO/H₂) is evidentie met lage prior maar hoge LR bij event |

**Bayes per container (aanbevolen kern):**
- Per inworp: classificator levert P(klasse | x) voor {geen metaal, blik/folie, sleutels/klein metaal, alkaline, elektronica zonder accu, Li-klein (<5 Wh), Li-middel (5–50 Wh), Li-groot (>50 Wh)} **[A]**.
- Risicoscore per inworp `rᵢ = Σ_k P(k|x)·w_k`, w_k uit A1 (brandkans × schade per klasse).
- Container: `R = Σ rᵢ` sinds laatste lediging + `P_groot = 1 − Π(1 − P(Li-groot|xᵢ))`.
- Alarmniveaus: **groen** (R < θ₁), **oranje** (θ₁ ≤ R < θ₂ → "laatste lediging van de route / niet extra persen"), **rood** (R ≥ θ₂ of P_groot > 0,5 of temp-event → aparte actie). θ's te kalibreren in Ronde 3 zodat oranje ≤ 10 % en rood ≤ 1 % van ledigingen **[A]** (werkbaarheidsgrens chauffeur).

## 2. Samenstelling restafvalzak NL

### 2.1 Bronnen

| Grootheid | Waarde | Bron (datum) |
|-----------|--------|--------------|
| Huishoudelijk restafval | 178 kg/inw/jr (2023) | CBS, jul 2024 – cbs.nl/nl-nl/nieuws/2024/30 |
| Ferro in restafval | 2,0 % gewicht | RWS, Samenstelling huish. restafval, sorteeranalyses 2022 (3-jr gem.) |
| Non-ferro | 1,6 % gewicht | idem |
| Metalen verpakkingen (gemeente Heerde) | 1,0 % gewicht | Eureco sorteeranalyse Heerde 2023 |
| Losse batterijen in restafval | **28 st/ton**; 0,055 % gewicht (~550 g/t); 97 % (gewicht) alkaline | Eureco i.o.v. St. OPEN, "Batterijen in huish. restafval 2025", apr 2026 (351 analyses, 222 t, 5 933 batterijen) |
| Idem 2024 | 20 st/ton (~50 mln/jr) | St. OPEN/Eureco 2024 |
| Landelijk | 1 460 t losse batterijen (74 mln st) + ingebouwd → 1 980 t, ~100 mln st/jr | idem 2025 |
| Ingebouwd in apparaten | ~26 mln st/jr → ~7 st/ton **[A: afgeleid]** | idem |
| Vapes | ~20 per vuilniswagenlading (~8–10 t **[A]**) → ~2/ton | Taskforce Batterijbranden, via Hart van Nederland 2025 |
| Branden inzameling | "elke week ergens een brand" (HvN 2025) vs "≥ 3×/maand" (NOS) / "tientallen per jaar" (NVRD) | tegenstrijdig – A1 |
| BE-referentie | 1 batterij per 100 kg huish. afval | Bebat 2024 |

Niet gevonden: aantal blikjes/folie-items per zak (alleen gewicht%), aandeel Li-ion onder losse batterijen naar aantal (wel: 97 % gewicht alkaline), samenstelling per zak (alle analyses rapporteren per ton). RWS-PDF 2024 (3-jr gem. 2023, publ. 2025-09) niet inleesbaar (proxy-blokkade) – getallen 2022 gebruikt.

### 2.2 Afgeleide verdelingen per zak (input Monte Carlo) **[A]**

Zak: 30–60 L, massa lognormaal mediaan 5 kg (laag 3 / hoog 9 kg) **[A]**.

| Item | Gem. per zak (basis) | Verdeling | Laag–hoog | Afleiding |
|------|--------------------|-----------|-----------|-----------|
| Stalen/alu blikjes (drank, conserven) | 2,5 | Neg.-binomiaal (r=1,5) | 1–5 | ~200 g metaal/zak, ~40 % verpakking **[A]**, 15–40 g/blik |
| Alu-folie / blisters / chipszakken (gemetalliseerd) | 3 | NB (r=1) | 1–6 | **[A]** |
| Sleutels / bestek / klein metaal | 0,15 | Poisson | 0,05–0,3 | **[A]** |
| Alkaline/Zn-C (AA/AAA) | 0,14 | Poisson, clusters (NB r=0,3) | 0,10–0,2 | 28/t × 5 kg; batterijen komen vaak in groepjes |
| Knoopcel (Li/alk) | 0,01 | Poisson | 0,005–0,02 | **[A]** |
| Elektronica zonder accu (kabels, kleine apparaten) | 0,1 | Poisson | 0,05–0,2 | **[A]** |
| Li-ion klein (vape, oordopjes, <5 Wh) | 0,015 | Poisson | 0,008–0,03 | ~2–5/t |
| Li-ion middel (telefoon, powerbank 5–50 Wh) | 0,004 | Poisson | 0,002–0,01 | **[A]** |
| Li-ion groot (>50 Wh: gereedschap, e-step) | 0,0005 | Poisson | 0,0002–0,002 | **[A]** |

### 2.3 Gevolg op containerniveau

| Scenario Li-items/ton | P(zak bevat Li) | E[Li]/lediging (80–120 zakken) | P(≥ 1 Li in lediging) |
|---|---|---|---|
| laag 2 | 1,2 % | 1,0–1,4 | 62–76 % |
| basis 5 | 3,0 % | 2,4–3,6 | 91–97 % |
| hoog 10 | 6,0 % | 4,8–7,2 | 99–100 % |

PPV van per-zak-detectie bij p = 3 %: (recall 0,9; FPR 0,30) → 8,5 % · (0,8; 0,10) → 20 % · (0,7; 0,03) → 42 % · (0,9; 0,01) → 74 %.

## 3. Signaalketen

### 3.1 Radio

| Optie | Payload | Energie per bericht | Kosten | Dekking ondergronds | Opmerking |
|-------|---------|--------------------|--------|---------------------|-----------|
| LoRaWAN EU868 | SF7–8: 222 B · SF9: 115 B · SF10–12: **51 B** (app-payload; +13 B overhead) | SF7 ~0,02 mWh, SF12 ~0,5 mWh **[A]** (1,2 s airtime @ 25 mW TX, ~120 mA) | KPN LoRa / TTN (gratis, fair use 30 s airtime/dag, 10 downlinks/dag) / Helium; ~EUR 1–3/jr/device **[A]** | Inworpzuil boven maaiveld: goed; in kuip: matig | 1 % duty-cycle; ruim genoeg voor 1–50 berichten/dag |
| NB-IoT / LTE-M | ≥ 1 kB, MQTT/CoAP over UDP | PSM 2,7–23 µA rust; ~5–20 mWh per sessie **[A]** | ~EUR 6–15/jr SIM **[A]** (KPN-tarief niet gevonden) | Beter indoor/ondergronds (+20 dB MCL) | Geschikt voor ruwe data (OTA-model, labels) |
| Meeliften op bestaande toegangscontrole (Mic-o-Data/Bammens/Ecosmart zuilcomputer, GPRS/LTE) | variabel | 0 extra radio | integratie-afspraak | n.v.t. | Zuil heeft al accu + pasregistratie + modem → laagste BOM |

Payload-ontwerp (11 B, past in SF12): zie §6 codeskelet.

### 3.2 Backend en integratie

| Systeem | Rol | Koppeling | Bron |
|---------|-----|-----------|------|
| HVC "ContainerDevice API" | vulgraadsensoren → backoffice | REST GET/POST, OAuth2 | TenderNed 298214/412908 (HVC vulgraadsensoren) |
| Almere aanbesteding | vulgraad naar routesoftware "conform STOSAG" | | TenderNed 419573 |
| STOSAG | pas/container/lezer/backoffice, ISO 14443-A passen | 4 koppelvlakken | Forum Standaardisatie; 2018: v1.0 verouderd, van lijst verwijderd |
| AMCS (o.a. Mic-o-Data-portaal, AMCS Vision AI), Bammens BWaste, Ecosmart, PWS/ProWaste | backoffice, route, boordcomputer | leverancier-API's (niet publiek gevonden) | – |
| Routeplanning (dynamisch op vulgraad) | voordeel bij ≥ 200 containers zelfde fractie | | Raadsbrief Heerhugowaard 2018 |
| Amsterdam | grootschalige uitrol vulgraadsensoren vanaf 2028 | | ZHAW/nieuws 2025 |

**Conclusie:** bouw de alarmen als **extra veld/event op de vulgraad-API** (`batteryRisk`: 0–3, `score`, `since_last_empty`) zodat bestaande routesoftware en boordcomputers het tonen zonder nieuw systeem. Daarnaast eigen lichtgewicht dashboard + webhook/e-mail. Open formaat voorstel: JSON (SensorThings/FIWARE-achtig) – geen bestaande standaard voor brandrisico gevonden.

## 4. Wat doet de ophaaldienst bij een melding?

Geen gepubliceerd NL-protocol gevonden; praktijk (lading op straat dumpen bij brand) wel gemeld (Nunspeet 2025). Voorgestelde actiematrix **[A]**:

| Niveau | Trigger | Actie chauffeur | Kosten/vertraging **[A]** |
|--------|---------|-----------------|---------------------------|
| Groen | R < θ₁ | normaal | 0 |
| Oranje | θ₁ ≤ R < θ₂ | container **als laatste van de route** legen, of persen uitstellen tot net voor overslag; extra blik op laadbak (thermische camera als aanwezig) | ~0–5 min, geen extra km |
| Rood | R ≥ θ₂, P_groot > 0,5 | **aparte lediging zonder persen** (kleine wagen / open container), of visuele check bovenzijde (deksel/trommel), zakken met harde objecten handmatig apart | 20–60 min, EUR 50–150 per actie **[A]** |
| Zwart | temp/gas-event in container (A4) | brandweer/ beheerder; container niet legen, afkoelen/afdekken; quarantaine | incident |
| Achteraf | elk rood alarm | terugkoppeling: was er iets? (label → model verbetert) | 2 min |

Notificatie chauffeur: via **boordcomputer / route-app** (AMCS, Bammens, PWS) als vlag op het containerpictogram; fallback SMS/Push. Moment: bij route-uitgifte 's ochtends + geo-fence 200 m voor container **[A]**. Eis: max ~1 rood per route per week, anders alarmmoeheid **[A]**.

## 5. AVG bij koppeling aan pashouder

| Aspect | Beoordeling | Bron/onderbouwing |
|--------|-------------|-------------------|
| Persoonsgegeven? | Containeralarm zonder pas: **nee**. Inworp-event + pas-ID: **ja** (pas herleidbaar tot adres) | AVG art. 4 |
| Grondslag | art. 6(1)(e) publieke taak (Wet milieubeheer art. 10.21 inzamelplicht; gemeentelijke afvalstoffenverordening) | **[A]** juridische check nodig |
| Doelbinding | Pasregistratie is er voor toegang/diftar; hergebruik voor "batterij-detectie per huishouden" = nieuw doel → verenigbaarheidstoets art. 6(4) | |
| Proportionaliteit | AP (2017, Arnhem): registratie zonder diftar = onnodig; ook mét diftar alleen wat nodig is. Per-zak detectie heeft FP-ratio 30–90 % (§2.3) → huishouden ten onrechte aanspreken = onevenredig | AP / Binnenlands Bestuur 2017 |
| DPIA | Verplicht bij koppeling: systematische monitoring + nieuwe technologie + mogelijk handhaving (AP DPIA-lijst) | AP-lijst verplichte DPIA |
| Geautomatiseerde besluitvorming | Boete/handhaving op basis van sensor alleen = art. 22 risico → menselijke tussenkomst verplicht | |
| Bewaartermijn | Voorstel: inworp-ruwe data 30 dagen; container-aggregaten onbeperkt; pas-koppeling alleen tijdelijk (≤ 7 d) gepseudonimiseerd, alleen voor *positieve* feedback **[A]** | |
| Advies | **Privacy by design: geen pas-koppeling in MVP**; optioneel "opt-in feedback" (huishouden kiest zelf meldingen) | |

## 6. Plan Ronde 3 (Monte Carlo + code)

**Simulatie (`experiments/A6_mc/`)**
1. `bag_model.py` – trek zakinhoud uit §2.2 (NB/Poisson), 1e6 zakken; drie scenario's laag/basis/hoog.
2. `sensor_models.py` – per concept (A2 inductie PI/multi-freq, A3 röntgen, A4 temp/gas) per itemklasse een kansverdeling van de feature (bv. lognormaal signaal μ_k, σ_k, plus maskering door andere items: optelling van signalen in de zak). Parameters aangeleverd door A2/A3/A4; placeholder-waarden vooraf gemarkeerd **[A]**.
3. `classifier.py` – drempel, logistic, kNN; per-zak risicoscore.
4. `container.py` – stroom van 80–120 zakken per lediging, Bayes-accumulatie, alarmniveaus.
5. `outcome.py` – koppeling aan A1: P(brand | Li-klasse in pers) → vermeden branden = Σ P(brand) × P(alarm ∧ juiste actie) × effectiviteit actie (oranje 30 %, rood 80 % **[A]**).
6. Output: ROC per concept (per zak én per lediging), recall / vals-alarmratio / alarmen per route per week vs θ, vermeden branden en EUR (→ A7), gevoeligheid voor prior (laag/basis/hoog).

**Code**
- `firmware/encode.py` (MicroPython-compatibel) – 11-byte payload: `ver(1) | flags(1) | seq(2) | n_inworp(2) | risk_score_u16(2) | max_item_class(1) | temp_c_i8(1) | batt_mV/20(1)`; ook MQTT-JSON variant.
- `decoder.js` – TTN/KPN payload-formatter.
- `dashboard.html` – statische mock: kaart/lijst containers, kleur per niveau, trend, actie-knop "geleegd/bevinding".

## Bronnen
- Eureco/St. OPEN, Batterijen in huishoudelijk restafval 2025 (apr 2026): https://www.stichting-open.org/onderzoek/batterijen-in-huishoudelijk-restafval/
- St. OPEN factsheet batterijen 2023 (jun 2024): https://stichting-open.org/wp-content/uploads/2024/06/st-open_factsheet-resultaten-batterijen-2023_en.pdf
- RWS, Samenstelling huish. restafval 2022: https://www.afvalcirculair.nl/publish/library/316/samenstelling-van-het-huishoudelijk-restafval-2022.pdf ; editie 2024 (sep 2025): https://open.rijkswaterstaat.nl/@295865/samenstelling-huishoudelijk-restafval
- CBS, Toename huishoudelijk afval 2023 (jul 2024): https://www.cbs.nl/nl-nl/nieuws/2024/30/toename-huishoudelijk-afval-in-2023
- Taskforce Batterijbranden jaaroverzicht 2024 (apr 2025): https://verenigingafvalbedrijven.nl/userfiles/files/Taskforce%20Batterijbranden%20-%20Jaaroverzicht%202024.pdf
- Hart van Nederland, brandgevaar vapes (2025): https://www.hartvannederland.nl/112/brand/artikelen/afvalbedrijven-waarschuwen-brandgevaar-vapes-batterijen
- TTN fair use / payload: https://www.thethingsnetwork.org/forum/t/fair-use-policy-explained/1300 ; EU868: https://www.thethingsnetwork.org/docs/lorawan/regional-parameters/eu868/
- NB-IoT standby 6,7–23 µA (IoT, jan 2026): https://doaj.org/article/2d9cbfc4721042ffa55aea879fe9a05b
- HVC/Almere aanbestedingen vulgraadsensoren: https://www.tenderned.nl/papi/tenderned-rs-tns/v2/publicaties/419573/documenten/14038782/content
- STOSAG evaluatie (mrt 2018): https://forumstandaardisatie.nl/sites/default/files/FS/2018/0314/FS-20180314.03A-Evaluatie-STOSAG-1.0.pdf
- Heerhugowaard slimme containers (2018): https://archief-gemeentebestuur.heerhugowaard.nl/Documenten/Ingekomen-stukken/CBB180063-Raadsinformatiebrief-terugkoppeling-motie-Slimme-ondergrondse-containers-1.pdf
- Arnhem afvalpas / AP (2017): https://www.binnenlandsbestuur.nl/bestuur-en-organisatie/arnhem-stelt-ondergrondse-containers-voorlopig-open ; Groningen: https://gemeenteraad.groningen.nl/Documenten/Document/Verwerking-persoonsgegevens-via-afvalpassen.pdf
- Bebat (BE, 2024): https://cms.bebat.be/sites/default/files/2024-03/Advertentie%20-%20A4%20Portrait%20-%20Restafval.pdf
