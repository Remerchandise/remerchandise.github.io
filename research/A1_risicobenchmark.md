# A1 – Risicobenchmark (Ronde 0)

Auteur: Agent 1 (Risicobenchmark). Datum: 2026-10-25. Prijspeil EUR 2026 excl. btw. Aannames: **[A]**.
Bronnen geraadpleegd via websearch op 2026-10-25. Primaire pdf's (Stichting OPEN 2025, Taskforce Batterijbranden 2023/2024, EPA 2021) waren **niet te downloaden** (proxy 403). Cijfers komen uit samenvattingen en persberichten; dat staat per bron vermeld.

---

## 1. Ontstekingsmechanismen (thermal runaway, TR)

| Mechanisme | Wat gebeurt er | Waar in de keten (zie kickoff §1) | Relevantie |
|---|---|---|---|
| Crush (pletten) | Separator scheurt → interne kortsluiting → lokale verhitting → afbraak van SEI/elektrolyt → TR (>150–200 °C, oppervlak tot ~700 °C) | Stap 5 persplaat, stap 7 shredder | **Hoofdmechanisme** |
| Penetratie (nagel, scherp metaal/glas) | Directe interne kortsluiting met kleine weerstand en de hoogste lokale stroomdichtheid | Stap 5–7 | Hoog |
| Externe kortsluiting | Polen worden overbrugd door folie, sleutels of andere cellen → Joule-verwarming. Alkaline 9V-blok en losse Li-cellen zijn hier gevoelig voor | Stap 1–3 (zak, container) | Laag–middel. Kan smeulen veroorzaken |
| Valschade / schok | Deuk of interne verschuiving zonder directe TR. **Latente** kortsluiting die uren tot dagen later kan doorslaan | Stap 2–4 | Laag per gebeurtenis, maar het verklaart containerbranden |
| Warmte van buiten (zon op deksel, buurbrand) | Versnelt zelfontlading en SEI-afbraak. Een TR-trigger pas boven ~80–120 °C | Stap 3 | Zeer laag |

Kernpunten:
- De toestand van de cel bepaalt de uitkomst. **SOC ≥ 50 %** is in twee onafhankelijke studies de praktische ondergrens voor het ontsteken van droog afval: Gausden & Cerik, *Batteries* 10(7):236, 2024-07 (vape-cellen bij ≤ 50 % SOC: piek ~131 °C, geen ontsteking van afval) en een stortplaatsstudie met 18650-cellen (*Process Safety Env. Prot.*, 2025: een enkele cel heeft ≥ 50 % SOC nodig om smeulbrand te starten in droog afval; de drempel stijgt bij vocht).
- Restlading in afgedankte cellen (Nigl e.a., *Waste Management* 2021, Oostenrijk, n = 980): **~24 % heeft ≥ 25 % SOC en ~12 % heeft ≥ 50 % SOC**. Ruwweg 1 op 4 tot 1 op 8 cellen kan een brand starten als hij kritisch beschadigd raakt.
- Lithium-metaal (CR2032, FR6) maakt bij beschadiging reactief Li vrij. Door de kleine energie-inhoud (CR2032 ≈ 0,7 Wh) is het afvalbrandrisico laag. Het belangrijkste risico van knoopcellen is inslikken, en dat is buiten scope.
- Alkaline en NiMH hebben **geen thermal runaway** (waterig elektrolyt). Alleen kortsluitwarmte, vooral bij een 9V-blok.

## 2. Energie per celtype

Aanname: E = U_nom × C. Laag/basis/hoog.

