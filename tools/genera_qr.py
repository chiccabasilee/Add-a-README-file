"""Genera il QR del menu con il logo al centro.

Uso:  python3 tools/genera_qr.py https://indirizzo-del-menu [cartella_output]
Crea menu-qr.svg, vettoriale: va bene per qualsiasi dimensione di stampa.
Richiede: pip install segno
"""
import re
import sys
from pathlib import Path

import segno

ROOT = Path(__file__).resolve().parent.parent
url = sys.argv[1]
out = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "qr"
out.mkdir(parents=True, exist_ok=True)

# Correzione d'errore H: il codice resta leggibile anche con il logo sopra
qr = segno.make(url, error="h", boost_error=False)
matrix = [list(r) for r in qr.matrix]
n = len(matrix)
quiet = 4
size = n + 2 * quiet

# Zona centrale lasciata libera per il logo (circa 22% del lato)
logo_mod = round(n * 0.22) | 1
c0 = (n - logo_mod) // 2
c1 = c0 + logo_mod

d = []
for y, row in enumerate(matrix):
    for x, v in enumerate(row):
        if v and not (c0 - 1 <= x <= c1 and c0 - 1 <= y <= c1):
            d.append(f"M{x + quiet} {y + quiet}h1v1h-1z")

logo = (ROOT / "assets" / "marchio.svg").read_text()
logo_inner = re.search(r"<svg[^>]*>(.*)</svg>", logo, re.S).group(1)
cx = quiet + n / 2
scale = logo_mod / 1000

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" shape-rendering="crispEdges">
<rect width="{size}" height="{size}" fill="#fff"/>
<path fill="#0d0d0d" d="{''.join(d)}"/>
<g transform="translate({cx - logo_mod / 2} {cx - logo_mod / 2}) scale({scale})" shape-rendering="geometricPrecision">{logo_inner}</g>
</svg>
'''
(out / "menu-qr.svg").write_text(svg)
print(f"QR {n}x{n} moduli -> {out / 'menu-qr.svg'}")
