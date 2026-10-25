# A5 – Product & hardware (Ronde 0)

Prijspeil EUR 2026 excl. btw. Aannames **[A]**. Bronnen met datum onderaan (§9). Rekensjabloon: `experiments/A5_energiebudget.py`.

## 1. Kernbevindingen (TL;DR)

| # | Bevinding | Gevolg voor product |
|---|-----------|---------------------|
| 1 | NL-inworpzuilen: **zuil 3 mm staal, verzinkt + poedercoat**; **trommel RVS 304, dubbelwandig, 30–60 L** (vaak 80 L met verkleiners). | Stalen zuil = volledige afscherming (skin depth ~0,3 mm bij 1 kHz) → spoel moet **in/aan de trommel of de inworpmond** zitten, nooit buiten de zuil. RVS 304 is niet-magnetisch en slecht geleidend (δ ≈ 13 mm @1 kHz, 4 mm @10 kHz) → velden dringen door 1–2 mm plaat, maar de trommel zelf is een groot, bewegend achtergronddoel → nulmeting per stand nodig. |
| 2 | Toegangscontrole is standaard in bestekken: paslezer + elektrisch slot + **batterij of accu + zonnepaneel** + modem (GPRS/LoRa → nu 4G/LTE-M, whitelist ≥ 3×/dag). Batterij ≥ 5 jaar, wisselbaar via inspectieluik in ≤ 5 min; elektronica ≥ 10 jaar levensduur; ≥ 5 jaar garantie. | Er ligt al **voeding, modem, pas-event en behuizing** in de zuil. Een OEM-insteekmodule hoeft alleen sensor + kleine MCU te leveren: marginale kosten en energie per inworp dalen sterk. Onderhoudsritme (batterijwissel 1e lijn door gemeente) sluit aan. |
| 3 | Energie per inworp is **klein** voor inductie/thermisch (0,01–0,2 mWh); communicatie domineert (LTE-M ~1 mWh/bericht **[A]**). | Batch-versturen (4×/dag) + direct alarm → 8–21 mWh/dag bij 30–150 inworpen → **5,6–14 jaar op één Li-SOCl2 D-cel** (LS33600, 43 Wh bruikbaar). Camera+AI 2× zwaarder, nog haalbaar. Röntgen (0,3–1,3 Wh/dag) is **niet batterijgevoed** te doen → netaansluiting of grote accu+zon. |
| 4 | Connectiviteit is goedkoop: 1NCE 10 jaar LTE-M/NB-IoT **EUR 10 eenmalig** (500 MB); TTN gratis (fair use 30 s airtime/dag); KPN LoRa/LTE-M-tarief niet publiek. | Connectiviteit ≈ EUR 0,1–1,5/maand/container; geen kostendrijver. |
| 5 | Zonnepaneel in december NL: ~0,5 kWh/m²·dag horizontaal; verticaal/beschaduwd op zuil 0,1–0,3 kWh/m²·dag **[A]**. Een 2 W paneel levert in dec ~0,1–0,5 Wh/dag. | Ruim genoeg voor inductie/thermisch/gas; zon alleen nodig bij camera/continu gas/radar. Zon = vandalisme- en vuilrisico → liever niet. |

## 2. Inworpzuilen en containers NL

| Fabrikant / leverancier | Product | Materialen / bijzonderheden | Bron / status |
|---|---|---|---|
| Bammens (NL) | Ondergrondse containers + inworpzuilen, pas-toegang | Zuil volledig 3 mm staal, thermisch verzinkt, 3-laags poedercoat; RVS-trommel zelfsmerend gelagerd | Offerte Stichtse Vecht op TenderNed **[datum document niet zichtbaar in zoekresultaat]** |
| Oranjewoud / Sidcon (NL) | Ondergrondse containers + zuilen | Plaatstaal, gepoedercoat (generiek bestek) | Productdetails **niet gevonden** |
| Villiger (CH/NL) | Ondergronds/semi-ondergronds | Staal/RVS **[A]** | **Niet gevonden** |
| Plastic Omnium / Sulo (nu Sulo/Hu = deel Plastic Omnium-afsplitsing) | Minicontainers (HDPE), ook ondergronds | Minicontainer = HDPE → metaaldetectie in deksel eenvoudig (geen afscherming) | **[A]** |
| Molok (FI) | Semi-ondergronds, deep collection | Betonnen/hout/composiet mantel, PE-zak; inworp met deksel, vaak zonder trommel | **[A]** |
| Toegangscontrole: o.a. Bammens, Vconsyst, Ecosmart, (ook Sidcon, Nedvang-integraties) | Paslezer + slot + modem | Batterij/accu+zon; GPRS→4G/LTE-M; ook vulgraadsensor | TenderNed-bestekken (meerdere gemeenten, o.a. Middelburg, Terneuzen); merk-specs **niet gevonden** |