| Type | Chemie | U_nom (V) | C (Ah) | **E laag / basis / hoog (Wh)** | Opmerking |
|---|---|---|---|---|---|
| Knoopcel CR2032 | Li-metaal (primair) | 3,0 | 0,22–0,24 | 0,6 / **0,7** / 0,7 | Geen TR-brandstof van betekenis |
| LR03 (AAA) alkaline | Zn-MnO2 | 1,5 (gem. ~1,2) | 1,0–1,2 | 1,2 / **1,5** / 1,8 | Geen TR |
| LR6 (AA) alkaline | Zn-MnO2 | 1,5 (gem. ~1,2) | 2,0–2,8 | 2,5 / **3,0** / 3,9 | Geen TR |
| FR6 (AA) lithium | Li-FeS2 | 1,5 | 3,0–3,5 | 4,0 / **4,5** / 5,0 | Li-metaal |
| NiMH AA | NiMH | 1,2 | 1,9–2,5 | 2,3 / **2,4** / 3,0 | Geen TR |
| Wegwerpvape (13300/13400 of pouch) | Li-ion | 3,7 | 0,28–0,65 (rechargeable "big puff" tot 1,0) | 1,0 / **2,0** / 3,7 | Vaak hoge restlading **[A]** |
| Oortjes / smartwatch | Li-ion pouch | 3,7–3,85 | 0,04–0,4 | 0,15 / **0,5** / 1,5 | |
| 18650 | Li-ion | 3,6 | 2,5–3,5 | 9 / **11** / 12,6 | |
| 21700 | Li-ion | 3,6 | 4,0–5,0 | 14 / **17** / 18 | |
| Telefoon (pouch) | Li-ion/LiPo | 3,85 | 3,0–5,0 | 11,5 / **15** / 19 | |
| Powerbank 5–20 Ah | Li-ion | 3,7 | 5–20 | 18 / **37** / 74 | |
| Laptop-pack | Li-ion | 11,1–15,4 | 3–6 | 40 / **55** / 100 | |
| Gereedschapsaccu 18 V | Li-ion | 18 | 2–5 | 36 / **72** / 90 | |
| E-bike-pack | Li-ion | 36 | 10–20 | 360 / **500** / 720 | Komt zelden in een zak, maar dominant in energie |
| E-step | Li-ion | 36–48 | 7–15 | 250 / **400** / 700 | |

Referentiepunten: luchtvaart (IATA) staat tot 100 Wh in de cabine toe zonder toestemming en 100–160 Wh met toestemming. Een 18650 bij 50 % SOC ≈ **5 Wh** vrij te maken energie is de laagst bekende "ontsteek-energie" voor droog afval (zie §1).

## 3. Li-ion vs. alkaline vs. lithium-metaal (knoopcel)

| Eigenschap | Li-ion | Li-metaal primair (CR2032, FR6) | Alkaline / NiMH |
|---|---|---|---|
| Thermal runaway | Ja (exotherm, zelfonderhoudend, brandbaar gas) | Beperkt. Li reageert met vocht | Nee |
| Energie per stuk | 0,5–700 Wh | 0,7–5 Wh | 1,5–4 Wh |
| Detectie-uiterlijk (voor A2/A3) | Opgerolde Cu/Al-folie (Al = kathodedrager, Cu = anodedrager), stalen of Al-huls, of pouch in een apparaat | Stalen schijf of huls | Stalen huls, Zn-poeder, MnO2. Geen foliewikkeling |
| Weging w_chem (voorstel) | **1,0** (LFP: 0,3) | **0,5** | **0,01** (9V-blok 0,1) |

Conclusie voor het product: **"batterij" ≠ "risico"**. Van de losse batterijen in het restafval is het grootste deel alkaline, en dat telt in de score bijna niet mee. Een detector die alkaline niet van Li-ion kan onderscheiden, moet op het aantal metalen objecten of op massa sturen en zal veel loos alarm geven (zie §7).

## 4. Branddata inzamelaars en verwerkers

