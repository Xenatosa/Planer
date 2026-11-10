# t61u: Gelaende-Netz exakt wie im Viewer (main.js) nachbauen und auf Loecher pruefen [A]
# Grobnetz (ohne Bandzellen, Abbruchkanten-Verschiebung, Randverrundung) + Feinband; LS=1 (Desktop) und LS=2 (Handy)
import json,gzip,base64,sys,numpy as np
from scipy.spatial import cKDTree
D=json.loads(gzip.decompress(open('relief_daten.json.gz','rb').read()))
NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
f32=lambda s:np.frombuffer(base64.b64decode(s),np.float32)
G=f32(D.get('GB',D['G'])).astype(float);WV=f32(D['WV']).astype(float)
FW=D['FW'];FS=FW['fs'];FX=NX*FS+1
band=np.frombuffer(base64.b64decode(FW['band']),np.uint32);BZ=np.zeros(NX*NY,bool);BZ[band]=True
VB=np.zeros((GY,GX),bool);B2=BZ.reshape(NY,NX)
for dj in range(RS+1):
    for di in range(RS+1):VB[dj:dj+NY*RS:RS,di:di+NX*RS:RS]|=B2
VB=VB.ravel()
I,J=np.meshgrid(np.arange(GX),np.arange(GY));I=I.ravel();J=J.ravel()
p=np.stack([I/RS,G,J/RS],1);q=p.copy();G2=G.reshape(GY,GX)
def nb(A,di,dj,fill):
    o=np.full_like(A,fill);ys=slice(max(0,-dj),GY-max(0,dj));xs=slice(max(0,-di),GX-max(0,di));yd=slice(max(0,dj),GY-max(0,-dj)) if False else None
    o[max(0,-dj):GY-max(0,dj),max(0,-di):GX-max(0,di)]=A[max(0,dj):GY+min(0,dj) if dj<0 else GY,max(0,di):GX+min(0,di) if di<0 else GX][:GY-abs(dj),:GX-abs(di)] if True else 0
    return o
def sh(A,di,dj,fill=np.nan):
    o=np.full(A.shape,fill,float);H,W=A.shape
    o[max(0,-dj):H-max(0,dj),max(0,-di):W-max(0,di)]=A[max(0,dj):H-max(0,-dj),max(0,di):W-max(0,-di)];return o
mn=G2.copy();mx=G2.copy()
for dj in(-1,0,1):
    for di in(-1,0,1):s=sh(G2,di,dj);mn=np.fmin(mn,s);mx=np.fmax(mx,s)
rng=(mx-mn).ravel()
X2=p[:,0].reshape(GY,GX);Z2=p[:,2].reshape(GY,GX);sx=np.zeros((GY,GX));sz=np.zeros((GY,GX));n=np.zeros((GY,GX))
for dj in range(-2,3):
    for di in range(-2,3):
        g=sh(G2,di,dj);ok=np.isfinite(g)&(np.abs(g-G2)<0.6);sx+=np.where(ok,sh(X2,di,dj),0);sz+=np.where(ok,sh(Z2,di,dj),0);n+=ok
