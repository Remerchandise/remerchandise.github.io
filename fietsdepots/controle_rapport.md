# Controlerapport fietsdepots Nederland

Controle door agent 13 op 2026-11-02. Invoer: `merged.json` (170 depots, 342 gemeenten, CBS 86247NED, peildatum 1-1-2026). Uitvoer: `gecontroleerd.json`, met dezelfde structuur plus het veld `controle` per depot.

## Werkwijze

- Alle 363 unieke URL's (bron_url en website van depots, bron_url van gemeenten) opgehaald met curl (-L, time-out 20 s, max. 4 parallel, 0,5 s pauze). Uitkomst: 325× 200, 30× 403, 6× 404, 2× geen verbinding. Daarnaast 2 pagina's met "pagina niet gevonden" bij status 200 en 1 redirect naar een nieuwsoverzicht. verlorenofgevonden.nl is alleen via /voorwerp/ en /overzicht opgevraagd; de 3 /api/object/-URL's zijn omgezet naar /voorwerp/.
- 119 depots met adres opnieuw gegeocodeerd via PDOK Locatieserver (adres, of weg als alleen de straat bekend is). Daarbij postcode, plaats, huisnummer en afstand (grens 300 m) vergeleken.
- Actualiteit: paginadatums (meta dateModified/DCTERMS, "geldend vanaf", Last-Modified) en de jaartallen in de notities nagelopen. Grens: november 2024.
- Consistentie: type, depot_id-verwijzingen, bediende_gemeenten tegenover de dekkingslijst, en depots met het gemeentehuis of stadskantoor als adres.

## Totalen depots

Unieke depots: **170**

| type | aantal |
|---|---|
| gemeentelijk | 128 |
| extern beheerd | 38 |
| regionaal | 4 |

| betrouwbaarheid | aantal | (vóór controle) |
|---|---|---|
| hoog | 72 | 74 |
| middel | 62 | 78 |
| laag | 36 | 18 |

Depots zonder coördinaten: **52**. Daarvan hebben er 51 geen adres; NH-gooise-meren heeft alleen een omschrijving ("naast station Naarden-Bussum") en is niet gegeocodeerd. Depots met benaderde coördinaten (alleen straat bekend, of huisnummer niet in BAG): 15.

## Gemeenten per uitkomst

Totaal: A = 141, B = 36, C = 165 (samen 342)

| provincie | A | B | C | totaal |
|---|---|---|---|---|
| Drenthe | 4 | 2 | 6 | 12 |
| Flevoland | 4 | 1 | 1 | 6 |
| Fryslân | 6 | 2 | 10 | 18 |
| Gelderland | 27 | 8 | 16 | 51 |
| Groningen | 5 | 1 | 4 | 10 |
| Limburg | 8 | 1 | 22 | 31 |
| Noord-Brabant | 27 | 3 | 26 | 56 |
| Noord-Holland | 10 | 6 | 28 | 44 |
| Overijssel | 14 | 2 | 9 | 25 |
| Utrecht | 13 | 3 | 10 | 26 |
| Zeeland | 5 | 1 | 7 | 13 |
| Zuid-Holland | 18 | 6 | 26 | 50 |

## Gecorrigeerde records

