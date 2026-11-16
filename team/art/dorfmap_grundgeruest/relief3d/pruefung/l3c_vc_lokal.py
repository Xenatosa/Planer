# L3c (16.11.2026, nach P2b/P2c): gen_textur.py vc rechnet die Farben (VC, FW.c) ueberall neu und wuerde damit auch
# P2b-Farbarbeit (p2b_r5_textur rampe_5, p2b_vc_lokal) ueberschreiben. Darum nach gen_textur.py vc: VC und FW.c ausserhalb
# von 8 Zellen um die L3c-Aenderungen (GB/WV aus pruefung/l3c_rueck.npz) auf den Vorher-Stand zuruecksetzen; innerhalb
# werden die Vorher-Werte in pruefung/l3c_vc_rueck.npz gesichert (Rueckweg).
#   python3 pruefung/l3c_vc_lokal.py VORHER.json.gz VORHER_NEU.json.gz     (relief3d/, nach gen_textur.py vc)
#   python3 pruefung/l3c_vc_lokal.py --aus                                  (nach relief_l3.py --stufe-c --aus)
import sys,json,gzip,base64,pathlib,numpy as np
from scipy import ndimage as nd
sys.path.insert(0,'.');import relief_l3 as L3
RV=pathlib.Path('pruefung/l3c_vc_rueck.npz')
DATEIEN=(('relief_daten.json.gz',False),('neu/relief_neu.json.gz',True))
if sys.argv[1]=='--aus':
    r=np.load(RV)
    for k,(pfad,kompakt) in enumerate(DATEIEN):
        D=json.load(gzip.open(pfad))
        vc=np.frombuffer(base64.b64decode(D['VC']),np.uint8).reshape(-1,3).copy();vc[r['vc_idx']]=r['vc_alt'];D['VC']=base64.b64encode(vc.tobytes()).decode()
        c=np.frombuffer(base64.b64decode(D['FW']['c']),np.uint8).reshape(-1,3).copy();c[r['fc_idx']]=r['fc_alt'];D['FW']['c']=base64.b64encode(c.tobytes()).decode()
        L3._schreibe(D,pathlib.Path(pfad),kompakt)
    RV.unlink();print('l3c_vc aus');sys.exit(0)
r=np.load('pruefung/l3c_rueck.npz');out={}
for k,((pfad,kompakt),vor) in enumerate(zip(DATEIEN,sys.argv[1:3])):
    D=json.load(gzip.open(pfad));A=json.load(gzip.open(vor));GY,GX=D['ny']*2+1,D['nx']*2+1
    m=np.zeros(GY*GX,bool);m[r['idx']]=True;m[r['wv_idx']]=True;m=nd.binary_dilation(m.reshape(GY,GX),iterations=16)
    vn=np.frombuffer(base64.b64decode(D['VC']),np.uint8).reshape(GY,GX,3).copy();va=np.frombuffer(base64.b64decode(A['VC']),np.uint8).reshape(GY,GX,3)
    n0=int((vn!=va).any(-1).sum());vn[~m]=va[~m];D['VC']=base64.b64encode(vn.tobytes()).decode()
    FS=D['FW']['fs'];FX=D['nx']*FS+1;vid=np.frombuffer(base64.b64decode(D['FW']['vid']),np.uint32).astype(np.int64)
    cn=np.frombuffer(base64.b64decode(D['FW']['c']),np.uint8).reshape(-1,3).copy();ca=np.frombuffer(base64.b64decode(A['FW']['c']),np.uint8).reshape(-1,3)
    gi=np.clip(np.rint((vid//FX)/FS*2).astype(int),0,GY-1);gj=np.clip(np.rint((vid%FX)/FS*2).astype(int),0,GX-1);aus=~m[gi,gj]
    f0=int((cn!=ca).any(-1).sum());cn[aus]=ca[aus];D['FW']['c']=base64.b64encode(cn.tobytes()).decode()
    if k==0:
        vi=np.flatnonzero((vn!=va).any(-1).reshape(-1));fi=np.flatnonzero((cn!=ca).any(-1))
        out=dict(vc_idx=vi,vc_alt=va.reshape(-1,3)[vi],fc_idx=fi,fc_alt=ca[fi])
    L3._schreibe(D,pathlib.Path(pfad),kompakt)
    print(pfad,'vc_geaendert',n0,'->',int((vn!=va).any(-1).sum()),'fw_c',f0,'->',int((cn!=ca).any(-1).sum()))
np.savez_compressed(RV,**out)
