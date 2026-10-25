# R1 – A3 concepten (Röntgen met stilstand)

Basis: `research/A3_rontgen.md`. EUR 2026 excl. btw; aannames **[A]**. Ronde 1 = divergeren, geen kritiek.

Gemeenschappelijk regelgevingskader: Bbs art. 3.18 lid 1 b – toestel **≤ 30 kV** (of ANVS-goedgekeurd type) én **≤ 1 µSv/h op 0,1 m** van elke bereikbare buitenzijde → geen kennisgeving/registratie/vergunning.

## Overzicht

| ID | Naam | Label | Sensor | kV / regime | Ruwe HW-kostprijs (laag/basis/hoog) |
|----|------|-------|--------|-------------|-------------------------------------|
| A3-C1 | Schaduwdoos | **Radicaal eenvoudig** + vergunningsvrij | 30 kV mini-buis + GOS-scherm + camera | ≤ 30 kV, vrijgesteld | 900 / 2 000 / 4 500 |
| A3-C2 | Trommelscan | vergunningsvrij, betere beeldkwaliteit | 30 kV waaierbundel + 64–128-kanaals lijnarray; trommelrotatie = scanbeweging | ≤ 30 kV, vrijgesteld | 1 200 / 2 800 / 6 000 |
| A3-C3 | Typegoedgekeurde dual-energy zuil | prestatievariant | 60–80 kV + dual-energy LDA | ANVS-typegoedkeuring → vrijgesteld | 5 000 / 9 000 / 18 000 |
| A3-C4 | Röntgen-ijkpaal ("teacher-sensor") | **Onconventioneel** | C1/C2-module, verplaatsbaar, labelt data voor goedkope sensoren (A2/A4) | ≤ 30 kV, vrijgesteld | 2 000 / 3 500 / 7 000 per module (1 per 20–50 containers) |
| A3-C5 | Pyro-röntgen op accu | Onconventioneel (speculatief) | pyro-elektrische bron + lijnarray, geen HV-voeding | juridisch onduidelijk | 2 500 / 4 000 / 7 000 |

---

## A3-C1 – Schaduwdoos (radicaal eenvoudig)
| Veld | Invulling |
|------|-----------|
| Sensor | Chinese vaste-anode mini-buis, hardwarematig begrensd op 30 kV, 1–4 W; GOS-versterkingsscherm 35×43 cm aan trommelwand; spiegel 45° + 12 MP camera (f/1,2); RPi 5 met klein CNN |
| Meetmoment | Per inworp, tijdens stilstand gesloten trommel: 3–10 s belichting (lange integratie compenseert lichtkoppeling ~10⁻³) |
| Drempel | Score per inworp: ≥ 1 opaak object met celvorm (cilinder 10–21 mm × 40–70 mm, knoopcel, pouch, celpakket) → "accu-inworp"; container-risico = Σ geschatte Wh sinds laatste lediging; alarm boven drempel A1 (bijv. ≥ 3 celobjecten of ≥ 50 Wh **[A]**) |
| Signaal | LTE-M bericht per inworp met thumbnail (alleen schaduwbeeld, geen persoonsgegevens); dashboard + push bij drempel |
| Verdienmodel | Abonnement per container EUR 35–60/mnd incl. hardware-lease **[A]** |
| Werking | Een 30 kV-bundel lichten de zak in de gesloten trommel door; organisch, papier, Al-blik en folie zijn (half)transparant, cellen zijn volledig zwart. Het CNN herkent vorm en telt cellen → Wh-schatting. Staal van de trommel (2–3 mm) is tegelijk de afscherming; interlock laat de buis alleen bij gesloten klep aan. |

## A3-C2 – Trommelscan
| Veld | Invulling |
|------|-----------|
| Sensor | 30 kV mini-buis met spleetcollimator (waaierbundel) + 64–128 CsI:Tl/Si-fotodiodekanalen (1,6–3 mm pitch) op de vaste zuilwand |
| Meetmoment | Per inworp tijdens de draaibeweging van de trommel (1–3 s) – de rotatie levert de tweede beeldas gratis; optioneel tweede waaier onder andere hoek → 2 projecties (minder overlap) |
| Drempel | Als C1; plus "hoog-Z oppervlak" ratio met dual-filter (Cu-gefilterde helft van de array) om laag-Z vs hoog-Z te scheiden |
| Signaal | Als C1 |
| Verdienmodel | Abonnement per container EUR 40–70/mnd **[A]** |
| Werking | Door de trommelrotatie schuift de zak langs een smalle waaierbundel; de lijnarray bouwt regel voor regel een beeld op met ~100× hogere detectorefficiëntie dan C1. Kleine collimeerde bundel = minder strooistraling = eenvoudiger ≤ 1 µSv/h. Twee projecties verminderen gemiste cellen door overlap. |

