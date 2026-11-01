# t53u: Formmessung Waende (Neigung im Wandband), Schuttfuss, Flussufer [R]
import json,gzip,base64,csv,numpy as np
D=json.load(gzip.open('relief_daten.json.gz'));NX,NY,RS=D['nx'],D['ny'],D['rs']
G=np.frombuffer(base64.b64decode(D['G']),np.float32).reshape(NY*RS+1,NX*RS+1).astype(float)
gy,gx=np.gradient(G,1/RS);sl=np.degrees(np.arctan(np.hypot(gx,gy)))[:-1,:-1].reshape(NY,RS,NX,RS).mean((1,3))
R=list(csv.DictReader(open('zellen_relief.csv')));A=lambda k:np.array([r[k] for r in R]).reshape(NY,NX)
kl=A('klippe');wa=A('wasser_eis')=='1'
out={}
for n,m in (('WAND',kl=='WAND'),('WAND_FUSS',kl=='WAND_FUSS')):
    v=sl[m];out[n]={'p10':round(float(np.percentile(v,10)),1),'p50':round(float(np.median(v)),1),'p90':round(float(np.percentile(v,90)),1),
      'anteil_60_85':round(float(((v>=60)&(v<=85)).mean()),2),'anteil_30_38':round(float(((v>=30)&(v<=38)).mean()),2)}
import scipy.ndimage as nd
uf=nd.binary_dilation(wa,iterations=2)&~wa&(kl=='');v=sl[uf];out['ufer_2zellen']={'p50':round(float(np.median(v)),1),'p90':round(float(np.percentile(v,90)),1)}
t=A('wasser_tiefe_m').astype(float)[wa];out['wassertiefe']={'min':float(t.min()),'p50':float(np.median(t)),'max':float(t.max())}
print(json.dumps(out))
