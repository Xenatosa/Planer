// P4f: Gesamtansicht der Karte (alle 56 Kacheln) aus Sueden schraeg oben. Aufruf: NODE_PATH=... HTML=/tmp/p4f/alle_kacheln.html OUT=/tmp/p4f/gesamt [SH=1] node gesamt.js
const E = process.env, { chromium } = require('playwright'), path = require('path'), fs = require('fs');
(async () => {
  const out = E.OUT || '/tmp/p4f/gesamt'; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 2400, height: 1500 } });
  await p.goto('file://' + path.resolve(E.HTML) + '?manual=1' + (E.SH ? '' : '&nosh=1'));
  await p.waitForFunction(() => (window.__test && window.__test.bereit) || window.__fehler, null, { timeout: 300000 });
  await p.addStyleTag({ content: '#p,#info,#lade{display:none!important}' });
  await p.evaluate(() => window.__test.stopRender());
  const V = [['gesamt_sued', 168, 150, 330, 50, 0], ['gesamt_steil', 168, 150, 300, 75, 0], ['gesamt_suedwest', 168, 150, 330, 40, -35]];
  for (const [n, x, z, d, el, az] of V) {
    await p.evaluate(([x, z, d, el, az]) => { const y = 0, e = el * Math.PI / 180, a = az * Math.PI / 180;
      window.__test.kam([x + d * Math.cos(e) * Math.sin(a), y + d * Math.sin(e), z + d * Math.cos(e) * Math.cos(a)], [x, y, z]); window.__test.renderOnce(); }, [x, z, d, el, az]);
    await p.screenshot({ path: path.join(out, n + (E.SH ? '_schatten' : '') + '.png') }); process.stdout.write(n + ' ');
  }
  await b.close(); console.log('fertig');
})().catch(e => { console.error(e); process.exit(2); });
