// t41u Viewer: NEU = echtes Relief (gen_relief.py), ALT = t39u-Welt. Alle Objekte PLATZHALTER.
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
const $=id=>document.getElementById(id);
const gz=async s=>{const b=Uint8Array.from(atob(s),c=>c.charCodeAt(0));return JSON.parse(await new Response(new Blob([b]).stream().pipeThrough(new DecompressionStream('gzip'))).text());};
const f32=s=>new Float32Array(Uint8Array.from(atob(s),c=>c.charCodeAt(0)).buffer),u8=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
const spaltenLesen=D=>{const sp={};for(const c of D.reihenfolge){const k=D.spalten[c],r=u8(k.i);sp[c]={w:k.w,i:k.t=='uint8'?r:k.t=='uint16'?new Uint16Array(r.buffer):new Uint32Array(r.buffer)};}return sp;};
(async()=>{
const DN=await gz(window.NEU_GZ),DA=await gz(window.ALT_GZ),NX=DN.nx,NY=DN.ny;
const ren=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});ren.setPixelRatio(Math.min(devicePixelRatio,2));
ren.setSize(innerWidth,innerHeight);ren.shadowMap.enabled=true;document.body.appendChild(ren.domElement);
const sc=new THREE.Scene();sc.background=new THREE.Color(0xcad6e4);sc.fog=new THREE.Fog(0xcad6e4,300,900);
const cam=new THREE.PerspectiveCamera(50,innerWidth/innerHeight,0.1,3000);
const oc=new OrbitControls(cam,ren.domElement);oc.enableDamping=true;oc.maxPolarAngle=Math.PI;oc.screenSpacePanning=true;
sc.add(new THREE.HemisphereLight(0xffffff,0x667788,0.6));
const sun=new THREE.DirectionalLight(0xffffff,1.6);sun.castShadow=true;sun.shadow.bias=-0.0008;sun.shadow.normalBias=0.4;sun.shadow.mapSize.set(4096,4096);
Object.assign(sun.shadow.camera,{left:-260,right:260,top:260,bottom:-260,near:1,far:900});sun.target.position.set(NX/2,0,NY/2);sc.add(sun,sun.target);
const ladeTex=u=>{const t=new THREE.TextureLoader().load(u);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;return t;};
const geo=(p,ix,uv,col)=>{const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));if(uv)g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));if(col)g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));if(ix)g.setIndex(ix);g.computeVertexNormals();return g;};
function sockel(Hrand,tief,root){const sp2=[],si=[],rand=[];for(let i=0;i<=NX;i++)rand.push([i,0]);for(let j=1;j<=NY;j++)rand.push([NX,j]);for(let i=NX-1;i>=0;i--)rand.push([i,NY]);for(let j=NY-1;j>=0;j--)rand.push([0,j]);
 rand.forEach(([i,j],n)=>{sp2.push(i,Hrand(i,j),j,i,tief,j);if(n)si.push(2*n-2,2*n-1,2*n,2*n,2*n-1,2*n+1);});
 root.add(new THREE.Mesh(geo(sp2,si),new THREE.MeshLambertMaterial({color:0x5a4a40,side:THREE.DoubleSide})));
 const bo=new THREE.Mesh(new THREE.PlaneGeometry(NX,NY),new THREE.MeshBasicMaterial({color:0x6a5a4e,side:THREE.DoubleSide}));bo.rotation.x=Math.PI/2;bo.position.set(NX/2,tief,NY/2);root.add(bo);
 const gh=new THREE.GridHelper(Math.max(NX,NY),Math.max(NX,NY)/12|0,0x222222,0x222222);gh.position.set(NX/2,tief-0.05,NY/2);root.add(gh);}
