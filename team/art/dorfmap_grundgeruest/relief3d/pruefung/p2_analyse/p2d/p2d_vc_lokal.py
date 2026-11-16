# P2d: nach gen_textur.py vc VC und FW.c ausserhalb von 8 Zellen um die P2d-Aenderungen (GB + VC aus p2d_rueck.npz) auf den
# Vorher-Stand zuruecksetzen (relief_daten + relief_neu). Aufruf (relief3d/): python3 pruefung/p2_analyse/p2d/p2d_vc_lokal.py VORHER.json.gz VORHER_NEU.json.gz [A]
import sys,json,gzip,base64,pathlib,numpy as np
from scipy import ndimage as nd
sys.path.insert(0,'.');import relief_l3 as L3
r=np.load('pruefung/p2_analyse/p2d/p2d_rueck.npz',allow_pickle=True)
for pfad,vor,kompakt in (('relief_daten.json.gz',sys.argv[1],False),('neu/relief_neu.json.gz',sys.argv[2],True)):
    D=json.load(gzip.open(pfad));A=json.load(gzip.open(vor));GY,GX=D['ny']*2+1,D['nx']*2+1
    m=np.zeros(GY*GX,bool);m[r['idx']]=True;m[r['vc_idx']]=True;m=nd.binary_dilation(m.reshape(GY,GX),iterations=16)
    x0,z0,x1,z1=L3.D2_BOX;m[z0*2:z1*2+1,x0*2:x1*2+1]=False
    vn=np.frombuffer(base64.b64decode(D['VC']),np.uint8).reshape(GY,GX,3).copy();va=np.frombuffer(base64.b64decode(A['VC']),np.uint8).reshape(GY,GX,3)
    n0=int((vn!=va).any(-1).sum());vn[~m]=va[~m];D['VC']=base64.b64encode(vn.tobytes()).decode()
    FS=D['FW']['fs'];FX=D['nx']*FS+1;vid=np.frombuffer(base64.b64decode(D['FW']['vid']),np.uint32).astype(np.int64)
    cn=np.frombuffer(base64.b64decode(D['FW']['c']),np.uint8).reshape(-1,3).copy();ca=np.frombuffer(base64.b64decode(A['FW']['c']),np.uint8).reshape(-1,3)
    gi=np.clip(np.rint((vid//FX)/FS*2).astype(int),0,GY-1);gj=np.clip(np.rint((vid%FX)/FS*2).astype(int),0,GX-1);aus=~m[gi,gj]
    f0=int((cn!=ca).any(-1).sum());cn[aus]=ca[aus];D['FW']['c']=base64.b64encode(cn.tobytes()).decode()
    L3._schreibe(D,pathlib.Path(pfad),kompakt)
    print(pfad,'vc_geaendert',n0,'->',int((vn!=va).any(-1).sum()),'fw_c',f0,'->',int((cn!=ca).any(-1).sum()))
