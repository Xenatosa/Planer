# t62u Runde J: Ufer sanft, Bett gleichmaessig tief, Kleinstuecke weg - nur Anzeige (GB/WV), Zellen bleiben [A]
import numpy as np,scipy.ndimage as nd
def ufer_glaetten(WV,G,Gv,VB,klein=20,tmin=0.35,tmax=1.2,breite=8,stufe=0.31,maxschnitt=1.5):
    import os
    WV=WV.copy();Gv=Gv.astype(float).copy();G=G.astype(float);st={}
    n0=int(nd.label(WV>-900,np.ones((3,3)))[1])
    M=WV>-900;lab,n=nd.label(M,np.ones((3,3)));sz=nd.sum(M,lab,range(1,n+1))
    kl=np.isin(lab,1+np.flatnonzero(sz<klein));WV[kl]=-999;Gv[kl]=G[kl];M=WV>-900
    st.update(stuecke_vorher=n0,kleinstuecke_entfernt=int((sz<klein).sum()),vertices_entfernt=int(kl.sum()))
    # Bett: Tiefe 0,35..1,2 m (Mulden auffuellen, Kuppen eingraben), Band nicht anfassen
    t=WV-Gv;flach=M&~VB&(t>tmax);Gv[flach]=WV[flach]-tmax;st['bett_aufgefuellt']=int(flach.sum())
    # Uferrand flach: Tiefe waechst vom Rand aus um hoechstens 0,25 m je Vertex (0,5 m) -> keine Stufe Land/Bett
    di=nd.distance_transform_edt(M);rand=M&~VB&(WV-Gv>0.06+0.25*di);Gv[rand]=(WV-(0.06+0.25*di))[rand];st['bettrand_angehoben']=int(rand.sum())
    # Ufer: Landstreifen bis 3 m neben Wasser, kein Band, kein Fels (Zellhang >60 Grad) -> Boeschung ca. 30 Grad, hoechstens 3 m Schnitt
    gy,gx=np.gradient(G,0.5);SL=np.degrees(np.arctan(np.hypot(gx,gy)))
    dist,ind=nd.distance_transform_edt(~M,return_indices=True);WVn=WV[ind[0],ind[1]]
    GRB=np.maximum(G-Gv,0)[ind[0],ind[1]]                     # Grabtiefe am naechsten Wasserpunkt -> erlaubter Schnitt am Ufer (Tal statt Kerbe)
    dvb=nd.distance_transform_edt(~VB);CAP=np.minimum.reduce([np.full(G.shape,maxschnitt),0.2*np.maximum(breite-dist,0),0.2*np.maximum(dvb-1,0)])   # erlaubter Schnitt laeuft zum Rand der Zone und zum Wandband weich aus
    zone=(~M)&(dist<=breite)&~VB&(SL<60)&(CAP>0)
    L=Gv.copy()
    for _ in range(breite+2):L=np.where(zone,np.minimum(L,nd.minimum_filter(L,3)+stufe),L)
    L=np.where(zone,np.maximum(L,np.maximum(G-CAP,WVn+0.08)),L)   # nicht unter Wasserspiegel, nicht tiefer als 3 m
    L=np.where(zone,np.minimum(Gv,L),Gv)
    S=nd.gaussian_filter(L,0.8);L=np.where(zone,np.minimum(Gv,np.maximum(S,WVn+0.08)),L)
    st['ufer_vertices_geaendert']=int((np.abs(L-Gv)>0.01).sum());Gv=L
    return WV.astype(np.float32),Gv.astype(np.float32),st

# ---- t62u Kaskade: Spiegel folgt der Talsohle (Becken + kurze Stufen), Hangwasser wird Land, Lauf bleibt zusammenhaengend [A]
import heapq
def _flut(m,H,extra=None):
    # priority flood from outlets (map edge + lowest point), returns order (outlet first), pred, spill S
    GY,GX=m.shape;P=np.argwhere(m);idx=-np.ones(m.shape,int);idx[m]=np.arange(len(P))
    n=len(P);S=np.full(n,np.inf);pred=-np.ones(n,int);done=np.zeros(n,bool);h=[]
    edge=(P[:,0]==0)|(P[:,1]==0)|(P[:,0]==GY-1)|(P[:,1]==GX-1)
    hv=H[m]
    seeds=list(np.flatnonzero(edge))+[int(np.argmin(hv))]+([] if extra is None else list(np.flatnonzero(extra[m])))
    for s in seeds:S[s]=hv[s];heapq.heappush(h,(hv[s],0.0,s))
    order=[];nb=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    while h:
        sv,dd,v=heapq.heappop(h)
        if done[v]:continue
        done[v]=True;order.append(v);y,x=P[v]
        for dy,dx in nb:
            yy,xx=y+dy,x+dx
            if 0<=yy<GY and 0<=xx<GX:
                w=idx[yy,xx]
                if w>=0 and not done[w]:
                    ns=max(sv,hv[w]);d2=dd+np.hypot(dy,dx)
                    if ns<S[w] or (ns==S[w] and d2<1e9 and pred[w]<0):S[w]=ns;pred[w]=v;heapq.heappush(h,(ns,d2,w))
    return P,np.array(order),pred,S

