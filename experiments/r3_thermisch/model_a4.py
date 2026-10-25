"""Gedeelde fysische modellen A4 (Ronde 3): warmte- en gastransport in een afvalcontainer.

Alle parameters met [A] zijn aannames; bandbreedtes laag/basis/hoog.
SI-eenheden. Gebruikt door warmte_gas.py, valsalarm_mc.py.
"""
import numpy as np
from scipy.special import erfc

# --- Afvalmatrix [A] (research/A4_thermisch_gas.md §2)
RHO_WASTE = 150.0        # kg/m3 losse zakken
CP_WASTE = 1500.0        # J/(kg K)
ALPHA = {"laag": 1.0e-7, "basis": 1.5e-7, "hoog": 3.0e-7}   # m2/s thermische diffusiviteit
D_GAS_EFF = {"laag": 3e-6, "basis": 5e-6, "hoog": 1e-5}      # m2/s effectieve diffusie in poreus afval
PERM = {"laag": 1e-8, "basis": 1e-7, "hoog": 1e-6}           # m2 permeabiliteit losse zakken [A]
MU_GAS = 2.2e-5          # Pa s (rookgas ~100 C)
RHO_AIR = 1.20           # kg/m3
G = 9.81

# --- Container [A]
AREA = 2.5               # m2 grondvlak 5 m3 container (~2 m hoog)
RISE_M_PER_DAY = 0.28    # m/dag stijging afvalniveau (5 m3/week)
HEADSPACE_M3 = {"laag": 3.5, "basis": 2.0, "hoog": 0.5}      # 'laag' risico = veel verdunning
ACH = {"laag": 5.0, "basis": 2.0, "hoog": 0.5}               # luchtwisselingen per uur


def k_waste(alpha):
    """Warmtegeleiding W/(m K) uit diffusiviteit."""
    return alpha * RHO_WASTE * CP_WASTE


def dT_pulse(Q_J, r, t, alpha):
    """Temperatuurstijging op afstand r (m), tijd t (s) na momentane warmtepuls Q (J) in oneindig medium.
    Factor 2: adiabatisch spiegelvlak (afvaloppervlak isoleert naar lucht)."""
    t = np.maximum(t, 1e-9)
    return 2 * Q_J / (RHO_WASTE * CP_WASTE * (4 * np.pi * alpha * t) ** 1.5) * np.exp(-r ** 2 / (4 * alpha * t))


def dT_continuous(P_W, r, t, alpha):
    """Temperatuurstijging door continue bron P (W), puntbron, met spiegelfactor 2."""
    t = np.maximum(t, 1e-9)
    k = k_waste(alpha)
    return 2 * P_W / (4 * np.pi * k * r) * erfc(r / (2 * np.sqrt(alpha * t)))


def t_diffusion(d, D):
    """Karakteristieke diffusietijd (s) over afstand d (m): t = d^2 / (2 D) (1D, 1/e-front)."""
    return d ** 2 / (2 * D)


def darcy_velocity(perm, dT_gas=80.0, T_amb=293.0):
    """Opwaartse Darcy-snelheid (m/s) van warm rookgas door poreus afval."""
    drho = RHO_AIR * (1 - T_amb / (T_amb + dT_gas))
    return perm * drho * G / MU_GAS


def headspace_conc_ppm(G_Lps, V_m3, ach, t_s):
    """Concentratie (ppm) in goed gemengde kopruimte bij constante bron G (L/s) vanaf t=0."""
    n = ach / 3600.0
    Css = G_Lps / 1000.0 / (n * V_m3) * 1e6
    return Css * (1 - np.exp(-n * np.maximum(t_s, 0)))


def sensor_first_order(signal, dt, t90):
    """Eerste-orde sensorrespons (t90 -> tau = t90/2.303)."""
    tau = t90 / 2.303
    out = np.empty_like(signal)
    a = dt / (tau + dt)
    y = signal[..., 0] * 0
    for i in range(signal.shape[-1]):
        y = y + a * (signal[..., i] - y)
        out[..., i] = y
    return out
