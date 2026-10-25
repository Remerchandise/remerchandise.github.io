#!/usr/bin/env python3
"""A6 – Firmware-skelet (MicroPython-stijl, draait ook op CPython als simulatie/zelftest).

Keten op het apparaat (K2/K5, OEM-module op de pas-zuil):
  pas-event / klep dicht -> meting tijdens stilstand trommel -> klasse {geen, cel, pakket}
  -> Bayes-containerscore (som E[Wh-eq | klasse], tabel via downlink instelbaar)
  -> niveau groen/oranje/rood (A1-R3-drempels) -> LoRaWAN-uplink (13 B) of MQTT-JSON.
Lediging wordt herkend via downlink "emptied" of een vulgraadsprong; dan reset.

Draaien:  python3 experiments/r3_signaal/firmware_skeleton.py      (zelftest + voorbeeldpayloads)

PAYLOAD v1 (13 bytes, big-endian; past in LoRaWAN EU868 SF12 = 51 B, ruim onder 11–20 B-eis):
  byte 0     : versie (hoog 4 bit, =1) | berichttype (laag 4 bit) 1=periodiek 2=alarm 3=event 4=geleegd 5=storing
  byte 1     : niveau (bit7-6: 0 groen,1 oranje,2 rood,3 zwart/event) | flags bit5..0:
               b5 sensorfout, b4 sabotage/klep geforceerd, b3 accu laag, b2 temp-event, b1 gas-event, b0 placeholder-model
  byte 2-3   : seq (u16, wrap)
  byte 4-5   : inworpen sinds lediging (u16)
  byte 6-7   : containerscore Wh-eq x10 (u16, 0..6553.5 Wh-eq, verzadigend)
  byte 8     : aantal 'cel'-uitkomsten sinds lediging (u8, verzadigend)
  byte 9     : aantal 'pakket'-uitkomsten sinds lediging (u8, verzadigend)
  byte 10    : hoogste inworp-score Wh-eq (u8, verzadigend op 255)
  byte 11    : temperatuur deksel/zuil degC (i8)
  byte 12    : accuspanning (mV-2000)/10 (u8 -> 2000..4550 mV)
DOWNLINK (fport 10): 0x01 = geleegd (reset);  0x02 + 3x u16 (E[Wh-eq|geen,cel,pakket] x100) = nieuwe posteriortabel;
                     0x03 + 4x u16 drempels (throw_or, throw_rood, cont_or, cont_rood) Wh-eq.
"""
try:  # MicroPython
    import ustruct as struct
    import utime as time
except ImportError:  # CPython
    import struct
    import time

VERSION = 1
MT_PERIODIC, MT_ALARM, MT_EVENT, MT_EMPTIED, MT_FAULT = 1, 2, 3, 4, 5
GREEN, ORANGE, RED, BLACK = 0, 1, 2, 3
GEEN, CEL, PAKKET = 0, 1, 2
F_SENSOR_FAULT, F_TAMPER, F_LOW_BATT, F_TEMP_EVT, F_GAS_EVT, F_PLACEHOLDER = 1 << 5, 1 << 4, 1 << 3, 1 << 2, 1 << 1, 1 << 0


# ---- hardware-abstractie (stubs; op doel-MCU vervangen door ADC/PI-driver) ------------
class PISensor:
    """Pulse-induction, 2 lussen + ferro-kanaal (K2). Op CPython: gesimuleerd met vaste reeks."""
    def __init__(self, demo=None):
        self.demo = list(demo or [])

    def measure(self, dwell_ms=3000):
        # MCU: n pulsen tijdens stilstand, gemiddelde vervalcurve (16 vensters) + ferro-kanaal.
        # Return feature-vector; hier: (klasse_hint,) voor simulatie.
        return self.demo.pop(0) if self.demo else (GEEN,)


def classify(features, coef=None):
    """Klasse uit features. Op het apparaat: logistische regressie/kNN met coefficienten uit
    sensor_model (A2). Hier: simulatie-hint doorgeven."""
    return features[0]


# ---- containerlogica ------------------------------------------------------------------
class Container:
    def __init__(self, post=(0.05, 3.0, 30.0), thr=(50, 75, 75, 150), placeholder=True):
        self.post = list(post)            # E[Wh-eq | geen, cel, pakket] – gekalibreerd in mc.py
        self.thr = list(thr)              # throw_or, throw_rood, cont_or, cont_rood (A1-R3)
        self.placeholder = placeholder
        self.reset()

    def reset(self):
        self.n_throw = 0
        self.score = 0.0
        self.n_cel = 0
        self.n_pak = 0
        self.max_throw = 0.0

    def add(self, cls):
        e = self.post[cls]
        self.n_throw += 1
        self.score += e
        self.max_throw = max(self.max_throw, e)
        if cls == CEL:
            self.n_cel += 1
        elif cls == PAKKET:
            self.n_pak += 1

    def level(self, event=False):
        if event:
            return BLACK
        t_or, t_rd, c_or, c_rd = self.thr
        if self.score >= c_rd or self.max_throw >= t_rd:
            return RED
        if self.score >= c_or or self.max_throw >= t_or or self.n_pak > 0:
            return ORANGE
        return GREEN


