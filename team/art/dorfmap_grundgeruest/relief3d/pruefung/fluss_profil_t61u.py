# t61u: Laengsprofil Wasserspiegel Quelle -> Muendung je Gewaesserstrang + Bergauf-Stellen [A]
# Aufruf: python3 pruefung/fluss_profil_t61u.py <diag.npz> <png> <json>   (npz aus DIAG=... python3 gen_relief.py)
# Weg: kuerzeste Wege im Wassernetz zur Muendung (tiefster Punkt / Kartenrand). Hauptstrang = laengster Weg.
# bergauf = Wasserspiegel steigt in Fliessrichtung (zum Vorgaenger Richtung Muendung) [S]
import sys,json,numpy as np,scipy.ndimage as nd
sys.path.insert(0,'.');from fluss_t61u import _graph
from scipy.sparse.csgraph import dijkstra
import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
d=np.load(sys.argv[1]);res={}
fig,axs=plt.subplots(4,2,figsize=(16,15))
for col,(kw,kg,tit) in enumerate((('WV_ALT','G_ALT','vorher'),('WV','G','nachher'))):
    WV=d[kw].astype(float);G=d[kg].astype(float);M=WV>-900;lab,n=nd.label(M,np.ones((3,3)));sz=nd.sum(M,lab,range(1,n+1))
    R={'komponenten':int(n),'kleinstteile_unter_20':int((sz<20).sum())};worst=(0.0,None,None);allv=0;nbad=0
    for c in range(1,n+1):
        m=lab==c
        if m.sum()<4:continue
        idx,P,g=_graph(m);out=np.zeros(m.shape,bool);out[0,:]=out[-1,:]=out[:,0]=out[:,-1]=True
        src=list(np.flatnonzero((out&m)[m]));src.append(int(np.argmin(WV[m])))
        s,pred,_=dijkstra(g,directed=False,indices=src,return_predecessors=True,min_only=True)
        w=WV[m];ok=pred>=0;up=np.zeros(len(w));up[ok]=w[pred[ok]]-w[ok]      # >0: stromab hoeher = bergauf
        allv+=len(w);nbad+=int((up>0.02).sum())
        # Bergauf-Hoehe ueber Weg kumuliert: wieviel steigt der Spiegel von Punkt v bis zur Muendung maximal an
        o=np.argsort(s);cm=w.copy()
        for v in o:
            p=pred[v]
            if p>=0:cm[v]=max(cm[p],w[v]) if False else max(cm[p],w[p])   # hoechster Spiegel stromab
        rise=cm-w;i=int(np.argmax(rise))
        if rise[i]>worst[0]:worst=(float(rise[i]),[float(P[i][1]/2),float(P[i][0]/2)],int(c))
        if m.sum()>=1000 and col>=0:
            k=int(np.argmax(np.where(np.isfinite(s),s,-1)));path=[k]
            while pred[path[-1]]>=0:path.append(pred[path[-1]])
            pp=P[path];ss=s[k]-s[path]
            nm=f'strang_{c}_{tit}';ax=axs[len([x for x in R if x.startswith('strang')])%4,col]
            ax.plot(ss,WV[pp[:,0],pp[:,1]],label='Wasserspiegel');ax.plot(ss,G[pp[:,0],pp[:,1]],'--',lw=0.8,label='Flussbett');ax.set_title(f'{tit}: Strang {c} von ({pp[0,1]/2:.0f},{pp[0,0]/2:.0f}) bis ({pp[-1,1]/2:.0f},{pp[-1,0]/2:.0f})')
            dw=np.diff(WV[pp[:,0],pp[:,1]]);j=int(np.argmax(dw)) if len(dw) else 0
            if len(dw) and dw[j]>0.02:ax.annotate(f'bergauf +{dw[j]:.2f} m',(ss[j],WV[pp[j,0],pp[j,1]]),color='r')
            ax.set_xlabel('Strecke ab Quelle [m]');ax.set_ylabel('Hoehe [m]');ax.grid(alpha=.3);ax.legend(fontsize=8)
            R[nm]={'laenge_m':round(float(ss[-1]),1),'quelle_m':round(float(WV[pp[0,0],pp[0,1]]),2),'muendung_m':round(float(WV[pp[-1,0],pp[-1,1]]),2),
                   'anstiege_gt_2cm':int((dw>0.02).sum()),'max_anstieg_m':round(float(max(dw.max(),0)),2),'max_anstieg_bei_xz':[float(pp[j,1]/2),float(pp[j,0]/2)],
                   'bett_ueber_spiegel':int((G[pp[:,0],pp[:,1]]>WV[pp[:,0],pp[:,1]]-0.01).sum())}
    R.update({'wasser_vertices':allv,'vertices_stromab_hoeher_gt_2cm':nbad,'max_bergauf_m':round(worst[0],2),'max_bergauf_ort_xz':worst[1],'max_bergauf_komponente':worst[2],
              'boden_ueber_wasser_vertices':int((M&(G>WV-0.01)).sum())})
    res[tit]=R
fig.tight_layout();fig.savefig(sys.argv[2],dpi=80);print(json.dumps(res,indent=1,ensure_ascii=False));json.dump(res,open(sys.argv[3],'w'),indent=1,ensure_ascii=False)
