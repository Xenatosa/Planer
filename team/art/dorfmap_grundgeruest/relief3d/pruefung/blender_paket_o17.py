"""O17 B: Blender-Paket aus dem Viewer-Dump (pruefung/blender_dump_o17.js). Nur Gelaende, Wasser, Baeume, Felsen/Steine/Gras.
Keine Gebaeude, keine Wege, keine Spielfigur. 1 Einheit = 1 m, Y oben (glTF), Vertexfarben COLOR_0, keine Texturen.
Aufruf: python3 pruefung/blender_paket_o17.py /tmp/o17_dump.json /workspace/dorfmap_blender_O17/dorfmap_O17.glb [A]"""
import json,base64,sys,numpy as np,trimesh
R=json.load(open(sys.argv[1]));f=lambda s:np.frombuffer(base64.b64decode(s),np.float32)
NAM={0:'gelaende_grobnetz',1:'gelaende_feinband_waende',2:'gelaende_rand_sockel',3:'gelaende_bodenplatte'}
sc=trimesh.Scene();zahl={};gi=0;grp={}
for r in R:
    e=r['ebene']
    if e in('wege','gebaeude','mensch') or not r['sichtbar'] or r['n']==0:continue
    P=f(r['pos']).reshape(-1,r['pi']).astype(float);n=len(P)
    T=np.frombuffer(base64.b64decode(r['idx']),np.uint32).reshape(-1,3) if r['idx'] else np.arange(n).reshape(-1,3)
    if r['col']:C=f(r['col']).reshape(-1,r['ci'])[:,:3]
    else:C=np.tile(np.array([int(r['farbe'][i:i+2],16)/255 for i in(0,2,4)]),(n,1))
    MW=np.array(r['mw']).reshape(4,4).T
    if r['inst']:
        IM=f(r['inst']).reshape(-1,4,4).transpose(0,2,1);IC=f(r['icol']).reshape(-1,3) if r['icol'] else None
        H=np.c_[P,np.ones(n)];PP=[];TT=[];CC=[]
        for k,m in enumerate(IM):
            PP.append((H@(MW@m).T)[:,:3]);TT.append(T+k*n);CC.append(C*IC[k] if IC is not None else C)
        P,T,C=np.concatenate(PP),np.concatenate(TT),np.concatenate(CC)
    else:P=(np.c_[P,np.ones(n)]@MW.T)[:,:3]
    if e=='gelaende':nm=NAM.get(gi,'gelaende_%d'%gi);gi+=1
    elif e=='wasser':nm='wasser'
    else:nm=e;grp[e]=grp.get(e,0)+1;nm='%s_%d'%(e,grp[e])
    VC=np.c_[np.clip(C,0,1)*255,np.full(len(C),255)].astype(np.uint8)
    sc.add_geometry(trimesh.Trimesh(P,T,vertex_colors=VC,process=False),nm,geom_name=nm);zahl[nm]=int(len(T))
sc.export(sys.argv[2]);json.dump({'dreiecke':zahl,'summe':sum(zahl.values())},open(sys.argv[2].replace('.glb','_inhalt.json'),'w'),indent=1)
print(zahl,sum(zahl.values()))
