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
wasser=wasser|(ug=='WASSER_EIS')
begehbar=~((ug=='UNBEKANNT')|(ug=='WALD')|(ug=='FELS_KLIPPE')|(ug=='WASSER_EIS')|(ug=='FELS_WALD')|(hind>0))|(ug=='WEG')|(ug=='BRUECKE')
bebaubar=senke&fe2&~wasser&~fz&(hind==0)&(weg=='')&~bruecke&~feuer

# ---- 3D/Hoehe/Fluss (t4u) ----
from skimage.morphology import skeletonize
BEZUG=float(os.environ.get('BEZUG_M','0'))          # Bezugsniveau = Senkenboden [A]
KL_PX=(190,240)                                       # Klippenwand Nord [S MASSGRUNDLAGE], Verkuerzung unbekannt
KL_M=round(sum(KL_PX)/2/PXM,1)                        # 8.6 m [R], ohne Projektionskorrektur [A]
hoehe=np.full((ny,nx),np.nan)
hoehe[senke&~wasser]=BEZUG                            # Senke als flach angenommen [A]
rand_out=(ug=='FELS_KLIPPE')|(ug=='FELS_WALD')|(ug=='WALD')|(ug=='UNBEKANNT')
nb=cv2.dilate(senke.astype(np.uint8),np.ones((3,3),np.uint8))>0
kl_kante=rand_out&nb                                  # Uebergang Senke->Fels/Rand = Klippenkante [R aus Masken]
nord=np.zeros((ny,nx),bool); nord[:int(ny*0.25),:]=True   # Nordwand: obere 25 % der Karte [A]
klippe_h=np.full((ny,nx),np.nan); klippe_h[kl_kante&nord]=KL_M
hoehe[kl_kante&nord]=BEZUG+KL_M                       # Oberkante Nordwand [R]
gy,gx=np.gradient(np.nan_to_num(hoehe,nan=np.nan))
nei=np.degrees(np.arctan(np.hypot(gx,gy)/(Z/PXM)))    # [R] nur wo Nachbarn bekannt
klippe=np.where(kl_kante,'KANTE','')
# Fluss: Mittellinie aus bach_schutz, Richtung aus Bachpolylinie frei_e2.py [S]
wm=A['bach_schutz'][::5,::5].astype(np.uint8)
dt=cv2.distanceTransform(wm,cv2.DIST_L2,5)*5          # px
sk=skeletonize(wm>0)
POLY={'BACH_NORD':[(-34,-12),(-36,0),(-39,15),(-44,40),(-49,60),(-52,80),(-54,92)],'BACH_SUED':[(-52,112),(-40,122),(-25,130),(-15,140)]}
P={k:np.array([((x+200)*30,(y+40)*30) for x,y in v],float) for k,v in POLY.items()}
SEE=(np.array([(-60+200)*30,(102+40)*30]),17*30)
fluss=np.zeros((ny,nx),'U10'); rich=np.zeros((ny,nx),'U2'); breite=np.full((ny,nx),np.nan)
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
tiefe=np.full((ny,nx),np.nan)                         # keine Quelle -> leer
ufer=(cv2.dilate(wasser.astype(np.uint8),np.ones((3,3),np.uint8))>0)&~wasser&begehbar
furt=wasser&(weg!='')&~bruecke                        # Weg quert Wasser ohne Bruecke [R]
MAXN=30.0                                             # begehbar_3d bis 30 Grad [A]
b3=np.where(np.isnan(nei),begehbar,(nei<=MAXN)&begehbar)|furt
fmt=lambda v: '' if np.isnan(v) else round(float(v),2)
o=f'raster_c20_z{Z}'
with open(o+'_zellen.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['cx','cy','px_x','px_y','untergrund','untergrund_quelle','zone','platz','weg_id','weg_klasse','hindernis','wasser_eis','schnee','senke_bb4','h4_ext','frei_e2','begehbar','bebaubar','klippe','skin_slot','hoehe_m','neigung_grad','klippe_hoehe_m','fluss_id','fliess_richtung','fluss_breite_m','wasser_tiefe_m','ufer','furt','begehbar_3d'])
    for y in range(ny):
        for x in range(nx):
            w.writerow([x,y,x*Z,y*Z,ug[y,x],quelle[y,x],zone[y,x],ids[platz[y,x]-1]['nr'] if platz[y,x] else '',weg[y,x],weg_kl[y,x],int(hind[y,x]),int(wasser[y,x]),int(schnee[y,x]),int(senke[y,x]),int(h4[y,x]),int(fe2[y,x]),int(begehbar[y,x]),int(bebaubar[y,x]),klippe[y,x],'ug_'+ug[y,x].lower(),fmt(hoehe[y,x]),fmt(nei[y,x]),fmt(klippe_h[y,x]),fluss[y,x],rich[y,x],fmt(breite[y,x]),'',int(ufer[y,x]),int(furt[y,x]),int(b3[y,x])])
st={k:int(v) for k,v in zip(*np.unique(ug,return_counts=True))}
json.dump(dict(karte='KANDIDAT_NICHT_FREIGEGEBEN_master_v18_p7_c20.png',karte_md5='d916c6ace52352d7fcf4ef13591cb5c0',karte_px=[W,H],px_pro_m=PXM,zelle_px=Z,zelle_m=Z/PXM,raster=[nx,ny],epoche='E1',epochen_variante='fest_c20',quelle_anteil={k:round(float((quelle==k).mean()*100),1) for k in ['MASKE','FARBE','KEINE']},
  zaehlung_untergrund=st,begehbar=int(begehbar.sum()),bebaubar=int(bebaubar.sum()),plaetze=len(ids),
  bezug_m=BEZUG,klippe_nord_m=KL_M,neigung_max_3d=MAXN,dreid=dict(achse_z='oben, Meter',einheit='m',ppu=256,unity_pro_m=PXM/256,px_pro_m=PXM),zellen_mit_hoehe=int((~np.isnan(hoehe)).sum()),fluss_zellen={k:int((fluss==k).sum()) for k in ['BACH_NORD','BACH_SUED','SEE']},fluss_breite_m_median={k:(round(float(np.nanmedian(breite[fluss==k])),2) if np.any(~np.isnan(breite[fluss==k])) else None) for k in ['BACH_NORD','BACH_SUED']},furt=int(furt.sum()),ufer=int(ufer.sum()),hinweis='hoehe_m nur Senke (Bezug) + Nordklippe; Rest leer, keine Hoehenkarte. wasser_tiefe_m leer, keine Quelle.'),open(o+'_meta.json','w'),ensure_ascii=False,indent=1)
COL={'BODEN':(196,170,120),'UNBEKANNT':(255,0,255),'SAND':(225,200,140),'WALD':(30,90,40),'FELS_KLIPPE':(130,70,30),'SCHNEE':(235,240,245),'FELS_WALD':(90,90,90),'WASSER_EIS':(60,120,220),'HOF':(220,190,90),'FEUER':(230,60,30),'WEG':(150,100,50),'BRUECKE':(130,60,160)}
img=np.zeros((ny,nx,3),np.uint8)
for k,c in COL.items(): img[ug==k]=c
img[(platz>0)&(ug!='WEG')]=(80,190,90); img[hind>0]=(255,140,0)
s=3; im=Image.fromarray(img).resize((nx*s,ny*s),Image.NEAREST); a=np.asarray(im).copy()
bb=np.repeat(np.repeat(bebaubar,s,0),s,1); a[bb&((np.indices(bb.shape).sum(0)%6)<1)]=(0,0,0)
im=Image.fromarray(a); L=Image.new('RGB',(im.width+330,max(im.height,600)),'white'); L.paste(im,(0,0)); d=ImageDraw.Draw(L)
try: ft=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
except: ft=None
items=list(COL.items())+[('PLATZ (99 Slots)',(80,190,90)),('HINDERNIS',(255,140,0))]
y=20; d.text((im.width+15,y),f'c20, Zelle {Z}px = {Z/PXM:g} m',fill='black',font=ft); y+=30
for k,c in items: d.rectangle([im.width+15,y,im.width+40,y+20],fill=c,outline='black'); d.text((im.width+50,y),k,fill='black',font=ft); y+=30
d.text((im.width+15,y),'schwarz schraffiert = bebaubar',fill='black',font=ft)
L.save(o+'_vorschau.png'); print(json.dumps(st),begehbar.sum(),bebaubar.sum(),nx,ny)

# Hoehen-/Fluss-Ansicht
v=np.full((ny,nx,3),200,np.uint8); v[np.isnan(hoehe)]=(170,170,170)
v[hoehe==BEZUG]=(120,200,120); v[~np.isnan(klippe_h)]=(120,60,20); v[(klippe=='KANTE')&np.isnan(klippe_h)]=(200,140,90)
FC={'BACH_NORD':(30,90,230),'BACH_SUED':(0,170,220),'SEE':(20,40,140)}
for k,c in FC.items(): v[fluss==k]=c
v[ufer]=(240,220,120); v[furt]=(255,0,0)
im=Image.fromarray(v).resize((nx*s,ny*s),Image.NEAREST); d0=ImageDraw.Draw(im)
DV={'O':(1,0),'SO':(1,1),'S':(0,1),'SW':(-1,1),'W':(-1,0),'NW':(-1,-1),'N':(0,-1),'NO':(1,-1)}
for cy,cx in zip(*np.nonzero(rich!='')):
    if (cy+cx)%6: continue
    dx,dy=DV[rich[cy,cx]]; x0,y0=cx*s+1,cy*s+1; d0.line([x0,y0,x0+dx*6,y0+dy*6],fill='white')
L=Image.new('RGB',(im.width+360,max(im.height,600)),'white'); L.paste(im,(0,0)); d=ImageDraw.Draw(L); y=20
d.text((im.width+15,y),f'Hoehe/Fluss, Zelle {Z}px',fill='black',font=ft); y+=30
for k,c in [(f'Senke hoehe_m={BEZUG:g} [A]',(120,200,120)),(f'Nordklippe {KL_M} m [R]',(120,60,20)),('Kante ohne Hoehe',(200,140,90)),('hoehe leer (keine Quelle)',(170,170,170)),('BACH_NORD',FC['BACH_NORD']),('BACH_SUED',FC['BACH_SUED']),('SEE',FC['SEE']),('Ufer (flach begehbar)',(240,220,120)),('Furt',(255,0,0))]:
    d.rectangle([im.width+15,y,im.width+40,y+20],fill=c,outline='black'); d.text((im.width+50,y),k,fill='black',font=ft); y+=30
d.text((im.width+15,y),'weisse Striche = Fliessrichtung',fill='black',font=ft)
L.save(o+'_hoehe_fluss.png')
print(json.load(open(o+'_meta.json')))

_o=Image.open(R+'KANDIDAT_NICHT_FREIGEGEBEN_master_v18_p7_c20.png').convert('RGB').resize((nx*3,ny*3),Image.BOX)
_v=Image.open(o+'_vorschau.png').crop((0,0,nx*3,ny*3))
Image.blend(_o,_v,0.5).save(o+'_overlay.png')
_n=Image.new('RGB',(nx*6+10,ny*3),'white'); _n.paste(_o,(0,0)); _n.paste(_v,(nx*3+10,0)); _n.save(o+'_vergleich.png')
