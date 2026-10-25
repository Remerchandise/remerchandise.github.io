"""A3 Ronde 3 – gedeeld röntgenmodel (K3: schaduwdoos <= 30 kV).

Bevat: materialen, buisspectrum, objecten in de zak, detectormodellen, kerma/H*(10).
Alle aannames gemarkeerd met [A]. Attenuatiedata: xcom_data.py (XCOM-equivalent, zie aldaar).
"""
import numpy as np
from xcom_data import mu_rho_el

AW = {'H': 1.008, 'Li': 6.94, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'Na': 22.99, 'Mg': 24.305,
      'Al': 26.98, 'Si': 28.085, 'S': 32.06, 'K': 39.098, 'Ca': 40.078, 'Cr': 51.996, 'Mn': 54.938, 'Fe': 55.845,
      'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38, 'I': 126.9, 'Cs': 132.91, 'Gd': 157.25,
      'W': 183.84, 'Pb': 207.2}


def formula(d):
    """{'Li':1,'Co':1,'O':2} -> massafracties"""
    m = {k: AW[k] * v for k, v in d.items()}
    t = sum(m.values())
    return {k: v / t for k, v in m.items()}


def mix(*parts):
    """mix((massfrac_dict, gewicht), ...) -> massafracties"""
    out = {}
    tot = sum(w for _, w in parts)
    for d, w in parts:
        for k, v in d.items():
            out[k] = out.get(k, 0) + v * w / tot
    return out


MAT = {
    'Fe': {'Fe': 1.0}, 'Al': {'Al': 1.0}, 'Cu': {'Cu': 1.0}, 'Pb': {'Pb': 1.0}, 'C': {'C': 1.0},
    'RVS304': {'Fe': 0.71, 'Cr': 0.18, 'Ni': 0.09, 'Mn': 0.02},
    'water': formula({'H': 2, 'O': 1}), 'PE': formula({'C': 2, 'H': 4}),
    'cellulose': formula({'C': 6, 'H': 10, 'O': 5}),
    'NMC811': formula({'Li': 1, 'Ni': 0.8, 'Mn': 0.1, 'Co': 0.1, 'O': 2}),
    'LCO': formula({'Li': 1, 'Co': 1, 'O': 2}),
    'MnO2': formula({'Mn': 1, 'O': 2}), 'Zn': {'Zn': 1.0}, 'brass': {'Cu': 0.63, 'Zn': 0.37},
    'glass': {'O': 0.46, 'Si': 0.336, 'Na': 0.096, 'Ca': 0.071, 'Mg': 0.024, 'Al': 0.006, 'K': 0.007},
    'GOS': formula({'Gd': 2, 'O': 2, 'S': 1}), 'CsI': formula({'Cs': 1, 'I': 1}),
}
MAT['jelly'] = mix((MAT['NMC811'], 0.45), (MAT['C'], 0.20), (MAT['Cu'], 0.15), (MAT['Al'], 0.07), (MAT['PE'], 0.13))  # [A]
MAT['alk'] = mix((MAT['MnO2'], 0.40), (MAT['Zn'], 0.25), (MAT['water'], 0.20), (MAT['C'], 0.05), (MAT['Fe'], 0.10))  # [A]
MAT['bag'] = mix((MAT['water'], 0.5), (MAT['cellulose'], 0.3), (MAT['PE'], 0.2))  # [A] organische zakmatrix


def mu_rho(mat, e):
    return sum(w * mu_rho_el(el, e) for el, w in MAT[mat].items())


