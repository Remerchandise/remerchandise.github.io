# Ronde 2 – Shortlist (Orchestrator)

## Wat de sparring opleverde (consensus na R2a/R2b)
1. **"Bevat een accu" per container zegt niets.** In 60–99 % van de ledigingen zit al ≥ 1 Li-item (A1, A6, A8). Alleen een **rangorde** of een **grote-pakketklasse (≥ 50 Wh-eq)** is bruikbaar.
2. **Inductie ziet staal, niet chemie.** 18650 ≈ AA-alkaline (alkaline 5–14× vaker), vapes ≈ folie; metaal in ~85 % van de zakken → PPV als Li-detector 7–27 % (A2, A6, A8). Uitgangspunt 3 van de opdrachtgever is daarmee als *Li-detector* zwak; als *pakketdetector* nog open.
3. **Röntgen per zuil faalt op prijs, niet op fysica.** ≤ 30 kV is vergunningsvrij mogelijk (Bbs art. 3.18, te bevestigen), maar EUR 1–8k per zuil ≫ vermeden schade (~EUR 3/container/maand) (A3, A7).
4. **Continue monitoring ziet een begraven cel niet vóór brand**; wel snelle branddetectie en een "niet legen"-vlag (A4).
5. **Het risico zit in de wagen (persen)** – een wagenoplossing is de benchmark die elk zuilconcept moet verslaan (A5, A7, A8).
6. **Goedkoopste platform = meeliften op de pas-zuil** (accu, modem, pas-event aanwezig) (A5, A7).

## Shortlist voor Ronde 3

| ID | Concept | Samengesteld uit | Waarom getest |
|----|---------|------------------|---------------|
| **K1** | **Strandmetaaldetector in de trommel** – VLF 2–3 frequenties, DD-spoel, alarm bij "Li-verdacht" | A2-C1 (opdrachtgever) | Verplicht; toetst uitgangspunt 3 |
| **K2** | **Pakketwachter** – PI 2-lussen, ferro-kanaal + vervalcurve, 3 klassen (geen/cel/pakket ≥ 50 Wh-eq), alleen rangorde; als OEM-module op de pas-zuil | A2-C3b + A1-C2b + A5-C1b | Sterkste inductie-variant met haalbare doelstelling |
| **K3** | **Röntgen-schaduwdoos ≤ 30 kV** – (a) vast per zuil, (b) rouleerende ijkpaal 1 per 20–50 containers | A3-C1 / A3-C4 | Enige principe dat cellen 'ziet' en telt; toetst uitgangspunt 1 (stilstand) |
| **K4** | **Deksel-eventmodule** – 8×8 IR + passieve CO-cel, continu, "niet legen"-vlag | A4-C1+ (+A4-C2) | Tweede meetmoment; laag energieverbruik |
| **K5** | **Hybride product** – K2 (rangorde) + K4 (event) + actieprotocol (oranje = laatst in route, rood = apart/niet persen) + twee gescheiden kanalen in software | A1-C3b + A6-C2 + K2 + K4 | Kandidaat-product: combineert goedkoop trigger + bevestiging |

Benchmarks (meegerekend, geen zuilproduct):
| **B1** | Thermische camera boven de laadbak van de wagen | A7-C5 / A5-C4b / A8-C2 | Dominantietest (checklist D3) |
| **B0** | Geen sensor: accu-brievenbus aan de zuil + steekproefsortering/risicokaart | A8-C1, A6-C1/C4, A8-C3, A1-C4, A7-C2 | Nulalternatief; levert ook ground truth |

## Wat afvalt en waarom
| Concept(en) | Reden |
|-------------|-------|
| A2-C2 PI-klikker, A1-C1 teller | Li-signaal verdrinkt in Poissonruis van metaaltellingen (A2, A6) – blijft als ondergrens in MC |
| A2-C4 remanentie | Mist pouches (> 60 % risico), ~18 J/puls (A1, A5) – optionele labproef |
| A2-C5 valkoker | Inbouw EUR 500+ en merkspecifiek (A5) – simulatievariant |
| A3-C2/C3/C5 | Prijs, geen netstroom, flux niet aangetoond (A3, A7) |
| A4-C6/C7, A5-C3 | Ziet alleen bovenlaag / gaat op in K4 |
| A4-C4 plop/drukpuls, A4-C5 vape-neus | Fysica onzeker → **alleen labtest** (protocol in R3), niet in vergelijking |
| A5-C4 inductieve laadbakring | Li niet te scheiden (A4) → vervangen door B1 thermisch |
| A6-C3 pieptrommel | Alleen zinvol als pakketklasse haalbaar is → optie binnen K2/K5 |
| A1-C5/A8-C1 met beloning, A8-C4 pas-bericht | Fraude, AVG (A6, A2) → B0 zonder beloning |
| A7-C4 shared savings, A1-C6 | Effect pas na ≥ 30.000 containerjaren aantoonbaar (A6, A7) |
| A7-C3 EPR-bounty | Afgeschaald tot co-financiering in businessmodel |
