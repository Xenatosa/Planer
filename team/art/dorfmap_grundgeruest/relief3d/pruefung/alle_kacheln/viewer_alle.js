// P10: Viewer fuer alle 56 Kachelmeshes. tileColor, foundationGeometry und makeMesh sind
// unveraenderte Kopien aus neu/viewer.js (renderNeuCore), damit Oberflaeche, Seiten und Boden
// je Kachel exakt wie in index.html entstehen. Unterschied: Kachelliste aus dem Paket statt
// fest D1/G1/D2, Kachelrand-Linie (Ebene 'raster') und Licht/Schatten folgen der Fokus-Kachel.
// P10b: Waende fuer alle Kacheln (Paket, neu/wand.py-Funktionen), Wege-Overlay aus WEGA und Wasser
// aus WV nach dem Rasterverfahren von main.js (Legacy-Viewer, Pfad ?wneu=0), Bruecken wie main.js,
// je Kachel als eigene Meshes in den Ebenen 'wege' und 'wasser' (nicht 'gelaende' -> Lochscan
// unveraendert). Kamera-API __test.blick({kachel|x,z, abstand, azimut, neigung}).

const decodeBytes = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
const decodeF32 = s => new Float32Array(decodeBytes(s).buffer);
const decodeU32 = s => new Uint32Array(decodeBytes(s).buffer);

function tileColor(source, positions, rs, nx, ny) {
  const bytes = decodeBytes(source.VC), gx = nx * rs + 1, gy = ny * rs + 1;
  if (bytes.length !== gx * gy * 3) throw new Error('VC hat eine unerwartete Laenge');
  const out = new Float32Array(positions.length);
  for (let k = 0; k < positions.length / 3; k++) {
    const x = Math.round(positions[k * 3] * rs), z = Math.round(positions[k * 3 + 2] * rs);
    if (x < 0 || z < 0 || x >= gx || z >= gy) throw new Error('Meshvertex ausserhalb des Reliefgitters');
    const from = (z * gx + x) * 3;
    for (let c = 0; c < 3; c++) out[k * 3 + c] = Math.pow(bytes[from + c] / 255, 2.2);
  }
  return out;
}

function foundationGeometry(THREE, top, indices, bounds, rs) {
  const cols = (bounds[2] - bounds[0]) * rs, rows = (bounds[3] - bounds[1]) * rs;
  const width = cols + 1, count = top.length / 3;
  let floor = Infinity;
  for (let i = 1; i < top.length; i += 3) floor = Math.min(floor, top[i]);
  floor = Math.min(-24, floor - 20);
  const bottom = new Float32Array(count * 3);
  for (let k = 0; k < count; k++) bottom.set([top[k * 3], floor, top[k * 3 + 2]], k * 3);
  const side = [];
  const boundary = [];
  for (let x = 0; x <= cols; x++) boundary.push(x);
  for (let z = 1; z <= rows; z++) boundary.push(z * width + cols);
  for (let x = cols - 1; x >= 0; x--) boundary.push(rows * width + x);
  for (let z = rows - 1; z > 0; z--) boundary.push(z * width);
  for (let i = 0; i < boundary.length; i++) {
    const a = boundary[i], b = boundary[(i + 1) % boundary.length];
    side.push(...top.subarray(a * 3, a * 3 + 3), ...top.subarray(b * 3, b * 3 + 3),
      ...bottom.subarray(b * 3, b * 3 + 3), ...bottom.subarray(a * 3, a * 3 + 3));
  }
  const bottomIndex = [];
  for (let z = 0; z < rows; z++) for (let x = 0; x < cols; x++) {
    const a = z * width + x, b = a + 1, c = a + width, d = c + 1;
    bottomIndex.push(d, c, a, b, d, a);
  }
  const sidePosition = new Float32Array(side);
  const sideIndex = new Uint32Array(boundary.length * 6);
  for (let i = 0; i < boundary.length; i++) sideIndex.set([4 * i, 4 * i + 1, 4 * i + 2, 4 * i, 4 * i + 2, 4 * i + 3], i * 6);
  const bottomGeo = new THREE.BufferGeometry();
  bottomGeo.setAttribute('position', new THREE.BufferAttribute(bottom, 3));
  bottomGeo.setIndex(bottomIndex);
  bottomGeo.computeVertexNormals();
  const sideGeo = new THREE.BufferGeometry();
  sideGeo.setAttribute('position', new THREE.BufferAttribute(sidePosition, 3));
  sideGeo.setIndex(new THREE.BufferAttribute(sideIndex, 1));
  sideGeo.computeVertexNormals();
  return { bottomGeo, sideGeo, floor };
}

