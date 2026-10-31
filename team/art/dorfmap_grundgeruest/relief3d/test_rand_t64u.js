// t64u: Randschlitz Gelaende-Randkante <-> Sockel-Oberkante im Viewer messen. node test_rand_t64u.js "file://.../index.html?lod=2"
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1280,height:800}});await p.goto(process.argv[2]);
await p.waitForFunction(()=>window.__test&&window.__test.bereit&&window.__RK,null,{timeout:600000});
const r=await p.evaluate(()=>{const out={},ST=8,NX=336,NY=303;for(const sd of['n','s','w','o']){
 const T=__RK.filter(([k])=>k[0]==sd).map(([k,y])=>[+k.slice(1)/ST,y]).sort((a,b)=>a[0]-b[0]);
 const S=__sockelTop.filter(([x,y,z])=>sd=='n'?Math.abs(z)<1e-6:sd=='s'?Math.abs(z-NY)<1e-6:sd=='w'?Math.abs(x)<1e-6:Math.abs(x-NX)<1e-6).map(([x,y,z])=>[(sd=='n'||sd=='s')?x:z,y]).sort((a,b)=>a[0]-b[0]);
 const ip=(L,t)=>{let lo=0,hi=L.length-1;if(t<=L[0][0])return L[0][1];if(t>=L[hi][0])return L[hi][1];while(hi-lo>1){const m=(lo+hi)>>1;if(L[m][0]<=t)lo=m;else hi=m;}const a=L[lo],c=L[hi];return a[1]+(c[1]-a[1])*(t-a[0])/(c[0]-a[0]);};
 let mn=0,mx=0,n2=0,wo=null;const chk=(t,d)=>{if(d<mn)mn=d;if(d>mx){mx=d;wo=t;}if(Math.abs(d)>0.02)n2++;};
 for(const[t,y]of T)chk(t,y-ip(S,t));for(const[t,y]of S)chk(t,ip(T,t)-y);
 out[{n:'nord',s:'sued',w:'west',o:'ost'}[sd]]={gelaende_punkte:T.length,sockel_punkte:S.length,min_m:+mn.toFixed(4),max_m:+mx.toFixed(4),punkte_gt_2cm:n2,max_bei:wo};}
 return out;});console.log(JSON.stringify(r));await b.close();})();
