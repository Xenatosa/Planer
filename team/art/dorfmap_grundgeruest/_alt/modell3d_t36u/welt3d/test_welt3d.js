// Headless-Test: node test_welt3d.js (NODE_PATH=/tmp/w3/node_modules)
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1280,height:800}});const fehler=[];
p.on('pageerror',e=>fehler.push('pageerror '+e.message));p.on('console',m=>{if(m.type()=='error')fehler.push('console '+m.text())});
await p.goto('file://'+path.resolve('index.html'));await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:120000});
const shot=async(n,f)=>{await p.evaluate(f);await p.waitForTimeout(1500);await p.screenshot({path:'test/'+n+'_v2.png'});};
await shot('w1_schraeg',()=>__test.setView('schraeg'));await shot('w2_oben',()=>__test.setView('oben'));
await shot('w3_unten',()=>__test.setView('unten'));await shot('w4_nord_rueckseite',()=>__test.setView('nord'));
const s=await p.evaluate(()=>window.__test);
await shot('w5_boden_dorf',()=>{const s=__test.start;__test.boden(s.x+8,s.z+14,0.3)});
await shot('w6_boden_wald',()=>__test.boden(30,200,1.2));
await p.evaluate(()=>__test.setView('oben'));await p.waitForTimeout(800);
const k1=await p.evaluate(()=>__test.klick(innerWidth/2,innerHeight/2));
await p.screenshot({path:'test/w7_klick_info_v2.png'});
// Gebaeude-Klick: Kamera auf Starthaus
await p.evaluate(()=>__test.setView('schraeg'));await p.waitForTimeout(500);
const k2=await p.evaluate(()=>{const h=__test.haus0;return __test.klickWelt(h.x,h.y+h.h*0.4,h.z)});await p.screenshot({path:'test/w8_klick_gebaeude_v2.png'});
const r={fehler,klick_mitte:k1?{art:k1.art,zell_id:k1.zell_id,untergrund:k1.untergrund,felder:Object.keys(k1).length}:null,klick_gebaeude:k2};
console.log(JSON.stringify(r,null,1));require('fs').writeFileSync('test/test_ergebnis.json',JSON.stringify(r,null,1));await b.close();})();
