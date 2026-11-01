# t67u Runde O A: Fehlerzaehler Feinrelief (FW_NPZ-Dump) + Objekte auf Wegen + Flussenden [S]
# Schwellen: Spitze = lok. Max (7x7) und >0,8 m ueber Median 11x11 (2,75 m) ; Nadel = Spitze mit >1,5 m ;
# Senke = Fuelltiefe (FH) - Fuelltiefe (FB, Grobform) > 0,8 m, Cluster >= 4 Punkte ; enger Grat = Kruemmung lap(FH,sig0.5)<-1,2/m bei Hoehe > Median+0,5 ;
# Stufe Feinband = |FH-FB| > 0,3 m auf Bandrand ; Objekt auf Weg = Abstand < 1,5 m + 0,5*h ; Flussende = Strang-Endpunkt (Skelett) > 1 m vom Rand und nicht in See
import sys,json,gzip,base64,numpy as np,scipy.ndimage as nd
from skimage.morphology import reconstruction
npz,out=sys.argv[1],sys.argv[2];d=np.load(npz);FH=d['FH'].astype(float);FB=d['FB'].astype(float);vin=d['vin']
med=nd.median_filter(FH,11);mx=nd.maximum_filter(FH,7)
def fuell(A):
    s=A.copy();s[1:-1,1:-1]=A.max();return reconstruction(s,A,method='erosion')
dep=(fuell(FH)-FH)-(fuell(FB)-FB)
lap=nd.laplace(nd.gaussian_filter(FH,2))*16
def cl(m,mn=1):
    l,n=nd.label(m);s=np.bincount(l.ravel())[1:];return int((s>=mn).sum()),l,s
inn=vin&nd.binary_erosion(vin,iterations=3)
R={}
sp=inn&(FH>=mx)&(FH-med>0.8);R['spitzen']=cl(sp)[0];R['nadeln_1_5m']=cl(sp&(FH-med>1.5))[0]
n,l,s=cl(inn&(dep>0.8),4);R['senken_0_8m']=n;R['senken_2m']=cl(inn&(dep>2.0),4)[0]
R['senke_max_m']=round(float((dep*inn).max()),2)
R['enge_grate']=cl(inn&(lap<-1.2)&(FH-med>0.5),3)[0]
rb=vin&~nd.binary_erosion(vin);R['stufe_bandrand']=int((rb&(np.abs(FH-FB)>0.3)).sum())
J,I=np.nonzero(sp&(FH-med>1.5));R['nadel_orte_xz']=[[round(i/4,1),round(j/4,1),round(float(FH[j,i]-med[j,i]),2)] for j,i in list(zip(J,I))[:400:20]]
J,I=np.nonzero(inn&(dep>2.0));R['senke_orte_xz']=[[round(i/4,1),round(j/4,1),round(float(dep[j,i]),2)] for j,i in list(zip(J,I))[::max(1,len(J)//20)]]
if len(sys.argv)>3:
    import csv
    D=json.load(gzip.open(sys.argv[3]));sys.path.insert(0,'.');import runde_o_t67u as RO
    OV=list(csv.DictReader(open(sys.argv[4]))) if len(sys.argv)>4 else []
    DI=RO.frei_maske(OV,D['rampenwege'],D['bruecken'],D['wege'],D['nx'],D['ny'])
    z={}
    for nm in['baeume','felsen','findlinge','steine','geroell']:
        z[nm]=sum(1 for o in D[nm] if DI[min(int(o[2]*4),DI.shape[0]-1),min(int(o[0]*4),DI.shape[1]-1)]<1.5+0.5*o[3])
    R['objekte_auf_wegen']=z
    WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(607,673);w=WV>-900
    from skimage.morphology import skeletonize
    sk=skeletonize(w);nb=nd.convolve(sk.astype(int),np.ones((3,3)),mode='constant')-1
    ends=np.argwhere(sk&(nb==1));lab,_=nd.label(w,np.ones((3,3)));gr=np.bincount(lab.ravel())
    br=nd.distance_transform_edt(w)
    fe=[]
    for j,i in ends:
        if min(j,i,606-j,672-i)<=2:continue
        if gr[lab[j,i]]<200:continue   # Tuempel/See
        win=WV[max(0,j-6):j+7,max(0,i-6):i+7];ww=win[win>-900]
        if WV[j,i]>ww.mean()-0.01:continue   # Quelle (oberes Ende), kein Austritt
        fe.append([i/2,j/2,round(float(WV[j,i]),2)])
    R['flussenden_blind']=len(fe);R['flussenden_orte_xz']=fe[:30]
json.dump(R,open(out,'w'),indent=1);print({k:v for k,v in R.items() if 'orte' not in k})
