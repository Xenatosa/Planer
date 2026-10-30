# t42u: Bodentextur = gemalte c20-Karte (Draufsicht). Gemaltes Wandband/Schatten wird mit Farbe der eigenen Ebene aufgefuellt,
# weil Wand jetzt echte Geometrie mit eigener Wandtextur ist und Licht/Schatten aus der Engine kommt. c20 selbst bleibt unveraendert.
import csv,numpy as np,scipy.ndimage as nd
from PIL import Image
NX,NY,PX=336,303,8
T=np.asarray(Image.open('../_alt/modell3d_t36u/textur_c20_8px.jpg').convert('RGB')).astype(float)/255
R=list(csv.DictReader(open('zellen_relief.csv')));A=lambda k:np.array([r[k] for r in R]).reshape(NY,NX)
ug=A('untergrund_c20');Hb=A('boden_hoehe_m').astype(float)
M=np.isin(ug,['KLIPPE_WAND','KLIPPE_KANTE','SCHATTEN'])
k=4;S=T.reshape(NY,PX,NX,PX,3).reshape(NY,PX,NX,PX,3)
small=np.asarray(Image.fromarray((T*255).astype(np.uint8)).resize((NX*2,NY*2),Image.BILINEAR)).astype(float)/255
Ms=np.kron(M,np.ones((2,2)))>0;Hs=np.kron(Hb,np.ones((2,2)))
fill=small.copy()
for h in np.unique(np.round(Hs[Ms])):
    ziel=Ms&(np.round(Hs)==h);quelle=(~Ms)&(np.abs(Hs-h)<1.0)
    if not quelle.any():quelle=~Ms
    out=np.zeros(small.shape);done=np.zeros(Hs.shape,bool)
    for s in (3,10,30,90):
        w=nd.gaussian_filter(quelle.astype(float),s);v=np.stack([nd.gaussian_filter(small[...,c]*quelle,s) for c in range(3)],-1)
        ok=ziel&~done&(w>0.02);out[ok]=v[ok]/w[ok][:,None];done|=ok
    rest=ziel&~done
    if rest.any():
        q2=~Ms;w=nd.gaussian_filter(q2.astype(float),20);v=np.stack([nd.gaussian_filter(small[...,c]*q2,20) for c in range(3)],-1);out[rest]=v[rest]/np.maximum(w[rest],1e-6)[:,None]
    fill[ziel]=out[ziel]
F=np.asarray(Image.fromarray((fill*255).astype(np.uint8)).resize((NX*PX,NY*PX),Image.BILINEAR)).astype(float)/255
a=nd.gaussian_filter(np.kron(M,np.ones((PX,PX))).astype(float),3)[...,None]
rs=np.random.default_rng(7);n=nd.gaussian_filter(rs.standard_normal((NY*PX,NX*PX)),1.5);n=1+0.03*n/n.std()
O=T*(1-a)+F*n[...,None]*a
Image.fromarray((np.clip(O,0,1)*255).astype(np.uint8)).save('textur_relief_t42u.jpg',quality=88)
print('maskiert',int(M.sum()),'Zellen')
