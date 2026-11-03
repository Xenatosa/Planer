# O18l-C (t112u): Vorschlag Wegverlaeufe. Jedes Rampenende und jede abgetrennte Dorfweg-Insel wird per Kostenweg (Neigung begrenzt, Wand/Wasser gesperrt bzw. Bruecke teuer) an das Netz angeschlossen.
# Overlay bleibt unveraendert; Ausgabe wegvorschlag.json + Bilder je Feld (rot alt, gruen neu). python3 wegvorschlag.py ../relief3d/relief_daten.json.gz
import json,gzip,sys,base64,numpy as np,scipy.ndimage as nd
from skimage.graph import MCP_Geometric
D=json.load(gzip.open(sys.argv[1]));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(GY,GX).astype(float);WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(GY,GX)
H=nd.map_coordinates(G,np.mgrid[0:NY,0:NX]*RS+RS/2,order=1);LAND=nd.map_coordinates((WV<=-900)*1.0,np.mgrid[0:NY,0:NX]*RS+RS/2,order=0)>0.5
gy,gx=np.gradient(H);S=np.hypot(gx,gy);SM=nd.maximum_filter(S,3)
K=np.where(SM<=0.25,1+4*SM,np.where(SM<=0.45,30.0+200*(SM-0.25),1e6));K[~LAND]=60.0   # Wasser = Bruecke noetig (teuer)
K[0,:]=K[-1,:]=K[:,0]=K[:,-1]=np.minimum(K[0,0],K[0,0])  # Rand normal
W=np.zeros((NY,NX),np.int32)   # 0 kein Weg, sonst Netz-ID
for x,z in D['wege']:W[z,x]=1
WA=np.frombuffer(base64.b64decode(D['WEGA']),np.uint8).reshape(GY,GX)[:-1:RS,:-1:RS]>20;W[WA]=1
for b in D['bruecken']:W[int(b[2]),int(b[0])]=1
def samp(r):
    r=np.asarray(r,float);L=np.r_[0,np.cumsum(np.hypot(*np.diff(r,axis=0).T))];t=np.arange(0,L[-1]+1e-6,0.5);return np.stack([np.interp(t,L,r[:,0]),np.interp(t,L,r[:,1])],1)
