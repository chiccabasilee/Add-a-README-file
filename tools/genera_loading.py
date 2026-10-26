"""Crea l'animazione "loading" con la pecora che salta, per annunciare l'apertura.

Uso:  python3 tools/genera_loading.py
Crea motion/loading.html: sfondo nero, la pecora crema attraversa lo schermo
da sinistra a destra galoppando e saltando a scatti (12 fotogrammi al secondo,
come un vecchio videogioco). Come le pecore che si contano per addormentarsi,
salta uno steccato e poi gli oggetti del bar: a ogni ostacolo compare il numero
e si accende un blocco della barra sotto la scritta LOADING. L'ultimo blocco
resta vuoto e lampeggia: stiamo per aprire.
I video si fanno da questa pagina con tools/registra_loading.js.
Richiede: pip install shapely
"""
import json
import math
import sys
from pathlib import Path

from shapely.affinity import affine_transform, scale, translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).resolve().parent))
from genera_pecora import CREMA, NERO, forme_pecora, tracciato  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LARGHEZZA = 400          # larghezza della pecora sulla scena di 1080
TERRA = 620              # linea di terra sulla scena
GALOPPO = 20             # px per fotogramma a terra
VOLO = 70                # px per fotogramma in aria
PAUSA = 18               # fotogrammi senza pecora alla fine, prima che rientri

# Pose: (zampe anteriori, zampe posteriori, inclinazione), vedi forme_pecora
POSE = {
    "ferma": (0, 0, 0),
    "aperta": (20, -22, 0),       # galoppo: zampe distese
    "raccolta": (-14, 16, 0),     # galoppo: zampe sotto la pancia
    "accucciata": (-12, 14, 0),
    "stacco": (-30, -45, 12),
    "su": (-50, -40, 8),
    "volo": (-55, -30, 0),
    "giu": (25, -30, -10),
    "atterra": (15, -8, -6),
}
nomi = list(POSE)
forme = {n: forme_pecora(*POSE[n]) for n in nomi}
# Quanto spostare ogni posa perché gli zoccoli tocchino terra
fondo = {n: unary_union(f).bounds[3] for n, f in forme.items()}
x0, y0, x1, y1 = unary_union(forme["ferma"]).bounds
cx = (x0 + x1) / 2
s = LARGHEZZA / (x1 - x0)
posa_svg = "".join(
    f'<path id="p-{n}" fill="{CREMA}" transform="translate(0 {(y1 - fondo[n]):.1f})" '
    f'd="{tracciato(forme[n])}"/>' for n in nomi)

# Dove stanno gli zoccoli rispetto al centro, sulla scena e con la pecora girata a destra:
# davanti (forme 3) e dietro (forme 2), per mettere l'ostacolo tra stacco e atterraggio
ZOCCOLI_DAVANTI = (cx - forme["ferma"][3].bounds[0]) * s
ZOCCOLI_DIETRO = (cx - forme["ferma"][2].bounds[2]) * s


# --- Ostacoli: crema, a spigoli vivi, con i tagli come la pecora --------------------
def stacca(parti, tagli=(), taglio=6):
    """Ogni parte meno quelle davanti (allargate del taglio), meno i tagli."""
    out = []
    for i, p in enumerate(parti):
        g = Polygon(p)
        davanti = unary_union([Polygon(q) for q in parti[i + 1:]])
        if not davanti.is_empty:
            g = g.difference(davanti.buffer(taglio, join_style="mitre"))
        for t in tagli:
            g = g.difference(Polygon(t))
        out.append(g)
    return out


def poligono(r, n, c=(0, 0), giro=0):
    return [(c[0] + r * math.cos(giro + 2 * math.pi * i / n),
             c[1] + r * math.sin(giro + 2 * math.pi * i / n)) for i in range(n)]


