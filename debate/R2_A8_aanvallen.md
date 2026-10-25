# R2a – A8 Red team: aanvallen

Toetsing tegen `R2_A8_redteam_checklist.md`. Basisgetallen: losse batterijen 28/t, waarvan ≈ 97 m% alkaline en losse Li-ion ≈ 1 op 395 **[V]**; vapes ≈ 2,3/t; ≈ 85 % van de zakken bevat metaal **[A]**; ≈ 3,6 Li-items per lediging; P_brand ≈ 3e-5 per lediging → ≈ 1,7 brand/jr per 1.000 containers (A1); vermeden schade ≈ EUR 3 per container per maand, waarvan > 85 % bij de verwerker (A7).

## 1. Sneltoets alle concepten A1–A7

| ID | Zwaarste faalwijze | Checkpunt | KO? |
|---|---|---|---|
| A1-C1 Teller-met-basislijn | Basislijn middelt ook échte accu's weg. Een uitschieter (feestdag, verhuizing) ≠ accu | B1, D1 | Nee (alleen als trend-tool) |
| A1-C2 Pareto-detector ≥ 20 Wh | Laptop/gereedschapspack ≈ pan, conservenblikstapel, fietsslot qua inductiemassa | A1 | **?** – hangt af van A2-meting |
| A1-C3 Pers-advies wagen | Geen eigen sensor; erft alle zwakte van upstream. CAN-interlock = typekeuring wagen | D3 | Nee |
| A1-C4 Steekproef-risicokaart | Geen real-time; waarde = beleid | — | Nee |
| A1-C5 Accu-sluis met beloning | Fraude met punten (oude batterijen hamsteren), brand in sluis | E3 | Nee |
| A1-C6 Verzekeringsindex | ≈ 1,7 brand/jr per 1.000 containers → index statistisch leeg | D5 | Nee (pas op schaal ≥ 50k containers) |
| A2-C1 VLF-strandmetaaldetector | Alkaline (≈ 394:1) en blik als "ferro-verdacht" | A1, A3, B1 | **Ja** |
| A2-C2 PI-klikker | Zegt alleen "metaal" → ≈ 85 % van de inworpen | B1, B2 | **Ja** als alarm. Nee als proxy |
| A2-C3 Rol-spectroscoop (MPT) | Overlap van objecten in één zak; bibliotheek ≠ veld | A1, A4 | ? (R3) |
| A2-C4 Magnetisatiepuls | Hypothese onbewezen; 10–50 mT door RVS-trommel | A1 | ? (R3) |
| A2-C5 Valkoker-tunnel | Inbouw in schacht per type container; vuil, natte zakken | C1, C4 | Nee |
| A3-C1/C2 30 kV-röntgen | Kosten EUR 2–3k per zuil; 1 µSv/h aantonen in vandalismeomgeving; publieke perceptie "röntgen op straat" | D6, E2 | **Ja** (kostprijs vs. EUR 3/mnd) |
| A3-C3 Dual-energy 60–80 kV | Als boven, ×4 | D6, E2 | **Ja** |
| A3-C4 Röntgen-ijkpaal | Geen; dit ís het validatie-instrument | E4 | **Nee – sterk** |
| A3-C5 Pyro-röntgen | Flux en juridische status onbekend | E2 | **Ja** (te speculatief) |
| A4-C1 Thermo-deksel | Detecteert brand, voorspelt niets; Sensoneo heeft het al | E5 | Nee |
| A4-C2 Snuffelneus | Rottingsgas, zomer; alleen bovenste ≈ 0,3 m | B3 | Nee |
| A4-C3 Waakstand na trigger | Trigger komt van A2 (≈ 85 % van de zakken) → altijd waakstand | B2 | Nee als prior zwak gewogen |
| A4-C4 Luister naar de plop | Demping door afval, verkeer, inworp zelf | A4 | ? (R3) |
| A4-C5 Vape-neus | Dichtgeknoopte zak; geur van andere zakken blijft in de trommel hangen | A2, C2 | ? (R3) – enige vape-kandidaat |
| A4-C6 Hotspot-kaart IR | Lens vuil/condens; alleen bovenste laag | C1 | Nee |
| A4-C7 Smeltdraad | Alleen late branddetectie; wel robuust | — | Nee |
| A5-C1 OEM-insteekmodule | Afhankelijk van zuil-OEM | zie §3 | Nee |
| A5-C2 Puck | Li-SOCl₂-cel in trommel, slijtage, vandalisme | C3, E3 | Nee |
| A5-C3 Deksel-sentinel | Overlapt met A4/Sensoneo | E5 | Nee |
| A5-C4 Laadbak-ring | 0,6–1 t metaalrijk afval in 0,3 s door ring in stalen wagen | A1 | **Ja** (inductief). Thermisch: nee |
| A5-C5 Trommel-oogster | Motor-/veertrommels; oogst bij zwakke duw | C5 | Nee |
| A6-C1 Risicokaart zonder sensor | Geen ground truth om te trainen | E4 | Nee – nulmeting |
| A6-C2 Bayes-hub | Garbage in, garbage out | — | Nee |
| A6-C3 Pieptrommel | Piept bij ≈ 85 % van de inworpen → binnen weken genegeerd | B3 | **Ja** bij inductie-trigger |
| A6-C4 Batterijsleuf | Brand/vandalisme in sleuf | E3 | Nee |
| A6-C5 Buurtscore | Meet sensorruis, niet gedrag | E4 | Nee mits gevalideerd |
| A7-C1 Meelifter zuil | Marge, kanaalmacht | zie §4 | Nee |
| A7-C2 Roulerende kaart | Weinig waarde zonder vervolgactie | D4 | Nee |
| A7-C3 EPR-bounty | OPEN wijst schade-verantwoordelijkheid af | zie §4 | ? |
| A7-C4 Shared savings | Attributie onmogelijk | D5 | **Ja** |
| A7-C5 Detector op wagen | Inductief: zie A5-C4; thermisch: concurrent bestaat | D3 | Nee (thermisch) |
| A7-C6 Bundel vulgraad + brand | Geen onderscheid t.o.v. Sensoneo | E5 | Nee, maar geen moat |