| record | correctie |
|---|---|
| FR-leeuwarden | bron_url /api/ -> /voorwerp/ (robots.txt); type gemeentelijk -> extern beheerd |
| FR-smallingerland | bron_url /api/ -> /voorwerp/ (robots.txt) |
| FR-ameland | betrouwbaarheid middel -> laag (actualiteit) |
| GE-harderwijk | betrouwbaarheid middel -> laag (actualiteit) |
| GE-elburg | postcode 8082 AC -> 8082 AD (BAG/PDOK) |
| GE-hattem | betrouwbaarheid middel -> laag (actualiteit) |
| GE-maasdriel | betrouwbaarheid middel -> laag (adres = gemeentehuis/stadskantoor) |
| GE-epe | betrouwbaarheid hoog -> laag (adres = gemeentehuis/stadskantoor) |
| GE-avri | type regionaal -> extern beheerd; betrouwbaarheid middel -> laag (actualiteit) |
| GR-het-hogeland | betrouwbaarheid middel -> laag (actualiteit) |
| LI-sittard-geleen | type gemeentelijk -> extern beheerd |
| NB-waalwijk-twiddus | betrouwbaarheid middel -> laag (actualiteit) |
| NB-halderberge | betrouwbaarheid middel -> laag (actualiteit) |
| NB-veldhoven | betrouwbaarheid middel -> laag (actualiteit) |
| NB-loon-op-zand | betrouwbaarheid middel -> laag (actualiteit) |
| NH-haarlem | type gemeentelijk -> regionaal |
| NH-amstelveen-gemeentewerf | type gemeentelijk -> regionaal |
| OV-wierden-fietskelder | betrouwbaarheid middel -> laag (adres = gemeentehuis/stadskantoor) |
| UT-houten | betrouwbaarheid middel -> laag (dode link) |
| UT-woudenberg | betrouwbaarheid middel -> laag (actualiteit) |
| ZE-zierikzee-zuidhoek | betrouwbaarheid hoog -> laag (actualiteit) |
| ZH-dordrecht | betrouwbaarheid middel -> laag (adres = gemeentehuis/stadskantoor) |
| ZH-katwijk-milieustraat | type gemeentelijk -> regionaal |
| ZH-schiedam | betrouwbaarheid middel -> laag (adres = gemeentehuis/stadskantoor) |
| ZH-wassenaar | betrouwbaarheid middel -> laag (adres = gemeentehuis/stadskantoor) |
| Ooststellingwerf | gemeente bron_url /api/ -> /voorwerp/ |
| Smallingerland | gemeente bron_url /api/ -> /voorwerp/ |

