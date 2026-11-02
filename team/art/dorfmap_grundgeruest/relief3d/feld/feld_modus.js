// Feld-Modus (t82u): Ausschnitt Feld + Rand aus der unveraenderten Hauptszene. Geometrie = Hauptviewer-Code, nur Dreiecke/Instanzen ausserhalb entfernt.
export async function feldModus(o){
 const {THREE,sc,NEU,cam,oc,HN,DN,ebSicht}=o,F=window.FELD,R=F.rand,X0=F.x0-R,X1=F.x1+R,Z0=F.z0-R,Z1=F.z1+R;
 const drin=(x,z)=>x>=X0&&x<=X1&&z>=Z0&&z<=Z1,imFeld=(x,z)=>x>=F.x0&&x<=F.x1&&z>=F.z0&&z<=F.z1;
 NEU.updateMatrixWorld(true);const v=new THREE.Vector3(),m4=new THREE.Matrix4(),st={dreiecke:0,instanzen:0};const rand=[],seen=new Set();
 const alle=[];NEU.traverse(m=>{if(m.isMesh&&m.geometry&&m.geometry.attributes.position)alle.push(m);});alle.forEach(m=>{let g=m.geometry;if(!m.isInstancedMesh){if(seen.has(g))m.geometry=g=g.clone();seen.add(g);}const P=g.attributes.position;
  if(m.isInstancedMesh){let k=0;for(let i=0;i<m.count;i++){m.getMatrixAt(i,m4);v.setFromMatrixPosition(m4).applyMatrix4(m.matrixWorld);if(drin(v.x,v.z)){if(k!=i){m.setMatrixAt(k,m4);if(m.instanceColor)m.instanceColor.setXYZ(k,m.instanceColor.getX(i),m.instanceColor.getY(i),m.instanceColor.getZ(i));}k++;}}
   m.count=k;m.instanceMatrix.needsUpdate=true;if(m.instanceColor)m.instanceColor.needsUpdate=true;m.computeBoundingSphere&&m.computeBoundingSphere();m.frustumCulled=false;st.instanzen+=k;return;}
  const I=g.index?g.index.array:null,n=I?I.length:P.count,mw=m.matrixWorld,ix=[],hf=m.userData.hausFlaechen,hf2=[],ri=[];const c=new THREE.Vector3();
  const gr=g.groups&&g.groups.length>1?g.groups:null;
  for(let t=0;t+2<n;t+=3){const a=I?I[t]:t,b=I?I[t+1]:t+1,cc=I?I[t+2]:t+2;c.set(0,0,0);for(const q of [a,b,cc]){v.fromBufferAttribute(P,q);c.add(v);}c.multiplyScalar(1/3).applyMatrix4(mw);
   const hz=hf&&m.userData.haeuser?m.userData.haeuser[hf[t/3]]:null;if(hz?drin(hz.x,hz.z):drin(c.x,c.z)){ix.push(a,b,cc);if(hf)hf2.push(hf[t/3]);if(m.userData.boden&&!imFeld(c.x,c.z))ri.push(a,b,cc);}}
  if(gr){// Gruppen (Mehrfachmaterial): je Gruppe getrennt filtern
   const nix=[],ng=[];for(const q of gr){const s=nix.length;for(let t=q.start;t<q.start+q.count&&t+2<n;t+=3){const a=I?I[t]:t,b=I?I[t+1]:t+1,cc=I?I[t+2]:t+2;c.set(0,0,0);for(const w of [a,b,cc]){v.fromBufferAttribute(P,w);c.add(v);}c.multiplyScalar(1/3).applyMatrix4(mw);if(drin(c.x,c.z))nix.push(a,b,cc);}ng.push([s,nix.length-s,q.materialIndex]);}
   g.setIndex(nix);g.clearGroups();for(const [s,k,mi] of ng)g.addGroup(s,k,mi);st.dreiecke+=nix.length/3;}
  else{g.setIndex(ix);g.setDrawRange(0,Infinity);st.dreiecke+=ix.length/3;}
  if(hf)m.userData.hausFlaechen=hf2;g.computeBoundingSphere();g.computeBoundingBox();
  if(ri.length){const rg=new THREE.BufferGeometry();rg.setAttribute('position',P);rg.setIndex(ri);const rm=new THREE.Mesh(rg,new THREE.MeshBasicMaterial({color:0x000000,transparent:true,opacity:0.42,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2}));rm.matrixAutoUpdate=false;rm.matrix.copy(mw);rm.renderOrder=5;rand.push(rm);}});
 // ferne Berge/Hintergrund (ausserhalb NEU) bleiben; Rand-Abdunklung + gelber Feldumriss
 const RG=new THREE.Group();RG.name='feld_rand';rand.forEach(r=>RG.add(r));sc.add(RG);
 const pts=[],H=(x,z)=>HN(x,z)+0.35,seg=(xa,za,xb,zb)=>{const L=Math.hypot(xb-xa,zb-za),N=Math.ceil(L/0.25);for(let i=0;i<=N;i++){const x=xa+(xb-xa)*i/N,z=za+(zb-za)*i/N;pts.push(new THREE.Vector3(x,H(x,z),z));}};
 seg(F.x0,F.z0,F.x1,F.z0);seg(F.x1,F.z0,F.x1,F.z1);seg(F.x1,F.z1,F.x0,F.z1);seg(F.x0,F.z1,F.x0,F.z0);
 const UM=new THREE.Group();UM.name='feld_umriss';const lm=new THREE.LineBasicMaterial({color:0xffe000,depthTest:false,transparent:true});
 UM.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),lm));
 // Band (breiter als 1-px-Linie): Streifen 0,35 m, immer sichtbar
 {const q=[];for(let i=0;i+1<pts.length;i++){const a=pts[i],b=pts[i+1];q.push(a.x,a.y,a.z,b.x,b.y,b.z,b.x,b.y+0.5,b.z,a.x,a.y,a.z,b.x,b.y+0.5,b.z,a.x,a.y+0.5,a.z);}
  const bg=new THREE.BufferGeometry();bg.setAttribute('position',new THREE.Float32BufferAttribute(q,3));UM.add(new THREE.Mesh(bg,new THREE.MeshBasicMaterial({color:0xffe000,side:THREE.DoubleSide,depthTest:false,transparent:true,opacity:0.9})));}
 for(const [x,z] of [[F.x0,F.z0],[F.x1,F.z0],[F.x1,F.z1],[F.x0,F.z1]]){const h=HN(x,z),p=new THREE.Mesh(new THREE.CylinderGeometry(0.25,0.25,6,8),new THREE.MeshBasicMaterial({color:0xffe000}));p.position.set(x,h+3,z);UM.add(p);}
 UM.traverse(q=>q.renderOrder=10);sc.add(UM);
 // Kamera: schraeg von Sueden (+z) ueber dem Feld
 const cx=(F.x0+F.x1)/2,cz=(F.z0+F.z1)/2,hm=HN(cx,cz),S=Math.max(F.x1-F.x0,F.z1-F.z0);
 const start=()=>{const k=Math.max(1,1.2*innerHeight/innerWidth);cam.position.set(cx,hm+S*1.25*k,cz+S*1.45*k);oc.target.set(cx,hm,cz);oc.update();};start();
 oc.minDistance=3;oc.maxDistance=400;oc.touches={ONE:THREE.TOUCH.ROTATE,TWO:THREE.TOUCH.DOLLY_PAN};
 // Clay-Umschalter (wie ?clay=1: Gelaende grau, andere Ebenen aus)
 const CZ=window.__clayZ||{},CL=new THREE.MeshLambertMaterial({color:0x9c9c9c,side:THREE.DoubleSide}),orig=new Map();for(const k of ['m','fwMesh','ovMesh'])if(CZ[k])orig.set(CZ[k],CZ[k].material);
 let clay=!!window.__clay;const ebene=(n,an)=>{document.querySelectorAll('[data-l]').forEach(c=>{if(c.dataset.l==n)c.checked=an;});};
 const setClay=an=>{clay=an;for(const [mm,mat] of orig)mm.material=an?CL:mat;for(const e of ['baeume','felsen','gebaeude','wasser','wege'])ebene(e,!an&&(e!='wege'||wegeAn));ebSicht();RG.visible=true;
  document.getElementById('bclay').textContent=an?'Textur':'Clay';};
 let wegeAn=true;const hatWege=NEU.children.some(g=>g.userData.ebene=='wege');
 window.__feldUI={setClay,start,umriss:()=>{UM.visible=!UM.visible;return UM.visible;},wege:()=>{wegeAn=!wegeAn;if(!clay){ebene('wege',wegeAn);ebSicht();}return wegeAn;},hatWege,clay:()=>clay};
 window.__feld={...st,feld:F.name,box:[X0,Z0,X1,Z1]};
}
