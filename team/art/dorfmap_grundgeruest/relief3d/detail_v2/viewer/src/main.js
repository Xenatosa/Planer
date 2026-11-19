// Viewer v2 (P3, DETAIL_V2_PLAN.md Abschnitt 9) fuer das Vektor-Mesh detail_v2/mesh/ [S].
// Laufkamera 1,7 m ueber Grund (WASD + Maus/Pointer-Lock, Touch: links laufen, rechts schauen), Orbit ohne 25-m-Grenze,
// ?clay=1 ?wire=1 ?kachelrand=1, Testkamera window.__test. Keine Texturen.
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { LineSegments2 } from 'three/examples/jsm/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/examples/jsm/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/examples/jsm/lines/LineMaterial.js';
import { Boden, begehbar, MAX_NEIGUNG } from './boden.js';

const T0 = performance.now();
const q = new URLSearchParams(location.search);
const flag = k => q.get(k) === '1';
const AUGE = Number(q.get('auge') || 1.7);              // Augenhoehe ueber Grund in m
const KLASSEN = flag('klassen'), CLAY = flag('clay') && !KLASSEN, WIRE = flag('wire'), RAND = flag('kachelrand'), MANUAL = flag('manual'), SCHATTEN = q.get('schatten') !== '0';
const MESH = q.get('mesh') || '../mesh/manifest.json';
const hud = document.getElementById('hud'), lade = document.getElementById('lade');
if (q.get('hud') === '0') { hud.style.display = 'none'; document.getElementById('knopf').style.display = 'none'; }
const log = (...a) => console.log('[dv2]', ...a);
const test = window.__test = { bereit: false, fehler: null, frames: 0 };
window.addEventListener('error', e => { test.fehler = String(e.message || e); });

const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); renderer.setSize(innerWidth, innerHeight);
renderer.shadowMap.enabled = SCHATTEN; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene(); scene.background = new THREE.Color(0xb8c7d2);
const camera = new THREE.PerspectiveCamera(Number(q.get('fov') || 60), innerWidth / innerHeight, 0.05, 2500);
scene.add(new THREE.HemisphereLight(0xe2edf6, 0x6d675c, Number(q.get("himmel") || 0.9)));
const sonne = new THREE.DirectionalLight(0xfff2dc, Number(q.get("sonne") || 2.8));
const SONNE_DIR = new THREE.Vector3().setFromSphericalCoords(1, THREE.MathUtils.degToRad(90 - Number(q.get("sonnenhoehe") || 32)), THREE.MathUtils.degToRad(Number(q.get("sonnenazimut") || 315)));
sonne.castShadow = SCHATTEN; sonne.shadow.mapSize.set(2048, 2048); sonne.shadow.bias = -0.0004; sonne.shadow.normalBias = 0.04;
sonne.shadow.camera.near = 1; sonne.shadow.camera.far = 800; scene.add(sonne, sonne.target);

