// Viewer v2 (P3, DETAIL_V2_PLAN.md Abschnitt 9) fuer das Vektor-Mesh detail_v2/mesh/ [S].
// Laufkamera 1,7 m ueber Grund (WASD + Maus/Pointer-Lock, Touch: links laufen, rechts schauen), Orbit ohne 25-m-Grenze,
// ?clay=1 ?wire=1 ?kachelrand=1, Testkamera window.__test. Keine Texturen.
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { LineSegments2 } from 'three/examples/jsm/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/examples/jsm/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/examples/jsm/lines/LineMaterial.js';
import { Boden } from './boden.js';

const T0 = performance.now();
const q = new URLSearchParams(location.search);
const flag = k => q.get(k) === '1';
const AUGE = Number(q.get('auge') || 1.7);              // Augenhoehe ueber Grund in m
const CLAY = flag('clay'), WIRE = flag('wire'), RAND = flag('kachelrand'), MANUAL = flag('manual'), SCHATTEN = q.get('schatten') !== '0';
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

const matGelaende = new THREE.MeshStandardMaterial({ color: CLAY ? 0x9c9c9c : 0xc9cdc4, roughness: 0.95, metalness: 0,
  polygonOffset: WIRE, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
const matWasser = new THREE.MeshStandardMaterial({ color: CLAY ? 0x8f99a0 : 0x4a7f9c, roughness: 0.25, transparent: true, opacity: CLAY ? 0.85 : 0.7, depthWrite: false });
const matSonst = new THREE.MeshStandardMaterial({ color: CLAY ? 0x9c9c9c : 0x8a7f72, roughness: 0.9 });
const rolle = name => /wasser/i.test(name) ? 'wasser' : /^(gelaende|terrain|boden)/i.test(name) || !name ? 'gelaende' : /bruecke|brücke/i.test(name) ? 'bruecke' : /wand/i.test(name) ? 'wand' : 'gelaende';
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
let boden = null, welt = { x: 336, z: 303 };
const blickVektor = (yaw, pitch) => new THREE.Vector3(Math.sin(yaw) * Math.cos(pitch), Math.sin(pitch), -Math.cos(yaw) * Math.cos(pitch));
function setzeLaufKamera() {
  const b = boden ? boden.hoehe(lauf.x, lauf.z, lauf.y ? lauf.y - AUGE : Infinity) : null;
  if (b !== null && b !== undefined) lauf.boden = b; lauf.y = (lauf.boden ?? 0) + AUGE;
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
    lauf.x = THREE.MathUtils.clamp(lauf.x + (Math.sin(lauf.yaw) * vor + Math.cos(lauf.yaw) * seit) * v, 0.01, welt.x - 0.01);
    lauf.z = THREE.MathUtils.clamp(lauf.z + (-Math.cos(lauf.yaw) * vor + Math.sin(lauf.yaw) * seit) * v, 0.01, welt.z - 0.01);
    setzeLaufKamera();
  } else orbit.update();
  folgeSchatten();
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
const render = () => { for (const m of linien) m.resolution.set(innerWidth, innerHeight); renderer.render(scene, camera); test.frames++; };
addEventListener('resize', () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); });

