// O18g Lochsuche: offene Kanten (nur 1 Dreieck) aller Gelaende-Meshes, global verschweisst 2 cm, ohne Kartenrand/Feldrand.
// HTML=index.html OUT=x.json RAND=0.6 node pruefung/loch_o18g.js
const E=process.env,{chromium}=require('playwright'),path=require('path'),fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage();await p.goto('file://'+path.resolve(E.HTML||'index.html')+(E.Q||''));
await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:300000});
const r=await p.evaluate((R)=>{const ms=[];__szene.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||!o.visible)return;let e='';for(let q=o;q;q=q.parent)if(q.userData&&q.userData.ebene){e=q.userData.ebene;break}if(e=='gelaende')ms.push(o)});
 const key=(x,y,z)=>Math.round(x*50)+','+Math.round(y*50)+','+Math.round(z*50);const E=new Map();let x0=1e9,x1=-1e9,z0=1e9,z1=-1e9,nt=0;const v=new (ms[0].position.constructor)();
 for(const m of ms){m.updateMatrixWorld();const g=m.geometry,P=g.attributes.position,I=g.index;const n=I?I.count:P.count;const K=[],W=[];
  for(let i=0;i<P.count;i++){v.fromBufferAttribute(P,i).applyMatrix4(m.matrixWorld);K.push(key(v.x,v.y,v.z));W.push([v.x,v.y,v.z]);x0=Math.min(x0,v.x);x1=Math.max(x1,v.x);z0=Math.min(z0,v.z);z1=Math.max(z1,v.z)}
  const gr=g.groups&&g.groups.length?g.groups:[{start:0,count:n}];
  for(const G of gr)for(let t=G.start;t<G.start+G.count;t+=3){nt++;const a=[0,1,2].map(j=>I?I.getX(t+j):t+j);
   if(K[a[0]]==K[a[1]]||K[a[1]]==K[a[2]]||K[a[0]]==K[a[2]])continue;
   for(let j=0;j<3;j++){const u=a[j],w=a[(j+1)%3];const k=K[u]<K[w]?K[u]+'|'+K[w]:K[w]+'|'+K[u];const e=E.get(k);if(e)e.n++;else E.set(k,{n:1,p:[(W[u][0]+W[w][0])/2,(W[u][1]+W[w][1])/2,(W[u][2]+W[w][2])/2]})}}}
 const L=[];for(const e of E.values())if(e.n==1){const [x,y,z]=e.p;if(x<x0+R||x>x1-R||z<z0+R||z>z1-R)continue;L.push(e.p.map(q=>+q.toFixed(2)))}
 return {meshes:ms.length,dreiecke:nt,offen_innen:L.length,bb:[x0,z0,x1,z1].map(q=>+q.toFixed(1)),punkte:L}},+(E.RAND||0.6));
console.log(JSON.stringify({...r,punkte:r.punkte.length}));if(E.OUT)fs.writeFileSync(E.OUT,JSON.stringify(r));await b.close();})();