// gemeinsame Objekte (Wege, Bruecken, Baeume, Felsen, Haeuser, Mensch) – Groessen [A] wie t39u
function objekte(D,H,root,mensch){const G={};const grp=n=>{G[n]=new THREE.Group();G[n].userData.ebene=n;root.add(G[n]);return G[n]};
 {const p=[];for(const [i,j] of D.wege){const q=[[i,j],[i,j+1],[i+1,j+1],[i+1,j]].map(([x,z])=>[x,H(Math.min(x,i+0.999),Math.min(z,j+0.999))+0.06,z]);p.push(...q[0],...q[1],...q[2],...q[0],...q[2],...q[3]);}
  grp('wege').add(new THREE.Mesh(geo(p),new THREE.MeshLambertMaterial({color:0x9c7b55,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2})));
  const bm=new THREE.InstancedMesh(new THREE.BoxGeometry(1,0.25,1),new THREE.MeshLambertMaterial({color:0x7a5230}),D.bruecken.length);const o=new THREE.Object3D();D.bruecken.forEach(([x,y,z],n)=>{o.position.set(x,y,z);o.updateMatrix();bm.setMatrixAt(n,o.matrix)});bm.castShadow=true;G.wege.add(bm);}
 const inst=(g,mat,L,fn,gn)=>{const m=new THREE.InstancedMesh(g,mat,L.length),o=new THREE.Object3D();L.forEach((e,n)=>{fn(o,e);o.updateMatrix();m.setMatrixAt(n,o.matrix)});m.castShadow=m.receiveShadow=true;(G[gn]||grp(gn)).add(m);};
 {const st=new THREE.CylinderGeometry(0.15,0.25,1,6).translate(0,0.5,0),k1=new THREE.ConeGeometry(0.42,0.6,7).translate(0,0.55,0),k2=new THREE.ConeGeometry(0.3,0.45,7).translate(0,0.85,0);
  inst(st,new THREE.MeshLambertMaterial({color:0x5b3b22}),D.baeume,(o,[x,y,z,h])=>{o.position.set(x,y,z);o.scale.set(1,h*0.25,1)},'baeume');const nm=new THREE.MeshLambertMaterial({color:0x2f5a46});
  for(const k of[k1,k2])inst(k,nm,D.baeume,(o,[x,y,z,h])=>{o.position.set(x,y,z);o.scale.set(h*0.5,h,h*0.5)},'baeume');}
 {const g=new THREE.DodecahedronGeometry(0.5,0).scale(1.2,0.8,1).translate(0,0.3,0),mat=new THREE.MeshLambertMaterial({color:0x8a7f78,flatShading:true});
  for(const L of[D.felsen,D.findlinge,D.steine])inst(g,mat,L,(o,[x,y,z,h,r])=>{o.position.set(x,y,z);o.rotation.y=r;o.scale.setScalar(h)},'felsen');}
 {const hmat=new THREE.MeshLambertMaterial({color:0xd9c7a8}),fmat=new THREE.MeshLambertMaterial({color:0xc98a4a}),dmat=new THREE.MeshLambertMaterial({color:0x8a3b2e}),pmat=new THREE.MeshLambertMaterial({color:0xb0a48c});
  const roof=geo([-.5,0,-.5,.5,0,-.5,0,1,-.5, -.5,0,.5,0,1,.5,.5,0,.5, -.5,0,-.5,0,1,-.5,0,1,.5, -.5,0,-.5,0,1,.5,-.5,0,.5, .5,0,-.5,.5,0,.5,0,1,.5, .5,0,-.5,0,1,.5,0,1,-.5]);
  grp('gebaeude');const box=new THREE.BoxGeometry(1,1,1).translate(0,0.5,0);
  D.haeuser.forEach(h=>{const platz=h.typ=='Quartiersplatz',m=new THREE.Mesh(box,platz?pmat:h.typ.startsWith('FUNKTION')?fmat:hmat);const wh=platz?h.h:h.h*0.7;
   m.position.set(h.x,h.y,h.z);m.scale.set(h.b*0.9,wh,h.t*0.9);m.castShadow=m.receiveShadow=true;m.userData.haus=h;G.gebaeude.add(m);
   if(!platz){const r=new THREE.Mesh(roof,dmat);r.position.set(h.x,h.y+wh,h.z);r.scale.set(h.b*0.95,h.h*0.3,h.t*0.95);if(h.b>h.t){r.rotation.y=Math.PI/2;r.scale.set(h.t*0.95,h.h*0.3,h.b*0.95);}r.castShadow=true;r.userData.haus=h;G.gebaeude.add(r);}});}
 {const m=new THREE.Mesh(new THREE.CapsuleGeometry(0.25,1.3,4,8).translate(0,0.9,0),new THREE.MeshLambertMaterial({color:0xe02020}));m.position.set(mensch.x,H(mensch.x,mensch.z),mensch.z);m.castShadow=true;m.userData.mensch=1;grp('mensch').add(m);}
 return G;}
