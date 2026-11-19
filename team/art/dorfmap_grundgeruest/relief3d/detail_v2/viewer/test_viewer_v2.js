// Playwright-Test Viewer v2 (P3) [S]. HeadlessChrome/SwiftShader, eigener statischer Server (file:// kann keine .glb holen).
// Aufruf (im Ordner relief3d):  NODE_DIR=/tmp/dv2_viewer/node node detail_v2/viewer/test_viewer_v2.js
//   MESH_DIR = Ordner mit manifest.json (Standard: /tmp/dv2_viewer/dummy_mesh, wird bei Bedarf mit dummy/erzeuge_dummy.py erzeugt)
//   BILDER   = Ausgabeordner fuer die Nachweisbilder (Standard /tmp/dv2_viewer/bilder)
//   START    = x,z,blick fuer die Nachweisbilder (Standard Dorfkern 209,118,200)
//   DATEN_DIR = Ordner mit query.mjs/png.mjs/... aus detail_v2/daten (P4, PR #52) fuer den optionalen queryPoint-Test (sonst uebersprungen)
const path = require('path'), fs = require('fs'), http = require('http'), zlib = require('zlib'), { execFileSync } = require('child_process');
const NODE_DIR = process.env.NODE_DIR || '/tmp/dv2_viewer/node';
const { chromium } = require(path.join(NODE_DIR, 'node_modules', 'playwright'));
const R3D = path.resolve(__dirname, '..', '..');
const MESH_DIR = path.resolve(process.env.MESH_DIR || '/tmp/dv2_viewer/dummy_mesh');
const BILDER = process.env.BILDER || '/tmp/dv2_viewer/bilder';
const [SX, SZ, SB] = (process.env.START || '209,118,200').split(',').map(Number);
const DATEN_DIR = process.env.DATEN_DIR ? path.resolve(process.env.DATEN_DIR) : null;
if (!fs.existsSync(path.join(MESH_DIR, 'manifest.json')))
  execFileSync('python3', [path.join(__dirname, 'dummy', 'erzeuge_dummy.py'), '--out', MESH_DIR], { stdio: 'inherit' });
