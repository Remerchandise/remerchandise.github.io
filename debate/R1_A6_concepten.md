# R1 – A6 concepten (software, signaal, gedrag)

Agent 6 · 2026-10-25 · EUR 2026 excl. btw · aannames **[A]** · onderbouwing in `research/A6_software.md`

Uitgangspunt uit research: in 60–100 % van de ledigingen zit ≥ 1 Li-item (basis 2,4–3,6 per lediging). Daarom sturen de concepten op **risicorangorde** en **minder batterijen erin**, niet op "batterij ja/nee".

| ID | Naam | Sensor | Meetmoment | Drempel | Signaal | Verdienmodel | Ruwe kostprijs **[A]** | Label |
|----|------|--------|-----------|---------|---------|--------------|-----------------------|-------|
| A6-C1 | **Risicokaart zonder sensor** | geen; bestaande data (inworpen per pas/container, vulgraad, buurtkenmerken, kalender) | per lediging (voorspeld) | top-10 % risicoscore per route | vlag in routesoftware/boordcomputer | SaaS EUR 1–2/container/mnd | hardware EUR 0; integratie EUR 5–15k per gemeente eenmalig | **radicaal eenvoudig** |
| A6-C2 | **Bayes-hub (sensor-agnostisch)** | elke sensor (A2 inductie, A4 temp/gas) + C1-prior | per inworp + continu | P(≥ 1 Li >50 Wh) > 0,5 of R > θ₂ (rood); oranje ≤ 10 % ledigingen | event `batteryRisk` 0–3 op vulgraad-API → boordcomputer; webhook/dashboard | licentie EUR 2–4/container/mnd bovenop hardware | software; op edge < 1 kB RAM | kern-softwarelaag |
| A6-C3 | **"Pieptrommel" – directe feedback aan inwerper** | goedkope inductiespoel (A2) in trommel + LED/zoemer/e-ink | per inworp (3–10 s stilstand) | per-zak score > θ_feedback (ruim, mag FP) | lokaal: lampje "Batterij erin? Haal eruit – inleveren bij supermarkt"; geen melding aan ophaaldienst nodig | per container EUR 3/mnd of eenmalig | EUR 40–70 extra op zuil | **onconventioneel** (gedrag i.p.v. alarm) |
| A6-C4 | **Batterijsleuf in de zuil** | geen detectie; gewichts- of tellerschakelaar in Stibat-inzamelbuisje aan de zuil (+ QR naar inleverpunten) | continu (sleufgebruik) | buis ≥ 80 % vol → legen | vol-melding mee op vulgraad-bericht | co-financiering Stibat/St. OPEN (producentenverantwoordelijkheid) + gemeente | EUR 25–60 per zuil + lediging **[A]** | radicaal eenvoudig (preventie) |
| A6-C5 | **Buurtscore "batterijvrije wijk"** | aggregaten van C2/C3 per container (geen pas) | weekelijks | daling t.o.v. eigen baseline | maandelijkse buurtkaart/app/bord bij zuil; beloning (buurtpot, Stibat-actie) | onderdeel abonnement + communicatiebudget gemeente | software; bord EUR 100/locatie | onconventioneel (gamification, AVG-proof) |

## Werking

**A6-C1 Risicokaart zonder sensor (radicaal eenvoudig).** Een model schat per container de verwachte Li-last uit gegevens die er al zijn: aantal inworpen sinds lediging, buurttype, studentenhuizen/horeca (vapes), feestdagen (kerst/Sinterklaas = speelgoed, nieuwe telefoons), eerdere branden. De top-10 % containers per route krijgt "oranje": als laatste legen, niet extra persen. Kost niets aan hardware en levert een baseline waartegen elke sensor zich in Ronde 3 moet bewijzen (meerwaarde = verschil t.o.v. C1).

**A6-C2 Bayes-hub.** Elke inworp levert een likelihood-ratio per itemklasse (geen metaal … Li-groot); de hub telt log-odds op per container, vervalt bij lediging en fuseert met continue temp/gas-data. Uitvoer is één veld `batteryRisk` (0 groen – 3 zwart) op de bestaande vulgraad-API (HVC ContainerDevice/OAuth2-patroon), zodat AMCS/Bammens/PWS-boordcomputers het tonen zonder nieuw scherm. Payload 11 B past op LoRaWAN SF12 (51 B) of meeliften op de modem van de toegangszuil.

**A6-C3 Pieptrommel (onconventioneel).** Niet de ophaaldienst maar de inwerper is de actor: zij kan de zak nog terugtrekken. Een ruime drempel is hier geen probleem (een vals lampje kost niets), wat het blikjes-probleem van inductie omzeilt. Effect = gedragsverandering; meetbaar via daling van het aantal triggers per 100 inworpen (A/B tussen zuilen).

**A6-C4 Batterijsleuf.** Maak inleveren makkelijker dan weggooien: een afsluitbaar Stibat-buisje op de zuil op het moment dat men toch al afval brengt. Belgisch Bebat-voorbeeld: 1 batterij per 100 kg afval na jaren breed inzamelnetwerk. Combineert met C3 (lampje wijst naar de sleuf).

**A6-C5 Buurtscore.** Alleen container-aggregaten, nooit pas-ID → geen persoonsgegevens, geen DPIA-zwaarte. Buurten zien hun trend ("−30 % batterijsignalen deze maand") en verdienen een beloning. Werkt als communicatie-instrument voor gemeente en Taskforce-doel (−10 %/jr batterijen in restafval).

## Wat C1–C5 samen betekenen voor de shortlist
- C2 is de onvermijdelijke softwarelaag onder elk sensorconcept; C1 is de nul-meting.
- C3/C4/C5 verplaatsen waarde van "branden in de wagen voorkomen" (stap 5) naar "batterij niet in de zak" (stap 1) – de enige plek waar het risico echt verdwijnt.
