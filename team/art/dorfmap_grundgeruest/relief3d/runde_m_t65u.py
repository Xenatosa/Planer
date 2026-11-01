# t65u Runde M: Korrekturen nur fuer Anzeige (relief_daten) + CSV-Nachlauf. Alle Zahlen landen in pruefung/runde_m_aenderungen_t65u.json [S]
import numpy as np,scipy.ndimage as nd,csv
def tri(GA,x,z,RS=2):
    i=x*RS;j=z*RS;i0=min(max(int(np.floor(i)),0),GA.shape[1]-2);j0=min(max(int(np.floor(j)),0),GA.shape[0]-2);u=i-i0;v=j-j0
    A,B,C,D=GA[j0,i0],GA[j0,i0+1],GA[j0+1,i0],GA[j0+1,i0+1]
    return float(A+(D-C)*u+(C-A)*v if v>=u else A+(B-A)*u+(D-B)*v)
def fluss_luecken(WV,GA,VB):
    """zwei trockene Luecken im Anzeige-Wasser schliessen (Pfad Quelle->Auslass lueckenlos): (a) See-Abfluss/Flussanfang 212,5|194,5 -> 215,5|197,5
    (b) Stummel x70-75 z252-261 -> Hauptfluss 73|262,5 (Luecke 1,5 m, in Runde L durch 'Wasser unter Boden entfernt' entstanden). Spiegel linear zwischen den Enden, Boden 0,3 m darunter
    ausser an Feinband-Ecken (VB): dort Spiegel 0,03 m ueber Boden und Oberlauf monoton nachgezogen [A]"""
    WV=WV.copy();GA=GA.copy();st={}
    lab,_=nd.label(WV>-900,np.ones((3,3)))
    for name,(a,b) in {'see_fluss':((212.5,194.5),(215.5,197.5)),'stummel':((73.0,261.0),(73.0,262.5))}.items():
        ja,ia=int(a[1]*2),int(a[0]*2);jb,ib=int(b[1]*2),int(b[0]*2);la,lb=float(WV[ja,ia]),float(WV[jb,ib]);ka=lab[ja,ia]
        n=int(max(abs(jb-ja),abs(ib-ia)))+1;neu=0;ab=0;hoch=-1e9;breite=1 if name=='see_fluss' else 0
        for t in np.linspace(0,1,n):
            j=int(round(ja+(jb-ja)*t));i=int(round(ia+(ib-ia)*t));lv=la+(lb-la)*t
            if name=='stummel':cols=range(ia-4,ia+6)  # ganze Stummelbreite (x71-75,5) an den Hauptfluss anschliessen
            else:cols=range(i-breite,i+breite+1)
            rows=[j] if name=='stummel' else range(j-breite,j+breite+1)
            for jj in rows:
                for ii in cols:
                    if name=='stummel' and WV[jj,ii]>-900:continue
                    if name=='stummel' and not (WV[jj-1:jj+3,ii]>-900).any():continue
                    if VB[jj,ii]:
                        l2=max(lv,float(GA[jj,ii])+0.03);hoch=max(hoch,l2)
                    else:
                        l2=lv
                        if GA[jj,ii]>l2-0.3:GA[jj,ii]=l2-0.3;ab+=1
                    if WV[jj,ii]<=-900:neu+=1
                    WV[jj,ii]=l2 if WV[jj,ii]<=-900 else min(WV[jj,ii],l2) if not VB[jj,ii] else max(WV[jj,ii],l2)
        oben=0
        if hoch>-1e8:
            m=(lab==ka)&(WV<hoch);oben=int(m.sum());WV[m]=hoch   # Oberlauf (Stummel) auf Spiegel der Engstelle anheben -> nie bergauf
        st[name]={'neue_wasserecken':neu,'boden_abgesenkt':ab,'oberlauf_angehoben':oben,'spiegel_von':round(la,3),'spiegel_bis':round(lb,3),'max_engstelle':round(hoch,3) if hoch>-1e8 else None}
    return WV,GA,st
