# P2b-Zusatz (QA P4c, Gate R1_blind rampe_5): milchiges, texturarmes Band entlang rampe_5 (D4/D5).
# Ursache [S]: VC ist dort ein glatter, fleckenloser Bereich (Fleck-Energie ~0,14 statt ~4 daneben), Rest einer frueheren Rampen-Glaettung.
# Abhilfe: nur Farbe (VC + FW.c), Hoehen/Wasser/Wege bleiben bytegleich. Im texturarmen Bereich um rampe_5 wird das
# Fleckmuster (VC minus Weichzeichnung) aus einem 22 Zellen westlich versetzten, normal texturierten Streifen aufgesetzt,
# mit weichem Rand (3 Knoten). Grundton bleibt. Aufruf in relief3d/ nach gen_textur.py vc.
import sys,json,gzip,base64,pathlib,numpy as np
from scipy import ndimage as nd
sys.path.insert(0,'.');import relief_l3 as L3
DX=-44   # Versatz in GB-Knoten (rs=2) = 22 Zellen
def maske(D):
    GY,GX=D['ny']*2+1,D['nx']*2+1;V=np.frombuffer(base64.b64decode(D['VC']),np.uint8).reshape(GY,GX,3).astype(float)
    L=V.mean(-1);hp=nd.uniform_filter(np.abs(L-nd.gaussian_filter(L,2)),11)   # Fleck-Energie
    P=np.array(D['rampenwege'][5]);lin=np.zeros((GY,GX),bool)
    for x,z in P: lin[int(round(z*2)),int(round(x*2))]=True
    nah=nd.distance_transform_edt(~lin)<=40          # 20 Zellen um rampe_5
    m=(hp<0.6)&nah;m=nd.binary_opening(m,iterations=2)
    lab,n=nd.label(m);gr=nd.sum(m,lab,range(1,n+1));keep=np.isin(lab,1+np.flatnonzero(gr>=400))
    keep=nd.binary_closing(keep,iterations=3);x0,z0,x1,z1=L3.D2_BOX;keep[z0*2:z1*2+1,x0*2:x1*2+1]=False
    return keep,V
def main():
    for pfad,kompakt in (('relief_daten.json.gz',False),('neu/relief_neu.json.gz',True)):
        D=json.load(gzip.open(pfad));GY,GX=D['ny']*2+1,D['nx']*2+1
        m,V=maske(D)
        w=np.clip(nd.distance_transform_edt(m)/3.0,0,1);w=w*w*(3-2*w)
        S=np.roll(V,DX,axis=1);det=S-nd.gaussian_filter(S,(3,3,0))
        Vn=np.clip(V+w[...,None]*det,0,255).round().astype(np.uint8);ge=(Vn!=V.astype(np.uint8)).any(-1)
        D['VC']=base64.b64encode(Vn.tobytes()).decode()
        FW=D['FW'];FS=int(FW['fs']);FX=D['nx']*FS+1;vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32).astype(np.int64)
        gi=np.clip(np.rint((vid//FX)/FS*2).astype(int),0,GY-1);gj=np.clip(np.rint((vid%FX)/FS*2).astype(int),0,GX-1)
        c=np.frombuffer(base64.b64decode(FW['c']),np.uint8).reshape(-1,3).copy();sel=ge[gi,gj];c[sel]=Vn[gi[sel],gj[sel]]
        FW['c']=base64.b64encode(c.tobytes()).decode()
        L3._schreibe(D,pathlib.Path(pfad),kompakt);print(pfad,'maske',int(m.sum()),'vc_geaendert',int(ge.sum()),'fw_c',int(sel.sum()))
main()
