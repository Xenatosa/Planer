# t34u: Regelpruefung aller Zellen (z25/z50) gegen die Feldregeln [R]
import csv,sys,json,collections
for z in (25,50):
    R=list(csv.DictReader(open(f'raster_c20_z{z}_zellen.csv'))); F=collections.Counter()
    NB={'UNBEKANNT','WALD','KLIPPE_WAND','KLIPPE_KANTE','FELS','WASSER_EIS'}
    ST={'SENKE':0,'PLATEAU_NORD':8.6,'TAL_SUED':-7.6,'OSTPLATEAU':6.7,'KRATER':0,'GIPFEL':7.6}
    for r in R:
        u=r['untergrund']; e=r['ebene']; h=float(r['hoehe_m']) if r['hoehe_m'] else None
        if not e: F['ebene leer']+=1
        if (u in NB or r['hindernis_id']!='0')==(r['begehbar']=='1'): F['begehbar falsch']+=1
        if r['bebaubar']=='1' and (r['begehbar']!='1' or r['senke_becken']!='1' or u not in('SCHNEE','BODEN','SAND')): F['bebaubar falsch']+=1
        if r['bebaubar']=='1' and r['bebaubar_erweitert']!='1': F['bebaubar nicht in erweitert']+=1
        if r['bebaubar_erweitert']=='1' and r['begehbar']!='1': F['erweitert nicht begehbar']+=1
        if (u in('KLIPPE_WAND','KLIPPE_KANTE'))!=(e=='WAND'): F['WAND passt nicht zu klippe']+=1
        if (u=='WASSER_EIS')!=(r['wasser_eis']=='1'): F['wasser_eis Flag']+=1
        if e in ST and h is not None and r['senke_becken']!='1' and abs(h-ST[e])>0.51: F[f'hoehe passt nicht zu {e}']+=1
        if r['senke_becken']=='1' and e!='SENKE' and e!='WAND': F['senke_becken nicht SENKE']+=1
        if e=='HANG' and h is not None and not (-7.61<=h<=8.61): F['HANG hoehe ausserhalb']+=1
        if r['ebene_hoeher']!=('1' if e in('PLATEAU_NORD','OSTPLATEAU','GIPFEL') else '0'): F['ebene_hoeher']+=1
    print(z,len(R),dict(F) or 'keine Verstoesse')
