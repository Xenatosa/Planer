# Kameras: T1-Nahbilder (je Kachel groesster T1-Treffer aus Basislauf, schraeg+drauf) und Feldansichten (56 Kacheln)
import json,gzip,base64,numpy as np,scipy.ndimage as nd,sys,subprocess
D=json.loads(gzip.decompress(subprocess.check_output(['git','show','8e374b0:./relief_daten.json.gz'])));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(GY,GX).astype(float)
H=lambda x,z:float(nd.map_coordinates(G,[[z*RS],[x*RS]],order=1)[0])
def cam(n,x,z,dx,dy,dz):h=H(x,z);return dict(n=n,pos=[x+dx,h+dy,z+dz],ziel=[x,h,z],az=315,el=45,st=90)
T=[t for t in json.loads(subprocess.check_output(['git','show','8e374b0:./pruefung/regeln_letzter_lauf.json']))['treffer'] if t['regel']=='T1_fleckrand'];best={}
for t in T:
    if t['feld'] not in best or t['wert']>best[t['feld']]['wert']:best[t['feld']]=t
out=sys.argv[1];C=[]
for f,t in sorted(best.items()):C+= [cam(f+'_schraeg',t['x'],t['z'],0,16,12),cam(f+'_drauf',t['x'],t['z'],0,24,0.5)]
json.dump(C,open(out+'/cams_t1.json','w'));json.dump(best,open(out+'/t1_best.json','w'),indent=0)
json.dump([cam('ABCDEFGH'[i]+str(j+1)+'_feld',42*i+21,min(43*j+21.5,302),0,42,36) for j in range(7) for i in range(8)],open(out+'/cams_feld.json','w'))
print(len(C),'T1-Kameras, 56 Feldkameras')