Toelichting bij de categorieën:
- **Actualiteit**: de enige bron dateert van vóór november 2024 (beleidsregels uit 2013-2024 die formeel nog gelden, of pagina's met een wijzigingsdatum in 2019-2023), en geen recentere bron bevestigt het.
- **Adres = gemeentehuis of stadskantoor**: de uitkomst A/B is blijven staan omdat er volgens de bron wel fysieke opslag of een ophaalpunt is. De betrouwbaarheid staat op laag tot de fysieke opslaglocatie is bevestigd.
- **Dode link**: alleen UT-houten is verlaagd. GE-renkum, GE-ermelo-proson, NB-geldrop-mierlo-lunet en NB-maashorst hebben ook een dode bron, maar stonden al op laag.
- **403 of geen verbinding** (30 + 2 URL's): genoteerd als "niet automatisch te verifiëren"; de betrouwbaarheid is daarom niet verlaagd.

Overige bevindingen (niet gewijzigd):
- GE-barneveld: PDOK vindt Baron van Nagellstraat 176 zonder postcode. De postcode 3771 LP kan daarom niet worden bevestigd; de coördinaten kloppen (0 m).
- Nevendepots GE-nijmegen-houthof, UT-utrecht-fietsverwijderd en ZH-dordrecht-kelvinstraat: de gemeente verwijst in de dekkingslijst naar het hoofddepot (één depot_id per gemeente). bediende_gemeenten is daar correct; dat is geen fout.
- Bij 13 depots staat het adres niet op de bron_url zelf, maar op een andere pagina die in de notities staat (bijv. contact- of werfpagina, iLost).
- GE-nijmegen en GE-nijmegen-houthof: de AFAC-site heeft Last-Modified 2022, maar nijmegen.nl (200) bevestigt de AFAC actueel. Daarom blijft de betrouwbaarheid hoog.
- NH-haarlem: de website fietsdepothaarlem.nl heeft een ongeldig TLS-certificaat en is niet te verifiëren.
- OV-zwolle-afac: een gemeentebericht meldt een tijdelijke verhuizing naar de Bogenhal. Het actuele adres moet worden nagebeld.

## Handmatig nabellen (233 gemeenten)

Dit zijn alle C-gemeenten en de A/B-gemeenten waarvan het depot geen adres heeft of betrouwbaarheid "laag" heeft. Het gemeentenummer staat er alleen bij als het als enig 14 0xx-nummer in de eigen gegevens van de gemeente voorkomt.

| gemeente | provincie | reden | algemeen nummer |
|---|---|---|---|
| Aa en Hunze | Drenthe | C: geen depot gevonden |  |
| De Wolden | Drenthe | C: geen depot gevonden | 14 0528 |
| Hoogeveen | Drenthe | C: geen depot gevonden | 14 0528 |
| Midden-Drenthe | Drenthe | C: geen depot gevonden |  |
| Noordenveld | Drenthe | C: geen depot gevonden |  |
| Tynaarlo | Drenthe | C: geen depot gevonden |  |
| Westerveld | Drenthe | A via DR-westerveld: depot zonder adres | 14 0521 |
| Lelystad | Flevoland | A via FL-lelystad: betrouwbaarheid laag | 14 0320 |
| Zeewolde | Flevoland | C: geen depot gevonden |  |
| Ameland | Fryslân | A via FR-ameland: depot zonder adres, betrouwbaarheid laag |  |
| Dantumadiel | Fryslân | C: geen depot gevonden |  |
| De Fryske Marren | Fryslân | C: geen depot gevonden |  |
| Noardeast-Fryslân | Fryslân | A via FR-noardeast-fryslan: depot zonder adres |  |
| Ooststellingwerf | Fryslân | C: geen depot gevonden |  |
| Opsterland | Fryslân | C: geen depot gevonden |  |
| Schiermonnikoog | Fryslân | C: geen depot gevonden |  |
| Smallingerland | Fryslân | A via FR-smallingerland: depot zonder adres |  |
| Súdwest-Fryslân | Fryslân | C: geen depot gevonden |  |
| Terschelling | Fryslân | C: geen depot gevonden |  |
| Vlieland | Fryslân | C: geen depot gevonden |  |
| Waadhoeke | Fryslân | C: geen depot gevonden |  |
| Weststellingwerf | Fryslân | C: geen depot gevonden |  |
| Aalten | Gelderland | C: geen depot gevonden |  |
| Berg en Dal | Gelderland | A via GE-berg-en-dal: depot zonder adres |  |
| Berkelland | Gelderland | C: geen depot gevonden |  |
| Bronckhorst | Gelderland | C: geen depot gevonden |  |
| Brummen | Gelderland | C: geen depot gevonden |  |
| Buren | Gelderland | C: geen depot gevonden |  |
| Culemborg | Gelderland | A via GE-culemborg: depot zonder adres |  |
| Doesburg | Gelderland | C: geen depot gevonden |  |
| Doetinchem | Gelderland | A via GE-doetinchem: depot zonder adres |  |
| Druten | Gelderland | C: geen depot gevonden |  |
| Duiven | Gelderland | A via GE-duiven: depot zonder adres |  |
| Epe | Gelderland | A via GE-epe: betrouwbaarheid laag |  |
| Ermelo | Gelderland | B via GE-ermelo-proson: betrouwbaarheid laag |  |
| Harderwijk | Gelderland | A via GE-harderwijk: betrouwbaarheid laag |  |
| Hattem | Gelderland | A via GE-hattem: betrouwbaarheid laag |  |
| Heerde | Gelderland | C: geen depot gevonden |  |
| Heumen | Gelderland | C: geen depot gevonden |  |
| Lingewaard | Gelderland | C: geen depot gevonden |  |
| Maasdriel | Gelderland | A via GE-maasdriel: betrouwbaarheid laag |  |
| Montferland | Gelderland | A via GE-montferland: depot zonder adres |  |
| Neder-Betuwe | Gelderland | B via GE-avri: depot zonder adres, betrouwbaarheid laag |  |
| Nunspeet | Gelderland | A via GE-nunspeet: depot zonder adres |  |
| Oost Gelre | Gelderland | A via GE-oost-gelre: depot zonder adres, betrouwbaarheid laag |  |
| Oude IJsselstreek | Gelderland | C: geen depot gevonden |  |
| Overbetuwe | Gelderland | B via GE-overbetuwe-leergeld: depot zonder adres |  |
| Putten | Gelderland | C: geen depot gevonden |  |
| Renkum | Gelderland | A via GE-renkum: betrouwbaarheid laag |  |
| Rozendaal | Gelderland | C: geen depot gevonden |  |
| Scherpenzeel | Gelderland | C: geen depot gevonden |  |
| Tiel | Gelderland | B via GE-tiel: depot zonder adres |  |
| Voorst | Gelderland | C: geen depot gevonden |  |
| West Maas en Waal | Gelderland | C: geen depot gevonden |  |
| Westervoort | Gelderland | A via GE-westervoort: depot zonder adres |  |
| Wijchen | Gelderland | B via GE-wijchen: depot zonder adres |  |
| Winterswijk | Gelderland | A via GE-winterswijk: depot zonder adres |  |
| Zaltbommel | Gelderland | A via GE-zaltbommel: depot zonder adres | 14 0418 |
| Zevenaar | Gelderland | A via GE-zevenaar: depot zonder adres, betrouwbaarheid laag |  |
| Zutphen | Gelderland | A via GE-zutphen: depot zonder adres, betrouwbaarheid laag |  |
| Het Hogeland | Groningen | A via GR-het-hogeland: depot zonder adres, betrouwbaarheid laag |  |
| Midden-Groningen | Groningen | A via GR-midden-groningen: depot zonder adres |  |
| Pekela | Groningen | C: geen depot gevonden |  |
| Stadskanaal | Groningen | C: geen depot gevonden |  |
| Veendam | Groningen | C: geen depot gevonden |  |
| Westerkwartier | Groningen | A via GR-westerkwartier: depot zonder adres | 14 0594 |
| Westerwolde | Groningen | C: geen depot gevonden |  |
| Beekdaelen | Limburg | C: geen depot gevonden |  |
| Beesel | Limburg | C: geen depot gevonden |  |
| Bergen (L.) | Limburg | C: geen depot gevonden |  |
| Brunssum | Limburg | C: geen depot gevonden |  |
| Echt-Susteren | Limburg | C: geen depot gevonden |  |
| Eijsden-Margraten | Limburg | C: geen depot gevonden |  |
| Gennep | Limburg | C: geen depot gevonden |  |
| Gulpen-Wittem | Limburg | C: geen depot gevonden | 14 043 |
| Heerlen | Limburg | A via LI-heerlen: depot zonder adres | 14 045 |
| Horst aan de Maas | Limburg | C: geen depot gevonden |  |
| Kerkrade | Limburg | C: geen depot gevonden |  |
| Leudal | Limburg | C: geen depot gevonden |  |
| Maasgouw | Limburg | C: geen depot gevonden |  |
| Meerssen | Limburg | C: geen depot gevonden |  |
| Mook en Middelaar | Limburg | C: geen depot gevonden |  |
| Nederweert | Limburg | A via LI-nederweert: depot zonder adres, betrouwbaarheid laag |  |
| Peel en Maas | Limburg | C: geen depot gevonden |  |
| Roerdalen | Limburg | C: geen depot gevonden |  |
| Simpelveld | Limburg | C: geen depot gevonden |  |
| Stein (L.) | Limburg | C: geen depot gevonden |  |
| Vaals | Limburg | C: geen depot gevonden |  |
| Valkenburg aan de Geul | Limburg | C: geen depot gevonden | 14 043 |
| Venlo | Limburg | A via LI-venlo: depot zonder adres | 14 077 |
| Venray | Limburg | C: geen depot gevonden |  |
| Voerendaal | Limburg | C: geen depot gevonden |  |
| Weert | Limburg | A via LI-weert: depot zonder adres, betrouwbaarheid laag |  |
| Alphen-Chaam | Noord-Brabant | C: geen depot gevonden |  |
| Altena | Noord-Brabant | C: geen depot gevonden |  |
| Asten | Noord-Brabant | A via NB-asten: depot zonder adres, betrouwbaarheid laag |  |
| Baarle-Nassau | Noord-Brabant | C: geen depot gevonden |  |
| Bergeijk | Noord-Brabant | C: geen depot gevonden |  |
| Bergen op Zoom | Noord-Brabant | A via NB-bergen-op-zoom: depot zonder adres | 14 0164 |
| Bernheze | Noord-Brabant | C: geen depot gevonden |  |
| Best | Noord-Brabant | A via NB-best: depot zonder adres | 14 0499 |
| Boekel | Noord-Brabant | C: geen depot gevonden |  |
| Cranendonck | Noord-Brabant | C: geen depot gevonden |  |
| Dongen | Noord-Brabant | C: geen depot gevonden |  |
| Drimmelen | Noord-Brabant | C: geen depot gevonden |  |
| Eersel | Noord-Brabant | C: geen depot gevonden |  |
| Etten-Leur | Noord-Brabant | C: geen depot gevonden |  |
| Geertruidenberg | Noord-Brabant | C: geen depot gevonden |  |
| Geldrop-Mierlo | Noord-Brabant | B via NB-geldrop-mierlo-lunet: depot zonder adres, betrouwbaarheid laag |  |
| Goirle | Noord-Brabant | C: geen depot gevonden |  |
| Halderberge | Noord-Brabant | A via NB-halderberge: betrouwbaarheid laag |  |
| Heeze-Leende | Noord-Brabant | A via NB-heeze-leende: depot zonder adres |  |
| Heusden | Noord-Brabant | C: geen depot gevonden |  |
| Hilvarenbeek | Noord-Brabant | C: geen depot gevonden |  |
| Laarbeek | Noord-Brabant | A via NB-laarbeek: depot zonder adres |  |
| Land van Cuijk | Noord-Brabant | C: geen depot gevonden |  |
| Loon op Zand | Noord-Brabant | A via NB-loon-op-zand: betrouwbaarheid laag |  |
| Maashorst | Noord-Brabant | A via NB-maashorst: betrouwbaarheid laag |  |
| Nuenen, Gerwen en Nederwetten | Noord-Brabant | C: geen depot gevonden |  |
| Oirschot | Noord-Brabant | C: geen depot gevonden |  |
| Oisterwijk | Noord-Brabant | C: geen depot gevonden |  |
| Reusel-De Mierden | Noord-Brabant | A via NB-reusel-de-mierden: depot zonder adres, betrouwbaarheid laag |  |
| Rucphen | Noord-Brabant | C: geen depot gevonden |  |
| Sint-Michielsgestel | Noord-Brabant | C: geen depot gevonden |  |
| Someren | Noord-Brabant | C: geen depot gevonden |  |
| Son en Breugel | Noord-Brabant | C: geen depot gevonden |  |
| Steenbergen | Noord-Brabant | A via NB-steenbergen: depot zonder adres |  |
| Valkenswaard | Noord-Brabant | A via NB-valkenswaard: depot zonder adres |  |
| Veldhoven | Noord-Brabant | A via NB-veldhoven: depot zonder adres, betrouwbaarheid laag | 14 040 |
| Waalre | Noord-Brabant | C: geen depot gevonden |  |
| Waalwijk | Noord-Brabant | B via NB-waalwijk-twiddus: betrouwbaarheid laag |  |
| Woensdrecht | Noord-Brabant | C: geen depot gevonden |  |
| Zundert | Noord-Brabant | C: geen depot gevonden |  |
| Alkmaar | Noord-Holland | B via NH-alkmaar-stadswerk072: depot zonder adres | 14 072 |
| Bergen (NH.) | Noord-Holland | C: geen depot gevonden |  |
| Beverwijk | Noord-Holland | C: geen depot gevonden |  |
| Blaricum | Noord-Holland | C: geen depot gevonden |  |
| Castricum | Noord-Holland | C: geen depot gevonden |  |
| Diemen | Noord-Holland | C: geen depot gevonden |  |
| Dijk en Waard | Noord-Holland | C: geen depot gevonden |  |
| Drechterland | Noord-Holland | C: geen depot gevonden |  |
| Edam-Volendam | Noord-Holland | C: geen depot gevonden |  |
| Enkhuizen | Noord-Holland | C: geen depot gevonden |  |
| Heemskerk | Noord-Holland | C: geen depot gevonden |  |
| Heiloo | Noord-Holland | C: geen depot gevonden |  |
| Hollands Kroon | Noord-Holland | C: geen depot gevonden |  |
| Hoorn | Noord-Holland | B via NH-afac-hoorn: depot zonder adres |  |
| Huizen | Noord-Holland | C: geen depot gevonden |  |
| Koggenland | Noord-Holland | C: geen depot gevonden |  |
| Landsmeer | Noord-Holland | C: geen depot gevonden |  |
| Laren (NH.) | Noord-Holland | C: geen depot gevonden |  |
| Medemblik | Noord-Holland | C: geen depot gevonden |  |
| Oostzaan | Noord-Holland | C: geen depot gevonden |  |
| Opmeer | Noord-Holland | A via NH-opmeer-gemeentewerf: depot zonder adres, betrouwbaarheid laag |  |
| Ouder-Amstel | Noord-Holland | C: geen depot gevonden |  |
| Purmerend | Noord-Holland | C: geen depot gevonden |  |
| Stede Broec | Noord-Holland | C: geen depot gevonden |  |
| Texel | Noord-Holland | C: geen depot gevonden |  |
| Uitgeest | Noord-Holland | C: geen depot gevonden |  |
| Uithoorn | Noord-Holland | C: geen depot gevonden |  |
| Velsen | Noord-Holland | C: geen depot gevonden |  |
| Waterland | Noord-Holland | C: geen depot gevonden |  |
| Wijdemeren | Noord-Holland | C: geen depot gevonden |  |
| Wormerland | Noord-Holland | C: geen depot gevonden |  |
| Dinkelland | Overijssel | C: geen depot gevonden |  |
| Hardenberg | Overijssel | A via OV-hardenberg: depot zonder adres | 14 0523 |
| Hof van Twente | Overijssel | C: geen depot gevonden |  |
| Kampen | Overijssel | A via OV-kampen: depot zonder adres |  |
| Losser | Overijssel | C: geen depot gevonden |  |
| Olst-Wijhe | Overijssel | C: geen depot gevonden |  |
| Ommen | Overijssel | C: geen depot gevonden | 14 0529 |
| Staphorst | Overijssel | C: geen depot gevonden |  |
| Steenwijkerland | Overijssel | C: geen depot gevonden | 14 0521 |
| Tubbergen | Overijssel | C: geen depot gevonden |  |
| Wierden | Overijssel | A via OV-wierden-fietskelder: betrouwbaarheid laag |  |
| Zwartewaterland | Overijssel | C: geen depot gevonden | 14 038 |
| Bunschoten | Utrecht | C: geen depot gevonden |  |
| De Bilt | Utrecht | C: geen depot gevonden |  |
| De Ronde Venen | Utrecht | C: geen depot gevonden |  |
| Eemnes | Utrecht | C: geen depot gevonden |  |
| Houten | Utrecht | A via UT-houten: depot zonder adres, betrouwbaarheid laag |  |
| IJsselstein | Utrecht | A via UT-ijsselstein: depot zonder adres, betrouwbaarheid laag | 14 030 |
| Leusden | Utrecht | C: geen depot gevonden |  |
| Lopik | Utrecht | C: geen depot gevonden |  |
| Montfoort | Utrecht | C: geen depot gevonden |  |
| Nieuwegein | Utrecht | C: geen depot gevonden |  |
| Renswoude | Utrecht | C: geen depot gevonden |  |
| Stichtse Vecht | Utrecht | A via UT-stichtse-vecht: depot zonder adres, betrouwbaarheid laag |  |
| Utrechtse Heuvelrug | Utrecht | A via UT-utrechtse-heuvelrug: depot zonder adres, betrouwbaarheid laag |  |
| Vijfheerenlanden | Utrecht | A via UT-vijfheerenlanden: depot zonder adres |  |
| Wijk bij Duurstede | Utrecht | C: geen depot gevonden |  |
| Woudenberg | Utrecht | A via UT-woudenberg: depot zonder adres, betrouwbaarheid laag | 14 033 |
| Zeist | Utrecht | A via UT-zeist: depot zonder adres | 14 030 |
| Borsele | Zeeland | C: geen depot gevonden |  |
| Kapelle | Zeeland | C: geen depot gevonden |  |
| Middelburg (Z.) | Zeeland | C: geen depot gevonden |  |
| Noord-Beveland | Zeeland | A via ZE-noord-beveland-gemeente: depot zonder adres | 14 0113 |
| Reimerswaal | Zeeland | B via ZE-rilland-vanhoek: depot zonder adres, betrouwbaarheid laag |  |
| Schouwen-Duiveland | Zeeland | A via ZE-zierikzee-zuidhoek: betrouwbaarheid laag |  |
| Sluis | Zeeland | C: geen depot gevonden |  |
| Tholen | Zeeland | C: geen depot gevonden |  |
| Veere | Zeeland | C: geen depot gevonden |  |
| Vlissingen | Zeeland | C: geen depot gevonden |  |
| Alblasserdam | Zuid-Holland | C: geen depot gevonden |  |
| Albrandswaard | Zuid-Holland | C: geen depot gevonden |  |
| Bodegraven-Reeuwijk | Zuid-Holland | C: geen depot gevonden |  |
| Dordrecht | Zuid-Holland | A via ZH-dordrecht: betrouwbaarheid laag | 14 078 |
| Gorinchem | Zuid-Holland | C: geen depot gevonden | 14 0183 |
| Hardinxveld-Giessendam | Zuid-Holland | C: geen depot gevonden | 14 0184 |
| Hendrik-Ido-Ambacht | Zuid-Holland | C: geen depot gevonden |  |
| Hillegom | Zuid-Holland | C: geen depot gevonden | 14 0252 |
| Hoeksche Waard | Zuid-Holland | C: geen depot gevonden |  |
| Kaag en Braassem | Zuid-Holland | C: geen depot gevonden |  |
| Krimpen aan den IJssel | Zuid-Holland | C: geen depot gevonden |  |
| Krimpenerwaard | Zuid-Holland | C: geen depot gevonden | 14 0182 |
| Leiderdorp | Zuid-Holland | A via ZH-leiderdorp-gemeentewerf: betrouwbaarheid laag |  |
| Lisse | Zuid-Holland | C: geen depot gevonden | 14 0252 |
| Maassluis | Zuid-Holland | C: geen depot gevonden |  |
| Midden-Delfland | Zuid-Holland | C: geen depot gevonden |  |
| Molenlanden | Zuid-Holland | C: geen depot gevonden |  |
| Nieuwkoop | Zuid-Holland | C: geen depot gevonden |  |
| Nissewaard | Zuid-Holland | C: geen depot gevonden | 14 0181 |
| Oegstgeest | Zuid-Holland | C: geen depot gevonden |  |
| Papendrecht | Zuid-Holland | C: geen depot gevonden | 14 078 |
| Ridderkerk | Zuid-Holland | C: geen depot gevonden |  |
| Schiedam | Zuid-Holland | A via ZH-schiedam: betrouwbaarheid laag | 14 010 |
| Sliedrecht | Zuid-Holland | C: geen depot gevonden |  |
| Teylingen | Zuid-Holland | C: geen depot gevonden | 14 0252 |
| Vlaardingen | Zuid-Holland | C: geen depot gevonden |  |
| Wassenaar | Zuid-Holland | A via ZH-wassenaar: betrouwbaarheid laag |  |
| Westland | Zuid-Holland | C: geen depot gevonden |  |
| Zoeterwoude | Zuid-Holland | C: geen depot gevonden |  |
| Zuidplas | Zuid-Holland | C: geen depot gevonden |  |
