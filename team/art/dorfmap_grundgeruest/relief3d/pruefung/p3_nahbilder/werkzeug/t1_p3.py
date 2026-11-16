# T1-Nachzaehlung wie pruefe_regeln.py (gleiche Formel), Ausgabe je Kachel; mit 2. Argument Liste je Treffer
import json,gzip,base64,numpy as np,scipy.ndimage as nd,sys,collections
D=json.load(gzip.open(sys.argv[1] if len(sys.argv)>1 else 'relief_daten.json.gz'));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(GY,GX).astype(float);LAND=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(GY,GX)<=-900
gy,gx=np.gradient(G,1/RS);WAND=np.hypot(gx,gy)>1.0
C=np.frombuffer(base64.b64decode(D['VC']),np.uint8).astype(float).reshape(GY,GX,3)
dc=np.linalg.norm(np.diff(C,axis=1)[:-1],axis=2)+np.linalg.norm(np.diff(C,axis=0)[:,:-1],axis=2)
R=LAND[:-1,:-1]&~nd.binary_dilation(WAND,iterations=RS)[:-1,:-1];lab,n=nd.label((dc>70)&R)
feld=lambda x,z:'ABCDEFGH'[int(np.clip(x//42,0,7))]+str(int(np.clip(z//43,0,6))+1)
cnt=collections.Counter()
for k in range(1,n+1):
    yy,xx=np.nonzero(lab==k)
    if len(xx)>=8:cnt[feld(xx.mean()/RS,yy.mean()/RS)]+=1;(print(feld(xx.mean()/RS,yy.mean()/RS),round(xx.mean()/RS,1),round(yy.mean()/RS,1),len(xx)) if len(sys.argv)>2 else 0)
print(json.dumps({'T1_ge8':sum(cnt.values()),'je_kachel':dict(sorted(cnt.items())),'dc_max_bewertet':round(float(dc[R].max()),1),'punkte_dc_gt70':int(((dc>70)&R).sum())}))
