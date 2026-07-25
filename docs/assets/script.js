(function () {
  "use strict";

  var REPO_OWNER = "gapolli";
  var REPO_NAME = "bagde-gen";

  /* ============================================================
     1. THEME TOGGLE
     ============================================================ */
  var themeToggle = document.getElementById("themeToggle");
  var html = document.documentElement;

  var savedTheme = localStorage.getItem("badgegen-theme");
  if (savedTheme === "light") html.classList.remove("dark");

  themeToggle.addEventListener("click", function () {
    html.classList.toggle("dark");
    var isDark = html.classList.contains("dark");
    localStorage.setItem("badgegen-theme", isDark ? "dark" : "light");
  });

  /* ============================================================
     2. SMOOTH SCROLL
     ============================================================ */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      var target = document.querySelector(anchor.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  /* ============================================================
     3. TOAST
     ============================================================ */
  function showToast(msg) {
    var toast = document.getElementById("toast");
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(function () {
      toast.classList.remove("show");
    }, 2000);
  }

  /* ============================================================
     4. INTERSECTION OBSERVER (fade-in animations)
     ============================================================ */
  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }
      });
    },
    { threshold: 0.1 },
  );

  function animateSelector(selector) {
    document.querySelectorAll(selector).forEach(function (el) {
      io.observe(el);
    });
  }

  /* ============================================================
     5. REPO STATS
     ============================================================ */
  fetch("https://api.github.com/repos/" + REPO_OWNER + "/" + REPO_NAME)
    .then(function (r) {
      return r.json();
    })
    .then(function (d) {
      document.getElementById("starCount").textContent =
        d.stargazers_count != null ? d.stargazers_count : "—";
      document.getElementById("forkCount").textContent =
        d.forks_count != null ? d.forks_count : "—";
      document.getElementById("issueCount").textContent =
        d.open_issues_count != null ? d.open_issues_count : "—";
    })
    .catch(function () {
      document.getElementById("starCount").textContent = "—";
      document.getElementById("forkCount").textContent = "—";
      document.getElementById("issueCount").textContent = "—";
    });

  /* ============================================================
     6. BADGE BUILDER
     ============================================================ */
  var b = {
    label: document.getElementById("badgeLabel"),
    message: document.getElementById("badgeMessage"),
    color: document.getElementById("badgeColor"),
    colorHex: document.getElementById("badgeColorHex"),
    labelColor: document.getElementById("badgeLabelColor"),
    style: document.getElementById("badgeStyle"),
    logo: document.getElementById("badgeLogo"),
    logoToggle: document.getElementById("logoColorToggle"),
    logoColor: document.getElementById("badgeLogoColor"),
    preview: document.getElementById("badgePreview"),
    url: document.getElementById("badgeUrl"),
    markdown: document.getElementById("badgeMarkdown"),
    copyBtn: document.getElementById("copyBtn"),
    copyMdBtn: document.getElementById("copyMdBtn"),
  };

  function san(s) {
    return encodeURIComponent(String(s || "").trim());
  }

  function buildUrl() {
    var label = san(b.label.value || "badge");
    var message = san(b.message.value || "demo");
    var color = b.colorHex.value.replace("#", "") || "blue";
    var url =
      "https://img.shields.io/badge/" + label + "-" + message + "-" + color;
    var params = ["style=" + b.style.value];
    if (b.logo.value.trim()) params.push("logo=" + san(b.logo.value));
    if (b.logoToggle.checked)
      params.push("logoColor=" + b.logoColor.value.replace("#", ""));
    var lc = b.labelColor.value.replace("#", "");
    if (lc && lc !== "555555") params.push("labelColor=" + lc);
    return url + "?" + params.join("&");
  }

  function updateBuilder() {
    var u = buildUrl();
    b.preview.src = u;
    b.preview.alt = b.label.value + " " + b.message.value;
    b.url.textContent = u;
    b.markdown.textContent = "![" + b.label.value + "](" + u + ")";
  }

  b.color.addEventListener("input", function () {
    b.colorHex.value = b.color.value.slice(1);
    updateBuilder();
  });
  b.colorHex.addEventListener("input", function () {
    var v = b.colorHex.value.startsWith("#")
      ? b.colorHex.value
      : "#" + b.colorHex.value;
    if (/^#[0-9A-Fa-f]{6}$/.test(v)) {
      b.color.value = v;
      updateBuilder();
    }
  });
  b.logoToggle.addEventListener("change", function () {
    b.logoColor.style.display = b.logoToggle.checked ? "" : "none";
    updateBuilder();
  });
  [b.label, b.message, b.style, b.logo, b.logoColor, b.labelColor].forEach(
    function (el) {
      el.addEventListener("input", updateBuilder);
      el.addEventListener("change", updateBuilder);
    },
  );

  b.copyBtn.addEventListener("click", function () {
    navigator.clipboard.writeText(b.url.textContent).then(function () {
      b.copyBtn.classList.add("copied");
      b.copyBtn.textContent = "✅ Copied!";
      showToast("URL copied to clipboard");
      setTimeout(function () {
        b.copyBtn.classList.remove("copied");
        b.copyBtn.textContent = "📋 Copy";
      }, 2000);
    });
  });

  b.copyMdBtn.addEventListener("click", function () {
    navigator.clipboard.writeText(b.markdown.textContent).then(function () {
      b.copyMdBtn.classList.add("copied");
      b.copyMdBtn.textContent = "✅ Copied!";
      showToast("Markdown copied to clipboard");
      setTimeout(function () {
        b.copyMdBtn.classList.remove("copied");
        b.copyMdBtn.textContent = "📋 Copy";
      }, 2000);
    });
  });

  updateBuilder();

  /* ============================================================
     7. CLI TERMINAL SIMULATOR
     ============================================================ */
  var tout = document.getElementById("terminalOutput");
  var tin = document.getElementById("terminalInput");
  var qbtns = document.querySelectorAll(".quick-btn");

  var cliResp = {
    help:
      "<strong>Badge Gen CLI v1.0.0 — Available Commands:</strong><br>" +
      '• <code class="bg-gray-800 px-2 py-0.5 rounded text-term-green">generate badge &lt;label&gt; &lt;message&gt; [style] [color]</code> — Create a badge<br>' +
      '• <code class="bg-gray-800 px-2 py-0.5 rounded text-term-green">list templates</code> — Show available badge templates<br>' +
      '• <code class="bg-gray-800 px-2 py-0.5 rounded text-term-green">batch generate &lt;config.json&gt;</code> — Process multiple badges<br>' +
      '• <code class="bg-gray-800 px-2 py-0.5 rounded text-term-green">version</code> — Show version info<br>' +
      '• <code class="bg-gray-800 px-2 py-0.5 rounded text-term-green">clear</code> — Clear terminal',
    version:
      '<span style="color:#3fb950">Badge Gen CLI v1.0.0</span><br>' +
      "Python engine: 3.12.0<br>Bash wrapper: 5.x<br>GitHub Actions: Compatible ✓",
    "list templates":
      '<span style="color:#58a6ff">Available Templates:</span><br>' +
      '• <code class="bg-gray-800 px-2 py-0.5 rounded text-term-green">tech-stack</code> — Technology badges (Python, Node, Docker, etc.)<br>' +
      '• <code class="bg-gray-800 px-2 py-0.5 rounded text-term-green">ci-status</code> — Build/test/coverage status<br>' +
      '• <code class="bg-gray-800 px-2 py-0.5 rounded text-term-green">security</code> — Snyk/vulnerability scanning<br>' +
      '• <code class="bg-gray-800 px-2 py-0.5 rounded text-term-green">metrics</code> — UptimeRobot, performance metrics',
    "batch generate config.json":
      '<span style="color:#3fb950">✓ Batch processing complete!</span><br>' +
      "Generated 3 badge sections from config.json<br>Updated: README.md<br>" +
      '<span style="color:#58a6ff">Tip: git add README.md && git commit -m "docs: updated badges"</span>',
  };

  function addLine(html, extraClass) {
    var line = document.createElement("div");
    line.className = "mb-2" + (extraClass ? " " + extraClass : "");
    line.innerHTML = html;
    tout.appendChild(line);
    tout.scrollTop = tout.scrollHeight;
  }

  function processCmd(cmd) {
    var t = cmd.toLowerCase().trim();

    if (t === "clear") {
      tout.innerHTML = "";
      return;
    }

    if (t.indexOf("generate badge") === 0) {
      var parts = cmd.split(/\s+/).slice(2);
      if (parts.length >= 2) {
        var label = parts[0],
          message = parts[1],
          style = parts[2] || "for-the-badge",
          color = parts[3] || "blue";
        var url =
          "https://img.shields.io/badge/" +
          encodeURIComponent(label) +
          "-" +
          encodeURIComponent(message) +
          "-" +
          color +
          "?style=" +
          style;
        addLine(
          '<span style="color:#3fb950">✓ Badge generated successfully!</span>',
        );
        addLine(
          'URL: <code class="bg-gray-800 px-2 py-0.5 rounded text-term-green">' +
            url +
            "</code>",
        );
        addLine(
          '<span style="color:#58a6ff">Preview:</span> <img src="' +
            url +
            '" style="vertical-align:middle;margin-top:8px;">',
        );
        return;
      } else {
        addLine(
          '<span style="color:#ff5f57">Error: Missing arguments. Usage: generate badge &lt;label&gt; &lt;message&gt; [style] [color]</span>',
        );
        return;
      }
    }

    if (cliResp[t]) {
      addLine(cliResp[t]);
      return;
    }

    addLine(
      '<span style="color:#ff5f57">Command not found: \'' +
        cmd +
        "'. Type 'help' for available commands.</span>",
    );
  }

  tin.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      var cmd = tin.value.trim();
      if (cmd) {
        addLine('<span style="color:#3fb950;font-weight:bold">$</span> ' + cmd);
        processCmd(cmd);
      }
      tin.value = "";
    }
  });

  qbtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var cmd = btn.getAttribute("data-cmd");
      addLine('<span style="color:#3fb950;font-weight:bold">$</span> ' + cmd);
      processCmd(cmd);
      tin.focus();
    });
  });

  document
    .querySelector(".bg-gray-950.border.border-gray-800.rounded-xl")
    .addEventListener("click", function () {
      tin.focus();
    });

  /* ============================================================
     8. CONTRIBUTORS
     ============================================================ */
  fetch(
    "https://api.github.com/repos/" +
      REPO_OWNER +
      "/" +
      REPO_NAME +
      "/contributors?per_page=30",
  )
    .then(function (r) {
      return r.json();
    })
    .then(function (data) {
      var grid = document.getElementById("contributorsGrid");
      if (!Array.isArray(data) || data.length === 0) {
        grid.innerHTML =
          '<div class="col-span-full text-center text-gray-500 py-10">No contributors yet. Be the first to contribute! 🚀</div>';
        return;
      }
      grid.innerHTML = data
        .map(function (c) {
          return (
            '<a href="' +
            c.html_url +
            '" target="_blank" rel="noopener" class="contributor-card flex flex-col items-center gap-2 text-center p-5 border border-gray-800 rounded-xl bg-gray-800/50 no-underline text-inherit hover:border-gray-600 transition-all">' +
            '<img src="' +
            c.avatar_url +
            '" alt="' +
            c.login +
            '" loading="lazy" class="w-16 h-16 rounded-full border-2 border-term-green">' +
            '<span class="font-semibold text-sm">' +
            c.login +
            "</span>" +
            '<span class="text-xs text-gray-500">' +
            c.contributions +
            " commits</span>" +
            "</a>"
          );
        })
        .join("");
      animateSelector(".contributor-card");
    })
    .catch(function () {
      document.getElementById("contributorsGrid").innerHTML =
        '<div class="col-span-full text-center text-gray-500 py-10">⚠️ Could not load contributors (API rate limit). <a href="https://github.com/' +
        REPO_OWNER +
        "/" +
        REPO_NAME +
        '/graphs/contributors" style="color:#3fb950" target="_blank" rel="noopener">Visit the repo ↗</a></div>';
    });

  /* ============================================================
     9. CHANGELOG
     ============================================================ */
  fetch(
    "https://api.github.com/repos/" +
      REPO_OWNER +
      "/" +
      REPO_NAME +
      "/releases?per_page=10",
  )
    .then(function (r) {
      return r.json();
    })
    .then(function (data) {
      var tl = document.getElementById("changelogTimeline");
      if (!Array.isArray(data) || data.length === 0) {
        tl.innerHTML =
          '<div class="timeline-item relative mb-9">' +
          '<div class="timeline-dot"></div>' +
          '<span class="inline-block bg-term-green/15 text-term-green text-xs font-bold px-2.5 py-0.5 rounded-full mb-2">Upcoming</span>' +
          '<div class="bg-gray-800/50 border border-gray-800 rounded-xl p-4 mt-2"><p class="text-sm text-gray-400">No releases published yet. Watch this space — the first release is coming soon! ⭐</p></div>' +
          "</div>";
        return;
      }
      tl.innerHTML = data
        .map(function (r) {
          var dt = new Date(r.published_at || r.created_at).toLocaleDateString(
            "en-US",
            { year: "numeric", month: "short", day: "numeric" },
          );
          var body = (r.body || "No release notes provided.")
            .replace(/```[\s\S]*?```/g, "")
            .replace(/[#>*_]/g, "")
            .trim();
          if (body.length > 350) body = body.substring(0, 350) + "…";
          var tag = r.tag_name || "untagged";
          var pre = r.prerelease
            ? '<span class="inline-block bg-term-yellow/15 text-term-yellow text-xs font-bold px-2.5 py-0.5 rounded-full mb-2">pre-release</span> '
            : "";
          return (
            '<div class="timeline-item relative mb-9">' +
            '<div class="timeline-dot"></div>' +
            pre +
            '<span class="inline-block bg-term-green/15 text-term-green text-xs font-bold px-2.5 py-0.5 rounded-full mb-2">v' +
            tag +
            "</span>" +
            '<span class="text-xs text-gray-500 ml-2">' +
            dt +
            "</span>" +
            '<div class="bg-gray-800/50 border border-gray-800 rounded-xl p-4 mt-2">' +
            '<p class="text-sm text-gray-400">' +
            body +
            "</p>" +
            '<a href="' +
            r.html_url +
            '" target="_blank" rel="noopener" style="display:inline-block;margin-top:10px;color:#3fb950;font-size:0.85rem;text-decoration:none;font-weight:600;">View full release →</a>' +
            "</div>" +
            "</div>"
          );
        })
        .join("");
      animateSelector(".timeline-item");
    })
    .catch(function () {
      document.getElementById("changelogTimeline").innerHTML =
        '<div class="timeline-item relative mb-9"><div class="timeline-dot"></div>' +
        '<span class="inline-block bg-term-green/15 text-term-green text-xs font-bold px-2.5 py-0.5 rounded-full mb-2">Info</span>' +
        '<div class="bg-gray-800/50 border border-gray-800 rounded-xl p-4 mt-2"><p class="text-sm text-gray-400">Could not load releases (API rate limit). <a href="https://github.com/' +
        REPO_OWNER +
        "/" +
        REPO_NAME +
        '/releases" style="color:#3fb950" target="_blank" rel="noopener">Visit the releases page ↗</a></p></div></div>';
    });

  /* ============================================================
     10. INIT ANIMATIONS
     ============================================================ */
  animateSelector(".feature-card");
  animateSelector(".flow-step");
  animateSelector(".gallery-group > div");
})();
