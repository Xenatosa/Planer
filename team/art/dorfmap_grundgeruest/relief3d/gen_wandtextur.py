# t43u: prozedurale, kachelbare Texturen [A]. wand_textur.png = Fels-Schichtung + Risse (Graustufen-Albedo, 1 Kachel = 6 m),
# detail_textur.png = feines Bodenrauschen (1 Kachel = 4 m). Farbe kommt im Viewer aus Material-Gewichten.
import numpy as np,scipy.ndimage as nd
from PIL import Image
r=np.random.default_rng(4);N=512
def fbm(n,okt,seed):
    g=np.random.default_rng(seed);o=np.zeros((n,n))
    for k in range(okt):s=n/(2**(k+2));o+=nd.gaussian_filter(g.standard_normal((n,n)),s,mode='wrap')*(0.55**k)*s**0.9
    return (o-o.mean())/o.std()
y=np.arange(N)[:,None]/N;x=np.arange(N)[None,:]/N
w=fbm(N,5,1);band=np.sin((y*9+0.15*w)*2*np.pi)+0.5*np.sin((y*23+0.04*w)*2*np.pi)   # Schichten (kachelbar)
risse=np.abs(fbm(N,4,2));risse=np.exp(-risse*6)                                     # Risse = Nulllinien
vert=np.abs(np.sin((x*4+0.15*fbm(N,4,3))*np.pi));vert=np.exp(-vert*5)*(fbm(N,2,8)>0.2)
A=0.62+0.045*band+0.10*fbm(N,6,5)-0.28*risse*(0.5+0.5*(fbm(N,3,6)>0))-0.12*vert+0.05*nd.gaussian_filter(vert,6,mode="wrap")
Image.fromarray((np.clip(A,0,1)*255).astype(np.uint8)).save('wand_textur.png')
D=0.5+0.5*np.tanh(0.6*fbm(256,6,9))
Image.fromarray((np.clip(0.75+0.25*D,0,1)*255).astype(np.uint8)).save('detail_textur.png')
print('ok')
