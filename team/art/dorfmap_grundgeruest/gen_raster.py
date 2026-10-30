# Dorfmap-Grundgeruest c20: Zellraster aus vorhandenen Masken (0 $, keine Bildgenerierung).
# Aufruf: python3 gen_raster.py [ZELLE_PX]   (Default 25 px = 1 m bei 25 px/m [F])
import sys, json, csv, glob, os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS=None
R='/workspace/handygame-plan/team/art/karten_konzept/dorfkarte_e1_final_neu/master_v18_p7/'
W,H=8400,7560; Z=int(sys.argv[1]) if len(sys.argv)>1 else 25; PXM=25
nx,ny=-(-W//Z),-(-H//Z)
def zell(mask_px, thr=0.5):
    m=np.zeros((ny*Z,nx*Z),np.float32); m[:H,:W]=mask_px
    return m.reshape(ny,Z,nx,Z).mean((1,3))>=thr
def frac(mask_px):
    m=np.zeros((ny*Z,nx*Z),np.float32); m[:H,:W]=mask_px; return m.reshape(ny,Z,nx,Z).mean((1,3))
def up(a,f,x0=0,y0=0):  # kleines Raster -> Vollbild px
    o=np.zeros((H,W),bool); b=np.repeat(np.repeat(a,f,0),f,1); h,w=min(b.shape[0],H-y0),min(b.shape[1],W-x0); o[y0:y0+h,x0:x0+w]=b[:h,:w]; return o
A={k:np.load(R+'arbeit/%s.npy'%k) for k in ['BB4','F4','H4_ext','bach_schutz']}
frei_e2=up(np.load(R+'slots_c20/mp/frei_e2.npy'),10)
hz=np.load(R+'slots_c20/hindernisse_c20_v2.npz'); hx0,hy0=(int(hz['X0'])+200)*30,(int(hz['Y0'])+40)*30
fels=up(hz['fels'],10,hx0,hy0); hid=np.zeros((H,W),np.int16); b=np.repeat(np.repeat(hz['idmap'],10,0),10,1); hid[hy0:hy0+b.shape[0],hx0:hx0+b.shape[1]]=b[:H-hy0,:W-hx0]
E=R+'layout_e1_v9/ebenen/'; man=json.load(open(E+'manifest.json'))['ebenen']
def ebene(name):
    e=json.load(open(E+name+'.json')) if os.path.exists(E+name+'.json') else {}
    me=man.get(name,e); mk=np.asarray(Image.open(E+me['maske']).convert('L'))>127; ox,oy=me['offset_px']
    o=np.zeros((H,W),bool); h,w=min(mk.shape[0],H-oy),min(mk.shape[1],W-ox); o[oy:oy+h,ox:ox+w]=mk[:h,:w]; return o
names=sorted(man)
zone=np.zeros((ny,nx),'U1')
for n in names:
    if n.startswith('10_zonenboden_'): zone[zell(ebene(n),0.5)]=n[-1]
weg=np.zeros((ny,nx),'U12'); weg_kl=np.zeros((ny,nx),'U10')
for n in names:
    if n.startswith('20_wege_'):
        c=zell(ebene(n),0.3); weg[c]=n[8:]; weg_kl[c]='HAUSWEG' if '_haus_' in n else ('ANBINDUNG' if n.endswith('_anb') else 'GASSE')
hof=np.zeros((ny,nx),bool); feuer=np.zeros((ny,nx),bool); bruecke=np.zeros((ny,nx),bool)
for n in names:
    if n.startswith('30_hof'): hof|=zell(ebene(n),0.5)
    if n.startswith('40_feuer'): feuer|=zell(ebene(n),0.5)
    if n.startswith('50_bruecke'): bruecke|=zell(ebene(n),0.3)
zj=json.load(open(R+'zonen_c20/zonen_c20_v9.json'))
pl=np.zeros((ny*Z,nx*Z),np.uint8); ids=[]
for i,p in enumerate(zj['plaetze'],1):
    cv2.fillPoly(pl,[np.array([[(x+200)*30,(y+40)*30] for x,y in p['poly']],np.int32)],i); ids.append(p)
plg=pl.reshape(ny,Z,nx,Z).transpose(0,2,1,3).reshape(ny,nx,-1)
platz=np.array([[np.bincount(c,minlength=len(ids)+1)[1:].argmax()+1 if (c>0).mean()>=0.5 else 0 for c in row] for row in plg])
wasser=zell(A['bach_schutz'],0.5); fz=zell(fels,0.5); rand=zell(~frei_e2&~A['BB4']&~A['F4'],0.5)
schnee=zell(A['F4'],0.5); senke=zell(A['BB4'],0.5); h4=zell(A['H4_ext'],0.5)
hind=np.zeros((ny,nx),np.int16); hf=frac(hid>0)>=0.5
hidc=hid[::Z,::Z]; hidp=np.zeros((ny,nx),np.int16); hidp[:hidc.shape[0],:hidc.shape[1]]=hidc; hind[hf]=hidp[hf]
fe2=zell(frei_e2,0.5)

# ---- Farbklassen fuer Zellen ohne Maskendaten (t5u) [R aus Originalkarte] ----
_m=np.asarray(Image.open(R+'KANDIDAT_NICHT_FREIGEGEBEN_master_v18_p7_c20.png').convert('RGB'))
_p=np.zeros((ny*Z,nx*Z,3),np.uint8); _p[:H,:W]=_m; _p[H:,:W]=_m[H-(ny*Z-H):H][::-1]; _p[:,W:]=_p[:,W-(nx*Z-W):W][:,::-1]; del _m
_hsv=cv2.cvtColor(_p,cv2.COLOR_RGB2HSV); del _p
def _fr(b): return b.reshape(ny,Z,nx,Z).mean((1,3))
_H,_S,_V=[_hsv[...,i].astype(np.int16) for i in range(3)]; del _hsv
f_wald=_fr(((_V<110)&(_H>=35)&(_H<=110))|(_V<70)); f_fels=_fr((_S>70)&((_H<25)|(_H>165))&(_V<200))
f_sand=_fr((_H>=12)&(_H<=28)&(_S>50)&(_S<=140)&(_V>=170)); f_wass=_fr((_H>=88)&(_H<=112)&(_S>=55)&(_V>=110)); f_schn=_fr((_S<45)&(_V>=185))
f_dark=_fr((_V<150)&(((_H>=128))|(_H<25))); f_navy=_fr((_V<150)&(_H>=95)&(_H<=140)); f_tree=_fr((_V<170)&(_H>=80)&(_H<128)&(_S>=40)); f_shade=_fr((_H>=100)&(_H<=135)&(_S>=15)&(_S<100)&(_V>=120)&(_V<215))
f_edge=_fr(cv2.Canny(_V.astype(np.uint8),60,140)>0)
del _H,_S,_V
farb=np.full((ny,nx),'UNBEKANNT',dtype='U12')
farb[f_schn>=0.3]='SCHNEE'; farb[f_sand>=0.35]='SAND'
farb[(f_schn<0.5)&(f_fels>=0.03)]='FELS_KLIPPE'; farb[(f_schn<0.5)&(f_wald>=0.15)]='WALD'
farb[f_wass>=0.35]='WASSER_EIS'
ug=np.full((ny,nx),'BODEN',dtype='U12')
quelle=np.full((ny,nx),'MASKE',dtype='U6')
ug[rand]='GESPERRT'; ug[schnee]='SCHNEE'; ug[fz]='FELS_WALD'; ug[wasser]='WASSER_EIS'; ug[hof]='HOF'; ug[feuer]='FEUER'
ug[weg!='']='WEG'; ug[bruecke]='BRUECKE'
ohne=(ug=='GESPERRT'); ug[ohne]=farb[ohne]; quelle[ohne]=np.where(farb[ohne]=='UNBEKANNT','KEINE','FARBE')
# ---- Klippenmaske per Bildanalyse (t6u) [R], Schwellen [A] ----
unb_vor=int((ug=='UNBEKANNT').sum())
fz_=ohne
baum=fz_&(ug!='WASSER_EIS')&(f_tree>=0.20)&(f_tree>f_dark)
wand=fz_&(ug!='WASSER_EIS')&~baum&(((f_dark>=0.12)&(f_edge>=0.04))|((f_fels>=0.03)&(f_schn<0.5)))
ug[baum]='WALD'
schat=fz_&~wand&~baum&(f_shade>=0.35)&(f_edge<0.06)
ug[wand]='KLIPPE_WAND'; ug[schat]='SCHATTEN'
# Wasser aus Farbe, das eigentlich Schatten ist: Komponenten, die ueberwiegend an Wand grenzen und klein/kompakt sind
_w=(fz_&(ug=='WASSER_EIS')).astype(np.uint8); _n,_l,_st,_=cv2.connectedComponentsWithStats(_w,8)
_wd=cv2.dilate((ug=='KLIPPE_WAND').astype(np.uint8),np.ones((3,3),np.uint8))>0
schatten_wasser=0
for i in range(1,_n):
    c=_l==i; rand=(cv2.dilate(c.astype(np.uint8),np.ones((3,3),np.uint8))>0)&~c
    if _st[i,4]<1500 and max(_st[i,2],_st[i,3])>=2.5*min(_st[i,2],_st[i,3]) and (_wd&rand).sum()/max(1,rand.sum())>=0.5 and f_shade[c].mean()>=0.2:
        ug[c]='SCHATTEN'; schatten_wasser+=int(c.sum())
# Mehrheitsfilter 3x3 nur auf Farbzellen; Kleinstflecken (<4 Zellen) gehen an die Nachbarmehrheit
KL=['SCHNEE','SAND','WALD','KLIPPE_WAND','SCHATTEN','WASSER_EIS','UNBEKANNT']
for _ in range(2):
    cnt=np.stack([cv2.filter2D((ug==k).astype(np.float32),-1,np.ones((3,3),np.float32),borderType=cv2.BORDER_REFLECT) for k in KL],-1)
    maj=np.array(KL)[cnt.argmax(-1)]; stark=cnt.max(-1)>=5
    for k in KL:
        n_,l_,st_,_=cv2.connectedComponentsWithStats(((ug==k)&fz_).astype(np.uint8),8)
        klein=np.isin(l_,np.nonzero(st_[:,4]<4)[0][1:]) if n_>1 else np.zeros_like(fz_)
        sel=klein&stark&fz_; ug[sel]=maj[sel]
    sel=fz_&(ug=='UNBEKANNT')&stark&(maj!='UNBEKANNT'); ug[sel]=maj[sel]
# FELS = kleine isolierte Wandkomponenten; KANTE = Wandzelle mit Nicht-Wand im Norden (Krone, Draufsicht von Sueden) [A]
_n,_l,_st,_=cv2.connectedComponentsWithStats((ug=='KLIPPE_WAND').astype(np.uint8),8)
ug[np.isin(_l,np.nonzero(_st[:,4]<30)[0][1:])&(ug=='KLIPPE_WAND')]='FELS'
_wa=ug=='KLIPPE_WAND'; _no=np.zeros_like(_wa); _no[1:]=~_wa[:-1]&(ug[:-1]!='UNBEKANNT')
ug[_wa&_no]='KLIPPE_KANTE'
quelle[fz_&(ug!='UNBEKANNT')]='FARBE'; quelle[fz_&(ug=='UNBEKANNT')]='KEINE'
# Overrides nach Sichtpruefung (t7u), nur auf UNBEKANNT-Zellen im Bereich
ovr_n=0
if Z==25 and os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'overrides_c20_z25.csv')):
    for _r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'overrides_c20_z25.csv'))):
        _s=(slice(int(_r['cy0']),int(_r['cy1'])+1),slice(int(_r['cx0']),int(_r['cx1'])+1)); _u=ug[_s]=='UNBEKANNT'
        ug[_s][_u]=_r['klasse']; ovr_n+=int(_u.sum())
