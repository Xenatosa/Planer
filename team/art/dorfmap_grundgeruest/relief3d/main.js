import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
// t41u Viewer: NEU = echtes Relief (gen_relief.py), ALT = t39u-Welt. Alle Objekte PLATZHALTER.
import * as THREE from 'three';
import {objekteNeu} from './objekte_neu.js';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
const $=id=>document.getElementById(id);
const gz=async s=>{const b=Uint8Array.from(atob(s),c=>c.charCodeAt(0));return JSON.parse(await new Response(new Blob([b]).stream().pipeThrough(new DecompressionStream('gzip'))).text());};
const f32=s=>new Float32Array(Uint8Array.from(atob(s),c=>c.charCodeAt(0)).buffer),u8=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
const hash=(a,b)=>{const v=Math.sin(a*12.9898+b*78.233)*43758.5453;return v-Math.floor(v);};
const spaltenLesen=D=>{const sp={};for(const c of D.reihenfolge){const k=D.spalten[c],r=u8(k.i);sp[c]={w:k.w,i:k.t=='uint8'?r:k.t=='uint16'?new Uint16Array(r.buffer):new Uint32Array(r.buffer)};}return sp;};
(async()=>{
const DN=await gz(window.NEU_GZ),DA=await gz(window.ALT_GZ),NX=DN.nx,NY=DN.ny;
const ren=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});ren.setPixelRatio(Math.min(devicePixelRatio,2));
ren.setSize(innerWidth,innerHeight);ren.shadowMap.enabled=!/[?&]nosh=1/.test(location.search);ren.shadowMap.type=THREE.PCFShadowMap;ren.toneMapping=THREE.ACESFilmicToneMapping;ren.toneMappingExposure=1.0;document.body.appendChild(ren.domElement);
const sc=new THREE.Scene();{const c=document.createElement('canvas');c.width=2;c.height=256;const x=c.getContext('2d'),g=x.createLinearGradient(0,0,0,256);g.addColorStop(0,'#5d8fc9');g.addColorStop(0.55,'#a9c6e4');g.addColorStop(1,'#dfe8ef');x.fillStyle=g;x.fillRect(0,0,2,256);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;sc.background=t;}sc.fog=new THREE.FogExp2(0xc9d8e6,0.0007);window.__sc=sc;window.__loch=()=>{sc.background=new THREE.Color(1,0,1);sc.fog=null;sc.traverse(o=>{if(!(o.isMesh||o.isLine||o.isPoints||o.isSprite))return;let e='';for(let q=o;q;q=q.parent)if(q.userData&&q.userData.ebene){e=q.userData.ebene;break}o.visible=(e=='gelaende')&&!o.isInstancedMesh;});};   // t64u Lochsuche-Hook [A]
   // t43u leichter Dunst [A]
{const NA=360,NR=30,R0=120,R1=2600,pos=[],col=[],idx=[],H=[];   // t53u: ferne Berge als echtes Hoehenfeld-Ring (Volumen, Grate, Taeler) statt Papierband [A]
 const rn=(a,b)=>{const v=Math.sin(a*12.9898+b*78.233)*43758.5453;return v-Math.floor(v);},vn=(x,y)=>{const i=Math.floor(x),j=Math.floor(y),fx=x-i,fy=y-j,u=fx*fx*(3-2*fx),w=fy*fy*(3-2*fy);return (rn(i,j)*(1-u)+rn(i+1,j)*u)*(1-w)+(rn(i,j+1)*(1-u)+rn(i+1,j+1)*u)*w;};
 const rid=(x,y)=>{let s=0,am=1,f=1;for(let o=0;o<4;o++){const v=1-Math.abs(vn(x*f,y*f)*2-1);s+=Math.pow(v,1.4+o*0.4)*am;am*=0.5;f*=2.03;}return s;};
 for(let j=0;j<=NR;j++)for(let i=0;i<=NA;i++){const a=i/NA*Math.PI*2,t=j/NR,R=R0+(R1-R0)*t,ii=i%NA,px=Math.cos(a)*R/170,py=Math.sin(a)*R/170;
  const tt=Math.max(0,(t-0.30)/0.70),env=Math.pow(Math.sin(Math.PI*Math.min(1,tt*1.1)),0.9),h=-40+env*(25+150*rid(px*0.8+3,py*0.8+7)*(0.45+0.8*vn(a*2.2,1)));H.push(h);pos.push(168+Math.cos(a)*R,h,151+Math.sin(a)*R);}
 const W=NA+1;for(let j=0;j<=NR;j++)for(let i=0;i<=NA;i++){const k=j*W+i,hl=H[j*W+Math.max(i-1,0)],hr=H[j*W+Math.min(i+1,NA)],hi=H[Math.max(j-1,0)*W+i],ho=H[Math.min(j+1,NR)*W+i];
  const a=i/NA*Math.PI*2,R=R0+(R1-R0)*j/NR,da=R*2*Math.PI/NA,dr=(R1-R0)/NR,gx=(hr-hl)/(2*da),gr=(ho-hi)/(2*dr),sl=Math.hypot(gx,gr);
  const ta=[-Math.sin(a),Math.cos(a)],ra=[Math.cos(a),Math.sin(a)],nx=-(gx*ta[0]+gr*ra[0]),nz=-(gx*ta[1]+gr*ra[1]),nl=Math.hypot(nx,1,nz),lit=Math.max(0,(nx*0.55+1*0.6+nz*0.35)/nl/0.9);
  const sn=Math.min(1,Math.max(0,(H[k]-105)/45))*Math.min(1,Math.max(0,1.2-sl*2.6));const fe=[0.36,0.35,0.36],wi=[0.86,0.88,0.91];
  let c=[0,1,2].map(q=>(fe[q]*(1-sn)+wi[q]*sn)*(0.55+0.55*lit));const hz=[0.80,0.86,0.92],d=0.18+0.45*j/NR+0.25*Math.max(0,1-(H[k]+40)/120);c=c.map((v,q)=>v*(1-Math.min(1,d))+hz[q]*Math.min(1,d));col.push(...c);
  if(i<NA&&j<NR)idx.push(k,k+W,k+1,k+1,k+W,k+W+1);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));g.setIndex(idx);
 const m=new THREE.Mesh(g,new THREE.MeshBasicMaterial({vertexColors:true,side:THREE.DoubleSide,fog:false,toneMapped:false}));m.name='ferneBerge';window.__fb=m;sc.add(m);}
