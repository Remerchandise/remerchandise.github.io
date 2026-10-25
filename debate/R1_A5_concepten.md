# R1 – A5 Product & hardware: concepten

Basis: `research/A5_hardware.md`. Prijzen EUR 2026 excl. btw, @1 000 st., aannames **[A]**. Geen kritiek in deze ronde; zwakke punten alleen benoemd als open vraag voor R2.

| ID | Naam | Sensor | Meetmoment | Drempel | Signaal | Verdienmodel | Ruwe kostprijs HW | Label |
|---|---|---|---|---|---|---|---|---|
| A5-C1 | **Pas-zuil OEM-insteekmodule** | Wervelstroom/PI-spoel in trommelwand + kleine MCU (STM32U5) | Per inworp, getriggerd door pas-event/trommel-dicht | Score > drempel (metaalsignatuur "cilindrisch/opgerold") → vlag in pas-record; container-score = som over dagen | Meelift op bestaand toegangsbericht (3×/dag) + direct alarm via OEM-modem | Licentie via OEM (Bammens/Vconsyst/Ecosmart): EUR 1–2 /container/mnd, of meeverkocht in nieuw bestek | 15–30 (module) + 30–60 installatie | **Radicaal eenvoudig (integratie)** |
| A5-C2 | **"Strandmetaaldetector-puck"** standalone | PI-detector, spoel Ø 15–20 cm, gegoten in IP68-puck op trommelachterwand | Per inworp (trilling/reed-contact wekt op), 3–5 s | Aantal inworpen met sterk metaal-/Li-signatuur per container per week | 1× per dag teller + direct alarm boven drempel; 1NCE LTE-M of LoRaWAN | Per container EUR 2–4/mnd incl. dashboard | 35–55 + 25–50 installatie | **Radicaal eenvoudig (standalone)** |
| A5-C3 | **Deksel-sentinel** continu | NTC-reeks + MOX-gas (BME688) + CO-cel, in containerkop/onder deksel | Continu, elke 5–15 min; snelle modus bij stijging | dT/dt > X K/h of CO/H2-trend → brandrisico-alarm | Alarm direct; status 1×/dag | Per container EUR 2–3/mnd; bundel met vulgraadsensor | 30–60 | Aanvullend (stap 3) |
| A5-C4 | **Laadbak-poort op de vuilniswagen** | Grote PI/VLF-ring om de stortopening van de kraanwagen + RFID/GPS van container (al aanwezig) | Bij lediging: inhoud valt 1–2 m door ring, vóór de persplaat | Signatuur per lediging; boven drempel → chauffeur stopt, container apart/handmatig | Cabine-display + backoffice; per lediging toegewezen aan container-ID | Per wagen EUR 150–300/mnd (1 wagen dekt 200–500 containers) | 1 500–4 000 per wagen | **Onconventioneel** |
| A5-C5 | **Batterijloze trommel-oogster** | Generator op trommelas (gebruiker draait trommel) → voedt LDC-wervelstroommeting + LoRaWAN-bericht | Per inworp, alleen met geoogste energie (0,6–1,2 J) | Per inworp score; drempel in cloud | 1 LoRa-pakket (SF7–SF9) per inworp; geen batterij, geen onderhoud | Per container EUR 1–2/mnd | 25–45 | **Onconventioneel** |

## Werking (2–3 zinnen per concept)

**A5-C1 – Pas-zuil OEM-insteekmodule.** De zuil heeft al accu, modem, behuizing en een pas-event dat het exacte begin/einde van elke inworp markeert. Een kleine dochterkaart met spoel in de trommelwand meet alleen tussen "trommel dicht" en "trommel kantelt" (1–10 s stilstand) en hangt een score aan het bestaande pas-record; geen eigen modem, sim, batterij of certificering van radio. Extra energie ~0,03–0,1 mWh/inworp (< 15 mWh/dag) – verwaarloosbaar t.o.v. slot en modem. Bonus: koppeling aan pas maakt (AVG-getoetste, A6) gedragsfeedback per huishouden mogelijk.

**A5-C2 – Strandmetaaldetector-puck.** Eén volledig gegoten puck (spoel + nRF9151 + 1× LS33600 D-cel) wordt met 4 RVS-bouten op de trommelachterwand gezet; plaatsen in 20 min, geen koppeling met wie dan ook. Wakker via trilling, 3–5 s PI-meting met nulmeting van de lege trommel, dagelijks één bericht. Energie 8–21 mWh/dag → 5,6–14 jaar op één cel.

**A5-C3 – Deksel-sentinel.** Meet waar het werkelijke brandrisico in de container zit (stap 3): temperatuur en uitgassing in de kopruimte van de container, uren tot dagen na inworp. Ondergebracht onder het zuildeksel/containerkop, eigen batterij of meeliften op toegangsaccu; combineert met bestaande vulgraadsensor (zelfde plek, zelfde bericht). Vooral zinvol als bevestiging van A2/C1/C2-vlaggen (A4 werkt de sensoriek uit).

**A5-C4 – Laadbak-poort op de vuilniswagen.** Niet elke container instrumenteren, maar de ~1 wagen die 200–500 containers leegt: tijdens lediging valt alles door een ring boven de stortopening, *vóór* de persplaat (stap 5 = hoofdbrandmoment uit kickoff). Container-ID komt uit het bestaande RFID/weegsysteem van de wagen; bij alarm stopt de chauffeur de persing of dumpt apart. Ordegrootte 100× minder apparaten, wel moeilijk signaal (vallende massa, metalen wagen) – voor A2/A8.

**A5-C5 – Batterijloze trommel-oogster.** De gebruiker levert bij elke inworp mechanische arbeid (~6 J) door de trommel te draaien; een kleine generator/piëzo oogst 0,6–1,2 J, genoeg voor één wervelstroommeting (0,03 mWh = 0,1 J) en één LoRa-pakket (0,005–0,02 mWh). Geen batterij = geen batterijwissel, geen brandbare cel in een brandsensor, onbeperkte levensduur. Open vraag: zuilen met motor-/veergestuurde trommels.

## Open vragen voor R2 (aan andere agents)

| Aan | Vraag |
|---|---|
| A2 | Detecteerbaarheid door/achter RVS 304-trommel (δ 4–13 mm) en op een meedraaiende spoel; vallende massa (C4) in 0,1–0,3 s? |
| A6 | Score in pas-record (C1): AVG en dashboardlogica; wat doet ophaaldienst met een vlag? |
| A7 | OEM-licentie vs. eigen abonnement; per-wagen-model (C4) vs. per-container |
| A4 | Sensorset C3, valse alarmen (zon op deksel) |
| A8 | Vandalisme/vuil op puck (C2), oogst-betrouwbaarheid (C5) |
