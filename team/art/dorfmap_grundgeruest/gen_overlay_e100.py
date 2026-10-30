# t26u: Wege/Deko v4b (355 Slots, 17 Bruecken, Deko) gegen Gelaende-Raster z25. Nur Overlay, Gelaende bleibt nackt. Quellen nur gelesen.
import json,csv,numpy as np,cv2,collections
Q='/workspace/handygame-plan/team/art/wege_deko_system/umrechnung_25pxm/'
NX,NY=336,303; rd=lambda: csv.DictReader(open('raster_c20_z25_zellen.csv'))
F={k:np.zeros((NY,NX),object) for k in ['ug']}; A={k:np.zeros((NY,NX),bool) for k in ['beg','beb','bzb','bzp','wasser','wand','hind']}; KAP=np.zeros((NY,NX))
for r in rd():
  x,y=int(r['cx']),int(r['cy']); F['ug'][y,x]=r['untergrund']
  A['beg'][y,x]=r['begehbar']=='1'; A['beb'][y,x]=r['bebaubar']=='1'; A['bzb'][y,x]=r['bauzone_bestand']=='1'; A['bzp'][y,x]=r['bauzone_plan']=='1'
  A['wasser'][y,x]=r['untergrund']=='WASSER_EIS'; A['wand'][y,x]=r['klippe']=='WAND'; A['hind'][y,x]=r['hindernis_id']!='0'; KAP[y,x]=float(r['deko_kapazitaet'] or 0)
UG=F['ug']; c=lambda m:(240+m[0],48+m[1])   # m_echt -> Zelle (px/25)
def kat(x,y):
  u=UG[y,x]
  if A['wand'][y,x]: return 'WAND'
  if u=='WASSER_EIS': return 'WASSER_EIS'
  if u in('SCHATTEN','WALD','FELS'): return u
  if A['hind'][y,x]: return 'HINDERNIS'
  return 'BEBAUBAR' if A['beb'][y,x] else 'BEGEHBAR_NICHT_BEBAUBAR' if A['beg'][y,x] else 'SONST_'+u
E=json.load(open(Q+'e100/stand_E100_e100plan_v4b.json')); V9=json.load(open(Q+'zonen_c20_v9_25pxm.json')); N=json.load(open(Q+'netz_e1_25pxm.json'))
S=[dict(id=p.get('nr',p.get('typ','')),ep=1,slot=f"{p['w']}x{p['h']}",poly=p['poly']) for p in V9['plaetze']]+[dict(id=p['id'],ep=p['schicht_epoche'],slot=p['slot'],poly=p['poly_m'],weg=p['weg_polyline_m']) for p in E['plaetze_neu']]
def zellen(poly):
  m=np.zeros((NY,NX),np.uint8); cv2.fillPoly(m,[np.round(np.array([c(q) for q in poly])*8).astype(np.int32)],1,shift=3) if False else None
  big=np.zeros((NY*4,NX*4),np.uint8); cv2.fillPoly(big,[np.round(np.array([c(q) for q in poly])*4).astype(np.int32)],1)
  return big.reshape(NY,4,NX,4).mean((1,3))>=0.5
rows=[];wald_slot=[];sl=np.zeros((NY,NX),int)
for s in S:
  z=zellen(s['poly']); ys,xs=np.nonzero(z); k=collections.Counter(kat(x,y) for x,y in zip(xs,ys)); n=len(xs) or 1
  sl[z]=np.where(sl[z]==0,1,sl[z]); s['z']=z
  rows.append(dict(slot_id=s['id'],epoche=s['ep'],groesse=s['slot'],zellen=len(xs),anteil_bebaubar=round(k['BEBAUBAR']/n,3),anteil_bauzone_plan=round(A['bzp'][z].mean() if len(xs) else 0,3),
    wand=k['WAND'],wasser_eis=k['WASSER_EIS'],schatten=k['SCHATTEN'],wald=k['WALD'],fels=k['FELS'],hindernis=k['HINDERNIS'],begehbar_nicht_bebaubar=k['BEGEHBAR_NICHT_BEBAUBAR'],sonst=sum(v for kk,v in k.items() if kk.startswith('SONST'))))
  for x,y in zip(xs,ys):
    if UG[y,x]=='WALD': wald_slot.append((s['id'],'slot',x,y))
# Wege 1,8 m -> 2 Zellen Strichbreite [A]
wald_weg=[];wm=np.zeros((NY,NX),np.uint8)
for s in S:
  if not s.get('weg') or len(s['weg'])<2: continue
  m=np.zeros((NY,NX),np.uint8); cv2.polylines(m,[np.round(np.array([c(q) for q in s['weg']])).astype(np.int32)],False,1,2); wm|=m
  for y,x in zip(*np.nonzero(m)):
    if UG[y,x]=='WALD': wald_weg.append((s['id'],'weg',x,y))
