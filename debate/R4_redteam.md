# R4 – Red team: finale toets (A8)

Getoetst tegen `R2_A8_redteam_checklist.md`. Bronnen: R3 A4/A6/A7 en A8 `power_analyse`. **[A]** = aanname.

## 1. Toets van de conditionele opties en de MVP

| Punt | B1oem (camera wagen) | K4add (deksel-add-on) | B0 (brievenbus, PRO) | MVP meet-zuil |
|---|---|---|---|---|
| A1–A3 discriminatie | n.v.t. (meet warmte) | n.v.t. (geen accudetector) | n.v.t. | **Nee verwacht** (AUC 0,56–0,6, A2). Dit is precies wat de MVP toetst |
| B1 PPV ≥ 50 % | onbekend: vals alarm in de wagen niet gemeten | nee: ≈ 1,9 vals alarm per containerjaar (A4) | n.v.t. | nee (verwacht 4–5 %) |
| B2 ≤ 2–3 meldingen per wagen per dag | ja, als vals alarm ≤ 1 per wagen per maand (te bewijzen) | ja op hotspots; nee breed (1,9/cj × 125 c/dag ≈ 0,65 per dag) | ja (alleen vol-melding) | n.v.t. (logt alleen) |
| C3/C4 vandalisme, klepstoring | ja (op de wagen, niet publiek) | ja (onder deksel) | **onbekend**: brand/vuurwerk in de bus, hengelen | ja (PE-liner, fail-open nog te borgen) |
| D1 draaiboek | **ja**: lading dumpen (gebeurt al, NH Nieuws) | ja: "niet legen" + brandweer | ja: Stibat-lediging | n.v.t. |
| D3 dominantie t.o.v. wagen | is zelf de benchmark | complementair (containerbrand, stap 3) | complementair (stap 1) | nee |
| D5 vermeden branden met getal | ja: 19 / 49 / 76 % detectie, 10 / 34 / 64 % schade-eq. (A4/A6) | ≈ 0 wagenbranden, wel containerbranden | 3 / 8 / 15 % minder Li-energie **[A]**, niet gemeten | n.v.t. |
| D6 ratio ≥ 1 | **ja ≥ ~3.000 c.** (0,58 bij 1.000, 1,33 bij 10.000) | nee (0,08); alleen ≥ 15 branden/1.000 cj | nee voor gemeente (0,02); ja als OPEN betaalt en sortering wegvalt | n.v.t. (go/no-go-budget EUR 37–102k) |
| E1 AVG | camera richt op laadbak → geen personen in beeld vereist | ja | ja (zonder beloning) | ja (geen pas-koppeling) |
| E4 validatieplan | ja, maar alleen indicatief: 12 mnd incidenten, statistisch zwak (≥ 41k cj nodig voor −30 %) | veld: 20 containers × 3 mnd | ja: 2 × ≥ 1 t "alle batterijen" | ja: 62 gespikete zakken per klasse |

**Oordeel**
- **B1oem: overleeft.** Voorwaarde: vals-alarm per wagen per maand moet in de pilot gemeten worden, want dat is de grootste onbekende.
- **K4add: overleeft alleen als niche-veiligheidsfunctie op hotspots.** Verkopen als "accudetectie" zou misleidend zijn.
- **B0: overleeft voorwaardelijk.** Het effect is onbewezen. Brandveiligheid van de bus (labtest) en de betaler OPEN zijn harde voorwaarden.
- **MVP: overleeft als falsificatie-experiment.** Het go/no-go-criterium (AUC ≥ 0,85, PPV ≥ 30 %) is goed gekozen. Wel aanvullen met: koppeling aan een pas uitgesloten, fail-open-klep, ≥ 300 echte zakken, en de 62 gespikete zakken per klasse geblindeerd.

## 2. Aanval op de eigen conclusie: te pessimistisch?

Break-even (aantal branden per 1.000 containerjaar voor ratio 1; basis 1,27; A7):