# ==== t9u/t10u: Gelaende-Layer von Plaetzen/Wegen trennen, Bereinigung, Hoehe ueberall ====
ovr=np.zeros((ny,nx),bool)
if Z==25:
    for _r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'overrides_c20_z25.csv'))):
        ovr[int(_r['cy0']):int(_r['cy1'])+1,int(_r['cx0']):int(_r['cx1'])+1]|=(ug[int(_r['cy0']):int(_r['cy1'])+1,int(_r['cx0']):int(_r['cx1'])+1]==_r['klasse'])
stat_vor={k:int(v) for k,v in zip(*np.unique(ug,return_counts=True))}
# (1) Overlay-Klassen raus: WEG/HOF/FEUER/BRUECKE -> Gelaende darunter (Farbe c20) [R], Bruecke ueber Wasser -> WASSER_EIS
ovl=np.isin(ug,['WEG','HOF','FEUER','BRUECKE'])
ug[ovl]=np.where(wasser[ovl]|(f_wass[ovl]>=0.35),'WASSER_EIS',np.where(f_schn[ovl]>=0.3,'SCHNEE','BODEN'))
quelle[ovl]='FARBE'
# (2) FELS_WALD (Hindernismaske, nur Bauzonen-Fenster) nach Farbe aufloesen: Wald / Wand / Fels [R], Schwellen [A]
fw=ug=='FELS_WALD'
ug[fw&(f_tree>=0.20)&(f_tree>f_dark)]='WALD'
ug[fw&(ug=='FELS_WALD')&(f_dark>=0.12)]='KLIPPE_WAND'
ug[fw&(ug=='FELS_WALD')&(f_schn>=0.5)]='SCHNEE'
ug[ug=='FELS_WALD']='FELS'
ug[ug=='FELS_KLIPPE']='KLIPPE_WAND'
ug[ug=='KLIPPE_KANTE']='KLIPPE_WAND'      # Kante wird nach Glaettung neu bestimmt
fest=ovr|(wasser&(quelle=='MASKE'))
# Randzeile 302 nur 10 px hoch (7560/25=302,4) -> Wert der Zeile darueber [R]
if H%Z and not ovr[-1].any(): ug[-1]=ug[-2]; quelle[-1]='RAND'
# BODEN aus Maske (Senke) ist in c20 Schnee, wo Farbe Schnee zeigt [R]
_bs=(ug=='BODEN')&(f_schn>=0.3)&~ovr; ug[_bs]='SCHNEE'; quelle[_bs]='FARBE'; boden_zu_schnee=int(_bs.sum())          # Overrides und Bachmaske bleiben unangetastet
# (3) Glaettung: 3x3-Mehrheit (>=5 Stimmen) 3 Durchlaeufe, dann Inseln <6 Zellen an Nachbarmehrheit [A]
GK=['BODEN','SCHNEE','SAND','WALD','KLIPPE_WAND','FELS','SCHATTEN','WASSER_EIS','UNBEKANNT']
def _maj():
    c=np.stack([cv2.filter2D((ug==k).astype(np.float32),-1,np.ones((3,3),np.float32),borderType=cv2.BORDER_REFLECT) for k in GK],-1)
    return np.array(GK)[c.argmax(-1)],c.max(-1)
