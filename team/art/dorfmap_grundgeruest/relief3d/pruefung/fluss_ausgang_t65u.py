# t65u Runde M 3: jedes Gewaesserstueck (Anzeige-WV, 0,5-m-Raster, 8er-Nachbarschaft): Quelle, Ende (Rand/See), Laenge, Gefaelle, lueckenloser Pfad, Monotonie [S]
import json,gzip,base64,sys,numpy as np,scipy.ndimage as nd,heapq
D=json.load(gzip.open(sys.argv[1] if len(sys.argv)>1 else 'relief_daten.json.gz'))
WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(607,673).astype(float);GB=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(607,673).astype(float)
H,Wd=WV.shape;w=WV>-900;lab,n=nd.label(w,np.ones((3,3)));out=[]
rand=np.zeros_like(w);rand[0,:]=rand[-1,:]=rand[:,0]=rand[:,-1]=True
for k in range(1,n+1):
    m=lab==k;js,is_=np.nonzero(m);cnt=len(js)
    hi=np.argmax(WV[m]);lo=np.argmin(WV[m]);q=(js[hi],is_[hi])
    am_rand=m&rand;ende=None
    if am_rand.any():
        jr,ir=np.nonzero(am_rand);e=np.argmin(WV[am_rand]);ende=(jr[e],ir[e]);art='Rand'
    else:ende=(js[lo],is_[lo]);art='Senke/See'
    # Pfad Quelle->Ende ueber Wasserpunkte (Dijkstra, Kosten = Anstieg*100+Schritt), dann Monotonie
    dist={q:0};prev={};pq=[(0,q)];
    while pq:
        c,p=heapq.heappop(pq)
        if p==ende:break
        if c>dist.get(p,1e18):continue
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                r=(p[0]+dy,p[1]+dx)
                if (dy or dx) and 0<=r[0]<H and 0<=r[1]<Wd and m[r]:
                    nc=c+np.hypot(dy,dx)+1e6*max(0,WV[r]-WV[p])
                    if nc<dist.get(r,1e18):dist[r]=nc;prev[r]=p;heapq.heappush(pq,(nc,r))
    pf=[ende]
    while pf[-1]!=q and pf[-1] in prev:pf.append(prev[pf[-1]])
    pf=pf[::-1];zus=pf[0]==q;wv=np.array([WV[p] for p in pf]);anst=np.maximum(0,np.diff(wv));L=float(sum(np.hypot(pf[i+1][0]-pf[i][0],pf[i+1][1]-pf[i][1]) for i in range(len(pf)-1))*0.5)
    # Auslass offen: Wasser am Rand ueber Boden und Randvertex-Boden nicht hoeher als Spiegel
    offen=None
    if art=='Rand':offen=bool(WV[ende]>=GB[ende]-0.01)
    out.append({'id':k,'punkte':cnt,'zellen_ca':round(cnt/4),'quelle_xz':[round(q[1]/2,1),round(q[0]/2,1)],'quelle_spiegel':round(WV[q],2),'ende_art':art,'ende_xz':[round(ende[1]/2,1),round(ende[0]/2,1)],
      'ende_spiegel':round(WV[ende],2),'laenge_m':round(L,1),'gefaelle_m':round(WV[q]-WV[ende],2),'gefaelle_promille':round(1000*(WV[q]-WV[ende])/max(L,0.5),1),
      'pfad_lueckenlos':bool(zus),'anstieg_summe_m':round(float(anst.sum()),3),'anstieg_max_m':round(float(anst.max()) if len(anst) else 0,3),'anstieg_orte_xz':[[pf[q+1][1]/2,pf[q+1][0]/2,round(float(anst[q]),4)] for q in np.nonzero(anst>0.0005)[0][:20]],'auslass_offen':offen,
      'randseite':(['Nord'] if ende[0]==0 else['Sued'] if ende[0]==H-1 else ['West'] if ende[1]==0 else ['Ost'] if ende[1]==Wd-1 else [''])[0] if art=='Rand' else ''})
out.sort(key=lambda o:-o['punkte'])
json.dump({'stuecke':len(out),'liste':out},open(sys.argv[2] if len(sys.argv)>2 else 'pruefung/fluss_ausgang_t65u.json','w'),indent=1,ensure_ascii=False)
for o in out:print(o['id'],o['zellen_ca'],o['quelle_xz'],o['quelle_spiegel'],'->',o['ende_art'],o['randseite'],o['ende_xz'],o['ende_spiegel'],'L',o['laenge_m'],'anst',o['anstieg_summe_m'],o['anstieg_max_m'],'offen',o['auslass_offen'],'lz',o['pfad_lueckenlos'])