**Bestekeisen (TenderNed, diverse gemeenten; data niet zichtbaar):**

| Eis | Waarde |
|---|---|
| Trommel | RVS 304, dubbelschalig, 60 L (of 80 L + demontabele verkleiners → 60 L) |
| Zuil | Verduurzaamd plaatstaal, gepoedercoat, vandalismebestendig |
| Voeding | Meegeleverde batterij of zonnecel; batterij later koppelbaar aan accu/zonnecellen; "accubox met zonnepaneel" bij restafval |
| Batterij | ≥ 5 jaar bij 3 communicatiemomenten/dag; via inspectieluik ≤ 5 min wisselbaar; marktgangbaar |
| Communicatie | Was "GPRS of LoRa", eis geschrapt → "dekkend, actueel"; ander bestek: whitelist ≥ 3×/dag via ≥ 4G |
| Levensduur | Elektronica (toegang + vulgraad) ≥ 10 jaar; ander bestek toegang ≥ 15 jaar, buitenbak 30 jaar |
| Garantie / beheer | ≥ 5 jaar; 1e lijn (reset, batterij, verstopping) door gemeente |

**Niet gevonden:** spanning/capaciteit van accu's in bestaande pas-zuilen (vermoedelijk 12 V lood/LiFePO4 7–40 Ah of 3,6 V Li-SOCl2-pakketten **[A]**); open OEM-interfaces (UART/RS485/CAN) van Bammens/Vconsyst/Ecosmart — moet in gesprek worden opgevraagd.

## 3. Metalen in en rond de inworp (relevant voor A2)

| Onderdeel | Materiaal | σ (MS/m) | µr | Skin depth 1 kHz | 10 kHz | Gevolg |
|---|---|---|---|---|---|---|
| Zuilmantel | S235 staal 3 mm | ~6 | 100–1000 | ~0,3 mm | ~0,1 mm | Volledige afscherming; montage binnenin |
| Trommel | RVS 304, 1–2 mm, dubbel | 1,4 | ~1 (licht magnetisch na vervorming) | ~13 mm | ~4 mm | Doorlatend maar groot achtergronddoel; draait mee → kalibratie per stand; spoel liefst in trommelbodem/-achterwand (draait mee: flexkabel, geen sleepring, rotatie ≤ 120° **[A]**) |
| Deksel/klep | Staal of RVS | – | – | – | – | Spoel onder klep alleen bruikbaar als klep kunststof is of spoel aan binnenzijde met afstand ≥ 20 mm **[A]** |
| Minicontainer / afvalbak | HDPE / soms staal (Amsterdamse bak) | – | – | – | – | HDPE ideaal voor sensor in deksel |

Optie die A2 moet toetsen: **kunststof (PE/UHMW) liner of venster** in RVS-trommel (vervangingsonderdeel, EUR 20–60 **[A]**) met spoel erachter.

## 4. Microcontrollers en modems (prijzen indicatief, 1k st.)

| Component | Rol | Slaap | Prijs (EUR) | Bron/opmerking |
|---|---|---|---|---|
| ESP32-S3 (module) | Camera/vector-AI, WiFi/BLE | 7–10 µA deep sleep (module + LDO ≥ 20 µA) | 2,5–3,5 **[A]** | Niet geschikt voor 10 j batterij zonder strak power-gating |
| nRF9151 SiP | LTE-M/NB-IoT + Cortex-M33 + GNSS | ~3 µA PSM | 15,6 @250 (Farnell, 2026 listing); 12–14 @1k **[A]** | Eén chip voor MCU + modem; aanbevolen standalone |
| nRF9160 | Voorganger | ~3 µA | 15–20 **[A]** | Vervangen door 9151 |
| STM32U5 | Ultra-low-power MCU, DSP | 2–4 µA Stop2 | 3–6 **[A]** | Goed voor PI/LDC-signaalverwerking |
| STM32WL (bv. RAK3172 module) | LoRaWAN SoC | ~2 µA | 5–8 **[A]** | Goedkoopste "eigen radio" |
| STM32N6 | Edge-AI NPU (camera) | hoog actief (~0,3–1 W) | 8–15 **[A]** | Alleen bij camera-concept; overkill voor inductie |
| Murata/Quectel BG77/BG95 | LTE-M modem (los) | ~3 µA PSM | 7–12 **[A]** | Alternatief naast losse MCU |
| TI LDC1612/LDC1101 | Inductie-naar-digitaal | µA | 2–4 **[A]** | VLF/wervelstroom front-end |

