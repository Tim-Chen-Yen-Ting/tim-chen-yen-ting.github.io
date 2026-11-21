(function () {
  var panels = Array.prototype.slice.call(document.querySelectorAll(".panel"));
  var tabLinks = Array.prototype.slice.call(document.querySelectorAll("#tabs a"));
  var ids = panels.map(function (p) { return p.id.replace("panel-", ""); });

  function show() {
    var id = (location.hash || "#about").slice(1);
    if (ids.indexOf(id) === -1) id = "about";
    document.body.setAttribute("data-tab", id);
    panels.forEach(function (p) { p.classList.toggle("active", p.id === "panel-" + id); });
    tabLinks.forEach(function (a) {
      var on = a.getAttribute("href") === "#" + id;
      a.classList.toggle("current", on);
      if (on) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", show);
  show();
  // the browser's own jump-to-hash can land after the script runs; reset once more
  window.addEventListener("load", function () { window.scrollTo(0, 0); });

  // Project dialogs
  document.querySelectorAll("[data-open]").forEach(function (tile) {
    tile.addEventListener("click", function () {
      var d = document.getElementById(tile.getAttribute("data-open"));
      if (d && d.showModal) d.showModal();
    });
  });
  document.querySelectorAll("dialog.modal").forEach(function (d) {
    // click on the backdrop (the dialog element itself) closes it
    d.addEventListener("click", function (e) { if (e.target === d) d.close(); });
  });

  // Language toggle (EN / 中文), remembered across visits
  var TITLES = { "en": "Yen-Ting (Tim) Chen", "zh-Hant": "陳彥廷 (Tim)" };
  function setLang(l) {
    if (l !== "en" && l !== "zh-Hant") l = "en";
    var root = document.documentElement;
    root.setAttribute("data-lang", l);
    root.setAttribute("lang", l);
    document.title = TITLES[l];
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