def fluss_kaskade(WV,G,VB,hmin=0.6,hang=0.5,tief=0.35,fuss=3):
    from scipy.sparse.csgraph import dijkstra
    from fluss_t61u import _graph
    from skimage.morphology import h_minima
    G=G.astype(float);M=WV>-900;WVn=np.full(WV.shape,-999.0);lab,n=nd.label(M,np.ones((3,3)));st={'komponenten':int(n),'becken':0,'hang_zu_land':0,'hang_behalten_fuer_lauf':0,'zum_ziel':[]}
    RIN=np.zeros(WV.shape,bool);SLG=np.degrees(np.arctan(np.hypot(*np.gradient(G,0.5))));FUSS=nd.binary_dilation(VB,iterations=fuss)|(nd.maximum_filter(SLG,3)>=55)
    for c in range(1,n+1):
        m=lab==c
        if m.sum()<4:continue
        B=nd.minimum_filter(np.where(m,G,1e4),5);B=np.where(B>9e3,G,B)          # Talsohle quer zum Lauf (2,5 m)
        A=np.where(m,B,B[m].max()+5);mi=h_minima(A,hmin).astype(bool)&m           # Becken (Senken >= hmin tief) sind Ziele, sonst Kartenrand
        st['becken']+=int(nd.label(mi)[1])
        P,o,pred,S=_flut(m,B,mi);L=np.full(m.shape,-999.0);L[m]=S
        hg=m&(G-L>hang)                                                            # Wasser liegt am Hang ueber der Talsohle
        hg|=m&FUSS&(G>L-tief)                                                      # am Wandband/Felsfuss nicht graben -> Ufer weicht von der Wand zurueck
        keep=m&~hg;l2,k2=nd.label(keep,np.ones((3,3)))
        if k2>1:                                                                   # Lauf zusammenhalten: billigster Weg durch Hangwasser
            idx,PP,g=_graph(m);cost=1.0+20.0*np.maximum(G-L,0)[m]
            g=g.tocoo();w=g.data*0.5*(cost[g.row]+cost[g.col]);from scipy.sparse import coo_matrix
            g2=coo_matrix((w,(g.row,g.col)),shape=g.shape).tocsr()
            big=np.argmax(nd.sum(keep,l2,range(1,k2+1)))+1;lk=l2[m]
            src=np.flatnonzero(lk==big);d,pr,_=dijkstra(g2,directed=False,indices=src,return_predecessors=True,min_only=True)
            res=np.zeros(len(PP),bool)
            for q in range(1,k2+1):
                if q==big:continue
                vs=np.flatnonzero(lk==q);v=vs[np.argmin(d[vs])]
                while v>=0 and lk[v]!=big:res[v]=True;v=pr[v]
            R=np.zeros(m.shape,bool);R[m]=res;R=nd.binary_dilation(R,np.ones((3,3)))&hg   # 1,5 m breite Rinne
            hg=hg&~R;st['hang_behalten_fuer_lauf']+=int(R.sum());RIN[R]=True
        st['hang_zu_land']+=int(hg.sum());L[hg]=-999;WVn[m&~hg]=L[m&~hg]
    # Rinne folgt dem Gelaende (Stufen statt Kerbe), danach Spiegel je Stueck neu geflutet -> nie bergauf
    T=np.where(RIN&(WVn>-900),np.maximum(WVn,G-tief),WVn);M2=WVn>-900;l3,n3=nd.label(M2,np.ones((3,3)))
    for c in range(1,n3+1):
        m=l3==c
        if m.sum()<4:continue
        A=np.where(m,T,T[m].max()+5);mi=h_minima(A,hmin).astype(bool)&m
        P,o,pred,S=_flut(m,T,mi);WVn[m]=S
    st['rinne_aufgefuellt_max_m']=round(float((WVn-T)[M2].max()),2)
    Gv=np.where(WVn>-900,np.minimum(G,WVn-tief),G);Gv=np.where(VB,G,Gv)
    weg=(WVn>-900)&(Gv>WVn-0.02);WVn[weg]=-999;st['ufer_entfernt_band']=int(weg.sum())
    st['grabtiefe_max_m']=round(float((G-Gv).max()),2);st['wasser_vertices']=int((WVn>-900).sum())
    return WVn.astype(np.float32),Gv.astype(np.float32),st
