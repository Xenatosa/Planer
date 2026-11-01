# t41u: echtes neues 3D-Relief. Quelle Lage: raster_c20_z25_zellen.csv (+ t36u-Sidecar fuer Felder). c20 unveraendert.
# Ausgabe: relief_daten.json.gz (Viewer), zellen_relief.csv (Sidecar), dorfmap_relief_z25.glb/.obj, relief_zaehlung.json
import os
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
u=(Hs-lo)/np.maximum(Rg,1e-6)-0.5+0.10*nf+0.13*RIB
krz=nd.gaussian_filter(np.kron(nd.binary_dilation(wand&(wn=='Krater'),iterations=4),np.ones((RS,RS))).astype(float),4)
steil_k=(1.0+1.6*np.clip(0.5+0.4*_fbm(18,36),0,1))*(1-krz)+1.6*krz                                            # t47u: Kraterrand als geboeschter Wall statt Senkrechtring [A]
t=np.clip(u*steil_k+0.5+0.25*krz*_fbm(6,11),0,1);t=t*t*(3-2*t)
# t48u R5: Kraterring mit radialen Felsrippen + 4 Scharten; uebrige Waende mit Grat-Rauschen (ridged). Ober-/Unterkante fix (sin(pi t)) [A]
_kc=np.argwhere(wand&(WN_VOR_K=='Krater')).mean(0)*RS;_jj,_ii=np.mgrid[0:Hn.shape[0],0:Hn.shape[1]];_ang=np.arctan2(_jj-_kc[0],_ii-_kc[1])
_rib=np.sin(_ang*13+1.6*_fbm(14,21));_rib=np.sign(_rib)*np.abs(_rib)**0.6
_sch=np.clip((np.abs(np.sin(_ang*2+0.7))-0.93)/0.07,0,1)
_rid=1-2*np.abs(np.clip(_fbm(5,22)/2.5,-1,1))
t=np.clip(t+np.sin(np.pi*t)*(krz*(0.20*_rib-0.45*_sch)+(1-krz)*0.10*(_rid-0.5)),0,1)
_ns=4+np.round(2*np.clip(0.5+0.4*_fbm(20,37),0,1));_tq=np.floor(t*_ns)/_ns;_fr=t*_ns-np.floor(t*_ns)
_led=(_fbm(9,38)>0.0)*(1-krz)
t=np.clip(t*(1-0.55*_led)+0.55*_led*(_tq+np.clip((_fr-0.55)/0.45,0,1)/_ns),0,1)   # Simse: flache Absaetze + steile Stufen
band=0.04*np.sin(t*np.pi*5+1.3*_fbm(8,9))*np.sin(np.pi*t)           # Simse/Baender in der Wand
tw=np.clip(u*1.5+0.62,0,1);apron=np.clip(tw,0,0.3)                    # Schuttkegel am Fuss
Gs=lo+Rg*np.clip(0.8*t+band+0.2*apron/0.3,0,1);Gs=np.where(Rg>SPRUNG,Gs,Hs)
Gsamp=Hs*(1-wz)+Gs*wz
vj,vi=np.mgrid[0:GY,0:GX].astype(float)
G=nd.map_coordinates(Gsamp,[vj-0.5,vi-0.5],order=1,mode='nearest').astype(np.float32)
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
# t53u R2/R3: Rampen + Serpentinen nach Erosion exakt ins Gitter (Kern 1,6 m eben laengs, Rand weich bis 3,6 m) [A]
from scipy.spatial import cKDTree
_PP=np.concatenate([p for p,_ in RAMPPROF]);_HH=np.concatenate([h for _,h in RAMPPROF]);_kd=cKDTree(_PP)
_vx=np.stack([vi.ravel()/RS,vj.ravel()/RS],1);_r,_k=_kd.query(_vx,distance_upper_bound=7.0);_ok=np.isfinite(_r)
_wv=nd.map_coordinates(np.kron(wa,np.ones((RS,RS))).astype(float),[vj-0.5,vi-0.5],order=0,mode='nearest').ravel()>0.5
_ok&=~_wv;_w=np.clip((7.0-_r[_ok])/5.4,0,1);_w=_w*_w*(3-2*_w);_g=G.ravel().astype(float);_g[_ok]=_g[_ok]*(1-_w)+_HH[_k[_ok]]*_w;G=_g.reshape(G.shape).astype(np.float32)
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
_wu=up(wa,0.6);_ul=np.clip(1-np.abs(_wu-0.35)/0.25,0,1)*(1-up(wand,0.6))
col=col*(1-0.75*_ul[...,None])+0.75*_ul[...,None]*np.array([0.30,0.29,0.27])
_kg=np.clip(up(kies,0.5)*1.4,0,1)*np.clip((_wu-0.5)*3,0,1);col=col*(1-_kg[...,None])+_kg[...,None]*np.array([0.62,0.58,0.52])
_fg=np.clip((_wu-0.6)*3,0,1)*(1-_kg);col=col*(1-0.7*_fg[...,None])+0.7*_fg[...,None]*np.array([0.42,0.40,0.36])
VC=(np.clip(col,0,1)*255).astype(np.uint8)
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
_A=G[_j,_i];_B=G[_j,_i+1];_C=G[_j+1,_i];_D=G[_j+1,_i+1]
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
import runde_o_t67u as RO;FH,BR_T67U=RO.bandrand_weich(FH,_FB0_T67U,_vin);print('bandrand_t67u',BR_T67U)   # t67u O5: keine Rechteck-Stufen am Feinbandrand [A]
import runde_o_t67u as RO;FH,ENTSP_T67U=RO.entspitzen(FH,FB,_vin);FH=np.where(_vin,FH,FB);print('entspitzen_t67u',ENTSP_T67U)   # t67u Runde O3: keine Nadeln/Trichter [A]
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
G_ANZ,GSP_T67U=RO.grob_entspitzen(G_ANZ,WV,BAND,RS);print('grobspitzen_t67u',GSP_T67U)   # t67u O7: Nadeln im Grobnetz ausserhalb Feinband [F] [A]
def vc_weich(VC,GA,WV,WEGA):   # t64u Runde L Boden: Vertexfarben im Flachland weichzeichnen (sigma 1,2 Ecken = 0,6 m) gegen blockige Gras/Erde/Schnee-Flecken; nicht an Wegen, Ufern, Hangkanten [A]
    C=VC.reshape(GA.shape+(3,)).astype(float);B=np.stack([nd.gaussian_filter(C[...,k],1.2) for k in range(3)],-1)
    gy,gx=np.gradient(GA.astype(float),0.5);sl=np.hypot(gx,gy)
    m=((sl<0.35)&(WEGA.reshape(GA.shape)<20)&(nd.distance_transform_edt(WV<=-900)>3)).astype(float);m=nd.gaussian_filter(m,1.0)
    N=C*(1-m[...,None])+B*m[...,None];out=np.clip(np.round(N),0,255).astype(np.uint8)
    return out.reshape(VC.shape),{'anteil':round(float((m>0.5).mean()),3),'farbaenderung_mittel':round(float(np.abs(N-C).mean()),2)}
