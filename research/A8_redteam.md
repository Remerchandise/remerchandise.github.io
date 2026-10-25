# A8 – Red team: faalwijzen, bewijs en concurrentie (Ronde 0)

Prijspeil EUR 2026 excl. btw. **[A]** = aanname. Bronnen met datum (jaar/maand). Toegang tot PDF's (rijksoverheid, stichting-open, verenigingafvalbedrijven) was vanuit de sandbox geblokkeerd (DNS/proxy 403); cijfers komen uit zoekmachine-samenvattingen van die PDF's en moeten door de Orchestrator/A1 aan de bron worden geverifieerd → gemarkeerd **[V]**.

## 1. Basisgetallen: hoe zeldzaam is "de accu" in de zak?

| Grootheid | Waarde | Bron |
|---|---|---|
| Huishoudelijk restafval NL | 177 kg/inw/jr (2023) → ≈ 3,2 Mt/jr | CBS, 2024-10 |
| Losse batterijen in restafval | gem. **28 /t** (mediaan 23 /t), 5.933 st in 222,3 t, 351 analyses; 0,055 m% | St.OPEN/Eureco "Batterijen in huish. restafval 2025", 2026-04/06 **[V]** |
| Batterijen in apparaten | ≈ 26 mln/jr (≈ 8 /t) | idem; Taskforce Batterijbranden jaaroverzicht 2024 (2025-04) **[V]** |
| Totaal | ≈ 100 mln batterijen, ≈ 1.980 t/jr | idem **[V]** |
| Chemie losse batterijen | ≈ 97 m% alkaline; losse Li-ion ≈ **1 op 395** | Taskforce jaaroverzicht (2023/2024) **[V]** |
| Vapes in restafval | ≈ 140.000 /week ≈ 7,3 mln/jr ≈ **2,3 vapes/t**; illegaal 20–40 mln/jr op markt | Taskforce Batterijbranden jaaroverzicht 2024 (2025-04) |
| Vapes per vuilniswagen | "gem. 20 vapes per vuilniswagen" (secundair, De Stentor via Hart van NL) | 2025-09 (primaire meting niet gevonden) |
| Metalen in restafval | ferro ≈ 4,5 m%, non-ferro ≈ 1,6 m% (fragment, jaar onzeker) | RWS sorteeranalyses 2023, gepubl. 2025-01 **[V]** |

### Afgeleide red-team-rekensom (A1/A6 graag overnemen of corrigeren)

| | Laag | Basis | Hoog |
|---|---|---|---|
| Massa zak uit 60 L-trommel **[A]** | 3 kg | 5 kg | 8 kg |
| Li-houdende items per ton (vapes 2,3 + Li in apparaten/powerbanks/losse Li) **[A]** | 3 | 4,5 | 7 |
| P(zak bevat ≥ 1 Li-item) | 0,9 % | **2,2 %** | 5,4 % |
| Metaal per zak (6 m%) | 180 g | **300 g** | 480 g |
| P(zak bevat geleidend metaal: blik, deksel, kroonkurk, folie, sleutel) **[A]** | 70 % | **85 %** | 95 % |
| Container 5 m³ bij 150–250 kg/m³ | 0,75 t | 1,0 t | 1,25 t |
| Verwacht aantal Li-items per lediging | 2,3 | **4,5** | 8,8 |
| P(container bevat ≥ 1 Li-item bij lediging, Poisson) | 90 % | **99 %** | > 99,9 % |

**Kernbevinding 1 – "container X bevat waarschijnlijk een accu" is altijd waar.** Een binaire containermelding draagt nagenoeg nul informatie. Alleen een *rangorde* (aantal, Wh, grote packs zoals e-bike/gereedschapsaccu) of een *per-inworp* signaal is bruikbaar.

**Kernbevinding 2 – base-rate-val per inworp.** Met prevalentie 2,2 % en een metaaldetector die 85 % van de zakken "ziet": zelfs met een slimme classificator (sensitiviteit 90 %, specificiteit 95 %) is PPV = 0,02·0,9 / (0,02·0,9 + 0,98·0,05) ≈ **27 %**; bij specificiteit 80 % ≈ 9 %. Drie van de vier alarmen zijn vals in het *gunstige* geval.

