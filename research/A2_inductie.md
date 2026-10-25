# A2 – Inductie & metaaldetectie (Ronde 0, research)

Agent 2. Peildatum 2026-10. EUR 2026 excl. btw (consumentenprijzen ÷1,21). Aannames **[A]**. Rekenwerk: `scratchpad/tau.py` (orde-grootte, wordt in Ronde 3 formeel in `experiments/`).

## 1. Principes in één tabel

| Principe | Hoe | Meetgrootheid | Sterk | Zwak | Bron |
|---|---|---|---|---|---|
| **VLF (IB, 1 frequentie, 3–20 kHz)** | Continu sinus-zendspoel, gebalanceerde ontvangspoel (DD / concentrisch) | Amplitude + fase (I/Q). Q≈geleiding, I≈ferro | Goedkoop, fase ⇒ "target-ID" ferro vs non-ferro | Eén fase-getal; groot dun Al-object en klein dik Cu-object geven zelfde fase; balans drift met temperatuur en omgevingsmetaal | Detector Prospector (forum, citaat Minelab-engineer, ~2019) |
| **Meerfrequent (Minelab Multi-IQ: 5/10/15/20/40 kHz gelijktijdig; BBS/FBS 1,5–100 kHz)** | Meerdere sinussen tegelijk, ontvanger gelockt op spoelstroom | Complex spectrum α(ω) | Spectrum ≈ verdeling van tijdconstanten ⇒ betere klassificatie; bodem-/achtergrondonderdrukking | Duurder in DSP; consumenten-boards hebben geen data-uitgang | Kelly Co / Adorama productpagina's Manticore (2023–2026) |
| **Pulsinductie (PI)** | Stroompuls 50–200 µs, uitschakelen, verval meten na 5–20 µs | v(t), multi-gate ⇒ vervalcurve | Ongevoelig voor statische achtergrond (zuil!), eenvoudige hardware (MOSFET + opamp + MCU-ADC), meet direct τ | Vroege τ (<10 µs: folie, dunne Cu) lastig door spoel-dempingstijd; ferro-discriminatie zwak zonder extra truc | Klassieke hobby-ontwerpen (Surf PI, Hammerhead, "Arduino PI") **[A: niet opnieuw geverifieerd]** |
| **Time-domain / eddy-current spectroscopie, magnetic polarizability tensor (MPT)** | Meet complex α(ω) of v(t) vanuit meerdere oriëntaties ⇒ 3×3 tensor per frequentie | Spectraal MPT-signatuur, rotatie-invariant | Wetenschappelijke basis voor klasse-ID van verborgen metaal (security, mijnen) | Vereist meerdere oriëntaties/spoelen + objectbibliotheek | Ledger & Lionheart; Wilson, Ledger & Lionheart, IJNME 2022; Özdeğer e.a., IEEE Sensors J 2023 |
| **Industriële tunneldetector (voeding)** | Gebalanceerde 3-spoelen tunnel, product beweegt erdoor | Fase + amplitude tijdens doorgang | Fe ≈1,5–2 mm bol detecteerbaar in kleine apertuur; apertuur ≈ product + 5 cm | Gevoeligheid ∝ apertuur⁻³ grofweg; vereist beweging; €10k+ **[A]** | Thermo Fisher FAQ; Fortress/Provisioner (2019–2024) |
| **Afval-sortering inductief** | Inductieve sensorlijst onder band (Steinert, Li-Tech NO 2025) | Metaal ja/nee + materiaal-indicatie | Bewezen in sortering, altijd **gecombineerd** met XRT/AI | Geen onafhankelijke data over inductie-alleen voor batterijen | Recycling Today (Steinert); Forskningsparken Li-Tech 2025; Fraunhofer IIS DangerSort 2025 (XRT+AI) |

Kernpunt: **geen enkele commerciële batterij-sorteerder vertrouwt op inductie alleen** (Steinert, Fraunhofer, VITO/Sortbat combineren met röntgen/beeld). Dat is een rode vlag voor uitgangspunt 3.

## 2. Fysica van de respons

Een object reageert met (i) een **magnetische** term (ferro: μr≫1, in fase met veld, frequentie-onafhankelijk bij lage f, *positieve* inductantieverandering) en (ii) **wervelstroom**-modes (elk een L-R-kring met τk; geven Q-component piek bij ωτ=1, in PI een e^(−t/τ)-staart). Eerste-orde τ:
- massieve bol: τ ≈ μσa²/π²; dunne cilinderschil (axiaal veld): τ ≈ μ0σ·a·d/2; ferro-wand diffusie: τ ≈ μrμ0σd².