# Coordinate con l'origine a terra, al centro; y negativo verso l'alto
OGGETTI = {
    "steccato": stacca([
        [(-68, -26), (68, -26), (68, -40), (-68, -40)],             # traverse
        [(-68, -70), (68, -70), (68, -84), (-68, -84)],
        [(-46, 0), (-28, 0), (-28, -96), (-37, -110), (-46, -96)],  # paletti a punta
        [(28, 0), (46, 0), (46, -96), (37, -110), (28, -96)],
    ]),
    "coppetta": stacca([
        [(-34, 0), (34, 0), (26, -9), (-26, -9)],                   # piede
        [(-4, -9), (4, -9), (4, -58), (-4, -58)],                   # stelo
        [(-46, -106), (46, -106), (5, -60), (-5, -60)],             # coppa
        poligono(9, 6, (10, -78)),                                  # oliva
    ], tagli=[[(-40, -96), (40, -96), (38, -93), (-38, -93)]]),     # bordo del liquido
    "shaker": stacca([
        [(-26, 0), (26, 0), (32, -64), (-32, -64)],                 # corpo
        [(-31, -70), (31, -70), (21, -94), (-21, -94)],             # filtro
        [(-9, -98), (9, -98), (7, -112), (-7, -112)],               # tappo
    ], tagli=[[(-20, -10), (-14, -10), (-18, -56), (-24, -56)]]),   # riflesso
    "pinta": stacca([
        [(-31, 0), (31, 0), (38, -92), (-38, -92)],                 # bicchiere
        [(-40, -98), (40, -98), (37, -112), (22, -106), (8, -118),  # schiuma a punte
         (-8, -110), (-24, -118), (-38, -110)],
    ], tagli=[[(-24, -10), (-18, -10), (-26, -80), (-32, -80)]]),
    "bottiglia": stacca([
        [(-22, 0), (22, 0), (22, -66), (9, -84), (-9, -84), (-22, -66)],   # corpo
        [(-7, -90), (7, -90), (7, -114), (-7, -114)],               # collo
    ], tagli=[[(-30, -22), (30, -22), (30, -27), (-30, -27)],       # etichetta
              [(-30, -48), (30, -48), (30, -53), (-30, -53)]]),
}
# Fetta di limone: anello di buccia e otto spicchi separati da raggi
_buccia = Polygon(poligono(50, 8, (0, -50), math.pi / 8))
_anello = _buccia.difference(Polygon(poligono(41, 8, (0, -50), math.pi / 8)))
_spicchi = Polygon(poligono(35, 8, (0, -50), math.pi / 8)).difference(unary_union([
    Polygon([(0, -50), (40 * math.cos(a - .09), -50 + 40 * math.sin(a - .09)),
             (40 * math.cos(a + .09), -50 + 40 * math.sin(a + .09))]).buffer(1.5)
    for a in [2 * math.pi * i / 8 for i in range(8)]]).union(Polygon(poligono(5, 8, (0, -50)))))
OGGETTI["limone"] = [_anello, _spicchi]
OGGETTI = {k: [scale(g, 1.25, 1.25, origin=(0, 0)) for g in v] for k, v in OGGETTI.items()}

# Due ostacoli per passaggio: tre salti non entrano nella larghezza dello schermo
PASSAGGI = [["steccato", "coppetta"], ["shaker", "pinta"], ["bottiglia", "limone"]]
BLOCCHI = sum(map(len, PASSAGGI)) + 1   # l'ultimo resta vuoto e lampeggia


def pecora_in_scena(posa, x, su):
    """La sagoma della pecora come appare sulla scena: girata a destra, centro in x."""
    return affine_transform(unary_union(forme[posa]),
                            [-s, 0, 0, s, x + s * cx, TERRA - su - s * fondo[posa]])


def posto_ostacolo(oggetto, salto):
    """Dove mettere l'ostacolo perché la pecora, fotogramma per fotogramma, lo scavalchi
    con più aria possibile. salto: [(posa, x, su)] dallo stacco all'atterraggio."""
    sagome = [pecora_in_scena(*f) for f in salto]
    forma = unary_union(OGGETTI[oggetto])
    def aria(ox):
        o = translate(forma, ox, TERRA)
        return min(g.distance(o) for g in sagome)
    da, a = salto[0][1], salto[-1][1]
    ox = max(range(round(da) - 150, round(a) + 150, 2), key=aria)
    assert aria(ox) >= 15, f"la pecora non supera {oggetto} ({aria(ox):.0f} px d'aria)"
    return ox


