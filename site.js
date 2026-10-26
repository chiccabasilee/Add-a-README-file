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

  // Menu ad hamburger a tutto schermo
  var nav = document.querySelector(".nav");
  var toggle = document.querySelector(".nav__toggle");
  if (nav && toggle) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("nav--open");
      toggle.setAttribute("aria-expanded", open);
      document.body.style.overflow = open ? "hidden" : "";
    });
    var close = function () {
      nav.classList.remove("nav--open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    };
    nav.querySelectorAll(".nav__panel a").forEach(function (a) { a.addEventListener("click", close); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  }

  if (window.MENU && window.MENU.anteprima) {
    var p = document.getElementById("preview");
    if (p) p.hidden = false;
  }
})();
