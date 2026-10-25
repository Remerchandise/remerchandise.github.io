# R1 – A8 (Red team): concepten

Uitgangspunt van het red team: de zuil-detector concurreert niet met "niets", maar met (a) een sensor op de **wagen** en (b) **zorgen dat de accu er niet in komt**. Deze concepten zijn bewust de "anti-producten" waartegen elk sensorconcept zich moet bewijzen. Prijspeil EUR 2026 excl. btw; **[A]** = aanname.

## A8-C1 – Accu-brievenbus aan de zuil  *(radicaal eenvoudig, anti-product)*

| Veld | Invulling |
|---|---|
| Sensor | Geen detectie van afval. Optioneel: 1 reed-/lichtsluis telt inworpen in de bus, vulgraad via gewicht |
| Meetmoment | Per inworp in de bus |
| Drempel | Bus ≥ 70 % vol of ≥ 2 kg → legen |
| Signaal | Bestaand IoT-vulgraadplatform; KCA-ploeg leegt bij melding of vaste frequentie (maandelijks) |
| Verdienmodel | Gemeente koopt/huurt bus; Stichting OPEN/producenten (UPV batterijen) vergoedt per ingezamelde kg; optioneel pas-beloning (gratis inworp/korting diftar) |
| Ruwe kostprijs | Bus RVS met vlamdovende vulling (vermiculiet), anti-hengel klep: EUR 150–250–400 **[A]**; montage EUR 75 |
| Werking | Een kleine, afsluitbare stalen inzamelbuis voor batterijen en vapes direct op de restafvalzuil, waar de burger tóch al staat. Niets te detecteren: je verlaagt de prevalentie bij de bron. Doel 10 %/jr minder batterijen in restafval sluit aan op Taskforce-ambitie. |

## A8-C2 – Detectie op de wagen, niet op de zuil  *(onconventioneel t.o.v. de brief: verplaats de sensor)*

| Veld | Invulling |
|---|---|
| Sensor | 1–2 thermische camera's (LWIR) + optioneel RGB-AI op de laadbak/stortkoker van de kraanwagen |
| Meetmoment | Elke lediging (container valt in laadbak) en continu tijdens persen |
| Drempel | Hotspot ≥ 60–90 °C of ΔT ≥ 30 K in ≤ 60 s **[A]**; AI-vlag "batterij/apparaat zichtbaar" |
| Signaal | Cabinealarm → pers stoppen, draaiboek "dumpplek"; GPS-tag van de laatst geleegde container → containerrisicokaart als bijproduct |
| Verdienmodel | Abonnement per wagen (EUR 100–200/mnd **[A]**) i.p.v. per zuil; data-laag per container als upsell |
| Ruwe kostprijs | EUR 3.000–5.000–8.000 per wagen **[A]** (Seek Thermal EFD-kit als referentie) |
| Werking | Eén sensor per wagen dekt ≈ 100–150 containers. Meet op het moment dat het brandmechanisme (persen) daadwerkelijk optreedt. De container-risicokaart ontstaat uit welke lediging een hotspot gaf – zonder één sensor in de openbare ruimte. Concurrent bestaat al (Goodyear/Seek, Republic/Oshkosh), dus voor ons eerder benchmark dan product. |

## A8-C3 – Steekproef-sorteerdienst + "spiegel"-sticker  *(radicaal eenvoudig, dienst i.p.v. apparaat)*

| Veld | Invulling |
|---|---|
| Sensor | Mens: kwartaalsteekproef 50–100 kg per containercluster, handmatig gesorteerd (accu's, vapes, Wh geschat) |
| Meetmoment | 4×/jr per cluster |
| Drempel | Cluster ≥ 2× gemeentelijk gemiddelde (bijv. ≥ 10 Li-items/t) → gerichte actie |
| Signaal | Rapport aan gemeente; QR-sticker op zuil "In deze buurt vonden we vorig kwartaal X vapes in het restafval – lever ze hier in: …" |
| Verdienmodel | Abonnement per gemeente (EUR 5–15k/jr **[A]**); optioneel gecombineerd met C1 |
| Ruwe kostprijs | ≈ EUR 150–300 per steekproef (2 personen × 2 h + afvoer) **[A]**; sticker EUR 5 |
| Werking | Levert de ground truth die elk sensorconcept nodig heeft (zonder dit kan niemand recall/precisie meten) en tegelijk lokale gedragsfeedback. Werkt in 1 week, zonder hardware, vandalismerisico of netwerk. |

## A8-C4 – Pasgekoppelde nudge na "grote-accu"-signaal  *(onconventioneel, hoog AVG-risico – bewust als stresstest)*

| Veld | Invulling |
|---|---|
| Sensor | Willekeurig zuil-sensorconcept (A2/A3) met hoge drempel: alleen groot pack (≥ 50 Wh of ≥ 300 g cellen) |
| Meetmoment | Per inworp, gekoppeld aan pasregistratie |
| Drempel | Zeer hoog (alleen e-bike/gereedschap/laptop), doel PPV ≥ 70 % |
| Signaal | Geen alarm naar ophaaldienst; brief/app-bericht aan pashouder-adres "mogelijk accu ingeworpen – hier kun je ze kwijt" |
| Verdienmodel | Gemeente (handhaving/communicatie-budget) |
| Ruwe kostprijs | Sensor-BOM + EUR 0,50–1 per bericht **[A]** |
| Werking | Ontwijkt het "ophaaldienst kan er niks mee"-probleem: het signaal stuurt gedrag van degene die het veroorzaakte. Vereist DPIA, grondslag (AVG art. 6) en een PPV die een onterechte brief zeldzaam maakt; bij PPV < 70 % is dit juridisch en reputationeel onverdedigbaar. |

## Samenvatting

| ID | Naam | Type | Kostprijs | Grootste zwakte |
|---|---|---|---|---|
| A8-C1 | Accu-brievenbus aan de zuil | Radicaal eenvoudig / anti-product | EUR 225–475 | Bus kan zelf branden/vandalisme; geen data over restafval |
| A8-C2 | Detectie op de wagen | Onconventioneel (sensor verplaatsen) | EUR 3–8k per wagen | Bestaat al; reactief (detecteert pas bij opwarming) |
| A8-C3 | Steekproef + spiegel-sticker | Radicaal eenvoudig / dienst | EUR 150–300 per steekproef | Arbeidsintensief, lage tijdsresolutie |
| A8-C4 | Pasgekoppelde nudge | Onconventioneel | sensor + EUR 1/bericht | AVG, vereist zeer hoge PPV |
