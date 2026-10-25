# Ronde 4 – Scorekaart, productkeuze en MVP (Orchestrator)

Bron: `experiments/r4_scorekaart/scorekaart.py` → `scorekaart.csv/json`. Gewichten: detectie 25 %, kosten 20 %, eenvoud 15 %, inpasbaarheid 15 %, juridisch/veiligheid 10 %, waarde 15 %. Prijspeil EUR 2026 excl. btw. Het werkpunt is werkbaar voor de ophaaldienst: ≤ 20 meldingen per 1.000 ledigingen, ≤ 1 rood per wagen per week (A6, A8).

## Scorekaart

| ID | Concept | Det | Kost | Eenv | Inpas | Jur | Waarde | **Gewogen** | Knock-out | Oordeel | Betrouwb. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | Strandmetaaldetector (VLF) | 1 | 3 | 4 | 3 | 5 | 1 | **2,55** | discriminatie | NIET AANBEVOLEN | hoog |
| K2 | Pakketwachter (PI, OEM) | 1,5 | 3 | 3 | 3 | 5 | 1 | **2,52** | vals alarm, prijs > schade | NIET AANBEVOLEN | middel |
| K3a | Röntgen vast per zuil | 3 | 1 | 2 | 1 | 3 | 2 | **2,00** | prijs, energie | NIET AANBEVOLEN | middel |
| K3b | Röntgen-ijkpaal | 3 | 2 | 2 | 3 | 3 | 2 | **2,50** | prijs (als product) | NIET AANBEVOLEN (wél als labinstrument) | middel |
| K4 | Deksel-eventmodule los | 2 | 4 | 4 | 4 | 5 | 2 | **3,30** | geen accudetector, prijs | NIET AANBEVOLEN | middel |
| K4add | K4 als add-on op vulgraadsensor, hotspots | 2 | 5 | 4 | 5 | 5 | 2 | **3,65** | – | **CONDITIONEEL** | laag |
| K5 | Hybride K2+K4 | 1,5 | 2 | 2 | 3 | 4 | 2 | **2,23** | vals alarm K2, prijs | NIET AANBEVOLEN | middel |
| B1 | Camera laadbak, abonnement | 4 | 3 | 4 | 4 | 4 | 3 | **3,65** | prijs > schade bij 1.000 c. | NIET AANBEVOLEN (zo) | middel |
| B1oem | Camera laadbak, fabrieksoptie wagen | 4 | 4 | 4 | 4 | 4 | 4 | **4,00** | – | **CONDITIONEEL** (benchmark, buiten zuil-scope) | middel |
| B0 | Accu-brievenbus aan zuil, PRO-betaald | 2 | 3 | 5 | 4 | 5 | 3 | **3,40** | – | **CONDITIONEEL** | laag |

Geen concept haalt **AANBEVOLEN**: in het basisscenario (1,27 wagenbranden per 1.000 containerjaar, A6/A1) is voor elk zuil- of containerconcept het abonnement hoger dan de vermeden schade (A7). Dat is de knock-out uit de opdracht.

## Per concept: de drie belangrijkste argumenten

**K1 – Strandmetaaldetector (uitgangspunt 3).** Betrouwbaarheid: hoog.
1. Inductie ziet staal, niet chemie. Een 18650 ≈ een AA-alkaline, en alkaline komt 5–14× vaker voor. In een echte zak (gemiddeld 5,9 metaalobjecten) wordt 13 % van de 18650's gedetecteerd. De AUC voor cel tegen gewone zak is 0,56–0,59 (A2 `r3_inductie`).
2. Bij ≤ 20 meldingen per 1.000 ledigingen is de energierecall 3,6 % en de PPV 5 %. Dat is nauwelijks beter dan willekeurig melden (1,5 %) (A6).
3. Langer meten dan ~0,3 s levert niets op. Stilstand helpt alleen om de trommel af te trekken. Uitgangspunt 1 geldt dus niet voor inductie (A2).

