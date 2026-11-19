// node --test test/  (aus relief3d/detail_v2/daten/)
// Stand Do 19.11.2026: Geruest-Tests gruen, slot.png committet; Tests, die echte Masken/Mesh brauchen, sind skip/todo (s. STATUS.md).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { deflateSync } from 'node:zlib';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import {
  kachelId, kachelGrenzen, weltZuPixel, weltZuUv1, dekodiereSlot, baueMeshIndex, erzeugeDatenschicht,
  ladeDatenschicht, pruefeDreiecksklasse, FLAECHE, UNTERGRUND, SLOT_BITS, BREITE_PX, HOEHE_PX,
} from '../query.mjs';
import { leseGlb, fuegeZusammen } from '../glb.mjs';
import { decodePng } from '../png.mjs';

const HIER = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const legende = JSON.parse(readFileSync(path.join(HIER, 'legende.json'), 'utf8'));
const slots = JSON.parse(readFileSync(path.join(HIER, 'slots.json'), 'utf8'));
const hat = (n) => existsSync(path.join(HIER, n));
const SLOT_PNG = process.env.DV2_SLOT_PNG || (hat('slot.png') ? path.join(HIER, 'slot.png') : null);
const MASKEN_DA = hat('flaeche.png') && hat('begehbar.png');
const MESH_DA = !!process.env.DV2_MESH; // Fr: Pfad zum P2-Mesh (manifest.json)

// Feste Punkte (Auftrag P4 / Plan Abschnitt 9)
const P = {
  dorfkern: [209, 118], e3_wasser: [189, 100], bruecke_e2: [192, 74.5],
  nordwand: [206.5, 35.5], // klippe=WAND, wand_name=Nord in zellen_relief.csv (Zelle 206|35) [S]
  d2_mitte: [147, 64.5],   // D2-Bereich 126-168 | 43-86 [S Plan 3.2]
};

test('Kachel-ID an festen Punkten', () => {
  assert.equal(kachelId(...P.dorfkern), 'E3');
  assert.equal(kachelId(...P.e3_wasser), 'E3');
  assert.equal(kachelId(...P.bruecke_e2), 'E2');
  assert.equal(kachelId(...P.nordwand), 'E1');
  assert.equal(kachelId(...P.d2_mitte), 'D2');
});

test('Kachel-ID an Kartenraendern und Schnittlinien', () => {
  assert.equal(kachelId(0, 0), 'A1');
  assert.equal(kachelId(336, 0), 'H1');
  assert.equal(kachelId(0, 303), 'A7');
  assert.equal(kachelId(336, 303), 'H7');
  assert.equal(kachelId(41.999, 42.999), 'A1');
  assert.equal(kachelId(42, 43), 'B2');          // Schnittlinie -> hoehere Kachel [A]
  assert.equal(kachelId(100, 301.5), 'C7');      // Randzeilen z 301-303 gehoeren zu Zeile 7 [S P10b]
  assert.deepEqual(kachelGrenzen('A1'), [0, 0, 42, 43]);
  assert.deepEqual(kachelGrenzen('H7'), [294, 258, 336, 303]);
  assert.deepEqual(kachelGrenzen('D2'), [126, 43, 168, 86]); // = D2-Bereich des Plans
  let n = 0; for (const b of 'ABCDEFGH') for (let j = 1; j <= 7; j++) { kachelGrenzen(b + j); n++; }
  assert.equal(n, 56);
  assert.throws(() => kachelGrenzen('I1'), RangeError);
});

test('ausserhalb der Karte -> RangeError', () => {
  for (const [x, z] of [[-0.01, 0], [0, -0.01], [336.01, 10], [10, 303.01], [NaN, 1]])
    assert.throws(() => kachelId(x, z), RangeError);
});

test('Massstab: Pixel und UV1 deckungsgleich', () => {
  assert.deepEqual(weltZuPixel(0, 0), { px: 0, py: 0 });
  assert.deepEqual(weltZuPixel(...P.bruecke_e2), { px: 1920, py: 745 });
  assert.deepEqual(weltZuPixel(336, 303), { px: 3359, py: 3029 });
  assert.deepEqual(weltZuPixel(0.1, 0.3), { px: 1, py: 3 }); // Gleitkomma 0,3*10
  const { u, v } = weltZuUv1(...P.dorfkern);
  assert.equal(Math.floor(u * BREITE_PX), weltZuPixel(...P.dorfkern).px);
  assert.equal(Math.floor(v * HOEHE_PX), weltZuPixel(...P.dorfkern).py);
  assert.equal(legende.massstab.px_pro_m, 10);
  assert.deepEqual(legende.massstab.raster_px, [3360, 3030]);
});

