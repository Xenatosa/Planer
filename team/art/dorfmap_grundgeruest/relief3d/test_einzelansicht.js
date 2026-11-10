const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1000,height:700}});await p.goto('file://'+path.resolve(process.argv[2]));
await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:180000});
await p.evaluate(()=>{__test.setModus('neu');__test.setView('fluss_ost')});await p.waitForTimeout(1500);await p.screenshot({path:process.argv[3],timeout:600000});await b.close();})();