**K2 – Pakketwachter.** Betrouwbaarheid: middel. Niets is gemeten; de objectparameters zijn aannames.
1. Het meest haalbare doel is een pakket ≥ 20 Wh-eq herkennen. Ook dan is de recall per inworp 8–12 % en de PPV 4 %. Positie geeft 171× spreiding en de Wh-fout is σ ≈ 0,7 (A2).
2. Op containerniveau is K2 even goed als B0 zonder sensor: energierecall 4,4 % in beide gevallen (A6).
3. De kostprijs is het laagst van alle zuilconcepten (TCO EUR 1,50 per maand). Het abonnement is EUR 10,7 bij 1.000 containers en EUR 5,7 bij 10.000 (A5, A7). De vermeden schade is EUR 0,08 per maand.

**K3a/K3b – Röntgen.** Betrouwbaarheid: middel. De regelgeving moet een stralingsdeskundige bevestigen.
1. Fysiek werkt het: cellen zijn zwart, blik en folie zijn transparant. De recall op pakketten per inworp is 82 % (A3, A6). Toch is de PPV op Li per inworp maar 12 %, omdat alkaline en sleutels er hetzelfde uitzien en dual-energy daar niet helpt.
2. Vergunningsvrij lijkt mogelijk: ≤ 30 kV en ≤ 1 µSv/h op 0,1 m (Bbs art. 3.18). De zuilwand van 3 mm staal geeft daarvoor ruim voldoende marge (A3).
3. De kosten zijn EUR 1.785 hardware per zuil, een abonnement van EUR 90 per maand en 1,2–5,5 Wh per dag. Dat is niet off-grid haalbaar (A5, A7). Stilstand maakt een goedkope detector mogelijk, maar niet een goedkoop product.

**K4 / K4add – Deksel-eventmodule.** Betrouwbaarheid: laag tot middel.
1. Hij waarschuwt vrijwel nooit vóór thermal runaway: in 0–5 % van de gevallen. Brand na TR ziet hij wel binnen 60 minuten, in 48–100 % van de gevallen (A4).
2. CO alleen geeft 2–36 valse alarmen per containerjaar door rotting. Met de regel stijgsnelheid + IR + CO blijft er ~1,9 alarm per containerjaar over door hete objecten (A4). Het is dus een branddetector, geen accudetector.
3. Als losse module kost hij EUR 13,9 per maand. Als add-on op een bestaande vulgraadsensor is dat EUR 2,2–3,6 (A7). Hij verdient zich terug vanaf ~15 containerbranden per 1.000 containerjaar, en dat haal je alleen op hotspots.

**K5 – Hybride.** Betrouwbaarheid: middel.
1. Hij erft het vals-alarmprobleem van K2. De energierecall is 4,4 %, gelijk aan B0.
2. Het is het duurste inductieconcept: abonnement EUR 18,6 per maand.
3. Wat wel blijft staan is het idee om rangorde en event in twee aparte kanalen te behandelen. Dat neemt de software van K4add en B1 over.

**B1 / B1oem – Thermische camera boven de laadbak (benchmark).** Betrouwbaarheid: middel.
1. Hij meet waar het risico ontstaat, bij het persen. Hij detecteert 19–76 % van de wagenbranden binnen ~1 s (A4, Seek Thermal/Goodyear 2025).
2. Als fabrieksoptie kost hij EUR 2,3 per container per maand bij 1.000 containers en EUR 0,97 bij 10.000. De verhouding baat/kosten is 0,58 tot 1,33, met break-even rond 3.000 containers, ofwel 10 wagens (A7).
3. De baat valt bij de inzamelaar (67 %), niet bij de gemeente. De inzamelaar is dus de koper, via het voertuigbestek.

