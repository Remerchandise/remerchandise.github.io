"""T3 – Dosis en afscherming: H*(10)-tempo op 0,1 m van bereikbare buitenzijde vs staaldikte; strooistraling naar de klep;
interlock-falen. Norm: Bbs art. 3.18 lid 1 b: <= 1 uSv/h op 0,1 m. Output: fig_dosis.png, t3_resultaten.txt"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import rontgen_model as R
ST = np.linspace(0, 4, 81)  # mm staal
RHO_FE = 7.87
CASES = [(30, 1.0, 'C0'), (30, 4.0, 'C1'), (50, 4.0, 'C2'), (80, 4.0, 'C3')]
R_PRIM = 0.75   # [A] bron -> 0,1 m buiten zuilwand achter detector
R_SCAT = 0.40   # [A] zak (strooibron) -> 0,1 m buiten klep/trommelachterwand
OMEGA = 0.44    # sr, bundel gecollimeerd op detector 0,4x0,4 m op 0,6 m
BAG_SC = 5.0    # g/cm2 zak voor strooiing [A]
def scat_frac(E):
    # water: incoherent ~0,18 cm2/g (20-60 keV), coherent ~0,068*(20/E)^2 (XCOM-orde) -> albedo; 0,5 zelfverzwakking [A]
    s = 0.18 + 0.068 * (20 / E) ** 2
    return (1 - np.exp(-R.mu_rho('bag', E) * BAG_SC)) * np.clip(s / R.mu_rho('bag', E), 0, 1) * 0.5
out = []
fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
for kv, P, c in CASES:
    E, N = R.spectrum(kv, P)
    # primair, lege trommel (worst case), geen verzwakking door detector [A conservatief]
    hp = [R.h10_rate_uSv_h(E, N * np.exp(-R.mu_rho('Fe', E) * RHO_FE * t / 10), R_PRIM) for t in ST]
    # strooi: N_scat totaal isotroop
    Ns = np.sum(N) * 0 + N * OMEGA * scat_frac(E) / (4 * np.pi)   # fotonen/s/sr equivalent
    hs = [R.h10_rate_uSv_h(E, Ns * np.exp(-R.mu_rho('RVS304', E) * 7.9 * t / 10), R_SCAT) for t in ST]
    ax[0].semilogy(ST, hp, color=c, label=f'{kv} kV {P:g} W')
    ax[1].semilogy(ST, hs, color=c, label=f'{kv} kV {P:g} W')
    def need(h):
        i = np.where(np.array(h) <= 1.0)[0]
        return f'{ST[i[0]]:.2f} mm' if len(i) else '>4 mm'
    out.append(f'{kv} kV {P:g} W: H*(10) primair onafgeschermd op {R_PRIM} m = {hp[0]:.3g} uSv/h; staal nodig voor 1 uSv/h: {need(hp)};'
               f' 3 mm staal -> {np.interp(3, ST, hp):.2g} uSv/h')
    out.append(f'           strooi naar klep onafgeschermd op {R_SCAT} m = {hs[0]:.3g} uSv/h; RVS nodig: {need(hs)}; 2 mm RVS -> {np.interp(2, ST, hs):.2g} uSv/h;'
               f' interlock-falen 10 s open klep -> {hs[0]*10/3600:.3g} uSv')
for a, t in zip(ax, ('Primaire bundel (lege trommel) door stalen zuilwand, 0,75 m', 'Strooistraling uit zak naar klepzijde door RVS, 0,40 m')):
    a.axhline(1.0, color='k', lw=1); a.text(0.05, 1.3, 'Bbs 3.18: 1 µSv/h op 0,1 m', fontsize=8)
    a.axvline(3.0 if 'zuil' in t else 2.0, color='grey', ls=':')
    a.set_xlabel('staaldikte [mm] (Fe resp. RVS 304)'); a.set_ylabel('H*(10)-tempo [µSv/h]'); a.set_title(t, fontsize=9)
    a.set_ylim(1e-8, 1e6); a.legend(fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(HERE, 'fig_dosis.png'), dpi=130)
# buisbehuizing lekstraling
E, N = R.spectrum(30, 4.0)
out.append(f'Buisbehuizing 1 mm Pb, 30 kV 4 W, 0,1 m: {R.h10_rate_uSv_h(E, N*np.exp(-R.mu_rho("Pb", E)*11.35*0.1), 0.1):.2g} uSv/h')
out.append(f'Dosis op zakinhoud per scan (5 s, 4 W, 0,3 m): {R.kerma_rate_uGy_h(E, N, 0.3)*5/3600:.0f} uGy luchtkerma')
open(os.path.join(HERE, 't3_resultaten.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
