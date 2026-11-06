# t16u: Plätze aus WACHSTUM (E16) und AUSBAU_E40 (Plan-m, 30 px/m) -> Zellen (25 px/m, Faktor 1,2) gegen Geländeraster.
# Quelle der Polygone: pruefung/quelle_plaetze_wachstum_ausbau_planm.json (aus ausbau.py exportiert, Quelle unverändert).
import csv,json,numpy as np,cv2
from collections import Counter
from PIL import Image
Z=list(csv.DictReader(open('raster_c20_z25_zellen.csv')))
nx=max(int(r['cx']) for r in Z)+1; ny=max(int(r['cy']) for r in Z)+1
A=lambda k:np.array([r[k] for r in Z]).reshape(ny,nx)
ug=A('untergrund'); beb=A('bebaubar')=='1'; bec=A('senke_becken')=='1'; beg=A('begehbar')=='1'
GR=0.95  # Anteil bebaubarer Zellen für "innerhalb" [A]
def grund(m):
    if beb[m].mean()>=GR: return 'innerhalb_bebaubar'
    z=m&~beb; c=Counter()
    for u,b,s in zip(ug[z],beg[z],bec[z]):
        c['WAND/FELS' if u in('FELS','KLIPPE','WAND') else 'WASSER/EIS' if u=='WASSER_EIS' else 'SCHATTEN' if u=='SCHATTEN' else 'WALD' if u=='WALD' else 'ausserhalb_senke' if not s else 'Abstand(Wand/Wasser 2 m)']+=1
    return c.most_common(1)[0][0]
D=json.load(open('pruefung/quelle_plaetze_wachstum_ausbau_planm.json')); res={}; rows=[]
for st,L in D.items():
    hit=np.zeros((ny,nx),bool); miss=np.zeros((ny,nx),bool); cnt=Counter()
    for p in L:
        m=np.zeros((ny,nx),np.uint8); cv2.fillPoly(m,[np.array([[(x+200)*30/25,(y+40)*30/25] for x,y in p['poly']],np.int32)],1); m=m>0
        if not m.any(): continue
        g=grund(m); cnt[g]+=1; (hit if g=='innerhalb_bebaubar' else miss)[m]=True
        rows.append([st,p['id'],p['typ'],int(p['deko']),p.get('E',''),int(m.sum()),round(float(beb[m].mean()),3),g,int(np.nonzero(m)[1].mean()),int(np.nonzero(m)[0].mean())])
    res[st]=dict(cnt); res[st]['gesamt']=sum(cnt.values())
    img=np.asarray(Image.open('raster_c20_z25_vorschau.png').convert('RGB'))[:ny*3,:nx*3].astype(float)*0.5+127
    up=lambda q:np.repeat(np.repeat(q,3,0),3,1)
    img[up(beb)]=img[up(beb)]*0.6+np.array([0,170,60])*0.4; img[up(hit)]=(0,90,255); img[up(miss)]=(230,0,0)
    Image.fromarray(img.astype(np.uint8)).save(f'pruefung/t16u_plaetze_{st}_gegen_bebaubar.png')
with open('pruefung/t16u_plaetze_gegen_bebaubar.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['stand','id','typ','deko','epoche','zellen','anteil_bebaubar','befund','cx','cy']); w.writerows(rows)
json.dump(res,open('pruefung/t16u_plaetze_gegen_bebaubar.json','w'),ensure_ascii=False,indent=1); print(res)
miss=[r for r in rows if r[7]!='innerhalb_bebaubar']
for st in D: print(st,'Fehl-Mittel cx/cy-Bereiche',Counter((r[8]//50*50,r[9]//50*50) for r in miss if r[0]==st).most_common(8))
