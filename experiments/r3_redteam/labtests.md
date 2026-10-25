# A8 – Labtestontwerpen (Ronde 3)

Dit document beschrijft de proeven voor alles wat **alleen met een prototype te bevestigen** is. Getallen voor n komen uit `power_analyse.py` (resultaten in `results.json`). EUR 2026 excl. btw, **[A]** = aanname.

## 0. Kerngetallen uit de power-analyse (params.py, basis)

| Grootheid | Laag | Basis | Hoog |
|---|---|---|---|
| P(zak bevat ≥ 1 Li-item) | 1,5 % | 2,9 % | 7,1 % |
| P(zak bevat Li ≥ 10 Wh-eq) | 0,15 % | 0,30 % | 0,75 % |
| P(zak bevat item ≥ 50 Wh-eq) — *in params alleen e-bike/step; laptop = 48* | 0,005 % | 0,010 % | 0,025 % |
| Natuurlijke zakken te sorteren voor recall 0,8 ± 0,10 (95 %), alle Li | 4.235 (21 t) | 2.133 (11 t) | 873 (4 t) |
| Idem, Li ≥ 10 Wh-eq | 41.365 (207 t) | 20.698 (104 t) | 8.298 (41 t) |
| Idem, ≥ 50 Wh-eq | 1,24 mln (6.200 t) | 0,62 mln (3.100 t) | 0,25 mln (1.240 t) |
| Positieve zakken nodig (recall 0,8; ± 0,10 / ± 0,05) | 62 / 246 | | |
| Alarmen nodig om PPV ≈ 0,27 op ± 0,10 te meten | 76 | | |
| Max. vals-positief per zak voor PPV ≥ 50 % op klasse ≥ 20 Wh-eq (prevalentie 0,15 %, recall 0,8) | **≤ 0,12 %** (specificiteit ≥ 99,88 %) | | |

**Gevolg 1.** Een veldtest met alleen natuurlijke zakken is onhaalbaar voor de klasse die ertoe doet (≥ 10–50 Wh-eq): daarvoor moet 100 tot 3.100 t afval gesorteerd worden. Recall op hoge-energie-items wordt daarom **met spiking gemeten** (geblindeerde testzakken met bekende inhoud). Natuurlijke zakken dienen alleen om de vals-alarmlast te meten.

**Gevolg 2.** De pakketwachter (K2) moet per zak specificiteit ≥ 99,88 % halen. Pannen en gereedschap alleen al zitten in ≈ 2 % van de zakken (params), dus die moeten voor ≥ 94 % als "geen pakket" worden herkend. Dit is het harde slaag/zak-criterium voor L1.

---

## L1 – Inductie (K1 VLF, K2 PI) in een echte RVS-trommel