fs.mkdirSync(BILDER, { recursive: true });
const TYP = { '.mjs': 'text/javascript', '.png': 'image/png', '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.glb': 'model/gltf-binary' };
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0]);
  const f = u.startsWith('/__mesh__/') ? path.join(MESH_DIR, u.slice(10)) : DATEN_DIR && u.startsWith('/__daten__/') ? path.join(DATEN_DIR, u.slice(11)) : path.join(R3D, u);
  if (!f.startsWith(R3D) && !f.startsWith(MESH_DIR) && !(DATEN_DIR && f.startsWith(DATEN_DIR))) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': TYP[path.extname(f)] || 'application/octet-stream' }); res.end(d); });
});
const erg = []; let rot = 0;
const pruef = (name, ok, wert) => { erg.push({ name, ok: !!ok, wert }); if (!ok) rot++; console.log(`${ok ? 'OK  ' : 'ROT '} ${name}${wert !== undefined ? ' · ' + JSON.stringify(wert) : ''}`); };
const man = JSON.parse(fs.readFileSync(path.join(MESH_DIR, 'manifest.json')));
const istDummy = /DUMMY/.test(man.quelle || '');
const KN = ['grund', 'weg', 'ufer', 'fels_klippe', 'wasser', 'bruecke'];
// glb lesen (POSITION, TEXCOORD_0/1, _FLAECHE, Indizes, Node-Transform) - eigener kleiner Leser, unabhaengig vom Viewer
function leseGlb(datei) {
  const b = fs.readFileSync(datei), jl = b.readUInt32LE(12), js = JSON.parse(b.subarray(20, 20 + jl)), bin = b.subarray(28 + jl);
  const T = { 5121: Uint8Array, 5123: Uint16Array, 5125: Uint32Array, 5126: Float32Array }, K = { SCALAR: 1, VEC2: 2, VEC3: 3 };
  const acc = i => { const a = js.accessors[i], v = js.bufferViews[a.bufferView], A = T[a.componentType], o = bin.byteOffset + (v.byteOffset || 0) + (a.byteOffset || 0);
    return { typ: a.componentType, d: new A(bin.buffer.slice(o, o + a.count * K[a.type] * A.BYTES_PER_ELEMENT)), min: a.min, max: a.max }; };
  const pr = js.meshes[0].primitives[0], at = pr.attributes;
  return { pos: acc(at.POSITION), uv0: at.TEXCOORD_0 !== undefined ? acc(at.TEXCOORD_0) : null, uv1: at.TEXCOORD_1 !== undefined ? acc(at.TEXCOORD_1) : null,
    fl: at._FLAECHE !== undefined ? acc(at._FLAECHE) : null, idx: acc(pr.indices).d, draco: !!(js.extensionsUsed || []).length,
    transform: (js.nodes || []).some(n => n.matrix || n.rotation || n.scale || (n.translation && n.translation.some(v => v))) };
}
function oben(netze, x, z) {   // Brute-Force-Strahl von oben: hoechstes Dreieck -> {y, klasse}
  let best = null;
  for (const g of netze) { const P = g.pos.d, I = g.idx;
    for (let t = 0; t < I.length; t += 3) { const a = I[t] * 3, b = I[t + 1] * 3, c = I[t + 2] * 3;
      const d = (P[b + 2] - P[c + 2]) * (P[a] - P[c]) + (P[c] - P[b]) * (P[a + 2] - P[c + 2]); if (Math.abs(d) < 1e-12) continue;
      const u = ((P[b + 2] - P[c + 2]) * (x - P[c]) + (P[c] - P[b]) * (z - P[c + 2])) / d, v = ((P[c + 2] - P[a + 2]) * (x - P[c]) + (P[a] - P[c]) * (z - P[c + 2])) / d, w = 1 - u - v;
      if (u < -1e-7 || v < -1e-7 || w < -1e-7) continue; const y = u * P[a + 1] + v * P[b + 1] + w * P[c + 1];
      if (!best || y > best.y) best = { y, klasse: g.fl.d[I[t]] }; } }
  return best;
}

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r)); const port = server.address().port;
  const basis = `http://127.0.0.1:${port}/detail_v2/viewer/index.html?mesh=/__mesh__/manifest.json`;
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const fehler = [];
  const oeffne = async (extra, opt = {}) => {
    const ctx = await browser.newContext({ viewport: { width: 960, height: 540 }, ...opt }); const p = await ctx.newPage();
    p.on('console', m => { if (m.type() === 'error' && !(/query=/.test(extra) && /404/.test(m.text()))) fehler.push(extra + ': ' + m.text()); if (/\[dv2\] bereit/.test(m.text())) console.log('     log', m.text()); });
    p.on('pageerror', e => fehler.push(extra + ': ' + e.message));
    await p.goto(basis + extra); await p.waitForFunction(() => window.__test && (window.__test.bereit || window.__test.fehler), null, { timeout: 240000 });
    const f = await p.evaluate(() => window.__test.fehler); if (f) throw new Error('Viewer-Fehler: ' + f);
    return p;
  };
  const bildStat = p => p.evaluate(async () => {   // Anteil Nicht-Himmel-Pixel und Helligkeitsstreuung
    const c = document.querySelector('canvas'), im = new Image(); im.src = c.toDataURL(); await im.decode();
    const k = document.createElement('canvas'); k.width = 240; k.height = 135; const g = k.getContext('2d'); g.drawImage(im, 0, 0, 240, 135);
    const d = g.getImageData(0, 0, 240, 135).data; let nh = 0, s = 0, s2 = 0, n = d.length / 4;
    for (let i = 0; i < d.length; i += 4) { const l = (d[i] + d[i + 1] + d[i + 2]) / 3; s += l; s2 += l * l; if (Math.abs(d[i] - 0xb8) + Math.abs(d[i + 1] - 0xc7) + Math.abs(d[i + 2] - 0xd2) > 30) nh++; }
    return { nicht_himmel: +(nh / n).toFixed(3), streuung: +Math.sqrt(s2 / n - (s / n) ** 2).toFixed(1) };
  });
  const foto = async (p, name) => { const f = path.join(BILDER, name); await p.screenshot({ path: f, type: 'jpeg', quality: 78 }); return f; };

  // 1) Laden + Ladezeit
  const p = await oeffne('&manual=1&hud=0');
  const info = await p.evaluate(() => window.__test.info());
  console.log('     Ladezeit', JSON.stringify(info.ladezeit), 'Dreiecke', info.dreiecke, 'Bytes', info.bytes);
  const summe = man.kacheln.reduce((s, k) => s + (k.dreiecke || 0), 0);
  pruef('alle Kacheln geladen', info.kacheln === man.kacheln.length && info.kacheln > 0, info.kacheln);
  const modellDreiecke = man.modelle ? man.modelle.reduce((s, o) => s + leseGlb(path.join(MESH_DIR, o.glb)).idx.length / 3, 0) : 0;
  pruef('Dreiecke = Manifest (+ Modelle)', !summe || info.dreiecke === summe + modellDreiecke, { viewer: info.dreiecke, manifest: summe, modelle: modellDreiecke });
  pruef('Budget je Kachel <= 60000, gesamt <= 1,6 Mio.', man.kacheln.every(k => (k.dreiecke || 0) <= 60000) && info.dreiecke <= 1.6e6, Math.max(...man.kacheln.map(k => k.dreiecke || 0)));
  // 1b) verbindliches Manifest-Format (Grundgeruest 19.11.2026) + glb-Inhalt
  const fehlF = [];
  const soll = (b, t) => { if (!b) fehlF.push(t); };
  soll(man.version === 1 && man.einheit === 'm' && man.ursprung === 'weltecke', 'version/einheit/ursprung');
  soll(man.karte && man.karte.breite === 336 && man.karte.tiefe === 303, 'karte');
  soll(man.klassen && KN.every((n, k) => man.klassen[String(k)] === n), 'klassen');
  soll(man.attribute && man.attribute.flaeche === '_FLAECHE', 'attribute');
  soll(man.uv && man.uv.TEXCOORD_0 === 'welt_xz_m' && man.uv.TEXCOORD_1 === 'karte_norm' && man.uv.TEXCOORD_2 === 'wegband', 'uv');
  soll(Array.isArray(man.kacheln) && man.kacheln.length === 56, 'kacheln 56');
  soll(Array.isArray(man.modelle) && man.modelle.some(o => o.id === 'bruecke_E2' && o.glb === 'modelle/bruecke_E2.glb' && o.klasse === 5), 'modelle bruecke_E2');
  const SX8 = [0, 42, 84, 126, 168, 210, 252, 294, 336], SZ8 = [0, 43, 86, 129, 172, 215, 258, 303];
  const glbs = {}; let klassenSumme = [0, 0, 0, 0, 0, 0], gemischtN = 0, uvFehler = 0, flFehler = 0, bboxFehler = 0, anteilFehler = 0;
  for (const k of man.kacheln) {
    const i = 'ABCDEFGH'.indexOf(k.id[0]), j = Number(k.id.slice(1)) - 1;
    soll(k.glb === `kacheln/${k.id}.glb`, `${k.id}: glb-Pfad`); soll(JSON.stringify(k.bbox) === JSON.stringify([SX8[i], SZ8[j], SX8[i + 1], SZ8[j + 1]]), `${k.id}: bbox Schnitt`);
    const g = glbs[k.id] = leseGlb(path.join(MESH_DIR, k.glb)); const P = g.pos.d, nT = g.idx.length / 3;
    soll(!g.draco && !g.transform, `${k.id}: Draco/Transform`); soll(nT === k.dreiecke && nT <= 60000, `${k.id}: dreiecke`);
    if (g.pos.min[0] < k.bbox[0] - 1e-4 || g.pos.max[0] > k.bbox[2] + 1e-4 || g.pos.min[2] < k.bbox[1] - 1e-4 || g.pos.max[2] > k.bbox[3] + 1e-4) bboxFehler++;
    if (!g.fl || g.fl.typ !== 5121) { flFehler++; continue; }
    for (let v = 0; v < P.length / 3; v++) { if (g.fl.d[v] > 5) flFehler++;
      if (!g.uv0 || !g.uv1 || Math.abs(g.uv0.d[2 * v] - P[3 * v]) > 1e-4 || Math.abs(g.uv0.d[2 * v + 1] - P[3 * v + 2]) > 1e-4 ||
          Math.abs(g.uv1.d[2 * v] - P[3 * v] / 336) > 1e-6 || Math.abs(g.uv1.d[2 * v + 1] - P[3 * v + 2] / 303) > 1e-6) uvFehler++; }
    const z = [0, 0, 0, 0, 0, 0];
    for (let t = 0; t < g.idx.length; t += 3) { const a = g.fl.d[g.idx[t]]; if (a !== g.fl.d[g.idx[t + 1]] || a !== g.fl.d[g.idx[t + 2]]) gemischtN++; z[a]++; }
    z.forEach((n, c) => { klassenSumme[c] += n; const soll_ = k.klassen_anteil[KN[c]] || 0; if (Math.abs(soll_ - n / nT) > 1e-4) anteilFehler++; });
  }
  const modellGlbs = man.modelle.map(o => { const g = leseGlb(path.join(MESH_DIR, o.glb)); g.id = o.id; g.klasse = o.klasse; return g; });
  for (const g of modellGlbs) { if (!g.fl || [...g.fl.d].some(v => v !== g.klasse)) flFehler++; for (let t = 0; t < g.idx.length; t++) klassenSumme[g.klasse] += t % 3 === 0 ? 1 : 0; }
  pruef('Manifest im verbindlichen Format (Felder, Pfade, bbox = Schnitt)', fehlF.length === 0 && info.formatWarnungen.length === 0, { fehler: fehlF.slice(0, 5), viewer: info.formatWarnungen });
  pruef('glb: kein Draco/Transform, POSITION in bbox, TEXCOORD_0 = Welt-XZ, TEXCOORD_1 = x/336,z/303', bboxFehler === 0 && uvFehler === 0, { bboxFehler, uvFehler });
  pruef('_FLAECHE: u8 0-5 je Vertex, Dreiecke klassenrein, klassen_anteil stimmt', flFehler === 0 && gemischtN === 0 && anteilFehler === 0, { flFehler, gemischtN, anteilFehler });
  const vk = info.klassen;
  pruef('Viewer liest _FLAECHE (Dreiecke je Klasse = glb, 0 gemischt, alle Meshes mit _FLAECHE)', KN.every((n, c) => vk.je_klasse[n] === klassenSumme[c]) && vk.gemischt === 0 && vk.ohne_klasse === 0 && vk.meshes_ohne_flaeche === 0 && info.modelle === man.modelle.length,
    { viewer: vk.je_klasse, glb: Object.fromEntries(KN.map((n, c) => [n, klassenSumme[c]])), modelle: info.modelle });
  // Strahl gegen Brute-Force aus den glb (Hoehe + Klasse) an 60 Zufallspunkten
  let strahlFehler = [], rnd = 7; const r = () => (rnd = (rnd * 16807) % 2147483647) / 2147483647;
  const pktS = Array.from({ length: 60 }, () => [r() * 336, r() * 303]).concat([[192, 74.5], [191.2, 72.1]]);
  const vt = await p.evaluate(pk => pk.map(([x, z]) => window.__test.treffer(x, z)), pktS);
  pktS.forEach(([x, z], n) => { const id = 'ABCDEFGH'[Math.min(7, Math.floor(x / 42))] + (Math.min(6, Math.floor(z / 43)) + 1);
    const b = oben([glbs[id], ...modellGlbs], x, z); if (!b || !vt[n] || Math.abs(b.y - vt[n].y) > 1e-4 || b.klasse !== vt[n].klasse) strahlFehler.push({ x, z, glb: b, viewer: vt[n] && { y: vt[n].y, k: vt[n].klasse } }); });
  pruef('Strahl: Hoehe und Klasse = Brute-Force aus glb (62 Punkte)', strahlFehler.length === 0, strahlFehler.slice(0, 3));
  pruef('Ladezeit gemessen', info.ladezeit && info.ladezeit.gesamt_ms > 0, info.ladezeit);
  // 2) Bodenstrahl gegen das Quellraster (nur Dummy: Gitterpunkte = GB exakt)
  if (istDummy) {
    const D = JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(R3D, 'relief_daten.json.gz')))); const rs = D.rs, GX = 336 * rs + 1;
    const GB = new Float32Array(new Uint8Array(Buffer.from(D.GB, 'base64')).buffer);
    const pkt = []; for (let i = 0; i < 60; i++) pkt.push([Math.round(((i * 37.3) % 336)), Math.round(((i * 53.1) % 303))]);
    pkt.push([42, 43], [0, 0], [336, 303], [294, 301], [209, 118]);
    const hs = await p.evaluate(pk => pk.map(([x, z]) => window.__test.boden(x, z)), pkt);
    const dmax = Math.max(...pkt.map(([x, z], i) => Math.abs(hs[i] - GB[z * rs * GX + x * rs])));
    pruef('Bodenstrahl = Raster an Gitterpunkten (|dh| < 1 mm)', dmax < 1e-3, +dmax.toExponential(2));
  }
  const ohneLuecke = await p.evaluate(() => { let n = 0, leer = 0; for (let x = 0.25; x < 336; x += 1.5) for (let z = 0.25; z < 303; z += 1.5) { n++; if (window.__test.boden(x, z) === null) leer++; } return { n, leer }; });
  pruef('Boden ueberall abfragbar (keine Loecher)', ohneLuecke.leer === 0, ohneLuecke);
  // 3) Laufkamera 1,7 m
  const l1 = await p.evaluate(([x, z, b]) => window.__test.lauf(x, z, b), [SX, SZ, SB]);
  pruef('lauf: Kamera 1,7 m ueber Grund', Math.abs(l1.ueber_grund - 1.7) < 1e-3 && Math.abs(l1.pos[1] - l1.boden - 1.7) < 1e-3, { y: +l1.pos[1].toFixed(3), boden: +l1.boden.toFixed(3) });
  const s1 = await p.evaluate(() => window.__test.schatten());
  const l2 = await p.evaluate(() => window.__test.lauf(150, 60, 90)); const s2 = await p.evaluate(() => window.__test.schatten());
  const dS = Math.hypot(s1.mitte[0] - SX, s1.mitte[2] - SZ), dS2 = Math.hypot(s2.mitte[0] - 150, s2.mitte[2] - 60);
  pruef('Schattenkarte folgt der Kamera', s1.castShadow && dS < 15 && dS2 < 15 && Math.hypot(s1.mitte[0] - s2.mitte[0], s1.mitte[2] - s2.mitte[2]) > 40, { s1: s1.mitte.map(v => +v.toFixed(1)), s2: s2.mitte.map(v => +v.toFixed(1)), halb: s2.halb });
  // 3b) Laufgeschwindigkeit deterministisch: W gedrueckt + __test.schritt(1 s) = 3 m, Shift = 7 m
  await p.evaluate(() => window.__test.lauf(209, 118, 90)); await p.keyboard.down('KeyW');
  const g1 = await p.evaluate(() => window.__test.schritt(1)); await p.keyboard.down('ShiftLeft');
  const g2 = await p.evaluate(() => window.__test.schritt(1)); await p.keyboard.up('ShiftLeft'); await p.keyboard.up('KeyW');
  pruef('Tempo: 3 m/s gehen, 7 m/s mit Shift, Hoehe gehalten', Math.abs(g1.pos[0] - 212) < 0.01 && Math.abs(g2.pos[0] - 219) < 0.01 && Math.abs(g2.ueber_grund - 1.7) < 1e-3, { x1: +g1.pos[0].toFixed(3), x2: +g2.pos[0].toFixed(3) });
  // 3c) Begehbarkeit: Klasse 3/4 und Neigung > 35 Grad gesperrt; auf Sperre zulaufen -> Halt davor
  const sperren = await p.evaluate(() => {
    const T = window.__test, out = {};
    for (let z = 1.5; z < 302 && Object.keys(out).length < 3; z += 1) for (let x = 6.5; x < 330; x += 1) {
      const t = T.treffer(x, z); if (!t) continue;
      const art = t.klasse === 4 ? 'wasser' : t.klasse === 3 ? 'fels' : t.klasse !== null && t.klasse !== 5 && t.neigung > T.maxNeigung ? 'steil' : null;
      if (!art || out[art]) continue;
      const s = T.treffer(x - 5, z); if (!s || !s.begehbar) continue;
      let frei = true; for (let d = 0.25; d < 3.5; d += 0.25) { const u = T.treffer(x - 5 + d, z); if (!u || !u.begehbar) { frei = false; break; } }
      if (frei) out[art] = { x, z, t };
    }
    return out;
  });
  for (const art of ['wasser', 'fels', 'steil']) {
    const z0 = sperren[art];
    if (!z0) { pruef(`Begehbarkeit ${art}: Testpunkt gefunden`, false, null); continue; }
    const g0 = await p.evaluate(() => window.__test.gesperrt());
    await p.evaluate(([x, z]) => window.__test.lauf(x - 5, z, 90), [z0.x, z0.z]); await p.keyboard.down('KeyW');
    let schlecht = 0, last;
    for (let i = 0; i < 40; i++) { last = await p.evaluate(() => window.__test.schritt(0.1)); if (last.begehbar !== true) schlecht++; }
    await p.keyboard.up('KeyW');
    const g1 = await p.evaluate(() => window.__test.gesperrt()), tz = await p.evaluate(([x, z]) => window.__test.treffer(x, z), [last.pos[0], last.pos[2]]);
    pruef(`Begehbarkeit ${art}: gesperrt (${art === 'steil' ? 'Neigung ' + z0.t.neigung.toFixed(1) + '°' : 'Klasse ' + z0.t.klasse}), Laeufer haelt davor`,
      !z0.t.begehbar && schlecht === 0 && last.pos[0] < z0.x && last.pos[0] > z0.x - 2 && tz.begehbar && g1 > g0 && Math.abs(last.ueber_grund - 1.7) < 1e-3,
      { sperre: [z0.x, z0.z], halt_x: +last.pos[0].toFixed(2), klasse_halt: tz.klasse, neigung_halt: +tz.neigung.toFixed(1), sperrungen: g1 - g0 });
  }
  // 3d) Bruecke E2 (Modell, Klasse 5): Strahl trifft Deck vor Wasser, Deck begehbar, Ueberqueren moeglich; daneben Wasser gesperrt
  const br = await p.evaluate(() => { const T = window.__test, d = T.treffer(191.5, 74.5), u = T.treffer(191.5, 74.5, -0.8); return { d, u }; });
  pruef('Bruecke: Strahl trifft Deck (Klasse 5, y 0,30) vor Wasser (Klasse 4 darunter)', br.d && br.d.klasse === 5 && Math.abs(br.d.y - 0.3) < 1e-4 && br.d.begehbar && br.d.netz === 'bruecke_E2' && br.u && br.u.klasse === 4 && br.u.y < br.d.y,
    { deck: br.d && { y: br.d.y, k: br.d.klasse, netz: br.d.netz }, darunter: br.u && { y: +br.u.y.toFixed(3), k: br.u.klasse } });
  await p.evaluate(() => window.__test.lauf(183, 74.5, 90)); await p.keyboard.down('KeyW');
  let aufDeck = 0, deckHoehe = true, fl;
  for (let i = 0; i < 60; i++) { fl = await p.evaluate(() => window.__test.schritt(0.1)); if (fl.klasse === 5) { aufDeck++; if (Math.abs(fl.pos[1] - 2.0) > 1e-3) deckHoehe = false; } }
  await p.keyboard.up('KeyW');
  pruef('Bruecke: Laeufer quert den Bach ueber das Deck (1,7 m ueber Deck)', fl.pos[0] > 199 && aufDeck >= 20 && deckHoehe, { ende_x: +fl.pos[0].toFixed(2), schritte_auf_deck: aufDeck });
  await p.evaluate(() => window.__test.lauf(183, 71.0, 90)); await p.keyboard.down('KeyW');
  for (let i = 0; i < 60; i++) fl = await p.evaluate(() => window.__test.schritt(0.1));
  await p.keyboard.up('KeyW');
  const wz = await p.evaluate(() => { const T = window.__test; for (let x = 186; x < 198; x += 0.25) { const t = T.treffer(x, 71); if (t && t.klasse === 4) return x; } return null; });
  pruef('neben der Bruecke (z 71): Wasser stoppt den Laeufer', wz !== null && fl.pos[0] < wz && fl.begehbar, { halt_x: +fl.pos[0].toFixed(2), wasser_ab_x: wz });

  // 4) Orbit ohne 25-m-Grenze
  const b0 = await p.evaluate(([x, z]) => window.__test.boden(x, z), [SX, SZ]);
  const o5 = await p.evaluate(([x, z, b]) => window.__test.kam([x, b + 5, z + 3], [x, b + 0.5, z]), [SX, SZ, b0]);
  const o1 = await p.evaluate(([x, z, b]) => window.__test.kam([x + 0.6, b + 1.2, z + 0.6], [x, b + 0.5, z]), [SX, SZ, b0]);
  pruef('kam: Orbit-Abstand 5 m und 1 m moeglich (< 25 m)', Math.abs(o5.abstand - Math.hypot(4.5, 3)) < 0.01 && o1.abstand < 1.2 && o1.minDistance < 25, { a5: +o5.abstand.toFixed(3), a1: +o1.abstand.toFixed(3), min: o1.minDistance });
  // 5) Nachweisbilder Clay kommen aus eigener Seite; hier Standard
  await p.evaluate(([x, z, b]) => window.__test.lauf(x, z, b, -4), [SX, SZ, SB]); const st0 = await bildStat(p);
  pruef('Standardbild 1,7 m hat Gelaende', st0.nicht_himmel > 0.3 && st0.streuung > 4, st0);
  await p.context().close();

  // 6) Clay: 1,7 m und 5 m (Nachweis)
  const pc = await oeffne('&manual=1&hud=0&clay=1');
  const lc = await pc.evaluate(([x, z, b]) => window.__test.lauf(x, z, b, -4), [SX, SZ, SB]); const sc1 = await bildStat(pc);
  const fc1 = await foto(pc, 'clay_1m7_dorfkern.jpg');
  const yaw = SB * Math.PI / 180, vx = Math.sin(yaw), vz = -Math.cos(yaw);
  const bv = await pc.evaluate(([x, z]) => window.__test.boden(x, z), [SX + vx * 25, SZ + vz * 25]);
  await pc.evaluate(([x, z, b, tx, tz, tb]) => window.__test.kam([x, b + 5, z], [tx, tb, tz]), [SX, SZ, lc.boden, SX + vx * 25, SZ + vz * 25, bv]);
  const z5 = await pc.evaluate(() => window.__test.zustand()); const sc5 = await bildStat(pc);
  const fc5 = await foto(pc, 'clay_5m_dorfkern.jpg');
  pruef('Clay 1,7 m Bild', sc1.nicht_himmel > 0.3 && sc1.streuung > 4, { ...sc1, bild: fc1 });
  pruef('Clay 5 m Bild', Math.abs(z5.ueber_grund - 5) < 0.01 && sc5.nicht_himmel > 0.3 && sc5.streuung > 4, { ...sc5, ueber_grund: +z5.ueber_grund.toFixed(3), bild: fc5 });
  await pc.context().close();
  // 7) Wire + Kachelrand
  const pw = await oeffne('&manual=1&hud=0&clay=1&wire=1&kachelrand=1');
  const iw = await pw.evaluate(() => window.__test.info());
  const be = await pw.evaluate(() => window.__test.boden(206, 124));
  await pw.evaluate(([b]) => window.__test.kam([204, b + 5, 120], [210, b, 129]), [be]);
  const sw = await bildStat(pw); const fw = await foto(pw, 'wire_rand_5m_E3E4.jpg');
  pruef('?wire=1&kachelrand=1: Linien da, Bild ok', iw.wire && iw.kachelrand && iw.linien === man.kacheln.length + (man.modelle || []).length + 1 && sw.streuung > 4, { linien: iw.linien, ...sw, bild: fw });
  await pw.context().close();
  // 7b) Clay 5 m am Grat G3 (Schatten sichtbar)
  const pg = await oeffne('&manual=1&hud=0&clay=1');
  const bg = await pg.evaluate(() => window.__test.boden(300, 105)), bg2 = await pg.evaluate(() => window.__test.boden(300, 90));
  await pg.evaluate(([b, b2]) => window.__test.kam([300, b + 5, 105], [300, b2, 90]), [bg, bg2]);
  const sg = await bildStat(pg); const fg = await foto(pg, 'clay_5m_grat_g3.jpg');
  pruef('Clay 5 m Grat G3 Bild', sg.nicht_himmel > 0.3 && sg.streuung > 4, { ...sg, bild: fg });
  await pg.context().close();

  // 7c) Schatten wirken: gleiche Ansicht mit/ohne Schattenkarte vergleichen (Klippen/Grat, Blick nach Osten)
  const grau = async extra => { const q = await oeffne('&manual=1&hud=0&clay=1' + extra);
    await q.evaluate(() => { const t = window.__test; t.kam([250, 60, 140], [300, t.boden(300, 95), 95]); });
    const g = await q.evaluate(async () => { const c = document.querySelector('canvas'), im = new Image(); im.src = c.toDataURL(); await im.decode();
      const k = document.createElement('canvas'); k.width = 240; k.height = 135; const x = k.getContext('2d'); x.drawImage(im, 0, 0, 240, 135);
      return Array.from(x.getImageData(0, 0, 240, 135).data.filter((_, i) => i % 4 === 0)); });
    await q.context().close(); return g; };
  const gm = await grau(''), go = await grau('&schatten=0');
  const anteil = gm.filter((v, i) => go[i] - v > 15).length / gm.length;
  pruef('Schattenkarte wirkt (dunklere Pixel mit Schatten)', anteil > 0.003, { anteil: +anteil.toFixed(4) });

  // 7d) ?klassen=1 Debug-Einfaerbung nach _FLAECHE (Bruecke E2 von 5 m)
  const pk = await oeffne('&manual=1&klassen=1');
  await pk.evaluate(() => { const t = window.__test; t.kam([186, 5.3, 66], [192, 0, 74.5]); });
  const farben = await pk.evaluate(async () => { const c = document.querySelector('canvas'), im = new Image(); im.src = c.toDataURL(); await im.decode();
    const k = document.createElement('canvas'); k.width = 240; k.height = 135; const g = k.getContext('2d'); g.drawImage(im, 0, 0, 240, 135);
    const d = g.getImageData(0, 0, 240, 135).data; let blau = 0, braun = 0; for (let i = 0; i < d.length; i += 4) { if (d[i + 2] > d[i] + 40 && d[i + 2] > 120) blau++; if (d[i] > d[i + 2] + 40 && d[i] > 70 && d[i + 1] < d[i] - 15) braun++; }
    return { blau: blau / (d.length / 4), braun: braun / (d.length / 4) }; });
  const fk = await foto(pk, 'klassen_5m_bruecke_e2.jpg');
  pruef('?klassen=1: Wasser blau, Bruecke/Weg braun sichtbar', farben.blau > 0.005 && farben.braun > 0.01, { blau: +farben.blau.toFixed(3), braun: +farben.braun.toFixed(3), bild: fk });
  await pk.context().close();
  // 7e) optional queryPoint (P4, detail_v2/daten/query.mjs) per ?query=
  if (DATEN_DIR && fs.existsSync(path.join(DATEN_DIR, 'query.mjs'))) {
    const pq = await oeffne('&manual=1&hud=0&query=/__daten__/');
    const iq = await pq.evaluate(() => ({ q: window.__test.query, t: window.__test.treffer(209, 118), l: window.__test.lauf(209, 118, 0) }));
    pruef('queryPoint (P4) eingehaengt: geladen, Kachel E3, Hoehe weiter aus dem Strahl', iq.q && !iq.q.fehler && iq.q.quellen && iq.t.kachel === 'E3' && Math.abs(iq.l.ueber_grund - 1.7) < 1e-3,
      { quellen: iq.q && iq.q.quellen, begehbar_quelle: iq.t.quelle });
    await pq.context().close();
  } else console.log('     queryPoint-Test uebersprungen (DATEN_DIR fehlt)');

  // 8) Live-Schleife: WASD, Taste O, Mausrad im Orbit
  const pl = await oeffne('&hud=1');
  await pl.evaluate(() => window.__test.lauf(209, 118, 0));
  await pl.mouse.click(480, 270); await pl.keyboard.down('KeyW'); await pl.waitForTimeout(1500); await pl.keyboard.up('KeyW'); await pl.waitForTimeout(150);
  const w1 = await pl.evaluate(() => window.__test.zustand());
  pruef('WASD: W laeuft nach Norden, 1,7 m gehalten', w1.pos[2] < 118 - 1 && Math.abs(w1.pos[0] - 209) < 0.3 && Math.abs(w1.ueber_grund - 1.7) < 1e-3, { x: +w1.pos[0].toFixed(2), z: +w1.pos[2].toFixed(2), blick: +w1.blick.toFixed(2), ueber_grund: +w1.ueber_grund.toFixed(4) });
  await pl.keyboard.down('KeyD'); await pl.waitForTimeout(800); await pl.keyboard.up('KeyD'); await pl.waitForTimeout(150);
  const w2 = await pl.evaluate(() => window.__test.zustand());
  pruef('WASD: D laeuft nach Osten', w2.pos[0] > w1.pos[0] + 0.8, { x: +w2.pos[0].toFixed(2) });
  await pl.keyboard.press('KeyO'); await pl.waitForTimeout(300);
  const o = await pl.evaluate(() => window.__test.zustand());
  for (let i = 0; i < 12; i++) { await pl.mouse.move(480, 270); await pl.mouse.wheel(0, -400); await pl.waitForTimeout(60); }
  await pl.waitForTimeout(600); const ow = await pl.evaluate(() => window.__test.zustand());
  pruef('Taste O -> Orbit, Mausrad zoomt unter 25 m', o.modus === 'orbit' && ow.abstand < Math.min(o.abstand, 25) - 1, { start: +o.abstand.toFixed(2), nach_rad: +ow.abstand.toFixed(2) });
  await pl.click('#knopf'); await pl.waitForTimeout(200);
  const k = await pl.evaluate(() => window.__test.zustand());
  pruef('Knopf -> zurueck Laufen (1,7 m)', k.modus === 'lauf' && Math.abs(k.ueber_grund - 1.7) < 1e-3, k.modus);
  await pl.context().close();

  // 9) Touch: linke Haelfte Stick, rechte Haelfte schauen
  const pt = await oeffne('&hud=0', { hasTouch: true, isMobile: true, viewport: { width: 800, height: 450 } });
  await pt.evaluate(() => window.__test.lauf(209, 118, 0));
  const cdp = await pt.context().newCDPSession(pt);
  const touch = async (type, pts) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: pts.map(([x, y], id) => ({ x, y, id })) });
  await touch('touchStart', [[150, 300]]); for (let i = 1; i <= 6; i++) { await touch('touchMove', [[150, 300 - i * 10]]); await pt.waitForTimeout(30); }
  await pt.waitForTimeout(1200); await touch('touchEnd', []); await pt.waitForTimeout(150);
  const t1 = await pt.evaluate(() => window.__test.zustand());
  await touch('touchStart', [[600, 225]]); for (let i = 1; i <= 8; i++) { await touch('touchMove', [[600 + i * 10, 225]]); await pt.waitForTimeout(30); }
  await touch('touchEnd', []); await pt.waitForTimeout(150);
  const t2 = await pt.evaluate(() => window.__test.zustand());
  pruef('Touch links: Stick laeuft (1,7 m)', t1.pos[2] < 118 - 1 && Math.abs(t1.ueber_grund - 1.7) < 1e-3, { z: +t1.pos[2].toFixed(2) });
  pruef('Touch rechts: schaut (Gier aendert sich)', Math.abs(t2.blick - t1.blick) > 5, { blick: +t2.blick.toFixed(1) });
  await pt.context().close();

  pruef('keine Konsolen-/Seitenfehler', fehler.length === 0, fehler.slice(0, 5));
  await browser.close(); server.close();
  fs.writeFileSync(path.join(BILDER, 'test_ergebnis.json'), JSON.stringify({ mesh: MESH_DIR, quelle: man.quelle, ladezeit: info.ladezeit, dreiecke: info.dreiecke, bytes: info.bytes, erg }, null, 1));
  console.log(rot ? `TEST ROT (${rot} von ${erg.length})` : `TEST GRUEN (${erg.length}/${erg.length})`);
  process.exit(rot ? 1 : 0);
})().catch(e => { console.error(e); server.close(); process.exit(2); });