# --- Tempi: un fotogramma per elemento -----------------------------------------------
SALTO = [("accucciata", 0, GALOPPO), ("stacco", 0, VOLO), ("su", 120, VOLO), ("volo", 180, VOLO),
         ("volo", 200, VOLO), ("volo", 190, VOLO), ("giu", 165, VOLO), ("giu", 105, VOLO),
         ("atterra", 0, VOLO), ("accucciata", 0, GALOPPO)]
TRA_SALTI = 2            # fotogrammi di galoppo tra un salto e l'altro
# Distanza tra due ostacoli, e da dove parte il galoppo perché la coppia stia al centro
PASSO = sum(dx for _, _, dx in SALTO) + TRA_SALTI * GALOPPO
DALLO_STACCO = (ZOCCOLI_DAVANTI + 7 * VOLO + ZOCCOLI_DIETRO) / 2   # ostacolo - stacco
PARTENZA = -LARGHEZZA / 2 - 30
GALOPPO_INIZIALE = round((540 - PASSO / 2 - DALLO_STACCO - VOLO - GALOPPO - PARTENZA) / GALOPPO)
fotogrammi, ostacoli, numeri = [], [], []
saltati = 0
for n, passaggio in enumerate(PASSAGGI):
    x, posti = PARTENZA, []

    def galoppa(k):
        global x
        for _ in range(k):
            x += GALOPPO
            aperta = len(fotogrammi) % 2 == 0
            fotogrammi.append({"p": "aperta" if aperta else "raccolta", "x": x,
                               "su": 6 if aperta else 0, "o": n, "b": saltati})

    galoppa(GALOPPO_INIZIALE)
    for oggetto in passaggio:
        for posa, su, dx in SALTO:
            x += dx
            if posa == "stacco":
                salto = []
            if posa in ("stacco", "su", "volo", "giu", "atterra"):
                salto.append((posa, x, su))
            if posa == "atterra":
                ox = posto_ostacolo(oggetto, salto)
                posti.append((oggetto, ox))
                saltati += 1
                numeri.append({"f": len(fotogrammi), "n": saltati, "x": round(ox)})
            fotogrammi.append({"p": posa, "x": x, "su": su, "o": n, "b": saltati})
        galoppa(TRA_SALTI)
    while x < 1080 + LARGHEZZA / 2 + 30:
        galoppa(1)
    ostacoli.append(posti)
fotogrammi += [{"p": "ferma", "x": 2000, "su": 0, "o": len(PASSAGGI) - 1, "b": saltati}] * PAUSA

ostacoli_svg = "".join(
    f'<g id="o-{n}" fill="{CREMA}">' + "".join(
        f'<path transform="translate({ox:.0f} {TERRA})" d="{tracciato(OGGETTI[ogg])}"/>'
        for ogg, ox in posti) + "</g>"
    for n, posti in enumerate(ostacoli))

pagina = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Black Sheep · Loading</title>
<style>
  @font-face {{ font-family: "Oswald"; font-weight: 600; font-display: block;
    src: url("../assets/fonts/oswald-latin-600-normal.woff2") format("woff2"); }}
  html, body {{ margin: 0; height: 100%; background: {NERO}; }}
  body {{ display: grid; place-items: center; overflow: hidden; }}
  svg {{ width: min(100vw, 100vh); height: auto; display: block; }}
