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
TESTA = -4       # inclinazione della testa in gradi (negativo = muso in giù)


def orecchio(ox, oy, s):
    # orecchio destro del logo (coordinate di marchio.svg)
    pts = [(695, 268), (759, 284), (785, 307), (817, 337), (817, 356), (734, 378), (697, 362)]
    return [(ox + (x - 700) * s, oy + (y - 320) * s) for x, y in pts]


def testa(pts, c=(385, 300), gradi=TESTA, scala=0.74, dx=-72, dy=30):
    # la testa si disegna attorno alla nuca, poi si inclina, si scala e si sposta sul collo
    a = math.radians(gradi)
    ca, sa = math.cos(a) * scala, math.sin(a) * scala
    return [(c[0] + dx + (x - c[0]) * ca - (y - c[1]) * sa,
             c[1] + dy + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def anteriore(x, top, bot):
    # dritta, con il ginocchio appena segnato e lo zoccolo a punta in avanti
    k = top + (bot - top) * 0.5
    return [(x, top), (x + 50, top), (x + 44, k), (x + 42, bot), (x + 4, bot),
            (x - 4, bot - 20), (x + 6, k)]


def posteriore(x, top, bot):
    # coscia larga, garretto che piega all'indietro, stinco che torna in avanti
    h = top + (bot - top) * 0.55
    return [(x, top), (x + 86, top), (x + 90, h), (x + 64, bot), (x + 26, bot),
            (x + 18, bot - 20), (x + 46, h), (x + 10, top + 60)]


def ruota(pts, gradi, c):
    a = math.radians(gradi)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


# Tagli a cuneo nel vello, larghi in alto e a punta in basso come la riga centrale del logo
TAGLI_CORPO = [
    [(430, 292), (454, 290), (404, 560)],
    [(606, 284), (632, 284), (596, 590)],
    [(772, 298), (798, 304), (818, 580)],
]
CENTRO = (600, 460)


def forme_pecora(ant=0, post=0, inclina=0):
    """Le parti della pecora, già staccate e smussate.

    ant e post ruotano le zampe anteriori e posteriori attorno all'attaccatura
    (gradi, positivo = zoccolo in avanti); inclina ruota tutta la pecora
    (positivo = muso in su). Con tutto a zero è la pecora ferma.
    """
    # Dal fondo al primo piano: ogni parte viene staccata da quelle davanti.
    # Le zampe stanno dietro al vello, che le copre in alto con le sue punte.
    parti = [
        ruota(posteriore(722, 540, 784), post * 0.8, (765, 560)),   # posteriore lontana
        ruota(anteriore(468, 540, 784), ant * 0.8, (493, 560)),     # anteriore lontana
        ruota(posteriore(800, 540, 802), post, (843, 560)),         # posteriore
        ruota(anteriore(398, 540, 802), ant, (423, 560)),           # anteriore
        [(300, 318), (380, 300), (520, 288), (700, 292), (830, 310), (895, 350),
         (925, 440), (915, 520), (884, 588), (842, 616), (800, 592), (740, 620),
         (690, 594), (620, 624), (560, 596), (500, 622), (440, 596), (380, 618),
         (330, 582), (282, 524), (266, 460), (290, 396)],                    # corpo
        testa(orecchio(400, 318, 0.8)),
        testa([(146, 428), (200, 380), (382, 290), (398, 362), (322, 446), (198, 478)]),  # guancia e muso
        testa([(178, 392), (250, 244), (306, 218), (354, 226), (382, 268),
               (376, 306), (326, 318)]),                                      # fronte e ciuffo
    ]
    parti = [ruota(p, inclina, CENTRO) for p in parti]
    tagli = unary_union([Polygon(ruota(t, inclina, CENTRO)) for t in TAGLI_CORPO])
    forme = []
    for i, pts in enumerate(parti):
        g = Polygon(pts)
        davanti = unary_union([Polygon(q) for q in parti[i + 1:]])
        if not davanti.is_empty:
            g = g.difference(davanti.buffer(TAGLIO, join_style="mitre"))
        if i == 4:  # corpo
            g = g.difference(tagli)
        forme.append(g.buffer(-SMUSSO).buffer(SMUSSO))
    return forme


def tracciato(forme, dx=0, dy=0, s=1):
    d = []
    for g in forme:
        for poly in getattr(g, "geoms", [g]):
            for ring in [poly.exterior, *poly.interiors]:
                c = ring.simplify(0.15).coords[:-1]
                d.append("M" + " L".join(f"{(x - dx) * s:.1f} {(y - dy) * s:.1f}" for x, y in c) + "Z")
    return "".join(d)


if __name__ == "__main__":
    forme = forme_pecora()
    x0, y0, x1, y1 = unary_union(forme).bounds

    # Pecora da sola, con un piccolo margine
    m = 10
    w, h = x1 - x0 + 2 * m, y1 - y0 + 2 * m
    d = tracciato(forme, x0 - m, y0 - m, 1)
    for nome, colore in [("pecora.svg", NERO), ("pecora-bianco.svg", CREMA)]:
        (ROOT / "assets" / nome).write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" '
            f'aria-label="Black Sheep"><path fill="{colore}" d="{d}"/></svg>\n')

    # Marchio: pecora crema centrata in un cerchio nero di 1000
    s = 640 / (x1 - x0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d = tracciato(forme, cx - 500 / s, cy - 500 / s, s)
    (ROOT / "assets" / "pecora-marchio.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img" aria-label="Black Sheep">'
        f'<circle cx="500" cy="500" r="500" fill="{NERO}"/><path fill="{CREMA}" d="{d}"/></svg>\n')
    print("Creati pecora.svg, pecora-bianco.svg, pecora-marchio.svg in assets/")
