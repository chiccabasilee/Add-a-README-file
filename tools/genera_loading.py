"""Crea l'animazione "loading" con la pecora che salta, per annunciare l'apertura.

Uso:  python3 tools/genera_loading.py
Crea motion/loading.html: sfondo nero, pecora crema che attraversa lo schermo
da sinistra a destra saltando a scatti (12 fotogrammi al secondo, come un
vecchio videogioco), scritta LOADING e una barra a blocchi che si riempie a
ogni salto; l'ultimo blocco lampeggia.
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

LARGHEZZA = 400          # larghezza della pecora sulla scena di 1080
TERRA = 620              # linea di terra sulla scena
s = LARGHEZZA / (x1 - x0)
posa_svg = "".join(
    f'<path id="p-{n}" fill="{CREMA}" transform="translate(0 {(y1 - fondo[n]):.1f})" '
    f'd="{tracciato(forme[n])}"/>' for n in nomi)

# Un salto, un fotogramma per riga: (posa, sollevamento in px sulla scena)
SALTO = [("ferma", 0), ("ferma", 0), ("ferma", 0), ("accucciata", 0), ("accucciata", 0),
         ("stacco", 0), ("su", 80), ("volo", 130), ("volo", 150), ("volo", 140),
         ("giu", 95), ("giu", 35), ("atterra", 0), ("accucciata", 0), ("accucciata", 0),
         ("ferma", 0)]
# Quanta parte del passo di un salto fa la pecora a ogni fotogramma: avanza solo in aria
AVANZA = [0, 0, 0, 0, 0, .05, .15, .15, .15, .15, .15, .15, .05, 0, 0, 0]
PASSO = 245              # px di scena per salto
PARTENZA = -120          # centro della pecora all'inizio: si vede appena la testa
SALTI = 6                # un blocco della barra per salto
BLOCCHI = SALTI + 1      # l'ultimo resta vuoto e lampeggia: stiamo per aprire
PAUSA = 18               # fotogrammi senza pecora alla fine, prima che rientri

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
  <g id="gruppo">
    <use id="pecora" href="#p-ferma"/>
  </g>
  <!-- x spostato di metà spaziatura: la spaziatura aggiunge aria anche dopo l'ultima lettera -->
  <text id="parola" x="547" y="760" text-anchor="middle" fill="{CREMA}" font-family="Oswald, Impact, sans-serif"
        font-weight="600" font-size="58" letter-spacing="14">LOADING</text>
  <rect id="d1" y="749" width="11" height="11" fill="{CREMA}"/>
  <rect id="d2" y="749" width="11" height="11" fill="{CREMA}"/>
  <rect id="d3" y="749" width="11" height="11" fill="{CREMA}"/>
  <g id="barra"></g>
</svg>
<script>
const FPS = 12, SALTO = {json.dumps(SALTO)}, SALTI = {SALTI}, BLOCCHI = {BLOCCHI}, PAUSA = {PAUSA};
const AVANZA = {json.dumps(AVANZA)}, PASSO = {PASSO}, PARTENZA = {PARTENZA};
const TOTALE = SALTO.length * SALTI + PAUSA;
const ns = "http://www.w3.org/2000/svg", barra = document.getElementById("barra");
const LB = 36, GAP = 10, X0 = 540 - (BLOCCHI * LB + (BLOCCHI - 1) * GAP) / 2;
const blocchi = [...Array(BLOCCHI)].map((_, i) => {{
  const r = document.createElementNS(ns, "rect");
  r.setAttribute("x", X0 + i * (LB + GAP)); r.setAttribute("y", 800);
  r.setAttribute("width", LB); r.setAttribute("height", 18);
  barra.appendChild(r); return r;
}});
const pecora = document.getElementById("pecora"), ombra = document.getElementById("ombra");
const gruppo = document.getElementById("gruppo");
const parola = document.getElementById("parola");

// Disegna il fotogramma f: sempre uguale per lo stesso f, così si può registrare
function disegna(f) {{
  f = ((f % TOTALE) + TOTALE) % TOTALE;
  const salto = Math.floor(f / SALTO.length);
  const [posa, su] = salto < SALTI ? SALTO[f % SALTO.length] : ["ferma", 0];
  // posizione orizzontale a scatti di 10 px; nella pausa la pecora è già uscita a destra
  const k = f % SALTO.length;
  const fatto = salto < SALTI ? salto + AVANZA.slice(0, k + 1).reduce((a, b) => a + b, 0) : SALTI;
  const x = Math.round((PARTENZA + PASSO * fatto) / 10) * 10;
  // la pecora è disegnata rivolta a sinistra: si specchia perché vada verso destra
  gruppo.setAttribute("transform",
    `translate(${{x}} {TERRA}) scale(-{s:.4f} {s:.4f}) translate({-(x0 + x1) / 2:.1f} {-y1:.1f})`);
  pecora.setAttribute("href", "#p-" + posa);
  pecora.setAttribute("y", -su / {s:.4f});
  const lo = Math.round((260 - su * 0.9) / 20) * 20;   // l'ombra si stringe a scatti
  ombra.setAttribute("x", x - lo / 2); ombra.setAttribute("width", lo);
  // un blocco in più quando la pecora atterra
  const pieni = salto < SALTI ? salto + (f % SALTO.length >= 12 ? 1 : 0) : SALTI;
  const lampo = Math.floor(f / 4) % 2 === 0;
  blocchi.forEach((r, i) => r.setAttribute("fill",
    i < pieni ? "{CREMA}" : (i === BLOCCHI - 1 && lampo ? "#9a958d" : "#2a2a2a")));
  // puntini quadrati dopo la parola, uno in più ogni 4 fotogrammi
  const punti = Math.floor(f / 4) % 4, fine = parola.getBBox().x + parola.getBBox().width;
  [1, 2, 3].forEach(i => {{
    const d = document.getElementById("d" + i);
    d.setAttribute("x", fine - 3 + (i - 1) * 20);
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
