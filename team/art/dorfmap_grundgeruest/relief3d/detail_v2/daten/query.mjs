// P4 detail_v2 Datenschicht: queryPoint(x, z) -> {hoehe, flaeche, untergrund, begehbar, slot, kachel}
// ESM, Node + Browser. Stand Do 19.11.2026 = Geruest (s. STATUS.md).
//
// Koordinaten: Viewer-Meter, 1 Einheit = 1 Zelle = 1 m. x in [0, 336], z in [0, 303].
// Raster: 0,1 m/px, 3360 x 3030, px = floor(x*10), py = floor(z*10) (deckungsgleich mit UV1 = (x/336, z/303)).
//
// Herkunft der Werte (Zielstand Fr):
//   Q11-Klasse Mesh-Dreiecksklasse aus glTF-Attribut _FLAECHE (glb.mjs, pruefeDreiecksklasse)
//   hoehe      exakt aus dem Mesh-Dreieck (Gitterindex, baryzentrisch); ersatzweise hoehe.png (nur wenn gesetzt)
//   F10        Wasserspiegel zaehlt nur ueber dem Gelaende (Spiegel im Ufer -> Gelaende-Klasse/-Hoehe)
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
 * flaechen (optional): je Vertex die Klasse 0-5 aus dem glTF-Attribut _FLAECHE (P2) [F ueber Grundgeruest 19.11.2026].
 * hoeheAus(x, z):  baryzentrisch interpolierte Hoehe der obersten Flaeche oder null.
 * klasseAus(x, z): Dreiecksklasse der obersten Flaeche (alle 3 Vertices gleich) oder null;
 *                  ein gemischtes Dreieck liefert -1 (Verstoss gegen "klassenrein").
 */
export function baueMeshIndex(positionen, indizes, zelle_m = 1, flaechen = null) {
  if (flaechen && flaechen.length * 3 !== positionen.length) throw new Error('_FLAECHE: Laenge passt nicht zu POSITION');
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
  /** alle Dreiecke unter/ueber (x, z): [{y, t, ny}] (ny = y-Komponente der Einheitsnormale, Vorzeichen nach Wicklung) */
  function treffer(x, z) {
    const i = Math.min(gx - 1, Math.floor(x / zelle_m)), j = Math.min(gz - 1, Math.floor(z / zelle_m)), k = j * gx + i;
    const out = [];
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
      out.push({ y: l1 * P[a + 1] + l2 * P[b + 1] + l3 * P[c + 1], t, ny: normaleY(t) });
    }
    return out;
  }
  function normaleY(t) {
    const P = positionen, a = indizes[3 * t] * 3, b = indizes[3 * t + 1] * 3, c = indizes[3 * t + 2] * 3;
    const ux = P[b] - P[a], uy = P[b + 1] - P[a + 1], uz = P[b + 2] - P[a + 2];
    const vx = P[c] - P[a], vy = P[c + 1] - P[a + 1], vz = P[c + 2] - P[a + 2];
    const nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
    const l = Math.hypot(nx, ny, nz);
    return l > 0 ? ny / l : 0;
  }
  // F10 [F Grundgeruest 19.11.2026]: Wasser-Dreiecke (_FLAECHE 4) zaehlen nur, wo sie echt UEBER der obersten
  // Nicht-Wasser-Flaeche liegen; steckt der Spiegel im Ufer (oder Gleichstand), gewinnen Gelaende-Klasse und -Hoehe.
  const istWasser = (t) => !!flaechen && flaechen[indizes[3 * t]] === WASSER_KLASSE && flaechen[indizes[3 * t + 1]] === WASSER_KLASSE && flaechen[indizes[3 * t + 2]] === WASSER_KLASSE;
  function oberstes(x, z) {
    let w = null, g = null;
    for (const h of treffer(x, z)) {
      if (istWasser(h.t)) { if (w === null || h.y > w.y) w = h; }
      else if (g === null || h.y > g.y) g = h;
    }
    const o = w && (!g || w.y > g.y) ? w : g;
    return o ? { y: o.y, t: o.t, ny: o.ny, f10: !!(w && g && o === g) } : { y: null, t: -1, ny: 0, f10: false };
  }
  const klasseVon = (t) => {
    const k0 = flaechen[indizes[3 * t]], k1 = flaechen[indizes[3 * t + 1]], k2 = flaechen[indizes[3 * t + 2]];
    return k0 === k1 && k1 === k2 ? k0 : -1;
  };
  return {
    dreiecke: nT,
    treffer,
    klasseVon: (t) => (flaechen ? klasseVon(t) : null),
    hoeheAus(x, z) { return oberstes(x, z).y; },
    /** true, wenn am Punkt ein Wasserspiegel im Gelaende steckt (F10 hat das Gelaende gewaehlt). */
    f10Aus(x, z) { return oberstes(x, z).f10; },
    /** Neigung der obersten Flaeche in Grad (0 = waagrecht; Wicklung egal) oder null. */
    neigungAus(x, z) { const o = oberstes(x, z); return o.t < 0 ? null : neigungGrad(o.ny); },
    klasseAus(x, z) {
      if (!flaechen) return null;
      const { t } = oberstes(x, z);
      return t < 0 ? null : klasseVon(t);
    },
    /** Anzahl nicht klassenreiner Dreiecke (Soll 0). */
    gemischteDreiecke() {
      if (!flaechen) return null;
      let n = 0;
      for (let t = 0; t < nT; t++) {
        const k0 = flaechen[indizes[3 * t]];
        if (k0 !== flaechen[indizes[3 * t + 1]] || k0 !== flaechen[indizes[3 * t + 2]]) n++;
      }
      return n;
    },
  };
}

