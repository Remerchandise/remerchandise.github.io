# R3 – A2 Inductie: resultaten (K1 strandmetaaldetector, K2 pakketwachter)

Draaien: `python3 experiments/r3_inductie/sim_inductie.py` vanuit de repo-root. Het script is deterministisch (vaste seeds), duurt ~70 s en schrijft `sensor_model_K1.json`, `sensor_model_K2.json`, `resultaten.json` en de figuren. Objectmodellen staan in `objects.py`. Itemklassen en zakinhoud komen uit `experiments/common/params.py`. Pakket = powerbank, laptop/gereedschap en e-bike (PACK_WHEQ = 20, besluit Orchestrator).

## Modelketen (methode)
1. **Object → polariseerbaarheidstensor.** Elk object is een som van modes in de dipoolbenadering, met per mode een diagonale tensor en een tijdconstante τ:
   - **Ferro-term**, voor VLF: M/(1+jωτw).
   - **Wervelstroom-modes**, voor VLF: −A·jωτ/(1+jωτ).
   - **PI-verval**: g(t) = Σ p·(t0/τ)·e^(−t/τ).

   De parameters volgen uit formules voor een dunne cilinderschil, een dunne schijf en een ferro-schil met demagnetisatie (`objects.py`, **[A]**). Varianten per klasse zijn onder meer: 18650/21700, AA/AAA/C, vape met Al-huls of kunststof en pouch of 13350-cel, telefoon met of zonder Al-frame, powerbank met n = Wh/11,5 cellen en Al- of kunststofbehuizing, gereedschaps- versus laptoppack, Al- versus stalen blik (geplet), folieprop versus vlak vel, sleutelbos versus schroeven/munten, stalen versus Al-pan, en PCB plus kleine ferro-delen. Overal ±15 % spreiding.
2. **Spoel.** Vierkante lus van 40×40 cm in de opening (T). K2 heeft een tweede lus in de bodem (B). Het veld volgt uit Biot-Savart. Respons = h_txᵀ·R·α·Rᵀ·h_rx, met willekeurige positie (kubus van 34 cm) en willekeurige oriëntatie.
3. **Zak.** Het doel-item plus realistische clutter, getrokken uit params.ITEMS (gemiddeld 5,9 metaalobjecten per zak; 78 % van de zakken bevat ≥ 3). De signalen tellen lineair op (superpositie).
4. **Ruis [A]**, uitgedrukt in cm³-equivalent in het lusmidden (laag/basis/hoog):
   - wit: 0,6/2/6 per 1 ms, gaat omlaag met √(T·1000);
   - driftvloer: 0,1/0,3/1;
   - restsignaal van de RVS-trommel en de verzinkte zuil met de spoel meedraaiend: 0,5/2/20, met een spectrale vorm (RVS-eddy τ 260 µs + ferro-zuil 5 ms).

   Ter vergelijking: een 18650 geeft gemiddeld over oriëntaties ≈ 37 cm³ in het lusmidden. Draait de spoel niet mee met de trommel, dan is de rest ≥ 200 (zie §5).
5. **Kenmerken.**
   - K1: I/Q bij 5, 15 en 40 kHz op één lus.
   - K2: 5 PI-vensters (10–810 µs) × 3 kanalen (TT, BB, TB) + ferrokanaal (Re α bij 1 kHz) op T en B.
   - Classifier: kNN (k = 31, klasse-gebalanceerd).
6. **Werkpunt.** Op Li-loze realistische zakken staan de drempels op 0,2 % vals "pakket" en 2 % vals "≥ cel" per zak. ROC-curves voor andere werkpunten staan in `fig_roc.png`.

## Test 1 – Responsspectra en vervalcurven (`fig_spectra.png`, `fig_decay.png`)
| Object | Ferro (I > 0 bij lage f)? | Overgangsfrequentie I+ → I− | Dominante τ |
|---|---|---|---|
| 18650 | ja, M ≈ 25–61 cm³ | ≈ 5 kHz | 8 µs schil, 50–140 µs wand |
| AA alkaline | ja, ≈ ½ × 18650 | ≈ 10 kHz | idem |
| Powerbank (4×18650) | ja, ≈ n × 18650 | ≈ 2 kHz (+ Al-behuizing) | + 150–400 µs |
| Telefoon, vape, laptoppack | nee (kleine ferro-delen) | – | 15–200 µs |
| Al-blik | nee | – | ≈ 50 µs, A ≈ 500–600 cm³ (10–20 × 18650) |
| Stalen blik, pan | ja, zeer groot (100–3000 cm³) | < 3 kHz | ms |

**Conclusie:** per object zijn er duidelijke verschillen. Het 18650-signaal is een geschaalde AA plus een kleine staart van de jellyroll.