### Schattingen per object (orde-grootte, scratchpad/tau.py)

| Object | Metaal | Ferro? | τ dominante mode | Anisotropie | Opmerking |
|---|---|---|---|---|---|
| **18650/21700 Li-ion** | Vernikkeld staal 0,2–0,3 mm **[A]**, σ≈6 MS/m, μr 100–300 **[A]**; binnen: Cu 8–10 µm + Al 12–15 µm spiraal | **Ja, sterk** | schil-lus ≈ 8 µs; wanddiffusie 50–140 µs; jellyroll transversaal ≈ 3–30 µs | Spiraal is **open** ⇒ axiale wervelstroom door rol vrijwel geblokkeerd; transversaal wel (lussen binnen één winding) | Signatuur ≈ "staal-staafje 18×65 mm" + kleine extra Cu/Al-staart. Blik-materiaal: forum endless-sphere (vernikkeld staal); sommige cellen Al-blik **[A]** |
| **AA alkaline LR6** | Vernikkeld staal blik; Zn-poeder-gel + MnO2 (slecht geleidend) | **Ja** | schil-lus ≈ 7 µs; geen sterke binnen-modes | Weinig | Lijkt sterk op 18650, ≈ ½ volume ⇒ **belangrijkste verwarring**. Li-ion 14500 (AA-maat) is van buiten niet te onderscheiden |
| **Pouch (telefoon, vape)** | Al-laminaatfolie ~40 µm **[A]**; stapel 15–30 Cu/Al-elektrodes | Nee (of klein: Ni-tabs) | folie ≈ 20 µs; **stapel ≈ 100–250 µs** (veld ⊥ vlak) | **Zeer sterk**: ⊥ vlak groot, ∥ vlak klein | Vlakke, gelaagde goede geleider ⇒ lange τ, groot. Toestel: + staalframe/shields + PCB |
| **Blikje 330 ml** | Al 3004, wand ~0,1 mm | Nee | ≈ 50 µs | Matig | Groot volume ⇒ groot signaal; τ overlapt met pouch-folie en munten |
| **Conservenblik** | Vertind staal | **Ja** | ~10–100 µs | Matig | Veel in restafval; **ferro-vals-alarm** voor magneet-concepten |
| **Aluminiumfolie** | Al 10–20 µm | Nee | vlak 30×30 cm ≈ 50 µs; verfrommeld ≈ 1–5 µs | Hoog als vlak | Verfrommeld ⇒ kortgesloten lussen klein ⇒ zwak + kort, PI-early-gate gevoelig |
| **Sleutelbos** | Messing/nikkel-zilver (non-ferro) + stalen ring | Deels | 30–200 µs (dikke plaat) | Gemengd | Lange τ zoals pouch-stapel; stalen ring ⇒ ferro-component |
| **PCB zonder accu** | Cu 35 µm vlakken, gaten | Weinig (componentjes, Ni) | 5–30 µs | Hoog | Grond-vlak = vlakke geleider, vergelijkbaar met kleine pouch-folie |

Conclusie fysica:
1. **18650 ≈ stalen buisje.** Inductie ziet vooral het stalen blik, niet de chemie. Onderscheid met AA-alkaline alleen via grootte (volume ∝ amplitude ~2×) — maar amplitude varieert door positie >100× (zie §3). ⇒ **"Li-ion vs alkaline" is met inductie alleen onbetrouwbaar** (hypothese; Ronde 3 kwantificeert).
2. **Pouch is juist wél karakteristiek** (lange τ + sterke anisotropie), maar botst met sleutels/munten/blikjes.
3. **Wh-schatting**: amplitude ∝ metaalvolume, niet ∝ Wh; cellen in een pakket (stalen/Al behuizing powerbank) worden één object. Hooguit grove klassen (geen / 1 cel / pakket).

## 3. Spoelgeometrie rond inworpopening (~40×40 cm)

Biot-Savart, vierkante lus 40×40 cm (scratchpad/tau.py), respons ∝ B_tx·B_rx ≈ B² (monostatisch):

| Positie object | B/B0 | Relatieve respons |
|---|---|---|
| midden, in vlak lus | 1,0 | 1 |
| 15 cm uit midden (5 cm van draad) | 1,9 | 3,5 |
| 2 cm van draad | 4,0 | 16 |
| 20 cm onder vlak, op as | 0,41 | 0,17 |
| 40 cm onder vlak | 0,12 | 0,015 |

