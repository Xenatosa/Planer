// t39u Prototyp-Welt Viewer. Alle Objekte = PLATZHALTER, aus Daten gesetzt (gen_welt3d.py).
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
const $=id=>document.getElementById(id);
async function daten(){const b=Uint8Array.from(atob(window.WELT_GZ),c=>c.charCodeAt(0));
 const s=new Blob([b]).stream().pipeThrough(new DecompressionStream('gzip'));return JSON.parse(await new Response(s).text());}
const f32=s=>new Float32Array(Uint8Array.from(atob(s),c=>c.charCodeAt(0)).buffer);
const u8=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
(async()=>{
const D=await daten(),NX=D.nx,NY=D.ny,E=f32(D.E),Eo=f32(D.Eo),WA=u8(D.wasser);
const sp={};for(const c of D.reihenfolge){const k=D.spalten[c],r=u8(k.i);sp[c]={w:k.w,i:k.t=='uint8'?r:k.t=='uint16'?new Uint16Array(r.buffer):new Uint32Array(r.buffer)};}
const H=(x,z)=>{x=Math.min(Math.max(x,0),NX-0.001);z=Math.min(Math.max(z,0),NY-0.001);const i=x|0,j=z|0,fx=x-i,fz=z-j,W=NX+1;
 return E[j*W+i]*(1-fx)*(1-fz)+E[j*W+i+1]*fx*(1-fz)+E[(j+1)*W+i]*(1-fx)*fz+E[(j+1)*W+i+1]*fx*fz;};
const ren=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});ren.setPixelRatio(Math.min(devicePixelRatio,2));
ren.setSize(innerWidth,innerHeight);ren.shadowMap.enabled=true;document.body.appendChild(ren.domElement);
const sc=new THREE.Scene();sc.background=new THREE.Color(0xcad6e4);sc.fog=new THREE.Fog(0xcad6e4,300,900);
const cam=new THREE.PerspectiveCamera(50,innerWidth/innerHeight,0.1,3000);
const oc=new OrbitControls(cam,ren.domElement);oc.enableDamping=true;oc.maxPolarAngle=Math.PI;oc.screenSpacePanning=true;
const amb=new THREE.HemisphereLight(0xffffff,0x667788,0.6);sc.add(amb);
const sun=new THREE.DirectionalLight(0xffffff,1.6);sun.castShadow=true;sun.shadow.bias=-0.0008;sun.shadow.normalBias=0.4;sun.shadow.mapSize.set(4096,4096);
Object.assign(sun.shadow.camera,{left:-260,right:260,top:260,bottom:-260,near:1,far:900});sun.target.position.set(NX/2,0,NY/2);sc.add(sun,sun.target);
const G={};const grp=n=>{G[n]=new THREE.Group();sc.add(G[n]);return G[n]};
// Gelaende
{const W=NX+1,Hh=NY+1,p=new Float32Array(W*Hh*3),uv=new Float32Array(W*Hh*2),ix=[];
 for(let j=0;j<Hh;j++)for(let i=0;i<W;i++){const k=j*W+i;p.set([i,E[k],j],k*3);uv.set([i/NX,1-j/NY],k*2);}
 for(let j=0;j<NY;j++)for(let i=0;i<NX;i++){const a=j*W+i,b=a+1,c=a+W,d=c+1;
  if(Math.abs(E[a]-E[d])<=Math.abs(E[b]-E[c]))ix.push(a,c,d,a,d,b);else ix.push(a,c,b,b,c,d);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(p,3));g.setAttribute('uv',new THREE.BufferAttribute(uv,2));
 g.setIndex(ix);g.computeVertexNormals();const tex=new THREE.TextureLoader().load(window.TEX);tex.colorSpace=THREE.SRGBColorSpace;tex.anisotropy=8;
 const m=new THREE.Mesh(g,new THREE.MeshLambertMaterial({map:tex,side:THREE.DoubleSide}));m.receiveShadow=true;m.castShadow=true;m.name='gelaende';grp('gelaende').add(m);
 // Sockel bis -14 m [A]
 const sp2=[],si=[];const rand=[];for(let i=0;i<=NX;i++)rand.push([i,0]);for(let j=1;j<=NY;j++)rand.push([NX,j]);for(let i=NX-1;i>=0;i--)rand.push([i,NY]);for(let j=NY-1;j>=0;j--)rand.push([0,j]);
 rand.forEach(([i,j],n)=>{sp2.push(i,E[j*W+i],j,i,-14,j);if(n)si.push(2*n-2,2*n-1,2*n,2*n,2*n-1,2*n+1);});
 const sg=new THREE.BufferGeometry();sg.setAttribute('position',new THREE.Float32BufferAttribute(sp2,3));sg.setIndex(si);sg.computeVertexNormals();
 G.gelaende.add(new THREE.Mesh(sg,new THREE.MeshLambertMaterial({color:0x5a4a40,side:THREE.DoubleSide})));
 const bo=new THREE.Mesh(new THREE.PlaneGeometry(NX,NY),new THREE.MeshBasicMaterial({color:0x6a5a4e,side:THREE.DoubleSide}));bo.rotation.x=Math.PI/2;bo.position.set(NX/2,-14,NY/2);G.gelaende.add(bo);const gh=new THREE.GridHelper(Math.max(NX,NY),Math.max(NX,NY)/12|0,0x222222,0x222222);gh.position.set(NX/2,-14.05,NY/2);G.gelaende.add(gh);}
