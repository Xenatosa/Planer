# Runde O18 [F t83u D1/G1, t85u H1, t86u A2, t87u C2] -- NUR Anzeige (G_ANZ, VC, WV, Feinband FW). G, CSV-Zellwerte (ausser Anzeige-Spalten), Zufallsfolgen unberuehrt.
# 1) Wasser ohne Fluss (fluss_id WASSER_FARBE-Komponenten ohne benannten Fluss) raus, Bett harmonisch auf Umgebung gefuellt, Farbe aus Umgebung.
# 2) Geschlossene Senken (Mulden nach innen) <= 3,5 m tief, <= 2500 Ecken gefuellt (Krater/Becken bleiben), weich eingeblendet.
# 3) Spitzen/Grate oben und Zacken nach unten gerundet (Grob + Feinband), ohne Wege/Rampen/Wasser.
import numpy as np,scipy.ndimage as nd,base64
from skimage.morphology import reconstruction
def _harm(a,M,it=3000):
    ys,xs=np.nonzero(M)
    if len(ys)==0:return a
    y0,y1,x0,x1=max(0,ys.min()-2),ys.max()+3,max(0,xs.min()-2),xs.max()+3
    s=a[y0:y1,x0:x1];m=M[y0:y1,x0:x1];s[m]=np.mean(s[~m])
    for _ in range(it):s[m]=0.25*(np.roll(s,1,0)+np.roll(s,-1,0)+np.roll(s,1,1)+np.roll(s,-1,1))[m]
    return a
def wasser_raus(G_ANZ,VC,WV,fl,wa,RS):
    GY,GX=G_ANZ.shape;benannt=wa&(fl!='WASSER_FARBE')&(fl!='')
    L,n=nd.label(wa);weg=np.zeros_like(wa);komp=[]
    for i,sl in enumerate(nd.find_objects(L),1):
        m=L==i
        if not (benannt&m).any():
            weg|=m;ys,xs=np.nonzero(m);komp.append(dict(n=int(m.sum()),x=[int(xs.min()),int(xs.max())],y=[int(ys.min()),int(ys.max())]))
    vm=nd.map_coordinates(np.kron(nd.binary_dilation(weg,iterations=2),np.ones((RS,RS))).astype(float),[np.mgrid[0:GY,0:GX][0]-0.5,np.mgrid[0:GY,0:GX][1]-0.5],order=0,mode='nearest')>0.5
    vb=nd.map_coordinates(np.kron(nd.binary_dilation(benannt,iterations=3),np.ones((RS,RS))).astype(float),[np.mgrid[0:GY,0:GX][0]-0.5,np.mgrid[0:GY,0:GX][1]-0.5],order=0,mode='nearest')>0.5
    vm&=~vb;nw=int(((WV>-900)&vm).sum());WV=np.where(vm,np.float32(-999),WV).astype(WV.dtype)
    M=nd.binary_dilation(vm,iterations=2)&~vb
    g=G_ANZ.astype(float);gn=_harm(g.copy(),M);w=nd.gaussian_filter(M.astype(float),1.5);w[M]=1
    C=VC.reshape(GY,GX,3).astype(float);Cn=C.copy()
    for k in range(3):Cn[...,k]=C[...,k]*(1-w)+_harm(C[...,k].copy(),nd.binary_dilation(M,iterations=1))*w
    G2=g*(1-w)+gn*w
    return G2.astype(G_ANZ.dtype),np.clip(np.round(Cn),0,255).astype(np.uint8).reshape(VC.shape),WV,w,{'flaechen':len(komp),'zellen':int(weg.sum()),'wasserecken_raus':nw,'liste':komp,'auftrag_max_m':round(float((G2-g).max()),2)}
def _senken(F,nass,TMAX=3.5,NMAX=2500):
    seed=F.copy();seed[1:-1,1:-1]=F.max();seed[nass]=F[nass]
    T=reconstruction(seed,F,method='erosion')-F;L,n=nd.label(T>0.02);keep=np.zeros(n+1,bool)
    if n:
        mx=nd.maximum(T,L,np.arange(1,n+1));sz=nd.sum(np.ones_like(T),L,np.arange(1,n+1));keep[1:]=(mx<=TMAX)&(sz<=NMAX)
    M=keep[L];return np.where(M,T,0),M,int(keep.sum())
def _runden(F,frei,sig,amp):
    """Spitzen oben und Zacken unten zum Gauss-Mittel ziehen, nur wo |F-gauss|>amp (Extremstellen), weich"""
    g=nd.gaussian_filter(F,sig);d=F-g;k=np.clip((np.abs(d)-amp)/amp,0,1);k=k*k*(3-2*k)*frei
    return F-d*k*0.8,int((k>0.05).sum())
