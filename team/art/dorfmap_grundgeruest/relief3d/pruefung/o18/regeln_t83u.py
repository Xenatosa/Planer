# t83u/t85u: Fehlerklassen-Metriken auf Anzeige-Gelaende (GB) je Raster-Feld: Mulden nach innen, Spitzen, Wasser ohne Fluss
import json,gzip,base64,numpy as np,scipy.ndimage as nd,os
H=os.path.dirname(os.path.abspath(__file__))
d=json.load(gzip.open(os.path.join(H,'../../relief_daten.json.gz')))
GX,GY=d['nx']*d['rs']+1,d['ny']*d['rs']+1
def f(k):return np.frombuffer(base64.b64decode(d[k]),np.float32).reshape(GY,GX)
GB=f('GB');WV=f('WV');RS=d['rs']
# Mulde: Tiefe unter geschlossener Fuellung (morphologische Rekonstruktion), trockene Ecken
fill=nd.grey_closing(GB,size=(9,9))
mulde=np.where(WV<-900,fill-GB,0)
# Spitze: Hoehe ueber Oeffnung
spitze=GB-nd.grey_opening(GB,size=(5,5))
res={}
for X in range(8):
  for R in range(7):
    s=np.s_[R*43*RS:(R+1)*43*RS,X*42*RS:(X+1)*42*RS]
    m=mulde[s];p=spitze[s]
    res[f"{'ABCDEFGH'[X]}{R+1}"]=dict(mulde_max=round(float(m.max()),2),mulde_ecken_gt1m=int((m>1).sum()),spitze_max=round(float(p.max()),2),spitze_ecken_gt1m=int((p>1).sum()))
json.dump(res,open(os.path.join(H,'regeln_t83u.json'),'w'),indent=1)
for k,v in sorted(res.items(),key=lambda kv:-kv[1]['mulde_ecken_gt1m'])[:15]:print(k,v)
for k in('D1','G1','H1'):print('*',k,res[k])