// Wasser
{const p=[],W=NX+1;for(let j=0;j<NY;j++)for(let i=0;i<NX;i++)if(WA[j*NX+i]){const a=j*W+i,q=[[i,j,a],[i,j+1,a+W],[i+1,j+1,a+W+1],[i+1,j,a+1]].map(([x,z,k])=>[x,Eo[k],z]);
 p.push(...q[0],...q[1],...q[2],...q[0],...q[2],...q[3]);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));g.computeVertexNormals();
 grp('wasser').add(new THREE.Mesh(g,new THREE.MeshPhongMaterial({color:0x4a8ec0,transparent:true,opacity:0.65,shininess:80,side:THREE.DoubleSide})));}
// Wege flach + Bruecken
{const p=[];for(const [i,j] of D.wege){const q=[[i,j],[i,j+1],[i+1,j+1],[i+1,j]].map(([x,z])=>[x,H(x,z)+0.06,z]);p.push(...q[0],...q[1],...q[2],...q[0],...q[2],...q[3]);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));g.computeVertexNormals();
 grp('wege').add(new THREE.Mesh(g,new THREE.MeshLambertMaterial({color:0x9c7b55,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2})));
 const bm=new THREE.InstancedMesh(new THREE.BoxGeometry(1,0.25,1),new THREE.MeshLambertMaterial({color:0x7a5230}),D.bruecken.length);
 const o=new THREE.Object3D();D.bruecken.forEach(([x,y,z],n)=>{o.position.set(x,y,z);o.updateMatrix();bm.setMatrixAt(n,o.matrix)});bm.castShadow=true;G.wege.add(bm);}
const inst=(geo,mat,L,fn,gn)=>{const m=new THREE.InstancedMesh(geo,mat,L.length),o=new THREE.Object3D();L.forEach((e,n)=>{fn(o,e);o.updateMatrix();m.setMatrixAt(n,o.matrix)});m.castShadow=m.receiveShadow=true;(G[gn]||grp(gn)).add(m);return m;};
// Baeume: Stamm + 2 Kegel
{const st=new THREE.CylinderGeometry(0.15,0.25,1,6).translate(0,0.5,0),k1=new THREE.ConeGeometry(0.42,0.6,7).translate(0,0.55,0),k2=new THREE.ConeGeometry(0.3,0.45,7).translate(0,0.85,0);
 inst(st,new THREE.MeshLambertMaterial({color:0x5b3b22}),D.baeume,(o,[x,y,z,h])=>{o.position.set(x,y,z);o.scale.set(1,h*0.25,1)},'baeume');
 const nm=new THREE.MeshLambertMaterial({color:0x2f5a46});
 for(const k of[k1,k2])inst(k,nm,D.baeume,(o,[x,y,z,h])=>{o.position.set(x,y,z);o.scale.set(h*0.5,h,h*0.5)},'baeume');}
