# t65u Runde M: Vollpruefung ALLER Zellen (336x303) aus zellen_relief.csv + relief_daten (Anzeige). Ausgabe pruefung/zellen_voll_t65u.json/.csv [S]
import csv,json,gzip,base64,collections,numpy as np,scipy.ndimage as nd
R=list(csv.DictReader(open('zellen_relief.csv')));D=json.load(gzip.open('relief_daten.json.gz'))
NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1;N=NX*NY;assert len(R)==N
K=list(R[0].keys());S=lambda k:np.array([r[k] for r in R]).reshape(NY,NX)
def F(k):
    a=S(k);o=np.full(a.shape,np.nan);m=a!='';o[m]=a[m].astype(float);return o
OUT=[];RES={}
def rep(name,mask,art,detail=None,grund=''):
    j,i=np.nonzero(mask);n=int(mask.sum());RES[name]={'anzahl':int(n),'art':art,'grund':grund,'orte':[[int(a),int(b)] for a,b in zip(i[:60],j[:60])]}
    for a,b in zip(i,j):OUT.append([name,art,int(a),int(b),'' if detail is None else str(detail[b,a])])
# ---- a) Sauberkeit
ERL={'untergrund':{'SCHNEE','WALD','WASSER_EIS','FELS','KLIPPE_WAND','BODEN','SAND','KLIPPE_KANTE'},'klippe':{'','WAND','WAND_FUSS','WAND_OBEN'},
 'wand_name':{'','Nord','Suedgrat','Krater','Ostgrat'},'fluss_id':{'','WASSER_FARBE','BACH_NORD','BACH_SUED','SEE'},'fliess_richtung':{'','S','SO'},
 'hindernis_art':{'','GELAENDE','MASKE'},'ebene':{'SENKE','HANG','TAL_SUED','PLATEAU_NORD','OSTPLATEAU','KRATERRAND','WAND','KRATER','GIPFEL','SIMS'}}
BIN=['wasser_eis','schnee','senke_bb4','h4_ext','frei_e2','begehbar','bebaubar','bebaubar_erweitert','ebene_hoeher','bauzone_bestand','bauzone_plan','senke_becken','ufer','begehbar_3d','deko_baum_ok','deko_fels_ok']
NUM=['hoehe_m','neigung_grad','klippe_hoehe_m','wasser_tiefe_m','deko_kapazitaet','flaeche_m2','boden_hoehe_m','ecke_nw_m','ecke_no_m','ecke_so_m','ecke_sw_m']
leer=np.zeros((NY,NX),int)
for k in K:
    a=S(k)
    if k in NUM+['zell_id','cx','cy','px_x','px_y']+BIN:leer+=(a=='')|(np.char.lower(a)=='nan')
rep('a_leer_oder_nan_pflichtfeld',leer>0,'fehler',leer)
unb=np.zeros((NY,NX),bool)
for k,v in ERL.items():unb|=~np.isin(S(k),list(v))
for k in BIN:unb|=~np.isin(S(k),['0','1'])
rep('a_unbekannter_wert',unb,'fehler')
rng=np.zeros((NY,NX),bool)
for k,(lo,hi) in {'hoehe_m':(-40,20),'boden_hoehe_m':(-40,20),'neigung_grad':(0,90),'klippe_hoehe_m':(0,30),'wasser_tiefe_m':(0,10),'deko_kapazitaet':(0,1),'flaeche_m2':(1,1)}.items():
    v=F(k);rng|=(v<lo)|(v>hi)
