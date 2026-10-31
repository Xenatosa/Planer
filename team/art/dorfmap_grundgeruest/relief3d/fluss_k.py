# t63u Runde K [F] (Fabian t62u/Runde K): Strang 13 (Westarm) im Tal um die Huegel herum neu legen.
# Zellen: alter Arm -> Land (Hoehe aus Umland, Untergrund vom naechsten Land), neuer Lauf = Talweg mit monoton fallendem Spiegel.
import numpy as np,scipy.ndimage as nd,heapq
def _dijkstra(Hf,frei,ziel,src,dold,a=40.0,g=0.08):
    NY,NX=Hf.shape;D=np.full(Hf.shape,np.inf);P=-np.ones(Hf.shape+(2,),int);D[src]=0;h=[(0.0,src)];e=None
    while h:
        dd,(y,x)=heapq.heappop(h)
        if dd>D[y,x]:continue
        if ziel[y,x]:e=(y,x);break
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                yy,xx=y+dy,x+dx
                if (dy or dx) and 0<=yy<NY and 0<=xx<NX and (frei[yy,xx] or ziel[yy,xx]):
                    l=np.hypot(dy,dx);c=l*(1+g*dold[yy,xx])+a*max(0.0,Hf[yy,xx]-Hf[y,x])
                    if dd+c<D[yy,xx]:D[yy,xx]=dd+c;P[yy,xx]=(y,x);heapq.heappush(h,(dd+c,(yy,xx)))
    out=[e]
    while P[e][0]>=0:e=tuple(P[e]);out.append(e)
    return np.array(out[::-1],float)
def _kurve(p,amp,wl=36.0,sig=5.0):
    # gleichmaessig 0,5 Zellen, glaetten, sanfte Maeander quer zur Laufrichtung (Enden ohne Versatz)
    s=np.r_[0,np.cumsum(np.hypot(*np.diff(p,axis=0).T))];t=np.arange(0,s[-1],0.5)
    q=np.c_[np.interp(t,s,p[:,0]),np.interp(t,s,p[:,1])];q=nd.gaussian_filter1d(q,sig*2,axis=0,mode='nearest');q[0]=p[0];q[-1]=p[-1]
    d=np.gradient(q,axis=0);d/=np.linalg.norm(d,axis=1,keepdims=True)+1e-9;nrm=np.c_[-d[:,1],d[:,0]]
    taper=np.clip(t/20,0,1)*np.clip((t[-1]-t)/20,0,1)
    return q+nrm*(amp*taper*np.sin(2*np.pi*t/wl))[:,None]
