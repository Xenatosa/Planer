// Dreiecke je Objektgruppe: NODE_PATH=/tmp/w3/node_modules node test_budget.js "file:///...index.html?lod=1"
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:390,height:844}});await p.goto(process.argv[2]);
await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:300000});await p.evaluate(()=>{__test.setModus('neu');__test.setView('schraeg')});await p.waitForTimeout(3000);
console.log(JSON.stringify(await p.evaluate(()=>{const r={};let s=0;__szene.traverse(o=>{if(!o.isMesh&&!o.isPoints)return;let v=true;for(let q=o;q;q=q.parent)if(!q.visible)v=false;if(!v)return;const g=o.geometry,t=(g.index?g.index.count:g.attributes.position.count)/3*(o.isInstancedMesh?o.count:1);let n=o.name||'';for(let q=o.parent;q&&!n;q=q.parent)n=q.name||(q.userData&&q.userData.ebene)||'';r[n||'?']=(r[n||'?']||0)+t;s+=t;if(o.isInstancedMesh&&n=='felsen')r['inst_'+o.id]=[(g.index?g.index.count:g.attributes.position.count)/3,o.count];});r.summe=s;r.info=__info();return r;}),null,1));await b.close();})();