## 2. Aanval A2 – strandmetaaldetector-route

1. **Base rate vernietigt het signaal (ernst: KO).** Een stalen celhuls is precies wat AA/AAA-alkaline ook heeft. Per ton restafval zitten ≈ 27 alkaline-cellen tegenover ≈ 0,07 losse Li-ion en ≈ 2,3 vapes. Zelfs een perfecte "cilindrische stalen cel"-detector meldt dus vooral alkaline. Daarbij komen ≈ 300 g metaal per zak (blik, kroonkurk, folie). De PPV voor "Li-item in zak" is 9–27 %, zelfs bij spec 80–95 %.
2. **De grootste Li-bron is inductief bijna onzichtbaar (ernst: hoog).** Een vape bevat een LiPo-pouch van 0,5–1,5 Wh in Al-laminaat en een Al-buisje. Dat lijkt inductief op een opgerolde folie of een blikje. A2 zegt dit zelf ("pouch ↔ sleutelbos/blikje").
3. **Geometrie (ernst: middel).** Een RVS-trommel van 2–3 mm dempt VLF. Een meedraaiende DD-spoel vraagt om een sleepring of kabel die bij elke inworp buigt, en ≈ 10⁵ cycli per jaar breekt kabels.
4. **Een hobbydetector (A2-C1 €165+) heeft geen data-uitgang.** Daarmee valt de letterlijke opdrachtgevershypothese af.

**Wat het zou redden:** inductie alléén als *Wh-klasse-detector voor grote packs* (A1-C2-logica: 9 % van de items, 59 % van de risico-energie) en als goedkope proxy, nooit als "Li-ion ja/nee". Bewijs in R3: ROC-curve op een mengsel van 18650/laptoppack, AA-batterijen, blikjes en folie in een echte RVS-trommel, plus kalibratie via A3-C4.

## 3. Aanval A5 – hardware

