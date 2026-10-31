// t44u: echte 3D-Platzhalter-Objekte fuer NEU (Fichten/Kiefern, Felsen, Haeuser). Alle Masse [A]. Instancing wo moeglich.
import * as THREE from 'three';
const hash=(a,b)=>{const v=Math.sin(a*12.9898+b*78.233)*43758.5453;return v-Math.floor(v);};
const lin=h=>new THREE.Color(h);   // Color(hex) ist sRGB -> intern linear
// nicht-indizierte Dreiecke mit Farbe -> flache Normalen
class Bau{constructor(){this.p=[];this.c=[];this.f=[];}
 tri(a,b,c,col,id=-1){if(this.flip)[b,c]=[c,b];this.p.push(...a,...b,...c);for(let i=0;i<3;i++)this.c.push(col.r,col.g,col.b);this.f.push(id);}
 quad(a,b,c,d,col,id){this.tri(a,b,c,col,id);this.tri(a,c,d,col,id);}
 box(x0,y0,z0,x1,y1,z1,col,id,ohneBoden=true){const fl0=this.flip;this.flip=false;const P=(x,y,z)=>[x,y,z];
  const v=[P(x0,y0,z0),P(x1,y0,z0),P(x1,y0,z1),P(x0,y0,z1),P(x0,y1,z0),P(x1,y1,z0),P(x1,y1,z1),P(x0,y1,z1)];
  const F=[[0,4,5,1],[1,5,6,2],[2,6,7,3],[3,7,4,0],[4,7,6,5]];if(!ohneBoden)F.push([0,1,2,3]);for(const [a,b,c,d] of F)this.quad(v[a],v[b],v[c],v[d],col,id);this.flip=fl0;}
 geo(){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(this.p,3));g.setAttribute('color',new THREE.Float32BufferAttribute(this.c,3));g.computeVertexNormals();return g;}}
// ---- Baeume ----
function fichte(var_){const B=new Bau(),r=s=>hash(var_*7.1,s);const stamm=lin(0x4a3322);
 B.box(-0.05,0,-0.05,0.05,0.35,0.05,stamm);const lagen=5+Math.floor(r(1)*2);
 for(let k=0;k<lagen;k++){const t=k/lagen,y0=0.18+t*0.70,hh=0.30-0.08*t,R=(0.40-0.30*t)*(0.9+0.2*r(k+3)),n=9;
  const gr=lin(0x2e5238).lerp(lin(0x46663f),r(k+11)),sn=lin(0xe9eef4);
  const top=[0,y0+hh,0];for(let i=0;i<n;i++){const a0=i/n*6.283+k,a1=(i+1)/n*6.283+k,rr=i=>R*(i%2?0.78:1.0);
   const A=[Math.cos(a0)*rr(i),y0-0.04*(i%2),Math.sin(a0)*rr(i)],C=[Math.cos(a1)*rr(i+1),y0-0.04*((i+1)%2),Math.sin(a1)*rr(i+1)];
   const m=(P,f)=>[top[0]+(P[0]-top[0])*f,top[1]+(P[1]-top[1])*f,top[2]+(P[2]-top[2])*f],f=0.55+0.25*r(k*13+i),A1=m(A,f),C1=m(C,f);   // Schnee innen, Zweigspitzen gruen
   B.tri(top,C1,A1,sn);B.quad(A1,C1,C,A,gr);B.tri(A,C,[0,y0-0.02,0],gr.clone().multiplyScalar(0.82));}}
 return B.geo();}
