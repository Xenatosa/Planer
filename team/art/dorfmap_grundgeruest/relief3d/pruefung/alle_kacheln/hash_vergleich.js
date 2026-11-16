// P10: Vertex-Hashes je Kachel im gerenderten Three.js-Szenengraph (Ebene 'gelaende').
// Laedt index.html (Referenz, D1/G1/D2) und das P10-HTML (alle Kacheln) in Chromium und
// vergleicht je Kachel Oberflaeche/Seiten/Boden: SHA-256 der Weltkoordinaten (Float32),
// der Indizes und der Vertexfarben. P10b: zusaetzlich Wandkoerper wand_D1/wand_G1 (Ebene 'waende').
// Aufruf (im Ordner relief3d): NODE_PATH=/tmp/w3/node_modules REF=index.html NEU=/tmp/p10/alle_kacheln.html \
//   OUT=/tmp/p10/hash_vergleich.json node pruefung/alle_kacheln/hash_vergleich.js
const E = process.env, { chromium } = require('playwright'), path = require('path'), fs = require('fs');
const ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];
async function hashes(browser, html) {
  const p = await browser.newPage();
  const t0 = Date.now();
  await p.goto('file://' + path.resolve(html) + '?manual=1&nosh=1');
  await p.waitForFunction(() => (window.__test && window.__test.bereit) || window.__fehler, null, { timeout: 300000 });
  const fehler = await p.evaluate(() => window.__fehler || null);
  if (fehler) throw new Error(fehler);
  const r = await p.evaluate(async () => {
    const hex = b => Array.from(new Uint8Array(b), x => x.toString(16).padStart(2, '0')).join('');
    const sha = async a => hex(await crypto.subtle.digest('SHA-256', new Uint8Array(a.buffer, a.byteOffset, a.byteLength)));
    __szene.updateMatrixWorld(true);
    const ms = [];
    __szene.traverse(o => { if (!o.isMesh || o.isInstancedMesh) return; let e = '';
      for (let q = o; q; q = q.parent) if (q.userData && q.userData.ebene) { e = q.userData.ebene; break; }
      if (e === 'gelaende' || e === 'waende') ms.push(o); });
    const out = {};
    const v = new (ms[0].position.constructor)();
    for (const m of ms) {
      const g = m.geometry, P = g.attributes.position, W = new Float32Array(P.count * 3);
      for (let i = 0; i < P.count; i++) { v.fromBufferAttribute(P, i).applyMatrix4(m.matrixWorld); W[i * 3] = v.x; W[i * 3 + 1] = v.y; W[i * 3 + 2] = v.z; }
      const I = g.index ? new Uint32Array(g.index.array) : new Uint32Array(0);
      const C = g.attributes.color ? new Float32Array(g.attributes.color.array) : new Float32Array(0);
      out[m.name] = { vertices: P.count, indices: I.length, pos_sha256: await sha(W), idx_sha256: await sha(I),
        col_sha256: C.length ? await sha(C) : null,
        matrix_identity: m.matrixWorld.elements.every((x, i) => x === [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1][i]) };
    }
    return out;
  });
  await p.close();
  return { html, meshes: r, ladezeit_s: (Date.now() - t0) / 1000 };
}
(async () => {
  const b = await chromium.launch({ args: ARGS });
  const ref = await hashes(b, E.REF || 'index.html');
  const neu = await hashes(b, E.NEU || '/tmp/p10/alle_kacheln.html');
  await b.close();
  const vergleich = {};
  for (const t of ['D1', 'G1', 'D2']) {
    const teile = {};
    let gleich = true;
    for (const art of ['surface', 'sides', 'bottom']) {
      const n = `terrain_${art}_${t}`, a = ref.meshes[n], c = neu.meshes[n];
      const g = !!(a && c && a.pos_sha256 === c.pos_sha256 && a.idx_sha256 === c.idx_sha256 && a.vertices === c.vertices);
      teile[art] = { identisch: g, ref_pos_sha256: a && a.pos_sha256, neu_pos_sha256: c && c.pos_sha256,
        ref_idx_sha256: a && a.idx_sha256, neu_idx_sha256: c && c.idx_sha256, vertices: c && c.vertices,
        farbe_identisch: !!(a && c && a.col_sha256 === c.col_sha256) };
      gleich = gleich && g;
    }
    // Wandkoerper (Ebene 'waende'): in index.html nur D1/G1, D2 wandfrei.
    const wn = `wand_${t}`, wa = ref.meshes[wn], wc = neu.meshes[wn];
    const wand = { ref_vorhanden: !!wa, neu_vorhanden: !!wc,
      identisch: (!wa && !wc) || !!(wa && wc && wa.pos_sha256 === wc.pos_sha256 && wa.idx_sha256 === wc.idx_sha256),
      ref_pos_sha256: wa && wa.pos_sha256, neu_pos_sha256: wc && wc.pos_sha256, vertices: wc && wc.vertices };
    vergleich[t] = { geometrisch_identisch: gleich, teile, wand };
  }
  const res = { referenz: ref.html, neu: neu.html, ladezeit_s: { referenz: ref.ladezeit_s, neu: neu.ladezeit_s },
    referenz_kacheln: Object.keys(ref.meshes).filter(n => n.startsWith('terrain_surface_')).map(n => n.slice(16)),
    neu_kacheln: Object.keys(neu.meshes).filter(n => n.startsWith('terrain_surface_')).map(n => n.slice(16)),
    vergleich, alle_identisch: Object.values(vergleich).every(x => x.geometrisch_identisch),
    waende_identisch: Object.values(vergleich).every(x => x.wand.identisch),
    neu_hashes: neu.meshes, referenz_hashes: ref.meshes };
  if (E.OUT) fs.writeFileSync(E.OUT, JSON.stringify(res, null, 1));
  console.log(JSON.stringify({ alle_identisch: res.alle_identisch, waende_identisch: res.waende_identisch, je_kachel: Object.fromEntries(Object.entries(vergleich).map(([k, x]) => [k, x.geometrisch_identisch])), neu_kacheln: res.neu_kacheln.length, ladezeit_s: res.ladezeit_s }));
  process.exit(res.alle_identisch && res.waende_identisch ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
