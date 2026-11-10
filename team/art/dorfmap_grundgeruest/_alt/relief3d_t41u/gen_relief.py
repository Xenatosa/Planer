# t41u: echtes neues 3D-Relief. Quelle Lage: raster_c20_z25_zellen.csv (+ t36u-Sidecar fuer Felder). c20 unveraendert.
# Ausgabe: relief_daten.json.gz (Viewer), zellen_relief.csv (Sidecar), dorfmap_relief_z25.glb/.obj, relief_zaehlung.json
import csv,json,gzip,base64,numpy as np,scipy.ndimage as nd
B='../';NX,NY=336,303;SPRUNG=2.5
R=list(csv.DictReader(open(B+'_alt/modell3d_t36u/zellen_eigenschaften.csv')))
cols=[c for c in R[0].keys() if not c.startswith('modell_')]
A=lambda k:np.array([r[k] for r in R]).reshape(NY,NX)
eb=A('ebene');wn=A('wand_name');ug=A('untergrund').copy();h0=A('hoehe_m').astype(float);wa=A('wasser_eis')=='1';fl=A('fluss_id');ha=A('hindernis_art')
wand=np.isin(ug,['KLIPPE_WAND','KLIPPE_KANTE'])
# --- Hoehen je Ebene (Wandhoehen aus Messung [R], Rest [A])
WANDH={'Nord':14.0,'Suedgrat':16.0,'Krater':11.0,'Ostgrat':12.0}
EBENE_H={'PLATEAU_NORD':14.0,'OSTPLATEAU':12.0,'TAL_SUED':-16.0,'GIPFEL':14.0,'KRATER':1.0}
H=h0.copy()
pos=h0>0;H[pos]=h0[pos]*1.7;neg=h0<0;H[neg]=h0[neg]*16/7.6          # Hang/Sims skaliert [A]
for e,v in EBENE_H.items():H[eb==e]=v
H[(eb=='SENKE')]=h0[eb=='SENKE']
# Wandband -> obere Ebene (Wand steht am Fuss) [F]
for w,v in {'Nord':14.0,'Krater':11.0,'Ostgrat':12.0}.items():H[wand&(wn==w)]=v
# Suedgrat + unbenannt: hoechster Nachbar ausserhalb Band, ausbreiten
rest=wand&~np.isin(wn,['Nord','Krater','Ostgrat']);K=~rest;Hk=np.where(K,H,-1e9)
for _ in range(60):
    d=nd.grey_dilation(Hk,size=3);neu=rest&~K&(d>-1e8);Hk[neu]=d[neu];K|=neu
    if not (rest&~K).any():break
H[rest]=Hk[rest]
Hboden=H.copy()
tiefe=np.where(fl=='SEE',3.0,1.5)                                      # [A]
H[wa]-=tiefe[wa];Wsp=np.where(wa,Hboden-0.3,np.nan)
# --- Ecken: Mittel der Nachbarn mit |dH|<=SPRUNG (glatte Flaechen, senkrechte Wand bei Sprung)
P=np.pad(H,1,mode='edge');C=np.zeros((NY,NX,4),np.float32)       # Ecken: 0=(x0,z0) 1=(x1,z0) 2=(x1,z1) 3=(x0,z1)
for k,(ox,oz) in enumerate([(0,0),(1,0),(1,1),(0,1)]):
    s=np.zeros((NY,NX));n=np.zeros((NY,NX))
    for dx in (ox-1,ox):
        for dz in (oz-1,oz):
            q=P[1+dz:1+dz+NY,1+dx:1+dx+NX];m=np.abs(q-H)<=SPRUNG;s+=np.where(m,q,0);n+=m
    C[...,k]=s/n
