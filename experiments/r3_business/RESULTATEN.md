# R3 – A7 Business: resultaten (FASE 2, definitief)

Script: `python3 experiments/r3_business/business.py` (deterministisch, < 3 s). Output: `tables.md` (alle tabellen), `results.json`, figuren `fig_prijs_vs_schade.png`, `fig_schaal.png`, `fig_unit_economics.png`, `fig_business_case.png`. EUR 2026 excl. btw.

**Inputs FASE 2:**
- BOM van A5: `product/BOM_samenvatting.csv`. Daaruit komen HW, installatie, kosten per maand en per jaar, eenmalige kosten (NRE/certificering, bv. de OEM-adapter EUR 50–150k) en het aantal containers per unit.
- MC van A6: `experiments/r3_classificatie/mc_results.json`. Daaruit komen de vermeden fractie wagenbranden, het aantal meldingen per 1.000 ledigingen en de brandfrequentie **0,07 / 1,27 / 48 per 1.000 containerjaar** (A1 R3).

**Afwijkingen [A]:**
- **K3b** dekt 1/35 van de containers tegelijk.
- **K4**: A6 rekent 0 vermeden wagenbranden. A7 telt wel containerbranden mee, plus 0 / 30 / 60 % effect van de "niet legen"-vlag bij incidenten die in de container beginnen.
- **B0** gebruikt een eigen preventiemodel: 3 / 8 / 15 % minder Li-energie in het restafval. De rangorde-MC van A6 past niet bij een inzamelsleuf.
- Bij **B1** telt de vermeden schade bij de verwerker voor 50 %.
- Nieuwe varianten:
  - **K4add**: K4 als add-on op een bestaande vulgraad- of zuilmodule.
  - **B1oem**: B1 als fabrieksoptie in de voertuigaanbesteding, zonder eigen sales.

Overige aannames:
- Schade per incident: wagen 10k / 25k / 50k, verwerker 5k / 25k / 75k, container 3k / 8k / 15k.
- Kosten per melding: EUR 10 / 40 / 150.
- Marge 40 %, levensduur 6 jaar.

## 1. Abonnementsprijs incl. marge, NRE en support (EUR per container per maand, basis [laag–hoog])

| Concept | 100 | 1.000 | 10.000 | Opmerking |
|---|---|---|---|---|
| K1 VLF | 34,8 | 14,6 [8,8–23,9] | 9,3 | |
| K2 Pakketwachter (OEM) | 40,7 | 10,7 [6,5–17,3] | 5,7 | NRE EUR 100k drukt hard op kleine schaal |
| K3a Röntgen vast | 130 | 90 [48–168] | 78 | |
| K3b Röntgen rouleert | 57 | 26,7 [12–49] | 20,6 | ≈ EUR 930 per unit per maand |
| K4 Deksel standalone | 32,8 | 13,9 [8,3–21,8] | 8,8 | |
| K5 Hybride | 65,7 | 18,6 [11,5–29,7] | 10,4 | NRE EUR 150k |
| B1 Wagencamera (eigen sales) | 25,8 | 8,4 [5,0–13,2] | 3,9 | ≈ EUR 1.180–2.530 per wagen per maand |
| **K4add** add-on | 11,3 | **3,6** [2,1–5,8] | **2,2** | sensoren EUR 40 + NRE; verkocht door vulgraad- of zuilleverancier |
| **B1oem** fabrieksoptie | 9,4 | **2,3** [1,3–3,7] | **0,97** | ≈ EUR 290–680 per wagen per maand |
| B0 Brievenbus + sortering | 44 | 23 [12–50] | 15 | sortering EUR 20k per klant per jaar domineert |

Support, CAC en NRE vormen 50–85 % van de kostprijs (behalve bij röntgen). Schaal werkt sterk: van 100 naar 10.000 containers wordt een abonnement 3–7× goedkoper (`fig_schaal.png`).

## 2. Business case: gemeente met 1.000 containers (EUR per container per jaar)

| Concept | Abonnement + acties | Vermeden schade laag / basis / hoog | Ratio basis | Knock-out? | Benodigde branden per 1.000 cj voor ratio 1 (basis 1,27) |
|---|---|---|---|---|---|
| K1 | 216 | 0,0 / 0,9 / 79 | 0,004 | **JA** | 318 |
| K2 | 170 | 0,0 / 1,0 / 117 | 0,006 | **JA** | 220 |
| K3a | 1.122 | 0,0 / 2,2 / 200 | 0,002 | **JA** | 647 |
| K3b | 361 | ~0 / 0,06 / 6 | 0,000 | **JA** (als bescherming) | 7.298 |
| K4 | 168 | 0,0 / 3,7 / 1.090 | 0,02 | **JA** | 58 |
| K5 | 268 | 0,0 / 1,0 / 117 | 0,004 | **JA** | 347 |
| B1 | 102 | 0,1 / 16,3 / 2.702 | 0,16 | **JA** | 8 |
| K4add | 45 | 0,0 / 3,7 / 1.090 | 0,08 | **JA** | 15 |
| **B1oem** | 28 | 0,1 / 16,3 / 2.702 | **0,58** (1,33 bij 10.000 containers) | **nee bij schaal ≥ ~3.000 containers / 10 wagens** | 2 |
| B0 | 278 | 0,0 / 5,2 / 934 | 0,02 | **JA** | 67 |

