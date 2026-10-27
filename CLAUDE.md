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
- Le foto le fa un fotografo già istruito dal cliente. **Stile fotografico**: flash diretto, tra professionale e giovanile; mani in azione, inquadrature strette, rossi e ambre dei drink.

## Obiettivo
- Sito completo su un dominio proprio, che il locale comprerà (per esempio blacksheepmenfi.it).
- QR sui tavoli che porta direttamente alla drink list: `https://<dominio>/drink/`.
- **Struttura decisa dal cliente** (27 ottobre): due pagine, aperte dal menu ad hamburger.
  - **Home**, con dentro **la storia** più in basso (ancora `#storia`).
  - **Drink list** con i prezzi (`/drink/`).
  - Niente pagine Food, Sabato o Storia separata. **Il luogo** (indirizzo, orari, telefono per prenotare, Instagram) sta in fondo a ogni pagina. I contatti sono ancora da definire meglio.
- **Elementi obbligatori** indicati dal cliente: base nera/antracite; foto flash; storia in home; pagina drink con prezzi; **una fascia che scorre** con "ogni settimana un menu food diverso" e frasi simili.
- Il cliente vorrebbe vedere il sito come artefatto di Claude: non si pubblica perché porta nome e logo di un'attività reale. Si lavora sui file e si mandano anteprime.

## Direzione grafica attuale (27 ottobre)
- Il cliente ha **scartato le tre direzioni** della fase 3 (`brand/direzioni.md`) e ha mandato ispirazioni proprie:
  - siti di Sifón (Madrid, il preferito) e Cantine;
  - un bar con cartellini bianchi su nero (Dolges);
  - due locandine: titolo gigante sopra la foto (Estadio) e foto tagliata ad angoli (Heat).
- Regola del cliente: **ispirarsi a Sifón senza copiarlo**.
- Tratti presi dalle ispirazioni:
  - fondo scuro uniforme e foto flash a tutta pagina;
  - titoli giganti in un bastone larghissimo e nerissimo;
  - frasi grandi in maiuscolo leggero;
  - una riga "parlata" in corsivo;
  - tre foto con didascalia;
  - fondo pagina su foto.
- **Cosa la rende nostra**:
  - in apertura c'è il **logo completo** a mano, non una scritta tipografica;
  - **gli archi a pennello del logo**, in **verde fluo** e **accorciati** (`assets/archi-fluo.svg`, la parte centrale degli archi), fanno da segno a mano: racchiudono parole e pulsanti come parentesi tonde (classe `.arc`), invece dell'ellisse di Sifón. Gli originali `archi.svg` e `archi-bianco.svg` restano;
  - la **fascia che scorre** è verde fluo, con la testa della pecora nera come separatore;
  - **scarabocchi a mano in verde fluo** sopra le foto e accanto ai testi, ispirati alle immagini del cliente con disegni a pennarello. Sono in `assets/scarabocchi/`, creati da `tools/genera_scarabocchi.py`: freccia, aureola, gocce, fiamme, stelle, shaker (Giacomo), coppa, cerchio, sottolineatura, pecorella (illustrazione, non il logo). Si mettono con `<span data-doodle="nome" style="posizione">` e si disegnano quando entrano nello schermo;
  - **note scritte** in corsivo fluo (classe `.nota`, per esempio "il capo del banco", "new entry!");
  - **pin tondi con la scritta in cerchio** (ispirati agli adesivi delle immagini del cliente, testi in italiano), in `assets/pin/`, creati da `tools/genera_pin.py`:
    - `siciliano`: "100% siciliano · cocktail & food lab", con la Sicilia tutta nera che beve un drink con la cannuccia e Menfi come puntino verde. È bianco perché in home sta a cavallo della fascia verde, e l'anello gira di continuo.
    - Nella drink list, al posto delle scritte normali: `preferito` (il preferito di Giacomo, con lo shaker), `nuovo` (appena uscito dal banco), `analcolico` (0%, zero alcol), `casa` (drink della casa, con la testa del logo).
    - Si usano con `<span data-pin="nome">`. Nella drink list basta scrivere, per esempio, `etichette: ["preferito"]` in `drink/menu.js`: un solo pin per drink.
    - La Sicilia viene da Natural Earth (pubblico dominio, pacchetto `world-atlas`), salvata in `tools/dati/sicilia.json`.
    - I testi dei pin sono testi veri in Archivo: funzionano solo inseriti nella pagina. Per stamparli vanno convertiti in tracciati.
  - frasi e testi sono nostri: niente traduzioni delle frasi di Sifón o Cantine.
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
- **Fasi del progetto di identità** (il cliente approva ogni passaggio): 1 brief (fatto), 2 analisi logo (**approvata**), 3 tre direzioni creative (**scartate**, vedi sopra), 4 la direzione nata dalle ispirazioni del cliente, applicata subito al sito (**in attesa di commenti**).
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
- **Colori**: nero `#0D0D0D` (barra, menu, fondo pagina), antracite `#171717` (sfondo delle pagine), antracite chiaro `#262626`, bianco `#F4F4F2` (testi), grigio `#8C8C88` (testi secondari), **verde fluo `#39FF14`** come unico accento (archi, scarabocchi, note, adesivi, fascia).
  - Antracite misurata sulle superfici del locale: ardesia `#4c4c4c` in originale, `#353535` scurita del 30%. Il verde delle pareti non è ancora misurato.