**B0 – Accu-brievenbus aan de zuil.** Betrouwbaarheid: laag, want het effect op het gedrag is onbekend.
1. Het pakt de prevalentie aan, zonder vals alarm en zonder persoonsgegevens.
2. Stichting OPEN heeft een wettelijk inzameldoel (63 % in 2027). Een gemeentelijk abonnement is daarom niet nodig.
3. Het effect is niet gemeten. Om 2× verschil in Li per ton tussen clusters aan te tonen is 1,5–8 t gesorteerd afval per cluster nodig (A8). Bij "alle batterijen" als maat volstaat ~1 t.

## Voorwaarden voor de CONDITIONELE opties

| Optie | Voorwaarde | Hoe toetsen |
|---|---|---|
| B1oem | Inzamelaar met ≥ 10 wagens (~3.000 containers) en ≥ 1,3 wagenbranden per 1.000 containerjaar. Vals alarm ≤ 1 per wagen per maand | Branddata van de inzamelaar over 3 jaar; pilot op 2 wagens gedurende 6 maanden |
| K4add | Alleen op containers met ≥ 15 brandmeldingen per 1.000 containerjaar, en meeliften op een bestaande vulgraadsensor tegen ≤ EUR 2 per maand | Brandhistorie per locatie; veldmeting op 20 containers gedurende 3 maanden (labtest L1–L5 van A4) |
| B0 | Betaling door de PRO, plaatsing aan de zuil zonder beloning, brandwerende bak. Doel ≥ 20 % minder Li per ton in het pilotcluster | Sorteeranalyse vóór en na: 2 × 1 t per cluster op de maat "alle batterijen" (A8) |

## Productkeuze

**Advies: start geen abonnement op een accudetector in de inworpzuil.** Uitgangspunt 3 (metaaldetector) en uitgangspunt 5 (abonnement per container) zijn op deze gegevens verworpen. Uitgangspunt 1 (stilstand) is maar deels juist: het helpt röntgen, maar maakt het niet betaalbaar. Uitgangspunt 2 (risicodrempel) klopt, maar die drempel is per container niet goed te meten: in 95 % van de ledigingen zit al een Li-item.

Wat wél waarde heeft, gesorteerd op waarde per euro:
1. **Thermische camera op de wagen** (B1oem), voor de inzamelaar.
2. **Preventie aan de zuil** (B0), betaald door de PRO.
3. **Brandmelding in de container** (K4add), alleen op hotspots.

## MVP: eenvoudigste prototype in één zuil (3–6 maanden)

De opdracht vraagt om een zuilprototype. Het eenvoudigste dat de kernvraag beslist, is een **meet-zuil**. Het doel is de modelaannames voor inductie te falsificeren of te bevestigen, plus een K4-lite onder de deksel. Het is bedoeld als go/no-go en niet als product.

| Onderdeel | Inhoud | Kosten laag / basis / hoog |
|---|---|---|
| K2-lite | 2 PI-lussen in een PE-liner, STM32-front-end, logging van ruwe vervalcurves | EUR 3k / 5k / 8k hardware |
| K4-lite | AMG8833-klasse IR + TGS5042 CO + NTC, BLE/LTE-M | EUR 0,3k / 0,5k / 1k |
| Engineering | Embedded, mechanisch, data: 300 / 450 / 700 h × EUR 95 | EUR 29k / 43k / 67k |
| Installatie | 1 zuil via de OEM-servicepartner, incl. vergunning gemeente | EUR 1k / 2k / 4k |
| Validatie | 62 gespikete zakken per klasse (A8) + 300 echte zakken handmatig sorteren | EUR 4k / 7k / 12k |
| Optioneel | Röntgen-referentiebeelden van 300 zakken (huur bagagescanner, lab) | EUR 0 / 5k / 10k |
| **Totaal** | | **EUR 37k / 62k / 102k** |

Go/no-go-criterium: pakket ≥ 20 Wh-eq met AUC ≥ 0,85 en PPV ≥ 30 % bij ≤ 2 % gemelde zakken in de echte RVS-trommel. Haalt het prototype dat niet, dan is de inductieroute definitief af. A2 verwacht een AUC van 0,56–0,6.
