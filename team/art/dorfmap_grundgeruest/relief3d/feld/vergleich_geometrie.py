# Vergleicht Dreiecksmengen (Weltkoordinaten-Vertices + Farben) je Mesh zweier Dumps. Aufruf: python3 feld/vergleich_geometrie.py dump.json
import json,sys,base64,hashlib,numpy as np
R=json.load(open(sys.argv[1]));(fa,A),(fb,B)=list(R.items())
def tris(m):
    P=np.frombuffer(base64.b64decode(m['pos']),np.float32).reshape(-1,m['pi'])
    C=np.frombuffer(base64.b64decode(m['col']),np.float32).reshape(-1,m['ci']) if m['col'] else np.zeros((len(P),0),np.float32)
    I=np.frombuffer(base64.b64decode(m['idx']),np.uint32) if m['idx'] else np.arange(len(P),dtype=np.uint32)
    k=3 if len(I)%3==0 else 1
    V=np.concatenate([P,C],1)[I].reshape(-1,k*(P.shape[1]+C.shape[1]))
    if m['inst']:return np.unique(V,axis=0),np.frombuffer(base64.b64decode(m['inst']),np.float32).reshape(-1,16)
    return np.unique(V,axis=0),None
print(len(A),len(B),'meshes');bad=0;tot=0
for i,(a,b) in enumerate(zip(A,B)):
    ta,ia=tris(a);tb,ib=tris(b);same=ta.shape==tb.shape and ta.tobytes()==tb.tobytes()
    si=True if ia is None else (ib is not None and np.array_equal(np.unique(ia,axis=0),np.unique(ib,axis=0)))
    tot+=len(ta)
    if not(same and si):bad+=1;print('UNGLEICH',i,a['ebene'],a['name'],ta.shape,tb.shape,'inst',None if ia is None else (len(ia),len(ib)))
print(json.dumps(dict(meshes=len(A),ungleich=bad,dreiecke_a=tot,gleich=bad==0 and len(A)==len(B))))