| Onderdeel | Ontwerp |
|---|---|
| Vraag | Scheidbaarheid Li-cel/-pakket tegenover alkaline, blik, folie, sleutels, pan; effect van positie, oriëntatie, trommelstand en drift |
| Opstelling | Originele inworptrommel (RVS 304, 1–2 mm, 30/60 L) uit een gesloopte zuil, gemonteerd in een verzinkte zuilmantel (3 mm). Spoelen volgens A2-ontwerp: K1 = DD-spoel 2–3 frequenties; K2 = 2 PI-lussen met 16–32 vervalvensters plus ferro-kanaal. Meedraaiend achter een kunststof liner (A3-aanval). Motorische trommelbediening voor herhaalbaarheid. Klimaatkast of buitenopstelling. |
| Testobjecten (≥ 3 merken/exemplaren per klasse) | **Li:** 18650 (vol/leeg), 21700, 14500, vapes (5 types, waarvan ≥ 2 illegaal), telefoons (3), oortjes, powerbank 10 en 20 Ah, laptoppack, gereedschapsaccu 18 V, e-bike-module. **Niet-Li:** AA/AAA alkaline (3 merken), 9 V, CR2032. **Clutter:** Al-blik heel en geplet, stalen conservenblik, 10 kroonkurken, Al-folieprop 5 en 20 g, theelichtjes, Al-koffiecups, sleutelbos, bestek, schaar, pan, oplader met kabel, afstandsbediening zonder batterij |
| Veiligheid | Cellen op 0–30 % SOC, polen afgeplakt; pakketten met BMS intact; brandblusdeken en zandbak; geen beschadigde cellen |
| Protocol A – losse objecten | Raster van 3×3×3 posities × 4 oriëntaties × 2 trommelstanden. Per meting een nulmeting van de lege trommel in dezelfde hoek. **n ≥ 50 metingen per klasse** → AUC ± 0,09 bij AUC 0,8; n = 100 → ± 0,06 |
| Protocol B – realistische zakken | 5 kg matrix (papier, nat gft, plastic), clutter getrokken uit `params.ITEMS`, wel/niet gespiked. **200 zakken (100 met, 100 zonder Li-pakket/-cel)**, gerandomiseerd en geblindeerd voor de operator |
| Protocol C – drift | 72 h lege trommel, −10…+50 °C, 85 % RV; 500 trommelcycli; detectorofset en ruis gelogd |
| Meettijd | Integratie 0,5 / 2 / 5 / 10 s per zak, om uitgangspunt 1 te toetsen (SNR ∝ √t of drift-gelimiteerd?) |
| Slaag/zak | **K1 (Li-detector):** specificiteit ≥ 95 % bij recall ≥ 80 % voor 18650 tegenover AA + blik (checklist A1). **K2:** specificiteit ≥ 99,88 % per zak voor klasse ≥ 20 Wh-eq bij recall ≥ 80 % (Protocol B, met pan/gereedschap in de clutter) |
| Kosten/doorlooptijd | Trommel en zuil EUR 1–3k, elektronica EUR 2k, objecten EUR 1,5k, 4–6 weken **[A]** |

## L2 – Röntgen K3: dosimetrie en beeld

| Onderdeel | Ontwerp |
|---|---|
| Vraag | (1) Is lekstraling ≤ 1 µSv/h op 0,1 m van elk bereikbaar oppervlak (Bbs art. 3.18) haalbaar bij maximale instellingen, ook bij fouten? (2) Scheiding cel/alkaline in een echte zak. |
| Opstelling | K3a-prototype in trommel; strooifantoom: 5 kg zak (water-equivalent 2–13 g/cm²) met Al- en Fe-objecten |
| Instrument | Gekalibreerde **ionisatiekamer** voor lage energie (10–40 keV); géén GM-buis, die onderschat bij lage energie. Plus passieve dosimeters (TLD/OSL) voor 1 maand |
| Protocol | Max kV/mA, raster van 10 cm over alle buitenoppervlakken plus de spleten van klep en trommel; ≥ 60 s per punt, achtergrond aftrekken. Foutinjectie: klep open tijdens belichting, interlock overbrugd, trommel half gesloten. Uitschakeltijd ≤ 10 ms meten. |
| Slaag/zak | Max ≤ 0,5 µSv/h (veiligheidsfactor 2) op elk punt; interlock in 100 % van 100 foutpogingen |
| Beeld | Protocol B uit L1 (200 zakken); gemeten: aantal cellen ± 1, en alkaline tegenover Li-ion (verwacht: niet scheidbaar bij 30 kV, A2-aanval) |
| Formeel | Voorleggen aan ANVS/stralingsdeskundige (niveau 3) vóór een veldtest |

## L3 – Vape-neus (A4-C5)

| Onderdeel | Ontwerp |
|---|---|
| Vraag | Ziet een MOX-sensor (BME688 ×2, verschillende heaterprofielen) in 2–10 s een vape of lekkende cel door een dichtgeknoopte zak? |
| Opstelling | Trommelmock van 60 L, PMMA, met klepbeweging die lucht uit de zak perst. Gecontroleerde ventilatie tussen runs. |
| Monsters | 10 vapetypes (nieuw, half leeg, lekkend), open e-liquid, 18650 met elektrolytlek (alleen in zuurkast). **Stoorbronnen:** parfum, schoonmaakmiddel, nat gft, koffiedik, luiers, sigarettenpeuken, alcohol, zure melk |
| Zakstatus | open / enkel geknoopt / dubbel verpakt |
| Protocol | Blootstelling 2, 5 en 10 s; geblindeerde, gerandomiseerde volgorde; **n ≥ 30 per conditie** (recall ± 0,15). Carry-over-test: 5 schone zakken direct na elke positieve. |
| Slaag/zak | Recall ≥ 50 % voor een vape in een geknoopte zak bij vals-alarm ≤ 5 % over de stoorbronnen; carry-over ≤ 1 vals alarm per 5 |

