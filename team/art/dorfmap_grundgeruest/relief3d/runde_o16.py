# Runde O16 [F t77u]: rampe_9 (Krater, (130,161)->(140,198)) + Ruecken bei 133|173 entfernt -- NUR Anzeige.
# Laeuft spaet (nach CSV, nach Feinband-Bau, vor Objekt-Nachlauf): G (Zellbasis) und alle Zufallsfolgen bleiben unberuehrt,
# nur G_ANZ/VC/Feinband-Ecken im Ruecken-Bereich werden ersetzt. zellen_relief.csv: nur boden_anzeige_m (Anzeige) folgt. Deterministisch.
import numpy as np,scipy.ndimage as nd,base64
BOX=(125.5,139.5,153.5,195.0);R=6.5;RB=3.0
def _maske(P,GY,GX,RS):
    vj,vi=np.mgrid[0:GY,0:GX]/RS
    Pd=np.concatenate([np.linspace(P[i],P[i+1],12) for i in range(len(P)-1)]);d=np.full((GY,GX),99.)
    for px,py in Pd:d=np.minimum(d,np.hypot(vi-px,vj-py))
    x0,x1,y0,y1=BOX;db=np.hypot(np.maximum(0,np.maximum(x0-vi,vi-x1)),np.maximum(0,np.maximum(y0-vj,vj-y1)))
    return np.minimum(d,R+db)   # O16b: Kasten mit echtem Abstand -> weicher Uebergang statt Naht an der Kastenkante [A]
def _fuell(a,M):
    ys,xs=np.nonzero(M);y0,y1,x0,x1=max(0,ys.min()-2),ys.max()+3,max(0,xs.min()-2),xs.max()+3
    s=a[y0:y1,x0:x1];m=M[y0:y1,x0:x1];s[m]=np.mean(s[~m])
    for _ in range(4000):s[m]=0.25*(np.roll(s,1,0)+np.roll(s,-1,0)+np.roll(s,1,1)+np.roll(s,-1,1))[m]   # harmonisch: kein Grat/Mulde/Extremum innen
    return a
def entfernen(G_ANZ,VC,WV,RAMPWEGE,RS,idx=9):
    P=np.array(RAMPWEGE[idx],float);assert abs(P[0,0]-130.26)<0.5 and abs(P[-1,1]-198.39)<0.5,P[[0,-1]]
    RAMPWEGE.pop(idx)
    GY,GX=G_ANZ.shape;d=_maske(P,GY,GX,RS)
    M=(d<=R)&~nd.binary_dilation(WV>-900,iterations=2)
    w=np.clip((R+RB-d)/RB,0,1);w=w*w*(3-2*w);w[M]=1;w[WV>-900]=0
    alt=G_ANZ.astype(float);g=_fuell(alt.copy(),M);gn=alt*(1-w)+g*w
    C=VC.reshape(GY,GX,3).astype(float);Cn=C.copy()
    for k in range(3):Cn[...,k]=C[...,k]*(1-w)+_fuell(C[...,k].copy(),M)*w
    dd=gn-alt;st={'ecken':int((np.abs(dd)>0.01).sum()),'abtrag_max_m':round(float(-dd.min()),2),'auftrag_max_m':round(float(dd.max()),2),'rampen_rest':len(RAMPWEGE)}
    return gn.astype(G_ANZ.dtype),np.clip(np.round(Cn),0,255).astype(np.uint8).reshape(VC.shape),w,st
def feinband(FW,G_ANZ,VC,w,NX,RS):
    """Feinband-Ecken im Bereich: Hoehe = Grob-Dreieck (wie FB 'exakt die G-Dreiecke'), Farbe = VC, Tint neutral, Schnee 0 -- weich mit w"""
    FS=FW['fs'];FX=NX*FS+1;vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fy=vid//FX;fx=vid%FX
    gx=fx/FS*RS;gy=fy/FS*RS;i=np.minimum(gx.astype(int),G_ANZ.shape[1]-2);j=np.minimum(gy.astype(int),G_ANZ.shape[0]-2);ax=gx-i;az=gy-j
    ww=nd.map_coordinates(w,[gy,gx],order=1);m=ww>1e-3
    if not m.any():return {'ecken':0}
    G=G_ANZ.astype(float);A,B,C,D=G[j,i],G[j,i+1],G[j+1,i],G[j+1,i+1]
    hg=np.where(az>=ax,A+az*(C-A)+ax*(D-C),A+ax*(B-A)+az*(D-B))
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float).copy();h[m]=h[m]*(1-ww[m])+hg[m]*ww[m]
    V=VC.reshape(G.shape+(3,)).astype(float);vc=np.stack([nd.map_coordinates(V[...,k],[gy[m],gx[m]],order=1) for k in range(3)],1)
    c=np.frombuffer(base64.b64decode(FW['c']),np.uint8).reshape(-1,3).astype(float).copy();c[m]=c[m]*(1-ww[m,None])+vc*ww[m,None]
    t=np.frombuffer(base64.b64decode(FW['t']),np.uint8).reshape(-1,3).astype(float).copy();t[m]=t[m]*(1-ww[m,None])+128*ww[m,None]
    s=np.frombuffer(base64.b64decode(FW['s']),np.uint8).astype(float).copy();s[m]=s[m]*(1-ww[m])
    FW['h']=base64.b64encode(h.astype(np.float32).tobytes()).decode()
    for k,a in(('c',c),('t',t),('s',s)):FW[k]=base64.b64encode(np.clip(np.round(a),0,255).astype(np.uint8).tobytes()).decode()
    return {'ecken':int(m.sum())}
