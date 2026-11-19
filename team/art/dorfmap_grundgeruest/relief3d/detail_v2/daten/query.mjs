// P4 detail_v2 Datenschicht: queryPoint(x, z) -> {hoehe, flaeche, untergrund, begehbar, slot, kachel}
// ESM, Node + Browser. Stand Do 19.11.2026 = Geruest (s. STATUS.md).
//
// Koordinaten: Viewer-Meter, 1 Einheit = 1 Zelle = 1 m. x in [0, 336], z in [0, 303].
// Raster: 0,1 m/px, 3360 x 3030, px = floor(x*10), py = floor(z*10) (deckungsgleich mit UV1 = (x/336, z/303)).
//
// Herkunft der Werte (Zielstand Fr):
//   hoehe      exakt aus dem Mesh-Dreieck (Gitterindex, baryzentrisch); ersatzweise hoehe.png (nur wenn gesetzt)
//   flaeche    flaeche.png (8 bit, Klassen-Index)       begehbar  begehbar.png (1 bit)
//   untergrund untergrund.png (8 bit) [A]              slot      slot.png (16 bit Bitfeld)
//   kachel     analytisch (A-H x 1-7, 42 x 43 m)
// Fehlt eine Quelle, ist der Wert null (nichts wird vorgetaeuscht). quellen() sagt, was geladen ist.

export const NX = 336, NY = 303, PX_PRO_M = 10;
export const BREITE_PX = NX * PX_PRO_M, HOEHE_PX = NY * PX_PRO_M;
const BUCHST = 'ABCDEFGH';

export const FLAECHE = ['grund', 'weg', 'ufer', 'fels_klippe', 'wasser', 'bruecke'];
export const UNTERGRUND = [null, 'schnee', 'wald', 'boden', 'sand'];
export const SLOT_BITS = { id: 0x0fff, deko_baum_ok: 1 << 12, deko_fels_ok: 1 << 13, bauplatz_zelle: 1 << 14 };

export function pruefePunkt(x, z) {
  if (!Number.isFinite(x) || !Number.isFinite(z) || x < 0 || z < 0 || x > NX || z > NY)
    throw new RangeError(`Punkt ausserhalb der Karte: ${x}|${z} (erlaubt 0-${NX} | 0-${NY})`);
}

/** Pixel (px, py) zum Weltpunkt; Kartenrand 336/303 wird auf das letzte Pixel geklemmt. */
export function weltZuPixel(x, z) {
  pruefePunkt(x, z);
  return { px: Math.min(BREITE_PX - 1, Math.floor(x * PX_PRO_M + 1e-9)),
           py: Math.min(HOEHE_PX - 1, Math.floor(z * PX_PRO_M + 1e-9)) };
}

/** UV1 = (x/336, z/303). */
export function weltZuUv1(x, z) { pruefePunkt(x, z); return { u: x / NX, v: z / NY }; }

/** Kachel-ID A1..H7: Spalte = min(floor(x/42),7), Zeile = min(floor(z/43),6)+1. */
export function kachelId(x, z) {
  pruefePunkt(x, z);
  const i = Math.min(7, Math.floor(x / 42)), j = Math.min(6, Math.floor(z / 43));
  return BUCHST[i] + (j + 1);
}

/** Bounds [x0, z0, x1, z1] einer Kachel (Zeile 7 bis z=303). */
export function kachelGrenzen(id) {
  const i = BUCHST.indexOf(id[0]), j = Number(id.slice(1)) - 1;
  if (i < 0 || !(j >= 0 && j <= 6) || id.length !== 2) throw new RangeError(`Kachel unbekannt: ${id}`);
  return [42 * i, 43 * j, 42 * (i + 1), j === 6 ? NY : 43 * (j + 1)];
}

/** slot.png-Wert dekodieren. slotsById (optional): Map id -> Eintrag aus slots.json. */
export function dekodiereSlot(wert, slotsById) {
  const id = wert & SLOT_BITS.id;
  const e = id && slotsById ? slotsById.get(id) : undefined;
  return {
    id: id || null,
    art: e ? e.art : null,
    name: e ? e.name : null,
    bauplatz_zelle: !!(wert & SLOT_BITS.bauplatz_zelle),
    deko_baum_ok: !!(wert & SLOT_BITS.deko_baum_ok),
    deko_fels_ok: !!(wert & SLOT_BITS.deko_fels_ok),
  };
}