# Bruecken
br=[]
for r in csv.DictReader(open(Q+'e100/liste_bruecken_e100_v4b.csv'),delimiter=';'):
  a=[float(v)/25 for v in r['px_start'].split(',')]; b=[float(v)/25 for v in r['px_ende'].split(',')]
  w=next(p['weg_polyline_m'] for p in E['plaetze_neu'] if p['id']==r['slot_id'])
  P=np.array([c(q) for q in w]); 
  def land(pt,richt):  # erste Wegzelle ausserhalb Wasser vor/nach dem Wasserstueck
    d=np.hypot(*(P-pt).T); i=int(d.argmin()); rng=range(i,-1,-1) if richt<0 else range(i,len(P))
    for j in rng:
      x,y=int(P[j][0]),int(P[j][1])
      if UG[y,x]!='WASSER_EIS': return x,y,UG[y,x],bool(A['beg'][y,x])
    return None
  la,lb=land(np.array(a),-1),land(np.array(b),1); mx,my=int((a[0]+b[0])/2),int((a[1]+b[1])/2)
  TS={'X084':('Treppe/Steg (Hoehe)','8.6','R: klippe_hoehe_m der Wandzellen (Wand Nord) am Weg; oben hoehe_m 8.6 [A], unten 0.0 [A]; Entscheidung [F] t28u')}  # Gelaende bleibt unveraendert
  wt,hh,hq=TS.get(r['slot_id'],('Bruecke (Wasser)','',''))
  br.append(dict(wegtyp=wt,hoehenunterschied_m=hh,hoehe_quelle=hq,id=r['slot_id'],epoche=r['schicht_epoche'],laenge_m=r['bruecke_m'],mitte_zelle=f'{mx},{my}',mitte_ug=UG[my,mx],mitte_wasser=UG[my,mx]=='WASSER_EIS',
    ende_a=f'{la[0]},{la[1]} {la[2]}' if la else '-',ende_a_begehbar=la[3] if la else False,ende_b=f'{lb[0]},{lb[1]} {lb[2]}' if lb else '-',ende_b_begehbar=lb[3] if lb else False))
# Deko
dk=[]
for d in N['dekoplaetze']:
  x,y=map(int,c(d['pos'])); dk.append(dict(id=d['id'],zelle=f'{x},{y}',ug=UG[y,x],wand=bool(A['wand'][y,x]),wasser=UG[y,x]=='WASSER_EIS',kapazitaet=KAP[y,x]))
TB=list(csv.DictReader(open(Q+'e100/tabelle_e1_e100_v4b.csv'),delimiter=';'))
o='pruefung/t26u_'
for nm,L in [('slots_gegen_gelaende',rows),('bruecken',br),('deko_netz',dk),('wald_unter_slots_wegen',[dict(id=a,art=b,cx=x,cy=y) for a,b,x,y in wald_slot+wald_weg])]:
  w=csv.DictWriter(open(o+nm+'.csv','w'),fieldnames=list(L[0])); w.writeheader(); w.writerows(L)
# Bilder
col={'BEBAUBAR':(70,170,70),'BEGEHBAR_NICHT_BEBAUBAR':(200,220,200),'WASSER_EIS':(220,160,60),'SCHATTEN':(120,120,120),'WALD':(30,90,30),'FELS':(110,110,150),'WAND':(40,40,40),'HINDERNIS':(0,120,255)}
base=np.zeros((NY,NX,3),np.uint8)
for y in range(NY):
  for x in range(NX): base[y,x]=col.get(kat(x,y),(235,235,235))