⇒ **Dynamisch bereik ≈ 1000×** binnen de trommel alleen door positie. Afstand-schaling ver weg: dipool ~1/r⁶ zend-ontvang. Gevolgen:
- Grootte-/Wh-schatting uit amplitude vereist **lokalisatie** (meerdere spoelen, bv. 2 lussen boven/onder of 4 zijspoelen ⇒ verhouding geeft positie).
- **Trommel draait**: geeft gratis 2–4 oriëntaties ⇒ anisotropie/MPT-schatting mogelijk, mits de spoel meedraait of de trommel kunststof is.
- **Stalen zuil/trommel = grootste probleem**: bewegend staal (trommel, klep) geeft signaal ≫ 18650. Opties: (a) spoel op/in de trommel, meedraaiend (statische achtergrond, wegbalanceren); (b) trommelbak vervangen door HDPE/GVK-inzet **[A: retrofit-kosten €150–400]**; (c) PI met differentiële meting "zelfde trommelstand, vóór vs na inworp".
- Doorvoerspoel/gradiometer in de valweg onder de trommel: veld uniformer (zoals voedingstunnel), maar meettijd ≈ 0,1–0,3 s en valschacht vaak staal.

## 4. Langer meten (uitgangspunt 1)

- Witte ruis: SNR ∝ √N. PI 1 kHz × 5 s ⇒ N=5000 ⇒ +37 dB. Met dipool 1/r⁶: bereik × 5000^(1/12) ≈ **×2**. VLF lock-in: bandbreedte 0,2 Hz i.p.v. 50 Hz: vergelijkbaar.
- Maar de **beperkende factor is clutter** (ander metaal in dezelfde zak) en **drift** (temperatuur spoel ~ppm/K, trommel-positie ±mm, 50 Hz netstoring, vrachtwagen/fiets in de buurt), niet witte ruis. Middeling boven ~0,5–1 s wint weinig.
- ⇒ Uitgangspunt 1 **deels waar**: stilstand maakt goedkope MCU-ADC (12 bit) bruikbaar en levert meerdere oriëntaties; het lost het discriminatieprobleem niet op. Container-continue inductie (uren) heeft geen meerwaarde: object verandert niet.

## 5. Componenten en prijzen (2026)

| Onderdeel | Prijs | Bron / status |
|---|---|---|
| TI LDC1612 (2-kan., 28 bit, L-meting via LC-resonantie) | ≈ €1,5 (ref. $1,65, LCSC, voorraad 0) | LCSC C202191, bekeken 2026-10 |
| TI LDC1101 (RP+L, 24 bit, tot 10 MHz) | ≈ €4,3 (Digikey $4,71, stuks) | Digikey, 2026-10 |
| LDC1612EVM | €168 (RS) | RS, 2026-10 |
| Beperking LDC-chips | Bereik ≈ 0,5–1× spoeldiameter, sensorfrequentie 1 kHz–10 MHz, bedoeld voor mm-afstand | TI datasheet **[A: niet herlezen]** |
| DIY PI: MCU (STM32G4/RP2040 €1–4), MOSFET 500 V €0,5, opamp/comparator €1, Cu-lus 1 m² €5–10, voeding | BOM elektronica **€15–30** | **[A]** schatting |
| DIY multi-freq VLF: MCU met DAC/ADC + klasse-D-driver + 2 opamps, DD-spoel | **€25–50** | **[A]** |
| Hobbydetector Minelab Vanquish 340 (multi-freq) | €199 incl. = **€165** excl. | MediaMarkt AT, 2026-07 |
| Garrett Ace 300i | €299 incl. = €247 excl. (ongedateerd) | paslaugos.lt |
| Hobby-boards hebben **geen data-uitgang**; reverse-engineeren/audio-uitgang afluisteren = hack, geen product | — | eigen analyse |
| Industriële tunnel-metaaldetector (voeding) | €8k–25k **[A]** | prijs niet gevonden |
| TI IWR6843 (60 GHz radar, chip) | $43–63 stuks (Mouser, ongedateerd); modules €100–300 **[A]** | Mouser |
| AMR-magnetometer 3-as (MMC5983MA / QMC5883L) | €1–4 **[A]**; ruis ~40 nT (MMC5983) **[A]** | niet geverifieerd |
| Fluxgate-module | €50–300 **[A]** | niet geverifieerd |

## 6. Alternatieve EM-principes (kort)

