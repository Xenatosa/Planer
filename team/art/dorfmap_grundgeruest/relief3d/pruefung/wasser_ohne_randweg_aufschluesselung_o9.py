# O9: wasser_ohne_randweg nach Komponenten aufschluesseln (Spiegel, Ufer, Ueberlauf). python3 ... relief_daten.json.gz [S]
import json,gzip,base64,heapq,numpy as np,scipy.ndimage as nd,sys
D=json.load(gzip.open(sys.argv[1]))
WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(607,673);w=WV>-900
ok=np.zeros(w.shape,bool);H=[]
for j,i in np.argwhere(w):
  if min(j,i,606-j,672-i)==0:ok[j,i]=True;heapq.heappush(H,(float(WV[j,i]),j,i))
while H:
  v,j,i=heapq.heappop(H)
  for dj in(-1,0,1):
    for di in(-1,0,1):
      a,b=j+dj,i+di
      if 0<=a<607 and 0<=b<673 and w[a,b] and not ok[a,b] and WV[a,b]>=WV[j,i]-0.01:ok[a,b]=True;heapq.heappush(H,(float(WV[a,b]),a,b))
m=w&~ok;l,n=nd.label(m,np.ones((3,3)))
R=[]
for k,sl in enumerate(nd.find_objects(l),1):
  c=(l[sl]==k);z=WV[sl][c];R.append((int(c.sum()),sl[1].start/2,sl[1].stop/2,sl[0].start/2,sl[0].stop/2,round(float(z.min()),2),round(float(z.max()),2)))
R.sort(reverse=True);print('summe',int(m.sum()),'komponenten',n)
for r in R[:25]:print(r)
print('klein(<20):',sum(1 for r in R if r[0]<20),sum(r[0] for r in R if r[0]<20))
# minimax-Barriere vom Teich zum Rand
import heapq
j0,i0=[(j,i) for j,i in np.argwhere(l==l[int(48*2),int(20*2)] if l[96,40] else (l==np.bincount(l.ravel())[1:].argsort()[-2]+1))][0]
best=np.full(w.shape,1e9);best[j0,i0]=WV[j0,i0];H=[(float(WV[j0,i0]),j0,i0)];par={}
while H:
  b,j,i=heapq.heappop(H)
  if b>best[j,i]:continue
  if ok[j,i]:
    print('erreicht Rand-OK bei x',i/2,'z',j/2,'barriere',round(b,2));break
  for dj in(-1,0,1):
    for di in(-1,0,1):
      a,c=j+dj,i+di
      if 0<=a<607 and 0<=c<673 and w[a,c]:
        nb=max(b,float(WV[a,c]))
        if nb<best[a,c]:best[a,c]=nb;par[(a,c)]=(j,i);heapq.heappush(H,(nb,a,c))
p=(j,i);path=[]
while p in par:path.append(p);p=par[p]
path=path[::-1];hs=[(x[1]/2,x[0]/2,round(float(WV[x]),2)) for x in path]
mx=max(hs,key=lambda t:t[2]);print('pfadlaenge',len(hs),'max',mx);print(hs[::max(1,len(hs)//15)])
print('ende',hs[-4:])
jj,ii=path[-1];print('ziel ok',ok[jj,ii],'WV',WV[jj,ii],'nachbarn',WV[jj-1:jj+2,ii-1:ii+2].round(2),ok[jj-1:jj+2,ii-1:ii+2])
L,_=nd.label(w,np.ones((3,3)))
for nm,(x,z) in {'teich':(20,48),'x35z55':(35,55.5),'x15z52':(15,52.5)}.items():
  k=L[int(z*2),int(x*2)];
  if k==0:
    jj,ii=int(z*2),int(x*2);sub=L[jj-6:jj+7,ii-6:ii+7];k=np.bincount(sub[sub>0]).argmax()
  s=np.argwhere(L==k);print(nm,'komp',k,'groesse',len(s),'bbox x',s[:,1].min()/2,s[:,1].max()/2,'z',s[:,0].min()/2,s[:,0].max()/2,'ok-anteil',ok[L==k].mean().round(3))
G=np.frombuffer(base64.b64decode(D['G']),np.float32).reshape(607,673)
for k in sorted(set(l.ravel())-{0}):
  m1=l==k;rim=nd.binary_dilation(m1,np.ones((3,3)),2)&~w
  print('komp',k,int(m1.sum()),'spiegel',round(float(WV[m1].max()),2),'ufer_min',round(float(G[rim].min()),2),'dicht' if G[rim].min()>WV[m1].max() else 'UEBERLAUF')
print('--- lokaler Ueberlauf (Boden-Nachbar tiefer als Spiegel-5cm)')
for k in sorted(set(l.ravel())-{0}):
  m1=l==k;n=0;mx=0
  for j,i in np.argwhere(m1):
    nb=G[max(0,j-1):j+2,max(0,i-1):i+2];wb=w[max(0,j-1):j+2,max(0,i-1):i+2]
    d=WV[j,i]-nb[~wb]
    if d.size and d.max()>0.05:n+=1;mx=max(mx,float(d.max()))
  print('komp',k,'pkt',n,'max',round(mx,2))
print('--- naechstes Rand-Wasser je Komp')
dt,ind=nd.distance_transform_edt(~ok,return_indices=True)
for k in (9,11,12,4):
  m1=l==k;pts=np.argwhere(m1);dd=dt[m1];a=pts[dd.argmin()];b=ind[:,a[0],a[1]]
  print(k,'von x',a[1]/2,'z',a[0]/2,'zu x',b[1]/2,'z',b[0]/2,'abst m',round(dd.min()/2,1),'WV dort',round(float(WV[b[0],b[1]]),2),'Boden dazw min/max',round(float(G[min(a[0],b[0]):max(a[0],b[0])+1,min(a[1],b[1]):max(a[1],b[1])+1].min()),2),round(float(G[min(a[0],b[0]):max(a[0],b[0])+1,min(a[1],b[1]):max(a[1],b[1])+1].max()),2))