const WF=DN.wandfuss,menschPos={x:WF.x,z:WF.z+2};   // Figur 2 m vor dem Nordwand-Fuss
// ---------- ALT (t39u) ----------
const ALT=new THREE.Group();sc.add(ALT);let HA;
{const E=f32(DA.E),Eo=f32(DA.Eo),WA=u8(DA.wasser),W=NX+1;
 HA=(x,z)=>{x=Math.min(Math.max(x,0),NX-0.001);z=Math.min(Math.max(z,0),NY-0.001);const i=x|0,j=z|0,fx=x-i,fz=z-j;return E[j*W+i]*(1-fx)*(1-fz)+E[j*W+i+1]*fx*(1-fz)+E[(j+1)*W+i]*(1-fx)*fz+E[(j+1)*W+i+1]*fx*fz;};
 const p=[],uv=[],ix=[];for(let j=0;j<=NY;j++)for(let i=0;i<=NX;i++){p.push(i,E[j*W+i],j);uv.push(i/NX,1-j/NY);}
 for(let j=0;j<NY;j++)for(let i=0;i<NX;i++){const a=j*W+i,b=a+1,c=a+W,d=c+1;if(Math.abs(E[a]-E[d])<=Math.abs(E[b]-E[c]))ix.push(a,c,d,a,d,b);else ix.push(a,c,b,b,c,d);}
 const m=new THREE.Mesh(geo(p,ix,uv),new THREE.MeshLambertMaterial({map:ladeTex(window.TEX),side:THREE.DoubleSide}));m.receiveShadow=m.castShadow=true;m.userData.boden=1;
 const g=new THREE.Group();g.userData.ebene='gelaende';g.add(m);ALT.add(g);sockel((i,j)=>E[j*W+i],-14,g);
 const q=[];for(let j=0;j<NY;j++)for(let i=0;i<NX;i++)if(WA[j*NX+i]){const a=j*W+i,v=[[i,j,a],[i,j+1,a+W],[i+1,j+1,a+W+1],[i+1,j,a+1]].map(([x,z,k])=>[x,Eo[k],z]);q.push(...v[0],...v[1],...v[2],...v[0],...v[2],...v[3]);}
 const wg=new THREE.Group();wg.userData.ebene='wasser';wg.add(new THREE.Mesh(geo(q),new THREE.MeshPhongMaterial({color:0x4a8ec0,transparent:true,opacity:0.65,shininess:80,side:THREE.DoubleSide})));ALT.add(wg);
 objekte(DA,HA,ALT,menschPos);}
// ---------- NEU (Relief t42u: glattes 0,5-m-Hoehenfeld, c20-Draufsicht als Bodentextur, Waende mit Wandtextur) ----------
const NEU=new THREE.Group();sc.add(NEU);const G=f32(DN.G),WV=f32(DN.WV),RS=DN.rs,GX=NX*RS+1,GY=NY*RS+1,COSW=Math.cos(DN.wandwinkel*Math.PI/180);
const HN=(x,z)=>{x=Math.min(Math.max(x*RS,0),GX-1.001);z=Math.min(Math.max(z*RS,0),GY-1.001);const i=x|0,j=z|0,fx=x-i,fz=z-j,k=j*GX+i;
 return G[k]*(1-fx)*(1-fz)+G[k+1]*fx*(1-fz)+G[k+GX]*(1-fx)*fz+G[k+GX+1]*fx*fz;};
{const p=new Float32Array(GX*GY*3),uv=new Float32Array(GX*GY*2);for(let j=0;j<GY;j++)for(let i=0;i<GX;i++){const k=j*GX+i;p.set([i/RS,G[k],j/RS],k*3);uv.set([i/RS/NX,1-j/RS/NY],k*2);}
 const bi=[],wp=[],wu=[];const V=k=>[p[k*3],p[k*3+1],p[k*3+2]];
 const tri=(a,b,c)=>{const A=V(a),B=V(b),C2=V(c),u=[B[0]-A[0],B[1]-A[1],B[2]-A[2]],v=[C2[0]-A[0],C2[1]-A[1],C2[2]-A[2]];
  const n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],l=Math.hypot(...n);
  if(Math.abs(n[1])/l>=COSW-1e-7){bi.push(a,b,c);return;}
  const ax=Math.abs(n[0])>Math.abs(n[2]);for(const P of[A,B,C2]){wp.push(...P);wu.push((ax?P[2]:P[0])/4,P[1]/8);}};
 for(let j=0;j<GY-1;j++)for(let i=0;i<GX-1;i++){const a=j*GX+i,b=a+1,c=a+GX,d=c+1;tri(a,c,d);tri(a,d,b);}
 const gb=new THREE.BufferGeometry();gb.setAttribute('position',new THREE.BufferAttribute(p,3));gb.setAttribute('uv',new THREE.BufferAttribute(uv,2));gb.setIndex(bi);gb.computeVertexNormals();
 const m=new THREE.Mesh(gb,new THREE.MeshLambertMaterial({map:ladeTex(window.RTEX),side:THREE.DoubleSide}));m.receiveShadow=m.castShadow=true;m.userData.boden=1;
 const g=new THREE.Group();g.userData.ebene='gelaende';g.add(m);NEU.add(g);
 const wt=ladeTex(window.WANDTEX);wt.wrapS=wt.wrapT=THREE.RepeatWrapping;
 const wm=new THREE.Mesh(geo(wp,null,wu),new THREE.MeshLambertMaterial({map:wt,side:THREE.DoubleSide}));wm.castShadow=wm.receiveShadow=true;wm.name='felswand';wm.userData.boden=1;g.add(wm);
 window.__dreiecke={boden:bi.length/3,wand:wp.length/9};
 sockel((i,j)=>HN(i,j),-30,g);
 const q=[];const wv=(i,j)=>WV[j*GX+i];for(let j=0;j<GY-1;j++)for(let i=0;i<GX-1;i++){const a=wv(i,j),b=wv(i+1,j),c=wv(i,j+1),d=wv(i+1,j+1);
  if(a>-900&&b>-900&&c>-900&&d>-900)q.push(i/RS,a,j/RS,i/RS,c,(j+1)/RS,(i+1)/RS,d,(j+1)/RS,i/RS,a,j/RS,(i+1)/RS,d,(j+1)/RS,(i+1)/RS,b,j/RS);}
 const wg=new THREE.Group();wg.userData.ebene='wasser';const wmesh=new THREE.Mesh(geo(q),new THREE.MeshPhongMaterial({color:0x4a8ec0,transparent:true,opacity:0.7,shininess:80,side:THREE.DoubleSide}));wmesh.receiveShadow=true;wg.add(wmesh);NEU.add(wg);
 objekte(DN,HN,NEU,menschPos);}
