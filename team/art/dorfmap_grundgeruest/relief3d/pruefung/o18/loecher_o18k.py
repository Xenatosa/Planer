# O18k (t107u): kartenweite Suche nach Loechern/Trichtern (Senke ggue. Umgebung) und Beulen, nur trockenes Land. python3 ... relief_daten.json.gz
import json,gzip,sys,base64,numpy as np,scipy.ndimage as nd
D=json.load(gzip.open(sys.argv[1]));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(GY,GX).astype(float)
WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(GY,GX) if 'WV' in D else None
land=(WV<=-900) if WV is not None else np.ones_like(G,bool);trocken=nd.binary_erosion(land,iterations=4*RS)
from skimage.morphology import reconstruction
sd=G.copy();sd[1:-1,1:-1]=G.max();fill=reconstruction(sd,G,method='erosion');tief=fill-G   # echte abflusslose Senke (Sink-Fill vom Kartenrand)
if WV is not None: tief[~land]=0
beul=G-nd.grey_opening(G,size=(4*RS+1,4*RS+1))
out=[]
for nm,A,thr in (('loch',tief,0.5),('beule',beul,0.6)):
    m=(A>thr)&trocken;lab,n=nd.label(m)
    for k in range(1,n+1):
        yy,xx=np.nonzero(lab==k);a=A[yy,xx];j=a.argmax();x,z=xx[j]/RS,yy[j]/RS
        out.append({'art':nm,'x':round(x,1),'z':round(z,1),'feld':'ABCDEFGH'[min(int(x//42),7)]+str(int(z//43)+1),'tiefe_m':round(float(a.max()),2),'flaeche_m2':round(len(xx)/RS/RS,1),'h':round(float(G[yy[j],xx[j]]),2)})
out.sort(key=lambda o:-o['tiefe_m']);json.dump(out,open(sys.argv[2],'w'),indent=0) if len(sys.argv)>2 else 0
print(len([o for o in out if o['art']=='loch']),'loecher',len([o for o in out if o['art']=='beule']),'beulen');[print(o) for o in out[:25]];[print(o) for o in out if o['feld']=='E1']
