// O17 B: Viewer-Szene (lod=0, ohne Wege-Overlay) als JSON-Dump fuer blender_paket_o17.py. NODE_PATH=/tmp/w3/node_modules OUT=x.json node pruefung/blender_dump_o17.js [A]
const E=process.env,{chromium}=require('playwright'),path=require('path'),fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1024,height:640}});p.on('pageerror',e=>console.log('PAGEERROR',e.message));
await p.goto('file://'+path.resolve(E.HTML||'index.html')+'?lod=0');
await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:300000});
const r=await p.evaluate(()=>JSON.stringify(window.__test.dump()));fs.writeFileSync(E.OUT||'/tmp/dump.json',r);await b.close();})();
