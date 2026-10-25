# R2a – A5 (Product & hardware) valt aan

Basis: `research/A5_hardware.md` (zuil 3 mm staal; trommel **dubbelwandig RVS 304**; bestek: batterij ≥ 5 jaar, elektronica ≥ 10 jaar, 1e lijn door gemeente). Ernst: **KO** / zwaar / licht. Aannames **[A]**.

## A3 – Röntgen

| Concept | Kritiek (hardware/energie/robuustheid/kosten) | Ernst | Wat het redt |
|---|---|---|---|
| A3-C1 Schaduwdoos | (1) **De trommel is dubbelwandig RVS, niet "2–3 mm staal als afscherming"**. µ/ρ(Fe, 30 keV) ≈ 8 cm²/g → 1 mm RVS laat e^-6,5 ≈ 0,15 % door; twee wanden ≈ 10⁻⁶. Een buis buiten de trommel ziet dus niets. (2) Een RPi 5 slurpt 2,5–3 W idle = 60–70 Wh/dag; 20–30 s booten past niet in 1–10 s stilstand. (3) Een GOS-scherm van 35×43 cm plus een spiegel in een natte, vuile trommel: geen IK10, condens op de lens. (4) Een 5 Wp paneel levert in dec ~1,5 Wh/dag, nodig is ≥ 2,4 Wh/dag (80 × 0,03 Wh) + MCU → 15–25 Wp + 100–200 Wh LiFePO4 met verwarming (niet laden < 0 °C). (5) EUR 35–60/mnd tegenover EUR 3/mnd vermeden schade (A7). | **KO** (fysica-integratie + business) | Buis en scherm **in** de trommelschaal, of PE/CFRP-vensters in beide wanden; MCU + neural accelerator (STM32N6) in plaats van RPi; alleen als A3-C4 rouleren, niet per container |
| A3-C2 Trommelscan | De lijnarray zit op de vaste zuilwand, dus de bundel moet door twee bewegende RVS-wanden (zie hierboven). Mensen draaien niet met constante snelheid → encoder nodig, en de zak rolt tijdens de rotatie → beeldvervorming. Elektronica naast een vallende zak: schok. | Zwaar | Vensters + hoekencoder (EUR 5–10) + scannen tijdens stilstand met een bewegende bron in plaats van de rotatie |
| A3-C3 Dual-energy | 10–20 W, 2–3 mm Pb (+10–20 kg), netaansluiting nodig (EUR 300–1 500/locatie **[A]**); EUR 9k. Ondergrondse zuilen hebben bijna nooit net. | Zwaar (buiten hotspots) | Alleen milieustraat, overslag of AVI-inlaat, waar net is |
| A3-C4 IJkpaal | Elke verplaatsing: zuil openen, inzet wisselen, interlock en stralingsmeting opnieuw → 2–4 manuur + EUR 300–600 per verhuizing **[A]**. Moet passen op ≥ 5 merken trommels. | Licht | Eén referentiezuil per merk; mobiel alleen tussen gelijke zuilen |
| A3-C5 Pyro-röntgen | Pyro-bronnen leveren ordes minder flux dan een buis **[A]** (op te zoeken); voor een beeld door een volle zak in 10 s onvoldoende. Laadcyclus 1–3 min > interval tussen inworpen bij piekdrukte. | **KO** tenzij flux aangetoond | Flux-meting aanleveren (A3) |

## A4 – Thermisch, gas, continu