// Klassen (verbindlich): 0 grund, 1 weg, 2 ufer, 3 fels_klippe, 4 wasser, 5 bruecke. Farben wie detail_v2/daten/legende.json (P4), nur Debug.
const KLASSEN_NAMEN = ['grund', 'weg', 'ufer', 'fels_klippe', 'wasser', 'bruecke'];
const FARBE_DEBUG = ['#c8d8b0', '#b08a5a', '#d8c890', '#7a7a80', '#3a78c8', '#8a4a20'].map(c => new THREE.Color(c));
const FARBE_STD = FARBE_DEBUG.map((c, k) => new THREE.Color(0xc9cdc4).lerp(c, [0.25, 0.45, 0.35, 0.35, 0.75, 0.6][k]));
const FARBE_OHNE = new THREE.Color(0xc9cdc4);
const matGelaende = new THREE.MeshStandardMaterial({ color: CLAY ? 0x9c9c9c : 0xffffff, vertexColors: !CLAY, roughness: 0.95, metalness: 0,
  polygonOffset: WIRE, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
function faerbe(geo, klasseFest) {   // Vertexfarben aus _FLAECHE (keine Texturen)
  if (CLAY) return; const P = geo.attributes.position, F = geo.attributes._flaeche, C = new Float32Array(P.count * 3), pal = KLASSEN ? FARBE_DEBUG : FARBE_STD;
  for (let i = 0; i < P.count; i++) { const k = F ? Math.round(F.getX(i)) : klasseFest; const c = pal[k] || FARBE_OHNE; C[i * 3] = c.r; C[i * 3 + 1] = c.g; C[i * 3 + 2] = c.b; }
  geo.setAttribute('color', new THREE.BufferAttribute(C, 3));
}
const matWasser = new THREE.MeshStandardMaterial({ color: CLAY ? 0x8f99a0 : 0x4a7f9c, roughness: 0.25, transparent: true, opacity: CLAY ? 0.85 : 0.7, depthWrite: false });
const matSonst = new THREE.MeshStandardMaterial({ color: CLAY ? 0x9c9c9c : 0x8a7f72, roughness: 0.9 });
const klasseAusName = name => /wasser/i.test(name) ? 4 : /bruecke|brücke/i.test(name) ? 5 : null;   // nur Altformat ohne _FLAECHE
const linien = [];
const linie = (pos, farbe, breite) => {
  const g = new LineSegmentsGeometry(); g.setPositions(pos);
  const m = new LineMaterial({ color: farbe, linewidth: breite, worldUnits: false }); m.resolution.set(innerWidth, innerHeight);
  const l = new LineSegments2(g, m); l.computeLineDistances(); linien.push(m); return l;
};

// ---- Steuerung ----
const orbit = new OrbitControls(camera, renderer.domElement);
orbit.enableDamping = true; orbit.dampingFactor = 0.1; orbit.minDistance = 0.3; orbit.maxDistance = 1500;   // keine 25-m-Grenze (P3)
orbit.maxPolarAngle = Math.PI / 2 - 0.02; orbit.screenSpacePanning = true; orbit.enabled = false;
const lauf = { x: 209, z: 118, yaw: 0, pitch: -0.05, y: 0 };            // yaw 0 = Blick nach Norden (-z)
let modus = q.get('modus') === 'orbit' ? 'orbit' : 'lauf';
const tasten = new Set(), stick = { x: 0, y: 0 }, blickDelta = { x: 0, y: 0 };
let boden = null, query = null, welt = { x: 336, z: 303 }, gesperrt = 0;
const blickVektor = (yaw, pitch) => new THREE.Vector3(Math.sin(yaw) * Math.cos(pitch), Math.sin(pitch), -Math.cos(yaw) * Math.cos(pitch));
const bodenRef = () => lauf.y ? lauf.y - AUGE : Infinity;
function trefferBei(x, z, yMax) {   // Strahl + Begehbarkeit; queryPoint (P4) ueberstimmt begehbar, falls dessen Maske geladen ist
  const t = boden?.treffer(x, z, yMax); if (!t) return null;
  t.begehbar = begehbar(t); t.quelle = 'mesh';
  if (query) { try { const qp = query.queryPoint(x, z); t.query = qp; if (qp && typeof qp.begehbar === 'boolean' && t.klasse !== 5) { t.begehbar = qp.begehbar; t.quelle = 'queryPoint'; } } catch (e) { /* ausserhalb */ } }
  return t;
}
function setzeLaufKamera() {
  const t = trefferBei(lauf.x, lauf.z, bodenRef());
  if (t) { lauf.boden = t.y; lauf.treffer = t; } lauf.y = (lauf.boden ?? 0) + AUGE;
  camera.position.set(lauf.x, lauf.y, lauf.z); camera.lookAt(camera.position.clone().add(blickVektor(lauf.yaw, lauf.pitch)));
}
function setzeModus(m) {
  if (m === modus) return;
  if (m === 'orbit') { const v = blickVektor(lauf.yaw, 0).multiplyScalar(10); const t = new THREE.Vector3(lauf.x + v.x, 0, lauf.z + v.z);
    t.y = boden?.hoehe(t.x, t.z) ?? lauf.boden ?? 0; orbit.target.copy(t); orbit.update(); }
  else { lauf.x = THREE.MathUtils.clamp(camera.position.x, 0, welt.x); lauf.z = THREE.MathUtils.clamp(camera.position.z, 0, welt.z);
    const d = new THREE.Vector3(); camera.getWorldDirection(d); lauf.yaw = Math.atan2(d.x, -d.z); lauf.pitch = 0; lauf.y = 0; }
  if (m === 'orbit' && document.pointerLockElement) document.exitPointerLock();
  modus = m; orbit.enabled = m === 'orbit'; document.getElementById('knopf').textContent = m === 'lauf' ? 'Orbit (O)' : 'Laufen (O)';
}
addEventListener('keydown', e => { tasten.add(e.code); if (e.code === 'KeyO') setzeModus(modus === 'lauf' ? 'orbit' : 'lauf'); });
addEventListener('keyup', e => tasten.delete(e.code)); addEventListener('blur', () => tasten.clear());
document.getElementById('knopf').addEventListener('click', e => { e.stopPropagation(); setzeModus(modus === 'lauf' ? 'orbit' : 'lauf'); });
const cv = renderer.domElement; let ziehen = false;
cv.addEventListener('click', () => { if (modus === 'lauf' && !matchMedia('(pointer: coarse)').matches && cv.requestPointerLock) cv.requestPointerLock(); });
cv.addEventListener('mousedown', () => { ziehen = true; }); addEventListener('mouseup', () => { ziehen = false; });
let sperrSprung = 0;   // Chrome liefert direkt nach dem Pointer-Lock einen Sprung in movementX/Y -> verwerfen
document.addEventListener('pointerlockchange', () => { sperrSprung = 2; });
addEventListener('mousemove', e => { if (modus !== 'lauf') return; if (sperrSprung > 0) { sperrSprung--; return; }
  if (Math.abs(e.movementX) > 250 || Math.abs(e.movementY) > 250) return;
  if (document.pointerLockElement === cv || ziehen) { blickDelta.x += e.movementX; blickDelta.y += e.movementY; } });
// Touch: linke Haelfte = Stick (laufen), rechte Haelfte = schauen
const touches = new Map(), stickEl = document.getElementById('stick');
cv.addEventListener('touchstart', e => { if (modus !== 'lauf') return; e.preventDefault();
  for (const t of e.changedTouches) { const links = t.clientX < innerWidth / 2; touches.set(t.identifier, { links, x0: t.clientX, y0: t.clientY, x: t.clientX, y: t.clientY });
    if (links) { stickEl.style.display = 'block'; stickEl.style.left = (t.clientX - 50) + 'px'; stickEl.style.top = (t.clientY - 50) + 'px'; } } }, { passive: false });
cv.addEventListener('touchmove', e => { if (modus !== 'lauf') return; e.preventDefault();
  for (const t of e.changedTouches) { const s = touches.get(t.identifier); if (!s) continue;
    if (s.links) { const dx = t.clientX - s.x0, dy = t.clientY - s.y0, r = Math.min(1, Math.hypot(dx, dy) / 60), a = Math.atan2(dy, dx); stick.x = Math.cos(a) * r; stick.y = Math.sin(a) * r; }
    else { blickDelta.x += (t.clientX - s.x) * 1.6; blickDelta.y += (t.clientY - s.y) * 1.6; }
    s.x = t.clientX; s.y = t.clientY; } }, { passive: false });
const touchEnde = e => { for (const t of e.changedTouches) { const s = touches.get(t.identifier); if (s?.links) { stick.x = stick.y = 0; stickEl.style.display = 'none'; } touches.delete(t.identifier); } };
cv.addEventListener('touchend', touchEnde); cv.addEventListener('touchcancel', touchEnde);

function schritt(dt) {
  if (modus === 'lauf') {
    lauf.yaw += blickDelta.x * 0.0022; lauf.pitch = THREE.MathUtils.clamp(lauf.pitch - blickDelta.y * 0.0022, -1.45, 1.45); blickDelta.x = blickDelta.y = 0;
    let vor = (tasten.has('KeyW') || tasten.has('ArrowUp') ? 1 : 0) - (tasten.has('KeyS') || tasten.has('ArrowDown') ? 1 : 0) - stick.y;
    let seit = (tasten.has('KeyD') || tasten.has('ArrowRight') ? 1 : 0) - (tasten.has('KeyA') || tasten.has('ArrowLeft') ? 1 : 0) + stick.x;
    const l = Math.hypot(vor, seit); if (l > 1) { vor /= l; seit /= l; }
    const v = (tasten.has('ShiftLeft') || tasten.has('ShiftRight') ? 7 : 3) * dt;
    const dx = (Math.sin(lauf.yaw) * vor + Math.cos(lauf.yaw) * seit) * v, dz = (-Math.cos(lauf.yaw) * vor + Math.sin(lauf.yaw) * seit) * v;
    if (dx || dz) bewege(dx, dz);
    setzeLaufKamera();
  } else orbit.update();
  folgeSchatten();
}
// Begehbarkeit: Klasse 3/4 oder Neigung > 35 Grad nicht betretbar, Bruecke (5) begehbar. In 0,25-m-Teilschritten,
// an der Grenze wird entlang der freien Achse gerutscht. Steht man (per __test.lauf) schon auf Gesperrtem, darf man heraus.
function bewege(dx, dz) {
  const n = Math.max(1, Math.ceil(Math.hypot(dx, dz) / 0.25)), sx = dx / n, sz = dz / n;
  const frei = (x, z) => { const t = trefferBei(x, z, bodenRef()); return t && t.begehbar; };
  const hier = frei(lauf.x, lauf.z);
  for (let i = 0; i < n; i++) {
    const kl = (v, m) => THREE.MathUtils.clamp(v, 0.01, m - 0.01), nx = kl(lauf.x + sx, welt.x), nz = kl(lauf.z + sz, welt.z);
    if (!hier || frei(nx, nz)) { lauf.x = nx; lauf.z = nz; }
    else if (frei(nx, lauf.z)) { lauf.x = nx; gesperrt++; } else if (frei(lauf.x, nz)) { lauf.z = nz; gesperrt++; } else { gesperrt++; break; }
    const t = trefferBei(lauf.x, lauf.z, bodenRef()); if (t) { lauf.boden = t.y; lauf.y = t.y + AUGE; }
  }
}
// Schattenkarte folgt der Kamera: Mitte = Laufposition bzw. Orbit-Ziel, Groesse nach Abstand, auf Texel gerastert.
const schattenInfo = { mitte: [0, 0, 0], halb: 0 };
function folgeSchatten() {
  const m = modus === 'lauf' ? new THREE.Vector3(lauf.x, lauf.boden ?? 0, lauf.z).add(blickVektor(lauf.yaw, 0).multiplyScalar(12)) : orbit.target.clone();
  const S = modus === 'lauf' ? 40 : THREE.MathUtils.clamp(camera.position.distanceTo(orbit.target) * 1.3, 30, 260);
  const tex = 2 * S / sonne.shadow.mapSize.x; m.x = Math.round(m.x / tex) * tex; m.z = Math.round(m.z / tex) * tex;
  const c = sonne.shadow.camera; if (c.right !== S) { c.left = c.bottom = -S; c.right = c.top = S; c.updateProjectionMatrix(); }
  sonne.target.position.copy(m); sonne.position.copy(m).addScaledVector(SONNE_DIR, 300); sonne.target.updateMatrixWorld();
  schattenInfo.mitte = [m.x, m.y, m.z]; schattenInfo.halb = S;
}
const render = () => { for (const m of linien) m.resolution.set(innerWidth, innerHeight); renderer.render(scene, camera); test.frames++; if (MANUAL && test.bereit) zeigeHud(); };
addEventListener('resize', () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); });

