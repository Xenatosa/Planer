# O18k Pruef-Gate (t109u). Kartenweit R1-R7 aus relief_daten.json.gz; Ausgabe Trefferliste (Regel, Feld, x|z m, Wert). Exit 1 wenn Treffer.
# python3 pruefung/pruefe_regeln.py [relief_daten.json.gz] [out.json]
import json,gzip,sys,base64,numpy as np,scipy.ndimage as nd
from skimage.morphology import reconstruction
f=sys.argv[1] if len(sys.argv)>1 else 'relief_daten.json.gz';D=json.load(gzip.open(f));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(GY,GX).astype(float);WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(GY,GX);LAND=WV<=-900
feld=lambda x,z:'ABCDEFGH'[int(np.clip(x//42,0,7))]+str(int(np.clip(z//43,0,6))+1)
hf=lambda X,Z:nd.map_coordinates(G,[np.asarray(Z,float)*RS,np.asarray(X,float)*RS],order=1,mode='nearest')
gy,gx=np.gradient(G,1/RS);ST=np.hypot(gx,gy);WAND=ST>1.0   # >45 Grad
T=[];hit=lambda r,x,z,w,**k:T.append(dict(regel=r,feld=feld(x,z),x=round(float(x),1),z=round(float(z),1),wert=w,**k))
# Wegmaske 1-m-Zellen: Dorfwege, WEGA, Bruecken, Rampen
W=np.zeros((NY,NX),np.int16);RID=-np.ones((NY,NX),np.int16)
for x,z in D['wege']:W[z,x]=1
W[(np.frombuffer(base64.b64decode(D['WEGA']),np.uint8).reshape(GY,GX)[:-1:RS,:-1:RS]>20)&(W==0)]=1
for b in D['bruecken']:W[int(b[2]),int(b[0])]=3
def samp(r,step=0.25):
    r=np.asarray(r,float);L=np.r_[0,np.cumsum(np.hypot(*np.diff(r,axis=0).T))];t=np.arange(0,L[-1]+1e-6,step);return np.stack([np.interp(t,L,r[:,0]),np.interp(t,L,r[:,1])],1),t
R=[samp(r) for r in D['rampenwege']]
for i,(p,_) in enumerate(R):
    zi=np.clip(p[:,1].astype(int),0,NY-1);xi=np.clip(p[:,0].astype(int),0,NX-1);W[zi,xi]=np.maximum(W[zi,xi],2);RID[zi,xi]=i
# R1 Enden
for i,(p,t) in enumerate(R):
    for nm,k,kk in (('anfang',0,8),('ende',-1,-9)):
        x,z=p[k];d=p[k]-p[kk];d/=np.hypot(*d) or 1;nrm=np.array([-d[1],d[0]])
        q=[p[k]+d*s+nrm*o for s in (0.5,1,1.5,2,3) for o in (-1,0,1)];st=max(float(nd.map_coordinates(ST,[[a[1]*RS],[a[0]*RS]],order=1)[0]) for a in q)
        z0,z1,x0,x1=max(0,int(z)-2),min(NY,int(z)+3),max(0,int(x)-2),min(NX,int(x)+3);sub=W[z0:z1,x0:x1];rid=RID[z0:z1,x0:x1]
        an=bool(((sub>0)&(rid!=i)).any());rand=x<3 or z<3 or x>NX-3 or z>NY-3
        nass=bool((~LAND[max(0,int((z-1.5)*RS)):int((z+1.5)*RS)+1,max(0,int((x-1.5)*RS)):int((x+1.5)*RS)+1]).any())
        if st>1.0:hit('R1_wand',x,z,round(st,2),weg=f'rampe_{i}',wo=nm)
        if nass:hit('R1_wasser',x,z,1,weg=f'rampe_{i}',wo=nm)
        if not an and not rand:hit('R1_blind',x,z,0,weg=f'rampe_{i}',wo=nm)
# R2 Komponenten
lab,n=nd.label(W>0,np.ones((3,3)));gr=np.bincount(lab.ravel());gr[0]=0;hp=gr.argmax()
for k in range(1,n+1):
    if k!=hp:yy,xx=np.nonzero(lab==k);hit('R2_getrennt',xx.mean(),yy.mean(),int(len(xx)))
# R3 Laengs/Quer je Rampe, Abschnitte 4 m
for i,(p,t) in enumerate(R):
    d=np.gradient(p,axis=0);d/=np.maximum(np.linalg.norm(d,axis=1,keepdims=True),1e-9);n_=np.stack([-d[:,1],d[:,0]],1)
    hc=hf(p[:,0],p[:,1]);q=(hf(*(p+n_*1.5).T)-hf(*(p-n_*1.5).T))/3*100
    lr=hc-nd.gaussian_filter1d(hc,8,mode='nearest');cv=np.abs(np.gradient(np.gradient(nd.gaussian_filter1d(hc,2),0.25),0.25))
    mid=(hf(*(p+n_*0.75).T)+hf(*(p-n_*0.75).T))/2;wb=np.abs(hc-(hf(*(p+n_*1.5).T)+hf(*(p-n_*1.5).T))/2)
    for j in range(0,len(p),16):
        s=slice(j,j+16);x,z=p[j]
        if np.abs(q[s]).max()>3.5:hit('R3_quer_pct',x,z,round(float(np.abs(q[s]).max()),1),weg=f'rampe_{i}')
        if np.abs(lr[s]).max()>0.08:hit('R3_laengs_m',x,z,round(float(np.abs(lr[s]).max()),3),weg=f'rampe_{i}')
        if wb[s].max()>0.08:hit('R3_woelb_m',x,z,round(float(wb[s].max()),3),weg=f'rampe_{i}')
# R4 Rand: Wegzellen <4 m vom Rand, Gefaelle zum Rand; Schlucht: Weg >1.5 m unter Gelaende 4 m seitlich beidseitig
for z,x in zip(*np.nonzero(W)):
    if x<=3 or z<=3 or x>=NX-4 or z>=NY-4:
        ex=0 if x<=3 else NX if x>=NX-4 else x+.5;ez=0 if z<=3 else NY if z>=NY-4 else z+.5
        dh=float(hf([x+.5],[z+.5])[0]-hf([np.clip(ex,0,NX)],[np.clip(ez,0,NY)])[0]);dist=max(np.hypot(ex-x-.5,ez-z-.5),0.5)
        if abs(dh)/dist>0.15:hit('R4_rand',x+.5,z+.5,round(dh,2))
for i,(p,t) in enumerate(R):
    d=np.gradient(p,axis=0);d/=np.maximum(np.linalg.norm(d,axis=1,keepdims=True),1e-9);n_=np.stack([-d[:,1],d[:,0]],1);hc=hf(*p.T)
    s=np.minimum(hf(*(p+n_*4).T),hf(*(p-n_*4).T))-hc
    for j in np.nonzero(s>1.5)[0][::16]:hit('R4_schlucht',*p[j],round(float(s[j]),2),weg=f'rampe_{i}')
# R5 Loecher (abflusslose Senken auf trockenem Land >1 m), Spitzen
sd=G.copy();sd[1:-1,1:-1]=G.max();tief=reconstruction(sd,G,method='erosion')-G;tief[~nd.binary_erosion(LAND,iterations=2*RS)]=0
lab,n=nd.label(tief>1.0)
for k in range(1,n+1):
    yy,xx=np.nonzero(lab==k);j=tief[yy,xx].argmax();hit('R5_loch',xx[j]/RS,yy[j]/RS,round(float(tief[yy[j],xx[j]]),2),m2=round(len(xx)/RS/RS,1))
sp=G-nd.grey_opening(G,size=(3,3))
WD=nd.binary_dilation(WAND,iterations=2*RS)
for zz,xx in zip(*np.nonzero((sp>0.5)&~WD)):hit('R5_spitze',xx/RS,zz/RS,round(float(sp[zz,xx]),2))
# R6 Objekte auf Weg, Wasser im Schnee (Wasser auf Plateau >10 m)
for kind in ('baeume','felsen','findlinge','steine','geroell','felsbloecke'):
    for o in D.get(kind,[]):
        try:x,z=float(o[0]),float(o[2])
        except Exception:continue
        if 0<=x<NX and 0<=z<NY and W[int(z),int(x)]:hit('R6_objekt_auf_weg',x,z,kind)
wh=(~LAND)&(G>10);lab,n=nd.label(wh)
for k in range(1,n+1):yy,xx=np.nonzero(lab==k);hit('R6_wasser_schnee',xx.mean()/RS,yy.mean()/RS,int(len(xx)))
# R7 Geometrie-Trennung: Fein-Daten muessen Wand/Boden/Weg-Kennung tragen
FW=D['FW'];
if not all(k in FW for k in ('vid','h','t')):hit('R7_trennung',0,0,'FW ohne t')
S={}
for t_ in T:S[t_['regel']]=S.get(t_['regel'],0)+1
print(json.dumps({'summe':len(T),'je_regel':S},ensure_ascii=False))
for t_ in T[:400]:print(t_)
if len(sys.argv)>2:json.dump({'summe':len(T),'je_regel':S,'treffer':T},open(sys.argv[2],'w'),indent=0,ensure_ascii=False)
sys.exit(1 if T else 0)
