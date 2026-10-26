# Progetto Black Sheep: sito, menu e QR

## Il locale
- **Black Sheep · Cocktail & Food Lab**, ex Irish pub. Motto: "Stand out like a Black Sheep".
- Indirizzo: Via Calogero Ognibene 30/32, 92013 Menfi (AG).
- Instagram: @black_sheep_menfi
- Telefono 329 773 0197, preso dalla storia "sala eventi". **Da confermare.**

## Brief (dettagli in `brand/brief.md`)
- Storia scritta dal cliente: Black Sheep nasce per "uscire dagli schemi" in un territorio dove la mixology è agli inizi; non solo bere un drink, ma un'esperienza di ricerca, creatività, gusto e condivisione.
- Tono di voce: amichevole, cool, non serioso.
- Spazio: antracite, **pareti verdi**, **griglia di alluminio a quadratini** sul bancone che regge le piante.
- Aperitivo ogni giorno; drink card aggiornata con drink speciali del proprietario **Giacomo**, bartender esperto, quest'anno affiancato da **Domenico**. Il sabato aperitivo e poi dj set.
- **2 novembre**: servizio fotografico (locale, drink e ritratti di Giacomo e Domenico) e piccola intervista ai due. Il sito va imbastito ora e corretto man mano.
- Pubblico 25–40 anni che vuole bere bene in un posto amichevole.
- **Riposizionamento**: l'anno scorso era visto come discoteca solo per un'ora a notte nel weekend; ora deve essere un locale di qualità aperto dal pomeriggio. Evitare i codici da discoteca.
- Le foto le fa un fotografo già istruito dal cliente; le ispirazioni sono in arrivo.

## Obiettivo
- Sito completo su un dominio proprio, che il locale comprerà (per esempio blacksheepmenfi.it).
- QR sui tavoli che porta direttamente alla drink list: `https://<dominio>/menu/#drink`.
- Sezioni richieste: **la storia**, **il luogo**, **drink list**, **menu food che cambia ogni settimana**.
- Stile **molto grafico**, sul modello di https://www.freniefrizioni.com/bar/ (dominio ora consentito nella rete dell'ambiente). Da lì abbiamo preso:
  - nero più un solo colore (loro giallo, noi crema);
  - nastri che scorrono, anche inclinati sopra la foto d'apertura;
  - titoli enormi e ruotati, frasi grandi in maiuscolo;
  - foto e testo sovrapposti in modo asimmetrico;
  - il simbolo ricorrente (per noi la pecora) e il fondo pagina tutto a colore.

## Identità visiva
- **Logo nuovo** "Black Sheep · Cocktail & Food Lab", vettoriale, in `assets/`:
  - `logo.svg` nero e `logo-bianco.svg` color crema, per sfondi scuri;
  - `logo-senza-archi.svg` e `logo-senza-archi-bianco.svg`, senza i due semicerchi accanto alla testa;
  - `marchio.svg`: solo la testa in un cerchio nero, usato per il QR e per l'icona del sito.
  - `logo-scritta.svg` / `logo-scritta-bianco.svg` (solo BLACK SHEEP + payoff) e `logo-testa.svg` / `logo-testa-bianco.svg` (solo testa, senza cerchio): estratti dal logo definitivo, non ridisegnati. Uso da approvare in fase di sistema.
  - `pecora.svg` (nera), `pecora-bianco.svg` (crema) e `pecora-marchio.svg` (nel cerchio nero): pecora intera di profilo nello stile della testa. Si rigenerano con `tools/genera_pecora.py`.
- **Logo definitivo**: confermato dal cliente; è lo stesso disegno da cui sono ricavati i vettoriali. Il file è un'immagine (PNG 2481×3508): per la stampa grande va chiesto il sorgente vettoriale a chi l'ha disegnato.
- **Analisi del logo** (fase 2, `brand/analisi-logo.html` e `.png`):
  - Formato 1,08 : 1. La testa occupa il 67% della larghezza e l'80% dell'altezza.
  - Gli archi stanno su un cerchio centrato sull'asse della testa. La testa esce dal cerchio in alto e la punta del muso cade tra BLACK e SHEEP.
  - Area di rispetto X = altezza della B di BLACK (11,4% del logo). Il payoff è alto la metà di X: il logo completo si legge fino a circa 110 px di altezza (25 mm in stampa); la testa da sola regge fino a 16 px.
  - Angoli della testa: quasi verticali, inclinati di 5–15° (il muso converge); tetto a ±30–40°; orecchie a ±15°.
  - Tre linguaggi nel logo: testa geometrica e precisa, archi a pennello secco, scritta a mano. Il sistema non deve aggiungere una quarta voce espressiva.
- **Fasi del progetto di identità** (il cliente approva ogni passaggio): 1 brief (domande inviate, risposte in attesa), 2 analisi logo (**approvata**), 3 tre direzioni creative, 4 sviluppo della direzione scelta.
  - Indicazione del cliente per la fase 3: andare oltre gli spunti ricavati dal logo, verso qualcosa di **più originale e con un effetto grafico molto forte**.
