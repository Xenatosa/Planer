import json,gzip,base64,numpy as np,scipy.ndimage as nd
D=json.load(gzip.open('relief_daten.json.gz'));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(GY,GX).astype(float);WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(GY,GX);LAND=WV<=-900
feld=lambda x,z:'ABCDEFGH'[int(np.clip(x//42,0,7))]+str(int(np.clip(z//43,0,6))+1)
W=np.zeros((NY,NX),np.int16);RID=-np.ones((NY,NX),np.int16)
for x,z in D['wege']:W[z,x]=1
WEGA=np.frombuffer(base64.b64decode(D['WEGA']),np.uint8).reshape(GY,GX)
W[(WEGA[:-1:RS,:-1:RS]>20)&(W==0)]=1
for b in D['bruecken']:W[int(b[2]),int(b[0])]=3
def samp(r,step=0.25):
    r=np.asarray(r,float);L=np.r_[0,np.cumsum(np.hypot(*np.diff(r,axis=0).T))];t=np.arange(0,L[-1]+1e-6,step);return np.stack([np.interp(t,L,r[:,0]),np.interp(t,L,r[:,1])],1),t
R=[samp(r) for r in D['rampenwege']]
for i,(p,_) in enumerate(R):
    zi=np.clip(p[:,1].astype(int),0,NY-1);xi=np.clip(p[:,0].astype(int),0,NX-1);W[zi,xi]=np.maximum(W[zi,xi],2);RID[zi,xi]=i
hf=lambda x,z:float(nd.map_coordinates(G,[[z*RS],[x*RS]],order=1)[0])
print('NX NY RS',NX,NY,RS,'wege',len(D['wege']),'rampen',len(D['rampenwege']),'bruecken',len(D['bruecken']))
out={'R1':[],'R2':[],'R6':[]}
for i,(p,t) in enumerate(R):
    L=t[-1]
    for nm,k in (('anfang',0),('ende',-1)):
        x,z=p[k]
        m=(W>0)&(RID!=i);yy,xx=np.nonzero(m);d=np.hypot(xx+.5-x,yy+.5-z);j=d.argmin()
        out['R1'].append(dict(weg=f'rampe_{i}',wo=nm,feld=feld(x,z),x=round(x,1),z=round(z,1),laenge_zellen=round(L,1),naechster_netzabstand_zellen=round(float(d[j]),1),naechste_zelle=[int(xx[j]),int(yy[j])],h_ende=round(hf(x,z),2),h_naechste=round(hf(xx[j]+.5,yy[j]+.5),2)))
lab,n=nd.label(W>0,np.ones((3,3)));gr=np.bincount(lab.ravel());gr[0]=0;hp=gr.argmax()
dist_hp=nd.distance_transform_edt(lab!=hp)
for k in range(1,n+1):
    if k==hp:continue
    yy,xx=np.nonzero(lab==k);dd=dist_hp[yy,xx];j=dd.argmin()
    typ=sorted(set(int(v) for v in W[yy,xx]));rids=sorted(set(int(v) for v in RID[yy,xx] if v>=0))
    out['R2'].append(dict(feld=feld(xx.mean(),yy.mean()),x=round(float(xx.mean()),1),z=round(float(yy.mean()),1),zellen=int(len(xx)),luecke_zur_hauptkomponente_zellen=round(float(dd[j]),1),an_stelle=[int(xx[j]),int(yy[j])],typen=typ,rampen=[f'rampe_{r}' for r in rids]))
wh=(~LAND)&(G>10);lab,n=nd.label(wh)
for k in range(1,n+1):
    yy,xx=np.nonzero(lab==k);out['R6'].append(dict(feld=feld(xx.mean()/RS,yy.mean()/RS),x=round(float(xx.mean()/RS),1),z=round(float(yy.mean()/RS),1),fein_zellen=int(len(xx)),h_min=round(float(G[yy,xx].min()),2),h_max=round(float(G[yy,xx].max()),2),wv_mittel=round(float(WV[yy,xx].mean()),2)))
json.dump(out,open('pruefung/p2_analyse/p2_analyse.json','w'),indent=1,ensure_ascii=False)
for k,v in out.items():
    print('==',k)
    for e in v:print(e)
np.save('/tmp/p2_W.npy',W)
