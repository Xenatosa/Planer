// O10 L1: echte gerenderte Dreiecke je Frame (renderer.info) im lod=1, mit/ohne Schatten. NODE_PATH=/tmp/w3/node_modules node test_dreiecke_l1.js "file:///...index.html?lod=1"
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});const out={};
for(const q of ['','&nosh=1']){const p=await b.newPage({viewport:{width:390,height:844}});await p.goto(process.argv[2]+q);
await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:300000});await p.evaluate(()=>{__test.setModus('neu');__test.setView('schraeg')});await p.waitForTimeout(3000);
out[q||'mit_schatten']=await p.evaluate(()=>{const r={info:__info()};let cs=0;const g={};__szene.traverse(o=>{if(!o.isMesh)return;let v=true;for(let x=o;x;x=x.parent)if(!x.visible)v=false;if(!v||!o.castShadow)return;const G=o.geometry,t=(G.index?G.index.count:G.attributes.position.count)/3*(o.isInstancedMesh?o.count:1);let n=o.name||'';for(let x=o.parent;x&&!n;x=x.parent)n=x.name||'';g[n]=(g[n]||0)+t;cs+=t});r.schattenwerfer=cs;r.sw_gruppen=g;return r});await p.close();}
console.log(JSON.stringify(out,null,1));await b.close();})();