VC,VCW_T64U=vc_weich(VC,G_ANZ,WV,WEGA);print('vcweich_t64u',VCW_T64U)
VC,VCF_T65U=RM.vc_flecken(VC,G_ANZ,WV);print('vcflecken_t65u',VCF_T65U)   # t65u Runde M1d [S]
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
if os.environ.get('DIAG'):np.savez_compressed(os.environ['DIAG'],WV=WV,G=G_ANZ,WV_ALT=WV_ALT,G_ALT=G,wa=wa,fl=fl.astype(str))
D={'nx':NX,'ny':NY,'G':b64(G),'GB':b64(G_ANZ),'VC':base64.b64encode(VC.tobytes()).decode(),'WEGA':base64.b64encode(WEGA.tobytes()).decode(),'geroell':geroell,'felsbloecke':felsbloecke,'gras':gras,'felsmesh':(json.load(open('blender/fels_meshes.json')) if os.path.exists('blender/fels_meshes.json') else []),'rampenwege':RAMPWEGE,'WV':b64(WV),'rs':RS,'wandwinkel':WANDWINKEL,'ug':spalten['untergrund'],'sprung':SPRUNG,'spalten':spalten,'reihenfolge':outcols,
 'haeuser':haeuser,'baeume':baeume,'felsen':felsen,'findlinge':findlinge,'steine':steine,'bruecken':bruecken,'wege':wege,'start':start,
 'wandfuss':{'x':fx+.5,'z':fy+.5,'h':round(float(H[fy-1,fx]-H[fy,fx]),1),'zelle':int(fy*NX+fx)},'wandhoehen':WANDH,'FW':FW}
open('relief_daten.json.gz','wb').write(gzip.compress(json.dumps(D,ensure_ascii=False).encode(),9))
Z={k:len(D[k]) for k in ['haeuser','baeume','felsen','findlinge','steine','bruecken','wege']}
Z.update(wand_dreiecke=int(len(TW)),boden_dreiecke=int((~ST).sum()),zellen_wand_steil=int(steil.sum()),
 zellen_wand_oben=int(oben.sum()),zellen_wand_fuss=int(fuss.sum()),hoehe_min=float(H.min()),hoehe_max=float(H.max()),wandfuss=D['wandfuss'],
 klippe_hoehe_median_3x3_je_wand={w:round(float(np.median((nd.maximum_filter(Hz,3)-nd.minimum_filter(Hz,3))[steil&nd.binary_dilation(wn==w,iterations=3)])),2) for w in WANDH},   # t44u: nur Abbruch, ohne Hang am Fuss
 klippe_hoehe_median_je_wand={w:round(float(np.median(kh[steil&nd.binary_dilation(wn==w,iterations=3)])),2) for w in WANDH},
 bandzellen_umgedeutet=int(wand.sum()),begehbar_3d=int(b3d.sum()))
json.dump(Z,open('relief_zaehlung.json','w'),indent=1,ensure_ascii=False);print(json.dumps(Z,ensure_ascii=False))
CSV_T65U,CSV_T65U_ORTE=RM.csv_nachlauf('zellen_relief.csv',WV,G_ANZ,NX,NY);print('csv_t65u',CSV_T65U)   # t65u Runde M1 [S]
json.dump({'fluss_luecken':LUECKE_T65U,'vertexfarben':VCF_T65U,'objekte':OBJ_T65U,'csv':CSV_T65U,'csv_orte':CSV_T65U_ORTE},open('pruefung/runde_m_aenderungen_t65u.json','w'),indent=1,ensure_ascii=False)
