# t61u Runde I: Wasserspiegel entlang des Flusslaufs monoton fallend + Bett nur in der Anzeige eingraben [A]
# Eingabe WV (0,5-m-Gitter, -999 = kein Wasser), G, VB (Bandvertices, unantastbar). Ausgabe WVn, Gview, Statistik.
import numpy as np,scipy.ndimage as nd
from scipy.sparse import coo_matrix;from scipy.sparse.csgraph import dijkstra
def _graph(m):
    GY,GX=m.shape;idx=-np.ones(m.shape,int);P=np.argwhere(m);idx[m]=np.arange(len(P));r=[];c=[];w=[]
    for dj,di in((0,1),(1,0),(1,1),(1,-1)):
        A=idx[:GY-dj,(0 if di>=0 else -di):GX-(di if di>0 else 0)];B=idx[dj:,(di if di>0 else 0):GX-(0 if di>=0 else -di)]
        ok=(A>=0)&(B>=0);r.append(A[ok]);c.append(B[ok]);w.append(np.full(int(ok.sum()),np.hypot(dj,di)*0.5))
    r=np.concatenate(r);c=np.concatenate(c);w=np.concatenate(w)
    return idx,P,coo_matrix((w,(r,c)),shape=(len(P),len(P))).tocsr()
def fluss_monoton(WV,G,VB,lev_roh,tief=0.35,maxgrab=9.0):
    GY,GX=WV.shape;M=WV>-900;WVn=np.full(WV.shape,-999.0);DIG=np.zeros(WV.shape);st={'komponenten':0}
    # Rohspiegel ohne Anklammern an Boden, Ausreisser (Wasser an Wandflanken) per 20%-Perzentil (4,5 m) entfernt
    R=nd.percentile_filter(np.where(M,lev_roh,1e4),20,size=9);R=np.where(R>9e3,lev_roh,R)
    lab,n=nd.label(M,np.ones((3,3)))
    for c in range(1,n+1):
        m=lab==c
        if m.sum()<4:continue
        st['komponenten']+=1
        idx,P,g=_graph(m);out=np.zeros(m.shape,bool);out[0,:]=out[-1,:]=out[:,0]=out[:,-1]=True
        src=list(np.flatnonzero((out&m)[m]));src.append(int(np.argmin(R[m])))
        s,pred,_=dijkstra(g,directed=False,indices=src,return_predecessors=True,min_only=True)
        o=np.argsort(s);r=R[m].astype(float);L=r.copy()
        reach=s.copy();haupt=-np.ones(len(s),int)            # Hauptarm = Kind mit dem laengsten Oberlauf (nicht das hoechste)
        for v in o[::-1]:
            p=pred[v]
            if p>=0 and (haupt[p]<0 or reach[v]>reach[p]):reach[p]=max(reach[p],reach[v]);haupt[p]=v
        def senken(L):                                       # stromab nie hoeher als der Hauptarm stromauf
            for v in o[::-1]:
                h=haupt[v]
                if h>=0:L[v]=min(L[v],L[h])
            return L
        for it in range(3):
            L=senken(L)
            F=np.zeros(m.shape);F[m]=L;W=nd.gaussian_filter(m.astype(float),1.5);L=(nd.gaussian_filter(F,1.5)/np.maximum(W,1e-6))[m]
            r=np.minimum(r,L+0.0)
        L=senken(L)
        for v in o:                                          # Seitenarme/Senken auf Muendungshoehe anheben -> streng monoton
            p=pred[v]
            if p>=0 and L[v]<L[p]:L[v]=L[p]
        WVn[m]=L
    # Ufer/Bett: Boden ueber Wasserspiegel -> im Kern (>=1 m vom Rand, kein Bandvertex) Bett eingraben, sonst Ufer (kein Wasser)
    Mi=nd.binary_erosion(M,np.ones((3,3)),iterations=2)
    hoch=M&(G>WVn-0.05);grab=hoch&~VB&(G-(WVn-tief)<=maxgrab)
    DIG[grab]=G[grab]-(WVn[grab]-tief)
    DIG=np.where(M&~VB,np.maximum(DIG,nd.gaussian_filter(DIG,1.0)*0.8),DIG)       # weicher Rand der Grabung
    DIG=np.where(VB,0,DIG);Gv=G-DIG
    weg=M&(Gv>WVn-0.02);WVn[weg]=-999
    M2=WVn>-900;lab2,n2=nd.label(M2,np.ones((3,3)))               # Nachlauf auf dem Endnetz: nur monoton machen (hebt nur an)
    for c in range(1,n2+1):
        m=lab2==c
        if m.sum()<2:continue
        idx,P,g=_graph(m);out=np.zeros(m.shape,bool);out[0,:]=out[-1,:]=out[:,0]=out[:,-1]=True
        src=list(np.flatnonzero((out&m)[m]));src.append(int(np.argmin(WVn[m])))
        s,pred,_=dijkstra(g,directed=False,indices=src,return_predecessors=True,min_only=True);L=WVn[m].copy()
        for v in np.argsort(s):
            p=pred[v]
            if p>=0 and L[v]<L[p]:L[v]=L[p]
        WVn[m]=L
    st.update({'wasser_vertices_vorher':int(M.sum()),'wasser_vertices_nachher':int((WVn>-900).sum()),'ufer_entfernt':int(weg.sum()),
      'bett_gegraben_vertices':int((DIG>0.01).sum()),'grabtiefe_max_m':round(float(DIG.max()),2),'spiegel_geaendert_mittel_m':round(float(np.abs(WVn-WV)[(WVn>-900)].mean()),3)})
    return WVn.astype(np.float32),Gv.astype(np.float32),st
