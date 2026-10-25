# R3 – A7 Business: resultaten FASE 1

Script: `python3 experiments/r3_business/business.py` (deterministisch, < 2 s). Output: `tables.md`, `results.json`, `fig_unit_economics.png`, `fig_business_case.png`. EUR 2026 excl. btw. **Status FASE 1: eigen BOM-schattingen en placeholder-recall** (A5-BOM en A6-MC nog niet aanwezig).

## Koppelpunten voor FASE 2 (parametrisering)
| Input | Bestand | Formaat | Effect |
|---|---|---|---|
| BOM A5 | `product/BOM_<ID>.csv` (ID = K1…K5, B1, B0) | kolommen `laag,basis,hoog` (of `prijs_laag`/`eur_basis`…), optioneel `aantal`; of een rij `totaal` | overschrijft `hw` (laag/basis/hoog) |
| MC A6 | `experiments/r3_classificatie/mc_results.json` (of `r3_business/mc_input.json`) | `{"K2": {"recall_energy":[l,b,h], "alarms_per_1000_emptyings":[l,b,h], "avoided_fire_fraction":[l,b,h]?, "fires_per_1000_containers_year":[l,b,h]?}}` | overschrijft recall, aantal meldingen, (optioneel) vermeden fractie en A1-brandfrequentie |
| Overige | `run(overrides={"K2": {...}, "cost_per_alarm": (..)})` | dict | gevoeligheidsanalyse |

## Test 1 – Unit economics en prijs (100 / 1.000 / 10.000 containers)
**Vraag:** wat kost het per container per maand, en tegen welke prijs moet het verkocht worden?
**Methode:** kostprijs = (hardware + installatie)/6 jaar + connectiviteit + cloud + onderhoud + support (platform + per eenheid) + CAC. Prijs = kostprijs bij 40 % brutomarge.

| EUR/container/mnd (basis [laag–hoog]) | 100 | 1.000 | 10.000 | Prijs bij 1.000 |
|---|---|---|---|---|
| K1 VLF-detector | 16,7 | 8,1 [4,7–13,2] | 5,4 | 13,6 |
| **K2 Pakketwachter (OEM)** | 10,8 | **5,1** [2,9–8,4] | **3,3** | 8,5 |
| K3a Röntgen vast | 50,6 | 35,9 [17–76] | 29,1 | 59,8 |
| K3b Röntgen rouleert (1 per 35) | 18,0 | 9,8 | 7,1 | 16,4 (≈ EUR 570 per unit/mnd) |
| K4 Deksel-event | 16,9 | 8,3 | 5,5 | 13,8 |
| K5 Hybride K2+K4 | 18,3 | 8,7 [5,2–13,9] | 5,7 | 14,5 |
| **B1 Thermisch laadbak** | 13,7 | **4,9** | **2,3** | 8,1 (≈ EUR 1.550–3.200 per wagen/mnd) |
| B0 Brievenbus + sortering | 29,8 | 16,7 | 11,7 | 27,8 |

**Conclusie:** behalve bij röntgen zijn support en CAC de grootste kostenpost, niet de hardware. Hardware is EUR 0,1–1,0 per maand, support + CAC EUR 3–5 per maand. Alleen OEM- of wagenzijdige routes komen onder EUR 5 per maand.

## Test 2 – Business case (klant met 1.000 containers, A1-brandkans)
**Aannames [A]:** branden 0,3 / 1,7 / 15 per 1.000 containerjaar (A1). Schade per incident: wagen 10k / 25k / 50k (params.ECON), verwerker 5k / 25k / 75k (verwachtingswaarde van een AVI-brand van EUR 1–5 mln), container 3k / 8k / 15k × 10–30 % dat in de container begint. Effectiviteit van de actie: wagen 0,3–0,7, verwerker 0,1–0,4. Kosten per melding EUR 10 / 40 / 150. Bruto schade basis ≈ **EUR 88 per container per jaar (EUR 7,3/mnd)**.