def vc_flecken(VC,GA,WV):
    """einzelne Vertexfarb-Ausreisser (>60 RGB-Abstand zum 3x3-Median, nicht an Wasser/Hang) auf den Median setzen [A]"""
    V=VC.astype(float);M=np.stack([nd.median_filter(V[...,k],size=3) for k in range(3)],-1);d=np.linalg.norm(V-M,axis=-1)
    gy,gx=np.gradient(GA.astype(float),0.5);sl=np.hypot(gx,gy)
    ok=(d>60)&(sl<0.7)&(nd.distance_transform_edt(WV<=-900)>2)
    V[ok]=M[ok];return np.clip(np.round(V),0,255).astype(np.uint8),{'vertexfarben_geglaettet':int(ok.sum())}
FUSS_R={'baeume':0.35}
def objekte(L5,GA,WV,OV,haeuser,rampen,bruecken,NX,NY):
    """Objekte exakt auf das Anzeige-Dreiecksnetz setzen (statt bilinear), schwebende Steine absenken, Baeume aus Haus/Weg/Bauplatz/Platz/Hof/Rampe/Bruecke,
    Abstand Baum-Baum >= 0,05*(h1+h2) (Stamm frei, Kronen duerfen sich beruehren), alles >45 Grad oder im Wasser raus. Formeln = pruefung/objekte_voll_t65u.py [A]"""
    st={};sper=np.zeros((NY,NX),bool)
    for o in OV:
        if o['weg_id'] or o['bauplatz']=='1' or o['platz'] or o['hof']=='1' or o['bruecke']=='1':sper[int(o['cy']),int(o['cx'])]=True
    WS=np.where(WV>-900,WV,-999.0);WOK=WV>-900
    gy,gx=np.gradient(GA.astype(float),0.5);SL=np.degrees(np.arctan(np.hypot(gx,gy)))
    ring=[(np.cos(a),np.sin(a)) for a in np.linspace(0,2*np.pi,8,endpoint=False)]
    def wsp(x,z):
        i0=int(x*2);j0=int(z*2)
        if not WOK[max(0,j0-1):j0+3,max(0,i0-1):i0+3].any():return -999.0
        return float(WS[max(0,j0-1):j0+3,max(0,i0-1):i0+3].max())
    for nm,L in L5.items():
        neu=[];c={'n_vorher':len(L),'hoehe_neu':0,'abgesenkt':0,'wasser':0,'steil':0,'ueberlapp':0,'abstand':0}
        for o in L:
            o=list(o);x,z,h=o[0],o[2],o[3];g0=tri(GA,x,z)
            gb=float(nd.map_coordinates(GA,[[z*2],[x*2]],order=1,mode='nearest')[0]);off=o[1]-gb if nm!='baeume' else 0.0
            if nm=='baeume':off=min(0.0,o[1]-gb)
            if o[1]-gb>1.0:c['wandnetz_behalten']=c.get('wandnetz_behalten',0)+1;neu.append(o);continue   # steht auf verschobenem Wand-/Feinband-Netz (Raycast-Hoehe), GA-Gitter gilt dort nicht
            y=round(g0+off,3)
            if abs(y-o[1])>0.005:c['hoehe_neu']+=1
            r=FUSS_R.get(nm,0.62*h);gs=[tri(GA,min(NX-0.01,max(0,x+r*a)),min(NY-0.01,max(0,z+r*b))) for a,b in ring]
            if nm!='baeume':
                unten=y-0.12*h
                if unten-min(gs)>0.15:y=round(min(gs)+0.15+0.12*h-0.01,3);c['abgesenkt']+=1
            elif (y-0.3)-min(gs)>0.15:y=round(min(gs)+0.45-0.01,3);c['abgesenkt']+=1
            o[1]=y
            if SL[min(int(round(z*2)),GA.shape[0]-1),min(int(round(x*2)),GA.shape[1]-1)]>45:c['steil']+=1;continue
            fuss=y-0.3 if nm=='baeume' else y
            if wsp(x,z)>fuss-(0.0 if nm=='baeume' else 0.12*h)+0.05:c['wasser']+=1;continue
            if nm=='baeume':
                cx,cz=int(min(NX-1,x)),int(min(NY-1,z))
                if sper[max(0,cz-0):cz+1,max(0,cx):cx+1].any() or any(abs(x-hh['x'])<hh['b']/2+1 and abs(z-hh['z'])<hh['t']/2+1 for hh in haeuser) \
                   or any(np.hypot(x-p[0],z-p[1])<1.5 for w in rampen for p in w) or any(np.hypot(x-b[0],z-b[2])<2.5 for b in bruecken):c['ueberlapp']+=1;continue
            neu.append(o)
        if nm=='baeume':
            neu.sort(key=lambda o:-o[3]);from scipy.spatial import cKDTree;P=np.array([[o[0],o[2]] for o in neu]);T=cKDTree(P);weg=np.zeros(len(neu),bool)
            for k,o in enumerate(neu):
                if weg[k]:continue
                for m in T.query_ball_point(P[k],0.05*(o[3]+12)):
                    if m>k and not weg[m] and np.hypot(*(P[m]-P[k]))<0.05*(o[3]+neu[m][3]):weg[m]=True
            c['abstand']=int(weg.sum());neu=[o for k,o in enumerate(neu) if not weg[k]]
        c['n_nachher']=len(neu);L[:]=neu;st[nm]=c
    return st