def gelaende(G_ANZ,WV,WEGA,RS):
    GY,GX=G_ANZ.shape;nass=WV>-900;F=G_ANZ.astype(float)
    T,M,n=_senken(F,nass);F2=F+T
    w=nd.gaussian_filter(nd.binary_dilation(M,iterations=2).astype(float),1.0)
    F2=F2*(1-w)+nd.gaussian_filter(F2,1.0)*w   # gefuellte Boeden nicht tellerflach, Rand weich
    F2=np.maximum(F2,F)   # nur auffuellen
    weg=(WEGA.reshape(GY,GX)>40);frei=(~nd.binary_dilation(nass|weg,iterations=3)).astype(float)
    F3,nr=_runden(F2,frei,1.2,0.35)
    return F3.astype(G_ANZ.dtype),{'senken_gefuellt':n,'senk_ecken':int(M.sum()),'auftrag_max_m':round(float(T.max()),2),'gerundet_ecken':nr,'rund_max_m':round(float(np.abs(F3-F2).max()),2)}
def feinband(FW,G_ANZ,WV,WEGA,NX,NY,RS):
    FS=FW['fs'];FX,FY=NX*FS+1,NY*FS+1;vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
    fy,fx=np.mgrid[0:FY,0:FX].astype(float);GA=G_ANZ.astype(float)
    F=nd.map_coordinates(GA,[fy/FS*RS,fx/FS*RS],order=1);F.ravel()[vid]=h
    inb=np.zeros(FX*FY,bool);inb[vid]=True;inb=inb.reshape(FY,FX)
    nass=nd.map_coordinates((WV>-900).astype(float),[fy/FS*RS,fx/FS*RS],order=0)>0.5
    weg=nd.map_coordinates((WEGA.reshape(G_ANZ.shape)>40).astype(float),[fy/FS*RS,fx/FS*RS],order=0)>0.5
    rand=inb&~nd.binary_erosion(inb,iterations=2)
    T,M,n=_senken(F,nass);F2=F+T*inb
    frei=(inb&~rand&~nd.binary_dilation(nass|weg,iterations=FS*2)).astype(float)
    F3,nr=_runden(F2,frei,1.6,0.25)
    F3,nr2=_runden(F3,frei,0.8,0.15)
    hn=F3.ravel()[vid];d=hn-h
    FW['h']=base64.b64encode(hn.astype(np.float32).tobytes()).decode()
    return {'senken_gefuellt':n,'auftrag_max_m':round(float(T[inb].max()),2),'gerundet':nr+nr2,'aenderung_max_m':round(float(np.abs(d).max()),2),'ecken_geaendert':int((np.abs(d)>0.01).sum())}
def fluss_tiefer(G_ANZ,WV,WEGA,bruecken,FW,NX,NY,RS,D=0.6,B=3.0):
    """O18 [F t88u B2]: Fluesse/Baeche waren nur 0,14-0,22 m tief, Ufer 0,4 m ueber Spiegel (wirkte wie flacher Fleck).
    Gesamtes Anzeige-Wasser um D tiefer (Spiegel gleichmaessig -> Gefaelle/Monotonie bleibt), Bett zusaetzlich zur Mitte bis 0,5 m,
    Boeschung an Land weich auf B m. Wege/Rampen und Bruecken-Enden (4 m) ausgenommen (weich). Feinband folgt derselben Absenkung."""
    GY,GX=G_ANZ.shape;nass=WV>-900;vj,vi=np.mgrid[0:GY,0:GX]/RS
    dL=nd.distance_transform_edt(~nass)/RS;dW=nd.distance_transform_edt(nass)/RS
    schutz=(WEGA.reshape(GY,GX)>40).astype(float)
    for b in bruecken:schutz=np.maximum(schutz,(np.hypot(vi-b[0],vj-b[2])<4).astype(float))
    schutz=np.clip(nd.gaussian_filter(schutz,1.5)*1.5,0,1)
    s=np.clip(1-dL/B,0,1);s=s*s*(3-2*s)
    delta=np.where(nass,-(D+np.minimum(0.5,0.25*dW)),-D*s*(1-schutz))
    delta=np.where(nass,delta,nd.gaussian_filter(delta,0.7)*(~nass)) if False else delta
    G2=G_ANZ.astype(float)+delta;WV2=np.where(nass,WV-D,WV)
    FS=FW['fs'];FX=NX*FS+1;vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fy=vid//FX;fx=vid%FX
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)+nd.map_coordinates(delta,[fy/FS*RS,fx/FS*RS],order=1)
    FW['h']=base64.b64encode(h.astype(np.float32).tobytes()).decode()
    return G2.astype(G_ANZ.dtype),WV2.astype(WV.dtype),{'D_m':D,'boeschung_m':B,'wasserecken':int(nass.sum()),'landecken_abgesenkt':int(((delta<-0.01)&~nass).sum()),'bett_max_m':round(float(-delta.min()),2)}