// ---------- Umschalter, Ebenen, Licht ----------
let modus='neu';const SP={alt:spaltenLesen(DA),neu:spaltenLesen(DN)};const Hf=()=>modus=='neu'?HN:HA;
const setModus=m=>{modus=m;ALT.visible=m=='alt';NEU.visible=m=='neu';$('modus').textContent=m=='neu'?'Ansicht: NEU (Relief t42u)':'Ansicht: ALT (t39u)';if(geh)cam.position.y=Hf()(cam.position.x,cam.position.z)+1.7;};
$('balt').onclick=()=>setModus('alt');$('bneu').onclick=()=>setModus('neu');
const ebSicht=()=>document.querySelectorAll('[data-l]').forEach(c=>[ALT,NEU].forEach(R=>R.children.forEach(g=>{if(g.userData.ebene==c.dataset.l)g.visible=c.checked;})));
document.querySelectorAll('[data-l]').forEach(c=>c.onchange=ebSicht);
const licht=()=>{const az=$('az').value*Math.PI/180,el=$('el').value*Math.PI/180;sun.position.set(NX/2+400*Math.cos(el)*Math.sin(az),400*Math.sin(el),NY/2-400*Math.cos(el)*Math.cos(az));sun.intensity=$('st').value/50;};
['az','el','st'].forEach(i=>$(i).oninput=licht);licht();
const V={schraeg:[[NX/2,260,NY+170],[NX/2,0,NY/2]],oben:[[NX/2,520,NY/2+0.1],[NX/2,0,NY/2]],unten:[[NX/2,-260,NY/2+180],[NX/2,-14,NY/2]],nord:[[NX/2,90,-150],[NX/2,0,NY/2]],
 nordwand:[[WF.x+10,40,WF.z+90],[WF.x,6,WF.z-5]],krater:[[160,70,230],[108,4,150]],suedwand:[[170,40,300],[170,-8,225]]};
