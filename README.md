# Sito · Black Sheep Cocktail & Food Lab (Menfi)

- `index.html`: home. `storia/`: la storia e Giacomo e Domenico. `drink/`: la drink list (ci porta il QR).
  - `drink/menu.js`: contenuto della drink list (categorie, voci, prezzi, allergeni). Per cambiare un drink o un prezzo si modifica solo questo file.
- `site.js`: nastri che scorrono e menu ad hamburger.
- `style.css`: grafica comune a tutte le pagine.
- `assets/`: logo vettoriale (`logo.svg` nero, `logo-bianco.svg` per sfondi scuri, `marchio.svg` per QR e icona), icone e font.
  I font sono ospitati sul sito (licenza OFL), così non ci sono richieste a servizi esterni.
- `tools/genera_qr.py`: genera il QR in SVG con il logo al centro (`pip install segno`, poi `python3 tools/genera_qr.py <indirizzo>`).