- **Font** (ospitati in `assets/fonts/`, licenza OFL, nessuna richiesta a Google):
  - **Archivo** variabile per tutto: titoli giganti in larghezza 125% e peso 900, frasi in maiuscolo peso 300, testi peso 400.
  - **Archivo corsivo** (`archivo-variabile-corsivo.woff2`) per la riga "parlata" di ogni sezione (classe `.voce`) e per le note. **Niente serif**: il cliente li ha esclusi.
  - Oswald 600 resta solo per l'animazione `motion/`; Inter e Oswald 500 solo per la tavola `brand/analisi-logo`.
- **Texture**: `assets/ardesia.jpg` (ardesia scurita, piastrella specchiata) resta per la foto profilo Instagram; il nuovo sito non la usa.

## Stato del codice
- Repository `chiccabasilee/Add-a-README-file`, branch `claude/qr-code-restaurant-menu-2vl2hr`.
- Pubblicazione prevista su GitHub Pages con il dominio personalizzato.
- Barra, menu ad hamburger, fascia e fondo pagina sono ripetuti in `index.html` e `drink/index.html`: se si cambiano, vanno cambiati in entrambe.
  - Barra: "Menu" a sinistra, logo solo scritta al centro (compare dopo l'apertura), "Prenota" tra gli archi a destra.
  - Menu ad hamburger a tutto schermo: Home, La storia, Drink list, poi Prenota, Instagram e indirizzo.
- `index.html` (home), in ordine:
  - apertura con foto flash a tutto schermo e logo completo bianco;
  - fascia che scorre;
  - intro con frasi grandi;
  - tre foto con didascalia;
  - **storia** (`#storia`) con titolo gigante "Uscire dagli schemi" e Giacomo e Domenico;
  - invito alla drink list ("Drink list" gigante sopra la foto);
  - di nuovo la fascia;
  - fondo pagina su foto con Il luogo e il logo completo.
- `assets/foto/`: foto segnaposto grigie (`apertura`, `trio-1..3`, `giacomo`, `domenico`, `drink`, `fondo`). Dopo il 2 novembre si sostituiscono con le foto vere, stessi nomi. Per le anteprime al cliente si usano le sue ispirazioni, mai committate perché non sono nostre.
- `site.js`:
  - costruisce la fascia che scorre;
  - anima i testi: i titoli giganti salgono riga per riga, gli elementi con `data-reveal` entrano dal basso;
  - inserisce e disegna gli scarabocchi;
  - rende piena la barra dopo l'apertura e apre/chiude il menu (anche con Esc).
  - Chi ha "riduci movimento" attivo vede tutto fermo.
  - Una riga nel `<head>` di ogni pagina aggiunge la classe `js`, così i testi da animare non lampeggiano.
- Anteprime per il cliente: il sito **non** va pubblicato come artefatto (nome e logo di un'attività reale). Per mostrare le animazioni si registra un video dello scorrimento con Playwright (`recordVideo`) e ffmpeg, su una copia nella scratchpad con le foto d'ispirazione.
- `drink/`: pagina della drink list con i prezzi (ci arriva il QR).
  - In alto "Drink list" gigante sopra una foto, poi la fascia e la barra delle categorie fissa.
  - Il contenuto sta in `drink/menu.js`, che per ora ha voci di esempio e `anteprima: true`.
  - Legenda dei 14 allergeni (Reg. UE 1169/2011) e coperto.
- `style.css`: grafica comune alle pagine.
- `tools/genera_qr.py`: crea il QR in SVG (libreria segno) con `marchio.svg` al centro e correzione d'errore H. Le prove di lettura con OpenCV vanno bene fino a 110 px.
  - Il QR definitivo **non è ancora stato generato**: si fa quando il dominio è scelto.
- `motion/`: animazione "loading" per annunciare l'apertura, stile vecchio videogioco (16 fotogrammi al secondo). Su sfondo nero, come le pecore che si contano per dormire, pecore crema entrano una dopo l'altra da sinistra, saltano **un solo oggetto al centro** ed escono a destra. L'oggetto cambia a ogni salto, solo simboli da bar lab: coppetta, shaker, beuta, pinta, bottiglia, fetta di limone (lo steccato è stato tolto su richiesta del cliente). Sotto, LOADING e una barra che si accende di un blocco a ogni salto; l'ultimo blocco lampeggia. Il ciclo (9,8 s) si ripete senza stacchi. Niente numeri (tolti su richiesta del cliente).
  - `loading.html` si crea con `tools/genera_loading.py`, che usa le pose di `forme_pecora()` in `tools/genera_pecora.py`.
  - Due temi: nero di base, crema con pecore nere aprendo `loading.html?tema=chiaro`.
  - `node tools/registra_loading.js` crea i video per i post Instagram, 1080×1080, 32 fps (ogni fotogramma resta fermo due volte): `loading-post-nero.mp4` e `loading-post-bianco.mp4`, mandati al cliente per scegliere il tema; poi, su richiesta, le stesse in 4:5 (1080×1350) `loading-post-4x5-nero.mp4` e `loading-post-4x5-bianco.mp4`. Con dei nomi come argomenti registra solo quei formati. Crea anche `loading.gif` (720×720) e `loading-storia.mp4` (1080×1920), entrambi a tema nero.
- `social/instagram-profilo.png`: foto profilo Instagram 1080×1080, già consegnata.
  - Logo bianco senza semicerchi, centrato, su ardesia scurita.
  - `instagram-profilo-chiara.png` è la stessa con la texture originale.

## Cosa manca dal cliente
1. Commenti su pin, archi fluo, scarabocchi e animazioni (mandati come video). Il cliente vuole cambiare alcune frasi: chiedere quali.
2. Drink list vera: drink, prezzi, coperto, allergeni.
3. Come gestire i contatti (per ora: telefono per prenotare).
4. Conferma del testo della storia e dettagli su Giacomo e Domenico (dopo l'intervista del 2 novembre).
5. Foto: locale, bancone, drink, sala eventi, locandine degli eventi.
6. Orari di apertura.
7. Partita IVA, obbligatoria sul sito di un'attività.
8. Dominio scelto e acquistato.
9. Texture ad alta risoluzione.
10. Dove va stampato il QR (adesivo, segnatavolo, vetrina) e a che misura.
