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
ren.setSize(innerWidth,innerHeight);ren.shadowMap.enabled=true;ren.shadowMap.type=THREE.PCFShadowMap;ren.toneMapping=THREE.ACESFilmicToneMapping;ren.toneMappingExposure=1.0;document.body.appendChild(ren.domElement);
const sc=new THREE.Scene();{const c=document.createElement('canvas');c.width=2;c.height=256;const x=c.getContext('2d'),g=x.createLinearGradient(0,0,0,256);g.addColorStop(0,'#5d8fc9');g.addColorStop(0.55,'#a9c6e4');g.addColorStop(1,'#dfe8ef');x.fillStyle=g;x.fillRect(0,0,2,256);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;sc.background=t;}sc.fog=new THREE.FogExp2(0xc9d8e6,0.0007);   // t43u leichter Dunst [A]
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
const oc=new OrbitControls(cam,ren.domElement);oc.enableDamping=true;oc.maxPolarAngle=Math.PI;oc.screenSpacePanning=true;
sc.add(new THREE.HemisphereLight(0xc2d8f2,0xa39c8e,1.2));
const sun=new THREE.DirectionalLight(0xfff0d8,1.6);sun.castShadow=true;sun.shadow.bias=-0.0003;sun.shadow.normalBias=0.12;sun.shadow.mapSize.set(4096,4096);sun.shadow.radius=1.6;
Object.assign(sun.shadow.camera,{left:-238,right:238,top:238,bottom:-238,near:1,far:900});sun.target.position.set(NX/2,0,NY/2);sc.add(sun,sun.target);
const ladeTex=u=>{const t=new THREE.TextureLoader().load(u);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;return t;};
const geo=(p,ix,uv,col)=>{const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));if(uv)g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));if(col)g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));if(ix)g.setIndex(ix);g.computeVertexNormals();return g;};
function sockel(Hrand,tief,root){const sp2=[],si=[],rand=[];for(let i=0;i<=NX;i++)rand.push([i,0]);for(let j=1;j<=NY;j++)rand.push([NX,j]);for(let i=NX-1;i>=0;i--)rand.push([i,NY]);for(let j=NY-1;j>=0;j--)rand.push([0,j]);
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
 {const hmat=new THREE.MeshLambertMaterial({color:0xd9c7a8}),fmat=new THREE.MeshLambertMaterial({color:0xc98a4a}),dmat=new THREE.MeshLambertMaterial({color:0x8a3b2e}),pmat=new THREE.MeshLambertMaterial({color:0xb0a48c});
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
const NEU=new THREE.Group();sc.add(NEU);const G=f32(DN.G),WV=f32(DN.WV),RS=DN.rs,GX=NX*RS+1,GY=NY*RS+1,COSW=Math.cos(DN.wandwinkel*Math.PI/180);
const HN=(x,z)=>{x=Math.min(Math.max(x*RS,0),GX-1.001);z=Math.min(Math.max(z*RS,0),GY-1.001);const i=x|0,j=z|0,fx=x-i,fz=z-j,k=j*GX+i;
 return G[k]*(1-fx)*(1-fz)+G[k+1]*fx*(1-fz)+G[k+GX]*(1-fx)*fz+G[k+GX+1]*fx*fz;};
{const p=new Float32Array(GX*GY*3),VC=u8(DN.VC),cl=new Float32Array(GX*GY*3);for(let k=0;k<GX*GY;k++){const i=k%GX,j=(k/GX)|0;p.set([i/RS,G[k],j/RS],k*3);for(let c=0;c<3;c++)cl[k*3+c]=Math.pow(VC[k*3+c]/255,2.2);}
 // t43u: EIN Bodennetz; Farbe = Material-Gewichte aus Zelleigenschaften (Vertexfarbe), Fels weich ueber Neigung + triplanar Wandtextur
 const bi=[];let nw=0;const tri=(a,b,c)=>{bi.push(a,b,c);const A=a*3,B=b*3,C=c*3,ux=p[B]-p[A],uy=p[B+1]-p[A+1],uz=p[B+2]-p[A+2],vx=p[C]-p[A],vy=p[C+1]-p[A+1],vz=p[C+2]-p[A+2];
  const nx=uy*vz-uz*vy,ny=uz*vx-ux*vz,nz=ux*vy-uy*vx;if(Math.abs(ny)/Math.hypot(nx,ny,nz)<COSW-1e-7)nw++;};
 const LS=(Math.min(innerWidth,innerHeight)<700||/lod=1/.test(location.search))?2:1;window.__lod=LS;   // LOD Handy [A]
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
  p.set(q);}
 const gb=new THREE.BufferGeometry();gb.setAttribute('position',new THREE.BufferAttribute(p,3));gb.setAttribute('color',new THREE.BufferAttribute(cl,3));gb.setIndex(bi);gb.computeVertexNormals();
 const wt=ladeTex(window.WANDTEX),dt=ladeTex(window.RTEX);for(const t of[wt,dt]){t.wrapS=t.wrapT=THREE.RepeatWrapping;t.colorSpace=THREE.NoColorSpace;}
 const mat=new THREE.MeshLambertMaterial({vertexColors:true,side:THREE.DoubleSide});
 mat.onBeforeCompile=sh=>{sh.uniforms.tW={value:wt};sh.uniforms.tD={value:dt};
  sh.vertexShader='varying vec3 vWP;varying vec3 vWN;\n'+sh.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvWP=(modelMatrix*vec4(transformed,1.)).xyz;vWN=normalize(mat3(modelMatrix)*objectNormal);');
  sh.fragmentShader='uniform sampler2D tW;uniform sampler2D tD;varying vec3 vWP;varying vec3 vWN;\n'+sh.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
   vec3 N=normalize(vWN);vec3 w=pow(abs(N),vec3(4.));w/=w.x+w.y+w.z;
   vec3 tr=texture2D(tW,vWP.zy/9.).rgb*w.x+texture2D(tW,vWP.xy/9.).rgb*w.z+texture2D(tW,vWP.xz/9.).rgb*w.y;
   vec3 tr2=texture2D(tW,vWP.zy/23.+.37).rgb*w.x+texture2D(tW,vWP.xy/23.+.37).rgb*w.z+texture2D(tW,vWP.xz/23.+.37).rgb*w.y;
   float d=texture2D(tD,vWP.xz/4.).r*0.6+texture2D(tD,vWP.xz/23.).r*0.4,gD=texture2D(tD,vWP.xz/61.+.2).r;
   diffuseColor.rgb*=(0.72+0.33*d)*(0.90+0.2*gD);
   {float f=texture2D(tD,vWP.xz/1.4+.37).r,L=dot(diffuseColor.rgb,vec3(.33));float sw=smoothstep(.55,.75,L);diffuseColor.rgb*=1.+sw*(f-.5)*.12;diffuseColor.rgb=mix(diffuseColor.rgb,diffuseColor.rgb*vec3(.90,.95,1.05),sw*(1.-d)*.6);}
   float st=1.-smoothstep(0.40,0.72,abs(N.y)+0.10*(d-0.8));
   vec3 tx=mix(tr,tr2,0.35);float r=dot(tx,vec3(0.33));
   vec3 fels=pow(tx,vec3(2.2))*vec3(1.05,0.98,0.92)*mix(0.85,1.25,gD)*1.15;
   float sn=smoothstep(0.48,0.62,abs(N.y)+0.18*(r-0.5));   // Schnee auf Simsen/Kanten [A]
   {float g2=texture2D(tD,vWP.xz/97.+vec2(.1,vWP.y/60.)).r;fels*=mix(vec3(.88,.92,1.0),vec3(1.10,1.0,.86),g2);   // grossraeumige Farbe [A]
    float ms=smoothstep(.30,.48,abs(N.y)+0.15*(r-0.5))*(1.-sn)*smoothstep(.45,.6,gD);fels=mix(fels,vec3(.16,.20,.11),ms*.55);}   // Moos auf Absaetzen [A]
   fels=mix(fels,vec3(0.80,0.84,0.90),sn*0.9);
   diffuseColor.rgb=mix(diffuseColor.rgb,fels,st);`).replace('#include <normal_fragment_maps>',`#include <normal_fragment_maps>
   {vec3 N2=normalize(vWN);vec3 w2=pow(abs(N2),vec3(4.));w2/=w2.x+w2.y+w2.z;   // t48u R5: Detail-Bump (triplanar) gegen "verpixelt" [A]
    float hb=(texture2D(tW,vWP.zy/3.).r*w2.x+texture2D(tW,vWP.xy/3.).r*w2.z+texture2D(tD,vWP.xz/1.7).r*w2.y)*0.7+(texture2D(tW,vWP.zy/9.).r*w2.x+texture2D(tW,vWP.xy/9.).r*w2.z+texture2D(tD,vWP.xz/6.).r*w2.y)*0.3;
    vec3 dpx=dFdx(-vViewPosition),dpy=dFdy(-vViewPosition);vec3 r1=cross(dpy,normal),r2=cross(normal,dpx);float det=dot(dpx,r1);
    vec3 grd=sign(det)*(dFdx(hb)*r1+dFdy(hb)*r2)*(0.6+1.4*(1.-abs(N2.y)));normal=normalize(abs(det)*normal-grd);}`);};
 const m=new THREE.Mesh(gb,mat);m.receiveShadow=m.castShadow=true;m.userData.boden=1;
 let fwMesh=null;if(FW){const b2=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0)).buffer,FS=FW.fs,FX=NX*FS+1,vid=new Uint32Array(b2(FW.vid)),fh=new Float32Array(b2(FW.h)),fc=new Uint8Array(b2(FW.c)),S=FS/(LS==1?1:2)>=1?(LS==1?1:2):1;
  const map=new Int32Array(FX*(NY*FS+1)).fill(-1);vid.forEach((k,n)=>map[k]=n);const fp=new Float32Array(vid.length*3),fcl=new Float32Array(vid.length*3);
  vid.forEach((k,n)=>{fp[n*3]=(k%FX)/FS;fp[n*3+1]=fh[n];fp[n*3+2]=((k/FX)|0)/FS;for(let c=0;c<3;c++)fcl[n*3+c]=Math.pow(fc[n*3+c]/255,2.2);});
  const fi=[];for(let z=0;z<NX*NY;z++){if(!BANDZ[z])continue;const x=z%NX,y=(z/NX)|0;for(let dj=0;dj<FS;dj+=S)for(let di=0;di<FS;di+=S){const a=map[(y*FS+dj)*FX+x*FS+di],b=map[(y*FS+dj)*FX+x*FS+di+S],c=map[(y*FS+dj+S)*FX+x*FS+di],d=map[(y*FS+dj+S)*FX+x*FS+di+S];fi.push(a,c,d,a,d,b);}}
  const fg=new THREE.BufferGeometry();fg.setAttribute('position',new THREE.BufferAttribute(fp,3));fg.setAttribute('color',new THREE.BufferAttribute(fcl,3));fg.setIndex(fi);fg.computeVertexNormals();
  fwMesh=new THREE.Mesh(fg,mat);fwMesh.receiveShadow=fwMesh.castShadow=true;fwMesh.userData.boden=1;window.__fw={dreiecke:fi.length/3,lod:S};}
 const g=new THREE.Group();g.userData.ebene='gelaende';g.add(m);if(fwMesh)g.add(fwMesh);NEU.add(g);
 if(/[?&]glb=1/.test(location.search)&&location.protocol.startsWith('http')){   // t48u R5: GLB-Pfad (lokaler Server), sonst Single-File-Daten [A]
  new GLTFLoader().load('dorfmap_relief_z25.glb',gl=>{const mat=new THREE.MeshLambertMaterial({vertexColors:true,side:THREE.DoubleSide});gl.scene.traverse(o=>{if(o.isMesh){o.material=mat;o.receiveShadow=true;o.castShadow=true;}});
   g.visible=false;const gg=new THREE.Group();gg.userData.ebene='gelaende';gg.add(gl.scene);NEU.add(gg);window.__glb={ok:true,meshes:gl.scene.children.length};},undefined,e=>{window.__glb={ok:false,fehler:String(e)};});}
 window.__dreiecke={boden:bi.length/3-nw,wand:nw};
 // Wege-Overlay: weicher Rand ueber Vertex-Alpha
 {const A=u8(DN.WEGA),wp=[],wc=[],wi=[],map=new Int32Array(GX*GY).fill(-1);const vx=k=>{if(map[k]<0){map[k]=wp.length/3;const i=k%GX,j=(k/GX)|0,h=hash(i,j);wp.push(i/RS,G[k]+0.05,j/RS);{const a=A[k]/255,e=a*a;wc.push(0.62-0.30*e+0.04*h,0.58-0.30*e+0.03*h,0.54-0.30*e+0.02*h,Math.min(0.85,Math.pow(a,1.4)*0.95));}}return map[k];};
  for(let j=0;j<GY-1;j++)for(let i=0;i<GX-1;i++){const a=j*GX+i,b=a+1,c=a+GX,d=c+1;if(A[a]|A[b]|A[c]|A[d])wi.push(vx(a),vx(c),vx(d),vx(a),vx(d),vx(b));}
  const wg=new THREE.BufferGeometry();wg.setAttribute('position',new THREE.Float32BufferAttribute(wp,3));wg.setAttribute('color',new THREE.Float32BufferAttribute(wc,4));wg.setIndex(wi);wg.computeVertexNormals();
  DN.wegMesh=new THREE.Mesh(wg,new THREE.MeshLambertMaterial({vertexColors:true,transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-2}));DN.wegMesh.receiveShadow=true;}
 sockel((i,j)=>{const k=Math.min(j*RS,GY-1)*GX+Math.min(i*RS,GX-1);return p[k*3+1];},-34,g);
 {const wp=[],wc=[],wi=[],map=new Int32Array(GX*GY).fill(-1),ok=k=>WV[k]>-900;const vx=k=>{if(map[k]<0){map[k]=wp.length/3;const i=k%GX,j=(k/GX)|0,t=ok(k)?Math.min(1,Math.max(0,(WV[k]-G[k])/1.5)):0;
   wp.push(i/RS,ok(k)?WV[k]:G[k]+0.02,j/RS);{const e=1-Math.min(1,t*4),q=(n=>ok(n)?Math.abs(WV[n]-WV[k]):0),fo=ok(k)?Math.min(1,Math.max(0,(q(k+1)+q(k-1)+q(k+GX)+q(k-GX)-0.35)*1.2)):0;   // t48u: Schaum/Wasserfall an Stufen [A]
   wc.push((0.06+0.5*e*e)*(1-fo)+0.86*fo,(0.16+0.48*e*e)*(1-fo)+0.90*fo,(0.21+0.45*e*e)*(1-fo)+0.93*fo,ok(k)?Math.max(0.55+0.35*Math.max(t,e*e),0.9*fo):0);};}return map[k];};   // flach hell/klar, tief dunkler [A]
  for(let j=0;j<GY-1;j++)for(let i=0;i<GX-1;i++){const a=j*GX+i,b=a+1,c=a+GX,d=c+1;if(ok(a)||ok(b)||ok(c)||ok(d))wi.push(vx(a),vx(c),vx(d),vx(a),vx(d),vx(b));}
  const g2=new THREE.BufferGeometry();g2.setAttribute('position',new THREE.Float32BufferAttribute(wp,3));g2.setAttribute('color',new THREE.Float32BufferAttribute(wc,4));g2.setIndex(wi);g2.computeVertexNormals();
  const wg=new THREE.Group();wg.userData.ebene='wasser';const wmesh=new THREE.Mesh(g2,new THREE.MeshPhongMaterial({vertexColors:true,transparent:true,depthWrite:false,shininess:90,specular:0x667788,side:THREE.DoubleSide}));wmesh.receiveShadow=true;const wu={value:0};window.__wu=wu;wmesh.material.onBeforeCompile=sh=>{sh.uniforms.uT=wu;sh.vertexShader='varying vec3 vWQ;\n'+sh.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\n vWQ=(modelMatrix*vec4(transformed,1.)).xyz;');
  sh.fragmentShader='uniform float uT;varying vec3 vWQ;\n'+sh.fragmentShader.replace('#include <color_fragment>','#include <color_fragment>\n {float s=sin(vWQ.x*.31+vWQ.z*.11-uT*.9)*sin(vWQ.z*.47-vWQ.x*.05+uT*.6)+.5*sin(vWQ.x*1.3-vWQ.z*.9-uT*1.7);diffuseColor.rgb*=1.+.07*s;diffuseColor.rgb+=vec3(.025,.03,.035)*max(0.,s-.6);}');};wg.add(wmesh);NEU.add(wg);}
 {const hG=(x,z)=>{const fi=Math.min(GX-2,Math.max(0,x*RS)),fj=Math.min(GY-2,Math.max(0,z*RS)),i=fi|0,j=fj|0,a=fi-i,b=fj-j,k=j*GX+i;return G[k]*(1-a)*(1-b)+G[k+1]*a*(1-b)+G[k+GX]*(1-a)*b+G[k+GX+1]*a*b;};   // t48u R5: Rampen-Pfade als Overlay (Ebene wege) [A]
  const p=[],ix=[];for(const L of(DN.rampenwege||[])){for(let n=0;n<L.length;n++){const[a0,b0]=L[Math.max(0,n-1)],[a1,b1]=L[Math.min(L.length-1,n+1)],dx=a1-a0,dz=b1-b0,l=Math.hypot(dx,dz)||1,ox=-dz/l*0.8,oz=dx/l*0.8,[x,z]=L[n];
    const o=p.length/3;p.push(x+ox,hG(x+ox,z+oz)+0.10,z+oz,x-ox,hG(x-ox,z-oz)+0.10,z-oz);if(n)ix.push(o-2,o-1,o,o-1,o+1,o);}}
  if(p.length){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));g.setIndex(ix);g.computeVertexNormals();
   const me=new THREE.Mesh(g,new THREE.MeshLambertMaterial({color:0x9a8a72,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2}));me.receiveShadow=true;const gr=new THREE.Group();gr.userData.ebene='wege';gr.add(me);NEU.add(gr);window.__rampenwege=(DN.rampenwege||[]).length;}}
 objekte(DN,HN,NEU,menschPos);}
// ---------- Umschalter, Ebenen, Licht ----------
let modus='neu';const SP={alt:spaltenLesen(DA),neu:spaltenLesen(DN)};const Hf=()=>modus=='neu'?HN:HA;
const setModus=m=>{modus=m;ALT.visible=m=='alt';NEU.visible=m=='neu';$('modus').textContent=m=='neu'?'Ansicht: NEU (Relief t43u)':'Ansicht: ALT (t39u)';if(geh)cam.position.y=Hf()(cam.position.x,cam.position.z)+1.7;};
$('balt').onclick=()=>setModus('alt');$('bneu').onclick=()=>setModus('neu');
const ebSicht=()=>document.querySelectorAll('[data-l]').forEach(c=>[ALT,NEU].forEach(R=>R.children.forEach(g=>{if(g.userData.ebene==c.dataset.l)g.visible=c.checked;})));
document.querySelectorAll('[data-l]').forEach(c=>c.onchange=ebSicht);
const licht=()=>{const az=$('az').value*Math.PI/180,el=$('el').value*Math.PI/180;sun.position.set(NX/2+400*Math.cos(el)*Math.sin(az),400*Math.sin(el),NY/2-400*Math.cos(el)*Math.cos(az));sun.intensity=$('st').value/50;};
['az','el','st'].forEach(i=>$(i).oninput=licht);licht();
const V={schraeg:[[NX/2,260,NY+170],[NX/2,0,NY/2]],oben:[[NX/2,520,NY/2+0.1],[NX/2,0,NY/2]],unten:[[NX/2,-260,NY/2+180],[NX/2,-14,NY/2]],rand:[[-40,30,NY+40],[40,-5,NY-40]],rueck:[[NX+120,120,-120],[NX/2,0,NY/2]],nord:[[NX/2,90,-150],[NX/2,0,NY/2]],
 nordwand:[[WF.x+10,40,WF.z+90],[WF.x,6,WF.z-5]],krater:[[160,70,230],[108,4,150]],suedwand:[[170,40,300],[170,-8,225]],sued:[[70,45,330],[75,-16,240]],fluss_ost:[[250,25,265],[219,-12,226]],dorf:[[DN.start.x+22,14,DN.start.z+26],[DN.start.x,1,DN.start.z]]};
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
window.__test={setView:n=>V2[n]?boden(...V2[n]):setView(n),boden,amWand,setModus,klick,start:DN.start,wandfuss:WF,haus0:DN.haeuser.find(h=>h.typ.startsWith('FUNKTION:Kaserne')),
 klickWelt:(x,y,z)=>{const v=new THREE.Vector3(x,y,z).project(cam);return klick((v.x+1)/2*innerWidth,(1-v.y)/2*innerHeight);},H:(x,z)=>Hf()(x,z),bereit:true};
setModus('neu');
let t0=performance.now();window.__szene=sc;window.__info=()=>({dreiecke_gerendert:ren.info.render.triangles,draws:ren.info.render.calls,haus_dreiecke:window.__hausDreiecke,zaun:window.__zaun});ren.setAnimationLoop(()=>{const t=performance.now(),dt=Math.min(0.1,(t-t0)/1000);t0=t;
 if(geh){const v=(keys.shift?12:4)*dt,f=new THREE.Vector3(-Math.sin(yaw),0,-Math.cos(yaw)),r=new THREE.Vector3(-f.z,0,f.x);
  if(keys.w)cam.position.addScaledVector(f,v);if(keys.s)cam.position.addScaledVector(f,-v);if(keys.d)cam.position.addScaledVector(r,v);if(keys.a)cam.position.addScaledVector(r,-v);
  cam.position.y=Hf()(cam.position.x,cam.position.z)+1.7;cam.rotation.set(pitch,yaw,0,'YXZ');}else oc.update();if(window.__wu)window.__wu.value=t/1000;(window.__fb&&(__fb.visible=cam.position.y>-30)),ren.render(sc,cam);});
onresize=()=>{cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix();ren.setSize(innerWidth,innerHeight);};
$('lade').remove();})().catch(e=>{document.body.insertAdjacentHTML('beforeend','<pre style="color:red">'+e.stack+'</pre>');throw e;});
