# O18k (t105u): Wegenetz als Graph pruefen: Komponenten, Rampen-Enden ohne Anschluss, Enden an Felswand/Kartenrand, steiler Randabfall. python3 ... relief_daten.json.gz [out.json]
import json,gzip,sys,base64,numpy as np,scipy.ndimage as nd
D=json.load(gzip.open(sys.argv[1]));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(GY,GX).astype(float);Gz=np.frombuffer(base64.b64decode(D['G']),np.float32).reshape(-1)
feld=lambda x,z:'ABCDEFGH'[int(np.clip(x//42,0,7))]+str(int(np.clip(z//43,0,6))+1)
h=lambda x,z:float(nd.map_coordinates(G,[[z*RS],[x*RS]],order=1,mode='nearest')[0])
W=np.zeros((NY,NX),np.int16)   # 1 Dorfweg, 2 Rampe, 3 Bruecke
for x,z in D['wege']:W[z,x]=1
WA=np.frombuffer(base64.b64decode(D['WEGA']),np.uint8).reshape(GY,GX)[:-1:RS,:-1:RS]>20;W[WA&(W==0)]=1   # Anzeige-Wegmaske dazu
for b in D['bruecken']:W[int(b[2]),int(b[0])]=3
R=[np.array(r,float) for r in D['rampenwege']]
for r in R:
    L=np.r_[0,np.cumsum(np.hypot(*np.diff(r,axis=0).T))]
    for t in np.arange(0,L[-1],0.25):x,z=np.interp(t,L,r[:,0]),np.interp(t,L,r[:,1]);W[min(int(z),NY-1),min(int(x),NX-1)]=max(W[min(int(z),NY-1),min(int(x),NX-1)],2)
lab,n=nd.label(W>0,np.ones((3,3)));gr=np.bincount(lab.ravel());gr[0]=0;haupt=int(gr.argmax())
gy,gx=np.gradient(G,1/RS);steil=np.hypot(gx,gy)
st=lambda x,z:float(nd.maximum_filter(steil,5)[int(z*RS),int(x*RS)])
out={'komponenten':[],'rampen_enden':[],'rand':[]}
for k in range(1,n+1):
    if k==haupt:continue
    yy,xx=np.nonzero(lab==k);out['komponenten'].append({'zellen':int(len(xx)),'mitte':[int(xx.mean()),int(yy.mean())],'feld':feld(xx.mean(),yy.mean()),'art':sorted({int(v) for v in W[yy,xx]})})
for i,r in enumerate(R):
    for e,(p,q) in (('anfang',(r[0],r[1])),('ende',(r[-1],r[-2]))):
        x,z=p;d=p-q;d/=np.hypot(*d) or 1
        # Anschluss: andere Wegzelle (nicht diese Rampe) innerhalb 1.5 m
        own=np.zeros_like(W,bool);L=np.r_[0,np.cumsum(np.hypot(*np.diff(r,axis=0).T))]
        for t in np.arange(0,L[-1],0.25):own[min(int(np.interp(t,L,r[:,1])),NY-1),min(int(np.interp(t,L,r[:,0])),NX-1)]=True
        z0,z1,x0,x1=max(0,int(z)-2),min(NY,int(z)+3),max(0,int(x)-2),min(NX,int(x)+3);anschl=bool(((W[z0:z1,x0:x1]>0)&~own[z0:z1,x0:x1]).any())
        dh=h(x+d[0]*2,z+d[1]*2)-h(x,z)
        out['rampen_enden'].append({'rampe':i,'wo':e,'x':round(float(x),1),'z':round(float(z),1),'feld':feld(x,z),'anschluss':anschl,'hoehe':round(h(x,z),2),'dh_2m_weiter':round(dh,2),'steil_max_dhdm':round(st(x,z),2),'am_rand':bool(x<4 or z<4 or x>NX-4 or z>NY-4)})
# Wegzellen am Kartenrand: Gefaelle der letzten 3 m zum Rand
for z in range(NY):
    for x in range(NX):
        if W[z,x] and (x<=3 or z<=3 or x>=NX-4 or z>=NY-4):
            nx_,nz_=(1 if x<=3 else -1 if x>=NX-4 else 0),(1 if z<=3 else -1 if z>=NY-4 else 0)
            d=h(x+0.5,z+0.5)-h(x+0.5+3*nx_,z+0.5+3*nz_);out['rand'].append({'x':x,'z':z,'feld':feld(x,z),'art':int(W[z,x]),'dh_rand_minus_innen_3m':round(d,2)})
json.dump(out,open(sys.argv[2],'w'),indent=0) if len(sys.argv)>2 else None
print('nebenkomponenten',len(out['komponenten']));[print(c) for c in out['komponenten']]
print('rampen_enden ohne anschluss / an wand');[print(e) for e in out['rampen_enden'] if not e['anschluss'] or e['steil_max_dhdm']>1.0]
rr=[r for r in out['rand'] if abs(r['dh_rand_minus_innen_3m'])>0.5];print('rand steil',len(rr),'von',len(out['rand']));[print(r) for r in rr[:30]]
