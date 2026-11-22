(function () {
  var panels = Array.prototype.slice.call(document.querySelectorAll(".panel"));
  var tabLinks = Array.prototype.slice.call(document.querySelectorAll("#tabs a"));
  var ids = panels.map(function (p) { return p.id.replace("panel-", ""); });

  function show() {
    if (document.body.hasAttribute("data-fixed-tab")) return; // standalone pages keep their own highlighted tab
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

  // Civilizism toy: media-style controls stepping one simulated housemate through seven stages of a day.
  var pl = document.getElementById("stageplay");
  if (pl) {
    pl.addEventListener("click", function (e) { e.stopPropagation(); }); // don't open the card's popup
    var caps = pl.querySelectorAll("#caps li"), clk = document.getElementById("clk"), agent = document.getElementById("agent"),
        bub = document.getElementById("bubble"), scrub = document.getElementById("scrub"), pbtn = document.getElementById("playbtn"),
        cur = 0, timer = null;
    function go(i) {
      cur = (i + caps.length) % caps.length; // wraps: the last stage leads back to the first
      caps.forEach(function (li, k) { li.classList.toggle("on", k === cur); });
      var li = caps[cur];
      clk.textContent = li.getAttribute("data-t");
      bub.textContent = li.getAttribute("data-emoji");
      agent.style.left = (Number(li.getAttribute("data-room")) * 33.333 + 16.667) + "%";
      scrub.value = cur;
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } pl.classList.remove("playing"); pbtn.textContent = "▶"; pbtn.setAttribute("aria-label", "Play"); }
    function play() {
      pl.classList.add("playing"); pbtn.textContent = "❚❚"; pbtn.setAttribute("aria-label", "Pause");
      timer = setInterval(function () { go(cur + 1); }, 1700); // loops until paused
    }
    pl.querySelectorAll(".tbtn").forEach(function (b) {
      b.addEventListener("click", function () {
        var t = b.getAttribute("data-t");
        if (t === "play") { if (timer) stop(); else play(); return; }
        stop();
        go(t === "first" ? 0 : t === "last" ? caps.length - 1 : t === "prev" ? cur - 1 : cur + 1);
      });
    });
    scrub.addEventListener("input", function () { stop(); go(Number(scrub.value)); });
    go(0);
  }

  // Nightly-eval toy on the Phygtl card: a physical button that counts to 192. It does not call anything.
  var run = document.getElementById("runbtn"), lcd = document.getElementById("lcd"), led = document.getElementById("led");
  if (run && lcd && led) {
    var busy = false;
    run.addEventListener("click", function (e) {
      e.stopPropagation(); // don't open the card's popup
      if (busy) return;
      busy = true; run.disabled = true; led.className = "led run";
      var n = 0;
      function finish() { lcd.textContent = "192 / 192"; led.className = "led ok"; run.disabled = false; busy = false; }
      if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) { finish(); return; }
      var t = setInterval(function () {
        n = Math.min(192, n + 8);
        lcd.textContent = ("00" + n).slice(-3) + " / 192";
        if (n >= 192) { clearInterval(t); finish(); }
      }, 45);
    });
  }

  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