// ---- Laden ----
// Verbindliches Format (Grundgeruest 19.11.2026): {version:1, einheit:"m", ursprung:"weltecke", karte:{breite,tiefe}, klassen, attribute:{flaeche:"_FLAECHE"},
// uv, kacheln:[{id, glb, bbox, dreiecke, klassen_anteil}], modelle:[{id, glb, klasse}]}. Pfade relativ zum Manifest. Altfelder werden toleriert.
function pruefeManifest(m) {
  const w = [], ist = (b, t) => { if (!b) w.push(t); };
  ist(m.version === 1, 'version != 1'); ist(m.einheit === 'm', 'einheit != "m"'); ist(m.ursprung === 'weltecke', 'ursprung != "weltecke"');
  ist(m.karte && m.karte.breite === 336 && m.karte.tiefe === 303, 'karte != {breite:336,tiefe:303}');
  ist(m.klassen && KLASSEN_NAMEN.every((n, k) => m.klassen[k] === n || m.klassen[String(k)] === n), 'klassen != 0 grund..5 bruecke');
  ist(m.attribute && m.attribute.flaeche === '_FLAECHE', 'attribute.flaeche != "_FLAECHE"');
  ist(m.uv && m.uv.TEXCOORD_0 === 'welt_xz_m' && m.uv.TEXCOORD_1 === 'karte_norm', 'uv TEXCOORD_0/1 fehlt');
  ist(Array.isArray(m.kacheln) && m.kacheln.length > 0, 'kacheln keine Liste');
  for (const k of Array.isArray(m.kacheln) ? m.kacheln : []) {
    ist(typeof k.id === 'string' && typeof k.glb === 'string', `kachel ${k.id}: id/glb fehlt`);
    ist(Array.isArray(k.bbox) && k.bbox.length === 4, `kachel ${k.id}: bbox fehlt`);
    ist(Number.isInteger(k.dreiecke) && k.dreiecke <= 60000, `kachel ${k.id}: dreiecke fehlt/> 60000`);
    ist(k.klassen_anteil && typeof k.klassen_anteil === 'object', `kachel ${k.id}: klassen_anteil fehlt`); }
  ist(Array.isArray(m.modelle), 'modelle keine Liste');
  for (const o of Array.isArray(m.modelle) ? m.modelle : []) ist(typeof o.id === 'string' && typeof o.glb === 'string' && Number.isInteger(o.klasse), `modell ${o.id}: id/glb/klasse fehlt`);
  return w;
}
async function laden() {
  const mUrl = new URL(MESH, location.href); const tM = performance.now();
  const man = await (await fetch(mUrl)).json();
  const formatWarnungen = pruefeManifest(man); if (formatWarnungen.length) console.warn('[dv2] Manifest weicht vom verbindlichen Format ab:', formatWarnungen.join('; '));
  let liste = Array.isArray(man.kacheln) ? man.kacheln : Object.entries(man.kacheln || {}).map(([id, k]) => ({ id, ...k }));
  liste = liste.map(k => ({ ...k, bbox: k.bbox || k.bounds, url: new URL(k.glb || k.datei || k.file || k.uri || `${k.id}.glb`, mUrl).href }));
  if (q.get('kacheln')) { const w = new Set(q.get('kacheln').toUpperCase().split(',')); liste = liste.filter(k => w.has(String(k.id).toUpperCase())); }
  const modelle = [...(man.modelle || []), ...(man.zusatz || [])].map(z => ({ ...z, url: new URL(z.glb || z.datei || z.file || z.uri, mUrl).href,
    klasse: Number.isInteger(z.klasse) ? z.klasse : z.rolle === 'bruecke' ? 5 : z.rolle === 'wasser' ? 4 : null }));
  welt = { x: man.karte?.breite ?? man.welt?.x_m ?? 336, z: man.karte?.tiefe ?? man.welt?.z_m ?? 303 };
  const loader = new GLTFLoader(); boden = new Boden(); const root = new THREE.Group(); scene.add(root);
  let fertig = 0, dreiecke = 0, bytes = 0, mitFlaeche = 0, ohneFlaeche = 0; const tL = performance.now(), jeKachel = {};
  const eine = async (k, istModell) => {
    const t = performance.now(); const r = await fetch(k.url); if (!r.ok) throw new Error(`${k.url}: HTTP ${r.status}`);
    const buf = await r.arrayBuffer(); bytes += buf.byteLength;
    const g = await loader.parseAsync(buf, k.url.replace(/[^/]*$/, ''));
    let n = 0;
    g.scene.traverse(o => { if (!o.isMesh) return;
      const fest = istModell ? k.klasse : klasseAusName(o.name || o.parent?.name || '');
      if (o.geometry.attributes._flaeche) mitFlaeche++; else ohneFlaeche++;
      if (!o.geometry.attributes.normal) o.geometry.computeVertexNormals();
      faerbe(o.geometry, fest); o.material = matGelaende;
      o.castShadow = true; o.receiveShadow = true; o.userData.kachel = k.id; o.userData.modell = istModell;
      n += o.geometry.index ? o.geometry.index.count / 3 : o.geometry.attributes.position.count / 3;
      boden.add(o, fest);
      if (WIRE) { o.updateMatrixWorld(true); const l = linie(kanten(o), 0x1d1f22, Number(q.get('wirebreite') || 1.6)); l.renderOrder = 2; root.add(l); } });
    root.add(g.scene); dreiecke += n; jeKachel[k.id ?? k.url] = { dreiecke: n, ms: Math.round(performance.now() - t), modell: istModell };
    fertig++; lade.textContent = `Lade Kacheln … ${fertig}/${liste.length + modelle.length}`;
  };
  const warte = [...liste.map(k => [k, false]), ...modelle.map(z => [z, true])]; const N = Number(q.get('parallel') || 6);
  await Promise.all(Array.from({ length: N }, async () => { while (warte.length) { const [k, z] = warte.shift(); await eine(k, z); } }));
  boden.fertig();
  if (RAND) {   // Kachelraster einmal global: Schnittlinien aus den bbox (Altformat: kachelschema)
    const xs = [...new Set(liste.flatMap(k => k.bbox ? [k.bbox[0], k.bbox[2]] : []))].sort((a, b) => a - b);
    const zs = [...new Set(liste.flatMap(k => k.bbox ? [k.bbox[1], k.bbox[3]] : []))].sort((a, b) => a - b);
    const X = xs.length ? xs : man.kachelschema?.schnitt_x || [], Z = zs.length ? zs : man.kachelschema?.schnitt_z || [];
    if (X.length && Z.length) root.add(kachelRaster(X, Z));
  }
  const tQ = performance.now();
  if (q.get('query')) {   // optional queryPoint aus detail_v2/daten/query.mjs (P4): ?query=1 -> ../daten/, sonst URL des Ordners
    const basis = new URL(q.get('query') === '1' ? '../daten/' : q.get('query').replace(/\/?$/, '/'), location.href).href;
    try { const mod = await import(/* @vite-ignore */ basis + 'query.mjs'); query = await mod.ladeDatenschicht(basis, {});
      test.query = { basis, quellen: query.quellen() }; log('queryPoint geladen', JSON.stringify(test.query));
    } catch (e) { test.query = { basis, fehler: String(e) }; console.warn('[dv2] queryPoint nicht geladen, nur Strahl:', String(e)); }
  }
  const tR = performance.now();
  const st = q.get('start')?.split(',').map(Number); if (st?.length >= 2) { lauf.x = st[0]; lauf.z = st[1]; lauf.yaw = THREE.MathUtils.degToRad(st[2] || 0); }
  if (modus === 'orbit') { lauf.y = 0; setzeLaufKamera(); camera.position.set(lauf.x, (lauf.boden ?? 0) + 60, lauf.z + 60); orbit.target.set(lauf.x, lauf.boden ?? 0, lauf.z); orbit.enabled = true; orbit.update(); }
  else setzeLaufKamera();
  folgeSchatten(); render();
  const ladezeit = { gesamt_ms: Math.round(performance.now() - T0), manifest_ms: Math.round(tL - tM), kacheln_ms: Math.round(tQ - tL),
    bodenindex_ms: boden.ms, query_ms: Math.round(tR - tQ), erstes_bild_ms: Math.round(performance.now() - tR) };
  const klassen = { je_klasse: Object.fromEntries(KLASSEN_NAMEN.map((n, k) => [n, boden.jeKlasse[k]])), gemischt: boden.gemischt, ohne_klasse: boden.ohneKlasse,
    meshes_mit_flaeche: mitFlaeche, meshes_ohne_flaeche: ohneFlaeche };
  Object.assign(test, { ladezeit, kacheln: liste.length, modelle: modelle.length, dreiecke, bytes, jeKachel, manifest: man, formatWarnungen, klassen });
  lade.style.display = 'none';
  hudText = `Viewer v2 · ${liste.length} Kacheln + ${modelle.length} Modelle · ${(dreiecke / 1e6).toFixed(2)} Mio. Dreiecke · ${(bytes / 1e6).toFixed(1)} MB · geladen in ${(ladezeit.gesamt_ms / 1000).toFixed(2)} s`
    + (formatWarnungen.length ? ` · Format: ${formatWarnungen.length} Abweichung(en)` : '')
    + `\n${CLAY ? 'Clay · ' : ''}${KLASSEN ? 'Klassen · ' : ''}${WIRE ? 'Wire · ' : ''}${RAND ? 'Kachelrand · ' : ''}${query ? 'queryPoint · ' : ''}O = Laufen/Orbit · WASD + Maus (Klick = Maus fangen) · Shift = schnell`
    + (KLASSEN ? '\n' + KLASSEN_NAMEN.map((n, k) => `${k} ${n}`).join(' · ') : '');
  log('bereit', JSON.stringify({ ladezeit, kacheln: liste.length, modelle: modelle.length, dreiecke, bytes, formatWarnungen: formatWarnungen.length, klassen }));
  test.bereit = true; document.documentElement.dataset.bereit = '1';
  if (!MANUAL) { let t = performance.now(), hudT = 0; renderer.setAnimationLoop(() => { const n = performance.now(); schritt(Math.min(0.1, (n - t) / 1000)); t = n; render();
    if (n - hudT > 250) { hudT = n; zeigeHud(); } }); } else zeigeHud();
}
let hudText = '';
function zeigeHud() { const t = modus === 'lauf' ? lauf.treffer : null;
  hud.textContent = hudText + (t ? `\nBoden ${t.y.toFixed(2)} m · ${t.klasse !== null ? KLASSEN_NAMEN[t.klasse] : 'ohne Klasse'} · ${t.neigung.toFixed(0)}° · ${t.begehbar ? 'begehbar' : 'gesperrt'} (${t.quelle})` : ''); }
