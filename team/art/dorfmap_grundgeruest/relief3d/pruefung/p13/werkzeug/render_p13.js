// P13 Diagnose-Render: Kritiker-Kameras (QA p4h rendere_kacheln.js) + Modi
const E = process.env, { chromium } = require('playwright'), path = require('path'), fs = require('fs');
(async () => {
  const dir = E.DIR; fs.mkdirSync(dir, { recursive: true });
  const B = +(E.B || 960), Hh = +(E.H || 680), DSF = +(E.DSF || 1);
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: B, height: Hh }, deviceScaleFactor: DSF });
  const fehler = []; p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') fehler.push(m.type() + ': ' + m.text()); }); p.on('pageerror', e => fehler.push('pageerror: ' + e.message));
  await p.goto('file://' + path.resolve(E.HTML) + '?manual=1' + (E.SH ? '' : '&nosh=1') + (E.PARAM ? '&' + E.PARAM : ''));
  await p.waitForFunction(() => (window.__test && window.__test.bereit) || window.__fehler, null, { timeout: 300000 });
  await p.addStyleTag({ content: '#p,#info,#lade{display:none!important}' });
  await p.evaluate(() => window.__test.stopRender());
  const info = await p.evaluate(mode => {
    if (!mode || !window.__dbg) return null;
    const { scene, THREE } = window.__dbg, st = {}, add = [];
    const basic = c => new THREE.MeshBasicMaterial({ color: c, side: THREE.DoubleSide });
    scene.traverse(o => { if (!o.isMesh) return; const n = o.name;
      const art = n.startsWith('terrain_surface') ? 'top' : n.startsWith('terrain_sides') || n.startsWith('terrain_bottom') ? 'fund' : n.startsWith('wand') ? 'wand' : n.startsWith('wege') ? 'wege' : n.startsWith('wasser') ? 'wasser' : 'sonst';
      st[art] = (st[art] || 0) + 1;
      if (mode === 'magenta' && art === 'top') { o.material = o.material.clone(); o.material.side = THREE.FrontSide;
        const bk = new THREE.Mesh(o.geometry, new THREE.MeshBasicMaterial({ color: 0xff00ff, side: THREE.BackSide })); bk.matrixAutoUpdate = false; bk.matrix.copy(o.matrixWorld); add.push(bk); }
      if (mode === 'magenta' && art === 'fund') { o.material = o.material.clone(); o.material.color.set(0x00ff00); o.material.emissive.set(0x00ff00); }
      if (mode === 'magenta' && art === 'wand') o.material = basic(0x00ffff);
      if (mode === 'front' && art === 'top') { o.material = o.material.clone(); o.material.side = THREE.FrontSide; }
      if (mode === 'nofund' && art === 'fund') o.visible = false;
    });
    for (const m of add) { m.matrixWorldAutoUpdate = false; m.matrixWorld.copy(m.matrix); scene.add(m); }
    return st;
  }, E.MODE || '').catch(e => 'ERR ' + e.message);
  if (E.CLEAR) await p.evaluate(c => { window.__dbg.scene.background = new window.__dbg.THREE.Color(c); }, E.CLEAR);
  const kam = async (x, z, d, el, az) => p.evaluate(([x, z, d, el, az]) => {
    const y = window.__test.H(x, z), e = el * Math.PI / 180, a = az * Math.PI / 180;
    window.__test.kam([x + d * Math.cos(e) * Math.sin(a), y + d * Math.sin(e), z + d * Math.cos(e) * Math.cos(a)], [x, y, z]); window.__test.renderOnce();
  }, [x, z, d, el, az]);
  for (const s of (E.SHOTS || 'B4_Q2,G3_U,H2_U').split(',')) {
    const [t, v] = s.split('_');
    if (v === 'U') await p.evaluate(t => { window.__test.focus(t, 1.6); window.__test.renderOnce(); }, t);
    else { const c = 'ABCDEFGH'.indexOf(t[0]), r = +t.slice(1) - 1, x0 = c * 42, z0 = r * 43, i = +v[1] - 1;
      const Q = [[x0 + 10.5, z0 + 10.75], [x0 + 31.5, z0 + 10.75], [x0 + 10.5, z0 + 32.25], [x0 + 31.5, z0 + 32.25]]; await kam(Q[i][0], Q[i][1], 30, 35, 0); }
    await p.screenshot({ path: path.join(dir, s + '.png') });
  }
  const gl = await p.evaluate(() => { const r = window.__dbg && window.__dbg.renderer; if (!r) return null; const c = r.getContext(); return { attr: c.getContextAttributes(), samples: c.getParameter(c.SAMPLES), renderer: c.getParameter(c.RENDERER) }; });
  const tri = E.TRI ? await p.evaluate(() => { const { scene } = window.__dbg; let neg = 0, alle = 0, offen = 0, innen = 0; scene.traverse(o => { if (!o.isMesh || !o.name.startsWith('terrain_surface')) return;
    const P = o.geometry.attributes.position.array, I = o.geometry.index.array, kant = new Map();
    for (let t = 0; t < I.length; t += 3) { const a = I[t] * 3, b = I[t + 1] * 3, c = I[t + 2] * 3; const ux = P[b] - P[a], uz = P[b + 2] - P[a + 2], vx = P[c] - P[a], vz = P[c + 2] - P[a + 2]; const ny = uz * vx - ux * vz; alle++; if (ny < 0) neg++;
      for (const [x, y] of [[I[t], I[t + 1]], [I[t + 1], I[t + 2]], [I[t + 2], I[t]]]) { const k = x < y ? x + ',' + y : y + ',' + x; kant.set(k, (kant.get(k) || 0) + 1); } }
    let x0 = 1e9, x1 = -1e9, z0 = 1e9, z1 = -1e9; for (let i = 0; i < P.length; i += 3) { x0 = Math.min(x0, P[i]); x1 = Math.max(x1, P[i]); z0 = Math.min(z0, P[i + 2]); z1 = Math.max(z1, P[i + 2]); }
    for (const [k, n] of kant) if (n === 1) { offen++; const [x, y] = k.split(',').map(Number); const rnd = v => Math.abs(P[v * 3] - x0) < 1e-4 || Math.abs(P[v * 3] - x1) < 1e-4 || Math.abs(P[v * 3 + 2] - z0) < 1e-4 || Math.abs(P[v * 3 + 2] - z1) < 1e-4; if (!(rnd(x) && rnd(y))) innen++; } });
    return { dreiecke: alle, nach_unten: neg, offene_kanten: offen, offene_innenkanten: innen }; }) : null;
  console.log(JSON.stringify({ info, fehler, gl, tri }));
  await b.close();
})().catch(e => { console.error(e); process.exit(2); });