## 5. Connectiviteit NL 2026

| Optie | Kosten | Energie/bericht | Dekking/opmerking | Bron |
|---|---|---|---|---|
| 1NCE IoT Lifetime Flat (LTE-M/NB-IoT via T-Mobile/DT-roaming) | EUR 10 eenmalig / 10 jaar, 500 MB + 250 SMS; alleen zakelijk | 0,5–2 mWh (LTE-M PSM) **[A]** | 500 MB/10 j = ~137 kB/dag: ruim (100 inworpen × 50 B = 5 kB) | 1NCE FAQ (ongedateerd; checken) |
| KPN LTE-M / NB-IoT (M2M) | **Niet publiek**; **[A]** 0,5–2 EUR/mnd bij volume | idem; NB-IoT bij slechte dekking (ondergrond, metalen zuil) tot 3–10 mWh | KPN schakelde 2G/3G uit (3G 2022); LTE-M + NB-IoT landelijk | Offerte nodig |
| Vodafone NB-IoT/LTE-M | **Niet gevonden**; **[A]** 0,5–2 EUR/mnd | idem | | |
| KPN LoRaWAN (ThingPark) | **Niet publiek**; **[A]** 0,5–1,5 EUR/mnd; via resellers (Thingsdata, Wireless Logic) | 0,005 (SF7)–0,06 (SF12) mWh | Downlink beperkt; in metalen zuil antenne naar buiten (onder kunststof kap) | Telecompaper 2015; resellers |
| The Things Network | Gratis community; fair use 30 s uplink-airtime/dag, ≤ 10 downlinks/dag | idem | Dekking stad goed, landelijk wisselend; geen SLA → niet voor gemeentelijk contract | TTN fair use policy **[A] jaartal niet gecontroleerd** |
| Meeliften op modem toegangscontrole | 0 extra (marginaal) | 0 extra (bericht gaat toch al 3×/dag) | Vereist OEM-afspraak | — |

Antenne: zuil = kooi van Faraday → antenne in kunststof kap/pasvenster of extern (EUR 2–8).

## 6. Voeding

| Bron | Specificatie | Prijs | EUR/Wh | Opmerking |
|---|---|---|---|---|
| Li-SOCl2 D-cel (Saft LS33600) | 3,6 V × 17 Ah = 61 Wh nominaal; ~43 Wh bruikbaar bij kou/pulsen **[A]** | 18,6 (1 st.) → 11–13,6 (60–180 st.) (TME, 2026 listing) | 0,18–0,30 | Zelfontlading < 1 %/j; passivatie → LTE-M pieken (≥ 0,5 A) via supercap/HLC-buffer (+ EUR 3–8) |
| Li-SOCl2 pakket 2S1P/3S1P (RS) | 7,2 V / 10,8 V | 113 / 192 (RS, 2026) | 0,9–1,0 | Kant-en-klare packs zijn 3–4× duurder per Wh |
| LiFePO4 12 V 7–20 Ah | 90–250 Wh | 40–120 **[A]** | ~0,4–0,5 | Laden < 0 °C niet toegestaan → BMS met laadblokkade/verwarming |
| Lood/AGM 12 V 7–26 Ah | 84–310 Wh | 20–70 **[A]** | ~0,2–0,25 | Goedkoop, zwaar, 3–5 j |
| Zonnepaneel 2–10 Wp | – | 10–40 **[A]** | – | Dec NL horizontaal ~0,5 kWh/m²·dag (KNMI De Bilt, klimatologisch ~1 600 J/cm² per dec **[A]**); 5 Wp × 0,5 h equiv × PR 0,6 ≈ 1,5 Wh/dag horizontaal, verticaal/schaduw 0,3–0,8 Wh/dag |
| Energie-oogst trommelrotatie | gebruiker draait trommel: ~20 N × 0,3 m ≈ 6 J; 10–20 % rendement → 0,6–1,2 J (0,17–0,33 mWh) per inworp **[A]** | 5–15 **[A]** | – | Genoeg voor 1 inductiemeting + LoRa-bericht; zie concept A5-C5 |
| Netaansluiting | Zelden aanwezig bij ondergrondse containers | aansluitkosten 300–1 500 per locatie **[A]** | – | Alleen bij röntgen |