/**
 * Gitterindex fuer ein Dreiecksnetz (Positionen x,y,z; y = Hoehe).
 * hoeheAus(x, z) liefert die baryzentrisch interpolierte Hoehe der obersten nach oben zeigenden Flaeche oder null.
 */
export function baueMeshIndex(positionen, indizes, zelle_m = 1) {
  const gx = Math.ceil(NX / zelle_m), gz = Math.ceil(NY / zelle_m);
  const zahl = new Uint32Array(gx * gz + 1);
  const nT = indizes.length / 3;
  const bb = (t, f) => {
    const a = indizes[3 * t] * 3, b = indizes[3 * t + 1] * 3, c = indizes[3 * t + 2] * 3, P = positionen;
    const x0 = Math.max(0, Math.floor(Math.min(P[a], P[b], P[c]) / zelle_m)), x1 = Math.min(gx - 1, Math.floor(Math.max(P[a], P[b], P[c]) / zelle_m));
    const z0 = Math.max(0, Math.floor(Math.min(P[a + 2], P[b + 2], P[c + 2]) / zelle_m)), z1 = Math.min(gz - 1, Math.floor(Math.max(P[a + 2], P[b + 2], P[c + 2]) / zelle_m));
    for (let j = z0; j <= z1; j++) for (let i = x0; i <= x1; i++) f(j * gx + i);
  };
  for (let t = 0; t < nT; t++) bb(t, (k) => { zahl[k + 1]++; });
  for (let k = 0; k < gx * gz; k++) zahl[k + 1] += zahl[k];
  const liste = new Uint32Array(zahl[gx * gz]), pos = zahl.slice(0, gx * gz);
  for (let t = 0; t < nT; t++) bb(t, (k) => { liste[pos[k]++] = t; });
  const EPS = 1e-9;
  return {
    dreiecke: nT,
    hoeheAus(x, z) {
      const i = Math.min(gx - 1, Math.floor(x / zelle_m)), j = Math.min(gz - 1, Math.floor(z / zelle_m)), k = j * gx + i;
      let best = null;
      for (let n = zahl[k]; n < zahl[k + 1]; n++) {
        const t = liste[n], P = positionen;
        const a = indizes[3 * t] * 3, b = indizes[3 * t + 1] * 3, c = indizes[3 * t + 2] * 3;
        const ax = P[a], az = P[a + 2], bx = P[b], bz = P[b + 2], cx = P[c], cz = P[c + 2];
        const d = (bz - cz) * (ax - cx) + (cx - bx) * (az - cz);
        if (Math.abs(d) < 1e-12) continue; // senkrechtes Dreieck (Wand) hat keine Draufsicht
        const l1 = ((bz - cz) * (x - cx) + (cx - bx) * (z - cz)) / d;
        const l2 = ((cz - az) * (x - cx) + (ax - cx) * (z - cz)) / d;
        const l3 = 1 - l1 - l2;
        if (l1 < -EPS || l2 < -EPS || l3 < -EPS) continue;
        const y = l1 * P[a + 1] + l2 * P[b + 1] + l3 * P[c + 1];
        if (best === null || y > best) best = y;
      }
      return best;
    },
  };
}

/**
 * Datenschicht aus geladenen Quellen bauen. Alle Quellen optional:
 *   { flaeche, begehbar, untergrund, slot, hoehe: {breite,hoehe,daten}, hoeheSkala: {offset_m, skala_m},
 *     mesh: {positionen, indizes}, slots: slots.json-Objekt }
 */
