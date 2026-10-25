# Accudetector inworpzuil – productontwerp en advies

Multi-agent ontwerpstudie (oktober 2026). Eindproduct: `deck/accudetector_inworpzuil.pptx` (+ `.pdf`).

| Map | Inhoud |
|---|---|
| `research/` | Ronde 0: research per agent (A1 risico … A8 red team), bronnen met datum |
| `debate/` | Kickoff, Ronde 1 concepten, Ronde 2 aanvallen/verdediging + shortlist, Ronde 4 scorekaart en red team |
| `experiments/` | Ronde 3: code, data en figuren per test; gedeelde parameters in `experiments/common/params.py`; scorekaart in `r4_scorekaart/` |
| `product/` | BOM per concept, productontwerp K2/K5 (MVP-meet-zuil), blokschema en montageschets |
| `deck/` | `charts.py` (grafieken) en `build_deck.py` (python-pptx) |

Reproduceren (vanuit repo-root):
```
pip install numpy scipy matplotlib python-pptx
python3 experiments/r3_risico/sim_drempel.py
python3 experiments/r3_inductie/sim_inductie.py
python3 experiments/r3_classificatie/mc.py
python3 experiments/r3_business/business.py
python3 experiments/r4_scorekaart/scorekaart.py
python3 deck/charts.py && python3 deck/build_deck.py
```

Kernadvies: geen abonnement op een accudetector in de zuil (knock-out: vals alarm en prijs ≫ vermeden schade).
Conditioneel: thermische camera boven de laadbak (inzamelaar, ≥ 10 wagens), accu-brievenbus aan de zuil (betaald door de PRO), K4 als add-on op hotspots.
MVP: één meet-zuil als go/no-go, EUR 37k / 62k / 102k, 3–6 maanden. Alle prestaties komen uit modellen, niets is fysiek gemeten.