# --- Kanten mit Sprung -> Wandflaechen; Kennzahlen je Zelle
fallx=C[:,:-1,[1,2]]-C[:,1:,[0,3]]   # links minus rechts
fallz=C[:-1,:,[3,2]]-C[1:,:,[0,1]]   # oben(nord) minus unten(sued)
kh=np.zeros((NY,NX));oben=np.zeros((NY,NX),bool);fuss=np.zeros((NY,NX),bool)
def reg(d,a,b):
    m=np.abs(d).max(-1);w=m>SPRUNG;hi=d.mean(-1)>0
    np.maximum.at(kh,a,np.where(w,m,0));np.maximum.at(kh,b,np.where(w,m,0))
    oben[a]|=w&hi;fuss[a]|=w&~hi;oben[b]|=w&~hi;fuss[b]|=w&hi
yy,xx=np.mgrid[0:NY,0:NX-1];reg(fallx,(yy,xx),(yy,xx+1))
yy,xx=np.mgrid[0:NY-1,0:NX];reg(fallz,(yy,xx),(yy+1,xx))
gx=((C[...,1]+C[...,2])-(C[...,0]+C[...,3]))/2;gz=((C[...,2]+C[...,3])-(C[...,0]+C[...,1]))/2
neig=np.degrees(np.arctan(np.hypot(gx,gz)))
# --- neuer Untergrund: Bandzellen sind jetzt Oberflaeche der oberen Ebene [F]
ug2=ug.copy();ug2[wand]='SCHNEE';ug2[wand&(wn=='Krater')]='FELS';ug2[ug=='SCHATTEN']='SCHNEE'
ug2[wa]='WASSER_EIS'
b3d_alt=A('begehbar_3d')=='1'
b3d=(neig<=35)&(b3d_alt|wand)&~(wa&(fl=='SEE'))
ebene2=eb.copy();ebene2[wand]=np.where(wn[wand]=='Nord','PLATEAU_NORD',np.where(wn[wand]=='Ostgrat','OSTPLATEAU',np.where(wn[wand]=='Krater','KRATERRAND','SENKE')))
kl=np.where(oben,'WAND_OBEN',np.where(fuss,'WAND_FUSS',''))
neu={'untergrund':ug2,'untergrund_quelle':np.where(ug2!=ug,'relief_t41u',A('untergrund_quelle')),'ebene':ebene2,'klippe':kl,
 'skin_slot':np.char.add('ug_',np.char.lower(ug2.astype(str))),'hoehe_m':np.round(H,2),'hoehe_quelle':np.full((NY,NX),'R_relief_t41u'),
 'neigung_grad':np.round(neig,1),'klippe_hoehe_m':np.round(kh,1),'klippe_hoehe_quelle':np.where(kh>0,'R_messung_t40u','') ,
 'wasser_tiefe_m':np.where(wa,tiefe,0).astype(str),'begehbar_3d':b3d.astype(int)}
extra={'boden_hoehe_m':np.round(Hboden,2),'wasserspiegel_m':np.where(wa,np.round(np.nan_to_num(Wsp),2).astype(str),''),
 'ecke_nw_m':np.round(C[...,0],2),'ecke_no_m':np.round(C[...,1],2),'ecke_so_m':np.round(C[...,2],2),'ecke_sw_m':np.round(C[...,3],2),
 'ebene_c20':eb,'untergrund_c20':ug}