export function erzeugeDatenschicht(q = {}) {
  for (const k of ['flaeche', 'begehbar', 'untergrund', 'slot', 'hoehe']) {
    const r = q[k];
    if (r && (r.breite !== BREITE_PX || r.hoehe !== HOEHE_PX))
      throw new Error(`${k}.png hat ${r.breite}x${r.hoehe} statt ${BREITE_PX}x${HOEHE_PX}`);
  }
  if (q.hoehe && !(q.hoeheSkala && Number.isFinite(q.hoeheSkala.offset_m) && Number.isFinite(q.hoeheSkala.skala_m)))
    throw new Error('hoehe.png ohne offset_m/skala_m');
  const meshIndex = q.mesh ? baueMeshIndex(q.mesh.positionen, q.mesh.indizes) : null;
  const slotsById = q.slots ? new Map(q.slots.slots.map((s) => [s.id, s])) : null;
  const lies = (r, px, py) => r.daten[py * BREITE_PX + px];

  function hoeheAusPng(x, z) {
    // bilinear zwischen Pixelmitten
    const r = q.hoehe, u = Math.min(BREITE_PX - 1, Math.max(0, x * PX_PRO_M - 0.5)), v = Math.min(HOEHE_PX - 1, Math.max(0, z * PX_PRO_M - 0.5));
    const i = Math.min(BREITE_PX - 2, Math.floor(u)), j = Math.min(HOEHE_PX - 2, Math.floor(v)), fu = u - i, fv = v - j;
    const w = (a, b) => lies(r, a, b);
    const g = (w(i, j) * (1 - fu) + w(i + 1, j) * fu) * (1 - fv) + (w(i, j + 1) * (1 - fu) + w(i + 1, j + 1) * fu) * fv;
    return q.hoeheSkala.offset_m + g * q.hoeheSkala.skala_m;
  }

  function queryPoint(x, z) {
    const { px, py } = weltZuPixel(x, z);
    let hoehe = null;
    if (meshIndex) hoehe = meshIndex.hoeheAus(x, z);
    else if (q.hoehe) hoehe = hoeheAusPng(x, z);
    return {
      hoehe,
      flaeche: q.flaeche ? (FLAECHE[lies(q.flaeche, px, py)] ?? null) : null,
      untergrund: q.untergrund ? (UNTERGRUND[lies(q.untergrund, px, py)] ?? null) : null,
      begehbar: q.begehbar ? lies(q.begehbar, px, py) === 1 : null,
      slot: q.slot ? dekodiereSlot(lies(q.slot, px, py), slotsById) : null,
      kachel: kachelId(x, z),
    };
  }

  return {
    queryPoint,
    quellen: () => ({
      hoehe: meshIndex ? 'mesh' : q.hoehe ? 'hoehe.png' : null,
      flaeche: q.flaeche ? 'flaeche.png' : null, untergrund: q.untergrund ? 'untergrund.png' : null,
      begehbar: q.begehbar ? 'begehbar.png' : null, slot: q.slot ? 'slot.png' : null,
      slots: slotsById ? 'slots.json' : null, kachel: 'analytisch',
    }),
  };
}

/**
 * Laedt die vorhandenen Dateien aus basis (Node: Ordnerpfad, Browser: URL). Fehlende Dateien -> Quelle null.
 * Mesh (P2-.glb) wird separat uebergeben: ladeDatenschicht(basis, {mesh}).
 */
export async function ladeDatenschicht(basis, extra = {}) {
  const { decodePng } = await import('./png.mjs');
  const node = typeof process !== 'undefined' && !!(process.versions && process.versions.node);
  const holen = async (name) => {
    try {
      if (node) {
        const fs = await import('node:fs/promises'), path = await import('node:path');
        return new Uint8Array(await fs.readFile(path.join(basis, name)));
      }
      const r = await fetch(new URL(name, basis.endsWith('/') ? basis : basis + '/'));
      return r.ok ? new Uint8Array(await r.arrayBuffer()) : null;
    } catch (e) {
      if (e && e.code === 'ENOENT') return null;
      throw e;
    }
  };
  const json = async (n) => { const b = await holen(n); return b ? JSON.parse(new TextDecoder().decode(b)) : null; };
  const png = async (n) => { const b = await holen(n); return b ? decodePng(b) : null; };
  const legende = await json('legende.json');
  const hs = legende && legende.dateien && legende.dateien['hoehe.png'];
  const q = {
    flaeche: await png('flaeche.png'), begehbar: await png('begehbar.png'), untergrund: await png('untergrund.png'),
    slot: await png('slot.png'), hoehe: await png('hoehe.png'), slots: await json('slots.json'), ...extra,
  };
  if (q.hoehe) q.hoeheSkala = { offset_m: hs && hs.offset_m, skala_m: hs && hs.skala_m };
  return { legende, ...erzeugeDatenschicht(q) };
}
