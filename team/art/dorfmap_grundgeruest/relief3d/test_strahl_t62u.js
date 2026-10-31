// t62u: Objekte gegen die echte Viewer-Oberflaeche (Raycast) pruefen. NODE_PATH=/tmp/w3/node_modules HTML=index.html Q='' OUT=x.json node test_strahl_t62u.js
const E=process.env,{chromium}=require('playwright'),path=require('path'),fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1280,height:800}});await p.goto('file://'+path.resolve(E.HTML||'index.html')+(E.Q||''));
await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:300000});
const r=await p.evaluate(()=>{const D=window.__daten||null;return null});
const zl=await p.evaluate(()=>{const o={};for(const k of['baeume','felsen','findlinge','steine','geroell'])o[k]=(window.DN||{})[k];return o});
fs.writeFileSync(E.OUT||'strahl.json',JSON.stringify(await p.evaluate(async P=>{const o={};for(const k in P)o[k]=__test.strahl(P[k]);return o},JSON.parse(fs.readFileSync(E.PTS)))));await b.close();})();
