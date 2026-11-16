# P2b-Zusatz (QA P4c W2): Wege G011 enden in E2 beidseits am Bach mit Brettstummeln (bruecken-Zellen 186|73-75 und 196-197|72-75),
# die Bruecke dazwischen fehlt. vektor.json sieht keine Furt vor (G011 Teil 1/2, wegenden ziel 'gelaende').
# Ergaenzt die Brueckenzellen x 187..195, z 74..75 im bestehenden Stil (Zellmitte, Deck y = 0,3 wie G014). Idempotent.
import sys,json,gzip,pathlib
sys.path.insert(0,'.');import relief_l3 as L3
NEU=[[x+.5,0.3,z+.5] for z in (74,75) for x in range(187,196)]
for pfad,kompakt in (('relief_daten.json.gz',False),('neu/relief_neu.json.gz',True)):
    D=json.load(gzip.open(pfad));alt={(b[0],b[2]) for b in D['bruecken']};n=0
    for b in NEU:
        if (b[0],b[2]) not in alt: D['bruecken'].append(b);n+=1
    L3._schreibe(D,pathlib.Path(pfad),kompakt);print(pfad,'bruecken +',n,'=',len(D['bruecken']))
