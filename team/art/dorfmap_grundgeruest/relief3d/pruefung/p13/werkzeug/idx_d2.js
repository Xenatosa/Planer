const { chromium } = require('playwright'), path = require('path'), crypto = require('crypto');
(async () => { const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] }); const out = {};
 for (const [n, f, prm] of [['basis', process.argv[2], ''], ['p13', process.argv[3], ''], ['p13_silh0', process.argv[3], '&silh=0']]) {
  const p = await b.newPage(); const fe = []; p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') fe.push(m.text()); }); p.on('pageerror', e => fe.push(e.message));
  await p.goto('file://' + path.resolve(f) + '?manual=1&nosh=1' + prm); await p.waitForFunction(() => window.__test && window.__test.bereit, null, { timeout: 300000 });
  const d = await p.evaluate(() => window.__test.dump()); const r = {};
  for (const o of d) if (/^terrain_(surface|sides|bottom)_(D1|G1|D2)$/.test(o.name)) r[o.name] = crypto.createHash('sha256').update(o.pos + '|' + o.idx).digest('hex').slice(0, 12);
  out[n] = { meshes: r, konsole: fe }; await p.close(); }
 console.log(JSON.stringify(out, null, 1)); await b.close(); })();
