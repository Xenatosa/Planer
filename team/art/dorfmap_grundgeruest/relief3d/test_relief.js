// Headless-Test: NODE_PATH=/tmp/w3/node_modules node test_relief.js  -> test/*_<SUF>.png; Env: HTML (Standard index.html), SUF (t43u), MODI (alt,neu), OUT (test), KURZ=1 nur Bilder
const E=process.env,HTML=E.HTML||'index.html',SUF=E.SUF||'t43u',MODI=(E.MODI||'alt,neu').split(','),OUT=E.OUT||'test';
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1280,height:800}});const fehler=[];
p.on('pageerror',e=>fehler.push('pageerror '+e.message));p.on('console',m=>{if(m.type()=='error')fehler.push('console '+m.text())});
await p.goto('file://'+path.resolve(HTML));await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:180000});
const shot=async(n,f)=>{await p.evaluate(f);await p.waitForTimeout(1500);await p.screenshot({path:OUT+'/'+n+'_'+SUF+'.png',timeout:600000});};
for(const v of (E.VIEWS||'schraeg,nordwand,krater,suedwand,oben,unten,rand,rueck,dorf').split(','))for(const m of MODI)await shot(`${v}_${m}`,new Function(`__test.setModus('${m}');__test.setView('${v}')`));
for(const m of MODI){await shot(`boden_wand_${m}`,new Function(`__test.setModus('${m}');__test.amWand()`));
 await shot(`totale_auge_${m}`,new Function(`__test.setModus('${m}');__test.boden(253,110,0,0.03)`));}
if(E.KURZ){console.log(JSON.stringify({fehler,dreiecke:await p.evaluate(()=>window.__dreiecke),info:await p.evaluate(()=>window.__info&&__info())}));await b.close();return;}
const hoehen=await p.evaluate(()=>{const w=__test.wandfuss;__test.setModus('neu');const n=[__test.H(w.x,w.z-1.5),__test.H(w.x,w.z+0.5)];__test.setModus('alt');const a=[__test.H(w.x,w.z-6),__test.H(w.x,w.z+0.5)];return{neu_oben_unten:n,alt_6m_noerdlich_unten:a};});
await p.evaluate(()=>{__test.setModus('neu');__test.setView('nordwand')});await p.waitForTimeout(800);
const k1=await p.evaluate(()=>{const w=__test.wandfuss;return __test.klickWelt(w.x,__test.H(w.x,w.z)+6,w.z-0.02)});
await p.screenshot({path:OUT+'/klick_wand_'+SUF+'.png'});
await p.evaluate(()=>__test.setView('schraeg'));await p.waitForTimeout(500);
const k2=await p.evaluate(()=>{const h=__test.haus0;return __test.klickWelt(h.x,h.y+h.h*0.4,h.z)});
const dr=await p.evaluate(()=>window.__dreiecke);const r={fehler,dreiecke:dr,hoehen,klick_wand:k1?{art:k1.art,zell_id:k1.zell_id,klippe:k1.klippe,klippe_hoehe_m:k1.klippe_hoehe_m,felder:Object.keys(k1).length}:null,klick_gebaeude:k2?{art:k2.art,id:k2.id}:null};
console.log(JSON.stringify(r,null,1));require('fs').writeFileSync(OUT+'/test_ergebnis.json',JSON.stringify(r,null,1));await b.close();})();