function kanten(o) {   // eindeutige Dreieckskanten in Weltkoordinaten (Wireframe mit dicken Linien)
  const g = o.geometry, P = g.attributes.position, I = g.index ? g.index.array : Array.from({ length: P.count }, (_, i) => i), seen = new Set(), out = [];
  const v = new THREE.Vector3(), w = new THREE.Vector3();
  for (let t = 0; t < I.length; t += 3) for (const [a, b] of [[I[t], I[t + 1]], [I[t + 1], I[t + 2]], [I[t + 2], I[t]]]) {
    const k = a < b ? a * 4294967296 + b : b * 4294967296 + a; if (seen.has(k)) continue; seen.add(k);
    v.fromBufferAttribute(P, a).applyMatrix4(o.matrixWorld); w.fromBufferAttribute(P, b).applyMatrix4(o.matrixWorld); out.push(v.x, v.y + 0.005, v.z, w.x, w.y + 0.005, w.z); }
  return out;
}
function kachelRaster(xs, zs) {   // Kachelgrenzen auf dem Gelaende (Hoehe per Bodenstrahl, 0,5-m-Schritte), 0,1 m angehoben
  const pkt = [], st = 0.5, h = (x, z) => (boden.hoehe(Math.min(Math.max(x, 0.001), welt.x - 0.001), Math.min(Math.max(z, 0.001), welt.z - 0.001)) ?? 0) + 0.1;
  const z0 = zs[0], z1 = zs[zs.length - 1], x0 = xs[0], x1 = xs[xs.length - 1];
  for (const x of xs) for (let z = z0; z < z1; z += st) { const zb = Math.min(z + st, z1); pkt.push(x, h(x, z), z, x, h(x, zb), zb); }
  for (const z of zs) for (let x = x0; x < x1; x += st) { const xb = Math.min(x + st, x1); pkt.push(x, h(x, z), z, xb, h(xb, z), z); }
  const l = linie(pkt, 0xffd21f, 2.5); l.renderOrder = 3; return l;
}

