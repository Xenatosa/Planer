// P14: Nutzer-Zoom per Mausrad (echte Wheel-Events auf dem Canvas, Animationsschleife aktiv) -> gemessener Abstand
const { chromium } = require('playwright'), path = require('path');
(async () => { const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] }); const out = {};
 for (const [n, f, prm] of JSON.parse(process.argv[2])) { const p = await b.newPage({ viewport: { width: 960, height: 680 } }); const fe = [];
  p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') fe.push(m.text()); }); p.on('pageerror', e => fe.push(e.message));
  await p.goto('file://' + path.resolve(f) + '?nosh=1' + prm); await p.waitForFunction(() => window.__test && window.__test.bereit, null, { timeout: 300000 });
  await p.addStyleTag({ content: '#p,#info,#lade{display:none!important}' });
  await p.evaluate(() => { const s = window.__test.start || { x: 147, z: 30 }; const y = window.__test.H(s.x, s.z); window.__test.kam([s.x, y + 23, s.z + 33], [s.x, y, s.z]); });
  const r = { start: await p.evaluate(() => window.__test.abstand()), minDistance: await p.evaluate(() => window.__test.minAbstand()) };
  await p.mouse.move(480, 340); for (let i = 0; i < 60; i++) { await p.mouse.wheel(0, -400); await p.waitForTimeout(30); }
  await p.waitForTimeout(1500); r.nach_60_wheel_rein = await p.evaluate(() => window.__test.abstand());
  for (let i = 0; i < 10; i++) { await p.mouse.wheel(0, 400); await p.waitForTimeout(30); } await p.waitForTimeout(1500); r.nach_10_wheel_raus = await p.evaluate(() => window.__test.abstand());
  await p.evaluate(() => { const s = window.__test.start || { x: 147, z: 30 }; const y = window.__test.H(s.x, s.z); window.__test.kam([s.x, y + 5, s.z + 7], [s.x, y, s.z]); });
  r.programmkamera_8_6m = await p.evaluate(() => window.__test.abstand());
  await p.mouse.wheel(0, -100); await p.waitForTimeout(1500); r.nach_programm_plus_1_wheel = await p.evaluate(() => window.__test.abstand());
  r.konsole = fe; out[n] = r; await p.close(); }
 console.log(JSON.stringify(out, null, 1)); await b.close(); })();