glatt_n=0
for _ in range(3):
    m,c=_maj(); sel=~fest&(c>=5)&(m!=ug); ug[sel]=m[sel]; glatt_n+=int(sel.sum())
for _ in range(3):
    m,c=_maj()
    for k in GK:
        n_,l_,st_,_=cv2.connectedComponentsWithStats((ug==k).astype(np.uint8),8)
        if n_>1:
            kl=np.isin(l_,np.nonzero(st_[:,4]<6)[0][1:])&~fest
            # Mehrheit ohne eigene Klasse
            cc=np.stack([cv2.filter2D((ug==j).astype(np.float32),-1,np.ones((5,5),np.float32)) if j!=k else np.zeros((ny,nx),np.float32) for j in GK],-1)
            mm=np.array(GK)[cc.argmax(-1)]; ug[kl]=mm[kl]; glatt_n+=int(kl.sum())
# Rest-UNBEKANNT: Komponenten <10 Zellen an Nachbarmehrheit [A]
n_,l_,st_,_=cv2.connectedComponentsWithStats((ug=='UNBEKANNT').astype(np.uint8),8)
cc=np.stack([cv2.filter2D((ug==j).astype(np.float32),-1,np.ones((7,7),np.float32)) if j!='UNBEKANNT' else np.zeros((ny,nx),np.float32) for j in GK],-1)
mm=np.array(GK)[cc.argmax(-1)]; kl=np.isin(l_,np.nonzero(st_[:,4]<10)[0][1:]); unb_filter=int(kl.sum()); ug[kl]=mm[kl]; quelle[kl]='FILTER'
# Baumstaemme im Wald: Wand/Fels-Komponenten <200 Zellen, deren Ring >=40 % WALD ist -> WALD [A]
wald_aus_wand=0
_wf=np.isin(ug,['KLIPPE_WAND','FELS'])&~ovr; n_,l_,st_,_=cv2.connectedComponentsWithStats(_wf.astype(np.uint8),8)
_wd=(ug=='WALD')
for i in range(1,n_):
    if st_[i,4]>=200: continue
    x,y,w_,h_=st_[i,:4]; sl=(slice(max(0,y-2),y+h_+2),slice(max(0,x-2),x+w_+2)); c=l_[sl]==i
    r=(cv2.dilate(c.astype(np.uint8),np.ones((5,5),np.uint8))>0)&~c
    if r.sum() and _wd[sl][r].mean()>=0.4: ug[sl][c]='WALD'; wald_aus_wand+=int(c.sum())
