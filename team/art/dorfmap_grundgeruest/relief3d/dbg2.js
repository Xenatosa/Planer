const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});const p=await b.newPage();
p.goto('file:///tmp/dl/o7.html',{timeout:0}).catch(()=>{});await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:150000,polling:1000});
const u=await p.evaluate(()=>{const {GX,GY,RS,WE,dist}=window.__wdbg,h=window.__hSurf;const o=[];for(let z=262;z<=276;z+=2){let r=[];for(let x=243;x<=269;x+=0.5){const k=Math.round(z*RS)*GX+Math.round(x*RS);r.push((WE[k]-h(x,z)).toFixed(2)+(dist[k]==0?"w":""))}o.push(z+": "+r.join(" "))}return o.join("\n")});console.log(u);await b.close();process.exit(0)})();
