// P10 Einstieg: entpackt das Meshpaket aller 56 Kacheln und startet den Kachel-Viewer.
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import {renderAlleKacheln} from './viewer_alle.js';
const $ = id => document.getElementById(id);
const gz = async s => { const b = Uint8Array.from(atob(s), c => c.charCodeAt(0));
  return JSON.parse(await new Response(new Blob([b]).stream().pipeThrough(new DecompressionStream('gzip'))).text()); };
const stufe = async t => { const l = $('lade'); if (l) l.textContent = 'Lade … ' + t; await new Promise(r => setTimeout(r, 0)); };
const fehler = e => { const l = $('lade'); const t = 'Fehler beim Laden: ' + (e && e.message || e) + '\n' + (e && e.stack || '');
  window.__fehler = t; if (l) { l.style.cssText += ';white-space:pre-wrap;color:#a00;font:13px monospace'; l.textContent = t; } };
addEventListener('error', ev => fehler(ev.error || ev.message));
addEventListener('unhandledrejection', ev => fehler(ev.reason));
(async () => {
  await stufe('Daten entpacken …');
  const DN = await gz(window.P10_GZ);
  await renderAlleKacheln({ THREE, OrbitControls, DN, stufe });
})();
