# O18k: Wegquerschnitte kartenweit messen (Quergefaelle, Woelbung, Laengsrauheit) auf Anzeige-Gelaende (Fein wo vorhanden, sonst Grob). python3 ... relief_daten.json.gz [out.json]
import json,gzip,sys,base64,numpy as np,scipy.ndimage as nd
from skimage.morphology import skeletonize
D=json.load(gzip.open(sys.argv[1]));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
f32=lambda s:np.frombuffer(base64.b64decode(s),np.float32)
GB=f32(D['GB']).reshape(GY,GX).astype(float);FW=D['FW'];FS=FW['fs'];FX,FY=NX*FS+1,NY*FS+1
vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);F=np.full((FY,FX),np.nan);F[vid//FX,vid%FX]=f32(FW['h'])
def H(x,z):
    x=np.asarray(x,float);z=np.asarray(z,float);g=nd.map_coordinates(GB,[z*RS,x*RS],order=1,mode='nearest')
    fz,fx=z*FS,x*FS;i0=np.clip(np.floor(fx).astype(int),0,FX-2);j0=np.clip(np.floor(fz).astype(int),0,FY-2);u=fx-i0;v=fz-j0
    a,b,c,d=F[j0,i0],F[j0,i0+1],F[j0+1,i0],F[j0+1,i0+1];f=a*(1-u)*(1-v)+b*u*(1-v)+c*(1-u)*v+d*u*v
    return np.where(np.isfinite(f),f,g)
feld=lambda x,z:'ABCDEFGH'[int(np.clip(x//42,0,7))]+str(int(np.clip(z//43,0,6))+1)
S=np.linspace(-1.5,1.5,13)
def profil(P,T,step=1.5):   # P Mittelpunkte (n,2), T Tangenten
    N=np.stack([-T[:,1],T[:,0]],1);X=P[:,None,0]+N[:,None,0]*S;Z=P[:,None,1]+N[:,None,1]*S;h=H(X,Z)
    A=np.stack([np.ones_like(S),S,S**2],1);co=np.linalg.lstsq(A,h.T,rcond=None)[0];lin=np.polyfit(S,h.T,1)
    quer=np.abs(lin[0])*100;woelb=np.abs(h-(lin[0][:,None]*S+lin[1][:,None])).max(1);hc=H(P[:,0],P[:,1]);rau=np.abs(np.convolve(hc,[1,-2,1],'valid'))if len(hc)>2 else np.zeros(1)
    return quer,woelb,rau,hc
def zus(name,P,quer,woelb,rau):
    fs=sorted({feld(*p) for p in P})
    return {'weg':name,'felder':fs,'n':len(P),'quer_mittel_pct':round(float(quer.mean()),1),'quer_max_pct':round(float(quer.max()),1),'quer_gt8_anteil':round(float((quer>8).mean()),2),'woelb_mittel_m':round(float(woelb.mean()),3),'woelb_max_m':round(float(woelb.max()),3),'laengs_rau_m':round(float(rau.mean()),3)}
R=[]
for k,W in enumerate(D['rampenwege']):
    W=np.array(W,float);L=np.r_[0,np.cumsum(np.hypot(*np.diff(W,axis=0).T))];t=np.arange(0.75,L[-1]-0.5,1.5)
    P=np.stack([np.interp(t,L,W[:,0]),np.interp(t,L,W[:,1])],1);T=np.stack([np.interp(t+0.5,L,W[:,0])-np.interp(t-0.5,L,W[:,0]),np.interp(t+0.5,L,W[:,1])-np.interp(t-0.5,L,W[:,1])],1);T/=np.linalg.norm(T,axis=1,keepdims=True)
    q,w,r,_=profil(P,T);R.append(zus('rampe_%d'%k,P,q,w,r));R[-1]['g1_schnitte']=[[round(p[0],1),round(p[1],1),round(float(a),1),round(float(b),3)] for p,a,b in zip(P,q,w) if 252<=p[0]<294 and p[1]<43]
WE=np.frombuffer(base64.b64decode(D['WEGA']),np.uint8).reshape(GY,GX)>20 if len(base64.b64decode(D['WEGA']))==GY*GX else None
if WE is not None:
    sk=skeletonize(WE);yy,xx=np.nonzero(sk);pts=np.stack([xx,yy],1)/RS;lab,n=nd.label(sk,np.ones((3,3)))
    for f in sorted({feld(*p) for p in pts}):
        m=np.array([feld(*p)==f for p in pts]);Q=pts[m][::3]
        if len(Q)<4:continue
        T=[]
        for p in Q:
            nb=pts[np.hypot(*(pts-p).T)<2.0]-p;u,s,vt=np.linalg.svd(nb-nb.mean(0)) if len(nb)>2 else (0,0,np.array([[1,0]]));T.append(vt[0])
        q,w,r,_=profil(Q,np.array(T));R.append(zus('WEGA_'+f,Q,q,w,np.zeros(1)))
R.sort(key=lambda r:(-('G1' in r['felder']),-r['quer_gt8_anteil']))
json.dump(R,open(sys.argv[2] if len(sys.argv)>2 else '/dev/stdout','w'),indent=0)
for r in R:
    if r['quer_mittel_pct']>8 or r['woelb_max_m']>0.15 or 'G1' in r['felder']:print({k:v for k,v in r.items() if k!='g1_schnitte'})
