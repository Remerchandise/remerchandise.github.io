// A6 – TTN / KPN Things payload formatter voor payload v1 (13 B). Zie firmware_skeleton.py.
// TTN v3: "Uplink payload formatter" -> Custom Javascript.
function decodeUplink(input) {
  var b = input.bytes;
  if (!b || b.length < 13) return { errors: ["payload te kort: " + (b ? b.length : 0) + " B"] };
  var u16 = function (i) { return (b[i] << 8) | b[i + 1]; };
  var lv = ["groen", "oranje", "rood", "zwart"];
  var types = { 1: "periodiek", 2: "alarm", 3: "event", 4: "geleegd", 5: "storing" };
  var f = b[1] & 0x3f;
  var temp = b[11] > 127 ? b[11] - 256 : b[11];
  return {
    data: {
      version: b[0] >> 4,
      type: types[b[0] & 0x0f] || "onbekend",
      level: lv[b[1] >> 6],
      flags: {
        sensor_fault: !!(f & 0x20), tamper: !!(f & 0x10), low_batt: !!(f & 0x08),
        temp_event: !!(f & 0x04), gas_event: !!(f & 0x02), placeholder_model: !!(f & 0x01)
      },
      seq: u16(2),
      throws: u16(4),
      score_wheq: u16(6) / 10,
      n_cel: b[8],
      n_pakket: b[9],
      max_throw_wheq: b[10],
      temp_c: temp,
      batt_mv: 2000 + 10 * b[12]
    },
    warnings: [],
    errors: []
  };
}

// Downlink-encoder: {cmd:"emptied"} | {cmd:"posterior", post:[geen,cel,pakket]} | {cmd:"thresholds", thr:[4]}
function encodeDownlink(input) {
  var d = input.data, out = [];
  var p16 = function (v) { v = Math.max(0, Math.min(65535, Math.round(v))); out.push(v >> 8, v & 0xff); };
  if (d.cmd === "emptied") out.push(0x01);
  else if (d.cmd === "posterior") { out.push(0x02); d.post.forEach(function (x) { p16(x * 100); }); }
  else if (d.cmd === "thresholds") { out.push(0x03); d.thr.forEach(p16); }
  else return { errors: ["onbekend commando"] };
  return { bytes: out, fPort: 10, warnings: [], errors: [] };
}

if (typeof module !== "undefined") module.exports = { decodeUplink: decodeUplink, encodeDownlink: encodeDownlink };
