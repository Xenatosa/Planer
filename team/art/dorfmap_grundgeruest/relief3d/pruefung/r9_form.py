# R8b Delle neben Weg, R9 Saegezahnrand, R9w Wellen (t122u/t123u). Netz Grob G (0,5 m). Liste je Feld. Exit 1 bei Treffern.
# R8b : abflusslose Mulde (Fuellung - G) > 0,30 m, Land, Neigung<1 (keine Wand/Fels), <=6 m von Rampenmittellinie oder Dorfweg; je Mulde 1 Treffer
# R9  : Wandkante (Neigung>1) gegen ihre geglaettete Form (Gauss 1 m): Zacken = Teilflaeche der Differenz mit Tiefe >=0,5 m (1 Zelle) und Flaeche <=2 m2 (Periode <2 m); je Feld 1 Treffer mit Anzahl
# R9w : Hang 0,15-0,8, >=1,5 m von Wand: Bandpass (Gauss 0,25 m - Gauss 1,5 m) |.|>0,10 m; je zusammenhaengender Flaeche >=1 m2 1 Treffer
import json,gzip,sys,base64,numpy as np,scipy.ndimage as nd
from skimage.morphology import reconstruction
f=sys.argv[1] if len(sys.argv)>1 else 'relief_daten.json.gz';D=json.load(gzip.open(f));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
feld=lambda x,z:'ABCDEFGH'[int(np.clip(x//42,0,7))]+str(int(np.clip(z//43,0,6))+1)
G=np.frombuffer(base64.b64decode(D['G']),np.float32).reshape(GY,GX).astype(float);WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(GY,GX)
LAND=WV<=-900;gy,gx=np.gradient(G,1/RS);S=np.hypot(gx,gy);WAND=S>1.0
WEG=np.zeros((GY,GX),bool)
for r in D['rampenwege']:
    r=np.asarray(r,float);L=np.r_[0,np.cumsum(np.hypot(*np.diff(r,axis=0).T))];t=np.arange(0,L[-1]+1e-6,0.25)
    WEG[np.clip((np.interp(t,L,r[:,1])*RS).round().astype(int),0,GY-1),np.clip((np.interp(t,L,r[:,0])*RS).round().astype(int),0,GX-1)]=1
for x,z in D['wege']:WEG[z*RS:z*RS+RS+1,x*RS:x*RS+RS+1]=1
DWEG=nd.distance_transform_edt(~WEG)/RS
T=[];S_={}
def hit(r,x,z,w,**k):T.append(dict(regel=r,feld=feld(x,z),x=round(float(x),1),z=round(float(z),1),wert=w,**k));S_[r]=S_.get(r,0)+1
sd=G.copy();sd[1:-1,1:-1]=G.max();tf=reconstruction(sd,G,method='erosion')-G
M=(tf>0.30)&LAND&~nd.binary_dilation(WAND,iterations=1);lab,n=nd.label(M)
for k,sl in enumerate(nd.find_objects(lab),1):
    m=lab[sl]==k;yy,xx=np.nonzero(m);yy=yy+sl[0].start;xx=xx+sl[1].start
    if DWEG[yy,xx].min()>6:continue
    j=np.argmax(tf[yy,xx]);hit('R8b_delle',xx[j]/RS,yy[j]/RS,round(float(tf[yy,xx].max()),2),abstand_weg=round(float(DWEG[yy,xx].min()),1))
Wg=nd.gaussian_filter(WAND*1.0,RS*1.0)>0.5;X=(WAND^Wg)&LAND;lab,n=nd.label(X);sz=nd.sum(X,lab,range(1,n+1));dt=nd.distance_transform_edt(X)/RS
mx=nd.maximum(dt,lab,range(1,n+1));zf={}
for k in range(n):
    if mx[k]>=0.5 and sz[k]/RS/RS<=2.0:
        yy,xx=np.nonzero(lab==k+1) if False else nd.center_of_mass(X,lab,k+1);f_=feld(xx/RS,yy/RS);zf.setdefault(f_,[0,xx/RS,yy/RS]);zf[f_][0]+=1
for f_,(c,x,z) in sorted(zf.items()):
    if c>=3:hit('R9_saegezahn',x,z,c)
BP=nd.gaussian_filter(G,RS*0.25)-nd.gaussian_filter(G,RS*1.5);H_=(S>0.15)&(S<0.8)&LAND&(nd.distance_transform_edt(~WAND)/RS>=1.5)&(np.abs(BP)>0.10)
lab,n=nd.label(H_)
for k,sl in enumerate(nd.find_objects(lab),1):
    m=lab[sl]==k
    if m.sum()/RS/RS<1.0:continue
    yy,xx=np.nonzero(m);hit('R9w_wellen',(xx.mean()+sl[1].start)/RS,(yy.mean()+sl[0].start)/RS,round(float(np.abs(BP[sl][m]).max()),2))
je_feld={}
for t in T:je_feld.setdefault(t['feld'],{}).setdefault(t['regel'],0);je_feld[t['feld']][t['regel']]+=1
out={'summe':len(T),'je_regel':S_,'je_feld':dict(sorted(je_feld.items())),'treffer':T}
print(json.dumps({k:out[k] for k in ('summe','je_regel')}))
if len(sys.argv)>2:json.dump(out,open(sys.argv[2],'w'),indent=0,ensure_ascii=False)
sys.exit(1 if T else 0)
