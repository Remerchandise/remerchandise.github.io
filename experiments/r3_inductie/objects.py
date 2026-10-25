"""Objectbibliotheek A2 (Ronde 3): elk object = lijst eddy-/ferro-modes (dipoolbenadering).

Mode = (kind, diag3 [cm^3], tau [s]); kind 1 = ferro (magnetische term M/(1+jw*tau_w)),
kind 2 = wervelstroom (-A*jw*tau/(1+jw*tau)). Body-as = z. Alles orde-grootte, zie RESULTATEN.md.
Formules: dunne cilinderschil tau=mu0*sigma*a*d/2; ferro-wanddiffusie tau_w=mur*mu0*sigma*d^2;
dunne schijf alpha_hf=-(8/3)a^3, tau~mu0*(sigma*d)*a/4 [A]; ferro schil chi_eff=mur*2d/a (axiaal),
mur*d/a (transversaal), demagnetisatie N_ax=1/(1+1.6*l/2a) [A, benadering prolate].
"""
import numpy as np

MU0 = 4e-7 * np.pi
MAXM = 8  # max modes per object (padding)


def _ln(rng, med, f):
    """lognormaal rond mediaan med met factor f (1 sigma)."""
    return med * np.exp(rng.normal(0, np.log(f)))


def shell(a, l, d, sig, mur=None):
    V = np.pi * a * a * l * 1e6  # cm^3
    p = l / (2 * a)
    nax = 1 / (1 + 1.6 * p)
    ntr = (1 - nax) / 2
    modes = []
    A = np.array([V / (1 - ntr), V / (1 - ntr), V / (1 - nax)])
    modes.append((2, A, MU0 * sig * a * d / 2))
    if mur:
        cax, ctr = mur * 2 * d / a, mur * d / a
        M = np.array([V * ctr / (1 + ntr * ctr), V * ctr / (1 + ntr * ctr), V * cax / (1 + nax * cax)])
        modes.append((1, M, mur * MU0 * sig * d * d))
    return modes


def disc(a, sigd, frac=1.0, edge=0.05):
    Az = 8 / 3 * (a * 100) ** 3 * frac
    return [(2, np.array([edge * Az, edge * Az, Az]), MU0 * sigd * a / 4)]


def scale(modes, k):
    return [(kd, D * k, t) for kd, D, t in modes]


def cell18650(rng, big=None):
    big = rng.random() < 0.2 if big is None else big
    a, l = (0.0105, 0.070) if big else (0.009, 0.065)
    d = rng.uniform(0.2e-3, 0.3e-3)
    m = shell(a, l, d, _ln(rng, 6e6, 1.2), mur=_ln(rng, 150, 1.6))
    V = np.pi * a * a * l * 1e6
    m.append((2, np.array([0.5 * V, 0.5 * V, 0.05 * V]), rng.uniform(10e-6, 30e-6)))  # jellyroll, axiaal open spiraal
    return m


