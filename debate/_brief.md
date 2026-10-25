# Gedeelde briefing voor alle agents

Project: goedkoop apparaat bij de inworpopening (trommel/klep) van ondergrondse restafvalcontainers in NL (eventueel openbare afvalbak, minicontainer) dat accu's/batterijen in het afval detecteert, het brandrisico per container inschat en de ophaaldienst waarschuwt. Verdienmodel: abonnement per gemeente of per container.

Uitgangspunten opdrachtgever (TOETSEN, niet aannemen):
1. Zak ligt even stil in zuil/trommel → langer meten met goedkopere sensoren.
2. Risicodrempel volstaat; niet elke batterij is gevaarlijk (aantal cellen, Wh, lithium).
3. Strandmetaaldetector bij de inworp is mogelijk het eenvoudigst/goedkoopst.
4. Melding naar ophaaldienst boven drempel.
5. Abonnement per gemeente/container.

Fysica: een stilliggende cel zendt niets uit. Detectie via materiaal (metalen behuizing, opgerolde Cu/Al folie → inductie), dichtheid/Z (röntgen), warmte, uitgassing. Toets onderscheid Li-ion vs blikjes, folie, sleutels, alkaline, elektronica zonder accu, en of hoeveelheid (cellen, Wh) te schatten is.

Meetmomenten: per inworp (s–tientallen s in trommel) én continu in container (uren–dagen).

Kwaliteitseisen: bronnen met datum (jaar/maand); aannames markeren met **[A]**; bandbreedtes laag/basis/hoog; EUR prijspeil 2026 excl. btw; SI; energie in Wh. Benoem wat je niet kon vinden. Schrijf in het Nederlands. Wees beknopt en concreet (tabellen > proza).

Repo-root: /home/user/remerchandise.github.io . Mappen: research/, debate/, experiments/, product/, deck/. Zie debate/00_orchestrator_kickoff.md voor de route en brandmomenten. Python met numpy, scipy, matplotlib beschikbaar. Je hebt WebSearch/WebFetch (laad via ToolSearch "select:WebSearch,WebFetch") — gebruik het voor actuele bronnen en prijzen. Doe GEEN git commits; de Orchestrator commit.

Format concept (Ronde 1): ID (bijv. A2-C1), naam, sensor, meetmoment, drempel, signaal, verdienmodel, ruwe kostprijs, 2–3 zinnen werking. Markeer welk concept "radicaal eenvoudig" en welk "onconventioneel" is.
