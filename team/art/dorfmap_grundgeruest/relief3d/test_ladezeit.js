// Ladezeit headless: NODE_PATH=/tmp/w3/node_modules node test_ladezeit.js /pfad/datei.html [n]
const {chromium}=require('playwright');
(async()=>{const f=process.argv[2],n=+(process.argv[3]||3),r=[];
for(let k=0;k<n;k++){const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1280,height:800}});const t0=Date.now();await p.goto('file://'+f);
await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:300000,polling:100});r.push((Date.now()-t0)/1000);await b.close();}
console.log(JSON.stringify({datei:f,sek:r,median:r.slice().sort((a,b)=>a-b)[r.length>>1]}));})();
