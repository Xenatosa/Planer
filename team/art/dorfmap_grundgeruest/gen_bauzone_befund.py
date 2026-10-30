# t16u: Befund, wo die Bauzone (bebaubar) für die Quellplätze WACHSTUM E16 / AUSBAU E40 nicht reicht. Keine eigenen Standorte.
import csv,json,numpy as np,cv2
from collections import Counter,defaultdict
from PIL import Image
Z=list(csv.DictReader(open('raster_c20_z25_zellen.csv')));nx=336;ny=303
A=lambda k:np.array([r[k] for r in Z]).reshape(ny,nx)
ug=A('untergrund');beg=A('begehbar')=='1';beb=A('bebaubar')=='1'
frei=beg&np.isin(ug,['SCHNEE','BODEN','SAND'])
def gebiet(cx,cy):
    if cy>=215: return 'Sued (Flussband)'
    if cx<150 and cy<100: return 'Nordwest-Ebene'
    if cx<150: return 'West-Tal'
    if cy<100 and cx>=250: return 'Nordost-Rand'
    return 'Senke-Rand'
R=[r for r in csv.DictReader(open('pruefung/t16u_plaetze_gegen_bebaubar.csv'))]
D=json.load(open('pruefung/quelle_plaetze_wachstum_ausbau_planm.json'))
out=[];erw={s:np.zeros((ny,nx),bool) for s in D}; blk={s:np.zeros((ny,nx),bool) for s in D}
for st,L in D.items():
    by={str(p['id']):p for p in L}
    for r in R:
        if r['stand']!=st or r['befund']=='innerhalb_bebaubar': continue
        m=np.zeros((ny,nx),np.uint8);cv2.fillPoly(m,[np.array([[(x+200)*1.2,(y+40)*1.2] for x,y in by[r['id']]['poly']],np.int32)],1);m=m>0
        f=float(frei[m].mean()); erw[st]|=m&frei&~beb; blk[st]|=m&~frei
        out.append(dict(stand=st,id=r['id'],typ=r['typ'],epoche=r['epoche'],cx=int(r['cx']),cy=int(r['cy']),gebiet=gebiet(int(r['cx']),int(r['cy'])),befund=r['befund'],anteil_gelaende_frei=round(f,3),
          loesung='Bauzone erweitern' if f>=0.95 else 'Bauzone erweitern + Platz kleiner/verschieben (Wald/Eis/Wand im Platz)'))
S=defaultdict(Counter)
for o in out: S[o['stand']][o['gebiet']]+=1
json.dump(dict(regel='Platz gilt als innerhalb, wenn >=95 % seiner Zellen bebaubar [A]; Umrechnung px=(x+200)*30, Zelle=px/25 (Plan-m*1,2)',
  zusammenfassung={s:dict(c) for s,c in S.items()},erweiterung_m2={s:int(erw[s].sum()) for s in D},gesperrt_im_platz_m2={s:int(blk[s].sum()) for s in D},plaetze=out),
  open('overlay_plaetze_erweiterung.json','w'),ensure_ascii=False,indent=1)
with open('overlay_plaetze_erweiterung.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
img=np.asarray(Image.open('raster_c20_z25_vorschau.png').convert('RGB'))[:ny*3,:nx*3].astype(float)*0.5+127
up=lambda q:np.repeat(np.repeat(q,3,0),3,1)
img[up(beb)]=img[up(beb)]*0.6+np.array([0,170,60])*0.4; img[up(erw['E40'])]=(255,140,0); img[up(erw['E16'])]=(200,0,200); img[up(blk['E40'])]=(220,0,0)
Image.fromarray(img.astype(np.uint8)).save('overlay_plaetze_erweiterung.png')
print({s:dict(c) for s,c in S.items()},{s:int(erw[s].sum()) for s in D},{s:int(blk[s].sum()) for s in D})