| Principe | Wat ziet het | 18650 vs rest | Verdict |
|---|---|---|---|
| **Magnetometrie (passief/aardveld)** | Geïnduceerde dipool van staal. 18650 in 50 µT: m ≈ 7·10⁻³ A·m² ⇒ ≈170 nT op 20 cm **[A, eigen berekening]** | Ziet ALLE ferro: AA, conservenblik, kroonkurk, schroeven | Goedkoop (€5), maar alleen "ferro-teller" |
| **Magnetometrie + DC-bias / magnetisatiepuls** | Remanentie & hysterese (zacht vs koud-vervormd staal); harmonischen (2f/3f) alleen van ferro | Dieptrekstaal van celblikken vs blikstaal: verschil onbekend | Onconventioneel, niet bewezen ⇒ R3-check |
| **Radar / mmWave (60–77 GHz)** | Metaal = perfecte reflector; dringt niet in metaal | Geen discriminatie batterij vs blik zonder beeldvorming; vocht/organisch diffuus | Nuttig voor vulgraad, niet voor batterij **[A]**. Walabot: actuele status niet gevonden |
| **Capacitief / diëlektrisch** | ε van inhoud; nat afval domineert | Geen specifiek batterij-signaal | Afgeraden |
| **Magnetische inductie-tomografie** | Ruimtelijke σ-kaart | Veel spoelen, complex | Te duur voor zuil |

## 7. Wat ik niet kon vinden
- Gemeten wanddikte/μr van 18650-blikken (teardown-data); gemeten PI-vervalcurves van Li-ion-cellen vs AA in de literatuur.
- Onafhankelijke cijfers voor inductie-alleen batterijdetectie in afval (alleen leveranciersclaims, altijd multisensor).
- Materiaal/wanddikte van NL-inworptrommels (staal vs RVS vs kunststof) — vraag aan A5.
- 1k-prijzen LDC-chips; actuele prijs/beschikbaarheid industriële tunneldetectoren.

## 8. Simulatieplan Ronde 3 (experiments/A2_inductie_sim/)

**Model-keten**: object-polariseerbaarheid α(ω) (3×3 tensor) → spoelgeometrie (Biot-Savart, reciprociteit V = jω·B_tx·α·B_rx / (μ0·I)) → ruis/drift/clutter → features → ROC.

| Object | Model | Parameters (laag/basis/hoog) |
|---|---|---|
| 18650 / 21700 | Permeabele geleidende **cilinderschil**: magnetische term α_m (demagnetisatiefactor N_ax≈0,1, N_tr≈0,45) + schil-mode τ=μ0σad/2 + wand-diffusiemode τ=μrμ0σd²; jellyroll als transversale eddy-mode met axiale onderdrukking ε=0,05/0,1/0,3 | d 0,2/0,25/0,3 mm; μr 50/150/400; σ 4/6/8 MS/m |
| AA alkaline | Zelfde schilmodel zonder jellyroll, a=7 mm, l=50 mm | idem |
| Pouch | Anisotrope gestapelde plaat: α_⊥ met 2–3 modes (folie ~20 µs, stapel 100–250 µs), α_∥ = 0,05–0,2·α_⊥ | lagen 10/20/40 |
| Blikje | Dunne Al-cilinderschil, τ≈50 µs (+ bodem als schijf) | d 0,08/0,1/0,12 mm |
| Al-folie | Vlak: schijf-mode; verfrommeld: N willekeurige kleine lussen (a 3–15 mm) ⇒ τ 1–10 µs | — |
| Sleutelbos | 3–6 platen (messing, τ 30–200 µs) + stalen ring (ferro-term) | — |
| Referentie | **Wait-model** (Wait 1951; Ward & Hohmann 1988) permeabele geleidende bol, analytisch, voor validatie (limieten: lage f ⇒ 2(μr−1)/(μr+2); hoge f ⇒ −1) | — |

Responsvormen: VLF/multi-freq α(ω)=Σ Ak·jωτk/(1+jωτk) − χm; PI v(t) ∝ Σ (Ak/τk)·e^(−t/τk) na ideale stap (met spoel-dempingstijd 5–15 µs als blinde zone).

**Monte-Carlo**: zakken met 0–3 clutter-objecten (verdeling met A1/A6), willekeurige positie/oriëntatie in 40×40×40 cm, 1–4 trommelstanden, ruis σ met middeling N, drift + bewegend-staal-restsignaal. Uitvoer: ROC "≥1 Li-ion cel" en "Wh-klasse", per concept (1 lus / 2 lussen / 4 spoelen; PI vs 5-freq). Tests: 18650 vs AA, pouch vs sleutelbos, cel in stalen apparaat (afscherming).
