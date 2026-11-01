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

def entspitzen(FH,FB,vin,it=3,frei=0.4,k=0.25,grat=(21,1.0,0.35)):
    """t67u O3: Nadelspitzen weich gegen Nachbarmedian (2,75 m) stauchen, isolierte Senken bis 0,5 m unter Ueberlaufhoehe fuellen (relativ zur Grobform -> Krater bleibt) [A]"""
    from skimage.morphology import reconstruction
    FH=FH.copy();st={}
    inn=nd.gaussian_filter(vin.astype(float),2)>0.98
    for n in range(it):
        md=nd.median_filter(FH,11);e=FH-md;ne=np.where(e>frei,frei+(e-frei)*k,e)
        dlt=nd.gaussian_filter(np.where(inn,ne-e,0),0.8);FH=FH+dlt*inn;st['abtrag_max_m_%d'%n]=round(float(-dlt.min()),2)
    if grat:   # O6: Saegezahn-Grate gegen 5-m-Median weich stauchen [A]
        w_,f_,k_=grat;md=nd.median_filter(FH,w_);e=FH-md;ne=np.where(e>f_,f_+(e-f_)*k_,e)
        dlt=nd.gaussian_filter(np.where(inn,ne-e,0),1.2);FH=FH+dlt*inn;st['grat_abtrag_max_m']=round(float(-dlt.min()),2)
        for _ in range(2):   # O7: konvexe Kanten (Gratsaegezahn) runden: Laplace-gewichtete Glaettung [A]
            g=nd.gaussian_filter(FH,2.0);lap=g-FH;wq=np.clip(-lap/0.6,0,1)*inn;FH=FH+wq*0.8*lap
        st['grat_rund_max_m']=round(float(-(wq*0.8*lap).min()),2)
    def fu(A):
        s=A.copy();s[1:-1,1:-1]=A.max();return reconstruction(s,A,method='erosion')
    dep=(fu(FH)-FH)-(fu(FB)-FB);add=np.clip(dep-0.5,0,None)*inn
    add=np.maximum(add,nd.gaussian_filter(add,1.0));FH=FH+add;st['senke_gefuellt_max_m']=round(float(add.max()),2);st['senke_punkte']=int((add>0.05).sum())
    return FH,st

def bandrand_weich(FH,FB0,vin,breite=8):
    """t67u O5: im Feinband innerhalb 'breite' Feinpunkten (2 m) vom Rand weich auf die exakte Grobform ueberblenden -> keine sichtbaren Rechteck-Stufen [A]"""
    d=nd.distance_transform_edt(vin);w=np.clip((d-1)/breite,0,1);w=w*w*(3-2*w)
    rb=vin&~nd.binary_erosion(vin);v=float(np.abs(FH-FB0)[rb].max()) if rb.any() else 0
    FH2=np.where(vin,FB0+w*(FH-FB0),FH)
    return FH2,{'stufe_max_vorher_m':round(v,2),'stufe_max_nachher_m':round(float(np.abs(FH2-FB0)[rb].max()),2),'punkte':int((vin&(w<1)).sum())}

def grob_entspitzen(GA,WV,BAND,RS,frei=0.8,k=0.3):
    """t67u O7: Einzelspitzen im Anzeige-Grobnetz (nicht Feinband, nicht Wasser, nicht Bandnachbar) gegen 5er-Median stauchen [A]"""
    GA=GA.copy();g=GA.astype(float);md=nd.median_filter(g,5);e=g-md
    bz=nd.binary_dilation(BAND,iterations=1);NY,NX=BAND.shape
    jj,ii=np.mgrid[0:GA.shape[0],0:GA.shape[1]];cy=np.clip(jj//RS,0,NY-1);cx=np.clip(ii//RS,0,NX-1)
    cy2=np.clip((jj-1)//RS,0,NY-1);cx2=np.clip((ii-1)//RS,0,NX-1)
    frei_m=~(bz[cy,cx]|bz[cy2,cx]|bz[cy,cx2]|bz[cy2,cx2])&~nd.binary_dilation(WV>-900,iterations=3)
    sel=frei_m&(e>frei);neu=np.where(sel,md+frei+(e-frei)*k,g)
    # O8: Nadeln auch am Wasser (nicht Bandnachbar), Boden bleibt >= Wasser+0.3 [A]
    wmx=nd.maximum_filter(np.where(WV>-900,WV,-999.0),7)
    sel2=~(bz[cy,cx]|bz[cy2,cx]|bz[cy,cx2]|bz[cy2,cx2])&~sel&(WV<=-900)&(e>1.2)
    n2=np.maximum(md+1.2+(e-1.2)*k,wmx+0.3);sel2&=n2<g;neu=np.where(sel2,n2,neu)
    GA[:]=neu.astype(GA.dtype)
    return GA,{'punkte':int(sel.sum()),'punkte_wasser':int(sel2.sum()),'abtrag_max_m':round(float((g-neu).max()),2)}

def nadel_kappen(FH,vin,schw=1.2,k=0.3):
    """t67u O8: letzte Einzelnadeln (>1,2 m ueber 11er-Median) weich kappen, nur Nadelumgebung (r=3), nicht am Bandrand [A]"""
    FH=FH.astype(float).copy();med=nd.median_filter(FH,11);mx=nd.maximum_filter(FH,7);e=FH-med
    dist=nd.distance_transform_edt(vin);inn=vin&(dist>=3);rampe=np.clip((dist-1)/3,0,1)
    kern=inn&(FH>=mx)&(e>schw);zone=nd.binary_dilation(kern,iterations=3)&inn
    ziel=np.where(e>schw,med+schw+(e-schw)*k,FH);w=nd.gaussian_filter(zone.astype(float),1.0)*rampe
    neu=FH*(1-w)+np.minimum(FH,ziel)*w
    return neu,{'nadeln':int(nd.label(kern)[1]),'abtrag_max_m':round(float((FH-neu).max()),2)}
