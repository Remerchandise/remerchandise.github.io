# A7 – Business model & abonnement (Ronde 0 research)

Prijspeil EUR 2026 excl. btw. **[A]** = aanname. Rekenmodel: `experiments/A7_unit_economics.py` (python3, geen dependencies).
Beperking: WebFetch werkte niet in deze sessie (DNS), dus de cijfers komen uit zoekresultaat-fragmenten. Citeer niets hieruit extern zonder de bron te openen.

## 1. Markt: hoeveel containers, hoeveel klanten

| Grootheid | Waarde | Bron / status |
|---|---|---|
| Gemeenten NL 1-1-2026 | **342** (gelijk aan 2024–2025) | CBS, *Gemeentelijke indeling op 1 januari 2026* |
| Ondergrondse containers (UGC) landelijk | **Geen landelijk cijfer gevonden.** "Ruim 100.000" niet bevestigd | zoeken in CBS/NVRD/leveranciers leverde niets op |
| Datapunt Utrecht | 2.189 UGC (2024); ca. 4.200 containers van alle typen (tender 2022) | DUIC 2024; TED 675611-2022 |
| Schatting UGC **restafval** NL | laag 30.000 / basis **45.000** / hoog 65.000 **[A]** | bottom-up: ~3–6 UGC per 1.000 inwoners in stedelijke gemeenten (Utrecht ~6 voor alle fracties), ~50 % restafval, landelijk minder dicht. "100.000" is aannemelijk als je **alle fracties** (glas, papier, pmd, semi-ondergronds) meetelt |
| Gem. UGC per gemeente | ~130 (45.000/342), sterk scheef: G4 elk duizenden, plattelandsgemeenten < 50 **[A]** | afgeleid |
| Huishoudens per rest-UGC | 50–150 **[A]** | gangbare normering, niet geverifieerd |

## 2. Wie beslist en betaalt

| Actor | Rol | Opmerking |
|---|---|---|
| Gemeente (raad/college) | Wettelijke zorgplicht huishoudelijk afval (Wet milieubeheer art. 10.21), stelt afvalstoffenheffing vast (kostendekkend) | Kosten gaan dus via de **afvalstoffenheffing naar bewoners**. EUR 20/container/maand = EUR 1,6–4,8 per huishouden per jaar **[A]** |
| Overheids-NV (HVC, ROVA, Cyclus, Circulus, RMN, …) | Inzameling en vaak eigenaar van containers; HVC heeft ca. 44 aandeelhouders (gemeenten + waterschappen; datum onbekend) | Lelystad: HVC betaalt sinds 1-1-2023 aanschaf en vervanging van UGC (raadsstuk Lelystad). ROVA werkt alleen voor deelnemende gemeenten en doet niet mee aan open aanbestedingen (raadsstuk Leusden 2025). **HVC = inzamelaar én AVI-exploitant**: draagt zowel wagen- als verwerkerschade → logische launching customer |
| Gemeenschappelijke regeling / dienst | Avalex (6 gemeenten; ook HVC-aandeelhouder), gemeentelijke dienst Amsterdam | Beslissingen gaan langzaam door de vele aandeelhouders (Rekenkamer Lelystad 2025 over HVC) |
| Privaat (Renewi, PreZero, Remondis) | Inzamelen in opdracht van gemeente | Draagt eigen wagenschade en verzekering; heeft prikkel, maar is geen eigenaar van de container |
| Leveranciers containers/toegangszuilen (Bammens, Sidcon, …) | Leveren zuil, trommel, pasjessysteem (vaak met eigen GPRS/LTE-modem en accu) | **Kanaalpartner**: elektronica, connectiviteit en servicebezoeken zitten er al |

### Aanbesteden
| Drempel 2026–2027 (excl. btw) | Bedrag | Bron |
|---|---|---|
| Leveringen/diensten, decentrale overheden | **EUR 216.000** (2024–2025: 221.000) | EU-publicatie 22-10-2025; Dirkzwager, CMS 2025 |
| Rijksoverheid | EUR 140.000 | idem |
| Werken | EUR 5.404.000 | idem |

