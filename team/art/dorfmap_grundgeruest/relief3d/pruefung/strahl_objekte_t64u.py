# t64u: Objekt-Raycast gegen das echte Viewer-Netz. 1) pts: python3 ... pts out.json  2) node test_strahl_t62u.js (PTS=out.json)  3) python3 ... werte strahl.json [S]
import json,gzip,sys
D=json.load(gzip.open('relief_daten.json.gz'));K=(('baeume',0.3),('felsen',0),('findlinge',0),('steine',0),('geroell',0))
if sys.argv[1]=='pts':json.dump({k:[[o[0],o[2]] for o in (D.get(k) or [])] for k,_ in K},open(sys.argv[2],'w'));sys.exit()
S=json.load(open(sys.argv[2]));R={}
for k,u in K:
    L=D.get(k) or [];c=dict(n=len(L),ohne_treffer=0,schwebend_gt_0_3m=0,versunken_gt_tol=0,im_wasser_gt_0_05m=0,max_abw_m=0.0)
    for o,(g,w) in zip(L,S[k]):
        if g is None:c['ohne_treffer']+=1;continue
        d=o[1]-u-g;tol=0.5 if k=='baeume' else max(0.5,0.6*o[3])
        c['schwebend_gt_0_3m']+=d>0.3;c['versunken_gt_tol']+=d<-tol
        if w is not None and w>g+0.05 and w>o[1]-u+0.05:c['im_wasser_gt_0_05m']+=1
        c['max_abw_m']=max(c['max_abw_m'],round(abs(d),2))
    R[k]=c
print(json.dumps(R))
