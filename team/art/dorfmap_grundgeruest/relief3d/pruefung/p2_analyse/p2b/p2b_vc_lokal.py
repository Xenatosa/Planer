# P2b: gen_textur.py vc aendert auf dem L3-Stand auch Kachel E4 (222 VC-Punkte, weit weg von den P2b-Stellen; GB dort unveraendert)
# -> T1 E4 175|144 neu. Nach gen_textur.py vc: VC und FW.c ausserhalb von 8 Zellen um die P2b-GB-Aenderungen auf den Vorher-Stand
# zuruecksetzen (relief_daten + relief_neu). Aufruf (relief3d/): python3 pruefung/p2_analyse/p2b/p2b_vc_lokal.py VORHER.json.gz VORHER_NEU.json.gz [A]
import sys,json,gzip,base64,numpy as np
from scipy import ndimage as nd
sys.path.insert(0,'.');import relief_l3 as L3
r=np.load('pruefung/p2_analyse/p2b/p2b_rueck.npz')
for pfad,vor,kompakt in (('relief_daten.json.gz',sys.argv[1],False),('neu/relief_neu.json.gz',sys.argv[2],True)):
    D=json.load(gzip.open(pfad));A=json.load(gzip.open(vor));GY,GX=D['ny']*2+1,D['nx']*2+1
    m=np.zeros(GY*GX,bool);m[r['idx']]=True;m=nd.binary_dilation(m.reshape(GY,GX),iterations=16)
    vn=np.frombuffer(base64.b64decode(D['VC']),np.uint8).reshape(GY,GX,3).copy();va=np.frombuffer(base64.b64decode(A['VC']),np.uint8).reshape(GY,GX,3)
    n0=int((vn!=va).any(-1).sum());vn[~m]=va[~m];D['VC']=base64.b64encode(vn.tobytes()).decode()
    FS=D['FW']['fs'];FX=D['nx']*FS+1;vid=np.frombuffer(base64.b64decode(D['FW']['vid']),np.uint32).astype(np.int64)
    cn=np.frombuffer(base64.b64decode(D['FW']['c']),np.uint8).reshape(-1,3).copy();ca=np.frombuffer(base64.b64decode(A['FW']['c']),np.uint8).reshape(-1,3)
    gi=np.clip(np.rint((vid//FX)/FS*2).astype(int),0,GY-1);gj=np.clip(np.rint((vid%FX)/FS*2).astype(int),0,GX-1);aus=~m[gi,gj]
    f0=int((cn!=ca).any(-1).sum());cn[aus]=ca[aus];D['FW']['c']=base64.b64encode(cn.tobytes()).decode()
    L3._schreibe(D,__import__('pathlib').Path(pfad),kompakt)
    print(pfad,'vc_geaendert',n0,'->',int((vn!=va).any(-1).sum()),'fw_c',f0,'->',int((cn!=ca).any(-1).sum()))