export const WASSER_KLASSE = 4;                      // F10: Wasserspiegel nur ueber dem Gelaende
export const BEGEHBAR_MAX_NEIGUNG_GRAD = 35;      // [F ueber Grundgeruest 19.11.2026]
export const NICHT_BEGEHBAR_KLASSEN = [3, 4];        // fels_klippe, wasser
export const DECK_FENSTER_M = 0.5;                   // [A] Deck = hoechste Aufwaertsflaeche <= tiefste + 0,5 m
export const DECK_NY_MIN = 0.5;                      // [A] Aufwaertsflaeche: Normale y >= 0,5 (<= 60 Grad), Wicklung nach glTF (CCW aussen)
export const FUGE_SUCHE_M = 0.02;                    // [A] Bohlenfuge 1 cm: Nachbarpunkte +-2 cm

export function neigungGrad(ny) { return (Math.acos(Math.min(1, Math.abs(ny))) * 180) / Math.PI; }

/** begehbar = Klasse nicht in {3,4} UND Neigung <= 35 Grad [F ueber Grundgeruest 19.11.2026]. klasse = Index 0-5. */
export function begehbarRegel(klasse, neigung) {
  if (klasse === null || klasse === undefined || klasse < 0 || neigung === null || neigung === undefined) return null;
  return !NICHT_BEGEHBAR_KLASSEN.includes(klasse) && neigung <= BEGEHBAR_MAX_NEIGUNG_GRAD + 1e-9;
}

/**
 * Gelaende aus Kachel-Mesh + Modellen (Bruecken aus manifest.modelle).
 * Im Bereich eines Modells gilt das Deck: unter den nach oben zeigenden Modellflaechen am Punkt die hoechste,
 * die hoechstens DECK_FENSTER_M ueber der tiefsten liegt (Bohle statt Traeger darunter, nicht Gelaender/Pfosten darueber) [A].
 * Faellt der Punkt in eine Bohlenfuge, werden Nachbarpunkte +-FUGE_SUCHE_M versucht.
 * kacheln: {positionen, indizes, flaechen}; modelle: [{id, klasse, mesh: {positionen, indizes}}]
 */
