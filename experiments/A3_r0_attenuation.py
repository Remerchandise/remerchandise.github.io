"""A3 Ronde 0: massieke verzwakkingscoefficienten + eerste transmissieschattingen.
Bron data: xraydb 4.5 (Elam/Chantler-tabellen; wijkt doorgaans <~5% af van NIST XCOM in 20-150 keV)."""
import numpy as np, xraydb as X

E = np.array([20, 30, 40, 59.5, 80, 100, 150, 662])*1e3  # eV
def mu_el(el): return np.array([X.mu_elam(el, e) for e in E])  # cm2/g, total incl. coherent
def mu_mix(massfrac):
    return sum(w*mu_el(el) for el, w in massfrac.items())/sum(massfrac.values())
def mf(formula):
    d = X.chemparse(formula); tot = sum(X.atomic_mass(k)*v for k,v in d.items())
    return {k: X.atomic_mass(k)*v/tot for k,v in d.items()}

mats = {
 'Cu': {'Cu':1}, 'Al': {'Al':1}, 'Fe (staal)': {'Fe':1}, 'Ni': {'Ni':1}, 'Zn': {'Zn':1},
 'C (grafiet)': {'C':1}, 'LiCoO2': mf('LiCoO2'), 'NMC811': mf('LiNi0.8Mn0.1Co0.1O2'),
 'LiFePO4': mf('LiFePO4'), 'MnO2': mf('MnO2'),
 'PE (C2H4)': mf('C2H4'), 'papier/cellulose': mf('C6H10O5'), 'water': mf('H2O'),
 'glas (sodalime)': {'O':0.46,'Si':0.336,'Na':0.096,'Ca':0.071,'Mg':0.024,'Al':0.006,'K':0.007},
 'Pb': {'Pb':1},
}
MU = {k: mu_mix(v) for k,v in mats.items()}
print('mu/rho [cm2/g] bij E [keV] =', (E/1e3).tolist())
for k,v in MU.items(): print(f'{k:18s}', ' '.join(f'{x:8.3f}' for x in v))

# samengestelde objecten: lijst (materiaal, massadikte g/cm2) langs de straal
w = lambda d: d  # notatie
jelly = {'NMC811':0.45,'C (grafiet)':0.20,'Cu':0.15,'Al':0.07,'PE (C2H4)':0.13}   # [A] massafracties jelly roll
mu_jelly = sum(f*MU[m] for m,f in jelly.items())
alk = {'MnO2':0.40,'Zn':0.25,'water':0.20,'C (grafiet)':0.05,'Fe (staal)':0.10}   # [A] inhoud AA alkaline
mu_alk = sum(f*MU[m] for m,f in alk.items())
bag = 0.5*MU['water']+0.3*MU['papier/cellulose']+0.2*MU['PE (C2H4)']             # [A] organische zakmatrix
objs = {
 'zak 40 cm @0,15 g/cm3 (6 g/cm2)':  bag*6.0,
 '18650 door hart (staal 0,39 + jelly 4,5)': MU['Fe (staal)']*0.39+mu_jelly*4.5,
 'pouch telefoon plat (1,2 g/cm2 jelly)': mu_jelly*1.2+MU['Al']*0.03,
 'AA alkaline door hart (4,1 g/cm2)': MU['Fe (staal)']*0.39+mu_alk*3.7,
 'Al-blikje 2 wanden (0,054 g/cm2)': MU['Al']*0.054,
 'staal conservenblik 2 wanden (0,31)': MU['Fe (staal)']*0.31,
 'Al-folie prop 10 lagen (0,04)': MU['Al']*0.04,
 'sleutel messing 2 mm (1,7 g/cm2 Cu)': MU['Cu']*1.7,
 'glazen fles 2 wanden 3 mm (1,5)': MU['glas (sodalime)']*1.5,
 'M8 bout staal (0,8 cm -> 6,3)': MU['Fe (staal)']*6.3,
}
print('\nln-verzwakking mu*t  (transmissie = exp(-mu*t))')
for k,v in objs.items(): print(f'{k:42s}', ' '.join(f'{x:8.2f}' for x in v))
print('\nDual-energy ratio R = mu*t(30keV)/mu*t(80keV) (proxy Zeff; hoger = hogere Z)')
for k,v in objs.items(): print(f'{k:42s} R30/80={v[1]/v[4]:6.2f}  R40/100={v[2]/v[5]:6.2f}')
print('\nAfscherming: transmissie door staal/lood bij 30 keV, 60 keV')
for t in [1,2,3]: print(f'staal {t} mm: 30keV {np.exp(-MU["Fe (staal)"][1]*7.87*t/10):.1e}  59.5keV {np.exp(-MU["Fe (staal)"][3]*7.87*t/10):.1e}')
for t in [0.5,1,2]: print(f'lood {t} mm: 30keV {np.exp(-MU["Pb"][1]*11.35*t/10):.1e}  59.5keV {np.exp(-MU["Pb"][3]*11.35*t/10):.1e}  100keV {np.exp(-MU["Pb"][5]*11.35*t/10):.1e}')
