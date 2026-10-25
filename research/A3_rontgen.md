# A3 – Röntgen met stilstand (Ronde 0: research)

Agent 3 · peildatum 2026-10-25 · EUR 2026 excl. btw · aannames **[A]** · rekenscripts: `experiments/A3_r0_attenuation.py`, `experiments/A3_r0_photonbudget.py`

## 0. Kernbevindingen (TL;DR)

| # | Bevinding | Zekerheid |
|---|-----------|-----------|
| 1 | **Vergunningsvrij röntgen is juridisch mogelijk**: Bbs art. 3.18 lid 1 onder b stelt handelingen met een toestel dat werkt bij **≤ 30 kV** (of van een **door de ANVS goedgekeurd type**) vrij van Afdeling 3.2 (kennisgeving/registratie/vergunning), mits **≤ 1 µSv/h op 0,1 m van elke bereikbare buitenzijde** onder normale bedrijfsomstandigheden. Onder c: apparatuur ≤ 5 kV (fysisch onbruikbaar). | Hoog (tekst via meerdere secundaire bronnen, zie §6); geconsolideerde versie 2025/26 zelf niet kunnen inzien |
| 2 | **30 kV is fysisch genoeg** om een zak restafval (≈ 6 g/cm²) te doorlichten (T ≈ 2–5 % na spectrumverharding) en cellen als **volledig opake objecten** te zien (18650: µt ≈ 24 bij 30 keV). Een stalen behuizing van 2–3 mm schermt 30 kV vrijwel volledig af (T ≈ 10⁻⁶ bij 30 keV). | Hoog (berekend) |
| 3 | **Bron is níet de bottleneck, detector wel.** 30 kV / 1 W geeft ~10³ fotonen/mm²/s áchter de zak op 0,6 m; 5 s stilstand → ~5·10³/mm². Stilstand maakt een **goedkope lens-gekoppelde detector** (GOS-scherm + camera, efficiëntie 10⁻³) bruikbaar – dáár zit de waarde van uitgangspunt 1. | Middel (orde-grootte, Kramers-model) |
| 4 | **Li-ion vs alkaline is met transmissie/dual-energy nauwelijks te onderscheiden** (zelfde vorm 14500/AA; R-waarde 11,5 vs 12,4; bij 30 kV beide opaak). Onderscheid alleen via **vorm/interne structuur** (≥ 60 kV, ≤ 0,5 mm resolutie) of context (telefoon, powerbank, e-sigaret, laptop = herkenbaar). Wel goed onderscheid t.o.v. Al-blik, folie, glas (transparant) en grotendeels t.o.v. sleutels/bouten (vorm). | Middel |
| 5 | **Radioactieve bron = knock-out.** Am-241 op vrijstellingsniveau (10 kBq) → 100 fotonen/pixel kost ~35 uur; sterkere bronnen vergunningplichtig, diefstal/zoekraakrisico in openbare ruimte, en AVI-poortmonitors alarmeren juist op radioactiviteit. | Hoog |
| 6 | Bestaande batterijdetectie met röntgen zit **alleen in sorteer-/verwerkingsinstallaties** (Visia, Fraunhofer DangerSort, PFU/Ricoh, TOMRA/Steinert XRT). Röntgen bij de inworp of in vuilniswagens: **niet gevonden**. | Middel |

## 1. Bronopties

| Optie | Spanning/energie | Vermogen | Prijs 2026 laag/basis/hoog **[A]** | Regelgeving NL | Oordeel |
|-------|------------------|----------|-----------------------------------|----------------|---------|
| Chinese mini-buis vaste anode (portable NDT/tandheelkunde) + HV-module | 30–50 kV | 1–50 W | 400 / 1 200 / 3 000 | ≤ 30 kV + ≤ 1 µSv/h → vrijgesteld (3.18-1b) | **Kandidaat** (instelbaar begrenzen op 30 kV, hardware-limiet!) |
| Moxtek MAGPRO (–6 tot –50 kV, 12 W, 50–1000 µA) [QD Europe datasheet, geraadpleegd 2026-10] | ≤ 50 kV | 4–12 W | 3 000 / 6 000 / 10 000 | > 30 kV → registratie, tenzij typegoedkeuring | Industriekwaliteit, te duur voor C1 |
| Amptek Mini-X2 (50 kV, 4 of 10 W, 5–200 µA; 70 kV-versie vervallen) [amptek.com, 2026-10] | ≤ 50 kV | 4–10 W | 8 000 / 12 000 / 16 000 | idem | Lab-instrument, te duur |
| Hamamatsu microfocus / monoblok 60–150 kV | 60–150 kV | 10–75 W | 5 000 / 10 000 / 25 000 | registratie of typegoedkeuring | Alleen voor C3 |
| Pyro-elektrische bron (Amptek COOL-X-type) | eindpunt tot ~35 keV | µW–mW, cyclisch | 1 500 / 3 000 / 5 000 | Juridisch onduidelijk (geen "potentiaalverschil" van voeding; eindpunt > 30 keV) | Onconventioneel; flux waarschijnlijk te laag – **niet geverifieerd** |
| Am-241 (59,5 keV, 36 %) vrijstellingsactiviteit 10 kBq | 59,5 keV | – | < 100 | vrijgesteld, maar fysisch nutteloos | **KO** |
| Am-241 / Cs-137 / Co-57 GBq-bron | 60–662 keV | – | 2 000–10 000 + borging | vergunning, beveiliging, afvoer | **KO** |

