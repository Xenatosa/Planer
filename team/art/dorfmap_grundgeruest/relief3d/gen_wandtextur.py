# t44u: prozedurale, kachelbare Texturen [A].
# wand_textur.png (RGB, 1 Kachel = 9 m): unregelmaessige Schichten (zufaellige Dicke, gewellt), Kluftbloecke (Voronoi), Bruchkanten, Farbwechsel warm/kalt.
# detail_textur.png (Graustufe, 1 Kachel = 4 m): Bodenfeinrauschen.
import numpy as np,scipy.ndimage as nd
from PIL import Image
N=512
def fbm(n,okt,seed,p=0.55):
    g=np.random.default_rng(seed);o=np.zeros((n,n))
    for k in range(okt):s=n/(2**(k+2));o+=nd.gaussian_filter(g.standard_normal((n,n)),s,mode='wrap')*(p**k)*s**0.9
    return (o-o.mean())/o.std()
r=np.random.default_rng(7);y=np.arange(N)[:,None]/N;x=np.arange(N)[None,:]/N
# Schichten: Grenzen bei zufaelligen Hoehen, mit Verwerfung
gr=np.sort(r.random(11));dick=np.diff(np.r_[gr,gr[0]+1])
yy=(y+0.035*fbm(N,4,1)+0.02*np.sin(x*2*np.pi*2))%1
idx=np.searchsorted(gr,yy)%len(gr);ton=r.random(len(gr))[idx]
grenz=np.min(np.abs(yy[...,None]-np.r_[gr,gr+1,gr-1][None,None,:]),-1);kante=np.exp(-grenz*N/2.5)
# Kluftbloecke: Voronoi mit Punkten (kachelbar)
P=r.random((38,2));d1=np.full((N,N),9.);d2=np.full((N,N),9.);X=np.broadcast_to(x,(N,N));Y=np.broadcast_to(y,(N,N))
for px,py in P:
    for ox in(-1,0,1):
        for oy in(-1,0,1):
            d=np.hypot((X-px-ox)*1.0,(Y-py-oy)*0.7);m=d<d1;d2=np.where(m,d1,np.minimum(d2,d));d1=np.where(m,d,d1)
kluft=np.exp(-(d2-d1)*N/7.0)*(0.4+0.6*(fbm(N,4,6)>0))*(fbm(N,3,5)>-0.3)
bl=np.zeros((N,N));lab=np.argmin(np.stack([np.hypot(((X-px+0.5)%1-0.5),((Y-py+0.5)%1-0.5)*0.7) for px,py in P]),0);bl=r.random(38)[lab]
h=0.55+0.13*(ton-0.5)+0.08*(bl-0.5)+0.09*fbm(N,6,3)-0.17*kluft-0.16*kante+0.10*np.clip(fbm(N,5,9),0,None)
warm=0.5+0.5*np.tanh(fbm(N,3,11))
R=h*(0.98+0.10*warm);G=h*(0.96+0.03*warm);B=h*(0.95-0.07*warm)
Image.fromarray((np.clip(np.stack([R,G,B],-1),0,1)*255).astype(np.uint8)).save('wand_textur.png')
D=0.5+0.5*np.tanh(0.6*fbm(256,6,9))
Image.fromarray((np.clip(0.75+0.25*D,0,1)*255).astype(np.uint8)).save('detail_textur.png')
print('ok')
