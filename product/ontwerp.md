# Productontwerp K2 "Pakketwachter" en K5 "Hybride" (A5, Ronde 3)

EUR 2026 excl. btw. Getallen uit `product/BOM_K2.csv`, `BOM_K5.csv` en `experiments/r3_hardware/RESULTATEN.md`. Aannames **[A]**.

## 1. Opbouw (zie `blokschema.png`)

| Blok | K2 (zuil) | K5 extra (container) |
|---|---|---|
| Sensor | 2 PI-lussen (boven en onder) gegoten in een PE-UHMW-trommelliner, meedraaiend; ferro-kanaal via DC-bias | Thermopile 8×8 + elektrochemische CO-cel + 2× NTC (binnen/buiten) + RH |
| Elektronica | PI front-end (MOSFET-driver, snelle opamp, ADC 1 MS/s) + STM32U5. Doet de nulmeting in dezelfde trommelhoek vóór en na de inworp, en de features → klasse geen/cel/pakket | nRF52 (BLE), event-logica dT/dt en CO-trend |
| Voeding | 12 V van de pas-zuil-accu via een geïsoleerde DC-DC, 6–26 mWh/dag | LS33600 (43 Wh bruikbaar), ~10 mWh/dag → ~12 j |
| Communicatie | Meeliften op het OEM-modem (RS485/UART). Payload ≤ 20 B per inworp (A6) of een samenvatting 3×/dag | BLE naar de K2-module, 1–3 m via de valschacht |
| Veiligheid | **Fail-open:** galvanisch gescheiden, geen eigen slot- of klepsturing. Bij een storing aan de sensor blijft de zuil gewoon werken (A8 C4-KO) | Geen bewegende delen |

## 2. Montage (zie `montage.png`)

| Onderdeel | Plaats | Tijd |
|---|---|---|
| Liner met lussen | In de RVS-trommel, met 4 RVS-blindklinkmoeren; vervangt de trommelverkleiner indien aanwezig | 30–45 min |
| Flexkabel | Robotkabel (≥ 300k buigcycli) van de trommelas naar de zuilkop, rotatie ≤ 120° | 10 min |
| Module | Zuilkop naast de OEM-controller, via het inspectieluik | 10 min |
| K4-lite | RVS-beugel onder de containerkop, kijkt naar beneden; bij een lediging bereikbaar | 20–30 min |

Het meest efficiënt is installeren tijdens het reguliere onderhoud van de toegangscontrole (1e/2e lijn). Ook een fabrieksoptie bij nieuwe zuilen is mogelijk, en dat is goedkoper.

## 3. Behuizing en omgeving

| Eis | Ontwerp |
|---|---|
| IP | Liner en lussen volledig ingegoten (IP68, bestand tegen hogedrukreiniging). Module in de zuilkop IP67 |
| IK | Liner IK10 (PE-UHMW 8–10 mm, slijtvast). De module zit achter de stalen zuilwand |
| Temperatuur | −25…+70 °C. Li-SOCl₂ in K4-lite is geschikt van −55 tot +85 °C |
| Condens | PU-potting + ePTFE-ventiel. Het IR-venster is HDPE met een hydrofobe coating |
| Chemie | Bestand tegen percolaat. Bevestiging in RVS 316 |
| Brandveiligheid | Geen Li-cel in de trommel (R2 A1/A8). In K4-lite een Li-SOCl₂ van 61 Wh op de container: in de risicoanalyse opnemen, alternatief ER18505 (~14 Wh) met een levensduur van ~4 j |

## 4. Onderhoud en levensduur

| Item | Interval | Wie |
|---|---|---|
| Liner (slijtdeel) | 5–10 j **[A]** | 2e lijn (OEM/servicepartner) |
| K4-lite batterij + CO-cel | samen elke 5–7 j | 1e lijn bij lediging |
| Zelftest | dagelijks: lusweerstand, nulniveau, drift → "sensor defect"; de zuil blijft werken | automatisch |
| Firmware | OTA via OEM-modem; BLE-DFU voor K4-lite | centraal |
| Ontwerplevensduur | 10 j elektronica (bestekeis) | – |

## 5. Van de plank vs. ontwikkelen

| Van de plank | Te ontwikkelen |
|---|---|
| STM32U5, nRF52, LS33600, AMG8833-klasse IR, TGS5042-klasse CO, robotkabel, ePTFE-ventiel | PI front-end met multi-gate en ferro-kanaal (A2-ontwerp) |
| OEM-modem en -accu (bij de partner) | Liner en lussen per trommeltype (≥ 3 varianten **[A]**) |
| Cloud/dashboard-stack (A6) | Classifier + kalibratie (dataset via K3b-ijkpaal) |
| | OEM-protocoladapter (NRE 50–150k per OEM) |

## 6. Kostprijs samengevat (basis)
- **K2:** HW 91 + installatie 45. Run EUR 0,2/mnd + 2/j. TCO ≈ **EUR 1,50/container/mnd**, exclusief NRE en marge.
- **K5:** HW 188 + installatie 75. TCO ≈ **EUR 3,14/container/mnd**.
- Ter vergelijking B1, thermische camera op de wagen: ≈ EUR 0,16/container/mnd.

## 7. Open risico's (voor R4)
1. PI-signaal achter de liner in de RVS-trommel: wacht op het A2-model.
2. Of de OEM wil meewerken, en de NRE.
3. Bereik van de BLE-link tussen container en zuil.
4. Varianten van de trommels.
