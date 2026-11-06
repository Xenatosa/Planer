# O18d [F G1 Pyramide, "nirgends Pyramiden"]: Spitzigkeit = Hoehe - Gauss-Mittel (sigma 1 m / 3 m) auf der sichtbaren Flaeche (Fein wo Band, sonst Grob, 0,25 m).
# Nur lokale Maxima (5x5) zaehlen. Pyramide = Spitzigkeit_1m > 0,25 m (scharfe Spitze) oder _3m > 1,5 m.
import json,gzip,base64,numpy as np,sys,scipy.ndimage as nd,collections
d=json.load(gzip.open(sys.argv[1]));RS=d['rs'];NX,NY=d['nx'],d['ny'];GX,GY=NX*RS+1,NY*RS+1
FW=d['FW'];FS=FW['fs'];FX,FY=NX*FS+1,NY*FS+1
vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);h=np.frombuffer(base64.b64decode(FW['h']),np.float32)
GB=np.frombuffer(base64.b64decode(d['GB']),np.float32).reshape(GY,GX).astype(float)
fy,fx=np.mgrid[0:FY,0:FX];F=np.full(FX*FY,np.nan);F[vid]=h;F=F.reshape(FY,FX);m=~np.isnan(F)
Ff=np.where(m,F,nd.map_coordinates(GB,[fy/FS*RS,fx/FS*RS],order=1))
s1=Ff-nd.gaussian_filter(Ff,4);s3=Ff-nd.gaussian_filter(Ff,12)
mx=(Ff==nd.maximum_filter(Ff,5));rand=np.zeros_like(mx);rand[8:-8,8:-8]=True
P=mx&rand&((s1>0.25)|(s3>1.5))
lab,n=nd.label(nd.binary_dilation(P,iterations=2));c=collections.Counter();top=[]
for i,sl in enumerate(nd.find_objects(lab)):
    yy,xx=np.nonzero(P[sl]&(lab[sl]==i+1))
    if len(yy)==0:continue
    y,x=(yy[0]+sl[0].start)/FS,(xx[0]+sl[1].start)/FS;f=f"{'ABCDEFGH'[min(7,int(x//42))]}{min(7,int(y//43.3))+1}";c[f]+=1
    top.append(dict(x=round(x,1),y=round(y,1),feld=f,s1=round(float(s1.max() if False else s1[int(y*FS),int(x*FS)]),2),s3=round(float(s3[int(y*FS),int(x*FS)]),2)))
top.sort(key=lambda t:-max(t['s1']*6,t['s3']))
r=dict(n=len(top),je_feld=dict(c.most_common()),top=top[:15]);print(json.dumps(r)[:900])
if len(sys.argv)>2:json.dump(r,open(sys.argv[2],'w'),indent=1)
