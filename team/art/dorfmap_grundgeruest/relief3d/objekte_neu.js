// t44u: echte 3D-Platzhalter-Objekte fuer NEU (Fichten/Kiefern, Felsen, Haeuser). Alle Masse [A]. Instancing wo moeglich.
import * as THREE from 'three';
const hash=(a,b)=>{const v=Math.sin(a*12.9898+b*78.233)*43758.5453;return v-Math.floor(v);};
const lin=h=>new THREE.Color(h);   // Color(hex) ist sRGB -> intern linear
// nicht-indizierte Dreiecke mit Farbe -> flache Normalen
class Bau{constructor(){this.p=[];this.c=[];this.f=[];}
 tri(a,b,c,col,id=-1){this.p.push(...a,...b,...c);for(let i=0;i<3;i++)this.c.push(col.r,col.g,col.b);this.f.push(id);}
 quad(a,b,c,d,col,id){this.tri(a,b,c,col,id);this.tri(a,c,d,col,id);}
 box(x0,y0,z0,x1,y1,z1,col,id,ohneBoden=true){const P=(x,y,z)=>[x,y,z];
  const v=[P(x0,y0,z0),P(x1,y0,z0),P(x1,y0,z1),P(x0,y0,z1),P(x0,y1,z0),P(x1,y1,z0),P(x1,y1,z1),P(x0,y1,z1)];
  const F=[[0,4,5,1],[1,5,6,2],[2,6,7,3],[3,7,4,0],[4,7,6,5]];if(!ohneBoden)F.push([0,1,2,3]);for(const [a,b,c,d] of F)this.quad(v[a],v[b],v[c],v[d],col,id);}
 geo(){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(this.p,3));g.setAttribute('color',new THREE.Float32BufferAttribute(this.c,3));g.computeVertexNormals();return g;}}
// ---- Baeume ----
function fichte(var_){const B=new Bau(),r=s=>hash(var_*7.1,s);const stamm=lin(0x4a3322);
 B.box(-0.05,0,-0.05,0.05,0.35,0.05,stamm);const lagen=5+Math.floor(r(1)*2);
 for(let k=0;k<lagen;k++){const t=k/lagen,y0=0.18+t*0.70,hh=0.30-0.08*t,R=(0.40-0.30*t)*(0.9+0.2*r(k+3)),n=9;
  const gr=lin(0x1f3d2c).lerp(lin(0x2c4a30),r(k+11)),sn=lin(0xe9eef4);
  const top=[0,y0+hh,0];for(let i=0;i<n;i++){const a0=i/n*6.283+k,a1=(i+1)/n*6.283+k,rr=i=>R*(i%2?0.78:1.0);
   const A=[Math.cos(a0)*rr(i),y0-0.04*(i%2),Math.sin(a0)*rr(i)],C=[Math.cos(a1)*rr(i+1),y0-0.04*((i+1)%2),Math.sin(a1)*rr(i+1)];
   const m=(P,f)=>[top[0]+(P[0]-top[0])*f,top[1]+(P[1]-top[1])*f,top[2]+(P[2]-top[2])*f],f=0.55+0.25*r(k*13+i),A1=m(A,f),C1=m(C,f);   // Schnee innen, Zweigspitzen gruen
   B.tri(top,C1,A1,sn);B.quad(A1,C1,C,A,gr);B.tri(A,C,[0,y0-0.02,0],gr.clone().multiplyScalar(0.6));}}
 return B.geo();}
function kiefer(var_){const B=new Bau(),r=s=>hash(var_*3.3,s);const stamm=lin(0x6b4a33);
 B.box(-0.04,0,-0.04,0.04,0.72,0.04,stamm);
 for(let k=0;k<3;k++){const cx=(r(k)-0.5)*0.25,cy=0.70+k*0.09,cz=(r(k+5)-0.5)*0.25,R=0.22+0.08*r(k+9),g=new THREE.IcosahedronGeometry(1,0).toNonIndexed();
  const P=g.attributes.position;for(let i=0;i<P.count;i+=3){const ny=(P.getY(i)+P.getY(i+1)+P.getY(i+2))/3;const col=ny>0.35?lin(0xe6ecf2):lin(0x2a4630);
   const pts=[0,1,2].map(j=>[cx+P.getX(i+j)*R,cy+P.getY(i+j)*R*0.45,cz+P.getZ(i+j)*R]);B.tri(pts[0],pts[1],pts[2],col);}}
 return B.geo();}
