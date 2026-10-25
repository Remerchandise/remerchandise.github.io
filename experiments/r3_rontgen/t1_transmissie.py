"""T1 – Beer-Lambert: transmissie/contrast van objecten in zak (2–13 g/cm2) + dual-energy. Output: fig_transmissie.png, fig_dualenergy.png, t1_resultaten.txt"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import rontgen_model as R
rng = np.random.default_rng(3)
out = []
E = np.linspace(10, 100, 400)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
for name, o in R.OBJECTS.items():
    ax[0].semilogy(E, np.exp(-R.mut(o['path'], E)), label=name)
for bg in (2, 5, 13):
    ax[0].semilogy(E, np.exp(-R.mu_rho('bag', E) * bg), 'k--', lw=1)
    ax[0].text(100, float(np.exp(-R.mu_rho('bag', 100) * bg)[0]), f' zak {bg}', fontsize=7, va='center')
ax[0].set_ylim(1e-8, 1.2); ax[0].set_xlabel('fotonenergie [keV]'); ax[0].set_ylabel('transmissie')
ax[0].axvspan(10, 30, color='orange', alpha=0.08); ax[0].text(12, 2e-8, '≤30 kV vrijgesteld', fontsize=8)
ax[0].legend(fontsize=7, loc='lower right'); ax[0].set_title('Monochromatische transmissie (object alleen; stippel = zak)')

# spectraal gewogen: T_obj = sum(N Tbag Tobj)/sum(N Tbag) bij 30 kV
bags = np.linspace(2, 13, 23)
Es, Ns = R.spectrum(30, 1.0)
out.append('Spectraal gemiddelde relatieve transmissie object (t.o.v. zak), 30 kV, filter 0,5 mm Al + PE-vensters')
out.append('object'.ljust(26) + ''.join(f'{b:>9.0f}' for b in (2, 5, 10, 13)))
for name, o in R.OBJECTS.items():
    Tb = [np.sum(Ns * np.exp(-R.mu_rho('bag', Es) * b) * np.exp(-R.mut(o['path'], Es))) / np.sum(Ns * np.exp(-R.mu_rho('bag', Es) * b)) for b in bags]
    ax[1].semilogy(bags, Tb, label=name)
    out.append(name.ljust(26) + ''.join(f'{np.interp(b, bags, Tb):9.1e}' for b in (2, 5, 10, 13)))
Tzak = [np.sum(Ns * np.exp(-R.mu_rho('bag', Es) * b)) / np.sum(Ns) for b in bags]
ax[1].semilogy(bags, Tzak, 'k--', lw=2, label='zak zelf (t.o.v. leeg)')
out.append('zak t.o.v. leeg'.ljust(26) + ''.join(f'{np.interp(b, bags, Tzak):9.1e}' for b in (2, 5, 10, 13)))
ax[1].axhline(0.05, color='grey', lw=0.8); ax[1].text(2.1, 0.06, 'contrastgrens ~95 % ("opaak")', fontsize=7)
ax[1].set_xlabel('massadikte zak [g/cm²]'); ax[1].set_ylabel('relatieve transmissie'); ax[1].set_ylim(1e-6, 1.5)
ax[1].set_title('30 kV-spectrum: object achter/in zak'); ax[1].legend(fontsize=7)
plt.tight_layout(); plt.savefig(os.path.join(HERE, 'fig_transmissie.png'), dpi=130)

# ---- dual-energy: split-filter 30 kV (0 vs 0,1 mm Cu) en 80 kV (ter vergelijking, niet vrijgesteld)
def logatt(path, bag, kv, cu):
    E, N = R.spectrum(kv, 1.0, filt=R.WINDOWS + (('Cu', 0.0896 * cu),))
    Nb = N * np.exp(-R.mu_rho('bag', E) * bag)
    return -np.log(np.sum(Nb * np.exp(-R.mut(path, E))) / np.sum(Nb)), np.sum(Nb)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
out.append('\nDual-energy R = ln(1/T_laag)/ln(1/T_hoog) (zak 5 g/cm2); NaN = opaak (T<1e-4) in laag kanaal')
for k, (kv, lo, hi) in enumerate([(30, 0.0, 1.0), (80, 0.0, 3.0)]):
    for name, o in R.OBJECTS.items():
        a = logatt(o['path'], 5, kv, lo)[0]; b = logatt(o['path'], 5, kv, hi)[0]
        opaque = a > 9.2
        R_ = a / b
        out.append(f'{kv} kV  {name:26s} mu_t laag={a:6.2f} hoog={b:6.2f} R={R_:5.2f}{"  (opaak)" if opaque else ""}')
        # ruis: 1e4 fotonen per pixel achter zak in laag kanaal [A]
        n = 1e4
        al = -np.log(rng.poisson(n * np.exp(-a), 200).clip(1) / n); bl = -np.log(rng.poisson(n * np.exp(-b), 200).clip(1) / n)
        ax[k].scatter(bl, al / bl, s=4, label=name)
    ax[k].set_xscale('log'); ax[k].set_xlabel('µt hoog-energiekanaal'); ax[k].set_ylabel('R = µt_laag/µt_hoog')
    ax[k].set_title(f'{kv} kV split-filter ({lo:g}/{hi:g} mm Cu), 1e4 fotonen/pixel')
ax[0].legend(fontsize=6, loc='upper left')
plt.tight_layout(); plt.savefig(os.path.join(HERE, 'fig_dualenergy.png'), dpi=130)
open(os.path.join(HERE, 't1_resultaten.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