### Nederland
| Bron (datum) | Cijfer | Kwaliteit |
|---|---|---|
| NVRD-inventarisatie via NOS ("Jaarlijks tientallen branden in vuilniswagens…", nos.nl/l/2485439, datum niet te verifiëren; ~2023 **[A]**) | "Tientallen" branden in vuilniswagens per jaar, **≥ 3 per maand** (≥ 36/jaar) | Inventarisatie, geen register |
| Vereniging Afvalbedrijven via brandveilig.com (art. 73102, datum onduidelijk) | ~**10 branden/maand ≈ 120/jaar**, inzamelplaatsen + afvalwagens samen (alle oorzaken die zij registreren) | Brancheregistratie |
| Hart van Nederland, 2025-09-08 | "Gemiddeld **wekelijks**" een brand bij afvalinzameling (~52/jaar). Taskforce Batterijbranden vond in 2024 gemiddeld **20 vapes per vuilniswagen** restafval | Persbericht |
| Tweede Kamer-stuk 2026D41104 (2026) | Sector: ~**38 %** van de branden bij afvalverwerkers komt door batterijen/accu's | Sectorclaim, geen jaartal |
| Brandweer Nederland (via brandveilig.com) | **Geen harde cijfers** over branden in vuilniswagens | — |
| Stichting Salvage / Verbond van Verzekeraars (2025) | Accu als oorzaak van woningbranden: 3 % (2023) → 5 % (2024) | Indirect (woning, niet afval) |
| Stichting OPEN/Eureco, "Batterijen in huishoudelijk restafval 2025" (v2, 2026-04-28) | 351 analyses, 222,3 t restafval: **5.933 losse batterijen (114 kg) = gem. 28/t, mediaan 23/t**. Batterijen ín apparaten zijn niet meegeteld | Sorteeranalyse, sterk |
| Stichting OPEN/Eureco, "E-waste in huish. restafval 2025" | ≥ 38 % van de apparaten in het restafval werkt op een losse batterij. 2024: ~26.000 t e-waste in de vuilniszak | Sorteeranalyse |
| Stibat/OPEN factsheet 2023 | Op de markt 10.851 t, ingezameld 5.200 t (46,1 %) | Register |

**Niet gevonden**: het aandeel Li-ion in de OPEN-sorteeranalyse (hoofdstuk 1.4 van de pdf, niet toegankelijk), een officieel jaarcijfer van branden in ondergrondse containers, en schadebedragen per vuilniswagenbrand in NL. Rijkswaterstaat heeft geen restafval-per-ton-cijfer voor Li gepubliceerd (wel Mobius 2020 voor IenW: 211–6.051 t Li-ion in lekstromen).

### Buitenland
| Bron (datum) | Cijfer |
|---|---|
| US EPA, *An Analysis of Lithium-ion Battery Fires in Waste Management and Recycling*, EPA 530-R-21-002 (2021-07) | 245 (waarschijnlijk door) LIB veroorzaakte branden bij 64 installaties, 2013–2020, 28 staten. Op basis van nieuwsberichten, dus een sterke onderschatting |
| Eunomia/ESA, *Cutting Lithium-ion Battery Fires in the Waste Industry* (2021-01) | UK: ~**201** LIB-afvalbranden per jaar, **~48 %** van de afvalbranden, ~**£158 mln/jaar**. Gemiddeld £173k per incident, ernstig ~£1,2 mln |
| ESA-leden 2019–2020 (via Waste360) | 670 branden, waarvan **38 %** door (vermoedelijk) LIB |
| Material Focus + NFCC (2024-05-10) | UK: **> 1.200** batterijbranden in vuilniswagens en op afvalterreinen (2023), +71 % t.o.v. ~700 (2022) |
| UK Battery Fire Tracker (circularonline, 2025/2026) | +88 % 2023→2025 (publiek gemelde incidenten). **Vapes 23 %** van de incidenten (grootste identificeerbare oorzaak). **52 % ontstaat in vuilniswagens** |
| Material Focus (2023-09 / begin 2025) | UK: 5 mln wegwerpvapes per week weggegooid (2023), 8,2 mln/week (begin 2025), na het verbod nog 6,3 mln/week. 0,15 g Li per vape |
| Resource Recycling Inc. / Fire Rover (2025-03, 2025-08) | VS/Canada: 373 (2023) → 430 (2024) → 448 (2025) gemelde brandincidenten bij installaties. Oorzaak vooral vapes en kleine elektronica (geen register) |
| ESA (2025) | UK-kosten > £1 mrd/jaar (bredere definitie dan Eunomia 2021) |

