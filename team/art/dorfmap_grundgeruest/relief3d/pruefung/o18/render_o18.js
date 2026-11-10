// O18: Kameraliste rendern. NODE_PATH=/tmp/w3/node_modules node pruefung/o18/render_o18.js index.html OUTDIR cams.json [query] [w h]
// cams.json: [{n,pos:[x,y,z],ziel:[x,y,z]}]  (Weltkoord. x=cx, z=cy, y=Hoehe; pos/ziel y relativ zu __test.H wenn 'rel':1)
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const [html,out,cf,q='',w='1400',h='900']=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});
const cams=JSON.parse(fs.readFileSync(cf));const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:+w,height:+h}});await p.goto('file://'+path.resolve(html)+q);
await p.waitForFunction(()=>window.__test&&window.__test.bereit&&!document.getElementById('lade'),null,{timeout:600000});
await p.evaluate(()=>{try{__test.setModus('neu')}catch(e){};document.querySelectorAll('body > div').forEach(e=>e.style.visibility='hidden')});
for(const c of cams){await p.evaluate(c=>{const P=c.pos.slice(),Z=c.ziel.slice();if(c.rel){const hz=__test.H(Z[0],Z[2]);P[1]+=hz;Z[1]+=hz;}__test.kam(P,Z);if(c.az!=null){for(const[k,v]of[['az',c.az],['el',c.el],['st',c.st||60]]){const e=document.getElementById(k);e.value=v;e.dispatchEvent(new Event('input'))}}},c);   // O18q: Licht je Kamera (az/el/st)
 await p.waitForTimeout(1800);await p.screenshot({path:`${out}/${c.n}.png`,timeout:600000});console.log('ok',c.n);}
await b.close();})();