function kiefer(var_){const B=new Bau(),r=s=>hash(var_*3.3,s);const stamm=lin(0x6b4a33);
 B.box(-0.04,0,-0.04,0.04,0.72,0.04,stamm);
 for(let k=0;k<3;k++){const cx=(r(k)-0.5)*0.25,cy=0.70+k*0.09,cz=(r(k+5)-0.5)*0.25,R=0.22+0.08*r(k+9),g=new THREE.IcosahedronGeometry(1,0).toNonIndexed();
  const P=g.attributes.position;for(let i=0;i<P.count;i+=3){const ny=(P.getY(i)+P.getY(i+1)+P.getY(i+2))/3;const col=ny>0.35?lin(0xe6ecf2):lin(0x3c5e40);
   const pts=[0,1,2].map(j=>[cx+P.getX(i+j)*R,cy+P.getY(i+j)*R*0.45,cz+P.getZ(i+j)*R]);B.tri(pts[0],pts[1],pts[2],col);}}
 return B.geo();}
// ---- Felsen: verformter Ikosaeder, Schnee oben, Flechten ----
function buschel(){const pos=[],col=[];for(let k=0;k<7;k++){const a=k/7*6.283+0.4*Math.sin(k*3),l=0.25+0.12*Math.sin(k*5),h=0.7+0.3*Math.cos(k*2),w=0.045;   // t48u: Trockengras-Bueschel [A]
  const bx=Math.cos(a)*0.05,bz=Math.sin(a)*0.05,tx=Math.cos(a)*l,tz=Math.sin(a)*l,px=-Math.sin(a)*w,pz=Math.cos(a)*w;
  pos.push(bx-px,0,bz-pz,bx+px,0,bz+pz,tx,h,tz);const c=[0.55+0.05*Math.sin(k),0.48,0.30];col.push(...c.map(q=>q*0.7),...c.map(q=>q*0.7),...c);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));g.computeVertexNormals();return g;}
