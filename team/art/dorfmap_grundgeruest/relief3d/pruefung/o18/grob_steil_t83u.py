# O18: steile SICHTBARE Grobnetz-Quads (Zelle nicht im Feinband) = Wandteile im 0,5-m-Netz -> Saegezaehne/"Dreiecke in den Boden".
import json,gzip,base64,numpy as np,sys,collections
d=json.load(gzip.open(sys.argv[1]));RS=d['rs'];NX,NY=d['nx'],d['ny'];GX,GY=NX*RS+1,NY*RS+1
G=np.frombuffer(base64.b64decode(d['GB']),np.float32).reshape(GY,GX).astype(float)
B=np.zeros(NX*NY,bool);B[np.frombuffer(base64.b64decode(d['FW']['band']),np.uint32)]=True;B=B.reshape(NY,NX)
q=np.maximum.reduce([np.abs(G[1:,:-1]-G[:-1,:-1]),np.abs(G[:-1,1:]-G[:-1,:-1]),np.abs(G[1:,1:]-G[1:,:-1]),np.abs(G[1:,1:]-G[:-1,1:])])*RS  # Steigung je Quad
cj,ci=np.mgrid[0:GY-1,0:GX-1]//RS;sicht=~B[np.minimum(cj,NY-1),np.minimum(ci,NX-1)]
r={}
for t in (1.5,3,6):
    M=(q>t)&sicht;jj,ii=np.nonzero(M)
    r[f'gt{t}']=dict(n=int(M.sum()),je_feld=dict(collections.Counter(f"{'ABCDEFGH'[min(7,int(i/RS//42))]}{min(7,int(j/RS//43))+1}" for j,i in zip(jj,ii)).most_common(15)))
print(json.dumps(r))
if len(sys.argv)>2:json.dump(r,open(sys.argv[2],'w'),indent=1)
