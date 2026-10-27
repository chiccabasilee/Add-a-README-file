(function () {
  document.documentElement.classList.add("js");
  var base = new URL(".", document.currentScript.src).href;
  var calmo = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Fascia che scorre: le frasi sono ripetute due volte di fila, così lo scorrimento non ha stacchi
  document.querySelectorAll(".band[data-items]").forEach(function (band) {
    var items = band.getAttribute("data-items").split("|");
    var track = document.createElement("div");
    track.className = "band__track";
    track.setAttribute("aria-hidden", "true");
    for (var i = 0; i < 8; i++) {
      items.forEach(function (text) {
        var item = document.createElement("span");
        item.className = "band__item";
        var img = document.createElement("img");
        img.src = base + "assets/logo-testa.svg";
        img.alt = "";
        item.appendChild(img);
        item.appendChild(document.createTextNode(text));
        track.appendChild(item);
      });
    }
    band.textContent = "";
    band.appendChild(track);
  });

  // Titoli giganti: ogni riga entra dal basso, dentro una maschera
  document.querySelectorAll(".mega").forEach(function (el) {
    el.innerHTML = el.innerHTML.split(/<br\s*\/?>/i).map(function (riga) {
      return '<span class="riga"><span>' + riga.trim() + "</span></span>";
    }).join("");
  });

  // Scarabocchi: l'SVG viene inserito nella pagina, così il tratto si può disegnare
  var disegna = function (el) {
    var paths = el.querySelectorAll("path");
    paths.forEach(function (p, i) {
      var len = p.getTotalLength();
      p.style.strokeDasharray = len;
      p.style.strokeDashoffset = calmo ? 0 : len;
      p.style.transition = "stroke-dashoffset " + Math.min(1.2, .4 + len / 900) + "s ease " + (.25 + i * .18) + "s";
    });
  };
  var inserisci = function (selettore, cartella, classe, dopo) {
    return Array.prototype.map.call(document.querySelectorAll(selettore), function (el) {
      el.classList.add(classe);
      var nome = el.getAttribute(selettore.slice(1, -1));
      return fetch(base + "assets/" + cartella + "/" + nome + ".svg")
        .then(function (r) { return r.text(); })
        .then(function (svg) { el.innerHTML = svg; if (dopo) dopo(el); });
    });
  };
  // Pin tondi con la scritta in cerchio (assets/pin), inseriti allo stesso modo
  var caricati = inserisci("[data-doodle]", "scarabocchi", "doodle", disegna)
    .concat(inserisci("[data-pin]", "pin", "pin-box"));

  // Quando un elemento entra nello schermo: testi che salgono, scarabocchi che si disegnano
  var mostra = function (el) {
    el.classList.add("in");
    el.querySelectorAll("path").forEach(function (p) { p.style.strokeDashoffset = 0; });
  };
  var osservati = document.querySelectorAll("[data-reveal], .mega, .nota, [data-doodle]");
  if (calmo || !("IntersectionObserver" in window)) {
    Promise.all(caricati).then(function () { osservati.forEach(mostra); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { mostra(e.target); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -12% 0px" });
    Promise.all(caricati).then(function () { osservati.forEach(function (el) { io.observe(el); }); });
  }

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