export function baueGelaende(kacheln, modelle = []) {
  const gi = baueMeshIndex(kacheln.positionen, kacheln.indizes, 1, kacheln.flaechen || null);
  const mi = modelle.map((m) => ({ id: m.id, klasse: m.klasse, idx: baueMeshIndex(m.mesh.positionen, m.mesh.indizes, 1) }));
  function deckAn(x, z) {
    for (const m of mi) {
      const h = m.idx.treffer(x, z).filter((e) => e.ny >= DECK_NY_MIN);
      if (!h.length) continue;
      const tief = Math.min(...h.map((e) => e.y));
      let best = null;
      for (const e of h) if (e.y <= tief + DECK_FENSTER_M + 1e-9 && (!best || e.y > best.y)) best = e;
      return { y: best.y, klasse: m.klasse, neigung: neigungGrad(best.ny), modell: m.id };
    }
    return null;
  }
  function deckAus(x, z) {
    const d = deckAn(x, z);
    if (d) return d;
    for (const [dx, dz] of [[FUGE_SUCHE_M, 0], [-FUGE_SUCHE_M, 0], [0, FUGE_SUCHE_M], [0, -FUGE_SUCHE_M]]) {
      const xx = x + dx, zz = z + dz;
      if (xx < 0 || zz < 0 || xx > NX || zz > NY) continue;
      const e = deckAn(xx, zz);
      if (e) return { ...e, fuge: true };
    }
    return null;
  }
  return {
    dreiecke: gi.dreiecke + mi.reduce((s, m) => s + m.idx.dreiecke, 0),
    deckAus,
    hoeheAus(x, z) { const d = deckAus(x, z); return d ? d.y : gi.hoeheAus(x, z); },
    klasseAus(x, z) { const d = deckAus(x, z); return d ? d.klasse : gi.klasseAus(x, z); },
    neigungAus(x, z) { const d = deckAus(x, z); return d ? d.neigung : gi.neigungAus(x, z); },
    begehbarAus(x, z) {
      const d = deckAus(x, z);
      return d ? begehbarRegel(d.klasse, d.neigung) : begehbarRegel(gi.klasseAus(x, z), gi.neigungAus(x, z));
    },
    gemischteDreiecke: () => gi.gemischteDreiecke(),
  };
}

/** Deterministischer Zufall (mulberry32) fuer reproduzierbare Stichproben. */
export function zufall(seed = 1) {
  let a = seed >>> 0;
  return () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}

/**
 * Q11 Flaechentyp: flaeche.png (ueber queryPoint) gegen die Dreiecksklasse _FLAECHE des Mesh an n Zufallspunkten.
 * Punkte ohne Mesh-Treffer zaehlen als "ohne_treffer" und nicht in die Quote. Soll: quote >= 0,995.
 */
export function pruefeDreiecksklasse(datenschicht, meshIndex, n = 10000, seed = 11) {
  const r = zufall(seed);
  let gleich = 0, ungleich = 0, ohne = 0, gemischt = 0;
  const beispiele = [];
  for (let k = 0; k < n; k++) {
    const x = r() * NX, z = r() * NY;
    const km = meshIndex.klasseAus(x, z);
    if (km === null) { ohne++; continue; }
    if (km === -1) { gemischt++; ungleich++; continue; }
    const f = datenschicht.flaecheRoh ? datenschicht.flaecheRoh(x, z) : datenschicht.queryPoint(x, z).flaeche;   // roh: ohne F10-Korrektur
    if (f === FLAECHE[km]) gleich++;
    else { ungleich++; if (beispiele.length < 20) beispiele.push({ x, z, png: f, mesh: FLAECHE[km] }); }
  }
  const quote = gleich + ungleich ? gleich / (gleich + ungleich) : null;
  return { n, gleich, ungleich, gemischt, ohne_treffer: ohne, quote, ok: quote !== null && quote >= 0.995, beispiele };
}

/**
 * Datenschicht aus geladenen Quellen bauen. Alle Quellen optional:
 *   { flaeche, begehbar, untergrund, slot, hoehe: {breite,hoehe,daten}, hoeheSkala: {offset_m, skala_m},
 *     mesh: {positionen, indizes, flaechen?} ODER gelaende: baueGelaende(...) / ladeMesh(...).gelaende, slots: slots.json-Objekt }
 */
