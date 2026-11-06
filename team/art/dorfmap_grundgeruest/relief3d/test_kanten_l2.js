// O10 L2: Kantenzaehlung je Gelaende-Mesh: offene Kanten, >2 Nutzer, doppelte Dreiecke, Faltungen (Nachbarnormalen dot<-0.2), Rueckseiten (Normal.y<0) nahe Problemstellen
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:400,height:300}});await p.goto(process.argv[2]);await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:300000});
const S=[['rand_ost_80',335.5,80.75],['rand_ost_265',335.5,265.75],['wand_264_24',277.5,28.2]];
console.log(JSON.stringify(await p.evaluate(S=>{const out=[];let gi=0;__szene.traverse(o=>{if(!o.isMesh||o.isInstancedMesh)return;let n='';for(let q=o;q&&!n;q=q.parent)n=q.name||(q.userData&&q.userData.ebene)||'';if(n!='gelaende')return;
o.updateMatrixWorld();const P=o.geometry.attributes.position,I=o.geometry.index;const nt=(I?I.count:P.count)/3;const ix=k=>I?I.getX(k):k;
// Positionen schweissen (1 mm), damit Naehte zwischen Teilnetzen sichtbar werden
const key=[],m=new Map();const W=[];const pos=[];for(let i=0;i<P.count;i++){const x=P.getX(i),y=P.getY(i),z=P.getZ(i);const k=Math.round(x*1000)+','+Math.round(y*1000)+','+Math.round(z*1000);let id=m.get(k);if(id===undefined){id=m.size;m.set(k,id);pos.push([x,y,z])}W.push(id)}
const E=new Map(),T=new Map();let dup=0,degen=0,neg=0;const tn=[];const near=S.map(()=>({offen:0,mehr2:0,falt:0,neg:0,degen:0}));
const nearI=c=>{for(let s=0;s<S.length;s++){if(Math.abs(c[0]-S[s][1])<12&&Math.abs(c[2]-S[s][2])<12)return s}return -1};
const ctr=[];for(let t=0;t<nt;t++){const a=W[ix(3*t)],b2=W[ix(3*t+1)],c=W[ix(3*t+2)];const A=pos[a],B=pos[b2],C=pos[c];const u=[B[0]-A[0],B[1]-A[1],B[2]-A[2]],w=[C[0]-A[0],C[1]-A[1],C[2]-A[2]];const N=[u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0]];const l=Math.hypot(...N);tn.push(l?N.map(x=>x/l):[0,0,0]);const cc=[(A[0]+B[0]+C[0])/3,(A[1]+B[1]+C[1])/3,(A[2]+B[2]+C[2])/3];ctr.push(cc);const s=nearI(cc);
if(l<1e-6){degen++;if(s>=0)near[s].degen++}if(l&&N[1]/l<0){neg++;if(s>=0)near[s].neg++}
const tk=[a,b2,c].sort((x,y)=>x-y).join();if(T.has(tk))dup++;T.set(tk,1);for(const [x,y] of [[a,b2],[b2,c],[c,a]]){const ek=x<y?x+'_'+y:y+'_'+x;if(!E.has(ek))E.set(ek,[]);E.get(ek).push(t)}}
let offen=0,mehr2=0,falt=0;const fp=[];for(const [ek,ts] of E){const pp=ek.split('_').map(Number);const mc=[(pos[pp[0]][0]+pos[pp[1]][0])/2,0,(pos[pp[0]][2]+pos[pp[1]][2])/2];const s=nearI(mc);if(ts.length==1){offen++;if(s>=0)near[s].offen++}if(ts.length>2){mehr2++;if(s>=0)near[s].mehr2++}if(ts.length==2){const A=tn[ts[0]],B=tn[ts[1]];if(A[0]*B[0]+A[1]*B[1]+A[2]*B[2]<-0.2){falt++;if(fp.length<4000)fp.push([+mc[0].toFixed(1),+mc[2].toFixed(1),+(A[1].toFixed(2)),+(B[1].toFixed(2))]);if(s>=0)near[s].falt++}}}
out.push({fp,mat:o.material.type,ud:JSON.stringify(o.userData).slice(0,80),mesh:gi++,name:o.name,tri:nt,offen,mehr2,falt,dup,degen,neg,near})});return out},S),null,0));await b.close();})();
