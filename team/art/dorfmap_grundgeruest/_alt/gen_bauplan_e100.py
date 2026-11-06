# Bauplan bis E100: Bedarf (Quellen siehe BAUPLAN_E100.md) gegen 99 Plaetze; neue Standorte nur auf bebaubar & in senke_becken,
# ohne bestehende Plaetze/Wege/Hoefe/Feuer/Bruecken. Bestehende 99 unveraendert. 0 $, keine Bildgenerierung.
import csv,json,numpy as np,cv2,math
from PIL import Image
P='/workspace/handygame-plan/team/'
G=P+'art/karten_konzept/dorfkarte_e1_final_neu/master_v18_p7/zonen_c20/'
ABST_M=4; ABST_GROSS_M=6; GROSS_AB_M=12   # F2: 2 Tiles = 4 m, 3 Tiles = 6 m bei Grossbauten [S f2-siedlung-abstand]; Grenze gross = 12 m [A]
zel=list(csv.DictReader(open('raster_c20_z25_zellen.csv'))); ov=list(csv.DictReader(open('raster_c20_z25_overlay_plaetze_wege.csv')))
nx=max(int(r['cx']) for r in zel)+1; ny=max(int(r['cy']) for r in zel)+1
beb=np.zeros((ny,nx),bool); bec=np.zeros((ny,nx),bool); bel=np.zeros((ny,nx),bool); feu=np.zeros((ny,nx),bool)
for r in zel: x,y=int(r['cx']),int(r['cy']); beb[y,x]=r['bebaubar']=='1'; bec[y,x]=r['senke_becken']=='1'
for r in ov:
    x,y=int(r['cx']),int(r['cy']); bel[y,x]=bool(r['platz']) or bool(r['weg_id']) or r['hof']=='1' or r['feuer']=='1' or r['bruecke']=='1'; feu[y,x]=r['feuer']=='1'
# Bestandsplaetze als Rechteck-Zellen voll belegen (Polygon)
zj=json.load(open(G+'zonen_c20_v9.json')); pm=np.zeros((ny,nx),np.uint8)
for p in zj['plaetze']: cv2.fillPoly(pm,[np.array([[(x+200)*30/25,(y+40)*30/25] for x,y in p['poly']],np.int32)],1)
bel|=pm>0
# --- Bedarf ---
g=list(csv.DictReader(open(G+'groessen_25slots/groessen_25_slots.csv'),delimiter=';'))
mass={x['slot_id']:x['platz_varC_m'] for x in g if x['epochengruppe']=='E12-E16' and x['platz_varC_m']}
def dim(s): a,b=s.split('x'); return float(a),float(b)
SL=json.load(open('bauplan_e100_bedarf.json'))
need=[]
for s in SL['slots']:
    if s['id']=='bld_palisade': continue
    w,h=dim(mass[s.get('mass_analog',s['id'])]); need.append(dict(id=s['id'],art='FUNKTION',ab=s['ab'],w=w,h=h,marker=s['marker']))
for i in range(SL['deko_haeuser_max']): w,h=dim(mass_h) if (mass_h:=SL['deko_haus_mass']) else (0,0); need.append(dict(id='deko_haus_%02d'%(i+1),art='DEKO_HAUS',ab=None,w=w,h=h,marker='A'))
for i in range(SL['flur_deko_e100']): need.append(dict(id='flur_deko_%02d'%(i+1),art='DEKO_FLUR',ab=None,w=3,h=3,marker='A'))
# --- Abgleich gegen 99 Bestandsplaetze (passt, wenn Platz >= Bedarf, Drehung erlaubt) ---
frei=sorted([dict(nr=p['nr'],w=p['w'],h=p['h'],typ=p['typ']) for p in zj['plaetze']],key=lambda p:p['w']*p['h'])
zu=[]
for n in sorted(need,key=lambda n:-n['w']*n['h']):
    f=next((p for p in frei if (n['w']<=p['w'] and n['h']<=p['h']) or (n['w']<=p['h'] and n['h']<=p['w'])),None)
    if f: frei.remove(f); n['bestand']=f['nr']; zu.append(n)
    else: n['bestand']=None