def fels_raus(felsbloecke,w,RS):
    n=len(felsbloecke);felsbloecke[:]=[f for f in felsbloecke if nd.map_coordinates(w,[[f[2]*RS],[f[0]*RS]],order=1)[0]<0.05];return n-len(felsbloecke)
def objekte_feinband(L,FW,NX,NY):
    """O16 R2: Objekte im Feinband auf die Feinband-Flaeche setzen, wenn sie >0,15 m darueber schweben (z.B. Baum 97,75|99,75: 0,36 m).
    Nur absenken, nie anheben. Basis: Baeume y-0,3, sonst y. Hoehe = min(bilinear, min(4 Ecken)+0,1) [A]"""
    FS=FW['fs'];FX,FY=NX*FS+1,NY*FS+1;vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);h=np.frombuffer(base64.b64decode(FW['h']),np.float32)
    F=np.full(FX*FY,np.nan,np.float32);F[vid]=h;F=F.reshape(FY,FX);st={}
    for nm,objs in L.items():
        off=0.3 if nm=='baeume' else 0.0;n=0
        for o in objs:
            fx,fy=o[0]*FS,o[2]*FS;i,j=int(np.floor(fx)),int(np.floor(fy))
            if not(0<=i<FX-1 and 0<=j<FY-1):continue
            q=F[j:j+2,i:i+2]
            if np.isnan(q).any():continue
            u,v=fx-i,fy-j;b=q[0,0]*(1-u)*(1-v)+q[0,1]*u*(1-v)+q[1,0]*(1-u)*v+q[1,1]*u*v;t=min(b,q.min()+0.1)
            if o[1]-off-t>0.15:o[1]=round(float(t+off),3);n+=1
        st[nm]=n
    return st
def geroell_raus(geroell,w,RS):
    """Geroell gehoerte zur Ruecken-Flanke; im Bereich (w>0,05) entfernen [A]"""
    n=len(geroell);geroell[:]=[o for o in geroell if nd.map_coordinates(w,[[o[2]*RS],[o[0]*RS]],order=1)[0]<0.05];return n-len(geroell)
def npz_nach(pfad,FW,G_ANZ,w,NX,NY,RS):
    """FW_NPZ-Dump fuer den Fehlerzaehler auf den Endstand bringen (FH = FW['h'] final, FB im Bereich = neue Grobform) [A]"""
    d=dict(np.load(pfad));FS=FW['fs'];FX=NX*FS+1;vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32)
    FH=d['FH'].astype(np.float32).copy();FH.ravel()[vid]=np.frombuffer(base64.b64decode(FW['h']),np.float32);d['FH']=FH
    fy,fx=np.mgrid[0:FH.shape[0],0:FH.shape[1]].astype(float);gx=fx/FS*RS;gy=fy/FS*RS
    i=np.minimum(gx.astype(int),G_ANZ.shape[1]-2);j=np.minimum(gy.astype(int),G_ANZ.shape[0]-2);ax=gx-i;az=gy-j;G=G_ANZ.astype(float)
    A,B,C,D=G[j,i],G[j,i+1],G[j+1,i],G[j+1,i+1];hg=np.where(az>=ax,A+az*(C-A)+ax*(D-C),A+ax*(B-A)+az*(D-B))
    ww=nd.map_coordinates(w,[gy,gx],order=1);d['FB']=(d['FB']*(1-ww)+hg*ww).astype(np.float32)
    np.savez_compressed(pfad,**d)
