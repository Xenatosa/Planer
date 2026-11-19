// Minimaler glb-Leser fuer die P2-Kacheln (ESM, Node + Browser, keine Abhaengigkeiten).
// Liest je Mesh-Primitive POSITION (float VEC3), Indizes (u8/u16/u32, sonst 0..n-1) und das
// Vertex-Attribut _FLAECHE (SCALAR, u8/u16/u32/float; Klasse 0-5) [F ueber Grundgeruest 19.11.2026].
// Node-Transformationen werden NICHT angewandt (P2 exportiert in Welt-Metern) - Abweichung -> Fehler.
// Ergebnis: {positionen: Float32Array, indizes: Uint32Array, flaechen: Uint8Array|null}

const KOMP = { 5121: Uint8Array, 5123: Uint16Array, 5125: Uint32Array, 5126: Float32Array };
const ANZ = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4 };

function accessor(gltf, bin, i) {
  const a = gltf.accessors[i], bv = gltf.bufferViews[a.bufferView], T = KOMP[a.componentType];
  if (!T) throw new Error(`glb: componentType ${a.componentType} nicht unterstuetzt`);
  const k = ANZ[a.type], gr = T.BYTES_PER_ELEMENT;
  const start = bin.byteOffset + (bv.byteOffset || 0) + (a.byteOffset || 0);
  const stride = bv.byteStride || k * gr;
  const out = new T(a.count * k);
  const dv = new DataView(bin.buffer);
  const lies = { 5121: (o) => dv.getUint8(o), 5123: (o) => dv.getUint16(o, true), 5125: (o) => dv.getUint32(o, true), 5126: (o) => dv.getFloat32(o, true) }[a.componentType];
  for (let n = 0; n < a.count; n++) for (let c = 0; c < k; c++) out[n * k + c] = lies(start + n * stride + c * gr);
  return out;
}

export function leseGlb(input) {
  const u8 = input instanceof Uint8Array ? input : new Uint8Array(input);
  const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
  if (dv.getUint32(0, true) !== 0x46546c67) throw new Error('keine glb-Datei');
  let off = 12, gltf = null, bin = null;
  while (off < u8.length) {
    const len = dv.getUint32(off, true), typ = dv.getUint32(off + 4, true), d = u8.subarray(off + 8, off + 8 + len);
    if (typ === 0x4e4f534a) gltf = JSON.parse(new TextDecoder().decode(d));
    else if (typ === 0x004e4942) bin = d;
    off += 8 + len;
  }
  if (!gltf) throw new Error('glb ohne JSON');
  for (const n of gltf.nodes || []) {
    if (n.matrix || n.rotation || n.scale || (n.translation && n.translation.some((v) => v !== 0)))
      throw new Error('glb: Node-Transformation vorhanden, erwartet Welt-Meter ohne Transform');
  }
  const P = [], I = [], F = []; let basis = 0, mitF = null;
  for (const m of gltf.meshes || []) for (const pr of m.primitives) {
    if ((pr.mode ?? 4) !== 4) continue;
    const pos = accessor(gltf, bin, pr.attributes.POSITION), nv = pos.length / 3;
    const idx = pr.indices !== undefined ? accessor(gltf, bin, pr.indices) : Uint32Array.from({ length: nv }, (_, i) => i);
    const hatF = pr.attributes._FLAECHE !== undefined;
    if (mitF === null) mitF = hatF; else if (mitF !== hatF) throw new Error('glb: _FLAECHE nur an einem Teil der Primitives');
    P.push(pos); I.push(Uint32Array.from(idx, (v) => v + basis));
    if (hatF) F.push(Uint8Array.from(accessor(gltf, bin, pr.attributes._FLAECHE), (v) => Math.round(v)));
    basis += nv;
  }
  const cat = (L, T) => { const o = new T(L.reduce((s, a) => s + a.length, 0)); let p = 0; for (const a of L) { o.set(a, p); p += a.length; } return o; };
  const flaechen = mitF ? cat(F, Uint8Array) : null;
  if (flaechen) for (const v of flaechen) if (v > 5) throw new Error(`glb: _FLAECHE-Wert ${v} nicht 0-5`);
  return { positionen: cat(P, Float32Array), indizes: cat(I, Uint32Array), flaechen };
}

/** Mehrere Kacheln (leseGlb-Ergebnisse) zu einem Netz zusammenfuehren. */
export function fuegeZusammen(teile) {
  let nv = 0, ni = 0; for (const t of teile) { nv += t.positionen.length; ni += t.indizes.length; }
  const positionen = new Float32Array(nv), indizes = new Uint32Array(ni);
  const mitF = teile.every((t) => t.flaechen), flaechen = mitF ? new Uint8Array(nv / 3) : null;
  let pv = 0, pi = 0;
  for (const t of teile) {
    positionen.set(t.positionen, pv);
    for (let k = 0; k < t.indizes.length; k++) indizes[pi + k] = t.indizes[k] + pv / 3;
    if (mitF) flaechen.set(t.flaechen, pv / 3);
    pv += t.positionen.length; pi += t.indizes.length;
  }
  return { positionen, indizes, flaechen };
}
