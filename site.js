(function () {
  // Fascia che scorre: le frasi sono ripetute due volte di fila, così lo scorrimento non ha stacchi
  document.querySelectorAll(".band[data-items]").forEach(function (band) {
    var items = band.getAttribute("data-items").split("|");
    var icon = band.getAttribute("data-icon");
    var track = document.createElement("div");
    track.className = "band__track";
    track.setAttribute("aria-hidden", "true");
    for (var i = 0; i < 8; i++) {
      items.forEach(function (text) {
        var item = document.createElement("span");
        item.className = "band__item";
        var img = document.createElement("img");
        img.src = icon;
        img.alt = "";
        item.appendChild(img);
        item.appendChild(document.createTextNode(text));
        track.appendChild(item);
      });
    }
    band.textContent = "";
    band.appendChild(track);
  });

  // Barra in alto: diventa piena dopo l'apertura; menu ad hamburger a tutto schermo
  var nav = document.querySelector(".nav");
  var toggle = document.querySelector(".nav__toggle");
  if (nav) {
    var solid = function () { nav.classList.toggle("nav--solid", window.scrollY > 40); };
    solid();
    window.addEventListener("scroll", solid, { passive: true });
  }
  if (nav && toggle) {
    var close = function () {
      nav.classList.remove("nav--open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    };
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("nav--open");
      toggle.setAttribute("aria-expanded", open);
      document.body.style.overflow = open ? "hidden" : "";
    });
    nav.querySelectorAll(".nav__panel a").forEach(function (a) { a.addEventListener("click", close); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  }

  if (window.MENU && window.MENU.anteprima) {
    var p = document.getElementById("preview");
    if (p) p.hidden = false;
  }
})();
