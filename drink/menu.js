// Contenuto della drink list. Per aggiornare un piatto o un prezzo basta modificare questo file.
// allergeni: numeri della legenda in fondo alla pagina (Reg. UE 1169/2011).
// etichette: un pin tondo sulla voce, uno solo per drink:
//   "preferito" (il preferito di Giacomo), "nuovo", "analcolico", "casa" (drink della casa).

window.MENU = {
  anteprima: true, // mettere false quando il menù è quello definitivo

  coperto: "", // es. "2,00"; vuoto = non mostrato

  sezioni: [
    {
      id: "drink", // il QR punta alla pagina /drink/
      nome: "Drink list",
      categorie: [
        {
          nome: "Signature",
          nota: "I nostri drink, creati al banco",
          voci: [
            { nome: "Nome cocktail", descrizione: "Ingrediente, ingrediente, guarnizione", prezzo: "0,00", etichette: ["preferito"] },
            { nome: "Nome cocktail", descrizione: "Ingrediente, ingrediente, guarnizione", prezzo: "0,00", etichette: ["nuovo"] },
            { nome: "Nome cocktail", descrizione: "Ingrediente, ingrediente, guarnizione", prezzo: "0,00", etichette: ["casa"] }
          ]
        },
        {
          nome: "Classici",
          voci: [
            { nome: "Nome cocktail", descrizione: "Ingrediente, ingrediente", prezzo: "0,00" },
            { nome: "Nome cocktail", descrizione: "Ingrediente, ingrediente", prezzo: "0,00" }
          ]
        },
        {
          nome: "Analcolici",
          voci: [
            { nome: "Nome analcolico", descrizione: "Ingrediente, ingrediente", prezzo: "0,00", etichette: ["analcolico"] }
          ]
        },
        {
          nome: "Vini",
          voci: [
            { nome: "Nome vino", descrizione: "Cantina · Denominazione", prezzo: "0,00 / 0,00" },
            { nome: "Nome vino", descrizione: "Cantina · Denominazione", prezzo: "0,00 / 0,00" }
          ]
        },
        {
          nome: "Birre",
          voci: [
            { nome: "Nome birra", descrizione: "Stile · 0,4 l", prezzo: "0,00", allergeni: [1] }
          ]
        }
      ]
    }
  ]
};