- **Regole d'uso del logo (decise dal cliente)**:
  - Il disegno del logo non si modifica né si reinterpreta: il sistema grafico si adatta intorno a lui.
  - Le versioni create in questo progetto restano tutte valide e non vanno cancellate.
  - **Sul sito si usa il logo completo, con gli archi** (`logo.svg` / `logo-bianco.svg`).
  - **Il logo senza archi si usa solo per la foto profilo Instagram.**
  - Il cliente permette di giocare con il logo (togliere gli archi, usare solo la scritta), ma di norma scritta e testa vanno insieme.
  - L'animale è **una pecora** (confermato): chiamarla sempre così.
  - **Configurazioni approvate**:
    - completo: sito, insegna, copertina del menu, materiali principali;
    - senza archi: solo foto profilo Instagram;
    - solo scritta: spazi orizzontali e stretti (barra del sito, fondo pagina, scontrini, intestazioni);
    - solo testa: usi piccoli e "da firma" (icona del browser, QR, timbri, sottobicchieri, adesivi, ghiaccio stampato).
  - **Colori del logo approvati**: nero e bianco sono i colori principali; anche l'antracite, che è il colore di tutto il locale.
  - Da chiarire: come va usata la pecora intera di profilo (personaggio/illustrazione, mai come secondo marchio).
- **Colori** (sito attuale, da rivedere nella fase 3): sfondo `#0d0d0d`, testo crema `#f2efe9`, grigio secondario `#9a958d`, linee `#2a2a2a`.
  - Antracite misurata sulle superfici: ardesia `#4c4c4c` in originale, `#353535` scurita del 30%. L'intonaco della prima foto è più caldo, circa `#574a38`.
- **Font**: Anton per i titoli da manifesto, Oswald per menu ed etichette (maiuscolo, spaziato), Inter per il testo. Sono ospitati in `assets/fonts/` con licenza OFL, quindi nessuna richiesta a Google e nessun banner cookie.
- **Texture**: ardesia antracite, scurita del 30% circa. Sul sito è `assets/ardesia.jpg`, una piastrella specchiata 1000×2000 fatta dall'originale 500×1000: con la versione ad alta risoluzione sparirebbe l'effetto specchio ai lati.

## Stato del codice
- Repository `chiccabasilee/Add-a-README-file`, branch `claude/qr-code-restaurant-menu-2vl2hr`.
- Pubblicazione prevista su GitHub Pages con il dominio personalizzato.
- `index.html` (home): apertura su ardesia con logo e due nastri inclinati, **storia**, **dietro al banco** (Giacomo e Domenico), nastri, **luogo**, **drink list**, **food della settimana**, pecora, fondo pagina crema.
  - La storia è il testo del cliente sistemato nel tono (proposto in chat, il cliente ha chiesto di imbastire e correggere strada facendo). Claim corto: "Uscire dagli schemi, un drink alla volta".
  - Il food della settimana in home è letto da `menu/menu.js`, quindi si aggiorna in un posto solo.
  - I testi sono bozze scritte senza informazioni dal cliente; le foto sono riquadri segnaposto.
- `site.js`: riempie i nastri che scorrono, gestisce il menu a tendina su telefono e mostra il food in home.
- `menu/`: pagina del menù pensata per il telefono, prima la drink list e poi il food.
  - Il contenuto sta in `menu/menu.js`, che per ora ha voci di esempio e `anteprima: true`. La sezione food ha il campo `settimana` con le date.
  - Barra delle categorie fissa in alto.
  - Legenda dei 14 allergeni (Reg. UE 1169/2011), nota sui surgelati, coperto.
- `style.css`: grafica comune alle pagine.
- `tools/genera_qr.py`: crea il QR in SVG (libreria segno) con `marchio.svg` al centro e correzione d'errore H. Le prove di lettura con OpenCV vanno bene fino a 110 px.
  - Il QR definitivo **non è ancora stato generato**: si fa quando il dominio è scelto.
- `motion/`: animazione "loading" per annunciare l'apertura, stile vecchio videogioco (12 fotogrammi al secondo). Su sfondo nero, come le pecore che si contano per dormire, pecore crema entrano una dopo l'altra da sinistra, saltano **un solo oggetto al centro** ed escono a destra. L'oggetto cambia a ogni salto: steccato, coppetta, shaker, pinta, bottiglia, fetta di limone. Sotto, LOADING e una barra che si accende di un blocco a ogni salto; l'ultimo blocco lampeggia. Il ciclo (13 s) si ripete senza stacchi. Niente numeri (tolti su richiesta del cliente).
  - `loading.html` si crea con `tools/genera_loading.py`, che usa le pose di `forme_pecora()` in `tools/genera_pecora.py`.
  - `loading.gif` (720×720), `loading-quadrato.mp4` (1080×1080) e `loading-storia.mp4` (1080×1920) si registrano con `node tools/registra_loading.js`. La GIF è ancora una prova da far approvare.
- `social/instagram-profilo.png`: foto profilo Instagram 1080×1080, già consegnata.
  - Logo bianco senza semicerchi, centrato, su ardesia scurita.
  - `instagram-profilo-chiara.png` è la stessa con la texture originale.

## Cosa manca dal cliente
1. Parere sulla nuova grafica (fatta sul modello di Freni e Frizioni).
2. Chi aggiorna il food ogni settimana. Due proposte:
   - un foglio Google che il sito legge da solo (consigliata);
   - il cliente manda il menu e lo aggiorna Claude.
3. Menu vero: drink e food, prezzi, coperto, allergeni, surgelati.
4. Conferma del testo della storia e dettagli su Giacomo e Domenico (dopo l'intervista del 2 novembre).
5. Foto: locale, bancone, drink, sala eventi, locandine degli eventi.
6. Orari di apertura.
7. Partita IVA, obbligatoria sul sito di un'attività.
8. Dominio scelto e acquistato.
9. Texture ad alta risoluzione.
10. Dove va stampato il QR (adesivo, segnatavolo, vetrina) e a che misura.