def csv_nachlauf(pfad,WV,GA,NX,NY):
    """Zellen-CSV: deko_baum_ok=0 auf WAND/Wasser; 3 Wasser-Restzellen ohne Anzeige-Wasser (148|0, 188|36, 222-223|202) trocken;
    neue Spalten wasser_anzeige / wasserspiegel_anzeige_m / boden_anzeige_m = Viewer-Stand (Zellmitte) [A]"""
    R=list(csv.DictReader(open(pfad)));K=list(R[0].keys());st={'deko_baum_ok_1_auf_0':[],'wasser_restzelle_trocken':[]}
    ws=np.where(WV>-900,WV,np.nan)
    for r in R:
        x,y=int(r['cx']),int(r['cy'])
        if r['deko_baum_ok']=='1' and (r['wasser_eis']=='1' or r['klippe']=='WAND'):r['deko_baum_ok']='0';st['deko_baum_ok_1_auf_0'].append([x,y])
        if (x,y) in [(148,0),(188,36),(222,202),(223,202)] and r['wasser_eis']=='1':
            st['wasser_restzelle_trocken'].append([x,y,r['untergrund'],r['fluss_id'],r['wasserspiegel_m']])
            nb=[R[yy*NX+xx] for yy in range(max(0,y-1),min(NY,y+2)) for xx in range(max(0,x-1),min(NX,x+2)) if R[yy*NX+xx]['wasser_eis']=='0']
            ugn=max(set(q['untergrund'] for q in nb),key=[q['untergrund'] for q in nb].count) if nb else r['untergrund_c20']
            r.update(wasser_eis='0',untergrund=ugn,untergrund_quelle='relief_t65u',fluss_id='',fliess_richtung='',fluss_breite_m='',wasser_tiefe_m='0.0',wasserspiegel_m='',skin_slot='ug_'+ugn.lower() if r['skin_slot']!='wand_fels' else 'wand_fels')
        sub=ws[y*2:y*2+3,x*2:x*2+3];w=np.isfinite(sub).any()
        r['wasser_anzeige']='1' if w else '0';r['wasserspiegel_anzeige_m']=str(round(float(np.nanmax(sub)),2)) if w else '';r['boden_anzeige_m']=str(round(float(GA[y*2+1,x*2+1]),2))
    K2=K+[k for k in ['wasser_anzeige','wasserspiegel_anzeige_m','boden_anzeige_m'] if k not in K]
    with open(pfad,'w',newline='') as f:
        w=csv.writer(f);w.writerow(K2);[w.writerow([r[k] for k in K2]) for r in R]
    return {k:(len(v) if isinstance(v,list) else v) for k,v in st.items()},st