rep('a_wertebereich',rng,'fehler')
zid=F('zell_id');cx=F('cx');cy=F('cy');J,I=np.mgrid[0:NY,0:NX]
rep('a_id_nicht_eindeutig_oder_falsch',(zid!=J*NX+I)|(cx!=I)|(cy!=J),'fehler')
RES['a_id_eindeutig']={'eindeutig':int(len(np.unique(zid))==N)}
w=S('wasser_eis')=='1';ug=S('untergrund');kl=S('klippe');ws=F('wasserspiegel_m');h=F('hoehe_m');bh=F('boden_hoehe_m');ng=F('neigung_grad')
rep('a_wasser_vs_untergrund',w!=(ug=='WASSER_EIS'),'fehler')
rep('a_wasser_vs_fluss_id',w!=(S('fluss_id')!=''),'fehler')
rep('a_wasser_vs_spiegel',w!=~np.isnan(ws),'fehler')
rep('a_wasser_vs_tiefe',w!=(F('wasser_tiefe_m')>0),'fehler')
rep('a_klippe_vs_hoehenquelle',(kl!='')!=(S('klippe_hoehe_quelle')!=''),'fehler')
rep('a_wandname_ohne_klippe',(S('wand_name')!='')&(kl==''),'fehler')
rep('a_begehbar3d_auf_WAND',(S('begehbar_3d')=='1')&(kl=='WAND'),'fehler')
rep('a_bebaubar_auf_wasser',(S('bebaubar')=='1')&w,'fehler')
rep('a_baum_ok_auf_wasser_oder_WAND',(S('deko_baum_ok')=='1')&(w|(kl=='WAND')),'fehler')
e4=np.stack([F(k) for k in ['ecke_nw_m','ecke_no_m','ecke_so_m','ecke_sw_m']])
rep('a_hoehe_ausserhalb_ecken',(h<e4.min(0)-0.6)|(h>e4.max(0)+0.6),'pruefen',h-e4.mean(0),'Zellmittel aus 3x3 Unterpunkten darf bis 0,6 m von den Ecken abweichen [A]')
rep('a_untergrund_KLIPPE_WAND_ausserhalb_ebene_WAND',(np.isin(ug,['KLIPPE_WAND','KLIPPE_KANTE']))&(S('ebene')!='WAND'),'fehler')
# ---- b) Sinnhaftigkeit
rep('b_spiegel_nicht_unter_land',w&~(ws<bh),'fehler',ws-bh)
rep('b_spiegel_unter_bett',w&(ws<h-0.02),'fehler',ws-h)
nw4=nd.convolve(w.astype(int),np.array([[0,1,0],[1,0,1],[0,1,0]]),mode='constant')
rep('b_wasser_einzelzelle',w&(nw4==0),'fehler')
lab,nl=nd.label(w);gr=nd.sum(w,lab,range(1,nl+1));klein=np.isin(lab,1+np.nonzero(gr<4)[0])
rep('b_wasserinsel_unter_4_zellen',klein,'fehler')
rep('b_WAND_ohne_hoehensprung',(kl=='WAND')&~(F('klippe_hoehe_m')>0),'fehler')
rep('b_bebaubar_hang_gt_30grad',(S('bebaubar')=='1')&(ng>30),'pruefen',ng,'bebaubar stammt aus c20-Plan (2D), Neigung aus Relief; Bauplaetze im Viewer separat auf eben gestellt [A]')
med=nd.median_filter(h,footprint=np.array([[1,1,1],[1,0,1],[1,1,1]]),mode='nearest');dh=h-med
nah_kl=nd.binary_dilation(kl!='',iterations=2)
rep('b_hoehe_ausreisser_gt_1m_ohne_klippe',(np.abs(dh)>1)&~nah_kl&~w,'fehler',dh)
rep('b_hoehe_ausreisser_gt_1m_an_klippe_oder_wasser',(np.abs(dh)>1)&(nah_kl|w),'gewollt',dh,'Wandfuss/-kopf bzw. Flussbett: Sprung ist gewollt')
def einzel(A):
    c=np.zeros((NY,NX),int);P=np.pad(A,1,mode='edge')
    for dy in(-1,0,1):
        for dx in(-1,0,1):
            if dy or dx:c+=(P[1+dy:1+dy+NY,1+dx:1+dx+NX]==A)
    return c==0
rep('b_untergrund_einzelzelle',einzel(ug),'pruefen',ug,'keine der 8 Nachbarn hat denselben Untergrund')
rep('b_ebene_einzelzelle',einzel(S('ebene')),'pruefen',S('ebene'))
rep('b_bauzone_plan_einzelzelle',einzel(S('bauzone_plan'))&(S('bauzone_plan')=='1'),'pruefen')
# ---- c) Uebergaenge gegen alle 8 Nachbarn
Pp=lambda A,v:np.pad(A,1,constant_values=v)
stufe=np.zeros((NY,NX));wechsel=collections.Counter();uwx=np.zeros((NY,NX),bool);hart=np.zeros((NY,NX),bool)
HART={frozenset(p) for p in [('FELS','SAND'),('WALD','SAND'),('WASSER_EIS','FELS'),('BODEN','WASSER_EIS')]}
uP=Pp(ug,'');hP=Pp(h,np.nan)
for dy in(-1,0,1):
    for dx in(-1,0,1):
        if not(dy or dx):continue
        nb=uP[1+dy:1+dy+NY,1+dx:1+dx+NX];hn=hP[1+dy:1+dy+NY,1+dx:1+dx+NX]
        stufe=np.fmax(stufe,np.abs(h-hn));d=(nb!=ug)&(nb!='')
        for a,b in zip(ug[d],nb[d]):wechsel[tuple(sorted((a,b)))]+=1
        for p in HART:
            a,b=tuple(p);hart|=((ug==a)&(nb==b))|((ug==b)&(nb==a))
