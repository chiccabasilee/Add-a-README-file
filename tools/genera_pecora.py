"""Disegna la pecora intera di profilo, nello stile della testa del logo.

Uso:  python3 tools/genera_pecora.py
Crea in assets/: pecora.svg (nera), pecora-bianco.svg (crema, per sfondi scuri)
e pecora-marchio.svg (pecora crema in un cerchio nero, come marchio.svg).
Richiede: pip install shapely

Ogni parte è un poligono a spigoli vivi; i tagli bianchi tra le parti e gli
angoli appena smussati riprendono la testa del logo. L'orecchio è quello del
logo, rimpicciolito.
"""
import math
from pathlib import Path

from shapely.geometry import Polygon
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent.parent
NERO, CREMA = "#0d0d0d", "#f2efe9"
TAGLIO = 8       # larghezza dei tagli tra le parti
SMUSSO = 3       # raggio degli angoli
TESTA = -10      # inclinazione della testa in gradi (negativo = muso in giù)


def orecchio(ox, oy, s):
    # orecchio destro del logo (coordinate di marchio.svg)
    pts = [(695, 268), (759, 284), (785, 307), (817, 337), (817, 356), (734, 378), (697, 362)]
    return [(ox + (x - 700) * s, oy + (y - 320) * s) for x, y in pts]


def ruota(pts, gradi, c=(385, 300)):
    a = math.radians(gradi)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def zampa(x0, top, bot, w=36, wb=24, ginocchio=0):
    # affusolata, con un leggero angolo al ginocchio e lo zoccolo smussato davanti
    k = top + (bot - top) * 0.55
    wk = (w + wb) / 2 + 2
    return [(x0, top), (x0 + w, top), (x0 + w - 6 - ginocchio, k), (x0 + w - 10, bot),
            (x0 + w - 4 - wb, bot), (x0 + w - 10 - wb, bot - 8), (x0 + w - 6 - ginocchio - wk, k)]


# Dal fondo al primo piano: ogni parte viene staccata da quelle davanti
parti = [
    zampa(752, 540, 788, ginocchio=-8),   # posteriore lontana
    zampa(478, 540, 788, ginocchio=6),    # anteriore lontana
    [(350, 330), (420, 290), (560, 272), (720, 277), (830, 312), (885, 392),
     (880, 482), (830, 560), (700, 592), (470, 592), (385, 562), (345, 470)],   # corpo
    zampa(712, 540, 800, ginocchio=-8),   # posteriore
    zampa(432, 540, 800, ginocchio=6),    # anteriore
    [(878, 420), (905, 438), (906, 500), (884, 512)],                         # coda
    ruota(orecchio(400, 318, 0.8), TESTA / 2),
    ruota([(162, 404), (200, 380), (382, 290), (398, 362), (322, 446),
           (205, 474), (170, 460), (150, 433)], TESTA),                         # guancia e muso
    ruota([(178, 392), (254, 246), (304, 224), (352, 230), (380, 268),
           (376, 306), (326, 318)], TESTA),                                     # fronte e ciuffo
]
CORPO = 2
# Tagli a cuneo nel vello, larghi in alto e a punta in basso come la riga centrale del logo
tagli_corpo = unary_union([
    Polygon([(452, 282), (474, 280), (418, 528)]),
    Polygon([(590, 262), (614, 262), (572, 575)]),
    Polygon([(748, 268), (772, 276), (796, 548)]),
])

forme = []
for i, pts in enumerate(parti):
    g = Polygon(pts)
    davanti = unary_union([Polygon(q) for q in parti[i + 1:]])
    if not davanti.is_empty:
        g = g.difference(davanti.buffer(TAGLIO, join_style="mitre"))
    if i == CORPO:
        g = g.difference(tagli_corpo)
    g = g.buffer(-SMUSSO).buffer(SMUSSO).buffer(SMUSSO * 0.6).buffer(-SMUSSO * 0.6)
    forme.append(g)

tutto = unary_union(forme)
x0, y0, x1, y1 = tutto.bounds


def tracciato(dx, dy, s):
    d = []
    for g in forme:
        for poly in getattr(g, "geoms", [g]):
            for ring in [poly.exterior, *poly.interiors]:
                c = ring.simplify(0.15).coords[:-1]
                d.append("M" + " L".join(f"{(x - dx) * s:.1f} {(y - dy) * s:.1f}" for x, y in c) + "Z")
    return "".join(d)


# Pecora da sola, con un piccolo margine
m = 10
w, h = x1 - x0 + 2 * m, y1 - y0 + 2 * m
d = tracciato(x0 - m, y0 - m, 1)
for nome, colore in [("pecora.svg", NERO), ("pecora-bianco.svg", CREMA)]:
    (ROOT / "assets" / nome).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" '
        f'aria-label="Black Sheep"><path fill="{colore}" d="{d}"/></svg>\n')

# Marchio: pecora crema centrata in un cerchio nero di 1000
s = 640 / (x1 - x0)
cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
d = tracciato(cx - 500 / s, cy - 500 / s, s)
(ROOT / "assets" / "pecora-marchio.svg").write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img" aria-label="Black Sheep">'
    f'<circle cx="500" cy="500" r="500" fill="{NERO}"/><path fill="{CREMA}" d="{d}"/></svg>\n')
print("Creati pecora.svg, pecora-bianco.svg, pecora-marchio.svg in assets/")
