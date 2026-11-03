# O18k Pruef-Gate (t109u). Kartenweit R1-R7 aus relief_daten.json.gz; Ausgabe Trefferliste (Regel, Feld, x|z m, Wert). Exit 1 wenn Treffer.
# python3 pruefung/pruefe_regeln.py [relief_daten.json.gz] [out.json]
import json,gzip,sys,base64,numpy as np,scipy.ndimage as nd
from skimage.morphology import reconstruction
f=sys.argv[1] if len(sys.argv)>1 else 'relief_daten.json.gz';D=json.load(gzip.open(f));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(GY,GX).astype(float);WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(GY,GX);LAND=WV<=-900
feld=lambda x,z:'ABCDEFGH'[int(np.clip(x//42,0,7))]+str(int(np.clip(z//43,0,6))+1)
hf=lambda X,Z:nd.map_coordinates(G,[np.asarray(Z,float)*RS,np.asarray(X,float)*RS],order=1,mode='nearest')
gy,gx=np.gradient(G,1/RS);ST=np.hypot(gx,gy);WAND=ST>1.0   # >45 Grad
T=[];hit=lambda r,x,z,w,**k:T.append(dict(regel=r,feld=feld(x,z),x=round(float(x),1),z=round(float(z),1),wert=w,**k))
# Wegmaske 1-m-Zellen: Dorfwege, WEGA, Bruecken, Rampen
W=np.zeros((NY,NX),np.int16);RID=-np.ones((NY,NX),np.int16)
for x,z in D['wege']:W[z,x]=1
W[(np.frombuffer(base64.b64decode(D['WEGA']),np.uint8).reshape(GY,GX)[:-1:RS,:-1:RS]>20)&(W==0)]=1
for b in D['bruecken']:W[int(b[2]),int(b[0])]=3
def samp(r,step=0.25):
    r=np.asarray(r,float);L=np.r_[0,np.cumsum(np.hypot(*np.diff(r,axis=0).T))];t=np.arange(0,L[-1]+1e-6,step);return np.stack([np.interp(t,L,r[:,0]),np.interp(t,L,r[:,1])],1),t
R=[samp(r) for r in D['rampenwege']]
for i,(p,_) in enumerate(R):
    zi=np.clip(p[:,1].astype(int),0,NY-1);xi=np.clip(p[:,0].astype(int),0,NX-1);W[zi,xi]=np.maximum(W[zi,xi],2);RID[zi,xi]=i
# R1 Enden
for i,(p,t) in enumerate(R):
    for nm,k,kk in (('anfang',0,8),('ende',-1,-9)):
        x,z=p[k];d=p[k]-p[kk];d/=np.hypot(*d) or 1;nrm=np.array([-d[1],d[0]])
        q=[p[k]+d*s+nrm*o for s in (0.5,1,1.5,2,3) for o in (-1,0,1)];st=max(float(nd.map_coordinates(ST,[[a[1]*RS],[a[0]*RS]],order=1)[0]) for a in q)
        z0,z1,x0,x1=max(0,int(z)-2),min(NY,int(z)+3),max(0,int(x)-2),min(NX,int(x)+3);sub=W[z0:z1,x0:x1];rid=RID[z0:z1,x0:x1]
        an=bool(((sub>0)&(rid!=i)).any());rand=x<3 or z<3 or x>NX-3 or z>NY-3
        nass=bool((~LAND[max(0,int((z-1.5)*RS)):int((z+1.5)*RS)+1,max(0,int((x-1.5)*RS)):int((x+1.5)*RS)+1]).any())
        if st>1.0:hit('R1_wand',x,z,round(st,2),weg=f'rampe_{i}',wo=nm)
        if nass:hit('R1_wasser',x,z,1,weg=f'rampe_{i}',wo=nm)
        if not an and not rand:hit('R1_blind',x,z,0,weg=f'rampe_{i}',wo=nm)
# R2 Komponenten
lab,n=nd.label(W>0,np.ones((3,3)));gr=np.bincount(lab.ravel());gr[0]=0;hp=gr.argmax()
for k in range(1,n+1):
    if k!=hp:yy,xx=np.nonzero(lab==k);hit('R2_getrennt',xx.mean(),yy.mean(),int(len(xx)))
# R3 Laengs/Quer je Rampe, Abschnitte 4 m
for i,(p,t) in enumerate(R):
    d=np.gradient(p,axis=0);d/=np.maximum(np.linalg.norm(d,axis=1,keepdims=True),1e-9);n_=np.stack([-d[:,1],d[:,0]],1)
    hc=hf(p[:,0],p[:,1]);q=(hf(*(p+n_*1.5).T)-hf(*(p-n_*1.5).T))/3*100
    lr=hc-nd.gaussian_filter1d(hc,8,mode='nearest');cv=np.abs(np.gradient(np.gradient(nd.gaussian_filter1d(hc,2),0.25),0.25))
    mid=(hf(*(p+n_*0.75).T)+hf(*(p-n_*0.75).T))/2;wb=np.abs(hc-(hf(*(p+n_*1.5).T)+hf(*(p-n_*1.5).T))/2)
    for j in range(0,len(p),16):
        s=slice(j,j+16);x,z=p[j]
        if np.abs(q[s]).max()>3.5:hit('R3_quer_pct',x,z,round(float(np.abs(q[s]).max()),1),weg=f'rampe_{i}')
        if np.abs(lr[s]).max()>0.08:hit('R3_laengs_m',x,z,round(float(np.abs(lr[s]).max()),3),weg=f'rampe_{i}')
        if wb[s].max()>0.08:hit('R3_woelb_m',x,z,round(float(wb[s].max()),3),weg=f'rampe_{i}')
# R4 Rand: Wegzellen <4 m vom Rand, Gefaelle zum Rand; Schlucht: Weg >1.5 m unter Gelaende 4 m seitlich beidseitig
for z,x in zip(*np.nonzero(W)):
    if x<=3 or z<=3 or x>=NX-4 or z>=NY-4:
        ex=0 if x<=3 else NX if x>=NX-4 else x+.5;ez=0 if z<=3 else NY if z>=NY-4 else z+.5
        dh=float(hf([x+.5],[z+.5])[0]-hf([np.clip(ex,0,NX)],[np.clip(ez,0,NY)])[0]);dist=max(np.hypot(ex-x-.5,ez-z-.5),0.5)
        if abs(dh)/dist>0.15:hit('R4_rand',x+.5,z+.5,round(dh,2))
for i,(p,t) in enumerate(R):
    d=np.gradient(p,axis=0);d/=np.maximum(np.linalg.norm(d,axis=1,keepdims=True),1e-9);n_=np.stack([-d[:,1],d[:,0]],1);hc=hf(*p.T)
    s=np.minimum(hf(*(p+n_*4).T),hf(*(p-n_*4).T))-hc
    for j in np.nonzero(s>1.5)[0][::16]:hit('R4_schlucht',*p[j],round(float(s[j]),2),weg=f'rampe_{i}')
# R5 Loecher (abflusslose Senken auf trockenem Land >1 m), Spitzen
sd=G.copy();sd[1:-1,1:-1]=G.max();tief=reconstruction(sd,G,method='erosion')-G;tief[~nd.binary_erosion(LAND,iterations=2*RS)]=0
lab,n=nd.label(tief>1.0)
for k in range(1,n+1):
    yy,xx=np.nonzero(lab==k);j=tief[yy,xx].argmax();hit('R5_loch',xx[j]/RS,yy[j]/RS,round(float(tief[yy[j],xx[j]]),2),m2=round(len(xx)/RS/RS,1))
sp=G-nd.grey_opening(G,size=(3,3))
WD=nd.binary_dilation(WAND,iterations=2*RS)
for zz,xx in zip(*np.nonzero((sp>0.5)&~WD)):hit('R5_spitze',xx/RS,zz/RS,round(float(sp[zz,xx]),2))
# R6 Objekte auf Weg, Wasser im Schnee (Wasser auf Plateau >10 m)
for kind in ('baeume','felsen','findlinge','steine','geroell','felsbloecke'):
    for o in D.get(kind,[]):
        try:x,z=float(o[0]),float(o[2])
        except Exception:continue
        if 0<=x<NX and 0<=z<NY and W[int(z),int(x)]:hit('R6_objekt_auf_weg',x,z,kind)
wh=(~LAND)&(G>10);lab,n=nd.label(wh)
for k in range(1,n+1):yy,xx=np.nonzero(lab==k);hit('R6_wasser_schnee',xx.mean()/RS,yy.mean()/RS,int(len(xx)))
# R7 Geometrie-Trennung: Fein-Daten muessen Wand/Boden/Weg-Kennung tragen
FW=D['FW'];
if not all(k in FW for k in ('vid','h','t')):hit('R7_trennung',0,0,'FW ohne t')

# ---------- GELAENDE G1-G11 (t110u) ----------
import os
LS=os.environ.get('LOCHSCAN')   # JSON von pruefung/loch_o18g.js
if LS and os.path.exists(LS):
    l=json.load(open(LS));
    if l.get('offen_innen',0):hit('G1_loch_offen',0,0,l['offen_innen'])
else:hit('G1_lochscan_fehlt',0,0,'LOCHSCAN=... setzen')
FWd=D['FW'];FS=FWd['fs'];FXn=NX*FS+1;vid=np.frombuffer(base64.b64decode(FWd['vid']),np.uint32);fh=np.frombuffer(base64.b64decode(FWd['h']),np.float32).astype(float)
FYn=NY*FS+1;F=np.full((FYn,FXn),np.nan);F[vid//FXn,vid%FXn]=fh;ok=np.isfinite(F);Fz=np.where(ok,F,0)
def ausreisser(A,okm,thr,nm,step):
    mn=nd.grey_erosion(np.where(okm,A,1e9),size=3);mx=nd.grey_dilation(np.where(okm,A,-1e9),size=3)
    nb=(nd.uniform_filter(np.where(okm,A,0),3)*9-A)/np.maximum(nd.uniform_filter(okm*1.0,3)*9-1,1)
    nn=nd.uniform_filter(okm*1.0,3)*9-okm;okm=okm&(nn>=3)   # O18r: Punkt ohne >=3 gueltige Nachbarn nicht werten (sonst nb=0 -> Treffer = Hoehe selbst, z.B. B1 80.2|36 10.2 m bei glattem Gelaende)
    up=(A-nb)*okm;dn=(nb-A)*okm
    for r,arr in ((nm[0],up),(nm[1],dn)):
        lab,n=nd.label(arr>thr)
        for k in range(1,n+1):yy,xx=np.nonzero(lab==k);j=arr[yy,xx].argmax();hit(r,xx[j]/step,yy[j]/step,round(float(arr[yy[j],xx[j]]),2))
ausreisser(G,~nd.binary_dilation(WAND,iterations=3*RS),0.45,   # O18m geeicht: 0.35-0.42 = Hangknick am Wandrand, Bild unauffaellig
 ('G2_spitze_oben','G3_spitze_unten'),RS)
WDF=nd.zoom(nd.binary_dilation(WAND,iterations=3*RS).astype(np.uint8),FS/RS,order=0)[:Fz.shape[0],:Fz.shape[1]]>0;WDF=np.pad(WDF,((0,Fz.shape[0]-WDF.shape[0]),(0,Fz.shape[1]-WDF.shape[1])),constant_values=True)
ausreisser(Fz,ok&nd.binary_erosion(ok,iterations=2)&~WDF,0.45,('G2_spitze_oben_fein','G3_spitze_unten_fein'),FS)   # O18m geeicht wie grob
lap=nd.laplace(nd.gaussian_filter(G,1));ref=nd.uniform_filter(np.abs(lap),20*RS);bad=(np.abs(lap)>np.maximum(6*ref,0.15))&LAND&~nd.binary_dilation(WAND,iterations=2*RS)
lab,n=nd.label(bad)
for k in range(1,n+1):
    yy,xx=np.nonzero(lab==k)
    if len(xx)>=4:hit('G4_delle_beule',xx.mean()/RS,yy.mean()/RS,round(float(np.abs(lap[yy,xx]).max()),2))
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'));from relief_o18n import g5_beulen;bb,_o=g5_beulen(G,RS,WAND,0.6);lab,n=nd.label(bb>0)   # O18n: neue Methode, Kantenpunkt hoeher als Plateau 2-5 m landeinwaerts (runde Kante zaehlt nicht), Schwelle 0.6 m   # O18m geeicht: 0.6-1.0 = Faltlinie Klippenkante, Bild unauffaellig
for k in range(1,n+1):yy,xx=np.nonzero(lab==k);hit('G5_beule_klippe',xx.mean()/RS,yy.mean()/RS,round(float(bb[yy,xx].max()),2))
# O18t Messkorrektur: G6/G11 auf der SICHTBAREN Flaeche (Feinband wo vorhanden, sonst Grobnetz); GATE_GROB=1 = alte Messung. Schwellen unveraendert [A]
GROB=bool(os.environ.get('GATE_GROB'));Fv=F[::FS//RS,::FS//RS][:GY,:GX];GV=G if GROB else np.where(np.isfinite(Fv),Fv,G)
def hv(x,z):
    if GROB:return float(hf([x],[z])[0])
    fx,fy=x*FS,z*FS;i,j=int(fx),int(fy)
    if 0<=i<FXn-1 and 0<=j<FYn-1 and ok[j:j+2,i:i+2].all():
        u,v=fx-i,fy-j;q=F[j:j+2,i:i+2];return float(q[0,0]*(1-u)*(1-v)+q[0,1]*u*(1-v)+q[1,0]*(1-u)*v+q[1,1]*u*v)
    return float(hf([x],[z])[0])
vgy,vgx=np.gradient(GV,1/RS);VST=np.hypot(vgx,vgy)
nrm=np.stack([-vgx,-vgy,np.ones_like(GV)]);nrm/=np.linalg.norm(nrm,axis=0);dn=sum(np.abs(np.diff(nrm[i],axis=1))[:-1] for i in range(3))
fac=(dn>0.25)&(VST[:-1,:-1]>0.15)&(VST[:-1,:-1]<0.8)&LAND[:-1,:-1];lab,n=nd.label(fac)
for k in range(1,n+1):
    yy,xx=np.nonzero(lab==k)
    if len(xx)>=6:hit('G6_facette',xx.mean()/RS,yy.mean()/RS,int(len(xx)))
M=WAND&LAND;rau=float(np.abs(G-nd.gaussian_filter(G,RS))[M].mean());glatt=nd.uniform_filter((np.abs(G-nd.gaussian_filter(G,RS))<0.05)*1.0,6*RS)>0.9
if rau<0.40:hit('G7_wand_glatt_gesamt',0,0,round(rau,3),ref='O17 0.589/O18j 0.463, Schwelle 0.40')
lab,n=nd.label(glatt&M)
for k in range(1,n+1):
    yy,xx=np.nonzero(lab==k)
    if len(xx)>40:hit('G7_wand_glatte_flaeche',xx.mean()/RS,yy.mean()/RS,int(len(xx)))
WAS=~LAND;lab,n=nd.label(WAS)
for k in range(1,n+1):
    yy,xx=np.nonzero(lab==k)
    if len(xx)>200*RS*RS and not (xx.min()==0 or yy.min()==0 or xx.max()==GX-1 or yy.max()==GY-1):hit('G8_fluss_nicht_bis_rand',xx.mean()/RS,yy.mean()/RS,int(len(xx)))
    tiefe=float(np.median(nd.grey_dilation(G,size=4*RS)[yy,xx]-G[yy,xx]))
    if len(xx)>200*RS*RS and tiefe<0.6:hit('G8_fluss_flach',xx.mean()/RS,yy.mean()/RS,round(tiefe,2))
# G9 = R6_wasser_schnee, G10 = R5_loch (gleiche Messung)
for kind in ('baeume','felsen','findlinge','steine','felsbloecke'):
    for o in D.get(kind,[]):
        try:x,y,z=float(o[0]),float(o[1]),float(o[2])
        except Exception:continue
        if not(0<=x<NX and 0<=z<NY):continue
        h0=hv(x,z);
        if abs(y-h0)>0.6:hit('G11_objekt_schwebt_sinkt',x,z,round(y-h0,2),art=kind)
        if kind=='baeume' and float(nd.map_coordinates(ST,[[z*RS],[x*RS]],order=1)[0])>0.9:hit('G11_baum_an_wand',x,z,kind)
# ---------- TEXTUR T1-T6 (Anzeige-Farbe VC, Daten) ----------
VC=np.frombuffer(base64.b64decode(D['VC']),np.uint8).astype(float)
if VC.size==GX*GY*3:
    C=VC.reshape(GY,GX,3);dc=np.linalg.norm(np.diff(C,axis=1)[:-1],axis=2)+np.linalg.norm(np.diff(C,axis=0)[:,:-1],axis=2)
    hart=(dc>70)&LAND[:-1,:-1]&~nd.binary_dilation(WAND,iterations=RS)[:-1,:-1];lab,n=nd.label(hart)
    for k in range(1,n+1):
        yy,xx=np.nonzero(lab==k)
        if len(xx)>=8:
            gerade=max(np.ptp(xx),np.ptp(yy))>=len(xx)*0.8;hit('T1_harte_farbkante'+('_gerade' if gerade else ''),xx.mean()/RS,yy.mean()/RS,int(len(xx)))
    hell=C.mean(2)>215;sn=(~LAND)&hell
    lab,n=nd.label(sn)
    for k in range(1,n+1):yy,xx=np.nonzero(lab==k);hit('T6_wasser_in_schnee_farbe',xx.mean()/RS,yy.mean()/RS,int(len(xx))) if len(xx)>4 else 0
else:hit('T_VC_format',0,0,int(VC.size))
for r in ('T2_textur_abgeschnitten','T3_streifen_ringe','T4_graue_flussstreifen','T5_textur_vs_clay'):
    if not os.environ.get('BILD_'+r.split('_')[0]):hit(r+'_bildpruefung_offen',0,0,'Bildvergleich Clay/Textur noetig: BILD_'+r.split('_')[0]+'=ok nach Sichtpruefung')
S={}
for t_ in T:S[t_['regel']]=S.get(t_['regel'],0)+1
print(json.dumps({'summe':len(T),'je_regel':S},ensure_ascii=False))
[print(t_) for t_ in T[:600]] if os.environ.get('LISTE') else None
# ---------- G7b Wandkontur-Staerke gegen O17 (f65298b), O18o [F G1 geschmolzener Vorhang] ----------
REF=os.environ.get('O17REF','/tmp/o18m/o17.json.gz')
if not os.path.exists(REF):
    import subprocess;open(REF,'wb').write(subprocess.check_output(['git','show','f65298b:team/art/dorfmap_grundgeruest/relief3d/relief_daten.json.gz']))
D7=json.load(gzip.open(REF));G7=np.frombuffer(base64.b64decode(D7['GB']),np.float32).reshape(G.shape).astype(float)
g7y,g7x=np.gradient(G7,1/RS);M7=(np.hypot(g7x,g7y)>1.0)&LAND
def kontur(A,M):
    rau=float(np.abs(A-nd.gaussian_filter(A,RS))[M].mean());kan=float(np.percentile(np.abs(nd.laplace(A))[M],90));return rau,kan
r0,k0=kontur(G7,M7);r1,k1=kontur(G,M7);T7={}
for nm,a,b in (('rauheit',r1,r0),('kantenschaerfe',k1,k0)):
    T7[nm]=[round(a,3),round(b,3)]
    if a<0.85*b:T.append({'regel':'G7b_wandkontur_'+nm,'feld':'-','x':0,'z':0,'wert':round(a/b,3)});S['G7b_wandkontur_'+nm]=S.get('G7b_wandkontur_'+nm,0)+1
# Feld je Wandkontur
for fx in range(8):
    for fz in range(7):
        sl=(slice(fz*43*RS,(fz+1)*43*RS),slice(fx*42*RS,(fx+1)*42*RS));m=M7[sl]
        if m.sum()<200:continue
        a=float(np.abs(G[sl]-nd.gaussian_filter(G,RS)[sl])[m].mean());b=float(np.abs(G7[sl]-nd.gaussian_filter(G7,RS)[sl])[m].mean())
        if a<0.85*b:T.append({'regel':'G7b_wandkontur_feld','feld':'ABCDEFGH'[fx]+str(fz+1),'x':fx*42+21,'z':fz*43+21,'wert':round(a/b,3)});S['G7b_wandkontur_feld']=S.get('G7b_wandkontur_feld',0)+1
print('G7b',T7,json.dumps({'summe':len(T),'je_regel':S},ensure_ascii=False))
if len(sys.argv)>2:json.dump({'summe':len(T),'je_regel':S,'treffer':T},open(sys.argv[2],'w'),indent=0,ensure_ascii=False)
sys.exit(1 if T else 0)
