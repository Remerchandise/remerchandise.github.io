# 00 – Orchestrator kickoff

Prijspeil: EUR 2026, excl. btw. Eenheden SI, energie in Wh. Aannames worden gemarkeerd met **[A]**.

## 1. Route van inworp tot verwerking en brandmomenten

| # | Stap | Wat gebeurt er met de zak | Brandmechanisme | Risico |
|---|------|---------------------------|-----------------|--------|
| 1 | Thuis / inzamelen | Accu of apparaat met accu belandt in restafvalzak | Meestal geen (cel nog intact) | Laag |
| 2 | Inworpzuil / trommel (pas, 30–60 L) | Zak ligt 1–10 s stil in trommel, valt daarna 1–3 m | Valschade aan cel (deuk) → zelden directe ontsteking | Laag |
| 3 | Ondergrondse container (3–5 m³), dagen tot 2 weken | Zak ligt onder andere zakken, drukbelasting, vocht, zon op deksel | Latente interne kortsluiting na valschade; zelfontbranding zeldzaam maar bekend (containerbranden) | Middel (kans laag, schade hoog: container + omgeving) |
| 4 | Lediging: kraan tilt container, bodemkleppen open boven wagen | Val 1–2 m in laadbak | Mechanische schok | Laag–middel |
| 5 | **Vuilniswagen: persplaat/compactie** | Cellen worden geplet en doorboord | **Hoofdmechanisme**: crush/penetratie → interne kortsluiting → thermal runaway binnen seconden–minuten | **Hoog** (chauffeur, wagen > EUR 300k) |
| 6 | Overslag / bunker AVI | Grijper, opslag in bunker | Gloeinest in bunker, beschadigde cellen | Hoog (bedrijfsschade, verzekering) |
| 7 | Verwerking (AVI, nascheiding, shredder) | Shredder | Benchmark: hier zitten de dure sorteerinstallaties | Hoog |

Conclusie voor het product: het grootste risico ontstaat **na** de zuil (stap 5–7). Een detector bij de inworp is dus vooral een **vroegwaarschuwing en sturingsinstrument** (welke container apart behandelen/legen, gedragsfeedback), plus beperkte bescherming van de container zelf (stap 3). Dit moet in de waardepropositie expliciet zijn.

## 2. Agentverdeling

| Agent | Rol | Motivatie |
|-------|-----|-----------|
| A1 | Risicobenchmark | Zonder drempel geen product; bepaalt wat "recall" betekent |
| A2 | Inductie & metaaldetectie | Hypothese opdrachtgever (strandmetaaldetector); waarschijnlijk goedkoopst |
| A3 | Röntgen met stilstand | Enige principe dat inhoud "ziet"; regelgeving is de crux |
| A4 | Thermisch, gas & continue monitoring | Tweede meetmoment (uren–dagen in container) |
| A5 | Product & hardware | BOM, energie, behuizing, montage – maakt concepten vergelijkbaar in euro's en Wh |
| A6 | Software, signaal & dashboard | Detectielogica + wat de ophaaldienst concreet doet; AVG |
| A7 | Business model | Abonnementsprijs vs. vermeden schade (knock-out criterium) |
| A8 | Red team | Valt elk concept aan; elk advies moet dit overleven |

Toegevoegd (binnen bestaande agents, geen aparte agent om dubbel werk te voorkomen):
- **Classificatie-Monte-Carlo** ligt bij A6 (detectielogica) met input van A1 (risico), A2/A3/A4 (sensormodellen).
- **Radar/mmWave en capacitief/dielectrisch** worden door A2 meegenomen als alternatieve elektromagnetische principes.

## 3. Planning vier rondes

| Ronde | Inhoud | Output |
|-------|--------|--------|
| 0 | Research per agent (bronnen met datum) | `/research/Ax_*.md` |
| 1 | Divergeren: ≥ 3 concepten per agent (1 radicaal eenvoudig, 1 onconventioneel), geen kritiek | `/debate/R1_Ax_concepten.md` |
| 2 | Sparren: elke agent valt ≥ 2 andere agents aan; bedenkers reageren; Orchestrator kiest 4–6 concepten | `/debate/R2_*.md`, `/debate/R2_shortlist.md` |
| 3 | Testen: rekenmodellen en simulaties | `/experiments/*` |
| 4 | Convergeren: scorekaart, red team, productkeuze, MVP | `/debate/R4_*.md`, `/product/*`, `/deck/*` |
