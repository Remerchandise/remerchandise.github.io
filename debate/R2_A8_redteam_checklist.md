# R2 – A8 Red-team-checklist

Elk concept op de shortlist moet deze checklist invullen (✔ / ✘ / ? + getal + bron). **KO** = knock-out: één ✘ = concept valt af of moet herontworpen worden. Onderbouwing: research/A8_redteam.md. **[A]** = aanname.

## A. Fysica en detectie

| # | Vraag | Norm | KO? |
|---|---|---|---|
| A1 | Hoe onderscheidt het concept een Li-cel van: Al-blikje, stalen conservenblik, kroonkurken, Al-folieprop, sleutelbos, Al-koffiecups? Toon gemeten/gesimuleerde signalen. | Specificiteit ≥ 95 % op zakken *mét* normaal metaal (≈ 85 % van zakken bevat metaal) | **KO** |
| A2 | Detecteert het een **vape met LiPo-pouch (0,5–1,5 Wh) in Al-behuizing**? Dat is de grootste Li-bron (≈ 7 mln/jr). | Recall vapes expliciet vermeld; "niet" mag, maar dan eerlijk in waardepropositie | Nee |
| A3 | Onderscheid alkaline AA/AAA (394 van 395 losse batterijen) vs. Li-ion? | Expliciet getal; zo niet: hoe telt alkaline mee in drempel | **KO** bij claim "Li-detectie" zonder dit |
| A4 | Wat gebeurt er bij afscherming (cel in metalen apparaat, cel tussen blikjes)? | Beschreven + effect op recall | Nee |
| A5 | Wordt Wh/aantal cellen geschat of alleen "aanwezig"? | Bij containermelding: rangorde/Wh verplicht (zie D1) | Nee |

## B. Base rate en alarmlast

| # | Vraag | Norm | KO? |
|---|---|---|---|
| B1 | Bereken PPV bij prevalentie 1 % / 2,2 % / 5 % Li-zakken met de opgegeven sens/spec. | PPV ≥ 50 % per gemeld item, óf meldingen alleen als geaggregeerde rangorde | **KO** |
| B2 | Aantal meldingen per wagen per dag bij realistische route (≈ 100–150 containers/dag **[A]**) | ≤ 2–3 actiegerichte meldingen/wagen/dag | **KO** |
| B3 | Hoe voorkom je alarm-moeheid (> 70 % onnodige alarmen = genegeerd; BMI-ervaring NL > 86–95 % loos)? | Verificatiestap of hoge drempel aantoonbaar | Nee |

## C. Omgeving en robuustheid

| # | Vraag | Norm | KO? |
|---|---|---|---|
| C1 | Werkt het met natte/lekkende zak, vet, ijzel, condens, −15…+60 °C (zon op deksel)? | IP67/IK10 of beargumenteerd | Nee |
| C2 | Wat bij overvolle trommel / geforceerde klep / zak blijft hangen? | Geen vals alarm; geen extra storing | Nee |
| C3 | Vandalisme en jaarwisseling (vuurwerk in trommel), schoppen, graffiti, diefstal | Geen bereikbare lens/antenne; vervangtijd ≤ 30 min | Nee |
| C4 | Verhoogt het concept het aantal storingen aan de zuil? (zuil = al hét storingspunt; Eindhoven ~1.000 meldingen/mnd) | MTBF-schatting; storing sensor ≠ storing toegang | **KO** als sensor de klep kan blokkeren |
| C5 | Energie & connectiviteit onder stalen deksel; levensduur batterij | ≥ 5 jr of netvoeding aanwezig; Dublin-les | Nee |
| C6 | Ontwijking: leidt het tot meer bijplaatsingen of accu's in pmd/gft? | Benoemd + mitigatie | Nee |

## D. Actie en waarde

| # | Vraag | Norm | KO? |
|---|---|---|---|
| D1 | Wat doet de ophaaldienst concreet met de melding (draaiboek)? "Container bevat waarschijnlijk accu" is bij ≈ 99 % van ledigingen waar. | Concreet draaiboek + kosten per actie (niet-persend legen, laatste in route, alert) | **KO** |
| D2 | Wie in de organisatie ontvangt het, binnen hoeveel tijd, in welk bestaand systeem? | Integratie met bestaand route/IoT-systeem; automatische push | Nee |
| D3 | Dominantietest vs. **thermische camera op de wagen** (EUR 3–8k per wagen, 1 wagen ≈ 100–150 containers) | Kosten per voorkomen brand lager óf aantoonbaar complementair | **KO** |
| D4 | Dominantietest vs. **accu-inzamelbus aan zuil / gedragsmaatregel** (A8-C1, A8-C3) | Concept voegt meetbaar iets toe | Nee |
| D5 | Welk deel van het risico (stap 5–7 in kickoff) wordt beïnvloed, en hoeveel branden/jr voorkomen per 1.000 containers? | Getal met bandbreedte, gekoppeld aan A1 | **KO** zonder getal |
| D6 | Business case: abonnement ≤ vermeden schade (A7) incl. kosten van vals alarm-acties | Terugverdientijd ≤ 3 jr **[A]** | **KO** |

## E. Juridisch, veiligheid, validatie

| # | Vraag | Norm | KO? |
|---|---|---|---|
| E1 | AVG: koppeling aan pas/adres? DPIA nodig? | Geen persoonsgegevens óf grondslag + DPIA | **KO** bij persoonsgerichte actie zonder grondslag |
| E2 | Straling (röntgen), EMC (inductie), vergunningen openbare ruimte | Vergunningsroute + doorlooptijd | **KO** voor röntgen zonder route |
| E3 | Kan het concept zelf brand/letsel veroorzaken (inzamelbus, hoogspanning, beknelling)? | Risicoanalyse | Nee |
| E4 | Hoe wordt recall/precisie in het veld gevalideerd (ground truth)? | Steekproef-sortering per cluster (A8-C3) of gelijkwaardig, n ≥ 30 containers | **KO** zonder validatieplan |
| E5 | Bestaande concurrenten (Seek Thermal/Goodyear, Republic/Oshkosh, WeSort.AI, Fraunhofer DangerSort, Lion Vision, inSystem.io, Sensoneo) benoemd en onderscheid duidelijk? | Ja | Nee |

## Scoring
- Elke KO ✘ → afvallen of herontwerp.
- Overige items: ✔ = 1, ? = 0,5, ✘ = 0; minimaal 70 % van de niet-KO-items om naar Ronde 4 te gaan.
