# t42u: Bodentextur = gemalte c20-Karte (Draufsicht). Gemaltes Wandband/Schatten wird mit Farbe der eigenen Ebene aufgefuellt,
# weil Wand jetzt echte Geometrie mit eigener Wandtextur ist und Licht/Schatten aus der Engine kommt. c20 selbst bleibt unveraendert.
# P3 (16.11.2026): zusaetzlich Modus "vc" = Fleckrand-Weichzeichnung der Anzeige-Vertexfarben (siehe vc_fleckrand_p3 unten).
#   python3 gen_textur.py        -> wie bisher textur_relief_t42u.jpg (t42u, unveraendert)
#   python3 gen_textur.py vc     -> NW-Ecke Detail (T2) + Fleckrand weich (T1): VC + FW.c in relief_daten.json.gz und neu/relief_neu.json.gz weich, danach RELIEF_NEU=1 python3 baue_html.py
import sys,os,json,gzip,base64,csv,numpy as np,scipy.ndimage as nd

def textur_t42u():
    from PIL import Image
    NX,NY,PX=336,303,8
    T=np.asarray(Image.open('../_alt/modell3d_t36u/textur_c20_8px.jpg').convert('RGB')).astype(float)/255
    R=list(csv.DictReader(open('zellen_relief.csv')));A=lambda k:np.array([r[k] for r in R]).reshape(NY,NX)
    ug=A('untergrund_c20');Hb=A('boden_hoehe_m').astype(float)
    M=np.isin(ug,['KLIPPE_WAND','KLIPPE_KANTE','SCHATTEN'])
    k=4;S=T.reshape(NY,PX,NX,PX,3).reshape(NY,PX,NX,PX,3)
    small=np.asarray(Image.fromarray((T*255).astype(np.uint8)).resize((NX*2,NY*2),Image.BILINEAR)).astype(float)/255
    Ms=np.kron(M,np.ones((2,2)))>0;Hs=np.kron(Hb,np.ones((2,2)))
    fill=small.copy()
    for h in np.unique(np.round(Hs[Ms])):
        ziel=Ms&(np.round(Hs)==h);quelle=(~Ms)&(np.abs(Hs-h)<1.0)
        if not quelle.any():quelle=~Ms
        out=np.zeros(small.shape);done=np.zeros(Hs.shape,bool)
        for s in (3,10,30,90):
            w=nd.gaussian_filter(quelle.astype(float),s);v=np.stack([nd.gaussian_filter(small[...,c]*quelle,s) for c in range(3)],-1)
            ok=ziel&~done&(w>0.02);out[ok]=v[ok]/w[ok][:,None];done|=ok
        rest=ziel&~done
        if rest.any():
            q2=~Ms;w=nd.gaussian_filter(q2.astype(float),20);v=np.stack([nd.gaussian_filter(small[...,c]*q2,20) for c in range(3)],-1);out[rest]=v[rest]/np.maximum(w[rest],1e-6)[:,None]
        fill[ziel]=out[ziel]
    F=np.asarray(Image.fromarray((fill*255).astype(np.uint8)).resize((NX*PX,NY*PX),Image.BILINEAR)).astype(float)/255
    a=nd.gaussian_filter(np.kron(M,np.ones((PX,PX))).astype(float),3)[...,None]
    rs=np.random.default_rng(7);n=nd.gaussian_filter(rs.standard_normal((NY*PX,NX*PX)),1.5);n=1+0.03*n/n.std()
    O=T*(1-a)+F*n[...,None]*a
    Image.fromarray((np.clip(O,0,1)*255).astype(np.uint8)).save('textur_relief_t42u.jpg',quality=88)
    print('maskiert',int(M.sum()),'Zellen')


# ---------- P3 Textur: T1_fleckrand (harte Schnee/Gras-Raender in VC) ----------
# Messung wie pruefung/pruefe_regeln.py T1 (dort unveraendert): dc = |dC/dx| + |dC/dz| je Gitterpunkt, Schwelle 70, nur Land ausserhalb 1 m Wandsaum.
# Hier: ueberall wo dc > ZIEL (62, Abstand zur Schwelle), Farbe lokal und iterativ weichzeichnen (Gauss 0,5 m, nur Landpunkte als Quelle,
# Gewicht weich ausgeblendet). Der Rand folgt damit der vorhandenen Fleckkontur (organisch, keine geraden Kanten), wird nur 1-3 m weich.
# Nur Farbdaten (VC, FW.c); Hoehen, Wasser, Wege bleiben bytegleich. Idempotent: zweiter Lauf aendert nichts (P11b: auch bei
# nicht konvergierenden Raendern, siehe Fixpunkt unten).
# FW.c (Feinband) wird danach aus der fertigen VC abgeleitet (siehe unten), damit Grob- und Feinnetz dieselbe Farbe zeigen.
def _dc(C):
    return np.linalg.norm(np.diff(C,axis=1)[:-1],axis=2)+np.linalg.norm(np.diff(C,axis=0)[:,:-1],axis=2)

