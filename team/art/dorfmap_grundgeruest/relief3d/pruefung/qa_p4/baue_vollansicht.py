# QA P4: baut den Voll-Viewer (main.js + relief_daten.json.gz, ganze Karte) NACH /tmp, ohne das Repo zu aendern.
# Grund: das eingecheckte relief3d/index.html ist der RELIEF_NEU-Prototyp (nur D1/G1/D2); C3/C4/C5/D4/B4 fehlen dort.
# Nutzt den Quelltext von relief3d/baue_html.py unveraendert, ersetzt nur Bundle- und Ausgabepfad (kein Schreiben nach /tmp/w3/bundle_r.js).
# Aufruf: python3 baue_vollansicht.py RELIEF3D_ORDNER AUSGABE.html [relief_daten.json.gz]
import sys,os,re
r3d=os.path.abspath(sys.argv[1]);out=os.path.abspath(sys.argv[2]);daten=os.path.abspath(sys.argv[3]) if len(sys.argv)>3 else None
src=open(os.path.join(r3d,'baue_html.py'),encoding='utf-8').read()
bundle=out+'.bundle.js'
assert src.count('/tmp/w3/bundle_r.js')==2 and "open('index.html','w')" in src
src=src.replace('/tmp/w3/bundle_r.js',bundle).replace("open('index.html','w')",f"open({out!r},'w')")
if daten:src=src.replace("RELIEF_DATEN='neu/relief_neu.json.gz' if RELIEF_NEU else 'relief_daten.json.gz'",f"RELIEF_DATEN={daten!r}")
os.environ.pop('RELIEF_NEU',None);os.chdir(r3d)
exec(compile(src,'baue_html.py(qa_p4)','exec'),{'__name__':'__main__'})
os.remove(bundle)