function makeMesh(THREE, positions, indices, material, name, group, normals = null) {
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  if (indices.length) geometry.setIndex(new THREE.BufferAttribute(indices, 1));
  if (normals && normals.length === positions.length) geometry.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
  else geometry.computeVertexNormals();
  const mesh = new THREE.Mesh(geometry, material);
  mesh.name = name;
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.userData.boden = true;
  group.add(mesh);
  return mesh;
}

export async function renderAlleKacheln({ THREE, OrbitControls, DN, stufe }) {
  const manifest = DN.alle_kacheln;
  if (!manifest || !manifest.tiles) throw new Error('alle_kacheln-Manifest fehlt');
  const { nx: NX, ny: NY, rs } = DN, GX = NX * rs + 1, GY = NY * rs + 1;
  const q = new URLSearchParams(location.search);
  const alle = manifest.reihenfolge;
  const wahl = q.get('kacheln') ? q.get('kacheln').split(',').map(s => s.trim().toUpperCase()).filter(Boolean) : alle;
  for (const t of wahl) if (!manifest.tiles[t]) throw new Error('Unbekannte Kachel ' + t);
  await stufe('Kachelmeshes bauen …');
  let renderer = null;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(innerWidth, innerHeight);
    renderer.shadowMap.enabled = !/[?&]nosh=1/.test(location.search);
    renderer.shadowMap.type = THREE.PCFShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    document.body.appendChild(renderer.domElement);
  } catch (_) { renderer = null; }

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xb8c7d2);
  const camera = new THREE.PerspectiveCamera(48, innerWidth / innerHeight, 0.1, 1800);
  const controls = new OrbitControls(camera, renderer ? renderer.domElement : document.body);
  controls.enableDamping = true; controls.dampingFactor = 0.08;
  controls.maxPolarAngle = Math.PI / 2 - 0.015; controls.minDistance = 2; controls.screenSpacePanning = true;
  scene.add(new THREE.HemisphereLight(0xe2edf6, 0x6d675c, 1.5));
  const sun = new THREE.DirectionalLight(0xfff2dc, 2.0);
  sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  const S = 75; sun.shadow.camera.left = -S; sun.shadow.camera.right = S; sun.shadow.camera.top = S; sun.shadow.camera.bottom = -S;
  sun.shadow.camera.near = 1; sun.shadow.camera.far = 1200;
  // P10b Darstellung (QA P4b Punkt 1): Schattenakne. Bias/NormalBias nur im Viewer; ?sbias= / ?snbias= zum Testen.
  sun.shadow.bias = Number(q.get('sbias') ?? -0.0005); sun.shadow.normalBias = Number(q.get('snbias') ?? 0.08);
  scene.add(sun, sun.target);

  const terrainRoot = new THREE.Group(); terrainRoot.userData.ebene = 'gelaende'; scene.add(terrainRoot);
  const wallRoot = new THREE.Group(); wallRoot.userData.ebene = 'waende'; scene.add(wallRoot);
  const rasterRoot = new THREE.Group(); rasterRoot.userData.ebene = 'raster'; scene.add(rasterRoot);
  const wegeRoot = new THREE.Group(); wegeRoot.userData.ebene = 'wege'; scene.add(wegeRoot);
  const wasserRoot = new THREE.Group(); wasserRoot.userData.ebene = 'wasser'; scene.add(wasserRoot);
  const ohne = new Set((q.get('ohne') || '').split(',').filter(Boolean));
  wegeRoot.visible = !ohne.has('wege'); wasserRoot.visible = !ohne.has('wasser'); wallRoot.visible = !ohne.has('waende');
  rasterRoot.visible = q.get('raster') !== '0';
  const clay = /[?&]clay=1/.test(location.search);
  const terrainMaterial = new THREE.MeshLambertMaterial({ color: clay ? 0x92918c : 0xffffff, vertexColors: !clay, side: THREE.DoubleSide });
  // P10b Darstellung (QA P4b Punkt 2): Seiten/Boden jeder Kachel liegen an der Naht exakt auf der
  // Oberkante der Nachbaroberflaeche (gleiche Tiefe) und gewinnen dort einzelne Pixel -> dunkle Haarlinie.
  // polygonOffset schiebt nur Seiten/Boden in der Tiefe nach hinten; Geometrie/Hashes unveraendert.
  // ?naht=0 schaltet die Hilfe ab (Vorher-Bild).
  const nahtHilfe = q.get('naht') !== '0';
  const foundationMaterial = new THREE.MeshLambertMaterial({ color: clay ? 0x77746e : 0x746e64, side: THREE.DoubleSide,
    polygonOffset: nahtHilfe, polygonOffsetFactor: nahtHilfe ? 4 : 0, polygonOffsetUnits: nahtHilfe ? 4 : 0 });
  const wallMaterial = new THREE.MeshLambertMaterial({ color: clay ? 0x85827b : 0x69645d, side: THREE.DoubleSide, flatShading: false,
    polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1 });
  const visibleHeights = new Float32Array(decodeBytes(DN.GB).buffer);
  const H = (x, z) => {
    const fx = Math.max(0, Math.min(x * rs, GX - 1.001)), fz = Math.max(0, Math.min(z * rs, GY - 1.001));
    const ix = Math.floor(fx), iz = Math.floor(fz), u = fx - ix, v = fz - iz, k = iz * GX + ix;
    return (visibleHeights[k] * (1 - u) + visibleHeights[k + 1] * u) * (1 - v) +
      (visibleHeights[k + GX] * (1 - u) + visibleHeights[k + GX + 1] * u) * v;
  };
  // Gesamt-Hoehenfeld wie main.js Zeile 109: GB, ueberschrieben mit den Vertexhoehen aller Kachelmeshes.
  const Gf = new Float32Array(visibleHeights), tilePos = {};
  for (const tile of alle) {
    const P = decodeF32(manifest.tiles[tile].vertices_xyz_f32); tilePos[tile] = P;
    for (let k = 0; k < P.length; k += 3) Gf[Math.round(P[k + 2] * rs) * GX + Math.round(P[k] * rs)] = P[k + 1];
  }
  const HG = (x, z) => {
    const fx = Math.max(0, Math.min(x * rs, GX - 1.001)), fz = Math.max(0, Math.min(z * rs, GY - 1.001));
    const ix = Math.floor(fx), iz = Math.floor(fz), u = fx - ix, v = fz - iz, k = iz * GX + ix;
    return (Gf[k] * (1 - u) + Gf[k + 1] * u) * (1 - v) + (Gf[k + GX] * (1 - u) + Gf[k + GX + 1] * u) * v;
  };
  const tileStats = {}, tileTop = {};
  for (const tile of wahl) {
    const t = manifest.tiles[tile], bounds = t.bounds;
    const positions = tilePos[tile], indices = decodeU32(t.indices_u32);
    if (positions.length / 3 !== t.vertices || indices.length / 3 !== t.triangles) throw new Error(`Meshzaehlung stimmt nicht: ${tile}`);
    const tileGroup = new THREE.Group(); tileGroup.name = `terrain_${tile}`;
    tileGroup.userData.ebene = 'gelaende'; tileGroup.userData.kachel = tile;
    terrainRoot.add(tileGroup);
    const colors = tileColor(DN, positions, rs, NX, NY);
    const top = makeMesh(THREE, positions, indices, terrainMaterial, `terrain_surface_${tile}`, tileGroup);
    if (!clay) top.geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    const sealed = foundationGeometry(THREE, positions, indices, bounds, t.samples_per_m);
    const side = new THREE.Mesh(sealed.sideGeo, foundationMaterial); side.name = `terrain_sides_${tile}`;
    side.castShadow = side.receiveShadow = true; side.userData.boden = true; tileGroup.add(side);
    const cap = new THREE.Mesh(sealed.bottomGeo, foundationMaterial); cap.name = `terrain_bottom_${tile}`;
    cap.castShadow = cap.receiveShadow = true; cap.userData.boden = true; tileGroup.add(cap);
    tileTop[tile] = positions;
    tileStats[tile] = { vertices: t.vertices, triangles: t.triangles, closedTriangles: t.closed_triangles,
      samplingM: t.sampling_m, surfaceMode: t.surface_mode };
    // Kachelrand als Linie 0,25 m ueber der Oberflaeche (nur Anzeige, Ebene 'raster', kein Mesh).
    const cols = (bounds[2] - bounds[0]) * rs, rows = (bounds[3] - bounds[1]) * rs, w = cols + 1, ring = [];
    for (let x = 0; x <= cols; x++) ring.push(x);
    for (let z = 1; z <= rows; z++) ring.push(z * w + cols);
    for (let x = cols - 1; x >= 0; x--) ring.push(rows * w + x);
    for (let z = rows - 1; z >= 0; z--) ring.push(z * w);
    const lp = new Float32Array(ring.length * 3);
    ring.forEach((k, i) => lp.set([positions[k * 3], positions[k * 3 + 1] + 0.25, positions[k * 3 + 2]], i * 3));
    const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.BufferAttribute(lp, 3));
    const line = new THREE.Line(lg, new THREE.LineBasicMaterial({ color: 0xffe14d }));
    line.name = `rand_${tile}`; line.visible = false; rasterRoot.add(line);
    if (tileGroup.children.length !== 3) throw new Error('Kachelgruppe unvollstaendig ' + tile);
  }
  const wallStats = {};
  const wandQuellen = Object.entries(manifest.waende?.tiles || {});
  if (q.get('d2wand') === '1' && manifest.waende?.d2_unterdrueckt_mesh) wandQuellen.push(['D2', manifest.waende.d2_unterdrueckt_mesh]);
  for (const [tile, t] of wandQuellen) {
    if (!wahl.includes(tile)) continue;
    if (!t || !t.triangles) continue;
    const positions = decodeF32(t.vertices_xyz_f32), indices = decodeU32(t.indices_u32);
    if (positions.length / 3 !== t.vertices || indices.length / 3 !== t.triangles) throw new Error(`Wandmeshzaehlung stimmt nicht: ${tile}`);
    const normals = t.normals_xyz_f32 ? decodeF32(t.normals_xyz_f32) : null;
    const group = new THREE.Group(); group.name = `waende_${tile}`;
    group.userData.ebene = 'waende'; group.userData.kachel = tile; wallRoot.add(group);
    makeMesh(THREE, positions, indices, wallMaterial, `wand_${tile}`, group, normals);
    wallStats[tile] = { features: t.features, vertices: t.vertices, triangles: t.triangles };
  }

  // ---- Wege-Overlay (main.js "Wege-Overlay: weicher Rand ueber Vertex-Alpha", LS=1) ----
  const hash = (a, b) => { const v = Math.sin(a * 12.9898 + b * 78.233) * 43758.5453; return v - Math.floor(v); };
  const overlayStats = {};
  const bereich = tile => { const b = manifest.tiles[tile].bounds; return [b[0] * rs, b[1] * rs, b[2] * rs, b[3] * rs]; };
  if (DN.WEGA) {
    const A = decodeBytes(DN.WEGA);
    if (A.length !== GX * GY) throw new Error('WEGA hat eine unerwartete Laenge');
    const mat = new THREE.MeshLambertMaterial({ vertexColors: true, transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2 });
    for (const tile of wahl) {
      const [i0, j0, i1, j1] = bereich(tile), wp = [], wc = [], wi = [], map = new Map();
      const vx = k => { let m = map.get(k); if (m === undefined) { m = wp.length / 3; map.set(k, m); const i = k % GX, j = (k / GX) | 0, h = hash(i, j);
        wp.push(i / rs, Gf[k] + 0.05, j / rs); const a = A[k] / 255, e = a * a, sa = Math.min(1, Math.max(0, (a - 0.22) / 0.3)), ka = sa * sa * (3 - 2 * sa);
        wc.push(0.62 - 0.30 * e + 0.04 * h, 0.58 - 0.30 * e + 0.03 * h, 0.54 - 0.30 * e + 0.02 * h, 0.88 * ka); } return m; };
      for (let j = j0; j < j1; j++) for (let i = i0; i < i1; i++) { const a = j * GX + i, b = a + 1, c = a + GX, d = c + 1;
        if (A[a] | A[b] | A[c] | A[d]) wi.push(vx(a), vx(c), vx(d), vx(a), vx(d), vx(b)); }
      overlayStats[tile] = { wege_dreiecke: wi.length / 3 };
      if (!wi.length) continue;
      const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(wp, 3));
      g.setAttribute('color', new THREE.Float32BufferAttribute(wc, 4)); g.setIndex(wi); g.computeVertexNormals();
      const m = new THREE.Mesh(g, mat); m.name = `wege_${tile}`; m.receiveShadow = true; m.renderOrder = 1;
      const grp = new THREE.Group(); grp.name = `wege_${tile}`; grp.userData.ebene = 'wege'; grp.userData.kachel = tile; grp.add(m); wegeRoot.add(grp);
    }
  }
  // Bruecken wie main.js (Box 1 x 0,25 x 1 je Eintrag), nur in geladenen Kacheln.
  const kachelVon = (x, z) => 'ABCDEFGH'[Math.min(7, Math.max(0, Math.floor(x / 42)))] + (Math.min(6, Math.max(0, Math.floor(z / 43))) + 1);
  const br = (DN.bruecken || []).filter(([x, , z]) => wahl.includes(kachelVon(x, z)));
  if (br.length) {
    const bm = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 0.25, 1), new THREE.MeshLambertMaterial({ color: 0x7a5230 }), br.length);
    const o = new THREE.Object3D(); br.forEach(([x, y, z], n) => { o.position.set(x, y, z); o.updateMatrix(); bm.setMatrixAt(n, o.matrix); });
    bm.castShadow = true; bm.name = 'bruecken'; const grp = new THREE.Group(); grp.userData.ebene = 'wege'; grp.add(bm); wegeRoot.add(grp);
  }
  // ---- Wasser (main.js Raster-Wassernetz, Pfad ?wneu=0: Spiegelglaettung O4, Randabsenkung O5 E1, Farben/Alpha/Schaum) ----
  if (DN.WV) {
    const WV = decodeF32(DN.WV), N = GX * GY, ok = k => WV[k] > -900, GL = Gf;
    if (WV.length !== N) throw new Error('WV hat eine unerwartete Laenge');
    const WR = new Float32Array(WV);
    { let A = new Float32Array(WV);
      for (let it = 0; it < 3; it++) { const B = new Float32Array(A); for (let j = 1; j < GY - 1; j++) for (let i = 1; i < GX - 1; i++) { const k = j * GX + i; if (!ok(k)) continue; const v = [];
        for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) { const n = k + dj * GX + di; if (n != k && ok(n) && A[n] > A[k] + 0.3) v.push(A[n]); }
        if (v.length >= 5) { v.sort((x, y) => x - y); B[k] = v[v.length >> 1]; } } A = B; }
      for (let it = 0; it < 16; it++) { const B = new Float32Array(A); for (let j = 1; j < GY - 1; j++) for (let i = 1; i < GX - 1; i++) { const k = j * GX + i; if (!ok(k)) continue; let s = 0, c = 0;
        for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) { const n = k + dj * GX + di; if (ok(n)) { s += A[n]; c++; } }
        B[k] = Math.min(WV[k] + 0.3, Math.max(WV[k] - 0.6, s / c)); } A = B; }
      WR.set(A); }
    const WD = new Float32Array(WR);
    { const O = new Float32Array(N); for (let k = 0; k < N; k++) if (ok(k)) { const d = WR[k] - GL[k]; if (d < 0.12) { const t = Math.min(1, Math.max(0, (0.12 - d) / 0.12)), w = t * t * (3 - 2 * t); O[k] = w * (GL[k] - 0.15 - WR[k]); } }
      for (let it = 0; it < 2; it++) { const B = new Float32Array(O); for (let j = 1; j < GY - 1; j++) for (let i = 1; i < GX - 1; i++) { const k = j * GX + i; if (!ok(k)) continue; let s = 0, c = 0;
        for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) { const n = k + dj * GX + di; if (ok(n)) { const g = (di && dj) ? 1 : (di || dj) ? 2 : 4; s += O[n] * g; c += g; } }
        B[k] = Math.min(O[k], s / c); } O.set(B); }
      for (let k = 0; k < N; k++) if (ok(k)) WD[k] = WR[k] + O[k]; }
    const nb = k => [k + 1, k - 1, k + GX, k - GX, k + GX + 1, k + GX - 1, k - GX + 1, k - GX - 1].filter(n => n >= 0 && n < N && ok(n));
    const hR = k => { if (ok(k)) return WD[k]; let s = 0, c = 0; for (const n of nb(k)) { s += WR[n]; c++; } return c ? Math.min(s / c, GL[k] + 0.02) : GL[k] + 0.02; };
    const mat = new THREE.MeshPhongMaterial({ vertexColors: true, transparent: true, depthWrite: false, shininess: 90, specular: 0x667788, side: THREE.DoubleSide, forceSinglePass: true });
    for (const tile of wahl) {
      const [i0, j0, i1, j1] = bereich(tile), wp = [], wc = [], wi = [], map = new Map();
      const vx = k => { let m = map.get(k); if (m !== undefined) return m; m = wp.length / 3; map.set(k, m);
        const i = k % GX, j = (k / GX) | 0, t = ok(k) ? Math.min(1, Math.max(0, (WV[k] - GL[k]) / 1.5)) : 0;
        wp.push(i / rs, hR(k), j / rs);
        const e = 1 - Math.min(1, t * 4), qd = n => ok(n) ? Math.abs(WV[n] - WV[k]) : 0;
        const fo0 = ok(k) ? Math.min(1, Math.max(0, (qd(k + 1) + qd(k - 1) + qd(k + GX) + qd(k - GX) - 0.9) * 0.7)) : 0, fo = Math.min(fo0, 0.3);
        wc.push((0.06 + 0.5 * e * e) * (1 - fo) + 0.70 * fo, (0.16 + 0.48 * e * e) * (1 - fo) + 0.76 * fo, (0.21 + 0.45 * e * e) * (1 - fo) + 0.80 * fo,
          Math.max(0.14 + 0.76 * Math.pow(Math.min(1, t * 1.15), 0.8), 0.35 * fo));
        return m; };
      for (let j = j0; j < j1; j++) for (let i = i0; i < i1; i++) { const a = j * GX + i, b = a + 1, c = a + GX, d = c + 1;
        if (ok(a) || ok(b) || ok(c) || ok(d)) wi.push(vx(a), vx(c), vx(d), vx(a), vx(d), vx(b)); }
      (overlayStats[tile] = overlayStats[tile] || {}).wasser_dreiecke = wi.length / 3;
      if (!wi.length) continue;
      const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(wp, 3));
      g.setAttribute('color', new THREE.Float32BufferAttribute(wc, 4)); g.setIndex(wi); g.computeVertexNormals();
      const m = new THREE.Mesh(g, mat); m.name = `wasser_${tile}`; m.receiveShadow = true; m.renderOrder = 2;
      const grp = new THREE.Group(); grp.name = `wasser_${tile}`; grp.userData.ebene = 'wasser'; grp.userData.kachel = tile; grp.add(m); wasserRoot.add(grp);
    }
  }

  // Fokus-Hoehe: Mittelwert der Kacheloberflaeche (robuster als ein Punkt bei Klippen).
  const tileCenter = tile => {
    const b = manifest.tiles[tile].bounds, x = (b[0] + b[2]) / 2, z = (b[1] + b[3]) / 2;
    const P = tileTop[tile]; let s = 0, n = 0;
    if (P) { for (let i = 1; i < P.length; i += 3) { s += P[i]; n++; } }
    return [x, n ? s / n : H(x, z), z];
  };
  let currentTile = wahl.includes('D1') ? 'D1' : wahl[0];
  const render = () => { if (renderer) renderer.render(scene, camera); };
  let lichtZiel = null;
  const light = () => {
    const [cx, cy, cz] = lichtZiel || tileCenter(currentTile);
    const az = Number(document.getElementById('az')?.value ?? 315) * Math.PI / 180;
    const el = Number(document.getElementById('el')?.value ?? 35) * Math.PI / 180;
    sun.target.position.set(cx, cy, cz);
    sun.position.set(cx + 430 * Math.cos(el) * Math.sin(az), cy + 430 * Math.sin(el), cz - 430 * Math.cos(el) * Math.cos(az));
    sun.target.updateMatrixWorld(); sun.intensity = Number(document.getElementById('st')?.value ?? 90) / 48;
  };
  const setCamera = (p, t) => { camera.position.set(...p); controls.target.set(...t); controls.update(); render(); };
  const schattenKachel = () => { sun.shadow.camera.left = sun.shadow.camera.bottom = -S; sun.shadow.camera.right = sun.shadow.camera.top = S; sun.shadow.camera.updateProjectionMatrix(); };
  // Schraegsicht wie neu/viewer.js focus(): Kamera (x-20, y+35, z+28) auf Kachelmitte; Abstand-Faktor k.
  const focus = (tile, k = 1) => {
    currentTile = tile; lichtZiel = null;
    document.querySelectorAll('[data-tile]').forEach(b => b.classList.toggle('sel', b.dataset.tile === tile));
    rasterRoot.children.forEach(l => { l.visible = l.name === `rand_${tile}`; });
    schattenKachel();
    const [x, y, z] = tileCenter(tile);
    setCamera(tile === 'D1' ? [x - 16 * k, y + 35 * k, z + 28 * k] : [x - 20 * k, y + 35 * k, z + 28 * k], [x, y, z]);
    light(); render();
    const label = document.getElementById('modus');
    if (label) label.textContent = `Kachel ${tile} · Mesh ${tileStats[tile].triangles.toLocaleString('de-DE')} Dreiecke · ${tileStats[tile].surfaceMode}`;
  };
  const rasterDiv = document.getElementById('raster');
  if (rasterDiv) for (let r = 1; r <= 7; r++) { for (const c of 'ABCDEFGH') { const n = c + r; const b = document.createElement('button');
    b.textContent = n; b.dataset.tile = n; b.disabled = !wahl.includes(n); b.onclick = () => focus(n); rasterDiv.appendChild(b); }
    rasterDiv.appendChild(document.createElement('br')); }
  document.querySelectorAll('[data-l]').forEach(c => c.onchange = () => {
    if (c.dataset.l === 'gelaende') terrainRoot.visible = c.checked;
    if (c.dataset.l === 'waende') wallRoot.visible = c.checked;
    if (c.dataset.l === 'raster') rasterRoot.visible = c.checked;
    if (c.dataset.l === 'wege') wegeRoot.visible = c.checked;
    if (c.dataset.l === 'wasser') wasserRoot.visible = c.checked;
    render();
  });
  ['az', 'el', 'st'].forEach(id => { const e = document.getElementById(id); if (e) e.oninput = () => { light(); render(); }; });
  const presets = {
    schraeg: () => focus(currentTile),
    oben: () => { const [x, y, z] = tileCenter(currentTile); setCamera([x, y + 85, z + 0.1], [x, y, z]); },
    karte: () => { rasterRoot.children.forEach(l => { l.visible = false; }); sun.shadow.camera.left = sun.shadow.camera.bottom = -260; sun.shadow.camera.right = sun.shadow.camera.top = 260;
      sun.shadow.camera.updateProjectionMatrix(); sun.target.position.set(NX / 2, 0, NY / 2); sun.target.updateMatrixWorld();
      const az = 315 * Math.PI / 180, el = 35 * Math.PI / 180;
      sun.position.set(NX / 2 + 430 * Math.cos(el) * Math.sin(az), 430 * Math.sin(el), NY / 2 - 430 * Math.cos(el) * Math.cos(az));
      setCamera([NX / 2, 330, NY / 2 + 260], [NX / 2, 0, NY / 2]); },
  };
  for (const t of wahl) presets[t] = () => focus(t);
  document.getElementById('reset').onclick = () => presets.schraeg();
  document.getElementById('voben').onclick = () => presets.oben();
  document.getElementById('vkarte').onclick = () => presets.karte();
  controls.addEventListener('change', render);
  const encode = array => {
    const bytes = new Uint8Array(array.buffer, array.byteOffset, array.byteLength);
    let s = ''; for (let i = 0; i < bytes.length; i += 32768) s += String.fromCharCode(...bytes.subarray(i, i + 32768));
    return btoa(s);
  };
  // Blick auf eine Stelle: Ziel = Kachelmitte (kachel) oder Punkt (x, z) auf dem Gelaende.
  // azimut = Blickrichtung in Grad (0 = Nord/-z, 90 = Ost/+x, 180 = Sued/+z, 270 = West/-x),
  // neigung = Grad unter der Horizontalen (90 = senkrecht von oben), abstand = Kameraabstand zum Ziel.
  // Standard entspricht focus(): azimut 35,5, neigung 45,5, abstand 49,1 x 1,6.
  const blick = ({ kachel, x, z, abstand = 78.6, azimut = 35.54, neigung = 45.5, rand = true } = {}) => {
    let ziel;
    if (kachel) { kachel = kachel.toUpperCase(); if (!tileTop[kachel]) throw new Error('Kachel nicht geladen: ' + kachel); ziel = tileCenter(kachel); }
    else { if (!Number.isFinite(x) || !Number.isFinite(z)) throw new Error('blick braucht kachel oder x und z'); ziel = [x, HG(x, z), z]; }
    const t = kachel || kachelVon(ziel[0], ziel[2]);
    currentTile = tileTop[t] ? t : currentTile;
    rasterRoot.children.forEach(l => { l.visible = rand && l.name === `rand_${t}`; });
    const a = azimut * Math.PI / 180, n = neigung * Math.PI / 180, d = abstand;
    const pos = [ziel[0] - Math.sin(a) * Math.cos(n) * d, ziel[1] + Math.sin(n) * d, ziel[2] + Math.cos(a) * Math.cos(n) * d];
    schattenKachel(); lichtZiel = ziel; setCamera(pos, ziel); light(); render();
    return { kachel: t, ziel: ziel.map(v => +v.toFixed(2)), kamera: pos.map(v => +v.toFixed(2)), abstand, azimut, neigung };
  };
  window.__szene = scene;
  window.__info = () => ({ kacheln: wahl.length, terrain: tileStats, waende: wallStats, overlays: overlayStats });
  window.__test = {
    bereit: true, kacheln: wahl.slice(), start: DN.start || { x: 147, z: 30 }, wandfuss: { x: 140, z: 35 },
    setModus: mode => { if (mode !== 'neu') throw new Error('Der Kern-Viewer enthaelt nur den neuen Prototyp'); },
    setView: name => (presets[name] || presets.schraeg)(), focus, blick, kam: (p, t) => setCamera(p, t), H, HG,
    darstellung: () => Object.fromEntries(wahl.map(t => [t, { gelaende_dreiecke: tileStats[t].triangles, surface_mode: tileStats[t].surfaceMode,
      wand_dreiecke: wallStats[t]?.triangles || 0, wege_dreiecke: overlayStats[t]?.wege_dreiecke || 0, wasser_dreiecke: overlayStats[t]?.wasser_dreiecke || 0,
      bruecken: br.filter(([x, , z]) => kachelVon(x, z) === t).length }])),
    dump: () => {
      scene.updateMatrixWorld(true);
      const out = [];
      scene.traverse(o => {
        if (!o.isMesh) return;
        const a = o.geometry.attributes;
        out.push({ name: o.name, ebene: o.parent?.userData?.ebene || '', sichtbar: o.visible,
          pos: encode(new Float32Array(a.position.array)), pi: a.position.itemSize,
          col: a.color ? encode(new Float32Array(a.color.array)) : null, ci: a.color?.itemSize || 0,
          idx: o.geometry.index ? encode(new Uint32Array(o.geometry.index.array)) : null,
          mw: Array.from(o.matrixWorld.elements), n: 1 });
      });
      return out;
    },
    stopRender: () => { if (renderer) renderer.setAnimationLoop(null); }, renderOnce: render,
    setLight: (az, el, st) => { document.getElementById('az').value = az; document.getElementById('el').value = el; document.getElementById('st').value = st; light(); render(); },
  };
  document.getElementById('info').textContent = `3D Meshes: ${wahl.length} Kacheln\nFlaechendreiecke: ${Object.values(tileStats).reduce((s, t) => s + t.triangles, 0).toLocaleString('de-DE')}\nWandkoerper: ${Object.keys(wallStats).length} Kacheln\nWege-Overlay: ${Object.values(overlayStats).filter(o => o.wege_dreiecke).length} Kacheln\nWasser: ${Object.values(overlayStats).filter(o => o.wasser_dreiecke).length} Kacheln`;
  const queryTile = q.get('tile');
  if (queryTile && presets[queryTile.toUpperCase()]) focus(queryTile.toUpperCase()); else focus(currentTile);
  if (renderer && !/[?&]manual=1/.test(location.search)) renderer.setAnimationLoop(() => { controls.update(); render(); });
  render();
  const loading = document.getElementById('lade');
  if (loading) { if (renderer) loading.remove(); else loading.textContent = 'WebGL nicht verfuegbar; Meshdaten fuer Pruefungen geladen.'; }
  window.addEventListener('resize', () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); if (renderer) renderer.setSize(innerWidth, innerHeight); render(); });
}
