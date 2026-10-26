"""Crea l'animazione "loading" con la pecora che salta, per annunciare l'apertura.

Uso:  python3 tools/genera_loading.py
Crea motion/loading.html: sfondo nero, pecora crema che salta a scatti
(12 fotogrammi al secondo, come un vecchio videogioco), scritta LOADING e una
barra a blocchi che si riempie a ogni salto; l'ultimo blocco lampeggia.
I video si fanno da questa pagina con tools/registra_loading.js.
Richiede: pip install shapely
"""
import json
import sys
from pathlib import Path

from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).resolve().parent))
from genera_pecora import CREMA, NERO, forme_pecora, tracciato  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Pose del salto: (zampe anteriori, zampe posteriori, inclinazione), vedi forme_pecora
POSE = {
    "ferma": (0, 0, 0),
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

LARGHEZZA = 600          # larghezza della pecora sulla scena di 1080
TERRA = 660              # linea di terra sulla scena
s = LARGHEZZA / (x1 - x0)
posa_svg = "".join(
    f'<path id="p-{n}" fill="{CREMA}" transform="translate(0 {(y1 - fondo[n]):.1f})" '
    f'd="{tracciato(forme[n])}"/>' for n in nomi)

# Un salto, un fotogramma per riga: (posa, sollevamento in px sulla scena)
SALTO = [("ferma", 0), ("ferma", 0), ("ferma", 0), ("accucciata", 0), ("accucciata", 0),
         ("stacco", 0), ("su", 90), ("volo", 150), ("volo", 170), ("volo", 160),
         ("giu", 110), ("giu", 40), ("atterra", 0), ("accucciata", 0), ("accucciata", 0),
         ("ferma", 0)]
SALTI = 6                # un blocco della barra per salto
BLOCCHI = SALTI + 1      # l'ultimo resta vuoto e lampeggia: stiamo per aprire
PAUSA = 18               # fotogrammi da fermi alla fine, prima di ricominciare

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
  <rect id="ombra" y="{TERRA + 8}" height="14" fill="#2a2a2a"/>
  <g transform="translate({540 - (x0 + x1) / 2 * s:.1f} {TERRA - y1 * s:.1f}) scale({s:.4f})">
    <use id="pecora" href="#p-ferma"/>
  </g>
  <!-- x spostato di metà spaziatura: la spaziatura aggiunge aria anche dopo l'ultima lettera -->
  <text id="parola" x="549" y="810" text-anchor="middle" fill="{CREMA}" font-family="Oswald, Impact, sans-serif"
        font-weight="600" font-size="76" letter-spacing="18">LOADING</text>
  <rect id="d1" y="796" width="14" height="14" fill="{CREMA}"/>
  <rect id="d2" y="796" width="14" height="14" fill="{CREMA}"/>
  <rect id="d3" y="796" width="14" height="14" fill="{CREMA}"/>
  <g id="barra"></g>
</svg>
<script>
const FPS = 12, SALTO = {json.dumps(SALTO)}, SALTI = {SALTI}, BLOCCHI = {BLOCCHI}, PAUSA = {PAUSA};
const TOTALE = SALTO.length * SALTI + PAUSA;
const ns = "http://www.w3.org/2000/svg", barra = document.getElementById("barra");
const LB = 46, GAP = 12, X0 = 540 - (BLOCCHI * LB + (BLOCCHI - 1) * GAP) / 2;
const blocchi = [...Array(BLOCCHI)].map((_, i) => {{
  const r = document.createElementNS(ns, "rect");
  r.setAttribute("x", X0 + i * (LB + GAP)); r.setAttribute("y", 860);
  r.setAttribute("width", LB); r.setAttribute("height", 24);
  barra.appendChild(r); return r;
}});
const pecora = document.getElementById("pecora"), ombra = document.getElementById("ombra");
const parola = document.getElementById("parola");

// Disegna il fotogramma f: sempre uguale per lo stesso f, così si può registrare
function disegna(f) {{
  f = ((f % TOTALE) + TOTALE) % TOTALE;
  const salto = Math.floor(f / SALTO.length);
  const [posa, su] = salto < SALTI ? SALTO[f % SALTO.length] : ["ferma", 0];
  pecora.setAttribute("href", "#p-" + posa);
  pecora.setAttribute("y", -su / {s:.4f});
  const lo = Math.round((380 - su * 1.1) / 20) * 20;   // l'ombra si stringe a scatti
  ombra.setAttribute("x", 540 - lo / 2); ombra.setAttribute("width", lo);
  // un blocco in più quando la pecora atterra
  const pieni = salto < SALTI ? salto + (f % SALTO.length >= 12 ? 1 : 0) : SALTI;
  const lampo = Math.floor(f / 4) % 2 === 0;
  blocchi.forEach((r, i) => r.setAttribute("fill",
    i < pieni ? "{CREMA}" : (i === BLOCCHI - 1 && lampo ? "#9a958d" : "#2a2a2a")));
  // puntini quadrati dopo la parola, uno in più ogni 4 fotogrammi
  const punti = Math.floor(f / 4) % 4, fine = parola.getBBox().x + parola.getBBox().width;
  [1, 2, 3].forEach(i => {{
    const d = document.getElementById("d" + i);
    d.setAttribute("x", fine - 4 + (i - 1) * 26);
    d.setAttribute("fill-opacity", i <= punti ? 1 : 0);
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
print("Creato motion/loading.html")
