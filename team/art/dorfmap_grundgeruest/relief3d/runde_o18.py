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
    # Versuch 2: Wege nicht mehr hart ausgenommen (gab 0,6-m-Stufe am Ufer, B2-Bild n2). Nur Bruecken: weicher Uebergang
    # 4..10 m, gilt fuer Wasser UND Land (Spiegel, Bett, Boeschung zusammen) -> keine Kante.
    db=np.full((GY,GX),1e9)
    for b in bruecken:db=np.minimum(db,np.hypot(vi-b[0],vj-b[2]))
    t=np.clip((db-4)/6,0,1);frei=t*t*(3-2*t)
    s=np.clip(1-dL/B,0,1);s=s*s*(3-2*s)
    delta=np.where(nass,-(D+np.minimum(0.5,0.25*dW)),-D*s)*frei
    G2=G_ANZ.astype(float)+delta;WV2=np.where(nass,WV-D*frei,WV)
    FS=FW['fs'];FX=NX*FS+1;vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fy=vid//FX;fx=vid%FX
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)+nd.map_coordinates(delta,[fy/FS*RS,fx/FS*RS],order=1)
    FW['h']=base64.b64encode(h.astype(np.float32).tobytes()).decode()
    return G2.astype(G_ANZ.dtype),WV2.astype(WV.dtype),{'D_m':D,'boeschung_m':B,'wasserecken':int(nass.sum()),'landecken_abgesenkt':int(((delta<-0.01)&~nass).sum()),'bett_max_m':round(float(-delta.min()),2)}

def _zmaske(F,thr):
    P=np.pad(F,1,mode='edge');c=P[1:-1,1:-1]
    dd=np.array([P[1:-1,2:]+P[1:-1,:-2]-2*c,P[2:,1:-1]+P[:-2,1:-1]-2*c,(P[2:,2:]+P[:-2,:-2]-2*c)/2,(P[2:,:-2]+P[:-2,2:]-2*c)/2])
    return (dd.min(0)>thr)|(dd.max(0)<-thr)

def entstacheln(G_ANZ,FW,NX,NY,RS,thr=0.25,it=6):
    """O18 [F A1 B1 C1 E1 F1 C2 'Dreiecke in den Boden', 'Spitzen']: Einzelpunkt-Ausreisser = in ALLEN 4 Richtungen gleich
    gekruemmt (Nadel/Loch, kein Hang/Wandfuss). Ersatz durch 3x3-Median, iterativ. Grobnetz komplett, Feinband nur
    Innenpunkte (alle 8 Nachbarn im Band) -> Bandnaht bleibt deckungsgleich. Deterministisch."""
    G=G_ANZ.astype(float);ng=0
    for _ in range(it):
        M=_zmaske(G,thr)
        if not M.any():break
        ng+=int(M.sum());G=np.where(M,nd.median_filter(G,3,mode='nearest'),G)
    FS=FW['fs'];FX,FY=NX*FS+1,NY*FS+1
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
    m=np.zeros(FX*FY,bool);m[vid]=True;m=m.reshape(FY,FX)
    inn=nd.binary_erosion(m,np.ones((3,3)),border_value=0)
    F=np.zeros(FX*FY);F[vid]=h;F=F.reshape(FY,FX);nf=0
    for _ in range(it):
        M=_zmaske(F,thr)&inn
        if not M.any():break
        nf+=int(M.sum());F=np.where(M,nd.median_filter(F,3,mode='nearest'),F)
    FW['h']=base64.b64encode(F.ravel()[vid].astype(np.float32).tobytes()).decode()
    return G.astype(G_ANZ.dtype),{'grob_ersetzt':ng,'fein_ersetzt':nf,'thr_m':thr}

def grob_wand_glatt(G_ANZ,FW,WV,WEGA,NX,NY,RS,it=3):
    """O18 [F A1 B1 E1 D1 H1 F1 'Dreiecke in den Boden']: Ursache = Wandteile ausserhalb des Feinbands (Band endet mitten
    in der Wand, darunter 0,5-m-Grobnetz mit Steigung >1,5..6). Dessen Hoehenrauschen + Diagonal-Triangulierung gibt
    Saegezaehne am Wandfuss. Fix: sichtbare steile Grobecken (Steigung>1,2) zum Gauss-Mittel (sig 1 Ecke = 0,5 m) ziehen,
    weich gewichtet, 3 Durchgaenge; Wasser/Wege ausgenommen. Bandrand folgt spaeter per bandnaht_j1 (deckungsgleich)."""
    GY,GX=G_ANZ.shape;G=G_ANZ.astype(float)
    B=np.zeros(NX*NY,bool);B[np.frombuffer(base64.b64decode(FW['band']),np.uint32)]=True;B=B.reshape(NY,NX)
    Bp=np.pad(B,1,constant_values=True);gj,gi=np.mgrid[0:GY,0:GX]//RS
    sicht=~(Bp[gj,gi]&Bp[gj+1,gi]&Bp[gj,gi+1]&Bp[gj+1,gi+1])
    fest=nd.binary_dilation((WV>-900)|(WEGA.reshape(GY,GX)>40),iterations=2)
    n=0
    for _ in range(it):
        gy,gx=np.gradient(G);s=np.hypot(gx,gy)*RS
        w=np.clip((s-1.2)/1.0,0,1)*sicht*(~fest);w=nd.gaussian_filter(w,0.7)*(~fest)
        n=max(n,int((w>0.05).sum()))
        G=G*(1-0.8*w)+nd.gaussian_filter(G,1.0)*0.8*w
    return G.astype(G_ANZ.dtype),{'ecken':n,'max_aenderung_m':round(float(np.abs(G-G_ANZ).max()),2)}