test('legende.json passt zu query.mjs', () => {
  assert.deepEqual(legende.flaeche.klassen.map((k) => k.name), FLAECHE);
  assert.deepEqual(legende.flaeche.klassen.map((k) => k.wert), [0, 1, 2, 3, 4, 5]);
  assert.deepEqual(legende.flaeche.prioritaet, ['wasser', 'bruecke', 'weg', 'ufer', 'fels_klippe', 'grund']);
  assert.deepEqual(legende.untergrund.codes.map((k) => k.name), UNTERGRUND);
  assert.equal(legende.slot_bits.id_maske, SLOT_BITS.id);
  assert.equal(legende.slot_bits.deko_baum_ok, SLOT_BITS.deko_baum_ok);
  assert.equal(legende.slot_bits.deko_fels_ok, SLOT_BITS.deko_fels_ok);
  assert.equal(legende.slot_bits.bauplatz_zelle, SLOT_BITS.bauplatz_zelle);
  assert.equal(legende.slot_bits.reserviert, 1 << 15);
  assert.match(legende.slot_bits.status, /^abgestimmt/);
  assert.ok(legende.dateien['untergrund.png']);
  assert.match(legende.dateien['slot.png'].status, /committet/);
  assert.deepEqual(legende.kacheln.schnitte_x, [0, 42, 84, 126, 168, 210, 252, 294, 336]);
  assert.deepEqual(legende.kacheln.schnitte_z, [0, 43, 86, 129, 172, 215, 258, 303]);
});

test('slots.json: Zaehlung = Sollwerte der Quelle', () => {
  for (const [k, v] of Object.entries(slots.abgleich)) assert.ok(v.ok, `${k}: ist ${v.ist}`);
  assert.equal(slots.zaehlung.plaetze_gesamt, 99);
  assert.equal(slots.zaehlung.deko_slots, 627);
  assert.equal(slots.zaehlung.bauplatz_zellen, 3292);
  const ids = new Set(slots.slots.map((s) => s.id));
  assert.equal(ids.size, slots.slots.length);
  assert.ok(Math.max(...ids) <= SLOT_BITS.id);
  const zellen = new Set();
  for (const s of slots.slots) for (const [cx, cz] of s.zellen_liste) {
    const k = cx + ',' + cz; assert.ok(!zellen.has(k), `Zelle ${k} doppelt`); zellen.add(k);
  }
  for (const q of Object.values(slots.quellen)) assert.match(q.git_blob, /^[0-9a-f]{40}$/);
});

test('Slot am festen Punkt D2-Mitte (Zelle 147|64 = Platz A19, Bauplatz) aus slots.json', () => {
  const s = slots.slots.find((e) => e.zellen_liste.some(([x, z]) => x === 147 && z === 64));
  assert.ok(s); assert.equal(s.name, 'A19'); assert.equal(s.art, 'bauplatz');
});

test('dekodiereSlot', () => {
  const m = new Map([[5, { art: 'bauplatz', name: 'A05' }]]);
  assert.deepEqual(dekodiereSlot(5 | SLOT_BITS.bauplatz_zelle | SLOT_BITS.deko_fels_ok, m),
    { id: 5, art: 'bauplatz', name: 'A05', bauplatz_zelle: true, deko_baum_ok: false, deko_fels_ok: true });
  assert.deepEqual(dekodiereSlot(SLOT_BITS.deko_baum_ok, m),
    { id: null, art: null, name: null, bauplatz_zelle: false, deko_baum_ok: true, deko_fels_ok: false });
});

