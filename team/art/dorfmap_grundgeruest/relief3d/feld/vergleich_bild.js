// Vergleichsbild: Hauptviewer (index.html?lod=1) vs Feld-HTML, gleiche Kamera (Feld-Startkamera). 
// NODE_PATH=/tmp/w3/node_modules node feld/vergleich_bild.js index.html feld.html out_prefix
const {chromium}=require('playwright');
(async()=>{const [main,feld,out]=process.argv.slice(2);const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const vp={width:1024,height:640};let kam=null;
for(const [f,q,n] of [[feld,'','feld'],[main,'?lod=1','haupt']]){const p=await b.newPage({viewport:vp});await p.goto('file://'+f+q);
 await p.waitForFunction(()=>window.__test&&window.__test.bereit&&!document.getElementById('lade'),null,{timeout:600000});
 if(!kam)kam=await p.evaluate(()=>{const F=window.FELD,cx=(F.x0+F.x1)/2,cz=(F.z0+F.z1)/2,h=__test.H(cx,cz),S=Math.max(F.x1-F.x0,F.z1-F.z0);return [[cx,h+S*1.25,cz+S*1.45],[cx,h,cz]];});
 await p.evaluate(k=>{__test.kam(k[0],k[1]);document.querySelectorAll('body > div').forEach(e=>e.style.visibility='hidden');for(const n of ['feld_umriss','feld_rand']){const o=window.__sc.getObjectByName(n);if(o)o.visible=false;}},kam);
 await p.waitForTimeout(2500);await p.screenshot({path:`${out}_${n}.png`,timeout:600000});await p.close();console.log('ok',n);}
await b.close();})();