def mini_senken(WV,aus=(563,672),tol=0.02):
    """Priority-Flood vom Auslass (Ostrand z281,5): Mulden im Spiegel < tol (Rundung) auf Ueberlaufhoehe -> nirgends bergauf; tiefe Becken (See -3 m) bleiben [A]"""
    import heapq;WV=WV.copy();w=WV>-900;lab,_=nd.label(w,np.ones((3,3)));m=lab==lab[aus];sp=np.full(WV.shape,np.inf);sp[aus]=WV[aus];pq=[(WV[aus],aus)];n=0;orte=[]
    while pq:
        s,p=heapq.heappop(pq)
        if s>sp[p]:continue
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                r=(p[0]+dy,p[1]+dx)
                if 0<=r[0]<WV.shape[0] and 0<=r[1]<WV.shape[1] and m[r] and sp[r]==np.inf:
                    sp[r]=max(WV[r],s);heapq.heappush(pq,(sp[r],r))
    d=np.where(m,sp-WV,0);k=(d>1e-6)&(d<tol);WV[k]=sp[k];j,i=np.nonzero(k)
    return WV,{'mulden_angehoben':int(k.sum()),'max_m':round(float(d[k].max()) if k.any() else 0,4),'orte_xz':[[i_/2,j_/2] for i_,j_ in zip(i[:20],j[:20])],'tiefe_becken_bleiben_punkte':int(((d>=tol)&m).sum())}
def tuempel_eben(WV,GA):
    """Tuempel x11-38 z40-60 (Senke, kein Abfluss moeglich: 2 m unter dem Bach 16,8 m oestlich): Spiegel war um 0,6 m geneigt -> eben auf -9,45, Zulauf bleibt [A]"""
    WV=WV.copy();lab,_=nd.label(WV>-900,np.ones((3,3)));w_=np.where(lab[78:122,20:80]>0,WV[78:122,20:80],99);jj,ii=np.unravel_index(w_.argmin(),w_.shape);k=lab[78+jj,20+ii];s=np.s_[:,:];sw=WV;sg=GA;p=(lab==k)&(WV<-8.95);L=-9.45;assert k>0 and (lab==k).sum()<2000,(lab==k).sum()
    nass=p&(sg<L-0.03);tro=p&~nass;sw[nass]=L;sw[tro]=-999.0
    return WV,{'eben_auf':L,'punkte':int(nass.sum()),'trocken':int(tro.sum())}
def strahl_hoehe(L5,pfad='pruefung/strahl_hoehe_t65u.json'):
    """Hoehe aus Browser-Raycast gegen das echte Viewer-Netz (test_strahl_t62u.js), weil Feinband/Wandnetz Vertices verschiebt und das GA-Gitter dort bis 1,3 m abweicht.
    Baeume: y=Treffer+0,3 (Fuss auf Boden); Steine/Felsen: Versatz zum Treffer auf [-0,25h, 0] begrenzt (kein Schweben, Einbettung wie gewollt) [S]"""
    import json,os
    if not os.path.exists(pfad):return L5,{'datei':'fehlt'}
    H=json.load(open(pfad));st={}
    for nm,L in L5.items():
        c=0;h_=H.get(nm,{});rr={k for n_,k in H.get('raus',[]) if n_==nm};n0=len(L);L[:]=[o for o in L if f"{o[0]:.3f}|{o[2]:.3f}" not in rr];st[nm+'_raus']=n0-len(L)
        for o in L:
            g=h_.get(f"{o[0]:.3f}|{o[2]:.3f}")
            if g is None:continue
            y=g+0.3 if nm=='baeume' else g+min(0.0,max(-0.25*o[3],o[1]-g))
            if abs(y-o[1])>0.005:o[1]=round(y,3);c+=1
        st[nm]=c
    return L5,st