# t12u: Sichtpruefungs-Overrides (Klasse von->nach in Rechteck) [S]
ovr12_n=0
_op=os.path.join(os.path.dirname(os.path.abspath(__file__)),'overrides_t12u.csv')
if Z==25 and os.path.exists(_op):
    for _r in csv.DictReader(open(_op)):
        _s=(slice(int(_r['cy0']),int(_r['cy1'])+1),slice(int(_r['cx0']),int(_r['cx1'])+1)); _u=ug[_s]==_r['von']
        ug[_s][_u]=_r['nach']; quelle[_s][_u]='OVERRIDE'; ovr[_s]|=_u; ovr12_n+=int(_u.sum())
# t12u: Suedwald-Band (suedlich des Flusses, y>=SW_Y): Stamm-Wand/Fels -> WALD, Luecken <=4 Zellen schliessen (5x5-Closing) [A]
SW_Y=int(276*25/Z); _band=np.zeros((ny,nx),bool); _band[SW_Y:]=True
_c=_band&np.isin(ug,['KLIPPE_WAND','FELS'])&~ovr; ug[_c]='WALD'; suedwald_n=int(_c.sum())
_wd=cv2.morphologyEx((ug=='WALD').astype(np.uint8),cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))>0
_nv=cv2.blur(f_navy.astype(np.float32),(3,3))>=0.04   # verschneite Baumkronen: dunkle Umrisslinien [A]
_wd|=_nv
_c=_band&_wd&np.isin(ug,['SCHNEE','SCHATTEN'])&~ovr; ug[_c]='WALD'; quelle[_c]='FILTER'; suedwald_n+=int(_c.sum())
# kleine Wandinseln = FELS; KANTE = Wandzelle mit Nicht-Wand im Norden, nur zusammenhaengende Kanten >=3 [A]
n_,l_,st_,_=cv2.connectedComponentsWithStats((ug=='KLIPPE_WAND').astype(np.uint8),8)
ug[np.isin(l_,np.nonzero(st_[:,4]<30)[0][1:])]='FELS'
_wa=ug=='KLIPPE_WAND'; _no=np.zeros_like(_wa); _no[1:]=~_wa[:-1]; _k=_wa&_no
n_,l_,st_,_=cv2.connectedComponentsWithStats(_k.astype(np.uint8),8); _k&=~np.isin(l_,np.nonzero(st_[:,4]<3)[0][1:]); ug[_k]='KLIPPE_KANTE'
# t12u: Rest-UNBEKANNT -> haeufigste Nachbarklasse im 5x5-Fenster (ohne UNBEKANNT) [A]
for _y,_x in zip(*np.nonzero(ug=='UNBEKANNT')):
    _n=ug[max(0,_y-2):_y+3,max(0,_x-2):_x+3].ravel(); _n=_n[_n!='UNBEKANNT']
    if len(_n): _v,_k=np.unique(_n,return_counts=True); ug[_y,_x]=_v[_k.argmax()]; quelle[_y,_x]='FILTER'
unb_nach=int((ug=='UNBEKANNT').sum())
# t12u: Teich NW + gefrorener Bach westlich Krater aus c20-Farbe (G-R>=10, B-R>=18, Zellanteil>=0,4, 2 groesste Komponenten, Loecher gefuellt) + Unterlauf als Linie aus Bild [S/A]
wasser_t12u=0
_wp=os.path.join(os.path.dirname(os.path.abspath(__file__)),'override_wasser_t12u.png')
if os.path.exists(_wp):
    _wm=cv2.imread(_wp,0).astype(np.float32)/255
    if _wm.shape!=(ny,nx): _wm=cv2.resize(_wm,(nx,ny),interpolation=cv2.INTER_AREA)
    _wm=(_wm>=0.5)&~np.isin(ug,['KLIPPE_WAND','KLIPPE_KANTE'])
    wasser_t12u=int((_wm&(ug!='WASSER_EIS')).sum()); ug[_wm]='WASSER_EIS'; quelle[_wm]='OVERRIDE'
# t14u: SCHATTEN-Flecken auf dem Flusseis Sued (Sichtpruefung sa1/sa2): Komponenten im Band y>=262 mit Wasserkontakt -> WASSER_EIS
_sb=(ug=='SCHATTEN'); _sb[:int(262*25/Z)]=False; _n,_l=cv2.connectedComponents(_sb.astype(np.uint8),connectivity=8)
_wn=cv2.dilate((ug=='WASSER_EIS').astype(np.uint8),np.ones((3,3),np.uint8))>0
_ids=np.unique(_l[_sb&_wn]); _m=np.isin(_l,_ids[_ids>0])&_sb; ug[_m]='WASSER_EIS'; quelle[_m]='FILTER'; eis_schatten_n=int(_m.sum())
wasser=(ug=='WASSER_EIS')
# (4) Hindernis ueber ganze Karte: Masken-ID (Fenster) + Gelaende (Wald/Fels/Klippe) [R aus Klasse]
hind_gel=np.isin(ug,['WALD','FELS','KLIPPE_WAND','KLIPPE_KANTE'])
hind_art=np.where(hind>0,'MASKE',np.where(hind_gel,'GELAENDE',''))
begehbar=~(np.isin(ug,['UNBEKANNT','WALD','KLIPPE_WAND','KLIPPE_KANTE','FELS','WASSER_EIS'])|(hind>0))
# t12u: bebaubar aus dem Gelaende: Senke zwischen den Waenden [A-Grenzen], ohne Wand/Wasser/Fels/Schatten/Wald, Mindestabstand Parameter [A]
bauzone_bestand=senke&fe2                                   # alte Fenstergrenze (BB4 & frei_e2), nur als Feld erhalten
BAU_ABST_WAND_M=float(os.environ.get('BAU_ABST_WAND_M','2')); BAU_ABST_WASSER_M=float(os.environ.get('BAU_ABST_WASSER_M','2'))
_q=lambda v:int(round(v*25/Z)); _wall=np.isin(ug,['KLIPPE_WAND','KLIPPE_KANTE'])
basin=np.zeros((ny,nx),bool); KR_X_OST=_q(136)
for y in range(_q(20),_q(257)):
    xs=np.nonzero(_wall[y,_q(71):_q(161)])[0]; xl=_q(71)+xs.max()+1 if len(xs) else KR_X_OST   # rechts der Kraterwand, sonst Krater-Ostkante [A]
    xs=np.nonzero(_wall[y,_q(270):])[0]; xr=_q(270)+xs.min() if len(xs) else nx            # links der Ostgratwand
    basin[y,xl:xr]=True
