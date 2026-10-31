// t64u Lochsuche: nur Gelaende sichtbar, Hintergrund magenta, Nebel aus; eingeschlossene Magenta-Flecken = Durchblick [A]
// NODE_PATH=/tmp/w3/node_modules HTML=index.html Q='?lod=1' OUT=dir CAMS='[[name,[p],[t]],..]' node test_loch_t64u.js
const E=process.env,CAMS=JSON.parse(require('fs').readFileSync(E.CAMS,'utf8'));const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:+(E.W||960),height:+(E.H||600)}});
await p.goto('file://'+path.resolve(E.HTML||'index.html')+(E.Q||''));await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:300000});
await p.evaluate(()=>__test.setModus('neu'));
await p.evaluate(()=>window.__loch());const res=[];
for(const [n,a,t] of CAMS){await p.evaluate(([a,t])=>__test.kam(a,t),[a,t]);await p.evaluate(()=>window.__loch());await p.waitForTimeout(400);
 const f=OUT=>OUT;const file=(E.OUT||'.')+'/'+n+'.png';await p.screenshot({path:file,timeout:600000});res.push(file);}
console.log(JSON.stringify({n:res.length,lod:await p.evaluate(()=>window.__lod)}));await b.close();})();
