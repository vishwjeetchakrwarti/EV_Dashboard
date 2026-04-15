/* =============================================
   EVPULSE DASHBOARD — main.js
   Path: ev_dashboard/static/js/main.js
   =============================================
   Features:
   1. CSV load karta hai aur stat cards fill karta hai
   2. Nav active state — scroll pe highlight
   3. Smooth scroll nav links ke liye
   4. Chart image error — placeholder dikhata hai
   5. Page load animations trigger
   ============================================= */


/* ============================================================
   1. CSV FETCH & PARSE — Stat Cards Fill Karna
   ============================================================ */

const CSV_PATH = "../data/Electric_Vehicle_Population_Data.csv";

// CSV text ko rows ke array mein convert karta hai
function parseCSV(text) {
  const lines  = text.trim().split("\n");
  const header = lines[0].split(",").map(h => h.trim().replace(/^"|"$/g, ""));
  const rows   = [];

  for (let i = 1; i < lines.length; i++) {
    const cols = smartSplit(lines[i]);
    if (cols.length < header.length) continue;
    const obj  = {};
    header.forEach((h, idx) => {
      obj[h] = (cols[idx] || "").trim().replace(/^"|"$/g, "");
    });
    rows.push(obj);
  }
  return rows;
}

// Comma split — quoted fields handle karta hai
function smartSplit(line) {
  const cols   = [];
  let cur      = "";
  let inQuote  = false;

  for (let ch of line) {
    if (ch === '"') {
      inQuote = !inQuote;
    } else if (ch === "," && !inQuote) {
      cols.push(cur);
      cur = "";
    } else {
      cur += ch;
    }
  }
  cols.push(cur);
  return cols;
}

// Numbers ko Indian/US short format mein convert karta hai  e.g. 185000 → 1.85L or 185K
function formatNum(n) {
  if (n >= 100000) return (n / 100000).toFixed(2) + "L";
  if (n >= 1000)   return (n / 1000).toFixed(1)   + "K";
  return n.toString();
}

// Counter animation — 0 se target tak
function animateCount(el, target, duration = 1400) {
  const start     = performance.now();
  const isDecimal = target % 1 !== 0;

  function step(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased    = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current  = Math.round(eased * target);
    el.textContent = formatNum(current);
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = formatNum(target);
  }
  requestAnimationFrame(step);
}

// Stat card elements
const elTotal  = document.getElementById("totalEVs");
const elBEV    = document.getElementById("totalBEV");
const elPHEV   = document.getElementById("totalPHEV");
const elCities = document.getElementById("totalCities");

// CSV load karke stats calculate karna
async function loadStats() {
  try {
    const resp = await fetch("/api/stats");
    if (!resp.ok) throw new Error("API error " + resp.status);

    const json = await resp.json();

    animateCount(elTotal,  json.total_evs);
    animateCount(elBEV,    json.total_bev);
    animateCount(elPHEV,   json.total_phev);
    animateCount(elCities, json.total_cities);

  } catch (err) {
    console.warn("Stats load nahi hua:", err.message);
    [elTotal, elBEV, elPHEV, elCities].forEach(el => {
      if (el) el.textContent = "N/A";
    });
  }
}
// async function loadStats() {
//   try {
//     const resp = await fetch(CSV_PATH);
//     if (!resp.ok) throw new Error("CSV not found — " + resp.status);

//     const text = await resp.text();
//     const rows = parseCSV(text);

//     const total  = rows.length;
//     const bev    = rows.filter(r => r["Electric Vehicle Type"]?.includes("BEV")).length;
//     const phev   = rows.filter(r => r["Electric Vehicle Type"]?.includes("PHEV")).length;
//     const cities = new Set(rows.map(r => r["City"]).filter(Boolean)).size;

//     // Cards mein animate karke dikhao
//     animateCount(elTotal,  total);
//     animateCount(elBEV,    bev);
//     animateCount(elPHEV,   phev);
//     animateCount(elCities, cities);

//   } catch (err) {
//     console.warn("CSV load nahi hua:", err.message);
//     // Fallback — dashes dikhao
//     [elTotal, elBEV, elPHEV, elCities].forEach(el => {
//       if (el) el.textContent = "N/A";
//     });
//   }
// }

// Page ready hone pe load karo
document.addEventListener("DOMContentLoaded", loadStats);


/* ============================================================
   2. CHART IMAGE PLACEHOLDER — agar png na mile
   ============================================================ */