## 2. Faalwijzen per sensorprincipe

| Faalwijze | Mechanisme | Ernst | Bewijs / status |
|---|---|---|---|
| Vals alarm metaaldetectie | Blikjes (Al/Fe, 15–40 g), conservenblik, kroonkurken, Al-folie (prop), aluminium vape-behuizing, sleutels, bestek, theelichtjes, koffiecups (Al) | **Hoog** | 6 m% metaal in restafval **[V]**; discriminatie klein-onschuldig vs. groot-gevaarlijk is het bekende kernprobleem van inductiedetectie (patentliteratuur US 5047718) |
| Gemiste pouch-cel | Vapes en dunne apparaten gebruiken LiPo-pouch (bijv. 210 mAh, 3,7 V, 0,78 Wh) in Al-laminaat: inductief ≈ folieprop; geen stalen can | **Hoog** – juist de grootste Li-bron (vapes) | Teardown recessim-wiki (z.d.), iFixit VOOM 280 mAh |
| Afscherming / maskering | Cel in metalen apparaat (laptop, gereedschap, Al-vape), naast blikjes in dezelfde zak → signaal niet te scheiden | Hoog | Fysica; geen veldcijfers gevonden |
| Alkaline als Li-ion | AA/AAA stalen can (97 m% van losse batterijen is alkaline) geeft vergelijkbaar inductief signaal als 18650 | **Hoog** – 394 van 395 losse batterijen zijn geen Li-ion **[V]** | Taskforce |
| Elektronica zonder accu | Kabels, opladers, PCB's, kleine apparaten: Cu-spoelen/trafo's | Middel | e-waste in restafval ≈ 1,3 kg/inw/jr (St.OPEN 2026) **[V]** |
| Nat/vervuild | Natte zak, lekvocht, vet: capacitief/dielectrisch en optisch onbruikbaar; condens op lenzen; ijzel op klep | Middel | Dublin bin-sensor trial 2023: hardware-fit, connectiviteit, batterijduur faalden |
| Overvolle trommel/container | Zak blijft in trommel hangen of trommel wordt geforceerd; container vol → bijplaatsing naast zuil → zak passeert sensor nooit | **Hoog** | Dordrecht: 60 % van bijgeplaatste voorwerpen past niet in trommel; Eindhoven: slechts 5 % van bijplaatsingen door storing |
| Ontwijking | Accu's, e-bike-packs, grote apparaten worden juist naast de container gezet of in grofvuil/pmd gegooid | Middel | Eindhoven/Dordrecht (bijplaatsingen bevatten ook elektrische apparaten) |
| Vandalisme/sabotage | Zuil is al hét storingspunt (pas, klep, trommel); extra elektronica = extra doelwit; jaarwisseling (vuurwerk in containers) | Hoog | Eindhoven ~1.000 meldingen/maand defecte containers (Omroep Brabant, ~2019); Amsterdam 400.000 klachten openbare ruimte 2021 vs 250.000 in 2019; Scheveningen: > 2/3 van kleine brandjes = containerbrand (NOS, jaarwisseling) |
| Energie & connectiviteit | Batterij in zuil leeg, LTE-M/NB-IoT slecht onder metalen deksel | Middel | Dublin 2023 (batterijduur, connectiviteit) |
| Röntgen | Stralingsvergunning (Kernenergiewet), publieke ruimte, kind in trommel – zie A3 | Knock-out-risico | — |

## 3. Reactie op meldingen: wat kan de ophaaldienst ermee?