// --- PNG-Decoder gegen einen eigenen Encoder (alle 5 Filter, 1/8/16 bit) ---
function crc32(b) { let c, t = crc32.t; if (!t) { t = crc32.t = new Uint32Array(256); for (let n = 0; n < 256; n++) { c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } } c = 0xffffffff; for (const x of b) c = t[(c ^ x) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; }
function chunk(typ, d) { const o = Buffer.alloc(12 + d.length); o.writeUInt32BE(d.length, 0); o.write(typ, 4, 'latin1'); Buffer.from(d).copy(o, 8); o.writeUInt32BE(crc32(o.subarray(4, 8 + d.length)), 8 + d.length); return o; }
function encodePng(w, h, bit, werte) {
  const zb = Math.ceil(w * bit / 8), bpp = Math.max(1, bit >> 3), roh = Buffer.alloc(h * (zb + 1));
  let vor = Buffer.alloc(zb);
  for (let y = 0; y < h; y++) {
    const z = Buffer.alloc(zb);
    for (let x = 0; x < w; x++) { const v = werte[y * w + x]; if (bit === 16) z.writeUInt16BE(v, 2 * x); else if (bit === 8) z[x] = v; else if (v) z[x >> 3] |= 0x80 >> (x & 7); }
    const f = y % 5; roh[y * (zb + 1)] = f;
    for (let i = 0; i < zb; i++) {
      const a = i >= bpp ? z[i - bpp] : 0, b = vor[i], c = i >= bpp ? vor[i - bpp] : 0;
      const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c);
      const pr = [0, a, b, (a + b) >> 1, pa <= pb && pa <= pc ? a : pb <= pc ? b : c][f];
      roh[y * (zb + 1) + 1 + i] = (z[i] - pr) & 255;
    }
    vor = z;
  }
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = bit; ihdr[9] = 0;
  return Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ihdr), chunk('IDAT', deflateSync(roh)), chunk('IEND', Buffer.alloc(0))]);
}

test('PNG-Decoder 1/8/16 bit, Filter 0-4', async () => {
  for (const bit of [1, 8, 16]) {
    const w = 13, h = 11, max = 2 ** bit;
    const werte = Array.from({ length: w * h }, (_, i) => (i * 2654435761) % max);
    const r = await decodePng(encodePng(w, h, bit, werte));
    assert.equal(r.breite, w); assert.equal(r.hoehe, h); assert.equal(r.bittiefe, bit);
    assert.deepEqual(Array.from(r.daten), werte);
  }
});

test('Mesh-Gitterindex: baryzentrische Hoehe exakt, Wanddreieck ignoriert', () => {
  // schiefe Ebene y = 0.1*x + 0.02*z + 3 ueber zwei Dreiecke, plus senkrechtes Wanddreieck
  const f = (x, z) => 0.1 * x + 0.02 * z + 3;
  const pos = new Float32Array([100, f(100, 50), 50, 110, f(110, 50), 50, 110, f(110, 60), 60, 100, f(100, 60), 60,
    105, 0, 55, 105, 20, 55, 106, 0, 55]);
  const idx = new Uint32Array([0, 1, 2, 0, 2, 3, 4, 5, 6]);
  const m = baueMeshIndex(pos, idx);
  for (const [x, z] of [[100, 50], [104.3, 51.7], [109.99, 59.99], [105.5, 55]]) assert.ok(Math.abs(m.hoeheAus(x, z) - f(x, z)) < 1e-4);
  assert.equal(m.hoeheAus(10, 10), null);
});

test('erzeugeDatenschicht ohne Quellen: nur Kachel, Rest null (nichts vorgetaeuscht)', () => {
  const d = erzeugeDatenschicht({});
  assert.deepEqual(d.queryPoint(...P.dorfkern), { hoehe: null, flaeche: null, untergrund: null, begehbar: null, slot: null, kachel: 'E3' });
  assert.equal(d.quellen().hoehe, null);
  assert.throws(() => erzeugeDatenschicht({ flaeche: { breite: 10, hoehe: 10, daten: new Uint8Array(100) } }), /3360x3030/);
});

test('ladeDatenschicht liest den Ordner (heute: keine Masken vorhanden -> null)', async () => {
  const d = await ladeDatenschicht(HIER);
  assert.equal(d.legende.schema, 'dv2-datenschicht/1');
  const r = d.queryPoint(...P.e3_wasser);
  assert.equal(r.kachel, 'E3');
  if (!MASKEN_DA) assert.equal(r.flaeche, null);
});

