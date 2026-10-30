# t39u: Prototyp-Welt. Daten fuer den Viewer aus Raster + modell3d (gen_modell3d.py vorher laufen lassen: /tmp/m3_*.npy).
# Alles aus Daten gesetzt; Groessen [A] stehen in GROESSEN. Ausgabe: welt_daten.json.gz (base64 in index.html)
import csv,json,gzip,base64,numpy as np,scipy.ndimage as nd,sys
B='../../';NX,NY=336,303
R=list(csv.DictReader(open(B+'modell3d/zellen_eigenschaften.csv')))
cols=list(R[0].keys());A=lambda k:np.array([r[k] for r in R]).reshape(NY,NX)
E=np.load('/tmp/m3_E.npy').astype(np.float32);Eo=np.load('/tmp/m3_Eo.npy').astype(np.float32)
ug=A('untergrund');wa=A('wasser_eis')=='1';ha=A('hindernis_art')
OV=list(csv.DictReader(open(B+'raster_c20_z25_overlay_plaetze_wege.csv')))
weg=np.zeros((NY,NX),bool);br=np.zeros((NY,NX),bool);deko=np.zeros((NY,NX),bool)
for o in OV:
    x,y=int(o['cx']),int(o['cy'])
    if o['weg_id']:weg[y,x]=1
    if o['bruecke']=='1':br[y,x]=1
    if o['dekoplaetze_netz']=='1':deko[y,x]=1
GROESSEN={'baum_hoehe_m':[6,10],'baum_raster_m':3,'fels_raster_m':3,'fels_hoehe_m':[0.8,2.2],'findling_hoehe_m':'0,6*sqrt(Flaeche) [A]',
 'deko_stein_m':0.6,'mensch_m':1.8,'haus_hoehe_m':{'Hütte':3,'kompakt':4,'schmal':5,'Standard':5,'Doppelhaus':5,'Eckhaus':6,'Turmhaus':9,'FUNKTION':7,'Quartiersplatz':0.15}}
rng=lambda x,y,s:((x*73856093)^(y*19349663)^(s*83492791))%10007/10007.0
hc=lambda x,y:float((E[y,x]+E[y+1,x]+E[y,x+1]+E[y+1,x+1])/4)
# Plaetze E40 (Quelle pruefung/quelle_plaetze_wachstum_ausbau_planm.json, Umrechnung wie pruef_plaetze_quellen.py)
P=json.load(open(B+'pruefung/quelle_plaetze_wachstum_ausbau_planm.json'))['E40'];belegt=np.zeros((NY,NX),bool);haeuser=[]
for p in P:
    q=np.array([[(x+200)*1.2,(y+40)*1.2] for x,y in p['poly']]);x0,y0=q.min(0);x1,y1=q.max(0)
    ix=slice(max(0,int(x0)),min(NX,int(np.ceil(x1))));iy=slice(max(0,int(y0)),min(NY,int(np.ceil(y1))));belegt[iy,ix]=1
    t=p['typ'];k='FUNKTION' if t.startswith('FUNKTION') else t
    g=float(np.median([hc(x,y) for y in range(iy.start,iy.stop) for x in range(ix.start,ix.stop)])) if (iy.stop>iy.start and ix.stop>ix.start) else 0
    haeuser.append({'id':p['id'],'typ':t,'x':round((x0+x1)/2,2),'z':round((y0+y1)/2,2),'b':round(x1-x0,2),'t':round(y1-y0,2),'h':GROESSEN['haus_hoehe_m'][k],'y':round(g,2)})
baeume=[];felsen=[];steine=[]
for y in range(NY):
    for x in range(NX):
        if belegt[y,x] or weg[y,x]:continue
        if ug[y,x]=='WALD' and x%3==0 and y%3==0:
            jx,jz=rng(x,y,1)*2.4,rng(x,y,2)*2.4;X,Z=min(x+jx,NX-0.5),min(y+jz,NY-0.5)
            baeume.append([round(X,2),round(hc(min(int(X),NX-1),min(int(Z),NY-1)),2),round(Z,2),round(6+4*rng(x,y,3),1)])
        if ug[y,x]=='FELS' and x%3==1 and y%3==1:
            felsen.append([x+0.5,round(hc(x,y),2),y+0.5,round(0.8+1.4*rng(x,y,4),2),round(rng(x,y,5)*6.28,2)])
        if deko[y,x] and not wa[y,x]:
            steine.append([x+0.5,round(hc(x,y),2),y+0.5,0.6,round(rng(x,y,6)*6.28,2)])
lab,n=nd.label(ha=='MASKE');findlinge=[]
for i,s in enumerate(nd.find_objects(lab)):
    m=lab[s]==i+1;cy,cx=nd.center_of_mass(m);a=int(m.sum());X,Z=s[1].start+cx+0.5,s[0].start+cy+0.5
    findlinge.append([round(X,2),round(hc(int(X),int(Z)),2),round(Z,2),round(0.6*np.sqrt(a),2),round(rng(int(X),int(Z),7)*6.28,2)])
bruecken=[[x+0.5,round(float(max(Eo[y:y+2,x:x+2].max(),E[y:y+2,x:x+2].max()))+0.3,2),y+0.5] for y,x in zip(*np.nonzero(br))]
wege=[[int(x),int(y)] for y,x in zip(*np.nonzero(weg))]
# Zelleigenschaften kompakt: je Spalte Werteliste + Index
spalten={}
for c in cols:
    u,idx=np.unique(A(c).ravel(),return_inverse=True)
    dt=np.uint8 if len(u)<256 else np.uint16 if len(u)<65536 else np.uint32
    spalten[c]={'w':u.tolist(),'t':dt.__name__,'i':base64.b64encode(idx.astype(dt).tobytes()).decode()}
D={'nx':NX,'ny':NY,'E':base64.b64encode(E.tobytes()).decode(),'Eo':base64.b64encode(Eo.tobytes()).decode(),
 'wasser':base64.b64encode(wa.astype(np.uint8).tobytes()).decode(),'spalten':spalten,'reihenfolge':cols,
 'haeuser':haeuser,'baeume':baeume,'felsen':felsen,'findlinge':findlinge,'steine':steine,'bruecken':bruecken,'wege':wege,'groessen':GROESSEN,
 'start':[h for h in haeuser if h['typ']=='FUNKTION:Starthaus'][0]}
open('welt_daten.json.gz','wb').write(gzip.compress(json.dumps(D,ensure_ascii=False).encode(),9))
ST={k:len(D[k]) for k in ['haeuser','baeume','felsen','findlinge','steine','bruecken','wege']};json.dump(ST,open('welt_zaehlung.json','w'));print(ST)
