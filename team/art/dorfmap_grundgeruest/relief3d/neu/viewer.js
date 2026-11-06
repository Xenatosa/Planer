// Renderer adapter for the opt-in tiled core in the shared main.js entry.

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

function makeMesh(THREE, positions, indices, material, name, group) {
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  if (indices.length) geometry.setIndex(new THREE.BufferAttribute(indices, 1));
  geometry.computeVertexNormals();
  const mesh = new THREE.Mesh(geometry, material);
  mesh.name = name;
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.userData.boden = true;
  group.add(mesh);
  return mesh;
}

export async function renderNeuCore({ THREE, OrbitControls, DN, stufe }) {
  const manifest = DN.neu_mesh_tiles;
  if (!manifest || !manifest.tiles || !manifest.waende) throw new Error('neu_mesh_tiles oder Wandmesh-Manifest fehlt');
  const { nx: NX, ny: NY, rs } = DN, GX = NX * rs + 1, GY = NY * rs + 1;
  await stufe('Prototyp-Meshes laden …');
  // The geometry checks also run in headless Chromium builds without WebGL.
  // Keep constructing the same THREE scene there; only the display is optional.
  let renderer = null;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(innerWidth, innerHeight);
    renderer.shadowMap.enabled = !/[?&]nosh=1/.test(location.search);
    renderer.shadowMap.type = THREE.PCFShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    document.body.appendChild(renderer.domElement);
  } catch (_) {
    renderer = null;
  }

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xb8c7d2);
  const camera = new THREE.PerspectiveCamera(48, innerWidth / innerHeight, 0.1, 1800);
  const controls = new OrbitControls(camera, renderer ? renderer.domElement : document.body);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.maxPolarAngle = Math.PI / 2 - 0.015;
  controls.minDistance = 2;
  controls.screenSpacePanning = true;
  scene.add(new THREE.HemisphereLight(0xe2edf6, 0x6d675c, 1.5));
  const sun = new THREE.DirectionalLight(0xfff2dc, 2.0);
  sun.position.set(340, 440, -150);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.camera.left = -230; sun.shadow.camera.right = 230;
  sun.shadow.camera.top = 230; sun.shadow.camera.bottom = -230;
  scene.add(sun, sun.target);

  const terrainRoot = new THREE.Group(); terrainRoot.userData.ebene = 'gelaende'; scene.add(terrainRoot);
  const wallRoot = new THREE.Group(); wallRoot.userData.ebene = 'waende'; scene.add(wallRoot);
  const clay = /[?&]clay=1/.test(location.search);
  const terrainMaterial = new THREE.MeshLambertMaterial({
    color: clay ? 0x92918c : 0xffffff, vertexColors: !clay, side: THREE.DoubleSide,
  });
  const foundationMaterial = new THREE.MeshLambertMaterial({
    color: clay ? 0x77746e : 0x746e64, side: THREE.DoubleSide,
  });
  const wallMaterial = new THREE.MeshLambertMaterial({
    color: clay ? 0x85827b : 0x69645d, side: THREE.DoubleSide, flatShading: true,
    polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1,
  });
  const visibleHeights = new Float32Array(decodeBytes(DN.GB || DN.G).buffer);
  const H = (x, z) => {
    const fx = Math.max(0, Math.min(x * rs, GX - 1.001)), fz = Math.max(0, Math.min(z * rs, GY - 1.001));
    const ix = Math.floor(fx), iz = Math.floor(fz), u = fx - ix, v = fz - iz, k = iz * GX + ix;
    return (visibleHeights[k] * (1 - u) + visibleHeights[k + 1] * u) * (1 - v) +
      (visibleHeights[k + GX] * (1 - u) + visibleHeights[k + GX + 1] * u) * v;
  };
  const tileStats = {};
  for (const tile of ['D1', 'G1', 'D2']) {
    const t = manifest.tiles[tile], bounds = t.bounds;
    const positions = decodeF32(t.vertices_xyz_f32), indices = decodeU32(t.indices_u32);
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
    tileStats[tile] = { vertices: t.vertices, triangles: t.triangles, closedTriangles: t.closed_triangles,
      samplingM: t.sampling_m, surfaceMode: t.surface_mode };
  }

  const wallStats = {};
  for (const tile of ['D1', 'G1']) {
    const t = manifest.waende.tiles[tile];
    if (!t || !t.triangles) continue;
    const positions = decodeF32(t.vertices_xyz_f32), indices = decodeU32(t.indices_u32);
    if (positions.length / 3 !== t.vertices || indices.length / 3 !== t.triangles) throw new Error(`Wandmeshzaehlung stimmt nicht: ${tile}`);
    const group = new THREE.Group(); group.name = `waende_${tile}`;
    group.userData.ebene = 'waende'; group.userData.kachel = tile; wallRoot.add(group);
    makeMesh(THREE, positions, indices, wallMaterial, `wand_${tile}`, group);
    wallStats[tile] = { features: t.features, vertices: t.vertices, triangles: t.triangles, minWidth: t.min_width_m };
  }
  if (manifest.waende.tiles.D2 && manifest.waende.tiles.D2.triangles !== 0) throw new Error('D2 muss wandfrei bleiben');

  const tileCenter = tile => {
    const b = manifest.tiles[tile].bounds, x = (b[0] + b[2]) / 2, z = (b[1] + b[3]) / 2;
    return [x, H(x, z), z];
  };
  let currentTile = 'D1';
  const setCamera = (p, t) => {
    camera.position.set(...p); controls.target.set(...t); controls.update(); render();
  };
  const focus = tile => {
    currentTile = tile;
    document.querySelectorAll('[data-tile]').forEach(b => b.classList.toggle('sel', b.dataset.tile === tile));
    const [x, y, z] = tileCenter(tile);
    const D1 = tile === 'D1';
    setCamera(D1 ? [x - 16, y + 35, z + 28] : [x - 20, y + 35, z + 28], [x, y, z]);
    const label = document.getElementById('modus');
    if (label) label.textContent = `Kachel ${tile} · Mesh ${tileStats[tile].triangles.toLocaleString('de-DE')} Dreiecke`;
  };
  const light = () => {
    const az = Number(document.getElementById('az')?.value ?? 315) * Math.PI / 180;
    const el = Number(document.getElementById('el')?.value ?? 45) * Math.PI / 180;
    sun.position.set(220 + 430 * Math.cos(el) * Math.sin(az), 430 * Math.sin(el), 160 - 430 * Math.cos(el) * Math.cos(az));
    sun.intensity = Number(document.getElementById('st')?.value ?? 90) / 48;
  };
  document.querySelectorAll('[data-tile]').forEach(b => b.onclick = () => focus(b.dataset.tile));
  document.querySelectorAll('[data-l]').forEach(c => c.onchange = () => {
    if (c.dataset.l === 'gelaende') terrainRoot.visible = c.checked;
    if (c.dataset.l === 'waende') wallRoot.visible = c.checked;
    render();
  });
  ['az', 'el', 'st'].forEach(id => { const e = document.getElementById(id); if (e) e.oninput = () => { light(); render(); }; });
  const presets = {
    schraeg: () => focus(currentTile),
    oben: () => { const [x, y, z] = tileCenter(currentTile); setCamera([x, y + 85, z + 0.1], [x, y, z]); },
    wandfuss: () => setCamera([127, H(127, 44) + 20, 43], [140, 1, 35]),
    D1: () => focus('D1'), G1: () => focus('G1'), D2: () => focus('D2'),
  };
  document.getElementById('reset').onclick = () => presets.schraeg();
  document.getElementById('voben').onclick = () => presets.oben();
  document.getElementById('vwand').onclick = () => presets.wandfuss();

  let frame = 0;
  const render = () => { if (renderer) renderer.render(scene, camera); };
  controls.addEventListener('change', render);
  light();
  const encode = array => {
    const bytes = new Uint8Array(array.buffer, array.byteOffset, array.byteLength);
    let s = ''; for (let i = 0; i < bytes.length; i += 32768) s += String.fromCharCode(...bytes.subarray(i, i + 32768));
    return btoa(s);
  };
  const allTriangles = manifest.lod1.total_triangles;
  window.__szene = scene;
  window.__info = () => ({ lod1_dreiecke: allTriangles, terrain: tileStats, waende: wallStats });
  window.__test = {
    bereit: true, start: DN.start || { x: 147, z: 30 }, wandfuss: { x: 140, z: 35 },
    setModus: mode => { if (mode !== 'neu') throw new Error('Der Kern-Viewer enthaelt nur den neuen Prototyp'); },
    setView: name => (presets[name] || presets.schraeg)(),
    kam: (p, t) => setCamera(p, t), H,
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
  const queryTile = new URLSearchParams(location.search).get('tile');
  if (queryTile && presets[queryTile]) focus(queryTile); else focus('D1');
  if (renderer && !/[?&]manual=1/.test(location.search)) renderer.setAnimationLoop(() => { controls.update(); render(); });
  render();
  const loading = document.getElementById('lade');
  if (loading) {
    if (renderer) loading.remove();
    else loading.textContent = 'WebGL nicht verfuegbar; Meshdaten fuer Pruefungen geladen.';
  }
  window.addEventListener('resize', () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); if (renderer) renderer.setSize(innerWidth, innerHeight); render(); });
  return { scene, camera, renderer, tileStats, wallStats, totalTriangles: allTriangles };
}