R=[samp(r) for r in D['rampenwege']];RM=np.zeros((NY,NX),bool)
for p in R:RM[np.clip(p[:,1].astype(int),0,NY-1),np.clip(p[:,0].astype(int),0,NX-1)]=True
NETZ=(W>0)|RM
def feld(x,z):return 'ABCDEFGH'[int(np.clip(x//42,0,7))]+str(int(np.clip(z//43,0,6))+1)
neu=[];done=NETZ.copy()
def verbinde(start_cells,ziel,name,KK=None):
    m=MCP_Geometric(K if KK is None else KK);c,_=m.find_costs(start_cells);zz,xx=np.nonzero(ziel)
    if not len(zz):return None
    j=np.argmin(c[zz,xx]);end=(zz[j],xx[j]);
    if not np.isfinite(c[end]) or c[end]>=1e6:return {'name':name,'status':'kein Weg ohne Wand'}
    tr=np.array(m.traceback(end));pts=[[int(b)+.5,int(a)+.5] for a,b in tr]
    h=H[tr[:,0],tr[:,1]];L=len(tr);steig=float(np.abs(np.diff(nd.gaussian_filter1d(h,3))).max()) if L>3 else 0
    return {'name':name,'punkte':pts[::2]+[pts[-1]],'laenge_m':L,'max_steigung':round(steig,3),'wasser_zellen':int((~LAND[tr[:,0],tr[:,1]]).sum()),'max_neigung_gelaende':round(float(SM[tr[:,0],tr[:,1]].max()),2),'felder':sorted({feld(*p) for p in pts})}
# 1) Rampen-Enden: Anschluss an Netz ausser eigener Rampe (oder Kartenrand)
for i,p in enumerate(R):
    own=np.zeros_like(RM);own[np.clip(p[:,1].astype(int),0,NY-1),np.clip(p[:,0].astype(int),0,NX-1)]=True
    ziel=nd.binary_erosion(NETZ&~nd.binary_dilation(own,iterations=1),iterations=0) if False else (NETZ&~nd.binary_dilation(own,iterations=2))
    for nm,k in (('anfang',0),('ende',-1)):
        x,z=p[k];st=[(int(min(z,NY-1)),int(min(x,NX-1)))];verschoben=None
        if K[st[0]]>=1e6:   # Ende liegt in Wand: entlang der Rampe zurueck zum ersten freien Punkt (max 12 m)
            q=p if k==0 else p[::-1]
            for a in q[:25]:
                if K[int(min(a[1],NY-1)),int(min(a[0],NX-1))]<1e6:st=[(int(a[1]),int(a[0]))];verschoben=[round(float(a[0]),1),round(float(a[1]),1)];break
        KO=K.copy();KO[own]=np.minimum(KO[own],2.0);v=verbinde(st,ziel,f'rampe_{i}_{nm}',KO)
        if v and v.get('status'):
            RA=np.zeros_like(ziel);RA[0,:]=RA[-1,:]=RA[:,0]=RA[:,-1]=True;v=verbinde(st,RA&(K<1e6),f'rampe_{i}_{nm}',KO);v and v.update(anschluss='Kartenrand (Plateau ohne Netz)')
        if v and verschoben:v['ende_verschieben_auf']=verschoben
        if v:v.update(von=[round(float(x),1),round(float(z),1)]);neu.append(v)
# 2) Dorfweg-Inseln an Hauptnetz
lab,n=nd.label(W>0,np.ones((3,3)));gr=np.bincount(lab.ravel());gr[0]=0;hp=gr.argmax()
for k in range(1,n+1):
    if k==hp:continue
    zz,xx=np.nonzero(lab==k);v=verbinde(list(zip(zz,xx)),lab==hp,f'insel_{feld(xx.mean(),zz.mean())}_{int(xx.mean())}_{int(zz.mean())}')
    if v:v.update(von=[int(xx.mean()),int(zz.mean())]);neu.append(v)
json.dump({'regeln':'Anschluss jedes Endes an Netz; Gelaende-Neigung <=0.25 normal, 0.25-0.45 teuer (Serpentine/Treppe), >0.45 gesperrt (Wand); Wasser = Bruecke','verbindungen':neu},open('wegvorschlag.json','w'),indent=1)
for v in neu:print(v['name'],v.get('status',''),v.get('laenge_m'),v.get('max_steigung'),v.get('wasser_zellen'),v.get('felder'))
# Bilder je Feld: Hoehe grau, alt rot, neu gruen
from PIL import Image
for fx in range(8):
    for fz in range(7):
        x0,x1,z0,z1=fx*42,min(fx*42+42,NX),fz*43,min(fz*43+43,NY)
        if x0>=NX or z0>=NY:continue
        hs=H[z0:z1,x0:x1];g=np.clip((hs+20)/36*200+40,0,255);sh=np.clip(128+(np.gradient(hs,axis=1)-np.gradient(hs,axis=0))*60,0,255);img=np.stack([g*0.6+sh*0.4]*3,-1)
        img[~LAND[z0:z1,x0:x1]]=[70,110,200];img[SM[z0:z1,x0:x1]>0.45]*=0.55
        img[NETZ[z0:z1,x0:x1]]=[220,40,40];hit=False
        for v in neu:
            for px,pz in v.get('punkte',[]):
                if x0<=px<x1 and z0<=pz<z1:img[int(pz)-z0,int(px)-x0]=[40,220,60];hit=True
        if hit or NETZ[z0:z1,x0:x1].any():Image.fromarray(img.astype(np.uint8)).resize(((x1-x0)*12,(z1-z0)*12),Image.NEAREST).save(f'feld_{"ABCDEFGH"[fx]}{fz+1}.png')
