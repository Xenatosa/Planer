// Bytegenau-Pruefung: NODE_PATH=/tmp/w3/node_modules node feld/vergleich_geometrie.js a.html b.html out.json -> dumpt __test.dump() beider Dateien
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [a,b2,o]=process.argv.slice(2);const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});const R={};
for(const f of [a,b2]){const p=await b.newPage({viewport:{width:800,height:600}});await p.goto('file://'+f);await p.waitForFunction(()=>window.__test&&window.__test.bereit&&window.__feld,null,{timeout:300000});R[f]=await p.evaluate(()=>__test.dump());await p.close();}
fs.writeFileSync(o,JSON.stringify(R));await b.close();})();
