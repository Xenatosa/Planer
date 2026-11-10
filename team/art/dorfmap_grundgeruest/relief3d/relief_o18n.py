import numpy as np,scipy.ndimage as nd
def g5_beulen(G,RS,WAND,thr=0.6):
    """O18m/n: echte Klippenbeule = Kantenpunkt hoeher als das Plateau 2-5 m landeinwaerts (senkrecht zur Wand). Runde, abfallende Kante zaehlt nicht."""
    dist=nd.distance_transform_edt(~WAND)/RS;dy,dx=np.gradient(nd.gaussian_filter(dist,RS));n=np.hypot(dx,dy)+1e-9;dx,dy=dx/n,dy/n
    OBEN=(dist>0)&(dist<=3)&(G>nd.grey_dilation(G,size=7*RS)-1.0);yy,xx=np.nonzero(OBEN)
    ref=np.full(len(yy),-1e9)
    for s in (2,3,4,5):ref=np.maximum(ref,nd.map_coordinates(G,[yy+dy[yy,xx]*s*RS,xx+dx[yy,xx]*s*RS],order=1,mode='nearest'))
    bb=np.zeros_like(G);bb[yy,xx]=G[yy,xx]-ref;return bb*(bb>thr),OBEN

def landschaft_final(GA,WV,WEGA,RS,frei_extra=None,it=3,rampen=None):
    """O18n (t112u, Regelwerk 1-3): kartenweiter Endschliff am Anzeige-Grobnetz. Nur ausserhalb Wand (+1 m), Wegband (+3.5 m), Wasser (+2 m), Hausplaetzen.
    G5 Klippenbeulen absenken, R5 Senken >0.8 m auffuellen, G2/G3 Einzelspitzen auf Nachbarmittel, G6 Facetten weich. Gibt (GA, stats) zurueck."""
    from skimage.morphology import reconstruction
    sh=GA.shape;G=np.asarray(GA,float).reshape(WV.shape).copy();LAND=WV<=-900
    gy,gx=np.gradient(G,1/RS);WAND=np.hypot(gx,gy)>1.0
    fest=nd.binary_dilation(WAND,iterations=RS)|nd.binary_dilation(WEGA>20,iterations=int(3.5*RS))|nd.binary_dilation(~LAND,iterations=2*RS)
    if frei_extra is not None:fest|=frei_extra
    if rampen:
        RM=np.zeros_like(fest)
        for r in rampen:
            r=np.asarray(r,float);L=np.r_[0,np.cumsum(np.hypot(*np.diff(r,axis=0).T))];t=np.arange(0,L[-1]+1e-6,0.25)
            xs=np.interp(t,L,r[:,0])*RS;zs=np.interp(t,L,r[:,1])*RS;RM[np.clip(zs.astype(int),0,RM.shape[0]-1),np.clip(xs.astype(int),0,RM.shape[1]-1)]=True
        fest|=nd.binary_dilation(RM,iterations=int(4*RS))
    fest_g5=WAND|nd.binary_dilation(WEGA>20,iterations=int(3.5*RS))|nd.binary_dilation(~LAND,iterations=2*RS)|(nd.binary_dilation(RM,iterations=int(4*RS)) if rampen else False)|(frei_extra if frei_extra is not None else False)
    frei=~fest;st={'g5':0,'r5':0,'spitze':0,'g6':0}
    for _ in range(it):
        gy,gx=np.gradient(G,1/RS);W2=np.hypot(gx,gy)>1.0
        bb,_o=g5_beulen(G,RS,W2,0.6);m=(bb>0)&~fest_g5&~W2&False;   # O18n: Absenken wirkungslos (3 Versuche, G5 176->177), aus; Klippenbeulen offen
        st['g5']+=int(m.sum())
        if m.any():
            low=np.where(m,bb-0.3,0);low=nd.grey_dilation(low,size=3);low=nd.gaussian_filter(low,1)*~fest_g5*~W2;G-=np.clip(low,0,None)
        nb=(nd.uniform_filter(G,3)*9-G)/8;d=G-nd.grey_opening(G,size=(3,3));m=((np.abs(G-nb)>0.35)|(d>0.4))&frei&nd.binary_erosion(frei,iterations=RS);st['spitze']+=int(m.sum())
        G=np.where(m,nb+np.clip(G-nb,-0.2,0.2),G)
        gy,gx=np.gradient(G,1/RS);S=np.hypot(gx,gy);n=np.stack([-gx,-gy,np.ones_like(G)]);n/=np.linalg.norm(n,axis=0)
        dn=np.zeros_like(G);dn[:,:-1]=np.maximum(dn[:,:-1],sum(np.abs(np.diff(n[i],axis=1)) for i in range(3)));dn[:-1,:]=np.maximum(dn[:-1,:],sum(np.abs(np.diff(n[i],axis=0)) for i in range(3)))
        m=(dn>0.2)&(S>0.12)&(S<0.85)&frei;st['g6']+=int(m.sum())
        if m.any():
            w=np.clip(nd.gaussian_filter(nd.binary_dilation(m,iterations=2)*1.0,1),0,1)*frei;G=G*(1-w)+w*nd.gaussian_filter(G,1.5)
    # keine neue Wand erzeugen
    gy,gx=np.gradient(G,1/RS);neu=(np.hypot(gx,gy)>1.0)&~WAND
    if neu.any():
        r=neu;G=np.where(r,np.asarray(GA,float).reshape(WV.shape),G)
    st['neue_wand_zurueck']=int(neu.sum())
    for _ in range(2):
        seed=G.copy();seed[1:-1,1:-1]=G.max();fill=reconstruction(seed,G,method='erosion');t=(fill-G)*LAND
        m=(t>0.8)&~WAND&~nd.binary_dilation(~LAND,iterations=2*RS);st['r5']+=int(m.sum())
        lift=np.where(m,t-0.5,0);lift=np.maximum(lift,nd.gaussian_filter(lift,1)*(t>0.3));G=G+np.minimum(lift,np.maximum(t-0.3,0))
    return G.astype(np.asarray(GA).dtype).reshape(sh),st