1. **A5-C2-puck (ernst: middel–hoog).** Een LS33600 Li-SOCl₂-cel in de trommel betekent een brandbare cel in een brandsensor, op de plek die elke zak raakt (vet, glas, vloeistof). Dublin 2023 faalde op behuizing en batterijduur. De vervangtijd en het vandalismeprofiel (jaarwisseling: > 2/3 van de kleine brandjes in Scheveningen zijn containerbranden) ontbreken.
2. **A5-C1/A7-C1 OEM-route (ernst: strategisch).** Het kanaal is sterk, maar de OEM (Bammens, Sidcon) heeft geen reden om onze IP te licentiëren als een spoel en firmware EUR 15–30 kosten: zij bouwen het zelf. Daar komt bij dat een sensorstoring de klep niet mag blokkeren (C4-KO). Dat moet de OEM certificeren.
3. **A5-C4 laadbak-ring (ernst: KO voor inductie).** 0,6–1 t afval met ≈ 40–60 kg metaal valt in 0,3 s door een ring in een stalen opbouw. Het signaal is altijd verzadigd en elke lediging scoort "metaal". De positie op de wagen is wél goed. Gebruik daar een thermische camera (Seek/Goodyear, kit ≈ EUR 3–8k **[A]**), die al bestaat.
4. **A5-C5 oogster (ernst: laag).** Elegant, maar vul aan met het aandeel motor-/veertrommels in NL en de LoRa-dekking onder een stalen deksel.

**Wat het zou redden:** één hardware-architectuur kiezen die de zuil niet kan laten falen (fail-open), netvoeding/accu van de zuil gebruikt, en geen eigen Li-cel in de trommel heeft. A5-C5 is dan een interessante variant.

## 4. Aanval A7 – verdienmodel

1. **A7-C1 (ernst: hoog).** Een prijs van EUR 2–4 per container per maand tegenover EUR 3 vermeden schade geeft een ROI van ≈ 1, *vóór* de kosten van vervolgacties op valse alarmen (extra lediging EUR 80–250 **[A]**). En de gemeente betaalt terwijl > 85 % van de baat bij de verwerker valt: dat is een split incentive.
2. **A7-C3 EPR-bounty (ernst: hoog).** Stichting OPEN publiceerde op 28-10-2025 "schade batterijbranden is niet voor rekening producent". Data over het lek naar restafval kopen kan, maar het wordt dan een onderzoeksbudget (sorteeranalyses doen ze al via Eureco, EUR 10–50k/jr **[A]**) en geen schaalbaar abonnement. Bovendien is ≈ 50–90 % van de vapes illegaal, dus er is geen producent die betaalt.
3. **A7-C4 shared savings (ernst: KO).** Een gemeente met 1.000 containers heeft ≈ 1,7 branden per jaar (0,3–15). Een basislijn van 3 jaar is ≈ 5 branden. Een daling van 30 % aantonen (Poisson, α = 0,05, power 0,8) vraagt orde ≥ 50–100 branden per arm, dus ≥ 30.000 containerjaren. Geen enkele klant kan de uitkomst meten, dus het wordt ruzie over attributie.
4. **A7-C6 (ernst: middel).** Sensoneo heeft vulgraad + temperatuur + kantelalarm al commercieel. De brand-upsell is daardoor commodity.

**Wat het zou redden:** de betaler wordt de verwerker/inzamelaar (HVC-achtig), met prijs per wagen of per gemeente in plaats van per container (A7-C2, A7-C5), en waarde gemeten op proxies (aantal hotspots, aantal batterijen/t via steekproef) in plaats van op branden.

## 5. Wat overeind staat (A8-oordeel)
- **Sterk:** A3-C4 (ijkpaal/ground truth), A6-C1 (nulmeting), A7-C2/A1-C4 (roulerende kaart), A7-C5/A1-C3 in thermische variant (wagenzijdig = waar stap 5 plaatsvindt), A6-C4/A1-C5/A8-C1 (inzamelsleuf = prevalentie omlaag).
- **Voorwaardelijk (R3 moet bewijzen):** A1-C2 + A2-C3 als grote-pack-detector, A4-C5 vape-neus, A4-C4 plop, A4-C2/A4-C3 als bevestiging.
- **Af:** A2-C1, A2-C2 als alarm, A3-C1/C2/C3/C5 als vaste zuilsensor, A5-C4 inductief, A6-C3 met inductie-trigger, A7-C4.