gew=nah_kl|nd.binary_dilation(w,iterations=1)
weg=np.zeros((NY,NX),bool)
for o in D.get('wege') or []:
    pts=o.get('p') if isinstance(o,dict) else o
    try:
        for q in pts:weg[min(NY-1,max(0,int(q[-1]))),min(NX-1,max(0,int(q[0])))]=True
    except Exception:pass
weg=nd.binary_dilation(weg,iterations=2)
rep('c_hoehenstufe_gt_1m_gewollt',(stufe>1)&gew,'gewollt',stufe,'Klippe/Wandfuss oder Flussbett')
rep('c_hoehenstufe_gt_1m_an_weg',(stufe>1)&~gew&weg,'gewollt',stufe,'Wegeinschnitt/Rampe')
rep('c_hoehenstufe_gt_1m_sonst',(stufe>1)&~gew&~weg,'pruefen',stufe)
rep('c_harter_untergrundwechsel',hart,'pruefen',ug,'Paare Fels/Sand, Wald/Sand, Wasser/Fels, Boden/Wasser; Anzeige mischt Vertexfarben weich (vc_weich/Ufer) [A]')
RES['c_untergrundwechsel_paare_gerichtet']={'/'.join(k):v for k,v in wechsel.most_common()}
uf=S('ufer')=='1';nwet=nd.binary_dilation(w,structure=np.ones((3,3)))&~w
rep('c_ufer_fehlt_an_wasserrand',nwet&~uf,'pruefen',None,'Ufer-Flag kommt aus c20, Wasserrand aus Relief')
rep('c_ufer_ohne_wasser_nachbar',uf&~nd.binary_dilation(w,structure=np.ones((3,3)),iterations=2),'pruefen')
zr=S('ebene');zrand=np.zeros((NY,NX),bool);zP=Pp(zr,'')
for dy in(-1,0,1):
    for dx in(-1,0,1):
        nb=zP[1+dy:1+dy+NY,1+dx:1+dx+NX];zrand|=(nb!=zr)&(nb!='')
rep('c_zonenrand_hoehenstufe_gt_2m_ohne_klippe',zrand&(stufe>2)&~gew,'pruefen',stufe)
# ---- d) Aussehen: Vertexfarbe je Zelle (Mittel der Unterpunkte) gegen 8 Nachbarn
VC=np.frombuffer(base64.b64decode(D['VC']),np.uint8).reshape(GY,GX,3).astype(float)
cm=np.stack([sum(VC[dy:dy+GY-1:RS,dx:dx+GX-1:RS,k][:NY,:NX] for dy in range(3) for dx in range(3))/9 for k in range(3)],-1)
mm=np.stack([nd.median_filter(cm[...,k],footprint=np.array([[1,1,1],[1,0,1],[1,1,1]]),mode='nearest') for k in range(3)],-1)
dc=np.linalg.norm(cm-mm,axis=-1)
rep('d_vertexfarbe_ausreisser_gt_60',(dc>60)&~gew,'fehler',dc)
rep('d_vertexfarbe_ausreisser_gt_60_an_klippe_wasser',(dc>60)&gew,'gewollt',dc,'Material wechselt an Wand/Wasser hart')
rep('d_vertexfarbe_ungueltig',~np.isfinite(cm).all(-1),'fehler')
GB=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(GY,GX)
rep('d_anzeigehoehe_nan',~np.isfinite(GB[:-1:RS,:-1:RS][:NY,:NX]),'fehler')
z={k:v['anzahl'] for k,v in RES.items() if 'anzahl' in v}
RES['_zusammenfassung']={'zellen_geprueft':N,'felder':len(K),'fehler_summe':sum(v['anzahl'] for v in RES.values() if v.get('art')=='fehler'),'je_pruefung':z}
json.dump(RES,open('pruefung/zellen_voll_t65u.json','w'),indent=1,ensure_ascii=False)
with open('pruefung/zellen_voll_t65u.csv','w',newline='') as f:
    wr=csv.writer(f);wr.writerow(['pruefung','art','cx','cy','wert']);wr.writerows(OUT)
print(json.dumps(RES['_zusammenfassung'],indent=0))