| Mogelijke actie | Haalbaar? | Kosten/nadelen **[A]** |
|---|---|---|
| Zak eruit halen | **Nee** – container 3–5 m³, zak onder andere zakken, arbo | — |
| Container apart legen met wagen zónder pers (kraan + open bak/haakarm) | Technisch ja | Extra rit EUR 80–200 per lediging **[A]**; ontwerpt de route om; materieel vaak niet beschikbaar |
| Container legen als laatste van de route / niet persen tot stort | Deels | Wagen vult sneller (geen compactie ≈ 3–5× volume) → extra losritten EUR 100–250 **[A]** |
| Chauffeur alert, thermische camera op laadbak meekijken | Ja | Vereist camera op wagen – dan is de wagen-sensor de echte detector |
| Lading op straat storten bij brand | Gebeurt nu al (Den Helder, Purmerend, Heemskerk, Hilversum, Ede, Eindhoven) | Straat dicht, 2e wagen, brandweer; schade-/opruimkosten niet gepubliceerd |
| Gedragscampagne gericht op wijk | Ja, goedkoop | Effect onzeker; Druten: afvalcoaches onvoldoende effect |

**Kernbevinding 3:** omdat (bijna) elke container een Li-item bevat, kan een ophaaldienst niet "alle gemelde containers apart" behandelen. Actie werkt alleen bij een selectieve top-X % (bijv. ≥ 20 Wh of ≥ 5 items) met een vooraf afgesproken draaiboek. Zonder draaiboek = dashboard dat niemand opent (Dublin: platform kon niet eens automatisch mailen naar de ploeg).

## 4. Alarm-moeheid (alarm fatigue)

| Context | Vals/onnodig aandeel | Bron |
|---|---|---|
| ICU-alarmen | 63,8 % vals (1.394/2.184 in 48 h) | Cho et al., Healthc Inform Res 2016-01 |
| ICU aritmie-alarmen | 87 % vals (9.351/10.699) | UCSF Alarm Study (Drew et al. 2014) |
| Automatische brandmeldinstallaties NL | ≈ 86 % van ≈ 60.000 loze uitrukken komt van BMI; NIFV/NVBR 2008: > 95 % van automatische meldingen onterecht | brandveilig.com (z.d., Siemens); omgevingsweb (2008-onderzoek) |

Les: wanneer > ~70 % van de meldingen niets oplevert, worden alarmen weggeklikt of uitgeschakeld; NL-brandweer reageerde met *verificatieplicht* en kosten doorbelasten. Ons product zit bij basisberekening (PPV 9–27 %) **ruim in de alarm-moeheidszone**.

## 5. Mislukte/teleurstellende smart-waste-pilots

| Pilot | Uitkomst | Faaloorzaak | Bron |
|---|---|---|---|
| Dublin City Council, ~130 bin-sensoren | Verwachte besparing niet gehaald | Behuizing paste niet, connectiviteit, batterijduur, geen automatische alert naar ploeg | Council report 2023; Dublin Inquirer |
| Dharamsala (IN), ondergrondse bakken met sensor (2017) | Bakken overlopen; sensoren kapot of genegeerd | Onderhoud, organisatie reageert niet | Tribune India (z.d.) |
| Cambridge (UK) | Deels succes: 6→5 rondes | Werkt alleen bij koppeling aan route-besluit | Cambridge scrutiny report |
| Generiek (patent) | Optische sensoren dichtgeslibd; slechte netwerkdekking | Vocht/vuil | USPTO 12488320 |

## 6. Bestaande producten en onderzoek (concurrentie)