| Concept | Kritiek | Ernst | Wat het redt |
|---|---|---|---|
| A4-C1 Thermo-deksel | (1) De **containerkop wordt bij elke lediging door de kraan opgetild** → een sensor die op de zuil/het platform zit verliest contact; op de container moet hij een eigen batterij en radio hebben, ondergronds onder beton en staal (NB-IoT met slechte dekking: 3–10 mWh/bericht). (2) MLX90614 met 90° FOV kijkt naar ~2–4 m²: een hotspot van 0,01 m² op 300 °C verhoogt het gemiddelde maar een paar K → verwarring met zon/rotting. (3) De IR-lens beslaat bij 100 % RV. | Zwaar | Unit vast aan de container (schokbestendig, IP68), LoRaWAN met antenne in de deksel-naad; thermopile-array 8×8 (EUR 15–25) in plaats van 1 pixel; verwarmd of hydrofoob venster |
| A4-C2 Snuffelneus | MOX (BME688) in 100 % RV met H₂S/siloxanen uit rottend afval → vergiftiging/drift; elektrochemische CO-cel 5–7 jaar **[A]**. Beide < 10 jaar levensduureis bestek, en ijken in het veld kan niet. Ethanol/VOC uit voedsel geeft grote achtergrond. | Zwaar | Wisselcartridge (sensor + batterij) die meegaat met de 5-jaarlijkse batterijwissel; zelfdiagnose drift |
| A4-C4 Plop | Wake-on-sound gaat af bij elke inworp, lediging, scooter en vuurwerk. Bij 100 valse wakes/dag × 30 min intensief meten (~10 mW **[A]**) = 500 mWh/dag = 180 Wh/jaar ≈ **4× LS33600 per jaar**. Het membraan (IP67) dempt ook nog 1–10 kHz. | **KO** voor batterij, zoals beschreven | Wake alleen bij drukpuls zonder gelijktijdig inworp-/klepevent; intensieve fase 2 min, passieve CO-cel als bevestiging |
| A4-C5 Vape-neus in trommel | Sensor in het natste, vuilste punt (percolaat, hogedrukreiniging, IP69K); het ePTFE-membraan slibt dicht. MOX-respons door een dichtgeknoopte zak in 2–10 s is onwaarschijnlijk (diffusie, τ tientallen s **[A]**). | Zwaar | Afzuiging uit de trommel-kopruimte naar een sensor in de zuilkop (pompje 50 mW × 5 s = 0,07 mWh) |
| A4-C6 Hotspot-kaart | MLX90640 kost EUR 40–60 (niet 28) en vraagt 80 mW; zelfde lens- en montageprobleem als C1. | Licht | Zie C1 |
| A4-C7 Smeltdraad | Kabel langs de binnenwand schuurt bij elke lediging (afval glijdt eruit), ~50–100×/jaar; de connector tussen de bewegende container en de zuil breekt. | Zwaar | Kabel alleen onder het deksel (geen afvalcontact) + uitlezing door een unit op de container zelf |

## A2 / A6 (kort)

| Concept | Kritiek | Ernst | Redding |
|---|---|---|---|
| A2-C4 Magnetisatiepuls | Veldenergie B²/2µ₀·V bij 30 mT over 0,05 m³ ≈ **18 J/puls** (+ wervelstroomverlies in de RVS-trommel). × 80/dag = 0,4 Wh/dag = 146 Wh/jaar → 3+ D-cellen/jaar; piekstromen van tientallen A. | Zwaar | 10 mT op een beperkt volume bij de trommelbodem (~2 J) of alleen bij een PI-trigger |
| A2-C5 Valkoker | Schachtgeometrie en invalbeveiliging verschillen per merk; inbouw betekent platform openen → installatie EUR 500+ **[A]**. | Licht/zwaar | Alleen bij nieuwbouw of in een fabrieksoptie (OEM) |
| A2-C1/C3 meedraaiende spoel | 80 inworpen/dag × 10 jaar ≈ 300k buigcycli voor de kabel. | Licht | Robot-flexkabel (EUR 5–10) of inductieve/NFC-koppeling |
| A6-C3 Pieptrommel | LED/zoemer is een vandalismedoel en kost energie; met e-ink of één ingebouwde LED achter polycarbonaat is het opgelost. | Licht | Meeliften op het display/de LED van de paslezer (OEM, A5-C1) |

**Rode draad:** alles wat door de RVS-trommel heen moet kijken (röntgen) of aan de container zelf hangt (A4) heeft een montage- en energieprobleem dat in R1 niet begroot is. Alleen concepten die meeliften op de voeding en het modem van de toegangszuil (A5-C1) of < 25 mWh/dag verbruiken (inductie, passieve CO) halen 10 jaar zonder net.