# --- neue Standorte: gierig, groesste zuerst, nah am Feuer (Ausbauringe) ---
fy,fx=[v.mean() for v in np.nonzero(feu)]
ok=beb&bec&~bel
neu=[]; occ=bel.copy()
for n in sorted([n for n in need if n['bestand'] is None],key=lambda n:-n['w']*n['h']):
    a=n['w']>=GROSS_AB_M or n['h']>=GROSS_AB_M; ab=ABST_GROSS_M if a else ABST_M
    best=None
    for (W,H) in {(math.ceil(n['w']),math.ceil(n['h'])),(math.ceil(n['h']),math.ceil(n['w']))}:
        k=cv2.dilate(occ.astype(np.uint8),np.ones((2*ab+1,2*ab+1),np.uint8))>0
        free=(ok&~k).astype(np.uint8); ii=cv2.integral(free)
        S=ii[H:,W:]-ii[:-H,W:]-ii[H:,:-W]+ii[:-H,:-W]; ys,xs=np.nonzero(S==W*H)
        if len(ys)==0: continue
        d=np.hypot(ys+H/2-fy,xs+W/2-fx); j=d.argmin()
        if best is None or d[j]<best[0]: best=(d[j],xs[j],ys[j],W,H)
    if best is None: n['neu']=None; continue
    d,x,y,W,H=best; occ[y:y+H,x:x+W]=True
    n['neu']=dict(cx0=int(x),cy0=int(y),cx1=int(x+W-1),cy1=int(y+H-1),dist_feuer_m=round(float(d),1),ring=int(d//40)+1)
    neu.append(n)
nicht=[n for n in need if n['bestand'] is None and n.get('neu') is None]
res=dict(abstand_m=ABST_M,abstand_gross_m=ABST_GROSS_M,bedarf=len(need),in_bestand=len(zu),neu=len(neu),nicht_platzierbar=len(nicht),
  flaeche_frei_zellen=int(ok.sum()),flaeche_bedarf_neu_m2=round(sum(n['w']*n['h'] for n in need if n['bestand'] is None),1),
  bestand_frei_nach_abgleich=len(frei),plaetze=need)
json.dump(res,open('overlay_plaetze_erweiterung.json','w'),ensure_ascii=False,indent=1)
with open('overlay_plaetze_erweiterung.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['id','art','ab_epoche','platz_w_m','platz_h_m','marker','bestand_platz','neu_cx0','neu_cy0','neu_cx1','neu_cy1','ring','dist_feuer_m'])
    for n in need:
        q=n.get('neu') or {}; w.writerow([n['id'],n['art'],n['ab'] or '',n['w'],n['h'],n['marker'],n['bestand'] or '',q.get('cx0',''),q.get('cy0',''),q.get('cx1',''),q.get('cy1',''),q.get('ring',''),q.get('dist_feuer_m','')])
# Vorschau
s=3; img=np.asarray(Image.open('raster_c20_z25_vorschau.png').convert('RGB'))[:ny*3,:nx*3].astype(np.float32)
img=img*0.45+255*0.55; up=lambda m:np.repeat(np.repeat(m,s,0),s,1)
img[up(beb&bec)]=img[up(beb&bec)]*0.6+np.array([0,170,60])*0.4; img[up(pm>0)]=(90,90,90)
img=img.astype(np.uint8).copy(); C={'FUNKTION':(220,0,0),'DEKO_HAUS':(0,80,220),'DEKO_FLUR':(230,140,0)}
for n in neu:
    q=n['neu']; cv2.rectangle(img,(q['cx0']*s,q['cy0']*s),((q['cx1']+1)*s-1,(q['cy1']+1)*s-1),C[n['art']],-1 if n['art']=='DEKO_FLUR' else 2)
cv2.circle(img,(int(fx*s),int(fy*s)),6,(0,0,0),-1)
for r in (40,80,120): cv2.circle(img,(int(fx*s),int(fy*s)),r*s,(0,0,0),1)
Image.fromarray(img).save('overlay_plaetze_erweiterung.png')
print({k:v for k,v in res.items() if k!='plaetze'}); print('nicht:',[(n['id'],n['w'],n['h']) for n in nicht])
