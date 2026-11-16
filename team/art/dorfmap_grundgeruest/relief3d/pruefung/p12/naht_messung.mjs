// P12: Normalen-Differenz an allen Kachelnaehten messen (vorher = je Kachel computeVertexNormals wie im
// Viewer, nachher = zusaetzlich neu/naht_normalen.js). Je Naht: Winkel zwischen den Normalen beider
// Kacheln am selben Gitterpunkt (Grad): max, mittel, p95, Anzahl > 1 Grad / > 5 Grad.
// Aufruf (relief3d/): NODE_PATH=<three> node pruefung/p12/naht_messung.mjs <paket.json.gz> <aus.json>
//   Paket = alle_kacheln.json.gz (56 Kacheln) oder neu/relief_neu.json.gz (D1/G1/D2 wie index.html).
import fs from 'fs'; import zlib from 'zlib'; import path from 'path'; import { createRequire } from 'module';
const require = createRequire(path.resolve('package.json'));
const THREE = require('three');
const quelle = fs.readFileSync(path.resolve('neu/naht_normalen.js'), 'utf8');
const { nahtNormalen } = await import('data:text/javascript;base64,' + Buffer.from(quelle).toString('base64'));
const [paket, aus] = process.argv.slice(2);
const D = JSON.parse(zlib.gunzipSync(fs.readFileSync(paket)));
const M = D.alle_kacheln || D.neu_mesh_tiles, rs = D.rs;
const f32 = s => { const b = Buffer.from(s, 'base64'); return new Float32Array(b.buffer, b.byteOffset, b.length / 4); };
const u32 = s => { const b = Buffer.from(s, 'base64'); return new Uint32Array(b.buffer, b.byteOffset, b.length / 4); };
const kacheln = Object.entries(M.tiles).map(([name, t]) => {
  const positions = new Float32Array(f32(t.vertices_xyz_f32)), indices = new Uint32Array(u32(t.indices_u32));
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  g.setIndex(new THREE.BufferAttribute(indices, 1)); g.computeVertexNormals();
  return { name, positions, indices, bounds: t.bounds, normals: g.attributes.normal.array };
});
const key = (p, k) => Math.round(p[k * 3 + 2] * rs) * 1048576 + Math.round(p[k * 3] * rs);
function messen() {
  const punkte = new Map();
  for (const t of kacheln) for (let k = 0; k < t.positions.length / 3; k++) {
    const gx = Math.round(t.positions[k * 3] * rs), gz = Math.round(t.positions[k * 3 + 2] * rs), [x0, z0, x1, z1] = t.bounds.map(v => v * rs);
    if (gx !== x0 && gx !== x1 && gz !== z0 && gz !== z1) continue;
    const g = key(t.positions, k); (punkte.get(g) || punkte.set(g, []).get(g)).push([t.name, t.normals.subarray(k * 3, k * 3 + 3), gx / rs, gz / rs]);
  }
  const naehte = {};
  for (const L of punkte.values()) for (let i = 0; i < L.length; i++) for (let j = i + 1; j < L.length; j++) {
    const [a, na, x, z] = L[i], [b, nb] = L[j], n = [a, b].sort().join('|');
    const c = Math.max(-1, Math.min(1, na[0] * nb[0] + na[1] * nb[1] + na[2] * nb[2])), w = Math.acos(c) * 180 / Math.PI;
    (naehte[n] ||= []).push([w, x, z]);
  }
  const out = {};
  for (const [n, L] of Object.entries(naehte)) {
    const w = L.map(e => e[0]).sort((p, q) => p - q), max = L.reduce((m, e) => e[0] > m[0] ? e : m, L[0]);
    out[n] = { punkte: L.length, max_grad: +w[w.length - 1].toFixed(3), mittel_grad: +(w.reduce((s, v) => s + v, 0) / w.length).toFixed(3),
      p95_grad: +w[Math.floor(0.95 * (w.length - 1))].toFixed(3), ueber_1: w.filter(v => v > 1).length, ueber_5: w.filter(v => v > 5).length,
      max_bei: [max[1], max[2]] };
  }
  return out;
}
const zusammen = r => { const v = Object.values(r); return { naehte: v.length, punkte: v.reduce((s, e) => s + e.punkte, 0),
  max_grad: Math.max(...v.map(e => e.max_grad)), ueber_1: v.reduce((s, e) => s + e.ueber_1, 0), ueber_5: v.reduce((s, e) => s + e.ueber_5, 0) }; };
const vorher = messen();
const innen = kacheln.map(t => new Float32Array(t.normals));
const info = nahtNormalen(kacheln, rs);
const nachher = messen();
// Kontrolle: Innenvertices unveraendert
let innenGeaendert = 0;
kacheln.forEach((t, i) => { for (let k = 0; k < t.normals.length; k++) if (t.normals[k] !== innen[i][k]) innenGeaendert++; });
const geaendertGesamt = Object.values(info.geaendert).reduce((s, v) => s + v, 0);
const bericht = { paket: path.basename(paket), kacheln: kacheln.length, vorher_gesamt: zusammen(vorher), nachher_gesamt: zusammen(nachher),
  randnormalen_geaendert: info.geaendert, normal_komponenten_geaendert: innenGeaendert, randvertices_geaendert: geaendertGesamt, vorher, nachher };
fs.writeFileSync(aus, JSON.stringify(bericht, null, 1));
console.log(JSON.stringify({ vorher: bericht.vorher_gesamt, nachher: bericht.nachher_gesamt, randvertices_geaendert: geaendertGesamt }));
for (const n of ['C4|D4', 'B6|C6', 'D1|D2']) if (vorher[n]) console.log(n, 'vorher', JSON.stringify(vorher[n]), 'nachher max', nachher[n].max_grad);
