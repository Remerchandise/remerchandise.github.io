# A8 – Resultaten Ronde 3 (red team)

Script: `python3 experiments/r3_redteam/power_analyse.py` (seed 8, < 10 s). Uitvoer: `results.json`, `fig_power_veldtest.png`, `fig_power_cluster.png`, `fig_power_brand.png`. Labtestontwerpen: `labtests.md`.

## T1 – Veldtest-omvang (recall ± 10 %)
- **Vraag:** hoeveel zakken moeten gesorteerd worden om de recall te meten?
- **Methode:** prevalentie per zak uit `params.ITEMS` (Poisson), normaalbenadering n_pos = z²·R(1−R)/h², gecontroleerd met simulatie (halve breedte 0,103 bij n = 62).
- **Aannames:** 5 kg per zak **[A]**, recall 0,8.
- **Resultaat (laag/basis/hoog):** alle Li 21/11/4 t; Li ≥ 10 Wh-eq 207/104/41 t; ≥ 50 Wh-eq 6.200/3.100/1.240 t.
- **Conclusie:** recall op hoge-energie-items kan alleen met **spiking** worden gemeten (62 positieven per klasse). Natuurlijke zakken dienen voor de vals-alarmlast. Dit is **alleen met prototype te bevestigen** → L1 en L5.

## T2 – Specificiteitseis voor de pakketwachter (K2)
- **Resultaat:** voor PPV ≥ 50 % op klasse ≥ 20 Wh-eq (prevalentie 0,15 % per zak) mag het vals-positief per zak hooguit **0,075–0,12 %** zijn (recall 0,5–0,8).
- **Conclusie:** pannen en gereedschap (≈ 2 % van de zakken) moeten voor ≥ 94 % als "geen pakket" worden herkend. Dat is het harde slaag/zak-criterium van L1, Protocol B. NB: in params valt alleen e-bike/step boven 50 Wh-eq (laptop 48), dus de klassegrens 50 is praktisch "alleen e-bike". Ik adviseer A1/A6 om 20 Wh-eq als pakketgrens te overwegen.

## T3 – Steekproef per cluster (B0)
- **Resultaat:** voor een 2× verschil in Li/t (power 0,8) is **8/4/1,5 t per cluster** nodig (laag/basis/hoog). Met de proxy "alle batterijen" (36/t) is dat ≈ 1 t.
- **Conclusie:** zelfcorrectie op A8-C3. Rapporteren op alle batterijen/t, ≥ 1 t per cluster per jaar.

## T4 – Branden als uitkomstmaat
- **Resultaat:** een brandreductie van 30 % aantonen vergt **412k/96k/41k containerjaren per arm**; voor 50 %: 135k/31k/13k.
- **Conclusie:** op branden afrekenen kan niet. Elke pilot of contract moet op proxies worden afgerekend.

## T5 – Labtests (alleen met prototype)
L1 inductie in een RVS-trommel (n ≥ 50 per klasse, 200 realistische zakken), L2 röntgen-dosimetrie (ionisatiekamer, ≤ 0,5 µSv/h, foutinjectie), L3 vape-neus (n ≥ 30 per conditie, 8 stoorbronnen), L4 drukpuls in een brandbunker op 0,2/0,5/1,0 m, L5 veldtest met 3 zuilen, spiking met RFID en ongeperst sorteren. Zie `labtests.md`.

## Voorbereiding red-team-toets Ronde 4: harde getallen die ik nodig heb

| Van | Getal (laag/basis/hoog) | Checklistpunt |
|---|---|---|
| A2 | ROC per klasse: specificiteit bij recall 0,8 voor 18650 tegenover AA + blik (K1) en voor ≥ 20 Wh-eq tegenover pan/gereedschap (K2); positie-afhankelijkheid | A1, A3, A4 |
| A3 | Lekstraling bij max instelling + 1 fout; kostprijs K3b per gemeente | E2, D6 |
| A4 | Vals alarm per containerjaar (K4); detectietijd B1 tot open vuur; P(vlag 'niet legen' terecht) | B3, D3 |
| A5 | MTBF, fail-open van de klep, vervangtijd, energie per dag, BOM K2/K5/B1 | C4, C5 |
| A6 | PPV per melding, **meldingen per wagen per dag**, energiegewogen recall, vermeden branden per 1.000 containers, voor K1–K5, B0 en B1 | B1, B2, D5 |
| A7 | Kosten per vermeden brand: K5 tegenover B1 tegenover B0; terugverdientijd voor de betaler die de baat heeft; kosten van een vervolgactie per vals alarm meegerekend | D3, D4, D6 |
| A1 | Aandeel risico-energie ≥ 20 Wh-eq en de vapebijdrage (die inductie mist) | A2, D5 |
