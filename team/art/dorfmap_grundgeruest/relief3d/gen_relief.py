# t41u: echtes neues 3D-Relief. Quelle Lage: raster_c20_z25_zellen.csv (+ t36u-Sidecar fuer Felder). c20 unveraendert.
# Ausgabe: relief_daten.json.gz (Viewer), zellen_relief.csv (Sidecar), dorfmap_relief_z25.glb/.obj, relief_zaehlung.json
import os
import csv,json,gzip,base64,numpy as np,scipy.ndimage as nd
_WELLEN_DIAG={}
def _wellen_snap(n,a):
    if os.environ.get('WELLEN_DIAG'):_WELLEN_DIAG[n]=np.asarray(a,dtype=np.float32).copy()
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
sg=wand&(wn=='Suedgrat');topf=nd.maximum_filter(np.where(sg&(H>-15),H,-1e9),size=31);dsg=nd.distance_transform_edt(~sg)
ziel=((eb=='TAL_SUED')&(dsg<=15)|(sg&(H<=-15.9)))&(topf>-1e8)
H[ziel]=np.minimum(H[ziel],-16-0.15*(1-dsg[ziel]/15))   # t46u: Fuss nie unter Talboden -16,8 (vorher Graeben bis -25,8 m wo Gratoberkante tief lag) [A]
# --- t47u: Flusslücken schliessen (c20: Wasser endet an Wandbaendern / 2-9 Zellen Luecken) [A]
def _flussluecken():
    lab,n=nd.label(wa,np.ones((3,3)));big=[i for i in range(1,n+1) if (lab==i).sum()>=30];log=[]
    for k,i in enumerate(big):
        di,ind=nd.distance_transform_edt(lab!=i,return_indices=True)
        for j in big[k+1:]:
            m=lab==j;dmin=di[m].min()
            if dmin<1.5 or dmin>12:continue
            yb,xb=[v[m][np.argmin(di[m])] for v in np.nonzero(np.ones_like(m))] if False else np.argwhere(m)[np.argmin(di[m])]
            ya,xa=ind[0][yb,xb],ind[1][yb,xb];ha_,hb_=H[ya,xa],H[yb,xb];L=int(max(abs(yb-ya),abs(xb-xa)))+1
            for t in np.linspace(0,1,L*2):
                y=int(round(ya+t*(yb-ya)));x=int(round(xa+t*(xb-xa)))
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        yy,xx=y+dy,x+dx
                        if 0<=yy<NY and 0<=xx<NX and not wa[yy,xx]:
                            wa[yy,xx]=True;fl[yy,xx]=fl[ya,xa];H[yy,xx]=ha_+t*(hb_-ha_);wand[yy,xx]=False;ug[yy,xx]='WASSER_EIS'
            log.append(((int(xa),int(ya)),(int(xb),int(yb)),round(float(dmin),1),round(float(ha_),1),round(float(hb_),1)))
    return log
FLUSSLUECKEN=_flussluecken();print('flussluecken',FLUSSLUECKEN)
# t47u: Stufen im Wasserspiegel >1 m/Zelle zu Stromschnellen verteilen [A]
for _ in range(3):
    Hw=np.where(wa,H,np.nan);st=np.zeros_like(wa)
    st[1:]|=np.abs(np.diff(Hw,axis=0))>0.9;st[:-1]|=np.abs(np.diff(Hw,axis=0))>0.9;st[:,1:]|=np.abs(np.diff(Hw,axis=1))>0.9;st[:,:-1]|=np.abs(np.diff(Hw,axis=1))>0.9
    zone=nd.binary_dilation(st,iterations=8)&wa
    if not zone.any():break
    sm=nd.gaussian_filter(np.where(wa,H,0),3)/np.maximum(nd.gaussian_filter(wa.astype(float),3),1e-6);H[zone]=sm[zone]
# t53u R2: Kraterring als Bergkranz: Gipfel/Kerben 3-10 Zellen hinter der Kraterkante (Wandsprung selbst bleibt) [A]
_kd_=nd.distance_transform_edt(~(wand&(wn=='Krater')))
_kr=(~wand)&(_kd_>=2)&(_kd_<=11)&(H>=9)&~wa&(eb!='KRATER')
_gn=nd.gaussian_filter(np.random.default_rng(57).standard_normal((NY,NX)),2.2);_gn/=_gn.std();_gr=1-np.abs(np.clip(_gn/1.6,-1,1))
_fall=np.clip((_kd_-2)/2,0,1)*np.clip((11-_kd_)/5,0,1)
H[_kr]+=(1.1*_gr**2-0.3)[_kr]*_fall[_kr]   # t54u-B: flacher, Kratersprung ~11 m
# t54u-B: Kraterfuss: Senke direkt unter der Kraterwand auf ~0 m anheben, nach innen weich auslaufen -> Sprung Fuss-Krone ~11 m [A]
_kf=(~wand)&(_kd_<=24)&(H<1.0)&np.isin(eb,['HANG','SENKE','KRATER'])
_kw=np.clip((_kd_-11)/13,0,1);_kw=_kw*_kw*(3-2*_kw)
H[_kf]=(np.minimum(H,0.0)*_kw+np.minimum(H,1.0)*0)[_kf]+np.where(H>0,H,0)[_kf]
# t63u Runde K [F] (Fabian t62u/Runde K): Strang 13 (Westarm) im Tal neu, Spiegel monoton fallend, alter Arm -> Land (fluss_k.py)
from fluss_k import fluss_k
_bel=np.zeros((NY,NX),bool)
for _p in json.load(open(B+'pruefung/quelle_plaetze_wachstum_ausbau_planm.json'))['E40']:
    _q=np.array([[(x+200)*1.2,(y+40)*1.2] for x,y in _p['poly']]);_x0,_y0=_q.min(0);_x1,_y1=_q.max(0);_bel[max(0,int(_y0)):int(np.ceil(_y1)),max(0,int(_x0)):int(np.ceil(_x1))]=True
H_VOR_K=H.copy();WA_VOR_K=wa.copy();FL_VOR_K=fl.copy();UG_VOR_K=ug.copy()
H,wa,fl,ug,_VY,_VX,FLUSS_K_NEU,FLUSS_K_ALT,FLUSS_K_KURVE,FLUSS_K_W,FLUSS_K=fluss_k(H,wa,fl,ug,wand,_kd_,_bel);print('fluss_k',FLUSS_K)
WN_VOR_K=wn.copy();eb=eb[_VY,_VX];wn=wn[_VY,_VX];ha=ha[_VY,_VX];_A0=A;A=lambda k:_A0(k) if k in('zell_id','cx','cy','px_x','px_y','flaeche_m2') else _A0(k)[_VY,_VX]   # Lage-Spalten bleiben, Inhalte folgen der Vorlage-Zelle
# t47u/t48u: natuerliche Abstiegsrampen schraeg an den Waenden (Gelaende, nicht Overlay); Zellwerte folgen aus G [A]
RAMPWEGE=[];RAMPPROF=[]
def _rampen():
    Pl0=json.load(open(B+'pruefung/quelle_plaetze_wachstum_ausbau_planm.json'))['E40'];hm=np.zeros((NY,NX),bool)
    for p in Pl0:
        q=np.array([[(x+200)*1.2,(y+40)*1.2] for x,y in p['poly']]);x0,y0=q.min(0);x1,y1=q.max(0);hm[max(0,int(y0)):int(np.ceil(y1)),max(0,int(x0)):int(np.ceil(x1))]=1
    hm=nd.binary_dilation(hm,iterations=3)|nd.binary_dilation(wa|WA_VOR_K,iterations=2)   # t63u: alter Arm bleibt Sperre -> Rampen wie Runde J (keine Nebenwirkung der Flussverlegung)
    Hsm=nd.gaussian_filter(H,4);gy,gx=np.gradient(Hsm);top=wand&(nd.minimum_filter(H,9)<H-6);log=[]
    yy,xx=np.mgrid[0:NY,0:NX]
    for w,anz in (('Nord',3),('Suedgrat',3),('Krater',4),('Ostgrat',2)):
        cand=np.argwhere(top&(wn==w));r=np.random.default_rng(len(w));r.shuffle(cand);gew=[]
        for y,x in cand[:400]:
            if min(np.hypot(x-155,y-12),np.hypot(x-125,y-126))<32:continue   # t53u: dort Serpentine X084/X069
            dn=-np.array([gx[y,x],gy[y,x]]);l=np.hypot(*dn)
            if l<1e-3:continue
            dn/=l
            for sg in (1,-1):
                tg=np.array([-dn[1],dn[0]])*sg;d=dn*0.45+tg*0.89;d/=np.hypot(*d)
                Ht=H[y,x];L=None
                for s_ in range(6,90):
                    X,Y=int(round(x+d[0]*s_)),int(round(y+d[1]*s_))
                    if not(2<=X<NX-2 and 2<=Y<NY-2) or hm[Y,X]:break
                    if s_>8 and Ht-H[Y,X]>=5 and s_*0.30>=Ht-H[Y,X]:L=s_;break        # Rampe (~17 Grad, t53u) trifft Gelaende
                if L and L>=12 and all(np.hypot(x-a,y-b)>25 for a,b,_ ,_ in gew):gew.append((x,y,d,L))
                if len(gew)>=anz:break
            if len(gew)>=anz:break
        for x,y,d,L in gew:
            Ht=H[y,x];He=H[int(round(y+d[1]*L)),int(round(x+d[0]*L))]
            RAMPWEGE.append([[round(float(x+0.5+d[0]*s_),2),round(float(y+0.5+d[1]*s_),2)] for s_ in np.arange(-1,L+1.01,1.0)])   # Overlay-Pfad (getrennt) [A]
            RAMPPROF.append((np.array([[x+0.5+d[0]*s_,y+0.5+d[1]*s_] for s_ in np.linspace(0,L,L*4+1)]),np.linspace(Ht,He,L*4+1)))
            for k in range(L*3+1):
                s_=k/3;cx,cy=x+d[0]*s_,y+d[1]*s_;hp=Ht+(He-Ht)*s_/L
                ys,xs=slice(max(0,int(cy)-5),int(cy)+6),slice(max(0,int(cx)-5),int(cx)+6)
                rr=np.hypot(xx[ys,xs]+0.5-cx,yy[ys,xs]+0.5-cy);sub=H[ys,xs]
                kern=rr<=1.8;sub[kern]=hp;wand[ys,xs][kern]=False
                rand=(rr>1.8)&(rr<5);fill=hp-(rr-1.8)*1.1;sub[rand]=np.where(sub[rand]<fill[rand],fill[rand],sub[rand])
            log.append((w,int(x),int(y),int(L),round(float(Ht),1),round(float(He),1)))
    return log
RAMPEN=_rampen();print('rampen',RAMPEN)
# t53u R3: Serpentinen (Gelaende, <=17 Grad, Spitzkehren) wo der Overlay-Plan Treppe/Abstieg ueber die Wand braucht: X084 (Wand Nord), X069 (Krater) [A]
SERPENTINEN=[]
def _serp(name,A_,B_,n=4,sg=1):
    A_=np.array(A_,float)+0.5;B_=np.array(B_,float)+0.5;Ht=float(H[int(A_[1]),int(A_[0])]);He=float(H[int(B_[1]),int(B_[0])])
    ax=B_-A_;d=np.hypot(*ax);pe=sg*np.array([-ax[1],ax[0]])/d;soll=abs(Ht-He)/np.tan(np.radians(16.5));s_=np.linspace(0,1,1200)
    for W in np.arange(0,14,0.1):
        P=A_[None]+s_[:,None]*ax[None]+pe[None]*(W*(2/np.pi)*np.arcsin(np.sin(np.pi*n*s_)))[:,None]
        L=np.r_[0,np.cumsum(np.hypot(*np.diff(P,axis=0).T))]
        if L[-1]>=soll:break
    hp=Ht+(He-Ht)*L/L[-1];yy,xx=np.mgrid[0:NY,0:NX]
    for (cx,cy),h in zip(P[::3],hp[::3]):
        ys,xs=slice(max(0,int(cy)-5),int(cy)+6),slice(max(0,int(cx)-5),int(cx)+6)
        rr=np.hypot(xx[ys,xs]+0.5-cx,yy[ys,xs]+0.5-cy);sub=H[ys,xs];kern=(rr<=1.8)&~wa[ys,xs];sub[kern]=h;wand[ys,xs][kern]=False
    RAMPPROF.append((P,hp));RAMPWEGE.append([[round(float(a),2),round(float(b),2)] for a,b in P[::20]]+[[round(float(P[-1,0]),2),round(float(P[-1,1]),2)]])
    SERPENTINEN.append((name,round(Ht,1),round(He,1),round(float(L[-1]),1),round(float(np.degrees(np.arctan(abs(Ht-He)/L[-1]))),1),round(float(W),1)))
_serp('X084',(148,2),(156,37),n=3,sg=1);_serp('X069',(127,133),(122,119),n=3)
print('serpentinen',SERPENTINEN)
Hboden=H.copy()
# t53u R4: Flussbett eingeschnitten: Tiefe nach Abstand zum Ufer, Kiesbaenke, Uferboeschung + Sandufer [A]
_dw=nd.distance_transform_edt(wa);_kb=nd.gaussian_filter(np.random.default_rng(54).standard_normal((NY,NX)),2.5);_kb/=_kb.std()
tiefe=np.where(fl=='SEE',3.0,np.clip(0.45+0.6*_dw,0.45,2.4));kies=wa&(fl!='SEE')&(_kb>0.9)&(_dw>=1.5)
tiefe=np.where(kies,np.minimum(tiefe,0.5),tiefe)
Wsp=np.where(wa,Hboden-0.3,np.nan)
_do,_ix=nd.distance_transform_edt(~wa,return_indices=True);_wl=(Hboden-0.3)[_ix[0],_ix[1]]
_hm4=np.zeros((NY,NX),bool)
for p in json.load(open(B+'pruefung/quelle_plaetze_wachstum_ausbau_planm.json'))['E40']:
    q=np.array([[(x+200)*1.2,(y+40)*1.2] for x,y in p['poly']]);x0,y0=q.min(0);x1,y1=q.max(0);_hm4[max(0,int(y0)):int(np.ceil(y1)),max(0,int(x0)):int(np.ceil(x1))]=1
_ub=(~wa)&(_do<=5)&~wand&~nd.binary_dilation(_hm4,iterations=2)&(H>_wl)&(H-_wl<4)
_sand=0.15+np.where(_kb>0,0.12,0.42)*(_do-0.5)                         # flaches Sandufer (~7 Grad) oder Boeschung (~23 Grad)
H[_ub]=np.minimum(H[_ub],(_wl+_sand)[_ub]);Hboden[_ub]=H[_ub]
H[wa]-=tiefe[wa]
# --- t42u: glattes Hoehenfeld G auf 0,5-m-Gitter (keine 1-m-Treppen). Waende = steile, leicht unregelmaessige Flaechen [A]
RS=2;GX,GY=NX*RS+1,NY*RS+1;WANDWINKEL=55.0
Hn=np.kron(H,np.ones((RS,RS)))                                     # Proben in Zellmitte-Unterteilung
J=np.zeros((NY,NX),bool);J[:,1:]|=np.abs(np.diff(H,axis=1))>SPRUNG;J[:,:-1]|=np.abs(np.diff(H,axis=1))>SPRUNG
J[1:,:]|=np.abs(np.diff(H,axis=0))>SPRUNG;J[:-1,:]|=np.abs(np.diff(H,axis=0))>SPRUNG
wz=nd.gaussian_filter(np.kron(nd.binary_dilation(J,iterations=3),np.ones((RS,RS))).astype(float),2)
rs=np.random.default_rng(42);noi=nd.gaussian_filter(rs.standard_normal(Hn.shape),3);noi/=noi.std()
Hs=nd.gaussian_filter(Hn,4.5)                                        # sigma 1,5 m [A]
lo=nd.minimum_filter(Hn,21);hi=nd.maximum_filter(Hn,21);Rg=hi-lo
# t47u: mehrskalige Felsform – Rippen/Runsen (grob+mittel+fein), Baender/Simse, Schuttfuss [A]
def _fbm(sig,seed):
    r=np.random.default_rng(seed);n=nd.gaussian_filter(r.standard_normal(Hn.shape),sig);return n/n.std()
nf=0.55*_fbm(10,7)+0.30*_fbm(4,8)+0.15*noi
# t53u R1: domain-warped ridged fBm -> Felsrippen/Runsen (verschieben die Wandlinie), variable Steilheit, Simse [A]
_jj0,_ii0=np.mgrid[0:Hn.shape[0],0:Hn.shape[1]].astype(float)
_wy=_jj0+7*_fbm(14,31);_wx=_ii0+7*_fbm(14,32)
_rw=sum(a*(1-np.abs(np.clip(nd.map_coordinates(_fbm(sg,sd),[_wy,_wx],order=1,mode='reflect')/2.2,-1,1))) for a,sg,sd in ((0.55,7,33),(0.30,3.5,34),(0.15,1.8,35)))
RIB=(_rw-_rw.mean())/_rw.std()                                       # >0 Rippe, <0 Runse
_WV=int(os.environ.get('WANDV','2'))   # O18u S3/S4 Varianten [A]
if _WV:
    _u0=(Hs-lo)/np.maximum(Rg,1e-6)-0.5+0.10*nf;_t0=np.clip(_u0*2+0.5,0,1)
    _dm=np.minimum(_t0,1-_t0)*Rg;_WM=np.clip((_dm-float(os.environ.get('FADE0','3.0')))/2.0,0,1)   # Rippen nur >3 m von Fuss/Kopf, 2 m Fade
else:_WM=1.0
_RG=float(os.environ.get('RIBG','1.5')) if _WV else 1.0   # O18v: Rippenverstaerkung Wandmitte (G7b-Rauheit) [A]
u=(Hs-lo)/np.maximum(Rg,1e-6)-0.5+0.10*nf+0.13*RIB*_WM*_RG
krz=nd.gaussian_filter(np.kron(nd.binary_dilation(wand&(wn=='Krater'),iterations=4),np.ones((RS,RS))).astype(float),4)
steil_k=(1.0+1.6*np.clip(0.5+0.4*_fbm(18,36),0,1))*(1-krz)+1.6*krz                                            # t47u: Kraterrand als geboeschter Wall statt Senkrechtring [A]
t=np.clip(u*steil_k+0.5+0.25*krz*_fbm(6,11),0,1);t=t*t*(3-2*t)
# t48u R5: Kraterring mit radialen Felsrippen + 4 Scharten; uebrige Waende mit Grat-Rauschen (ridged). Ober-/Unterkante fix (sin(pi t)) [A]
_kc=np.argwhere(wand&(WN_VOR_K=='Krater')).mean(0)*RS;_jj,_ii=np.mgrid[0:Hn.shape[0],0:Hn.shape[1]];_ang=np.arctan2(_jj-_kc[0],_ii-_kc[1])
_rib=np.sin(_ang*13+1.6*_fbm(14,21));_rib=np.sign(_rib)*np.abs(_rib)**0.6
_sch=np.clip((np.abs(np.sin(_ang*2+0.7))-0.93)/0.07,0,1)
_rid=1-2*np.abs(np.clip(_fbm(5,22)/2.5,-1,1))
t=np.clip(t+np.sin(np.pi*t)*(krz*(0.20*_rib-0.45*_sch)+(1-krz)*0.10*(_rid-0.5)*_WM*_RG),0,1)
_ns=4+np.round(2*np.clip(0.5+0.4*_fbm(20,37),0,1));_tq=np.floor(t*_ns)/_ns;_fr=t*_ns-np.floor(t*_ns)
_led=(_fbm(9,38)>0.0)*(1-krz)*_WM
t=np.clip(t*(1-0.55*_led)+0.55*_led*(_tq+np.clip((_fr-0.55)/0.45,0,1)/_ns),0,1)   # Simse: flache Absaetze + steile Stufen
band=0.04*np.sin(t*np.pi*5+1.3*_fbm(8,9))*np.sin(np.pi*t)*_WM           # Simse/Baender in der Wand
tw=np.clip(u*1.5+0.62,0,1);apron=np.clip(tw,0,0.3)                    # Schuttkegel am Fuss
Gs=lo+Rg*np.clip(0.8*t+band+0.2*apron/0.3,0,1);Gs=np.where(Rg>SPRUNG,Gs,Hs)
if _WV:
    _cap=nd.maximum_filter(Hs,int(os.environ.get('CAPW','7')));_ex=np.maximum(Gs-_cap,0)*(0 if os.environ.get('NOCAP') else 1);Gs=Gs-(nd.gaussian_filter(_ex,1.5)*(Rg>SPRUNG) if _WV>=3 else _ex)   # G5: Kante nicht hoeher als Plateau in Naehe [A]
    if _WV>=2:_sg=float(os.environ.get('KEHLE','2'));Gs=np.where(Rg>SPRUNG,nd.gaussian_filter(Gs,_sg)*(1-_WM)+Gs*_WM,Gs)   # Fuss/Kopf weich (C1-Hohlkehle) [A]
Gsamp=Hs*(1-wz)+Gs*wz
vj,vi=np.mgrid[0:GY,0:GX].astype(float)
G=nd.map_coordinates(Gsamp,[vj-0.5,vi-0.5],order=1,mode='nearest').astype(np.float32)
_wellen_snap('g_wandmodell',G)
# t50u: thermische Erosion nur im Wandfuss (Schutthalden, Rinnen); Plateaus/Talboden/Wasser fix [A]
_fm=nd.map_coordinates(((t<0.22)&(Rg>SPRUNG)).astype(float),[vj-0.5,vi-0.5],order=1)>0.5
_fm&=~(nd.map_coordinates(nd.binary_dilation(np.kron(wa,np.ones((RS,RS))),iterations=3).astype(float),[vj-0.5,vi-0.5],order=0)>0.5)
TAL=np.tan(np.radians(34))/RS;Ge=G.astype(np.float64)
for _ in range(30):
    for ax,sh in ((0,1),(0,-1),(1,1),(1,-1)):
        Nb=np.roll(Ge,sh,axis=ax);ok=_fm&np.roll(_fm,sh,axis=ax);ex=np.where(ok,np.clip(Ge-Nb-TAL,0,None)*0.2,0)
        Ge-=ex;Ge+=np.roll(ex,-sh,axis=ax)
