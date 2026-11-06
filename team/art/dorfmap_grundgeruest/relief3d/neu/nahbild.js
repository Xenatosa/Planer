// Deterministic PNG close-up metrics. Uses only Node built-ins (zlib/fs/path).
// These are image proxies for comparison, not a substitute for visual review.
'use strict';
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

function decodePng(file) {
  const buf = fs.readFileSync(file);
  if (buf.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') throw new Error(`Not PNG: ${file}`);
  let width = 0, height = 0, depth = 0, type = 0, interlace = 0;
  const ids = [];
  for (let off = 8; off < buf.length;) {
    const n = buf.readUInt32BE(off), name = buf.toString('ascii', off + 4, off + 8), data = buf.subarray(off + 8, off + 8 + n);
    if (name === 'IHDR') { width = data.readUInt32BE(0); height = data.readUInt32BE(4); depth = data[8]; type = data[9]; interlace = data[12]; }
    if (name === 'IDAT') ids.push(data);
    off += n + 12;
    if (name === 'IEND') break;
  }
  if (depth !== 8 || interlace !== 0 || ![2, 6].includes(type)) throw new Error(`Unsupported PNG encoding ${depth}/${type}/${interlace}: ${file}`);
  const channels = type === 6 ? 4 : 3, stride = width * channels;
  const raw = zlib.inflateSync(Buffer.concat(ids));
  const pix = Buffer.alloc(height * stride);
  for (let y = 0; y < height; y++) {
    const filter = raw[y * (stride + 1)];
    const src = y * (stride + 1) + 1, dst = y * stride;
    for (let x = 0; x < stride; x++) {
      const a = x >= channels ? pix[dst + x - channels] : 0;
      const b = y ? pix[dst + x - stride] : 0;
      const c = y && x >= channels ? pix[dst + x - stride - channels] : 0;
      let value = raw[src + x];
      if (filter === 1) value += a;
      else if (filter === 2) value += b;
      else if (filter === 3) value += Math.floor((a + b) / 2);
      else if (filter === 4) {
        const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c);
        value += pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
      } else if (filter !== 0) throw new Error(`Bad PNG filter ${filter}: ${file}`);
      pix[dst + x] = value & 255;
    }
  }
  const rgb = new Uint8Array(width * height * 3), lum = new Float32Array(width * height), ground = new Uint8Array(width * height);
  for (let i = 0, j = 0; i < width * height; i++, j += channels) {
    const r = pix[j], g = pix[j + 1], b = pix[j + 2], k = i * 3;
    rgb[k] = r; rgb[k + 1] = g; rgb[k + 2] = b;
    lum[i] = 0.299 * r + 0.587 * g + 0.114 * b;
    // The blue-dominant sky/fog is excluded. Clay surfaces are neutral; texture
    // backgrounds are blue, while land, vegetation, roads and objects remain.
    ground[i] = (b - r <= 24 || g - r < 9 || r > 180) ? 1 : 0;
  }
  return { width, height, rgb, lum, ground };
}

function components(mask, width, height, minSize, maxSize) {
  const n = width * height, seen = new Uint8Array(n), queue = new Int32Array(n);
  let count = 0, pixels = 0;
  for (let start = 0; start < n; start++) {
    if (!mask[start] || seen[start]) continue;
    let head = 0, tail = 0;
    queue[tail++] = start; seen[start] = 1;
    while (head < tail) {
      const at = queue[head++], x = at % width, y = (at / width) | 0;
      if (x && mask[at - 1] && !seen[at - 1]) { seen[at - 1] = 1; queue[tail++] = at - 1; }
      if (x + 1 < width && mask[at + 1] && !seen[at + 1]) { seen[at + 1] = 1; queue[tail++] = at + 1; }
      if (y && mask[at - width] && !seen[at - width]) { seen[at - width] = 1; queue[tail++] = at - width; }
      if (y + 1 < height && mask[at + width] && !seen[at + width]) { seen[at + width] = 1; queue[tail++] = at + width; }
    }
    if (tail >= minSize && tail <= maxSize) { count++; pixels += tail; }
  }
  return { count, pixels };
}

function boxMean(src, w, h, radius) {
  const stride = w + 1, integral = new Float64Array((w + 1) * (h + 1));
  for (let y = 1; y <= h; y++) {
    let row = 0;
    for (let x = 1; x <= w; x++) { row += src[(y - 1) * w + x - 1]; integral[y * stride + x] = integral[(y - 1) * stride + x] + row; }
  }
  const out = new Float32Array(w * h);
  for (let y = 0; y < h; y++) {
    const y0 = Math.max(0, y - radius), y1 = Math.min(h, y + radius + 1);
    for (let x = 0; x < w; x++) {
      const x0 = Math.max(0, x - radius), x1 = Math.min(w, x + radius + 1);
      const sum = integral[y1 * stride + x1] - integral[y0 * stride + x1] - integral[y1 * stride + x0] + integral[y0 * stride + x0];
      out[y * w + x] = sum / ((y1 - y0) * (x1 - x0));
    }
  }
  return out;
}

