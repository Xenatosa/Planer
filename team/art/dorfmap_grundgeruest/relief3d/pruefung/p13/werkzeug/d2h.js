const { chromium } = require('playwright'), path = require('path');
(async () => { const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] }); const out = {};
 for (const [n, prm] of [['p13', ''], ['silh0', '&silh=0']]) { const p = await b.newPage(); const f = [];
  p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') f.push(m.text()); }); p.on('pageerror', e => f.push(e.message));
  await p.goto('file://' + path.resolve(process.argv[2]) + '?manual=1&nosh=1' + prm);
  await p.waitForFunction(() => (window.__test && window.__test.bereit) || window.__fehler, null, { timeout: 300000 });
  out[n] = await p.evaluate(async () => { const { scene, THREE } = window.__dbg, r = {};
   const h = async a => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new Uint8Array(a.buffer, a.byteOffset, a.byteLength)))).map(x => x.toString(16).padStart(2, '0')).join('').slice(0, 8);
   const ms = []; scene.traverse(o => { if (o.isMesh && /^terrain_(surface|sides|bottom)_D2$/.test(o.name)) ms.push(o); });
   for (const o of ms) r[o.name] = { pos: await h(o.geometry.attributes.position.array), nor: await h(o.geometry.attributes.normal.array), side: o.material.side, shadowSide: o.material.shadowSide };
   return r; }); out[n].konsole = f; await p.close(); }
 console.log(JSON.stringify(out)); await b.close(); })();