Fotonbudget (W-anode, Kramers, 0,5 mm Al filter, pixel 1 mm² op 0,6 m, zak 6 g/cm²; overschatting ~2× **[A]**):

| Bron | X-straalvermogen | fotonen/mm²/s zonder zak | achter zak | Ē achter zak |
|------|------------------|--------------------------|------------|--------------|
| 30 kV, 1 W | 2,4 mW | 4,8·10⁴ | 1,1·10³ | 23,8 keV |
| 30 kV, 4 W | 9,8 mW | 1,9·10⁵ | 4,3·10³ | 23,8 keV |
| 50 kV, 4 W | 16 mW | 4,4·10⁵ | 3,5·10⁴ | 32,7 keV |
| 80 kV, 10 W | 65 mW | 1,8·10⁶ | 2,4·10⁵ | 43 keV |
| Am-241 10 kBq | – | 8·10⁻⁴ | – | 59,5 keV |

Conclusie: een **zwakke bron met lange belichting volstaat ruim** voor een schaduwbeeld (100 fotonen/pixel achter de zak in < 0,1 s bij 30 kV/1 W met een efficiënte detector). Lange belichting (1–10 s) is nodig om een **inefficiënte, goedkope detector** te compenseren, niet de bron.

## 2. Detectoropties

| Detector | Principe | Resolutie | Efficiëntie bij ~25 keV | Prijs laag/basis/hoog **[A]** | Past bij |
|----------|----------|-----------|--------------------------|-------------------------------|----------|
| GOS/CsI-versterkingsscherm 35×43 cm + spiegel + camera (RPi HQ/IMX-sensor, f/1,2) | lens-gekoppeld, 2D | 1–3 mm na binning | ~10⁻³ lichtkoppeling → ~0,5–1 e⁻ per röntgenfoton (quantum sink, compenseren met 5–10 s + binning) | 150 / 400 / 900 | **C1** (stilstand essentieel) |
| Lijnarray CsI:Tl + Si-fotodiodes, 64–128 kanalen, 1,6–3 mm pitch (zelfbouw / goedkope OEM) | 1D, scan door beweging | 1,6–3 mm | 50–80 % | 300 / 900 / 2 000 | **C2** (trommelrotatie = scan) |
| Industriële LDA (Detection Technology X-Scan/AVA, dual-energy sandwich) | 1D, dual-energy | 0,4–1,6 mm | > 80 % | 2 000 / 5 000 / 10 000 (geen lijstprijs gevonden) | C3 |
| Flatpanel CMOS/a-Si 43×43 cm | 2D direct | 0,1–0,2 mm | > 60 % | 4 000 / 9 000 / 20 000 | te duur per container |
| Losse CdTe/CZT spectroscopische detector (bijv. Amptek XR-100CdTe) | 1 pixel, energieresolutie | – | ~100 % | 4 000 / 6 000 / 9 000 | Alleen Z-meting in 1 punt → onbruikbaar voor zak |
| Scintillator + SiPM, 8–16 losse kanalen | "spikkel"-detectie, geen beeld | grof (cm) | hoog | 150 / 400 / 800 | onconventioneel: telt opake objecten, geen vorm → weinig discriminatie |
| Backscatter (bron + detector zelfde zijde) | Compton-terugstrooiing | grof | laag, alleen oppervlak zak | — | Eenzijdige montage voordeel, maar cel in zakkern onzichtbaar → afgewezen |