def make(item, rng, wh):
    """Geef modes voor één object van klasse item (params.ITEMS-sleutel) met energie wh."""
    m = []
    if item == "cel_18650":
        m = cell18650(rng)
    elif item == "alkaline":
        r = rng.random()
        a, l = (0.007, 0.050) if r < 0.8 else ((0.00525, 0.0445) if r < 0.95 else (0.013, 0.050))
        m = shell(a, l, rng.uniform(0.2e-3, 0.3e-3), _ln(rng, 6e6, 1.2), mur=_ln(rng, 150, 1.6))
        V = np.pi * a * a * l * 1e6
        m.append((2, np.array([0.1, 0.1, 0.1]) * V, 3e-6))  # Zn-gel/MnO2 slecht geleidend
    elif item == "knoopcel":
        m = [(1, np.array([2.5, 2.5, 1.0]) * _ln(rng, 1, 1.3), 60e-6)] + disc(0.010, 6e6 * 0.25e-3 * 2, 1.0, 0.1)
    elif item == "vape":
        if rng.random() < 0.6:  # Al-huls
            m += shell(rng.uniform(0.008, 0.011), rng.uniform(0.07, 0.11), rng.uniform(0.3e-3, 0.6e-3), 2.5e7)
            shield = 0.5
        else:
            shield = 1.0
        if rng.random() < 0.3:  # stalen 13350/13450-cel
            mm = shell(0.0065, 0.04, 0.2e-3, 6e6, mur=_ln(rng, 150, 1.6))
            m += scale(mm, shield)
        else:  # kleine pouch
            m += scale(disc(0.012, 4000, 0.6), shield)
        m.append((1, np.array([0.3, 0.3, 0.3]), 30e-6))  # verwarmingsspiraal/contacten
    elif item == "li_klein_overig":
        m = disc(0.008, 3000, 0.8) + [(2, np.array([0.1, 0.1, 1.0]), 5e-6)]
    elif item == "telefoon":
        a = rng.uniform(0.035, 0.042) * np.sqrt(max(wh, 5) / 15) ** 0.5
        m = disc(a, rng.uniform(8000, 16000), 0.7) + disc(a, 3.5e7 * 40e-6, 0.3)
        if rng.random() < 0.7:  # Al-frame
            m.append((2, np.array([0.05, 0.05, 1.0]) * 0.6 * 8 / 3 * ((a + 0.005) * 100) ** 3, rng.uniform(60e-6, 200e-6)))
        m.append((1, np.array([1.5, 1.5, 0.5]) * rng.uniform(1, 3) + np.array([0, 0, 2.0]), 50e-6))
    elif item == "powerbank":
        n = max(1, int(round(wh / 11.5)))
        m = scale(cell18650(rng, big=False), n)
        if rng.random() < 0.5:  # Al-behuizing
            V = n * 30.0
            m.append((2, np.array([1.2, 1.2, 1.2]) * V, rng.uniform(150e-6, 400e-6)))
        m.append((2, np.array([0.1, 0.1, 1.0]) * 5, 10e-6))  # PCB
    elif item == "laptop_gereedschap":
        if rng.random() < 0.5:  # gereedschapsaccu: 18650/21700-array
            n = max(2, int(round(wh / 11.5)))
            m = scale(cell18650(rng), n)
        else:  # laptoppack: 3-4 grote pouches
            n = rng.integers(3, 5)
            m = scale(disc(rng.uniform(0.04, 0.05), rng.uniform(10000, 18000), 0.8), n)
        m.append((2, np.array([0.1, 0.1, 1.0]) * 10, 15e-6))
    elif item == "ebike_step":
        n = max(10, int(round(wh / 11.5)))
        m = scale(cell18650(rng), n)
        m.append((2, np.array([1, 1, 1]) * n * 25.0, rng.uniform(0.5e-3, 2e-3)))
    elif item == "blik":
        if rng.random() < 0.7:  # Al-drankblik
            m = shell(0.033, 0.115, rng.uniform(0.09e-3, 0.11e-3), _ln(rng, 2.5e7, 1.1))
            if rng.random() < 0.4:  # geplet
                m = [(k, D * rng.uniform(0.2, 0.6), t * rng.uniform(0.3, 0.7)) for k, D, t in m]
        else:  # vertind stalen conservenblik
            m = shell(rng.uniform(0.03, 0.042), rng.uniform(0.07, 0.115), 0.2e-3, 6e6, mur=_ln(rng, 200, 1.5))
    elif item == "folie":
        if rng.random() < 0.85:  # prop
            m = [(2, np.array([1, 1, 1]) * _ln(rng, 1.0, 2.0), rng.uniform(1e-6, 8e-6))]
        else:  # vlakke schaal/vel
            m = disc(rng.uniform(0.05, 0.10), 3.5e7 * rng.uniform(15e-6, 60e-6), 0.3, 0.1)
    elif item == "sleutel_klein_metaal":
        if rng.random() < 0.6:  # sleutelbos
            k = rng.integers(2, 6)
            m = [(2, np.array([0.15, 0.15, 1.0]) * 9 * 0.7 * k, rng.uniform(80e-6, 250e-6)),
                 (1, np.array([1, 1, 1]) * rng.uniform(1, 4), 50e-6)]
        else:  # schroeven, munten, kroonkurken
            m = [(1, np.array([1, 1, 1]) * rng.uniform(0.5, 5), 30e-6),
                 (2, np.array([0.3, 0.3, 1]) * rng.uniform(1, 8), rng.uniform(10e-6, 80e-6))]
    elif item == "pan_gereedschap":
        if rng.random() < 0.6:  # staal
            s = rng.uniform(300, 3000)
            m = [(1, np.array([1, 1, 1]) * s, rng.uniform(1e-3, 10e-3)),
                 (2, np.array([1, 1, 1]) * 0.3 * s, rng.uniform(0.5e-3, 5e-3))]
        else:  # Al-pan
            m = disc(rng.uniform(0.09, 0.14), 2.5e7 * rng.uniform(2e-3, 4e-3), 1.0, 0.2)
    elif item == "elektronica_zonder_accu":
        m = disc(rng.uniform(0.02, 0.06), 5.8e7 * 35e-6 * rng.uniform(1, 4), 0.3, 0.1)
        m.append((1, np.array([1, 1, 1]) * rng.uniform(0.5, 20), rng.uniform(20e-6, 200e-6)))
    else:
        raise KeyError(item)
    # +-15% spreiding op amplitudes en tijdconstanten (productievariatie, vervorming) [A]
    return [(k, D * _ln(rng, 1, 1.15), t * _ln(rng, 1, 1.15)) for k, D, t in m]


def pad(modes):
    kind = np.zeros(MAXM, int); D = np.zeros((MAXM, 3)); tau = np.ones(MAXM) * 1e-6
    for i, (k, d, t) in enumerate(modes[:MAXM]):
        kind[i], D[i], tau[i] = k, d, t
    return kind, D, tau
