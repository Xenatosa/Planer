// P10: Nahbild je Kachel (schraeg von oben, Kamera wie neu/viewer.js focus()) fuer Sichtpruefung.
// Aufruf (im Ordner relief3d):
//   NODE_PATH=/tmp/w3/node_modules HTML=/tmp/p10/alle_kacheln.html DIR=/tmp/p10/nahbilder \
//   [KACHELN=C3,D1] [ABSTAND=1.6] [B=1024 H=768] [CLAY=1] [KARTE=0] node pruefung/alle_kacheln/nahbild_alle.js
// Schreibt DIR/darstellung.json (Dreiecke je Kachel und Ebene), DIR/<Kachel>.png, DIR/karte.png (ganze Karte, KARTE=0 aus) und DIR/nahbilder.json.
const E = process.env, { chromium } = require('playwright'), path = require('path'), fs = require('fs');
(async () => {
  const dir = E.DIR || '/tmp/p10/nahbilder';
  if (path.resolve(dir).startsWith('/tmp/w3')) throw new Error('Ausgabe nach /tmp/w3 gesperrt');
  fs.mkdirSync(dir, { recursive: true });
  const B = +(E.B || 1024), H = +(E.H || 768), k = +(E.ABSTAND || 1.6);
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: B, height: H } });
  const t0 = Date.now();
  await p.goto('file://' + path.resolve(E.HTML || '/tmp/p10/alle_kacheln.html') + '?manual=1' + (E.CLAY ? '&clay=1' : '') + (E.Q || ''));
  await p.waitForFunction(() => (window.__test && window.__test.bereit) || window.__fehler, null, { timeout: 300000 });
  const fehler = await p.evaluate(() => window.__fehler || null);
  if (fehler) throw new Error(fehler);
  await p.addStyleTag({ content: '#p,#info{display:none!important}#nbl{position:absolute;left:10px;top:8px;z-index:9;font:bold 28px system-ui;color:#fff;text-shadow:0 0 4px #000,0 0 2px #000}' });
  await p.evaluate(() => { window.__test.stopRender(); const d = document.createElement('div'); d.id = 'nbl'; document.body.appendChild(d); });
  const ladezeit = (Date.now() - t0) / 1000;
  const alle = await p.evaluate(() => window.__test.kacheln);
  if (await p.evaluate(() => !!window.__test.darstellung))
    fs.writeFileSync(path.join(dir, 'darstellung.json'), JSON.stringify(await p.evaluate(() => window.__test.darstellung()), null, 1));
  const wahl = E.KACHELN ? E.KACHELN.split(',').map(s => s.trim().toUpperCase()) : alle;
  const log = { html: E.HTML || '/tmp/p10/alle_kacheln.html', abstand: k, groesse: [B, H], ladezeit_s: ladezeit, bilder: {} };
  for (const t of wahl) {
    const t1 = Date.now();
    await p.evaluate(([t, k]) => {
      window.__test.focus(t, k); document.getElementById('nbl').textContent = t;
      window.__test.renderOnce();
    }, [t, k]);
    const datei = path.join(dir, `${t}.png`);
    await p.screenshot({ path: datei });
    log.bilder[t] = { datei, sekunden: (Date.now() - t1) / 1000, bytes: fs.statSync(datei).size };
    process.stdout.write(t + ' ');
  }
  if (E.KARTE !== '0') {  // zusaetzlich die ganze Karte schraeg von Sueden (karte.png)
    const t1 = Date.now();
    await p.evaluate(() => { window.__test.setView('karte'); document.getElementById('nbl').textContent = 'Karte A1-H7'; window.__test.renderOnce(); });
    const datei = path.join(dir, 'karte.png'); await p.screenshot({ path: datei });
    log.karte = { datei, sekunden: (Date.now() - t1) / 1000, bytes: fs.statSync(datei).size };
  }
  log.gesamt_s = (Date.now() - t0) / 1000;
  fs.writeFileSync(path.join(dir, 'nahbilder.json'), JSON.stringify(log, null, 1));
  console.log('\n' + JSON.stringify({ bilder: Object.keys(log.bilder).length, ladezeit_s: ladezeit, gesamt_s: log.gesamt_s }));
  await b.close();
})().catch(e => { console.error(e); process.exit(2); });
