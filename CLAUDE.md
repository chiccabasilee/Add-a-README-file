# Progetto Black Sheep: sito, menu e QR

## Il locale
- **Black Sheep · Cocktail & Food Lab**, ex Irish pub. Motto: "Stand out like a Black Sheep".
- Indirizzo: Via Calogero Ognibene 30/32, 92013 Menfi (AG).
- Instagram: @black_sheep_menfi
- Telefono 329 773 0197, preso dalla storia "sala eventi". **Da confermare.**

## Obiettivo
- Sito completo su un dominio proprio, che il locale comprerà (per esempio blacksheepmenfi.it).
- QR sui tavoli che porta direttamente alla drink list: `https://<dominio>/menu/#drink`.
- Sezioni richieste: **la storia**, **il luogo**, **drink list**, **menu food che cambia ogni settimana**.
- Stile **molto grafico**, sul modello di https://www.freniefrizioni.com/bar/. Quel sito non è raggiungibile dall'ambiente di sviluppo: servono gli screenshot fatti dal cliente.

## Identità visiva
- **Logo nuovo** "Black Sheep · Cocktail & Food Lab", vettoriale, in `assets/`:
  - `logo.svg` nero e `logo-bianco.svg` color crema, per sfondi scuri;
  - `logo-senza-archi.svg` e `logo-senza-archi-bianco.svg`, senza i due semicerchi accanto alla testa;
  - `marchio.svg`: solo la testa in un cerchio nero, usato per il QR e per l'icona del sito.
- **Colori**: sfondo `#0d0d0d`, testo crema `#f2efe9`, grigio secondario `#9a958d`, linee `#2a2a2a`.
- **Font**: Oswald per i titoli (maiuscolo, spaziato) e Inter per il testo. Sono ospitati in `assets/fonts/` con licenza OFL, quindi nessuna richiesta a Google e nessun banner cookie.
- **Texture**: ardesia antracite, scurita del 30% circa (ricevuta a 500×1000; serve la versione ad alta risoluzione per usarla sul sito).

## Stato del codice
- Repository `chiccabasilee/Add-a-README-file`, branch `claude/qr-code-restaurant-menu-2vl2hr`.
- Pubblicazione prevista su GitHub Pages con il dominio personalizzato.
- `index.html` (home, prima bozza): apertura con logo, il locale, menù, eventi, sala eventi, dove siamo, fondo pagina.
  - **Da ristrutturare** in: storia, luogo, drink list, food della settimana.
  - I testi sono bozze scritte senza informazioni dal cliente; le foto sono riquadri segnaposto.
- `menu/`: pagina del menù pensata per il telefono, prima la drink list e poi il food.
  - Il contenuto sta in `menu/menu.js`, che per ora ha voci di esempio e `anteprima: true`.
  - Barra delle categorie fissa in alto.
  - Legenda dei 14 allergeni (Reg. UE 1169/2011), nota sui surgelati, coperto.
- `style.css`: grafica comune alle pagine.
- `tools/genera_qr.py`: crea il QR in SVG (libreria segno) con `marchio.svg` al centro e correzione d'errore H. Le prove di lettura con OpenCV vanno bene fino a 110 px.
  - Il QR definitivo **non è ancora stato generato**: si fa quando il dominio è scelto.
- `social/instagram-profilo.png`: foto profilo Instagram 1080×1080, già consegnata.
  - Logo bianco senza semicerchi, centrato, su ardesia scurita.
  - `instagram-profilo-chiara.png` è la stessa con la texture originale.

## Cosa manca dal cliente
1. Screenshot del sito Freni e Frizioni e cosa piace di più.
2. Chi aggiorna il food ogni settimana. Due proposte:
   - un foglio Google che il sito legge da solo (consigliata);
   - il cliente manda il menu e lo aggiorna Claude.
3. Menu vero: drink e food, prezzi, coperto, allergeni, surgelati.
4. La storia vera del locale.
5. Foto: locale, bancone, drink, sala eventi, locandine degli eventi.
6. Orari di apertura.
7. Partita IVA, obbligatoria sul sito di un'attività.
8. Dominio scelto e acquistato.
9. Texture ad alta risoluzione.
10. Dove va stampato il QR (adesivo, segnatavolo, vetrina) e a che misura.
