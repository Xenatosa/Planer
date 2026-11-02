# O18: geschlossene Senken + Spitzen im Feinband FW (Endstand), Grob-GB ausserhalb als Rand. Rekonstruktions-Fuellung.
import json,gzip,base64,numpy as np,scipy.ndimage as nd,os,sys
from skimage.morphology import reconstruction
src=sys.argv[1];d=json.load(gzip.open(src));RS=d['rs'];NX,NY=d['nx'],d['ny'];GX,GY=NX*RS+1,NY*RS+1
FW=d['FW'];FS=FW['fs'];FX,FY=NX*FS+1,NY*FS+1
vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);h=np.frombuffer(base64.b64decode(FW['h']),np.float32)
GB=np.frombuffer(base64.b64decode(d['GB']),np.float32).reshape(GY,GX).astype(float);WV=np.frombuffer(base64.b64decode(d['WV']),np.float32).reshape(GY,GX)
fy,fx=np.mgrid[0:FY,0:FX].astype(float)
F=nd.map_coordinates(GB,[fy/FS*RS,fx/FS*RS],order=1);F.ravel()[vid]=h
nass=nd.map_coordinates((WV>-900).astype(float),[fy/FS*RS,fx/FS*RS],order=0)>0.5
inb=np.zeros(FX*FY,bool);inb[vid]=True;inb=inb.reshape(FY,FX)
seed=F.copy();seed[1:-1,1:-1]=F.max();seed[nass]=F[nass]
T=reconstruction(seed,F,method='erosion')-F
S=F-reconstruction(np.where(nass,F,F-50).clip(F.min()),F) if False else F-nd.grey_opening(F,size=(FS+1,FS+1))
def komp(M,V):
    L,n=nd.label(M);r=[]
    for i,sl in enumerate(nd.find_objects(L),1):
        m=L[sl]==i;j,k=np.argwhere(m).mean(0)+[sl[0].start,sl[1].start];x,y=k/FS,j/FS
        r.append(dict(x=round(x,1),y=round(y,1),feld=f"{'ABCDEFGH'[min(7,int(x//42))]}{min(7,int(y//43))+1}",wert=round(float(V[sl][m].max()),2),ecken=int(m.sum())))
    return sorted(r,key=lambda c:-c['wert'])
sen=komp((T>0.3)&inb,T);spi=komp((S>0.8)&inb,S)
out=dict(fs=FS,senken_gt0_3=len(sen),senken_gt1=sum(c['wert']>1 for c in sen),spitzen_gt0_8=len(spi),spitzen_gt1_5=sum(c['wert']>1.5 for c in spi),senken=sen,spitzen=spi)
if len(sys.argv)>2:json.dump(out,open(sys.argv[2],'w'),indent=1)
print({k:v for k,v in out.items() if k not in('senken','spitzen')})
import collections
print('senken je feld',collections.Counter(c['feld'] for c in sen).most_common(12))
print('spitzen je feld',collections.Counter(c['feld'] for c in spi).most_common(12))
for c in sen[:12]:print('S',c)
for c in spi[:8]:print('P',c)
