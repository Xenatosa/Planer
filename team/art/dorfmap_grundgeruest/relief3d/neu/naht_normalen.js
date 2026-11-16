// P12: Normalen an Kachelnaehten gemeinsam rechnen.
// Jede Kacheloberflaeche ist ein eigenes Mesh; computeVertexNormals() sieht an der Kachelkante nur die
// Dreiecke der eigenen Kachel. Bei gleicher Hoehe auf beiden Seiten entstehen so zwei verschiedene
// Normalen am selben Punkt -> harte Helligkeitslinie genau auf der Naht (QA P4c: x=126 C4/D4, x=84 B6/C6).
// Hier werden fuer jeden Randvertex die (flaechengewichteten, wie three.js computeVertexNormals) Dreiecks-
// normalen ALLER Kacheln aufsummiert, die diesen Punkt teilen, und die normierte Summe allen Kacheln
// gegeben. Das ist genau die Normale, die ein einziges zusammenhaengendes Mesh dort haette.
// Nur Randvertices werden geaendert; Innenvertices, Positionen und Indizes bleiben unveraendert.
//   kacheln: [{ name, positions: Float32Array, indices: Uint32Array, bounds: [x0,z0,x1,z1], normals?: Float32Array }]
//   rs: Rastersamples je Karteneinheit (Positionen * rs = ganzzahlige Gitterindizes)
// Rueckgabe: { geaendert: {name: anzahl}, naehte: anzahl gemeinsamer Punkte }; normals werden in place gesetzt.
export function randIndizes(positions, bounds, rs) {
  const [x0, z0, x1, z1] = bounds.map(v => Math.round(v * rs)), out = [];
  for (let k = 0; k < positions.length / 3; k++) {
    const gx = Math.round(positions[k * 3] * rs), gz = Math.round(positions[k * 3 + 2] * rs);
    if (gx === x0 || gx === x1 || gz === z0 || gz === z1) out.push(k);
  }
  return out;
}

export function nahtNormalen(kacheln, rs, tolHoehe = 1e-4) {
  const summe = new Map();   // Gitterschluessel -> [nx, ny, nz, y, anzahlKacheln]
  const key = (p, k) => Math.round(p[k * 3 + 2] * rs) * 1048576 + Math.round(p[k * 3] * rs);
  const rand = [];
  for (const t of kacheln) {
    const p = t.positions, idx = t.indices, ri = randIndizes(p, t.bounds, rs), istRand = new Uint8Array(p.length / 3);
    for (const k of ri) istRand[k] = 1;
    const acc = new Map();
    for (let i = 0; i < idx.length; i += 3) {
      const a = idx[i], b = idx[i + 1], c = idx[i + 2];
      if (!istRand[a] && !istRand[b] && !istRand[c]) continue;
      // wie three.js: cb = C - B, ab = A - B, n = cb x ab (ungenormt = flaechengewichtet)
      const cbx = p[c * 3] - p[b * 3], cby = p[c * 3 + 1] - p[b * 3 + 1], cbz = p[c * 3 + 2] - p[b * 3 + 2];
      const abx = p[a * 3] - p[b * 3], aby = p[a * 3 + 1] - p[b * 3 + 1], abz = p[a * 3 + 2] - p[b * 3 + 2];
      const nx = cby * abz - cbz * aby, ny = cbz * abx - cbx * abz, nz = cbx * aby - cby * abx;
      for (const v of [a, b, c]) {
        if (!istRand[v]) continue;
        const s = acc.get(v) || [0, 0, 0]; s[0] += nx; s[1] += ny; s[2] += nz; acc.set(v, s);
      }
    }
    for (const [v, s] of acc) {
      const g = key(p, v), y = p[v * 3 + 1], e = summe.get(g);
      if (!e) summe.set(g, [s[0], s[1], s[2], y, 1]);
      else if (Math.abs(e[3] - y) <= tolHoehe) { e[0] += s[0]; e[1] += s[1]; e[2] += s[2]; e[4] += 1; }
    }
    rand.push([t, ri]);
  }
  const geaendert = {};
  let naehte = 0;
  for (const e of summe.values()) if (e[4] > 1) naehte++;
  for (const [t, ri] of rand) {
    if (!t.normals) continue;
    let n = 0;
    for (const v of ri) {
      const e = summe.get(key(t.positions, v));
      if (!e || e[4] < 2 || Math.abs(e[3] - t.positions[v * 3 + 1]) > tolHoehe) continue;
      const l = Math.hypot(e[0], e[1], e[2]) || 1;
      t.normals[v * 3] = e[0] / l; t.normals[v * 3 + 1] = e[1] / l; t.normals[v * 3 + 2] = e[2] / l; n++;
    }
    geaendert[t.name] = n;
  }
  return { geaendert, naehte };
}
