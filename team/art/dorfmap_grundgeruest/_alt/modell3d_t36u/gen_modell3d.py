# t36u: sauberes 3D-Gelaende aus c20 + z25. 1 Einheit = 1 m, y oben, x=cx, z=cy.
# Alle Hoehen [A] (raster_c20_z25_zellen.csv). Keine Bildgenerierung.
import csv,json,numpy as np,trimesh
from scipy import ndimage as nd
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from PIL import Image
C20='/workspace/handygame-plan/team/art/karten_konzept/dorfkarte_e1_final_neu/master_v18_p7/KANDIDAT_NICHT_FREIGEGEBEN_master_v18_p7_c20.png'
NX,NY=336,303; SOCKEL=-14.0                      # Sockelunterkante [A]
TIEFE={'SEE':1.5,'WASSER_FARBE':1.0,'BACH_NORD':0.5,'BACH_SUED':0.5}  # [A]
H=np.zeros((NY,NX));W=np.zeros((NY,NX),bool);WA=np.zeros((NY,NX),bool);TF=np.zeros((NY,NX))
for r in csv.DictReader(open('../raster_c20_z25_zellen.csv')):
    x,y=int(r['cx']),int(r['cy']);H[y,x]=float(r['hoehe_m']);W[y,x]=r['ebene']=='WAND'
    if r['wasser_eis']=='1': WA[y,x]=1;TF[y,x]=TIEFE.get(r['fluss_id'],0.8)
# 1) Wandzellen: harmonische Fuellung zwischen freien Nachbarn -> steile, glatte Felsrampe (keine Saeulen)
# freie Nachbarzellen mit Sprung >1 m (Stufe ohne Wand im Raster) werden mitgefuellt -> Abweichung [F]
J=np.zeros_like(W)
for ax in (0,1):
    d=np.abs(np.diff(H,axis=ax))>1.0
    m=d&~np.take(W,range(H.shape[ax]-1),axis=ax)&~np.take(W,range(1,H.shape[ax]),axis=ax)
    if ax==0: J[:-1]|=m;J[1:]|=m
    else: J[:,:-1]|=m;J[:,1:]|=m
J=nd.binary_dilation(J,iterations=1)&~W;np.save('/tmp/m3_J.npy',J);print('Sprungzellen ohne Wand',int(J.sum()))
W0=W.copy();W=W|J
idx=-np.ones((NY,NX),int);ys,xs=np.nonzero(W);idx[ys,xs]=np.arange(len(ys))
A=lil_matrix((len(ys),len(ys)));b=np.zeros(len(ys))
for i,(y,x) in enumerate(zip(ys,xs)):
    n=0
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<NY and 0<=xx<NX:
            n+=1
            if W[yy,xx]: A[i,idx[yy,xx]]=-1
            else: b[i]+=H[yy,xx]
    A[i,i]=n
H[ys,xs]=spsolve(A.tocsr(),b);W=W0
# 2) Treppen glaetten: Gauss nur innerhalb freier Flaeche (Wand bleibt scharf), Plateaus bleiben flach
F=~W; g=nd.gaussian_filter(np.where(F,H,0),1.5); w=nd.gaussian_filter(F.astype(float),1.5)
Hs=np.where(F,g/np.maximum(w,1e-6),H)
# 3) Wasser: Flussbett tiefer, zur Mitte hin tiefer; Oberflaeche 0,1 m unter Ufer [A]
dist=nd.distance_transform_edt(WA)
BETT=Hs-np.where(WA,TF*np.minimum(1,dist/3)+0.1,0)
OBER=np.where(WA,Hs-0.1,np.nan)
# Eckpunkte (NY+1)x(NX+1): Mittel der angrenzenden Zellen
def ecken(Z,m=None):
    P=np.pad(Z,1,mode='edge');M=np.pad(np.ones_like(Z) if m is None else m.astype(float),1)
    s=sum(P[a:a+NY+1,c:c+NX+1]*M[a:a+NY+1,c:c+NX+1] for a in(0,1) for c in(0,1))
    n=sum(M[a:a+NY+1,c:c+NX+1] for a in(0,1) for c in(0,1));return s/np.maximum(n,1e-9)