# t48u R5: hydraulische Erosion (Tropfen-Modell), nur Wandzone ohne Wasser, Abtrag/Ablage je Punkt max 0,8 m [A]
_hm=nd.map_coordinates(((t>0.05)&(t<0.95)&(Rg>SPRUNG)).astype(float),[vj-0.5,vi-0.5],order=1)>0.5
_hm&=~(nd.map_coordinates(nd.binary_dilation(np.kron(wa,np.ones((RS,RS))),iterations=3).astype(float),[vj-0.5,vi-0.5],order=0)>0.5)
_G0=Ge.copy();_hr=np.random.default_rng(77);_st=np.argwhere(_hm);_st=_st[_hr.integers(0,len(_st),min(30000,len(_st)))]
_EF='erosion_start_t63u.npy'   # t63u: Tropfen-Startpunkte aus Runde J (ohne Flussverlegung) eingefroren -> Erosion ausserhalb des Westarms unveraendert [A]
if os.path.exists(_EF):_st=np.load(_EF).astype(int)
else:np.save(_EF,_st.astype(np.int16))
_gy,_gx=np.gradient(Ge)
for _y,_x in _st:
    y,x=float(_y),float(_x);sed=0.0;v=1.0
    for _k in range(24):
        iy,ix=int(y),int(x)
        if not(0<iy<GY-1 and 0<ix<GX-1) or not _hm[iy,ix]:break
        dy,dx=-_gy[iy,ix],-_gx[iy,ix];l=np.hypot(dx,dy)
        if l<1e-4:break
        ny_,nx_=y+dy/l*0.7,x+dx/l*0.7;h0=Ge[iy,ix];h1=Ge[int(ny_),int(nx_)];dh=h0-h1
        cap=max(dh,0.01)*v*0.5
        if sed>cap or dh<0:dep=min(sed,max(-dh,0)) if dh<0 else (sed-cap)*0.3;Ge[iy,ix]+=dep;sed-=dep
        else:er=min((cap-sed)*0.3,dh*0.5);Ge[iy,ix]-=er;sed+=er
        v=np.sqrt(max(v*v+dh*0.5,0.01));y,x=ny_,nx_
Ge=_G0+np.clip(nd.gaussian_filter(Ge-_G0,0.6),-0.8,0.8)
print('hydro_erosion_m',round(float(np.abs(Ge-_G0).max()),2),round(float(np.abs(Ge-_G0)[_hm].mean()),3))
G=Ge.astype(np.float32)
_wellen_snap('g_erosion',G)
# t53u R2/R3: Rampen + Serpentinen nach Erosion exakt ins Gitter (Kern 1,6 m eben laengs, Rand weich bis 3,6 m) [A]
from scipy.spatial import cKDTree
_PP=np.concatenate([p for p,_ in RAMPPROF]);_HH=np.concatenate([h for _,h in RAMPPROF]);_kd=cKDTree(_PP)
_vx=np.stack([vi.ravel()/RS,vj.ravel()/RS],1);_r,_k=_kd.query(_vx,distance_upper_bound=7.0);_ok=np.isfinite(_r)
_wv=nd.map_coordinates(np.kron(wa,np.ones((RS,RS))).astype(float),[vj-0.5,vi-0.5],order=0,mode='nearest').ravel()>0.5
_ok&=~_wv;_w=np.clip((7.0-_r[_ok])/5.4,0,1);_w=_w*_w*(3-2*_w);_g=G.ravel().astype(float);_g[_ok]=_g[_ok]*(1-_w)+_HH[_k[_ok]]*_w;G=_g.reshape(G.shape).astype(np.float32)
_wellen_snap('g_rampen',G)
RAMP_STEIL=[]
for p,h in RAMPPROF:
    gp=nd.map_coordinates(G,[p[:,1]*RS,p[:,0]*RS],order=1);L=np.r_[0,np.cumsum(np.hypot(*np.diff(p,axis=0).T))]
    i=np.searchsorted(L,np.arange(0,L[-1],2.0));sl=np.degrees(np.arctan(np.abs(np.diff(gp[i]))/2.0)) if len(i)>1 else [0]
    RAMP_STEIL.append(round(float(np.max(sl)),1))
print('rampen_max_grad_je_2m',RAMP_STEIL)
wm=np.kron(wa,np.ones((RS,RS))).astype(float);Wn=np.kron(np.nan_to_num(Wsp),np.ones((RS,RS)))
lev=nd.gaussian_filter(Wn*wm,2)/np.maximum(nd.gaussian_filter(wm,2),1e-6)
wmask=nd.map_coordinates(nd.gaussian_filter(wm,1),[vj-0.5,vi-0.5],order=1,mode='nearest')>0.5
WV=np.where(wmask,np.maximum(nd.map_coordinates(lev,[vj-0.5,vi-0.5],order=1,mode='nearest'),G+0.05),-999).astype(np.float32)
LEV_ROH=nd.map_coordinates(lev,[vj-0.5,vi-0.5],order=1,mode='nearest')   # t61u [A]
# t132u: R8b-Dellen im abgeleiteten G nur anheben, wenn die ganze Senke an einem Weg/Rampenweg liegt.
# Zellquellen und Wandpunkte bleiben unangetastet; DELLENWEG=0 schaltet die Variante aus.
def dellen_bei_wegen_anheben(GA,WVA):
    variante=int(os.environ.get('DELLENWEG','1'))
    if variante not in (0,1):raise ValueError('DELLENWEG muss 0 oder 1 sein')
    if variante==0:return GA,{'variante':0,'komponenten':0,'punkte':0,'max_anhebung_m':0.0}
    from skimage.morphology import reconstruction
    _G=np.asarray(GA,dtype=np.float32)
    _weg=np.zeros((GY,GX),bool)
    for _o in csv.DictReader(open(B+'raster_c20_z25_overlay_plaetze_wege.csv')):
        if not _o['weg_id']:continue
        _x,_y=int(_o['cx']),int(_o['cy'])
        _weg[_y*RS:_y*RS+RS+1,_x*RS:_x*RS+RS+1]=True
    for _r in RAMPWEGE:
        _r=np.asarray(_r,float);_L=np.r_[0,np.cumsum(np.hypot(*np.diff(_r,axis=0).T))]
        _t=np.arange(0,_L[-1]+1e-6,0.25)
        _y=np.clip((np.interp(_t,_L,_r[:,1])*RS).round().astype(int),0,GY-1)
        _x=np.clip((np.interp(_t,_L,_r[:,0])*RS).round().astype(int),0,GX-1)
        _weg[_y,_x]=True
    _abstand=nd.distance_transform_edt(~_weg)/RS
    _punkte=_komponenten=0;_max=0.0;_durchlaeufe=0
    for _it in range(3):
        _saum=_G.copy();_saum[1:-1,1:-1]=float(_G.max())
        _fuellung=reconstruction(_saum,_G,method='erosion')-_G
        _gy,_gx=np.gradient(_G.astype(float),1/RS);_wand=np.hypot(_gx,_gy)>1.0
        _mulde=(_fuellung>0.30)&(WVA<=-900)&~nd.binary_dilation(_wand,iterations=1)
        _lab,_n=nd.label(_mulde);_heben=np.zeros_like(_mulde);_anz=0
        for _k,_sl in enumerate(nd.find_objects(_lab),1):
            _m=_lab[_sl]==_k
            if _abstand[_sl][_m].min()<=6.0:_heben[_sl]|=_m;_anz+=1
        if not _heben.any():break
        _durchlaeufe+=1;_punkte+=int(_heben.sum());_komponenten+=_anz
        _max=max(_max,float(_fuellung[_heben].max()))
        _G[_heben]=(_G[_heben]+_fuellung[_heben]).astype(np.float32)
    return _G,{'variante':1,'durchlaeufe':_durchlaeufe,'komponenten':_komponenten,
                'punkte':_punkte,'max_anhebung_m':round(_max,3)}
# Dreiecke je Teilquadrat (a=oben links,b=oben rechts,c=unten links,d=unten rechts): (a,c,d) und (a,d,b) – gleich im Viewer
def tri_steil(G):
    a=G[:-1,:-1];b=G[:-1,1:];c=G[1:,:-1];d=G[1:,1:];s=1/RS
    def ny(dx1,dy1,dz1,dx2,dy2,dz2):
        n=np.stack([dy1*dz2-dz1*dy2,dz1*dx2-dx1*dz2,dx1*dy2-dy1*dx2]);return np.abs(n[1])/np.linalg.norm(n,axis=0)
    z0=np.zeros_like(a)
    n1=ny(z0,c-a,z0+s,z0+s,d-a,z0+s);n2=ny(z0+s,d-a,z0+s,z0+s,b-a,z0)
    return np.degrees(np.arccos(np.clip(n1,0,1))),np.degrees(np.arccos(np.clip(n2,0,1)))
W1,W2=tri_steil(G);Wq=np.maximum(W1,W2)                           # Neigung je Teilquadrat
neig=Wq.reshape(NY,RS,NX,RS).max((1,3))
steil=neig>WANDWINKEL
Hz=sum(G[dy:dy+GY-1:RS,dx:dx+GX-1:RS][:NY,:NX] for dy in range(3) for dx in range(3))/9    # Zellmittel 3x3 Punkte
Gmax=nd.maximum_filter(np.maximum.reduceat(np.maximum.reduceat(G,np.arange(0,GY-1,RS),0),np.arange(0,GX-1,RS),1)[:NY,:NX],5)
Gmin=nd.minimum_filter(np.minimum.reduceat(np.minimum.reduceat(G,np.arange(0,GY-1,RS),0),np.arange(0,GX-1,RS),1)[:NY,:NX],5)
nb=nd.binary_dilation(steil,structure=np.ones((3,3)))&~steil
mid=(Gmax+Gmin)/2
oben=nb&(Hz>=mid);fuss=nb&(Hz<mid)
kh=np.where(steil|nb,Gmax-Gmin,0.0)
C=np.stack([G[0:-1:RS,0:-1:RS][:NY,:NX],G[0:-1:RS,RS::RS][:NY,:NX],G[RS::RS,RS::RS][:NY,:NX],G[RS::RS,0:-1:RS][:NY,:NX]],-1)
# --- neuer Untergrund: Bandzellen sind jetzt Oberflaeche der oberen Ebene [F]
ug2=ug.copy();ug2[wand]='SCHNEE';ug2[wand&(wn=='Krater')&(nd.gaussian_filter(np.random.default_rng(5).standard_normal((NY,NX)),3)>0.25)]='FELS';ug2[ug=='SCHATTEN']='SCHNEE'
ug2[wa]='WASSER_EIS'
b3d_alt=A('begehbar_3d')=='1'
b3d=(neig<=35)&(b3d_alt|wand)&~(wa&(fl=='SEE'))
ebene2=eb.copy();ebene2[wand]=np.where(wn[wand]=='Nord','PLATEAU_NORD',np.where(wn[wand]=='Ostgrat','OSTPLATEAU',np.where(wn[wand]=='Krater','KRATERRAND','SENKE')))
kl=np.where(steil,'WAND',np.where(oben,'WAND_OBEN',np.where(fuss,'WAND_FUSS','')))
neu={'untergrund':ug2,'untergrund_quelle':np.where(ug2!=ug,'relief_t43u',A('untergrund_quelle')),'ebene':ebene2,'klippe':kl,
 'skin_slot':np.where(steil,'wand_fels',np.char.add('ug_',np.char.lower(ug2.astype(str)))),'hoehe_m':np.round(Hz,2),'hoehe_quelle':np.full((NY,NX),'R_relief_t43u'),
 'neigung_grad':np.round(neig,1),'klippe_hoehe_m':np.round(kh,1),'klippe_hoehe_quelle':np.where(kh>0,'R_messung_t40u','') ,
 'wasser_tiefe_m':np.where(wa,np.round(tiefe,2),0).astype(str),'begehbar_3d':b3d.astype(int),'wasser_eis':wa.astype(int).astype(str),'fluss_id':fl}
extra={'boden_hoehe_m':np.round(Hboden,2),'wasserspiegel_m':np.where(wa,np.round(np.nan_to_num(Wsp),2).astype(str),''),
 'ecke_nw_m':np.round(C[...,0],2),'ecke_no_m':np.round(C[...,1],2),'ecke_so_m':np.round(C[...,2],2),'ecke_sw_m':np.round(C[...,3],2),
 'ebene_c20':eb,'untergrund_c20':ug}
