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
ug=np.full((ny,nx),'BODEN',dtype='U10')
ug[rand]='GESPERRT'; ug[schnee]='SCHNEE'; ug[fz]='FELS_WALD'; ug[wasser]='WASSER_EIS'; ug[hof]='HOF'; ug[feuer]='FEUER'
ug[weg!='']='WEG'; ug[bruecke]='BRUECKE'
begehbar=~((ug=='GESPERRT')|(ug=='WASSER_EIS')|(ug=='FELS_WALD')|(hind>0))|(ug=='WEG')|(ug=='BRUECKE')
bebaubar=senke&fe2&~wasser&~fz&(hind==0)&(weg=='')&~bruecke&~feuer
o=f'raster_c20_z{Z}'
with open(o+'_zellen.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['cx','cy','px_x','px_y','untergrund','zone','platz','weg_id','weg_klasse','hindernis','wasser_eis','schnee','senke_bb4','h4_ext','frei_e2','begehbar','bebaubar','hoehe_stufe','klippe','skin_slot'])
    for y in range(ny):
        for x in range(nx):
            w.writerow([x,y,x*Z,y*Z,ug[y,x],zone[y,x],ids[platz[y,x]-1]['nr'] if platz[y,x] else '',weg[y,x],weg_kl[y,x],int(hind[y,x]),int(wasser[y,x]),int(schnee[y,x]),int(senke[y,x]),int(h4[y,x]),int(fe2[y,x]),int(begehbar[y,x]),int(bebaubar[y,x]),'', '', 'ug_'+ug[y,x].lower()])
st={k:int(v) for k,v in zip(*np.unique(ug,return_counts=True))}
json.dump(dict(karte='KANDIDAT_NICHT_FREIGEGEBEN_master_v18_p7_c20.png',karte_md5='d916c6ace52352d7fcf4ef13591cb5c0',karte_px=[W,H],px_pro_m=PXM,zelle_px=Z,zelle_m=Z/PXM,raster=[nx,ny],epoche='E1',epochen_variante='fest_c20',
  zaehlung_untergrund=st,begehbar=int(begehbar.sum()),bebaubar=int(bebaubar.sum()),plaetze=len(ids),
  hinweis='hoehe_stufe/klippe leer: keine Hoehenkarte vorhanden [A]'),open(o+'_meta.json','w'),ensure_ascii=False,indent=1)
COL={'BODEN':(196,170,120),'GESPERRT':(150,150,150),'SCHNEE':(235,240,245),'FELS_WALD':(90,90,90),'WASSER_EIS':(60,120,220),'HOF':(220,190,90),'FEUER':(230,60,30),'WEG':(150,100,50),'BRUECKE':(130,60,160)}
img=np.zeros((ny,nx,3),np.uint8)
for k,c in COL.items(): img[ug==k]=c
img[(platz>0)&(ug!='WEG')]=(80,190,90); img[hind>0]=(200,0,200)
s=3; im=Image.fromarray(img).resize((nx*s,ny*s),Image.NEAREST); a=np.asarray(im).copy()
bb=np.repeat(np.repeat(bebaubar,s,0),s,1); a[bb&((np.indices(bb.shape).sum(0)%6)<1)]=(0,0,0)
im=Image.fromarray(a); L=Image.new('RGB',(im.width+330,max(im.height,600)),'white'); L.paste(im,(0,0)); d=ImageDraw.Draw(L)
try: ft=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
except: ft=None
items=list(COL.items())+[('PLATZ (99 Slots)',(80,190,90)),('HINDERNIS',(200,0,200))]
y=20; d.text((im.width+15,y),f'c20, Zelle {Z}px = {Z/PXM:g} m',fill='black',font=ft); y+=30
for k,c in items: d.rectangle([im.width+15,y,im.width+40,y+20],fill=c,outline='black'); d.text((im.width+50,y),k,fill='black',font=ft); y+=30
d.text((im.width+15,y),'schwarz schraffiert = bebaubar',fill='black',font=ft)
L.save(o+'_vorschau.png'); print(json.dumps(st),begehbar.sum(),bebaubar.sum(),nx,ny)
