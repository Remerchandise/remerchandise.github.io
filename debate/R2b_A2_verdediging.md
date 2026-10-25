# R2b – A2 verdediging (inductie)

Ik neem de kernkritiek over (A1, A3, A4, A6, A8):
- inductie ziet staal, en 18650 ≈ AA;
- ~85 % van de zakken bevat metaal;
- vapes zijn inductief bijna onzichtbaar;
- de positie in de trommel geeft ~1000× spreiding in signaalsterkte.

**Inductie claimt dus nooit "Li-detectie".** De enige overlevende rol is het herkennen van **grote pakketten** (≥ 50 Wh-eq) als prior voor de rangorde per container.

| Concept | Status | Motivatie (getal/bron) | R3-test die bevestigt of ontkracht |
|---|---|---|---|
| **A2-C1** Strandmetaaldetector | **INGETROKKEN** als zelfstandig concept | Een hobbydetector heeft geen data-uitgang (A8 §2.4). Een ferro-trigger telt vooral alkaline (394:1, A1/A6) en de PPV wordt ≤ 7–17 % (A6 #6). Het VLF-ferrokanaal gaat op in C3. | – (zit in de C3-simulatie als "1 lus, 2 freq") |
| **A2-C2** PI-klikker | **INGETROKKEN** als product. Blijft bestaan als de goedkoopste hardwarelaag (één lus plus MCU) van C3 | Eén meetvenster geeft ≈ een inworpteller. De Poissonruis van ~340 ± 18 metaaltellingen overstemt 3,6 Li-items (R2a A1-C1). Ook als trigger zinloos: hij vuurt bij 85 % van de inworpen (A4 #1, A8). | ROC van "1 lus, 1 venster" als ondergrens in de Monte Carlo |
| **A2-C3** Rol-spectroscoop | **VERBETERD → "Pakketwachter"** | Nieuwe versie: 2 lussen (boven/onder) plus een ferrokanaal en een τ-spectrum vanuit 2–4 trommelstanden. Er zijn alleen 3 klassen: *geen / losse cel(len) / pakket ≥ 50 Wh-eq*. Het pakket wordt herkend aan **N parallelle stalen cilinders** (powerbank, e-bike, gereedschap: anisotroop en sterk ferromagnetisch) of een **grote gestapelde pouch** (laptop: τ 100–250 µs, sterk anisotroop). Er is geen melding per inworp; het concept levert een container-rangorde (top 1 % per route, A6 #2) die A4-C3 of A1-C3 voedt. Vapes worden expliciet uitgesloten. | Monte Carlo met superpositie van clutter (2,5 blikjes + 3 folie-items per zak, A6), positie/oriëntatie willekeurig. **Bevestigd als**: (a) de lokalisatie brengt de amplitudefout terug tot < 3× (σ_log ≤ 0,5, A1 #2); (b) bij spec ≥ 99 % voor "pakket" tegen een pan, broodrooster, fietsslot of blikstapel is de recall ≥ 60 %. **Ontkracht als** de pan/laptop-overlap > 5 % FP oplevert. Daarna een labtest met n ≥ 300 synthetische zakken (A6 #7) |
| **A2-C4** Magnetisatiepuls | **INGETROKKEN** (het continue deel en de puls van 10–50 mT) | 18–60 J per puls (A3 #4, A5); de zuil en de trommel worden zelf gemagnetiseerd (A4 #3); pouch en vape zijn niet-ferro (A1 #3, A6 #8). Het remanentiecontrast tussen celstaal en blikstaal is onbewezen. Het ferrosignaal komt goedkoper uit het VLF-I-kanaal van C3. | Optioneel, als labproef van 1 dag: de remanentie van een 18650 tegenover een conservenblik tegenover een schroef bij 5 mT (n ≥ 20). Alleen als C3 een extra ferrokenmerk nodig heeft |
| **A2-C5** Valkoker-tunnel | **INGETROKKEN** als product (retrofit €200–500+ per schacht, A4/A5). Blijft alleen bestaan als **simulatievariant** | Dient om uitgangspunt 1 te toetsen: weegt geometrie zwaarder dan meettijd? | In de Monte Carlo: tunnel bij 0,2 s tegenover een lus bij 5 s middeling. Als de tunnel duidelijk wint, alleen een OEM-optie voor nieuwbouw |

**Praktijkpunt overgenomen:** de meedraaiende spoel (A5) maakt ~300k buigcycli in 10 jaar. Daarom een robot-flexkabel of contactloze koppeling.

**Eerlijke waardepropositie:** de pakketwachter ziet hooguit het grote-pakketsegment (≈ 9 % van de items, ≈ 59 % van de risico-energie, A1). Vapes en losse cellen ziet hij niet; daarvoor zijn A4-C5 of de A3-C4-ijking nodig.