## 7. Behuizing, omgeving, montage

| Eis | Waarde | Motivering |
|---|---|---|
| Dichtheid | IP67 (zuilkop), **IP68/IP69K** in trommel (regen, percolaat, hogedrukreiniging) | Trommel is nat en vuil |
| Slagvastheid | IK10 (20 J) | Vandalisme, zakken met glas/hout |
| Temperatuur | −25…+70 °C (zwarte zuilkop in zon) **[A]** | Li-SOCl2: −55…+85 °C OK; LiFePO4 laden niet < 0 °C |
| Condens | Potting (PU/epoxy) of conformal coating + Gore-ventiel | Dagelijkse temperatuurcycli |
| Chemisch | Bestand tegen percolaat, zuren, reinigingsmiddelen; RVS 316 bevestiging | |
| EMC/radio | CE/RED (EN 300 220 LoRa / EN 301 908 LTE), EN 61000-6-2/3 | Eenmalig EUR 15–40k **[A]** |

| Montagepositie | Meetkwaliteit (inductie) | Kabel/energie | Onderhoud | Opmerking |
|---|---|---|---|---|
| **In trommelbodem/-achterwand** (draait mee) | Beste: zak ligt 1–10 s stil, 5–20 cm afstand | Flexkabel naar zuilkop of eigen batterij | Vuil, nat, schokken → potting | Voorkeur voor A2-concepten |
| Achter kunststof liner/venster in trommel | Goed | idem | Liner = slijtdeel | Vergt trommelaanpassing |
| In zuildeksel/klep | Matig: zak beweegt, afstand groter | Dicht bij bestaande elektronica | Makkelijk | Alleen bij kunststof klep |
| Ring om inworpmond (onder trommel, valschacht) | Zak valt in 0,1–0,3 s → korte meting | Vaste montage | Goed bereikbaar | Walk-through-principe |
| Onder containerdeksel / in containerkop | n.v.t. voor inworp; wel continu (temp/gas) | Eigen batterij | Bereikbaar bij lediging | A4-concepten |
| In zuilkop naast paslezer (OEM) | Alleen elektronica; sensor via kabel | Gedeelde accu+modem | Mee met toegang | OEM-route |

Onderhoud/levensduur-doel: 10 jaar elektronica, batterijwissel ≤ 1× per 5–10 jaar (synchroon met toegangscontrole), zelftest + "stuck/vuil"-detectie, OTA-firmware. Uitval door vandalisme/brand **[A]** 1–3 %/jaar.

## 8. Sjablonen voor Ronde 3

### 8a. Energiebudget (basis-aannames; script `experiments/A5_energiebudget.py`)

MCU actief 15 mW tijdens meting; systeemspanning 3,6 V.

| Sensortype | Vermogen (mW) | Meettijd l/b/h (s) | mWh/inworp l/b/h | mWh/dag @30 / 80 / 150 inworpen* |
|---|---|---|---|---|
| PI-metaaldetector | 60 | 2/5/10 | 0,042 / 0,104 / 0,208 | 8,4 / 13,6 / 20,9 |
| Wervelstroom LDC (VLF) | 6 | 2/5/10 | 0,012 / 0,029 / 0,058 | 6,2 / 7,6 / 9,7 |
| Thermopile-array 32×24 | 80 | 1/3/5 | 0,026 / 0,079 / 0,132 | 7,7 / 11,6 / 17,2 |
| Thermopile 8×8 / enkel | 15 | 1/3/5 | 0,008 / 0,025 / 0,042 | 6,0 / 7,3 / 9,0 |
| mmWave 60 GHz | 300 | 0,5/1/2 | 0,044 / 0,087 / 0,175 | 7,9 / 12,3 / 18,4 |
| Camera + edge-AI (ESP32-S3) | 400 | 1/2/4 | 0,115 / 0,231 / 0,461 | 12,2 / 23,7 / 39,9 |
| MOX-gas puls (BME688) | 40 | 1/2/5 | 0,015 / 0,031 / 0,076 | 6,2 / 7,7 / 9,9 |
| Röntgen (vergelijking) | 30 000 | 0,5/1/2 | 4,2 / 8,3 / 16,7 | 255 / 672 / 1 256 |

