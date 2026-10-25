"""A1 – Risicomodel (Ronde 3). Importeerbaar door A6.

Gebruik (vanuit repo-root):
    import sys; sys.path.insert(0, "experiments/r3_risico")
    from risk import p_fire, wheq, p_fire_from_wheq, expected_fires_per_1000

Model (research/A1_risicobenchmark.md §7):
    Wh-eq_i  = Wh_i * w_chem_i * w_state_i            (params.ITEMS)
    p_i      = 1 - exp(-k * Wh-eq_i)                  per item per ketenpassage (inworp -> pers -> verwerking)
    P_brand  = 1 - prod(1 - p_i) = 1 - exp(-k * sum Wh-eq_i)
    k        = params.K_PER_WHEQ[scenario]  (top-down gekalibreerd op NL-brandcijfers)
"""
from __future__ import annotations

import math
import os
import sys
from collections.abc import Iterable, Mapping

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "common"))
import params  # noqa: E402

ITEMS = params.ITEMS
K_PER_WHEQ = params.K_PER_WHEQ
_IDX = {"laag": 0, "basis": 1, "hoog": 2}


def k_value(k="basis") -> float:
    """k als getal; accepteert 'laag'|'basis'|'hoog' of een float."""
    return float(K_PER_WHEQ[k]) if isinstance(k, str) else float(k)


def wheq(cls: str, wh: float | None = None, wh_case: str = "basis",
         w_state: float | None = None) -> float:
    """Wh-eq van één item. wh=None -> params-waarde (laag/basis/hoog via wh_case)."""
    it = ITEMS[cls]
    e = it["wh"][_IDX[wh_case]] if wh is None else float(wh)
    ws = it["w_state"] if w_state is None else float(w_state)
    return e * it["w_chem"] * ws


def _total_wheq(items) -> float:
    """Somt Wh-eq over diverse invoervormen:
    - Mapping {klasse: aantal}
    - iterable van: 'klasse' | ('klasse', wh) | {'cls': klasse, 'wh': wh(optioneel), 'n': aantal(optioneel)}
      | float/int (al een Wh-eq-waarde)
    """
    if isinstance(items, Mapping) and "cls" not in items:
        return sum(n * wheq(c) for c, n in items.items())
    if isinstance(items, Mapping):
        items = [items]
    tot = 0.0
    for x in items:
        if isinstance(x, str):
            tot += wheq(x)
        elif isinstance(x, (int, float)):
            tot += float(x)
        elif isinstance(x, Mapping):
            tot += x.get("n", 1) * wheq(x["cls"], x.get("wh"))
        else:  # tuple/list
            c, w = x[0], (x[1] if len(x) > 1 else None)
            tot += wheq(c, w)
    return tot


def p_fire_from_wheq(r, k="basis"):
    """P_brand bij totale Wh-eq r (float of numpy-array)."""
    kk = k_value(k)
    try:
        import numpy as np
        return -np.expm1(-kk * np.asarray(r, dtype=float))
    except ImportError:  # pragma: no cover
        return -math.expm1(-kk * float(r))


def p_fire(items, k="basis") -> float:
    """Brandkans per ketenpassage voor een verzameling items (één zak, inworp of containerlediging).

    >>> p_fire({"powerbank": 1})                 # ~4.4e-5
    >>> p_fire(["vape", ("laptop_gereedschap", 80)], k="hoog")
    """
    return float(p_fire_from_wheq(_total_wheq(items), k))


def p_item(cls: str, wh: float | None = None, k="basis") -> float:
    return float(p_fire_from_wheq(wheq(cls, wh), k))


# --- Verwachte branden, consistent gekalibreerd (A1 R0 §6b) -------------------------------
# Waargenomen NL wagenbranden x onderregistratie, gedeeld door NL lediging-equivalenten.
NL = {
    "restafval_t": 2.9e6,                       # [A] huishoudelijk restafval NL per jaar
    "t_per_emptying": 100 * params.BAG["mass_kg_median"] / 1000,   # 0,5 t
    "fires_obs": {"laag": 36, "basis": 52, "hoog": 120},           # NVRD / HvN / VA
    "underreg": {"laag": 1, "basis": 3, "hoog": 10},               # [A]
}


def fires_per_emptying(case="basis") -> float:
    n_emp = NL["restafval_t"] / NL["t_per_emptying"]
    return NL["fires_obs"][case] * NL["underreg"][case] / n_emp


def expected_fires_per_1000(case="basis", emptyings_per_year=None) -> float:
    """Verwachte brandincidenten per 1.000 containers per jaar (waarneming-gekalibreerd)."""
    e = emptyings_per_year or params.CONTAINER["emptyings_per_year"]
    return 1000 * e * fires_per_emptying(case)


def mean_wheq_per_emptying(scale=1.0, bags=100) -> float:
    """Verwachte Wh-eq per lediging volgens params.ITEMS (basis-Wh)."""
    return bags * scale * sum(it["mean"] * wheq(c) for c, it in ITEMS.items() if it["li"])


def calibrated_k(case="basis", scale=1.0) -> float:
    """k zodanig dat params-itemmix x scale de waargenomen brandfrequentie reproduceert."""
    return fires_per_emptying(case) / mean_wheq_per_emptying(scale)


if __name__ == "__main__":
    print("Wh-eq per lediging (basis):", round(mean_wheq_per_emptying(), 2))
    for c in ("laag", "basis", "hoog"):
        print(c, "branden/1000 cont/jr:", round(expected_fires_per_1000(c), 2),
              " k_cal:", f"{calibrated_k(c):.2e}", " params k:", f"{K_PER_WHEQ[c]:.1e}")
    print("p_fire powerbank:", f"{p_fire({'powerbank': 1}):.2e}")
    print("p_fire e-bike (hoog k):", f"{p_fire(['ebike_step'], k='hoog'):.2e}")
