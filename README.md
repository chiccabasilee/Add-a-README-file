# Sito · Black Sheep Cocktail & Food Lab (Menfi)

- `index.html`: home, con la storia più in basso. `drink/`: la drink list con i prezzi (ci porta il QR).
  - `drink/menu.js`: contenuto della drink list (categorie, voci, prezzi, allergeni). Per cambiare un drink o un prezzo si modifica solo questo file.
- `site.js`: fascia che scorre, barra in alto e menu ad hamburger.
- `assets/foto/`: foto del sito (per ora segnaposto; si sostituiscono tenendo gli stessi nomi).
- `style.css`: grafica comune a tutte le pagine.
- `assets/`: logo vettoriale (`logo.svg` nero, `logo-bianco.svg` per sfondi scuri, `marchio.svg` per QR e icona), archi del logo come segno grafico, icone e font.
  I font sono ospitati sul sito (licenza OFL), così non ci sono richieste a servizi esterni.
- `tools/genera_qr.py`: genera il QR in SVG con il logo al centro (`pip install segno`, poi `python3 tools/genera_qr.py <indirizzo>`).