\* basis-meettijd + slaap 15 µA (1,3 mWh/dag; bandbreedte 5–50 µA = 0,4–4,3 mWh/dag) + 4 LTE-M-berichten/dag à 1 mWh **[A]**.
Elk inworp direct via LTE-M: PI 34 / 90 / 167 mWh/dag; via LoRaWAN SF12: 6 / 14 / 26 mWh/dag.
Levensduur PI + LTE-M batch op 1× LS33600 (43 Wh bruikbaar): **13,9 / 8,6 / 5,6 jaar** bij 30 / 80 / 150 inworpen/dag.

| Invulregel per concept | Laag | Basis | Hoog |
|---|---|---|---|
| Slaapstroom systeem (µA) | | | |
| mWh per inworp (sensor + MCU) | | | |
| Berichten/dag × mWh/bericht | | | |
| Continu-meting (mWh/dag) | | | |
| **Totaal mWh/dag @30/80/150** | | | |
| Energiebron + bruikbare Wh | | | |
| **Levensduur (jaar) / benodigd paneel (Wp)** | | | |

### 8b. BOM-sjabloon (EUR excl. btw, @1 000 st.)

| Post | Laag | Basis | Hoog | Bron/aanname |
|---|---|---|---|---|
| Sensor front-end (spoel, IC, optiek) | | | | |
| MCU / SoC | | | | |
| Radio/modem + antenne | | | | |
| SIM / connectiviteit (eenmalig) | | | | |
| Voeding (cel/pack/accu, buffer, paneel) | | | | |
| PCB + passieven + assemblage | | | | |
| Behuizing (IP68/IK10) + potting + bevestiging | | | | |
| Kabel/connector/flex naar trommel | | | | |
| Test, kalibratie, verpakking | | | | |
| **Kostprijs hardware** | | | | |
| Installatie per container (arbeid + reis) | | | | |
| Certificering (eenmalig, gedeeld over N st.) | | | | |
| Connectiviteit/cloud per maand | | | | |
| Onderhoud per jaar (batterij, uitval) | | | | |
| **TCO 10 jaar per container** | | | | |

Referentiewaarden voor invullen: PCB+assemblage 4–10; behuizing+potting 6–20; installatie 25–75 per container (15–30 min + reis) **[A]**; certificering 15–40k eenmalig **[A]**.

## 9. Bronnen

| Bron | Datum | Gebruikt voor |
|---|---|---|
| TenderNed, Bammens-offerte gemeente Stichtse Vecht (publicatie 212540 e.a.) – tenderned.nl/papi/tenderned-rs-tns/v2/publicaties/… | ongedateerd in zoekresultaat (± 2019–2023) **[A]** | Zuil 3 mm staal, RVS-trommel |
| TenderNed, bestekken inzameling/toegangscontrole (publicaties 221122, 265278, 286057, 294953, 318040, 325387) incl. Terneuzen NvI, Middelburg | ± 2020–2024 **[A]** | Trommel RVS 304 60 L, voeding, batterij ≥ 5 j, 4G, levensduur, garantie |
| TME, Saft LS33600 (tme.eu katalog saft) | geraadpleegd okt 2026 | Li-SOCl2-prijs |
| RS Components BE/IT, LS33600 2S1P/3S1P | geraadpleegd okt 2026 | Pack-prijs |
| Farnell DE, nRF9151-LACA-R (dp 4472255) | geraadpleegd okt 2026 | MCU/modem-prijs |
| 1NCE FAQ "What is included in the IoT Flat Rate" | ongedateerd, geraadpleegd okt 2026 | EUR 10 / 10 jaar / 500 MB |
| Telecompaper "KPN van start met LoRa-netwerk" | 2015 | KPN LoRa |
| KNMI maandoverzichten december (cdn.knmi.nl mow_YYYY12.pdf) | 2008–2023 | Instraling dec (waarde ~0,5 kWh/m²·dag = aanname, niet uit PDF gelezen) |

**Niet gevonden:** KPN/Vodafone IoT-tarieven, Bammens/Vconsyst/Ecosmart accu-specs en OEM-interfaces, Villiger/Sidcon/Molok materiaal-datasheets, actuele prijzen ESP32-S3/STM32 (aangenomen).