for x in range(nx):
    ys=np.nonzero(_wall[:_q(76),x])[0]; basin[:ys.max()+1 if len(ys) else 0,x]=False                   # unter der Nordwand
    ys=np.nonzero(_wall[_q(205):_q(257),x])[0]; basin[_q(205)+ys.min() if len(ys) else _q(257):,x]=False  # ueber dem Suedgrat
basin=cv2.morphologyEx(basin.astype(np.uint8),cv2.MORPH_OPEN,np.ones((max(3,_q(9)),)*2,np.uint8))>0  # schmale Auslaeufer (Paesse) kappen [A]
n_,l_=cv2.connectedComponents(basin.astype(np.uint8),connectivity=4); basin=l_==l_[_q(120),_q(230)]
_dw=cv2.distanceTransform((~_wall).astype(np.uint8),cv2.DIST_L2,5)*Z/PXM; _dq=cv2.distanceTransform((~wasser).astype(np.uint8),cv2.DIST_L2,5)*Z/PXM
bebaubar=basin&begehbar&np.isin(ug,['SCHNEE','BODEN','SAND'])&(_dw>=BAU_ABST_WAND_M)&(_dq>=BAU_ABST_WASSER_M)&(hind==0)
# (5) Deko-Kapazitaet aus Massgrundlage (BERICHT_NETZ_E1 9.2: Mindestabstand 1,5 m, Footprint-Rand 0,5 m) [R]
DEKO_ABST=1.5; deko_kap=np.where(begehbar&~np.isin(ug,['SCHATTEN']) | (ug=='SCHATTEN')&begehbar, round((Z/PXM)**2/DEKO_ABST**2,2),0.0)
deko_baum=begehbar&np.isin(ug,['BODEN','SCHNEE','SCHATTEN'])&~bebaubar          # Baum nur ausserhalb Bauzone [A]
deko_fels=begehbar&np.isin(ug,['BODEN','SCHNEE','SCHATTEN','SAND'])
# ---- 3D/Hoehe (t4u, erweitert t9u) ----
from skimage.morphology import skeletonize
BEZUG=float(os.environ.get('BEZUG_M','0'))
KL_PX=(190,240); KL_M=round(sum(KL_PX)/2/PXM,1)
WAND_H={'Krater':(round(KL_M*145/163,1),(71,92,136,204)),'Suedgrat':(round(KL_M*144/163,1),(0,205,328,256)),'Ostgrat':(round(KL_M*127/163,1),(270,60,335,205))}
WAND_H={k:(h,tuple(min(v*25//Z,(nx if i%2==0 else ny)-1) for i,v in enumerate(b))) for k,(h,b) in WAND_H.items()}  # Fenster in z25-Zellen, auf Z skaliert
_wk=np.isin(ug,['KLIPPE_WAND','KLIPPE_KANTE'])
NB=int(ny*0.25); nord=np.zeros((ny,nx),bool); nord[:NB]=True
hoehe=np.full((ny,nx),BEZUG); hq=np.full((ny,nx),'A',dtype='U1'); hq[senke]='R'
for x in range(nx):                     # Nordplateau: oberhalb der obersten Nordwandzelle = Oberkante [A]
    yy=np.nonzero(_wk[:NB,x])[0]
    if len(yy): hoehe[:yy.min(),x]=BEZUG+KL_M
_h,(a_,b_,c_,d_)=WAND_H['Suedgrat']
for x in range(a_,c_+1):                # Suedvorland: unterhalb der untersten Gratwand, Grat faellt nach Sueden ab [A]
    yy=np.nonzero(_wk[b_:d_+1,x])[0]
    if len(yy): hoehe[b_+yy.max()+1:,x]=BEZUG-_h
_h,(a_,b_,c_,d_)=WAND_H['Ostgrat']
for y in range(b_,d_+1):                # Ostplateau: rechts der aeussersten Ostwand liegt hoeher (Wand zeigt nach Westen) [A]
    xx=np.nonzero(_wk[y,a_:c_+1])[0]
    if len(xx): hoehe[y,a_+xx.max()+1:]=BEZUG+_h
hoehe[senke&~wasser]=BEZUG
klippe_h=np.where(_wk,KL_M,np.nan); wand_name=np.where(_wk&nord,'Nord','')
for _n,(_h,(_a,_b,_c,_d)) in WAND_H.items():
    _m=np.zeros((ny,nx),bool); _m[_b:_d+1,_a:_c+1]=True; _m&=_wk&~nord; klippe_h[_m]=_h; wand_name[_m]=_n
klippe_quelle=np.where(np.isnan(klippe_h),'',np.where(nord,'R','A'))
kl_kante=ug=='KLIPPE_KANTE'
klippe=np.where(kl_kante,'KANTE',np.where(ug=='KLIPPE_WAND','WAND',''))
gy,gx=np.gradient(hoehe); nei=np.degrees(np.arctan(np.hypot(gx,gy)/(Z/PXM)))
nei[_wk]=90.0
# Fluss: Mittellinie aus bach_schutz, Richtung aus Bachpolylinie frei_e2.py [S]
wm=A['bach_schutz'][::5,::5].astype(np.uint8)
dt=cv2.distanceTransform(wm,cv2.DIST_L2,5)*5          # px
sk=skeletonize(wm>0)
POLY={'BACH_NORD':[(-34,-12),(-36,0),(-39,15),(-44,40),(-49,60),(-52,80),(-54,92)],'BACH_SUED':[(-52,112),(-40,122),(-25,130),(-15,140)]}
P={k:np.array([((x+200)*30,(y+40)*30) for x,y in v],float) for k,v in POLY.items()}
SEE=(np.array([(-60+200)*30,(102+40)*30]),17*30)
fluss=np.zeros((ny,nx),'U12'); rich=np.zeros((ny,nx),'U2'); breite=np.full((ny,nx),np.nan)
D8=['O','SO','S','SW','W','NW','N','NO']
for cy,cx in zip(*np.nonzero(wasser)):
    p=np.array([cx*Z+Z/2,cy*Z+Z/2])
    if np.hypot(*(p-SEE[0]))<=SEE[1]: fluss[cy,cx]='SEE'; continue
    if quelle[cy,cx]=='FARBE': fluss[cy,cx]='WASSER_FARBE'; continue
    best=None
    for k,L in P.items():
        for a,b in zip(L[:-1],L[1:]):
            t=np.clip(np.dot(p-a,b-a)/np.dot(b-a,b-a),0,1); d=np.hypot(*(p-(a+t*(b-a))))
            if best is None or d<best[0]: best=(d,k,b-a)
    fluss[cy,cx]=best[1]; v=best[2]; ang=np.degrees(np.arctan2(v[1],v[0]))%360; rich[cy,cx]=D8[int((ang+22.5)//45)%8]
for k in ['BACH_NORD','BACH_SUED','SEE']:
    pass
# Breite je Zelle: 2*max. Abstand zum Ufer auf Mittellinie im Zellblock [R]
bw=np.zeros((ny*Z//5+Z,nx*Z//5+Z)); skd=np.where(sk,dt*2,0); bw[:skd.shape[0],:skd.shape[1]]=skd
f=Z//5; bwg=bw[:ny*f,:nx*f].reshape(ny,f,nx,f).max((1,3)); breite[(bwg>0)&wasser]=bwg[(bwg>0)&wasser]/PXM
tiefe=np.full((ny,nx),np.nan)                         # keine Quelle -> leer (Luecke, siehe SPEC)
ufer=(cv2.dilate(wasser.astype(np.uint8),np.ones((3,3),np.uint8))>0)&~wasser&begehbar
MAXN=30.0
b3=(nei<=MAXN)&begehbar
fmt=lambda v: '' if np.isnan(v) else round(float(v),2)
o=f'raster_c20_z{Z}'
SP=['cx','cy','px_x','px_y','untergrund','untergrund_quelle','hindernis_id','hindernis_art','wasser_eis','schnee','senke_bb4','h4_ext','frei_e2','begehbar','bebaubar','bauzone_bestand','senke_becken','klippe','wand_name','skin_slot','hoehe_m','hoehe_quelle','neigung_grad','klippe_hoehe_m','klippe_hoehe_quelle','fluss_id','fliess_richtung','fluss_breite_m','wasser_tiefe_m','ufer','begehbar_3d','deko_kapazitaet','deko_baum_ok','deko_fels_ok','flaeche_m2']
with open(o+'_zellen.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(SP)
    for y in range(ny):
        for x in range(nx):
            w.writerow([x,y,x*Z,y*Z,ug[y,x],quelle[y,x],int(hind[y,x]),hind_art[y,x],int(wasser[y,x]),int(schnee[y,x]),int(senke[y,x]),int(h4[y,x]),int(fe2[y,x]),int(begehbar[y,x]),int(bebaubar[y,x]),int(bauzone_bestand[y,x]),int(basin[y,x]),klippe[y,x],wand_name[y,x],'ug_'+ug[y,x].lower(),fmt(hoehe[y,x]),hq[y,x],fmt(nei[y,x]),fmt(klippe_h[y,x]),klippe_quelle[y,x],fluss[y,x],rich[y,x],fmt(breite[y,x]),'',int(ufer[y,x]),int(b3[y,x]),deko_kap[y,x],int(deko_baum[y,x]),int(deko_fels[y,x]),(Z/PXM)**2])
# ---- Overlay-Layer Plaetze/Wege (abschaltbar, t10u) ----
DP=[]
for fn in sorted(glob.glob(R+'zonen_c20/modulsystem_e1/karten/e1/dekoplaetze/*.json')):
    for p in json.load(open(fn))['dekoplaetze']:
        if p.get('status')=='ok': DP.append(p)
dp_n=np.zeros((ny,nx),np.int16)
for p in DP:
    x,y=p['pos']; cx,cy=int((x+200)*30//Z),int((y+40)*30//Z)
    if 0<=cx<nx and 0<=cy<ny: dp_n[cy,cx]+=1
bp=(platz>0)&bebaubar
with open(o+'_overlay_plaetze_wege.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['cx','cy','zone','platz','bauplatz','weg_id','weg_klasse','hof','feuer','bruecke','furt','dekoplaetze_netz'])
    for y,x in zip(*np.nonzero((zone!='')|(platz>0)|(weg!='')|hof|feuer|bruecke|(dp_n>0))):
        w.writerow([x,y,zone[y,x],ids[platz[y,x]-1]['nr'] if platz[y,x] else '',int(bp[y,x]),weg[y,x],weg_kl[y,x],int(hof[y,x]),int(feuer[y,x]),int(bruecke[y,x]),int(wasser[y,x]&(weg[y,x]!='')&~bruecke[y,x]),int(dp_n[y,x])])
st={k:int(v) for k,v in zip(*np.unique(ug,return_counts=True))}
json.dump(dict(karte='KANDIDAT_NICHT_FREIGEGEBEN_master_v18_p7_c20.png',karte_md5='d916c6ace52352d7fcf4ef13591cb5c0',karte_px=[W,H],px_pro_m=PXM,zelle_px=Z,zelle_m=Z/PXM,raster=[nx,ny],epoche='E1',epochen_variante='fest_c20',
  layer={'gelaende':o+'_zellen.csv','overlay_plaetze_wege':o+'_overlay_plaetze_wege.csv'},
  unbekannt_vorher=unb_vor,unbekannt_nachher=unb_nach,unbekannt_filter=unb_filter,glaettung_zellen=glatt_n,boden_zu_schnee=boden_zu_schnee,wasser_t12u=wasser_t12u,ovr12_n=ovr12_n,suedwald_n=suedwald_n,wald_aus_wand=wald_aus_wand,overrides_zellen=ovr_n,schatten_statt_wasser=schatten_wasser,zaehlung_vor_t9u=stat_vor,
  wand_hoehe_m={'Nord':[KL_M,'R'],**{k:[v[0],'A'] for k,v in WAND_H.items()},'sonstige':[KL_M,'A']},wand_hoehe_herleitung='Median senkrechte Felslaufweite px: Nord 163, Krater 145, Suedgrat 144, Ostgrat 127; h=8.6*px/163; Schatten nicht messbar',klippe_nord_band_m=[7.6,9.6],
  hoehe_stufen_m={'Senke':BEZUG,'Nordplateau':BEZUG+KL_M,'Ostplateau':BEZUG+WAND_H['Ostgrat'][0],'Suedvorland':BEZUG-WAND_H['Suedgrat'][0],'Rest':BEZUG},
  quelle_anteil={k:round(float((quelle==k).mean()*100),1) for k in ['MASKE','FARBE','FILTER','KEINE']},
  zaehlung_untergrund=st,begehbar=int(begehbar.sum()),bebaubar=int(bebaubar.sum()),bauzone_bestand=int(bauzone_bestand.sum()),senke_becken=int(basin.sum()),bebaubar_param=dict(abstand_wand_m=BAU_ABST_WAND_M,abstand_wasser_m=BAU_ABST_WASSER_M,marker='A'),bebaubar_ausserhalb_bestand=int((bebaubar&~bauzone_bestand).sum()),hindernis_maske=int((hind>0).sum()),hindernis_gelaende=int((hind_art=='GELAENDE').sum()),plaetze=len(ids),dekoplaetze_netz=len(DP),
  groessenbezug=dict(px_pro_m=PXM,zelle_m=Z/PXM,zelle_m2=(Z/PXM)**2,unity_pro_m=PXM/256,ppu=256,nordwand_m=KL_M,deko_mindestabstand_m=DEKO_ABST,deko_footprint_rand_m=0.5,quelle='MASSGRUNDLAGE 25 px/m [F]; BERICHT_NETZ_E1 9.2'),
  bezug_m=BEZUG,neigung_max_3d=MAXN,dreid=dict(achse_z='oben, Meter',einheit='m',ppu=256,unity_pro_m=PXM/256,px_pro_m=PXM),
  fluss_zellen={k:int((fluss==k).sum()) for k in ['BACH_NORD','BACH_SUED','SEE','WASSER_FARBE']},fluss_breite_m_median={k:(round(float(np.nanmedian(breite[fluss==k])),2) if np.any(~np.isnan(breite[fluss==k])) else None) for k in ['BACH_NORD','BACH_SUED']},ufer=int(ufer.sum()),
  luecken=['wasser_tiefe_m leer: keine Quelle','hoehe_m ausserhalb Senke nur Stufen [A], keine Hoehenkarte','Kraterinneres auf Bezug [A]']),open(o+'_meta.json','w'),ensure_ascii=False,indent=1)
COL={'BODEN':(196,170,120),'SCHNEE':(240,243,247),'SAND':(230,205,140),'SCHATTEN':(160,170,210),'WALD':(25,110,55),'FELS':(150,140,130),'KLIPPE_WAND':(110,60,25),'KLIPPE_KANTE':(255,215,0),'WASSER_EIS':(60,120,220),'UNBEKANNT':(255,0,255)}
s=3
try: ft=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
except: ft=None
def legende(a,items,titel,fn,extra=()):
    im=Image.fromarray(a); L=Image.new('RGB',(im.width+380,max(im.height,600)),'white'); L.paste(im,(0,0)); d=ImageDraw.Draw(L); y=20
    d.text((im.width+15,y),titel,fill='black',font=ft); y+=30
    for k,c in items: d.rectangle([im.width+15,y,im.width+40,y+20],fill=c,outline='black'); d.text((im.width+50,y),f'{k} ({int(st.get(k,0))})' if k in st else k,fill='black',font=ft); y+=28
    for t in extra: d.text((im.width+15,y),t,fill='black',font=ft); y+=24
    L.save(fn)
img=np.zeros((ny,nx,3),np.uint8)
for k,c in COL.items(): img[ug==k]=c
a=np.asarray(Image.fromarray(img).resize((nx*s,ny*s),Image.NEAREST)).copy()
legende(a,list(COL.items()),f'Gelaende c20, Zelle {Z}px = {Z/PXM:g} m',o+'_vorschau.png',['nur Untergrundfarben, keine Schraffur','bebaubar: eigene Vorschau _bebaubar.png','Plaetze/Wege: _overlay_plaetze_wege.png'])
# Bebaubar-Vorschau (t12u): Gelaende blass, bebaubar gruen halbtransparent, Bauzone-Bestand Umriss, Hindernis-Maske orange
bv=(img*0.5+255*0.5).astype(np.float32); bv[bebaubar]=bv[bebaubar]*0.45+np.array([0,170,60])*0.55; bv[hind>0]=bv[hind>0]*0.5+np.array([255,120,0])*0.5
bv=np.asarray(Image.fromarray(bv.astype(np.uint8)).resize((nx*s,ny*s),Image.NEAREST)).copy()
_cn,_=cv2.findContours(np.repeat(np.repeat(bauzone_bestand,s,0),s,1).astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); cv2.drawContours(bv,_cn,-1,(0,0,0),1)
_cn,_=cv2.findContours(np.repeat(np.repeat(basin,s,0),s,1).astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); cv2.drawContours(bv,_cn,-1,(200,0,200),1)
st['bebaubar']=int(bebaubar.sum()); st['bauzone_bestand']=int(bauzone_bestand.sum()); st['senke_becken']=int(basin.sum())
legende(bv,[('bebaubar',(0,170,60)),('Hindernis Maske',(255,120,0)),('bauzone_bestand (Umriss schwarz)',(0,0,0)),('senke_becken (Umriss violett)',(200,0,200))],f'Bebaubar aus Gelaende, Abstand Wand {BAU_ABST_WAND_M:g} m / Wasser {BAU_ABST_WASSER_M:g} m [A]',o+'_bebaubar.png',[f"bebaubar {int(bebaubar.sum())} Zellen",f"davon ausserhalb Bestand {int((bebaubar&~bauzone_bestand).sum())}"])
# Overlay-Vorschau
ov=(img*0.45+255*0.55).astype(np.uint8)
for m_,c in [(zone!='',(230,230,170)),(platz>0,(80,190,90)),(weg!='',(150,100,50)),(hof,(220,190,90)),(feuer,(230,60,30)),(bruecke,(130,60,160)),(dp_n>0,(255,0,120))]: ov[m_]=c
legende(np.asarray(Image.fromarray(ov).resize((nx*s,ny*s),Image.NEAREST)),[('Zone',(230,230,170)),('Platz (99)',(80,190,90)),('Weg',(150,100,50)),('Hof',(220,190,90)),('Feuer',(230,60,30)),('Bruecke',(130,60,160)),(f'Dekoplatz Netz ({len(DP)})',(255,0,120))],'Overlay Plaetze/Wege (abschaltbar)',o+'_overlay_plaetze_wege.png',['Gelaende blass darunter'])
# Hoehen-/Fluss-Ansicht
v=np.zeros((ny,nx,3),np.uint8)
HC={BEZUG:(120,200,120),BEZUG+KL_M:(240,200,120),BEZUG+WAND_H['Ostgrat'][0]:(230,170,90),BEZUG-WAND_H['Suedgrat'][0]:(140,170,230)}
for h_,c in HC.items(): v[np.isclose(hoehe,h_)]=c
v[klippe_quelle=='R']=(120,60,20); v[klippe_quelle=='A']=(190,120,170)
FC={'BACH_NORD':(30,90,230),'BACH_SUED':(0,170,220),'SEE':(20,40,140),'WASSER_FARBE':(100,140,200)}
for k,c in FC.items(): v[fluss==k]=c
v[ufer]=(240,220,120)
im=Image.fromarray(v).resize((nx*s,ny*s),Image.NEAREST); d0=ImageDraw.Draw(im)
DV={'O':(1,0),'SO':(1,1),'S':(0,1),'SW':(-1,1),'W':(-1,0),'NW':(-1,-1),'N':(0,-1),'NO':(1,-1)}
for cy,cx in zip(*np.nonzero(rich!='')):
    if (cy+cx)%6: continue
    dx,dy=DV[rich[cy,cx]]; x0,y0=cx*s+1,cy*s+1; d0.line([x0,y0,x0+dx*6,y0+dy*6],fill='white')
legende(np.asarray(im),[(f'Senke/Rest {BEZUG:g} m [R/A]',(120,200,120)),(f'Nordplateau +{KL_M} m [A]',(240,200,120)),(f"Ostplateau +{WAND_H['Ostgrat'][0]} m [A]",(230,170,90)),(f"Suedvorland -{WAND_H['Suedgrat'][0]} m [A]",(140,170,230)),(f'Nordwand {KL_M} m [R]',(120,60,20)),(f'andere Waende {WAND_H["Ostgrat"][0]}-{WAND_H["Krater"][0]} m [A]',(190,120,170)),('BACH_NORD',FC['BACH_NORD']),('BACH_SUED',FC['BACH_SUED']),('SEE',FC['SEE']),('Wasser (Farbe)',FC['WASSER_FARBE']),('Ufer',(240,220,120))],f'Hoehe/Fluss, Zelle {Z}px',o+'_hoehe_fluss.png',['weisse Striche = Fliessrichtung','Wassertiefe: keine Quelle (leer)'])
_o=Image.open(R+'KANDIDAT_NICHT_FREIGEGEBEN_master_v18_p7_c20.png').convert('RGB').resize((nx*3,ny*3),Image.BOX)
_v=Image.open(o+'_vorschau.png').crop((0,0,nx*3,ny*3))
Image.blend(_o,_v,0.5).save(o+'_overlay.png')
_n=Image.new('RGB',(nx*6+10,ny*3),'white'); _n.paste(_o,(0,0)); _n.paste(_v,(nx*3+10,0)); _n.save(o+'_vergleich.png')
_u=(ug=='UNBEKANNT').astype(np.uint8); _n,_l,_st,_=cv2.connectedComponentsWithStats(_u,8)
with open(o+'_unbekannt_pruefliste.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['nr','cx0','cy0','cx1','cy1','zellen','px_x0','px_y0','px_x1','px_y1'])
    for i in np.argsort(-_st[1:,4])+1:
        x,y,ww,hh,a_=_st[i]; w.writerow([i,x,y,x+ww-1,y+hh-1,a_,x*Z,y*Z,(x+ww)*Z,(y+hh)*Z])
np.save('/tmp/ug_z%d.npy'%Z,ug)
print(json.dumps(st),unb_nach,begehbar.sum(),bebaubar.sum())
