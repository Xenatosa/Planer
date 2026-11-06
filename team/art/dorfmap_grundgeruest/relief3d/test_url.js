// Misst eine URL (z. B. Handy-LOD oder GLB-Pfad): NODE_PATH=/tmp/w3/node_modules node test_url.js "http://localhost:8000/index.html?lod=1" out.png [breite hoehe] [ansicht]
const {chromium}=require('playwright');
(async()=>{const [u,o,w,h,v]=process.argv.slice(2);const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:+(w||1280),height:+(h||800)}});const t0=Date.now();await p.goto(u);
await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:300000});const lade=Date.now()-t0;
await p.evaluate(v=>{__test.setModus('neu');__test.setView(v)},v||'schraeg');await p.waitForTimeout(4000);await p.screenshot({path:o,timeout:600000});
console.log(JSON.stringify({url:u,lade_ms:lade,info:await p.evaluate(()=>window.__info&&__info()),glb:await p.evaluate(()=>window.__glb||null),lod:await p.evaluate(()=>window.__lod||1),felsbloecke:await p.evaluate(()=>window.__felsbloecke)}));await b.close();})();
