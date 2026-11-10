# t63u: strenge Gefaelle-Pruefung des Wasserspiegels (auch ueber Wasserscheiden) [S]
# Je Wasserstueck: Auslass = tiefster Randpunkt (Kartenrand), sonst tiefster Punkt (Endsee).
# Priority-Flood vom Auslass: S = noetiger Spiegel, damit alles Wasser zum Auslass fliessen kann.
# bergauf = S - WV > 2 cm (Wasser liegt hinter einer Schwelle / Wasserscheide).
import json,gzip,base64,sys,heapq,numpy as np,scipy.ndimage as nd
D=json.load(gzip.open(sys.argv[1] if len(sys.argv)>1 else 'relief_daten.json.gz'));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(GY,GX).astype(float);M=WV>-900
lab,n=nd.label(M,np.ones((3,3)));ed=np.zeros(M.shape,bool);ed[0,:]=ed[-1,:]=ed[:,0]=ed[:,-1]=True
out={'stuecke':int(n),'je_stueck':[]};BA=np.zeros(M.shape)
for k in range(1,n+1):
    m=lab==k;idx=np.argwhere(m);sz=len(idx)
    e=m&ed;
    if e.any():o=tuple(np.argwhere(e)[np.argmin(WV[e])]);art='rand'
    else:o=tuple(idx[np.argmin(WV[m])]);art='endsee'
    S=np.full(M.shape,np.inf);S[o]=WV[o];h=[(WV[o],o)];
    while h:
        s,(y,x)=heapq.heappop(h)
        if s>S[y,x]:continue
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                yy,xx=y+dy,x+dx
                if (dy or dx) and 0<=yy<GY and 0<=xx<GX and m[yy,xx]:
                    v=max(WV[yy,xx],s)
                    if v<S[yy,xx]:S[yy,xx]=v;heapq.heappush(h,(v,(yy,xx)))
    r=np.where(m,S-WV,0);BA=np.maximum(BA,r);nb=int((r>0.02).sum())
    out['je_stueck'].append({'nr':k,'ecken':sz,'auslass':art,'auslass_xz':[round(o[1]/RS,1),round(o[0]/RS,1)],'auslass_wv':round(float(WV[o]),2),'bergauf_ecken_gt_2cm':nb,'bergauf_max_m':round(float(r.max()),2),
        'spiegel_von_bis':[round(float(WV[m].max()),2),round(float(WV[m].min()),2)]})
out['bergauf_ecken_gesamt']=sum(s['bergauf_ecken_gt_2cm'] for s in out['je_stueck']);out['bergauf_max_m']=max(s['bergauf_max_m'] for s in out['je_stueck'])
if len(sys.argv)>2:np.save(sys.argv[2],BA.astype(np.float32))
print(json.dumps(out))