## L4 – Drukpuls / "plop" (A4-C4)

| Onderdeel | Ontwerp |
|---|---|
| Vraag | Is het openen van een ventiel of pouch door ≥ 0,5 m afval hoorbaar of meetbaar met een MEMS-microfoon en barometer? |
| Opstelling | Container-mock van 1 m³ gevuld met echt restafval, in een brandproefbunker van een geaccrediteerd lab (Efectis/TNO/DNV **[A]**) |
| Protocol | Venting opwekken met spijker of overladen van 18650 en pouch op 0,2 / 0,5 / 1,0 m diepte, 5 herhalingen per diepte. Sensoren onder het deksel. Ook 2 weken achtergrondopname bij een echte container (verkeer, inworp, wind, jaarwisseling). |
| Slaag/zak | Detectie ≥ 80 % op 0,5 m bij ≤ 1 vals alarm per container per maand (uit de achtergronddata) |

## L5 – Veldtest 1–3 zuilen met steekproefsortering als ground truth

| Onderdeel | Ontwerp |
|---|---|
| Vraag | Recall, vals-alarmlast en meldingen per route onder echte omstandigheden |
| Opzet | 2 zuilen met prototype (K2/K5), 1 controlezuil, 8 weken. Na elke lediging gaat de inhoud **ongeperst** naar een sorteerlocatie (Eureco-methode), met een niet-persende kraanwagen |
| Koppeling zak ↔ inworp | Natuurlijke zakken zijn achteraf niet aan een inworp te koppelen zonder camera (AVG). Daarom: (a) **spiking** met RFID-gelabelde, geblindeerde testzakken (62 per klasse voor recall ± 0,10; 246 voor ± 0,05), en (b) natuurlijke zakken alleen op **containerniveau** (aantal Li-items en Wh tegenover containerscore) en voor vals-alarm per inworp |
| Omvang natuurlijk | Basis 2.133 zakken ≈ 11 t voor recall van "alle Li" (± 0,10). Met 3 containers × 8 ledigingen × ≈ 0,6 t ≈ 14 t is dat haalbaar. De klasse ≥ 10 Wh-eq is **niet haalbaar** (104 t) → spiking |
| PPV | ≥ 76 alarmen nodig voor PPV ± 0,10 rond 0,27 |
| Kosten | Sorteren ≈ EUR 150–250/t, extra ledigingen ≈ EUR 100–200 per stuk → EUR 10–20k plus personeel **[A]** |

## L6 – Steekproefsortering als dienst (B0/A8-C3): zelfcorrectie

Voor een 2× verschil in Li-items/t tussen twee clusters (power 0,8, α 5 %) is **≈ 4 t per cluster nodig (basis; laag 8 t, hoog 1,5 t)**. Mijn R1-voorstel (50–100 kg per kwartaal) is dus te zwak voor lithium. Met de proxy "alle batterijen" (≈ 36/t, Eureco-methode) is **≈ 1 t per cluster** genoeg. → B0 moet rapporteren op *alle batterijen/t* (inclusief alkaline) per wijkcluster, met ≥ 1 t per cluster per jaar.

## L7 – Branden als uitkomstmaat: niet doen

Om een brandreductie van 30 % aan te tonen zijn per arm **≈ 96.000 containerjaren** nodig (laag 412.000, hoog 41.000); voor 50 % ≈ 31.000. Elke businesscase of pilot die op "minder branden" wordt afgerekend is daarom onmeetbaar. Afrekenen moet op proxies: batterijen/t, recall bij spiking en meldingen per route.
