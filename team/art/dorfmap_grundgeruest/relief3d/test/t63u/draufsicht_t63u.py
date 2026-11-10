# t63u: Draufsicht Flusslinie vorher (Runde J) / nachher (Runde K) auf Schummerung, mit Wegen/Bauplaetzen/Haeusern [S]
import json,gzip,base64,sys,csv,numpy as np,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
def lade(p):
    D=json.load(gzip.open(p));f=lambda k:np.frombuffer(base64.b64decode(D[k]),np.float32).reshape(607,673).astype(float);return f('GB'),f('WV'),D
O=list(csv.DictReader(open('../raster_c20_z25_overlay_plaetze_wege.csv')));weg=np.array([(int(r['cx']),int(r['cy'])) for r in O if r['weg_id']])
bau=np.array([(int(r['cx']),int(r['cy'])) for r in O if r['bauplatz'] not in('','0')])
fig,ax=plt.subplots(1,2,figsize=(20,11))
for a,(p,t) in zip(ax,((sys.argv[1],'vorher: Runde J'),(sys.argv[2],'nachher: Runde K'))):
    G,W,D=lade(p);hs=LightSource(315,40).hillshade(G,vert_exag=2,dx=.5,dy=.5)
    a.imshow(hs,cmap='gray',extent=(0,336.5,303.5,0));a.imshow(np.ma.masked_where(W<-900,W),cmap='winter',alpha=.85,extent=(0,336.5,303.5,0))
    a.scatter(weg[:,0]+.5,weg[:,1]+.5,s=1,c='orange',label='Weg');a.scatter(bau[:,0]+.5,bau[:,1]+.5,s=1,c='red',label='Bauplatz')
    h=np.array([[o['x'],o['z']] if isinstance(o,dict) else [o[0],o[2]] for o in D['haeuser']]);a.scatter(h[:,0],h[:,1],s=6,c='magenta',marker='s',label='Haus')
    a.set_xlim(0,130);a.set_ylim(290,20);a.set_title(t,fontsize=15);a.grid(alpha=.3);a.legend(loc='upper right',markerscale=5)
fig.tight_layout();fig.savefig(sys.argv[3],dpi=70)
