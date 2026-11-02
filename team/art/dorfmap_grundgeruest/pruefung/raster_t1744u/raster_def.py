"""Rasterdefinition t1744u: 8 Spalten (A-H) x 7 Reihen (1-7) ueber 336x303 Zellen (1 Zelle = 25 px = 1 m)."""
import csv, gzip, json, os, math
import numpy as np
HIER=os.path.dirname(os.path.abspath(__file__))
R3D=os.path.join(HIER,'..','..','relief3d')
NX,NY=336,303; NSP,NRE=8,7
SP='ABCDEFGH'
def grenzen(n,k): return [round(i*n/k) for i in range(k+1)]
GX,GY=grenzen(NX,NSP),grenzen(NY,NRE)
def felder():
    out=[]
    for r in range(NRE):
        for s in range(NSP):
            out.append(dict(feld=f'{SP[s]}{r+1}',spalte=SP[s],reihe=r+1,cx0=GX[s],cx1=GX[s+1]-1,cy0=GY[r],cy1=GY[r+1]-1))
    return out
def feld_von(cx,cy):
    s=min(int(np.searchsorted(GX,cx,side='right'))-1,NSP-1); r=min(int(np.searchsorted(GY,cy,side='right'))-1,NRE-1)
    return f'{SP[s]}{r+1}'
def hoehen():
    H=np.zeros((NY,NX))
    with open(os.path.join(R3D,'zellen_relief.csv')) as f:
        for z in csv.DictReader(f): H[int(z['cy']),int(z['cx'])]=float(z['boden_anzeige_m'] or z['hoehe_m'] or 0)
    return H
