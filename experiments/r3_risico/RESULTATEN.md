# R3 – A1 Risicomodel: resultaten

Scripts (vanuit repo-root, deterministisch, seed 20261025, < 2 s):
- `python3 experiments/r3_risico/risk.py`: module + zelftest. **A6 importeert `p_fire(items, k)`.**
- `python3 experiments/r3_risico/sim_drempel.py` → `fig_risico_vs_drempel.png`, `fig_pareto.png`, `fig_brandkans_container.png`, `resultaten.json`

Parameters: `experiments/common/params.py` (ITEMS, SCENARIOS, K_PER_WHEQ, 100 zakken per lediging, 52 ledigingen per jaar). Afwijkingen:
- params gebruikt knoopcel w_chem 0,3 (A1-R0: 0,5) en vape w_state 1,5. Ik volg params.
- params geeft **14,7 Wh-eq per lediging** (A1-R0: 22). Daarom bevat `risk.calibrated_k()` een k die precies de waargenomen brandfrequentie reproduceert: laag 4,2e-7 / basis 1,8e-6 / hoog 1,4e-5. Dat ligt dicht bij params-K.

## API `risk.py`

| Functie | Doel |
|---|---|
| `p_fire(items, k="basis")` | P_brand = 1 − exp(−k·ΣWh-eq). Invoer: `{klasse: n}`, een lijst van `"klasse"`, `("klasse", wh)` of `{"cls", "wh", "n"}`, of floats (Wh-eq). `k` = "laag"\|"basis"\|"hoog" of een getal |
| `p_fire_from_wheq(r, k)` | Gevectoriseerd (numpy) |
| `wheq(cls, wh=None)`, `p_item(cls)` | Per item |
| `expected_fires_per_1000(case)` | Branden per 1.000 containers per jaar, gekalibreerd op waarneming |
| `calibrated_k(case, scale)` | k passend bij de params-mix |

## Test 1 – Brandkans per container

**Vraag**: hoe groot is de brandkans per lediging en per 1.000 containers, en hoe verdeelt de risico-energie zich?

**Methode**: Monte-Carlo over 40.000 ledigingen per scenario. Li-items per zak worden Poisson getrokken volgens params. Wh per item komt uit een driehoeksverdeling (laag, basis, hoog). Daaruit volgen Wh-eq en P_brand.

| | Laag | Basis | Hoog |
|---|---|---|---|
| Wh-eq per lediging: gemiddeld / mediaan / p99 | 7,8 / 2,3 / 67 | 15,7 / 6,4 / 118 | 40 / 21 / 433 |
| Ledigingen met ≥ 1 Li-item | 77 % | **95 %** | 99,9 % |
| **Branden per 1.000 containers per jaar (gekalibreerd op NL-waarneming × onderregistratie)** | **0,32** | **1,4** | **10,8** |
| Idem, naïef (params-K × scenario; hoeken niet consistent) | 0,07 | 1,2 | 48 (stress) |
| P_brand bij 150 Wh-eq (k basis / hoog) | 2,3e-4 / 3,4e-3 | | |

De naïeve "hoog"-waarde combineert een hoge k met een hoog aantal items. Dat telt de onzekerheid dubbel, want k is gekalibreerd op het aantal items. Gebruik de **gekalibreerde rij** (aannames **[A]**: 2,9 Mt restafval, 0,5 t per lediging, 36/52/120 waargenomen branden, onderregistratie ×1/×3/×10).

**Pareto (basis, fig_pareto.png)**

| Klasse | Aandeel items | Aandeel Wh-eq |
|---|---|---|
| Knoopcel | 34 % | 1 % |
| Vape | 34 % | **21 %** (UK-tracker: 23 % van de incidenten) |
| Klein overig | 17 % | 2 % |
| 18650 / telefoon | 5 % / 5 % | 7 % / 10 % |
| Powerbank | 3,5 % | **22 %** |
| Laptop / gereedschap | 1,4 % | 14 % |
| E-bike / step | 0,3 % | **22 %** |

- Powerbank en groter: **5 % van de items, 58 % van het risico**.
- Items ≥ 50 Wh-eq: **1,4 % van de items, 33 % van het risico**.
- Top 10 % van de items: 68 % van het risico.

## Test 2 – Gevoeligheid van de drempels (bovengrens)

**Vraag**: welke energiegewogen recall is haalbaar per aantal meldingen, met een perfecte Li-sensor en met een fout in de Wh-schatting?

**Methode**:
- Elk Li-item krijgt een geschatte Wh-eq = waar × LN(0, σ), met σ = 0 / 0,3 / 0,5 / 1,0.
- Clutter (alkaline, blik) zit er **niet** in; dat is de bovengrens. De werkelijke vals-alarmlast komt uit de MC van A6 met de sensormodellen van A2/A3.
- Melding per inworp bij geschatte Wh-eq ≥ T, of per container bij ΣWh-eq ≥ T.
- Meldingen per wagen per dag = meldingen per 1.000 ledigingen × 0,125 (125 containers per route per dag **[A]**).

