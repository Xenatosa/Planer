# t67u Runde O: Fluesse offen bis zum Kartenrand (alle 4 Seiten) [A]
import numpy as np,scipy.ndimage as nd
def rand_oeffnen(WV,GA,maxd=10,minpkt=200):
    WV=WV.copy();GA=GA.copy();st={'zeilen':0,'punkte':0,'seiten':{}}
    lab,n=nd.label(WV>-900,np.ones((3,3)));gr=np.bincount(lab.ravel());
    big=np.isin(lab,[k for k in range(1,n+1) if gr[k]>=minpkt])
    for side in range(4):
        w=np.rot90(WV,side).copy();g=np.rot90(GA,side).copy();lb=np.rot90(lab,side);b=np.rot90(big,side)&~np.isin(lb,np.unique(lb[:,0][lb[:,0]>0]));c=0   # nur Arme, deren Strang diesen Rand noch nicht erreicht
        for j in range(w.shape[0]):
            row=b[j,:maxd+1]
            if row[0] or not row.any():continue
            i0=int(np.argmax(row))
            # nur wenn der Arm zum Rand zeigt: Wasser auch weiter innen in dieser Zeile
            if not b[j,i0:i0+6].all():continue
            for i in range(i0):
                d=i0-i;w[j,i]=w[j,i0]-0.03*d;g[j,i]=min(g[j,i],g[j,i0]-0.03*d)
            c+=1;st['punkte']+=i0
        if c:st['seiten'][['West','Nord','Ost','Sued'][side]]=c
        WV=np.rot90(w,-side).copy();GA=np.rot90(g,-side).copy();st['zeilen']+=c
    return WV,GA,st
