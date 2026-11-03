#!/usr/bin/env python3
"""O18z t118u: Zwischenlieferungs-Banner als einklappbare Leiste unten (ueber Fusszeile #ban), nur Darstellung.
Nutzung: python3 pruefung/banner_o18z.py datei.html ...  (ersetzt vorhandenes #o18z_banner, idempotent)"""
import re,sys,html
KURZ='ZWISCHENLIEFERUNG, Gate rot 596/443'
def neu(rest):
    return ('<div id="o18z_banner" style="position:fixed;left:0;right:0;bottom:0;z-index:40;pointer-events:none;'
     'font:11px sans-serif;color:#fff"><div id="o18z_kopf" style="display:inline-block;pointer-events:auto;cursor:pointer;'
     'background:#b00020e6;padding:2px 8px;border-radius:0 6px 0 0;white-space:nowrap">&#9650; '+KURZ+'</div>'
     '<div id="o18z_rest" style="display:none;pointer-events:auto;background:#b00020f0;padding:4px 8px;max-height:35vh;overflow:auto">'+rest+'</div></div>'
     '<script>(function(){var b=document.getElementById("o18z_banner"),k=document.getElementById("o18z_kopf"),r=document.getElementById("o18z_rest");'
     'function p(){var f=document.getElementById("ban");b.style.bottom=(f&&f.offsetHeight?f.offsetHeight:0)+"px";}'
     'k.onclick=function(e){e.stopPropagation();var a=r.style.display=="none";r.style.display=a?"block":"none";k.innerHTML=(a?"&#9660; ":"&#9650; ")+'+repr(KURZ)+';};'
     'addEventListener("resize",p);addEventListener("load",p);setTimeout(p,500);setTimeout(p,4000);p();})();</script>')
for fn in sys.argv[1:]:
    s=open(fn,encoding='utf-8').read()
    i=s.find('<div id="o18z_banner"')
    if i<0: print('kein banner',fn);continue
    t=s.find('ZWISCHENLIEFERUNG O18z',i); rest=s[t:s.find('</div>',t)]
    e=s.rfind('k.innerHTML=(a?')
    j=s.find('</script>',e)+9 if e>i else s.find('</div>',t)+6
    class M: pass
    m=M(); m.start=lambda:i; m.end=lambda:j
    s=s[:m.start()]+neu(rest)+s[m.end():]
    open(fn,'w',encoding='utf-8').write(s); print('ok',fn)