// index.html mein onerror="showPlaceholder(this, 'filename')" se call hota hai
function showPlaceholder(imgEl, filename) {
  const wrapper = imgEl.closest(".chart-wrapper");
  if (!wrapper) return;

  wrapper.innerHTML = `
    <div class="chart-placeholder">
      <span>📊</span>
      <span style="font-size:13px;color:var(--text-secondary)">Chart abhi generate nahi hua</span>
      <code>charts/${filename}</code>
      <span style="font-size:11px;color:var(--text-muted);margin-top:4px">
        Pehle <strong style="color:var(--accent)">generate_charts.py</strong> chalao
      </span>
    </div>`;
}

// Global mein expose karo (HTML onerror ke liye)
window.showPlaceholder = showPlaceholder;


/* ============================================================
   3. NAV — Active Link (Scroll-based Highlight)
   ============================================================ */

const NAV_LINKS = document.querySelectorAll(".nav-link[href^='#']");
const SECTIONS  = Array.from(NAV_LINKS)
  .map(a => document.querySelector(a.getAttribute("href")))
  .filter(Boolean);

function updateActiveNav() {
  const scrollY = window.scrollY + 100; // header height offset

  let current = SECTIONS[0];
  SECTIONS.forEach(sec => {
    if (sec.offsetTop <= scrollY) current = sec;
  });

  NAV_LINKS.forEach(a => {
    const isActive = a.getAttribute("href") === "#" + current?.id;
    a.classList.toggle("active", isActive);
  });
}

window.addEventListener("scroll", updateActiveNav, { passive: true });
updateActiveNav(); // page load pe bhi run karo


/* ============================================================
   4. SMOOTH SCROLL — Nav Links
   ============================================================ */

NAV_LINKS.forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    const target = document.querySelector(link.getAttribute("href"));
    if (!target) return;

    const offset = 80; // sticky header height
    const top    = target.getBoundingClientRect().top + window.scrollY - offset;

    window.scrollTo({ top, behavior: "smooth" });
  });
});


/* ============================================================
   5. INTERSECTION OBSERVER — Chart Cards Animate on Scroll
   ============================================================ */

const OBSERVER_OPTIONS = {
  threshold: 0.12,
  rootMargin: "0px 0px -40px 0px"
};

const cardObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animationPlayState = "running";
      cardObserver.unobserve(entry.target);
    }
  });
}, OBSERVER_OPTIONS);

// Saare chart-card aur stat-card ko observe karo
document.querySelectorAll(".chart-card, .stat-card").forEach(card => {
  card.style.animationPlayState = "paused"; // pehle rok do
  cardObserver.observe(card);
});


/* ============================================================
   6. CHART IMAGE — Lightbox (click pe bada karna)
   ============================================================ */

// Lightbox overlay create karo
const lightbox = document.createElement("div");
lightbox.id    = "lightbox";
lightbox.style.cssText = `
  display:none; position:fixed; inset:0; z-index:9999;
  background:rgba(0,0,0,0.88); backdrop-filter:blur(8px);
  align-items:center; justify-content:center; cursor:zoom-out;
`;
lightbox.innerHTML = `
  <img id="lb-img" style="
    max-width:92vw; max-height:90vh; border-radius:12px;
    box-shadow:0 0 60px rgba(0,200,255,0.25);
    animation:lbIn .25s ease;
  "/>
  <span id="lb-close" style="
    position:fixed; top:22px; right:28px;
    font-size:28px; color:#fff; cursor:pointer; opacity:0.7;
  ">✕</span>
`;
document.body.appendChild(lightbox);

// Lightbox CSS animation
const lbStyle       = document.createElement("style");
lbStyle.textContent = `@keyframes lbIn { from{opacity:0;transform:scale(.94)} to{opacity:1;transform:scale(1)} }`;
document.head.appendChild(lbStyle);

const lbImg   = document.getElementById("lb-img");
const lbClose = document.getElementById("lb-close");

// Chart image click pe lightbox kholo
document.querySelectorAll(".chart-img").forEach(img => {
  img.style.cursor = "zoom-in";
  img.addEventListener("click", () => {
    lbImg.src            = img.src;
    lbImg.alt            = img.alt;
    lightbox.style.display = "flex";
    document.body.style.overflow = "hidden";
  });
});

// Lightbox band karo
function closeLightbox() {
  lightbox.style.display       = "none";
  document.body.style.overflow = "";
}

lightbox.addEventListener("click", e => { if (e.target === lightbox) closeLightbox(); });
lbClose.addEventListener("click", closeLightbox);
document.addEventListener("keydown", e => { if (e.key === "Escape") closeLightbox(); });


/* ============================================================
   7. CONSOLE WELCOME MESSAGE
   ============================================================ */

console.log(
  "%c⚡ EVPULSE Dashboard Loaded",
  "color:#00c8ff; font-family:monospace; font-size:14px; font-weight:bold;"
);
console.log(
  "%c📂 CSV Path: " + CSV_PATH,
  "color:#00ff9d; font-family:monospace; font-size:11px;"
);