### Aandeel vapes
- UK: 23 % van de publiek gemelde afvalbranden (Battery Fire Tracker, 2025).
- NL: 20 vapes per vuilniswagenlading (Taskforce, 2024). Bij een lading van ~8 t **[A]** is dat ~2,5 vapes/t.
- Gausden & Cerik 2024: bij ≤ 50 % SOC ontsteekt een vape-cel geen afval. Het risico komt van vapes met een volle cel (weggegooid omdat de vloeistof op is) **[A]**.

## 5. Concentratie Li-cellen in restafval

| Bron | Alle batterijen (stuks/t) | Li (stuks/t) |
|---|---|---|
| Stichting OPEN/Eureco 2025 (NL, los) | **28 (mediaan 23)** | n.b. (pdf niet leesbaar) |
| Nigl & Pomberger, BAT-SAFE (AT, 2019) | ~20 (0,05 massa-%) | **~2** (0,002 massa-%) |
| Saubermacher (AT, 2023) | ~20 | ≥ 1 |
| Taskforce NL (2024), alleen vapes | — | ~2,5 vapes/t **[A]** (20 per wagen, 8 t) |

**Voorstel Li-items per ton restafval (los + in apparaat + vapes): laag 3 / basis 6 / hoog 12 [A].**
Bij ~2,9 Mt huishoudelijk restafval per jaar **[A]** (~160 kg/inw.) zijn dat ~17 mln Li-items per jaar in het NL-restafval (bandbreedte 9–35 mln).
Een ondergrondse container van 5 m³ bij ~120 kg/m³ **[A]** bevat ≈ 0,6 t per lediging, dus **gemiddeld ~3,6 Li-items** (1,8–7,2).

## 6. Kans op ontsteking bij compactie

Er bestaat **geen gepubliceerde studie die "p(ontsteking | compactie in vuilniswagen)" per cel direct meet**. Twee benaderingen:

**a) Bottom-up (lab)**: p_i = P(SOC ≥ 50 %) × P(kritische schade | pers) × P(afval ontsteekt | TR)

| Factor | Laag | Basis | Hoog | Bron |
|---|---|---|---|---|
| P(SOC ≥ 50 %) | 0,12 | 0,12 | 0,24 (≥ 25 %) | Nigl 2021 |
| P(kritische schade \| pers) | 0,05 | 0,2 | 0,5 | **[A]** (in apparaat lager dan een losse cel) |
| P(ontsteking omgeving \| TR) | 0,3 | 0,6 | 0,9 | **[A]**, Gausden 2024, PSEP 2025 |
| **p_i bottom-up** | **1,8e-3** | **1,4e-2** | **1,1e-1** | |

**b) Top-down (gekalibreerd op NL-brandcijfers)**: p_i = registreerde branden × onderregistratiefactor / aantal Li-items

| | Laag | Basis | Hoog |
|---|---|---|---|
| Branden in wagens per jaar (NL) | 36 (NVRD) | 52 (HvN) | 120 (VA, incl. inzamelplaatsen) |
| Onderregistratie (gedoofd of gestort zonder melding) | ×1 | ×3 | ×10 |
| Li-items per jaar | 35 mln | 17 mln | 9 mln |
| **p_i per item per ketenpassage** | **1e-6** | **9e-6** | **1,4e-4** |

**Belangrijkste bevinding**: de lab-kans ligt **2–4 ordes van grootte hoger** dan wat de praktijk laat zien. Verklaringen **[A]**: de meeste persingen beschadigen de cel niet kritisch, de omringende natte massa dooft, kleine branden worden gestort en niet gemeld, en het aantal Li-items wordt mogelijk overschat. Voor productbeslissingen gebruik ik **(b)**, met (a) als bovengrens voor de stresstest.

Gevolg: **P_brand per containerlediging (basis) ≈ 3e-5**. Een gemeente met 1.000 containers die wekelijks worden geleegd (52.000 ledigingen per jaar) heeft dus **~1,7 brandincidenten per jaar** die aan haar containers toe te schrijven zijn (bandbreedte 0,3–15). Dit is de knock-out-input voor A7.

