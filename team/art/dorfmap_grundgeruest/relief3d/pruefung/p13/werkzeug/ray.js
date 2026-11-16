const { chromium } = require('playwright'), path = require('path');
(async () => { const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
 const p = await b.newPage({ viewport: { width: 960, height: 680 } });
 await p.goto('file://' + path.resolve('diag/alle_kacheln.html') + '?manual=1&nosh=1');
 await p.waitForFunction(() => window.__test && window.__test.bereit, null, { timeout: 300000 });
 await p.addStyleTag({ content: '#p,#info,#lade{display:none!important}' }); await p.evaluate(() => window.__test.stopRender());
 const r = await p.evaluate(pts => { window.__test.focus('D3', 1.6); window.__test.renderOnce(); const { scene, THREE, camera } = window.__dbg;
  const ter = [], wat = []; scene.traverse(o => { if (o.isMesh && o.name.startsWith('terrain_surface')) ter.push(o); if (o.isMesh && o.name.startsWith('wasser')) wat.push(o); });
  const rc = new THREE.Raycaster(); return pts.map(([x, y]) => { rc.setFromCamera(new THREE.Vector2(x / 960 * 2 - 1, -y / 680 * 2 + 1), camera);
   const ht = rc.intersectObjects(ter, false)[0], hw = rc.intersectObjects(wat, false)[0];
   return { px: [x, y], gelaende: ht && [ht.point.x, ht.point.y, ht.point.z].map(v => +v.toFixed(3)), normal_y: ht && +ht.face.normal.y.toFixed(3), wasser: hw && [hw.point.x, hw.point.y, hw.point.z].map(v => +v.toFixed(3)), H: ht && +window.__test.HG(ht.point.x, ht.point.z).toFixed(3) }; }); },
  [[690 - 0.57 * 4, 172 + 0.82 * 4], [690 - 0.57 * 6, 172 + 0.82 * 6], [690 - 0.57 * 7, 172 + 0.82 * 7], [690 - 0.57 * 8, 172 + 0.82 * 8], [690, 172], [690 + 0.57 * 7, 172 - 0.82 * 7]]);
 console.log(JSON.stringify(r)); await b.close(); })();
