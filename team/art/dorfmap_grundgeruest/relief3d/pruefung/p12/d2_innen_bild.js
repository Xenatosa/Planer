// P12: Nahbild D2-Innenflaeche (abseits Naht D1/D2, z>=54) fuer Vorher/Nachher-Pixelvergleich.
// Aufruf: NODE_PATH=/tmp/relief3d_bau_node/node_modules node pruefung/p12/d2_innen_bild.js <index.html> <out.png> [&nosh=1]
const { chromium } = require('playwright'), path = require('path');
(async () => {
  const [html, out, q] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1024, height: 768 } });
  await p.goto('file://' + path.resolve(html) + '?manual=1&tile=D2' + (q || ''));
  await p.waitForFunction(() => window.__test && window.__test.bereit, null, { timeout: 300000 });
  await p.addStyleTag({ content: 'body>*:not(canvas){display:none!important}' });
  await p.evaluate(() => { window.__test.stopRender(); const H = window.__test.H, y = H(147, 70);
    window.__test.kam([147, y + 22, 54], [147, y, 74]); window.__test.renderOnce(); });
  await p.screenshot({ path: out }); await b.close();
})();
