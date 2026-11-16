# P2: SHA-256 der D2-Ausschnitte (Zellen x126-168, z43-86, rs=2) aus relief_daten.json.gz. Soll: GB 749d3c4b..., VC b67dc719...
import json,gzip,base64,hashlib,sys,numpy as np
D=json.load(gzip.open(sys.argv[1] if len(sys.argv)>1 else 'relief_daten.json.gz'));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
x0,z0,x1,z1=126,43,168,86;sl=(slice(z0*RS,z1*RS+1),slice(x0*RS,x1*RS+1))
for k,t,n in (('GB',np.float32,1),('VC',np.uint8,3),('WV',np.float32,1),('WEGA',np.uint8,1)):
    a=np.frombuffer(base64.b64decode(D[k]),t).reshape((GY,GX,3) if n==3 else (GY,GX))
    print('D2_'+k,hashlib.sha256(np.ascontiguousarray(a[sl]).tobytes()).hexdigest())