// Felsen, Findlinge, Deko-Steine
{const geo=new THREE.DodecahedronGeometry(0.5,0).scale(1.2,0.8,1).translate(0,0.3,0),mat=new THREE.MeshLambertMaterial({color:0x8a7f78,flatShading:true});
 for(const L of[D.felsen,D.findlinge,D.steine])inst(geo,mat,L,(o,[x,y,z,h,r])=>{o.position.set(x,y,z);o.rotation.y=r;o.scale.setScalar(h)},'felsen');}
// Haeuser: Quader + Satteldach
{const hmat=new THREE.MeshLambertMaterial({color:0xd9c7a8}),fmat=new THREE.MeshLambertMaterial({color:0xc98a4a}),dmat=new THREE.MeshLambertMaterial({color:0x8a3b2e}),pmat=new THREE.MeshLambertMaterial({color:0xb0a48c});
 const roof=new THREE.BufferGeometry();roof.setAttribute('position',new THREE.Float32BufferAttribute([-.5,0,-.5,.5,0,-.5,0,1,-.5, -.5,0,.5,0,1,.5,.5,0,.5, -.5,0,-.5,0,1,-.5,0,1,.5, -.5,0,-.5,0,1,.5,-.5,0,.5, .5,0,-.5,.5,0,.5,0,1,.5, .5,0,-.5,0,1,.5,0,1,-.5],3));roof.computeVertexNormals();
 grp('gebaeude');const box=new THREE.BoxGeometry(1,1,1).translate(0,0.5,0);
 D.haeuser.forEach(h=>{const platz=h.typ=='Quartiersplatz',m=new THREE.Mesh(box,platz?pmat:h.typ.startsWith('FUNKTION')?fmat:hmat);
  const wh=platz?h.h:h.h*0.7;m.position.set(h.x,h.y,h.z);m.scale.set(h.b*0.9,wh,h.t*0.9);m.castShadow=m.receiveShadow=true;m.userData.haus=h;G.gebaeude.add(m);
  if(!platz){const r=new THREE.Mesh(roof,dmat);r.position.set(h.x,h.y+wh,h.z);r.scale.set(h.b*0.95,h.h*0.3,h.t*0.95);if(h.b>h.t){r.rotation.y=Math.PI/2;r.scale.set(h.t*0.95,h.h*0.3,h.b*0.95);}r.castShadow=true;r.userData.haus=h;G.gebaeude.add(r);}});}
// Referenzmensch 1,8 m
{const s=D.start,x=s.x+s.b/2+2,z=s.z;const m=new THREE.Mesh(new THREE.CapsuleGeometry(0.25,1.3,4,8).translate(0,0.9,0),new THREE.MeshLambertMaterial({color:0xe02020}));
 m.position.set(x,H(x,z),z);m.castShadow=true;m.userData.mensch=1;grp('mensch').add(m);}