SC=4;sumE={}
for Ep in (16,40,70,100):
  im=cv2.resize(base,(NX*SC,NY*SC),interpolation=cv2.INTER_NEAREST)
  cn,_=cv2.findContours(cv2.resize(A['bzp'].astype(np.uint8),(NX*SC,NY*SC),interpolation=cv2.INTER_NEAREST),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); cv2.drawContours(im,cn,-1,(255,0,255),1)
  aus=0
  for s,r in zip(S,rows):
    if s['ep']>Ep: continue
    ok=r['anteil_bebaubar']>=0.95; aus+=not ok
    p=np.round(np.array([c(q) for q in s['poly']])*SC).astype(np.int32); cv2.polylines(im,[p],True,(255,255,255) if ok else (0,0,255),2 if not ok else 1)
    if s.get('weg') and len(s['weg'])>1: cv2.polylines(im,[np.round(np.array([c(q) for q in s['weg']])*SC).astype(np.int32)],False,(0,200,255),1)
  for b in br:
    if int(b['epoche'])<=Ep: x,y=map(int,b['mitte_zelle'].split(',')); cv2.circle(im,(x*SC,y*SC),6,(0,255,255) if b['wegtyp'].startswith('Bruecke') else (255,0,0),2)
  n=sum(1 for s in S if s['ep']<=Ep); sumE[Ep]=dict(slots=n,nicht_innen=aus)
  for i,t in enumerate([f'E{Ep}: {n} Slots, {aus} nicht >=95% bebaubar (rot). Overlay, Gelaende nackt. Magenta=bauzone_plan, gelb=Bruecke, blau=Treppe/Steg']):
    cv2.rectangle(im,(0,0),(NX*SC,28),(0,0,0),-1); cv2.putText(im,t,(8,20),cv2.FONT_HERSHEY_SIMPLEX,0.55,(255,255,255),1)
  cv2.imwrite(o+f'overlay_E{Ep}.png',im)
# bauzone_plan Konflikte
def konf(m,ursache): return [dict(cx=x,cy=y,ug=UG[y,x],ursache=ursache(x,y)) for y,x in zip(*np.nonzero(m))]
u1=lambda x,y:'WAND' if A['wand'][y,x] else 'WASSER_EIS' if UG[y,x]=='WASSER_EIS' else UG[y,x] if UG[y,x] in('WALD','SCHATTEN','FELS') else 'HINDERNIS' if A['hind'][y,x] else 'nicht begehbar' if not A['beg'][y,x] else 'Abstand Wand/Wasser <2 m oder ausserhalb senke_becken'
u2=lambda x,y:'ausserhalb BB4-Planmaske (Gelaende frei, Planmaske kleiner)'
k1=konf(A['bzp']&~A['beb'],u1); k2=konf(A['beb']&~A['bzp'],u2)
for nm,L in [('bauzone_plan_nicht_bebaubar',k1),('bebaubar_nicht_bauzone_plan',k2)]:
  w=csv.DictWriter(open(o+nm+'.csv','w'),fieldnames=['cx','cy','ug','ursache']); w.writeheader(); w.writerows(L)
R=dict(slots=len(S),slots_innen95=sum(r['anteil_bebaubar']>=0.95 for r in rows),anteil_bebaubar_mittel=round(np.mean([r['anteil_bebaubar'] for r in rows]),3),
 slots_mit=dict(wand=sum(r['wand']>0 for r in rows),wasser=sum(r['wasser_eis']>0 for r in rows),schatten=sum(r['schatten']>0 for r in rows),wald=sum(r['wald']>0 for r in rows),fels=sum(r['fels']>0 for r in rows),hindernis=sum(r['hindernis']>0 for r in rows)),
 zellen_slots=dict(wand=sum(r['wand'] for r in rows),wasser=sum(r['wasser_eis'] for r in rows),schatten=sum(r['schatten'] for r in rows),wald=sum(r['wald'] for r in rows)),
 bruecken=len(br),bruecke_mitte_wasser=sum(b['mitte_wasser'] for b in br),bruecke_beide_enden_begehbar=sum(b['ende_a_begehbar'] and b['ende_b_begehbar'] for b in br),
 deko_netz=len(dk),deko_auf_wand=sum(d['wand'] for d in dk),deko_auf_wasser=sum(d['wasser'] for d in dk),deko_kap0=sum(d['kapazitaet']==0 for d in dk),deko_ug=dict(collections.Counter(d['ug'] for d in dk)),
 deko_soll=dict((t['E'],(t['dekoplaetze'],t['deko_limit'])) for t in TB if t['E'] in('1','16','40','70','100')),kapazitaet_summe=round(float(KAP.sum()),1),
 wald_zellen_slots=len(set((x,y) for _,_,x,y in wald_slot)),wald_zellen_wege=len(set((x,y) for _,_,x,y in wald_weg)),slots_mit_wald_ids=len(set(a for a,_,_,_ in wald_slot)),wege_mit_wald=len(set(a for a,_,_,_ in wald_weg)),
 bzp_nicht_beb=len(k1),bzp_nicht_beb_ursache=dict(collections.Counter(k['ursache'] for k in k1)),beb_nicht_bzp=len(k2),je_epoche=sumE)
json.dump(R,open(o+'zusammenfassung.json','w'),indent=1,ensure_ascii=False,default=int); print(json.dumps(R,ensure_ascii=False,default=int))
