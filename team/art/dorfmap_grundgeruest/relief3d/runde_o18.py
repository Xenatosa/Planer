import os
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

def band_erweitern(FW,G_ANZ,VC,WV,WEGA,belegt,NX,NY,RS,thr=2.0):
    """O18 Teil 2 [F 'Dreiecke in den Boden', Option a]: Feinband spaet auf alle Zellen erweitern, in denen das sichtbare
    Grobnetz steil ist (Steigung>thr, +1 Zelle Rand). Ursache war: BAND schliesst Wassernaehe (dil 1), belegt und erst
    spaeter (Anzeige-Schritte) steil gewordene Zellen aus -> Wandteile im 0,5-m-Netz mit Saegezaehnen.
    Neue Feinpunkte: kubischer Spline aus G_ANZ (glatt, keine Diagonal-Knicke), Farbe aus VC, Tint neutral, Schnee 0
    (wie Bandrand). Nasse Zellen, Wege (WEGA>40) und Gebaeude bleiben grob. Rand wird danach per bandnaht_j1 gepinnt."""
    GY,GX=G_ANZ.shape;FS=FW['fs'];FX,FY=NX*FS+1,NY*FS+1;G=G_ANZ.astype(float)
    B=np.zeros(NX*NY,bool);B[np.frombuffer(base64.b64decode(FW['band']),np.uint32)]=True;B=B.reshape(NY,NX)
    q=np.maximum.reduce([np.abs(G[1:,:-1]-G[:-1,:-1]),np.abs(G[:-1,1:]-G[:-1,:-1]),np.abs(G[1:,1:]-G[1:,:-1]),np.abs(G[1:,1:]-G[:-1,1:]),np.abs(G[1:,1:]-G[:-1,:-1])/1.414,np.abs(G[1:,:-1]-G[:-1,1:])/1.414])*RS
    cq=nd.maximum_filter(q,size=RS,origin=-(RS//2))[::RS,::RS][:NY,:NX]
    wet=nd.maximum_filter((WV>-900).astype(np.uint8),size=RS+1,origin=-(RS//2))[::RS,::RS][:NY,:NX]>0
    weg=nd.maximum_filter((WEGA.reshape(GY,GX)>40).astype(np.uint8),size=RS+1,origin=-(RS//2))[::RS,::RS][:NY,:NX]>0
    S=(cq>thr)&~B;S=nd.binary_dilation(S,iterations=1)&~B&~weg&~belegt
    # O18d [F C2 Zahnkante]: konvexe Grate/Kuppen direkt am Bandrand -> Naht (0,25/0,5-m-Stich) lag auf dem Grat = Zaehne. Kuppe ganz ins Band.
    cv=(G-nd.gaussian_filter(G,3.0));cvc=nd.maximum_filter(cv,size=RS,origin=-(RS//2))[::RS,::RS][:NY,:NX]
    # O18d A1: Lippe (Plateau->Wand) mit Treppen-Bandrand; C2-Kegel ist belegt (Platz E40) -> blieb grob = Zahnkante
    S2=(cvc>0.10)&nd.binary_dilation(B|S,iterations=3)&~B;S2=nd.binary_dilation(S2,iterations=3)&~B&~weg;S=S|S2|((cq>thr)&belegt&~B&~weg)
    if os.environ.get('BDBG'):print('BDBG',[(int(cq[y,x]*10),int(cvc[y,x]*100),int(weg[y,x]),int(belegt[y,x]),int(B[y,x])) for y,x in((28,20),(29,20),(29,24),(30,24))])   # O18b: auch nasse Schluchtzellen (Bett unter Spiegel geklemmt)
    if not S.any():return {'zellen':0}
    B2=B|S
    # Feinpunkte aller Bandzellen
    cy,cx=np.nonzero(B2);u=np.zeros((FY,FX),bool)
    for a in range(FS+1):
        for b in range(FS+1):u[cy*FS+a,cx*FS+b]=True
    vid_alt=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);vid=np.flatnonzero(u.ravel()).astype(np.uint32)
    neu=~np.isin(vid,vid_alt);pos=np.searchsorted(vid_alt,vid[~neu])
    fy=vid//FX;fx=vid%FX;gy=fy/FS*RS;gx=fx/FS*RS
    hs=nd.map_coordinates(nd.spline_filter(G,order=3),[gy[neu],gx[neu]],order=3,prefilter=False,mode='nearest')
    hl=nd.map_coordinates(G,[gy[neu],gx[neu]],order=1)
    hs=np.clip(hs,hl-0.6,hl+0.6)   # kein Ueberschwingen
    Wn=np.where(WV>-900,WV,np.nan).astype(float);wi=[gy[neu],gx[neu]];wl=nd.map_coordinates(np.nan_to_num(Wn,nan=-999),wi,order=1);wok=nd.map_coordinates((WV>-900).astype(float),wi,order=1)>0.99
    hs=np.where(wok,np.minimum(hs,wl-0.08),hs)
    def mix(key,dt,k,fill):
        a=np.frombuffer(base64.b64decode(FW[key]),dt).reshape(len(vid_alt),*( (k,) if k>1 else ()))
        o=np.zeros((len(vid),)+a.shape[1:],dt);o[~neu]=a[pos];o[neu]=fill;return o
    h=mix('h',np.float32,1,0);h[neu]=hs
    V=VC.reshape(GY,GX,3).astype(float);vc=np.stack([nd.map_coordinates(V[...,k],[gy[neu],gx[neu]],order=1) for k in range(3)],1)
    c=mix('c',np.uint8,3,0);c[neu]=np.clip(np.round(vc),0,255)
    t=mix('t',np.uint8,3,128);s=mix('s',np.uint8,1,0)
    FW['vid']=base64.b64encode(vid.tobytes()).decode();FW['h']=base64.b64encode(h.astype(np.float32).tobytes()).decode()
    FW['c']=base64.b64encode(c.tobytes()).decode();FW['t']=base64.b64encode(t.tobytes()).decode();FW['s']=base64.b64encode(s.tobytes()).decode()
    FW['band']=base64.b64encode(np.flatnonzero(B2.ravel()).astype(np.uint32).tobytes()).decode()
    return {'zellen':int(S.sum()),'punkte_neu':int(neu.sum()),'B':B2,'vid':vid}

def naht_weich(FW,G_ANZ,BAND,NX,NY,RS,L=1.25):
    """O18 [F Zacken am Bandrand]: bandnaht_j1 pinnt die Randpunkte auf G_ANZ (Sprung bis 2,6 m), das Innere blieb ->
    Stufe/Zacke eine Feinreihe hinter dem Rand. Hier: Randversatz weich ins Innere tragen (Gewicht 1 am Rand -> 0 nach L m),
    Versatz als normierte Gauss-Interpolation der Randwerte. Randpunkte = exakt G_ANZ (kein Spalt)."""
    FS=FW['fs'];FX,FY=NX*FS+1,NY*FS+1;GY,GX=G_ANZ.shape
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fy=vid//FX;fx=vid%FX
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float).copy()
    BP=np.pad(BAND,1,constant_values=False)
    def bc(yy,xx):return BP[np.clip(yy,-1,NY)+1,np.clip(xx,-1,NX)+1]
    ya=(fy-(fy%FS==0))//FS;yb=fy//FS;xa=(fx-(fx%FS==0))//FS;xb=fx//FS
    ya=np.where(fy%FS==0,(fy-1)//FS,fy//FS);xa=np.where(fx%FS==0,(fx-1)//FS,fx//FS)
    rand=~(bc(ya,xa)&bc(ya,xb)&bc(yb,xa)&bc(yb,xb))
    gi=nd.map_coordinates(G_ANZ.astype(float),[fy/FS*RS,fx/FS*RS],order=1,mode='nearest')
    d=gi-h
    D=np.zeros((FY,FX));W=np.zeros((FY,FX));D[fy[rand],fx[rand]]=d[rand];W[fy[rand],fx[rand]]=1
    sg=L*FS/2;Dg=nd.gaussian_filter(D,sg);Wg=nd.gaussian_filter(W,sg)
    M=np.ones((FY,FX),bool);M[fy[rand],fx[rand]]=False;dist=nd.distance_transform_edt(M)/FS
    w=np.clip(1-dist/L,0,1);w=w*w*(3-2*w)
    corr=np.where(Wg>1e-4,Dg/np.maximum(Wg,1e-4),0)*w
    h2=h+corr[fy,fx];h2[rand]=gi[rand]
    FW['h']=base64.b64encode(h2.astype(np.float32).tobytes()).decode()
    return {'randpunkte':int(rand.sum()),'max_versatz_m':round(float(np.abs(d[rand]).max()),2),'innen_geaendert':int((np.abs(corr[fy,fx])>0.01).sum())}

def fein_glatt(FW,BAND,NX,NY,thr=0.35,it=8):
    """O18 [F Zacken/Kerben im Feinband, Gipfel rund]: Knicke/Kerben/Spitzen im Feinband (|Laplace 4-Nachbarn|>thr m bei 0,25 m)
    iterativ zum Gauss-Mittel ziehen (weich gewichtet). Randpunkte und Punkte ohne volle Nachbarschaft bleiben fest."""
    FS=FW['fs'];FX,FY=NX*FS+1,NY*FS+1
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
    F=np.full((FY,FX),np.nan);F.ravel()[vid]=h;ok=~np.isnan(F)
    BP=np.repeat(np.repeat(BAND,FS,0),FS,1);inn=np.zeros((FY,FX),bool);inn[:-1,:-1]=BP
    inn=nd.binary_erosion(ok&nd.binary_erosion(np.pad(inn,0)|False,iterations=0) if False else ok,iterations=2)
    Fz=np.where(ok,F,0.0);n=0
    for _ in range(it):
        lap=np.zeros_like(Fz);lap[1:-1,1:-1]=(Fz[:-2,1:-1]+Fz[2:,1:-1]+Fz[1:-1,:-2]+Fz[1:-1,2:])/4-Fz[1:-1,1:-1]
        w=np.clip((np.abs(lap)-thr)/thr,0,1);w=np.maximum(w,nd.maximum_filter(w,3)*0.5)*inn
        if w.max()==0:break
        n=max(n,int((w>0).sum()))
        Wk=nd.gaussian_filter(ok.astype(float),1.0);Gs=nd.gaussian_filter(Fz,1.0)/np.maximum(Wk,1e-6)
        Fz=np.where(inn,Fz*(1-w)+Gs*w,Fz)
    h2=Fz.ravel()[vid];FW['h']=base64.b64encode(h2.astype(np.float32).tobytes()).decode()
    return {'punkte':n,'max_m':round(float(np.abs(h2-h).max()),2)}

def kaskade_glatt(G_ANZ,WV,RS,sig=1.0):
    """O18 [F F6 Restzacken]: Steile Bachkaskaden (F6/G7/E7) – Bett und Spiegel stufig je Ecke. Nur nasse Ecken mit Gefaelle>1:
    Bett und Spiegel per normierter Gauss-Mittelung ueber nasse Ecken glaetten; Bett bleibt >=0,1 m unter Spiegel."""
    w=(WV>-900);G=G_ANZ.astype(float);V=np.where(w,WV,0.0).astype(float)
    gy,gx=np.gradient(np.where(w,V,np.nan));s=np.nan_to_num(np.hypot(gx,gy))*RS
    m=w&(nd.maximum_filter(s,3)>1.0)
    if not m.any():return G_ANZ,WV,{'ecken':0}
    W=nd.gaussian_filter(w.astype(float),sig)+1e-9
    Gs=nd.gaussian_filter(np.where(w,G,0),sig)/W;Vs=nd.gaussian_filter(V,sig)/W
    V2=np.where(m,Vs,WV);G2=np.where(m,np.minimum(Gs,V2-0.1),G)
    return G2.astype(G_ANZ.dtype),V2.astype(WV.dtype),{'ecken':int(m.sum()),'max_m':round(float(np.abs(G2-G).max()),2)}

def gipfel_rund(G_ANZ,WV,WEGA,belegt,RS,sig=2.5,thr=0.12,it=10,cap=3.0):   # O18d: staerker (G1-Pyramide blieb)
    """O18c [F G1-Block, C2-Kegel, Gipfelrundung]: konvexe Spitzen/Grate (Gauss-Mittel liegt >thr m unter dem Punkt)
    weich absenken (nur absenken, nie anheben). Wasser, Wege, belegte Zellen ausgenommen. Deterministisch."""
    G=G_ANZ.astype(float);fest=(WV>-900)|(WEGA>0)
    if belegt is not None:
        b=np.asarray(belegt)
        if b.shape!=G.shape:
            b=np.kron(b,np.ones((RS,RS),bool))[:G.shape[0],:G.shape[1]]
            if b.shape!=G.shape:b=np.pad(b,((0,G.shape[0]-b.shape[0]),(0,G.shape[1]-b.shape[1])))
        fest=fest|b
    fest=nd.binary_dilation(fest,iterations=1);tap=np.clip((nd.distance_transform_edt(~fest)-1)/5.0,0,1);n=0;G0=G.copy()   # O18d: weich auslaufen statt harter Kante
    for _ in range(it):
        Gs=nd.gaussian_filter(G,sig);k=G-Gs
        w=np.clip((k-thr)/thr,0,1)*tap
        w=nd.gaussian_filter(w,1.0)*tap
        n=max(n,int((w>0.05).sum()));G=np.maximum(np.minimum(G,G*(1-w)+Gs*w),G0-cap)
    return G.astype(G_ANZ.dtype),{'ecken':n,'max_m':round(float((G0-G).max()),2)}

def fein_gipfel(FW,BAND,NX,NY,sig=4.0,thr=0.08,it=10,cap=3.0):   # O18d: staerker
    """O18c [F Gipfelrundung im Feinband]: wie gipfel_rund, im Feinraster; Bandrand (2 Punkte) fest."""
    FS=FW['fs'];FX,FY=NX*FS+1,NY*FS+1
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
    F=np.full((FY,FX),np.nan);F.ravel()[vid]=h;ok=~np.isnan(F);inn=nd.binary_erosion(ok,iterations=2);tap=np.clip((nd.distance_transform_edt(ok)-2)/10.0,0,1)   # O18d: Rand weich, sonst Stufe am Bandrand
    Fz=np.where(ok,F,0.0);Wk=None;n=0
    for _ in range(it):
        Wk=nd.gaussian_filter(ok.astype(float),sig);Gs=nd.gaussian_filter(Fz,sig)/np.maximum(Wk,1e-6)
        w=np.clip((Fz-Gs-thr)/thr,0,1)*tap;w=nd.gaussian_filter(w,1.0)*tap
        n=max(n,int((w>0.05).sum()));Fz=np.where(inn,np.maximum(np.minimum(Fz,Fz*(1-w)+Gs*w),np.where(ok,F,0.0)-cap),Fz)
    h2=Fz.ravel()[vid];FW['h']=base64.b64encode(h2.astype(np.float32).tobytes()).decode()
    return {'punkte':n,'max_m':round(float((h-h2).max()),2)}

def farbe_weich(VC,FW,RS,NX,NY,box=(0,0,24,45),sig=5.0):
    """O18d [F A1 braune Flaeche, harte Kante]: Quellkarte hat in A1 am Kartenrand einen geraden FELS-Streifen (x<15) mit
    senkrechter Kante zu SCHNEE. Nur Anzeige-Farbe: in der Box Farbsprung > 40 (0..255) per Gauss weich machen, Gewicht
    laeuft zum Boxrand aus. Grob-VC und Feinband-Farbe gleich behandelt. Deterministisch."""
    GY,GX=NY*RS+1,NX*RS+1;V=VC.reshape(GY,GX,3).astype(float)
    x0,y0,x1,y1=[v*RS for v in box];L=V.mean(2)
    gm=np.hypot(nd.sobel(L,0),nd.sobel(L,1))/8;e=(gm>6).astype(float);e[:, :]*=0;e[y0:y1,x0:x1]=(gm[y0:y1,x0:x1]>6)
    w=np.clip(nd.gaussian_filter(nd.binary_dilation(e>0,iterations=int(sig*1.5)).astype(float),sig/2)*1.5,0,1)
    Vs=np.stack([nd.gaussian_filter(V[...,k],sig) for k in range(3)],2)
    V2=V*(1-w[...,None])+Vs*w[...,None];VC[:]=np.clip(np.round(V2),0,255).astype(VC.dtype).reshape(VC.shape)
    FS=FW['fs'];FX=NX*FS+1;vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);c=np.frombuffer(base64.b64decode(FW['c']),np.uint8).reshape(-1,3).astype(float).copy()
    gy=(vid//FX)/FS*RS;gx=(vid%FX)/FS*RS;wf=nd.map_coordinates(w,[gy,gx],order=1);k=wf>0.01
    if k.any():
        cs=np.stack([nd.map_coordinates(Vs[...,j],[gy[k],gx[k]],order=1) for j in range(3)],1);c[k]=c[k]*(1-wf[k,None])+cs*wf[k,None]
        FW['c']=base64.b64encode(np.clip(np.round(c),0,255).astype(np.uint8).tobytes()).decode()
    return {'punkte':int((w>0.05).sum()),'fein':int(k.sum())}