outcols=cols+list(extra)
F={c:(neu[c] if c in neu else extra[c] if c in extra else A(c)) for c in outcols}
with open('zellen_relief.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(outcols)
    for y in range(NY):
        for x in range(NX):w.writerow([F[c][y,x] for c in outcols])
# --- Mesh (gleiche Dreiecke + gleiche Wandregel wie Viewer) -> GLB mit "boden" (UV = c20-Draufsicht) und "waende"
import trimesh
V=np.stack([vi.ravel()/RS,G.ravel(),vj.ravel()/RS],1);UV=np.stack([vi.ravel()/RS/NX,1-vj.ravel()/RS/NY],1)
I=(np.arange(GY-1)[:,None]*GX+np.arange(GX-1)[None,:]);a=I;b=I+1;c=I+GX;d=I+GX+1
T1=np.stack([a,c,d],-1);T2=np.stack([a,d,b],-1)
TT=np.concatenate([T1.reshape(-1,3),T2.reshape(-1,3)]);ST=np.concatenate([W1.ravel(),W2.ravel()])>WANDWINKEL
sc=trimesh.Scene()
sc.add_geometry(trimesh.Trimesh(V,TT[~ST][:,::-1],process=False,visual=trimesh.visual.TextureVisuals(uv=UV)),'boden')
sc.add_geometry(trimesh.Trimesh(V,TT[ST][:,::-1],process=False),'waende')
sc.export('dorfmap_relief_z25.glb');TW=TT[ST]
# --- Objekte (Groessen wie t39u, nur auf neues Relief)
hc=lambda x,y:float(nd.map_coordinates(G,[[y*RS],[x*RS]],order=1,mode='nearest')[0])
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
    gg=G[iy.start*RS:iy.stop*RS+1,ix.start*RS:ix.stop*RS+1];g=float(np.median(gg)) if gg.size else 0
    haeuser.append({'id':p['id'],'typ':t,'x':round((x0+x1)/2,2),'z':round((y0+y1)/2,2),'b':round(x1-x0,2),'t':round(y1-y0,2),'h':HH[k],'y':round(g,2)})
# t43u: Objekte in Gruppen (Dichte aus weichem Rauschen), Groessen-/Drehvarianz, Kraterrand duenner, Geroell am Wandfuss [A]
rs2=np.random.default_rng(43);dich=nd.gaussian_filter(rs2.standard_normal((NY,NX)),4);dich/=dich.std()
baeume=[];felsen=[];steine=[];geroell=[]
for y in range(NY):
    for x in range(NX):
        if belegt[y,x] or weg[y,x] or steil[y,x]:continue
        u=rs2.random(5)
        if ug2[y,x]=='WALD' and u[0]<0.22*np.clip(0.6+0.8*dich[y,x],0,1.6):
            X,Z=min(x+u[1],NX-0.5),min(y+u[2],NY-0.5);baeume.append([round(X,2),round(hc(X,Z),2),round(Z,2),round(5+6*u[3]**1.5,1),round(u[4]*6.28,2),round(rs2.random(),2)])
        if ug2[y,x]=='FELS' and u[0]<(0.05 if wn[y,x]=='Krater' else 0.09)*np.clip(0.5+dich[y,x],0,2):
            s=0.5+1.6*u[3]**2;X,Z=x+u[1],y+u[2];felsen.append([round(X,2),round(hc(X,Z)-0.25*s,2),round(Z,2),round(s,2),round(u[4]*6.28,2)])
        if deko[y,x] and not wa[y,x] and u[0]<0.5:X,Z=x+u[1],y+u[2];steine.append([round(X,2),round(hc(X,Z)-0.1,2),round(Z,2),round(0.3+0.5*u[3],2),round(u[4]*6.28,2)])
        if fuss[y,x] and not wa[y,x] and u[0]<0.18:
            for _ in range(1+int(u[3]*3)):
                v=rs2.random(4);s=0.2+0.6*v[2]**2;X,Z=x+v[0],y+v[1];geroell.append([round(X,2),round(hc(X,Z)-0.2*s,2),round(Z,2),round(s,2),round(v[3]*6.28,2)])
# t48u: Ufersteine, Baumgruppen an Klippenkanten, Trockengras-Bueschel [A]
ufr=nd.binary_dilation(wa,iterations=1)&~wa&~belegt&~steil;kante=nd.binary_dilation(steil,iterations=4)&~nd.binary_dilation(steil,iterations=1)&~belegt&~wa&~weg
hoch=nd.maximum_filter(Hz,7)-Hz<1.0;gras=[];r48=np.random.default_rng(481);grp_=nd.gaussian_filter(r48.standard_normal((NY,NX)),2.5);grp_/=grp_.std()
for y,x in np.argwhere(ufr):
    u=r48.random(4)
    if u[0]<0.45:X,Z=x+u[1],y+u[2];s=0.25+0.7*u[3]**2;steine.append([round(X,2),round(hc(X,Z)-0.15*s,2),round(Z,2),round(s,2),round(u[0]*14,2)])
for y,x in np.argwhere(kante&hoch&(grp_>0.6)):
    u=r48.random(6)
    if u[0]<0.55:X,Z=x+u[1],y+u[2];baeume.append([round(X,2),round(hc(X,Z),2),round(Z,2),round(5+7*u[3]**1.3,1),round(u[4]*6.28,2),round(u[5],2)])
for y,x in np.argwhere((ug2=='SCHNEE')&~belegt&~weg&~steil&~wa):
    u=r48.random(5)
    if u[0]<0.10*np.clip(grp_[y,x]+0.6,0,2):X,Z=x+u[1],y+u[2];gras.append([round(X,2),round(hc(X,Z),2),round(Z,2),round(0.35+0.5*u[3],2),round(u[4]*6.28,2)])
# t48u: Felsbloecke/Felsplatten entlang aller Wandbaender (eigene Meshes, Instancing) [A]
gzy,gzx=np.gradient(Hz);bl_r=np.random.default_rng(48);felsbloecke=[]
for y,x in np.argwhere(steil&~wa):
    u=bl_r.random(7)
    if True:continue   # t54u: keine Blockinstanzen mehr als Wandform (Fels = Feinrelief FW) [A]
    nx_,nz_=-gzx[y,x],-gzy[y,x];l=np.hypot(nx_,nz_)+1e-6;nx_/=l;nz_/=l   # Blick talwaerts
    X,Z=x+0.5+0.6*(u[1]-0.5),y+0.5+0.6*(u[2]-0.5);Y=hc(X,Z)
    gr=0.45 if u[6]<0.3 else (1.0 if u[6]<0.85 else 1.45)   # t48u R5: Groessenmix klein/mittel/gross [A]
    sx=gr*(2.0+3.8*u[3]**1.3);sy=gr*(1.2+3.0*u[4]**1.5);sz=gr*(1.3+1.6*u[5])
    felsbloecke.append([round(X+0.35*nx_,2),round(Y-0.25*sy,2),round(Z+0.35*nz_,2),round(sx,2),round(sy,2),round(sz,2),round(float(np.arctan2(nx_,nz_)),3),round(u[6]-0.5,2)])
# t53u R1: Ueberhaenge = flache Blender-Felsplatten an der Wandkrone, 1-2 m ueber die Kante talwaerts auskragend [A]
UEBERHANG=0;_ohr=np.random.default_rng(531);_kr2=oben&nd.binary_dilation(steil,iterations=1)&~wa&~belegt&~weg&~nd.binary_dilation(wa,iterations=4)
for y,x in np.argwhere(_kr2):
    u=_ohr.random(6)
    if True:continue   # t54u: Ueberhang-Platten entfernt (Blockhaufen-Eindruck)
    nx_,nz_=-gzx[y,x],-gzy[y,x];l=np.hypot(nx_,nz_)+1e-6;nx_/=l;nz_/=l
    X,Z=x+0.5,y+0.5;Y=float(Gmax[y,x]) if False else hc(X,Z);ko=1.0+1.0*u[1]
    sx=3.0+3.5*u[2];sy=0.9+0.9*u[3];sz=2.2+1.8*u[4]
    felsbloecke.append([round(X+ko*nx_,2),round(Y-0.45*sy,2),round(Z+ko*nz_,2),round(sx,2),round(sy,2),round(sz,2),round(float(np.arctan2(nx_,nz_)),3),round(u[5]-0.5,2)]);UEBERHANG+=1
print('ueberhaenge',UEBERHANG)
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
# t43u: Bodenfarbe je Vertex aus Zelleigenschaften (Splat-Gewichte, weich), c20 nur als schwache Toenung (12 %) [A]
from PIL import Image
up=lambda M,s=1.5:nd.map_coordinates(nd.gaussian_filter(np.kron(M.astype(float),np.ones((RS,RS))),s*RS),[vj-0.5,vi-0.5],order=1,mode='nearest')
nz=lambda s,sd:(lambda a:a/a.std())(nd.gaussian_filter(np.random.default_rng(sd).standard_normal((GY,GX)),s))
MAT={'SCHNEE':(0.88,0.91,0.95),'WALD':(0.70,0.74,0.69),'FELS':(0.52,0.49,0.46),'BODEN':(0.47,0.37,0.27),'SAND':(0.78,0.69,0.53),'WASSER_EIS':(0.66,0.76,0.82)}
gew={k:up(ug2==k)*(1+0.35*nz(4,i))**2 for i,k in enumerate(MAT)}
gew['MOOS']=up(ug2=='WALD',3.0)*np.clip(nz(3,31),0,None)*0.8;MAT['MOOS']=(0.36,0.42,0.27)   # Moos/Nadelstreu am Waldrand [A]
gew['ERDE2']=up(np.isin(ug2,['BODEN','FELS']),2.0)*np.clip(nz(2,33)-0.6,0,None)*0.7;MAT['ERDE2']=(0.38,0.30,0.22)
gew['GEROELL']=up(fuss|steil,1.0)*0.9*(1+0.4*nz(2,11)).clip(0);MAT['GEROELL']=(0.55,0.53,0.50)
_gn=0.6*nz(6,51)+0.4*nz(1.5,52);_sl=np.hypot(*np.gradient(G))*RS   # t48u: fleckiger Schnee – Trockengras/Moos schaut durch, mehr an Kuppen/Hangkanten [A]
gew['GRAS']=up(ug2=='SCHNEE')*np.clip(_gn-0.75+0.5*np.clip(_sl-0.3,0,1),0,None)*2.8;MAT['GRAS']=(0.50,0.47,0.31)
gew['MOOS2']=up(ug2=='SCHNEE')*np.clip(nz(2.5,53)-1.3,0,None)*gew['GRAS'].clip(0,1)*3;MAT['MOOS2']=(0.30,0.36,0.24)
gew['NASS']=np.clip(up(wa,1.0)-0.05,0,1)*0.6;MAT['NASS']=(0.40,0.45,0.48)
S=sum(gew.values())+1e-6;col=sum(np.array(MAT[k])[None,None,:]*(gew[k]/S)[...,None] for k in gew)
c20=np.asarray(Image.open('../_alt/modell3d_t36u/textur_c20_8px.jpg').convert('RGB').resize((GX,GY),Image.BILINEAR)).astype(float)/255
c20=np.stack([nd.gaussian_filter(c20[...,c],6) for c in range(3)],-1);ton=c20/np.maximum(c20.mean(-1,keepdims=True),1e-3)
gzv,gxv=np.gradient(G);weh=np.clip(0.5+0.8*nz(10,41)+0.6*np.tanh(gzv*3),0,1);sn=gew['SCHNEE']/S
col=col*(1-sn*0.10*weh)[...,None]+(sn*0.10*weh)[...,None]*np.array([0.70,0.80,0.95])
col=col*(1+0.12*(ton-1))*(1+0.05*nz(1.5,21))[...,None]
# t54u-C: klare Uferlinie (nasser dunkler Saum direkt am Wasser) + Kies/Flussgrund hell sichtbar unter flachem Wasser [A]
def ufer_farbe(col,_wu):
    _ul=np.clip(1-np.abs(_wu-0.35)/0.25,0,1)*(1-up(wand,0.6))
    col=col*(1-0.75*_ul[...,None])+0.75*_ul[...,None]*np.array([0.30,0.29,0.27])
    _kg=np.clip(up(kies,0.5)*1.4,0,1)*np.clip((_wu-0.5)*3,0,1);col=col*(1-_kg[...,None])+_kg[...,None]*np.array([0.62,0.58,0.52])
    _fg=np.clip((_wu-0.6)*3,0,1)*(1-_kg);return col*(1-0.7*_fg[...,None])+0.7*_fg[...,None]*np.array([0.42,0.40,0.36])
COL_BASIS=col.copy();WU_ZELLE=up(wa,0.6)
VC=(np.clip(ufer_farbe(col,WU_ZELLE),0,1)*255).astype(np.uint8)
# t48u R5: GLB neu mit Vertexfarben (boden+waende), fuer GLTFLoader-Pfad im Viewer (?glb=1 ueber lokalen Server) [A]
_vc=np.concatenate([VC.reshape(-1,3),np.full((VC.reshape(-1,3).shape[0],1),255,np.uint8)],1)
sc=trimesh.Scene()
sc.add_geometry(trimesh.Trimesh(V,TT[~ST][:,::-1],process=False,vertex_colors=_vc),'boden')
sc.add_geometry(trimesh.Trimesh(V,TT[ST][:,::-1],process=False,vertex_colors=_vc),'waende')
sc.export('dorfmap_relief_z25.glb')
# t54u: Feinrelief der Wandbaender (0,25 m) als zusammenhaengende Felsform; nur Anzeige, Zellwerte bleiben aus G [A]
FS=4;FXn,FYn=NX*FS+1,NY*FS+1
_rkd=cKDTree(np.concatenate([p for p,_ in RAMPPROF]));_cc=np.stack(np.meshgrid(np.arange(NX)+0.5,np.arange(NY)+0.5),-1).reshape(-1,2)
_nahr=(_rkd.query(_cc,distance_upper_bound=4.5)[0]<9).reshape(NY,NX)
BAND=nd.binary_dilation(steil|oben|fuss,iterations=3)&~nd.binary_dilation(wa,iterations=1)&~belegt   # Runde E: Band breiter (3 statt 1) [A]   # t54u-C: Rampennaehe jetzt im Band (FD dort weich auf 0) statt glatter grauer Streifen
BAND=nd.binary_opening(BAND,iterations=1)|(BAND&steil)
_fy,_fx=np.mgrid[0:FYn,0:FXn].astype(float);_gx=_fx/FS*RS;_gy=_fy/FS*RS
_i=np.minimum(_gx.astype(int),GX-2);_j=np.minimum(_gy.astype(int),GY-2);_ax=_gx-_i;_az=_gy-_j
import runde_o_t67u as RO;G_SP_T67U,GSP9_T67U=RO.grob_spitzen_alle(G);print('grobspitzen9_t67u',GSP9_T67U)   # t67u O9: Grobspitzen auch an Feinband-Ecken, Grob+Fein gemeinsam (nur Anzeige) [A]
_jj,_ii=np.mgrid[0:G.shape[0],0:G.shape[1]];_cy=np.clip(_jj//RS,0,BAND.shape[0]-1);_cx=np.clip(_ii//RS,0,BAND.shape[1]-1);_cy2=np.clip((_jj-1)//RS,0,BAND.shape[0]-1);_cx2=np.clip((_ii-1)//RS,0,BAND.shape[1]-1);_mk=~(BAND[_cy,_cx]&BAND[_cy2,_cx]&BAND[_cy,_cx2]&BAND[_cy2,_cx2]);G_SP_T67U,KB_T67U=RO.kegel_breit(G_SP_T67U,_mk);print('kegelbreit_t67u',KB_T67U)   # t67u O9b: breite Kegel ausserhalb Feinband-Inneres, vor FB-Bau -> kein Spalt [A]
_A=G_SP_T67U[_j,_i];_B=G_SP_T67U[_j,_i+1];_C=G_SP_T67U[_j+1,_i];_D=G_SP_T67U[_j+1,_i+1]
FB=np.where(_az>=_ax,_A+_az*(_C-_A)+_ax*(_D-_C),_A+_ax*(_B-_A)+_az*(_D-_B))       # exakt die G-Dreiecke
_FB0_T67U=FB.copy()   # t67u O5: exakte Grobform fuer Bandrand-Uebergang [A]
_qb=np.kron(BAND,np.ones((FS,FS),bool));_qp=np.pad(_qb,1)
_vin=_qp[:-1,:-1]&_qp[:-1,1:]&_qp[1:,:-1]&_qp[1:,1:]                                   # Vertex innen (alle 4 Quads im Band)
_wf=nd.distance_transform_edt(_vin)/10.0;_wf=np.clip(_wf,0,1);_wf=_wf*_wf*(3-2*_wf)
def _ff(sig,seed):
    r=np.random.default_rng(seed);n=nd.gaussian_filter(r.standard_normal((FYn,FXn)).astype(np.float32),sig);return n/n.std()
_wy=_fy+16*_ff(30,61);_wx=_fx+16*_ff(30,62)
_R=sum(a*(1-np.abs(np.clip(nd.map_coordinates(_ff(sg,sd),[_wy,_wx],order=1,mode='reflect')/2.0,-1,1))) for a,sg,sd in ((0.5,18,63),(0.3,8,64),(0.2,3.5,65)))
_R=(_R-_R.min())/(_R.max()-_R.min())
_sgy,_sgx=np.gradient(FB,1/FS);_sl=np.degrees(np.arctan(np.hypot(_sgx,_sgy)));_sf=np.clip((nd.gaussian_filter(_sl,3)-20)/35,0,1)
# t54u-C: Wandform = Schichtbaender (Terrassen/Absaetze) + Rinnen/Rippen in Falllinie + ridged fBm + hydraulische & thermische Erosion [A]
_fbs=nd.gaussian_filter(FB,6);_gyy,_gxx=np.gradient(_fbs,1/FS);_gm=np.hypot(_gxx,_gyy)+1e-6;_tx,_ty=-_gyy/_gm,_gxx/_gm      # Tangente (Hoehenlinie)
_xm,_ym=_fx/FS,_fy/FS;_sco=(_xm*_tx+_ym*_ty)+3.0*_ff(60,71)                                                            # Konturkoordinate [m]
_lo=nd.minimum_filter(FB,41);_hi=nd.maximum_filter(FB,41);_tl0=np.clip((FB-_lo)/np.maximum(_hi-_lo,1),0,1);_bell=np.sin(np.pi*_tl0)
_NT=np.random.default_rng(72).standard_normal((512,512));_NT=nd.gaussian_filter(_NT,3,mode='wrap');_NT/=_NT.std()
def _nt(a,b,o=0.0):return nd.map_coordinates(_NT,[np.mod(b+o,512),np.mod(a,512)],order=1,mode='grid-wrap')
_g1=_nt(_sco/0.7,FB/2.5+_ff(30,73)*2,0);_g2=_nt(_sco/0.3+100,FB/1.2,200)
_rib=(np.abs(np.clip(_g1/2,-1,1))**0.6-0.55)*1.3+(np.abs(np.clip(_g2/2,-1,1))**0.7-0.55)*0.45                         # scharfe Rinnen, runde Rippen
# Voronoi-Pfeiler (Kluefte): jede Zelle ~5 m eigener Versatz + eigene Schichtphase, schmale Kluft an den Grenzen [A]
_vr=np.random.default_rng(80);_npf=int(FXn*FYn/(20*20));_vp=np.stack([_vr.random(_npf)*FYn,_vr.random(_npf)*FXn],1)
_vq=np.stack([_fy.ravel()+6*_ff(25,81).ravel(),_fx.ravel()+6*_ff(25,82).ravel()],1);_vd,_vi=cKDTree(_vp).query(_vq,k=2)
_vi=_vi[:,0].reshape(FB.shape);_kl=np.clip(1-(_vd[:,1]-_vd[:,0]).reshape(FB.shape)/3.0,0,1)**2
_voff=(_vr.random(_npf)*2-1)[_vi];_vph=_vr.random(_npf)[_vi]
_T=2.6+0.6*_ff(50,74);_Lc=(FB+1.0*_ff(35,75)+0.4*_ff(8,76))/_T+0.45*_vph;_lk=np.floor(_Lc);_lf=_Lc-_lk
_pr=np.clip((_lf-0.55)/0.45,0,1);_pr=_pr*_pr*(3-2*_pr);_ter=(_pr-_lf)*_T*0.75                                          # Absatz flach, Stufe steil
_rdq=np.full(FB.shape,99.0);_qq=np.argwhere(_vin);_rdq[_qq[:,0],_qq[:,1]]=_rkd.query(_qq[:,::-1]/FS,distance_upper_bound=8)[0]
_wr=np.clip((np.minimum(_rdq,8)-1.6)/3.0,0,1);_wr=_wr*_wr*(3-2*_wr);_wf=_wf*_wr
# Runde D: Oberkante seitlich verspringen – Warp der Feinbasis im Band (Vorspruenge/Buchten bis ~2,5 m); Zellwerte bleiben unberuehrt [A]
_fjj,_fii=np.mgrid[0:FB.shape[0],0:FB.shape[1]].astype(float);_rq=lambda sg,sd:(lambda n:n/n.std())(nd.gaussian_filter(np.random.default_rng(sd).standard_normal(FB.shape),sg))
_wa=_wf*np.clip(nd.distance_transform_edt(_vin)/24.0,0,1);_wa=_wa*_wa*(3-2*_wa)   # Runde E: weicher, weiter [A]
FB=np.where(_vin,nd.map_coordinates(FB,[_fjj+_wa*(14*_rq(40,91)+6*_rq(12,92)+2.5*_rq(4,95)),_fii+_wa*(14*_rq(40,93)+6*_rq(12,94)+2.5*_rq(4,96))],order=1,mode='nearest'),FB)
FB=np.where(_vin,FB*(1-_wf)+nd.gaussian_filter(FB,1.6)*_wf,FB)   # Politur t58u: Gitter-/Treppenartefakte aus bilinearem Grobgitter glaetten (nur Feinband) [A]
_qy,_qx=np.gradient(nd.gaussian_filter(FB,3),1/FS);_gm=np.clip(np.hypot(_qx,_qy),0.4,2.0)   # Runde D: eigene Namen (Runde C ueberschrieb _gy/_gx -> Farbe 0 = schwarz) [A]   # seitlicher Versatz: dh=dx*Steigung [A]
_RB=(np.abs(np.clip(_nt(_sco/2.6+300,FB/9.0,400)/1.6,-1,1))**0.7-0.55)*2.2   # Runde E: Grossrippen/-rinnen in Falllinie [A]
FD=_wf*_sf*(1.4*_ter+_gm*(_RB*(0.4+0.8*_bell)+_rib*(0.5+0.9*_bell)+1.0*(_R-0.5)+_bell**0.6*(1.2*_voff-0.45*_kl)))+_wf*(1-_sf)*0.5*(_R**2)
# t57u: Grat mit Tuermen/Felsnasen an der Oberkante (echte Geometrie), laeuft weich in die Flaeche aus [A]
_ed=nd.gaussian_filter(_sf,7);_cz=_wf*np.clip((_tl0-0.62)/0.3,0,1)*np.clip(_ed*2.2,0,1)
_pk=np.clip(1-np.abs(_ff(9,201))/1.6,0,1)**3;_pk2=np.clip(1-np.abs(_ff(4,202))/1.6,0,1)**3
_TW=_cz*(4.2*_pk*(0.6+0.6*np.clip(_voff,0,1))+1.6*_pk2+0.8*np.clip(_RB,0,None))
FD=FD+_TW
# Runde F: Pfeiler + Kare in Falllinie (grosse Skala, ~14 m Abstand), Gipfelpyramiden mit Facetten und Saetteln am Grat [A]
_pf=np.sin(2*np.pi*(_sco/14.0+0.35*_ff(40,211)));_pf=np.sign(_pf)*np.abs(_pf)**0.5
FD=FD+_wf*_sf*_bell**0.5*_gm*1.05*_pf                                                    # Pfeiler (+) / Kar-Rinne (-), seitlich wirksam ueber Steigung
_kar=_wf*np.clip((_tl0-0.55)/0.35,0,1)*np.clip(-_pf,0,1)*np.clip(_ed*2,0,1);FD=FD-2.8*_kar   # Kare: Mulden an der Oberkante zwischen Pfeilern
_cq=np.argwhere((_cz>0.55)&(_pf>0.6));_rp=np.random.default_rng(212);_PY=[]
if len(_cq):
    _rp.shuffle(_cq);_kt=[]
    for q in _cq:
        if all(abs(q[0]-k[0])+abs(q[1]-k[1])>150 for k in _kt):_kt.append(q)
    for q in _kt[:60]:
        r=_rp.uniform(28,44);h=_rp.uniform(4.5,8.0);a0=_rp.uniform(0,np.pi/2)
        y0,y1,x0,x1=max(0,int(q[0]-r)),min(FB.shape[0],int(q[0]+r)+1),max(0,int(q[1]-r)),min(FB.shape[1],int(q[1]+r)+1)
        dy,dx=_fy[y0:y1,x0:x1]-q[0],_fx[y0:y1,x0:x1]-q[1]
        d=np.maximum(np.abs(dx*np.cos(a0)+dy*np.sin(a0)),np.abs(-dx*np.sin(a0)+dy*np.cos(a0)))*0.75+0.25*np.hypot(dx,dy)   # 4 Facetten, Kanten scharf
        FD[y0:y1,x0:x1]+=_wf[y0:y1,x0:x1]*h*(lambda p:p*p*(3-2*p))(np.clip(1-d/r,0,1))**0.8;_PY.append((float(q[1]/FS),float(q[0]/FS),round(h,1)))
FH=FB+FD
if os.environ.get('G6DIAG'):np.savez_compressed(os.environ['G6DIAG'],FB=FB,FD=FD,ter=_wf*_sf*1.4*_ter,vor=_wf*_sf*_gm*_bell**0.6*(1.2*_voff-0.45*_kl),pf=_wf*_sf*_bell**0.5*_gm*1.05*_pf,kar=-2.8*_kar,TW=_TW,rib=_wf*_sf*_gm*(_RB*(0.4+0.8*_bell)+_rib*(0.5+0.9*_bell)),vin=_vin,wf=_wf)   # O18s G6-Ursache (nur Diagnose)
# hydraulische Erosion (Tropfen, vektorisiert) nur im Feinband
_hr2=np.random.default_rng(78);_cand=np.argwhere(_vin&(_wf>0.3));_ND=min(90000,len(_cand))
_p=_cand[_hr2.integers(0,len(_cand),_ND)].astype(float)+_hr2.random((_ND,2));_v=np.zeros((_ND,2));_sed=np.zeros(_ND);_wat=np.ones(_ND)
for _k in range(70):
    _iy=np.clip(_p[:,0].astype(int),1,FYn-2);_ix=np.clip(_p[:,1].astype(int),1,FXn-2)
    _dy=(FH[_iy+1,_ix]-FH[_iy-1,_ix])/2;_dx=(FH[_iy,_ix+1]-FH[_iy,_ix-1])/2
    _v=0.3*_v-0.7*np.stack([_dy,_dx],1);_vn=np.linalg.norm(_v,axis=1)+1e-9;_v/=_vn[:,None]
    _pn=_p+_v;_jy=np.clip(_pn[:,0].astype(int),1,FYn-2);_jx=np.clip(_pn[:,1].astype(int),1,FXn-2)
    _ok=_vin[_jy,_jx]&_vin[_iy,_ix];_dh=FH[_jy,_jx]-FH[_iy,_ix]
    _cap=np.maximum(-_dh,0.01)*_wat*0.9;_e=np.where(_sed<_cap,np.minimum((_cap-_sed)*0.25,0.05),0);_d=np.where(_sed>=_cap,(_sed-_cap)*0.3,0)
    _d=np.where(_dh>0,np.minimum(_sed,_dh),_d);_e=np.where(_ok,_e,0);_d=np.where(_ok,_d,_sed)
    np.add.at(FH,(_iy,_ix),_d-_e);_sed+=_e-_d;_wat*=0.98;_p=np.where(_ok[:,None],_pn,_p)
_ER=nd.gaussian_filter(FH-(FB+FD),1.5)                                                                                    # <0 = Abtrag (Rinne)
_fe=_vin&(_wf>0)                                                  # thermische Glaettung (Grenzwinkel 62 Grad)
_tl=np.tan(np.radians(66))/FS
for _ in range(30):
    for ax,sh in ((0,1),(0,-1),(1,1),(1,-1)):
        Nb=np.roll(FH,sh,axis=ax);ex=np.where(_fe&np.roll(_fe,sh,axis=ax),np.clip(FH-Nb-_tl,0,None)*0.25,0);FH-=ex;FH+=np.roll(ex,-sh,axis=ax)
FH=np.where(_vin,FH,FB)
# Runde H: Grate schaerfen (Unscharf-Maske nur auf Ruecken, begrenzt) + Felszahn t58u bei x~186 z~37 [A]
_g3=nd.gaussian_filter(FH,3);_rk=np.clip(FH-_g3,0,1.2);FH=np.where(_vin,FH+_wf*_sf*0.4*nd.gaussian_filter(_rk,0.7),FB)
_zx,_zy=186*FS,37*FS;_zw=np.zeros_like(FH);_ys,_xs=slice(_zy-60,_zy+60),slice(_zx-60,_zx+60)
_gzy,_gzx=np.gradient(nd.gaussian_filter(FB,6));_ang=np.arctan2(_gzy[_zy,_zx],_gzx[_zy,_zx])
_dy,_dx=_fy[_ys,_xs]-_zy,_fx[_ys,_xs]-_zx;_al=_dx*np.cos(_ang)+_dy*np.sin(_ang);_qu=-_dx*np.sin(_ang)+_dy*np.cos(_ang)
_pl=np.clip(1-np.abs(_al)/34,0,1);_pl=_pl*_pl*(3-2*_pl);_pq=np.clip(1-np.abs(_qu)/(9+4*np.clip(-_al/34,0,1)),0,1)   # Querprofil linear = klare Gratkante, Fuss breiter
_zw[_ys,_xs]=_pl*_pq**1.1*(1+0.12*np.sin(_al/3.1))
FH=np.where(_vin,FH+_wf*4.5*_zw,FB);_zm=nd.gaussian_filter((_zw>0.02).astype(float),3)

# Politur t58u: Nadelspitzen/Zacken abrunden (lokale Ueberhoehung gegen Umgebung daempfen) [A]
for _ in range(2):
    _g4=nd.gaussian_filter(FH,4);_nad=_wf*(1-_zm)*np.clip((FH-_g4-1.1)/1.5,0,1);FH=np.where(_vin,FH*(1-0.45*_nad)+nd.gaussian_filter(FH,1.8)*0.45*_nad,FB)
# Runde G: Gesimse = steile Kante unter leicht vorgezogener Oberkante, sparsam (Rauschmaske) [A]
_gs=_wf*_sf*np.clip(1-np.abs(_tl0-0.86)/0.06,0,1)*np.clip(_ff(25,231)-0.2,0,1)
FH=np.where(_vin,FH+0.9*nd.gaussian_filter(_gs,1.0),FB)
# Runde F: Schneebaender als Geometrie auf Absaetzen (flach in steiler Umgebung): 0,1-0,3 m Polster [A]
_fs3=np.degrees(np.arctan(np.hypot(*np.gradient(FH,1/FS))));_ab=np.clip((38-_fs3)/12,0,1)*np.clip((nd.gaussian_filter(_fs3,6)-35)/15,0,1)
FH=np.where(_vin,FH+_wf*nd.gaussian_filter(_ab,1.2)*(0.22+0.08*_ff(5,213)),FB)
# t57u: Schutthalde am Fuss als echte Kegel (nur unten, glatt) [A]
_fz2=_wf*np.clip((0.30-_tl0)/0.2,0,1);_sh=nd.gaussian_filter(FH,10)-0.25+0.5*_ff(14,203)*0.3;FH=np.where(_vin,np.maximum(FH,FH*(1-_fz2)+np.maximum(FH,_sh)*_fz2),FB)
_ap=nd.gaussian_filter(FH,8)-0.15;_fz=_wf*np.clip((0.28-_tl0)/0.18,0,1);FH=np.where(_vin,np.maximum(FH,_fz*_ap+(1-_fz)*FH),FB)   # nur am Wandfuss fuellen (t54u-D, vorher ganze Wand -> Relief weg)   # Schuttfuss/Kehlen fuellen
import runde_o_t67u as RO;FH,BR_T67U=RO.bandrand_weich(FH,_FB0_T67U,_vin,breite=int(os.environ.get('BANDRAND_B','12')));print('bandrand_t67u',BR_T67U)   # t67u O5: keine Rechteck-Stufen am Feinbandrand [A]
import runde_o_t67u as RO;FH,ENTSP_T67U=RO.entspitzen(FH,FB,_vin);FH=np.where(_vin,FH,FB);FH,NK_T67U=RO.nadel_kappen(FH,_vin);print('entspitzen_t67u',ENTSP_T67U,NK_T67U)   # t67u Runde O3: keine Nadeln/Trichter [A]
FH,ZF_T67U=RO.zacken_fein(FH,_vin);FH=np.where(_vin,FH,FB);print('zackenfein_t67u',ZF_T67U)   # t67u O9b: Restzacken Feinband [A]
def keile_fein(FH,vin,T=0.6,K=0.4):   # O9 K3 [F]: 1-Ecken-breite Kerben/Grate (0,25 m breit, >0,6 m tief) quer zur Wand = Keile -> auf 40 % Tiefe, 2 Ecken breit; breitere Rinnen/Rippen bleiben [A]
    n=0;F=FH.copy()
    for it in range(3):
        for ax in (0,1):
            a=np.roll(F,1,ax);b=np.roll(F,-1,ax);m=(a+b)/2;lo=np.minimum(a,b);hi=np.maximum(a,b)
            k=vin&((F<lo-T)|(F>hi+T));k[0]=k[-1]=k[:,0]=k[:,-1]=False
            F=np.where(k,m+K*(F-m),F);n+=int(k.sum())
    return F,n
def messergrate_fein(FH,vin,T=0.3,K=0.5):   # O10 L2 [F]: 1-Ecken-Messergrate/-kerben (beidseitig >0,3 m auf 0,25 m, auch diagonal) erzeugen Faltdreiecke (Nachbarnormalen gegenlaeufig) = dunkle Haarlinien -> Hoehe zur Haelfte Richtung Nachbarmittel [A]
    n=0;F=FH.copy();vin2=nd.binary_erosion(vin,iterations=2)   # O11 M1: Bandrand (2 Ecken) nicht anfassen, sonst Stufe zum Grobnetz [A]
   
    for it in range(3):
        for sh in ((1,0),(0,1),(1,1),(1,-1)):
            a=np.roll(F,sh,(0,1));b=np.roll(F,(-sh[0],-sh[1]),(0,1));m=(a+b)/2;lo=np.minimum(a,b);hi=np.maximum(a,b)
            k=vin2&((F<lo-T)|(F>hi+T));k[0]=k[-1]=k[:,0]=k[:,-1]=False
            F=np.where(k,m+K*(F-m),F);n+=int(k.sum())
    return F,n
FH,KF_O9=keile_fein(FH,_vin);FH,KF_O10=messergrate_fein(FH,_vin);print('messergrate_o10',KF_O10);FH=np.where(_vin,FH,FB);print('keile_o9',KF_O9)
# Felsfarben je Schicht (grau/ocker/dunkel/hell) + Schnee auf Absaetzen und in Rinnen [A]
_PAL=np.array([[0.96,0.98,1.04],[0.70,0.71,0.77],[1.10,1.10,1.13],[0.84,0.85,0.90],[1.08,0.98,0.84]])   # Runde D: grau/dunkelgrau, ocker sparsam (Index 4, selten) [A]
_li=(np.mod(_lk*7+np.floor(2*_ff(80,77)),4)).astype(int);_li=np.where(_ff(30,78)>1.3,4,_li);_tint=_PAL[_li]*(0.92+0.08*_ff(6,79))[...,None]
_tint*=np.where(_rib<-0.25,0.85,1.0)[...,None]                                                                          # dunkle Rinnen
_fsl2=np.degrees(np.arctan(np.hypot(*np.gradient(FH,1/FS))));_lap=nd.laplace(nd.gaussian_filter(FH,2))
_snow=np.clip((42-_fsl2)/8,0,1)+np.clip(_lap*4-0.2,0,0.5)*np.clip((62-_fsl2)/12,0,1)+0.8*np.clip(-_rib-0.35,0,1)*np.clip((66-_fsl2)/14,0,1)   # Runde D: Schnee in Rinnen [A]
_snow=np.clip(nd.gaussian_filter(_snow,0.6)*_wf*_sf,0,1)
_fv=np.argwhere(_qb.any() and np.ones(1,bool))  # Platzhalter
_used=np.zeros((FYn,FXn),bool);_used[:-1,:-1]|=_qb;_used[1:,:-1]|=_qb;_used[:-1,1:]|=_qb;_used[1:,1:]|=_qb
_vid=np.flatnonzero(_used.ravel()).astype(np.uint32)
_vcf=np.stack([nd.map_coordinates(VC.reshape(GY,GX,3)[...,c].astype(float),[_gy.ravel()[_vid],_gx.ravel()[_vid]],order=1) for c in range(3)],1)
FW={'fs':FS,'band':base64.b64encode(np.flatnonzero(BAND.ravel()).astype(np.uint32).tobytes()).decode(),'vid':base64.b64encode(_vid.tobytes()).decode(),
    'h':base64.b64encode(FH.ravel()[_vid].astype(np.float32).tobytes()).decode(),'c':base64.b64encode(np.clip(_vcf,0,255).astype(np.uint8).tobytes()).decode(),
    't':base64.b64encode(np.clip(_tint.reshape(-1,3)[_vid]*128,0,255).astype(np.uint8).tobytes()).decode(),'s':base64.b64encode(np.clip(_snow.ravel()[_vid]*255,0,255).astype(np.uint8).tobytes()).decode()}
# Runde F: Ueberhaenge/Felsnasen als zusaetzliche Fels-Meshes (Hoehenfeld kann nicht ueberhaengen) [A]
def _ico(n):
    t=(1+5**.5)/2;V=[(-1,t,0),(1,t,0),(-1,-t,0),(1,-t,0),(0,-1,t),(0,1,t),(0,-1,-t),(0,1,-t),(t,0,-1),(t,0,1),(-t,0,-1),(-t,0,1)]
    F=[(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),(3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),(4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)]
    V=[np.array(v,float)/np.linalg.norm(v) for v in V]
    for _ in range(n):
        C={};F2=[]
        def mid(a,b):
            k=(min(a,b),max(a,b))
            if k not in C:m=V[a]+V[b];V.append(m/np.linalg.norm(m));C[k]=len(V)-1
            return C[k]
        for a,b,c in F:ab,bc,ca=mid(a,b),mid(b,c),mid(c,a);F2+=[(a,ab,ca),(b,bc,ab),(c,ca,bc),(ab,bc,ca)]
        F=F2
    return np.array(V),np.array(F)
_IV,_IF=_ico(2)
_gyF,_gxF=np.gradient(nd.gaussian_filter(FH,3),1/FS)
_ovk=_vin&(_wf>0.85)&(_sf>0.7)&(_tl0>0.68)&(_tl0<0.9)&(np.hypot(_gyF,_gxF)>1.4)
_oc=np.argwhere(_ovk);_ro=np.random.default_rng(611);_ro.shuffle(_oc);_OP=[];_OI=[];_ON=0;_sel=[]
def _hat(x,z):return nd.map_coordinates(FH,[np.clip(z*FS,0,FYn-1),np.clip(x*FS,0,FXn-1)],order=1)
for q in _oc:
    if len(_sel)>=36:break
    if any((q[0]-s[0])**2+(q[1]-s[1])**2<70**2 for s in _sel):continue
    _sel.append(q);gy,gx=_gyF[q[0],q[1]],_gxF[q[0],q[1]];g=np.hypot(gx,gy);nx_,nz_=-gx/g,-gy/g   # bergab
    L=_ro.uniform(1.6,2.6);W=_ro.uniform(2.4,4.0);Hh=_ro.uniform(1.0,1.8);out=_ro.uniform(0.5,0.9)*L
    ph=_ro.uniform(0,6.3,(3,3));fr=_ro.uniform(1.5,3.5,3)
    v=_IV.copy();nz=sum(0.18/(k+1)*np.sin(fr[k]*(k+1)*(v@np.array([np.cos(ph[k,0]),np.sin(ph[k,1]),np.cos(ph[k,2])]))+ph[k,0]) for k in range(3))
    v=v*(1+nz)[:,None];v[:,1]=np.where(v[:,1]<0,v[:,1]*0.45,v[:,1])                                   # flache Unterseite = Nase
    x0,z0=q[1]/FS+nx_*out,q[0]/FS+nz_*out;y0=FH[q[0],q[1]]-0.35
    X=x0+v[:,0]*L*nx_-v[:,2]*W*nz_;Z=z0+v[:,0]*L*nz_+v[:,2]*W*nx_;Y=y0+v[:,1]*Hh
    ht=_hat(X,Z);Y=np.where(ht>y0,np.minimum(Y,ht+0.08),Y);Y=np.where(v[:,1]>0,np.minimum(Y,np.maximum(np.minimum(ht+0.08,y0+0.45),y0)),Y)   # Politur: Oberseite buendig mit Kante, keine Kissen                                              # hinten/oben ins Gelaende einbetten, kein Spalt
    _OP.append(np.stack([X,Y,Z],1));_OI.append(_IF+_ON);_ON+=len(v)
if _OP and os.environ.get('OV')=='1':   # Runde G: Nasen-Meshes aus (sahen wie Platten aus), Ueberhang-Wirkung per Gesims im Hoehenfeld [A]
    FW['ov']=base64.b64encode(np.concatenate(_OP).astype(np.float32).tobytes()).decode();FW['ovi']=base64.b64encode(np.concatenate(_OI).astype(np.uint32).tobytes()).decode()
print('ueberhaenge',len(_sel),'dreiecke',sum(len(i) for i in _OI))
_fsl=np.degrees(np.arctan(np.hypot(*np.gradient(FH,1/FS))))
FW_MESS={'band_zellen':int(BAND.sum()),'dreiecke_voll':int(BAND.sum()*FS*FS*2),'neigung_steilband_mittel':round(float(_fsl[_vin&(_sf>0.5)].mean()),1),
 'neigung_p10_p90':[round(float(np.percentile(_fsl[_vin&(_sf>0.5)],q)),1) for q in (10,90)],'versatz_max_m':round(float(FD.max()),2),'neigung_grob_mittel':round(float(np.degrees(np.arctan(np.hypot(*np.gradient(FB,1/FS))))[_vin&(_sf>0.5)].mean()),1)}
print('feinrelief',FW_MESS)
if os.environ.get('FW_NPZ'):np.savez_compressed(os.environ['FW_NPZ'],FH=FH.astype(np.float32),FB=FB.astype(np.float32),vin=_vin,tint=_tint.astype(np.float32),snow=_snow.astype(np.float32))   # t54u: Blender-Versuch [A]
# t59u: Baeume/Felsen/Findlinge/Steine/Geroell/Gras an neue Feinform anpassen (auf Boden, nicht im Fels, nicht schwebend) [A]
_fsP=np.degrees(np.arctan(np.hypot(*np.gradient(FH,1/FS))));_vinP=_vin&(_wf>0.02)
_ovc=[(float(p[:,0].mean()),float(p[:,2].mean()),float(np.ptp(p[:,0])/2+np.ptp(p[:,2])/2)/2+0.5) for p in _OP] if os.environ.get('OV')=='1' else []
PASS={}
for _k,_lim in (('baeume',35),('felsen',60),('findlinge',45),('steine',50),('geroell',55),('gras',40)):
    _L=locals().get(_k);vor=[0,0,0];nach=[0,0,0]
    if not _L:continue
    for o in _L:
        fx_,fz_=o[0]*FS,o[2]*FS;iy,ix=int(round(fz_)),int(round(fx_))
        if not(0<=iy<FYn and 0<=ix<FXn) or not _vinP[iy,ix]:continue
        h=float(nd.map_coordinates(FH,[[fz_],[fx_]],order=1)[0]);ov=any((o[0]-a)**2+(o[2]-b)**2<r*r for a,b,r in _ovc)
        vor[0]+=o[1]>h+0.25;vor[1]+=o[1]<h-0.25;vor[2]+=(_fsP[iy,ix]>_lim)or ov
        if _fsP[iy,ix]>_lim or ov:      # auf naechste flache Feinstelle (<=3 m) ausserhalb der Nasen ruecken
            y0_,x0_=max(iy-12,0),max(ix-12,0);w=_fsP[y0_:iy+13,x0_:ix+13];ok=(w<=_lim)&_vinP[y0_:iy+13,x0_:ix+13]
            if ok.any():
                c=np.argwhere(ok);c=c[np.argsort((c[:,0]+y0_-iy)**2+(c[:,1]+x0_-ix)**2)]
                for cc in c:
                    nx2,nz2=(cc[1]+x0_)/FS,(cc[0]+y0_)/FS
                    if not any((nx2-a)**2+(nz2-b)**2<r*r for a,b,r in _ovc):o[0],o[2]=round(nx2,2),round(nz2,2);break
            fx_,fz_=o[0]*FS,o[2]*FS;iy,ix=int(round(fz_)),int(round(fx_))
        o[1]=round(float(nd.map_coordinates(FH,[[fz_],[fx_]],order=1)[0]),2)
        nach[2]+=(_fsP[min(iy,FYn-1),min(ix,FXn-1)]>_lim) or any((o[0]-a)**2+(o[2]-b)**2<r*r for a,b,r in _ovc)
    PASS[_k]={'schwebend_vor':int(vor[0]),'versunken_vor':int(vor[1]),'steil_oder_nase_vor':int(vor[2]),'steil_oder_nase_nach':int(nach[2])}
print('platzierung',json.dumps(PASS))
json.dump(PASS,open('pruefung/platzierung_t59u.json','w'),indent=1)
WEGA=(np.clip(up(weg,0.6)*1.6,0,1)*255).astype(np.uint8)
# t61u Runde I: Wasserspiegel monoton, Bett nur fuer die Anzeige eingraben (Zellen/CSV/glb oben schon geschrieben, bleiben gleich) [A]
from fluss_t61u import fluss_monoton
_VBc=np.zeros((GY,GX),bool)
for _dj in range(RS+1):
    for _di in range(RS+1):_VBc[_dj:_dj+NY*RS:RS,_di:_di+NX*RS:RS]|=BAND
if os.environ.get('FDUMP'):np.savez_compressed(os.environ['FDUMP'],WV=WV,G=G,VB=_VBc,LEV=LEV_ROH)
WV_ALT=WV.copy();WV,G_ANZ,FLUSS_T61U=fluss_monoton(WV,G,_VBc,LEV_ROH);print('fluss_t61u',FLUSS_T61U)
from fluss_t62u import ufer_glaetten,fluss_kaskade
WV,G_ANZ,KASK_T62U=fluss_kaskade(WV_ALT,G,_VBc);print('kaskade_t62u',KASK_T62U)   # t62u ersetzt den t61u-Spiegel (6-9 m Grabung) [A]
WV,G_ANZ,UFER_T62U=ufer_glaetten(WV,G,G_ANZ,_VBc);print('ufer_t62u',UFER_T62U)
from fluss_k import spiegel_monoton
WV,G_ANZ,MONO_T63U=spiegel_monoton(WV,G_ANZ,_VBc);print('spiegel_t63u',MONO_T63U)
from fluss_k import gefaelle_flach
WV,G_ANZ,FLACH_T63U=gefaelle_flach(WV,G_ANZ);print('flach_t63u',FLACH_T63U)   # t63u: Suedfluss leichtes Gefaelle [A]   # t63u Runde K: streng fallend, Becken flach, Stufen <= ~1 m [A]
def stummel_runden(WV,GA):   # t64u K9: Suedfluss-Stichgraben x64-68 z252-263 war kastenfoermig (gerader Kanal, 0,35 m Kastenprofil, gerade abgeschnittener Kopf) -> Kopf verjuengt, Breite schwankt, U-Profil, Spiegel faellt zur Muendung [A]
    WV=WV.copy();GA=GA.copy();j0,j1,i0,i1=500,527,132,152
    J,I=np.mgrid[j0:j1,i0:i1];w0=WV[j0:j1,i0:i1]>-900;w0[J>=523]=False
    jj,ii=J[w0].astype(float),I[w0].astype(float);A=np.polyfit(jj,ii,1)   # Mittellinie i=A0*j+A1
    t=(J-jj.min())/(jj.max()-jj.min());lat=np.abs(I-(A[0]*J+A[1])-1.3*np.sin(t*5.5)*np.clip(t*3,0,1)*np.clip((1-t)*4,0,1))/np.sqrt(1+A[0]**2)   # leichte Kruemmung, Muendung unveraendert
    lv=np.polyfit(jj,WV[j0:j1,i0:i1][w0],1);LV=np.minimum(lv[0]*J+lv[1],lv[0]*jj.min()+lv[1])
    hw=0.4+2.3*np.clip(t/0.45,0,1)**0.6*(1+0.16*np.sin(t*9.0)+0.08*np.sin(t*23.0))
    w1=(lat<hw)&(J<523)&(J>=jj.min()-1)
    rem=w0&~w1;add=w1&~w0;st={'entfernt':int(rem.sum()),'neu':int(add.sum())}
    sw=WV[j0:j1,i0:i1];sg=GA[j0:j1,i0:i1]
    sw[rem]=-999;sw[w1]=LV[w1]
    rel=np.clip(lat/np.maximum(hw,0.5),0,1.5)
    bed=LV-0.05-0.32*np.clip(1-rel**2,0,1)*np.clip(t/0.3,0.25,1)
    sg[w1]=np.minimum(sg[w1],bed[w1]) if False else bed[w1]
    ring=(~w1)&(lat<hw+3.0)&(J<525)&(J>=jj.min()-6)
    bank=LV+0.05+0.12*np.clip(lat-hw,0,3)
    sg[ring]=np.where(sg[ring]<bank[ring],bank[ring],sg[ring])
    st['spiegel_kopf']=round(float(LV.max()),3);st['spiegel_muendung']=round(float(LV[w1].min()),3)
    return WV,GA,st
WV,G_ANZ,STUMMEL_T64U=stummel_runden(WV,G_ANZ);print('stummel_t64u',STUMMEL_T64U)
def schlucht_breiter(WV,GA):   # t64u K9: Schluchtwasser x210-227 z229-245 nur 1-1,5 m Streifen -> bis 2 Zellen in flachen Schluchtboden ausdehnen (Spiegel = kleinster Nachbarspiegel, nie hoeher) [A]
    WV=WV.copy();GA=GA.copy();j0,j1,i0,i1=458,492,425,465;n=0
    for it in range(2):
        sw=WV[j0:j1,i0:i1];sg=GA[j0:j1,i0:i1];w=sw>-900
        nmin=-nd.grey_erosion(np.where(w,-sw,-1e9),size=3)   # dummy
        lo=nd.minimum_filter(np.where(w,sw,1e9),size=3)
        cand=(~w)&(lo<1e8)&(sg<lo+0.6)
        sw[cand]=lo[cand];cg=cand&~_VBc[j0:j1,i0:i1];sg[cg]=np.minimum(sg[cg],lo[cg]-0.12);n+=int(cand.sum())   # t64u Le: Boden nicht an Feinband-Ecken absenken (sonst Spalt 0,33 m bei 216/240) [S]
    return WV,GA,{'neu_wasser':n}
WV,G_ANZ,SCHLUCHT_T64U=schlucht_breiter(WV,G_ANZ);print('schlucht_t64u',SCHLUCHT_T64U)
_wu=(WV>-900)&(WV<G_ANZ);WV=np.where(_wu,np.float32(-999.0),WV).astype(WV.dtype);SCHLUCHT_T64U['wv_unter_boden_entfernt']=int(_wu.sum());print('wv_unter_t64u',int(_wu.sum()))   # t64u Le: verdeckte Wasserecken (Spiegel unter Boden) raus [S]
import runde_m_t65u as RM;WV,G_ANZ,LUECKE_T65U=RM.fluss_luecken(WV,G_ANZ,_VBc);print('luecke_t65u',LUECKE_T65U);WV,LUECKE_T65U['tuempel']=RM.tuempel_eben(WV,G_ANZ);WV,LUECKE_T65U['mulden']=RM.mini_senken(WV);print('mulden_t65u',LUECKE_T65U['tuempel'],LUECKE_T65U['mulden'])   # t65u Runde M3: Fluss lueckenlos bis Auslass [S]
import runde_o_t67u as RO;WV,G_ANZ,RAND_T67U=RO.rand_oeffnen(WV,G_ANZ);print('rand_t67u',RAND_T67U)   # t67u Runde O: Flussarme bis Kartenrand offen [A]
G_ANZ=(G_ANZ+np.where(WV>-900,0,G_SP_T67U-G)).astype(G_ANZ.dtype);G_ANZ,GSP_T67U=RO.grob_entspitzen(G_ANZ,WV,BAND,RS);print('grobspitzen_t67u',GSP_T67U)   # t67u O7: Nadeln im Grobnetz ausserhalb Feinband [F] [A]
_m5=nd.median_filter(G_ANZ,5);_fp=np.ones((3,3),bool);_fp[1,1]=0;_nb=nd.maximum_filter(G_ANZ,footprint=_fp);_zs=(G_ANZ-_m5>1.5)&(G_ANZ-_nb>0.5)&_mk;G_ANZ=np.where(_zs,np.maximum(_nb,_m5+0.5),G_ANZ).astype(G_ANZ.dtype);print('einzelzahn_t67u',int(_zs.sum()))   # t67u O9: Einzelzaehne Grobnetz (105|47) [F] [A]
def ufer_weich(GA,WV):   # O9 Nachlauf: Ufer-Treppen glaetten. Nur Boden-Hoehen an Land-Ecken bis 2 m vom Wasser, nicht im Feinband/an Feinband-Ecken/Wegen; Ufer bleibt ueber dem Spiegel [A]
    w=WV>-900;G0=GA.astype(float)
    i1=np.where(w,0,1);ds=nd.distance_transform_edt(i1)
    k=(~w)&(ds<=4)&_mk&~nd.binary_dilation(~_mk,iterations=2)&~nd.binary_dilation(_VBc,iterations=2)&(WEGA.reshape(GA.shape)<20)
    gw=np.clip(1.0-(ds-1)/4.0,0,1)*k
    wvm=nd.maximum_filter(np.where(w,WV,-1e9),3)   # hoechster Nachbar-Spiegel
    G1=G0.copy()
    for _ in range(4):
        B=nd.gaussian_filter(G1,1.0);G1=np.where(k,np.clip(G1+(B-G1)*gw,G0-0.4,G0+0.4),G1)
        G1=np.where(k&(wvm>-1e8),np.maximum(G1,wvm+0.03),G1)
    d=G1-G0;return G1.astype(GA.dtype),{'ecken':int(k.sum()),'max_aenderung_m':round(float(np.abs(d).max()),3),'mittel_m':round(float(np.abs(d[k]).mean()),3)}
G_ANZ,UFER_O9=ufer_weich(G_ANZ,WV);print('ufer_o9',UFER_O9)
_fp8=np.ones((3,3),bool);_fp8[1,1]=0;_wnb=nd.minimum_filter(np.where(WV>-900,WV,1e9),footprint=_fp8);_ein=(WV>-900)&(_wnb<1e8)&(WV<_wnb-0.01)&(nd.maximum_filter(np.where(WV>-900,WV,-1e9),footprint=_fp8)<WV+5);_ein&=(_wnb-WV<=0.1);WV=np.where(_ein,_wnb,WV).astype(WV.dtype);print('wasser_einzelsenken_o9',int(_ein.sum()))   # O9: einzelne Wasser-Senkenpunkte (Endstummel) auf Nachbarspiegel heben [S]
def ufer_profil(GA,WV,B=2.5,DM=1.0,TAN=0.70):   # O7 I2 [F]: Bett/Ufer glatt statt zellweise (letzte nasse Ecke 0,3-0,4 m tief, Land daneben ueber Spiegel = senkrechte Stufe). Nur Anzeige-Hoehen; WV/Zellen unveraendert. Signierter Abstand zur Kante (Kante = Mitte zw. nasser und trockener Ecke), Bett-Tiefe = DM*smoothstep(s/B) (nur anheben), Land <= Spiegel+0,02+0,7*s (35 Grad, nur absenken). Nicht im Feinband/Wegen [A]
    w=WV>-900;G0=GA.astype(float);h=1.0/RS
    si=(nd.distance_transform_edt(w)-0.5)*h;so=(nd.distance_transform_edt(~w)-0.5)*h
    if not os.environ.get('UFERPROFIL_ALT'):_sd=nd.gaussian_filter(si-so,4.0);si=np.where(w,np.maximum(_sd,0.25*h),si);so=np.where(~w,np.maximum(-_sd,0.25*h),so)   # O10 L3 [F]: Abstand aus geglaettetem signiertem Distanzfeld -> keine Zell-Terrassen am Ufer [A]
    _,(iy,ix)=nd.distance_transform_edt(~w,return_indices=True);wvn=WV[iy,ix].astype(float)
    frei=_mk&~nd.binary_dilation(_VBc,iterations=2)&(WEGA.reshape(GA.shape)<20)
    t=np.clip(si/B,0,1);sm=t*t*(3-2*t);bett=w&frei&(si<B)
    G1=np.where(bett,np.maximum(G0,WV-np.maximum(DM*sm,0.03)),G0)
    land=(~w)&frei&(so<B*1.5)
    G1=np.where(land,np.maximum(np.minimum(G1,wvn+0.02+TAN*so),np.minimum(G1,wvn+0.02)),G1)
    G1=np.where(land,np.maximum(G1,G0-1.0),G1)   # Fels/Wand: hoechstens 1 m absenken, dort steiler erlaubt
    d=G1-G0;return G1.astype(GA.dtype),{'bett_ecken':int((bett&(d>0.005)).sum()),'land_ecken':int((land&(d<-0.005)).sum()),'max_anhebung_m':round(float(d.max()),2),'max_absenkung_m':round(float(-d.min()),2)}
def _kontur_zus(w,add,rem):   # Wegnahmen, die ein Gewaesser zerteilen, zuruecknehmen
    S=np.ones((3,3));L0,_=nd.label(w|add,S)
    for it in range(6):
        W2=(w|add)&~rem;L2,n2=nd.label(W2,S)
        if n2==0:return rem
        sz=np.bincount(L2.ravel());own=np.zeros(n2+1,int);idx=np.flatnonzero(L2.ravel());own[L2.ravel()[idx]]=L0.ravel()[idx];best={}
        for k in range(1,n2+1):
            o=own[k]
            if o not in best or sz[k]>sz[best[o]]:best[o]=k
        keep=np.zeros(n2+1,bool);keep[list(best.values())]=True;keep[0]=True;bad=~keep[L2]
        if not bad.any():return rem
        rem=rem&~nd.binary_dilation(bad,iterations=3)
    return np.zeros_like(rem)
def kontur_glatt(GA,WV,SIG=4.0,HMAX=0.5):   # O9 K1 [F]: Wasserumriss aus geglaettetem Nassfeld (Gauss 2 m, Schwelle 0,5) statt Zell-Treppe. Nur Anzeige-Ecken (WV/G_ANZ), Zellspalten unveraendert. Zufuegen: nur bis 2 m neben Wasser und Boden <= Spiegel+0,5. Wegnehmen: nur Randecken neben breitem Wasser, kein Zerteilen. Nicht Feinband/Wege [A]
    w=WV>-900;bl=nd.gaussian_filter(w.astype(float),SIG);e=nd.distance_transform_edt(w)
    frei=_mk&~nd.binary_dilation(_VBc,iterations=2)&(WEGA.reshape(GA.shape)<20)
    _,(iy,ix)=nd.distance_transform_edt(~w,return_indices=True);wvn=WV[iy,ix]
    add=(~w)&frei&(bl>0.5)&(GA<=wvn+HMAX)&nd.binary_dilation(w,iterations=4)
    wmin=nd.minimum_filter(np.where(w,WV,1e9),9);wmax=nd.maximum_filter(np.where(w,WV,-1e9),9);add&=(wmax-wmin<0.1)   # nur an ruhigem Wasser (kein Stufen-Kurzschluss -> kein Bergauf)
    rem=_kontur_zus(w,add,w&frei&(bl<0.5)&(e<=3.01)&(nd.maximum_filter(e,9)>=4)&(wmax-wmin<0.1)&~(nd.maximum_filter(np.where(w,WV,-1e9),3)>WV+0.02))   # K1b: Rinnen-Ecken (tiefer als Nachbar) bleiben -> kein Bergauf-Umweg
    W2=(w|add)&~rem;_L,_n=nd.label(W2,np.ones((3,3)));_ok=np.zeros(_n+1,bool);_ok[np.unique(_L[w&W2])]=True;_ok[0]=True;add&=_ok[_L];W2=(w|add)&~rem   # K1b: neue Einzelecken ohne Altwasser verwerfen
    rd=lambda m:int(m[0].sum()+m[-1].sum()+m[:,0].sum()+m[:,-1].sum())
    WV2=np.where(add,wvn,np.where(rem,-999,WV)).astype(WV.dtype)
    return WV2,{'zu':int(add.sum()),'weg':int(rem.sum()),'komp_vor':int(nd.label(w,np.ones((3,3)))[1]),'komp_nach':int(nd.label(W2,np.ones((3,3)))[1]),'randecken_vor':rd(w),'randecken_nach':rd(W2)}
WV_ZELLE=WV.copy()
if os.environ.get('KDBG'):np.savez_compressed(os.environ['KDBG'],WV=WV,GA=G_ANZ,mk=_mk,vb=_VBc,wega=WEGA.reshape(G_ANZ.shape))
if not os.environ.get('KONTUR_ALT'):WV,KONTUR_K1=kontur_glatt(G_ANZ,WV);print('kontur_k1',KONTUR_K1)
if not os.environ.get('KONTUR_ALT') and not os.environ.get('UFERFARBE_ALT'):   # O9 K1b [F]: Uferband/Saum/Kies aus geglaetteter Wasserkontur (Ecken-Nassfeld) statt Zellmaske
    _wk=nd.gaussian_filter((WV>-900).astype(float),1.2);_wu=_wk
    VC=(np.clip(ufer_farbe(COL_BASIS,_wu),0,1)*255).astype(np.uint8);print('uferfarbe_k1b',float(np.abs(_wu-WU_ZELLE).mean()))
if not os.environ.get('UFER_ALT'):G_ANZ,UFER_O7=ufer_profil(G_ANZ,WV);print('ufer_o7',UFER_O7)
def bett_glatt(GA,WV,SIG=2.5,DMIN=0.05,DM=1.0,B=2.5,MAXD=0.5):   # O8 J2 [F]: Bett-Tiefe IM Wasser glatt (Gauss ueber nasse Ecken) statt zellweise Bloecke; WV unveraendert. Nur Anzeige.
    w=WV>-900;G0=GA.astype(float);h=1.0/RS;s=SIG/h
    frei=_mk&~nd.binary_dilation(_VBc,iterations=2)&(WEGA.reshape(GA.shape)<20)
    D=np.where(w,WV-G0,0.0);Dc=np.clip(D,0,None)
    Ds=nd.gaussian_filter(Dc*w,s)/np.maximum(nd.gaussian_filter(w.astype(float),s),1e-6)
    si=(nd.distance_transform_edt(w)-0.5)*h;t=np.clip(si/B,0,1);sm=t*t*(3-2*t)
    Dt=np.maximum(np.minimum(Ds,np.where(si<B,np.maximum(DM*sm,Ds*sm),Ds)),DMIN)
    Dt=np.clip(Dt,D-MAXD,D+MAXD);Dt=np.maximum(Dt,DMIN)
    m=w&frei;G1=np.where(m,WV-Dt,G0)
    neg=w&~m&(G1>WV-DMIN)&~nd.binary_dilation(_VBc,iterations=1)   # nasse Ecken mit Tiefe<5 cm ausserhalb frei (nicht am Feinband)
    G1=np.where(neg,WV-DMIN,G1)
    d=G1-G0;Dn=np.where(w,WV-G1,9)
    return G1.astype(GA.dtype),{'ecken':int((m&(np.abs(d)>0.005)).sum()),'neg_fix':int(neg.sum()),'max_hoch':round(float(d.max()),2),'max_tief':round(float(-d.min()),2),'tiefe_lt0_rest':int((w&(Dn<0)).sum()),'tiefe_lt5cm_rest':int((w&(Dn<0.049)).sum()),'tiefe_lt0_vorher':int((w&(D<0)).sum())}
if not os.environ.get('BETT_ALT'):G_ANZ,BETT_J2=bett_glatt(G_ANZ,WV);print('bett_j2',BETT_J2)
def vc_weich(VC,GA,WV,WEGA):   # t64u Runde L Boden: Vertexfarben im Flachland weichzeichnen (sigma 1,2 Ecken = 0,6 m) gegen blockige Gras/Erde/Schnee-Flecken; nicht an Wegen, Ufern, Hangkanten [A]
    C=VC.reshape(GA.shape+(3,)).astype(float);B=np.stack([nd.gaussian_filter(C[...,k],1.2) for k in range(3)],-1)
    gy,gx=np.gradient(GA.astype(float),0.5);sl=np.hypot(gx,gy)
    m=((sl<0.35)&(WEGA.reshape(GA.shape)<20)&(nd.distance_transform_edt(WV<=-900)>3)).astype(float);m=nd.gaussian_filter(m,1.0)
    N=C*(1-m[...,None])+B*m[...,None];out=np.clip(np.round(N),0,255).astype(np.uint8)
    return out.reshape(VC.shape),{'anteil':round(float((m>0.5).mean()),3),'farbaenderung_mittel':round(float(np.abs(N-C).mean()),2)}
VC,VCW_T64U=vc_weich(VC,G_ANZ,WV,WEGA);print('vcweich_t64u',VCW_T64U)
VC,VCF_T65U=RM.vc_flecken(VC,G_ANZ,WV);print('vcflecken_t65u',VCF_T65U)   # t65u Runde M1d [S]
def vc_ufer_weich(VC,GA,WV,WEGA):   # O9 Nachlauf: Uferfarben folgen sonst dem 1-m-Zellraster (Treppen/Saegezaehne am Wasser). Weichzeichnen bis 3 m vom Wasser, nicht auf Wegen [A]
    C=VC.reshape(GA.shape+(3,)).astype(float);B=np.stack([nd.gaussian_filter(C[...,k],1.6) for k in range(3)],-1)
    ds=nd.distance_transform_edt(WV<=-900);m=((ds<=6)&(WEGA.reshape(GA.shape)<20)).astype(float);m=nd.gaussian_filter(m,1.0)
    N=C*(1-m[...,None])+B*m[...,None];return np.clip(np.round(N),0,255).astype(np.uint8).reshape(VC.shape),{'anteil':round(float((m>0.5).mean()),3)}
VC,VCU_O9=vc_ufer_weich(VC,G_ANZ,WV,WEGA);print('vcufer_o9',VCU_O9)
import runde_o16 as R16;G_ANZ,VC,R16_W,RAMPE9_O16=R16.entfernen(G_ANZ,VC,WV,RAMPWEGE,RS);RAMPE9_O16['feinband']=R16.feinband(FW,G_ANZ,VC,R16_W,NX,RS);RAMPE9_O16['felsbloecke_raus']=R16.fels_raus(felsbloecke,R16_W,RS);print('rampe9_o16',RAMPE9_O16)   # O16 [F t77u]: rampe_9 + Ruecken 133|173 weg, nur Anzeige (G/CSV-Zellwerte bleiben) [A]
_WEG_G0=G_ANZ.reshape(GY,GX).astype(float).copy();_WEG_V0=np.frombuffer(base64.b64decode(FW['vid']),np.uint32).copy();_WEG_F0=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float).copy()   # O18h [F G1 Steinweg war in O17 besser]: Stand vor allen O18-Schritten merken
_wellen_snap('gb_vor_o18',G_ANZ)
def _wand_maske(thr=1.0):   # O18i: Felswand = Steilheit Stand vor O18 >thr (dh/dm), 1 m erweitert
    gy,gx=np.gradient(_WEG_G0*1.0,1.0/RS);m=np.hypot(gx,gy)>thr;return nd.binary_dilation(m,iterations=max(1,int(RS)))
if not os.environ.get('WAND_ALT'):   # O18i [F G1 Felswand blobbig, Konturen als echte Geometrie]: gipfel_rund/fein_gipfel (Messung WANDMESS: 0.93/0.56 m an Wand) nur ausserhalb Steilwand
    import runde_o18 as _R;_WW=np.clip(nd.distance_transform_edt(~_wand_maske())/RS,0,1)   # 0 in Wand, 1 ab 1 m Abstand
    _gr0,_fg0=_R.gipfel_rund,_R.fein_gipfel
    def _gr_w(G,*a,**k):
        G0=G.reshape(GY,GX).astype(float).copy();r=_gr0(G,*a,**k);n=r[0].reshape(GY,GX).astype(float);n=G0+(n-G0)*_WW;return (n.reshape(r[0].shape).astype(r[0].dtype),)+tuple(r[1:])
    def _fg_w(FW_,*a,**k):
        h0=np.frombuffer(base64.b64decode(FW_['h']),np.float32).astype(float).copy();r=_fg0(FW_,*a,**k);h1=np.frombuffer(base64.b64decode(FW_['h']),np.float32).astype(float)
        vid=np.frombuffer(base64.b64decode(FW_['vid']),np.uint32);wf=nd.map_coordinates(_WW,[vid//FXn/FS*RS,vid%FXn/FS*RS],order=1,mode='nearest')
        FW_['h']=base64.b64encode((h0+(h1-h0)*wf).astype(np.float32).tobytes()).decode();return r
    _R.gipfel_rund,_R.fein_gipfel=_gr_w,_fg_w
    def _gw(f):   # O18j [F Felswaende ohne Kanten]: Grob-Glaettungen (Messung o18j_wandrau grob 0.589->0.449; grob_entzacken 0.17+0.05 m, grob_wand_glatt 0.016, entstacheln 0.013 an Wand) nur ausserhalb Wand
        def g(G,*a,**k):
            G0=G.reshape(GY,GX).astype(float).copy();r=f(G,*a,**k);o=r[0];n=G0+(o.reshape(GY,GX).astype(float)-G0)*_WW;return (n.reshape(o.shape).astype(o.dtype),)+tuple(r[1:])
        return g
    if not os.environ.get('WANDJ_ALT'):
        for _n in ['grob_wand_glatt','entstacheln']:setattr(_R,_n,_gw(getattr(_R,_n)))
        _ge0=_R.grob_entzacken
        def _ge_w(G,WV_,RS_,**k):   # an Wand nur 3 Durchgaenge (echte Nadeln), ausserhalb volle 8 (sonst Grobzacken 7->48)
            o,st=_ge0(G,WV_,RS_,**k);l,_=_ge0(G,WV_,RS_,it=3);n=l.reshape(GY,GX).astype(float)*(1-_WW)+o.reshape(GY,GX).astype(float)*_WW;return n.reshape(o.shape).astype(o.dtype),st
        _R.grob_entzacken=_ge_w
if os.environ.get('WANDMESS'):   # O18i Diagnose: welche O18-Glaettung veraendert Wandpunkte
    import runde_o18 as _R;_WM=_wand_maske();_WMESS={}
    def _wrap(n,f):
        def g(*a,**k):
            G=a[0].reshape(GY,GX).astype(float).copy() if isinstance(a[0],np.ndarray) and a[0].size==GY*GX else None;h0=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float).copy()
            r=f(*a,**k);h1=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
            dg=0.0
            if G is not None:
                o=r[0] if isinstance(r,tuple) else r
                if isinstance(o,np.ndarray) and o.size==G.size: dg=float(np.abs(o.reshape(GY,GX)-G)[_WM].mean())
            dh=float(np.abs(h1-h0).mean()) if h1.size==h0.size else -1
            _WMESS[n]=(_WMESS.get(n,(0,0))[0]+dg,_WMESS.get(n,(0,0))[1]+dh);print('WANDMESS',n,round(dg,4),round(dh,4));return r
        return g
    for n in ['grob_wand_glatt','entstacheln','kaskade_glatt','gipfel_rund','naht_weich','fein_glatt','fein_gipfel','fein_entzacken','grob_entzacken','kante_bilateral','ufer_weich','ufer_boeschung']: setattr(_R,n,_wrap(n,getattr(_R,n)))
import os as _o18os
if not _o18os.environ.get('O18_AUS'):   # Runde O18 [F t83u/t85u/t86u/t87u]: Wasser ohne Fluss raus, Senken gefuellt, Spitzen/Zacken gerundet -- nur Anzeige [A]
    import runde_o18 as R18;G_ANZ,VC,WV,R18_W,O18_W=R18.wasser_raus(G_ANZ,VC,WV,fl,wa,RS);O18_W['feinband']=R16.feinband(FW,G_ANZ,VC,R18_W,NX,RS);G_ANZ,O18_G=R18.gelaende(G_ANZ,WV,WEGA,RS);O18_F=R18.feinband(FW,G_ANZ,WV,WEGA,NX,NY,RS);G_ANZ,WV,O18_T=R18.fluss_tiefer(G_ANZ,WV,WEGA,bruecken,FW,NX,NY,RS);G_ANZ,O18_GW=R18.grob_wand_glatt(G_ANZ,FW,WV,WEGA,NX,NY,RS);print('o18_grobwand',O18_GW);G_ANZ,O18_Z=R18.entstacheln(G_ANZ,FW,NX,NY,RS);print('o18_zacken',O18_Z);G_ANZ,WV,_kg=R18.kaskade_glatt(G_ANZ,WV,RS);print('o18_kaskade',_kg);G_ANZ,_gr=R18.gipfel_rund(G_ANZ,WV,WEGA,belegt,RS) if not os.environ.get('GIPFEL_ALT') else (G_ANZ,{});print('o18_gipfel_rund',_gr);_HSM=R18.haus_sockel_feld(haeuser,WV,GY,GX,RS);G_ANZ,_hs=R18.haus_sockel_grob(G_ANZ,_HSM);print('o18d_haus_sockel_grob',_hs);_be=R18.band_erweitern(FW,G_ANZ,VC,WV,WEGA,belegt,NX,NY,RS);
    if 'B' in _be:BAND=_be.pop('B');_vid=_be.pop('vid')
    print('o18_band_erweitert',_be);print('o18_fluss',O18_T);print('o18_wasser',{k:v for k,v in O18_W.items() if k!='liste'});print('o18_gelaende',O18_G);print('o18_feinband',O18_F)
    import json as _j18;_j18.dump({'wasser':O18_W,'gelaende':O18_G,'feinband':O18_F,'fluss':O18_T},open('pruefung/o18/aenderungen_o18.json','w'),indent=1)

def _anz_objekte():                                    # t62u: Objekte der Anzeige folgen dem eingegrabenen/aufgefuellten Boden, keine Baeume/Steine im Wasser
    dG=G_ANZ.astype(float)-G;st={}
    _WVM3=nd.maximum_filter(np.where(WV>-900,WV,-999.0),5);_WVMX=nd.maximum_filter(np.where(WV>-900,WV,-999.0),5);_gy,_gx=np.gradient(G_ANZ.astype(float),1/RS);_SLMX=nd.maximum_filter(np.degrees(np.arctan(np.hypot(_gx,_gy))),3)
    _WOK=WV>-900;_WS=np.where(_WOK,WV,G_ANZ+0.02)
    def _wflaeche(i,j):                     # t63u: Wasserflaeche genau wie main.js (Dreiecke a,c,d / a,d,b; trockene Ecken G+0,02), -999 wenn keine Wasserzelle
        i0=min(max(int(np.floor(i)),0),_WS.shape[1]-2);j0=min(max(int(np.floor(j)),0),_WS.shape[0]-2);u=i-i0;v=j-j0
        if not _WOK[j0:j0+2,i0:i0+2].any():return -999.0
        A,B,C,Dd=_WS[j0,i0],_WS[j0,i0+1],_WS[j0+1,i0],_WS[j0+1,i0+1]
        h=A+(Dd-C)*u+(C-A)*v if v>=u else A+(B-A)*u+(Dd-B)*v
        return float(h)
    for nm,L in(('baeume',baeume),('felsen',felsen),('findlinge',findlinge),('steine',steine),('geroell',geroell)):
        neu=[];v=0;w=0
        for o in L:
            j,i=o[2]*RS,o[0]*RS;d=float(nd.map_coordinates(dG,[[j],[i]],order=1,mode='nearest')[0]);wv=float(nd.map_coordinates(WV,[[j],[i]],order=0,mode='nearest')[0])
            if abs(d)>0.01:o=list(o);o[1]=round(o[1]+d,3);v+=1
            if wv>-900 and wv>o[1]+0.15*(o[3] if nm!='baeume' else 1):w+=1;continue
            if nm!='baeume' and (float(nd.map_coordinates(_WVM3,[[j],[i]],order=0,mode='nearest')[0])>o[1] or _wflaeche(i,j)>o[1]):st['stein_wasser3_entfernt_t63u']=st.get('stein_wasser3_entfernt_t63u',0)+1;continue   # t63u: kein Stein unter Wasserspiegel (5x5-Ecken: Wasserdreiecke reichen bis an Nachbarecken, wie Raycast) [A]
            if nm=='baeume':                       # t63u Runde K: kein Baum am Wasserrand (1 m Umkreis) oder auf Hang >45 Grad (Anzeige-Gelaende) [A]
                wn_=float(nd.map_coordinates(_WVMX,[[j],[i]],order=0,mode='nearest')[0]);sl_=float(nd.map_coordinates(_SLMX,[[j],[i]],order=0,mode='nearest')[0])
                if wn_>o[1]-0.3:st['baum_wasserrand_entfernt']=st.get('baum_wasserrand_entfernt',0)+1;continue
                if sl_>45:st['baum_steil_entfernt']=st.get('baum_steil_entfernt',0)+1;continue
            neu.append(o)
        L[:]=neu;st[nm]={'verschoben':v,'im_wasser_entfernt':w}
    return st
OBJ_T62U=_anz_objekte();print('objekte_t62u',OBJ_T62U)
OBJ_T65U=RM.objekte({'baeume':baeume,'felsen':felsen,'findlinge':findlinge,'steine':steine,'geroell':geroell},G_ANZ,WV,OV,haeuser,RAMPWEGE,bruecken,NX,NY);print('objekte_t65u',OBJ_T65U)   # t65u Runde M2 [S]
_DFREI=RO.frei_maske(OV,RAMPWEGE,bruecken,wege,NX,NY);WEGFREI_T67U=RO.wege_frei({'baeume':baeume,'felsen':felsen,'findlinge':findlinge,'steine':steine,'geroell':geroell},_DFREI);print('wegfrei_t67u',WEGFREI_T67U)   # t67u Runde O2: 1,5 m + Kronen-/Objektradius frei neben allen Wegen/Rampen/Bruecken/Plaetzen [A]
_,STRAHL_T65U=RM.strahl_hoehe({'baeume':baeume,'felsen':felsen,'findlinge':findlinge,'steine':steine,'geroell':geroell});print('strahl_t65u',STRAHL_T65U)   # t65u M2: Hoehe = Viewer-Raycast [S]
def _bandnaht_j1():   # O8 J1: Feinband-Randpunkte = Grobnetz (G_ANZ wurde nach FW noch geaendert) [S]
    fy=_vid//FXn;fx=_vid%FXn;BP=np.pad(BAND,1);x=fx//FS;y=fy//FS
    b=lambda xx,yy:BP[np.clip(yy,-1,NY)+1,np.clip(xx,-1,NX)+1]
    hz=(fy%FS==0)&~(b(x,y-1)&b(x,y)&b(x-(fx%FS==0),y-1)&b(x-(fx%FS==0),y))
    vt=(fx%FS==0)&~(b(x-1,y)&b(x,y)&b(x-1,y-(fy%FS==0))&b(x,y-(fy%FS==0)))
    m=hz|vt;h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float).copy()
    gi=nd.map_coordinates(G_ANZ.reshape(GY,GX).astype(float),[fy[m]/FS*RS,fx[m]/FS*RS],order=1,mode='nearest')
    d=np.abs(h[m]-gi);h[m]=gi;FW['h']=base64.b64encode(h.astype(np.float32).tobytes()).decode()
    return {'punkte':int(m.sum()),'geaendert_gt_1mm':int((d>1e-3).sum()),'max_m':round(float(d.max()),3)}
if not os.environ.get('NAHT_ALT'):(print('naht_weich_o18',R18.naht_weich(FW,G_ANZ.reshape(GY,GX),BAND,NX,NY,RS)),print('fein_glatt_o18',R18.fein_glatt(FW,BAND,NX,NY,thr=0.22,it=14)),print('fein_gipfel_o18',R18.fein_gipfel(FW,BAND,NX,NY))) if not os.environ.get('O18_AUS') else None;print('bandnaht_j1',_bandnaht_j1())   # O18: Randversatz weich nach innen, dann Rand exakt [A]
_SHC0=json.load(open('pruefung/strahl_hoehe_t65u.json')) if os.path.exists('pruefung/strahl_hoehe_t65u.json') else {};RAMPE9_O16['objekte_feinband']=R16.objekte_feinband({_k:[o for o in _L if f"{o[0]:.3f}|{o[2]:.3f}" not in _SHC0.get(_k,{})] for _k,_L in (('baeume',baeume),('felsen',felsen),('findlinge',findlinge),('steine',steine),('geroell',geroell))},FW,NX,NY)   # O18t: Raycast-gesetzte Objekte nicht nachtraeglich absenken [A];RAMPE9_O16['geroell_raus']=R16.geroell_raus(geroell,R16_W,RS);print('objfein_o16',RAMPE9_O16['objekte_feinband']);print('geroell_o16',RAMPE9_O16['geroell_raus'])
if os.environ.get('FW_NPZ'):R16.npz_nach(os.environ['FW_NPZ'],FW,G_ANZ,R16_W,NX,NY,RS)   # O16: Fehlerzaehler sieht den Endstand [A]   # O16 R2: Schwebende im Feinband absenken [A]
if os.environ.get('DIAG'):np.savez_compressed(os.environ['DIAG'],WV=WV,G=G_ANZ,WV_ALT=WV_ALT,G_ALT=G,wa=wa,fl=fl.astype(str))
_wellen_snap('gb_nach_o18kern',G_ANZ)
G_ANZ,_uw=R18.ufer_weich(FW,G_ANZ,WV,NX,NY,RS);print('o18d_ufer_weich',_uw);G_ANZ,_ub=R18.ufer_boeschung(FW,G_ANZ,WV,NX,NY,RS);print('o18d_ufer_boeschung',_ub);G_ANZ,_hs2=R18.haus_sockel_grob(G_ANZ,_HSM);print('o18d_haus_sockel_fein',R18.haus_sockel_fein(FW,_HSM,NX,RS));print('o18d_entzacken',R18.fein_entzacken(FW,NX,NY));G_ANZ,_ge=R18.grob_entzacken(G_ANZ,WV,RS);print('o18e_grob_entzacken',_ge);print('o18d_farbe_weich',R18.farbe_weich(VC,FW,RS,NX,NY))   # O18d A1 [A]
G_ANZ,WV,_ft=R18.fluss_einschnitt(FW,G_ANZ,WV,NX,NY,RS);print('o18d_fluss_einschnitt',_ft);print('o18f_kante',R18.kante_bilateral(FW,NX,NY,it=2));print('o18e_entzacken2',R18.fein_entzacken(FW,NX,NY));G_ANZ,_ge2=R18.grob_entzacken(G_ANZ,WV,RS);print('o18e_grob_entzacken2',_ge2)
def _wand_neu():   # O18p [F Wandform neu]: relief_wand.py auf Wandmaske (Zellsteilheit vor O18 >1.0, +1 m), nicht Weg/Rampe +-4 m, nicht Wasser +-2 m; Grob + Feinband punktweise
    import relief_wand as RW
    M=_wand_maske();W=WEGA.reshape(GY,GX)>20
    for r in RAMPWEGE:
        r=np.asarray(r,float);L=np.r_[0,np.cumsum(np.hypot(*np.diff(r,axis=0).T))];t=np.arange(0,L[-1]+1e-6,0.25);W[np.clip((np.interp(t,L,r[:,1])*RS).astype(int),0,GY-1),np.clip((np.interp(t,L,r[:,0])*RS).astype(int),0,GX-1)]=True
    frei=(nd.distance_transform_edt(~W)/RS>4)&(nd.distance_transform_edt(WV.reshape(GY,GX)<=-900)/RS>2)
    GA=G_ANZ.reshape(GY,GX).astype(float);F=RW.vorbereiten(GA,M,RS,frei);nG,d=RW.verformen_grob(F,GA)
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fz=vid//FXn/FS;fx=vid%FXn/FS
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float);hn=RW.verformen_fein(F,fx,fz,h);FW['h']=base64.b64encode(hn.astype(np.float32).tobytes()).decode()
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'grob':int((np.abs(d)>0.01).sum()),'fein':int((np.abs(hn-h)>0.01).sum()),'max':round(float(np.abs(d).max()),2)}
def _wand_zurueck():   # O18o [F G1 "geschmolzener Vorhang", D1 Felsbaender verwaschen]: Wandzone (O17-Wandmaske, +0.5 m) Grob+Fein auf O17-Form (f65298b) zurueck, 1 m Auslauf; nicht Wege/Rampen +-4 m, nicht Wasser +-2 m
    M=_wand_maske();W=WEGA.reshape(GY,GX)>20
    for r in RAMPWEGE:
        r=np.asarray(r,float);L=np.r_[0,np.cumsum(np.hypot(*np.diff(r,axis=0).T))];t=np.arange(0,L[-1]+1e-6,0.25);W[np.clip((np.interp(t,L,r[:,1])*RS).astype(int),0,GY-1),np.clip((np.interp(t,L,r[:,0])*RS).astype(int),0,GX-1)]=True
    frei=(nd.distance_transform_edt(~W)/RS>4)&(nd.distance_transform_edt(WV.reshape(GY,GX)<=-900)/RS>2)
    d=nd.distance_transform_edt(~M)/RS;w=np.clip(1-(d-0.5)/1.0,0,1)*frei
    GA=G_ANZ.reshape(GY,GX).astype(float);dG=_WEG_G0-GA;nG=GA+w*np.where(w>=0.999,dG,np.maximum(dG,0))   # O18o Versuch 3: im Auslauf nur anheben (keine O17-Fusssenken)
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fy=vid//FXn;fx=vid%FXn;wf=nd.map_coordinates(w,[fy/FS*RS,fx/FS*RS],order=1,mode='nearest')
    o=np.argsort(_WEG_V0);p=np.clip(np.searchsorted(_WEG_V0[o],vid),0,len(o)-1);hit=_WEG_V0[o][p]==vid;wf=wf*hit   # nur gleiche vid (sonst keine O17-Form)
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float);alt=np.where(hit,_WEG_F0[o][p],h);h=h+wf*np.where(wf>=0.999,alt-h,np.maximum(alt-h,0));FW['h']=base64.b64encode(h.astype(np.float32).tobytes()).decode()
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'grob_pkt':int((w>0).sum()),'fein_pkt':int((wf>0).sum())}
def _weg_zurueck():   # O18h: Wegbereich (WEGA>20, +-3 m voll, 2 m Auslauf, nicht <2 m am Wasser) auf O17-Stand (vor O18-Glaettungen) zurueck; Fein: gleiche vid -> alter Wert, neue vid -> alter Grobwert
    W=WEGA.reshape(GY,GX)>20;d=nd.distance_transform_edt(~W)/RS;w=np.clip(1-(d-3)/2,0,1)
    w=w*(nd.distance_transform_edt(WV.reshape(GY,GX)<=-900)/RS>2)
    GA=G_ANZ.reshape(GY,GX).astype(float);nG=GA*(1-w)+_WEG_G0*w
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fy=vid//FXn;fx=vid%FXn;wf=nd.map_coordinates(w,[fy/FS*RS,fx/FS*RS],order=1,mode='nearest')
    alt=nd.map_coordinates(_WEG_G0,[fy/FS*RS,fx/FS*RS],order=1,mode='nearest');o=np.argsort(_WEG_V0);p=np.clip(np.searchsorted(_WEG_V0[o],vid),0,len(o)-1);hit=_WEG_V0[o][p]==vid;alt[hit]=_WEG_F0[o][p][hit]
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float);h=h*(1-wf)+alt*wf;FW['h']=base64.b64encode(h.astype(np.float32).tobytes()).decode()
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'grob_pkt':int((w>0).sum()),'fein_pkt':int((wf>0).sum()),'fein_alt_vid':int(hit[wf>0].sum())}
def _weg_wulst():   # O18i [F G1 heller Wulst an Wegunterkante]: talseitig 0-2.5 m neben Weg Hoehe auf Linie Wegkante->Gelaende in 4 m deckeln (Grob+Fein)
    GA=G_ANZ.reshape(GY,GX).astype(float);W=WEGA.reshape(GY,GX)>20
    R=np.zeros((GY,GX),bool)   # nur Rampenwege (G1-Steinweg ist Rampe; WEGA-Dorfwege liessen Zacken steigen): Mittellinie verdichtet, Radius 1.5 m
    for P in RAMPWEGE:
        P=np.array(P,float)
        for p,q in zip(P[:-1],P[1:]):
            for t in np.linspace(0,1,int(np.hypot(*(q-p))*4)+2):
                x,y=(p+(q-p)*t)*RS;R[int(np.clip(round(y),0,GY-1)),int(np.clip(round(x),0,GX-1))]=True
    W=(nd.distance_transform_edt(~R)/RS<=1.5);d,(iy,ix)=nd.distance_transform_edt(~W,return_indices=True);d=d/RS
    yy,xx=np.mgrid[0:GY,0:GX];vy=yy-iy;vx=xx-ix;n=np.maximum(np.hypot(vy,vx),1e-6);hp=GA[iy,ix]
    s4=nd.map_coordinates(GA,[iy+vy/n*4*RS,ix+vx/n*4*RS],order=1,mode='nearest')
    tg=hp+0.02+(s4-hp)*np.clip(d,0,4)/4*(0 if os.environ.get('WULST_ALT') else 1);m=(d>0)&(d<=2.5)&(s4<hp-1.0)&(WV.reshape(GY,GX)<=-900)&(GA>tg+0.05)&(xx>=252*RS)&(xx<294*RS)&(yy<42*RS);ms=np.clip(nd.gaussian_filter(m.astype(float),1.5)*2,0,1);capf=np.where(m,tg,GA)   # O18j [F heller Streifen = flache Stufe unter Wegkante, Shader-Schnee nach |N.y|]: Ziel = Linie Wegkante->Gelaende 4 m (keine Simse)   # nur echter Buckel ueber Wegkante -> auf Kantenhoehe, weicher Uebergang   # nur Feld G1 (kartenweit stiegen Feinzacken 31->42/49)
    nG=GA-np.maximum(GA-nd.grey_dilation(np.where(m,capf,-1e4),size=3).clip(min=-1e3),0)*ms*(nd.grey_dilation(m,size=3));nG=np.where(np.isfinite(nG),nG,GA);k=int((nG<GA-0.01).sum())
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fy=vid//FXn/FS*RS;fx=vid%FXn/FS*RS
    cf=nd.map_coordinates(np.where(m,capf,nG),[fy,fx],order=1,mode='nearest');mf=nd.map_coordinates(ms,[fy,fx],order=1,mode='nearest')
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float);hn=h-np.maximum(h-cf,0)*mf;kf=int((hn<h-0.01).sum());FW['h']=base64.b64encode(hn.astype(np.float32).tobytes()).decode()
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'grob':k,'fein':kf}
def _weg_eben():   # O18k [F pt104u G1 Steinweg uneben/gewoelbt, kippt zur Seite; Messung rampe_1 quer 28.7 %]: Rampenwege +-1.5 m quer eben (2 % zur Bergseite), Laengsprofil Gauss 3 m, Auslauf 1.5-3.5 m smoothstep, nicht <2 m am Wasser; Grob+Fein
    from scipy.spatial import cKDTree
    GA=G_ANZ.reshape(GY,GX).astype(float);hf=lambda X,Z:nd.map_coordinates(GA,[np.asarray(Z)*RS,np.asarray(X)*RS],order=1,mode='nearest')
    P=[];T=[];HC=[];SG=[];Pl=[];Ll=[]
    for W in RAMPWEGE:
        W=np.array(W,float);L=np.r_[0,np.cumsum(np.hypot(*np.diff(W,axis=0).T))];t=np.arange(0,L[-1]+1e-6,0.25)
        p=np.stack([np.interp(t,L,W[:,0]),np.interp(t,L,W[:,1])],1);d=np.gradient(p,axis=0);d/=np.maximum(np.linalg.norm(d,axis=1,keepdims=True),1e-9);n=np.stack([-d[:,1],d[:,0]],1)
        hc=nd.gaussian_filter1d(hf(p[:,0],p[:,1]),12,mode='nearest');b=hf(p[:,0]+n[:,0]*1.5,p[:,1]+n[:,1]*1.5)-hf(p[:,0]-n[:,0]*1.5,p[:,1]-n[:,1]*1.5);sg=np.sign(nd.gaussian_filter1d(b,12,mode='nearest'))
        P.append(p);T.append(n);HC.append(hc);SG.append(sg);Pl.append(p);Ll.append(t)
    P=np.concatenate(P);T=np.concatenate(T);HC=np.concatenate(HC);SG=np.concatenate(SG);kd=cKDTree(P)
    if os.environ.get('KREUZ','0')!='0':   # O18r verworfen (R3 laengs 35->45, G6 +10):  [Gate R3 quer bis 101 %: Kreuzungen rampe_2/11, 3/5 und Kehre rampe_12 mit 2-4 m Abstand, nearest-Band springt]: Hoehenprofile an Kreuzungen/Kehren angleichen (Mittel), Korrektur laengs Gauss 4 m
        RI=np.concatenate([np.full(len(q),j) for j,q in enumerate(Pl)]);LL=np.concatenate(Ll);pr=kd.query_pairs(3.2,output_type='ndarray')
        pr=pr[(RI[pr[:,0]]!=RI[pr[:,1]])|(np.abs(LL[pr[:,0]]-LL[pr[:,1]])>8)];st=np.r_[0,np.cumsum([len(q) for q in Pl])]
        for _ in range(30):
            dl=np.zeros(len(P));cn=np.zeros(len(P));m=(HC[pr[:,0]]+HC[pr[:,1]])/2
            np.add.at(dl,pr[:,0],m-HC[pr[:,0]]);np.add.at(dl,pr[:,1],m-HC[pr[:,1]]);np.add.at(cn,pr[:,0],1);np.add.at(cn,pr[:,1],1)
            for j in range(len(Pl)):
                a,b=st[j],st[j+1];g=nd.gaussian_filter1d(cn[a:b],16,mode='nearest');HC[a:b]+=0.7*nd.gaussian_filter1d(dl[a:b],16,mode='nearest')/np.maximum(g,1e-3)*np.clip(g*40,0,1)
        print('o18r_kreuz_paare',len(pr),'rest_max',round(float(np.abs(HC[pr[:,0]]-HC[pr[:,1]]).max()),3) if len(pr) else 0)
    wasser=nd.distance_transform_edt(WV.reshape(GY,GX)<=-900)/RS
    WANDNEU=os.environ.get('RAMPENBAND','1')!='0';hfein=None;hgel=lambda X,Z:hf(X,Z) if hfein is None else hfein
    def ziel(X,Z):
        Q=np.stack([X,Z],1);dist,i=kd.query(Q,distance_upper_bound=(6.1 if WANDNEU else 3.6));ok=np.isfinite(dist);i=np.where(ok,i,0)
        s=((Q-P[i])*T[i]).sum(1);w=np.where(dist<=1.5,1.0,np.clip((3.5-dist)/2.0,0,1));w=w*w*(3-2*w)*ok
        if WANDNEU:   # O18p [F Rampe nicht Wurst]: Band 3 m eben (2 % Quergefaelle), ab 1.5 m gerade Boeschung 0.7 bis Gelaende, max 6 m
            zb=HC[i]-0.015*np.clip(s,-1.5,1.5)*SG[i];g0=hgel(X,Z);dist=np.where(ok,dist,99.0);dd=np.clip(dist-2.5,0,None);k=0.7*np.where(dd<1,dd*dd/2,dd-0.5)+1e-6;zz=np.where(ok,zb+k*np.tanh((g0-zb)/k),0.0)   # O18r V1: eben 2.5 m, Boeschung C1-weich (tanh statt clip), Fade 4.5-6 m
            fw=np.clip((6.0-np.nan_to_num(dist,posinf=99))/1.5,0,1);w=fw*fw*(3-2*fw)*ok*1.0*(nd.map_coordinates(wasser,[Z*RS,X*RS],order=0,mode='nearest')>2);return zz,w
        w=w*(nd.map_coordinates(wasser,[Z*RS,X*RS],order=0,mode='nearest')>2);return HC[i]-0.02*np.clip(s,-1.5,1.5)*SG[i],w
    yy,xx=np.mgrid[0:GY,0:GX];z,w=ziel(xx.ravel()/RS,yy.ravel()/RS);nG=GA.ravel()*(1-w)+z*w
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fz=vid//FXn/FS;fx=vid%FXn/FS;hfein=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float);zf,wf=ziel(fx,fz)
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float);h=h*(1-wf)+zf*wf;FW['h']=base64.b64encode(h.astype(np.float32).tobytes()).decode()
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'grob':int((w>0).sum()),'fein':int((wf>0).sum())}
def _senke_fuellen():   # O18r [Gate R5 loch 40: abflusslose Senken >1 m auf trockenem Land, meist am Wegrand/Wandfuss, von landschaft_final ausgenommen]: Senken auf 0.8 m Tiefe anheben (nur anheben), Rand weich Gauss 1 m; Grob+Fein
    from skimage.morphology import reconstruction
    GA=G_ANZ.reshape(GY,GX).astype(float);LAND=WV.reshape(GY,GX)<=-900
    sd=GA.copy();sd[1:-1,1:-1]=GA.max();t=reconstruction(sd,GA,method='erosion')-GA;t[~nd.binary_erosion(LAND,iterations=2*RS)]=0
    d=np.clip(t-0.95,0,None)   # V3: nur Grubenspitze auf 0.95 m Tiefe (V1 flach 0.8: G6 +16, V2 Kuppe: R3 +13, G5 +6)
    nG=GA+d
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fz=vid//FXn/FS;fx=vid%FXn/FS
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float);h=h+nd.map_coordinates(d,[fz*RS,fx*RS],order=1,mode='nearest');FW['h']=base64.b64encode(h.astype(np.float32).tobytes()).decode()
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'punkte':int((d>0.01).sum()),'max':round(float(d.max()),2)}
def _rand_auslauf():   # O18k [F t105u D1 Weg geht steil nach unten aus der Map; Messung rampe_11 Start 148.5|2.5, Kartenrand 14.0 -> 2.1 m Kerbe, O17 14.0]: Rampenende am Kartenrand -> Rand auf Randhoehe, linear auf Gelaende in 10 m, quer +-8 m voll, 8-14 m Auslauf; Grob+Fein
    GA=G_ANZ.reshape(GY,GX).astype(float);hf=lambda X,Z:nd.map_coordinates(GA,[np.asarray(Z)*RS,np.asarray(X)*RS],order=1,mode='nearest');E=[]
    for W in RAMPWEGE:
        for x,z in (W[0],W[-1]):
            for ax,v,lim in ((1,z,0),(1,z,NY),(0,x,0),(0,x,NX)):
                if abs(v-lim)<4:
                    u=x if ax==1 else z;q=np.arange(u-30,u+31,0.5);rr=hf(q,np.full_like(q,lim)) if ax==1 else hf(np.full_like(q,lim),q)
                    E.append((ax,lim,u,float(np.percentile(rr,80))))
    LW=(WV.reshape(GY,GX)<=-900);GAs=nd.grey_erosion(LW,size=(10*RS+1,10*RS+1))   # O18k [F t107u E1 sehr tiefes Loch: Nordrand 171-183 Kerbe bis -4.7 m, Plateau 14 m]: trockene Randkerben >2 m (kein Wasser in 5 m) ebenso auf Randhoehe
    for ax,lim,e,lw in ((1,0,GA[0],GAs[0]),(1,NY,GA[-1],GAs[-1]),(0,0,GA[:,0],GAs[:,0]),(0,NX,GA[:,-1],GAs[:,-1])):
        ref=nd.percentile_filter(e,80,size=60*RS);lab,n=nd.label((ref-e>2)&lw)
        for i in range(1,n+1):
            ii=np.nonzero(lab==i)[0];j=ii[(ref-e)[ii].argmax()];E.append((ax,lim,j/RS,float(ref[j])))
    def lift(X,Z,H):
        for ax,lim,u,eh in E:
            d=np.abs((Z if ax==1 else X)-lim);t=np.abs((X if ax==1 else Z)-u);a=np.clip(d/10,0,1)
            far=hf(X,np.full_like(X,lim+np.sign(0.5-lim/ (NY if ax==1 else NX))*10)) if ax==1 else hf(np.full_like(Z,lim+np.sign(0.5-lim/NX)*10),Z)
            ln=eh+(far-eh)*a;w=np.clip((14-t)/6,0,1);w=w*w*(3-2*w)*(d<10)
            H=H+np.maximum(ln-H,0)*w
        return H
    yy,xx=np.mgrid[0:GY,0:GX];nG=lift(xx.ravel()/RS,yy.ravel()/RS,GA.ravel())
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fz=vid//FXn/FS;fx=vid%FXn/FS
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float);h2=lift(fx,fz,h);FW['h']=base64.b64encode(h2.astype(np.float32).tobytes()).decode()
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'enden':[(a,l,round(u,1),round(e,2)) for a,l,u,e in E],'grob':int((nG>GA.ravel()+0.01).sum()),'fein':int((h2>h+0.01).sum())}
def _anschluss_gang():   # O18k [F t106u F1 Weg endet an Felswand, rampe_1 Ende 227.1|37.0 h0.4, 2 m weiter +2.0 m Fels; naechster Dorfweg 245|41]: Gelaende-Gang Rampenende -> Dorfweg, Polylinie 227.1|37.0 -> 232|40 -> 245|41, Hoehe linear Ende->Ziel, nur absenken bis 1.2 m ueber Linie, 1.5 m voll, 1.5-3.5 m Auslauf; Grob+Fein
    from scipy.spatial import cKDTree
    GA=G_ANZ.reshape(GY,GX).astype(float);hf=lambda X,Z:nd.map_coordinates(GA,[np.asarray(Z)*RS,np.asarray(X)*RS],order=1,mode='nearest')
    W=np.array([[227.1,37.0],[232.0,40.0],[245.0,41.0]]);L=np.r_[0,np.cumsum(np.hypot(*np.diff(W,axis=0).T))];t=np.arange(0,L[-1]+1e-6,0.25)
    P=np.stack([np.interp(t,L,W[:,0]),np.interp(t,L,W[:,1])],1);h0,h1=float(hf([W[0,0]],[W[0,1]])[0]),float(hf([W[-1,0]],[W[-1,1]])[0]);HL=h0+(h1-h0)*t/L[-1];kd=cKDTree(P)
    def f(X,Z,H):
        d,i=kd.query(np.stack([X,Z],1),distance_upper_bound=3.6);ok=np.isfinite(d);i=np.where(ok,i,0);w=np.where(d<=1.5,1.0,np.clip((3.5-d)/2,0,1));w=w*w*(3-2*w)*ok
        return H-np.maximum(H-HL[i]-0.05,0)*w
    yy,xx=np.mgrid[0:GY,0:GX];nG=f(xx.ravel()/RS,yy.ravel()/RS,GA.ravel())
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fz=vid//FXn/FS;fx=vid%FXn/FS;h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float);h2=f(fx,fz,h);FW['h']=base64.b64encode(h2.astype(np.float32).tobytes()).decode()
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'h_ende':round(h0,2),'h_ziel':round(h1,2),'grob':int((nG<GA.ravel()-0.01).sum()),'fein':int((h2<h-0.01).sum()),'max_ab':round(float((GA.ravel()-nG).max()),2)}
def _rand_weg():   # O18w [Gate R4_rand H2 332.5|64.5 dh -0.6 m]: Wegzellen <4 m am Kartenrand: Gelaende zwischen Weg und Rand linear auf Weghoehe (max 0.1 m/m), 1 m quer; nur Grob ausserhalb Feinband [A]
    GA=G_ANZ.reshape(GY,GX).astype(float);hf=lambda X,Z:float(nd.map_coordinates(GA,[[Z*RS],[X*RS]],order=1,mode='nearest')[0]);Wm=np.zeros((NY,NX),bool)
    for x,z in wege:Wm[z,x]=1
    Wm|=(WEGA.reshape(GY,GX)[:-1:RS,:-1:RS]>20);n=0;nG=GA.copy()
    for z,x in zip(*np.nonzero(Wm)):
        if not(x<=3 or z<=3 or x>=NX-4 or z>=NY-4):continue
        ex=0 if x<=3 else NX if x>=NX-4 else x+.5;ez=0 if z<=3 else NY if z>=NY-4 else z+.5;dist=max(np.hypot(ex-x-.5,ez-z-.5),0.5)
        h0=hf(x+.5,z+.5);he=hf(ex,ez)
        if abs(h0-he)/dist<=0.12:continue
        for t in np.linspace(0,1,int(dist*RS*2)+2):
            px,pz=x+.5+(ex-x-.5)*t,z+.5+(ez-z-.5)*t;hz=h0+np.clip(he-h0,-0.1*dist,0.1*dist)*t
            for o in (-1,0,1):
                qx,qz=(px+o/RS,pz) if ex!=x+.5 else (px,pz+o/RS);i,j=int(round(qx*RS)),int(round(qz*RS))
                if 0<=i<GX and 0<=j<GY:nG[j,i]=hz
        n+=1
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'zellen':n}
def _wand_mikro(A=float(os.environ.get('WMR','0.25'))):   # O18w [Gate G7b_wandkontur_rauheit 0.758<0.85]: Wand-Mikrorelief nur Wandmitte (Steilheit>1, 1 m eingerueckt, weicher Rand 1 m), ohne Fade-Glaettung, Grob+Fein aus EINEM Rauschfeld (0.25 m Raster, Gauss 0.35 m), deterministisch [A]
    GA=G_ANZ.reshape(GY,GX).astype(float);gy,gx=np.gradient(GA,1/RS);K=(np.hypot(gx,gy)>float(os.environ.get('WMK','0.8')))&(WV.reshape(GY,GX)<=-900)
    wk=np.clip(nd.gaussian_filter(K*1.0,RS*0.5)*2-0.5,0,1)*(np.hypot(gx,gy)>0.8)
    rng=np.random.default_rng(1811);N=nd.gaussian_filter(rng.standard_normal((FYn,FXn)),float(os.environ.get('WMS','1.4')));N/=N.std()
    nk=nd.map_coordinates(N,np.mgrid[0:GY,0:GX]*(FS/RS),order=1);nG=GA+A*nk*wk
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fy=vid//FXn;fx=vid%FXn;h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
    wf=nd.map_coordinates(wk,[fy/FS*RS,fx/FS*RS],order=1);h=h+A*N[fy,fx]*wf;FW['h']=base64.b64encode(h.astype(np.float32).tobytes()).decode()
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'ecken':int((wk>0).sum()),'A':A}
def _falten_glatt(SG=float(os.environ.get('FALTSG','1.0'))):   # O18w [Gate G6 Facetten >=3 m von Wand = echte Knicklinien, Bild g6eich/g6_fern_*]: Normalensprung dn>0.25 auf Hang 0.15-0.8, >=3 m von Wand, nicht Weg/Wasser: Gauss SG m, Grob+Fein [A]
    GA=G_ANZ.reshape(GY,GX).astype(float);gy,gx=np.gradient(GA,1/RS);st=np.hypot(gx,gy);W_=st>1.0
    n=np.stack([-gx,-gy,np.ones_like(GA)]);n/=np.linalg.norm(n,axis=0);dn=np.zeros_like(GA);dn[:,:-1]=sum(np.abs(np.diff(n[i],axis=1)) for i in range(3))
    LAND_=WV.reshape(GY,GX)<=-900;M=(dn>0.25)&(st>0.15)&(st<0.8)&LAND_&~nd.binary_dilation(W_,iterations=int(float(os.environ.get('FALTWD','1'))*RS))&~nd.binary_dilation(WEGA.reshape(GY,GX)>20,iterations=3*RS)
    w=np.clip(nd.gaussian_filter(nd.binary_dilation(M,iterations=RS)*1.0,RS*0.5)*1.5,0,1)*nd.binary_erosion(LAND_,iterations=RS)
    _yy,_xx=np.mgrid[0:GY,0:GX]
    for _r in RAMPWEGE:   # O18y [Gate R1_wand rampe_1/rampe_2 Enden]: Rampenenden 6 m frei lassen [A]
        _p=np.asarray([(q[0],q[1]) if not isinstance(q,dict) else (q['x'],q['z']) for q in (_r['punkte'] if isinstance(_r,dict) else _r)],float)
        for _e in (_p[0],_p[-1]):w[np.hypot(_xx/RS-_e[0],_yy/RS-_e[1])<float(os.environ.get('FALTRE','6'))]=0
    if os.environ.get('FALTFADE','0')!='0':w*=np.clip((nd.distance_transform_edt(~W_)/RS-1)/2,0,1)   # O18y: Gewicht 1->3 m Wandabstand einblenden (G7b_feld)
    S=nd.gaussian_filter(GA,SG*RS)
    _BX=[(74,96,149,186),(85,104,201,227),(313,322,223,239),(109,124,167,187),(108,123,112,125),(173,181,127,153),(84,101,133,149),(187,192,71,94)]   # O18y S2: 8 groesste G6-Cluster (single-link 8 m) nach b3b3b94
    LS=float(os.environ.get('FALTLS','0'))
    if LS>0:
        BM=np.zeros_like(GA,bool)
        for x0,x1,z0,z1 in _BX:BM[max(0,(z0-3)*RS):(z1+3)*RS,max(0,(x0-3)*RS):(x1+3)*RS]=1
        S=np.where(BM,nd.gaussian_filter(GA,LS*RS),S)
    nG=GA*(1-w)+S*w
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fy=vid//FXn;fx=vid%FXn;h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
    wf=nd.map_coordinates(w,[fy/FS*RS,fx/FS*RS],order=1);d=nd.map_coordinates(S-GA,[fy/FS*RS,fx/FS*RS],order=1)
    F=np.full((FYn,FXn),np.nan);F[fy,fx]=h;ok=np.isfinite(F);Sf=nd.gaussian_filter(np.where(ok,F,0),SG*FS)/np.maximum(nd.gaussian_filter(ok*1.0,SG*FS),1e-6)
    if LS>0:
        _Sl=nd.gaussian_filter(np.where(ok,F,0),LS*FS)/np.maximum(nd.gaussian_filter(ok*1.0,LS*FS),1e-6);_BF=nd.zoom(BM.astype(np.uint8),FS/RS,order=0);_B=np.zeros((FYn,FXn),bool);_B[:min(FYn,_BF.shape[0]),:min(FXn,_BF.shape[1])]=_BF[:FYn,:FXn]>0;Sf=np.where(_B,_Sl,Sf)
    h=h*(1-wf)+Sf[fy,fx]*wf;FW['h']=base64.b64encode(h.astype(np.float32).tobytes()).decode()
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'ecken':int((w>0.01).sum())}
def _hangwellen_glatt():   # O18w: Anzeige-Bandpass auf Haengen, Quellfeld G bleibt unveraendert; D2 bleibt Bytegleich
    A=float(os.environ.get('WELLEN','0.6'))
    if A==0:return G_ANZ,{'aus':True}
    if A not in (0.25,0.4,0.6):raise ValueError('WELLEN muss 0, 0.25, 0.4 oder 0.6 sein')
    GA=G_ANZ.reshape(GY,GX).astype(float);gy,gx=np.gradient(GA,1/RS);sl=np.hypot(gx,gy);W_=sl>1.0;LAND_=WV.reshape(GY,GX)<=-900
    wandabstand=nd.distance_transform_edt(~W_)/RS;weg=WEGA.reshape(GY,GX)>20
    for _r in RAMPWEGE:
        _p=np.asarray(_r,float);_L=np.r_[0,np.cumsum(np.hypot(*np.diff(_p,axis=0).T))];_t=np.arange(0,_L[-1]+1e-6,0.25)
        weg[np.clip((np.interp(_t,_L,_p[:,1])*RS).round().astype(int),0,GY-1),np.clip((np.interp(_t,_L,_p[:,0])*RS).round().astype(int),0,GX-1)]=True
    wegabstand=nd.distance_transform_edt(~weg)/RS
    M=(sl>0.15)&(sl<0.8)&LAND_&(wandabstand>=1.5)&(wegabstand>=3.0)
    # D2 ist feste Regressionsbasis; auch Feinbandpunkte dort bleiben unangetastet.
    M[43*RS:86*RS+1,126*RS:168*RS+1]=False
    w=np.clip(nd.distance_transform_edt(M)/2.0,0,1);w=w*w*(3-2*w)
    sm=nd.gaussian_filter(GA,0.75*RS);d=np.clip(sm-GA,-A,A)*w;nG=GA+d
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fy=vid//FXn;fx=vid%FXn
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float).copy()
    dh=nd.map_coordinates(d,[fy/FS*RS,fx/FS*RS],order=1,mode='nearest')
    xf=fx/FS;zf=fy/FS;d2=(xf>=126)&(xf<=168)&(zf>=43)&(zf<=86);dh[d2]=0
    h+=dh;FW['h']=base64.b64encode(h.astype(np.float32).tobytes()).decode()
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'ecken':int((np.abs(d)>1e-6).sum()),'max_m':round(float(np.abs(d).max()),3),'rms_m':round(float(np.sqrt(np.mean(d*d))),4)}
def _entspitzen(T=float(os.environ.get('SPITZE_T','0.38'))):   # O18w [Gate G2/G3/G2f/G3f]: Einzelpunkte >T ueber/unter 3x3-Nachbarmittel ausserhalb Wand+3 m auf Mittel+-T klemmen; Grob+Fein [A]
    GA=G_ANZ.reshape(GY,GX).astype(float);gy,gx=np.gradient(GA,1/RS);WD=nd.binary_dilation(np.hypot(gx,gy)>1.0,iterations=int(float(os.environ.get('SPITZE_WD','6'))*RS))
    def kl(A,okm,n=3):
        c=0
        for _ in range(n):
            nb=(nd.uniform_filter(np.where(okm,A,0),3)*9-A*okm)/np.maximum(nd.uniform_filter(okm*1.0,3)*9-okm,1);d=(A-nb)*okm;m=np.abs(d)>T;c+=int(m.sum());A=np.where(m,nb+np.sign(d)*T*0.9,A)
        return A,c
    LAND=WV.reshape(GY,GX)<=-900;nG,cg=kl(GA,~WD&~LAND)
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
    F=np.full((FYn,FXn),np.nan);F[vid//FXn,vid%FXn]=h;ok=np.isfinite(F)
    WDF=nd.map_coordinates(WD*1.0,np.mgrid[0:FYn,0:FXn]/FS*RS,order=0,mode='nearest')>0;LF=nd.map_coordinates(LAND*1.0,np.mgrid[0:FYn,0:FXn]/FS*RS,order=0,mode='nearest')>0
    F2,cf=F,0;h2=h;FW['h']=base64.b64encode(h2.astype(np.float32).tobytes()).decode()
    return nG.reshape(G_ANZ.shape).astype(G_ANZ.dtype),{'grob':cg,'fein':cf}
def _wandstreifen_glatt():   # t128u [F K5b]: kurze Normalenperioden auf Steilwaenden glatten; Grenze wird danach an GB gepinnt
    global G_ANZ,BAND,_vid
    if os.environ.get('WANDSTREIFEN','1')=='0':return {'aus':'WANDSTREIFEN=0'}
    sig=float(os.environ.get('WANDSTREIFEN_SIG','1.0'))
    felder=os.environ.get('WANDSTREIFEN_FELDER','*').split(',')
    TM=np.ones((NY,NX),bool)
    if '*' not in felder:
        TM[:]=False
        for f in felder:
            if len(f)<2 or f[0] not in 'ABCDEFGH' or not f[1:].isdigit():continue
            tx,ty=ord(f[0])-65,int(f[1:])-1
            if 0<=tx<8 and 0<=ty<7:TM[ty*43:min((ty+1)*43,NY),tx*42:min((tx+1)*42,NX)]=True
    if '*' in felder:
        import runde_o18 as RW18
        BAND0=BAND.copy()
        ext=RW18.band_erweitern(FW,G_ANZ,VC,WV,WEGA,belegt,NX,NY,RS,thr=1.0)
        if 'B' in ext:
            B2=ext.pop('B');_vid=ext.pop('vid')
            # D2 ist unveraenderte Regressionsbasis; auch geteilte Randpunkte
            # bleiben stabil. Sperre das Feld plus eine Bandzelle Puffer.
            y0,y1=max(0,43-1),min(NY,86+1);x0,x1=max(0,126-1),min(NX,168+1)
            locked=np.zeros_like(BAND);locked[y0:y1,x0:x1]=True
            B2[locked]=BAND0[locked];BAND=B2
            FW['band']=base64.b64encode(np.flatnonzero(BAND.ravel()).astype(np.uint32).tobytes()).decode()
            cy,cx=np.nonzero(BAND);used=np.zeros((FYn,FXn),bool)
            for ay in range(FS+1):
                for ax in range(FS+1):used[cy*FS+ay,cx*FS+ax]=True
            vid2=np.flatnonzero(used.ravel()).astype(np.uint32);keepgrid=np.zeros(FYn*FXn,bool);keepgrid[vid2]=True
            vid_alt=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);keep=keepgrid[vid_alt]
            FW['vid']=base64.b64encode(vid_alt[keep].tobytes()).decode()
            for key,width in (('h',1),('c',3),('t',3),('s',1)):
                arr=np.frombuffer(base64.b64decode(FW[key]),np.float32 if key=='h' else np.uint8)
                FW[key]=base64.b64encode(arr.reshape(-1,width)[keep].tobytes()).decode()
            _vid=vid_alt[keep]
    else:ext={'hinweis':'Prototyp nur in '+','.join(felder)+'; Feinband-Erweiterung folgt im Kartenlauf'}
    if sig<=0:return {'aus':'WANDSTREIFEN_SIG<=0','band':ext}
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);fy=vid//FXn;fx=vid%FXn
    h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
    F=np.zeros((FYn,FXn),np.float32);OK=np.zeros((FYn,FXn),bool);F[fy,fx]=h;OK[fy,fx]=True
    Sm=nd.gaussian_filter(F,sig*FS)/np.maximum(nd.gaussian_filter(OK.astype(np.float32),sig*FS),1e-6)
    GA=G_ANZ.reshape(GY,GX).astype(float);gy,gx=np.gradient(GA,1/RS)
    M=(np.hypot(gx,gy)>1.0)&(WV.reshape(GY,GX)<=-900)&(WEGA.reshape(GY,GX)<20)
    if '*' in felder:M[max(0,43*RS-RS):min(GY,86*RS+RS),max(0,126*RS-RS):min(GX,168*RS+RS)]=False
    if '*' not in felder:
        tz,tx=np.mgrid[0:GY,0:GX];TG=nd.map_coordinates(TM.astype(np.float32),[tz/RS,tx/RS],order=0,mode='nearest')>0.5;M&=TG
    smask=nd.gaussian_filter(M.astype(np.float32),RS*0.5)
    if '*' in felder:smask[max(0,43*RS-RS):min(GY,86*RS+RS),max(0,126*RS-RS):min(GX,168*RS+RS)]=0
    gsig=float(os.environ.get('WANDSTREIFEN_GROBSIG','0'))
    Gsm=nd.gaussian_filter(GA,gsig*RS) if gsig>0 else GA;GA2=GA*(1-smask)+Gsm*smask
    G_ANZ=GA2.reshape(G_ANZ.shape).astype(G_ANZ.dtype);GA=G_ANZ.reshape(GY,GX).astype(float)
    gy,gx=np.gradient(GA,1/RS);M=(np.hypot(gx,gy)>1.0)&(WV.reshape(GY,GX)<=-900)&(WEGA.reshape(GY,GX)<20)
    if '*' in felder:M[max(0,43*RS-RS):min(GY,86*RS+RS),max(0,126*RS-RS):min(GX,168*RS+RS)]=False
    if '*' not in felder:M&=TG
    wm=nd.map_coordinates(M.astype(np.float32),[fy/FS*RS,fx/FS*RS],order=0,mode='nearest')>0.5
    BC=np.repeat(np.repeat(BAND,FS,axis=0),FS,axis=1);BV=np.zeros((FYn,FXn),bool);BV[:-1,:-1]|=BC;BV[1:,:-1]|=BC;BV[:-1,1:]|=BC;BV[1:,1:]|=BC
    fade=np.clip(nd.distance_transform_edt(BV)[fy,fx]/FS,0,1)
    if '*' not in felder:
        TF=np.repeat(np.repeat(TM,FS,axis=0),FS,axis=1);TF=np.pad(TF,((0,1),(0,1)),mode='edge');fade*=TF[fy,fx]
    w=wm*fade;h2=h*(1-w)+Sm[fy,fx]*w;FW['h']=base64.b64encode(h2.astype(np.float32).tobytes()).decode()
    return {'sigma_m':sig,'grob_sigma_m':gsig,'wandpunkte':int(wm.sum()),'geaendert':int((np.abs(h2-h)>0.01).sum()),'max_m':round(float(np.abs(h2-h).max()),3),'band':ext}
