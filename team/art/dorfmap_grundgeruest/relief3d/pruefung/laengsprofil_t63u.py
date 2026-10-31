# t63u Runde K [S]: Laengsprofil aller Flussstraenge (Wasserstuecke >=200 Ecken) aus relief_daten.json.gz
# Je Stueck: Auslass wie pruefe_gefaelle_t63u (tiefster Randpunkt, sonst Endsee), Fliessbaum per Priority-Flood,
# laengster Weg Quelle->Auslass; Bergauf = Anstieg entlang dieses Weges in Fliessrichtung (>2 cm), Stufen = Sprung zwischen Nachbarecken.
# Aufruf: python3 laengsprofil_t63u.py daten.json.gz ausgabe.png ausgabe.json [Titel]
import json,gzip,base64,sys,heapq,numpy as np,scipy.ndimage as nd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
D=json.load(gzip.open(sys.argv[1]));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
f=lambda k:np.frombuffer(base64.b64decode(D[k]),np.float32).reshape(GY,GX).astype(float)
WV=f('WV');G=f('GB') if D.get('GB') else f('G');M=WV>-900
gy,gx=np.gradient(G,1/RS);STEIL=nd.binary_dilation(np.degrees(np.arctan(np.hypot(gx,gy)))>55,iterations=4)  # Wandband/Schlucht
lab,n=nd.label(M,np.ones((3,3)));ed=np.zeros(M.shape,bool);ed[0,:]=ed[-1,:]=ed[:,0]=ed[:,-1]=True
R=[];fig=plt.figure(figsize=(16,10));ax=fig.add_subplot(111);cm=plt.get_cmap('tab20')
for k in range(1,n+1):
    m=lab==k;sz=int(m.sum())
    if sz<200:continue
    e=m&ed;o=tuple(np.argwhere(e)[np.argmin(WV[e])]) if e.any() else tuple(np.argwhere(m)[np.argmin(WV[m])]);art='rand' if e.any() else 'endsee'
    S=np.full(M.shape,np.inf);P=-np.ones(M.shape+(2,),int);L=np.zeros(M.shape);S[o]=WV[o];h=[(WV[o],0.0,o)]
    while h:
        s,l,(y,x)=heapq.heappop(h)
        if s>S[y,x]:continue
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                yy,xx=y+dy,x+dx
                if (dy or dx) and 0<=yy<GY and 0<=xx<GX and m[yy,xx]:
                    v=max(WV[yy,xx],s)
                    if v<S[yy,xx]:S[yy,xx]=v;P[yy,xx]=(y,x);L[yy,xx]=l+np.hypot(dy,dx)/RS;heapq.heappush(h,(v,L[yy,xx],(yy,xx)))
    q=tuple(np.argwhere(m)[np.argmax(np.where(m,L,-1)[m])]);pfad=[q]
    while pfad[-1]!=o and P[pfad[-1]][0]>=0:pfad.append(tuple(P[pfad[-1]]))
    pf=np.array(pfad);w=WV[pf[:,0],pf[:,1]];g=G[pf[:,0],pf[:,1]];d=L[pf[:,0],pf[:,1]];dz=w[:-1]-w[1:]   # dz>0 = faellt
    st=STEIL[pf[:-1,0],pf[:-1,1]]
    # Stufen im ganzen Stueck (Fliessbaum-Kanten)
    yy,xx=np.nonzero(m&(P[...,0]>=0));sd=WV[yy,xx]-WV[P[yy,xx,0],P[yy,xx,1]];sst=STEIL[yy,xx]
    r={'nr':k,'ecken':sz,'auslass':art,'auslass_xz':[o[1]/RS,o[0]/RS],'quelle_xz':[q[1]/RS,q[0]/RS],'laenge_m':round(float(d[0]),1),
       'spiegel_quelle':round(float(w[0]),2),'spiegel_auslass':round(float(w[-1]),2),'bergauf_entlang_pfad_gt_2cm':int((dz<-0.02).sum()),
       'bergauf_ueber_wasserscheide_ecken_gt_2cm':int((np.where(m,S-WV,0)>0.02).sum()),
       'stufen_gt_1m_ausserhalb_schlucht':int(((sd>1.0)&~sst).sum()),'stufen_gt_1m_in_schlucht_wandband':int(((sd>1.0)&sst).sum()),
       'stufe_max_ausserhalb_schlucht_m':round(float(sd[~sst].max()) if (~sst).any() else 0,2),'stufe_max_m':round(float(sd.max()),2),'stufen_gt_0_3m':int((sd>0.3).sum())}
    R.append(r);c=cm(len(R)%20)
    ax.plot(d[0]-d,w,color=c,lw=1.6,label=f"Stueck {k} ({sz} Ecken) Quelle x{q[1]/RS:.0f} z{q[0]/RS:.0f} -> {art} x{o[1]/RS:.0f} z{o[0]/RS:.0f}")
    ax.plot(d[0]-d,g,color=c,lw=0.6,ls=':')
ax.set_xlabel('Laufweg ab Quelle [m]');ax.set_ylabel('Hoehe [m]  (durchgezogen = Wasserspiegel, gepunktet = Grund)');ax.grid(alpha=.3);ax.legend(fontsize=8)
ax.set_title(sys.argv[4] if len(sys.argv)>4 else 'Laengsprofile');fig.tight_layout();fig.savefig(sys.argv[2],dpi=80)
Z={'stuecke_ge200':len(R),'bergauf_summe':sum(r['bergauf_ueber_wasserscheide_ecken_gt_2cm'] for r in R),'bergauf_pfad_summe':sum(r['bergauf_entlang_pfad_gt_2cm'] for r in R),
   'stufen_gt_1m_ausserhalb_schlucht':sum(r['stufen_gt_1m_ausserhalb_schlucht'] for r in R),'stufen_gt_1m_schlucht':sum(r['stufen_gt_1m_in_schlucht_wandband'] for r in R),'je_stueck':R}
json.dump(Z,open(sys.argv[3],'w'),indent=1);print(json.dumps({k:v for k,v in Z.items() if k!='je_stueck'}))
