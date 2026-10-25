"""A3 Ronde 0: orde-grootte fotonbudget. Kramers-spectrum W-anode, isotroop, zelfabsorptie verwaarloosd
(=> overschatting ~2x **[A]**). Detectorpixel 1 mm2 op 0,6 m van focus, zak 6 g/cm2 organisch."""
import numpy as np, xraydb as X
def mu(el_frac, E): return sum(w*X.mu_elam(el,E) for el,w in el_frac.items())
bag = {'H':0.09,'C':0.40,'O':0.51}           # [A] organisch/water-mix
def run(kV, P_W, filt_mmAl=0.5, R=0.6, pix_mm2=1.0, t_s=1.0, bag_g=6.0):
    E = np.linspace(5e3, kV*1e3, 400); dE = E[1]-E[0]
    eta = 1.1e-9*74*kV*1e3; Px = eta*P_W
    shape = (kV*1e3-E)/E                      # dN/dE (relatief)
    norm = Px/np.sum(shape*E*1.602e-19*dE)    # fotonen/s/eV
    N = shape*norm*dE                         # fotonen/s per bin in 4pi
    Tf = np.exp(-np.array([X.mu_elam('Al',e) for e in E])*2.7*filt_mmAl/10)
    Tb = np.exp(-np.array([mu(bag,e) for e in E])*bag_g)
    frac = (pix_mm2*1e-6)/(4*np.pi*R**2)
    n0 = np.sum(N*Tf)*frac*t_s; nb = np.sum(N*Tf*Tb)*frac*t_s
    Ebar = np.sum(N*Tf*Tb*E)/np.sum(N*Tf*Tb)/1e3
    return Px, n0, nb, Ebar
for kV,P in [(30,1),(30,4),(30,10),(50,4),(80,10)]:
    Px,n0,nb,Eb = run(kV,P)
    print(f'{kV} kV {P:>3} W: Px={Px*1e3:6.1f} mW  fotonen/mm2/s zonder zak={n0:9.2e}  achter zak={nb:9.2e}  Egem achter zak={Eb:4.1f} keV')
# Am-241 vrijstellingsactiviteit 1e4 Bq, 59,5 keV yield 0,359
A=1e4; n=A*0.359/(4*np.pi*0.6**2)*1e-6
print(f'Am-241 10 kBq: {n:.2e} fotonen/mm2/s op 0,6 m  -> 100 fotonen/pixel vergt {100/n/3600:.0f} uur')
A=3.7e9; n=A*0.359/(4*np.pi*0.6**2)*1e-6
print(f'Am-241 3,7 GBq (100 mCi, vergunningplichtig): {n:.2e} fotonen/mm2/s')
