// NODE_PATH=/tmp/w3/node_modules node feld/test_feld.js OUTJSON BILDDIR datei1.html ... (Env: VW,VH,QS)
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [oj,bd,...dat]=process.argv.slice(2);fs.mkdirSync(bd,{recursive:true});const R=[];
const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
for(const f of dat){const p=await b.newPage({viewport:{width:+(process.env.VW||1280),height:+(process.env.VH||800)}});const err=[];
 p.on('pageerror',e=>err.push('pageerror: '+e.message));p.on('console',m=>{if(m.type()=='error')err.push('console: '+m.text())});
 const t0=Date.now();let ok=true;try{await p.goto('file://'+f+(process.env.QS||''));await p.waitForFunction(()=>window.__test&&window.__test.bereit&&!document.getElementById('lade'),null,{timeout:120000,polling:100});}catch(e){ok=false;err.push('timeout/'+e.message.slice(0,200));}
 const sek=(Date.now()-t0)/1000;await p.waitForTimeout(1500);
 const info=ok?await p.evaluate(()=>({...window.__info(),feld:window.__feld,lod:window.__lod})):null;
 const n=f.split('/').pop().replace('.html','');try{await p.screenshot({path:`${bd}/${n}${process.env.SUF||''}.png`,timeout:300000});}catch(e){err.push('screenshot: '+e.message.slice(0,100));}
 R.push({datei:f.split('/').pop(),mb:+(fs.statSync(f).size/1e6).toFixed(2),ladezeit_s:sek,fehler:err,info});console.log(JSON.stringify(R[R.length-1]));await p.close();}
await b.close();fs.writeFileSync(oj,JSON.stringify(R,null,1));})();
