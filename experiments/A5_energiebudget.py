"""A5 energiebudget-sjabloon. Vul per concept SENSOREN/COMMS in (Ronde 3).
Alle energie in mWh; vermogens in mW; tijd in s. Waarden zijn basis-aannames [A] uit research/A5_hardware.md."""
V = 3.6  # V systeemspanning (Li-SOCl2)

# per inworp: (vermogen mW, meettijd s)  -> laag/basis/hoog meettijd
SENSOR = {
    "PI-metaaldetector":        (60, (2, 5, 10)),
    "Wervelstroom LDC (VLF)":   (6, (2, 5, 10)),
    "Thermopile-array 32x24":   (80, (1, 3, 5)),
    "Thermopile 8x8 / enkel":   (15, (1, 3, 5)),
    "mmWave 60 GHz":            (300, (0.5, 1, 2)),
    "Camera + edge-AI (S3)":    (400, (1, 2, 4)),
    "MOX-gas puls (BME688)":    (40, (1, 2, 5)),
    "Rontgen (ter vergelijking)": (30000, (0.5, 1, 2)),
}
MCU_ACTIVE_MW = 15        # MCU actief tijdens meting
SLEEP_UA = (5, 15, 50)    # systeemslaapstroom laag/basis/hoog
COMMS_MWH = {"LoRaWAN SF7": 0.005, "LoRaWAN SF12": 0.06, "LTE-M PSM": 1.0, "NB-IoT (slechte dekking)": 3.0}
INWORPEN = (30, 80, 150)

def per_inworp(p_mw, t_s):
    return (p_mw + MCU_ACTIVE_MW) * t_s / 3600

def dag(sensor, comms, n, berichten=4, sleep_ua=15, alarm=0):
    p, (tl, tb, th) = SENSOR[sensor]
    e = n * per_inworp(p, tb) + sleep_ua * 1e-3 * V * 24 + (berichten + alarm) * COMMS_MWH[comms]
    return e

if __name__ == "__main__":
    print("Per inworp (mWh) laag/basis/hoog:")
    for k, (p, ts) in SENSOR.items():
        print(f"  {k:28s}", " / ".join(f"{per_inworp(p,t):.3f}" for t in ts))
    print("Slaap mWh/dag:", [round(u*1e-3*V*24, 2) for u in SLEEP_UA])
    print("\nmWh/dag (basis meettijd, 15 uA, 4 berichten/dag LTE-M):")
    for k in SENSOR:
        print(f"  {k:28s}", " / ".join(f"{dag(k,'LTE-M PSM',n):.1f}" for n in INWORPEN))
    print("\nmWh/dag bij 'ieder inworp direct versturen' (LTE-M), PI:",
          [round(dag('PI-metaaldetector','LTE-M PSM',n,berichten=n),1) for n in INWORPEN])
    print("mWh/dag idem LoRaWAN SF12, PI:",
          [round(dag('PI-metaaldetector','LoRaWAN SF12',n,berichten=n),1) for n in INWORPEN])
    usable = 3.6*17*0.7  # LS33600, 70% bruikbaar
    for n in INWORPEN:
        d = dag('PI-metaaldetector','LTE-M PSM',n)
        print(f"PI+LTE-M {n}/dag: {d:.1f} mWh/dag -> {usable*1000/d/365:.1f} jaar op 1x LS33600 ({usable:.0f} Wh bruikbaar)")
