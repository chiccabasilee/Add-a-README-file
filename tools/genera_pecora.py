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
SMUSSO = 1.2     # raggio degli angoli: basso, per restare spigolosa
TESTA = -16      # inclinazione della testa in gradi (negativo = muso in giù)


def orecchio(ox, oy, s):
    # orecchio destro del logo (coordinate di marchio.svg)
    pts = [(695, 268), (759, 284), (785, 307), (817, 337), (817, 356), (734, 378), (697, 362)]
    return [(ox + (x - 700) * s, oy + (y - 320) * s) for x, y in pts]


def testa(pts, c=(385, 300), gradi=TESTA, scala=1.05, dx=10, dy=78):
    # la testa si disegna attorno alla nuca, poi si inclina, si ingrandisce e si abbassa
    a = math.radians(gradi)
    ca, sa = math.cos(a) * scala, math.sin(a) * scala
    return [(c[0] + dx + (x - c[0]) * ca - (y - c[1]) * sa,
             c[1] + dy + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def zampa(x0, top, bot, w=54, wb=42):
    # corta e robusta, con lo zoccolo a punta in avanti
    return [(x0, top), (x0 + w, top), (x0 + w - 4, bot), (x0 - 8, bot), (x0 + 2, bot - 26)]


# Dal fondo al primo piano: ogni parte viene staccata da quelle davanti.
# Le zampe stanno dietro al vello, che le copre in alto con le sue punte.
parti = [
    zampa(800, 560, 772),                 # posteriore lontana
    zampa(500, 560, 772),                 # anteriore lontana
    zampa(735, 560, 792),                 # posteriore
    zampa(430, 560, 792),                 # anteriore
    [(894, 436), (930, 470), (906, 536)],                                     # coda
    [(370, 292), (440, 246), (570, 226), (712, 232), (812, 258), (876, 312),
     (912, 420), (896, 520), (858, 604), (816, 662), (770, 614), (706, 670),
     (648, 618), (574, 676), (510, 622), (444, 664), (396, 606), (356, 522),
     (340, 420)],                                                             # corpo
    testa(orecchio(400, 318, 0.8)),
    testa([(146, 428), (200, 380), (382, 290), (398, 362), (322, 446), (198, 478)]),  # guancia e muso
    testa([(178, 392), (250, 244), (306, 218), (354, 226), (382, 268),
           (376, 306), (326, 318)]),                                          # fronte e ciuffo
]
CORPO = 5
# Tagli a cuneo nel vello, larghi in alto e a punta in basso come la riga centrale del logo
tagli_corpo = unary_union([
    Polygon([(470, 236), (496, 232), (440, 560)]),
    Polygon([(612, 222), (640, 222), (600, 600)]),
    Polygon([(760, 240), (788, 248), (812, 590)]),
])

forme = []
for i, pts in enumerate(parti):
    g = Polygon(pts)
    davanti = unary_union([Polygon(q) for q in parti[i + 1:]])
    if not davanti.is_empty:
        g = g.difference(davanti.buffer(TAGLIO, join_style="mitre"))
    if i == CORPO:
        g = g.difference(tagli_corpo)
    g = g.buffer(-SMUSSO).buffer(SMUSSO)
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