const cam=new THREE.PerspectiveCamera(50,innerWidth/innerHeight,0.1,3000);
const SWON=/[?&]softwater=1/.test(location.search),SWH=(Math.min(innerWidth,innerHeight)<700||/lod=1/.test(location.search))?0.5:1;/* O5: Handy halbe Aufloesung Tiefenpass [A] */
const swRT=new THREE.WebGLRenderTarget(4,4,{depthTexture:new THREE.DepthTexture(4,4,THREE.UnsignedIntType)});swRT.depthTexture.minFilter=swRT.depthTexture.magFilter=THREE.NearestFilter;
window.__swU={d:{value:swRT.depthTexture},r:{value:new THREE.Vector2(1,1)},on:{value:SWON?1:0}};const swM=new THREE.MeshBasicMaterial({colorWrite:false});
function swPass(){if(!SWON||!window.__wmesh)return;const v=new THREE.Vector2();ren.getDrawingBufferSize(v);const w=Math.max(1,Math.round(v.x*SWH)),h=Math.max(1,Math.round(v.y*SWH));if(swRT.width!=w||swRT.height!=h)swRT.setSize(w,h);window.__swU.r.value.set(v.x,v.y);const wv=window.__wmesh.visible;window.__wmesh.visible=false;sc.overrideMaterial=swM;ren.setRenderTarget(swRT);ren.render(sc,cam);ren.setRenderTarget(null);sc.overrideMaterial=null;window.__wmesh.visible=wv;}
const oc=new OrbitControls(cam,ren.domElement);oc.enableDamping=true;oc.maxPolarAngle=Math.PI;oc.screenSpacePanning=true;
sc.add(new THREE.HemisphereLight(0xc2d8f2,0xa39c8e,1.2));
const sun=new THREE.DirectionalLight(0xfff0d8,1.6);sun.castShadow=true;sun.shadow.bias=-0.0003;sun.shadow.normalBias=0.12;sun.shadow.mapSize.set(4096,4096);sun.shadow.radius=1.6;
Object.assign(sun.shadow.camera,{left:-238,right:238,top:238,bottom:-238,near:1,far:900});sun.target.position.set(NX/2,0,NY/2);sc.add(sun,sun.target);
const ladeTex=u=>{const t=new THREE.TextureLoader().load(u);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;return t;};
const geo=(p,ix,uv,col)=>{const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));if(uv)g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));if(col)g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));if(ix)g.setIndex(ix);g.computeVertexNormals();return g;};
function sockel(Hrand,tief,root,st=1){const sp2=[],si=[],rand=[];for(let i=0;i<=NX*st;i++)rand.push([i/st,0]);for(let j=1;j<=NY*st;j++)rand.push([NX,j/st]);for(let i=NX*st-1;i>=0;i--)rand.push([i/st,NY]);for(let j=NY*st-1;j>=0;j--)rand.push([0,j/st]);   // t64u: st = Stuetzen je Meter
 window.__sockelTop=rand.map(([i,j])=>[i,Hrand(i,j),j]);   // t64u: fuer Randmessung
 rand.forEach(([i,j],n)=>{sp2.push(i,Hrand(i,j),j,i,tief,j);if(n)si.push(2*n-2,2*n-1,2*n,2*n,2*n-1,2*n+1);});
 const sm=new THREE.MeshLambertMaterial({color:0xffffff,side:THREE.DoubleSide});sm.onBeforeCompile=sh=>{sh.vertexShader='varying vec3 vSP;\n'+sh.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvSP=(modelMatrix*vec4(transformed,1.)).xyz;');
  sh.fragmentShader='varying vec3 vSP;\n'+sh.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
  {float u=vSP.x+vSP.z,w=sin(u*.043)*2.2+sin(u*.17+1.3)*.6+sin(u*.9)*.12,y=vSP.y+w;float b=fract(y/3.1),b2=fract(y/0.8+sin(u*.31)*.3);
   vec3 c=mix(vec3(.30,.27,.24),vec3(.40,.37,.33),smoothstep(.0,.25,b)*smoothstep(1.,.75,b));c=mix(c,vec3(.48,.44,.38),step(.82,b)*.7);c*=.9+.12*b2;
   c=mix(c,vec3(.22,.17,.13),smoothstep(-4.,-.5,vSP.y)*.0);c*=.85+.3*fract(sin(floor(y/3.1)*12.9)*437.);
   diffuseColor.rgb=pow(c,vec3(2.2))*2.6;}`);};
 root.add(new THREE.Mesh(geo(sp2,si),sm));
 const bo=new THREE.Mesh(new THREE.PlaneGeometry(NX,NY),(()=>{const bm=new THREE.MeshBasicMaterial({color:0xffffff,side:THREE.DoubleSide});bm.onBeforeCompile=sh=>{sh.vertexShader='varying vec3 vBP;\n'+sh.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvBP=(modelMatrix*vec4(transformed,1.)).xyz;');sh.fragmentShader='varying vec3 vBP;\n'+sh.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
 {vec2 q=vBP.xz;float f=q.x*.6+q.y*.8+9.*sin(q.x*.021)+5.*sin(q.y*.033+1.)+1.5*sin(q.x*.11+q.y*.07);float b=fract(f/7.),k=fract(sin(floor(f/7.)*12.9)*437.);
  vec3 c=mix(vec3(.24,.22,.20),vec3(.36,.33,.29),.5+.5*k);c=mix(c,vec3(.44,.40,.35),step(.86,b)*.6);c*=.88+.12*fract(f/1.3);diffuseColor.rgb=pow(c,vec3(2.2))*1.6;}`);};return bm;})());bo.rotation.x=Math.PI/2;bo.position.set(NX/2,tief,NY/2);root.add(bo);
 }
