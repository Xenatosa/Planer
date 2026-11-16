# Welche Schluessel unterscheiden sich gegenueber 8e374b0? (Soll: nur VC und FW.c)
import json,gzip,subprocess
for p in ('relief_daten.json.gz','neu/relief_neu.json.gz'):
    A=json.loads(gzip.decompress(subprocess.check_output(['git','show',f'8e374b0:./{p}'])));B=json.load(gzip.open(p))
    print(p,'abweichend:',sorted(k for k in set(A)|set(B) if A.get(k)!=B.get(k)),'FW:',[k for k in A['FW'] if A['FW'][k]!=B['FW'][k]],'neu_mesh_tiles gleich:',A.get('neu_mesh_tiles')==B.get('neu_mesh_tiles'))
