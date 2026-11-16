# sha256 des Viewer-Bundles in index.html (Text zwischen 'RELIEF_NEU_VIEWER=1;</script><script>' und dem letzten '</script>')
import sys,hashlib
for p in sys.argv[1:]:
    s=open(p,'rb').read(); m=b'window.RELIEF_NEU_VIEWER=1;</script><script>'; a=s.index(m)+len(m); e=s.rindex(b'</script>')
    print(hashlib.sha256(s[a:e]).hexdigest(), e-a, p)
