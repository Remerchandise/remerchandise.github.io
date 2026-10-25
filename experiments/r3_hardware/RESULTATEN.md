# R3 – A5 Hardware: resultaten

Script: `python3 experiments/r3_hardware/bom_energie.py`. Het script is deterministisch en heeft geen random. Uitvoer:
- `product/BOM_{K1,K2,K3a,K3b,K4,K5,B1,B0}.csv`
- `product/BOM_samenvatting.csv`
- `experiments/r3_hardware/energie_tabel.csv` en `fig_energie.png`
- `product/blokschema.png` en `product/montage.png`

Alle bedragen in EUR 2026 excl. btw, @1 000 st. Aannames **[A]**.

## Formaat van de BOM-CSV (voor A7)
Kolommen: `concept, post, categorie, laag, basis, hoog, bron_aanname`. De categorieën zijn:
- `hw`: per unit
- `installatie`: per unit
- `eenmalig`: programma, door A7 te spreiden
- `per_maand`, `per_jaar`: per unit
- `dekking`: containers per unit
- `optie_hw`: niet in het totaal

Onderaan elk bestand staan de regels `TOTAAL_*`. In `BOM_samenvatting.csv` staat `tco_per_container_per_maand` = (hw + installatie + 10 j × run) / dekking / 120. Daarin zitten **geen** eenmalige kosten en **geen** marge.

## Test 1 – BOM per concept

| Concept | HW/unit l/b/h | Install. basis | Eenmalig basis | Run basis | Dekking | TCO/container/mnd l/b/h |
|---|---|---|---|---|---|---|
| K1 VLF standalone | 91 / 137 / 223 | 60 | 30k | 0,5/mnd + 6/j | 1 | 1,44 / **2,64** / 5,11 |
| K2 pakketwachter OEM | 54 / 91 / 160 | 45 | 100k (EMC + NRE) | 0,2/mnd + 2/j | 1 | 0,83 / **1,50** / 2,79 |
| K3a röntgen vast | 860 / 1 785 / 3 675 | 650 | 80k | 2/mnd + 220/j | 1 | 21,5 / **40,6** / 77,1 |
| K3b röntgen-ijkpaal | idem | 650 | 80k | + verhuizing 3,6k/j | 20–50 | 2,4 / **9,7** / 33,9 |
| K4 deksel-event | 70 / 103 / 158 | 30 | 25k | 0,8/mnd + 7/j | 1 | 1,38 / **2,49** / 4,23 |
| K5 = K2 + K4-lite | 120 / 188 / 304 | 75 | 150k | 0,2/mnd + 9/j | 1 | 1,88 / **3,14** / 5,41 |
| B1 thermische camera wagen | 700 / 2 050 / 4 800 | 600 | 15k | 10/mnd + 200/j | 200–500 | 0,04 / **0,16** / 0,52 |
| B0 accu-brievenbus | 25 / 40 / 60 | 40 | – | 25/j lediging | 1 | 1,21 / **2,75** / 5,17 |

**Conclusies**
- Alleen **K2** blijft per container onder de ~EUR 3/mnd vermeden schade (A7), met marge voor eenmalige kosten, OEM-marge en support.
- K5 en K1 zitten er net boven, K3a ligt er een factor 10 boven.
- **B1 is per container 10–20× goedkoper** dan elk zuilconcept. De zuilconcepten moeten dus een ander voordeel hebben dan kosten: vroege rangorde vóór lediging, en gedrag.
- De kostendrijvers van K1, K2 en K5 zijn de **PE-liner (15–60)** en de **flexkabel**, niet de elektronica.

## Test 2 – Energiebudget vs. off-grid capaciteit

Model: mWh/dag = n × E_inworp + E_vast (slaap, continu, communicatie).

| Concept | E_inworp mWh l/b/h | E_vast mWh/dag l/b/h | mWh/dag basis @30/80/150 | Jaar op 1× LS33600 (43 Wh) basis | Voeding |
|---|---|---|---|---|---|
| K1 | 0,04/0,08/0,15 | 2,4/6,3/14,3 | 8,7 / 12,7 / 18,3 | 13,5 / 9,3 / 6,4 | LS33600 OK (≥ 5 j, ook bij hoog) |
| K2 | 0,06/0,16/0,30 | 0,5/1,5/4,0 | 6,3 / 14,3 / 25,5 | (standalone-optie 18,7 / 8,2 / 4,6) | Pas-zuil-accu: < 1–5 % extra last **[A]** |
| K3a | 20/36/70 | 24/72/240 | 1 152 / 2 952 / 5 472 | < 0,1 | 20–50 Wp paneel + 200 Wh LiFePO4 (verwarmd) of net. 5 Wp in december ≈ 0,75 Wh/dag: te weinig |
| K4 | – | 6/12/25 | 12 (onafhankelijk van n) | 9,8 (5–20 j) | LS33600 OK |
| K5 | zuildeel = K2 | containerdeel 5/10/21 | 10 | 11,8 | zuil-accu + LS33600 op de container |
| B1 | – | 120–150 Wh/dag | – | – | 24 V boordnet, niet beperkend |

Uitgangspunten **[A]**:
- PI met 2 lussen ~100 mW gedurende 2–10 s (afgeleid uit A2-R0). VLF 40 mW + MCU 15 mW.
- Slaap 5–50 µA. LTE-M 1 mWh per bericht; NB-IoT onder het deksel 3–10 mWh.
- IR 8×8: 15 mW × 10–15 s per 10 min. CO-bias ~10 µA.
- Röntgen 0,03 Wh/inworp (A3) + compute 2 W × 10 s; standby 1–10 mW.

Figuur `fig_energie.png`.

**Conclusies**
- Alle inductieve en thermische concepten zitten op 6–40 mWh/dag. Dat past ruim binnen één D-cel voor ≥ 5 jaar (de bestekeis), of verwaarloosbaar op de pas-zuil-accu.
- Röntgen zit **100–400× hoger**. Off-grid in december is dat niet te doen zonder groot paneel en accu, en dat zou uitgangspunt 1 ("langer meten") ook nog duurder maken.
- Langer meten (5 → 10 s) verdubbelt de inductie-energie, maar die blijft dan nog < 40 mWh/dag. **Uitgangspunt 1 is energetisch gratis voor inductie** en duur voor röntgen.

**Alleen met een prototype te bevestigen**
- Werkelijke slaapstroom van de hele module, inclusief lekstroom van de potting bij 100 % RV.
- Piekstroom PI-lussen vs. passivatie van de Li-SOCl₂-cel bij −10 °C.
- Restcapaciteit van de pas-zuil-accu in de winter (opvragen bij de OEM).
- BLE-link van container naar zuil door valschacht en stalen platform (RSSI-meting).

Labtest:
- **Opstelling:** module + 2 lussen in een echte 60 L RVS-trommel in een klimaatkast (−20/+25/+60 °C).
- **Meetprotocol:** Otii/Joulescope; 1 000 inworp-cycli; 72 h slaap.
- **Criteria:** slaap ≤ 20 µA; ≤ 0,3 mWh per inworp; geen brown-out bij −20 °C.
- **BLE:** 3 locaties met verschillende platformtypes, 2 weken, ≥ 99 % pakketontvangst.

## Test 3 – Productontwerp K2/K5
Zie `product/ontwerp.md`, `product/blokschema.png` en `product/montage.png`.