</style>
</head>
<body>
<svg viewBox="0 0 1080 1080" role="img" aria-label="Black Sheep: loading">
  <defs>{posa_svg}</defs>
  {ostacoli_svg}
  <rect id="ombra" y="{TERRA + 8}" height="14" fill="#2a2a2a"/>
  <g id="gruppo"><use id="pecora" href="#p-ferma"/></g>
  <text id="numero" y="0" text-anchor="middle" fill="{CREMA}" font-family="Oswald, Impact, sans-serif"
        font-weight="600" font-size="72"></text>
  <!-- x spostato di metà spaziatura: la spaziatura aggiunge aria anche dopo l'ultima lettera -->
  <text id="parola" x="547" y="760" text-anchor="middle" fill="{CREMA}" font-family="Oswald, Impact, sans-serif"
        font-weight="600" font-size="58" letter-spacing="14">LOADING</text>
  <rect id="d1" y="749" width="11" height="11" fill="{CREMA}"/>
  <rect id="d2" y="749" width="11" height="11" fill="{CREMA}"/>
  <rect id="d3" y="749" width="11" height="11" fill="{CREMA}"/>
  <g id="barra"></g>
</svg>
<script>
const FPS = 12, F = {json.dumps(fotogrammi, separators=(",", ":"))};
const NUMERI = {json.dumps(numeri, separators=(",", ":"))}, BLOCCHI = {BLOCCHI}, PASSAGGI = {len(PASSAGGI)};
const TOTALE = F.length, $ = id => document.getElementById(id);
const LB = 36, GAP = 10, X0 = 540 - (BLOCCHI * LB + (BLOCCHI - 1) * GAP) / 2;
const blocchi = [...Array(BLOCCHI)].map((_, i) => {{
  const r = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  r.setAttribute("x", X0 + i * (LB + GAP)); r.setAttribute("y", 800);
  r.setAttribute("width", LB); r.setAttribute("height", 18);
  $("barra").appendChild(r); return r;
}});

// Disegna il fotogramma f: sempre uguale per lo stesso f, così si può registrare
function disegna(f) {{
  f = ((f % TOTALE) + TOTALE) % TOTALE;
  const {{ p, x, su, o, b }} = F[f];
  // la pecora è disegnata rivolta a sinistra: si specchia perché vada verso destra
  $("gruppo").setAttribute("transform",
    `translate(${{x}} {TERRA}) scale(-{s:.4f} {s:.4f}) translate({-cx:.1f} {-y1:.1f})`);
  $("pecora").setAttribute("href", "#p-" + p);
  $("pecora").setAttribute("y", -su / {s:.4f});
  const lo = Math.round((260 - su * 0.9) / 20) * 20;   // l'ombra si stringe a scatti
  $("ombra").setAttribute("x", x - lo / 2); $("ombra").setAttribute("width", lo);
  for (let n = 0; n < PASSAGGI; n++) $("o-" + n).style.display = n === o ? "" : "none";
  // il numero dell'ostacolo appena saltato sale a scatti e sparisce, come un punteggio
  const num = NUMERI.find(m => f >= m.f && f < m.f + 8);
  $("numero").textContent = num ? num.n : "";
  if (num) {{ $("numero").setAttribute("x", num.x); $("numero").setAttribute("y", {TERRA - 190} - (f - num.f) * 10); }}
  const lampo = Math.floor(f / 4) % 2 === 0;
  blocchi.forEach((r, i) => r.setAttribute("fill",
    i < b ? "{CREMA}" : (i === BLOCCHI - 1 && lampo ? "#9a958d" : "#2a2a2a")));
  // puntini quadrati dopo la parola, uno in più ogni 4 fotogrammi
  const punti = Math.floor(f / 4) % 4, bb = $("parola").getBBox();
  [1, 2, 3].forEach(i => {{
    $("d" + i).setAttribute("x", bb.x + bb.width - 3 + (i - 1) * 20);
    $("d" + i).setAttribute("fill-opacity", i <= punti ? 1 : 0);
  }});
}}
window.disegna = disegna; window.TOTALE = TOTALE; window.FPS = FPS;
document.fonts.ready.then(() => disegna(0));
if (!location.search.includes("registra")) {{
  let f = 0;
  setInterval(() => disegna(++f), 1000 / FPS);
}}
</script>
</body>
</html>
"""
(ROOT / "motion").mkdir(exist_ok=True)
(ROOT / "motion" / "loading.html").write_text(pagina)
print(f"Creato motion/loading.html: {len(fotogrammi)} fotogrammi, {len(fotogrammi) / 12:.1f} s")
