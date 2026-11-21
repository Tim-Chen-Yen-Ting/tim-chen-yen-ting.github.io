(function () {
  var panels = Array.prototype.slice.call(document.querySelectorAll(".panel"));
  var tabLinks = Array.prototype.slice.call(document.querySelectorAll("#tabs a"));
  var ids = panels.map(function (p) { return p.id.replace("panel-", ""); });

  function show() {
    var parts = (location.hash || "#home").slice(1).split("/");
    var id = parts[0], slug = parts[1];
    if (id === "about" || id === "experience") id = "home"; // old links still work; #experience/phygtl lives on Home
    if (ids.indexOf(id) === -1) id = "home";
    document.body.setAttribute("data-tab", id);
    panels.forEach(function (p) { p.classList.toggle("active", p.id === "panel-" + id); });
    tabLinks.forEach(function (a) {
      var on = a.getAttribute("href") === "#" + id;
      a.classList.toggle("current", on);
      if (on) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    window.scrollTo(0, 0);
    // Deep link: #projects/civilizism or #experience/phygtl opens that popup
    if (slug) {
      var dlg = document.querySelector('dialog.modal[data-slug="' + slug + '"]');
      if (dlg && !dlg.open && dlg.showModal) dlg.showModal();
    }
  }
  window.addEventListener("hashchange", show);
  show();
  // the browser's own jump-to-hash can land after the script runs; reset once more
  window.addEventListener("load", function () { window.scrollTo(0, 0); });

  // Project dialogs: any element with data-open opens its dialog (links inside it still work normally)
  function openFrom(el) {
    var d = document.getElementById(el.getAttribute("data-open"));
    if (d && d.showModal && !d.open) {
      d.showModal();
      // keep the address bar shareable while a popup is open
      if (d.dataset.slug && history.replaceState) history.replaceState(null, "", "#" + d.dataset.section + "/" + d.dataset.slug);
    }
  }
  var openedByKeyboard = false;
  document.addEventListener("click", function (e) {
    if (e.target.closest("a")) return;
    var t = e.target.closest("[data-open]");
    if (t) {
      openedByKeyboard = e.detail === 0; // a real mouse click reports detail >= 1
      openFrom(t);
    }
  });
  document.addEventListener("keydown", function (e) {
    if ((e.key === "Enter" || e.key === " ") && e.target.matches && e.target.matches('[role="button"][data-open]')) {
      e.preventDefault();
      openedByKeyboard = true;
      openFrom(e.target);
    }
  });
  document.querySelectorAll("dialog.modal").forEach(function (d) {
    // click on the backdrop (the dialog element itself) closes it
    d.addEventListener("click", function (e) { if (e.target === d) d.close(); });
    // Closing a dialog hands focus back to whatever opened it, which leaves it looking "hovered".
    // Keep that for keyboard users; for mouse users, drop it.
    d.addEventListener("close", function () {
      var a = document.activeElement;
      if (!openedByKeyboard && a && a !== document.body && a.blur) a.blur();
      if (d.dataset.slug && history.replaceState) history.replaceState(null, "", "#" + (document.body.getAttribute("data-tab") || "home"));
    });
  });

  // Language toggle (EN / 中文), remembered across visits
  var TITLES = { "en": "Yen-Ting (Tim) Chen | AI Systems & Evaluation, UCLA Statistics & Data Science", "zh-Hant": "陳彥廷 (Tim) | AI 系統與評測，UCLA 統計與資料科學" };
  function setLang(l) {
    if (l !== "en" && l !== "zh-Hant") l = "en";
    var root = document.documentElement;
    root.setAttribute("data-lang", l);
    root.setAttribute("lang", l);
    document.title = document.body.getAttribute(l === "en" ? "data-title-en" : "data-title-zh") || TITLES[l];
    try { localStorage.setItem("lang", l); } catch (e) {}
  }
  var saved = null;
  try { saved = localStorage.getItem("lang"); } catch (e) {}
  setLang(saved || "en");
  document.querySelectorAll("[data-set-lang]").forEach(function (b) {
    b.addEventListener("click", function () { setLang(b.getAttribute("data-set-lang")); });
  });

  // Live local times for the Contact page
  function tick() {
    [["clock-la", "America/Los_Angeles"], ["clock-tpe", "Asia/Taipei"]].forEach(function (c) {
      var el = document.getElementById(c[0]);
      if (!el) return;
      try {
        el.textContent = new Intl.DateTimeFormat("en-US", {
          timeZone: c[1], hour: "numeric", minute: "2-digit", weekday: "short"
        }).format(new Date());
      } catch (e) { el.textContent = "--:--"; }
    });
  }
  tick();
  setInterval(tick, 20000);

  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
