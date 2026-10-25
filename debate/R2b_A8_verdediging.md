# R2b – A8 verdediging / verbetering

Geen aanval noemde A8-concepten bij ID. Ik heb daarom de aanvallen op functioneel gelijke concepten op mijn concepten toegepast:
- A1-C5 en A6-C4 (sluis/sleuf) → A8-C1
- A7-C5 en A5-C4 (wagen) → A8-C2
- A5-C1 (pas-koppeling) → A8-C4

| Concept | Status | Motivatie (getal/bron) | Test Ronde 3 |
|---|---|---|---|
| **A8-C1 Accu-brievenbus aan de zuil** | **VERBETERD** | Nieuwe versie: brandwerende RVS-bus met vermiculietvulling en anti-hengelklep. **Geen** Wh-gewogen beloning en geen pas-koppeling; hooguit een vaste, anonieme buurtbeloning (A6-C5). Lediging via de Stibat/OPEN-keten. Overgenomen aanvallen: fraude met Wh-punten via inductie en weegcel (A2 over A1-C5), AVG door pas-punten (A6, Arnhem/AP 2017), brandhaard in de zuil (E3). Zonder beloning vervallen fraude en AVG. Het brandrisico in de bus is klein: < 1 kg cellen, ongeperst, in een stalen omhulsel. | (1) Effectmodel: Bebat-referentie ≈ 1 batterij per 100 kg na een breed netwerk (A6). Doorrekenen wat −10 %/jr Li-items in restafval doet met P_brand (A1-model). (2) Thermische test: één 18650 in thermal runaway in een gevulde bus. Blijft de buitenwand onder 100 °C? |
| **A8-C2 Detectie op de wagen (thermisch)** | **VERDEDIGD, rol aangescherpt** | A4 en A6 bevestigen: inductie op de wagen is KO, thermisch is "bewezen" (Seek/Goodyear, SWANA 2025). De kritiek van A4 dat het pas ná de crush ziet klopt. Thermal runaway volgt binnen seconden tot minuten, en het alarm geeft de chauffeur tijd om de lading te dumpen vóór een wagenbrand. Dat is precies de schade (wagen > EUR 300k, chauffeur) uit stap 5. Rol: **vangnet en D3-benchmark**, plus containerrisicokaart via GPS van de laatste lediging. | (1) Kosten per voorkomen wagenbrand: EUR 3–8k per wagen tegenover de schadeverdeling van A7. (2) Literatuur/leverancier: tijd tussen hotspot en open vuur in de laadbak, en het vals-alarmpercentage (nu onbekend). |
| **A8-C3 Steekproef-sorteerdienst + spiegelsticker** | **VERDEDIGD** | A6 (over A1-C6/A7-C4) en A4 (over A6-C1) stellen allebei voor om af te rekenen en te valideren op "batterijen/t in steekproefsortering". Dat ís dit concept. Branden zijn statistisch onbruikbaar: 1,6 per jaar per 1.000 containers. Een steekproef levert binnen één kwartaal ground truth op (Eureco: 351 analyses, 222 t). Sticker zonder pas = AVG-licht. | Poweranalyse: hoeveel steekproeven van 50–100 kg zijn nodig om per cluster een verschil van 2× in Li-items/t te zien (Poisson, ≈ 4,5 Li/t)? Kosten per cluster per jaar. |
| **A8-C4 Pasgekoppelde nudge** | **INGETROKKEN** | De aanval van A1 op A5-C1 telt hier ook: 73–91 % fout-positieven, en een huishouden met blikjes of alkaline wordt onterecht aangesproken. Mijn eigen KO E1/B1: zonder PPV ≥ 70 % is dit onverdedigbaar, en geen R1-sensor komt daar aantoonbaar in de buurt. Heropenen alleen als R3 voor grote packs (≥ 50 Wh) een PPV ≥ 70 % laat zien. | Geen eigen test. Volgt uit de ROC van A2-C3/A1-C2 voor grote packs. |

## Eindstand A8
Testen in R3: **A8-C1** (bus, als preventie-baseline), **A8-C2** (thermische wagencamera als dominantie-benchmark D3) en **A8-C3** (steekproef als ground truth en betaalproxy). A8-C4 is ingetrokken.