let geh=false,yaw=0,pitch=0;const setView=n=>{geh=false;oc.enabled=true;const [p,t]=V[n];cam.position.set(...p);oc.target.set(...t);oc.update();};
const boden=(x,z,yw,pt=0)=>{geh=true;oc.enabled=false;yaw=yw;pitch=pt;cam.position.set(x,Hf()(x,z)+1.7,z);cam.rotation.set(pitch,yaw,0,'YXZ');};
const amWand=()=>boden(WF.x+3,WF.z+15,0.12,0.3);
$('reset').onclick=()=>setView('schraeg');$('vunten').onclick=()=>setView('unten');$('voben').onclick=()=>setView('oben');$('vwand').onclick=amWand;
$('gehen').onclick=()=>{if(geh)setView('schraeg');else boden(DN.start.x+6,DN.start.z+8,0);};
setView('schraeg');
const keys={};onkeydown=e=>keys[e.key.toLowerCase()]=1;onkeyup=e=>keys[e.key.toLowerCase()]=0;
let drag=null;ren.domElement.addEventListener('pointerdown',e=>drag=[e.clientX,e.clientY,e.clientX,e.clientY]);
ren.domElement.addEventListener('pointermove',e=>{if(geh&&drag){yaw-=(e.clientX-drag[0])*0.005;pitch=Math.max(-1.4,Math.min(1.4,pitch-(e.clientY-drag[1])*0.005));drag[0]=e.clientX;drag[1]=e.clientY;}});
ren.domElement.addEventListener('pointerup',e=>{if(drag&&Math.hypot(e.clientX-drag[2],e.clientY-drag[3])<4)klick(e.clientX,e.clientY);drag=null;});
const rc=new THREE.Raycaster(),mk=new THREE.Mesh(new THREE.BoxGeometry(1,0.3,1),new THREE.MeshBasicMaterial({color:0xff00ff,wireframe:true}));sc.add(mk);mk.visible=false;
function zelle(cx,cy){const sp=SP[modus],D=modus=='neu'?DN:DA,i=cy*NX+cx,o={};for(const c of D.reihenfolge)o[c]=sp[c].w[sp[c].i[i]];return o;}
function klick(sx,sy){rc.setFromCamera(new THREE.Vector2(sx/innerWidth*2-1,-sy/innerHeight*2+1),cam);const R=modus=='neu'?NEU:ALT,ziele=[];
 R.traverseVisible(o=>{if(o.isMesh&&(o.userData.haus||o.userData.mensch||o.userData.boden))ziele.push(o)});const h=rc.intersectObjects(ziele,false)[0];let txt='nichts getroffen',res=null;
 if(h&&h.object.userData.haus){const u=h.object.userData.haus;res={art:'gebaeude',...u};txt=`<b>Gebäude-Platzhalter E40</b>\nid ${u.id} · ${u.typ}\n${u.b}×${u.t} m, Höhe ${u.h} m [A]`;}
 else if(h&&h.object.userData.mensch){res={art:'mensch'};txt='<b>Referenzfigur</b> 1,8 m';}
 else if(h){const n=h.face.normal.clone().transformDirection(h.object.matrixWorld),pt=h.point.clone().addScaledVector(n,-0.05);
  const cx=Math.min(NX-1,Math.max(0,Math.floor(pt.x))),cy=Math.min(NY-1,Math.max(0,Math.floor(pt.z)));const z=zelle(cx,cy);res={art:h.object.name=='felswand'?'felswand':'zelle',...z};
  mk.position.set(cx+0.5,Hf()(cx+0.5,cy+0.5)+0.15,cy+0.5);mk.visible=true;txt=(res.art=='felswand'?'<b>Felswand</b> an ':'')+'<b>Zelle '+z.zell_id+'</b> ('+modus+')\n'+Object.entries(z).map(([k,v])=>k+': '+v).join('\n');}
 $('info').innerHTML=txt;window.__letzterKlick=res;return res;}
window.__test={setView,boden,amWand,setModus,klick,start:DN.start,wandfuss:WF,haus0:DN.haeuser.find(h=>h.typ.startsWith('FUNKTION:Kaserne')),
 klickWelt:(x,y,z)=>{const v=new THREE.Vector3(x,y,z).project(cam);return klick((v.x+1)/2*innerWidth,(1-v.y)/2*innerHeight);},H:(x,z)=>Hf()(x,z),bereit:true};
setModus('neu');
let t0=performance.now();ren.setAnimationLoop(()=>{const t=performance.now(),dt=Math.min(0.1,(t-t0)/1000);t0=t;
 if(geh){const v=(keys.shift?12:4)*dt,f=new THREE.Vector3(-Math.sin(yaw),0,-Math.cos(yaw)),r=new THREE.Vector3(-f.z,0,f.x);
  if(keys.w)cam.position.addScaledVector(f,v);if(keys.s)cam.position.addScaledVector(f,-v);if(keys.d)cam.position.addScaledVector(r,v);if(keys.a)cam.position.addScaledVector(r,-v);
  cam.position.y=Hf()(cam.position.x,cam.position.z)+1.7;cam.rotation.set(pitch,yaw,0,'YXZ');}else oc.update();ren.render(sc,cam);});
onresize=()=>{cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix();ren.setSize(innerWidth,innerHeight);};
$('lade').remove();})().catch(e=>{document.body.insertAdjacentHTML('beforeend','<pre style="color:red">'+e.stack+'</pre>');throw e;});
