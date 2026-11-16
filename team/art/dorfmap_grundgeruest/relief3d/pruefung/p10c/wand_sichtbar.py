#!/usr/bin/env python3
# P10c: Anteil Wandvertices ueber dem Gelaende je Kachel (vorher/nachher). Aufruf: python3 wand_sichtbar.py <alle_kacheln_vorher.json.gz> <alle_kacheln_nachher.json.gz>
import gzip,json,base64,numpy as np,sys
def lade(p):
    d=json.loads(gzip.decompress(open(p,'rb').read()));A=d['alle_kacheln'];rs=2
    G=np.full((607,673),np.nan,np.float32)
    for t,x in A['tiles'].items():
        P=np.frombuffer(base64.b64decode(x['vertices_xyz_f32']),'<f4').reshape(-1,3)
        G[np.rint(P[:,2]*rs).astype(int),np.rint(P[:,0]*rs).astype(int)]=P[:,1]
    out={}
    for t,w in A['waende']['tiles'].items():
        if not w.get('vertices'): continue
        P=np.frombuffer(base64.b64decode(w['vertices_xyz_f32']),'<f4').reshape(-1,3).astype(float)
        u=np.clip(P[:,0]*rs,0,671.999);v=np.clip(P[:,2]*rs,0,605.999);i=np.floor(u).astype(int);j=np.floor(v).astype(int);fu=u-i;fv=v-j
        g=(G[j,i]*(1-fu)*(1-fv)+G[j,i+1]*fu*(1-fv)+G[j+1,i]*(1-fu)*fv+G[j+1,i+1]*fu*fv)
        ueber=P[:,1]-g
        out[t]={'vertices':len(P),'ueber_gelaende_0_1m':int((ueber>0.1).sum()),'anteil':round(float((ueber>0.1).mean()),3),'max_ueber_m':round(float(ueber.max()),2)}
    return out
a=lade(sys.argv[1]);b=lade(sys.argv[2])
tot=lambda o:(sum(x['vertices'] for x in o.values()),sum(x['ueber_gelaende_0_1m'] for x in o.values()))
print(json.dumps({'vorher':a,'nachher':b,'summe_vorher':tot(a),'summe_nachher':tot(b)}))
