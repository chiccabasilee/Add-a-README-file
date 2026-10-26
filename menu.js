// Contenuto del menu. Per aggiornare un piatto o un prezzo basta modificare questo file.
// allergeni: numeri della legenda in fondo alla pagina (Reg. UE 1169/2011).
// surgelato: true aggiunge l'asterisco "prodotto surgelato".

window.MENU = {
  anteprima: true, // mettere false quando il menu è quello definitivo

  coperto: "2,00",

  categorie: [
    {
      nome: "Cocktail Signature",
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
    },
    {
      nome: "Food",
      voci: [
        { nome: "Nome piatto", descrizione: "Ingredienti principali", prezzo: "0,00", allergeni: [1, 3, 7] },
        { nome: "Nome piatto", descrizione: "Ingredienti principali", prezzo: "0,00", allergeni: [1, 7], surgelato: true }
      ]
    }
  ]
};
