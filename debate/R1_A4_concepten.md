# R1 – A4 concepten (thermisch, gas, continue monitoring)

Basis: research/A4_thermisch_gas.md. EUR 2026 excl. btw, ruwe kostprijs = sensor-meerkosten bovenop basismodule (MCU + NB-IoT/LTE-M + batterij + behuizing, door A5 te begroten, **[A]** ~€35–60). Geen kritiek in deze ronde; zwaktes alleen genoteerd voor R2.

Kerninzicht dat de concepten stuurt: in de container is **branddetectie binnen minuten** realistisch, **voorspelling vóór TR** alleen voor cellen bovenin. Waarde zit in (a) "NIET LEGEN / apart legen"-vlag voor de chauffeur en (b) combinatie met inworpdetectie.

## Overzicht

| ID | Naam | Type | Sensor | Meetmoment | Meerkosten | Energie |
|---|---|---|---|---|---|---|
| A4-C1 | Thermo-deksel | **Radicaal eenvoudig** | 2 NTC + 1-pixel IR | continu | €8–20 | < 0,5 Wh/jr |
| A4-C2 | Snuffelneus multi-gas | basis | BME688 + TGS5042 CO + SHT4x | continu | €22–35 | 1–3 Wh/jr |
| A4-C3 | Inworp-getriggerde waakstand | **Combinatie** | C2 + trigger van A2-metaaldetector | inworp → 72 h verhoogd | €0–10 extra | +0,5 Wh/jr |
| A4-C4 | "Luister naar de plop" | **Onconventioneel** | MEMS-mic + barometer + CO | continu, wake-on-event | €6–15 | < 1 Wh/jr |
| A4-C5 | Vape-neus in de trommel | **Onconventioneel** | BME688 in trommel, AI-geurprofiel | per inworp (s) | €6–10 | < 1 Wh/jr |
| A4-C6 | Hotspot-kaart met zak-tracking | Combinatie | MLX90640 boven afvalstapel + inworp-event | per inworp + elke 10 min | €28–40 | 1–3 Wh/jr |
| A4-C7 | Smeltdraad-wand | Radicaal eenvoudig (passief) | lineaire thermokabel 68 °C langs binnenwand | continu, passief | €15–40 | 0 |

---

### A4-C1 – Thermo-deksel (radicaal eenvoudig)
- **Sensor:** NTC onder deksel + NTC referentie buiten + MLX90614 (1 pixel, FOV 90°) naar beneden.
- **Meetmoment:** elke 5 min; bij ΔT > 2 K/5 min → elke 30 s.
- **Drempel:** IR-oppervlak > 70 °C óf dT/dt > 5 K/5 min t.o.v. buitenreferentie (compenseert zon); 2 opeenvolgende metingen.
- **Signaal:** "Brand/hotspot container X – niet legen, brandweer/handhaving"; push + dashboard-rood.
- **Verdienmodel:** add-on op bestaand vulgraadabonnement (€1–2/container/maand) of in basisabonnement.
- **Werking:** meet alleen het oppervlak en de kopruimte; detecteert brand/smeulen bovenin binnen minuten en een warme pluim van dieper smeulen binnen tientallen minuten. Geen voorspelling vóór TR. Feitelijk wat Sensoneo/Ecube al hebben, maar met dT/dt- en referentielogica.

### A4-C2 – Snuffelneus multi-gas (coïncidentiedetector)
- **Sensor:** Bosch BME688 (heaterprofiel getraind op elektrolytdamp/rook/compost), Figaro TGS5042 (CO, zonder heater), SHT4x; ePTFE-membraan, bovenin kopruimte.
- **Meetmoment:** elke 2 min (BME688 ULP), CO continu (passief).
- **Drempel:** ≥ 2 van 3 binnen 5 min: CO-sprong > 30 ppm, BME688-klasse "elektrolyt/rook" > 0,8, T-sprong > 3 K. Rotting (trage stijging, H₂ zonder CO-sprong) wordt weggefilterd via dC/dt.
- **Signaal:** niveau 1 "verdacht gas-event" (container prioriteren / apart legen); niveau 2 "brand".
- **Verdienmodel:** per container €2–4/maand; gemeente betaalt voor de containers met hoogste risico (stations, flats).
- **Werking:** vangt TR en smeulen sneller dan temperatuur (gas stijgt met pluim, T niet). Vangt pre-TR venting alleen als cel in de bovenste ~0,3 m ligt. Meet ook "kleine" events (vape die ventileert maar niet ontsteekt) → risicohistorie per container.

### A4-C3 – Inworp-getriggerde waakstand (combinatie met inworpdetectie)
- **Sensor:** C1 of C2, plus digitaal signaal van inworpdetector (A2 inductie/A3).
- **Meetmoment:** normaal elke 10 min; na een "verdachte inworp" 72 h elke 30–60 s en drempels 50 % lager.
- **Drempel:** Bayesiaans: P(brand) = prior(verdachte inworp, aantal sinds laatste lediging) × likelihood(gas/T). Containers met ≥ N verdachte inworpen → "apart legen / niet persen" advies.
- **Signaal:** dagelijkse risicolijst voor de planner + real-time brandalarm.
- **Verdienmodel:** bundel "inworp + bewaking" per container; hogere tier.
- **Werking:** inworpdetectie zegt *dat* er waarschijnlijk een cel in zit; continu-monitoring bevestigt of er iets *gebeurt*. Spaart energie (alleen intensief meten als het ertoe doet) en verlaagt vals alarm (rottingsgas zonder verdachte inworp = laag gewicht).

