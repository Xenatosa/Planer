// P10b: Nahbild fuer eine gegebene Stelle (QA/Kritiker).
// Aufruf (im Ordner relief3d), Beispiele siehe README:
//   NODE_PATH=/tmp/w3/node_modules node pruefung/alle_kacheln/nahbild.js --kachel C3 --out /tmp/p10b/c3.png
//   NODE_PATH=/tmp/w3/node_modules node pruefung/alle_kacheln/nahbild.js --xz 147.5,30 --abstand 30 --azimut 0 --neigung 35 --out /tmp/p10b/stelle.png
// Optionen: --html (Standard /tmp/p10b/alle_kacheln.html) --kachel K | --xz X,Z  --abstand m (78.6)
//   --azimut Grad Blickrichtung (0=Nord/-z, 90=Ost/+x, 180=Sued, 270=West; Standard 35.54)
//   --neigung Grad unter Horizont (90=senkrecht; Standard 45.5) --breite 1024 --hoehe 768
//   --dir <ordner> (Ausgabeordner, ersetzt den Ordner von --out/Listenpfaden)
//   --param 'naht=0&sbias=0&snbias=0' (Viewer-Parameter, Vorher-Bilder)
//   --ohne wasser,wege,waende  --clay  --nur-kacheln C3,D3 (schneller laden)  --kein-rand  --titel "Text"
//   --liste datei.json  (Array von {kachel|x,z,abstand,azimut,neigung,out,titel} -> mehrere Bilder in einem Lauf)
const { chromium } = require('playwright'), path = require('path'), fs = require('fs');
const a = process.argv.slice(2), opt = {};
for (let i = 0; i < a.length; i++) { if (!a[i].startsWith('--')) continue; const k = a[i].slice(2); const v = (a[i + 1] && !a[i + 1].startsWith('--')) ? a[++i] : true; opt[k] = v; }
const zahl = (v, d) => v === undefined ? d : +v;
const auftrag = o => {
  const r = { abstand: zahl(o.abstand, 78.6), azimut: zahl(o.azimut, 35.54), neigung: zahl(o.neigung, 45.5), rand: !o['kein-rand'] && o.rand !== false };
  if (o.kachel) r.kachel = String(o.kachel).toUpperCase();
  else if (o.xz) { const [x, z] = String(o.xz).split(/[,|]/).map(Number); r.x = x; r.z = z; }
  else if (o.x !== undefined) { r.x = +o.x; r.z = +o.z; }
  else throw new Error('--kachel oder --xz X,Z angeben');
  if (!o.out) throw new Error('--out <datei.png> angeben');
  if (path.resolve(o.dir || o.out).startsWith('/tmp/w3') || path.resolve(o.out).startsWith('/tmp/w3')) throw new Error('Ausgabe nach /tmp/w3 gesperrt');
  return { blick: r, out: o.dir ? path.join(o.dir, path.basename(o.out)) : o.out, titel: o.titel };
};
(async () => {
  const liste = opt.liste ? JSON.parse(fs.readFileSync(opt.liste, 'utf8')).map(o => auftrag({ ...opt, ...o })) : [auftrag(opt)];
  const html = path.resolve(opt.html || '/tmp/p10b/alle_kacheln.html');
  const qs = ['manual=1'];
  if (opt.clay) qs.push('clay=1');
  if (opt.ohne) qs.push('ohne=' + opt.ohne);
  if (opt['nur-kacheln']) qs.push('kacheln=' + opt['nur-kacheln']);
  if (opt.param) qs.push(...String(opt.param).split('&').filter(Boolean)); // z. B. --param 'naht=0&sbias=0'
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: zahl(opt.breite, 1024), height: zahl(opt.hoehe, 768) } });
  const t0 = Date.now();
  await p.goto('file://' + html + '?' + qs.join('&'));
  await p.waitForFunction(() => (window.__test && window.__test.bereit) || window.__fehler, null, { timeout: 300000 });
  const fehler = await p.evaluate(() => window.__fehler || null);
  if (fehler) throw new Error(fehler);
  await p.addStyleTag({ content: '#p,#info{display:none!important}#nbl{position:absolute;left:10px;top:8px;z-index:9;font:bold 22px system-ui;color:#fff;text-shadow:0 0 4px #000,0 0 2px #000}' });
  await p.evaluate(() => { window.__test.stopRender(); const d = document.createElement('div'); d.id = 'nbl'; document.body.appendChild(d); });
  const log = [];
  for (const j of liste) {
    const info = await p.evaluate(([bl, titel]) => { const r = window.__test.blick(bl);
      document.getElementById('nbl').textContent = titel || `${r.kachel} · Ziel ${r.ziel[0]}|${r.ziel[2]} · Az ${bl.azimut}° · Neig ${bl.neigung}° · ${bl.abstand} m`;
      window.__test.renderOnce(); return r; }, [j.blick, j.titel]);
    fs.mkdirSync(path.dirname(path.resolve(j.out)), { recursive: true });
    await p.screenshot({ path: j.out });
    log.push({ out: j.out, ...info });
  }
  console.log(JSON.stringify({ html, ladezeit_s: null, bilder: log, gesamt_s: (Date.now() - t0) / 1000 }));
  await b.close();
})().catch(e => { console.error(String(e && e.stack || e)); process.exit(2); });
