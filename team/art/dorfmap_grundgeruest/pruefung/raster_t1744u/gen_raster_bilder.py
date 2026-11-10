"""t1744u Raster-Methode: setzt Uebersicht, Feldbilder, Gruppenboegen und Index aus gerenderten Rohbildern zusammen.
Rohbilder: render_kameras.js (Kameras aus gen_kameras.py). Karte/Zellwerte werden nicht veraendert."""
import json, math, os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from raster_def import *
ROH=sys.argv[1] if len(sys.argv)>1 else '/tmp/rr'
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def F(n): return ImageFont.truetype(FB,n)
import scipy.ndimage as nd
H0=hoehen(); FL=felder(); H=nd.gaussian_filter(H0,2)  # Feldumriss Schraegansicht: leicht geglaettet
HU=nd.gaussian_filter(H0,8)  # Uebersicht: stark geglaettet -> gerade Linien
KF={k['name']:k for k in json.load(open(os.path.join(HIER,'kameras_felder.json')))}
KU=json.load(open(os.path.join(HIER,'kameras_uebersicht.json')))[0]
BANNER=open(f'{ROH}/u/banner.txt').read().strip()
COMMIT=subprocess.check_output(['git','rev-parse','--short','HEAD'],cwd=HIER).decode().strip()
STAND=f'Commit {COMMIT} | {BANNER}'
def proj(k,P):
    p=np.array(k['p'],float);t=np.array(k['t'],float);f=t-p;f/=np.linalg.norm(f)
    r=np.cross(f,[0,1,0]);r/=np.linalg.norm(r);u=np.cross(r,f);v=np.array(P,float)-p
    d=v@f; th=math.tan(math.radians(25)); a=k['w']/k['h']
    if d<=0.5: return None
    return ((v@r)/(d*th*a)+1)/2*k['w'], (1-(v@u)/(d*th))/2*k['h']
def hz(x,z): return H[min(max(int(z),0),NY-1),min(max(int(x),0),NX-1)]
def umriss(k,x0,x1,z0,z1,schritt=1.0):
    pts=[]
    for (ax,az,bx,bz) in [(x0,z0,x1,z0),(x1,z0,x1,z1),(x1,z1,x0,z1),(x0,z1,x0,z0)]:
        n=max(1,int(max(abs(bx-ax),abs(bz-az))/schritt))
        for i in range(n+1):
            x=ax+(bx-ax)*i/n; z=az+(bz-az)*i/n; q=proj(k,(x,hz(min(x,NX-0.01),min(z,NY-0.01)),z)); pts.append(q)
    return pts
def linie(d,pts,col,w):
    for a,b in zip(pts,pts[1:]):
        if a and b: d.line([a,b],fill=col,width=w)
def textbox(d,xy,s,f,fg=(255,255,255),bg=(0,0,0),pad=6,anchor='mm'):
    bb=d.textbbox(xy,s,font=f,anchor=anchor); d.rectangle([bb[0]-pad,bb[1]-pad,bb[2]+pad,bb[3]+pad],fill=bg); d.text(xy,s,font=f,fill=fg,anchor=anchor)
# ---- Uebersicht
U=Image.open(f'{ROH}/u/uebersicht_roh.png').convert('RGB'); d=ImageDraw.Draw(U)
def up(x,z): return proj(KU,(x,HU[min(int(z),NY-1),min(int(x),NX-1)],z))
for gx in GX:
    linie(d,[up(gx,z) for z in np.arange(0,NY+.1,1)],(0,0,0),6); linie(d,[up(gx,z) for z in np.arange(0,NY+.1,1)],(255,235,0),3)
for gy in GY:
    linie(d,[up(x,gy) for x in np.arange(0,NX+.1,1)],(0,0,0),6); linie(d,[up(x,gy) for x in np.arange(0,NX+.1,1)],(255,235,0),3)