function measure(file) {
  const { width: w, height: h, lum, ground } = decodePng(file), n = w * h;
  const gx = new Float32Array(n), gy = new Float32Array(n), jump = new Uint8Array(n);
  let groundPixels = 0, strongJumps = 0, teeth = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const i = y * w + x;
    if (ground[i]) groundPixels++;
    if (x + 1 < w && ground[i] && ground[i + 1]) {
      gx[i] = lum[i + 1] - lum[i];
      const a = Math.abs(gx[i]);
      if (a >= 24) { jump[i] = 1; strongJumps++; }
      if (a >= 9 && i >= 2 && Math.abs(gx[i - 1]) >= 9 && gx[i] * gx[i - 1] < 0) teeth++;
    }
    if (y + 1 < h && ground[i] && ground[i + w]) {
      gy[i] = lum[i + w] - lum[i];
      const a = Math.abs(gy[i]);
      if (a >= 24) { jump[i] = 1; strongJumps++; }
      if (a >= 9 && i >= 2 * w && Math.abs(gy[i - w]) >= 9 && gy[i] * gy[i - w] < 0) teeth++;
    }
  }
  const lumaMean = boxMean(lum, w, h, 4), dark = new Uint8Array(n), bright = new Uint8Array(n);
  for (let i = 0; i < n; i++) {
    if (!ground[i]) continue;
    const residual = lum[i] - lumaMean[i];
    if (residual < -28) dark[i] = 1;
    if (residual > 28) bright[i] = 1;
  }
  const holes = components(dark, w, h, 3, 1800), flecks = components(bright, w, h, 3, 1800);
  let facets = 0, patchCount = 0;
  const patch = 12;
  for (let y0 = 0; y0 + patch <= h; y0 += patch) for (let x0 = 0; x0 + patch <= w; x0 += patch) {
    let valid = 0, sx = 0, sy = 0, sxx = 0, syy = 0, mag = 0, samples = 0;
    for (let y = y0; y < y0 + patch; y++) for (let x = x0; x < x0 + patch; x++) {
      const i = y * w + x;
      if (ground[i]) valid++;
      if (x + 1 < w && y + 1 < h && ground[i] && ground[i + 1] && ground[i + w]) {
        const a = gx[i], b = gy[i]; sx += a; sy += b; sxx += a * a; syy += b * b; mag += Math.hypot(a, b); samples++;
      }
    }
    if (valid < patch * patch * 0.88 || samples < patch * patch * 0.55) continue;
    patchCount++;
    const vx = Math.max(0, sxx / samples - (sx / samples) ** 2), vy = Math.max(0, syy / samples - (sy / samples) ** 2), mean = mag / samples;
    if (mean >= 0.35 && mean <= 22 && vx + vy <= 3.0) facets++;
  }
  const jumpRuns = components(jump, w, h, 2, n).count;
  return {
    pixel: { width: w, height: h }, ground_pixel: groundPixels,
    kantenzaehne: teeth,
    facetten: facets,
    normale_spruenge: strongJumps,
    normale_sprung_inseln: jumpRuns,
    loecher: holes.count,
    loch_pixel: holes.pixels,
    flecken: flecks.count,
    fleck_pixel: flecks.pixels,
    loch_flecken: holes.count + flecks.count,
    patches_geprueft: patchCount,
  };
}

function parseArgs(argv) {
  if (argv[0] === '--files') {
    const outAt = argv.indexOf('--out');
    if (outAt < 0 || !argv[outAt + 1]) throw new Error('Usage: nahbild.js --files image.png ... --out werte.json');
    const files = argv.slice(1, outAt).filter(x => x !== '--out');
    return { files, out: argv[outAt + 1] };
  }
  return { root: argv[0], out: argv[1] };
}

function listPng(root) {
  const result = [];
  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const p = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(p);
      else if (/\.png$/i.test(entry.name)) result.push(p);
    }
  }
  walk(root);
  return result;
}

function names(file, root) {
  const rel = root ? path.relative(root, file) : file;
  const parts = rel.split(path.sep), base = path.basename(file, '.png');
  const m = /^([A-H][1-7])_(.+)$/.exec(base);
  return { tile: m ? m[1] : null, camera: m ? m[2] : base, mode: root ? parts[0] : null };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const root = args.root ? path.resolve(args.root) : null;
  const files = args.files || listPng(root);
  const images = files.map(file => ({
    ...names(path.resolve(file), root),
    datei: root ? path.relative(root, path.resolve(file)) : file,
    ...measure(file),
  }));
  images.sort((a, b) => `${a.tile}/${a.mode}/${a.camera}/${a.datei}`.localeCompare(`${b.tile}/${b.mode}/${b.camera}/${b.datei}`));
  const result = { schema: 'nahbild-v1', hinweis: 'Bildzahlen sind deterministische Sichtindikatoren; stets mit den gespeicherten Bildern pruefen.', bilder: images.length, images };
  fs.writeFileSync(args.out, JSON.stringify(result, null, 2) + '\n');
  process.stdout.write(JSON.stringify({ bilder: images.length, datei: args.out }) + '\n');
}

if (require.main === module) main();
module.exports = { decodePng, measure, components };