// Licht
const licht=()=>{const az=$('az').value*Math.PI/180,el=$('el').value*Math.PI/180;sun.position.set(NX/2+400*Math.cos(el)*Math.sin(az),400*Math.sin(el),NY/2-400*Math.cos(el)*Math.cos(az));sun.intensity=$('st').value/50;};
['az','el','st'].forEach(i=>$(i).oninput=licht);licht();
document.querySelectorAll('[data-l]').forEach(c=>c.onchange=()=>G[c.dataset.l].visible=c.checked);
// Ansichten
const V={schraeg:[[NX/2,260,NY+170],[NX/2,0,NY/2]],oben:[[NX/2,520,NY/2+0.1],[NX/2,0,NY/2]],unten:[[NX/2,-260,NY/2+180],[NX/2,-14,NY/2]],nord:[[NX/2,90,-150],[NX/2,0,NY/2]]};
let geh=false,yaw=0,pitch=0;const setView=n=>{geh=false;oc.enabled=true;const [p,t]=V[n];cam.position.set(...p);oc.target.set(...t);oc.update();};
const boden=(x,z,yw)=>{geh=true;oc.enabled=false;yaw=yw;pitch=0;cam.position.set(x,H(x,z)+1.7,z);};
$('reset').onclick=()=>setView('schraeg');$('vunten').onclick=()=>setView('unten');$('voben').onclick=()=>setView('oben');
$('gehen').onclick=()=>{if(geh)setView('schraeg');else boden(D.start.x+6,D.start.z+8,0);};
setView('schraeg');
const keys={};onkeydown=e=>keys[e.key.toLowerCase()]=1;onkeyup=e=>keys[e.key.toLowerCase()]=0;
let drag=null;ren.domElement.addEventListener('pointerdown',e=>drag=[e.clientX,e.clientY,e.clientX,e.clientY]);
ren.domElement.addEventListener('pointermove',e=>{if(geh&&drag){yaw-=(e.clientX-drag[0])*0.005;pitch=Math.max(-1.4,Math.min(1.4,pitch-(e.clientY-drag[1])*0.005));drag[0]=e.clientX;drag[1]=e.clientY;}});
ren.domElement.addEventListener('pointerup',e=>{if(drag&&Math.hypot(e.clientX-drag[2],e.clientY-drag[3])<4)klick(e.clientX,e.clientY);drag=null;});
// Klick-Info
const rc=new THREE.Raycaster(),mk=new THREE.Mesh(new THREE.BoxGeometry(1,0.3,1),new THREE.MeshBasicMaterial({color:0xff00ff,wireframe:true}));sc.add(mk);mk.visible=false;
function zelle(cx,cy){const i=cy*NX+cx,o={};for(const c of D.reihenfolge)o[c]=sp[c].w[sp[c].i[i]];return o;}
function klick(sx,sy){rc.setFromCamera(new THREE.Vector2(sx/innerWidth*2-1,-sy/innerHeight*2+1),cam);
 const ziele=[...G.gebaeude.children,...G.mensch.children,G.gelaende.children[0]].filter(o=>o.parent.visible);const h=rc.intersectObjects(ziele)[0];let txt='nichts getroffen',res=null;
 if(h&&h.object.userData.haus){const u=h.object.userData.haus;res={art:'gebaeude',...u};txt=`<b>Gebäude-Platzhalter E40</b>\nid ${u.id} · ${u.typ}\n${u.b}×${u.t} m, Höhe ${u.h} m [A]`;}
 else if(h&&h.object.userData.mensch){res={art:'mensch'};txt='<b>Referenzfigur</b> 1,8 m';}
 else if(h){const cx=Math.min(NX-1,Math.floor(h.point.x)),cy=Math.min(NY-1,Math.floor(h.point.z));const z=zelle(cx,cy);res={art:'zelle',...z};
  mk.position.set(cx+0.5,H(cx+0.5,cy+0.5)+0.15,cy+0.5);mk.visible=true;txt='<b>Zelle '+z.zell_id+'</b>\n'+Object.entries(z).map(([k,v])=>k+': '+v).join('\n');}
 $('info').innerHTML=txt;window.__letzterKlick=res;return res;}
window.__test={setView,boden,klick,start:D.start,haus0:D.haeuser.find(h=>h.typ.startsWith('FUNKTION:Kaserne')),klickWelt:(x,y,z)=>{const v=new THREE.Vector3(x,y,z).project(cam);return klick((v.x+1)/2*innerWidth,(1-v.y)/2*innerHeight);},bereit:true,zaehl:{haeuser:D.haeuser.length,baeume:D.baeume.length}};
let t0=performance.now();ren.setAnimationLoop(()=>{const t=performance.now(),dt=Math.min(0.1,(t-t0)/1000);t0=t;
 if(geh){const v=(keys.shift?12:4)*dt,f=new THREE.Vector3(-Math.sin(yaw),0,-Math.cos(yaw)),r=new THREE.Vector3(-f.z,0,f.x);
  if(keys.w)cam.position.addScaledVector(f,v);if(keys.s)cam.position.addScaledVector(f,-v);if(keys.d)cam.position.addScaledVector(r,v);if(keys.a)cam.position.addScaledVector(r,-v);
  cam.position.y=H(cam.position.x,cam.position.z)+1.7;cam.rotation.set(pitch,yaw,0,'YXZ');}else oc.update();ren.render(sc,cam);});
onresize=()=>{cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix();ren.setSize(innerWidth,innerHeight);};
$('lade').remove();})().catch(e=>{document.body.insertAdjacentHTML('beforeend','<pre style="color:red">'+e.stack+'</pre>');throw e;});