// ---- Laden ----
async function laden() {
  const mUrl = new URL(MESH, location.href); const tM = performance.now();
  const man = await (await fetch(mUrl)).json();
  let liste = Array.isArray(man.kacheln) ? man.kacheln : Object.entries(man.kacheln || {}).map(([id, k]) => ({ id, ...k }));
  liste = liste.map(k => ({ ...k, url: new URL(k.datei || k.file || k.glb || k.uri || `${k.id}.glb`, mUrl).href }));
  if (q.get('kacheln')) { const w = new Set(q.get('kacheln').toUpperCase().split(',')); liste = liste.filter(k => w.has(String(k.id).toUpperCase())); }
  const zusatz = (man.zusatz || []).map(z => ({ ...z, url: new URL(z.datei || z.file || z.uri, mUrl).href }));
  welt = { x: man.welt?.x_m ?? 336, z: man.welt?.z_m ?? 303 };
  const loader = new GLTFLoader(); boden = new Boden(); const root = new THREE.Group(); scene.add(root);
  let fertig = 0, dreiecke = 0, bytes = 0; const tL = performance.now(), jeKachel = {};
  const eine = async (k, istZusatz) => {
    const t = performance.now(); const buf = await (await fetch(k.url)).arrayBuffer(); bytes += buf.byteLength;
    const g = await loader.parseAsync(buf, k.url.replace(/[^/]*$/, ''));
    let n = 0;
    g.scene.traverse(o => { if (!o.isMesh) return; const r = k.rolle || rolle(o.name || o.parent?.name || '');
      o.material = r === 'wasser' ? matWasser : r === 'gelaende' ? matGelaende : matSonst;
      if (!o.geometry.attributes.normal) o.geometry.computeVertexNormals();
      o.castShadow = r !== 'wasser'; o.receiveShadow = true; o.userData.rolle = r; o.userData.kachel = k.id;
      const tri = o.geometry.index ? o.geometry.index.count / 3 : o.geometry.attributes.position.count / 3; n += tri;
      if (r !== 'wasser') boden.add(o);
      if (WIRE) { o.updateMatrixWorld(true); const l = linie(kanten(o), 0x1d1f22, Number(q.get('wirebreite') || 1.6)); l.renderOrder = 2; root.add(l); } });
    root.add(g.scene); dreiecke += n; jeKachel[k.id ?? k.url] = { dreiecke: n, ms: Math.round(performance.now() - t) };
    fertig++; lade.textContent = `Lade Kacheln … ${fertig}/${liste.length + zusatz.length}`;
  };
  const warte = [...liste.map(k => [k, false]), ...zusatz.map(z => [z, true])]; const N = Number(q.get('parallel') || 6);
  await Promise.all(Array.from({ length: N }, async () => { while (warte.length) { const [k, z] = warte.shift(); await eine(k, z); } }));
  boden.fertig();
  if (RAND) {   // Kachelraster einmal global: Schnittlinien aus dem Manifest bzw. aus den bounds
    const xs = man.kachelschema?.schnitt_x || [...new Set(liste.flatMap(k => k.bounds ? [k.bounds[0], k.bounds[2]] : []))].sort((a, b) => a - b);
    const zs = man.kachelschema?.schnitt_z || [...new Set(liste.flatMap(k => k.bounds ? [k.bounds[1], k.bounds[3]] : []))].sort((a, b) => a - b);
    if (xs.length && zs.length) root.add(kachelRaster(xs, zs));
  }
  const tR = performance.now();
  const st = q.get('start')?.split(',').map(Number); if (st?.length >= 2) { lauf.x = st[0]; lauf.z = st[1]; lauf.yaw = THREE.MathUtils.degToRad(st[2] || 0); }
  if (modus === 'orbit') { lauf.y = 0; setzeLaufKamera(); camera.position.set(lauf.x, (lauf.boden ?? 0) + 60, lauf.z + 60); orbit.target.set(lauf.x, lauf.boden ?? 0, lauf.z); orbit.enabled = true; orbit.update(); }
  else setzeLaufKamera();
  folgeSchatten(); render();
  const ladezeit = { gesamt_ms: Math.round(performance.now() - T0), manifest_ms: Math.round(tL - tM), kacheln_ms: Math.round(tR - tL),
    bodenindex_ms: boden.ms, erstes_bild_ms: Math.round(performance.now() - tR) };
  Object.assign(test, { ladezeit, kacheln: liste.length, zusatz: zusatz.length, dreiecke, bytes, jeKachel, manifest: man });
  lade.style.display = 'none';
  hud.textContent = `Viewer v2 · ${liste.length} Kacheln · ${(dreiecke / 1e6).toFixed(2)} Mio. Dreiecke · ${(bytes / 1e6).toFixed(1)} MB · geladen in ${(ladezeit.gesamt_ms / 1000).toFixed(2)} s`
    + `\n${CLAY ? 'Clay · ' : ''}${WIRE ? 'Wire · ' : ''}${RAND ? 'Kachelrand · ' : ''}O = Laufen/Orbit · WASD + Maus (Klick = Maus fangen) · Shift = schnell`;
  log('bereit', JSON.stringify({ ladezeit, kacheln: liste.length, dreiecke, bytes }));
  test.bereit = true; document.documentElement.dataset.bereit = '1';
  if (!MANUAL) { let t = performance.now(); renderer.setAnimationLoop(() => { const n = performance.now(); schritt(Math.min(0.1, (n - t) / 1000)); t = n; render(); }); }
}
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
  zustand: () => ({ modus, pos: camera.position.toArray(), boden: modus === 'lauf' ? lauf.boden : null,
    blick: THREE.MathUtils.radToDeg(lauf.yaw), abstand: modus === 'orbit' ? camera.position.distanceTo(orbit.target) : null,
    minDistance: orbit.minDistance, ueber_grund: modus === 'lauf' ? lauf.y - lauf.boden : camera.position.y - (boden?.hoehe(camera.position.x, camera.position.z) ?? 0) }),
  schatten: () => ({ ...schattenInfo, castShadow: sonne.castShadow }),
  schritt: dt => { schritt(dt); render(); return test.zustand(); },
  render, stopRender: () => renderer.setAnimationLoop(null),
  info: () => ({ ladezeit: test.ladezeit, kacheln: test.kacheln, dreiecke: test.dreiecke, bytes: test.bytes, modus, clay: CLAY, wire: WIRE, kachelrand: RAND, linien: linien.length }),
});
laden().catch(e => { test.fehler = String(e && e.stack || e); lade.textContent = 'Fehler: ' + e; console.error('[dv2] Ladefehler', e); });
