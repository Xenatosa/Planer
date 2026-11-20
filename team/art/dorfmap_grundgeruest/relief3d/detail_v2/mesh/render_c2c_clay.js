// Honest Clay evidence renders for the C2c CDT mesh.
// Run from relief3d with NODE_DIR=/tmp/relief3d_bau_node and MESH_DIR pointing
// at detail_v2/mesh. Output defaults to /workspace/dorfmap_final/detail_v2/tag2_clay.
const path = require('path');
const fs = require('fs');
const http = require('http');
const NODE_DIR = process.env.NODE_DIR || '/tmp/relief3d_bau_node';
const { chromium } = require(path.join(NODE_DIR, 'node_modules', 'playwright'));
const R3D = path.resolve(__dirname, '..', '..');
const MESH_DIR = path.resolve(process.env.MESH_DIR || __dirname);
const OUT_DIR = process.env.OUT_DIR || '/workspace/dorfmap_final/detail_v2/tag2_clay';
const types = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.glb': 'model/gltf-binary' };
fs.mkdirSync(OUT_DIR, { recursive: true });

const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0]);
  const f = u.startsWith('/__mesh__/') ? path.join(MESH_DIR, u.slice(10)) : path.join(R3D, u);
  if (!f.startsWith(R3D) && !f.startsWith(MESH_DIR)) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (e, d) => {
    if (e) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' });
    res.end(d);
  });
});

const views = [
  { id: 'D3', tile: 'D3', x: 146, z: 119, tx: 153, tz: 103, targetY: 0.25 },
  { id: 'E3_bach', tile: 'E3', x: 193, z: 110, tx: 188.5, tz: 94, targetY: 0.3 },
  { id: 'E2_bruecke', tile: 'E2', x: 192, z: 84, tx: 192, tz: 72, targetY: 0.3 },
  { id: 'dorfkern', tile: 'E3', x: 209, z: 128, tx: 209, tz: 108, targetY: 0.5 },
];

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const url = `http://127.0.0.1:${server.address().port}/detail_v2/viewer/index.html?mesh=/__mesh__/manifest.json`;
  const browser = await chromium.launch({ headless: false, executablePath: process.env.CHROME_BIN || '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--enable-webgl',
    '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  try {
    for (const v of views) {
      const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
      const q = `&manual=1&hud=0&clay=1&kacheln=${v.tile}&schatten=1`;
      await page.goto(url + q);
      await page.waitForFunction(() => window.__test && (window.__test.bereit || window.__test.fehler), null, { timeout: 240000 });
      const error = await page.evaluate(() => window.__test.fehler);
      if (error) throw new Error(`${v.id}: ${error}`);
      for (const [suffix, eyeHeight] of [['1p7m', 1.7], ['5m', 5.0]]) {
        const base = await page.evaluate(([x, z]) => window.__test.boden(x, z), [v.x, v.z]);
        const targetBase = await page.evaluate(([x, z]) => window.__test.boden(x, z), [v.tx, v.tz]);
        await page.evaluate(([v, base, targetBase, eyeHeight]) => {
          window.__test.kam([v.x, (base ?? 0) + eyeHeight, v.z],
                            [v.tx, (targetBase ?? 0) + v.targetY, v.tz]);
          window.__test.render();
        }, [v, base, targetBase, eyeHeight]);
        const name = `c2c_${v.id}_${suffix}.jpg`;
        await page.screenshot({ path: path.join(OUT_DIR, name), type: 'jpeg', quality: 90 });
        console.log(`${name}: eye=${eyeHeight}m, tile=${v.tile}, ground=${base}`);
      }
      await page.close();
    }
  } finally {
    await browser.close();
    server.close();
  }
})().catch(e => { console.error(e); process.exitCode = 1; });
