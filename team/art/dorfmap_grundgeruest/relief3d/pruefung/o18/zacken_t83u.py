# O18 [F A1,B1,C1,E1,F1,C2]: "Dreiecke in den Boden"/Zacken: Punkt-Ausreisser im Feinband UND Grobnetz.
# Zacke nach unten: beide 1D-2.-Ableitungen (x und z, plus 2 Diagonalen) > thr (konkav in ALLEN Richtungen = Loch/Nadel),
# nach oben: alle < -thr. Glatte Steilhaenge/Wandfuesse sind nur in EINER Richtung gekruemmt -> nicht gezaehlt.
import json,gzip,base64,numpy as np,sys,collections,scipy.ndimage as nd
d=json.load(gzip.open(sys.argv[1]));RS=d['rs'];NX,NY=d['nx'],d['ny'];GX,GY=NX*RS+1,NY*RS+1
FW=d['FW'];FS=FW['fs'];FX,FY=NX*FS+1,NY*FS+1
vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);h=np.frombuffer(base64.b64decode(FW['h']),np.float32)
GB=np.frombuffer(base64.b64decode(d['GB']),np.float32).reshape(GY,GX).astype(float)
def zack(F,sp,thr):
    P=np.pad(F,1,mode='edge');c=P[1:-1,1:-1]
    dd=[P[1:-1,2:]+P[1:-1,:-2]-2*c,P[2:,1:-1]+P[:-2,1:-1]-2*c,(P[2:,2:]+P[:-2,:-2]-2*c)/2,(P[2:,:-2]+P[:-2,2:]-2*c)/2]
    dd=np.array(dd);return np.min(dd,0)>thr,np.max(dd,0)<-thr,np.min(dd,0),-np.max(dd,0)
def feld(x,y):return f"{'ABCDEFGH'[min(7,int(x//42))]}{min(7,int(y//43))+1}"
out={}
fy,fx=np.mgrid[0:FY,0:FX]
F=np.full(FX*FY,np.nan);F[vid]=h;F=F.reshape(FY,FX);m=~np.isnan(F)
Ff=np.where(m,F,nd.map_coordinates(GB,[fy/FS*RS,fx/FS*RS],order=1))
thr=float(sys.argv[3]) if len(sys.argv)>3 else 0.25
B=np.zeros(NX*NY,bool);B[np.frombuffer(base64.b64decode(FW['band']),np.uint32)]=True;B=B.reshape(NY,NX)
Bp=np.pad(B,1,constant_values=True);gj,gi=np.mgrid[0:GY,0:GX]//RS
sicht=~(Bp[gj,gi]&Bp[gj+1,gi]&Bp[gj,gi+1]&Bp[gj+1,gi+1])  # Grobecke sichtbar, wenn eine angrenzende Zelle kein Band ist
for nm,A,sp,ok in (('fein',Ff,FS,m),('grob',GB,RS,sicht)):
    u,o,vu,vo=zack(A,sp,thr);r={}
    for k,M,V in (('unten',u&ok,vu),('oben',o&ok,vo)):
        L,n=nd.label(M);lst=[]
        for i,sl in enumerate(nd.find_objects(L),1):
            mm=L[sl]==i;j,kk=np.argwhere(mm).mean(0)+[sl[0].start,sl[1].start];x,y=kk/sp,j/sp
            lst.append(dict(x=round(x,2),y=round(y,2),feld=feld(x,y),wert=round(float(V[sl][mm].max()),2)))
        lst.sort(key=lambda c:-c['wert']);r[k]=dict(n=len(lst),je_feld=dict(collections.Counter(c['feld'] for c in lst).most_common()),top=lst[:40])
    out[nm]=r
    print(nm,{k:(v['n'],list(v['je_feld'].items())[:10]) for k,v in r.items()})
if len(sys.argv)>2:json.dump(out,open(sys.argv[2],'w'),indent=1)
