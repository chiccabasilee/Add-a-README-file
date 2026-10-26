(function () {
  // Nastri: il testo viene ripetuto due volte di fila, così lo scorrimento non ha stacchi
  document.querySelectorAll(".tape[data-text]").forEach(function (tape) {
    var text = tape.getAttribute("data-text");
    var half = new Array(8).join(text + " — ");
    var track = document.createElement("span");
    track.className = "tape__track";
    track.setAttribute("aria-hidden", "true");
    track.textContent = half + half;
    tape.textContent = "";
    tape.appendChild(track);
  });

  // Menu a tendina su telefono
  var nav = document.querySelector(".nav");
  var toggle = document.querySelector(".nav__toggle");
  if (nav && toggle) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("nav--open");
      toggle.setAttribute("aria-expanded", open);
      document.body.style.overflow = open ? "hidden" : "";
    });
    nav.querySelectorAll(".nav__links a").forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("nav--open");
        toggle.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
      });
    });
  }

  // Home: food della settimana preso dallo stesso file del menù
  var dishes = document.getElementById("dishes");
  if (dishes && window.MENU) {
    var food = window.MENU.sezioni.filter(function (s) { return s.id === "food"; })[0];
    if (food) {
      if (food.settimana) document.getElementById("week").textContent = "Settimana " + food.settimana;
      food.categorie.forEach(function (cat) {
        cat.voci.forEach(function (v) {
          var li = document.createElement("li");
          var left = document.createElement("div");
          var name = document.createElement("strong");
          name.textContent = v.nome;
          left.appendChild(name);
          if (v.descrizione) {
            var d = document.createElement("span");
            d.textContent = v.descrizione;
            left.appendChild(d);
          }
          var price = document.createElement("em");
          price.textContent = "€ " + v.prezzo;
          li.appendChild(left);
          li.appendChild(price);
          dishes.appendChild(li);
        });
      });
    }
  }

  if (window.MENU && window.MENU.anteprima) {
    var p = document.getElementById("preview");
    if (p) p.hidden = false;
  }
})();