def fluss_k(H,wa,fl,ug,wand,kd,bel,src=(46,72),mund=(260,264),r=2.3,kmin=27):
    NY,NX=H.shape;X=np.arange(NX)[None,:];Y=np.arange(NY)[:,None];H0=H.copy();wa0=wa.copy();st={}
    lab,n=nd.label(wa,np.ones((3,3)));m=lab==lab[mund];west=m&(X<100)&(Y<252)
    # 1) alter Arm -> Land: Hoehe aus Land ohne Wandband (normierte Gaussfuellung), Untergrund vom naechsten Landnachbarn
    land=~wa&~wand;Hf=H.copy();todo=west.copy()
    for s in (1.5,3,6,12):
        num=nd.gaussian_filter(np.where(land,H,0),s);den=nd.gaussian_filter(land.astype(float),s);ok=todo&(den>0.02)
        Hf[ok]=(num/np.maximum(den,1e-9))[ok];todo&=~ok
    _,iL=nd.distance_transform_edt(wa|wand,return_indices=True)
    # 2) Talweg: frei = keine Bauplaetze/Haeuser (+2), kein Wandband (+3), Abstand Kraterwand >= kmin (Kraterfuss-Anhebung _kf)
    dold=nd.distance_transform_edt(~west);ziel=m&(Y>=255)&~west&(X>=40)&(X<=95)
    frei0=~nd.binary_dilation(bel,iterations=1)&~wand
    frei=~nd.binary_dilation(bel,iterations=5)&~nd.binary_dilation(wand,iterations=4)&(kd>=kmin)
    yy,xx=np.ogrid[:NY,:NX];frei|=((yy-src[0])**2+(xx-src[1])**2<=36)&~wand
    p=_dijkstra(Hf,frei,ziel,src,dold);st['talweg_zellen']=len(p)
    ok_=frei0|m&~west
    for amp,sg in ((1.6,5),(0.8,4),(0.0,3),(0.0,1.5),(0.0,0.5)):
        q=_kurve(p,amp,sig=sg);dist,ind=nd.distance_transform_edt(np.ones((NY,NX),bool)&~_rast(q,NY,NX),return_indices=True)
        neu=(dist<=r)&~(m&~west)
        if (neu&~ok_).sum()==0:break
    st['maeander_amplitude_zellen']=amp;st['glaettung_sigma']=sg;st['neu_auf_sperre']=int((neu&~ok_).sum())
    # 3) Spiegel: Talsohle entlang der Kurve, kumulatives Minimum, geglaettet (bleibt monoton fallend)
    hq=nd.map_coordinates(Hf,[q[:,0],q[:,1]],order=1);hl=np.array([Hf[max(0,int(a)-2):int(a)+3,max(0,int(b)-2):int(b)+3].min() for a,b in q])
    W=np.minimum.accumulate(np.minimum(hq,hl+0.0));W=np.minimum(nd.gaussian_filter1d(W,12,mode='nearest'),W);W=np.minimum.accumulate(W)
    alt=m&~west;inn=alt[np.clip(np.round(q[:,0]).astype(int),0,NY-1),np.clip(np.round(q[:,1]).astype(int),0,NX-1)];e=int(np.argmax(inn)) if inn.any() else len(q)-1
    ziel_lev=float(np.median(H[alt&(nd.distance_transform_edt(~_rast(q[e:e+1],NY,NX))<4)]));dE=np.maximum(e-np.arange(len(q)),0)*0.5
    tal=np.flatnonzero(W<=ziel_lev+0.05);e2=int(tal[0]) if len(tal) else e;dE=np.maximum(e2-np.arange(len(q)),0)*0.5;st['talboden_index']=e2
    W=np.minimum(W,ziel_lev+0.15*dE);W=np.maximum(W,ziel_lev);st['muendung_index']=e;st['muendung_spiegel']=round(ziel_lev,2)   # Muendung: Rampe 15 cm/m statt Absturz
    # Kurvenindex je Zelle (naechste Stuetzstelle)
    qi=np.full((NY,NX),-1);qi[np.clip(np.round(q[:,0]).astype(int),0,NY-1),np.clip(np.round(q[:,1]).astype(int),0,NX-1)]=np.arange(len(q))
    K=qi>=0;_,ii=nd.distance_transform_edt(~K,return_indices=True);QI=qi[ii[0],ii[1]]
    Wz=W[QI]
    # 4) schreiben
    Hn=np.where(west,Hf,H);wan=wa&~west;fln=fl.copy();ugn=ug.copy()
    fln[west]='';ugn[west]=ug[iL[0],iL[1]][west]
    _,iO=nd.distance_transform_edt(~west,return_indices=True)
    Hn[neu]=Wz[neu];wan[neu]=True;fln[neu]=fl[iO[0],iO[1]][neu];ugn[neu]='WASSER_EIS'
    # Ufer nicht tiefer als Spiegel+0,3 (Wasser darf nicht seitlich auslaufen): Damm bis 2 Zellen
    du,iu=nd.distance_transform_edt(~neu,return_indices=True);Wu=Hn[iu[0],iu[1]]
    damm=(~wan)&(du<=2.5)&(Hn<Wu+0.05)&~wand;st['ufer_angehoben_zellen']=int(damm.sum());st['ufer_angehoben_max_m']=round(float((Wu+0.05-Hn)[damm].max()) if damm.any() else 0,2)
    Hn[damm]=(Wu+0.05)[damm]
    # Vorlage-Index fuer uebrige Quellspalten: neues Wasser <- naechste alte Armzelle, neues Land <- naechste Landzelle
    VY,VX=np.mgrid[:NY,:NX];alt_land=west&~neu;VY[alt_land]=iL[0][alt_land];VX[alt_land]=iL[1][alt_land];nw=neu&~wa0;VY[nw]=iO[0][nw];VX[nw]=iO[1][nw]
    gr=neu&~west;st['graben_max_m']=round(float((H0-Hn)[neu&~wa0].max()),2);st['graben_ueber_1m_zellen']=int(((H0-Hn)>1.0)[neu&~wa0].sum())
    st.update(alt_arm_zellen=int(west.sum()),alt_zu_land=int(alt_land.sum()),neu_wasser=int(nw.sum()),bleibt_wasser=int((neu&wa0).sum()),
        spiegel_quelle=round(float(W[0]),2),spiegel_muendung=round(float(W[-1]),2),laenge_m=round(len(q)*0.5,1),max_gefaelle_je_m=round(float(-np.diff(W).min()*2),3),
        anstieg_max=round(float(np.diff(W).max()),4))
    return Hn,wan,fln,ugn,VY,VX,neu,west,q,W,st