Consequentie: de drempel geldt voor de **totale contractwaarde over de looptijd**. Bij EUR 20/maand × 72 maanden = EUR 1.440 per container wordt de drempel al bij **~150 containers** gehaald. Daarboven is een Europese aanbesteding nodig (doorlooptijd 6–12 maanden **[A]**). Kleinere pilots kunnen meervoudig onderhands. Overheids-NV's zijn doorgaans zelf ook aanbestedende dienst. Een snellere route is meeliften op een bestaand raamcontract voor UGC of toegangscontrole; daar zijn abonnements- en telemetrieposten al gangbaar (TenderNed 2026, NvI: "post toevoegen voor abonnementskosten"; Middelburg least toegangs- en vulgraadsystemen 96 maanden).

## 3. Schadekant: wat kost een brand?

| Post | Waarde | Bron / status |
|---|---|---|
| Branden in vuilniswagens | "Jaarlijks tientallen", "zeker 3 per maand" (≥ 36/jaar) | NVRD-inventarisatie via NOS (datum te controleren, ca. 2023) |
| Branden bij commerciële bedrijven (inzamelplaatsen + wagens) | ~10 per maand ≈ 120 per jaar | Vereniging Afvalbedrijven via NOS |
| Aandeel batterijen in branden bij verwerkers | **38 %** (eigen claim van de sector) | Kamerstuk 2026D41104; Omroep Gelderland |
| Batterijen in restafval | > 100 miljoen in 2025 | Stichting OPEN via adblom.nl |
| Vapes | ~20.000 per dag in restafval (VA); ~140.000 per week (Taskforce); gem. 20 vapes per vuilniswagen restafval | Vereniging Afvalbedrijven; Taskforce Batterijbranden |
| Registratie | Rijk en veiligheidsregio's registreren afval-/batterijbranden **niet apart** | Kamerantwoord 2026; Omroep Gelderland |
| Schade bij afvalbranden (alle oorzaken) | EUR 175 mln in 3 jaar (≈ 58 mln/jaar); sommige verzekeraars stoppen met afvalbedrijven | Verbond van Verzekeraars via brandveilig.com (**oud, ca. 2017**) |
| Batterijbrand, individuele claims | ~EUR 1 mln (één groot incident); claims in portefeuille EUR 1,5–5 mln (afgelopen 5 jaar) | podcast verzekeringsmakelaar, recyclepro.eu (BE, 2024/25) |
| Verzekeringspremie | "stijgende premies" in de recyclingsector, zonder bedragen | Taskforce Batterijbranden, jaaroverzicht 2024 (apr 2025) |
| Huisvuilwagen, diesel | ~EUR 250.000 (raming Waalwijk 2023); 2 wagens + 96 maanden onderhoud EUR 463.010 (Sliedrecht 2019) | TED/TenderNed |
| Huisvuilwagen, elektrisch | tot EUR 475.000 (Oosterhout 2023); raming EUR 1 mln per stuk incl. instandhouding (Almere 2026) | raadsbesluit Oosterhout; TED 317944-2026 |
| Schade per wagenbrand | **Niet gevonden.** Aanname: klein (afval op straat storten, blussen, reinigen, 1–3 dagen stilstand) EUR 3–10k; laadbak/hydrauliek EUR 30–100k; total loss EUR 250–500k. Gewogen gemiddelde 10k / **25k** / 50k **[A]** | — |
| Nieuwe UGC incl. plaatsing | EUR 6.100 (Vlissingen ~2020: container 3.425 + put 875 + plaatsing 1.800); EUR 8.750 (Asten); EUR 9.500 (Arnhem) | raadsstukken |
| Schade aan UGC door vandalisme | 90 containers voor EUR 70.000 ≈ EUR 780 per stuk (jaarwisseling) | AT5/NH Nieuws |
| Containerbrand door accu | frequentie **niet gevonden**; 0,02 / 0,05 / 0,1 % van de UGC per jaar **[A]** | — |
| Afvalstoffenbelasting (verbranden) | EUR 39,71/t (2025) → EUR 90,21/t (2028) | Kamervragen 2026 |

