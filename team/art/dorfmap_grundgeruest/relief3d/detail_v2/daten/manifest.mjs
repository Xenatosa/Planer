// Loader fuer relief3d/detail_v2/mesh/manifest.json (Schema festgelegt vom Grundgeruest 19.11.2026) [F].
// ESM, Node + Browser. ladeMesh(pfadOderUrl) -> {manifest, kacheln, modelle, gelaende, pruefung}
import { leseGlb, fuegeZusammen } from './glb.mjs';
import { baueGelaende, kachelGrenzen, NX, NY } from './query.mjs';

export const KLASSEN_SOLL = { 0: 'grund', 1: 'weg', 2: 'ufer', 3: 'fels_klippe', 4: 'wasser', 5: 'bruecke' };
const istZahl = (v) => typeof v === 'number' && Number.isFinite(v);
const relPfad = (p) => typeof p === 'string' && p.length > 0 && !p.startsWith('/') && !/^[a-z]+:/i.test(p) && !p.split('/').includes('..');

/** Schemapruefung. Rueckgabe {fehler: [...], vollstaendig: bool (alle 56 Kacheln)}. */
export function pruefeManifest(m) {
  const f = [];
  if (!m || typeof m !== 'object') return { fehler: ['manifest ist kein Objekt'], vollstaendig: false };
  if (m.version !== 1) f.push(`version ${m.version} statt 1`);
  if (m.einheit !== 'm') f.push(`einheit ${m.einheit} statt m`);
  if (m.ursprung !== 'weltecke') f.push(`ursprung ${m.ursprung} statt weltecke`);
  if (!m.karte || m.karte.breite !== NX || m.karte.tiefe !== NY) f.push(`karte ${JSON.stringify(m.karte)} statt {breite:${NX},tiefe:${NY}}`);
  const kl = m.klassen || {};
  if (JSON.stringify(Object.keys(kl).sort()) !== JSON.stringify(Object.keys(KLASSEN_SOLL)) || Object.entries(KLASSEN_SOLL).some(([k, v]) => kl[k] !== v))
    f.push(`klassen ${JSON.stringify(kl)} weichen von ${JSON.stringify(KLASSEN_SOLL)} ab`);
  if (!m.attribute || typeof m.attribute.flaeche !== 'string' || !m.attribute.flaeche) f.push('attribute.flaeche fehlt');
  if (!m.uv || typeof m.uv !== 'object') f.push('uv fehlt');
  if (!Array.isArray(m.kacheln) || !m.kacheln.length) f.push('kacheln leer');
  const ids = new Set();
  for (const [n, k] of (m.kacheln || []).entries()) {
    const w = `kacheln[${n}]`;
    if (!/^[A-H][1-7]$/.test(k.id || '')) { f.push(`${w}: id ${k.id}`); continue; }
    if (ids.has(k.id)) f.push(`${w}: id ${k.id} doppelt`); ids.add(k.id);
    if (!relPfad(k.glb)) f.push(`${w}: glb-Pfad ${k.glb}`);
    const soll = kachelGrenzen(k.id);
    if (!Array.isArray(k.bbox) || k.bbox.length !== 4 || !k.bbox.every(istZahl) || k.bbox.some((v, i) => Math.abs(v - soll[i]) > 1e-6))
      f.push(`${w} ${k.id}: bbox ${JSON.stringify(k.bbox)} statt ${JSON.stringify(soll)}`);
    if (!Number.isInteger(k.dreiecke) || k.dreiecke < 0) f.push(`${w} ${k.id}: dreiecke ${k.dreiecke}`);
    if (k.klassen_anteil !== undefined) {
      const ka = k.klassen_anteil;
      if (typeof ka !== 'object' || Object.keys(ka).some((x) => !(x in KLASSEN_SOLL)) || !Object.values(ka).every(istZahl))
        f.push(`${w} ${k.id}: klassen_anteil ${JSON.stringify(ka)}`);
      else { const s = Object.values(ka).reduce((a, b) => a + b, 0); if (s > 0 && Math.abs(s - 1) > 0.01 && Math.abs(s - 100) > 1) f.push(`${w} ${k.id}: klassen_anteil Summe ${s}`); }
    }
  }
  for (const [n, md] of (m.modelle || []).entries()) {
    if (!md.id || !relPfad(md.glb) || !Number.isInteger(md.klasse) || !(md.klasse in KLASSEN_SOLL)) f.push(`modelle[${n}]: ${JSON.stringify(md)}`);
  }
  return { fehler: f, vollstaendig: ids.size === 56 };
}

async function holer(basis) {
  const node = typeof process !== 'undefined' && !!(process.versions && process.versions.node);
  if (node) {
    const fs = await import('node:fs/promises'), path = await import('node:path');
    return { lies: async (rel) => new Uint8Array(await fs.readFile(path.join(basis, rel))) };
  }
  const b = basis.endsWith('/') ? basis : basis + '/';
  return { lies: async (rel) => { const r = await fetch(new URL(rel, b)); if (!r.ok) throw new Error(`${rel}: HTTP ${r.status}`); return new Uint8Array(await r.arrayBuffer()); } };
}

/**
 * Laedt manifest.json (Node: Dateipfad, Browser: URL), prueft das Schema, liest alle Kachel- und Modell-.glb,
 * prueft dreiecke je Kachel und Klassenreinheit und baut das Gelaende (Kacheln + Bruecken-Deck).
 */
export async function ladeMesh(manifestPfad, { nurKacheln = null } = {}) {
  const node = typeof process !== 'undefined' && !!(process.versions && process.versions.node);
  let basis;
  if (node) { const path = await import('node:path'); basis = path.dirname(manifestPfad); }
  else basis = new URL('.', manifestPfad).href;
  const h = await holer(basis);
  const manifest = JSON.parse(new TextDecoder().decode(await h.lies(node ? (await import('node:path')).basename(manifestPfad) : new URL(manifestPfad).pathname.split('/').pop())));
  const pr = pruefeManifest(manifest);
  if (pr.fehler.length) throw new Error('manifest.json ungueltig: ' + pr.fehler.join('; '));
  const attr = manifest.attribute.flaeche;
  const teile = [], abw = [];
  for (const k of manifest.kacheln) {
    if (nurKacheln && !nurKacheln.includes(k.id)) continue;
    const t = leseGlb(await h.lies(k.glb), attr);
    if (!t.flaechen) throw new Error(`${k.glb}: Attribut ${attr} fehlt`);
    const n = t.indizes.length / 3;
    if (n !== k.dreiecke) abw.push(`${k.id}: ${n} Dreiecke statt ${k.dreiecke}`);
    teile.push(t);
  }
  if (abw.length) throw new Error('manifest.dreiecke passt nicht: ' + abw.join('; '));
  const modelle = [];
  for (const md of manifest.modelle || []) {
    const t = leseGlb(await h.lies(md.glb), attr);
    modelle.push({ id: md.id, klasse: md.klasse, mesh: t });
  }
  const kacheln = fuegeZusammen(teile);
  const gelaende = baueGelaende(kacheln, modelle);
  return { manifest, kacheln, modelle, gelaende, pruefung: { ...pr, gemischte_dreiecke: gelaende.gemischteDreiecke() } };
}