## 3. Massieke verzwakkingscoëfficiënten µ/ρ [cm²/g]

Bron: xraydb 4.5.8 (Elam-tabellen); NIST XCOM was niet bereikbaar vanuit de sandbox. Afwijking t.o.v. XCOM in 20–150 keV typisch < 5 % **[A]** – in Ronde 3 steekproefsgewijs controleren.

| Materiaal | 20 keV | 30 | 40 | 59,5 | 80 | 100 | 150 | 662 |
|-----------|-------|-----|-----|------|-----|-----|-----|-----|
| Cu | 33,8 | 10,9 | 4,86 | 1,63 | 0,763 | 0,458 | 0,222 | 0,073 |
| Al | 3,44 | 1,13 | 0,568 | 0,281 | 0,202 | 0,170 | 0,138 | 0,075 |
| Fe (staal) | 25,7 | 8,18 | 3,63 | 1,23 | 0,595 | 0,372 | 0,196 | 0,073 |
| Ni | 32,2 | 10,3 | 4,60 | 1,55 | 0,731 | 0,444 | 0,221 | 0,076 |
| Zn | 37,2 | 12,1 | 5,38 | 1,80 | 0,837 | 0,497 | 0,234 | 0,073 |
| C (grafiet) | 0,442 | 0,256 | 0,208 | 0,176 | 0,161 | 0,151 | 0,135 | 0,077 |
| LiCoO₂ | 17,2 | 5,53 | 2,49 | 0,882 | 0,451 | 0,298 | 0,175 | 0,074 |
| NMC811 | 18,8 | 6,08 | 2,74 | 0,962 | 0,486 | 0,317 | 0,182 | 0,075 |
| LiFePO₄ | 10,5 | 3,39 | 1,56 | 0,590 | 0,330 | 0,237 | 0,158 | 0,075 |
| MnO₂ (alkaline) | 14,6 | 4,65 | 2,10 | 0,755 | 0,397 | 0,270 | 0,166 | 0,074 |
| PE | 0,432 | 0,271 | 0,227 | 0,197 | 0,182 | 0,172 | 0,153 | 0,088 |
| Papier/cellulose | 0,646 | 0,323 | 0,241 | 0,193 | 0,174 | 0,162 | 0,143 | 0,082 |
| Water | 0,810 | 0,376 | 0,268 | 0,207 | 0,184 | 0,171 | 0,151 | 0,086 |
| Glas (natronkalk) | 3,19 | 1,07 | 0,548 | 0,279 | 0,203 | 0,173 | 0,141 | 0,077 |
| Pb | 86,4 | 30,3 | 14,4 | 5,13 | 2,42 | 5,55 | 2,02 | 0,110 |

### Objecten in de zak: µ·t (transmissie = e^(−µt)) en dual-energy-ratio

Samenstellingen **[A]**: jelly roll 45 % NMC, 20 % grafiet, 15 % Cu, 7 % Al, 13 % elektrolyt/separator (als PE); AA: 40 % MnO₂, 25 % Zn, 20 % water/KOH, 5 % C, 10 % staal.

| Object (massadikte langs straal) | 20 keV | 30 | 40 | 59,5 | 80 | 100 | R = µt₃₀/µt₈₀ |
|----------------------------------|-------|-----|-----|------|-----|-----|-----|
| Zak 40 cm × 0,15 g/cm³ (6 g/cm² organisch) | 4,1 | 2,0 | 1,5 | 1,2 | 1,1 | 1,0 | 1,9 |
| 18650 door hart (0,39 staal + 4,5 jelly) | 73 | 24 | 11 | 3,9 | 2,1 | 1,4 | 11,5 |
| Telefoon-pouch plat (1,2 g/cm² jelly) | 17 | 5,5 | 2,5 | 0,9 | 0,5 | 0,3 | 11,2 |
| AA alkaline door hart | 76 | 25 | 11 | 3,9 | 2,0 | 1,3 | 12,4 |
| Al-blikje, 2 wanden (0,054 g/cm²) | 0,19 | 0,06 | 0,03 | 0,02 | 0,01 | 0,01 | 5,6 |
| Stalen conservenblik, 2 wanden (0,31) | 8,0 | 2,5 | 1,1 | 0,4 | 0,2 | 0,1 | 13,7 |
| Al-folie prop, 10 lagen | 0,14 | 0,05 | 0,02 | 0,01 | 0,01 | 0,01 | 5,6 |
| Messing sleutel 2 mm | 57 | 19 | 8,3 | 2,8 | 1,3 | 0,8 | 14,3 |
| Glazen fles, 2 wanden 3 mm | 4,8 | 1,6 | 0,8 | 0,4 | 0,3 | 0,3 | 5,3 |
| Stalen bout M8 | 162 | 52 | 23 | 7,8 | 3,8 | 2,3 | 13,7 |