def vc_fleckrand_p3(D,C_ein=None,ziel=62.0,sig=1.0,max_it=200,max_fix=5000):
    NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
    G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(GY,GX).astype(float)
    LAND=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(GY,GX)<=-900
    gy,gx=np.gradient(G,1/RS);WAND=np.hypot(gx,gy)>1.0
    R=LAND&~nd.binary_dilation(WAND,iterations=RS)
    C0=np.frombuffer(base64.b64decode(D['VC']),np.uint8).reshape(GY,GX,3).astype(float);C=(C0 if C_ein is None else C_ein).astype(float).copy()
    Lf=LAND.astype(float);den=np.maximum(nd.gaussian_filter(Lf,sig),1e-6)
    def schlecht(C):
        dc=_dc(np.round(C));bad=np.zeros((GY,GX),bool);bad[:-1,:-1]=(dc>ziel)&R[:-1,:-1]
        bad[:-1,1:]|=bad[:-1,:-1];bad[1:,:-1]|=bad[:-1,:-1];return bad
    def schritt(C,bad):
        m=nd.binary_dilation(bad,iterations=1)&LAND
        w=(np.clip(nd.gaussian_filter(m.astype(float),0.7)*1.6,0,1)*Lf)[...,None]
        B=np.stack([nd.gaussian_filter(C[...,c]*Lf,sig)/den for c in range(3)],-1)
        return C*(1-w)+B*w
    # P11b: bisher nicht idempotent. Wo der Fleckrand in max_it Iterationen nicht unter ZIEL kommt (Endstand: 107 Punkte in E4),
    # lief jeder weitere vc-Lauf vom eigenen Ausgabestand aus 200 weitere Iterationen -> VC aenderte sich bei jedem Lauf
    # (kein Zufall: Seeds fest, keine Threads/Reihenfolgen; Ursache ist die Abhaengigkeit vom vorherigen Ausgabestand).
    # Jetzt: nach max_it ohne Konvergenz wird auf dem gerundeten Gitter bis zum Fixpunkt weitergerechnet; ist die Eingabe
    # schon ein Fixpunkt (= Ergebnis eines frueheren Laufs auf demselben GB/WV), bleibt sie unveraendert. Wo der Rand
    # konvergiert (bad leer), ist das Ergebnis wie bisher.
    fix_it=0;Ci=np.round(C);bad=schlecht(Ci)
    if bad.any() and np.array_equal(np.round(schritt(Ci,bad)),Ci):
        it=0;C=Ci   # Eingabe ist schon Fixpunkt (Ergebnis eines frueheren Laufs): nichts zu tun
    else:
        for it in range(max_it):
            bad=schlecht(C)
            if not bad.any():break
            C=schritt(C,bad)
        if bad.any() and it==max_it-1:
            C=np.round(C)
            for fix_it in range(1,max_fix+1):
                bad=schlecht(C)
                if not bad.any():break
                Cn=np.round(schritt(C,bad))
                if np.array_equal(Cn,C):break
                C=Cn
    bad=schlecht(C)
    Cn=np.clip(np.round(C),0,255).astype(np.uint8);dl=Cn.astype(float)-C0;d=np.abs(dl).max(2)
    FW=D['FW'];FS=FW['fs'];FXn=NX*FS+1;vid=np.frombuffer(base64.b64decode(FW['vid']),np.uint32)
    fc=np.frombuffer(base64.b64decode(FW['c']),np.uint8).reshape(-1,3).astype(float)
    fc2=np.clip(np.round(np.stack([nd.map_coordinates(Cn[...,c].astype(float),[(vid//FXn)/FS*RS,(vid%FXn)/FS*RS],order=1) for c in range(3)],1)),0,255).astype(np.uint8)
    info={'iterationen':it,'fixpunkt_iterationen':fix_it,'rest_ueber_ziel':int(bad.sum()),'vc_punkte_geaendert':int((d>0).sum()),'vc_punkte_ueber_10':int((d>10).sum()),
          'vc_max_aenderung':int(d.max()),'fw_c_geaendert':int((np.abs(fc2.astype(float)-fc).max(1)>0).sum())}
    return Cn,fc2,info

# ---------- P3 Textur T2: NW-Ecke (A1/A2, x<40 m, z<70 m) ohne Feindetail ----------
# Befund 16.11.: dort ist VC eine stark weichgezeichnete Flaeche (Detailmass ~1,3 statt ~15 daneben) mit gerader Kante bei x~35 m / z~64 m
# -> wirkt im Bild wie abgeschnittene/verschmierte Textur. Abhilfe nur Farbe: Rand mit weichem Rauschversatz (bis ~2 m) organisch machen,
# Feindetail (Hochpass) aus dem Gelaende 35,5 m oestlich einblenden. Grundfarbe (FELS/SCHNEE) bleibt. Nicht an Wasser (2 m Abstand).
def vc_ecke_nw_p3(D,C):
    NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
    LAND=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(GY,GX)<=-900
    C=C.astype(float);L=np.stack([nd.gaussian_filter(C[...,c],2) for c in range(3)],-1);hp=C-L
    det=nd.uniform_filter(np.abs(hp).sum(2),9)
    box=np.zeros((GY,GX),bool);box[:70*RS,:40*RS]=True
    lab,n=nd.label((det<4)&box)
    if n==0:return C,{'ecke_px':0}
    sz=np.bincount(lab.ravel());sz[0]=0
    if sz.max()<2000:return C,{'ecke_px':0}   # nur die grosse glatte Flaeche, sonst nichts (idempotent)
    M=nd.binary_closing(lab==sz.argmax(),iterations=3)
    saum=nd.binary_dilation(M,iterations=8*RS)&LAND;nass=nd.binary_dilation(~LAND,iterations=4)
    ww=np.clip(nd.gaussian_filter(saum.astype(float),4)*1.5-0.25,0,1)*np.clip(nd.gaussian_filter((~nass).astype(float),1.5)*2-1,0,1)
    rng=np.random.default_rng(5)
    def f(s,a):n_=nd.gaussian_filter(rng.standard_normal((GY,GX)),s);return n_/n_.std()*a
    dx=(f(6,3.0)+f(2.5,1.2))*ww;dy=(f(6,3.0)+f(2.5,1.2))*ww
    yy,xx=np.mgrid[0:GY,0:GX].astype(float)
    srcL=nd.map_coordinates(LAND.astype(float),[yy+dy,xx+dx],order=1,mode='nearest')>0.99
    Wc=np.stack([nd.map_coordinates(C[...,c],[yy+dy,xx+dx],order=1,mode='nearest') for c in range(3)],-1)
    Wc=np.where((srcL&LAND)[...,None],Wc,C)
    w=np.clip(nd.gaussian_filter(M.astype(float),2.0)*1.3,0,1)*LAND
    O=np.clip(Wc+w[...,None]*np.roll(hp,-71,axis=1),0,255)
    return O,{'ecke_px':int(M.sum()),'ecke_saum_px':int((ww>0).sum())}

def _schreibe(D,pfad,kompakt):
    js=json.dumps(D,ensure_ascii=False,separators=(",",":")) if kompakt else json.dumps(D,ensure_ascii=False)
    open(pfad,'wb').write(gzip.compress(js.encode(),9,mtime=0))

def vc_lauf(quelle='relief_daten.json.gz',neu='neu/relief_neu.json.gz'):
    D=json.load(gzip.open(quelle))
    C0=np.frombuffer(base64.b64decode(D['VC']),np.uint8).reshape(D['ny']*D['rs']+1,D['nx']*D['rs']+1,3)
    C1,ie=vc_ecke_nw_p3(D,C0);Cn,fc2,info=vc_fleckrand_p3(D,C1);info.update(ie)
    vc=base64.b64encode(Cn.tobytes()).decode();c=base64.b64encode(fc2.tobytes()).decode()
    if vc==D['VC'] and c==D['FW']['c']:print('vc_p3 unveraendert',info);return info
    D['VC']=vc;D['FW']['c']=c;_schreibe(D,quelle,False)
    if neu and os.path.exists(neu):   # Viewer-Paket = relief_daten + neu_mesh_tiles; nur VC/FW.c ersetzen, Kachelmeshes/Hoehen unveraendert
        N=json.load(gzip.open(neu));N['VC']=vc;N['FW']['c']=c;_schreibe(N,neu,True)
    print('vc_p3',json.dumps(info));return info

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='vc':vc_lauf(*sys.argv[2:4])
    else:textur_t42u()