## A3-C3 – Typegoedgekeurde dual-energy zuil (prestatievariant)
| Veld | Invulling |
|------|-----------|
| Sensor | 60–80 kV monoblok 10–20 W, dual-energy sandwich-LDA (0,8 mm), 2–3 mm Pb-equivalent afscherming |
| Meetmoment | Per inworp, 1–5 s |
| Drempel | Classificatie Li-ion / alkaline / NiMH / lood via interne structuur + R-waarde; risicoscore met Wh en chemie |
| Signaal | Als C1 + chemie-label |
| Verdienmodel | Duurdere hotspot-dienst: milieustraten, winkelcentra, hoogbouw, overslagstation, AVI-bunkerinlaat; EUR 150–300/mnd per unit **[A]** |
| Werking | Hogere energie laat cellen deels door, waardoor spiraal-jelly-roll vs Zn-gel en celaantal in pakketten zichtbaar worden. Juridisch: eenmalige ANVS-typegoedkeuring (art. 3.18-1b "goedgekeurd type") maakt elke geïnstalleerde unit vrijgesteld; tot die tijd registratie. |

## A3-C4 – Röntgen-ijkpaal / "teacher-sensor" (onconventioneel)
| Veld | Invulling |
|------|-----------|
| Sensor | C1- of C2-module als demontabele inzet in een standaardzuil, plus de goedkope sensor(en) van A2 (inductie) en A4 (gas/thermisch) |
| Meetmoment | Per inworp, 1–3 maanden per locatie, dan doorschuiven |
| Drempel | Geen eigen alarm nodig; produceert gelabelde paren (röntgenbeeld ↔ inductie-/gassignaal) om de drempel en classifier van de goedkope sensor per gemeente te kalibreren; tijdelijk wél alarm op locatie |
| Signaal | Dataset + kalibratierapport per gemeente; vals-positief/negatief-cijfers van het goedkope systeem |
| Verdienmodel | Kalibratie-/nulmetingsdienst per gemeente (EUR 5–15 k per campagne **[A]**) bovenop het A2/A4-abonnement; ook "hotspotkaart" (waar zitten accu's in restafval) voor beleid/handhaving |
| Werking | Röntgen is de enige sensor die "ziet" wat er in de zak zit, maar is te duur voor elke container. Door een paar rouleerende units als waarheidsbron te gebruiken krijgt het goedkope systeem een gemeten recall/precisie en wordt het per regio bijgeleerd. Eén unit bedient 20–50 containers per jaar. |

## A3-C5 – Pyro-röntgen op accu (onconventioneel, speculatief)
| Veld | Invulling |
|------|-----------|
| Sensor | Pyro-elektrische röntgenbron (LiTaO₃-kristal, thermische cyclus, eindpunt ~35 keV) + lijnarray C2 |
| Meetmoment | Per inworp; bron "laadt" in 1–3 min, flitst tijdens stilstand |
| Drempel / signaal | Als C1 |
| Verdienmodel | Als C1, voor zuilen zonder netaansluiting |
| Werking | Geen hoogspanningsvoeding: een verwarmd/afgekoeld kristal versnelt elektronen naar een target. Mogelijk zeer laag stroomverbruik en intrinsiek "uit" bij storing. Flux, levensduur en juridische status (> 30 keV eindpunt, geen voedingsspanning) **niet geverifieerd**. |

## Afgewezen in R0 (ter info)
- Radioactieve bron (Am-241, Cs-137): vrijstellingsactiviteit fysisch nutteloos, sterker = vergunning + diefstalrisico in openbare ruimte → **KO**.
- Backscatter: ziet alleen buitenkant zak → cellen in de kern gemist.
- Enkele CdTe-spectroscoop: geen beeld.