// ---- Felsen: verformter Ikosaeder, Schnee oben, Flechten ----
function fels(var_){const g=new THREE.IcosahedronGeometry(0.55,2),P=g.attributes.position;
 for(let i=0;i<P.count;i++){const v=new THREE.Vector3().fromBufferAttribute(P,i),n=v.clone().normalize();
  let f=1+0.22*Math.sin(n.x*3.1+var_)*Math.cos(n.z*2.7-var_*2)+0.12*Math.sin(n.y*6+n.x*5+var_*3);
  if(n.dot(new THREE.Vector3(Math.cos(var_*5),0.3,Math.sin(var_*5)).normalize())>0.55)f*=0.82;   // Bruchflaeche
  v.multiplyScalar(f);v.y*=0.72;P.setXYZ(i,v.x,v.y,v.z);}
 const ng=g.toNonIndexed();ng.computeVertexNormals();const N=ng.attributes.normal,Q=ng.attributes.position,col=[];
 for(let i=0;i<Q.count;i+=3){const ny=(N.getY(i)+N.getY(i+1)+N.getY(i+2))/3,h=hash(i,var_);
  const c=ny>0.62?lin(0xe4e9ef):(h<0.12?lin(0x6f7350):lin(0x75706a).multiplyScalar(0.75+0.4*h));for(let j=0;j<3;j++)col.push(c.r,c.g,c.b);}
 ng.setAttribute('color',new THREE.Float32BufferAttribute(col,3));ng.translate(0,0.22,0);return ng;}
// ---- Haeuser ----
const WAND={Hütte:[0x7a5a3c,0x6e4f34],Standard:[0xd8cdb6,0xcfc2a6],schmal:[0xcbbfa5,0xb9ab8e],Turmhaus:[0x9c968c,0x8d877e],kompakt:[0xd2c4a8,0xc7b796],
 Doppelhaus:[0xd6c9ae,0xc9bb9c],Eckhaus:[0xcfc0a2,0xc2b393],'FUNKTION:Ressource':[0x8a6a48,0x7a5d40],'FUNKTION:Kaserne':[0x8f8a80,0x847f76],'FUNKTION:Spezial':[0xa49c8e,0x958e80],'FUNKTION:Starthaus':[0xc9a878,0xbd9c6c]};
function haus(B,h,id){const b=h.b*0.9,t=h.t*0.9,platz=h.typ=='Quartiersplatz',x=h.x,z=h.z,y=h.y,lang=b>=t;
 if(platz){B.box(x-b/2,y-0.3,z-t/2,x+b/2,y+0.12,z+t/2,lin(0x9a948a),id);return;}
 const turm=h.typ=='Turmhaus',holz=h.typ=='Hütte'||h.typ=='FUNKTION:Ressource';const wc=WAND[h.typ]||WAND.Standard,wcol=lin(wc[0]).lerp(lin(wc[1]),hash(id,1));
 const wh=Math.max(2.4,turm?h.h*0.85:h.h*0.62),sock=0.6;
 B.box(x-b/2-0.1,y-1.0,z-t/2-0.1,x+b/2+0.1,y+sock,z+t/2+0.1,lin(0x6d6a64).multiplyScalar(0.9+0.2*hash(id,2)),id);   // Steinsockel, in Hang eingelassen
 B.box(x-b/2,y+sock,z-t/2,x+b/2,y+wh,z+t/2,wcol,id);
 if(!holz&&!turm){const fw=lin(0x5a3a24);for(const s of[-1,1]){B.box(x-b/2-0.02,y+sock,z+s*t/2-0.14,x+b/2+0.02,y+sock+0.18,z+s*t/2+0.14,fw,id);B.box(x-b/2-0.02,y+wh-0.2,z+s*t/2-0.14,x+b/2+0.02,y+wh,z+s*t/2+0.14,fw,id);
}
  for(const sx of[-1,1])for(const sz of[-1,1])B.box(x+sx*b/2-0.16,y+sock,z+sz*t/2-0.16,x+sx*b/2+0.16,y+wh,z+sz*t/2+0.16,fw,id);}   // Fachwerk-Ecken/Balken
 // Fenster und Tuer: dunkles Glas mit hellem Rahmen, leicht vorgesetzt
 const fen=lin(0x223038),rah=lin(0xe8e0cc),tur=lin(0x4b2e1c);const L=lang?b:t,Q=lang?t:b;
 const setz=(u,v,w,hgt,seite,col,tiefe=0.06)=>{const s=seite*Q/2;const pts=lang?[x+u-w/2,z+s,x+u+w/2]:[x+s,z+u-w/2,z+u+w/2];
  if(lang)B.box(pts[0],y+v,z+s-(seite>0?0:tiefe),pts[2],y+v+hgt,z+s+(seite>0?tiefe:0),col,id);else B.box(x+s-(seite>0?0:tiefe),y+v,pts[1],x+s+(seite>0?tiefe:0),y+v+hgt,pts[2],col,id);};
 const nF=Math.max(1,Math.floor((L-1.5)/2.2)),etagen=Math.max(1,Math.floor((wh-sock)/2.4));
 for(const seite of[-1,1])for(let e=0;e<etagen;e++)for(let i=0;i<nF;i++){const u=-L/2+(i+0.5)*L/nF;if(e==0&&seite==1&&i==Math.floor(nF/2))continue;
  setz(u,sock+0.9+e*2.4,0.95,1.05,seite,rah,0.07);setz(u,sock+0.98+e*2.4,0.75,0.88,seite,fen,0.09);}
 setz((nF%2?0:L/(2*nF)),sock,1.1,2.0,1,tur,0.08);setz((nF%2?0:L/(2*nF)),sock+2.0,1.3,0.15,1,rah,0.1);
 // Satteldach mit Ueberstand + Schneehaube; First entlang der langen Seite
 const ov=0.45,dh=turm?Math.min(b,t)*0.9:Math.min(b,t)*0.55,dach=lin(holz?0x4a3424:0x5b3326).lerp(lin(0x3c3a38),hash(id,3)*0.6),sn=lin(0xeef2f7);
 const Y=y+wh,P=(l,q,yy)=>lang?[x+l,yy,z+q]:[x+q,yy,z+l];const l0=-L/2-ov,l1=L/2+ov,q0=-Q/2-ov,q1=Q/2+ov,ys=Y-ov*dh/(Q/2);
 for(const [qa,qb] of[[q0,0],[q1,0]]){const A=P(l0,qa,ys),Bp=P(l1,qa,ys),C=P(l1,qb,Y+dh),D=P(l0,qb,Y+dh);
  const k=qa<0;if(k){B.quad(A,D,C,Bp,dach,id);}else{B.quad(A,Bp,C,D,dach,id);}
  const yq=q=>Y+dh-(Y+dh-ys)*Math.abs(q)/Math.abs(qa)+0.16,qq=qa*0.86;const A2=P(l0+0.08,qq,yq(qq)),B2=P(l1-0.08,qq,yq(qq)),C2=P(l1-0.08,0,Y+dh+0.16),D2=P(l0+0.08,0,Y+dh+0.16);   // Schneehaube [A]
  if(k)B.quad(A2,D2,C2,B2,sn,id);else B.quad(A2,B2,C2,D2,sn,id);}
 for(const l of[-L/2,L/2]){const a=P(l,-Q/2,Y),c=P(l,Q/2,Y),d=P(l,0,Y+dh);B.tri(a,d,c,wcol,id);B.tri(a,c,d,wcol,id);}   // Giebel
 const ks=hash(id,4)-0.5;if(!platz){const cx=lang?x+ks*L*0.5:x+Q*0.2,cz=lang?z+Q*0.2:z+ks*L*0.5;B.box(cx-0.3,Y,cz-0.3,cx+0.3,Y+dh+0.9,cz+0.3,lin(0x6a625a),id);B.box(cx-0.33,Y+dh+0.9,cz-0.33,cx+0.33,Y+dh+1.05,cz+0.33,sn,id);}}