**Resultaat (basis, fig_risico_vs_drempel.png)**

| Drempel | σ = 0: recall / meldingen per 1.000 / per wagen per dag | σ = 0,5 | σ = 1,0 |
|---|---|---|---|
| Inworp ≥ 10 Wh-eq | 66 % / 258 / 32 | 66 % / 297 | 66 % / 412 |
| Inworp ≥ 50 Wh-eq | **33 % / 40 / 5** | 36 % / 55 | 38 % / 84 |
| Inworp ≥ 75 Wh-eq | **22 % / 10 / 1,3** | 27 % / 27 | 32 % / 55 |
| Container ≥ 50 Wh-eq | 45 % / 63 / 8 | 46 % / 73 | 49 % / 103 |
| Container ≥ 150 Wh-eq | **23 % / 9 / 1,2** | 23 % / 11 | 27 % / 27 |

Laag- en hoogscenario: zie `resultaten.json`. Inworp ≥ 50 Wh-eq bij σ = 0 geeft 19,7 meldingen per 1.000 (laag) en 102 per 1.000 (hoog). Container ≥ 150 geeft 4,4 (laag) en 27 (hoog).

**Conclusies**
1. **Plafond**: met ≤ 2–3 meldingen per wagen per dag (checklist B2, ≈ ≤ 20 per 1.000 ledigingen) haalt zelfs een **perfecte** sensor maar **~22–30 % energiegewogen recall**. Dat is grotendeels e-bike, step en grote packs.
2. Een fout in de Wh-schatting kost weinig recall, maar **verdubbelt tot verviervoudigt de alarmlast** bij hoge drempels (σ = 1: ×5 bij T = 75). **Eis aan de sensor: σ_log(Wh) ≤ 0,5.**
3. Een drempel per inworp ≥ 50 Wh-eq (pakketklasse) is net zo efficiënt als de containerdrempel en makkelijker uit te leggen. **Aanpassing van de drempels uit R0**:
   - **Oranje** = inworp ≥ 50 Wh-eq of container ≥ 75. Als rangorde: top ~5 % per route.
   - **Rood** = inworp ≥ 75–100 Wh-eq, container ≥ 150, of een A4-event. Dat geeft ~1 per wagen per dag.
   - Groen onder 50 Wh-eq per inworp. Vapes en knoopcellen (35 % van het risico) zijn met een sensor bij de inworp **niet economisch te alarmeren**: daar zijn prevalentiemaatregelen nodig (B0).
4. **Vermeden branden** = gekalibreerde branden × recall × effectiviteit van de actie **[A]** (0,3 / 0,5 / 0,8):
   - laag: 0,32 × 0,22 × 0,3 ≈ **0,02**
   - basis: 1,4 × 0,28 × 0,5 ≈ **0,2**
   - hoog: 10,8 × 0,35 × 0,8 ≈ **3,0** per 1.000 containers per jaar
   - Bij EUR 10k / 25k / 50k per incident (params.ECON) is dat ≈ **EUR 0,02 / 0,4 / 12,5 per container per maand** vermeden schade, voor een perfecte sensor. Dit is input voor A7: het basisscenario is ~7× lager dan de bruto EUR 3/maand.

## Alleen met prototype of veldwerk te bevestigen

| Parameter | Waarom kritisch | Labtestontwerp |
|---|---|---|
| p(TR en ontsteking \| pers) per klasse en SOC (bepaalt k bottom-up; nu 2–4 ordes verschil met de waarneming) | Bepaalt de absolute brandkans en de weging van vapes | **Opstelling**: hydraulische pers 20–40 kN met stalen plaat (pers van een vuilniswagen nabootsen) in een brandcel met afzuiging, thermokoppels en IR-camera. **Objecten**: vape (13400/pouch), 18650, telefoon-pouch, powerbank, laptoppack, elk ingebed in 20 kg synthetisch restafval (droog/nat). **Protocol**: SOC 0 / 25 / 50 / 100 %, n = 20 per combinatie (~400 tests). Uitkomsten: TR ja/nee, T_max, ontsteking van de omgeving binnen 30 min. Logistische regressie p(ontsteking \| Wh, SOC, vocht) |
| Li-items per ton en de mix (bepaalt de verdeling van de Wh-eq) | Grootste onzekerheid; de OPEN-pdf (hoofdstuk 1.4) was niet leesbaar | Sorteeranalyse (Eureco-methode) van 30 containerledigingen (~15 t) met registratie van klasse, chemie, Wh van het etiket en SOC (spanningsmeting). Voor ±20 % op Li per ton bij ~6/t zijn ~100 Li-items nodig, dus ≥ 15 t |
| Onderregistratie van wagenbranden | Bepaalt het niveau van k | Logboekonderzoek bij 3–5 inzamelaars (incidenten inclusief "zelf geblust"), 12 maanden |
| Effectiviteit van de actie (laatst in de route, niet persen) | Lineair in de vermeden schade | Niet in het lab te bepalen. Expertsessie met chauffeurs en de veldpilot (A8) |