function block(var_,det,nr){const fm=window.__FM&&window.__FM[nr];let g;if(fm&&det>1){g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(fm.p,3));g.setIndex(fm.i);}else g=new THREE.IcosahedronGeometry(0.6,det);const P=g.attributes.position,bl=!!(fm&&det>1);   // Blender-Grundform (Desktop), Ikosaeder (Handy) [A]
   // t48u R5: unregelmaessiger Fels: Schichten, Bruch, Neigung, Ueberhang [A]
 const sd=k=>hash(Math.round(var_*97)+k,k*13+7),ov=(sd(1)-0.3)*0.5,lean=(sd(2)-0.5)*0.5,nl=3+Math.floor(sd(3)*4),bp=new THREE.Vector3(sd(4)-0.5,sd(5)*0.8,sd(6)-0.5).normalize(),bd=0.18+0.25*sd(7);
 for(let i=0;i<P.count;i++){const v=new THREE.Vector3().fromBufferAttribute(P,i),n=v.clone().normalize();
  let r=1+0.18*Math.sin(n.x*4.1+var_)*Math.cos(n.z*3.3-var_*2)+0.09*Math.sin(n.y*9+n.x*7+var_*3)+0.05*Math.sin(n.z*17+n.y*11);
  if(bl)v.multiplyScalar(1+0.4*(r-1));else v.copy(n).multiplyScalar(0.6*r);
  const L=(v.y+0.6)/1.2*nl,li=Math.floor(L),fr=L-li;   // Schichtung: jede Lage leicht versetzt + Stufenkante
  const off=0.07*(hash(li,var_*5)-0.5);v.x+=off;v.z+=off*0.6;const sh=1-0.10*Math.max(0,fr-0.75)/0.25;v.x*=sh;v.z*=sh;
  v.y=(li+Math.min(1,fr*1.15))/nl*1.2-0.6;
  const dd=v.dot(bp);if(dd>bd)v.addScaledVector(bp,-(dd-bd)*0.9);   // Bruchflaeche
  const k=1+ov*(v.y+0.6);v.x*=k;v.z*=k;v.x+=lean*(v.y+0.6);   // Ueberhang/Neigung
  P.setXYZ(i,v.x,v.y,v.z);}
 const ng=g.toNonIndexed();ng.computeVertexNormals();const N=ng.attributes.normal,Q=ng.attributes.position,col=[];
 const tint=[[1.02,0.97,0.90],[0.96,0.96,0.98],[1.05,0.95,0.84],[0.93,0.95,0.97],[1.0,0.93,0.86],[0.98,0.98,0.95]][Math.floor(sd(8)*6)];
 for(let i=0;i<Q.count;i+=3){const ny=(N.getY(i)+N.getY(i+1)+N.getY(i+2))/3,yy=(Q.getY(i)+Q.getY(i+1)+Q.getY(i+2))/3,xx=Q.getX(i),zz=Q.getZ(i),h=hash(i,var_*7);
  const fl=Math.sin(xx*9+var_)*Math.cos(zz*8-var_)+0.5*Math.sin(yy*13+xx*5);let c;
  const li=Math.floor((yy+0.6)/1.2*nl),st=hash(li,var_*3);const v=0.30+0.16*st+0.05*h;c=[v*tint[0],v*tint[1],v*tint[2]];
  if(ny>0.62&&fl>-0.5)c=[0.88+0.05*h,0.90+0.05*h,0.95];else if(ny>0.25&&fl>0.35)c=[0.27+0.05*h,0.33+0.05*h,0.18];   // Schnee-/Moosflecken
  else if(ny<-0.25)c=c.map(q=>q*0.62);
  for(let k=0;k<3;k++)col.push(...c);}
 ng.setAttribute('color',new THREE.Float32BufferAttribute(col,3));return ng;}
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
let GL=null,KAM=[];   // Fenster mit Licht (unbeleuchtet) und Kaminpositionen fuer Rauch
const DACHF={Hütte:0x4a3424,'FUNKTION:Ressource':0x4f3826,Turmhaus:0x4a4a4e,'FUNKTION:Kaserne':0x45474b,'FUNKTION:Spezial':0x5a3a2c};
const LADEN=[0x3d5a3a,0x6e2f24,0x34506a,0x5a4a32];
function haus(B,h,id){const b=h.b*0.9,t=h.t*0.9,platz=h.typ=='Quartiersplatz',x=h.x,z=h.z,y=h.y,lang=b>=t;
 if(platz){B.box(x-b/2,y-0.3,z-t/2,x+b/2,y+0.12,z+t/2,lin(0x9a948a),id);return;}
 B.flip=!lang;   // P() spiegelt bei b<t die Achsen -> Wicklung umdrehen
 const r=k=>hash(id*1.37+k*0.71,k*3.1+id*0.013);
 const turm=h.typ=='Turmhaus',holz=h.typ=='Hütte'||h.typ=='FUNKTION:Ressource';const wc=WAND[h.typ]||WAND.Standard,wcol=lin(wc[0]).lerp(lin(wc[1]),r(1));
 wcol.offsetHSL((r(9)-0.5)*0.03,(r(10)-0.5)*0.10,(r(11)-0.5)*0.07);   // keine identischen Nachbarn [A]
 const L=lang?b:t,Q=lang?t:b,P=(l,q,yy)=>lang?[x+l,yy,z+q]:[x+q,yy,z+l];
 const bx=(l0,l1,q0,q1,y0,y1,col)=>{const a=P(l0,q0,0),c=P(l1,q1,0);B.box(Math.min(a[0],c[0]),y0,Math.min(a[2],c[2]),Math.max(a[0],c[0]),y1,Math.max(a[2],c[2]),col,id);};
 const wh=Math.max(2.5,turm?h.h*0.85:h.h*(0.52+0.14*r(2))),sock=0.45+0.3*r(12),sn=lin(0xeef2f7);
 bx(-L/2-0.1,L/2+0.1,-Q/2-0.1,Q/2+0.1,y-1.0,y+sock,lin(0x6d6a64).multiplyScalar(0.85+0.25*r(13)));   // Steinsockel
 bx(-L/2,L/2,-Q/2,Q/2,y+sock,y+wh,wcol);
 const fw=lin(0x4e3220).multiplyScalar(0.85+0.3*r(14));
 if(holz){for(let yy=y+sock+0.3;yy<y+wh-0.1;yy+=0.34)bx(-L/2-0.03,L/2+0.03,-Q/2-0.03,Q/2+0.03,yy,yy+0.05,wcol.clone().multiplyScalar(0.62));}   // Blockbohlen-Fugen
 else if(!turm){for(const s of[-1,1]){bx(-L/2-0.02,L/2+0.02,s*Q/2-0.12,s*Q/2+0.12,y+sock,y+sock+0.16,fw);bx(-L/2-0.02,L/2+0.02,s*Q/2-0.12,s*Q/2+0.12,y+wh-0.18,y+wh,fw);}
  for(const sl of[-1,1])for(const sq of[-1,1])bx(sl*L/2-0.14,sl*L/2+0.14,sq*Q/2-0.14,sq*Q/2+0.14,y+sock,y+wh,fw);}
 // Fenster: Rahmen, Glas (warm beleuchtet oder dunkel), Laeden, Schnee auf Sims
 const rah=lin(0xe2d9c4),tur=lin(0x4b2e1c).multiplyScalar(0.8+0.4*r(15)),lad=lin(LADEN[Math.floor(r(16)*4)]),mitL=!turm&&r(17)<0.7;
 const nF=Math.max(1,Math.floor((L-1.5)/2.3)),etagen=Math.max(1,Math.floor((wh-sock)/2.4)),tm=nF%2?0:L/(2*nF);
 const fl=(u,v,w,hh,s,col,d,bau=B)=>{const q=s*Q/2,a=P(u-w/2,q,0),c=P(u+w/2,q+s*d,0);bau.box(Math.min(a[0],c[0]),y+v,Math.min(a[2],c[2]),Math.max(a[0],c[0]),y+v+hh,Math.max(a[2],c[2]),col,id);};
 for(const s of[-1,1])for(let e=0;e<etagen;e++)for(let i=0;i<nF;i++){const u=-L/2+(i+0.5)*L/nF;if(e==0&&s==1&&Math.abs(u-tm)<0.6)continue;const v=sock+0.85+e*2.4;
  fl(u,v,0.95,1.1,s,rah,0.06);const an=r(30+i+e*7+s*3)<0.55;fl(u,v+0.08,0.75,0.94,s,an?lin(0xffc070):lin(0x2a3644),0.08,an?GL:B);
  fl(u,v-0.06,1.05,0.07,s,sn,0.2);if(mitL){fl(u-0.68,v,0.36,1.1,s,lad,0.1);fl(u+0.68,v,0.36,1.1,s,lad,0.1);}}
 fl(tm,sock,1.1,2.0,1,tur,0.08);fl(tm,sock+2.0,1.3,0.12,1,rah,0.1);
 // Vordach ueber der Tuer mit Schnee
 const dachc=lin(DACHF[h.typ]||0x5b3326).lerp(lin(0x3c3a38),r(3)*0.6);fl(tm,sock+2.3,1.9,0.12,1,dachc,0.95);fl(tm,sock+2.42,1.8,0.1,1,sn,0.9);
 // Satteldach in Schindelreihen + Schneehaube mit wechselnder Bedeckung
 const ov=0.45,dh=turm?Math.min(b,t)*0.9:Math.min(b,t)*(0.40+0.28*r(4)),Y=y+wh,l0=-L/2-ov,l1=L/2+ov,cf=0.5+0.4*r(5);
 for(const s of[-1,1]){const qa=s*(Q/2+ov),ys=Y-ov*dh/(Q/2),n=Math.max(4,Math.round(Math.hypot(Q/2+ov,dh)/0.42));
  const yq=q=>Y+dh-(Y+dh-ys)*Math.abs(q)/Math.abs(qa);
  for(let k=0;k<n;k++){const qA=qa*(1-k/n),qB=qa*(1-(k+1)/n),dy=0.05;const c=dachc.clone().multiplyScalar(0.82+0.3*hash(k+id,id*0.3));
   const nl=Math.max(2,Math.round((l1-l0)/1.3));for(let m=0;m<nl;m++){const la=l0+(l1-l0)*m/nl,lb=l0+(l1-l0)*(m+1)/nl,cc=c.clone().multiplyScalar(0.88+0.24*hash(k*7+m+id,m*1.7+s));   // Schindelfelder [A]
    const A=P(la,qA,yq(qA)-dy),Bp=P(lb,qA,yq(qA)-dy),C=P(lb,qB,yq(qB)),D=P(la,qB,yq(qB));if(s<0)B.quad(A,D,C,Bp,cc,id);else B.quad(A,Bp,C,D,cc,id);}}
  {const fa=lin(0x3a2618),ed=0.24;const E1=P(l0,qa,ys-0.06),E2=P(l1,qa,ys-0.06),E3=P(l1,qa,ys-0.06-ed),E4=P(l0,qa,ys-0.06-ed);B.quad(E1,E2,E3,E4,fa,id);B.quad(E1,E4,E3,E2,fa,id);   // Traufbrett
   for(const l of[l0,l1]){const V1=P(l,qa,ys-0.04),V2=P(l,0,Y+dh-0.02),V3=P(l,0,Y+dh-0.02-ed),V4=P(l,qa,ys-0.04-ed);B.quad(V1,V2,V3,V4,fa,id);B.quad(V1,V4,V3,V2,fa,id);}}   // Ortgang
  const nsg=Math.max(3,Math.round((l1-l0)/0.7)),e=0.14,cmK=m=>Math.min(0.97,Math.max(0.3,cf+(Math.sin(m*0.9+id)*0.6+hash(id*2.3+m,s*5.1+m)-0.5)*0.14)),emK=m=>e*(0.75+0.5*hash(m,id+s));
  for(let m=0;m<nsg;m++){const la=l0+0.06+(l1-l0-0.12)*m/nsg,lb=l0+0.06+(l1-l0-0.12)*(m+1)/nsg,qa2=qa*cmK(m),qb2=qa*cmK(m+1),ea=emK(m),eb=emK(m+1);   // Schneekante als stetige Wellenlinie [A]
   const sr=sn.clone().multiplyScalar(0.97+0.04*hash(id,s)),se=sn.clone().multiplyScalar(0.93).lerp(lin(0xc8d4e6),0.25);   // Traufe kuehler, First heller
   const A2=P(la,qa2,yq(qa2)+ea),B2=P(lb,qb2,yq(qb2)+eb),C2=P(lb,0,Y+dh+e),D2=P(la,0,Y+dh+e);if(s<0){B.quad(A2,D2,C2,B2,sr,id);}else{B.quad(A2,B2,C2,D2,sr,id);}
   const A3=P(la,qa2,yq(qa2)),B3=P(lb,qb2,yq(qb2));if(s<0)B.quad(A3,A2,B2,B3,se,id);else B.quad(A3,B3,B2,A2,se,id);}}
 for(const l of[-L/2,L/2]){const a=P(l,-Q/2,Y),c=P(l,Q/2,Y),d=P(l,0,Y+dh);const gc=holz?wcol.clone().multiplyScalar(0.85):wcol;B.tri(a,d,c,gc,id);B.tri(a,c,d,gc,id);}   // Giebel
 // Anbau (Schuppen) an einer Giebelseite, Holzstapel an der Rueckseite
 if(!turm&&r(6)<0.45){const al=1.3+0.6*r(7),ah=Math.min(wh*0.75,2.4),sg=r(8)<0.5?1:-1,l=sg*L/2;
  bx(Math.min(l,l+sg*al),Math.max(l,l+sg*al),-Q*0.32,Q*0.32,y,y+ah,lin(0x6e5038).multiplyScalar(0.85+0.3*r(18)));
  const ra=P(l,-Q*0.38,y+ah+0.55),rb=P(l,Q*0.38,y+ah+0.55),rc=P(l+sg*(al+0.25),Q*0.38,y+ah-0.05),rd=P(l+sg*(al+0.25),-Q*0.38,y+ah-0.05);
  const up=p=>[p[0],p[1]+0.1,p[2]];if(sg>0^lang){B.quad(ra,rb,rc,rd,dachc,id);B.quad(up(ra),up(rb),up(rc),up(rd),sn,id);}else{B.quad(ra,rd,rc,rb,dachc,id);B.quad(up(ra),up(rd),up(rc),up(rb),sn,id);}}
 if(r(19)<0.55){const u=(r(20)-0.5)*L*0.4,wl=1.6+r(21);fl(u,0,wl,1.0,-1,lin(0x8a6440),0.6);fl(u,1.0,wl,0.1,-1,sn,0.6);}
 const ks=r(22)-0.5;if(true){const cl=ks*L*0.5,cq=Q*0.2*(r(23)<0.5?1:-1),[cx,,cz]=P(cl,cq,0);B.box(cx-0.3,Y,cz-0.3,cx+0.3,Y+dh+0.75,cz+0.3,lin(0x6a625a).multiplyScalar(0.85+0.3*r(25)),id);B.box(cx-0.34,Y+dh+0.75,cz-0.34,cx+0.34,Y+dh+0.9,cz+0.34,lin(0x3e3832),id);B.box(cx-0.34,Y+dh+0.9,cz-0.34,cx+0.34,Y+dh+1.04,cz+0.34,sn,id);if(r(24)<0.6)KAM.push([cx,Y+dh+1.1,cz]);}B.flip=false;}
