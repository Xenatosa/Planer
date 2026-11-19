// Bodenhaftung per senkrechtem Strahl auf das Mesh [S]: je Mesh ein 2-m-Zellraster der Dreiecke (xz),
// Abfrage = Punkt-in-Dreieck (baryzentrisch) und Hoehe aus der Dreiecksebene. Exakt wie ein Raycast nach unten,
// aber O(1) je Abfrage. Spaeter optional durch queryPoint (P4) ersetzbar.
const ZELLE = 2;
export class Boden {
  constructor() { this.netze = []; this.ms = 0; }
  add(mesh) {
    const t0 = performance.now(); mesh.updateMatrixWorld(true);
    const g = mesh.geometry, P = g.attributes.position, n = P.count, W = new Float32Array(n * 3), e = mesh.matrixWorld.elements;
    for (let i = 0; i < n; i++) { const x = P.getX(i), y = P.getY(i), z = P.getZ(i);
      W[i * 3] = e[0] * x + e[4] * y + e[8] * z + e[12]; W[i * 3 + 1] = e[1] * x + e[5] * y + e[9] * z + e[13]; W[i * 3 + 2] = e[2] * x + e[6] * y + e[10] * z + e[14]; }
    const I = g.index ? g.index.array : Uint32Array.from({ length: n }, (_, i) => i);
    let x0 = Infinity, z0 = Infinity, x1 = -Infinity, z1 = -Infinity;
    for (let i = 0; i < n; i++) { const x = W[i * 3], z = W[i * 3 + 2]; if (x < x0) x0 = x; if (x > x1) x1 = x; if (z < z0) z0 = z; if (z > z1) z1 = z; }
    const nx = Math.max(1, Math.ceil((x1 - x0) / ZELLE)), nz = Math.max(1, Math.ceil((z1 - z0) / ZELLE)), zellen = Array.from({ length: nx * nz }, () => []);
    for (let t = 0; t < I.length; t += 3) { const a = I[t] * 3, b = I[t + 1] * 3, c = I[t + 2] * 3;
      const ia = Math.min(W[a], W[b], W[c]), ib = Math.max(W[a], W[b], W[c]), ja = Math.min(W[a + 2], W[b + 2], W[c + 2]), jb = Math.max(W[a + 2], W[b + 2], W[c + 2]);
      for (let j = Math.max(0, Math.floor((ja - z0) / ZELLE)); j <= Math.min(nz - 1, Math.floor((jb - z0) / ZELLE)); j++)
        for (let i = Math.max(0, Math.floor((ia - x0) / ZELLE)); i <= Math.min(nx - 1, Math.floor((ib - x0) / ZELLE)); i++) zellen[j * nx + i].push(t); }
    this.netze.push({ W, I, x0, z0, x1, z1, nx, nz, zellen }); this.ms += performance.now() - t0;
  }
  fertig() { this.ms = Math.round(this.ms); }
  // hoechste Flaeche unter (x,z); mit yMax: hoechste Flaeche bis yMax + 0,6 m (Stufenhoehe), sonst die hoechste.
  hoehe(x, z, yMax = Infinity) {
    let best = null, bestUnter = null;
    for (const m of this.netze) {
      if (x < m.x0 - 1e-6 || x > m.x1 + 1e-6 || z < m.z0 - 1e-6 || z > m.z1 + 1e-6) continue;
      const i = Math.min(m.nx - 1, Math.floor((x - m.x0) / ZELLE)), j = Math.min(m.nz - 1, Math.floor((z - m.z0) / ZELLE)), W = m.W, I = m.I;
      for (const t of m.zellen[j * m.nx + i]) { const a = I[t] * 3, b = I[t + 1] * 3, c = I[t + 2] * 3;
        const ax = W[a], az = W[a + 2], bx = W[b], bz = W[b + 2], cx = W[c], cz = W[c + 2];
        const d = (bz - cz) * (ax - cx) + (cx - bx) * (az - cz); if (Math.abs(d) < 1e-12) continue;
        const u = ((bz - cz) * (x - cx) + (cx - bx) * (z - cz)) / d, v = ((cz - az) * (x - cx) + (ax - cx) * (z - cz)) / d, w = 1 - u - v;
        if (u < -1e-7 || v < -1e-7 || w < -1e-7) continue;
        const y = u * W[a + 1] + v * W[b + 1] + w * W[c + 1];
        if (best === null || y > best) best = y; if (y <= yMax + 0.6 && (bestUnter === null || y > bestUnter)) bestUnter = y; }
    }
    return bestUnter ?? best;
  }
}