// gemeinsame Objekte (Wege, Bruecken, Baeume, Felsen, Haeuser, Mensch) – Groessen [A] wie t39u
function objekte(D,H,root,mensch){const G={};const grp=n=>{G[n]=new THREE.Group();G[n].userData.ebene=n;root.add(G[n]);return G[n]};
 {if(D.WEGA)grp('wege').add(D.wegMesh);else{const p=[];for(const [i,j] of D.wege){const q=[[i,j],[i,j+1],[i+1,j+1],[i+1,j]].map(([x,z])=>[x,H(Math.min(x,i+0.999),Math.min(z,j+0.999))+0.06,z]);p.push(...q[0],...q[1],...q[2],...q[0],...q[2],...q[3]);}
  grp('wege').add(new THREE.Mesh(geo(p),new THREE.MeshLambertMaterial({color:0x9c7b55,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2})));}
  const bm=new THREE.InstancedMesh(new THREE.BoxGeometry(1,0.25,1),new THREE.MeshLambertMaterial({color:0x7a5230}),D.bruecken.length);const o=new THREE.Object3D();D.bruecken.forEach(([x,y,z],n)=>{o.position.set(x,y,z);o.updateMatrix();bm.setMatrixAt(n,o.matrix)});bm.castShadow=true;G.wege.add(bm);}
 const inst=(g,mat,L,fn,gn)=>{const m=new THREE.InstancedMesh(g,mat,L.length),o=new THREE.Object3D();L.forEach((e,n)=>{fn(o,e);o.updateMatrix();m.setMatrixAt(n,o.matrix)});m.castShadow=m.receiveShadow=true;(G[gn]||grp(gn)).add(m);};
 if(D.wegMesh)window.__hausDreiecke=objekteNeu(D,H,G,grp);else{
 {const st=new THREE.CylinderGeometry(0.15,0.25,1,6).translate(0,0.5,0),k1=new THREE.ConeGeometry(0.42,0.6,8).translate(0,0.55,0),k2=new THREE.ConeGeometry(0.3,0.45,8).translate(0,0.85,0);
  const s1=new THREE.ConeGeometry(0.29,0.22,8).translate(0,0.66,0),s2=new THREE.ConeGeometry(0.2,0.2,8).translate(0,0.99,0);   // Schneekappen [A]
  inst(st,new THREE.MeshLambertMaterial({color:0x4e3424}),D.baeume,(o,[x,y,z,h,r])=>{o.position.set(x,y-0.3,z);o.rotation.set(0,r||0,0);o.scale.set(1,h*0.25,1)},'baeume');
  const nm=new THREE.MeshLambertMaterial({color:0xffffff}),sm=new THREE.MeshLambertMaterial({color:0xf2f5fa});
  const tf=(o,[x,y,z,h,r])=>{o.position.set(x,y-0.3,z);o.rotation.set(0,r||0,0);o.scale.set(h*0.5,h,h*0.5)};
  for(const k of[k1,k2]){inst(k,nm,D.baeume,tf,'baeume');const m=G.baeume.children.at(-1),c=new THREE.Color();
   D.baeume.forEach((b,n)=>{const t=b[5]??hash(b[0],b[2]);c.setHSL(0.40+0.06*t,0.28+0.12*t,0.17+0.07*t);m.setColorAt(n,c)});}
  if(D.baeume[0]&&D.baeume[0].length>4)for(const k of[s1,s2])inst(k,sm,D.baeume,tf,'baeume');}
 {const g=new THREE.IcosahedronGeometry(0.55,1),P=g.attributes.position,col=[];for(let i=0;i<P.count;i++){const x=P.getX(i),y=P.getY(i),z=P.getZ(i),f=0.8+0.35*hash(Math.round(x*50),Math.round(y*50+z*31));P.setXYZ(i,x*f*1.25,y*f*0.75,z*f);}
  g.computeVertexNormals();g.translate(0,0.3,0);const N=g.attributes.normal;for(let i=0;i<P.count;i++){const sn=N.getY(i)>0.5?1:0,v=0.42+0.12*hash(i,3);col.push(...(sn?[0.92,0.94,0.97]:[v,v*0.97,v*0.93]));}
  g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));const mat=new THREE.MeshLambertMaterial({vertexColors:true,flatShading:true});
  for(const L of[D.felsen,D.findlinge,D.steine,D.geroell||[]])inst(g,mat,L,(o,[x,y,z,h,r])=>{const a=hash(x,z),b=hash(z,x);o.position.set(x,y,z);o.rotation.set((a-0.5)*0.5,r,(b-0.5)*0.5);o.scale.set(h*(0.8+0.5*a),h*(0.6+0.5*b),h*(0.8+0.5*b))},'felsen');}
 {const hmat=new THREE.MeshLambertMaterial({color:0xd9c7a8}),fmat=new THREE.MeshLambertMaterial({color:0xc98a4a}),dmat=new THREE.MeshLambertMaterial({color:0x8a3b2e}),pmat=new THREE.MeshLambertMaterial({color:0x8f8a82});
  const roof=geo([-.5,0,-.5,.5,0,-.5,0,1,-.5, -.5,0,.5,0,1,.5,.5,0,.5, -.5,0,-.5,0,1,-.5,0,1,.5, -.5,0,-.5,0,1,.5,-.5,0,.5, .5,0,-.5,.5,0,.5,0,1,.5, .5,0,-.5,0,1,.5,0,1,-.5]);
  grp('gebaeude');const box=new THREE.BoxGeometry(1,1,1).translate(0,0.5,0);
  D.haeuser.forEach(h=>{const platz=h.typ=='Quartiersplatz',m=new THREE.Mesh(box,platz?pmat:h.typ.startsWith('FUNKTION')?fmat:hmat);const wh=platz?h.h:h.h*0.7;
   m.position.set(h.x,h.y,h.z);m.scale.set(h.b*0.9,wh,h.t*0.9);m.castShadow=m.receiveShadow=true;m.userData.haus=h;G.gebaeude.add(m);
   if(!platz){const r=new THREE.Mesh(roof,dmat);r.position.set(h.x,h.y+wh,h.z);r.scale.set(h.b*0.95,h.h*0.3,h.t*0.95);if(h.b>h.t){r.rotation.y=Math.PI/2;r.scale.set(h.t*0.95,h.h*0.3,h.b*0.95);}r.castShadow=true;r.userData.haus=h;G.gebaeude.add(r);}});}
 }
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
const NEU=new THREE.Group();sc.add(NEU);const G=f32(DN.GB||DN.G),WV=f32(DN.WV),RS=DN.rs,GX=NX*RS+1,GY=NY*RS+1,COSW=Math.cos(DN.wandwinkel*Math.PI/180);const gH9=(x,z)=>{const u=Math.min(Math.max(x*RS,0),GX-1.001),v=Math.min(Math.max(z*RS,0),GY-1.001),i=Math.floor(u),j=Math.floor(v),fu=u-i,fv=v-j,a=G[j*GX+i],b=G[j*GX+i+1],c=G[(j+1)*GX+i],d=G[(j+1)*GX+i+1];return (a*(1-fu)+b*fu)*(1-fv)+(c*(1-fu)+d*fu)*fv;},gN9=(x,z)=>{const e=0.5/RS,hx=(gH9(x+e,z)-gH9(x-e,z))/(2*e),hz=(gH9(x,z+e)-gH9(x,z-e))/(2*e),l=Math.hypot(hx,1,hz);return [-hx/l,1/l,-hz/l];};   // t67u O9 S3 [A]
const HN=(x,z)=>{x=Math.min(Math.max(x*RS,0),GX-1.001);z=Math.min(Math.max(z*RS,0),GY-1.001);const i=x|0,j=z|0,fx=x-i,fz=z-j,k=j*GX+i;
 return G[k]*(1-fx)*(1-fz)+G[k+1]*fx*(1-fz)+G[k+GX]*(1-fx)*fz+G[k+GX+1]*fx*fz;};
{const p=new Float32Array(GX*GY*3),VC=u8(DN.VC),cl=new Float32Array(GX*GY*3);for(let k=0;k<GX*GY;k++){const i=k%GX,j=(k/GX)|0;p.set([i/RS,G[k],j/RS],k*3);for(let c=0;c<3;c++)cl[k*3+c]=Math.pow(VC[k*3+c]/255,2.2);}
 // t43u: EIN Bodennetz; Farbe = Material-Gewichte aus Zelleigenschaften (Vertexfarbe), Fels weich ueber Neigung + triplanar Wandtextur
 const bi=[];let nw=0;const tri=(a,b,c)=>{bi.push(a,b,c);const A=a*3,B=b*3,C=c*3,ux=p[B]-p[A],uy=p[B+1]-p[A+1],uz=p[B+2]-p[A+2],vx=p[C]-p[A],vy=p[C+1]-p[A+1],vz=p[C+2]-p[A+2];
  const nx=uy*vz-uz*vy,ny=uz*vx-ux*vz,nz=ux*vy-uy*vx;if(Math.abs(ny)/Math.hypot(nx,ny,nz)<COSW-1e-7)nw++;};
 const LS=/[?&]lod=0/.test(location.search)?1:((Math.min(innerWidth,innerHeight)<700||/lod=1/.test(location.search))?2:1);window.__lod=LS;const HID=new Set(((location.search.match(/[?&]hide=([^&]*)/)||[])[1]||'').split(','));   // LOD Handy [A]
 const FW=DN.FW,BANDZ=new Uint8Array(NX*NY);if(FW)for(const z of new Uint32Array(Uint8Array.from(atob(FW.band),c=>c.charCodeAt(0)).buffer))BANDZ[z]=1;   // t54u Feinrelief-Band
 const VB=new Uint8Array(GX*GY);for(let z=0;z<NX*NY;z++)if(BANDZ[z]){const x=z%NX,y=(z/NX)|0;for(let dj=0;dj<=RS;dj++)for(let di=0;di<=RS;di++)VB[(y*RS+dj)*GX+x*RS+di]=1;}
 for(let j=0;j<GY-LS;j+=LS)for(let i=0;i<GX-LS;i+=LS){if(BANDZ[((j/RS)|0)*NX+((i/RS)|0)])continue;const a=j*GX+i,b=a+LS,c=a+GX*LS,d=c+LS;tri(a,c,d);tri(a,d,b);}
 {// t44u r9: Abbruchkante glaetten (nur Netz, nicht Zellwerte): Kantenpunkte in x/z zum Mittel gleich hoher Nachbarn ziehen [A]
  const q=p.slice(),rng=k=>{let a=1e9,b=-1e9;const i=k%GX,j=(k/GX)|0;for(let dj=-1;dj<=1;dj++)for(let di=-1;di<=1;di++){const ii=i+di,jj=j+dj;if(ii<0||jj<0||ii>=GX||jj>=GY)continue;const g=G[jj*GX+ii];a=Math.min(a,g);b=Math.max(b,g);}return b-a;};
  for(let k=0;k<GX*GY;k++){if(VB[k]||rng(k)<1.5)continue;const i=k%GX,j=(k/GX)|0;let sx=0,sz=0,n=0;
   for(let dj=-2;dj<=2;dj++)for(let di=-2;di<=2;di++){const ii=i+di,jj=j+dj;if(ii<0||jj<0||ii>=GX||jj>=GY)continue;const kk=jj*GX+ii;if(Math.abs(G[kk]-G[k])<0.6){sx+=p[kk*3];sz+=p[kk*3+2];n++;}}
   if(n>2&&i>0&&j>0&&i<GX-1&&j<GY-1){q[k*3]=p[k*3]*0.4+0.6*sx/n;q[k*3+2]=p[k*3+2]*0.4+0.6*sz/n;}}
  // Kartenrand: tiefe Kerben (Flussaustritt) weich verrunden, nur Netz [A]
  for(let k=0;k<GX*GY;k++){const i=k%GX,j=(k/GX)|0,dr=Math.min(i,j,GX-1-i,GY-1-j);if(dr>10||VB[k])continue;let s2=0,n=0;
   for(let dj=-4;dj<=4;dj++)for(let di=-4;di<=4;di++){const ii=Math.min(Math.max(i+di,0),GX-1),jj=Math.min(Math.max(j+dj,0),GY-1);s2+=G[jj*GX+ii];n++;}
   const w=(1-dr/10.5)*Math.min(1,rng(k)/1.5+0.0);q[k*3+1]=G[k]*(1-w)+w*Math.min(G[k],s2/n)*1+w*0;}
  // t64u: umgeklappte Grobdreiecke (19 bei LS1) -> Verschiebung ihrer Ecken zuruecknehmen [A]
  {let nf=0;for(let it=0;it<4;it++){let c=0;for(let n=0;n<bi.length;n+=3){const A=bi[n]*3,B=bi[n+1]*3,C=bi[n+2]*3;
    const o0=(p[B]-p[A])*(p[C+2]-p[A+2])-(p[B+2]-p[A+2])*(p[C]-p[A]),o1=(q[B]-q[A])*(q[C+2]-q[A+2])-(q[B+2]-q[A+2])*(q[C]-q[A]);
    if(o0*o1<=0){for(const V of[A,B,C]){q[V]=p[V];q[V+2]=p[V+2];}c++;}}if(it==0)nf=c;if(!c)break;}window.__umgeklappt=nf;}
  p.set(q);}
 const gb=new THREE.BufferGeometry();gb.setAttribute('position',new THREE.BufferAttribute(p,3));gb.setAttribute('color',new THREE.BufferAttribute(cl,3));gb.setIndex(bi);gb.computeVertexNormals();{const NA=gb.attributes.normal.array,used=new Uint8Array(GX*GY);for(const v of bi)used[v]=1;let nb=0;for(let k=0;k<GX*GY;k++){if(!VB[k]||!used[k])continue;const g=gN9((k%GX)/RS,((k/GX)|0)/RS);NA[k*3]=g[0];NA[k*3+1]=g[1];NA[k*3+2]=g[2];nb++;}gb.attributes.normal.needsUpdate=true;window.__grobrand=nb;}   // t67u O9 S3: Grob-Randnormalen gleich Fein [A]
 const wt=ladeTex(window.WANDTEX),dt=ladeTex(window.RTEX);for(const t of[wt,dt]){t.wrapS=t.wrapT=THREE.RepeatWrapping;t.colorSpace=THREE.NoColorSpace;}
 const mat=new THREE.MeshLambertMaterial({vertexColors:true,side:THREE.DoubleSide}),matF=new THREE.MeshLambertMaterial({vertexColors:true,side:THREE.DoubleSide});matF.customProgramCacheKey=()=>'fw54';
 const _pat=FWM=>sh=>{sh.uniforms.tW={value:wt};sh.uniforms.tD={value:dt};
  sh.vertexShader='varying vec3 vWP;varying vec3 vWN;'+(FWM?'attribute vec3 ftint;attribute float fsnow;varying vec3 vFT;varying float vFS;':'')+'\n'+sh.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\n'+(FWM?'vFT=ftint;vFS=fsnow;':'')+'vWP=(modelMatrix*vec4(transformed,1.)).xyz;vWN=normalize(mat3(modelMatrix)*objectNormal);');
  sh.fragmentShader='uniform sampler2D tW;uniform sampler2D tD;varying vec3 vWP;varying vec3 vWN;'+(FWM?'\n#define FWM 1\nvarying vec3 vFT;varying float vFS;':'')+'\n'+sh.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
   vec3 N=normalize(vWN);vec3 w=pow(abs(N),vec3(4.));w/=w.x+w.y+w.z;
   mat2 RT1=mat2(.96,-.28,.28,.96);vec3 tr=texture2D(tW,RT1*vWP.zy/9.).rgb*w.x+texture2D(tW,RT1*vWP.xy/9.).rgb*w.z+texture2D(tW,vWP.xz/9.).rgb*w.y;   // t66u N2: um -16 Grad gedreht, Schichtlinien nicht mehr waagrecht gestapelt [A]
   mat2 RT=mat2(.8,.6,-.6,.8);vec3 tr2=texture2D(tW,RT*vWP.zy/23.+.37).rgb*w.x+texture2D(tW,RT*vWP.xy/23.+.37).rgb*w.z+texture2D(tW,vWP.xz/23.+.37).rgb*w.y;   // t65u M4: zweite Wandprobe um 37 Grad gedreht -> waagrechte Schichtstreifen gebrochen, Form unveraendert [A]
   #define TD3(s,o) (texture2D(tD,vWP.zy/(s)+(o)).r*w.x+texture2D(tD,vWP.xy/(s)+(o)).r*w.z+texture2D(tD,vWP.xz/(s)+(o)).r*w.y)
   float d=TD3(4.,0.)*0.6+TD3(23.,0.)*0.4,gD=TD3(61.,.2);   // t64u K9: Boden-Detail triplanar statt nur xz -> keine senkrechten Streifen/gestreckte Wandtextur [A]
   diffuseColor.rgb*=(0.72+0.33*d)*(0.90+0.2*gD);
   {float f=TD3(1.4,.37),L=dot(diffuseColor.rgb,vec3(.33));float sw=smoothstep(.55,.75,L);diffuseColor.rgb*=1.+sw*(f-.5)*.12;diffuseColor.rgb=mix(diffuseColor.rgb,diffuseColor.rgb*vec3(.90,.95,1.05),sw*(1.-d)*.6);}
   float nzS=TD3(3.3,.53)*.6+TD3(11.,.29)*.4;   // O9: Rauschen gegen Dreieckszaehne an Schnee-/Felsgrenze, nur Farbe [A]
   float st=1.-smoothstep(0.32,0.80,abs(N.y)+0.10*(d-0.8)+0.30*(nzS-0.5));
   vec3 tx=mix(tr,tr2,0.5);float r=dot(tx,vec3(0.33));
   vec3 fels=pow(tx,vec3(2.2))*vec3(1.0,1.0,1.0)*mix(0.80,1.25,gD)*1.15;
   float sn=smoothstep(0.44,0.66,abs(N.y)+0.18*(r-0.5)+0.20*(nzS-0.5));   // Schnee auf Simsen/Kanten [A]
   {float g2=TD3(97.,.1);fels*=mix(vec3(.90,.93,1.0),vec3(1.05,1.0,.92),g2);   // grossraeumige Farbe [A]
    float ms=smoothstep(.30,.48,abs(N.y)+0.15*(r-0.5))*(1.-sn)*smoothstep(.45,.6,gD);fels=mix(fels,vec3(.16,.20,.11),ms*.55);}   // Moos auf Absaetzen [A]
   #ifdef FWM
   fels*=vFT*2.;fels=mix(vec3(dot(fels,vec3(.333))),fels,.5);   // Runde D: grauer [A]
   sn=max(sn,smoothstep(0.1,0.9,vFS+0.55*(nzS-0.5)));st=max(st,smoothstep(.05,.3,vFS)*0.0+st);
   #endif
   fels=mix(fels,vec3(0.80,0.84,0.90),sn*0.9);
   diffuseColor.rgb=mix(diffuseColor.rgb,fels,st);`).replace('#include <normal_fragment_maps>',/[?&]nobump=1/.test(location.search)?'#include <normal_fragment_maps>':`#include <normal_fragment_maps>
   {vec3 N2=normalize(vWN);vec3 w2=pow(abs(N2),vec3(4.));w2/=w2.x+w2.y+w2.z;   // t48u R5: Detail-Bump (triplanar) gegen "verpixelt" [A]
    float hb=((texture2D(tD,vWP.zy/3.1+.21).r*.5+texture2D(tD,vWP.zy/2.3).r*.5)*w2.x+(texture2D(tD,vWP.xy/3.1+.21).r*.5+texture2D(tD,vWP.xy/2.3).r*.5)*w2.z+texture2D(tD,vWP.xz/5.1).r*w2.y)*0.7+(texture2D(tD,vWP.zy/9.).r*w2.x+texture2D(tD,vWP.xy/9.).r*w2.z+texture2D(tD,vWP.xz/6.).r*w2.y)*0.3;
    vec3 dpx=dFdx(-vViewPosition),dpy=dFdy(-vViewPosition);vec3 r1=cross(dpy,normal),r2=cross(normal,dpx);float det=dot(dpx,r1);
    vec3 grd=sign(det)*(dFdx(hb)*r1+dFdy(hb)*r2)*(0.22+1.78*(1.-abs(N2.y)));/* O3: Boden-Bump grober+schwaecher, sonst 2x2-Pixel-Kaestchen im Schnee (dFdx/dFdy) [A] */normal=normalize(abs(det)*normal-grd);}`);};
 mat.onBeforeCompile=_pat(0);matF.onBeforeCompile=_pat(1);
 const m=new THREE.Mesh(gb,mat);m.receiveShadow=m.castShadow=true;m.userData.boden=1;
 let fwMesh=null;if(FW){const b2=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0)).buffer,FS=FW.fs,FX=NX*FS+1,vid=new Uint32Array(b2(FW.vid)),fh=new Float32Array(b2(FW.h)),fc=new Uint8Array(b2(FW.c)),S=FS/(LS==1?1:2)>=1?(LS==1?1:2):1;
  const map=new Int32Array(FX*(NY*FS+1)).fill(-1);vid.forEach((k,n)=>map[k]=n);const fp=new Float32Array(vid.length*3),fcl=new Float32Array(vid.length*3);
  vid.forEach((k,n)=>{fp[n*3]=(k%FX)/FS;fp[n*3+1]=fh[n];fp[n*3+2]=((k/FX)|0)/FS;for(let c=0;c<3;c++)fcl[n*3+c]=Math.pow(fc[n*3+c]/255,2.2);});
  // t61u: Handy-LOD (Grobnetz 1 m) – Feinband-Randpunkte in Kantenmitte auf die Grobkante legen, sonst Spalt bis 0,5 m [A]
  if(LS==2){const H=FS/2,bz=(x,y)=>x>=0&&y>=0&&x<NX&&y<NY&&BANDZ[y*NX+x];vid.forEach((k,n)=>{const fx=k%FX,fy=(k/FX)|0,x=(fx/FS)|0,y=(fy/FS)|0;
   if(fy%FS==0&&fx%FS==H){if(!(bz(x,y-1)&&bz(x,y))){const a=(fy/FS*RS)*GX+x*RS;fp[n*3+1]=(G[a]+G[a+RS])/2;}}
   else if(fx%FS==0&&fy%FS==H){if(!(bz(x-1,y)&&bz(x,y))){const a=(y*RS)*GX+fx/FS*RS;fp[n*3+1]=(G[a]+G[a+RS*GX])/2;}}});}
  const fi=[];for(let z=0;z<NX*NY;z++){if(!BANDZ[z])continue;const x=z%NX,y=(z/NX)|0;for(let dj=0;dj<FS;dj+=S)for(let di=0;di<FS;di+=S){const a=map[(y*FS+dj)*FX+x*FS+di],b=map[(y*FS+dj)*FX+x*FS+di+S],c=map[(y*FS+dj+S)*FX+x*FS+di],d=map[(y*FS+dj+S)*FX+x*FS+di+S];fi.push(a,c,d,a,d,b);}}
  // t64u: T-Stoss Feinband/Grobnetz (26478 offene Innenkanten, geometrisch 0 Spalt) -> Rasterfunken; Schuerze 0,35 m nach unten unter jeder Grenzkante [A]
  let fpA=fp,fclA=fcl,nS=0;const SRC=[];{const bz=(x,y)=>x>=0&&y>=0&&x<NX&&y<NY&&BANDZ[y*NX+x],xp=[],xc=[],base=vid.length,dup=(v,d=0.35)=>{const n=base+xp.length/3;xp.push(fp[v*3],fp[v*3+1]-d,fp[v*3+2]);xc.push(fcl[v*3],fcl[v*3+1],fcl[v*3+2]);SRC.push(v);return n;};
   for(let z=0;z<NX*NY;z++){if(!BANDZ[z])continue;const x=z%NX,y=(z/NX)|0;const sides=[[0,-1,(t)=>[(y*FS)*FX+x*FS+t]],[0,1,(t)=>[((y+1)*FS)*FX+x*FS+t]],[-1,0,(t)=>[(y*FS+t)*FX+x*FS]],[1,0,(t)=>[(y*FS+t)*FX+(x+1)*FS]]];
    for(const [dx,dy,K] of sides){const nx=x+dx,ny=y+dy;if(nx<0||ny<0||nx>=NX||ny>=NY||bz(nx,ny))continue;for(let t=0;t<FS;t+=S){const a=map[K(t)[0]],b=map[K(t+S)[0]];if(a<0||b<0)continue;const a1=dup(a,0),b1=dup(b,0),a2=dup(a),b2=dup(b);fi.push(a1,b1,b2,a1,b2,a2);nS+=2;}}}
   if(xp.length){fpA=new Float32Array(fp.length+xp.length);fpA.set(fp);fpA.set(xp,fp.length);fclA=new Float32Array(fcl.length+xc.length);fclA.set(fcl);fclA.set(xc,fcl.length);}}
  window.__schuerze=nS;
  const fg=new THREE.BufferGeometry();fg.setAttribute('position',new THREE.BufferAttribute(fpA,3));fg.setAttribute('color',new THREE.BufferAttribute(fclA,3));if(FW.t){{const t0=new Uint8Array(b2(FW.t)),s0=new Uint8Array(b2(FW.s)),N=vid.length+SRC.length,ft=new Float32Array(N*3),fs=new Float32Array(N);for(let n=0;n<N;n++){const v=n<vid.length?n:SRC[n-vid.length];ft[n*3]=t0[v*3]/256;ft[n*3+1]=t0[v*3+1]/256;ft[n*3+2]=t0[v*3+2]/256;fs[n]=s0[v]/255;}fg.setAttribute('ftint',new THREE.BufferAttribute(ft,3));fg.setAttribute('fsnow',new THREE.BufferAttribute(fs,1));}}fg.setIndex(fi);fg.computeVertexNormals();if(!/[?&]nosn=1/.test(location.search)){const NA=fg.attributes.normal.array,IX=fg.index.array,nv=NA.length/3;for(let it=0;it<3;it++){const acc=new Float32Array(NA.length),cnt=new Float32Array(nv);for(let t=0;t<IX.length;t+=3){const a=IX[t],b=IX[t+1],c=IX[t+2];for(const [u,v] of [[a,b],[b,c],[c,a],[b,a],[c,b],[a,c]]){acc[u*3]+=NA[v*3];acc[u*3+1]+=NA[v*3+1];acc[u*3+2]+=NA[v*3+2];cnt[u]++;}}for(let v=0;v<nv;v++){if(!cnt[v])continue;const ny=Math.abs(NA[v*3+1]),k=0.6*Math.min(1,Math.max(0,(0.85-ny)/0.2));if(!k)continue;let x=NA[v*3]*(1-k)+acc[v*3]/cnt[v]*k,y=NA[v*3+1]*(1-k)+acc[v*3+1]/cnt[v]*k,z=NA[v*3+2]*(1-k)+acc[v*3+2]/cnt[v]*k;const l=Math.hypot(x,y,z)||1;NA[v*3]=x/l;NA[v*3+1]=y/l;NA[v*3+2]=z/l;}}fg.attributes.normal.needsUpdate=true;}{const NA=fg.attributes.normal.array,bz=(x,y)=>x<0||y<0||x>=NX||y>=NY||BANDZ[y*NX+x];let nb=0;for(let n=0;n<vid.length;n++){const X=fpA[n*3],Z=fpA[n*3+2],cx=Math.floor(X),cz=Math.floor(Z);let dm=9;for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){if(bz(cx+dx,cz+dy))continue;const ex=Math.max(cx+dx-X,0,X-(cx+dx+1)),ez=Math.max(cz+dy-Z,0,Z-(cz+dy+1));dm=Math.min(dm,Math.hypot(ex,ez));}if(dm>0.75)continue;const w=dm<0.01?1:Math.max(0,1-dm/0.75)*0.7;const g=gN9(X,Z);let x=NA[n*3]*(1-w)+g[0]*w,y=NA[n*3+1]*(1-w)+g[1]*w,z=NA[n*3+2]*(1-w)+g[2]*w;const l=Math.hypot(x,y,z)||1;NA[n*3]=x/l;NA[n*3+1]=y/l;NA[n*3+2]=z/l;nb++;}fg.attributes.normal.needsUpdate=true;window.__randnormalen=nb;}   // t67u O9 S3: Feinband-Randnormalen = Grobnetz-Gradient -> keine Schattierungs-Naht [A]   // t66u N1: Normalen an Steilflaechen geglaettet (nur Schattierung, Positionen unveraendert) gegen waagrechte Feinstreifen [A]
  fwMesh=new THREE.Mesh(fg,matF);fwMesh.receiveShadow=fwMesh.castShadow=true;fwMesh.userData.boden=1;window.__fw={dreiecke:fi.length/3,lod:S};window.__fwm=fwMesh;}
 let ovMesh=null;if(FW&&FW.ov){const b3=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0)).buffer;const og=new THREE.BufferGeometry();og.setAttribute('position',new THREE.BufferAttribute(new Float32Array(b3(FW.ov)),3));og.setIndex(new THREE.BufferAttribute(new Uint32Array(b3(FW.ovi)),1));og.computeVertexNormals();ovMesh=new THREE.Mesh(og,new THREE.MeshStandardMaterial({color:0x8d8d92,roughness:0.95}));ovMesh.castShadow=ovMesh.receiveShadow=true;window.__ov={dreiecke:og.index.count/3};}   // Runde F: Ueberhaenge als Zusatz-Meshes [A]
 const g=new THREE.Group();g.userData.ebene='gelaende';g.add(m);if(fwMesh)g.add(fwMesh);window.__bodenMeshes=[m,fwMesh].filter(Boolean);if(ovMesh){g.add(ovMesh);ovMesh.visible=!/[?&]noov=1/.test(location.search);}NEU.add(g);
 if(/[?&]clay=1/.test(location.search)){const CL=new THREE.MeshLambertMaterial({color:0x9c9c9c,side:THREE.DoubleSide});m.material=CL;if(fwMesh)fwMesh.material=CL;if(ovMesh)ovMesh.material=CL;window.__clay=1;}   // t55u: Formbeweis einfarbig grau, ohne Textur/Vertexfarben/Bump [A]
 if(/[?&]glb=1/.test(location.search)&&location.protocol.startsWith('http')){   // t48u R5: GLB-Pfad (lokaler Server), sonst Single-File-Daten [A]
  new GLTFLoader().load('dorfmap_relief_z25.glb',gl=>{const mat=new THREE.MeshLambertMaterial({vertexColors:true,side:THREE.DoubleSide});gl.scene.traverse(o=>{if(o.isMesh){o.material=mat;o.receiveShadow=true;o.castShadow=true;}});
   g.visible=false;const gg=new THREE.Group();gg.userData.ebene='gelaende';gg.add(gl.scene);NEU.add(gg);window.__glb={ok:true,meshes:gl.scene.children.length};},undefined,e=>{window.__glb={ok:false,fehler:String(e)};});}
 window.__dreiecke={boden:bi.length/3-nw,wand:nw};
 // Wege-Overlay: weicher Rand ueber Vertex-Alpha
 {const A=u8(DN.WEGA),wp=[],wc=[],wi=[],map=new Int32Array(GX*GY).fill(-1);const vx=k=>{if(map[k]<0){map[k]=wp.length/3;const i=k%GX,j=(k/GX)|0,h=hash(i,j);wp.push(i/RS,G[k]+0.05,j/RS);{const a=A[k]/255,e=a*a;wc.push(0.62-0.30*e+0.04*h,0.58-0.30*e+0.03*h,0.54-0.30*e+0.02*h,Math.min(0.85,Math.pow(a,1.4)*0.95));}}return map[k];};
  for(let j=0;j<GY-1;j++)for(let i=0;i<GX-1;i++){const a=j*GX+i,b=a+1,c=a+GX,d=c+1;if(A[a]|A[b]|A[c]|A[d])wi.push(vx(a),vx(c),vx(d),vx(a),vx(d),vx(b));}
  const wg=new THREE.BufferGeometry();wg.setAttribute('position',new THREE.Float32BufferAttribute(wp,3));wg.setAttribute('color',new THREE.Float32BufferAttribute(wc,4));wg.setIndex(wi);wg.computeVertexNormals();
  DN.wegMesh=new THREE.Mesh(wg,new THREE.MeshLambertMaterial({vertexColors:true,transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-2}));DN.wegMesh.receiveShadow=true;}
 {// t64u: Sockel-Oberkante = exakt die gerenderte Gelaende-Randlinie (Grob 0,5/1 m + Feinband 0,25/0,5 m), vorher nur 1-m-Stuetzen -> Randschlitze bis 0,69 m [A]
  const RK=new Map(),ST=8,add=(P,I)=>{for(let n=0;n<I.length;n++){const v=I[n],x=P[v*3],y=P[v*3+1],z=P[v*3+2];let k=null;
   if(Math.abs(z)<1e-4)k='n'+Math.round(x*ST);else if(Math.abs(z-NY)<1e-4)k='s'+Math.round(x*ST);else if(Math.abs(x)<1e-4)k='w'+Math.round(z*ST);else if(Math.abs(x-NX)<1e-4)k='o'+Math.round(z*ST);
   if(k!==null)RK.set(k,y);}};
  add(gb.attributes.position.array,gb.index.array);if(fwMesh)add(fwMesh.geometry.attributes.position.array,fwMesh.geometry.index.array);
  const HR=(x,z)=>{const sd=z<1e-4?'n':z>NY-1e-4?'s':x<1e-4?'w':'o',t=Math.round((sd=='n'||sd=='s'?x:z)*ST);if(RK.has(sd+t))return RK.get(sd+t);
   let a=t,b=t;while(!RK.has(sd+a)&&t-a<64)a--;while(!RK.has(sd+b)&&b-t<64)b++;const ya=RK.get(sd+a),yb=RK.get(sd+b);if(ya===undefined)return yb;if(yb===undefined)return ya;return ya+(yb-ya)*(t-a)/(b-a);};
  window.__randpunkte=RK.size;window.__RK=[...RK];sockel(HR,-34,g,4);}
 {const wp=[],wc=[],wi=[],map=new Int32Array(GX*GY).fill(-1),ok=k=>WV[k]>-900;const wm=new Float32Array(GX*GY);{const m0=new Float32Array(GX*GY);for(let k=0;k<GX*GY;k++)m0[k]=ok(k)?1:0;for(let j=0;j<GY;j++)for(let i=0;i<GX;i++){let s=0,c=0;for(let dj=-2;dj<=2;dj++)for(let di=-2;di<=2;di++){const ii=i+di,jj=j+dj;if(ii<0||jj<0||ii>=GX||jj>=GY)continue;const wt=3-Math.max(Math.abs(di),Math.abs(dj));s+=m0[jj*GX+ii]*wt;c+=wt;}wm[j*GX+i]=s/c;}}const wmA=[];   // O9: weiche Wasserrand-Maske (Isolinie statt Zellraster-Treppe) [A]
 const GL=(()=>{if(LS<2)return G;const R=new Float32Array(G);for(let j=0;j<GY;j++)for(let i=0;i<GX;i++){const k=j*GX+i,oi=i&1,oj=j&1;if(!oi&&!oj)continue;if(oi&&!oj)R[k]=(G[k-1]+G[k+1])/2;else if(oj&&!oi)R[k]=(G[k-GX]+G[k+GX])/2;else R[k]=(G[k-GX-1]+G[k+GX+1])/2;}return R;})();   /* O4: Handy-LOD (1-m-Boden): Wasser-Randhoehen auf den tatsaechlich gezeichneten 1-m-Boden beziehen, sonst 1-m-Saegezaehne [S/A] */
 const WR=new Float32Array(WV);{let A=new Float32Array(WV);for(let it=0;it<3;it++){const B=new Float32Array(A);for(let j=1;j<GY-1;j++)for(let i=1;i<GX-1;i++){const k=j*GX+i;if(!ok(k))continue;const v=[];for(let dj=-1;dj<=1;dj++)for(let di=-1;di<=1;di++){const n=k+dj*GX+di;if(n!=k&&ok(n)&&A[n]>A[k]+0.3)v.push(A[n]);}if(v.length>=5){v.sort((x,y)=>x-y);B[k]=v[v.length>>1];}}A=B;}   /* O4: schmale tiefere Flusslinie mitten im See (0,6-0,7 m unter Seespiegel, Zickzack) nur in der Darstellung auf Seespiegel heben [S/A] */
for(let it=0;it<16;it++){const B=new Float32Array(A);for(let j=1;j<GY-1;j++)for(let i=1;i<GX-1;i++){const k=j*GX+i;if(!ok(k))continue;let s=0,c=0;for(let dj=-1;dj<=1;dj++)for(let di=-1;di<=1;di++){const n=k+dj*GX+di;if(ok(n)){s+=A[n];c++;}}B[k]=Math.min(WV[k]+0.3,Math.max(WV[k]-0.6,s/c));/* O5 D3 Test: Spiegelstufen weiter glaetten [A] */}A=B;}WR.set(A);}   // O4: nur Darstellung: Wasserspiegel weich (Stufen im 0,5-m-Raster -> keine Treppen/Saegezaehne), Daten unveraendert [A]
 const WD=new Float32Array(WR);{const O=new Float32Array(GX*GY);for(let k=0;k<GX*GY;k++)if(ok(k)){const d=WR[k]-GL[k];if(d<0.12){const t=Math.min(1,Math.max(0,(0.12-d)/0.12)),w=t*t*(3-2*t);O[k]=w*(GL[k]-0.15-WR[k]);}}for(let it=0;it<2;it++){const B=new Float32Array(O);for(let j=1;j<GY-1;j++)for(let i=1;i<GX-1;i++){const k=j*GX+i;if(!ok(k))continue;let s=0,c=0;for(let dj=-1;dj<=1;dj++)for(let di=-1;di<=1;di++){const n=k+dj*GX+di;if(ok(n)){const g=(di&&dj)?1:(di||dj)?2:4;s+=O[n]*g;c+=g;}}B[k]=Math.min(O[k],s/c);}O.set(B);}for(let k=0;k<GX*GY;k++)if(ok(k))WD[k]=WR[k]+O[k];}window.__WD=WD;window.__WOK=ok;/* O5 E1: flache Ecken nur in Darstellung unter Boden absenken, Gauss-Uebergang -> glatte Schnittlinie [A] */
const hR=k=>{if(ok(k))return WD[k];let s=0,c=0;for(const n of[k+1,k-1,k+GX,k-GX,k+GX+1,k+GX-1,k-GX+1,k-GX-1])if(n>=0&&n<GX*GY&&ok(n)){s+=WR[n];c++;}return c?Math.min(s/c,GL[k]+0.02):GL[k]+0.02;},hD=k=>{if(LS<2||!/[?&]wlod=1/.test(location.search))return hR(k);/* V2 ohne Wirkung -> nur mit ?wlod=1 */const i=k%GX,j=(k/GX)|0,oi=i&1,oj=j&1;if((!oi&&!oj)||i==0||j==0||i>=GX-1||j>=GY-1)return hR(k);if(oi&&!oj)return(hR(k-1)+hR(k+1))/2;if(oj&&!oi)return(hR(k-GX)+hR(k+GX))/2;return(hR(k-GX-1)+hR(k+GX+1))/2;};/* O5 E1 V2: Handy-LOD Wasserhoehen ungerader Ecken wie Boden interpolieren [A] */const vx=k=>{if(map[k]<0){map[k]=wp.length/3;const i=k%GX,j=(k/GX)|0,t=ok(k)?Math.min(1,Math.max(0,(WV[k]-GL[k])/1.5)):0;
   let hx=GL[k]+0.02,dL=-1;if(!ok(k)){let s=0,c=0;for(const n of[k+1,k-1,k+GX,k-GX,k+GX+1,k+GX-1,k-GX+1,k-GX-1])if(n>=0&&n<GX*GY&&ok(n)){s+=WR[n];c++;}if(c){dL=s/c-GL[k];hx=Math.min(s/c,GL[k]+0.02);}}   // O4: trockener Rand auf Nachbar-Spiegel -> Schnitt mit Gelaende = Hoehenlinie [A]
   wp.push(i/RS,hD(k),j/RS);{const hw=ok(k)?WR[k]:hx,d=ok(k)?hw-GL[k]:dL;wmA.push(Math.min(1.2,Math.max(0.,0.5+0.22*(d+0.03)/0.12)));}/* O4: Alpha-Rand aus Wassertiefe, linear je Dreieck -> glatte Kante statt 0,5-m-Zellmaske [A] */{const rim=ok(k)&&!(ok(k+1)&&ok(k-1)&&ok(k+GX)&&ok(k-GX)),e=1-Math.min(1,t*4),q=(n=>ok(n)?Math.abs(WV[n]-WV[k]):0),fo0=ok(k)?Math.min(1,Math.max(0,(q(k+1)+q(k-1)+q(k+GX)+q(k-GX)-0.9)*0.7)):0,fo=Math.min(fo0,0.3);   // Runde E: Schaum gedeckelt [A]
     // t48u: Schaum/Wasserfall an Stufen [A]
   wc.push((0.06+0.5*e*e)*(1-fo)+0.70*fo,(0.16+0.48*e*e)*(1-fo)+0.76*fo,(0.21+0.45*e*e)*(1-fo)+0.80*fo,Math.max(0.14+0.76*Math.pow(Math.min(1,t*1.15),0.8),0.35*fo));};}   // Runde D: weniger Ufer-Schaum [A]
return map[k];};   // t54u: flach transparent (Kies sichtbar), Eis-/Uferlinie am Rand [A]   // flach hell/klar, tief dunkler [A]
  for(let j=0;j<GY-1;j++)for(let i=0;i<GX-1;i++){const a=j*GX+i,b=a+1,c=a+GX,d=c+1;if(ok(a)||ok(b)||ok(c)||ok(d)){const voll=ok(a)&&ok(b)&&ok(c)&&ok(d);if(voll?HID.has('winnen'):HID.has('wrand'))continue;wi.push(vx(a),vx(c),vx(d),vx(a),vx(d),vx(b));}/* O5 D1: Teilgruppen winnen (alle 4 Ecken nass) / wrand (Randzellen) [A] */}
  const g2=new THREE.BufferGeometry();g2.setAttribute('position',new THREE.Float32BufferAttribute(wp,3));g2.setAttribute('color',new THREE.Float32BufferAttribute(wc,4));g2.setAttribute('wmask',new THREE.Float32BufferAttribute(wmA,1));g2.setIndex(wi);g2.computeVertexNormals();
  const wg=new THREE.Group();wg.userData.ebene='wasser';const wmesh=new THREE.Mesh(g2,new THREE.MeshPhongMaterial({vertexColors:true,transparent:true,depthWrite:false,shininess:90,specular:0x667788,side:THREE.DoubleSide}));wmesh.receiveShadow=true;const wu={value:0};window.__wu=wu;wmesh.material.onBeforeCompile=sh=>{sh.uniforms.uT=wu;sh.uniforms.uD=window.__swU.d;sh.uniforms.uRes=window.__swU.r;sh.uniforms.uN={value:cam.near};sh.uniforms.uF={value:cam.far};sh.uniforms.uSW=window.__swU.on;sh.vertexShader='attribute float wmask;varying float vWM;varying vec3 vWQ;\n'+sh.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\n vWQ=(modelMatrix*vec4(transformed,1.)).xyz;vWM=wmask;');
  sh.fragmentShader='uniform float uT;uniform sampler2D uD;uniform vec2 uRes;uniform float uN,uF,uSW;float lz(float d){return uN*uF/((uF-uN)*d-uF);}varying float vWM;varying vec3 vWQ;\n'+sh.fragmentShader.replace('#include <color_fragment>','#include <color_fragment>\n {float nr=sin(vWQ.x*2.1+vWQ.z*1.3)*sin(vWQ.z*2.7-vWQ.x*.8);if(uSW>.5){float zg=lz(texture2D(uD,gl_FragCoord.xy/uRes).r),zw=lz(gl_FragCoord.z);vec3 gp=cameraPosition+(vWQ-cameraPosition)*(zg/zw);float dp=max(0.,vWQ.y-gp.y);diffuseColor.a=max(diffuseColor.a,.45)*smoothstep(0.,.30,dp+.03*nr);diffuseColor.rgb=mix(diffuseColor.rgb,vec3(.86,.9,.92),.35*(1.-smoothstep(0.,.07,dp)));}else{diffuseColor.a*=smoothstep(.50,.72,vWM+.05*nr);}/* O5: weiche Wasserkante aus Szenentiefe [A] *//* O4 F2: Tiefe je Pixel statt Ecken-Maske [A] */}\n {float s=sin(vWQ.x*.31+vWQ.z*.11-uT*.9)*sin(vWQ.z*.47-vWQ.x*.05+uT*.6)+.5*sin(vWQ.x*1.3-vWQ.z*.9-uT*1.7);diffuseColor.rgb*=1.+.07*s;diffuseColor.rgb+=vec3(.025,.03,.035)*max(0.,s-.6);}');};window.__wmesh=wmesh;wg.add(wmesh);if(/[?&]nowa=1/.test(location.search))wg.visible=false;NEU.add(wg);}
 {const hG=(x,z)=>{const fi=Math.min(GX-2,Math.max(0,x*RS)),fj=Math.min(GY-2,Math.max(0,z*RS)),i=fi|0,j=fj|0,a=fi-i,b=fj-j,k=j*GX+i;return G[k]*(1-a)*(1-b)+G[k+1]*a*(1-b)+G[k+GX]*(1-a)*b+G[k+GX+1]*a*b;};   // t48u R5: Rampen-Pfade als Overlay (Ebene wege) [A]
  // t67u O8: Rampen folgen der sichtbaren Oberflaeche (Strahl auf Grob+Feinnetz), 5 Querpunkte, Raender blenden aus, leicht geschwungen [A]
  const BM=(window.__bodenMeshes||[]);NEU.updateMatrixWorld(true);const rcR=new THREE.Raycaster(),vR=new THREE.Vector3(),dn=new THREE.Vector3(0,-1,0);
  const hS=(x,z)=>{vR.set(x,0,z);NEU.localToWorld(vR);rcR.set(new THREE.Vector3(vR.x,500,vR.z),dn);const h=rcR.intersectObjects(BM,false);if(h.length){const q=NEU.worldToLocal(h[0].point.clone());return q.y;}return hG(x,z);};
  const p=[],ix=[],cR=[],QO=[-1.15,-0.7,0,0.7,1.15],QA=[0,1,1,1,0],QH=[0.02,0.06,0.07,0.06,0.02];let wi=0;
  for(const L0 of(DN.rampenwege||[])){wi++;const L=[];for(let m=0;m<L0.length;m++){L.push(L0[m]);if(m<L0.length-1)for(const f of[1/3,2/3])L.push([L0[m][0]+(L0[m+1][0]-L0[m][0])*f,L0[m][1]+(L0[m+1][1]-L0[m][1])*f]);}   // t67u O9 S4: Rampe 3x dichter -> folgt Feinrelief statt zu ueberbruecken [A]
   for(let n=0;n<L.length;n++){const[a0,b0]=L[Math.max(0,n-1)],[a1,b1]=L[Math.min(L.length-1,n+1)],dx=a1-a0,dz=b1-b0,l=Math.hypot(dx,dz)||1,nx=-dz/l,nz=dx/l,[x0,z0]=L[n];
    const n3=n/3,end=Math.min(n3,(L.length-1-n)/3),sw=(0.32*Math.sin(n3*0.21+wi*1.7)+0.15*Math.sin(n3*0.57+wi))*Math.min(1,end/4),x=x0+nx*sw,z=z0+nz*sw;const o=p.length/3;
    const hc=hS(x,z);for(let q=0;q<5;q++){const px=x+nx*QO[q],pz=z+nz*QO[q],hq=hS(px,pz),dq=Math.abs(hq-hc);p.push(px,(dq>0.5?hc+Math.sign(hq-hc)*0.5:hq)+QH[q],pz);const v=0.94+0.06*Math.sin(n/3*1.3+q);cR.push(0.25*v,0.19*v,0.12*v,dq>0.5?0:QA[q]*Math.min(1,Math.min(n,L.length-1-n)/6));}   // t67u O9 S5: an Kanten kein senkrechtes Brett (Rand klemmen+ausblenden) [A]
    if(n)for(let q=0;q<4;q++){const A=o-5+q,B=o+q;ix.push(A,A+1,B,A+1,B+1,B);}}}
  if(p.length){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));g.setAttribute('color',new THREE.Float32BufferAttribute(cR,4));g.setIndex(ix);g.computeVertexNormals();
   const me=new THREE.Mesh(g,new THREE.MeshLambertMaterial({vertexColors:true,transparent:true,depthWrite:false,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2}));me.receiveShadow=true;me.renderOrder=2;me.visible=!/[?&]noramp=1/.test(location.search);const gr=new THREE.Group();gr.userData.ebene='wege';gr.add(me);NEU.add(gr);window.__rampenwege=(DN.rampenwege||[]).length;}}
 objekte(DN,HN,NEU,menschPos);}
// ---------- Umschalter, Ebenen, Licht ----------
let modus='neu';const SP={alt:spaltenLesen(DA),neu:spaltenLesen(DN)};const Hf=()=>modus=='neu'?HN:HA;
const setModus=m=>{modus=m;ALT.visible=m=='alt';NEU.visible=m=='neu';$('modus').textContent=m=='neu'?'Ansicht: NEU (Relief t67u, Runde O)':'Ansicht: ALT (t39u)';if(geh)cam.position.y=Hf()(cam.position.x,cam.position.z)+1.7;};
$('balt').onclick=()=>setModus('alt');$('bneu').onclick=()=>setModus('neu');
const ebSicht=()=>document.querySelectorAll('[data-l]').forEach(c=>[ALT,NEU].forEach(R=>R.children.forEach(g=>{if(g.userData.ebene==c.dataset.l)g.visible=c.checked;})));
if(/[?&]nowa=1/.test(location.search)){document.querySelectorAll('[data-l]').forEach(c=>{if(c.dataset.l=='wasser')c.checked=false;});ebSicht();setTimeout(ebSicht,3000);}   // O4: Schalter Wasser aus [A]
if(/[?&]clay=1/.test(location.search)){document.querySelectorAll('[data-l]').forEach(c=>{if(c.dataset.l!='gelaende')c.checked=false;});ebSicht();setTimeout(ebSicht,3000);}   // t55u: nur Gelaende-Form [A]
document.querySelectorAll('[data-l]').forEach(c=>c.onchange=ebSicht);
const licht=()=>{const az=$('az').value*Math.PI/180,el=$('el').value*Math.PI/180;sun.position.set(NX/2+400*Math.cos(el)*Math.sin(az),400*Math.sin(el),NY/2-400*Math.cos(el)*Math.cos(az));sun.intensity=$('st').value/50;};
['az','el','st'].forEach(i=>$(i).oninput=licht);licht();
const V={schraeg:[[NX/2,260,NY+170],[NX/2,0,NY/2]],oben:[[NX/2,520,NY/2+0.1],[NX/2,0,NY/2]],unten:[[NX/2,-260,NY/2+180],[NX/2,-14,NY/2]],rand:[[-40,30,NY+40],[40,-5,NY-40]],rueck:[[NX+120,120,-120],[NX/2,0,NY/2]],nord:[[NX/2,90,-150],[NX/2,0,NY/2]],
 nordwand:[[WF.x+10,40,WF.z+90],[WF.x,6,WF.z-5]],krater:[[160,70,230],[108,4,150]],suedwand:[[170,40,300],[170,-8,225]],sued:[[70,45,330],[75,-16,240]],fluss_ost:[[250,25,265],[219,-12,226]],silh_sued:[[95,-4,236],[200,6,228]],silh_nord:[[WF.x-70,16,WF.z+4],[WF.x+40,20,WF.z]],dorf:[[DN.start.x+22,14,DN.start.z+26],[DN.start.x,1,DN.start.z]]};
let geh=false,yaw=0,pitch=0;const setView=n=>{geh=false;oc.enabled=true;const [p,t]=V[n];cam.position.set(...p);oc.target.set(...t);oc.update();};
const boden=(x,z,yw,pt=0)=>{geh=true;oc.enabled=false;yaw=yw;pitch=pt;cam.position.set(x,Hf()(x,z)+1.7,z);cam.rotation.set(pitch,yaw,0,'YXZ');};
const V2={totale_auge:[DN.start.x,DN.start.z+30,0,0.06]};V.totale_auge=null;
const amWand=()=>{let best=[WF.x+4,WF.z+22],bs=-1e9;for(let dz=14;dz<=34;dz+=2)for(let dx=-12;dx<=12;dx+=2){const cx=WF.x+dx,cz=WF.z+dz;let s=-Math.abs(dz-20)*0.3-Math.abs(dx)*0.2;
  for(const h of DN.haeuser){const r=Math.max(h.b,h.t)/2+2;for(let k=0;k<=10;k++){const px=cx+(WF.x-cx)*k/10,pz=cz+(WF.z-cz)*k/10;if(Math.hypot(h.x-px,h.z-pz)<r+(k==0?4:0))s-=100;}}
  if(s>bs){bs=s;best=[cx,cz];}}const [cx,cz]=best;boden(cx,cz,Math.atan2(-(WF.x-cx),-(WF.z-cz)),0.32);};   // freie Sichtlinie zur Wand [A]
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
 R.traverseVisible(o=>{if(o.isMesh&&(o.userData.haus||o.userData.mensch||o.userData.boden||o.userData.hausFlaechen))ziele.push(o)});const h=rc.intersectObjects(ziele,false)[0];let txt='nichts getroffen',res=null;
 const hu=h&&(h.object.userData.hausFlaechen?h.object.userData.haeuser[h.object.userData.hausFlaechen[h.faceIndex]]:h.object.userData.haus);
 if(hu){const u=hu;res={art:'gebaeude',skin_slot:'haus_'+u.typ.toLowerCase(),...u};txt=`<b>Gebäude-Platzhalter E40</b>\nid ${u.id} · ${u.typ}\n${u.b}×${u.t} m, Höhe ${u.h} m [A]`;}
 else if(h&&h.object.userData.mensch&&!hu){res={art:'mensch'};txt='<b>Referenzfigur</b> 1,8 m';}
 else if(h){const n=h.face.normal.clone().transformDirection(h.object.matrixWorld),pt=h.point.clone().addScaledVector(n,-0.05);
  const cx=Math.min(NX-1,Math.max(0,Math.floor(pt.x))),cy=Math.min(NY-1,Math.max(0,Math.floor(pt.z)));const z=zelle(cx,cy);res={art:(h.object.name=='felswand'||(modus=='neu'&&Math.abs(n.y)<COSW))?'felswand':'zelle',...z};
  mk.position.set(cx+0.5,Hf()(cx+0.5,cy+0.5)+0.15,cy+0.5);mk.visible=true;txt=(res.art=='felswand'?'<b>Felswand</b> an ':'')+'<b>Zelle '+z.zell_id+'</b> ('+modus+')\n'+Object.entries(z).map(([k,v])=>k+': '+v).join('\n');}
 $('info').innerHTML=txt;window.__letzterKlick=res;return res;}
window.__test={setView:n=>V2[n]?boden(...V2[n]):setView(n),kam:(p,t)=>{V.__k=[p,t];setView('__k')},strahl:(P)=>{const rc=new THREE.Raycaster(),ms={g:[],w:[]};NEU.traverse(o=>{if(!o.isMesh||o.isInstancedMesh)return;let e='';for(let q=o;q;q=q.parent)if(q.userData&&q.userData.ebene){e=q.userData.ebene;break}if(e=='gelaende')ms.g.push(o);if(e=='wasser')ms.w.push(o)});const d=new THREE.Vector3(0,-1,0);return P.map(([x,z])=>{rc.set(new THREE.Vector3(x,200,z),d);const hg=rc.intersectObjects(ms.g,false),hw=rc.intersectObjects(ms.w,false);return[hg.length?+hg[0].point.y.toFixed(3):null,hw.length?+hw[0].point.y.toFixed(3):null]})},boden,amWand,setModus,klick,start:DN.start,wandfuss:WF,haus0:DN.haeuser.find(h=>h.typ.startsWith('FUNKTION:Kaserne')),
 klickWelt:(x,y,z)=>{const v=new THREE.Vector3(x,y,z).project(cam);return klick((v.x+1)/2*innerWidth,(1-v.y)/2*innerHeight);},H:(x,z)=>Hf()(x,z),bereit:true};
setModus('neu');
let t0=performance.now();window.__szene=sc;window.__info=()=>({dreiecke_gerendert:ren.info.render.triangles,draws:ren.info.render.calls,haus_dreiecke:window.__hausDreiecke,zaun:window.__zaun});ren.setAnimationLoop(()=>{const t=performance.now(),dt=Math.min(0.1,(t-t0)/1000);t0=t;
 if(geh){const v=(keys.shift?12:4)*dt,f=new THREE.Vector3(-Math.sin(yaw),0,-Math.cos(yaw)),r=new THREE.Vector3(-f.z,0,f.x);
  if(keys.w)cam.position.addScaledVector(f,v);if(keys.s)cam.position.addScaledVector(f,-v);if(keys.d)cam.position.addScaledVector(r,v);if(keys.a)cam.position.addScaledVector(r,-v);
  cam.position.y=Hf()(cam.position.x,cam.position.z)+1.7;cam.rotation.set(pitch,yaw,0,'YXZ');}else oc.update();if(window.__wu)window.__wu.value=t/1000;(window.__fb&&(__fb.visible=cam.position.y>-30)),swPass(),ren.render(sc,cam);});
onresize=()=>{cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix();ren.setSize(innerWidth,innerHeight);};
$('lade').remove();})().catch(e=>{document.body.insertAdjacentHTML('beforeend','<pre style="color:red">'+e.stack+'</pre>');throw e;});