Lezing:
- **Al-blik, folie, glas**: transparant tot half-transparant, lage R → nooit verward met een cel. (Dit is precies waar een metaaldetector (A2) wél vals alarm geeft op blik/folie – röntgen is hier complementair.)
- **Cel, sleutel, bout, munt, conservenblik-rand**: bij 30 kV allemaal opaak → onderscheid uitsluitend via **vorm** (cilinder 18×65 / 14×50 / 21×70 mm, knoopcel-schijf, rechthoekige pouch met tabs, celpakket in powerbank/laptop).
- **Dual-energy** scheidt "laag-Z" (organisch, Al, glas) van "hoog-Z" uitstekend, maar cel (11,5) vs alkaline (12,4) vs staal (13,7) verschillen < 10–20 % in R; met overlap en spectrumverharding in een volle zak **[A]** onvoldoende robuust. Li-ion vs alkaline: interne structuur (spiraal + holle doorn vs Zn-gel + messing pen) bij ≥ 60 kV en ≤ 0,5 mm.
- **Hoeveelheid (cellen, Wh)**: aantal en formaat van opake cilinders/prisma's is uit het beeld te tellen → Wh-schatting per formaat (18650 ≈ 10–13 Wh, 21700 ≈ 15–18 Wh, telefoon 12–20 Wh) **[A]**. Overlap van objecten in 2D-projectie geeft onderschatting.

## 4. Typische zakinhoud (input voor simulatie)

| Parameter | Laag / basis / hoog | Bron |
|-----------|---------------------|------|
| Volume zak | 30 / 50 / 60 L | inworpopening trommel (kickoff) |
| Massa | 3 / 5 / 10 kg | opdracht; **[A]** |
| Bulkdichtheid | 0,10 / 0,15 / 0,30 g/cm³ | opdracht |
| Weglengte door zak | 25 / 35 / 45 cm | **[A]** |
| Massadikte | 2,5 / 5–6 / 13 g/cm² | berekend |
| Samenstelling (massa) | GFT/etensresten ~30 %, papier ~15 %, kunststof ~15 %, luiers/hygiëne ~8 %, textiel ~5 %, glas ~3 %, metaal ~2–3 %, rest | Indicatief uit landelijke sorteeranalyses restafval (Rijkswaterstaat/Afvalmonitor); **exacte recente cijfers niet kunnen verifiëren** |

Bij de hoge waarde (13 g/cm², natte GFT) daalt T bij 30 kV tot ~10⁻³–10⁻⁴: dan wordt 30 kV krap. Stilstand (10 s) compenseert dat deels. Dit is het grootste fysische risico van de vergunningsvrije variant → Ronde 3.

## 5. Dosis en afscherming

| Grootheid | Waarde | Toelichting |
|-----------|--------|-------------|
| Kerma in primaire bundel, 30 kV/1 W op 0,6 m | ~5–10 µGy/s (~20–40 mGy/h) **[A]** | fluentie 4,8·10⁴/mm²/s × ~5,8·10³ fotonen/mm² per µGy (20 keV) |
| Benodigde verzwakking tot 1 µSv/h op 0,1 m | ≥ 10⁻⁵ | incl. kortere afstand **[A]** |
| Staal 1 / 2 / 3 mm bij 30 keV | 1,6·10⁻³ / 2,6·10⁻⁶ / 4·10⁻⁹ | trommels zijn al 2–4 mm staal **[A]** |
| Lood 1 / 2 mm bij 59,5 keV | 3·10⁻³ / 9·10⁻⁶ | voor 60–80 kV-variant: 2–3 mm Pb-equivalent rond bundel |
| Dosis per scan op inhoud zak | ~10–50 µGy | irrelevant (afval), geen persoon in bundel bij interlock |
| Limiet publiek | 1 mSv/j (Bbs) ; ANVS hanteert in vergunningen een dosisbeperking van 0,1 mSv/j per bron **[A]** | passant op 0,1 m bij 1 µSv/h gedurende 10 s/dag → ~0,001 mSv/j |
| Zones | bewaakte zone > 1 mSv/j, gecontroleerde zone > 6 mSv/j | bij ≤ 1 µSv/h aan buitenzijde geen zone nodig |

