# R8 Wegkreuzungen und Gabelungen (t120u/t121u, REGELN_VERPFLICHTEND.md Abschnitt R8). Gerendertes Netz = Grob G + Feinband FW (0,25 m).
# Kreuzungen: Rampenenden (Abzweig/Anschluss), Rampe x Rampe <6 m (andere Rampe oder gleiche Rampe >8 m Bogenabstand = Kehre), Rampe x Dorfweg (Kontakt <1,5 m), Dorfweg-Knoten (>=3 Arme).
# Je Kreuzung (Umkreis 4 m, nur Wegflaeche = <1,5 m von Mittellinie bzw. Dorfwegzelle):
#  R8_stufe  : max |dh| zwischen benachbarten Feinpunkten (0,25 m) > 0,20 m
#  R8_gitter : Kreuzungsflaeche (r 2 m) Abweichung von Ausgleichsebene, Differenz auf 1 m > 0,15 m
#  R8_quer   : Neigung der Ausgleichsebene (r 1,5 m) > 3 %
# python3 pruefung/r8_kreuzung.py [relief_daten.json.gz] [out.json]  -> Exit 1 bei Treffern
import json,gzip,sys,base64,numpy as np,scipy.ndimage as nd
from scipy.spatial import cKDTree
from r8a_policy import r8a_exception_for_endpoint, r8a_pair_is_hit, r8a_pair_limit_m
f=sys.argv[1] if len(sys.argv)>1 else 'relief_daten.json.gz';D=json.load(gzip.open(f));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
feld=lambda x,z:'ABCDEFGH'[int(np.clip(x//42,0,7))]+str(int(np.clip(z//43,0,6))+1)
G=np.frombuffer(base64.b64decode(D['G']),np.float32).reshape(GY,GX).astype(float);FW=D['FW'];FS=FW['fs'];FYn,FXn=NY*FS+1,NX*FS+1
yy,xx=np.mgrid[0:FYn,0:FXn];H=nd.map_coordinates(G,[yy/FS*RS,xx/FS*RS],order=1)
H.flat[np.frombuffer(base64.b64decode(FW['vid']),np.uint32)]=np.frombuffer(base64.b64decode(FW['h']),np.float32)
def samp(r,step=0.25):
    r=np.asarray(r,float);L=np.r_[0,np.cumsum(np.hypot(*np.diff(r,axis=0).T))];t=np.arange(0,L[-1]+1e-6,step);return np.stack([np.interp(t,L,r[:,0]),np.interp(t,L,r[:,1])],1),t
R=[samp(r) for r in D['rampenwege']]
DW=np.zeros((NY,NX),bool)
for x,z in D['wege']:DW[z,x]=1
DW|=np.frombuffer(base64.b64decode(D['WEGA']),np.uint8).reshape(GY,GX)[:-1:RS,:-1:RS]>20
RZ=np.zeros((NY,NX),bool)
for p,_ in R:RZ[np.clip(p[:,1].astype(int),0,NY-1),np.clip(p[:,0].astype(int),0,NX-1)]=1
DWo=DW&~nd.binary_dilation(RZ,iterations=1)   # Dorfweg ohne Rampenzellen
K=[]   # (x,z,art)
P=np.concatenate([p for p,_ in R]);RI=np.concatenate([np.full(len(p),i) for i,(p,_) in enumerate(R)]);LL=np.concatenate([t for _,t in R]);kd=cKDTree(P)
pr=kd.query_pairs(6.0,output_type='ndarray');pr=pr[(RI[pr[:,0]]!=RI[pr[:,1]])|(np.abs(LL[pr[:,0]]-LL[pr[:,1]])>8)]
for a,b in pr:K.append(((P[a]+P[b])/2,f'rampe_{RI[a]}x{RI[b]}',np.hypot(*(P[a]-P[b]))))
dz,dx=np.nonzero(DWo);DC=np.stack([dx+0.5,dz+0.5],1);kdw=cKDTree(DC)
dd,_=kdw.query(P,distance_upper_bound=1.5)
for j in np.nonzero(np.isfinite(dd))[0]:K.append((P[j],f'rampe_{RI[j]}xdorfweg',dd[j]))
for i,(p,_) in enumerate(R):   # Weg-Wand-Abzweig/Anschluss: jedes Rampenende (Uebergang Band -> Plateau/Dorfweg)
    K.append((p[0],f'rampe_{i}_anfang',0));K.append((p[-1],f'rampe_{i}_ende',0))
# Dorfweg-Knoten: Zelle mit >=3 getrennten Arm-Richtungen (4er-Nachbarn)
n4=sum(np.roll(DW,s,a) for s,a in ((1,0),(-1,0),(1,1),(-1,1)))
for z,x in zip(*np.nonzero(DW&(n4>=3))):K.append((np.array([x+0.5,z+0.5]),'dorfweg_knoten',0))
# Cluster single-link 4 m -> Kreuzungen
C=np.array([k[0] for k in K]);ck=cKDTree(C);prc=ck.query_pairs(4.0,output_type='ndarray');par=np.arange(len(C))
def fi(i):
    while par[i]!=i:par[i]=par[par[i]];i=par[i]
    return i
for a,b in prc:par[fi(a)]=fi(b)
grp={}
for i in range(len(C)):grp.setdefault(fi(i),[]).append(i)
# Wegflaeche fein
WM=np.zeros((FYn,FXn),bool)
for p,_ in R:WM[np.clip((p[:,1]*FS).round().astype(int),0,FYn-1),np.clip((p[:,0]*FS).round().astype(int),0,FXn-1)]=1
WM=nd.distance_transform_edt(~WM)/FS<=1.5
WM[:-1,:-1]|=np.kron(DW,np.ones((FS,FS),bool))
T=[];S={}
def hit(r,x,z,w,**k):T.append(dict(regel=r,feld=feld(x,z),x=round(float(x),1),z=round(float(z),1),wert=w,**k));S[r]=S.get(r,0)+1
KL=[]
for g in grp.values():
    arten=sorted(set(K[i][1] for i in g))
    if arten==['dorfweg_knoten']:
        c=C[g].mean(0)
    else:
        g2=[i for i in g if K[i][1]!='dorfweg_knoten'];c=C[g2].mean(0)
    x,z=c;KL.append({'x':round(float(x),1),'z':round(float(z),1),'feld':feld(x,z),'art':'+'.join(a for a in arten if True)[:120]})
    y0,x0=int(round(z*FS)),int(round(x*FS));r=4*FS;sl=(slice(max(0,y0-r),y0+r+1),slice(max(0,x0-r),x0+r+1))
    A=H[sl];M=WM[sl];yy_,xx_=np.mgrid[sl];DI=np.hypot(yy_/FS-z,xx_/FS-x);M=M&(DI<=4)
    st=0.0
    for ax in (0,1):
        dA=np.abs(np.diff(A,axis=ax));mm=(M[1:,:]&M[:-1,:]) if ax==0 else (M[:,1:]&M[:,:-1])
        if mm.any():st=max(st,float(dA[mm].max()))
    KL[-1]['stufe']=round(st,3)
    if st>0.20:hit('R8_stufe',x,z,round(st,2),art=KL[-1]['art'])
    m2=M&(DI<=2.0)
    if m2.sum()>10:
        X=np.c_[xx_[m2]/FS-x,yy_[m2]/FS-z,np.ones(m2.sum())];co=np.linalg.lstsq(X,A[m2],rcond=None)[0];Res=np.full(A.shape,np.nan);Res[m2]=A[m2]-X@co
        gi=0.0
        for ax in (0,1):
            dR=np.abs(Res[FS:,:]-Res[:-FS,:]) if ax==0 else np.abs(Res[:,FS:]-Res[:,:-FS]);gi=max(gi,float(np.nanmax(dR)) if np.isfinite(dR).any() else 0)
        KL[-1]['gitter']=round(gi,3)
        if gi>0.15:hit('R8_gitter',x,z,round(gi,2),art=KL[-1]['art'])
    m1=M&(DI<=1.5)
    if m1.sum()>10:
        X=np.c_[xx_[m1]/FS-x,yy_[m1]/FS-z,np.ones(m1.sum())];co=np.linalg.lstsq(X,A[m1],rcond=None)[0];q=float(np.hypot(co[0],co[1])*100)
        if all(K[i][1].endswith(('_anfang','_ende')) for i in g):   # reines Wegende: Quergefaelle senkrecht zur Wegrichtung (Laengsgefaelle zaehlt nicht)
            i0=g[0];ri=int(K[i0][1].split('_')[1]);pp=R[ri][0];dv=(pp[min(8,len(pp)-1)]-pp[0]) if K[i0][1].endswith('_anfang') else (pp[-1]-pp[max(0,len(pp)-9)]);dv=dv/max(np.hypot(*dv),1e-9);q=float(abs(-dv[1]*co[0]+dv[0]*co[1])*100);KL[-1]['quer_pct']=round(q,1)
        if q>3.0:hit('R8_quer',x,z,round(q,1),art=KL[-1]['art'])
# R8a Wegende (t122u): Auslauf 4 m hinter dem Ende, Streifen +-2,5 m um die verlaengerte Mittellinie, ohne Wand (Neigung>1).
# Alle Wegenden behalten 0,10 m, ausser R8a_ausnahme_rampe2_start ([F] Fabian, t166s961, 2026-11-13):
# nur rampe_2_anfang bei 126.51|31.62 erhaelt im eigenen 4-m-Auslauf 0,18 m.
gyF,gxF=np.gradient(H,1/FS);WANDF=np.hypot(gxF,gyF)>1.0
for i,(p,_) in enumerate(R):
    for e,(q0,q1) in (('anfang',(p[0],p[min(8,len(p)-1)])),('ende',(p[-1],p[max(0,len(p)-9)]))):
        dv=q0-q1;dv=dv/max(np.hypot(*dv),1e-9);nv=np.array([-dv[1],dv[0]])
        y0,x0=int(round(q0[1]*FS)),int(round(q0[0]*FS));r=6*FS;sl=(slice(max(0,y0-r),y0+r+1),slice(max(0,x0-r),x0+r+1));yy_,xx_=np.mgrid[sl]
        rx,rz=xx_/FS-q0[0],yy_/FS-q0[1];lo=rx*dv[0]+rz*dv[1];qu=rx*nv[0]+rz*nv[1]
        M=(lo>=-1)&(lo<=4)&(np.abs(qu)<=2.5)&~WANDF[sl]&(xx_>0)&(yy_>0)&(xx_<FXn-1)&(yy_<FYn-1);A=H[sl];st=0.0
        for ax in (0,1):
            dA=np.abs(np.diff(A,axis=ax));mm=(M[1:,:]&M[:-1,:]) if ax==0 else (M[:,1:]&M[:,:-1])
            if mm.any():st=max(st,float(dA[mm].max()))
        weg=f'rampe_{i}_{e}';limit=r8a_pair_limit_m(weg,q0);ausnahme=r8a_exception_for_endpoint(weg,q0)
        if r8a_pair_is_hit(st,weg,q0):hit('R8a_wegende',q0[0],q0[1],round(st,2),weg=weg,limit_m=limit,ausnahme=ausnahme)
je_feld={}
for t in T:je_feld.setdefault(t['feld'],{}).setdefault(t['regel'],0);je_feld[t['feld']][t['regel']]+=1
out={'summe':len(T),'je_regel':S,'kreuzungen':len(KL),'je_feld':dict(sorted(je_feld.items())),'treffer':T,'liste':KL}
print(json.dumps({k:out[k] for k in ('summe','je_regel','kreuzungen')}))
if len(sys.argv)>2:json.dump(out,open(sys.argv[2],'w'),indent=0,ensure_ascii=False)
sys.exit(1 if T else 0)