export function objekteNeu(D,H,G,grp){
 const mat=new THREE.MeshLambertMaterial({vertexColors:true});
 const inst=(geo,L,fn,gn,farbe)=>{const m=new THREE.InstancedMesh(geo,mat,L.length),o=new THREE.Object3D(),c=new THREE.Color();L.forEach((e,n)=>{fn(o,e,n);o.updateMatrix();m.setMatrixAt(n,o.matrix);if(farbe){farbe(c,e,n);m.setColorAt(n,c);}});m.castShadow=m.receiveShadow=true;(G[gn]||grp(gn)).add(m);return m;};
 const VAR=4,tf=(o,[x,y,z,h,r])=>{o.position.set(x,y-0.15,z);o.rotation.set((hash(x,z)-0.5)*0.06,r||0,(hash(z,x)-0.5)*0.06);const s=0.85+0.3*hash(z,x+1);o.scale.set(h*s,h,h*s);};
 const fc=(c,b)=>{const t=b[5]??hash(b[0],b[2]);c.setRGB(0.85+0.15*t,0.9+0.1*t,0.85+0.15*(1-t));};
 for(let v=0;v<VAR;v++){inst(fichte(v),D.baeume.filter((b,n)=>(n%5)!=4&&n%VAR==v),tf,'baeume',fc);}
 inst(kiefer(1),D.baeume.filter((b,n)=>(n%5)==4),tf,'baeume',fc);
 const FV=[fels(1),fels(2.3),fels(3.7)];const ff=(o,[x,y,z,h,r])=>{const a=hash(x,z),b=hash(z,x);h=Math.min(h,2.6);o.position.set(x,y-0.22*h,z);o.rotation.set((a-0.5)*0.6,r,(b-0.5)*0.6);o.scale.set(h*(0.8+0.5*a),h*(0.55+0.5*b),h*(0.8+0.5*b));};
 {const lod=window.__lod||1,BV=[1.1,2.6,4.2,5.9,7.3,8.8,10.4,12.1].map((v,n)=>(window.__FM=D.felsmesh,block(v,lod==1?2:1,n))),L=(D.felsbloecke||[]).filter((e,n)=>lod==1||n%2==0);
  const bf=(o,[x,y,z,sx,sy,sz,r,t])=>{o.position.set(x,y,z);o.rotation.set(t*0.5,r+t*0.6,-t*0.35);o.scale.set(sx*(lod==1?1:1.3),sy,sz);};
  const bc=(c,e)=>{const t=hash(e[0]*3,e[2]*3);const u=hash(e[1]*5,e[0]*7);c.setRGB(0.80+0.35*t,0.78+0.30*t*u+0.05,0.74+0.28*(1-t));};
  BV.forEach((g,v)=>inst(g,L.filter((e,n)=>n%8==v),bf,'felsen',bc));window.__felsbloecke=L.length;}
 if(D.gras&&D.gras.length){const lod=window.__lod||1,L=D.gras.filter((e,n)=>lod==1||n%3==0),gm=new THREE.MeshLambertMaterial({vertexColors:true,side:THREE.DoubleSide});
  const m=new THREE.InstancedMesh(buschel(),gm,L.length),o=new THREE.Object3D();L.forEach(([x,y,z,h,r],n)=>{o.position.set(x,y-0.05,z);o.rotation.set(0,r,0);o.scale.set(h*1.4,h,h*1.4);o.updateMatrix();m.setMatrixAt(n,o.matrix)});m.receiveShadow=true;(G.felsen||grp('felsen')).add(m);}
 const alle=[...D.felsen,...D.findlinge,...D.steine,...(D.geroell||[])];FV.forEach((g,v)=>inst(g,alle.filter((e,n)=>n%3==v),ff,'felsen'));
 GL=new Bau();KAM=[];const B=new Bau();D.haeuser.forEach((h,i)=>haus(B,h,i));const hmat=new THREE.MeshLambertMaterial({vertexColors:true});hmat.onBeforeCompile=sh=>{sh.fragmentShader=sh.fragmentShader.replace('#include <emissivemap_fragment>','#include <emissivemap_fragment>\n totalEmissiveRadiance+=vColor.rgb*0.22;');};   // Aufhellung Schattenseite [A]
 const hm=new THREE.Mesh(B.geo(),hmat);hm.castShadow=hm.receiveShadow=true;hm.userData.hausFlaechen=B.f;hm.userData.haeuser=D.haeuser;grp('gebaeude').add(hm);grp('gebaeude').add(zaeune(D,H));
 const gm=new THREE.Mesh(GL.geo(),new THREE.MeshBasicMaterial({vertexColors:true}));gm.material.color.setScalar(0.85);grp('gebaeude').add(gm);   // Fensterlicht [A]
 {const cv=document.createElement('canvas');cv.width=cv.height=64;const g=cv.getContext('2d'),rg=g.createRadialGradient(32,32,0,32,32,32);rg.addColorStop(0,'rgba(255,255,255,0.9)');rg.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=rg;g.fillRect(0,0,64,64);
  const NP=5,pos=new Float32Array(KAM.length*NP*3),pg=new THREE.BufferGeometry();pg.setAttribute('position',new THREE.BufferAttribute(pos,3));
  const pm=new THREE.Points(pg,new THREE.PointsMaterial({map:new THREE.CanvasTexture(cv),size:2.6,transparent:true,opacity:0.32,depthWrite:false,color:0xd9dde2}));pm.frustumCulled=false;
  pm.onBeforeRender=()=>{const t=performance.now()/1000;KAM.forEach(([cx,cy,cz],k)=>{for(let n=0;n<NP;n++){const f=((t*0.25+n/NP+hash(k,1))%1),o=(k*NP+n)*3;pos[o]=cx+f*f*3.5+Math.sin(t+n+k)*0.25;pos[o+1]=cy+f*5.5;pos[o+2]=cz+f*1.2;}});pg.attributes.position.needsUpdate=true;};
  grp('gebaeude').add(pm);}   // Kaminrauch, Wind nach Osten [A]
 return (B.p.length+GL.p.length)/9;}

