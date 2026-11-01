// t64u Lochsuche (Kopie t61u, LOCH=1 -> __loch(): Magenta-Hintergrund, nur Gelaende, UI aus): NODE_PATH=/tmp/w3/node_modules HTML=index.html Q='?clay=1' OUT=dir SUF=x CAMS='[["name",[px,py,pz],[tx,ty,tz]],...]' node test_nah_t61u.js
const E=process.env,HTML=E.HTML||'index.html',SUF=E.SUF||'t61u',OUT=E.OUT||'test',CAMS=JSON.parse(E.CAMS);
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:+(E.W||1280),height:+(E.H||800)}});const fehler=[];p.on('pageerror',e=>fehler.push(e.message));
await p.goto('file://'+path.resolve(HTML)+(E.Q||''));await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:180000});
await p.evaluate(()=>__test.setModus('neu'));if(E.HIDE)await p.evaluate(h=>{for(const l of h.split(',')){const c=document.querySelector(`input[data-l=${l}]`);if(c&&c.checked)c.click();}},E.HIDE);
if(E.LOCH)await p.evaluate(()=>{__loch();for(const e of document.body.querySelectorAll('*'))if(e.tagName!='CANVAS'&&!e.querySelector('canvas'))e.style.display='none';});
for(const [n,a,t] of CAMS){await p.evaluate(([a,t])=>__test.kam(a,t),[a,t]);await p.waitForTimeout(1200);await p.screenshot({path:OUT+'/'+n+'_'+SUF+'.png',timeout:600000});}
console.log(JSON.stringify({fehler,lod:await p.evaluate(()=>window.__lod)}));await b.close();})();