def _rast(q,NY,NX):
    R=np.zeros((NY,NX),bool);R[np.clip(np.round(q[:,0]).astype(int),0,NY-1),np.clip(np.round(q[:,1]).astype(int),0,NX-1)]=True;return R

def _flut_rand(m,H):
    # priority flood nur vom Kartenrand (sonst tiefster Punkt = Endsee); liefert Reihenfolge, Vorgaenger, Ueberlaufhoehe
    GY,GX=m.shape;P=np.argwhere(m);idx=-np.ones(m.shape,int);idx[m]=np.arange(len(P));n=len(P)
    S=np.full(n,np.inf);pred=-np.ones(n,int);done=np.zeros(n,bool);hv=H[m];h=[]
    edge=np.flatnonzero((P[:,0]==0)|(P[:,1]==0)|(P[:,0]==GY-1)|(P[:,1]==GX-1))
    seeds=[int(edge[np.argmin(hv[edge])])] if len(edge) else [int(np.argmin(hv))]
    for s_ in seeds:S[s_]=hv[s_];heapq.heappush(h,(hv[s_],0.0,s_))
    order=[]
    while h:
        sv,dd,v=heapq.heappop(h)
        if done[v]:continue
        done[v]=True;order.append(v);y,x=P[v]
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                yy,xx=y+dy,x+dx
                if (dy or dx) and 0<=yy<GY and 0<=xx<GX:
                    w=idx[yy,xx]
                    if w>=0 and not done[w]:
                        ns=max(sv,hv[w])
                        if ns<S[w]:S[w]=ns;pred[w]=v;heapq.heappush(h,(ns,dd+np.hypot(dy,dx),w))
    return P,np.array(order),pred,S

# ---- t63u Anzeige: Wasserspiegel je Stueck streng zum Auslass fallend (auch ueber Becken/Wasserscheiden) [A]
# 1) Becken bis Ueberlauf fuellen (Spiegel flach), 2) wo das Ufer tiefer liegt: Spiegel auf Ufer-5cm begrenzen und die Schwelle
#    flussab auf diese Hoehe abtragen (Baum-Durchlauf Blatt->Auslass), 3) quer glaetten + wiederholen, 4) Bett unter Spiegel.
def spiegel_monoton(WV,Gv,VB,tief=0.30,runden=4,sig=1.5):
    WV=WV.astype(float).copy();Gv=Gv.astype(float).copy();M=WV>-900;st={}
    lab,n=nd.label(M,np.ones((3,3)));land=~M
    Gl=np.where(land,Gv,1e4);U=nd.grey_erosion(Gl,size=5)-0.05;U=np.where(U>9e3,1e4,U)     # tiefstes Ufer im Umkreis 1 m
    W0=WV.copy();T=WV.copy()
    for k in range(1,n+1):
        m=lab==k
        if m.sum()<4:continue
        P,o,pred,S=_flut_rand(m,WV)                 # nur Kartenrand / tiefster Punkt als Auslass -> Becken werden gefuellt
        Wk=np.minimum(S,U[m])
        for r in range(runden):
            for v in o[::-1]:                       # Blatt -> Auslass: Eltern nie hoeher als Kind
                p_=pred[v]
                if p_>=0 and Wk[p_]>Wk[v]:Wk[p_]=Wk[v]
            if r<runden-1:
                F=np.zeros(M.shape);F[m]=Wk;num=nd.gaussian_filter(np.where(m,F,0),sig);den=nd.gaussian_filter(m.astype(float),sig)
                Wk=np.minimum((num/np.maximum(den,1e-9))[m],np.minimum(S,U[m]))
        T[m]=Wk
    WV=np.where(M,T,-999.0)
    d=np.where(M,WV-W0,0);st['gefuellt_vertices']=int((d>0.02).sum());st['gefuellt_max_m']=round(float(d.max()),2)
    st['abgesenkt_vertices']=int((d<-0.02).sum());st['abgesenkt_max_m']=round(float(-d.min()),2)
    bett=M&(Gv>WV-tief)&~VB;st['bett_tiefer_vertices']=int(bett.sum());st['bett_tiefer_max_m']=round(float((Gv-(WV-tief))[bett].max()) if bett.any() else 0,2)
    Gv[bett]=(WV-tief)[bett]
    weg=M&VB&(Gv>WV-0.02);WV[weg]=-999;st['am_wandband_entfernt']=int(weg.sum())
    return WV.astype(np.float32),Gv.astype(np.float32),st