## 7. Risicoscore

### 7.1 Definitie
Per inworp *j* en per container *c* (cumulatief sinds de laatste lediging):

R = Σ_i ( E_i × w_chem,i × w_toestand,i )   [eenheid: **Wh-eq**]

| Parameter | Waarden (basis; bandbreedte) |
|---|---|
| E_i | Tabel §2. Bij een onbekend type: de klasse-schatting uit de sensor (A2/A3), anders de default **6 Wh-eq** (gemiddeld Li-item, zie hieronder) |
| w_chem | Li-ion NMC/LCO/pouch 1,0; LFP 0,3 (0,2–0,5); Li-metaal 0,5 (0,3–1); NiMH 0,05; alkaline/ZnC 0,01; 9V-blok 0,1 |
| w_toestand | Ingebouwd in apparaat 0,5 (0,3–0,8); losse cel 1,0; vape 1,0 (1–2, vanwege hoge SOC en dunne huls); opgezwollen, warm of beschadigd (A4-signaal) 3,0 |
| SOC | Niet meetbaar → zit impliciet in de kalibratie (verwachtingswaarde) |

Gemiddeld Li-item (mix **[A]**: 40 % vape, 20 % klein apparaat, 15 % CR2032/Li-primair, 8 % losse 18650/21700, 8 % telefoon, 5 % powerbank, 3,5 % laptop/gereedschap, 0,5 % e-bike/step): **E_eff ≈ 6,1 Wh-eq**.
**Pareto**: items ≥ 20 Wh-eq (powerbank, laptop, e-bike) zijn ~9 % van de items maar dragen **~59 % van de risico-energie**. Vapes zijn 40 % van de items maar 13 % van de Wh-eq. Dat botst met de 23 % van de UK-incidenten, en daarom wordt w_toestand voor vapes in Ronde 3 gevarieerd.

### 7.2 Drempels (voorstel)

Basislijn: een gemiddelde containerlediging bevat al ~3,6 × 6,1 ≈ **22 Wh-eq**. Een drempel onder ~50 Wh-eq per container maakt de meeste containers oranje, met alarmmoeheid als gevolg.

| Niveau | **Per inworp** | **Per container (sinds lediging)** | Onderbouwing | Actie (voorstel aan A6) |
|---|---|---|---|---|
| Groen | R < 10 Wh-eq | R < 50 Wh-eq | Onder de ontsteekgrens van een enkele cel (~5 Wh vrij bij 50 % SOC). Vapes, knoopcellen, alkaline en oortjes vallen hieronder | Niets. Alleen statistiek |
| Oranje | 10 ≤ R < 50 | 50 ≤ R < 150 | Telefoon, losse 18650's, kleine powerbank. Container ≈ 2–7× de basislijn | Op het dashboard. Container als laatste in de route legen, met korte of geen persslag **[A]** |
| Rood | R ≥ 50, **of** een enkel item ≥ 50 Wh-eq | R ≥ 150, **of** een A4-signaal (warmte/gas) | Laptop-, gereedschaps- en e-bike-klasse (IATA-referentie 100 Wh). P_brand per passage ≈ 1e-4 (basis), 3–5× een gemiddelde container | Push-melding. Apart legen (niet persen) of het item verwijderen. Bij warmte: brandweerprotocol |

### 7.3 Brandkansmodel per container
P_brand,c = 1 − Π_i (1 − p_i) ≈ 1 − exp(−k · R_c) met p_i = 1 − exp(−k · E_i · w_chem · w_toestand)

| k (per Wh-eq per ketenpassage) | Laag | Basis | Hoog (top-down) | Stress (bottom-up) |
|---|---|---|---|---|
| k | 1,7e-7 | 1,5e-6 | 2,3e-5 | ~2e-3 |

| R_c (Wh-eq) | 5 | 22 (gemiddeld) | 50 | 150 | 500 (e-bike) |
|---|---|---|---|---|---|
| P_brand basis | 7e-6 | 3e-5 | 7e-5 | 2e-4 | 7e-4 |
| P_brand hoog | 1e-4 | 5e-4 | 1e-3 | 3e-3 | 1e-2 |