export function erzeugeDatenschicht(q = {}) {
  for (const k of ['flaeche', 'begehbar', 'untergrund', 'slot', 'hoehe']) {
    const r = q[k];
    if (r && (r.breite !== BREITE_PX || r.hoehe !== HOEHE_PX))
      throw new Error(`${k}.png hat ${r.breite}x${r.hoehe} statt ${BREITE_PX}x${HOEHE_PX}`);
  }
  if (q.hoehe && !(q.hoeheSkala && Number.isFinite(q.hoeheSkala.offset_m) && Number.isFinite(q.hoeheSkala.skala_m)))
    throw new Error('hoehe.png ohne offset_m/skala_m');
  const meshIndex = q.gelaende ? q.gelaende : q.mesh ? baueMeshIndex(q.mesh.positionen, q.mesh.indizes, 1, q.mesh.flaechen || null) : null;
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
    let flaeche = q.flaeche ? (FLAECHE[lies(q.flaeche, px, py)] ?? null) : null;
    let begehbar = q.begehbar ? lies(q.begehbar, px, py) === 1 : (meshIndex && meshIndex.begehbarAus ? meshIndex.begehbarAus(x, z) : null);
    // F10: flaeche.png sagt Wasser, das Mesh hat dort aber Gelaende ueber dem Spiegel -> Gelaende-Klasse (Hoehe ist schon Gelaende)
    if (flaeche === 'wasser' && meshIndex && meshIndex.klasseAus) {
      const k = meshIndex.klasseAus(x, z);
      if (k !== null && k >= 0 && k !== WASSER_KLASSE) {
        flaeche = FLAECHE[k];
        if (meshIndex.begehbarAus) begehbar = meshIndex.begehbarAus(x, z);
        else if (meshIndex.neigungAus) begehbar = begehbarRegel(k, meshIndex.neigungAus(x, z));
      }
    }
    return {
      hoehe,
      flaeche,
      untergrund: q.untergrund ? (UNTERGRUND[lies(q.untergrund, px, py)] ?? null) : null,
      begehbar,
      slot: q.slot ? dekodiereSlot(lies(q.slot, px, py), slotsById) : null,
      kachel: kachelId(x, z),
    };
  }

  /** flaeche.png ohne F10-Korrektur (fuer Q11: Raster gegen Mesh ehrlich vergleichen). */
  function flaecheRoh(x, z) { const { px, py } = weltZuPixel(x, z); return q.flaeche ? (FLAECHE[lies(q.flaeche, px, py)] ?? null) : null; }

  return {
    queryPoint,
    flaecheRoh,
    meshIndex,
    quellen: () => ({
      hoehe: meshIndex ? 'mesh' : q.hoehe ? 'hoehe.png' : null,
      flaeche: q.flaeche ? 'flaeche.png' : null, untergrund: q.untergrund ? 'untergrund.png' : null,
      begehbar: q.begehbar ? 'begehbar.png' : meshIndex && meshIndex.begehbarAus ? 'mesh-regel' : null, slot: q.slot ? 'slot.png' : null,
      slots: slotsById ? 'slots.json' : null, kachel: 'analytisch',
    }),
  };
}

/**
 * Laedt die vorhandenen Dateien aus basis (Node: Ordnerpfad, Browser: URL). Fehlende Dateien -> Quelle null.
 * Mesh: ladeDatenschicht(basis, {gelaende: (await ladeMesh(manifest)).gelaende}) (manifest.mjs).
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
  const mm = await json('masken_meta.json');  // von baue_masken.py: hoehe offset/skala
  const hs = (mm && mm.hoehe) || (legende && legende.dateien && legende.dateien['hoehe.png']);
  const q = {
    flaeche: await png('flaeche.png'), begehbar: await png('begehbar.png'), untergrund: await png('untergrund.png'),
    slot: await png('slot.png'), hoehe: await png('hoehe.png'), slots: await json('slots.json'), ...extra,
  };
  if (q.hoehe) q.hoeheSkala = { offset_m: hs && hs.offset_m, skala_m: hs && hs.skala_m };
  return { legende, ...erzeugeDatenschicht(q) };
}
