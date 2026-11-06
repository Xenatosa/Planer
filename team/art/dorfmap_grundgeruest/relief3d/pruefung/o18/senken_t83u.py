# O18: geschlossene Senken (Mulden nach innen) im Anzeige-Gelaende GB: Fuellung per morphologischer Rekonstruktion,
# Tiefe = gefuellt - GB. Wandfuss-Innenecken entwaessern -> zaehlen NICHT (Bereinigung ggue. regeln_t83u closing-Mass).
import json,gzip,base64,numpy as np,scipy.ndimage as nd,os,sys
from skimage.morphology import reconstruction
H=os.path.dirname(os.path.abspath(__file__))
src=sys.argv[1] if len(sys.argv)>1 else os.path.join(H,'../../relief_daten.json.gz')
d=json.load(gzip.open(src));RS=d['rs'];GX,GY=d['nx']*RS+1,d['ny']*RS+1
f=lambda k:np.frombuffer(base64.b64decode(d[k]),np.float32).reshape(GY,GX).astype(np.float64)
GB=f('GB');WV=f('WV')
def senken(GB,WV):
    nass=WV>-900
    seed=GB.copy();seed[1:-1,1:-1]=GB.max();seed[nass]=GB[nass]   # Rand und Wasser = Abfluss
    F=reconstruction(seed,GB,method='erosion');return F-GB
T=senken(GB,WV)
L,n=nd.label(T>0.3)
komp=[]
for i,sl in enumerate(nd.find_objects(L),1):
    m=L[sl]==i;t=T[sl][m];j,k=np.argwhere(m).mean(0)+[sl[0].start,sl[1].start]
    x,y=k/RS,j/RS
    komp.append(dict(x=round(x,1),y=round(y,1),feld=f"{'ABCDEFGH'[min(7,int(x//42))]}{min(7,int(y//43))+1}",tiefe=round(float(t.max()),2),ecken=int(m.sum())))
komp.sort(key=lambda c:-c['tiefe'])
out=dict(quelle=os.path.basename(src),senken_gt0_3=len(komp),gt1=sum(c['tiefe']>1 for c in komp),gt2=sum(c['tiefe']>2 for c in komp),liste=komp)
if len(sys.argv)>2:json.dump(out,open(sys.argv[2],'w'),indent=1)
print({k:v for k,v in out.items() if k!='liste'})
for c in komp[:30]:print(c)
