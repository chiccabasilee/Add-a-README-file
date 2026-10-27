"""Disegna i pin (adesivi tondi con la scritta in cerchio) del sito: assets/pin/*.svg.

I testi sono veri testi SVG in Archivo: il sito inserisce i pin nella pagina
(come gli scarabocchi), così usano il font del sito e l'anello può girare.

La Sicilia viene dai dati Natural Earth (pubblico dominio, pacchetto world-atlas,
scala 10m), salvati in tools/dati/sicilia.json come [longitudine, latitudine].

Uso:  python3 tools/genera_pin.py
"""
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "pin"
NERO, BIANCO, FLUO = "#0d0d0d", "#f4f4f2", "#39ff14"

R_TESTO = 74                      # raggio su cui corre la scritta
GIRO = 2 * math.pi * R_TESTO      # lunghezza della circonferenza


def anello(nome, testo, colore, dimensione=None):
    """Scritta che fa il giro completo del cerchio, distribuita in modo uniforme.
    La grandezza si sceglie dalla lunghezza del testo, così le lettere non si allargano troppo."""
    lettere = len(re.sub(r"&\w+;", "x", testo))
    dimensione = dimensione or round(min(19, max(13, GIRO / (lettere * 0.7))), 1)
    d = (f"M100 {100 - R_TESTO} a{R_TESTO} {R_TESTO} 0 1 1 0 {2 * R_TESTO} "
         f"a{R_TESTO} {R_TESTO} 0 1 1 0 {-2 * R_TESTO}")
    return (f'<g class="pin__anello"><path id="giro-{nome}" d="{d}" fill="none"/>'
            f'<text fill="{colore}" font-family="Archivo, sans-serif" font-weight="700" font-size="{dimensione}" '
            f'style="font-stretch:112%" textLength="{GIRO - 2:.1f}" lengthAdjust="spacing">'
            f'<textPath href="#giro-{nome}">{testo}</textPath></text></g>')


def centro_testo(righe, colore, dimensione, peso=900, largo=125, y0=None):
    passo = dimensione * 0.86
    y0 = y0 if y0 is not None else 100 - passo * (len(righe) - 1) / 2 + dimensione * 0.33
    return "".join(
        f'<text x="100" y="{y0 + i * passo:.1f}" text-anchor="middle" fill="{colore}" font-family="Archivo, sans-serif" '
        f'font-weight="{peso}" font-size="{dimensione}" style="font-stretch:{largo}%;letter-spacing:-.02em">{r}</text>'
        for i, r in enumerate(righe))


def sicilia(cx, cy, larghezza):
    """Contorno della Sicilia proiettato (equirettangolare corretta alla latitudine) e centrato."""
    punti = json.loads((ROOT / "tools" / "dati" / "sicilia.json").read_text())
    k = math.cos(math.radians(37.6))
    xs = [lon * k for lon, _ in punti]
    ys = [-lat for _, lat in punti]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    s = larghezza / (x1 - x0)
    ox, oy = cx - (x0 + x1) / 2 * s, cy - (y0 + y1) / 2 * s
    pt = [(x * s + ox, y * s + oy) for x, y in zip(xs, ys)]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pt) + "Z"
    # Menfi: 37.60 N, 12.97 E
    menfi = (12.97 * k * s + ox, -37.60 * s + oy)
    # punta nord-est (Capo Peloro, vicino a Messina): dove la Sicilia "beve"
    capo = max(pt, key=lambda p: p[0] - p[1] * 0.6)
    return d, menfi, capo


def testa(cx, cy, altezza, colore):
    """La testa della pecora del logo, così com'è (configurazione "solo testa" approvata)."""
    svg = (ROOT / "assets" / "logo-testa.svg").read_text()
    w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups())
    d = re.search(r' d="([^"]+)"', svg).group(1)
    larghezza = altezza * w / h
    return (f'<svg x="{cx - larghezza / 2:.1f}" y="{cy - altezza / 2:.1f}" width="{larghezza:.1f}" height="{altezza:.1f}" '
            f'viewBox="0 0 {w:.0f} {h:.0f}"><path fill="{colore}" fill-rule="evenodd" d="{d}"/></svg>')


def shaker(cx, cy, colore):
    return (f'<g fill="{colore}" transform="translate({cx - 20} {cy - 38})">'
            f'<path d="M14 0h12l2 8h-16z"/><path d="M9 10h22l3 14H6z"/><path d="M4 27h32l-6 49H10z"/></g>')


def pin(nome, sfondo, contenuto, bordo=None):
    b = f'<circle cx="100" cy="100" r="93" fill="none" stroke="{bordo}" stroke-width="3"/>' if bordo else ""
    (OUT / f"{nome}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" class="pin pin--{nome}" role="img">'
        f'<circle cx="100" cy="100" r="98" fill="{sfondo}"/>{b}{contenuto}</svg>\n')


OUT.mkdir(parents=True, exist_ok=True)

# Home: la Sicilia tutta nera che beve un drink, con l'anello che gira.
# Fondo bianco perché sta a cavallo della fascia verde; Menfi è il puntino verde.
d, menfi, capo = sicilia(88, 108, 100)
gx, gy = 146, 90   # coppetta a destra della punta nord-est
coppa = (f'<path d="M{gx - 17} {gy} h34 l-12 14 q-5 3 -10 0 z" fill="{NERO}"/>'
         f'<path d="M{gx} {gy + 15} v15 M{gx - 9} {gy + 31} h18" stroke="{NERO}" stroke-width="3.2" stroke-linecap="round"/>')
cannuccia = f'<path d="M{capo[0]:.1f} {capo[1]:.1f} Q{gx - 10} {gy - 22} {gx + 5} {gy + 7}" fill="none" stroke="{NERO}" stroke-width="2.8" stroke-linecap="round"/>'
pin("siciliano", BIANCO,
    anello("siciliano", "100% SICILIANO • COCKTAIL &amp; FOOD LAB • ", NERO)
    + f'<path d="{d}" fill="{NERO}"/>' + cannuccia + coppa
    + f'<circle cx="{menfi[0]:.1f}" cy="{menfi[1]:.1f}" r="2.6" fill="{FLUO}"/>')

# Drink list: etichette al posto delle scritte normali
pin("preferito", FLUO, anello("preferito", "IL PREFERITO DI GIACOMO • DA PROVARE • ", NERO) + shaker(100, 104, NERO))
pin("analcolico", BIANCO, anello("analcolico", "ANALCOLICO • ZERO ALCOL • TUTTO IL GUSTO • ", NERO) + centro_testo(["0%"], NERO, 46))
pin("nuovo", NERO, anello("nuovo", "APPENA USCITO DAL BANCO • NUOVO DRINK • ", FLUO) + centro_testo(["NUOVO"], FLUO, 25), bordo=FLUO)
pin("casa", BIANCO, anello("casa", "BLACK SHEEP • MENFI • DRINK DELLA CASA • ", NERO) + testa(100, 100, 66, NERO))
print("pin in", OUT)