### A4-C4 – "Luister naar de plop" (onconventioneel)
- **Sensor:** MEMS-microfoon met wake-on-sound (≈10 µW), barometer BMP390, TGS5042 CO.
- **Meetmoment:** altijd luisteren op laagvermogen; bij transiënt (vent-"plop"/sis 1–10 kHz, of drukpuls > 10 Pa) → 30 min intensief gas/T meten.
- **Drempel:** akoestisch vent-signatuur-classifier (tinyML op MCU) + drukpuls + CO-stijging binnen 10 min.
- **Signaal:** "mogelijk accu geventileerd in container X" (geel) → rood bij CO-bevestiging.
- **Verdienmodel:** als C2.
- **Werking:** het openen van een veiligheidsventiel is een mechanische gebeurtenis die geluid en een kleine drukgolf maakt – signalen die door afval heen veel sneller reizen dan warmte of diffuserend gas (geluid: ms; druk: s). Daarmee is het het enige principe dat vóór TR kan waarschuwen ook voor een zak onderin. Onzeker: demping door afval, achtergrondgeluid (verkeer, inworp zelf → maskeren tijdens inworp).

### A4-C5 – Vape-neus in de trommel (onconventioneel)
- **Sensor:** BME688 (of 2 stuks met verschillende heaterprofielen) in de inworptrommel; trommel/klep drukt lucht uit de zak bij sluiten.
- **Meetmoment:** per inworp, 2–10 s stilstand (uitgangspunt 1 opdrachtgever).
- **Drempel:** AI-geurprofiel "e-liquid (PG/VG + aroma)" of "elektrolyt (DMC/EMC)" > drempel.
- **Signaal:** telling vapes/lekkende cellen per container → zelfde risico-score als A2; gedragscampagne per wijk.
- **Verdienmodel:** inworpabonnement; data voor gemeente (vape-statistiek → handhaving/statiegeld-lobby).
- **Werking:** wegwerpvapes zijn een grote bron en ruiken sterk; een gedeukte of lekkende cel geeft carbonaat-damp. Een neus in een klein volume (30–60 L trommel) ziet ppm-niveaus die in de 5 m³ container onmeetbaar zijn. Complementair aan metaaldetectie (vape = weinig metaal, moeilijk voor inductie).

### A4-C6 – Hotspot-kaart met zak-tracking (combinatie)
- **Sensor:** MLX90640 (32×24 IR) onder deksel, kijkt op de afvalstapel; trigger van inworpdetector.
- **Meetmoment:** IR-frame direct na elke inworp + elke 10 min.
- **Drempel:** pixel > 60 °C of pixel-dT/dt > 3 K/10 min boven ruimtelijk mediaan; extra gewicht op pixels waar een "verdachte zak" landde.
- **Signaal:** hotspot-alarm met locatie; "verdachte zak ligt bovenop – nu nog bereikbaar" (optie: handmatig verwijderen bij vroege lediging).
- **Verdienmodel:** premium-tier voor hotspots (stations, binnenstad).
- **Werking:** bij elke inworp registreert het IR-beeld waar de nieuwe zak landt (temperatuurverschil vers vs. oud afval). Valt die samen met een verdachte inworp, dan wordt dat gebied intensief bewaakt tot het wordt bedekt. Ziet cellen bovenin minuten vóór ontsteking (oppervlakte-opwarming), maar niets van dieper.

### A4-C7 – Smeltdraad-wand (radicaal eenvoudig, passief)
- **Sensor:** digitale lineaire thermokabel (68 °C of 88 °C) in een spiraal langs de binnenwand en onder de deksel; aangesloten op 1 GPIO van bestaande vulgraadsensor.
- **Meetmoment:** continu, 0 W.
- **Drempel:** kabel sluit kort bij lokale T > nominaal.
- **Signaal:** "brand container X" binair.
- **Verdienmodel:** eenmalige retrofit €50–100 incl. montage + €0,50/maand in bestaand abonnement.
- **Werking:** brandmeldtechniek uit tunnels/transportbanden; geen kalibratie, geen drift, geen vals alarm door rotting (die haalt nooit 68 °C). Alleen brand die de wand bereikt; geen vroegwaarschuwing.

## Hypotheses om in R2/R3 te toetsen
1. Continue monitoring = branddetectie, niet TR-voorspelling (behalve C4 en cellen bovenin).
2. Gas (C2) is 3–10× sneller dan temperatuur (C1) bij cel op > 0,3 m diepte.
3. Combinatie met inworpdetectie (C3) halveert vals alarm t.o.v. gas-alleen **[A]**.
4. Akoestische ventdetectie (C4) werkt door ≥ 1 m afval – onbekend, fysiek testen.
5. Vape-geur (C5) is in 2–10 s detecteerbaar door een dichtgeknoopte zak – onbekend, fysiek testen.