test('slot.png (0,1 m) an festen Punkten', { skip: SLOT_PNG ? false : 'slot.png fehlt (python3 baue_legende_slots.py --slot-png slot.png)' }, async () => {
  const slot = await decodePng(readFileSync(SLOT_PNG));
  const d = erzeugeDatenschicht({ slot, slots });
  const s = d.queryPoint(...P.d2_mitte).slot;
  assert.equal(s.name, 'A19'); assert.equal(s.art, 'bauplatz'); assert.equal(s.bauplatz_zelle, true);
  assert.equal(d.queryPoint(...P.e3_wasser).slot.id, null);
  // jede Slot-Zelle: Pixelmitte traegt die Slot-ID
  for (const e of slots.slots) for (const [cx, cz] of e.zellen_liste)
    assert.equal(d.queryPoint(cx + 0.55, cz + 0.55).slot.id, e.id);
});

test('Masken an festen Punkten (flaeche/begehbar/untergrund)', { skip: MASKEN_DA ? false : 'wartet auf P1 Vektoren (Do 19:00) + P2 Mesh (Fr ~10-12)' }, async () => {
  const d = await ladeDatenschicht(HIER);
  assert.equal(d.queryPoint(...P.e3_wasser).flaeche, 'wasser');
  assert.equal(d.queryPoint(...P.e3_wasser).begehbar, false);
  assert.equal(d.queryPoint(...P.bruecke_e2).flaeche, 'bruecke');
  assert.equal(d.queryPoint(...P.bruecke_e2).begehbar, true);
  assert.equal(d.queryPoint(...P.nordwand).flaeche, 'fels_klippe');
  assert.equal(d.queryPoint(...P.dorfkern).begehbar, true);
  assert.equal(d.queryPoint(...P.d2_mitte).begehbar, true);
  for (const [x, z] of [[0, 0], [336, 0], [0, 303], [336, 303]]) assert.ok(FLAECHE.includes(d.queryPoint(x, z).flaeche));
});

test('Hoehe an festen Punkten aus Mesh', { skip: MESH_DA ? false : 'wartet auf P2 Mesh (Fr ~10-12)' }, () => {});
test('Q11: Hoehe vs. Mesh-Strahl <= 2 cm an 10 000 Zufallspunkten', { todo: 'Fr nach P2; unabhaengiger Strahl (three.js Raycaster) gegen queryPoint' });
test('Q11: Flaechentyp = Dreiecksklasse >= 99,5 % (echtes Mesh)', { skip: MESH_DA && MASKEN_DA ? false : 'wartet auf P2-Mesh mit _FLAECHE + flaeche.png (Fr)' }, () => {
  // Fr: Kachel-.glb laut manifest mit leseGlb lesen, fuegeZusammen, baueMeshIndex(..., flaechen),
  // pruefeDreiecksklasse(datenschicht, meshIndex, 10000) -> ok; gemischteDreiecke() === 0.
  assert.fail('Manifest-Format von P2 noch nicht eingebunden');
});

// --- Vorbereitung Dreiecksklasse ueber glTF-Attribut _FLAECHE (Entscheidung Grundgeruest 19.11.2026) ---
function baueGlb(primitives) {
  // primitives: [{pos: Float32Array, idx: Uint16Array|Uint32Array, fl: Uint8Array}]
  const teile = [], acc = [], views = [], prims = []; let off = 0;
  const add = (arr, ct, typ, count, target) => {
    const b = Buffer.from(arr.buffer, arr.byteOffset, arr.byteLength), pad = (4 - (b.length % 4)) % 4;
    views.push({ buffer: 0, byteOffset: off, byteLength: b.length, ...(target ? { target } : {}) });
    acc.push({ bufferView: views.length - 1, componentType: ct, count, type: typ });
    teile.push(b, Buffer.alloc(pad)); off += b.length + pad; return acc.length - 1;
  };
  for (const p of primitives) {
    const a = { POSITION: add(p.pos, 5126, 'VEC3', p.pos.length / 3, 34962) };
    if (p.fl) a._FLAECHE = add(p.fl, 5121, 'SCALAR', p.fl.length, 34962);
    prims.push({ attributes: a, indices: add(p.idx, p.idx instanceof Uint16Array ? 5123 : 5125, 'SCALAR', p.idx.length, 34963), mode: 4 });
  }
  const bin = Buffer.concat(teile);
  const gltf = { asset: { version: '2.0' }, buffers: [{ byteLength: bin.length }], bufferViews: views, accessors: acc,
    meshes: [{ primitives: prims }], nodes: [{ mesh: 0 }], scenes: [{ nodes: [0] }], scene: 0 };
  let js = Buffer.from(JSON.stringify(gltf)); js = Buffer.concat([js, Buffer.alloc((4 - (js.length % 4)) % 4, 0x20)]);
  const kopf = Buffer.alloc(12); kopf.writeUInt32LE(0x46546c67, 0); kopf.writeUInt32LE(2, 4); kopf.writeUInt32LE(12 + 8 + js.length + 8 + bin.length, 8);
  const ch = (typ, d) => { const h = Buffer.alloc(8); h.writeUInt32LE(d.length, 0); h.writeUInt32LE(typ, 4); return Buffer.concat([h, d]); };
  return Buffer.concat([kopf, ch(0x4e4f534a, js), ch(0x004e4942, bin)]);
}
// Kartenhaelfte als Rechteck aus 2 Dreiecken, Klasse k an allen Vertices
const haelfte = (x0, x1, k) => ({
  pos: new Float32Array([x0, 1, 0, x1, 1, 0, x1, 2, 303, x0, 2, 303]), idx: new Uint16Array([0, 1, 2, 0, 2, 3]), fl: new Uint8Array([k, k, k, k]) });