def _sat(v, hi):
    return 0 if v < 0 else (hi if v > hi else int(v))


def encode(c, mtype, seq, temp_c=12, batt_mv=3600, flags=0, event=False):
    lvl = c.level(event)
    if c.placeholder:
        flags |= F_PLACEHOLDER
    b0 = (VERSION << 4) | (mtype & 0x0F)
    b1 = (lvl << 6) | (flags & 0x3F)
    return struct.pack(">BBHHHBBBbB", b0, b1, seq & 0xFFFF, _sat(c.n_throw, 65535),
                       _sat(round(c.score * 10), 65535), _sat(c.n_cel, 255), _sat(c.n_pak, 255),
                       _sat(round(c.max_throw), 255), max(-128, min(127, int(temp_c))),
                       _sat((batt_mv - 2000) // 10, 255))


def decode(b):
    """Referentiedecoder (zelfde logica als ttn_decoder.js)."""
    v = struct.unpack(">BBHHHBBBbB", bytes(b))
    names = ["groen", "oranje", "rood", "zwart"]
    return {"version": v[0] >> 4, "type": v[0] & 0x0F, "level": names[v[1] >> 6],
            "flags": {"sensor_fault": bool(v[1] & F_SENSOR_FAULT), "tamper": bool(v[1] & F_TAMPER),
                      "low_batt": bool(v[1] & F_LOW_BATT), "temp_event": bool(v[1] & F_TEMP_EVT),
                      "gas_event": bool(v[1] & F_GAS_EVT), "placeholder_model": bool(v[1] & F_PLACEHOLDER)},
            "seq": v[2], "throws": v[3], "score_wheq": v[4] / 10, "n_cel": v[5], "n_pakket": v[6],
            "max_throw_wheq": v[7], "temp_c": v[8], "batt_mv": 2000 + 10 * v[9]}


def to_mqtt_json(c, device_id, seq, temp_c, batt_mv, event=False):
    """Alternatief voor NB-IoT/LTE-M of de modem van de pas-zuil (topic: bwr/<gemeente>/<device>/up)."""
    import json
    names = ["groen", "oranje", "rood", "zwart"]
    return json.dumps({"device": device_id, "seq": seq, "level": names[c.level(event)], "throws": c.n_throw,
                       "score_wheq": round(c.score, 1), "n_cel": c.n_cel, "n_pakket": c.n_pak,
                       "max_throw_wheq": round(c.max_throw, 1), "temp_c": temp_c, "batt_mv": batt_mv,
                       "model": "placeholder" if c.placeholder else "v1"}, separators=(",", ":"))


def handle_downlink(c, data):
    if not data:
        return
    if data[0] == 0x01:
        c.reset()
    elif data[0] == 0x02 and len(data) >= 7:
        c.post = [x / 100 for x in struct.unpack(">HHH", bytes(data[1:7]))]
    elif data[0] == 0x03 and len(data) >= 9:
        c.thr = list(struct.unpack(">HHHH", bytes(data[1:9])))


# ---- hoofdlus -------------------------------------------------------------------------
def main_loop(sensor, radio_send, wait_for_throw, read_temp, read_batt, periodic_s=6 * 3600):
    """Op het apparaat: slaap tot pas-/klep-interrupt; meet; stuur alleen bij niveauwissel + periodiek."""
    c, seq, last_lvl, last_tx = Container(), 0, GREEN, time.time()
    while True:
        ev = wait_for_throw(periodic_s)          # blokkeert in deep-sleep; None = timeout
        if ev == "throw":
            c.add(classify(sensor.measure()))
        elif ev == "emptied":
            c.reset()
            radio_send(encode(c, MT_EMPTIED, seq, read_temp(), read_batt())); seq += 1
            continue
        lvl = c.level()
        if lvl > last_lvl:                        # escalatie -> direct
            radio_send(encode(c, MT_ALARM, seq, read_temp(), read_batt())); seq += 1
        elif time.time() - last_tx >= periodic_s:
            radio_send(encode(c, MT_PERIODIC, seq, read_temp(), read_batt())); seq += 1
            last_tx = time.time()
        last_lvl = lvl


def _selftest():
    c = Container()
    for cls in [GEEN] * 60 + [CEL] * 25 + [PAKKET]:
        c.add(cls)
    p = encode(c, MT_ALARM, 7, temp_c=14, batt_mv=3610)
    d = decode(p)
    assert len(p) == 13 and d["throws"] == 86 and d["n_pakket"] == 1 and d["level"] == "oranje", d
    handle_downlink(c, bytes([0x01]))
    assert c.n_throw == 0
    handle_downlink(c, bytes([0x02]) + struct.pack(">HHH", 5, 250, 4000))
    assert c.post == [0.05, 2.5, 40.0]
    print("payload hex:", p.hex(), "(", len(p), "B )")
    print("decoded    :", d)
    c2 = Container()
    for cls in [CEL] * 3:
        c2.add(cls)
    print("mqtt       :", to_mqtt_json(c2, "zuil-0042", 8, 13, 3590))
    print("zelftest OK")
    return p


if __name__ == "__main__":
    _selftest()
