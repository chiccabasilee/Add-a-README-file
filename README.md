# Menù digitale · Black Sheep Menfi

Pagina del menù raggiungibile dal QR code sui tavoli.

- `menu.js`: il contenuto del menù (categorie, voci, prezzi, allergeni). Per cambiare un prezzo si modifica solo questo file.
- `index.html`, `style.css`, `app.js`: pagina e grafica.
- `assets/`: logo vettoriale (`logo.svg` nero, `logo-bianco.svg` per sfondi scuri, `marchio.svg` per QR e icona).
- `qr/`: QR definitivo per `https://chiccabasilee.github.io/blacksheep-menu/` (`menu-qr.svg` per la tipografia, `menu-qr.png` 2000 px).
- `tools/genera_qr.py`: genera il QR in SVG con il logo al centro (`pip install segno`, poi `python3 tools/genera_qr.py <indirizzo>`).

Il QR punta sempre allo stesso indirizzo: aggiornando il menù non serve ristamparlo.
