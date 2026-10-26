# Sito · Black Sheep Cocktail & Food Lab (Menfi)

- `index.html`: home del sito (storia, luogo, drink list, food della settimana).
- `site.js`: nastri che scorrono, menu su telefono, food della settimana in home.
- `menu/`: pagina del menù. Il QR sui tavoli punta a `menu/#drink`, che apre direttamente la drink list.
  - `menu/menu.js`: contenuto del menù (sezioni, categorie, voci, prezzi, allergeni) e date della settimana del food. Per cambiare un piatto o un prezzo si modifica solo questo file.
- `style.css`: grafica comune alle due pagine.
- `assets/`: logo vettoriale (`logo.svg` nero, `logo-bianco.svg` per sfondi scuri, `marchio.svg` per QR e icona), icone e font.
  I font sono ospitati sul sito (licenza OFL), così non ci sono richieste a servizi esterni.
- `tools/genera_qr.py`: genera il QR in SVG con il logo al centro (`pip install segno`, poi `python3 tools/genera_qr.py <indirizzo>`).
