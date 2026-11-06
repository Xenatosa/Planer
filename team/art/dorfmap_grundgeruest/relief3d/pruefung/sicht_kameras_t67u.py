# t67u Runde O C: Nahkamera-Raster (Wandbaender, Gipfel, Krater, Raender, Fluss, Rampen); Kamera frei (Sichtlinie ueber Gelaende, >5 m von Baeumen/Haeusern) [A]
import sys,json,gzip,base64,numpy as np,scipy.ndimage as nd
F=np.load(sys.argv[1]);FH=F['FH'].astype(float);vin=F['vin'];D=json.load(gzip.open('relief_daten.json.gz'))
GB=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(607,673).astype(float)
HH=np.where(vin,FH,nd.zoom(GB,(FH.shape[0]/607,FH.shape[1]/673),order=1)[:FH.shape[0],:FH.shape[1]])
def h(x,z):return float(HH[min(max(int(z*4),0),HH.shape[0]-1),min(max(int(x*4),0),HH.shape[1]-1)])
B=np.array([[b[0],b[2]] for b in D['baeume']]);Hs=np.array([[o['x'],o['z']] for o in D['haeuser']])
def frei(x,z):
    if len(B) and (np.hypot(B[:,0]-x,B[:,1]-z)<5).any():return False
    if (np.hypot(Hs[:,0]-x,Hs[:,1]-z)<9).any():return False
    return 1<x<335 and 1<z<302
def kam(n,x,z,dist=14,up=6):
    best=None;ht=h(x,z)
    for a in np.linspace(0,2*np.pi,24,endpoint=False):
        for dd in (dist,dist*0.7,dist*1.3):
            cx,cz=x+dd*np.cos(a),z+dd*np.sin(a)
            if not frei(cx,cz):continue
            cy=max(h(cx,cz),ht)+up
            ok=all(h(x+(cx-x)*t,z+(cz-z)*t)<ht+(cy-ht)*t-0.8 for t in np.linspace(0.15,1,14))
            if ok:
                sc=h(cx,cz)
                if best is None or sc<best[0]:best=(sc,cx,cy,cz)
        if best:break
    if not best:return None
    return [n,[round(best[1],1),round(best[2],1),round(best[3],1)],[round(x,1),round(ht,1),round(z,1)]]
C=[];sl=np.degrees(np.arctan(np.hypot(*np.gradient(nd.gaussian_filter(FH,2),0.25))))
# Wandbaender: 24-m-Raster ueber steile Punkte
for zz in range(0,303,24):
    for xx in range(0,336,24):
        m=(sl[zz*4:(zz+24)*4,xx*4:(xx+24)*4]>45)&vin[zz*4:(zz+24)*4,xx*4:(xx+24)*4]
        if m.sum()>200:
            j,i=np.argwhere(m)[m.sum()//2];C.append(('wand_%d_%d'%(xx,zz),xx+i/4,zz+j/4))
# Gipfel
mx=(FH==nd.maximum_filter(FH,120))&vin;pk=np.argwhere(mx);pk=sorted(pk,key=lambda p:-FH[p[0],p[1]])[:10]
for k,(j,i) in enumerate(pk):C.append(('gipfel_%d'%k,i/4,j/4))
for k,(x,z) in enumerate([(103,155),(95,145),(111,165),(95,165)]):C.append(('krater_%d'%k,x,z))
for k,(x,z) in enumerate([(3,60),(3,150),(3,246),(333,80),(333,200),(333,280),(80,3),(215,3),(150,300),(280,300)]):C.append(('rand_%d'%k,x,z))
WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(607,673);J,I=np.nonzero(WV>-900)
for k in range(0,len(J),len(J)//10):C.append(('fluss_%d'%(k//(len(J)//10)),I[k]/2,J[k]/2))
for k,pl in enumerate(D['rampenwege']):p=pl[len(pl)//2];C.append(('rampe_%d'%k,p[0],p[1]))
out=[];fehl=[]
for n,x,z in C:
    c=kam(n,x,z)
    (out.append(c) if c else fehl.append(n))
json.dump(out,open(sys.argv[2],'w'));print(len(C),'kameras',len(out),'ohne',fehl)
