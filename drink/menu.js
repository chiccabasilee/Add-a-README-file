// Contenuto della drink list. Per aggiornare un piatto o un prezzo basta modificare questo file.
// allergeni: numeri della legenda in fondo alla pagina (Reg. UE 1169/2011).

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
            { nome: "Nome cocktail", descrizione: "Ingrediente, ingrediente, guarnizione", prezzo: "0,00" },
            { nome: "Nome cocktail", descrizione: "Ingrediente, ingrediente, guarnizione", prezzo: "0,00" },
            { nome: "Nome cocktail", descrizione: "Ingrediente, ingrediente, guarnizione", prezzo: "0,00" }
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