outcols=cols+list(extra)
F={c:(neu[c] if c in neu else extra[c] if c in extra else A(c)) for c in outcols}
with open('zellen_relief.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(outcols)
    for y in range(NY):
        for x in range(NX):w.writerow([F[c][y,x] for c in outcols])
# --- Mesh (gleicher Algorithmus wie Viewer) fuer GLB/OBJ
V=[];T=[];VW=[];TW=[]
for y in range(NY):
    for x in range(NX):
        c=C[y,x];b=len(V);V+= [(x,c[0],y),(x+1,c[1],y),(x+1,c[2],y+1),(x,c[3],y+1)];T+=[(b,b+3,b+2),(b,b+2,b+1)]
def wq(p):b=len(VW);VW.extend(p);TW.extend([(b,b+1,b+2),(b,b+2,b+3)])
for y in range(NY):
    for x in range(NX-1):
        a=C[y,x];c=C[y,x+1]
        if max(abs(a[1]-c[0]),abs(a[2]-c[3]))>0.01:wq([(x+1,a[1],y),(x+1,a[2],y+1),(x+1,c[3],y+1),(x+1,c[0],y)])
for y in range(NY-1):
    for x in range(NX):
        a=C[y,x];c=C[y+1,x]
        if max(abs(a[3]-c[0]),abs(a[2]-c[1]))>0.01:wq([(x,a[3],y+1),(x+1,a[2],y+1),(x+1,c[1],y+1),(x,c[0],y+1)])
import trimesh
sc=trimesh.Scene()
sc.add_geometry(trimesh.Trimesh(np.array(V),np.array(T),process=False),'boden')
sc.add_geometry(trimesh.Trimesh(np.array(VW),np.array(TW),process=False),'waende')
sc.export('dorfmap_relief_z25.glb')
with open('dorfmap_relief_z25.obj','w') as f:
    f.write('# t41u Relief, 1 Einheit=1 m, x=cx, y=hoch, z=cy\no boden\n');f.writelines(f'v {a} {b:.2f} {c}\n' for a,b,c in V)
    f.writelines(f'f {a+1} {b+1} {c+1}\n' for a,b,c in T);o=len(V);f.write('o waende\n')
    f.writelines(f'v {a} {b:.2f} {c}\n' for a,b,c in VW);f.writelines(f'f {a+1+o} {b+1+o} {c+1+o}\n' for a,b,c in TW)
# --- Objekte (Groessen wie t39u, nur auf neues Relief)
hc=lambda x,y:float(C[min(int(y),NY-1),min(int(x),NX-1)].mean())
OV=list(csv.DictReader(open(B+'raster_c20_z25_overlay_plaetze_wege.csv')))
weg=np.zeros((NY,NX),bool);br=np.zeros((NY,NX),bool);deko=np.zeros((NY,NX),bool)
for o in OV:
    x,y=int(o['cx']),int(o['cy']);weg[y,x]|=bool(o['weg_id']);br[y,x]|=o['bruecke']=='1';deko[y,x]|=o['dekoplaetze_netz']=='1'
rng=lambda x,y,s:((x*73856093)^(y*19349663)^(s*83492791))%10007/10007.0
Pl=json.load(open(B+'pruefung/quelle_plaetze_wachstum_ausbau_planm.json'))['E40'];belegt=np.zeros((NY,NX),bool);haeuser=[]
HH={'Hütte':3,'kompakt':4,'schmal':5,'Standard':5,'Doppelhaus':5,'Eckhaus':6,'Turmhaus':9,'FUNKTION':7,'Quartiersplatz':0.15}
for p in Pl:
    q=np.array([[(x+200)*1.2,(y+40)*1.2] for x,y in p['poly']]);x0,y0=q.min(0);x1,y1=q.max(0)
    ix=slice(max(0,int(x0)),min(NX,int(np.ceil(x1))));iy=slice(max(0,int(y0)),min(NY,int(np.ceil(y1))));belegt[iy,ix]=1
    t=p['typ'];k='FUNKTION' if t.startswith('FUNKTION') else t
    g=float(np.median(Hboden[iy,ix])) if Hboden[iy,ix].size else 0
    haeuser.append({'id':p['id'],'typ':t,'x':round((x0+x1)/2,2),'z':round((y0+y1)/2,2),'b':round(x1-x0,2),'t':round(y1-y0,2),'h':HH[k],'y':round(g,2)})
baeume=[];felsen=[];steine=[]
for y in range(NY):
    for x in range(NX):
        if belegt[y,x] or weg[y,x]:continue
        if ug2[y,x]=='WALD' and x%3==0 and y%3==0:
            X,Z=min(x+rng(x,y,1)*2.4,NX-0.5),min(y+rng(x,y,2)*2.4,NY-0.5);baeume.append([round(X,2),round(hc(X,Z),2),round(Z,2),round(6+4*rng(x,y,3),1)])
        if ug2[y,x]=='FELS' and x%3==1 and y%3==1:felsen.append([x+.5,round(hc(x,y),2),y+.5,round(.8+1.4*rng(x,y,4),2),round(rng(x,y,5)*6.28,2)])
        if deko[y,x] and not wa[y,x]:steine.append([x+.5,round(hc(x,y),2),y+.5,.6,round(rng(x,y,6)*6.28,2)])
lab,n=nd.label(ha=='MASKE');findlinge=[]
for i,s in enumerate(nd.find_objects(lab)):
    m=lab[s]==i+1;cy,cx=nd.center_of_mass(m);a=int(m.sum());X,Z=s[1].start+cx+.5,s[0].start+cy+.5
    findlinge.append([round(X,2),round(hc(X,Z),2),round(Z,2),round(.6*np.sqrt(a),2),round(rng(int(X),int(Z),7)*6.28,2)])
bruecken=[[x+.5,round(float(Hboden[y,x])+0.3,2),y+.5] for y,x in zip(*np.nonzero(br))]
wege=[[int(x),int(y)] for y,x in zip(*np.nonzero(weg))]
start=[h for h in haeuser if h['typ']=='FUNKTION:Starthaus'][0]
# Wandfuss Nordwand naechst Start: Zelle mit Nordnachbar >=10 m hoeher
fz=[(abs(x-start['x'])+abs(y-start['z']),x,y) for y in range(1,NY) for x in range(NX) if wn[y-1,x]=='Nord' and H[y-1,x]-H[y,x]>=10 and abs(H[y,x])<1 and not wa[y,x]]
obj=[(o[0],o[2]) for L in (baeume,felsen,findlinge,steine) for o in L]+[(h['x'],h['z']) for h in haeuser]
frei=lambda x,y:not any(abs(ox-x-.5)<2.5 and 0<oz-y<15 for ox,oz in obj) and not wa[y:y+15,max(0,x-1):x+2].any() and np.abs(H[y:y+15,max(0,x-1):x+2]-H[y,x]).max()<2
fz=sorted(fz);_,fx,fy=next(f for f in fz if frei(f[1],f[2]))
spalten={}
for c in outcols:
    u,idx=np.unique(F[c].astype(str).ravel(),return_inverse=True);dt=np.uint8 if len(u)<256 else np.uint16 if len(u)<65536 else np.uint32
    spalten[c]={'w':u.tolist(),'t':dt.__name__,'i':base64.b64encode(idx.astype(dt).tobytes()).decode()}
b64=lambda a:base64.b64encode(np.ascontiguousarray(a,np.float32).tobytes()).decode()
D={'nx':NX,'ny':NY,'C':b64(C),'W':b64(np.nan_to_num(Wsp,nan=-999)),'ug':spalten['untergrund'],'sprung':SPRUNG,'spalten':spalten,'reihenfolge':outcols,
 'haeuser':haeuser,'baeume':baeume,'felsen':felsen,'findlinge':findlinge,'steine':steine,'bruecken':bruecken,'wege':wege,'start':start,
 'wandfuss':{'x':fx+.5,'z':fy+.5,'h':round(float(H[fy-1,fx]-H[fy,fx]),1),'zelle':int(fy*NX+fx)},'wandhoehen':WANDH}
open('relief_daten.json.gz','wb').write(gzip.compress(json.dumps(D,ensure_ascii=False).encode(),9))
Z={k:len(D[k]) for k in ['haeuser','baeume','felsen','findlinge','steine','bruecken','wege']}
Z.update(wandflaechen_quads=len(TW)//2,wand_kanten_ueber_2_5m=int((np.abs(fallx).max(-1)>SPRUNG).sum()+(np.abs(fallz).max(-1)>SPRUNG).sum()),
 zellen_wand_oben=int(oben.sum()),zellen_wand_fuss=int(fuss.sum()),hoehe_min=float(H.min()),hoehe_max=float(H.max()),wandfuss=D['wandfuss'],
 klippe_hoehe_median_je_wand={w:float(np.median(kh[(wn==w)&oben])) if ((wn==w)&oben).any() else None for w in WANDH},
 bandzellen_umgedeutet=int(wand.sum()),begehbar_3d=int(b3d.sum()))
json.dump(Z,open('relief_zaehlung.json','w'),indent=1,ensure_ascii=False);print(json.dumps(Z,ensure_ascii=False))
