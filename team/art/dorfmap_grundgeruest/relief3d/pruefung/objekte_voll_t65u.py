# t65u Runde M2: alle Objekte gegen Viewer-Raycast (strahl.json aus test_strahl_t62u.js) + Daten: schwebend/versunken >0,15 m, Wasser, Hang >45 Grad, Baum-Ueberlappung, Baumabstand. python3 ... strahl.json [S]
import json,gzip,sys,base64,numpy as np
from scipy.spatial import cKDTree
D=json.load(gzip.open('relief_daten.json.gz'));S=json.load(open(sys.argv[1]))
GB=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(607,673).astype(float);WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(607,673)
gy,gx=np.gradient(GB,0.5);SL=np.degrees(np.arctan(np.hypot(gx,gy)))
ALT={'baeume':(80.1,174.9),'steine':[(276.1,267.1),(308.0,273.5)],'geroell':[(149.4,31.2),(271.2,116.2),(271.3,116.6)]}
R={};ORTE={}
for k in ('baeume','felsen','findlinge','steine','geroell'):
    L=D[k];c=dict(n=len(L),schwebend_gt_0_15=0,versunken_gt_0_15=0,im_wasser=0,hang_gt_45=0);o_=[]
    for o,(g,w) in zip(L,S[k]):
        if g is None:continue
        if k=='baeume':d=o[1]-0.3-g;s=d>0.15;v=d<-0.15
        else:d=o[1]-g;s=d>0.15;v=d<-0.25*o[3]-0.15
        c['schwebend_gt_0_15']+=s;c['versunken_gt_0_15']+=v
        if s or v:o_.append([o[0],o[2],round(d,2)])
        fuss=o[1]-0.3 if k=='baeume' else o[1]
        if w is not None and w>fuss+0.05:c['im_wasser']+=1
        c['hang_gt_45']+=bool(SL[min(int(round(o[2]*2)),606),min(int(round(o[0]*2)),672)]>45 and o[1]-GB[min(int(round(o[2]*2)),606),min(int(round(o[0]*2)),672)]<1)
    R[k]=c;ORTE[k]=o_[:30]
B=D['baeume'];P=np.array([[o[0],o[2]] for o in B]);T=cKDTree(P);dd,_=T.query(P,2);nn=dd[:,1]
R['baeume']['abstand_naechster_m']={'min':round(float(nn.min()),2),'p10':round(float(np.percentile(nn,10)),2),'median':round(float(np.median(nn)),2)}
R['baeume']['ueber_haus']=sum(any(abs(o[0]-h['x'])<h['b']/2 and abs(o[2]-h['z'])<h['t']/2 for h in D['haeuser']) for o in B)
near=lambda x,z,L,r:min([np.hypot(x-p[0],z-p[1]) for p in L] or [99])<r
R['alte_ausreisser']={}
for k,v in ALT.items():
    for x,z in (v if isinstance(v,list) else [v]):
        m=[(o,s) for o,s in zip(D[k],S[k]) if np.hypot(o[0]-x,o[2]-z)<0.3]
        R['alte_ausreisser'][f'{k} {x}|{z}']=('entfernt' if not m else [round((o[1]-(0.3 if k=='baeume' else 0))-s[0],2) for o,s in m])
R['orte']=ORTE;json.dump(R,open('pruefung/objekte_voll_t65u.json','w'),indent=1);print(json.dumps({k:v for k,v in R.items() if k!='orte'}))