| Concept | Break-even | Factor t.o.v. basis | Realistisch? |
|---|---|---|---|
| B1oem | 2 | 1,6× | **Ja**: VA ≈ 120 branden/jr bij inzameling; NVRD ≥ 36/jr wagens. Op ≈ 3,2 Mt ≈ 100k containerjaar-equivalent **[A]** ≈ 0,4–1,2 per 1.000. Bij een slechte vloot of hoog vape-gebruik haalbaar |
| K4add | 15 | 12× | Alleen hotspots (stations, jaarwisseling) |
| B0 | 67 | 53× | Nee als brandbescherming; wel als EPR-inzamelkanaal (andere baat) |
| K2 | 220 | 170× | Nee |
| K1 | 318 | 250× | Nee |

**Wat zou het omdraaien?**
- **(a) Brandkans 10×:** die zit nog onder de break-even van K2 (220).
- **(b) Schade per brand 10×:** bijvoorbeeld een grote sorteerinstallatie- of bunkerbrand van EUR 1–10 mln, zoals Duitse sorteerinstallaties (> 10.000 branden/jr, 80 % Li). Maar een perfecte zuilsensor raakt binnen het meldingsbudget maar ≈ 6 % van het risico (A6). K2 komt dan op ratio ≈ 0,06.
- **(c) Data- en gedragswaarde:** stel dat een zuilsignaal Li in restafval met 10 % verlaagt over de hele keten. Bij een totale schade van ≈ EUR 48 per container per jaar (afgeleid uit B1: 16,3/0,34) is dat ≈ EUR 5 per container per jaar, tegenover EUR 170 kosten (K2).
- Pas bij het hoge scenario (48 branden/1.000 cj) **én** gedragseffect ≥ 30 % wordt een zuilproduct verdedigbaar. Dat vereist voorwaarden waarvoor ik geen bewijs vond.

**Oordeel: de conclusie is robuust.** De enige echte omslag is een *regelgevend* scenario dat de waarde niet uit schade haalt: een verplichte meting van het EPR-lek door OPEN of IenW. Dan is K3b als meetdienst (EUR 5–15k per campagne) de kandidaat, niet een abonnement.

## 3. Top-5 risico's van het geadviseerde pad (slide 21)

| # | Risico | Kans | Impact | Mitigatie |
|---|---|---|---|---|
| 1 | B1: te veel vals alarm (zon, hete motor/uitlaat, hydraulische olie) → chauffeur negeert alarm (alarm-moeheid, BMI-ervaring ≥ 86 % loos) | Middel | Hoog | Pilot 2–4 wagens × 6 mnd; doel ≤ 1 vals alarm per wagen per maand; ΔT/dt-regel; terugkoppelknop |
| 2 | Geen koper: inzamelaar ziet baat niet (attributie onmeetbaar: ≥ 41k–412k cj voor −30 %) | Hoog | Hoog | Verkopen op arbo/chauffeursveiligheid en verzekeringspremie; fabrieksoptie via voertuigbestek (HVC/Renewi) |
| 3 | Concurrent eerst: Seek Thermal, Oshkosh/Republic, wagenbouwers (Geesink, Terberg) bouwen het zelf in | Hoog | Middel | Geen eigen hardware; rol = integratie, draaiboek, data-laag en risicokaart |
| 4 | B0-bus wordt zelf brand- of vandalismebron (jaarwisseling, hengelen) | Middel | Middel | Brandwerende RVS, vermiculiet, labtest TR van 1 cel; tijdens de jaarwisseling afsluiten |
| 5 | MVP geeft fout-positieve "go" (labzakken te schoon, positie-effect 171×) → investering in een doodlopende inductieroute | Laag–middel | Hoog | Geblindeerd, realistische metaalmix (5,9 metaalobjecten per zak), echte RVS-trommel, vooraf vastgelegd criterium, onafhankelijke beoordeling |

## 4. Is "alleen melden, niet ingrijpen" genoeg?

**Nee.**
- Zonder actie is de vermeden schade **EUR 0**.
- Mét actie levert zelfs een perfecte zuilsensor ≤ **EUR 0,15 per container per maand** op (5,8 % van de wagenbranden); K2 levert EUR 0,04.
- Elke melding kost EUR 10–150 aan vervolgactie. Dat is EUR 42 per container per jaar bij 20 meldingen per 1.000 ledigingen, en ≈ 40× de baat (A7).
- Melden zonder ingreep is dus een kostenpost. Waarde ontstaat alleen bij ingrijpen in de wagen (B1: dumpen) of aan de bron (B0).