for f in FL:
    q=up((f['cx0']+f['cx1']+1)/2,(f['cy0']+f['cy1']+1)/2); textbox(d,q,f['feld'],F(38),bg=(170,0,0),pad=5)
W=1080; kopf=150; fuss=230; O=Image.new('RGB',(W,kopf+U.height+fuss),(20,20,20)); O.paste(U,(0,kopf)); d=ImageDraw.Draw(O)
d.text((W//2,45),'Epodarien Dorfmap – Raster',font=F(52),fill='white',anchor='mm')
d.text((W//2,110),'Draufsicht, Norden oben | 8 Spalten A–H × 7 Reihen 1–7',font=F(30),fill=(255,235,0),anchor='mm')
y=kopf+U.height+20
for s in ['Pro Feld bitte nur: „passt“ oder „falsch“',f'Feld = 42 m breit × 43–44 m hoch (Zellen 1 m)',STAND]:
    d.text((W//2,y+30),s,font=F(30 if 'Commit' not in s else 24),fill='white',anchor='mm'); y+=65
O.save(os.path.join(HIER,'uebersicht_raster.jpg'),quality=90)
# ---- Insetkarte
INS_W=260; ins_basis=U.copy().resize((INS_W,int(U.height*INS_W/U.width)))
def inset(f):
    I=Image.open(f'{ROH}/u/uebersicht_roh.png').convert('RGBA'); L=Image.new('RGBA',I.size,(0,0,0,0)); d=ImageDraw.Draw(L)
    a=up(f['cx0'],f['cy0']); b=up(f['cx1']+1,f['cy1']+1)
    for gx in GX: d.line([up(gx,0),up(gx,NY)],fill=(255,235,0,255),width=3)
    for gy in GY: d.line([up(0,gy),up(NX,gy)],fill=(255,235,0,255),width=3)
    d.rectangle([a,b],fill=(255,0,0,110)); d.rectangle([a,b],outline=(0,0,0,255),width=18); d.rectangle([a,b],outline=(255,30,30,255),width=11)
    I=Image.alpha_composite(I,L).convert('RGB')
    p0=up(0,0); p1=up(NX,NY); I=I.crop((int(p0[0])-6,int(p0[1])-6,int(p1[0])+6,int(p1[1])+6))
    I=I.resize((INS_W,int(I.height*INS_W/I.width)),Image.LANCZOS); d=ImageDraw.Draw(I)
    d.rectangle([0,0,I.width-1,I.height-1],outline='white',width=3)
    textbox(d,(I.width//2,14),'Lage '+f['feld'],F(20),bg=(0,0,0),pad=3); return I
# ---- Feldbilder
os.makedirs(os.path.join(HIER,'felder'),exist_ok=True); idx=[]
for f in FL:
    n='feld_'+f['feld']; k=KF[n]; R=Image.open(f'{ROH}/f/{n}.png').convert('RGB'); d=ImageDraw.Draw(R)
    pts=umriss(k,f['cx0'],f['cx1']+1,f['cy0'],f['cy1']+1); linie(d,pts,(0,0,0),7); linie(d,pts,(255,235,0),3)
    I=inset(f); R.paste(I,(R.width-I.width-8,R.height-I.height-8))
    kopf=90; B=Image.new('RGB',(R.width,R.height+kopf+44),(20,20,20)); B.paste(R,(0,kopf)); d=ImageDraw.Draw(B)
    textbox(d,(20,kopf//2),f['feld'],F(66),bg=(170,0,0),anchor='lm',pad=8)
    d.text((175,kopf//2-16),f"x {f['cx0']}–{f['cx1']+1} m, y {f['cy0']}–{f['cy1']+1} m",font=F(28),fill='white',anchor='lm')
    d.text((175,kopf//2+20),'Schrägansicht von Süden, Handy-LOD, gelb = Feldgrenze',font=F(22),fill=(200,200,200),anchor='lm')
    d.text((10,B.height-22),STAND,font=F(18),fill=(180,180,180),anchor='lm')
    p=os.path.join(HIER,'felder',n+'.jpg'); B.save(p,quality=88)
    idx.append(dict(**f,meter_x=[f['cx0'],f['cx1']+1],meter_y=[f['cy0'],f['cy1']+1],bild=f'felder/{n}.jpg',commit=COMMIT,banner=BANNER,
                    kamera=dict(position=k['p'],ziel=k['t'],fov=50,query='?lod=1 (LS=2)')))
# ---- Gruppen (6er, zeilenweise A1..H1,A2..)
G=[]
for i in range(0,len(idx),6):
    g=f'G{i//6+1:02d}'; mem=idx[i:i+6]; G.append(dict(gruppe=g,felder=[m['feld'] for m in mem],bogen=f'gruppen/gruppe_{g}.jpg'))
os.makedirs(os.path.join(HIER,'gruppen'),exist_ok=True)
for g in G:
    ims=[Image.open(os.path.join(HIER,'felder',f'feld_{x}.jpg')) for x in g['felder']]
    tw=540; th=int(ims[0].height*tw/ims[0].width); kopf=80
    S=Image.new("RGB",(2*tw+10,kopf+((len(ims)+1)//2)*(th+10)),(20,20,20)); d=ImageDraw.Draw(S)
    d.text((S.width//2,kopf//2),f"{g['gruppe']}: {', '.join(g['felder'])}",font=F(40),fill='white',anchor='mm')
    for j,im in enumerate(ims):
        x=(j%2)*(tw+10); y=kopf+(j//2)*(th+10); S.paste(im.resize((tw,th),Image.LANCZOS),(x,y))
        textbox(d,(x+12,y+12),g['felder'][j],F(56),bg=(170,0,0),anchor='lt',pad=6)
    S.save(os.path.join(HIER,g['bogen']),quality=88)
json.dump(dict(stand=STAND,commit=COMMIT,banner=BANNER,raster=dict(spalten=NSP,reihen=NRE,grenzen_x=GX,grenzen_y=GY,zelle_m=1,px_pro_zelle=25),
               uebersicht='uebersicht_raster.jpg',felder=idx),open(os.path.join(HIER,'RASTER_INDEX.json'),'w'),indent=1,ensure_ascii=False)
json.dump(dict(stand=STAND,anzahl=len(G),gruppen=G),open(os.path.join(HIER,'RASTER_GRUPPEN.json'),'w'),indent=1,ensure_ascii=False)
L=[f'# RASTER_INDEX t1744u','',f'Stand: {STAND}  ','Raster: 8 Spalten (A–H) × 7 Reihen (1–7) = 56 Felder, Zellen 1 m (25 px). Zellbereiche inklusiv, Meterbereiche halboffen.','',
   'Übersicht: `uebersicht_raster.jpg`. Feldbilder: `felder/feld_XY.jpg`. Gruppenbögen: `gruppen/gruppe_Gnn.jpg`.','',
   '| Feld | cx0–cx1 | cy0–cy1 | x [m] | y [m] | Bild | Gruppe |','|---|---|---|---|---|---|---|']
gm={x:g['gruppe'] for g in G for x in g['felder']}
for m in idx: L.append(f"| {m['feld']} | {m['cx0']}–{m['cx1']} | {m['cy0']}–{m['cy1']} | {m['cx0']}–{m['cx1']+1} | {m['cy0']}–{m['cy1']+1} | {m['bild']} | {gm[m['feld']]} |")
L+=['',f'Gruppen ({len(G)}): '+'; '.join(f"{g['gruppe']} = {g['felder'][0]}–{g['felder'][-1]}" for g in G)]
open(os.path.join(HIER,'RASTER_INDEX.md'),'w').write('\n'.join(L)+'\n'); print(STAND,len(idx),len(G))
