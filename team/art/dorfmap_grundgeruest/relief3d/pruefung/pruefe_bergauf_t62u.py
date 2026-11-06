# t62u: nie bergauf? Jede Wasserstelle braucht einen Weg zum Abfluss (Kartenrand oder Becken), der nie steigt [S]
import sys,json,numpy as np,scipy.ndimage as nd
sys.path.insert(0,'.');from fluss_t62u import _flut
from skimage.morphology import h_minima
d=np.load(sys.argv[1]);W=d['WV'].astype(float);M=W>-900;lab,n=nd.label(M,np.ones((3,3)));r={'stuecke':int(n),'bergauf_gt_2cm_mit_becken':0,'max_bergauf_m':0.0,'becken_ohne_randabfluss':0,'stufen_gt_30cm':0,'stufe_max_m':0.0}
for c in range(1,n+1):
    m=lab==c;A=np.where(m,W,W[m].max()+5);mi=h_minima(A,0.02).astype(bool)&m
    P,o,pred,S=_flut(m,W,mi);u=S-W[m];r['bergauf_gt_2cm_mit_becken']+=int((u>0.02).sum());r['max_bergauf_m']=max(r['max_bergauf_m'],round(float(u.max()),3))
    ed=np.zeros(m.shape,bool);ed[0,:]=ed[-1,:]=ed[:,0]=ed[:,-1]=True;bl,bn=nd.label(nd.binary_dilation(mi,iterations=1)&m,np.ones((3,3)))
    r['becken_ohne_randabfluss']+=sum(1 for b in range(1,bn+1) if not (ed&(bl==b)).any())-(0 if (ed&m).any() else 1)   # tiefster Punkt eines Stueckes ohne Rand = Endsee, zaehlt nicht
    dz=[];w=W[m]
    for v in range(len(P)):
        if pred[v]>=0:dz.append(w[v]-w[pred[v]])
    dz=np.array(dz) if dz else np.zeros(1);r['stufen_gt_30cm']+=int((dz>0.3).sum());r['stufe_max_m']=max(r['stufe_max_m'],round(float(dz.max()),2))
print(json.dumps(r))
