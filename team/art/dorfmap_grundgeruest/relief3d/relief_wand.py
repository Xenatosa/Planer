"""O18p [F 'geschmolzener Vorhang' -> Wandform neu]: kartenweite Felswand-Geometrie, punktweise fuer Grobnetz UND Feinband.
vorbereiten(G,M,RS,frei) baut Felder (Fuss Hu, Oberkante Ho, Fall-/Streichrichtung, Gewicht); verformen(F,x_m,z_m,h) liefert neue Hoehen.
Strata: kartenweit durchlaufende Baender 1.5-4 m (deterministisch, Seed), je Band Gesims (flach) + Stirn (steil), Gesimstiefe 0.3-1.2 m;
Rippen/Risse: Ridged-Noise, kurz in Streich-, lang in Fallrichtung; Oberkante gerundet und Fuss weicher Auslauf ueber Gewicht sin(pi s);
Mittelhoehe: grossraeumiges Mittel der Verschiebung (Gauss 4 m) wird abgezogen. Keine Zufallsquelle ausser default_rng(seed)."""
import numpy as np, scipy.ndimage as nd
P=dict(band_min=2.5,band_max=4.0,gesims=0.55,stirn_exp=3.0,stufe=1.0,rippe=0.5,rippe_lam=5.0,rand=1.5,wexp=1.5,seed=1817)   # O18p V3: Gesimse breiter, Rippen schwaecher/laenger (V2 wirkte wie Vorhangfalten)
def vorbereiten(G,M,RS,frei,P=P):
    G=np.asarray(G,float);rng=np.random.default_rng(int(P['seed']));Mf=M&frei;k=int(3*RS)
    Hu=nd.grey_erosion(np.where(M,G,1e9),size=2*k+1);Ho=nd.grey_dilation(np.where(M,G,-1e9),size=2*k+1)
    Hu=nd.gaussian_filter(np.where(M,Hu,G),RS);Ho=nd.gaussian_filter(np.where(M,Ho,G),RS)
    gr=[np.floor(G.min())-5]
    while gr[-1]<G.max()+5:gr.append(gr[-1]+rng.uniform(P['band_min'],P['band_max']))
    gs=nd.gaussian_filter(G,2*RS);gy,gx=np.gradient(gs);nn=np.hypot(gx,gy)+1e-9
    dist=nd.distance_transform_edt(Mf)/RS;wr=nd.gaussian_filter(np.clip(dist/P['rand'],0,1)*Mf,0.6)
    ph=nd.gaussian_filter(rng.standard_normal((64,64)),1.5);ph/=ph.std()
    return dict(RS=RS,Hu=Hu,Ho=Ho,gr=np.array(gr),ux=-gy/nn,uy=gx/nn,wr=wr,ph=ph,P=dict(P))
def _at(A,x,z,RS,o=1):return nd.map_coordinates(A,[np.asarray(z)*RS,np.asarray(x)*RS],order=o,mode='nearest')
def _roh(F,x,z,h):
    P=F['P'];RS=F['RS'];Hu=_at(F['Hu'],x,z,RS);Ho=_at(F['Ho'],x,z,RS);wr=_at(F['wr'],x,z,RS)
    s=np.clip((h-Hu)/np.maximum(Ho-Hu,0.5),0,1);gr=F['gr'];i=np.clip(np.searchsorted(gr,h)-1,0,len(gr)-2);b0=gr[i];bh=gr[i+1]-b0;t=(h-b0)/bh
    gs=P['gesims']*(0.7+0.6*((i*0.6180339)%1))
    f=np.where(t<gs,t*0.05,0.05*gs+(1-0.05*gs)*np.clip((t-gs)/(1-gs),0,1)**(1/P['stirn_exp']))
    d=(b0+bh*f-h)*P['stufe']
    ux=_at(F['ux'],x,z,RS);uy=_at(F['uy'],x,z,RS);lam=P['rippe_lam'];u=(x*ux+z*uy)/lam;v=(x*uy-z*ux)/(lam*4)
    smp=lambda a,b:nd.map_coordinates(F['ph'],[np.mod(a,64),np.mod(b,64)],order=3,mode='grid-wrap')
    rid=0.65*(1-np.abs(smp(u,v)))+0.35*(1-np.abs(smp(u*2.1+17,v*1.7+5)))-0.62
    d=d+P['rippe']*rid
    return d*np.sin(np.pi*s)**P['wexp']*wr
def verformen_grob(F,G):
    RS=F['RS'];yy,xx=np.mgrid[0:G.shape[0],0:G.shape[1]];d=_roh(F,(xx/RS).ravel(),(yy/RS).ravel(),np.asarray(G,float).ravel()).reshape(G.shape)
    F['mittel']=nd.gaussian_filter(d,4*RS)*F['wr'];return G+d-F['mittel'],d-F['mittel']
def verformen_fein(F,x,z,h):return h+_roh(F,x,z,h)-_at(F['mittel'],x,z,F['RS'])
