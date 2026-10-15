(function () {
  "use strict";

  var LANGS = ["pt", "en"];
  var STORAGE_KEY = "lang";
  var T = window.I18N || {};

  function readSaved() {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }
  function save(lang) {
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) { /* armazenamento indisponivel: segue sem salvar */ }
  }
  function initialLang() {
    var saved = readSaved();
    if (LANGS.indexOf(saved) !== -1) return saved;
    var nav = (navigator.language || "pt").toLowerCase();
    return nav.indexOf("pt") === 0 ? "pt" : "en";
  }

  function text(key, lang) {
    var entry = T[key];
    if (!entry || typeof entry[lang] !== "string") {
      console.warn("i18n: chave ausente", key, lang);
      return null;
    }
    return entry[lang];
  }

  function apply(lang) {
    document.documentElement.lang = lang === "pt" ? "pt-BR" : "en";

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var v = text(el.getAttribute("data-i18n"), lang);
      if (v !== null) el.textContent = v;
    });
    document.querySelectorAll("[data-i18n-alt]").forEach(function (el) {
      var v = text(el.getAttribute("data-i18n-alt"), lang);
      if (v !== null) el.setAttribute("alt", v);
    });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      var v = text(el.getAttribute("data-i18n-aria"), lang);
      if (v !== null) el.setAttribute("aria-label", v);
    });

    var title = text("meta.title", lang);
    if (title) document.title = title;
    var desc = text("meta.description", lang);
    var meta = document.querySelector('meta[name="description"]');
    if (desc && meta) meta.setAttribute("content", desc);

    document.querySelectorAll(".lang button").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-lang") === lang));
    });
  }

  function setLang(lang) {
    apply(lang);
    save(lang);
  }

  // Foto: mostra a imagem so se carregar; senao fica o avatar com a inicial.
  function setupPhoto() {
    var img = document.getElementById("foto");
    if (!img) return;
    function show() { img.hidden = false; }
    function hide() { img.hidden = true; }
    img.addEventListener("load", show);
    img.addEventListener("error", hide);
    if (img.complete) { if (img.naturalWidth > 0) show(); else hide(); }
  }

  // Carrossel: botoes rolam a faixa; a faixa tambem e navegavel pelo teclado.
  function setupCarousels() {
    document.querySelectorAll(".carousel").forEach(function (c) {
      var track = c.querySelector(".track");
      var prev = c.querySelector(".car-btn.prev");
      var next = c.querySelector(".car-btn.next");
      if (!track) return;
      function step(dir) { track.scrollBy({ left: dir * track.clientWidth * 0.8, behavior: "smooth" }); }
      if (prev) prev.addEventListener("click", function () { step(-1); });
      if (next) next.addEventListener("click", function () { step(1); });
    });
  }

  // Lightbox: a miniatura abre na mesma pagina, com X, Esc e clique no fundo para sair.
  function setupLightbox() {
    var box = document.getElementById("lightbox");
    var img = document.getElementById("lb-img");
    if (!box || !img || typeof box.showModal !== "function") return; // sem suporte: o link abre a imagem normalmente
    var stage = box.querySelector(".lb-stage");
    var closeBtn = box.querySelector(".lb-close");

    function open(link) {
      var thumb = link.querySelector("img");
      img.alt = thumb ? thumb.alt : "";
      stage.classList.remove("tall");
      stage.scrollTop = 0;
      img.onload = function () {
        stage.classList.toggle("tall", img.naturalHeight / img.naturalWidth > 1.2);
      };
      img.src = link.getAttribute("href");
      box.showModal();
    }

    document.querySelectorAll(".track a").forEach(function (a) {
      a.addEventListener("click", function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return; // deixa abrir em outra aba se pedir
        e.preventDefault();
        open(a);
      });
    });

    closeBtn.addEventListener("click", function () { box.close(); });
    box.addEventListener("click", function (e) {
      if (e.target === box || e.target === stage) box.close();
    });
    box.addEventListener("close", function () { img.removeAttribute("src"); });
  }

  document.querySelectorAll(".lang button").forEach(function (b) {
    b.addEventListener("click", function () { setLang(b.getAttribute("data-lang")); });
  });

  setupPhoto();
  setupCarousels();
  setupLightbox();
  apply(initialLang());
})();
