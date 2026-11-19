// Bodenhaftung per senkrechtem Strahl auf das Mesh [S]: je Mesh ein 2-m-Zellraster der Dreiecke (xz),
// Abfrage = Punkt-in-Dreieck (baryzentrisch), Hoehe aus der Dreiecksebene, Klasse aus _FLAECHE, Neigung aus der Dreiecksnormale.
// Exakt wie ein Raycast nach unten, aber O(1) je Abfrage. Gleiches Verfahren wie baueMeshIndex in detail_v2/daten/query.mjs (P4).
const ZELLE = 2;
export const NICHT_BEGEHBAR = new Set([3, 4]);   // fels_klippe, wasser (verbindlich Grundgeruest 19.11.2026)
export const MAX_NEIGUNG = 35;                   // Grad
export function begehbar(t) {
  if (!t) return false;
  if (t.klasse !== null && NICHT_BEGEHBAR.has(t.klasse)) return false;
  if (t.klasse === 5) return true;               // Brueckendeck begehbar
  return t.neigung <= MAX_NEIGUNG;
}
export class Boden {
  constructor() { this.netze = []; this.ms = 0; this.gemischt = 0; this.dreiecke = 0; this.jeKlasse = [0, 0, 0, 0, 0, 0]; this.ohneKlasse = 0; }
  // klasseFest: Klasse fuer Meshes ohne _FLAECHE (z. B. modelle[].klasse), sonst null
  add(mesh, klasseFest = null) {
    const t0 = performance.now(); mesh.updateMatrixWorld(true);
    const g = mesh.geometry, P = g.attributes.position, n = P.count, W = new Float32Array(n * 3), e = mesh.matrixWorld.elements;
    for (let i = 0; i < n; i++) { const x = P.getX(i), y = P.getY(i), z = P.getZ(i);
      W[i * 3] = e[0] * x + e[4] * y + e[8] * z + e[12]; W[i * 3 + 1] = e[1] * x + e[5] * y + e[9] * z + e[13]; W[i * 3 + 2] = e[2] * x + e[6] * y + e[10] * z + e[14]; }
    const I = g.index ? g.index.array : Uint32Array.from({ length: n }, (_, i) => i);
    const FA = g.attributes._flaeche;                       // GLTFLoader: _FLAECHE -> attributes._flaeche
    const F = FA ? Uint8Array.from(FA.array, v => Math.round(v)) : null;
    const nT = I.length / 3, TK = new Int8Array(nT);         // Dreiecksklasse (-1 = gemischt, -2 = keine)
    for (let t = 0; t < nT; t++) {
      if (F) { const k0 = F[I[3 * t]], k1 = F[I[3 * t + 1]], k2 = F[I[3 * t + 2]]; if (k0 === k1 && k1 === k2) { TK[t] = k0; if (k0 <= 5) this.jeKlasse[k0]++; } else { TK[t] = -1; this.gemischt++; } }
      else if (klasseFest !== null) { TK[t] = klasseFest; this.jeKlasse[klasseFest]++; } else { TK[t] = -2; this.ohneKlasse++; }
    }
    this.dreiecke += nT;
    let x0 = Infinity, z0 = Infinity, x1 = -Infinity, z1 = -Infinity;
    for (let i = 0; i < n; i++) { const x = W[i * 3], z = W[i * 3 + 2]; if (x < x0) x0 = x; if (x > x1) x1 = x; if (z < z0) z0 = z; if (z > z1) z1 = z; }
    const nx = Math.max(1, Math.ceil((x1 - x0) / ZELLE)), nz = Math.max(1, Math.ceil((z1 - z0) / ZELLE)), zellen = Array.from({ length: nx * nz }, () => []);
    for (let t = 0; t < I.length; t += 3) { const a = I[t] * 3, b = I[t + 1] * 3, c = I[t + 2] * 3;
      const ia = Math.min(W[a], W[b], W[c]), ib = Math.max(W[a], W[b], W[c]), ja = Math.min(W[a + 2], W[b + 2], W[c + 2]), jb = Math.max(W[a + 2], W[b + 2], W[c + 2]);
      for (let j = Math.max(0, Math.floor((ja - z0) / ZELLE)); j <= Math.min(nz - 1, Math.floor((jb - z0) / ZELLE)); j++)
        for (let i = Math.max(0, Math.floor((ia - x0) / ZELLE)); i <= Math.min(nx - 1, Math.floor((ib - x0) / ZELLE)); i++) zellen[j * nx + i].push(t); }
    this.netze.push({ W, I, TK, x0, z0, x1, z1, nx, nz, zellen, name: mesh.name }); this.ms += performance.now() - t0;
  }
  fertig() { this.ms = Math.round(this.ms); }
  // Treffer des Strahls: hoechste Flaeche bis yMax + 0,6 m (Stufe), sonst die hoechste. -> {y, klasse, neigung, netz} | null
  treffer(x, z, yMax = Infinity) {
    let best = null, unter = null;
    for (const m of this.netze) {
      if (x < m.x0 - 1e-6 || x > m.x1 + 1e-6 || z < m.z0 - 1e-6 || z > m.z1 + 1e-6) continue;
      const i = Math.min(m.nx - 1, Math.floor((x - m.x0) / ZELLE)), j = Math.min(m.nz - 1, Math.floor((z - m.z0) / ZELLE)), W = m.W, I = m.I;
      for (const t of m.zellen[j * m.nx + i]) { const a = I[t] * 3, b = I[t + 1] * 3, c = I[t + 2] * 3;
        const ax = W[a], az = W[a + 2], bx = W[b], bz = W[b + 2], cx = W[c], cz = W[c + 2];
        const d = (bz - cz) * (ax - cx) + (cx - bx) * (az - cz); if (Math.abs(d) < 1e-12) continue;   // senkrecht: keine Draufsicht
        const u = ((bz - cz) * (x - cx) + (cx - bx) * (z - cz)) / d, v = ((cz - az) * (x - cx) + (ax - cx) * (z - cz)) / d, w = 1 - u - v;
        if (u < -1e-7 || v < -1e-7 || w < -1e-7) continue;
        const y = u * W[a + 1] + v * W[b + 1] + w * W[c + 1];
        const h = { y, m, t };
        if (best === null || y > best.y) best = h; if (y <= yMax + 0.6 && (unter === null || y > unter.y)) unter = h; }
    }
    const h = unter ?? best; if (!h) return null;
    const { m, t } = h, W = m.W, a = m.I[t] * 3, b = m.I[t + 1] * 3, c = m.I[t + 2] * 3;   // t = Index-Offset (3 * Dreieck)
    const ux = W[b] - W[a], uy = W[b + 1] - W[a + 1], uz = W[b + 2] - W[a + 2], vx = W[c] - W[a], vy = W[c + 1] - W[a + 1], vz = W[c + 2] - W[a + 2];
    const nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
    const neigung = Math.acos(Math.min(1, Math.abs(ny) / Math.hypot(nx, ny, nz))) * 180 / Math.PI;
    const k = m.TK[t / 3];
    return { y: h.y, klasse: k >= 0 ? k : null, gemischt: k === -1, neigung, netz: m.name };
  }
  hoehe(x, z, yMax = Infinity) { const t = this.treffer(x, z, yMax); return t ? t.y : null; }
}