E=ecken(BETT)
Eo=ecken(np.nan_to_num(OBER),WA)
rand=[(0,x) for x in range(NX+1)]+[(y,NX) for y in range(1,NY+1)]+[(NY,x) for x in range(NX-1,-1,-1)]+[(y,0) for y in range(NY-1,0,-1)]
Image.open(C20).convert('RGB').crop((0,0,NX*25,NY*25)).resize((NX*8,NY*8),Image.LANCZOS).save('textur_c20_8px.jpg',quality=90)
# ---------------- t36u Teil 2: Mesh je Zelle mit Eigenschaften ----------------
import pygltflib as G, struct, collections
R={(int(r['cx']),int(r['cy'])):r for r in csv.DictReader(open('../raster_c20_z25_zellen.csv'))}
FELDER=list(next(iter(R.values())).keys())
zid=lambda x,y:y*NX+x                                # Zell-ID = cy*336+cx
HM=(E[:-1,:-1]+E[1:,:-1]+E[:-1,1:]+E[1:,1:])/4       # Modellhoehe je Zelle (Mittel der Ecken)
# Sidecar: alle Rasterfelder unveraendert + Modellfelder
with open('zellen_eigenschaften.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['zell_id']+FELDER+['modell_hoehe_m','modell_abw_m','modell_gruppe'])
    for y in range(NY):
        for x in range(NX):
            r=R[(x,y)];w.writerow([zid(x,y)]+[r[k] for k in FELDER]+[f'{HM[y,x]:.3f}',f'{HM[y,x]-float(r["hoehe_m"]):.3f}',r['untergrund']])
# Geometrie: 4 eigene Ecken je Zelle -> Zell-ID und Kachel-UV exakt pro Flaeche
def zellquad(y,x,Z):
    p=np.array([[x,Z[y,x],y],[x+1,Z[y,x+1],y],[x+1,Z[y+1,x+1],y+1],[x,Z[y+1,x],y+1]],np.float32)
    flip=abs(Z[y,x]-Z[y+1,x+1])>abs(Z[y,x+1]-Z[y+1,x])
    return p,([0,3,1,1,3,2] if flip else [0,3,2,0,2,1])
grp=collections.defaultdict(lambda:{'P':[],'I':[],'ID':[]})
for y in range(NY):
    for x in range(NX):
        g=grp[R[(x,y)]['untergrund']];p,t=zellquad(y,x,E);o=len(g['P'])*4
        g['P'].append(p);g['I']+= [o+i for i in t];g['ID'].append(zid(x,y))
# Wasseroberflaeche als eigene Gruppe (gleiche Zell-IDs der Wasserzellen)
for y,x in zip(*np.nonzero(WA)):
    g=grp['WASSER_OBERFLAECHE'];p,t=zellquad(y,x,Eo);o=len(g['P'])*4
    g['P'].append(p);g['I']+=[o+i for i in t];g['ID'].append(zid(x,y))
# Sockel (ID -1)
g=grp['SOCKEL'];P=[];I=[]
for i in range(len(rand)):
    j=(i+1)%len(rand);(y0,x0),(y1,x1)=rand[i],rand[j]
    q=np.array([[x0,E[y0,x0],y0],[x1,E[y1,x1],y1],[x1,SOCKEL,y1],[x0,SOCKEL,y0]],np.float32);o=len(g['P'])*4
    g['P'].append(q);g['I']+=[o,o+1,o+2,o,o+2,o+3];g['ID'].append(-1)
for i in range(len(rand)):   # Boden als Faecher, gleiche Randpunkte wie Sockel -> keine T-Stellen
    j=(i+1)%len(rand);(y0,x0),(y1,x1)=rand[i],rand[j]
    q=np.array([[x0,SOCKEL,y0],[x1,SOCKEL,y1],[NX/2,SOCKEL,NY/2],[NX/2,SOCKEL,NY/2]],np.float32);o=len(g['P'])*4
    g['P'].append(q);g['I']+=[o,o+2,o+1];g['ID'].append(-1)
# glTF bauen
blob=bytearray();gl=G.GLTF2(asset=G.Asset(version='2.0',generator='gen_modell3d.py t36u'),scene=0,scenes=[G.Scene(nodes=[])],
 extras={'einheit':'1 = 1 m','achsen':'x=cx, y=oben, z=cy','zell_id':'cy*336+cx (Sockel -1)','sidecar':'zellen_eigenschaften.csv','felder':FELDER,
        'TEXCOORD_0':'c20-Vorschau (ganze Karte)','TEXCOORD_1':'Kachel-UV 0..1 je Zelle fuer Skins','_ZELL_ID':'Vertex-Attribut float'})
def acc(arr,typ,ctype,target=None,mm=False):
    global blob
    while len(blob)%4: blob+=b'\0'
    b=arr.tobytes();bv=G.BufferView(buffer=0,byteOffset=len(blob),byteLength=len(b),target=target);blob+=b
    gl.bufferViews.append(bv);a=G.Accessor(bufferView=len(gl.bufferViews)-1,componentType=ctype,count=len(arr),type=typ)
    if mm: a.min=arr.min(0).tolist();a.max=arr.max(0).tolist()
    gl.accessors.append(a);return len(gl.accessors)-1
img_c20=open('textur_c20_8px.jpg','rb').read()
while len(blob)%4: blob+=b'\0'
gl.bufferViews.append(G.BufferView(buffer=0,byteOffset=len(blob),byteLength=len(img_c20)));blob+=img_c20
gl.images=[G.Image(bufferView=0,mimeType='image/jpeg')];gl.samplers=[G.Sampler()];gl.textures=[G.Texture(source=0,sampler=0)]
MATS={}
def material(n):
    if n not in MATS:
        if n=='WASSER_OBERFLAECHE': m=G.Material(name='Wasser',alphaMode='BLEND',pbrMetallicRoughness=G.PbrMetallicRoughness(baseColorFactor=[0.25,0.5,0.7,0.6],metallicFactor=0,roughnessFactor=0.1))
        elif n=='SOCKEL': m=G.Material(name='Sockel',pbrMetallicRoughness=G.PbrMetallicRoughness(baseColorFactor=[0.36,0.31,0.29,1],metallicFactor=0,roughnessFactor=1))
        else: m=G.Material(name=('Wand_' if n.startswith('KLIPPE') else 'Gelaende_')+n,pbrMetallicRoughness=G.PbrMetallicRoughness(baseColorTexture=G.TextureInfo(index=0,texCoord=0),metallicFactor=0,roughnessFactor=0.9))
        gl.materials.append(m);MATS[n]=len(gl.materials)-1
    return MATS[n]
STAT={}
for n,g in grp.items():
    P=np.vstack(g['P']).astype(np.float32);I=np.array(g['I'],np.uint32);ID=np.repeat(np.array(g['ID'],np.float32),4)
    tm=trimesh.Trimesh(P,I.reshape(-1,3),process=False);N=tm.vertex_normals.astype(np.float32)
    # glatte Normalen: ueber gemeinsame Positionen mitteln
    key=np.round(P,3);_,inv=np.unique(key,axis=0,return_inverse=True);inv=inv.ravel()
    acc_n=np.zeros((inv.max()+1,3));np.add.at(acc_n,inv,N);N=acc_n[inv];N=(N/np.maximum(np.linalg.norm(N,axis=1,keepdims=True),1e-9)).astype(np.float32)
    UV0=np.c_[P[:,0]/NX,P[:,2]/NY].astype(np.float32)
    UV1=np.tile(np.array([[0,0],[1,0],[1,1],[0,1]],np.float32),(len(g['P']),1))
    at=G.Attributes(POSITION=acc(P,'VEC3',5126,34962,True),NORMAL=acc(N,'VEC3',5126,34962),TEXCOORD_0=acc(UV0,'VEC2',5126,34962),TEXCOORD_1=acc(UV1,'VEC2',5126,34962))
    at._ZELL_ID=acc(ID,'SCALAR',5126,34962)
    prim=G.Primitive(attributes=at,indices=acc(I,'SCALAR',5125,34963),material=material(n))
    gl.meshes.append(G.Mesh(name=n,primitives=[prim],extras={'untergrund':n,'zellen':int(len(g['ID']))}))
    gl.nodes.append(G.Node(name=n,mesh=len(gl.meshes)-1));gl.scenes[0].nodes.append(len(gl.nodes)-1);STAT[n]=(len(g['ID']),len(I)//3)
gl.buffers=[G.Buffer(byteLength=len(blob))];gl.set_binary_blob(bytes(blob));gl.save_binary('dorfmap_c20_z25.glb')
# OBJ zusaetzlich (Gruppen je Untergrund, Kachel-UV nicht enthalten)
with open('dorfmap_c20_z25.obj','w') as f:
    f.write('# t36u Dorfmap, 1=1m, y oben. Gruppen je Untergrund. Zell-ID je Flaeche in Kommentar "# zid"\nmtllib dorfmap_c20_z25.mtl\n');o=1
    for n,g in grp.items():
        f.write(f'g {n}\nusemtl {"Wasser" if n=="WASSER_OBERFLAECHE" else "Sockel" if n=="SOCKEL" else "c20"}\n')
        for q,i_ in zip(g['P'],g['ID']):
            for p in q: f.write(f'v {p[0]:.0f} {p[1]:.3f} {p[2]:.0f}\nvt {p[0]/NX:.5f} {1-p[2]/NY:.5f}\n')
            f.write(f'# zid {i_}\n')
        I=np.array(g['I']).reshape(-1,3)+o
        for t in I: f.write(f'f {t[0]}/{t[0]} {t[1]}/{t[1]} {t[2]}/{t[2]}\n')
        o+=len(g['P'])*4
open('dorfmap_c20_z25.mtl','w').write('newmtl c20\nmap_Kd textur_c20_8px.jpg\nnewmtl Wasser\nKd 0.25 0.5 0.7\nd 0.6\nnewmtl Sockel\nKd 0.36 0.31 0.29\n')
# ---- automatische Pruefung
allP=np.vstack([np.vstack(g['P']) for n,g in grp.items() if n!='WASSER_OBERFLAECHE']);allI=[];o=0
for n,g in grp.items():
    if n=='WASSER_OBERFLAECHE': continue
    allI.append(np.array(g['I'])+o);o+=len(g['P'])*4
voll=trimesh.Trimesh(allP,np.concatenate(allI).reshape(-1,3),process=True)
top=voll.face_normals;cent=voll.triangles_center
oben=cent[:,1]>SOCKEL+0.01
Pd=np.pad(E,1,mode='edge');nb=np.stack([Pd[1+a:NY+2+a,1+b:NX+2+b] for a in(-1,0,1) for b in(-1,0,1) if a or b])
spitz=((E-nb.max(0))>0.3)|((nb.min(0)-E)>0.3)
frei_ecken=ecken(F.astype(float))>0.999;lap=np.abs(E-nd.uniform_filter(E,3,mode='nearest'))
P_={'gruppen':{k:{'zellen':v[0],'dreiecke':v[1]} for k,v in STAT.items()},'dreiecke_gesamt':sum(v[1] for v in STAT.values()),
 'geschlossen_wasserdicht_ohne_wasser':bool(voll.is_watertight),'volumen_m3':round(float(voll.volume)),'euler':int(voll.euler_number),
 'flips_oberflaeche':int(((top[:,1]<=0)&oben&(np.abs(top[:,1])>1e-6)&(cent[:,0]>0.01)&(cent[:,0]<NX-0.01)&(cent[:,2]>0.01)&(cent[:,2]<NY-0.01)).sum()),
 'entartete_dreiecke':int((voll.area_faces<1e-9).sum()),
 'max_steigung_freiflaeche_grad':round(float(np.degrees(np.arctan(np.abs(np.gradient(E)).max(0)[frei_ecken].max()))),1),
 'spitzen_eckpunkt_0.3m_ueber_oder_unter_allen_8_nachbarn':int(spitz.sum()),'hoehe_min_max_m':[round(float(E.min()),2),round(float(E.max()),2)]}
json.dump(P_,open('pruefung_mesh.json','w'),indent=1,ensure_ascii=False);print(json.dumps(P_,ensure_ascii=False))
np.save('/tmp/m3_E.npy',E);np.save('/tmp/m3_HM.npy',HM);np.save('/tmp/m3_Eo.npy',Eo)
