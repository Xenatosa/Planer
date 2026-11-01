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

def frei_maske(OV,rampen,bruecken,wege,NX,NY,fs=4):
    """Sperrflaeche (Weg/Rampe/Bruecke/Bauplatz/Platz/Hof) auf 0,25-m-Raster; Rueckgabe Abstand [m] zur Sperrflaeche [A]"""
    M=np.zeros((NY*fs,NX*fs),bool)
    def zel(cx,cy):M[int(cy)*fs:int(cy)*fs+fs,int(cx)*fs:int(cx)*fs+fs]=True
    for o in OV:
        if o['weg_id'] or o['bauplatz']=='1' or o['platz'] or o['hof']=='1' or o['bruecke']=='1':zel(o['cx'],o['cy'])
    for c in wege:zel(c[0],c[1])
    for b in bruecken:zel(b[0],b[2])
    for pl in rampen:
        for a,b in zip(pl[:-1],pl[1:]):
            for t in np.linspace(0,1,12):
                x=a[0]+(b[0]-a[0])*t;z=a[1]+(b[1]-a[1])*t;j,i=int(z*fs),int(x*fs)
                M[max(0,j-2):j+3,max(0,i-2):i+3]=True   # Rampenachse +-0,5 m
    return nd.distance_transform_edt(~M)/fs
def wege_frei(L5,DIST,rand=1.5,fs=4):
    st={}
    for nm,L in L5.items():
        neu=[];n=0
        for o in L:
            r=0.5*o[3] if nm=='baeume' else 0.5*o[3]
            j=min(int(o[2]*fs),DIST.shape[0]-1);i=min(int(o[0]*fs),DIST.shape[1]-1)
            if DIST[j,i]<rand+r:n+=1;continue
            neu.append(o)
        L[:]=neu;st[nm]=n
    return st