G_ANZ,_ag=(_anschluss_gang() if not os.environ.get('ANSCHLUSS_ALT') else (G_ANZ,{}));print('o18k_anschluss_gang',_ag);G_ANZ,_ra=(_rand_auslauf() if not os.environ.get('RANDAUS_ALT') else (G_ANZ,{}));print('o18k_rand_auslauf',_ra);G_ANZ,_wz=_weg_zurueck();print('o18h_weg_zurueck',_wz);G_ANZ,_wu=_weg_wulst();print('o18i_weg_wulst',_wu);G_ANZ,_we=(_weg_eben() if not os.environ.get('WEGEBEN_ALT') else (G_ANZ,{}));print('o18k_weg_eben',_we);G_ANZ,_lf=(__import__('relief_o18n').landschaft_final(G_ANZ,WV,WEGA.reshape(WV.shape),RS,_HSM.reshape(WV.shape)>0 if '_HSM' in globals() and np.size(_HSM)==WV.size else None,rampen=RAMPWEGE) if not os.environ.get('LF_ALT') else (G_ANZ,{}));print('o18n_landschaft_final',_lf);print('o18h_entzacken',R18.fein_entzacken(FW,NX,NY));G_ANZ,_wzr=(_wand_zurueck() if os.environ.get('WANDZ') else (G_ANZ,{'aus':'WANDZ=1 fuer O18o-Wandruecknahme; verworfen: R5 40->54, G5 169->183, O17-Saegezaehne G1'}));print('o18o_wand_zurueck',_wzr);G_ANZ,_wn=(_wand_neu() if os.environ.get('WANDNEU','0')!='0' else (G_ANZ,{'aus':'WANDNEU=1 schaltet ein; O18p 3 Versuche: G7b erfuellt, aber G2f/G5/G6/R5 neu'}));print('o18p_wand_neu',_wn);G_ANZ,_sf=(_senke_fuellen() if os.environ.get('SENKE','0')!='0' else (G_ANZ,{'aus':'SENKE=1 schaltet ein; O18r 3 Versuche R5 40->0, aber G6 +13..+16, G2f +1, T1 +1'}));print('o18r_senke',_sf);G_ANZ,_es=(_entspitzen() if os.environ.get('SPITZE','0')!='0' else (G_ANZ,{}));print('o18w_entspitzen',_es);G_ANZ,_rw=(_rand_weg() if os.environ.get('RANDWEG','1')!='0' else (G_ANZ,{}));print('o18w_rand_weg',_rw);G_ANZ,_wm=(_wand_mikro() if os.environ.get('WMR','0')!='0' else (G_ANZ,{}));print('o18w_wand_mikro',_wm);G_ANZ,_fg=(_falten_glatt() if os.environ.get('FALT','1')!='0' else (G_ANZ,{}));print('o18w_falten_glatt',_fg);_ws=_wandstreifen_glatt();print('o18s_wandstreifen',_ws);print('o18g_bandnaht_final',_bandnaht_j1())   # O18g [F G1/H1 Durchsicht-Schlitze]: O18d-f aendern Fein/Grob nach J1 -> Naht am Ende erneut exakt
_wellen_snap('gb_nach_falten_vor_hangwellen',G_ANZ)
G_ANZ,_hw=_hangwellen_glatt();print('o18w_hangwellen_glatt',_hw);print('o18g_bandnaht_nach_hangwellen',_bandnaht_j1())
_wellen_snap('gb_anzeige_final',G_ANZ)
if os.environ.get('WELLEN_DIAG'):np.savez_compressed(os.environ['WELLEN_DIAG'],**_WELLEN_DIAG)
def _wand_rau():   # O18j: Wandrauheit (mittl. |h - Gauss 1 m|) Stand O17 vs jetzt, Grob + Fein (gleiche vid)
    M=_wand_maske();r=lambda A:float(np.abs(A-nd.gaussian_filter(A,RS*1.0))[M].mean());GA=G_ANZ.reshape(GY,GX).astype(float)
    vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
    def fr(V,H):
        F=np.full((FYn,FXn),np.nan);F[V//FXn,V%FXn]=H;ok=np.isfinite(F);Fz=np.where(ok,F,0);g=nd.gaussian_filter(Fz,FS)/np.maximum(nd.gaussian_filter(ok*1.0,FS),1e-6)
        mf=ok&nd.map_coordinates(M*1.0,np.mgrid[0:FYn,0:FXn]/FS*RS,order=0,mode='nearest').astype(bool);return float(np.abs(F-g)[mf].mean()),int(mf.sum())
    return {'grob_o17':round(r(_WEG_G0),4),'grob_jetzt':round(r(GA),4),'wandzellen':int(M.sum()),'fein_o17':[round(x,4) if isinstance(x,float) else x for x in fr(_WEG_V0,_WEG_F0)],'fein_jetzt':[round(x,4) if isinstance(x,float) else x for x in fr(vid,h)]}
print('o18j_wandrau',_wand_rau())
_VW=json.load(open('pruefung/o18/versunken_weg.json')) if os.path.exists('pruefung/o18/versunken_weg.json') else []   # O18d [F 7 versunkene Geroellteile]: Raycast-gemeldete versunkene/im Wasser stehende Objekte entfernen [A]
_vwn=0
for _k,_x,_z,_d in _VW:
    _L=globals()[_k];_i=[i for i,o in enumerate(_L) if abs(o[0]-_x)<0.02 and abs(o[2]-_z)<0.02]
    for i in reversed(_i):_L.pop(i);_vwn+=1
print('o18d_versunken_entfernt',_vwn,len(_VW))
# O18m G11 (t112u): Objekte auf das endgueltige Anzeige-Gelaende setzen, Baeume an Wand (>0.9) entfernen [F]
_SHC=json.load(open('pruefung/strahl_hoehe_t65u.json')) if os.path.exists('pruefung/strahl_hoehe_t65u.json') else {};_GA=np.asarray(G_ANZ,float);_gy,_gx=np.gradient(_GA,1/RS);_ST=np.hypot(_gx,_gy);_g11=[0,0]
for _k in ('baeume','felsen','findlinge','steine','felsbloecke'):
    _L=globals().get(_k,[]);_neu=[]
    for o in _L:
        try:_x,_y,_z=float(o[0]),float(o[1]),float(o[2])
        except Exception:_neu.append(o);continue
        if _k=='baeume' and 0<=_x<NX and 0<=_z<NY and float(nd.map_coordinates(_ST,[[_z*RS],[_x*RS]],order=1)[0])>0.9:_g11[1]+=1;continue
        if f"{o[0]:.3f}|{o[2]:.3f}" in _SHC.get(_k,{}):_neu.append(o);continue   # O18t: Raycast-Hoehe (Anzeige-Netz) hat Vorrang vor G_ANZ [A]
        if 0<=_x<NX and 0<=_z<NY:
            _h=float(nd.map_coordinates(_GA,[[_z*RS],[_x*RS]],order=1,mode='nearest')[0])
            if abs(_y-_h)>0.6:o=list(o);o[1]=round(_h,2);_g11[0]+=1
        _neu.append(o)
    _L[:]=_neu
print('o18m_g11_gesetzt_entfernt',_g11)
def _t1_naht():   # O18w [Gate T1_harte_farbkante, 4 Naehte G2 284|75, C2 84|84, B2 82|86, B3 77|93]: gerade Farbkanten (dc>70, Lauf >=9 Ecken) im Umkreis 2 Ecken weichzeichnen (Gauss 1.5 Ecken), nur Land ausserhalb Wand [A]
    C=VC.reshape(GY,GX,3).astype(float);GA=np.asarray(G_ANZ,float).reshape(GY,GX);gy,gx=np.gradient(GA,1/RS);WAND_=np.hypot(gx,gy)>1.0;LAND_=WV.reshape(GY,GX)<=-900
    dc=np.linalg.norm(np.diff(C,axis=1)[:-1],axis=2)+np.linalg.norm(np.diff(C,axis=0)[:,:-1],axis=2)
    hart=(dc>70)&LAND_[:-1,:-1]&~nd.binary_dilation(WAND_,iterations=RS)[:-1,:-1];lab,n=nd.label(hart);OB=nd.find_objects(lab);M=np.zeros((GY,GX),bool);k_=0
    for k in range(1,n+1):
        sl=OB[k-1];sub=(lab[sl]==k)
        if sub.sum()<8:continue
        lauf=max(max((np.diff(np.r_[0,r_,0]).nonzero()[0].reshape(-1,2)@[-1,1]).max(initial=0) for r_ in A_.astype(int)) for A_ in (sub,sub.T))
        if lauf>=9:M[:-1,:-1][sl]|=sub;k_+=1
    M=nd.binary_dilation(M,iterations=int(os.environ.get('T1R','2')))&LAND_;sg=float(os.environ.get('T1S','1.5'))
    B=np.stack([nd.gaussian_filter(C[...,i],sg) for i in range(3)],-1);C[M]=B[M]
    return np.clip(np.round(C),0,255).astype(VC.dtype).reshape(VC.shape),{'naehte':k_,'ecken':int(M.sum())}
VC,_t1=(_t1_naht() if os.environ.get('T1NAHT','1')!='0' else (VC,{}));print('o18w_t1_naht',_t1)

def _terrasse_c2():   # c2: Stufenprofile im Hang glätten; Fade auf 3 m hält Nahtwerte und -neigung fest [A]
    global G,G_ANZ
    _var=int(os.environ.get('C2TERR','1'))  # 0 aus, 1 = gezielter Nordhang, sigma 1 m (Standard)
    if _var not in (0,1):raise ValueError('C2TERR muss 0 oder 1 sein')
    if _var==0:return {'variante':0,'grob_geaendert':0,'fein_geaendert':0,'max_m':0.0}
    _sg=1.0
    _xx=np.arange(GX,dtype=float)[None,:]/RS;_zz=np.arange(GY,dtype=float)[:,None]/RS
    _d=np.minimum.reduce([np.broadcast_to(_xx-84,(GY,GX)),np.broadcast_to(126-_xx,(GY,GX)),np.broadcast_to(_zz-43,(GY,GX)),np.broadcast_to(86-_zz,(GY,GX))])
    _u=np.clip(_d/3.0,0,1);_rand=_u*_u*(3-2*_u)
    _v=np.clip(np.minimum(_zz-43,56-_zz)/2.5,0,1);_v=_v*_v*(3-2*_v);_rand*=_v
    _land=WV.reshape(GY,GX)<=-900
    _road=WEGA.reshape(GY,GX)>20
    for _x,_z in wege:
        _road[int(_z*RS):int(_z*RS+RS+1),int(_x*RS):int(_x*RS+RS+1)]=True
    for _r in RAMPWEGE:
        _p=np.asarray(_r,float);_L=np.r_[0,np.cumsum(np.hypot(*np.diff(_p,axis=0).T))];_t=np.arange(0,_L[-1]+1e-6,0.25)
        _yi=np.clip((np.interp(_t,_L,_p[:,1])*RS).round().astype(int),0,GY-1);_xi=np.clip((np.interp(_t,_L,_p[:,0])*RS).round().astype(int),0,GX-1);_road[_yi,_xi]=True
    _w=_rand*_land*(~_road);_max=0.0
    _old=np.asarray(G_ANZ).reshape(GY,GX).astype(float);_smooth=nd.gaussian_filter(_old,_sg*RS);_neu=(_old*(1-_w)+_smooth*_w).astype(G_ANZ.dtype)
    _dh=_neu.astype(float)-_old;_max=float(np.abs(_dh).max());_changed=int((np.abs(_dh)>1e-6).sum());G_ANZ=_neu.reshape(np.shape(G_ANZ))
    _vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);_fy=_vid//FXn;_fx=_vid%FXn;_h=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
    _df=nd.map_coordinates(_dh,[_fy/FS*RS,_fx/FS*RS],order=1,mode='nearest')
    _hn=(_h+_df).astype(np.float32);_changed_f=int((np.abs(_hn-_h)>1e-6).sum());_max=max(_max,float(np.abs(_hn-_h).max()))
    FW['h']=base64.b64encode(_hn.tobytes()).decode()
    return {'variante':_var,'sigma_m':_sg,'grob_geaendert':_changed,'fein_geaendert':_changed_f,'max_m':round(_max,3)}