| Speler | Waar in keten | Principe | Status/prestatie | Bron |
|---|---|---|---|---|
| **Seek Thermal / City of Goodyear (AZ)** | Vuilniswagen, hopper | 2 thermische sensoren, cabinedisplay, alarm 200 °F (93 °C), 12 V | Pilot → SWANA 2025 Best Safety Innovation Award; geen onafhankelijke recall-cijfers | goodyearaz.gov 2025; thermal.com EFD-brochure 2026 |
| **Republic Services + Oshkosh** | Vuilniswagen (EV), bij inname | AI-camera scant lading, chauffeur markeert "sensitive load" | Demo CES 2025-01 | Waste360 2025-01 |
| **Fraunhofer IIS + Lobbe – DangerSort** | Vóór sorteerinstallatie | Hoge-doorvoer röntgen + AI, tot ≈ 30 t/h | Prototype eind 2024, in bedrijf; "yield > 90 %" | Fraunhofer persbericht 2025-05 |
| **Fraunhofer EZRT + WeSort.AI – BREATHE** | Sorteerinstallatie | Multi-energie röntgen + AI | Project 2023-03 – 2025-02 | iis.fraunhofer.de |
| **WeSort.AI – Battery.Sort / X.Sort** | Sorteerinstallatie, front-end | Röntgen + AI, tot 50 cm laagdikte | Klanten Korn Recycling, PreZero; claim −94 % brandrisico (Korn); ≈ EUR 10 mln funding 2026-03 | letsrecycle; ki-syndikat |
| **Lion Vision (UK)** | WEEE-sorteerlijn | Camera + ML, > 600 cilindercellen/h | In bedrijf o.a. SWEEEP Kent (2024) | Recycling Magazine 2024-05 |
| **inSystem.io (NL)** | Sorteerlijn | "Gravity Sorter": AI-camera in vrije val + luchtstoten, 5–70 mm, > 96 % zuiverheid, ≤ 6 t/h | Veldproeven | recyclinginside; MENAFN 2024 |
| **HOBI** | MRF / truck-scanner | Röntgen + camera | Vendor: 94–98 % nauwkeurigheid | hobi.com |
| **DeB-AT (AT)** | Gemengd afval | Sensor + AI | Doel > 95 % detectie (project) | FFG-projectdatabase |
| **Sensoneo** | In container | Vulgraad + temperatuur/brandalarm + kantelalarm | Commercieel, ook (semi-)ondergronds | sensoneo.com, Sigfox partners |
| arXiv 2606.11779 (HS Ruhr West) | Onderzoek | YOLOv5m op röntgen | 94 % precisie | arXiv 2026-06 |

**Kernbevinding 4:** de markt beweegt naar detectie **op de wagen** (thermisch/AI-camera, 1 sensor per wagen i.p.v. per zuil) en **vóór de sorteerinstallatie** (röntgen+AI, bewezen). Detectie bij de inworpzuil heeft geen gevonden concurrent – dat kan witte ruimte zijn óf een signaal dat het niet werkt. Een NL-gemeente met 1.000 zuilen en 10 wagens vergelijkt EUR/zuil × 1.000 met EUR/wagen × 10.

## 7. Brandcijfers NL (context voor A1/A7)

| Cijfer | Waarde | Bron |
|---|---|---|
| Branden in vuilniswagens | ≥ 3 /maand ("tientallen/jr"), stijgend | NVRD via NOS (≈ 2023) |
| Branden inzamelpunten + wagens | ≈ 10 /maand ≈ 120 /jr | Vereniging Afvalbedrijven |
| Branden bij afvalinzameling | "gemiddeld elke week ergens" | Hart van NL 2025-09 |
| Brandweer harde cijfers | Niet beschikbaar | NOS |
| DE: branden in sorteerinstallaties | > 10.000 /jr, ≈ 80 % Li-ion | Fraunhofer 2025-05 (BDE-studie) |
| Batterijbrand-oorzaak voorbeeld | E-bike-motor/accu in restafval (Heerhugowaard) | NH Nieuws |

## 8. Niet gevonden
- Exacte NL-cijfers vandalisme/defecten aan pasvalidatiezuilen (alleen Eindhoven ~1.000 meldingen/maand, jaar ~2019; aantal containers onbekend).
- Kosten van een extra niet-persende lediging en schadebedragen vuilniswagenbrand (NL).
- Aandeel branden dat in de ondergrondse container zelf ontstaat (vs. wagen).
- Onafhankelijke recall/vals-alarmcijfers van thermische truck-camera's.
- Geverifieerde ferro/non-ferro-percentages RWS 2023 (PDF niet bereikbaar).
- Verdeling cel-behuizing (staal/Al/pouch) in vapes.
