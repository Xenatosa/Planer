# L3f Messbild: VC (linear), VC-Gradient, GB-Schummerung mit Maskenkante, E3-West x 180-194 z 94-124. Aufruf: python3 l3f_vcplot.py out.png daten.gz [daten2.gz]
import gzip,json,base64,numpy as np,sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
out=sys.argv[1]; fs=sys.argv[2:]
x0,x1,z0,z1=180,194,94,124
fig,ax=plt.subplots(len(fs),3,figsize=(18,11*len(fs)))
ax=np.atleast_2d(ax)
for r,f in enumerate(fs):
    D=json.loads(gzip.decompress(open(f,'rb').read())); rs=D['rs']; GX=D['nx']*rs+1; GY=D['ny']*rs+1
    GB=np.frombuffer(base64.b64decode(D['GB']),'<f4').reshape(GY,GX); WV=np.frombuffer(base64.b64decode(D['WV']),'<f4').reshape(GY,GX)
    VC=np.frombuffer(base64.b64decode(D['VC']),np.uint8).reshape(GY,GX,3)
    sl=(slice(z0*rs,z1*rs+1),slice(x0*rs,x1*rs+1)); ext=[x0-0.25,x1+0.25,z1+0.25,z0-0.25]
    Lin=((VC[sl]/255.0)**2.2).mean(-1)
    gy,gx=np.gradient(Lin); G=np.hypot(gx,gy)
    gy2,gx2=np.gradient(GB[sl].astype(float)); hs=-gx2-gy2
    for c,(im,cm,t) in enumerate([(Lin,'gray','VC linear hell'),(G,'magma','VC Gradient'),(hs,'gray','GB Schummer')]):
        a=ax[r,c]; a.imshow(im,extent=ext,cmap=cm,interpolation='nearest',vmin=np.percentile(im,1),vmax=np.percentile(im,99))
        a.contour(np.arange(x0*rs,x1*rs+1)/rs,np.arange(z0*rs,z1*rs+1)/rs,(WV[sl]>-900).astype(float),[0.5],colors='c',linewidths=0.8)
        a.set_title(f.split('/')[-1]+' '+t)
plt.tight_layout(); plt.savefig(out,dpi=50)