## Test 2 – Scheidbaarheid van losse objecten (Fisher-LDA, basisruis, T = 2 s)
| Paar | K1 AUC | K2 AUC |
|---|---|---|
| 18650 ↔ AA alkaline | 0,73 | 0,87 |
| telefoon ↔ sleutels/klein metaal | 0,81 | 0,96 |
| powerbank ↔ pan/gereedschap | 1,00 | 1,00 |
| vape ↔ blik | 0,94 | 1,00 |
| vape ↔ folieprop | 0,75 | 0,65 |

Dit is de bovengrens, met één object in de trommel. `fig_feature_space.png` laat zien dat de fase/amplitude-clusters sterk overlappen. De schaal-invariante kenmerken van K2 (vervalhelling, ferro-ratio) scheiden de pan, maar niet cel ↔ blik ↔ folie.

## Test 3 – Realistische zak (hoofdresultaat)
P(uitvoer) = [geen, cel, pakket] bij basisruis en T = 2 s. Links het item alléén, rechts **in een realistische zak**.

| Item | K1 alleen | K1 in zak | K2 alleen | K2 in zak |
|---|---|---|---|---|
| alkaline | .90/.10/.00 | .95/.05/.01 | .98/.02/.00 | .97/.03/.00 |
| pan/gereedschap | .98/.00/.01 | .93/.04/**.03** | .99/.01/.00 | .92/.03/**.05** |
| vape | .99/.01/.00 | .96/.04/.00 | .96/.04/.00 | .98/.02/.00 |
| 18650 | .67/.32/.01 | .87/**.13**/.01 | .81/.19/.00 | .91/**.09**/.01 |
| telefoon | .84/.17/.00 | .94/.06/.00 | .71/.29/.00 | .94/.06/.00 |
| powerbank | .45/.33/.22 | .78/.13/**.10** | .36/.46/.18 | .81/.16/**.03** |
| laptop/gereedschap | .38/.28/.34 | .76/.17/**.08** | .30/.55/.14 | .80/.16/**.05** |
| e-bike/step | .13/.18/.69 | .38/.16/**.46** | .20/.06/.74 | .24/.06/**.71** |
| *Li-loze zak (vals)* | – | .98/.017/.002 | – | .98/.020/.003 |

Kerncijfers (laag / basis / hoog ruis; "ideaal" = ruisloos):

| | K1 | K2 |
|---|---|---|
| Recall "pakket", energiegewogen, in zak | 0,23 / **0,25** / 0,21 (ideaal 0,23) | 0,33 / **0,32** / 0,08 (ideaal 0,18 *) |
| Li-energie met uitvoer ≥ cel | 0,24 / 0,26 / 0,21 | 0,32 / 0,27 / 0,09 |
| Extra miskans Li door n = 0/1/2/3+ metaalobjecten | 0 / .17 / .33 / .55 | 0 / .18 / .30 / .52 |
| AUC pakket ↔ clutterzak | 0,81 | 0,82 |
| AUC 18650/telefoon/vape ↔ clutterzak | 0,59 | 0,56 |

\* De kNN-schatting is onstabiel bij ruisloze kenmerken. Ruis in de ordegrootte van de spreiding ±0,05–0,1 in recall verandert de conclusie niet.

**PPV-afleiding.** Per zak geldt P(pakket-item) ≈ 0,0015 (params, basis). Count-gewogen recall pakket: K1 ≈ 0,12, K2 ≈ 0,06. Bij 0,2 % vals pakket per zak volgt:
- **PPV ≈ 8 % (K1) en ≈ 3 % (K2).**
- Per containerlediging (100 zakken): ≈ 0,2 valse en ≈ 0,02 terechte pakketmeldingen.
- Voor "≥ cel" is de AUC ≈ 0,56–0,59, dus nauwelijks beter dan toeval.

**Conclusie Test 3:**
1. **De beperking is clutter, niet ruis of meettijd.** Laag, basis en ideaal geven dezelfde recall voor K1. Alleen hoog restsignaal van de trommel (K2) maakt het slechter.
2. **Losse cellen, telefoons en vapes zijn in een echte zak inductief niet te detecteren** (AUC ≈ 0,56–0,59). Uitgangspunt 3 als Li-detector: **verworpen**.
3. **Alleen een e-bike-/steppack** (n ≥ 20 cellen) wordt bruikbaar herkend (46–71 %). Powerbanks en gereedschapsaccu's worden voor 90–97 % gemist bij een acceptabel vals-alarmniveau.
4. **K2 is in deze opzet niet beter dan K1.** Twee lussen en PI-vensters helpen bij losse objecten (AUC 0,87–0,96), maar in de zak domineert de superpositie met blikjes en pannen. Een sterkere classifier dan kNN kan dit iets verbeteren. Het overlap-mechanisme blijft: een powerbank lijkt op een stalen blik plus wat staal.

## Test 4 – Positie en meettijd (`fig_meettijd.png`)
- **Positiespreiding** (één lus, isotroop object): P99/P1 = **171×** (P5–P95 ≈ 60×). Dat is minder extreem dan de 1000× die ik in R0 schatte; die R0-schatting omvatte ook de positie vlak naast de draad.
- **Wh-schatting K2** (lineaire regressie op de kenmerken, Li-items van 18650 tot laptop): σ(ln Wh) = **0,63 alleen / 0,73 in zak** (σ log10 = 0,27 / 0,32, dus een factor ≈ 2). Dat is **boven** het A1-criterium σ_ln ≤ 0,5. Grof (klasse) kan het wel, fijn niet.
- **Meettijd.** De witte ruis daalt met √N, maar de driftvloer plus de trommelrest worden al na **≈ 10–20 ms** dominant. SNR van een 18650 op een ongunstige positie (P5) bij T = 0,1 / 2 / 10 s:
  - laag: 1,3 / 1,3 / 1,3
  - basis: 0,33 / 0,33 / 0,33
  - hoog: 0,03 / 0,03 / 0,03

  Zonder trommelrest stijgt de SNR tot ≈ 2 bij T ≥ 0,3 s. Een K1-run met T = 0,2 s gaf dezelfde recall als met 2 s (0,25).

  **Uitgangspunt 1 (langer meten) levert voor inductie niets op boven ~0,3 s.** De stilstand is wel nodig voor een stabiele trommelpositie (achtergrondaftrek).

## Test 5 – RVS-trommel en stalen zuil
De RVS 304-trommel (≈ 0,2 m², 1,5 mm) heeft een equivalente polariseerbaarheid van grofweg 10⁴ cm³ op enkele cm van de spoel, ≈ 300× een 18650. Gevolgen:
- **Spoel niet meedraaiend:** een positieherhaalbaarheid van ±1 mm geeft al een rest ≥ 100–300 cm³. Dat is **KO** voor elke celdetectie.
- **Spoel meedraaiend, op afstandhouders van ≥ 3 cm van het RVS:** rest 0,5–20 cm³ **[A]**, gedomineerd door temperatuur (RVS σ ≈ −0,1 %/K) en de verzinkte zuil. Dit is alleen met een prototype te bevestigen.

## Alleen met prototype te bevestigen + labtestontwerp
| Wat | Opstelling | Testobjecten | Protocol | n |
|---|---|---|---|---|
| Echte responsen (valideer `objects.py`) | PI- en VLF-board (5/15/40 kHz) + lus van 40×40 cm op houten mal, buiten metaal ≥ 1 m | 18650 (5 merken, Ni-staal + 1 Al-blik), 21700, AA/AAA/C (alkaline + 14500 Li-ion), 3 telefoons, 5 vapes, 3 powerbanks, 2 gereedschapsaccu's, 1 laptoppack, Al- en stalen blikjes (heel + geplet), folieprop, sleutelbos, pan, hamer, PCB | Object op XYZ-raster (5×5×5, 8 cm) × 6 oriëntaties; I/Q en vervalcurve 2–1000 µs | ≥ 30 objecten × 750 metingen |
| Trommelrest | Echte RVS-trommel (A5-type) met meedraaiende spoel, zuil eromheen | leeg + referentie-18650 in het midden | 200 open/sluitcycli, −10…+40 °C (klimaatkast/buiten), restsignaal versus cyclus en T | 200 cycli × 3 temperaturen |
| Superpositie en zakken | Idem in de trommel | 300 samengestelde zakken (realistische clutter volgens params) met en zonder Li-item, blind gelabeld | Meting 2 s; classifier trainen op de helft en testen op de andere helft | n ≥ 300 (A6 #7) |
| Valkoker-variant (A2-C5) | Optioneel: tunnelspoel 50×50 cm, zak laten vallen | dezelfde zakken | Doorgang 0,2 s | 100 |

**Doorslaggevende test:** recall "pakket" bij ≤ 0,2 % vals per zak in echte zakken. Valt deze < 30 % (simulatie: 3–10 % voor een powerbank), dan vervalt inductie ook als pakketwachter. Dan blijft hooguit een e-bike-accu-alarm over.

## Conclusie voor de shortlist
- **K1 (strandmetaaldetector)** detecteert in een realistische zak: 18650 ≈ 13 %, powerbank ≈ 22 % (≥ cel), bij 2 % vals per zak. PPV als Li-detector ≪ 50 % → **KO op checklist B1/A3**.
- **K2 (pakketwachter)**: PPV voor pakketmeldingen 3–8 %. Alleen e-bike/step betrouwbaar. Niet zelfstandig verkoopbaar. Hooguit als zwakke prior (likelihood ratio "pakket"-uitvoer ≈ 15–50 voor een groot pack) binnen K5, mits A6 laat zien dat de rangorde dit oplevert.