Gevolg voor de waardepropositie: zelfs een rode container brandt in de basis met minder dan 1 op 1.000 kans. Het product verkoopt **risicoreductie op populatieniveau** (welk deel van de verwachte brand-energie wordt afgevangen), niet het voorspellen van één brand.

## 8. Parameters voor de Ronde 3-simulatie (gevoeligheidsanalyse)

| # | Parameter | Range | Waarom |
|---|---|---|---|
| 1 | Li-items per ton | 3 / 6 / 12 | Grootste onzekerheid in de kalibratie |
| 2 | Itemmix (aandeel vape, powerbank, laptop, e-bike) | ±50 % per klasse | Pareto-gevoeligheid |
| 3 | Onderregistratiefactor | 1 / 3 / 10 | Bepaalt k |
| 4 | w_toestand vape | 1 / 1,5 / 2 | Reconciliatie met 23 % UK-vape-incidenten |
| 5 | w_toestand in-apparaat | 0,3 / 0,5 / 0,8 | |
| 6 | Drempel per inworp | 5–100 Wh-eq | ROC-curve |
| 7 | Drempel per container | 20–300 Wh-eq | Alarmen per 1.000 ledigingen versus afgevangen risico |
| 8 | Sensorfout (input A2/A3/A4): P(Li \| detectie), Wh-schattingsfout (log-normaal σ = 0,3–1,0), alkaline-vals-positief | Van andere agents | Energiegewogen recall |
| 9 | Ledigingsinterval | 3–14 dagen | Accumulatie per container |
| 10 | Containervolume en dichtheid | 3–5 m³, 100–150 kg/m³ | Items per lediging |

**Outputmetrics**: (1) energiegewogen recall = afgevangen Σ Wh-eq / totaal Σ Wh-eq; (2) oranje- en roodmeldingen per 1.000 ledigingen; (3) vermeden branden per 1.000 containers per jaar (input voor A7); (4) Pareto-curve recall versus alarmlast als functie van de drempel.

## 9. Bronnen (met datum)
- Nigl T. e.a., "The fire risk of portable batteries in their end-of-life: SOC of waste LIBs in Austria", *Waste Management*, 2021 (PubMed 33843368).
- Nigl T. e.a., "Lithium-Ion Batteries as Ignition Sources in Waste Treatment Processes – semi-quantitative risk analysis", *Processes* 9(1):49, 2021-01.
- Nigl & Pomberger, BAT-SAFE handout Steiermark, 2019; Nigl e.a., *Waste Manag. Res.*, 2020-05.
- Gausden & Cerik, "Single-Use Vape Batteries: Investigating Their Potential as Ignition Sources…", *Batteries* 10(7):236, 2024-07.
- "Underground fires induced by disposed Li-ion battery in peatland and landfill", *Process Safety and Environmental Protection*, 2025.
- US EPA, EPA 530-R-21-002, 2021-07.
- Eunomia/ESA, *Cutting Lithium-ion Battery Fires in the Waste Industry*, 2021-01 (NFCC-bericht 2021-01-13).
- Material Focus & NFCC, persbericht 2024-05-10; Material Focus vape-cijfers 2023-09 en 2025.
- UK Battery Fire Tracker via circularonline.co.uk, 2025/2026.
- Resource Recycling, 2025-03-18 en 2025-08-13 (Fire Rover-rapport).
- NOS, nos.nl/l/2485439 (NVRD-inventarisatie, datum niet geverifieerd).
- brandveilig.com art. 73102 (Vereniging Afvalbedrijven).
- Hart van Nederland, 2025-09-08.
- Tweede Kamer, document 2026D41104 (2026).
- Stichting OPEN/Eureco, *Batterijen in huishoudelijk restafval 2025*, v2 2026-04-28; *E-waste in huish. restafval 2025*; factsheet batterijen 2023 (2024-06).
- Stichting Salvage / Verbond van Verzekeraars, brandclaims 2024 (pers 2025).
