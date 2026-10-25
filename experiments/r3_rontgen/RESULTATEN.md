# R3 – A3 Röntgen (K3a vast per zuil, K3b ijkpaal): resultaten

Scripts (vanuit repo-root, deterministisch, totaal < 10 s): `python3 experiments/r3_rontgen/t1_transmissie.py`, `t2_snr_tijd.py`, `t3_dosis.py`, `t4_sensor_kosten.py`. Gedeeld model: `rontgen_model.py`. Attenuatiedata: `xcom_data.py`. De tabel komt uit xraydb/Elam, dezelfde Scofield/Hubbell-basis als NIST XCOM. Steekproef tegen gepubliceerde XCOM-waarden (water, Al, Fe, Cu, Pb, C): afwijking < 0,5 %. Ruwe uitvoer staat in `t1…t4_resultaten.txt`. **[A]** = aanname.

## Kerncijfers

| Grootheid | Laag | Basis | Hoog | Bron |
|---|---|---|---|---|
| Transmissie zak (30 kV, t.o.v. leeg) bij 2 / 5 / 10–13 g/cm² | 0,21 | 0,038 | 0,0034–0,0009 | T1 |
| Restransmissie cel/sleutel/AA achter zak | < 10⁻¹⁰ | (volledig opaak) | | T1 |
| Restransmissie Al-blik / folie / glas | 0,85–0,93 / 0,88–0,93 / 0,04–0,10 | | | T1 |
| Benodigde stilstand (pixel-SNR ≥ 5, 30 kV 4 W, GOS + 4/3"-camera) | 0,1 s (2 g/cm²) | 0,2 s (5 g/cm²) | 2,5 s (10) / 14 s (13) | T2 |
| Idem, goedkoopste camera (RPi HQ) | 0,6 s | 4,5 s | > 30 s (≥ 10 g/cm²) | T2 |
| Energie per inworp (4 W, 5 s) | 0,003 Wh (1 s) | 0,013 Wh | 0,08 Wh (30 s) | T2 |
| Staal voor ≤ 1 µSv/h op 0,1 m, primaire bundel 30 kV | 0,75 mm (1 W) | 0,9 mm (4 W) | 3,5 mm bij 50 kV; > 4 mm bij 80 kV | T3 |
| Lekstraling bij 3 mm zuilwand, 30 kV 4 W | | 1·10⁻⁷ µSv/h | | T3 |
| Dosis bij falende interlock (10 s, open klep, 30 kV 4 W) | 0,25 µSv (1 W) | 1,0 µSv | 2,6–4,3 µSv (50–80 kV) | T3 |
| K3a vast per zuil, TCO 6 jr | €33 | **€71** | €149 per container/mnd | T4 |
| K3b netwerk (1 unit per 50/35/20 containers, campagnes van 3 mnd) | €7 | **€20** | €60 per container/mnd | T4 |
| K3b als ijkcampagne (5 units × 1 jaar per gemeente van 1 000 containers) | €22 k | **€42 k/jaar** | €72 k (= €1,8–6,0 per container/mnd in dat jaar) | T4 |
| Vermeden schade (A7) | | ~€3 per container/mnd | | A7 |

## T1 – Beer-Lambert, contrast, dual-energy
- **Vraag:** Zijn cellen in een zak van 2–13 g/cm² zichtbaar bij ≤ 30 kV, en zijn ze te onderscheiden van blik, folie, sleutel en alkaline?
- **Methode:** µ/ρ per element (XCOM-equivalent) met mengregel. Kramers-spectrum van een W-anode met 0,5 mm Al en twee PE-vensters van 3 mm (R2b: venster in de RVS-trommel). Objectpaden zoals in `OBJECTS` **[A]**: 18650 = 0,39 g/cm² staal + 4,5 g/cm² jelly roll.
- **Resultaat** (`fig_transmissie.png`):
  - Alle cellen (18650, AA, vape-kern, telefoon-pouch) en sleutels zijn bij 30 kV volledig opaak, ook achter 13 g/cm².
  - Al-blik en folie zijn bijna transparant (T ≈ 0,9). Hier faalt inductie juist (A2), dus röntgen vult dat aan.
  - Een staalblik geeft T 0,01–0,03. Dat is herkenbaar aan vorm en randen.
- **Dual-energy** (`fig_dualenergy.png`):
  - Bij 30 kV (split-filter 0/1 mm Cu) zijn R-waarden 1,03–1,26 en zijn de opake objecten ongedefinieerd. Dual-energy is bij 30 kV **zinloos**.
  - Ook bij 80 kV is R voor 18650 1,19 en voor AA-alkaline 1,20, dus **chemie is niet te scheiden**.
  - Wat wél werkt: laag-Z (blik, folie, glas: R 1,5–1,9) tegenover cel/sleutel.
- **Conclusie:** Bij 30 kV is detectie een kwestie van **vormherkenning van opake objecten**. Li-ion en alkaline van dezelfde vorm (AA/14500) blijven niet te onderscheiden. Pakketten (powerbank, laptop, e-bike) zijn wel goed te herkennen aan het aantal en de rangschikking van cellen.

## T2 – Fotonstatistiek en stilstand (uitgangspunt 1)
- **Methode:**
  - Fluentie op 0,6 m, detectorabsorptie (GOS 70 mg/cm², CsI).
  - Lenskoppeling η = 0,8/(4N²(1+m)²) **[A]**, leesruis en donkerstroom.
  - Strooi/primair-verhouding 0,10 per g/cm² (kegelbundel) en 0,03 (waaierbundel) **[A]**.
  - Pixel 2×2 mm; norm SNR ≥ 5 (Rose) **[A]**.
- **Resultaat** (`fig_snr_vs_tijd.png`): de tabel hierboven. Een flatpanel heeft bij alle zakken < 1 s nodig. Een lijnarray die tijdens stilstand scant heeft 0,8 s nodig bij 5 g/cm² en 4 W, en faalt bij ≥ 10 g/cm² binnen 10 s.
- **Conclusie (uitgangspunt 1):** Stilstand levert bij röntgen **geen betere fysica**, maar maakt een **goedkope lens-gekoppelde detector** mogelijk: 1–15 s in plaats van een flatpanel van €9 k.
  - Dat bespaart ~€8 k per unit.
  - Natte, zware zakken (≥ 10 g/cm², **[A]** ~3–5 % van de zakken) vragen 2,5–15 s. Is de stilstand korter, dan worden ze gemist (`P_HEAVY_FAIL` = 0,03 in de JSON).
  - Onzekerheid: de buisopbrengst van het Kramers-model (85 µGy/mAs op 1 m bij 30 kV) kan een factor 2 te hoog zijn. Dan verdubbelen de tijden.

## T3 – Dosis en afscherming
- **Methode:**
  - H*(10) uit het spectrum met µen/ρ van lucht (NIST) en H*(10)/Ka (ICRP 74).
  - Primaire bundel in het slechtste geval: lege trommel, detector niet meegerekend.
  - Enkelvoudige strooiing uit de zak (5 g/cm², bundel 0,44 sr) naar de klepzijde door RVS.
- **Resultaat** (`fig_dosis.png`):
  - Bij 30 kV volstaat < 1 mm staal. De bestaande zuilwand (3 mm) geeft een marge van ~10⁷.
  - Strooistraling naar de klep: 2 mm RVS geeft ~10⁻⁵ µSv/h.
  - Bij 50 kV is ≥ 3,5 mm staal nodig, bij 80 kV > 4 mm. Daar is lood nodig.
  - Een falende interlock geeft bij 30 kV ≤ 1 µSv per 10 s.
  - Buisbehuizing met 1 mm Pb: verwaarloosbaar.
- **Conclusie:** De dosisnorm van Bbs 3.18-1b is bij 30 kV ruim haalbaar. Het risico zit in **spleten en vensters** (niet gemodelleerd) en in de interlock, niet in de wanddikte.

## T4 – sensor_model_K3.json en kosten
- **p_out_given_item** [geen, cel, pakket], met PACK_WHEQ = 20 (Orchestrator):

| Item | Output |
|---|---|
| 18650 | 0,10 / 0,89 / 0,01 |
| telefoon | 0,08 / 0,85 / 0,08 |
| powerbank | 0,08 / 0,12 / 0,80 |
| laptop | 0,08 / 0,01 / 0,91 |
| e-bike | 0,06 / 0 / 0,94 |
| vape | 0,22 / 0,78 / 0 |
| **alkaline** | **0,15 / 0,85 / 0** |
| sleutel | 0,96 / 0,04 / 0 |
| pan/gereedschap | 0,90 / 0,05 / 0,05 |
| blik | 0,99 / 0,01 / 0 |
| folie | 0,998 / 0,002 / 0 |

- **Hoe de getallen tot stand komen:**
  - p_det komt uit T1 (opaak + vorm) plus een expertschatting van de vormherkenning **[A]**.
  - Wh-schatting: lognormaal met σ = 0,35 **[A]**; de sensor neemt w_state 0,8 aan.
  - Masking: [0; 0,006; 0,012; 0,03].
  - Extra veld `wh_est_given_item`: A6 moet de geschatte Wh van de "cel"-objecten per inworp optellen. Zo wordt een bundel alkaline als pakket gezien.
- **Kosten** (`fig_kosten.png`):
  - K3a is 11–50× de vermeden schade, dus **KO als product**.
  - K3b als netwerk (€20/mnd) is ook te duur.
  - K3b als tijdelijke **ijk- of validatiecampagne** kost ~€42 k per gemeente-jaar. Eens per 3 jaar is dat ≈ €1,2 per container/mnd. Daarmee is het betaalbaar als nulmeting of ground truth voor K2/K5 (A8-E4).

## Alleen met prototype te bevestigen + labtestontwerp
| Test | Opstelling | Testobjecten | Protocol |
|---|---|---|---|
| L1 Buisopbrengst & SNR | 30 kV-buis (≤ 4 W), GOS-scherm, 4/3"-camera in een mock-up van de trommel met PE-vensters | PMMA/water-fantomen 2–13 g/cm², 18650 en AA erin | Meet SNR vs t (0,1–30 s); kalibreert de Kramers-factor (verwacht 0,5–2×) |
| L2 Herkenning | Zelfde opstelling | 200 echte restafvalzakken (gesorteerd = ground truth) + ingebrachte items uit params.ITEMS (n ≥ 30 per klasse) | Blind CNN-/menselijke beoordeling, matrix p_out_given_item, overlap-miskans |
| L3 Dosimetrie | Volledige zuil, gekalibreerde dosistempometer (H*(10), ≥ 20 keV) | Lege trommel, volle zak, open-klep-scenario | Raster van 0,1 m rond alle bereikbare oppervlakken, spleten en vensters; interlock-faalinjectie; rapport door stralingsdeskundige voor ANVS-vooroverleg |
| L4 Zware zak | Natte GFT-zakken 8–15 kg | – | Fractie zakken met SNR < 5 binnen de werkelijke stilstand (P_HEAVY_FAIL) |

Niet gemodelleerd: meervoudige strooiing, spleetlekken, CNN-prestatie (alleen aangenomen), temperatuur/condens op de lens, en de magnificatiefout bij de Wh-schatting.
