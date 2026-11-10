// Rendert Kameraliste (JSON: [{name,p:[x,y,z],t:[x,y,z],w,h}]) aus index.html; Karte unveraendert.
// Aufruf: NODE_PATH=/tmp/w3/node_modules node render_kameras.js <index.html> <kameras.json> <outdir> [query]
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const [html,kj,out,q]=process.argv.slice(2);const K=JSON.parse(fs.readFileSync(kj));
const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:K[0].w,height:K[0].h}});
await p.goto('file://'+path.resolve(html)+(q||''));
await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:300000});
await p.evaluate(()=>{__test.setModus('neu');window.__banner=(document.getElementById('modus')||{}).textContent||'';document.querySelectorAll('body > div, #ui, #info, #lade, .panel').forEach(e=>{if(e.tagName!='CANVAS')e.style.visibility='hidden'})});
fs.writeFileSync(out+'/banner.txt',await p.evaluate(()=>window.__banner));
for(const k of K){if(fs.existsSync(out+'/'+k.name+'.png'))continue;
 await p.evaluate(([a,t])=>__test.kam(a,t),[k.p,k.t]);await p.waitForTimeout(1200);
 await p.screenshot({path:out+'/'+k.name+'.png',timeout:600000});console.log('ok',k.name);}
await b.close();})();