# Objecten: lijst (materiaal, massadikte g/cm2) langs centrale straal; projectie-oppervlak cm2  [A]
OBJECTS = {
    '18650 (hart)':          dict(path=[('Fe', 0.39), ('jelly', 4.5)], area=11.7),
    'telefoon-pouch (plat)': dict(path=[('jelly', 1.2), ('Al', 0.03), ('glass', 0.5)], area=100.0),
    'vape (Al-huls+13350)':  dict(path=[('Al', 0.54), ('jelly', 2.5), ('Fe', 0.1)], area=12.0),
    'oortje/knoopcel':       dict(path=[('Fe', 0.2), ('jelly', 0.6)], area=3.0),
    'AA alkaline (hart)':    dict(path=[('Fe', 0.39), ('alk', 3.7)], area=7.3),
    'Al-blikje':             dict(path=[('Al', 0.054)], area=80.0),
    'staalblik (wanden)':    dict(path=[('Fe', 0.31)], area=80.0),
    'Al-folieprop':          dict(path=[('Al', 0.04)], area=30.0),
    'sleutel messing':       dict(path=[('brass', 1.7)], area=4.0),
    'glazen fles':           dict(path=[('glass', 1.5)], area=150.0),
}


def mut(path, e):
    return sum(mu_rho(m, e) * t for m, t in path)


# ---------------- buisspectrum ----------------
AIR_MUEN = (np.array([10, 15, 20, 30, 40, 50, 60, 80, 100, 150.]),
            np.array([4.742, 1.334, 0.5389, 0.1537, 0.06833, 0.04098, 0.03041, 0.02407, 0.02325, 0.02496]))
# NIST Hubbell & Seltzer (NISTIR 5632, 1995/2004): mu_en/rho droge lucht [cm2/g]
H10_PER_KA = (np.array([10, 15, 20, 30, 40, 50, 60, 80, 100, 150.]),
              np.array([0.008, 0.26, 0.61, 1.10, 1.47, 1.67, 1.74, 1.72, 1.65, 1.49]))
# ICRP 74 (1996), tabel A.21: H*(10)/K_a [Sv/Gy]


def loginterp(tab, e):
    return np.exp(np.interp(np.log(e), np.log(tab[0]), np.log(tab[1])))


WINDOWS = (('Al', 0.135), ('PE', 0.57))  # [A] 0,5 mm Al buisfilter + 2 PE-vensters 3 mm in trommelwanden (R2b)


def spectrum(kv, p_w, filt=WINDOWS, self_abs=0.5, n=300):
    """Kramers-spectrum W-anode. Retour: E [keV], N [fotonen/s/sr per bin].
    eta = 1.1e-9*Z*V (Kramers/Compton). Isotroop in 4pi, factor self_abs voor anode-zelfabsorptie [A].
    filt: lijst (materiaal, g/cm2); standaard WINDOWS."""
    E = np.linspace(8, kv, n)[:-1] + (kv - 8) / n / 2
    dE = (kv - 8) / n
    eta = 1.1e-9 * 74 * kv * 1e3
    px = eta * p_w * self_abs
    shape = (kv - E) / E
    norm = px / np.sum(shape * E * 1.602e-16 * dE)
    N = shape * norm * dE / (4 * np.pi)
    for m, t in filt:
        N = N * np.exp(-mu_rho(m, E) * t)
    return E, N


def kerma_rate_uGy_h(E, N_sr, r_m):
    """luchtkerma-tempo [uGy/h] op afstand r uit spectrum (fotonen/s/sr)."""
    fl = N_sr / (r_m * 100) ** 2  # /cm2/s
    k = np.sum(fl * E * 1.602e-16 * loginterp(AIR_MUEN, E)) * 1e3  # J/kg/s = Gy/s ; *1e3 g->kg
    return k * 1e6 * 3600


def h10_rate_uSv_h(E, N_sr, r_m):
    fl = N_sr / (r_m * 100) ** 2
    k = fl * E * 1.602e-16 * loginterp(AIR_MUEN, E) * 1e3
    return np.sum(k * loginterp(H10_PER_KA, E)) * 1e6 * 3600