inner=(I>0)&(J>0)&(I<GX-1)&(J<GY-1);m=(~VB)&(rng>=1.5)&(n.ravel()>2)&inner
q[m,0]=p[m,0]*0.4+0.6*(sx.ravel()/np.maximum(n.ravel(),1))[m];q[m,2]=p[m,2]*0.4+0.6*(sz.ravel()/np.maximum(n.ravel(),1))[m]
dr=np.minimum.reduce([I,J,GX-1-I,GY-1-J]);GP=np.pad(G2,4,mode='edge');s2=sum(GP[4+dj:4+dj+GY,4+di:4+di+GX] for dj in range(-4,5) for di in range(-4,5)).ravel()/81
m2=(dr<=10)&~VB;w=(1-dr/10.5)*np.minimum(1,rng/1.5);q[m2,1]=(G*(1-w)+w*np.minimum(G,s2))[m2]
def build(LS):
    tri=[]
    jj,ii=np.meshgrid(np.arange(0,GY-LS,LS),np.arange(0,GX-LS,LS),indexing='ij');jj=jj.ravel();ii=ii.ravel()
    keep=~BZ[(jj//RS)*NX+(ii//RS)];jj,ii=jj[keep],ii[keep];a=jj*GX+ii;b=a+LS;c=a+GX*LS;d=c+LS
    T=np.concatenate([np.stack([a,c,d],1),np.stack([a,d,b],1)])
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fh=f32(FW['h']).astype(float)
    S=1 if LS==1 else 2;mp=np.full(FX*(NY*FS+1),-1,np.int64);mp[vid]=np.arange(len(vid))
    fp=np.stack([(vid%FX)/FS,fh,(vid//FX)/FS],1)
    if LS==2:   # t61u-Fix wie main.js
        fx=vid%FX;fy=vid//FX;x=fx//FS;y=fy//FS;Hh=FS//2;B2p=np.pad(B2,1)
        bz=lambda xx,yy:B2p[yy+1,xx+1]
        m1=(fy%FS==0)&(fx%FS==Hh);s1=m1&~(bz(np.minimum(x,NX-1),y-1)&bz(np.minimum(x,NX-1),np.minimum(y,NY)))
        a=(fy//FS*RS)*GX+x*RS;fp[s1,1]=(G[a[s1]]+G[a[s1]+RS])/2
        m2=(fx%FS==0)&(fy%FS==Hh);s2=m2&~(bz(x-1,np.minimum(y,NY-1))&bz(np.minimum(x,NX),np.minimum(y,NY-1)))
        a=(y*RS)*GX+fx//FS*RS;fp[s2,1]=(G[a[s2]]+G[a[s2]+RS*GX])/2
    bz=np.flatnonzero(BZ);x=bz%NX;y=bz//NX;F=[]
    for dj in range(0,FS,S):
        for di in range(0,FS,S):
            A=mp[(y*FS+dj)*FX+x*FS+di];B=mp[(y*FS+dj)*FX+x*FS+di+S];C=mp[(y*FS+dj+S)*FX+x*FS+di];Dd=mp[(y*FS+dj+S)*FX+x*FS+di+S];F+=[np.stack([A,C,Dd],1),np.stack([A,Dd,B],1)]
    F=np.concatenate(F)+len(q)
    P=np.concatenate([q,fp]);T=np.concatenate([T,F]);return P,T
def check(LS):
    P,T=build(LS);res={'LS':LS,'dreiecke':int(len(T)),'nan_hoehen':int((~np.isfinite(P[T].reshape(-1,3))).any(1).sum()),'fehlende_indizes':int((T<0).sum())}
    key=np.round(P*1e4).astype(np.int64);u,inv=np.unique(key,axis=0,return_inverse=True);inv=inv.ravel();T2=inv[T]
    deg=(T2[:,0]==T2[:,1])|(T2[:,1]==T2[:,2])|(T2[:,0]==T2[:,2]);res['entartet']=int(deg.sum());T2=T2[~deg]
    E=np.sort(np.concatenate([T2[:,[0,1]],T2[:,[1,2]],T2[:,[2,0]]]),1);ue,cnt=np.unique(E,axis=0,return_counts=True)
    U=u/1e4;op=ue[cnt==1];res['nicht_manifold_kanten']=int((cnt>2).sum())
    pa,pb=U[op[:,0]],U[op[:,1]]
    rand=lambda v:(np.abs(v[:,0])<1e-3)|(np.abs(v[:,0]-NX)<1e-3)|(np.abs(v[:,2])<1e-3)|(np.abs(v[:,2]-NY)<1e-3)
    innen=~(rand(pa)&rand(pb));pa,pb=pa[innen],pb[innen];res['offene_kanten_innen']=int(innen.sum())
    # T-Stoesse: offene Kanten, deren Punkte auf einer anderen offenen Kante liegen -> Spaltbreite messen
    t=np.linspace(0,1,5)[:,None,None];S_=(pa[None]*(1-t)+pb[None]*t).reshape(-1,3);own=np.tile(np.arange(len(pa)),5)
    seg_mid=(pa+pb)/2;kd=cKDTree(seg_mid);gap=np.zeros(len(S_))
    _,cand=kd.query(S_,k=min(40,len(pa)))
    best=np.full(len(S_),np.inf)
    for k in range(cand.shape[1]):
        c=cand[:,k];okc=c!=own;A=pa[c];B=pb[c];ab=B-A;tt=np.clip(((S_-A)*ab).sum(1)/np.maximum((ab*ab).sum(1),1e-12),0,1);d=np.linalg.norm(A+ab*tt[:,None]-S_,axis=1)
        best=np.where(okc,np.minimum(best,d),best)
    gk=best.reshape(5,-1).max(0)
    res['spalt_max_m']=round(float(gk.max()),4) if len(gk) else 0;res['kanten_mit_spalt_gt_1cm']=int((gk>0.01).sum());res['kanten_mit_spalt_gt_1mm']=int((gk>0.001).sum())
    bad=(pa+pb)[gk>0.01]/2;res['spalt_orte_beispiele']=[[round(float(v[0]),1),round(float(v[2]),1)] for v in bad[:: max(1,len(bad)//12)][:12]]
    return res,bad
out={}
for LS in(1,2):
    r,bad=check(LS);out['LS%d'%LS]=r;np.save('/workspace/t61/spalt_LS%d.npy'%LS,bad)
# Wasser: Wasserflaeche unter Gelaende / Gelaende ueber Wasser in Wasserzone
ok=WV>-900;out['wasser']={'wasser_vertices':int(ok.sum()),'wv_unter_gelaende':int((WV[ok]<G[ok]).sum()),'nan':int((~np.isfinite(WV)).sum())}
out['gelaende']={'g_min':round(float(G.min()),2),'g_max':round(float(G.max()),2),'unter_sockel_-34':int((G<-34).sum()),'nan':int((~np.isfinite(G)).sum())}
print(json.dumps(out,indent=1,ensure_ascii=False))
if len(sys.argv)>1:json.dump(out,open(sys.argv[1],'w'),indent=1,ensure_ascii=False)
