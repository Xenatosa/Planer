# t62u: Steilheit der Anzeige (GB) gegen Zellgelaende (G), Wassertiefe, Stuecke [S]
import json,gzip,base64,sys,numpy as np,scipy.ndimage as nd
D=json.load(gzip.open(sys.argv[1] if len(sys.argv)>1 else 'relief_daten.json.gz'));GX,GY=D['nx']*2+1,D['ny']*2+1
f=lambda k:np.frombuffer(base64.b64decode(D[k]),np.float32).reshape(GY,GX).astype(float)
G=f('G');B=f('GB');WV=f('WV');M=WV>-900
sl=lambda A:np.degrees(np.arctan(np.hypot(*np.gradient(A,0.5))))
a=sl(G);b=sl(B);neu=(b>60)&(a<=60);t=(WV-B)[M];lab,n=nd.label(M,np.ones((3,3)));sz=np.sort(nd.sum(M,lab,range(1,n+1)))[::-1]
d=np.abs(G-B)>0.006;Z=d.reshape(-1)
C=np.zeros((D['ny'],D['nx']),bool)
for i in range(3):
    for j in range(3):C|=d[i:i+D['ny']*2:2,j:j+D['nx']*2:2]
print(json.dumps({'neu_steiler_60':int(neu.sum()),'davon_land':int((neu&~M).sum()),'davon_wasser':int((neu&M).sum()),
 'max_schnitt_m':round(float((G-B).max()),2),'max_auffuellung_m':round(float((B-G).max()),2),'anzeige_abweichend_vertices':int(d.sum()),'anzeige_abweichend_zellen':int(C.sum()),
 'tiefe_min':round(float(t.min()),2),'tiefe_p10':round(float(np.percentile(t,10)),2),'tiefe_p50':round(float(np.percentile(t,50)),2),'tiefe_p90':round(float(np.percentile(t,90)),2),'tiefe_max':round(float(t.max()),2),
 'stuecke':int(n),'stuecke_unter_20':int((sz<20).sum()),'groessen':[int(x) for x in sz[:8]]}))