## 4. Andere betalers

| Kandidaat | Grondslag | Haalbaarheid |
|---|---|---|
| **Producenten (EPR) – Stichting OPEN** (sinds 1-1-2024 uitvoerder voor batterijen, opvolger van Stibat) | Batterijverordening (EU) 2023/1542: inzameldoel draagbare batterijen **63 % eind 2027, 73 % eind 2030** (was 45 %). Producenten betalen per stuk/kg ("enkele centen") | Middel. OPEN heeft belang bij **data over waar batterijen in het restafval belanden**, om inzetbakken en campagnes te sturen. Brandschade valt niet onder hun wettelijke plicht. Tarieven 2026 (OPEN, okt 2025) niet kunnen openen |
| **Verzekeraar** (wagenpark, AVI-brand/bedrijfsschade) | Lagere schadelast, verzekerbaarheid | Laag–middel. Verzekeraars eisen preventie (blussystemen, thermische camera's in de bunker), maar betalen zelden voor sensoren. Een premiekorting als hefboom is realistischer dan financiering |
| **AVI / nascheider** (HVC, AEB, Attero, AVR, PreZero) | Bunker- en shredderbranden, de dure kant van de keten | Middel. Alleen zinvol als de detectie ook de stroom naar de AVI verandert (aparte lediging, of minder batterijen door gedragseffect) |
| **Toegangszuil-leverancier** | Functie-upsell op bestaande installed base | Hoog als kanaal, niet als eindbetaler |

## 5. Vergelijkbare IoT-abonnementen

| Product | Prijs | Status |
|---|---|---|
| Sensoneo (vulgraad) | Geen openbare prijs. Starterkit: sensor + 3 maanden software, data apart | sensoneo.com (fetch mislukt) |
| Nordsense, gemeente Varde (DK) | 30 containers; investering DKK 30.000 (≈ EUR 4.000 → ≈ EUR 134 per container, als dit het totaal is); besparing DKK 40.000 per jaar | nordsense.com case |
| Markt (vulgraad) | ordegrootte hardware EUR 100–250 + SaaS EUR 3–10 per sensor per maand **[A, uit geheugen, niet geverifieerd]** | — |
| Heerhugowaard 2018 | vulgraadinzameling pas rendabel vanaf ≥ 200 UGC van één fractie; zuilen zonder stroom | raadsinformatiebrief |
| Connectiviteit LTE-M/NB-IoT/LoRa (KPN e.a.) | EUR 0,4–1,5 per maand **[A]**; geen openbare tarieven gevonden | — |

**Ankerpunt:** de klant is gewend aan EUR 3–10 per container per maand voor een sensor die aantoonbaar rijkosten bespaart. Een brandsensor zonder directe besparing moet daaronder blijven, of moet gebundeld worden.

## 6. Unit economics (uit `experiments/A7_unit_economics.py`)

Aannames: device EUR 80 / 150 / 300 (A5 levert de BOM), installatie EUR 40 / 80 / 150, levensduur 6 jaar, connectiviteit EUR 0,4 / 0,9 / 1,5 per maand, uitval 5–12 % per jaar, vaste support EUR 15k / 60k / 250k per jaar, CAC EUR 15–50k per klant.

| EUR per container per maand (basis) | 100 | 1.000 | 10.000 |
|---|---|---|---|
| Hardware (afschrijving) | 2,08 | 1,67 | 1,35 |
| Installatie | 1,11 | 0,94 | 0,94 |
| Connectiviteit | 0,90 | 0,90 | 0,90 |
| Cloud | 0,90 | 0,45 | 0,30 |
| Onderhoud | 1,08 | 1,08 | 1,08 |
| Support (vast, verdeeld) | 12,50 | 5,00 | 2,08 |
| CAC | 4,17 | 2,08 | 1,25 |
| **Kostprijs** (laag–hoog) | **22,7** (13,8–36,2) | **12,1** (7,0–20,2) | **7,9** (4,3–13,8) |
| Prijs bij 40 % brutomarge | 37,9 | 20,2 | 13,2 |

### Vermeden schade per container (top-down landelijk)
Formule: (wagenbranden × schade + batterijschade bij verwerkers + containerbranden) × aandeel van de UGC-route × recall × effectiviteit van de actie ÷ aantal UGC.

| | laag | basis | hoog |
|---|---|---|---|
| Wagenbranden per jaar × schade | 40 × 10k | 80 × 25k | 150 × 50k |
| Batterijschade bij verwerkers per jaar **[A]** (≈ 38 % van de oude VvV-58 mln, geïndexeerd) | 10 mln | 22 mln | 40 mln |
| Aandeel UGC-route **[A]** | 15 % | 25 % | 35 % |
| Recall × effectiviteit **[A]** | 0,3 × 0,3 | 0,5 × 0,5 | 0,7 × 0,7 |
| **Vermeden schade per container per jaar** | EUR 2 | **EUR 34** | EUR 276 |
| Per maand | 0,19 | **2,86** | 23,0 |
| Landelijk vermeden per jaar | 0,15 mln | 1,5 mln | 8,3 mln |

**Knock-out:** in het basisscenario levert de vermeden schade **~EUR 3 per container per maand** op, terwijl de kostprijs bij 1.000 containers **~EUR 12** is (factor 4) en bij 10.000 containers ~EUR 8 (factor 3). Voorbeeldgemeente met 250 UGC: EUR 8,6k vermeden per jaar tegenover EUR 61k abonnement. Ruim 85 % van de vermeden schade valt bij de **verwerker**, niet bij de gemeente. Alleen het hoge scenario loont, en dat vereist hoge recall én een effectieve vervolgactie.

Gevolgen voor het ontwerp:
1. Kosten per container moeten naar **≤ EUR 3–5 per maand**. Grootste hefbomen: support/CAC (kanaal via zuilleverancier of overheids-NV) en geen eigen modem.
2. **Niet elke container instrumenteren**: steekproef of roulatie, of detectie per wagen in plaats van per container.
3. **Andere waarde stapelen**: gedragsdata voor het inzameldoel van 63 %, bundel met vulgraad/toegang, veiligheid van de chauffeur (Arbo; niet in euro's uitgedrukt).
4. De betaler moet daar liggen waar de schade valt: **verwerker/AVI of EPR**.

## 7. Niet gevonden
Landelijk aantal UGC; schade per wagenbrand; frequentie van containerbranden door accu's; actuele premiecijfers (Verbond); tarieven 2026 van Stichting OPEN; openbare prijzen voor vulgraadsensoren en IoT-connectiviteit; recent landelijk schadebedrag voor batterijbranden (alleen VK: GBP 158 mln per jaar).

## Bronnen (geraadpleegd 2026-10)
- CBS, Gemeentelijke indeling op 1 januari 2026 – cbs.nl
- Dirkzwager / CMS, Europese drempelbedragen 2026–2027 (okt 2025)
- NOS, "Jaarlijks tientallen branden in vuilniswagens door batterijen en accu's" – nos.nl/l/2485439
- Tweede Kamer 2026D41104 (Kamervragen batterijbranden, 2026)
- Omroep Gelderland, "100 miljoen batterijen nog steeds bij restafval" (2025/26)
- Stichting OPEN, Jaaroverzicht Taskforce Batterijbranden 2024 (15-04-2025)
- Vereniging Afvalbedrijven, "20.000 vapes per dag in restafval"
- recyclepro.eu, Li-ion in afvalstromen: brandrisico's en verzekeringen
- brandveilig.com, "Afvalbranden: tientallen miljoenen schade" (Verbond van Verzekeraars, ca. 2017)
- TED/TenderNed: Waalwijk 2023, Sliedrecht 2019, Almere 2026 (317944-2026), Utrecht 675611-2022; raadsbesluit Oosterhout 2023
- Raadsstukken: Arnhem, Vlissingen, Asten (UGC-prijzen); Lelystad (HVC); Leusden 2025 (ROVA); Heerhugowaard 2018
- DUIC 2024 (Utrecht 2.189 UGC); AT5/NH Nieuws (vandalismeschade)
- Nordsense, case Varde
