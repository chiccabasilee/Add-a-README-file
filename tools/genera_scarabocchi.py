"""Disegna gli scarabocchi a mano del sito (assets/scarabocchi/*.svg).

Ogni scarabocchio è una linea tremolante, come fatta col pennarello: si parte da
pochi punti guida, si aggiunge un tremolio casuale (sempre lo stesso, il seme è
fisso) e si ammorbidisce con curve. Il colore è currentColor, così il sito lo
colora di verde fluo e può animare il tratto mentre "si disegna".

Uso:  python3 tools/genera_scarabocchi.py
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "scarabocchi"


def tremola(punti, ampiezza, seme):
    rnd = random.Random(seme)
    return [(x + rnd.uniform(-ampiezza, ampiezza), y + rnd.uniform(-ampiezza, ampiezza)) for x, y in punti]


def curva(punti):
    """Catmull-Rom → curve di Bézier: una linea morbida che passa per tutti i punti."""
    p = [punti[0]] + punti + [punti[-1]]
    d = f"M{p[1][0]:.1f} {p[1][1]:.1f}"
    for i in range(1, len(p) - 2):
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p[i - 1], p[i], p[i + 1], p[i + 2]
        d += (f" C{x1 + (x2 - x0) / 6:.1f} {y1 + (y2 - y0) / 6:.1f}"
              f" {x2 - (x3 - x1) / 6:.1f} {y2 - (y3 - y1) / 6:.1f} {x2:.1f} {y2:.1f}")
    return d


def tratto(punti, ampiezza=1.6, seme=1):
    return curva(tremola(punti, ampiezza, seme))


def spigoli(punti, ampiezza=1.6, seme=1):
    """Linea spezzata tremolante: per le forme con angoli (shaker, coppa)."""
    p = tremola(punti, ampiezza, seme)
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in p)


def ellisse(cx, cy, rx, ry, giri=1.15, passi=60, onda=0, inizio=-2.2):
    pts = []
    for i in range(int(passi * giri) + 1):
        a = inizio + 2 * math.pi * i / passi
        r = 1 + (0.012 * math.sin(i * 1.7) if onda == 0 else onda * math.sin(i * 2.4))
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a) + i * 0.08))
    return pts


def svg(nome, tracciati, w=200, h=200, spessore=6):
    paths = "\n".join(f'  <path d="{d}"/>' for d in tracciati)
    (OUT / f"{nome}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="none" stroke="currentColor" '
        f'stroke-width="{spessore}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">\n{paths}\n</svg>\n')


OUT.mkdir(parents=True, exist_ok=True)

# Freccia curva, per indicare qualcosa (un drink, un pulsante)
svg("freccia", [
    tratto([(16, 40), (40, 120), (95, 168), (150, 160), (178, 118)], 2, 11),
    tratto([(150, 112), (180, 114), (184, 146)], 1.2, 12),
])

# Aureola tremolante sopra un bicchiere
svg("aureola", [curva(ellisse(100, 60, 82, 22, giri=1.2, passi=46, onda=0.05))], 200, 120)

# Gocce che colano dal bordo di un bicchiere
gocce = [tratto([(30, 20), (98, 14), (170, 22)], 1.5, 21)]
for i, (x, lung) in enumerate([(42, 70), (70, 110), (101, 60), (130, 120), (160, 80)]):
    pts = [(x + 6 * math.sin(k * 1.3 + i), 22 + k * lung / 6) for k in range(7)]
    gocce.append(curva(tremola(pts, 1.2, 30 + i)))
    gocce.append(tratto([(x - 3, 30 + lung), (x + 3, 34 + lung)], 1, 40 + i))
svg("gocce", gocce, 200, 170)

# Fiamme: un drink "che spacca"
svg("fiamme", [tratto([(20, 180), (34, 110), (52, 140), (64, 60), (88, 120), (100, 18),
                       (118, 112), (138, 54), (152, 130), (170, 96), (182, 180)], 2.5, 51)])

# Stelline
stelle = []
for j, (cx, cy, r) in enumerate([(60, 70, 34), (140, 40, 20), (150, 130, 24)]):
    stelle.append(tratto([(cx, cy - r), (cx + r * .15, cy - r * .15), (cx + r, cy), (cx + r * .15, cy + r * .15),
                          (cx, cy + r), (cx - r * .15, cy + r * .15), (cx - r, cy), (cx - r * .15, cy - r * .15), (cx, cy - r)], 1.2, 60 + j))
svg("stelle", stelle)

# Shaker: lo strumento di Giacomo (cobbler: tappo, filtro, corpo che si allarga verso l'alto)
svg("shaker", [
    tratto([(86, 30), (90, 16), (110, 16), (114, 30)], 1, 71),                               # tappo
    spigoli([(80, 32), (120, 32), (126, 62), (74, 62), (80, 32)], 1.2, 72),                  # filtro
    spigoli([(70, 66), (130, 66), (118, 188), (82, 188), (70, 66)], 1.4, 73),                # corpo
    tratto([(86, 92), (88, 150)], 1, 74),                                                     # riflesso
])

# Coppetta da cocktail
svg("coppa", [
    spigoli([(30, 40), (170, 40)], 1.2, 80),
    tratto([(30, 40), (52, 80), (88, 98), (112, 98), (148, 80), (170, 40)], 1.5, 81),
    tratto([(100, 98), (99, 170)], 1.2, 82),
    tratto([(64, 176), (100, 168), (138, 176)], 1.2, 83),
])

# Cerchio a scarabocchio, per evidenziare
svg("cerchio", [curva(ellisse(100, 60, 88, 40, giri=1.25, passi=40))], 200, 120)

# Sottolineatura veloce
svg("sottolinea", [tratto([(8, 30), (60, 20), (120, 24), (192, 12)], 1.5, 91),
                   tratto([(30, 40), (110, 32), (170, 30)], 1.5, 92)], 200, 50)

# Pecorella a scarabocchio (illustrazione, non il logo): corpo a nuvola, testa, zampe
nuvola = []
for k in range(0, 361, 18):
    a = math.radians(k)
    r = 1 + 0.12 * math.sin(a * 7)
    nuvola.append((100 + 62 * r * math.cos(a), 92 + 40 * r * math.sin(a)))
svg("pecorella", [
    curva(tremola(nuvola, 1.2, 101)),
    curva(tremola(ellisse(28, 82, 16, 22, giri=1.05, passi=18), 0.8, 102)),               # testa
    tratto([(18, 64), (6, 58)], 0.6, 107),                                                  # orecchio
    tratto([(72, 128), (70, 168)], 1, 103), tratto([(96, 132), (96, 172)], 1, 104),
    tratto([(122, 130), (124, 170)], 1, 105), tratto([(144, 124), (148, 162)], 1, 106),
])
print("scarabocchi in", OUT)
