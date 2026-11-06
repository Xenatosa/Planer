import json,math,numpy as np
from raster_def import *
H=hoehen(); K=[]; FW,FH=900,675
for f in felder():
    xc=(f['cx0']+f['cx1']+1)/2; zc=(f['cy0']+f['cy1']+1)/2
    hc=float(np.median(H[f['cy0']:f['cy1']+1,f['cx0']:f['cx1']+1]))
    K.append(dict(name='feld_'+f['feld'],p=[xc,hc+72,zc+64],t=[xc,hc,zc],w=FW,h=FH))
json.dump(K,open(os.path.join(HIER,'kameras_felder.json')+'','w'))
OW,OH=1080,975; h=(NY/2+4)/math.tan(math.radians(25))
json.dump([dict(name='uebersicht_roh',p=[NX/2,h,NY/2+0.01],t=[NX/2,0,NY/2],w=OW,h=OH)],open(os.path.join(HIER,'kameras_uebersicht.json')+'','w'))
print(len(K),h)
