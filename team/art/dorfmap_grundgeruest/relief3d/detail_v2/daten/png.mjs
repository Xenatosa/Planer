// Minimaler PNG-Decoder fuer die Datenschicht (ESM, Node + Browser, keine Abhaengigkeiten).
// Unterstuetzt: nicht verschachtelt (interlace 0), Farbtyp 0 (Graustufe) mit 1/8/16 bit
// und Farbtyp 3 (indiziert) mit 8 bit (Rueckgabe = Index). Filter 0-4.
// Ergebnis: {breite, hoehe, bittiefe, farbtyp, daten} mit daten = Uint8Array bzw. Uint16Array (16 bit), zeilenweise.

const SIG = [137, 80, 78, 71, 13, 10, 26, 10];

async function inflate(bytes) {
  if (typeof process !== 'undefined' && process.versions && process.versions.node) {
    const zlib = await import('node:zlib');
    return new Uint8Array(zlib.inflateSync(bytes));
  }
  // Browser: zlib-Strom = 'deflate'
  const ds = new DecompressionStream('deflate');
  const buf = await new Response(new Blob([bytes]).stream().pipeThrough(ds)).arrayBuffer();
  return new Uint8Array(buf);
}

function paeth(a, b, c) {
  const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c);
  return pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
}

export async function decodePng(input) {
  const u8 = input instanceof Uint8Array ? input : new Uint8Array(input);
  for (let i = 0; i < 8; i++) if (u8[i] !== SIG[i]) throw new Error('keine PNG-Datei');
  const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
  let off = 8, breite = 0, hoehe = 0, bittiefe = 0, farbtyp = 0, interlace = 0;
  const idat = [];
  while (off < u8.length) {
    const len = dv.getUint32(off), typ = String.fromCharCode(...u8.subarray(off + 4, off + 8));
    const d = u8.subarray(off + 8, off + 8 + len);
    if (typ === 'IHDR') {
      breite = dv.getUint32(off + 8); hoehe = dv.getUint32(off + 12);
      bittiefe = d[8]; farbtyp = d[9]; interlace = d[12];
    } else if (typ === 'IDAT') idat.push(d);
    else if (typ === 'IEND') break;
    off += 12 + len;
  }
  if (interlace !== 0) throw new Error('Interlace nicht unterstuetzt');
  if (!((farbtyp === 0 && [1, 8, 16].includes(bittiefe)) || (farbtyp === 3 && bittiefe === 8)))
    throw new Error(`PNG-Format nicht unterstuetzt: Farbtyp ${farbtyp}, ${bittiefe} bit`);
  let n = 0; for (const c of idat) n += c.length;
  const z = new Uint8Array(n); n = 0; for (const c of idat) { z.set(c, n); n += c.length; }
  const roh = await inflate(z);
  const bpp = Math.max(1, bittiefe >> 3);            // Byte pro Pixel fuer Filter
  const zb = Math.ceil((breite * bittiefe) / 8);      // Byte pro Zeile
  if (roh.length < hoehe * (zb + 1)) throw new Error('PNG-Daten zu kurz');
  const zeilen = new Uint8Array(hoehe * zb);
  let vor = new Uint8Array(zb);
  for (let y = 0; y < hoehe; y++) {
    const f = roh[y * (zb + 1)], src = roh.subarray(y * (zb + 1) + 1, (y + 1) * (zb + 1));
    const cur = zeilen.subarray(y * zb, (y + 1) * zb);
    for (let i = 0; i < zb; i++) {
      const a = i >= bpp ? cur[i - bpp] : 0, b = vor[i], c = i >= bpp ? vor[i - bpp] : 0;
      let v = src[i];
      if (f === 1) v += a; else if (f === 2) v += b; else if (f === 3) v += (a + b) >> 1;
      else if (f === 4) v += paeth(a, b, c); else if (f !== 0) throw new Error(`Filter ${f}`);
      cur[i] = v & 255;
    }
    vor = cur;
  }
  let daten;
  if (bittiefe === 16) {
    daten = new Uint16Array(breite * hoehe);
    for (let i = 0; i < daten.length; i++) daten[i] = (zeilen[2 * i] << 8) | zeilen[2 * i + 1];
  } else if (bittiefe === 8) daten = zeilen;
  else {
    daten = new Uint8Array(breite * hoehe);
    for (let y = 0; y < hoehe; y++) for (let x = 0; x < breite; x++)
      daten[y * breite + x] = (zeilen[y * zb + (x >> 3)] >> (7 - (x & 7))) & 1;
  }
  return { breite, hoehe, bittiefe, farbtyp, daten };
}