_C2TERR=_terrasse_c2();print('c2_terrasse',_C2TERR)   # nur sichtbares Nordhangband in C2; G bleibt t42u-quellgleich
_G_DAVOR=G.copy();G,DELLENWEG_MESS=dellen_bei_wegen_anheben(G,WV);print('dellen_wege_t132u',DELLENWEG_MESS)
_DELTA=G.astype(float)-_G_DAVOR.astype(float)
if np.any(np.abs(_DELTA)>1e-7):
    _DELTA_ANZEIGE=nd.gaussian_filter(_DELTA,0.6)   # leichte Rundung (0,3 m) in GB/Feinmesh, damit keine neuen R5-Becken entstehen
    G_ANZ=(np.asarray(G_ANZ).reshape(GY,GX).astype(float)+_DELTA_ANZEIGE).astype(np.float32)
    _vid_l=np.frombuffer(base64.b64decode(FW['vid']),np.uint32);_fy_l=_vid_l//FXn;_fx_l=_vid_l%FXn
    _fh_l=np.frombuffer(base64.b64decode(FW['h']),np.float32).astype(float)
    _dh_l=nd.map_coordinates(_DELTA_ANZEIGE,[_fy_l/FS*RS,_fx_l/FS*RS],order=1,mode='nearest')
    FW['h']=base64.b64encode((_fh_l+_dh_l).astype(np.float32).tobytes()).decode()
    _obj_anhebung_l={'objekte':0,'max_m':0.0}
    for _liste_l in (baeume,felsen,findlinge,steine,geroell,felsbloecke):
        for _obj_l in _liste_l:
            _dh_obj_l=float(nd.map_coordinates(_DELTA_ANZEIGE,[[float(_obj_l[2])*RS],[float(_obj_l[0])*RS]],order=1,mode='nearest')[0])
            if _dh_obj_l>0.005:
                _obj_l[1]=round(float(_obj_l[1])+_dh_obj_l,2)
                _obj_anhebung_l['objekte']+=1;_obj_anhebung_l['max_m']=max(_obj_anhebung_l['max_m'],_dh_obj_l)
    _obj_anhebung_l['max_m']=round(_obj_anhebung_l['max_m'],3);print('dellen_objekte_t132u',_obj_anhebung_l)
    W1,W2=tri_steil(G);Wq=np.maximum(W1,W2);neig=Wq.reshape(NY,RS,NX,RS).max((1,3));steil=neig>WANDWINKEL
    Hz=sum(G[dy:dy+GY-1:RS,dx:dx+GX-1:RS][:NY,:NX] for dy in range(3) for dx in range(3))/9
    Gmax=nd.maximum_filter(np.maximum.reduceat(np.maximum.reduceat(G,np.arange(0,GY-1,RS),0),np.arange(0,GX-1,RS),1)[:NY,:NX],5)
    Gmin=nd.minimum_filter(np.minimum.reduceat(np.minimum.reduceat(G,np.arange(0,GY-1,RS),0),np.arange(0,GX-1,RS),1)[:NY,:NX],5)
    nb=nd.binary_dilation(steil,structure=np.ones((3,3)))&~steil;mid=(Gmax+Gmin)/2
    oben=nb&(Hz>=mid);fuss=nb&(Hz<mid);kh=np.where(steil|nb,Gmax-Gmin,0.0)
    b3d=(neig<=35)&(b3d_alt|wand)&~(wa&(fl=='SEE'))
    F.update({'hoehe_m':np.round(Hz,2),'neigung_grad':np.round(neig,1),
      'ecke_nw_m':np.round(G[0:-1:RS,0:-1:RS][:NY,:NX],2),
      'ecke_so_m':np.round(G[RS::RS,RS::RS],2),
      'klippe':np.where(steil,'WAND',np.where(oben,'WAND_OBEN',np.where(fuss,'WAND_FUSS',''))),
      'skin_slot':np.where(steil,'wand_fels',np.char.add('ug_',np.char.lower(ug2.astype(str)))),
      'klippe_hoehe_m':np.round(kh,1),
      'klippe_hoehe_quelle':np.where(kh>0,'R_messung_t40u',''),
      'begehbar_3d':b3d.astype(int)})
    spalten={}
    for _c_l in outcols:
        _u_l,_idx_l=np.unique(F[_c_l].astype(str).ravel(),return_inverse=True)
        _dt_l=np.uint8 if len(_u_l)<256 else np.uint16 if len(_u_l)<65536 else np.uint32
        spalten[_c_l]={'w':_u_l.tolist(),'t':_dt_l.__name__,'i':base64.b64encode(_idx_l.astype(_dt_l).tobytes()).decode()}
    with open('zellen_relief.csv','w',newline='') as _csv_l:
        _writer_l=csv.writer(_csv_l);_writer_l.writerow(outcols)
        for _y_l in range(NY):
            for _x_l in range(NX):_writer_l.writerow([F[_c_l][_y_l,_x_l] for _c_l in outcols])
    V=np.stack([vi.ravel()/RS,G.ravel(),vj.ravel()/RS],1)
    ST=np.concatenate([W1.ravel(),W2.ravel()])>WANDWINKEL;TW=TT[ST]
    _scene_l=trimesh.Scene()
    _scene_l.add_geometry(trimesh.Trimesh(V,TT[~ST][:,::-1],process=False,vertex_colors=_vc),'boden')
    _scene_l.add_geometry(trimesh.Trimesh(V,TT[ST][:,::-1],process=False,vertex_colors=_vc),'waende')
    _scene_l.export('dorfmap_relief_z25.glb')
