/* Consent-gated analytics: GA4 (audience, acquisition, events) + Microsoft Clarity
 * (heatmaps, session recordings). Nothing loads before the visitor accepts.
 * Choice is stored for 6 months (CNIL recommendation), then asked again. */
(function () {
  var cfg = window.SITE_ANALYTICS || {};
  if (!cfg.ga4 && !cfg.clarity) return;

  var KEY = "consent-v1";
  var MAX_AGE = 1000 * 60 * 60 * 24 * 182;
  var page = document.body.dataset;

  function readChoice() {
    try {
      var c = JSON.parse(localStorage.getItem(KEY) || "null");
      if (c && Date.now() - c.t < MAX_AGE) return c.v;
    } catch (e) {}
    return null;
  }

  function saveChoice(v) {
    try { localStorage.setItem(KEY, JSON.stringify({ v: v, t: Date.now() })); } catch (e) {}
  }

  function loadScript(src) {
    var s = document.createElement("script");
    s.async = true;
    s.src = src;
    document.head.appendChild(s);
  }

  // --- event helpers ----------------------------------------------------------
  function track(name, params) {
    params = params || {};
    if (page.slug) {
      params.article_slug = page.slug;
      params.article_keyword = page.keyword;
    }
    if (window.gtag) window.gtag("event", name, params);
    if (window.clarity) window.clarity("event", name);
  }

  function articleContext() {
    if (!page.slug) return {};
    var ageDays = Math.floor((Date.now() - Date.parse(page.published)) / 86400000);
    return {
      article_slug: page.slug,
      article_keyword: page.keyword,
      article_tags: page.tags,
      article_words: Number(page.words),
      article_age_days: ageDays,
      content_group: page.tags ? page.tags.split(",")[0] : "article",
    };
  }

  // --- vendors ----------------------------------------------------------------
  function startGA4() {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("consent", "default", {
      ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied",
      analytics_storage: "granted",
    });
    var ctx = articleContext();
    ctx.page_type = page.slug ? "article" : (page.type || "page");
    window.gtag("config", cfg.ga4, ctx);
    loadScript("https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(cfg.ga4));
  }

  function startClarity() {
    (function (c, l, a, r, i) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      var t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
      var y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", cfg.clarity);
    window.clarity("consent");
    if (page.slug) {
      window.clarity("set", "article", page.slug);
      window.clarity("set", "keyword", page.keyword || "");
    }
  }

  // --- behaviour tracking -----------------------------------------------------
  function startBehaviour() {
    // Scroll depth milestones.
    var marks = [25, 50, 75, 100], hit = {};
    function onScroll() {
      var h = document.documentElement;
      var pct = (h.scrollTop + window.innerHeight) / h.scrollHeight * 100;
      marks.forEach(function (m) {
        if (pct >= m - 1 && !hit[m]) { hit[m] = 1; track("scroll_depth", { percent: m }); }
      });
      maybeRead();
    }
    window.addEventListener("scroll", onScroll, { passive: true });

    // Active (visible) reading time, and a "read" event once really read.
    var active = 0, read = false, last = Date.now();
    setInterval(function () {
      if (document.visibilityState === "visible") active += (Date.now() - last) / 1000;
      last = Date.now();
      maybeRead();
    }, 5000);
    function maybeRead() {
      if (read || !page.slug || !hit[75]) return;
      var expected = Number(page.words || 0) / 250 * 60 * 0.4;  // 40% of reading time
      if (active >= Math.max(30, expected)) {
        read = true;
        track("article_read", { engaged_seconds: Math.round(active) });
      }
    }
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "hidden" && page.slug) {
        track("reading_time", { engaged_seconds: Math.round(active), max_scroll: Object.keys(hit).pop() || 0 });
      }
    });

    // Clicks: internal links (where in the page), outbound links, TOC, tags.
    document.addEventListener("click", function (e) {
      var a = e.target.closest("a");
      if (!a) return;
      var zone = a.closest(".toc") ? "toc" : a.closest(".related") ? "related"
        : a.closest(".tags") ? "tags" : a.closest(".content") ? "body"
        : a.closest("header") ? "header" : a.closest("footer") ? "footer" : "other";
      var external = a.hostname && a.hostname !== location.hostname;
      track(external ? "outbound_click" : "internal_link_click", {
        link_url: a.href, link_text: (a.textContent || "").trim().slice(0, 100), link_zone: zone,
      });
    });

    // FAQ questions opened = what readers still wonder about.
    document.querySelectorAll(".faq details").forEach(function (d) {
      d.addEventListener("toggle", function () {
        if (d.open) track("faq_open", { question: d.querySelector("summary").textContent.slice(0, 100) });
      });
    });

    // Copied text (often numbers from worked examples).
    document.addEventListener("copy", function () {
      var txt = String(window.getSelection()).trim();
      if (txt) track("copy_text", { text: txt.slice(0, 100), length: txt.length });
    });
  }

  function start() {
    if (cfg.ga4) startGA4();
    if (cfg.clarity) startClarity();
    startBehaviour();
  }

  // --- banner -----------------------------------------------------------------
  var banner = document.getElementById("consent");
  function showBanner() { banner.hidden = false; }
  banner.querySelector("[data-accept]").addEventListener("click", function () {
    saveChoice("granted"); banner.hidden = true; start();
  });
  banner.querySelector("[data-refuse]").addEventListener("click", function () {
    var was = readChoice();
    saveChoice("denied"); banner.hidden = true;
    document.cookie.split(";").forEach(function (c) {
      var name = c.split("=")[0].trim();
      if (/^(_ga|_gid|_clck|_clsk|CLID|MUID)/.test(name)) {
        var host = location.hostname.split(".");
        for (var i = 0; i < host.length - 1; i++) {
          document.cookie = name + "=; Max-Age=0; path=/; domain=." + host.slice(i).join(".");
        }
        document.cookie = name + "=; Max-Age=0; path=/";
      }
    });
    if (was === "granted") location.reload();  // stop trackers already running
  });
  document.querySelectorAll("[data-consent-open]").forEach(function (el) {
    el.addEventListener("click", function (e) { e.preventDefault(); showBanner(); });
  });

  var choice = readChoice();
  if (choice === "granted") start();
  else if (choice === null) showBanner();
})();
