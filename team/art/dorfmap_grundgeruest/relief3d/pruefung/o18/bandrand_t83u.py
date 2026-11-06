# O18: stufe_bandrand direkt am Endstand: Feinband-Randpunkte (Punkt mit fehlendem 8er-Nachbarn) gegen Grobnetz GB
# (gleiche Dreiecksinterpolation wie npz_nach). Grund: fehlerzaehler_t67u vergleicht mit FB aus Zeile 571 (vor O18),
# O18 aendert G_ANZ danach -> dort Scheinstufen. Schwelle 0,3 m wie t67u.
import json,gzip,base64,numpy as np,scipy.ndimage as nd,sys
d=json.load(gzip.open(sys.argv[1]));RS=d['rs'];NX,NY=d['nx'],d['ny'];GX,GY=NX*RS+1,NY*RS+1
FW=d['FW'];FS=FW['fs'];FX,FY=NX*FS+1,NY*FS+1
vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
G=np.frombuffer(base64.b64decode(d['GB']),np.float32).reshape(GY,GX).astype(float)
m=np.zeros(FX*FY,bool);m[vid]=True;m=m.reshape(FY,FX);rand=(m&~nd.binary_erosion(m,np.ones((3,3)),border_value=1)).ravel()[vid]
fy,fx=vid//FX,vid%FX;gx=fx/FS*RS;gy=fy/FS*RS
i=np.minimum(gx.astype(int),GX-2);j=np.minimum(gy.astype(int),GY-2);ax=gx-i;az=gy-j
A,B,C,D=G[j,i],G[j,i+1],G[j+1,i],G[j+1,i+1];hg=np.where(az>=ax,A+az*(C-A)+ax*(D-C),A+ax*(B-A)+az*(D-B))
dd=np.abs(h-hg)[rand];print({'randpunkte':int(rand.sum()),'stufe_bandrand_gt0_3':int((dd>0.3).sum()),'max_m':round(float(dd.max()),3)})
