# R1 – A2 concepten (Inductie & metaaldetectie)

Divergeren, geen kritiek. Prijzen EUR 2026 excl. btw, BOM per zuil (hardware sensor + elektronica, excl. gateway/behuizing → A5). Aannames **[A]**. Onderbouwing: `research/A2_inductie.md`.

| ID | Naam | Sensor | Meetmoment | Drempel | Signaal | Verdienmodel | Ruwe kostprijs | Label |
|---|---|---|---|---|---|---|---|---|
| A2-C1 | **Strandmetaaldetector-in-de-trommel** (variant opdrachtgever) | VLF 2–3 frequenties, DD-spoel rond trommelopening (meedraaiend) | Per inworp, 2–5 s stilstand | "Ferro + grootte-index ≥ X" ⇒ verdacht | Teller verdachte inworpen per container → melding bij ≥ N | Abonnement per container (€5–10/mnd) **[A]** | €40–80 (eigen board); €165+ als hobbydetector wordt gehackt | Opdrachtgever |
| A2-C2 | **PI-klikker** | 1 lus + MCU-PI (MOSFET, opamp, ADC), één vervalvenster | Per inworp, vóór/na-verschil in zelfde trommelstand | Metaal-amplitude boven drempel | "Metaal-inworp" teller + grove grootte; container-score | Per gemeente (bulk, laag tarief) | €15–30 | **Radicaal eenvoudig** |
| A2-C3 | **Rol-spectroscoop (MPT)** | PI multi-gate (16–32 vensters) + ferro-kanaal (VLF-I of DC-bias), 2 lussen boven/onder voor lokalisatie | Per inworp; trommelrotatie levert 2–4 oriëntaties | Classifier-score P(Li-ion) ≥ p + Wh-klasse (geen/cel/pakket) | Risicoscore per container; ophaaldienst ziet "x waarschijnlijke Li-items" | Per container, premium-tier met dashboard | €50–100 | Ambitieus |
| A2-C4 | **Magnetisatiepuls-geheugen** | Pulsspoel (DC-puls 10–50 mT) + 4 AMR-magnetometers (€1–4 per stuk) | Per inworp: pulsen, dan remanentie/hysterese meten; continu in container via magnetometers in wand | Remanent moment + hysterese-vorm ⇒ "hard dieptrekstaal (cel)" vs "zacht blikstaal" | Ferro-teller + celkans | Per container | €20–40 | **Onconventioneel** |
| A2-C5 | **Valkoker-tunnel** | Gebalanceerde 3-spoelen tunnel (zoals voedingsindustrie) rond valweg onder trommel, 5-freq | Tijdens val (0,1–0,3 s) – toetst uitgangspunt 1 omgekeerd | Fase/amplitude-gate per klasse | Teller per container | Per container | €60–150 + inbouw in schacht | Contrast-concept |

## Werking (2–3 zinnen per concept)

**A2-C1 Strandmetaaldetector-in-de-trommel.** Een gebalanceerde DD-spoel wordt op de trommel gemonteerd zodat hij meedraait (stalen achtergrond is dan statisch en weg te balanceren). Tijdens de stilstand meet een 2–3-frequentie VLF de I/Q-respons met lock-in middeling; ferro-fase plus amplitude boven een drempel telt als "verdacht". Eigen board i.p.v. hobbydetector omdat consumentendetectoren geen data-uitgang hebben.

**A2-C2 PI-klikker (radicaal eenvoudig).** Eén koperlus rond de opening, MCU stuurt 1 kHz pulsen, één ADC-sample op ~20 µs; het verschil vóór/na inworp in dezelfde trommelstand onderdrukt de stalen zuil. Het zegt alleen "er zat (veel) metaal in" — geen batterij-identificatie — maar levert per container een goedkope metaal-inworp-statistiek die als proxy/trigger voor een duurdere sensor (A3/A4) kan dienen.

**A2-C3 Rol-spectroscoop.** Meet de volledige vervalcurve (τ-spectrum) plus een ferro-kanaal, vanuit 2–4 trommelstanden, en schat zo een (vereenvoudigde) magnetische polariseerbaarheidstensor; twee lussen geven positie zodat amplitude naar metaalvolume kan worden omgerekend. Een classifier, getraind op een bibliotheek (18650, AA, pouch, blik, folie, sleutels, telefoons), geeft P(Li-ion) en een grove Wh-klasse.

**A2-C4 Magnetisatiepuls-geheugen (onconventioneel).** Een korte sterke DC-veldpuls magnetiseert stalen objecten; goedkope magnetometers meten daarna het remanente moment en (met een kleine wisselbias) de hysterese/harmonischen. Hypothese: koud dieptrokken vernikkeld celstaal heeft andere remanentie dan vertind blikstaal of schroeven; dezelfde magnetometers in de containerwand volgen continu het totale ferro-moment over dagen.

**A2-C5 Valkoker-tunnel.** Zoals in de voedingsindustrie: zak valt door een uniforme gebalanceerde tunnel, waardoor positie-afhankelijkheid veel kleiner is dan bij een lus aan de rand. Bewust tegen uitgangspunt 1 in (korte meting, maar betere geometrie) om te toetsen of geometrie belangrijker is dan meettijd.

## Eerste verwachting (hypothese, toets in R3)
- Alle inductieve concepten zien 18650 betrouwbaar als "stalen object"; onderscheid 18650 ↔ AA-alkaline ↔ conservenblik-fragment is de zwakke plek, pouch ↔ sleutelbos/blikje de tweede.
- Inductie is waarschijnlijk het best als **goedkope eerste trap / proxy** (C2/C3), niet als eindoordeel.