Ontwerpeisen: (1) bundel uitsluitend aan bij **gesloten trommel** (dubbele, fail-safe interlock, hardware); (2) bundel horizontaal/omhoog, niet door de stortkoker naar beneden; (3) hardwarematige kV-begrenzing ≤ 30 kV (zener/HV-module zonder hogere instelling) om binnen 3.18-1b te blijven; (4) storings-/vandalismegeval meenemen (de vrijstelling eist "normale bedrijfsomstandigheden", ANVS zal fail-safe willen zien **[A]**).

## 6. Regelgeving NL

| Regime (Bbs, 2018, uitvoering 2013/59/Euratom) | Wanneer | Gevolg |
|-------------------------------------------------|---------|--------|
| **Vrijgesteld, art. 3.18 lid 1 b** | toestel ≤ 30 kV **óf** door ANVS (verordening/beschikking) goedgekeurd type, **én** ≤ 1 µSv/h op 0,1 m van elke bereikbare buitenzijde | Geen kennisgeving/registratie/vergunning (Afdeling 3.2 niet van toepassing). Lid 2: ANVS kan nadere regels stellen over goedkeuring. |
| Vrijgesteld, art. 3.18 lid 1 c | elektrische apparatuur, onderdelen ≤ 5 kV | fysisch onbruikbaar (geen penetratie) |
| Vrijgesteld, art. 3.18 lid 1 a | apparaat met ingekapselde bron, goedgekeurd type, ≤ 1 µSv/h | n.v.t. (radioactieve bron KO) |
| Kennisgeving | handelingen met laag risico die niet registratie-/vergunningplichtig zijn; ≥ 3 weken vooraf (art. 3.11) | voor toestellen in praktijk zelden; ANVS werkt met registratie |
| **Registratie** | lichtere toestemming; ANVS noemt als voorbeeld "een enkele bagagescanner bij de ingang van een gebouw"; categorie volgens lijst geïdentificeerde handelingen, Bijlage 3.1-A Regeling Bbs; aanvraag via ANVS-loket (eHerkenning) | Per ondernemer/handeling; stralingsbeschermingsdeskundige + toezichthoudend medewerker, RI&E, registratie toestellen |
| Vergunning | meerdere röntgentoestellen / complexere toepassing | zwaar; voor 1 000+ containers vrijwel zeker vergunning als niet vrijgesteld **[A]** |

Conclusie regelgeving:
1. **Route A – ≤ 30 kV + ≤ 1 µSv/h** → wettelijk vrijgesteld, per installatie geen ANVS-procedure. Fysisch haalbaar (§3, §5). Dit is de enige route die met een abonnementsmodel op 1 000+ containers schaalt zonder per-locatie-toestemming.
2. **Route B – > 30 kV (50–80 kV) met ANVS-typegoedkeuring** → na éénmalige goedkeuring ook vrijgesteld per installatie. Doorlooptijd en eisen onbekend (**niet gevonden**); tot dan registratie/vergunning.
3. **Route C – registratie/vergunning** per gemeente/inzamelaar → stralingsdeskundige, jaarlijkse controles; past niet bij "goedkoop, onbemand, duizenden locaties".
4. **Open punten** (vooroverleg ANVS aanbevolen): (a) **rechtvaardiging** – een nieuwe soort handeling moet gerechtvaardigd zijn (Euratom art. 19); onduidelijk of dit ook geldt voor vrijgestelde toestellen **[A: waarschijnlijk wel principieel, praktisch licht]**; (b) interpretatie "bereikbare buitenzijde" bij een trommel die door het publiek geopend wordt en een container die bij lediging omhoog komt; (c) onbemand in openbare ruimte + vandalisme; (d) status pyro-elektrische bron. De geconsolideerde Bbs-tekst (wetten.overheid.nl) en ANVS-pagina's waren vanuit de sandbox **niet bereikbaar**; artikeltekst 3.18 is overgenomen uit meerdere secundaire weergaven (Staatsblad 2017, 404; inview.nl; RUG Handboek Stralingshygiëne) en moet door een stralingsdeskundige worden bevestigd.

## 7. Bestaande producten en markt