// t44u r9: Zaeune nur wo rechnerisch frei (keine Nachbarhaeuser, keine Wegzellen, kein Steilhang, kein Wasser) [A]
export function zaeune(D,HN,grpFn){const B=new Bau(),W=new Set(D.wege.map(([x,y])=>y*1e4+x)),HS=D.haeuser;let nS=0,nV=0;
 const frei=(px,pz,self)=>{if(px<1||pz<1||px>D.nx-1||pz>D.ny-1)return false;if(W.has(Math.floor(pz)*1e4+Math.floor(px)))return false;
  for(let o=0;o<HS.length;o++){const h=HS[o];if(h.typ=='Quartiersplatz'&&o!=self){if(Math.abs(px-h.x)<h.b/2+0.8&&Math.abs(pz-h.z)<h.t/2+0.8)return false;continue;}
   const m=o==self?0.4:0.9;if(Math.abs(px-h.x)<h.b*0.45+m+(o==self?0:0)&&Math.abs(pz-h.z)<h.t*0.45+m)return false;}return true;};
 const holz=lin(0x5a3e28);
 HS.forEach((h,id)=>{if(h.typ=='Quartiersplatz'||h.typ=='Turmhaus'||hash(id*3.3,7.7)>0.4)return;const ab=1.8,hb=h.b*0.45+ab,ht=h.t*0.45+ab;
  const ec=[[h.x-hb,h.z-ht],[h.x+hb,h.z-ht],[h.x+hb,h.z+ht],[h.x-hb,h.z+ht]];
  for(let sgi=0;sgi<4;sgi++){if(sgi==2)continue;   // Vorderseite (Tuer) offen
   const [ax,az]=ec[sgi],[bx2,bz]=ec[(sgi+1)%4],len=Math.hypot(bx2-ax,bz-az),n=Math.max(1,Math.round(len/1.8));
   for(let k=0;k<n;k++){nV++;const f0=k/n,f1=(k+1)/n,x0=ax+(bx2-ax)*f0,z0=az+(bz-az)*f0,x1=ax+(bx2-ax)*f1,z1=az+(bz-az)*f1;
    const y0=HN(x0,z0),y1=HN(x1,z1),ym=HN((x0+x1)/2,(z0+z1)/2);
    if(Math.abs(y0-h.y)>1.2||Math.abs(y1-h.y)>1.2||Math.abs(y0-y1)>0.5||Math.abs(ym-(y0+y1)/2)>0.25)continue;
    if(!frei(x0,z0,id)||!frei(x1,z1,id)||!frei((x0+x1)/2,(z0+z1)/2,id))continue;nS++;
    const c=holz.clone().multiplyScalar(0.8+0.4*hash(x0,z0));B.box(x0-0.06,y0-0.2,z0-0.06,x0+0.06,y0+1.0,z0+0.06,c,-1);B.box(x0-0.06,y0+1.0,z0-0.06,x0+0.06,y0+1.08,z0+0.06,lin(0xeef2f7),-1);
    for(const hh of[0.4,0.8]){const dx=x1-x0,dz=z1-z0,L=Math.hypot(dx,dz),nx=-dz/L*0.025,nz=dx/L*0.025;
     const a=[x0+nx,y0+hh,z0+nz],b=[x1+nx,y1+hh,z1+nz],a2=[x0+nx,y0+hh+0.09,z0+nz],b2=[x1+nx,y1+hh+0.09,z1+nz];B.quad(a,b,b2,a2,c,-1);B.quad(a,a2,b2,b,c,-1);}}}});
 const m=new THREE.Mesh(B.geo(),new THREE.MeshLambertMaterial({vertexColors:true}));m.castShadow=m.receiveShadow=true;m.userData.zaun={segmente:nS,geprueft:nV};window.__zaun=m.userData.zaun;return m;}
