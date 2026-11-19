// Playwright-Test Viewer v2 (P3) [S]. HeadlessChrome/SwiftShader, eigener statischer Server (file:// kann keine .glb holen).
// Aufruf (im Ordner relief3d):  NODE_DIR=/tmp/dv2_viewer/node node detail_v2/viewer/test_viewer_v2.js
//   MESH_DIR = Ordner mit manifest.json (Standard: /tmp/dv2_viewer/dummy_mesh, wird bei Bedarf mit dummy/erzeuge_dummy.py erzeugt)
//   BILDER   = Ausgabeordner fuer die Nachweisbilder (Standard /tmp/dv2_viewer/bilder)
//   START    = x,z,blick fuer die Nachweisbilder (Standard Dorfkern 209,118,200)
const path = require('path'), fs = require('fs'), http = require('http'), zlib = require('zlib'), { execFileSync } = require('child_process');
const NODE_DIR = process.env.NODE_DIR || '/tmp/dv2_viewer/node';
const { chromium } = require(path.join(NODE_DIR, 'node_modules', 'playwright'));
const R3D = path.resolve(__dirname, '..', '..');
const MESH_DIR = path.resolve(process.env.MESH_DIR || '/tmp/dv2_viewer/dummy_mesh');
const BILDER = process.env.BILDER || '/tmp/dv2_viewer/bilder';
const [SX, SZ, SB] = (process.env.START || '209,118,200').split(',').map(Number);
if (!fs.existsSync(path.join(MESH_DIR, 'manifest.json')))
  execFileSync('python3', [path.join(__dirname, 'dummy', 'erzeuge_dummy.py'), '--out', MESH_DIR], { stdio: 'inherit' });
fs.mkdirSync(BILDER, { recursive: true });
const TYP = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.glb': 'model/gltf-binary' };
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0]);
  const f = u.startsWith('/__mesh__/') ? path.join(MESH_DIR, u.slice(10)) : path.join(R3D, u);
  if (!f.startsWith(R3D) && !f.startsWith(MESH_DIR)) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': TYP[path.extname(f)] || 'application/octet-stream' }); res.end(d); });
});
const erg = []; let rot = 0;
const pruef = (name, ok, wert) => { erg.push({ name, ok: !!ok, wert }); if (!ok) rot++; console.log(`${ok ? 'OK  ' : 'ROT '} ${name}${wert !== undefined ? ' · ' + JSON.stringify(wert) : ''}`); };
const man = JSON.parse(fs.readFileSync(path.join(MESH_DIR, 'manifest.json')));
const istDummy = /DUMMY/.test(man.quelle || '');

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r)); const port = server.address().port;
  const basis = `http://127.0.0.1:${port}/detail_v2/viewer/index.html?mesh=/__mesh__/manifest.json`;
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const fehler = [];
  const oeffne = async (extra, opt = {}) => {
    const ctx = await browser.newContext({ viewport: { width: 960, height: 540 }, ...opt }); const p = await ctx.newPage();
    p.on('console', m => { if (m.type() === 'error') fehler.push(extra + ': ' + m.text()); if (/\[dv2\] bereit/.test(m.text())) console.log('     log', m.text()); });
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
  pruef('Dreiecke = Manifest', !summe || info.dreiecke === summe, { viewer: info.dreiecke, manifest: summe });
  pruef('Budget je Kachel <= 60000, gesamt <= 1,6 Mio.', man.kacheln.every(k => (k.dreiecke || 0) <= 60000) && info.dreiecke <= 1.6e6, Math.max(...man.kacheln.map(k => k.dreiecke || 0)));
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
  pruef('?wire=1&kachelrand=1: Linien da, Bild ok', iw.wire && iw.kachelrand && iw.linien === man.kacheln.length + 1 && sw.streuung > 4, { linien: iw.linien, ...sw, bild: fw });
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
