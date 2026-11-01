# t65u M2b: Walddichte je 10-m-Zelle vor Runde M (595215f) gegen jetzt; Luecken = Zellen mit >=4 Baeumen vorher und <50 % jetzt. python3 ... alt.json.gz [S]
import json,gzip,sys,numpy as np
from scipy.spatial import cKDTree
A=json.load(gzip.open(sys.argv[1]))['baeume'];B=json.load(gzip.open('relief_daten.json.gz'))['baeume']
a=np.array([[o[0],o[2]] for o in A]);b=np.array([[o[0],o[2]] for o in B])
H=lambda p:np.histogram2d(p[:,0],p[:,1],bins=[34,31],range=[[0,340],[0,310]])[0];ha,hb=H(a),H(b);m=ha>=4
na=cKDTree(a).query(a,2)[0][:,1];nb=cKDTree(b).query(b,2)[0][:,1]
R={'baeume_vorher':len(a),'baeume_jetzt':len(b),'waldzellen_10m':int(m.sum()),'dichte_verlust_mittel':round(float(1-hb[m].sum()/ha[m].sum()),3),
'zellen_verlust_gt_50':[[int(i)*10,int(j)*10,int(ha[i,j]),int(hb[i,j])] for i,j in np.argwhere(m&(hb<0.5*ha))],'zellen_verlust_gt_30':int((m&(hb<0.7*ha)).sum()),
'nn_vorher':{'min':round(float(na.min()),2),'doppelte_lt_0_1m':int((na<0.1).sum()),'median':round(float(np.median(na)),2)},'nn_jetzt':{'min':round(float(nb.min()),2),'median':round(float(np.median(nb)),2)}}
json.dump(R,open('pruefung/wald_dichte_t65u.json','w'),indent=1);print(json.dumps(R))
