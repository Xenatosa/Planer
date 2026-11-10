# t36u: einfacher Software-Renderer (z-Buffer, Perspektive, Lambert-Licht) direkt aus der GLB.
# Aufruf: python3 render_modell3d.py [skin_gruppe skin_bild ausgabe]
import sys,numpy as np,pygltflib as G
from PIL import Image
from multiprocessing import Pool
NX,NY=336,303
gl=G.GLTF2().load_binary('dorfmap_c20_z25.glb');blob=gl.binary_blob()
def lese(i,n):
    a=gl.accessors[i];bv=gl.bufferViews[a.bufferView];dt={5126:np.float32,5125:np.uint32}[a.componentType]
    return np.frombuffer(blob,dt,a.count*n,bv.byteOffset+(a.byteOffset or 0)).reshape(a.count,n)
TEX=np.asarray(Image.open('textur_c20_8px.jpg')).astype(np.float32)/255
SKIN=None
if len(sys.argv)>3: SKIN=(sys.argv[1],np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(np.float32)/255)
TEILE=[]
for m in gl.meshes:
    p=m.primitives[0];TEILE.append((m.name,lese(p.attributes.POSITION,3).astype(float),lese(p.attributes.NORMAL,3).astype(float),
      lese(p.attributes.TEXCOORD_0,2).astype(float),lese(p.attributes.TEXCOORD_1,2).astype(float),lese(p.indices,1)[:,0].reshape(-1,3)))
L=np.array([-0.5,0.75,-0.45]);L/=np.linalg.norm(L)   # Licht von Nordwest oben [A]
def farbe(name,uv0,uv1,n):
    if name=='SOCKEL': c=np.array([0.42,0.36,0.33])
    elif name=='WASSER_OBERFLAECHE': c=np.array([0.35,0.6,0.8])
    elif SKIN and name==SKIN[0]:
        t=SKIN[1];c=t[np.clip((uv1[1]*(t.shape[0]-1)).astype(int),0,t.shape[0]-1),np.clip((uv1[0]*(t.shape[1]-1)).astype(int),0,t.shape[1]-1)]
    else: c=TEX[np.clip((uv0[1]*(TEX.shape[0]-1)).astype(int),0,TEX.shape[0]-1),np.clip((uv0[0]*(TEX.shape[1]-1)).astype(int),0,TEX.shape[1]-1)]
    return c*(0.55+0.55*max(0,float(n@L)))
def render(a):
    name_out,eye,ziel,fov,Wd,Hd=a
    eye=np.array(eye,float);ziel=np.array(ziel,float);f=ziel-eye;f/=np.linalg.norm(f)
    r=np.cross(f,[0,1,0]);r/=np.linalg.norm(r);u=np.cross(r,f);foc=Hd/2/np.tan(np.radians(fov/2))
    img=np.full((Hd,Wd,3),[0.80,0.85,0.90]);zb=np.full((Hd,Wd),np.inf);wasser=[]
    for name,P,N,U0,U1,I in TEILE:
        d=P-eye;z=d@f;sx=Wd/2+foc*(d@r)/np.maximum(z,1e-3);sy=Hd/2-foc*(d@u)/np.maximum(z,1e-3)
        for t in I:
            if (z[t]<0.5).any(): continue
            x0,x1=int(max(0,np.floor(sx[t].min()))),int(min(Wd-1,np.ceil(sx[t].max())));y0,y1=int(max(0,np.floor(sy[t].min()))),int(min(Hd-1,np.ceil(sy[t].max())))
            if x0>x1 or y0>y1: continue
            X,Y=np.meshgrid(np.arange(x0,x1+1)+0.5,np.arange(y0,y1+1)+0.5)
            (xa,xb,xc),(ya,yb,yc)=sx[t],sy[t];den=(yb-yc)*(xa-xc)+(xc-xb)*(ya-yc)
            if abs(den)<1e-9: continue
            w0=((yb-yc)*(X-xc)+(xc-xb)*(Y-yc))/den;w1=((yc-ya)*(X-xc)+(xa-xc)*(Y-yc))/den;w2=1-w0-w1
            m=(w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)
            if not m.any(): continue
            zz=1/(w0/z[t[0]]+w1/z[t[1]]+w2/z[t[2]])
            n=N[t].mean(0);n/=np.linalg.norm(n)+1e-9
            yi,xi=np.nonzero(m);yi+=y0;xi+=x0;zz=zz[m]
            ws=(np.c_[w0[m]/z[t[0]],w1[m]/z[t[1]],w2[m]/z[t[2]]])*zz[:,None]
            uv0=(ws@U0[t]).T;uv1=(ws@U1[t]).T
            c=farbe(name,uv0,uv1,n)
            if name=='WASSER_OBERFLAECHE': wasser.append((yi,xi,zz,c));continue
            ok=zz<zb[yi,xi];yi,xi=yi[ok],xi[ok];zb[yi,xi]=zz[ok];img[yi,xi]=c[ok] if c.ndim==2 else c
    for yi,xi,zz,c in wasser:
        ok=zz<zb[yi,xi]-0.01;img[yi[ok],xi[ok]]=0.45*img[yi[ok],xi[ok]]+0.55*(c[ok] if c.ndim==2 else c)
    Image.fromarray((np.clip(img,0,1)*255).astype(np.uint8)).save(name_out)
M=(NX/2,0,NY/2)
ANS=[('r1_schraeg_suedost.png',(330,140,420),M,40,1600,1000),
     ('r2_schraeg_nordwest_rueckseite.png',(-60,130,-110),M,40,1600,1000),
     ('r3_von_oben.png',(NX/2,520,NY/2+1),M,40,1400,1300),
     ('r4_sued_flach.png',(NX/2,25,NY+150),(NX/2,0,NY/2),45,1600,800),
     ('r5_nord_rueckseite.png',(NX/2,60,-150),(NX/2,0,NY/2),45,1600,900),
     ('r6_ost.png',(NX+170,80,NY/2),(NX/2,0,NY/2),45,1600,900),
     ('r7_west.png',(-170,80,NY/2),(NX/2,0,NY/2),45,1600,900),
     ('r8_rand_flach_suedwestecke.png',(-25,3,NY+25),(60,-2,NY-60),60,1600,900)]
if SKIN: ANS=[(sys.argv[3],(170,60,330),(150,0,250),45,1400,900)]
if __name__=='__main__':
    with Pool(8) as p: p.map(render,ANS)