| Product / project | Wat | Waar in keten | Datum bron |
|-------------------|-----|---------------|------------|
| Visia (VS) | AI + röntgen op inkomende band MRF (Rumpke, Casella); laserpointer voor handmatige uitname; claimt Li-ion vs alkaline/lood | Stap 7 | WasteDive, 2025 |
| Fraunhofer IIS "DangerSort" (DE) | Röntgen + AI op band, persluchtuitstoot; ook batterijen ín apparaten; veldtest LOBBE; looptijd t/m 2025-08 | Stap 7 | TechXplore 2025-05 |
| PFU/Ricoh "Raptor VISION BATTERY" (JP, met IHI) | Röntgen + AI, batterijen vóór verwerkingsapparatuur | Stap 6–7 | Ricoh, 2025-10-31 |
| TOMRA X-TRACT, Steinert XSS T | Dual-energy XRT-sorteerders (metalen, mineralen); 100–160 kV, > EUR 300 k **[A]** | Stap 7 | fabrikantinfo |
| Smiths Detection / Rapiscan / Nuctech bagagescanners | 140–160 kV, ~EUR 20–40 k **[A]**; in NL registratieplichtig | referentie | ANVS (inspecties 2024-02) |
| Detection Technology AVA (Zero) | Goedkopere dual-energy lijndetectoren voor value-segment scanners | component | electronicsforu, 2024–25 |
| Greyparrot, Recycleye | camera-AI, geen röntgen | Stap 7 | – |
| Röntgen in vuilniswagen of bij inworp | **niet gevonden** | – | – |

## 8. Kosten (hardware per inworpzuil, EUR 2026 excl. btw, **[A]**)

| Post | Laag | Basis | Hoog |
|------|------|-------|------|
| Bron ≤ 30 kV + HV + kV-begrenzing | 400 | 1 200 | 3 000 |
| Detector (C1: scherm + camera / C2: lijnarray) | 150 | 600 | 2 000 |
| Afscherming, interlocks, behuizing | 150 | 400 | 1 200 |
| Compute (RPi 5 / Jetson Orin Nano) + modem | 100 | 250 | 600 |
| Montage + keuring/meetrapport stralingsdeskundige (eenmalig) | 200 | 500 | 1 500 |
| **Totaal** | **1 000** | **2 950** | **8 300** |

Energie per inworp **[A]**: buis 4 W elektrisch ×2 (HV-rendement) × 5 s + compute 6 W × 10 s ≈ 0,03 Wh; 100 inworpen/dag → ~3 Wh/dag + stand-by. Netaansluiting of grote accu nodig – afstemmen met A5.

## 9. Plan Ronde 3 (experiments/A3_*)

| # | Model | Methode | Uitkomst |
|---|-------|---------|----------|
| 1 | Beer-Lambert polychromatisch | Kramers/TASMIP-spectrum 25–30–50–80 kV, filters; µ/ρ uit xraydb, controle 5 punten tegen NIST XCOM | T en contrast per object × zakdikte (2,5–13 g/cm²) |
| 2 | Contrast cel vs blik/folie/sleutel/munt/bout | 2D-projectiefantoom (synthetische zakken: random objecten, overlap) → CNR-kaarten | Detecteerbaarheid per object, vals-positieven per vorm |
| 3 | Dual-energy discriminatie | R-verdeling met fotonruis, overlap en beam hardening; 30/30-gefilterd vs 50/80 kV | ROC Li-ion vs alkaline vs staal; aanname: R alleen bruikbaar laag-Z vs hoog-Z |
| 4 | Fotonstatistiek bij laag vermogen | Poisson-ruis + detectorefficiëntie (GOS+camera 10⁻³; lijnarray 0,7) vs integratietijd 0,1–20 s | Minimale stilstand per detectortype; toets uitgangspunt 1 |
| 5 | Dosis + afscherming | kerma in bundel, transmissie staal/lood, strooistraling (single-scatter, 90°) aan opening/koker | Dikte staal/Pb voor ≤ 1 µSv/h op 0,1 m; interlock-eisen |
| 6 | Telling & Wh | herkenning formaat → Wh-schatting incl. overlap-onderschatting | Input voor A1-drempel en A6-Monte-Carlo |

## 10. Niet gevonden / onzeker
- Geconsolideerde Bbs- en Regeling-Bbs-tekst 2026 (sandbox geblokkeerd); Bijlage 3.1-A categorienummers.
- Procedure en doorlooptijd ANVS-typegoedkeuring voor toestellen.
- Lijstprijzen LDA's, Moxtek, Amptek (alleen offerte).
- Flux pyro-elektrische bronnen en hun juridische status.
- Recente NL-sorteeranalyse restafval met batterijfractie (→ A1).
