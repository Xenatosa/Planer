// Headless-Test: NODE_PATH=/tmp/w3/node_modules node test_relief.js  -> test/*_t42u.png, test/test_ergebnis.json
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1280,height:800}});const fehler=[];
p.on('pageerror',e=>fehler.push('pageerror '+e.message));p.on('console',m=>{if(m.type()=='error')fehler.push('console '+m.text())});
await p.goto('file://'+path.resolve('index.html'));await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:180000});
const shot=async(n,f)=>{await p.evaluate(f);await p.waitForTimeout(1500);await p.screenshot({path:'test/'+n+'_t42u.png'});};
for(const v of ['schraeg','nordwand','krater','suedwand','oben'])for(const m of ['alt','neu'])await shot(`${v}_${m}`,new Function(`__test.setModus('${m}');__test.setView('${v}')`));
for(const m of ['alt','neu'])await shot(`boden_wand_${m}`,new Function(`__test.setModus('${m}');__test.amWand()`));
const hoehen=await p.evaluate(()=>{const w=__test.wandfuss;__test.setModus('neu');const n=[__test.H(w.x,w.z-1.5),__test.H(w.x,w.z+0.5)];__test.setModus('alt');const a=[__test.H(w.x,w.z-6),__test.H(w.x,w.z+0.5)];return{neu_oben_unten:n,alt_6m_noerdlich_unten:a};});
await p.evaluate(()=>{__test.setModus('neu');__test.setView('nordwand')});await p.waitForTimeout(800);
const k1=await p.evaluate(()=>{const w=__test.wandfuss;return __test.klickWelt(w.x,__test.H(w.x,w.z)+6,w.z-0.02)});
await p.screenshot({path:'test/klick_wand_t42u.png'});
await p.evaluate(()=>__test.setView('schraeg'));await p.waitForTimeout(500);
const k2=await p.evaluate(()=>{const h=__test.haus0;return __test.klickWelt(h.x,h.y+h.h*0.4,h.z)});
const dr=await p.evaluate(()=>window.__dreiecke);const r={fehler,dreiecke:dr,hoehen,klick_wand:k1?{art:k1.art,zell_id:k1.zell_id,klippe:k1.klippe,klippe_hoehe_m:k1.klippe_hoehe_m,felder:Object.keys(k1).length}:null,klick_gebaeude:k2?{art:k2.art,id:k2.id}:null};
console.log(JSON.stringify(r,null,1));require('fs').writeFileSync('test/test_ergebnis.json',JSON.stringify(r,null,1));await b.close();})();
