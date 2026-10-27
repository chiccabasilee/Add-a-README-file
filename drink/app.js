(function () {
  var data = window.MENU;
  var menu = document.getElementById("menu");
  var tabs = document.getElementById("tabs");

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  function slug(s) {
    return s.toLowerCase().normalize("NFD").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  }

  data.sezioni.forEach(function (sez, si) {
    if (si > 0) tabs.appendChild(el("span", "tabs__sep"));

    var group = el("section", "group");
    group.id = sez.id;
    // con una sola sezione il titolo grande è già in cima alla pagina
    if (data.sezioni.length > 1) group.appendChild(el("h2", "group__title", sez.nome));
    if (sez.settimana) group.appendChild(el("p", "week group__week", "Settimana " + sez.settimana));

    sez.categorie.forEach(function (cat) {
      var id = sez.id + "-" + slug(cat.nome);

      var tab = el("a", "tabs__item", cat.nome);
      tab.href = "#" + id;
      tabs.appendChild(tab);

      var sec = el("section", "cat");
      sec.id = id;
      sec.appendChild(el("h3", "cat__title", cat.nome));
      if (cat.nota) sec.appendChild(el("p", "cat__note", cat.nota));

      var list = el("ul", "items");
      cat.voci.forEach(function (v) {
        var li = el("li", "item");
        var head = el("div", "item__head");
        var name = el("span", "item__name", v.nome);
        if (v.surgelato) name.appendChild(el("span", "item__frozen", "*"));
        if (v.preferito) name.appendChild(el("span", "sticker", "Il preferito di Giacomo"));
        head.appendChild(name);
        head.appendChild(el("span", "item__price", "€ " + v.prezzo));
        li.appendChild(head);
        if (v.descrizione) li.appendChild(el("p", "item__desc", v.descrizione));
        if (v.allergeni && v.allergeni.length) {
          li.appendChild(el("p", "item__all", "Allergeni: " + v.allergeni.join(" · ")));
        }
        list.appendChild(li);
      });
      sec.appendChild(list);
      group.appendChild(sec);
    });

    menu.appendChild(group);
  });

  if (data.coperto) document.getElementById("coperto").textContent = "Coperto € " + data.coperto;
  if (data.anteprima) document.getElementById("preview").hidden = false;

  // Il menù è generato qui: se il link contiene #drink o #food, ci si porta lì ora
  if (location.hash) {
    var target = document.getElementById(location.hash.slice(1));
    if (target) target.scrollIntoView();
  }

  // Evidenzia la categoria visibile e la tiene in vista nella barra
  var links = tabs.querySelectorAll("a");
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      links.forEach(function (a) {
        var on = a.getAttribute("href") === "#" + e.target.id;
        a.classList.toggle("is-active", on);
        if (on) tabs.scrollTo({ left: a.offsetLeft - 16, behavior: "smooth" });
      });
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  document.querySelectorAll(".cat").forEach(function (s) { obs.observe(s); });
})();
