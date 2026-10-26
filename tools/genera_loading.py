"""Crea l'animazione "loading" con la pecora che salta, per annunciare l'apertura.

Uso:  python3 tools/genera_loading.py
Crea motion/loading.html: sfondo nero e, come le pecore che si contano per
addormentarsi, pecore crema che una dopo l'altra entrano da sinistra, saltano
l'oggetto al centro ed escono a destra, galoppando a scatti (12 fotogrammi al
secondo, come un vecchio videogioco). L'oggetto cambia a ogni salto: steccato
e poi gli oggetti del bar. Sotto, la scritta LOADING e una barra a blocchi che
si riempie a ogni salto; l'ultimo blocco resta vuoto e lampeggia: stiamo per aprire.
Il ciclo si ripete senza stacchi. GIF e video si fanno da questa pagina con
tools/registra_loading.js.
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

# Un oggetto per salto, sempre al centro della scena
ORDINE = ["steccato", "coppetta", "shaker", "pinta", "bottiglia", "limone"]
CENTRO = 540
BLOCCHI = len(ORDINE) + 1   # l'ultimo resta vuoto e lampeggia
INTERVALLO = 26             # fotogrammi tra l'entrata di una pecora e la successiva:
                            # a terra restano a 26 x 20 = 520 px, 120 px tra una e l'altra


def pecora_in_scena(posa, x, su):
    """La sagoma della pecora come appare sulla scena: girata a destra, centro in x."""
    return affine_transform(unary_union(forme[posa]),
                            [-s, 0, 0, s, x + s * cx, TERRA - su - s * fondo[posa]])


# --- La vita di una pecora: entra, galoppa, salta l'oggetto centrale, esce ------------
SALTO = [("accucciata", 0, GALOPPO), ("stacco", 0, VOLO), ("su", 120, VOLO), ("volo", 180, VOLO),
         ("volo", 200, VOLO), ("volo", 190, VOLO), ("giu", 165, VOLO), ("giu", 105, VOLO),
         ("atterra", 0, VOLO), ("accucciata", 0, GALOPPO)]
IN_ARIA = ("stacco", "su", "volo", "giu", "atterra")

# Dove staccare perché la pecora scavalchi con più aria possibile tutti gli oggetti al centro
x, salto = 0, []
for posa, su, dx in SALTO:
    x += dx
    if posa in IN_ARIA:
        salto.append((posa, x - SALTO[0][2] - SALTO[1][2], su))   # x relativo allo stacco
oggetti_al_centro = [translate(unary_union(OGGETTI[o]), CENTRO, TERRA) for o in ORDINE]


def aria(stacco):
    sagome = [pecora_in_scena(p, stacco + x, su) for p, x, su in salto]
    return min(g.distance(o) for g in sagome for o in oggetti_al_centro)


STACCO = max(range(CENTRO - 450, CENTRO, 2), key=aria)
assert aria(STACCO) >= 15, f"la pecora non supera gli oggetti ({aria(STACCO):.0f} px d'aria)"

ENTRATA = -LARGHEZZA / 2 - 30
galoppi = math.ceil((STACCO - SALTO[0][2] - SALTO[1][2] - ENTRATA) / GALOPPO)
x = STACCO - SALTO[0][2] - SALTO[1][2] - galoppi * GALOPPO
vita = []


def galoppa():
    global x
    x += GALOPPO
    aperta = len(vita) % 2 == 0
    vita.append(("aperta" if aperta else "raccolta", x, 6 if aperta else 0))


for _ in range(galoppi):
    galoppa()
for posa, su, dx in SALTO:
    x += dx
    if posa == "atterra":
        ATTERRA = len(vita)
    vita.append((posa, x, su))
while x < 1080 + LARGHEZZA / 2 + 30:
    galoppa()
CAMBIO = ATTERRA + 3        # l'oggetto cambia quando la pecora è scesa e passata

# --- Il ciclo: una pecora per oggetto, ognuna INTERVALLO fotogrammi dopo l'altra ------
CICLO = INTERVALLO * len(ORDINE)
assert len(vita) < CICLO
fotogrammi = []
for f in range(CICLO):
    pecore = []
    for k in range(len(ORDINE)):
        t = (f - INTERVALLO * k) % CICLO
        if t < len(vita):
            posa, x, su = vita[t]
            pecore.append([k, posa, round(x), su])
    oggetto = ((f - CAMBIO) // INTERVALLO + 1) % len(ORDINE)
    pieni = sum((INTERVALLO * k + ATTERRA) % CICLO <= f for k in range(len(ORDINE)))
    fotogrammi.append({"s": pecore, "o": oggetto, "b": pieni})

ostacoli_svg = "".join(
    f'<path id="o-{i}" fill="{CREMA}" transform="translate({CENTRO} {TERRA})" '
    f'd="{tracciato(OGGETTI[o])}"/>' for i, o in enumerate(ORDINE))
pecore_svg = "".join(
    f'<rect id="ombra-{k}" y="{TERRA + 8}" height="14" fill="#2a2a2a"/>'
    f'<g id="g-{k}"><use id="u-{k}" href="#p-ferma"/></g>' for k in range(len(ORDINE)))

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
  {pecore_svg}
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
const BLOCCHI = {BLOCCHI}, PECORE = {len(ORDINE)};
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
  const {{ s, o, b }} = F[f];
  for (let k = 0; k < PECORE; k++) {{
    $("g-" + k).style.display = "none"; $("ombra-" + k).style.display = "none";
  }}
  for (const [k, p, x, su] of s) {{
    // la pecora è disegnata rivolta a sinistra: si specchia perché vada verso destra
    $("g-" + k).style.display = ""; $("ombra-" + k).style.display = "";
    $("g-" + k).setAttribute("transform",
      `translate(${{x}} {TERRA}) scale(-{s:.4f} {s:.4f}) translate({-cx:.1f} {-y1:.1f})`);
    $("u-" + k).setAttribute("href", "#p-" + p);
    $("u-" + k).setAttribute("y", -su / {s:.4f});
    const lo = Math.round((260 - su * 0.9) / 20) * 20;   // l'ombra si stringe a scatti
    $("ombra-" + k).setAttribute("x", x - lo / 2); $("ombra-" + k).setAttribute("width", lo);
  }}
  for (let i = 0; i < PECORE; i++) $("o-" + i).style.display = i === o ? "" : "none";
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
print(f"Creato motion/loading.html: {len(fotogrammi)} fotogrammi, {len(fotogrammi) / 12:.1f} s, "
      f"{aria(STACCO):.0f} px d'aria sugli oggetti")