test('glb.mjs liest POSITION, Indizes und _FLAECHE (2 Primitives, zusammengefuehrt)', () => {
  const m = leseGlb(baueGlb([haelfte(0, 168, 0), haelfte(168, 336, 4)]));
  assert.equal(m.positionen.length, 24); assert.deepEqual(Array.from(m.indizes), [0, 1, 2, 0, 2, 3, 4, 5, 6, 4, 6, 7]);
  assert.deepEqual(Array.from(m.flaechen), [0, 0, 0, 0, 4, 4, 4, 4]);
  const z = fuegeZusammen([m, leseGlb(baueGlb([haelfte(0, 10, 1)]))]);
  assert.equal(z.indizes[12], 8); assert.equal(z.flaechen.length, 12);
  assert.throws(() => leseGlb(baueGlb([{ ...haelfte(0, 1, 0), fl: new Uint8Array([7, 7, 7, 7]) }])), /nicht 0-5/);
});

test('Dreiecksklasse ueber _FLAECHE: klasseAus, gemischte Dreiecke, Q11-Quote gegen flaeche-Raster', () => {
  const m = leseGlb(baueGlb([haelfte(0, 168, 0), haelfte(168, 336, 4)]));
  const mi = baueMeshIndex(m.positionen, m.indizes, 1, m.flaechen);
  assert.equal(mi.klasseAus(10, 10), 0); assert.equal(mi.klasseAus(200, 10), 4);
  assert.equal(mi.gemischteDreiecke(), 0);
  // flaeche-Raster: links grund, rechts wasser -> 100 %
  const daten = new Uint8Array(BREITE_PX * HOEHE_PX);
  for (let y = 0; y < HOEHE_PX; y++) daten.fill(4, y * BREITE_PX + 1680, (y + 1) * BREITE_PX);
  const d = erzeugeDatenschicht({ flaeche: { breite: BREITE_PX, hoehe: HOEHE_PX, daten }, mesh: m });
  const r = pruefeDreiecksklasse(d, d.meshIndex, 10000);
  assert.equal(r.quote, 1); assert.ok(r.ok); assert.equal(r.ohne_treffer, 0);
  // Raster um 2 m verschoben -> ~0,6 % falsch -> nicht ok
  const d2 = new Uint8Array(BREITE_PX * HOEHE_PX);
  for (let y = 0; y < HOEHE_PX; y++) d2.fill(4, y * BREITE_PX + 1700, (y + 1) * BREITE_PX);
  const r2 = pruefeDreiecksklasse(erzeugeDatenschicht({ flaeche: { breite: BREITE_PX, hoehe: HOEHE_PX, daten: d2 } }), mi, 10000);
  assert.ok(!r2.ok && r2.quote < 0.995 && r2.quote > 0.98, `quote ${r2.quote}`);
  // gemischtes Dreieck wird erkannt
  const g = baueMeshIndex(new Float32Array([0, 0, 0, 10, 0, 0, 0, 0, 10]), new Uint32Array([0, 1, 2]), 1, new Uint8Array([0, 1, 0]));
  assert.equal(g.klasseAus(1, 1), -1); assert.equal(g.gemischteDreiecke(), 1);
});