export function objekteNeu(D,H,G,grp){
 const mat=new THREE.MeshLambertMaterial({vertexColors:true});
 const inst=(geo,L,fn,gn,farbe)=>{const m=new THREE.InstancedMesh(geo,mat,L.length),o=new THREE.Object3D(),c=new THREE.Color();L.forEach((e,n)=>{fn(o,e,n);o.updateMatrix();m.setMatrixAt(n,o.matrix);if(farbe){farbe(c,e,n);m.setColorAt(n,c);}});m.castShadow=m.receiveShadow=true;(G[gn]||grp(gn)).add(m);return m;};
 const VAR=4,tf=(o,[x,y,z,h,r])=>{o.position.set(x,y-0.15,z);o.rotation.set((hash(x,z)-0.5)*0.06,r||0,(hash(z,x)-0.5)*0.06);const s=0.85+0.3*hash(z,x+1);o.scale.set(h*s,h,h*s);};
 const fc=(c,b)=>{const t=b[5]??hash(b[0],b[2]);c.setRGB(0.85+0.15*t,0.9+0.1*t,0.85+0.15*(1-t));};
 for(let v=0;v<VAR;v++){inst(fichte(v),D.baeume.filter((b,n)=>(n%5)!=4&&n%VAR==v),tf,'baeume',fc);}
 inst(kiefer(1),D.baeume.filter((b,n)=>(n%5)==4),tf,'baeume',fc);
 const FV=[fels(1),fels(2.3),fels(3.7)];const ff=(o,[x,y,z,h,r])=>{const a=hash(x,z),b=hash(z,x);o.position.set(x,y,z);o.rotation.set((a-0.5)*0.6,r,(b-0.5)*0.6);o.scale.set(h*(0.8+0.5*a),h*(0.55+0.5*b),h*(0.8+0.5*b));};
 const alle=[...D.felsen,...D.findlinge,...D.steine,...(D.geroell||[])];FV.forEach((g,v)=>inst(g,alle.filter((e,n)=>n%3==v),ff,'felsen'));
 const B=new Bau();D.haeuser.forEach((h,i)=>haus(B,h,i));const hmat=new THREE.MeshLambertMaterial({vertexColors:true});hmat.onBeforeCompile=sh=>{sh.fragmentShader=sh.fragmentShader.replace('#include <emissivemap_fragment>','#include <emissivemap_fragment>\n totalEmissiveRadiance+=vColor.rgb*0.22;');};   // Aufhellung Schattenseite [A]
 const hm=new THREE.Mesh(B.geo(),hmat);hm.castShadow=hm.receiveShadow=true;hm.userData.hausFlaechen=B.f;hm.userData.haeuser=D.haeuser;grp('gebaeude').add(hm);
 return B.p.length/9;}
