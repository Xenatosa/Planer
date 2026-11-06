# t34u 3D-Gelaendemodell aus c20 + z25-Raster (hoehe_m, ebene). Keine Bildgenerierung, nur Geometrie.
# Hoehen: alle [A] aus raster_c20_z25_zellen.csv. Wandzellen: Hoehe der naechsten freien Zelle [A]
# -> Stufe liegt in der Wandmitte, Wand senkrecht. Export OBJ in Metern (1 Zelle = 1 m), Renders mit Ueberhoehung x3 [F].
import csv,numpy as np
from scipy import ndimage as nd
from PIL import Image
C20='/workspace/handygame-plan/team/art/karten_konzept/dorfkarte_e1_final_neu/master_v18_p7/KANDIDAT_NICHT_FREIGEGEBEN_master_v18_p7_c20.png'
NX,NY=336,303
H=np.zeros((NY,NX));W=np.zeros((NY,NX),bool)
for r in csv.DictReader(open('../raster_c20_z25_zellen.csv')):
    x,y=int(r['cx']),int(r['cy']);H[y,x]=float(r['hoehe_m']);W[y,x]=r['ebene']=='WAND'
_,(iy,ix)=nd.distance_transform_edt(W,return_indices=True)
H3=H[iy,ix]                      # Wand -> naechste freie Zelle
np.save('hoehe3d_z25.npy',H3)
tex=Image.open(C20).convert('RGB').crop((0,0,NX*25,NY*25))
tex.resize((NX*8,NY*8),Image.LANCZOS).save('textur_c20_8px.jpg',quality=90)
# OBJ: Zellmitte-Gitter + senkrechte Stufen ueber doppelte Kantenpunkte (Zellquadrate einzeln)
with open('dorfmap_c20_z25.obj','w') as f:
    f.write('# Epodarien Dorfmap c20, z25, Meter, y=hoch. Hoehen [A]\nmtllib dorfmap_c20_z25.mtl\nusemtl c20\n')
    # je Zelle 4 Ecken mit Zellhoehe -> Plateaus flach, Stufen senkrecht
    vid={}
    def v(x,y,h):
        k=(x,y,round(h,2))
        if k not in vid:
            vid[k]=len(vid)+1; f.write(f'v {x:.0f} {h:.2f} {y:.0f}\nvt {x/NX:.5f} {1-y/NY:.5f}\n')
        return vid[k]
    faces=[]
    for y in range(NY):
        for x in range(NX):
            h=H3[y,x];a,b,c,d=v(x,y,h),v(x+1,y,h),v(x+1,y+1,h),v(x,y+1,h);faces.append((a,d,c,b))
            if x+1<NX and abs(H3[y,x+1]-h)>1e-3:
                g=H3[y,x+1];faces.append((v(x+1,y,h),v(x+1,y+1,h),v(x+1,y+1,g),v(x+1,y,g)))
            if y+1<NY and abs(H3[y+1,x]-h)>1e-3:
                g=H3[y+1,x];faces.append((v(x,y+1,h),v(x+1,y+1,h),v(x+1,y+1,g),v(x,y+1,g)))
    for q in faces: f.write('f '+' '.join(f'{i}/{i}' for i in q)+'\n')
open('dorfmap_c20_z25.mtl','w').write('newmtl c20\nKd 1 1 1\nmap_Kd textur_c20_8px.jpg\n')
print('Ecken',len(vid),'Flaechen',len(faces))
# ---- Renders: Punktwolke mit z-Buffer, 4 Punkte/m, senkrechte Waende aufgefuellt
U=4;EX=3.0
T=np.asarray(tex.resize((NX*U,NY*U),Image.LANCZOS)).astype(float)/255
Hu=H3.repeat(U,0).repeat(U,1)*EX
yy,xx=np.mgrid[0:NY*U,0:NX*U];P=[np.c_[xx.ravel()/U,yy.ravel()/U,Hu.ravel()]];Cc=[T.reshape(-1,3)]
for ax in (0,1):
    d=np.diff(Hu,axis=ax);
    m=np.abs(d)>0.3
    ys,xs=np.nonzero(m)
    hi=np.where(ax==0,Hu[ys,xs],Hu[ys,xs]);lo=Hu[ys+(ax==0),xs+(ax==1)]
    for t in np.linspace(0,1,40)[1:-1]:
        P.append(np.c_[(xs+0.5*(ax==1))/U,(ys+0.5*(ax==0))/U,hi+(lo-hi)*t]);Cc.append(T[ys,xs]*0.75)
P=np.vstack(P);Cc=np.vstack(Cc)
# einfache Schattierung ueber Hangneigung
gy,gx=np.gradient(H3*EX);sh=np.clip(0.85-0.15*(gx-gy),0.5,1.15)
def render(name,az,el,Wd=1600,Hd=1100,top=False):
    X=P[:,0]-NX/2;Y=P[:,1]-NY/2;Z=P[:,2]
    a=np.radians(az);e=np.radians(el)
    xr=X*np.cos(a)-Y*np.sin(a);yr=X*np.sin(a)+Y*np.cos(a)   # yr = Tiefe (Blickrichtung)
    sx=xr; sy=yr*np.sin(e)-Z*np.cos(e); dep=yr*np.cos(e)+Z*np.sin(e)
    s=min(Wd/(np.ptp(sx)+10),Hd/(np.ptp(sy)+10))
    px=((sx-sx.min())*s+5).astype(int);py=((sy-sy.min())*s+5).astype(int)
    img=np.ones((Hd+20,Wd+20,3))*0.93;zb=np.full((Hd+20,Wd+20),-1e9)
    k=max(1,int(np.ceil(s/U)))
    o=np.argsort(dep)                      # hinten zuerst -> vorne ueberschreibt
    for dx in range(k):
        for dy in range(k):
            img[py[o]+dy,px[o]+dx]=Cc[o]
    im=Image.fromarray((np.clip(img,0,1)*255).astype(np.uint8))
    bb=Image.fromarray(((zb<0)&(np.abs(img-0.93).sum(-1)>0.01)).astype(np.uint8)*255).getbbox()
    im.crop((max(0,bb[0]-10),max(0,bb[1]-10),bb[2]+10,bb[3]+10)).save(name)
# Blick: az=0 -> von Sueden (Kamera im Sueden, schaut nach Norden)
render('render_schraeg_suedost.png',35,40)
render('render_von_oben.png',0,90)
render('render_sued.png',0,25)
render('render_nord.png',180,25)
render('render_west.png',-90,25)
render('render_ost.png',90,25)
