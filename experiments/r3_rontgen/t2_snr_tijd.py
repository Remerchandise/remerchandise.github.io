"""T2 – Fotonstatistiek bij 30 kV, laag vermogen, integratietijd 0,1–30 s (toets uitgangspunt 1: wat levert stilstand op?).
Output: fig_snr_vs_tijd.png, t2_resultaten.txt (t_min voor pixel-SNR >= 5 per detector/zak/vermogen)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import rontgen_model as R
T = np.logspace(-1, np.log10(30), 40)
BAGS = (2, 5, 10, 13)       # laag / basis / hoog / extreem (natte GFT) [A]
OBJ = {'18650': R.OBJECTS['18650 (hart)']['path'], 'oortje/knoopcel (dun)': R.OBJECTS['oortje/knoopcel']['path']}
SNR_REQ = 5.0               # [A] Rose-criterium per 2x2 mm pixel voor vormsegmentatie
out = ['t_min [s] voor pixel-SNR >= 5 (2x2 mm), object = 18650 | oortje; ">30" = niet binnen 30 s']
fig, axs = plt.subplots(1, 4, figsize=(17, 4.6), sharey=True)
for ax, det in zip(axs, R.DETECTORS):
    out.append(f'\n{det}')
    for P, ls in ((1.0, '-'), (4.0, '--')):
        E, N = R.spectrum(30, P)
        for bg, c in zip(BAGS, ('C0', 'C1', 'C3', 'k')):
            s = np.array([R.snr_pixel(det, E, N, bg, OBJ['18650'], t) for t in T])
            s2 = np.array([R.snr_pixel(det, E, N, bg, OBJ['oortje/knoopcel (dun)'], t) for t in T])
            ax.loglog(T, s, ls, color=c, label=f'zak {bg} g/cm², {P:g} W' if True else None)
            def tmin(x):
                i = np.where(x >= SNR_REQ)[0]
                return f'{T[i[0]]:5.2f}' if len(i) else '  >30'
            out.append(f'  {P:g} W, zak {bg:>2} g/cm2: t_min 18650 = {tmin(s)} s | oortje = {tmin(s2)} s')
    ax.axhline(SNR_REQ, color='grey', lw=0.8); ax.axvspan(1, 10, color='green', alpha=0.07)
    ax.text(1.1, 0.012, 'stilstand 1–10 s', fontsize=7)
    ax.set_title(det, fontsize=9); ax.set_xlabel('integratietijd [s]'); ax.set_ylim(1e-2, 1e3)
axs[0].set_ylabel('pixel-SNR (2×2 mm), 18650 vs zak'); axs[0].legend(fontsize=6, ncol=1)
fig.suptitle('30 kV W-buis, 0,5 mm Al + PE-vensters, SID 0,6 m – getrokken 1 W, gestippeld 4 W', fontsize=10)
plt.tight_layout(); plt.savefig(os.path.join(HERE, 'fig_snr_vs_tijd.png'), dpi=130)
# energie per inworp [A]: buis elektrisch = 2x röntgenbuisvermogen (HV-rendement 50 %), + elektronica 1,5 W (MCU+NPU+camera)
out.append('\nEnergie per inworp [Wh] = (2*P_buis + 1,5 W) * t / 3600')
for P in (1, 4):
    for t in (1, 5, 10, 30):
        out.append(f'  {P} W buis, {t:>2} s: {(2*P+1.5)*t/3600:.4f} Wh  -> 80 inworpen/dag: {(2*P+1.5)*t/3600*80:.2f} Wh/dag')
open(os.path.join(HERE, 't2_resultaten.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
