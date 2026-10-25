"""A7 unit-economics model: kostprijs per container per maand vs vermeden schade.
Alle bedragen EUR 2026 excl. btw. Aannames [A] zie research/A7_business.md.
Scenario's: laag / basis / hoog (kostenzijde: laag = goedkoop)."""
import numpy as np

LIFE_Y = 6          # [A] afschrijvingstermijn device (jaar)
SC = ["laag", "basis", "hoog"]

# kostenposten per container, afhankelijk van schaal (100 / 1000 / 10000)
def costs(n, s):
    i = SC.index(s)
    scale = {100: 1.0, 1000: 0.8, 10000: 0.65}[n]          # [A] volumekorting hardware
    hw = [80, 150, 300][i] * scale                            # device incl. behuizing, accu
    inst = [40, 80, 150][i] * (1.0 if n == 100 else 0.85)     # retrofit in zuil
    conn = [0.4, 0.9, 1.5][i]                                 # LTE-M/NB-IoT/LoRa p/m
    cloud = [0.15, 0.3, 0.6][i] * {100: 3, 1000: 1.5, 10000: 1}[n]
    # onderhoud: uitval 5/8/12 % per jaar, interventie 60/100/150 EUR; accuwissel 1x in levensduur
    maint_y = [0.05, 0.08, 0.12][i] * [60, 100, 150][i] + [15, 30, 50][i] / LIFE_Y
    # support/dashboard/accountmanagement: vaste kosten verdeeld
    support_fixed_y = {100: 15000, 1000: 60000, 10000: 250000}[n] * [0.7, 1, 1.4][i]
    # CAC: aanbesteding/pilot per klant; gemiddeld klantformaat
    cust = {100: 1, 1000: 5, 10000: 30}[n]
    cac_per_cust = [15000, 30000, 50000][i]
    cac_y = cust * cac_per_cust / LIFE_Y
    pm = {
        "hardware": hw / LIFE_Y / 12,
        "installatie": inst / LIFE_Y / 12,
        "connectiviteit": conn,
        "cloud": cloud,
        "onderhoud": maint_y / 12,
        "support": support_fixed_y / n / 12,
        "CAC": cac_y / n / 12,
    }
    pm["kostprijs"] = sum(pm.values())
    return pm

# vermeden schade per container per jaar (landelijk top-down)
def avoided(s):
    i = SC.index(s)  # hier: laag = weinig vermeden schade
    ugc = [65000, 45000, 30000][i]              # aantal ondergrondse restafvalcontainers [A]
    truck_fires = [40, 80, 150][i]              # branden in inzamelwagens per jaar
    dmg_truck = [10000, 25000, 50000][i]        # gem. schade per wagenbrand incl. stilstand [A]
    proc_dmg = [10e6, 22e6, 40e6][i]            # batterij-gerelateerde schade verwerkers p/j [A]
    share_ugc = [0.15, 0.25, 0.35][i]           # aandeel batterijrisico via UGC-route [A]
    recall = [0.3, 0.5, 0.7][i]                 # detectie (afh. van A2/A6)
    efficacy = [0.3, 0.5, 0.7][i]               # fractie gedetecteerd die echt brand voorkomt [A]
    cont_fire = ugc * [0.0002, 0.0005, 0.001][i] * [6000, 8000, 9500][i]  # containerbrand door accu
    truck = truck_fires * dmg_truck * share_ugc
    proc = proc_dmg * share_ugc
    tot = (truck + proc + cont_fire) * recall * efficacy
    return dict(truck=truck * recall * efficacy / ugc, proc=proc * recall * efficacy / ugc,
                cont=cont_fire * recall * efficacy / ugc, tot_y=tot / ugc, tot_pm=tot / ugc / 12,
                nat_tot=tot, gross=truck + proc + cont_fire)

if __name__ == "__main__":
    print("## Kostprijs per container per maand (EUR)")
    keys = ["hardware", "installatie", "connectiviteit", "cloud", "onderhoud", "support", "CAC", "kostprijs"]
    print("| post | " + " | ".join(f"{n} {s}" for n in (100, 1000, 10000) for s in ("laag", "basis", "hoog")) + " |")
    print("|---" * 10 + "|")
    for k in keys:
        print(f"| {k} | " + " | ".join(f"{costs(n, s)[k]:.2f}" for n in (100, 1000, 10000) for s in SC) + " |")
    print("\n## Prijs bij 40% brutomarge (basis)")
    for n in (100, 1000, 10000):
        c = costs(n, "basis")["kostprijs"]
        print(f"{n}: kostprijs {c:.2f} -> prijs {c/0.6:.2f} p/m, {c/0.6*12:.0f} p/j")
    print("\n## Vermeden schade per container")
    for s in SC:
        a = avoided(s)
        print(f"{s}: wagen {a['truck']:.1f}, verwerker {a['proc']:.1f}, container {a['cont']:.1f} "
              f"=> {a['tot_y']:.1f} p/j = {a['tot_pm']:.2f} p/m; landelijk bruto UGC-route {a['gross']/1e6:.1f} M, vermeden {a['nat_tot']/1e6:.2f} M")
    # gemeente van 50.000 inw met ~250 UGC [A]
    print("\n## Gemeente 250 UGC (basis)")
    a = avoided("basis"); c = costs(1000, "basis")["kostprijs"] / 0.6
    print(f"vermeden {a['tot_y']*250:.0f} p/j vs abonnement {c*12*250:.0f} p/j")
