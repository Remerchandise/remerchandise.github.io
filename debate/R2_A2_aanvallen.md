# R2a – A2 valt aan (EM/fysica + kosten/praktijk)

Ernst: **KO** / zwaar / licht. Getallen zijn eigen schattingen, tenzij er een bron staat. **[A]** = aanname. Dempingscoëfficiënten (μ/ρ) zijn NIST XCOM-orde-waarden uit mijn hoofd en nog niet opnieuw opgezocht **[A]**.

## A3 – Röntgen

| Concept | Kritiek | Ernst | Wat redt het |
|---|---|---|---|
| A3-C1 Schaduwdoos | **De trommel is RVS 304 (A5) en ligt in de bundel.** Fe bij 20 keV: μ/ρ ≈ 26 cm²/g, dus μ ≈ 200 cm⁻¹. Door 1 mm RVS komt e⁻²⁰ ≈ 0 door. "Het trommelstaal is tegelijk de afscherming" botst met "door de zak heen kijken". Ook als de buis en het scherm ín de trommel zitten: 40 cm zak van ~0,15 g/cm³ is ≈ 6 g/cm² water. Transmissie bij 20 keV ≈ e⁻⁴·⁹ ≈ 0,7 %, bij 30 keV ≈ 10 %. Bij een 1–4 W-buis plus een lichtkoppeling van 10⁻³ (camera op scherm) is het beeld fotonarm. | **KO** zonder een herontwerp van de trommel | Kunststof (HDPE) trommelinzet of een Al/CFRP-venster in het bundelpad. Laat een fotonenbudget zien: kwanta per pixel achter 6 g/cm² plus 2 zakwanden |
| A3-C1/C2 | **Alkaline en Li-ion zijn allebei volledig zwart.** Twee stalen wanden van 0,25 mm bij 30 keV: μ ≈ 65 cm⁻¹, dus ≈ e⁻³·². Daarbij komen Zn/MnO2 of de Cu-jellyroll. Een 14500 Li-ion en een AA hebben exact dezelfde vorm. Volgens A8 zijn 394 van de 395 losse batterijen alkaline, dus het vormherkennende CNN telt vooral alkaline. Dat is hetzelfde probleem dat inductie heeft. | zwaar (checklist A3) | Alleen A3-C3 (60–80 kV, dual-energy) ziet de jellyroll tegenover de Zn-gel. Of: alkaline als Wh-eq meetellen en dat eerlijk claimen |
| A3-C2 Trommelscan | De lijnarray staat op de *vaste* zuilwand en de RVS-trommel draait ertussen. Dan zit er tijdens de scan 1–2 mm staal in de bundel (zie boven). De zak tuimelt tijdens de 1–3 s rotatie, waardoor het beeld vervormt en cellen dubbel geteld of gemist worden. | **KO** zoals beschreven | Sleuf of venster in de trommel dat meedraait. Scannen in de eindstand, niet tijdens het tuimelen |
| A3-C1/C2 kosten | €35–70 per container per maand, tegenover vermeden schade van ~€3 per container per maand (A7). Dat is 10–20× te duur. | **KO** als een unit per container | Alleen als rouleerunit (A3-C4) of op hotspots |
| A3-C4 Teacher | Sterk idee. Risico: labels sluiten alleen aan als de goedkope sensor dezelfde trommel en dezelfde zakpositie ziet. Een röntgenmodule in de trommel verandert ook de metalen omgeving van de inductiespoel (buis en afscherming = veel metaal), dus de kalibratie wordt niet zomaar overdraagbaar. | licht | De inductiekalibratie meten met en zonder de röntgenmodule, en de module met kunststof bevestigen |

## A4 – Thermisch/gas

| Concept | Kritiek | Ernst | Wat redt het |
|---|---|---|---|
| A4-C3 Waakstand op A2-trigger | Volgens A8 bevat ≈ 85 % van de zakken metaal. Een inductietrigger op "metaal" vuurt dus bij bijna elke inworp: de waakstand staat altijd aan, en er komt geen energiewinst en geen vermindering van vals alarm. Mijn eigen analyse (research/A2): ook een trigger op "stalen cilinder" wordt gedomineerd door AA-alkaline. | zwaar | Triggeren op een smalle klasse (A2-C3: groot pakket, of meerdere parallelle stalen cilinders). De prior expliciet zwak maken (likelihood ratio ≈ 1,5–3 **[A]**) |
| A4-C5 Vape-neus | Een dichtgeknoopte PE-zak en luchtverversing via een open trommel. Een BME688-respons in 2–10 s is onbewezen (A4 zegt dat zelf). E-liquidgeur zit ook op lege vape-verpakkingen. Pluspunt: dit is precies het gat dat inductie laat (vape ≈ klein Al-buisje, lijkt op een blikje of koffiecup). | zwaar | Fysieke test met 20 dichte zakken. Inzetten als aanvulling op inductie, niet los |
| A4-C1 / C7 | De fysica klopt, maar het is branddetectie en geen preventie. Volgens A4 zit het hoofdrisico in de wagen (stap 5) en daar is geen meetvenster. Dominantietest D3: een thermische camera op de wagen dekt 100–150 containers. | licht | Verkopen als goedkope add-on op een bestaande vulgraadsensor (€1–2 per maand), niet als kernproduct |
| A4-C4 Plop | Een vent-plop van enkele Pa onder ≥ 1 m afval, tegen inworpgeluid, verkeer en regen op een stalen deksel: de SNR is onbekend. | licht | Akoestische meting in een gevulde container |

## A1 – Risicoconcepten

| Concept | Kritiek | Ernst | Wat redt het |
|---|---|---|---|
| A1-C1 Teller-met-basislijn | **Het signaal verdrinkt in Poissonruis.** Per lediging ~400 inworpen **[A]**, waarvan ~85 % met metaal: ≈ 340 ± 18 metaaltellingen. De ~3,6 Li-items vallen daar ruim binnen (< 0,2σ). De regel "×3 voortschrijdend gemiddelde" meet dan drukte, niet accu's. "Elke detectie = 6 Wh-eq" heeft geen fysische basis. | **KO** als accu-indicator | Alleen tellen in een smalle, sterk ferromagnetische klasse met lokalisatie (A2-C3), en de A3-C4-ijking gebruiken om de klassekans te bepalen |
| A1-C2 Pareto | Dit past het best bij inductie: een powerbank of e-bike-pack = N parallelle stalen cilinders, met een groot, anisotroop en ferromagnetisch signaal. Maar een pan, gereedschap, conservenblik of laptopchassis (Mg/Al plus PCB) geeft een vergelijkbare amplitude, en de positie varieert het signaal ~1000× (research/A2 §3). | zwaar | Meerdere spoelen voor lokalisatie, plus het τ-spectrum en een array-patroon herkennen. Dit is mijn voorkeurscombinatie voor R3 |
| A1-C5 Accu-sluis | Met inductie plus weegcel is fraude triviaal: een stalen buisje van 18×65 mm of bouten "zijn" een 18650, en punten worden geld. Het concentreren van Li-cellen in de zuil schept bovendien zelf een brandhaard (E3). | zwaar | Beloning alleen na handmatige of röntgencontrole bij lediging, of een vaste beloning per inworp zonder Wh-weging. Een brandwerende bak |