D={'nx':NX,'ny':NY,'G':b64(G),'GB':b64(G_ANZ),'VC':base64.b64encode(VC.tobytes()).decode(),'WEGA':base64.b64encode(WEGA.tobytes()).decode(),'geroell':geroell,'felsbloecke':felsbloecke,'gras':gras,'felsmesh':(json.load(open('blender/fels_meshes.json')) if os.path.exists('blender/fels_meshes.json') else []),'rampenwege':RAMPWEGE,'WV':b64(WV),'rs':RS,'wandwinkel':WANDWINKEL,'ug':spalten['untergrund'],'sprung':SPRUNG,'spalten':spalten,'reihenfolge':outcols,
 'haeuser':haeuser,'baeume':baeume,'felsen':felsen,'findlinge':findlinge,'steine':steine,'bruecken':bruecken,'wege':wege,'start':start,
 'wandfuss':{'x':fx+.5,'z':fy+.5,'h':round(float(H[fy-1,fx]-H[fy,fx]),1),'zelle':int(fy*NX+fx)},'wandhoehen':WANDH,'FW':FW}
open('relief_daten.json.gz','wb').write(gzip.compress(json.dumps(D,ensure_ascii=False).encode(),9,mtime=0))   # O11 M2: gzip ohne Zeitstempel -> gleicher Code = gleiche Datei [A]
Z={k:len(D[k]) for k in ['haeuser','baeume','felsen','findlinge','steine','bruecken','wege']}
Z.update(wand_dreiecke=int(len(TW)),boden_dreiecke=int((~ST).sum()),zellen_wand_steil=int(steil.sum()),
 zellen_wand_oben=int(oben.sum()),zellen_wand_fuss=int(fuss.sum()),hoehe_min=float(H.min()),hoehe_max=float(H.max()),wandfuss=D['wandfuss'],
 klippe_hoehe_median_3x3_je_wand={w:round(float(np.median((nd.maximum_filter(Hz,3)-nd.minimum_filter(Hz,3))[steil&nd.binary_dilation(wn==w,iterations=3)])),2) for w in WANDH},   # t44u: nur Abbruch, ohne Hang am Fuss
 klippe_hoehe_median_je_wand={w:round(float(np.median(kh[steil&nd.binary_dilation(wn==w,iterations=3)])),2) for w in WANDH},
 bandzellen_umgedeutet=int(wand.sum()),begehbar_3d=int(b3d.sum()))
json.dump(Z,open('relief_zaehlung.json','w'),indent=1,ensure_ascii=False);print(json.dumps(Z,ensure_ascii=False))
CSV_T65U,CSV_T65U_ORTE=RM.csv_nachlauf('zellen_relief.csv',WV,G_ANZ,NX,NY);print('csv_t65u',CSV_T65U)   # t65u Runde M1 [S]
json.dump({'fluss_luecken':LUECKE_T65U,'vertexfarben':VCF_T65U,'objekte':OBJ_T65U,'csv':CSV_T65U,'csv_orte':CSV_T65U_ORTE},open('pruefung/runde_m_aenderungen_t65u.json','w'),indent=1,ensure_ascii=False)