| Concept | Abonnement + acties (EUR/container/jr) | Vermeden laag / basis / hoog | Ratio basis | Benodigde branden per 1.000 cj voor ratio 1 |
|---|---|---|---|---|
| K1 | 246 | 0,1 / 7 / 390 | 0,03 | 56 |
| K2 | 133 | 0,3 / 13 / 634 | 0,10 | 17 |
| K3a | 730 | 0,6 / 24 / 878 | 0,03 | 52 |
| K3b | 209 | ~0 / 0,7 / 25 | 0,003 | 522 (waarde = ground truth, geen bescherming) |
| K4 | 168 | 0,1 / 10 / 492 | 0,06 | 27 |
| K5 | 205 | 0,4 / 19 / 806 | 0,09 | 18 |
| **B1** | **98** | 1,1 / **31** / 998 | **0,31** | **5** |
| B0 | 333 | 0,1 / 7 / 291 | 0,02 | 81 |

**Conclusie:**
1. **Geen enkel concept is rendabel in het basisscenario** (ratio ≤ 0,3). Alle concepten worden rendabel in het hoge A1-scenario (15 branden per 1.000 cj), behalve K3b.
2. **B1 domineert** (D3-test). K5 en K2 moeten 3–4× meer branden per 1.000 cj hebben dan B1 om quitte te spelen.
3. **De kosten van vervolgacties bij vals alarm zijn al hoger dan de vermeden schade** voor K1 (EUR 83/jr) en K2/K5 (EUR 31/jr) tegenover EUR 7–19 vermeden. A6 moet de meldingen terugbrengen naar ≤ 5 per 1.000 ledigingen, of oranje moet gratis zijn ("laatst in route").
4. Max. prijs die de vermeden schade dekt (zonder acties): K2 EUR 1,1, K5 EUR 1,6, B1 EUR 2,6 per container per maand. **Een prijs van EUR 1–2,5 per maand is het plafond op basis van schade.**

## Test 3 – Betalers
| Betaler | Aandeel baat (basis) | Beoordeling |
|---|---|---|
| Gemeente / eigenaar container | 0–8 % (alleen K4/K5 container-events) | Betaalt via afvalstoffenheffing, maar heeft nauwelijks eigen baat. Koopt alleen voor beleid/data (B0/K3b-kaart) of veiligheid |
| Inzamelaar (wagen + chauffeur) | 50–75 % | **Logische betaler voor B1 en K2/K5**; plus Arbo-argument (niet in euro's) |
| Verwerker / AVI | 25–48 % | Mede-betaler. Bij een overheids-NV die ook AVI is (HVC-model) valt de baat op één balans: 75–100 % |
| Verzekeraar | via verwerker/inzamelaar | Premiekorting als hefboom, geen financier (geen bron die betaling aantoont) |
| PRO (Stichting OPEN) | 0 % brandschade (OPEN, 28-10-2025) | Alleen co-financiering van data (B0/K3b), orde EUR 10–50k per jaar |

## Alleen met prototype/veld te bevestigen
- **Kosten van vervolgacties en echte meldingsdruk:** in een veldpilot (1 inzamelaar, 50–100 containers, 3 maanden) registreren per melding: actie (laatst in route / apart / niets), extra minuten en kilometers, en uitkomst (steekproefsortering als ground truth, A8 power-analyse).
- **Effectiviteit van de actie** (eff_truck): kan "niet persen / apart storten" een brand na crush echt voorkomen? Logboek van wagenincidenten bij de pilot-inzamelaar, vóór en na (alleen indicatief: Poisson-limiet, zie A6/A8).
- **Betaalbereidheid:** 5 gesprekken (HVC, ROVA, Cyclus, Renewi, een verzekeraar) met prijsvraag (Van Westendorp) voor B1 per wagen en K2 per container.