// ---- Test-API ----
Object.assign(test, {
  kam: (p, t) => { setzeModus('orbit'); camera.position.set(...p); orbit.target.set(...t); orbit.update(); folgeSchatten(); render(); return test.zustand(); },
  lauf: (x, z, blick = 0, neigung = 0) => { setzeModus('lauf'); Object.assign(lauf, { x, z, yaw: THREE.MathUtils.degToRad(blick), pitch: THREE.MathUtils.degToRad(neigung), y: 0 });
    setzeLaufKamera(); folgeSchatten(); render(); return test.zustand(); },
  boden: (x, z, yMax) => boden?.hoehe(x, z, yMax) ?? null,
  treffer: (x, z, yMax) => { const t = trefferBei(x, z, yMax); if (!t) return null; const { query: qp, ...r } = t; return { ...r, klassenname: t.klasse !== null ? KLASSEN_NAMEN[t.klasse] : null, kachel: qp?.kachel ?? null }; },
  gesperrt: () => gesperrt, maxNeigung: MAX_NEIGUNG,
  zustand: () => ({ modus, pos: camera.position.toArray(), boden: modus === 'lauf' ? lauf.boden : null,
    blick: THREE.MathUtils.radToDeg(lauf.yaw), abstand: modus === 'orbit' ? camera.position.distanceTo(orbit.target) : null,
    minDistance: orbit.minDistance, klasse: modus === 'lauf' ? lauf.treffer?.klasse ?? null : null, begehbar: modus === 'lauf' ? lauf.treffer?.begehbar ?? null : null, ueber_grund: modus === 'lauf' ? lauf.y - lauf.boden : camera.position.y - (boden?.hoehe(camera.position.x, camera.position.z) ?? 0) }),
  schatten: () => ({ ...schattenInfo, castShadow: sonne.castShadow }),
  schritt: dt => { schritt(dt); render(); return test.zustand(); },
  render, stopRender: () => renderer.setAnimationLoop(null),
  info: () => ({ ladezeit: test.ladezeit, kacheln: test.kacheln, modelle: test.modelle, klassen: test.klassen, formatWarnungen: test.formatWarnungen, query: test.query ?? null, klassenFarben: KLASSEN, dreiecke: test.dreiecke, bytes: test.bytes, modus, clay: CLAY, wire: WIRE, kachelrand: RAND, linien: linien.length }),
});
laden().catch(e => { test.fehler = String(e && e.stack || e); lade.textContent = 'Fehler: ' + e; console.error('[dv2] Ladefehler', e); });