**Conclusie:**
- In het basisscenario (1,27 branden per 1.000 containerjaar) haalt **geen enkel zuil- of containerconcept** de vermeden schade. Ze zitten een factor 50–600 te laag.
- Alleen de **wagencamera als fabrieksoptie (B1oem)** komt bij schaal boven break-even.
- In het hoge scenario (48 branden per 1.000 cj) wordt alles behalve K1/K2/K3/K5 rendabel.
- De **kosten van vervolgacties (EUR 42 per container per jaar bij 20 meldingen per 1.000 ledigingen)** zijn bij K1/K2/K5 al 40× hoger dan wat ze aan schade voorkomen. Het werkpunt "oranje ≤ 20 per 1.000" van A6 is dus te ruim als oranje geld kost.

## 3. Betaalmodel per overlevende optie

| Optie | Betaler | Model | Waarom |
|---|---|---|---|
| **B1 wagencamera** | **Inzamelaar/vlooteigenaar** (overheids-NV of Renewi/PreZero), met korting van de verzekeraar | **Fabrieksoptie in de voertuigaanbesteding** (EUR 3–7k per wagen) + data/service EUR 15–40 per wagen per maand. Valt onder het voertuigbestek (Almere 2026: ~EUR 1 mln per wagen), dus geen eigen aanbesteding | 67 % van de baat ligt bij de wageneigenaar, 33 % bij de verwerker. Chauffeursveiligheid (Arbo) is een tweede argument. Eigen sales per wagen is te duur (ratio 0,16) |
| **K4 als add-on** | Gemeente/eigenaar container, via de bestaande vulgraad- of zuilleverancier | Optie EUR 1–2 per container per maand op een bestaand abonnement, of eenmalig EUR 60–80 bij nieuwe containers | Waarde (EUR 0,3 per maand) dekt de prijs niet. Verkopen als **veiligheids- en "niet legen"-functie** op hotspots (flats, stations), niet voor alle containers |
| **B0 preventie / inzamelsleuf** | **Stichting OPEN (EPR)** voor de buizen en het legen; gemeente voor de plaatsing | Buis bij de zuil = uitbreiding van het bestaande OPEN-inzamelnet (kosten EUR 25–50 per jaar). Sorteeranalyse als co-financiering (OPEN/IenW, EUR 10–50k per jaar) | OPEN moet naar 63 % inzameling in 2027 (Batterijverordening). Het verlaagt de prevalentie bij **alle** schakels. Geen abonnement van ons |
| **K3b ijk- of meetdienst** | **Wij zelf (R&D) + OPEN/IenW** | Projectdienst EUR 5–15k per campagne per gemeente, geen abonnement | Waarde = ground truth en hotspotkaart, niet bescherming (vermeden schade ≈ 0). Valt ruim onder de drempel van EUR 216k, dus onderhands te gunnen |

## 4. Markt en beslissers (uit `research/A7_business.md`)

**Markt**
- Aantal ondergrondse containers NL: **geen landelijk cijfer gevonden**. Schatting restafval 30k / **45k** / 65k **[A]**. "Ruim 100.000" is alleen aannemelijk als je alle fracties meetelt.
- Gemeenten: 342 (CBS 2026), gemiddeld ~130 rest-UGC per gemeente, sterk scheef verdeeld. Utrecht heeft 2.189 UGC (2024).
- Voor B1: ~400–600 kraanwagens voor UGC **[A]**.

**Wie beslist**
- De gemeente heeft de zorgplicht en betaalt via de afvalstoffenheffing.
- De uitvoering en vaak het eigendom van containers en wagens liggen bij een overheids-NV (HVC ~44 aandeelhouders, ROVA, Cyclus, Circulus, RMN), een gemeenschappelijke regeling (Avalex) of een private inzamelaar (Renewi, PreZero) op contract.

**Inkoop**
- Europese drempel EUR 216k (2026–2027). Een abonnement van EUR 10 per maand haalt die bij ~300 containers over 6 jaar.
- Launching customer: een NV die inzamelaar én AVI is (HVC).

## Alleen met prototype/veld te bevestigen
- Werkelijke kosten per melding en wat de chauffeur doet: pilot met 1 inzamelaar, 2–3 wagens met B1 en 50–100 containers, 3 maanden logboek.
- Effect van B1 in de wagen (blustijd, schade per incident tegenover historie): incidentregistratie bij de inzamelaar, minstens 12 maanden. Statistisch alleen indicatief, zie A6/A8.
- Betaalbereidheid: gesprekken met HVC, ROVA, Cyclus, Renewi, een verzekeraar en Stichting OPEN.
