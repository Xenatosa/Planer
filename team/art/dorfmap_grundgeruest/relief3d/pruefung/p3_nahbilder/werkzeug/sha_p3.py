# SHA-Belege: geschuetzte Dateien + Hoehen-/Wege-/Wasserfelder in relief_daten.json.gz. Aufruf aus relief3d/: python3 pruefung/p3_nahbilder/werkzeug/sha_p3.py [relief.json.gz]
import json,gzip,base64,hashlib,numpy as np,sys
f=sys.argv[1] if len(sys.argv)>1 else 'relief_daten.json.gz'
for p in ('neu/zellen_relief.csv','neu/vektor.json','neu/felder.json'):print(p,hashlib.sha256(open(p,'rb').read()).hexdigest())
D=json.load(gzip.open(f));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(GY,GX);x0,z0,x1,z1=126,43,168,86
print('D2-Hoehe (GB D2-Kachel)',hashlib.sha256(G[z0*RS:z1*RS+1,x0*RS:x1*RS+1].astype('<f4').tobytes()).hexdigest())
h=lambda b:hashlib.sha256(b).hexdigest()
for k in ('GB','G','WV','WEGA'):print(k,h(D[k].encode()))
for k in ('h','vid','band','t','s'):print('FW.'+k,h(D['FW'][k].encode()))
for k in ('wege','rampenwege','bruecken','haeuser'):print(k,h(json.dumps(D[k]).encode()))
