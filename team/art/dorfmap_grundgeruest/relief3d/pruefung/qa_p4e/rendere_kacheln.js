// P4d: SH=1 rendert mit Schatten (ohne nosh=1).
// QA P4b: je Kachel 1 Uebersicht (wie P10 focus, Abstand 1.6) + 4 Viertel-Nahbilder (Spielkamera aus Sueden, 35 Grad, Abstand D m)
// + optional Punktliste (PUNKTE=json [{n,x,z,d?,el?,az?}]) fuer Detailbilder.
// Aufruf (im Ordner relief3d): NODE_PATH=/tmp/w3/node_modules HTML=/tmp/p4b/alle_kacheln.html DIR=/tmp/p4b/roh [KACHELN=C3,D1] [CLAY=1] [D=30] node pruefung/qa_p4b/rendere_kacheln.js
const E = process.env, { chromium } = require('playwright'), path = require('path'), fs = require('fs');
(async () => {
  const dir = E.DIR || '/tmp/p4b/roh'; fs.mkdirSync(dir, { recursive: true });
  const B = +(E.B || 960), Hh = +(E.H || 680), D = +(E.D || 30);
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: B, height: Hh } });
  await p.goto('file://' + path.resolve(E.HTML || '/tmp/p4b/alle_kacheln.html') + '?manual=1' + (E.SH ? '' : '&nosh=1') + (E.CLAY ? '&clay=1' : ''));
  await p.waitForFunction(() => (window.__test && window.__test.bereit) || window.__fehler, null, { timeout: 300000 });
  await p.addStyleTag({ content: '#p,#info,#lade{display:none!important}' });
  await p.evaluate(() => window.__test.stopRender());
  const kam = async (x, z, d, el, az) => p.evaluate(([x, z, d, el, az]) => {
    const y = window.__test.H(x, z), e = el * Math.PI / 180, a = az * Math.PI / 180; // az 0 = Kamera im Sueden (z+), Blick nach Norden
    window.__test.kam([x + d * Math.cos(e) * Math.sin(a), y + d * Math.sin(e), z + d * Math.cos(e) * Math.cos(a)], [x, y, z]); window.__test.renderOnce();
  }, [x, z, d, el, az]);
  if (E.PUNKTE) {
    for (const q of JSON.parse(fs.readFileSync(E.PUNKTE))) { await kam(q.x, q.z, q.d || 15, q.el || 35, q.az || 0); await p.screenshot({ path: path.join(dir, q.n + '.png') }); process.stdout.write(q.n + ' '); }
  } else {
    const alle = await p.evaluate(() => window.__test.kacheln);
    const wahl = E.KACHELN ? E.KACHELN.split(',') : alle;
    for (const t of wahl) {
      await p.evaluate(t => { window.__test.focus(t, 1.6); window.__test.renderOnce(); }, t);
      await p.screenshot({ path: path.join(dir, `${t}_U.png`) });
      const c = 'ABCDEFGH'.indexOf(t[0]), r = +t.slice(1) - 1, x0 = c * 42, z0 = r * 43;
      const Q = [[x0 + 10.5, z0 + 10.75], [x0 + 31.5, z0 + 10.75], [x0 + 10.5, z0 + 32.25], [x0 + 31.5, z0 + 32.25]];
      for (let i = 0; i < 4; i++) { await kam(Q[i][0], Q[i][1], D, 35, 0); await p.screenshot({ path: path.join(dir, `${t}_Q${i + 1}.png`) }); }
      process.stdout.write(t + ' ');
    }
  }
  await b.close(); console.log('fertig');
})().catch(e => { console.error(e); process.exit(2); });