# ---------------- detectoren ----------------
SID_M = 0.6      # [A] bron-detector afstand in zuil
PIX_MM = 2.0     # [A] effectieve pixel in objectvlak (na binning) voor vormherkenning
SPR_PER_G = {'cone': 0.10, 'fan': 0.03}  # [A] strooi/primair per g/cm2 zak, zonder rooster


def fluence_at_det(E, N_sr):
    return N_sr / (SID_M * 1000) ** 2  # fotonen/s/mm2 per bin


DETECTORS = {
    # g: elektronen (of kwanta) per geabsorbeerd röntgenfoton; rn: leesruis per sensorpixel; px_um sensorpixel
    'GOS + RPi HQ-camera (1/2.3")': dict(kind='lens', screen=('GOS', 0.070), ly_per_kev=60 * 0.5,
                                         N=1.2, field_mm=400, sensor_mm=6.3, px_um=1.55, qe=0.6, rn=3.0, dark=2.0,
                                         geom='cone', cost=(150, 400, 900)),
    'GOS + 4/3"-camera f/0,95':     dict(kind='lens', screen=('GOS', 0.070), ly_per_kev=60 * 0.5,
                                         N=0.95, field_mm=400, sensor_mm=13.0, px_um=4.63, qe=0.7, rn=1.6, dark=0.5,
                                         geom='cone', cost=(600, 1200, 2000)),
    'CsI-lijnarray 1,6 mm (scan)':  dict(kind='lda', screen=('CsI', 0.5 * 4.51 * 0.1), pitch_mm=1.6, scan_mm=400,
                                         geom='fan', cost=(300, 900, 2000)),
    'CMOS-flatpanel 43x43':         dict(kind='fp', screen=('CsI', 0.06), geom='cone', cost=(4000, 9000, 20000)),
}


def lens_gain(d, e_kev):
    m = d['field_mm'] / d['sensor_mm']
    eta = 0.8 / (4 * d['N'] ** 2 * (1 + m) ** 2)
    return e_kev * d['ly_per_kev'] * eta * d['qe'], m


def pixel_quanta(det, E, N_sr, bag_g, obj_path=None, t=1.0, pix_mm=PIX_MM):
    """Retour (mean_bg, var_bg, mean_obj, var_obj) in detectorsignaal-eenheden (elektronen of geabsorbeerde fotonen)."""
    d = DETECTORS[det]
    fl = fluence_at_det(E, N_sr)
    Tbag = np.exp(-mu_rho('bag', E) * bag_g)
    Tobj = np.exp(-mut(obj_path, E)) if obj_path else np.ones_like(E)
    sm, st = d['screen']
    absf = 1 - np.exp(-mu_rho(sm, E) * st)
    area = pix_mm ** 2
    tt = t * (d['pitch_mm'] / d['scan_mm']) if d['kind'] == 'lda' else t
    spr = SPR_PER_G[d['geom']] * bag_g
    prim_bg = fl * Tbag * absf * area * tt
    scat = np.sum(prim_bg) * spr  # strooistraling, ~ gelijk spectrum [A]
    out = []
    for T in (np.ones_like(E), Tobj):
        prim = prim_bg * T
        if d['kind'] == 'lens':
            g, m = lens_gain(d, E)
            gs = np.sum(prim_bg * g) / max(np.sum(prim_bg), 1e-30)
            mean = np.sum(prim * g) + scat * gs
            nq = np.sum(prim) + scat
            n_spx = (pix_mm * 1000 / m / d['px_um']) ** 2
            var = mean * (1 + gs) + n_spx * (d['rn'] ** 2 + d['dark'] * t)
        else:
            mean = np.sum(prim) + scat
            var = mean * 1.2  # [A] Swank/elektronische ruis +20 %
        out += [mean, var]
    return out


def snr_pixel(det, E, N_sr, bag_g, obj_path, t):
    mb, vb, mo, vo = pixel_quanta(det, E, N_sr, bag_g, obj_path, t)
    return (mb - mo) / np.sqrt(vb + vo)
