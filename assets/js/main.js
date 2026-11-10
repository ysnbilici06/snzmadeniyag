/* ==========================================================
   SNZ Madeni Yağ & Oto Market — ortak script
   İletişim bilgilerini yalnızca aşağıdaki SITE nesnesinden güncelleyin.
   ========================================================== */

const SITE = {
  phone1: "0543 488 22 53",
  phone2: "0541 334 22 51",
  whatsapp: "905434882253",           // başında 90, boşluksuz
  email: "info@snzmadeniyag.com",     // TODO: gerçek e-posta
  address: "Sehaş Arena İş Merkezi, Ahi Evran, 225. Cd. Sincan Sanayi Sitesi No:38D Blok1, Sincan/Ankara",
  addressShort: "Sehaş Arena İş Merkezi, Sincan Sanayi Sitesi, Ankara", // üst bar için kısa hali
  addressShortEn: "Sehaş Arena Business Center, Sincan Industrial Estate, Ankara",
  addressEn: "Sehaş Arena Business Center, Ahi Evran, 225th St., Sincan Industrial Estate No:38D Block 1, Sincan/Ankara, Türkiye",
  mapQuery: "39.9672737,32.562601",   // dükkânın koordinatı (gömülü harita)
  hours: { weekdays: "08:30 – 19:00", saturday: "08:30 – 19:00", sunday: "Kapalı", sundayEn: "Closed" },
  instagram: "#",
  mapsUrl: "https://www.google.com/maps/place/SNZ+MADEN%C4%B0+YA%C4%9E/@39.9672737,32.562601,17z/data=!4m6!3m5!1s0x14d33120fec1f999:0xb1a20a6dd8406cb8!8m2!3d39.9672737!4d32.562601!16s%2Fg%2F11xzzy9mgh",  // Google Haritalar işletme kaydı
  directionsUrl: "https://www.google.com/maps/dir/?api=1&destination=39.9672737,32.562601",
  googleReviewsUrl: "https://www.google.com/maps/place/SNZ+MADEN%C4%B0+YA%C4%9E/@39.9672737,32.562601,17z/data=!4m6!3m5!1s0x14d33120fec1f999:0xb1a20a6dd8406cb8!8m2!3d39.9672737!4d32.562601!16s%2Fg%2F11xzzy9mgh",  // Google yorumları (işletme kaydı)
};

/* ---------- Müşteri yorumları ----------
   Yalnızca GERÇEK yorumları ekleyin (örn. Google işletme profilinizden, müşterinin izniyle).
   Örnek: { name: "Ahmet Y.", text: "Yorum metni", rating: 5, source: "Google" },        */
const REVIEWS = [];

const tel = (p) => "tel:+90" + p.replace(/\D/g, "").replace(/^0/, "");
const waLink = (text = "") => `https://wa.me/${SITE.whatsapp}${text ? "?text=" + encodeURIComponent(text) : ""}`;

/* ---------- İkonlar ---------- */
const ICONS = {
  phone: '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
  pin: '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
  clock: '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
  mail: '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
  arrow: '<path d="M5 12h14M13 5l7 7-7 7"/>',
  check: '<circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 5-6"/>',
  oil: '<path d="M3 13h3l2-3h6l2 2h3l2-2v7a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M8 10V7h4v3M10 7V5M20 4s-2 2.2-2 3.5a2 2 0 0 0 4 0C22 6.2 20 4 20 4z"/>',
  battery: '<rect x="2" y="7" width="20" height="13" rx="2"/><path d="M6 7V4h3v3M15 7V4h3v3M6 13.5h4M8 11.5v4M14 13.5h4"/>',
  gear: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
  drop: '<path d="M12 2.7s-6 6.4-6 11.3a6 6 0 0 0 12 0c0-4.9-6-11.3-6-11.3z"/>',
  snow: '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1 19.1 4.9M9 4l3 2 3-2M9 20l3-2 3 2M4 9l2 3-2 3M20 9l-2 3 2 3"/>',
  filter: '<path d="M22 3H2l8 9.5V19l4 2v-8.5z"/>',
  truck: '<path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>',
  tractor: '<circle cx="7" cy="17" r="4"/><circle cx="19" cy="18" r="2"/><path d="M3 13V6h7l2 6h7v4M10 6V3"/>',
  shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
  tag: '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1.5"/>',
  wrench: '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
  bolt: '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
  users: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
  box: '<path d="M21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4a2 2 0 0 0 1-1.7z"/><path d="M3.3 7 12 12l8.7-5M12 22V12"/>',
  star: '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
  camera: '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
  car: '<path d="M5 17H3v-5l2-5h14l2 5v5h-2M5 12h14"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/>',
};
const WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zM20.5 3.5A11.8 11.8 0 0 0 1.9 17.7L.2 24l6.4-1.7A11.8 11.8 0 0 0 24 12c0-3.2-1.2-6.1-3.5-8.5z"/></svg>';

const svg = (name) =>
  name === "whatsapp" ? WA_ICON
    : `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[name] || ""}</svg>`;

/* ---------- Header & Footer ---------- */
const NAV = [
  ["index.html", "Ana Sayfa", "Home"],
  ["hakkimizda.html", "Hakkımızda", "About"],
  ["urunler.html", "Ürünler", "Products"],
  ["hizmetler.html", "Hizmetler", "Services"],
  ["projeler.html", "Projeler", "Projects"],
  ["galeri.html", "Galeri", "Gallery"],
  ["markalar.html", "Markalar", "Brands"],
  ["sss.html", "SSS", "FAQ"],
  ["iletisim.html", "İletişim", "Contact"],
];

function renderLayout() {
  const page = location.pathname.split("/").pop() || "index.html";
  const navLinks = NAV.map(([href, tr, en]) =>
    `<a href="${href}" class="${href === page ? "active" : ""}" data-en="${en}">${tr}</a>`).join("");

  const header = `
  <div class="topbar">
    <div class="container">
      <div class="topbar-info">
        <span class="tb-phones">${svg("phone")}<a href="${tel(SITE.phone1)}">${SITE.phone1}</a><i class="tb-sep">-</i><a href="${tel(SITE.phone2)}">${SITE.phone2}</a></span>
        <span class="hide-sm">${svg("pin")}<a href="${SITE.mapsUrl}" target="_blank" rel="noopener" data-en="${SITE.addressShortEn}">${SITE.addressShort}</a></span>
        <span class="hide-sm hide-md">${svg("clock")}<span data-en="Mon – Sat: ${SITE.hours.weekdays}">Pzt – Cmt: ${SITE.hours.weekdays}</span></span>
      </div>
      <div class="lang-switch" role="group" aria-label="Dil / Language">
        <button type="button" data-lang="tr">TR</button><button type="button" data-lang="en">EN</button>
      </div>
    </div>
  </div>
  <header class="header" id="header">
    <div class="container">
      <a href="index.html" class="logo" aria-label="SNZ Madeni Yağ">
        <span class="logo-mark">SNZ</span>
        <span class="logo-text"><span data-en="Lubricants &amp; Auto Market">Madeni Yağ &amp; Oto Market</span><small data-en="Battery Market">Akü Market</small></span>
      </a>
      <nav class="nav" id="nav">${navLinks}</nav>
      <div class="header-cta">
        <a href="${tel(SITE.phone1)}" class="btn btn-primary">${svg("phone")}<span data-en="Call Now">Hemen Ara</span></a>
        <button class="menu-toggle" id="menuToggle" aria-label="Menü"><span></span></button>
      </div>
    </div>
  </header>`;

  const footer = `
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <a href="index.html" class="logo">
            <span class="logo-mark">SNZ</span>
            <span class="logo-text"><span data-en="Lubricants &amp; Auto Market">Madeni Yağ &amp; Oto Market</span><small data-en="Battery Market">Akü Market</small></span>
          </a>
          <p class="footer-about" data-en="The right oil, battery and maintenance product for every vehicle and engine — with original products from leading brands and expert advice.">Her türlü araca ve motora uygun madeni yağ, akü ve bakım ürünleri; dünya markalarının orijinal ürünleri ve uzman tavsiyesiyle.</p>
        </div>
        <div>
          <h4 data-en="Pages">Sayfalar</h4>
          <ul>${NAV.map(([h, tr, en]) => `<li><a href="${h}" data-en="${en}">${tr}</a></li>`).join("")}</ul>
        </div>
        <div>
          <h4 data-en="Products">Ürünler</h4>
          <ul>
            <li><a href="urunler.html#motor" data-en="Engine Oils">Motor Yağları</a></li>
            <li><a href="urunler.html#aku" data-en="Batteries">Aküler</a></li>
            <li><a href="urunler.html#endustriyel" data-en="Hydraulic &amp; Grease">Hidrolik &amp; Gres</a></li>
            <li><a href="urunler.html#bakim" data-en="AdBlue &amp; Antifreeze">AdBlue &amp; Antifriz</a></li>
            <li><a href="urunler.html#bakim" data-en="Filters &amp; Care">Filtre &amp; Bakım</a></li>
          </ul>
        </div>
        <div>
          <h4 data-en="Contact">İletişim</h4>
          <ul class="footer-contact">
            <li>${svg("phone")}<span><a href="${tel(SITE.phone1)}">${SITE.phone1}</a><br><a href="${tel(SITE.phone2)}">${SITE.phone2}</a></span></li>
            <li>${svg("mail")}<a href="mailto:${SITE.email}">${SITE.email}</a></li>
            <li>${svg("pin")}<span data-en="${SITE.addressEn}">${SITE.address}</span></li>
            <li>${svg("clock")}<span data-en="Mon – Sat: ${SITE.hours.weekdays}<br>Sunday: ${SITE.hours.sundayEn}">Pzt – Cmt: ${SITE.hours.weekdays}<br>Pazar: ${SITE.hours.sunday}</span></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© ${new Date().getFullYear()} SNZ Madeni Yağ &amp; Oto Market. <span data-en="All rights reserved.">Tüm hakları saklıdır.</span></span>
        <span><a href="gizlilik.html" data-en="Privacy Policy &amp; KVKK">Gizlilik Politikası &amp; KVKK</a> · <a href="site-haritasi.html" data-en="Sitemap">Site Haritası</a></span>
      </div>
    </div>
  </footer>
  <div class="float-actions">
    <a href="${waLink("Merhaba, ürünleriniz hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener" class="float-btn float-wa" aria-label="WhatsApp">${WA_ICON}</a>
    <a href="${tel(SITE.phone1)}" class="float-btn float-call" aria-label="Ara">${svg("phone")}</a>
  </div>
  <nav class="mobile-bar" aria-label="Hızlı iletişim">
    <a href="${tel(SITE.phone1)}" class="mb-call">${svg("phone")}<span data-en="Call">Ara</span></a>
    <a href="${waLink("Merhaba, bilgi almak istiyorum.")}" target="_blank" rel="noopener" class="mb-wa">${WA_ICON}<span>WhatsApp</span></a>
    <a href="${SITE.directionsUrl}" target="_blank" rel="noopener" class="mb-map">${svg("pin")}<span data-en="Directions">Yol Tarifi</span></a>
  </nav>`;

  document.getElementById("site-header").outerHTML = header;
  document.getElementById("site-footer").outerHTML = footer;
}

/* ---------- Dil (TR / EN) ---------- */
function setLang(lang) {
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-en]").forEach((el) => {
    if (el.dataset.tr === undefined) el.dataset.tr = el.innerHTML;
    el.innerHTML = lang === "en" ? el.dataset.en : el.dataset.tr;
  });
  document.querySelectorAll("[data-en-ph]").forEach((el) => {
    if (el.dataset.trPh === undefined) el.dataset.trPh = el.placeholder;
    el.placeholder = lang === "en" ? el.dataset.enPh : el.dataset.trPh;
  });
  const t = document.body.dataset;
  if (t.titleEn) {
    if (!t.titleTr) t.titleTr = document.title;
    document.title = lang === "en" ? t.titleEn : t.titleTr;
  }
  document.querySelectorAll(".lang-switch button").forEach((b) =>
    b.classList.toggle("active", b.dataset.lang === lang));
  try { localStorage.setItem("snz-lang", lang); } catch (e) {}
}
const currentLang = () => document.documentElement.lang === "en" ? "en" : "tr";

/* ---------- Başlat ---------- */
document.addEventListener("DOMContentLoaded", () => {
  renderLayout();

  // Sayfa içindeki <i data-icon="..."> ve bağlantı yer tutucuları
  document.querySelectorAll("[data-icon]").forEach((el) => (el.outerHTML = svg(el.dataset.icon)));
  document.querySelectorAll("[data-site]").forEach((el) => {
    const key = el.dataset.site;
    if (key === "phone1" || key === "phone2") { el.href = tel(SITE[key]); if (!el.textContent.trim()) el.textContent = SITE[key]; }
    if (key === "whatsapp") el.href = waLink(el.dataset.msg || "Merhaba, bilgi almak istiyorum.");
    if (key === "address") { el.textContent = SITE.address; el.dataset.en = SITE.addressEn; }
    if (key === "maps") el.href = SITE.mapsUrl;
    if (key === "directions") el.href = SITE.directionsUrl;
    if (key === "email") { el.href = "mailto:" + SITE.email; if (!el.textContent.trim()) el.textContent = SITE.email; }
  });
  document.querySelectorAll("[data-map]").forEach((el) => {
    el.src = "https://maps.google.com/maps?q=" + encodeURIComponent(SITE.mapQuery) + "&z=17&output=embed";
  });

  // İletişim sayfası: adres ve saatler
  const fill = (id, tr, en) => {
    const el = document.getElementById(id);
    if (el) { el.innerHTML = tr; if (en) el.dataset.en = en; }
  };
  fill("addr", SITE.address, SITE.addressEn);
  fill("h-week", SITE.hours.weekdays);
  fill("h-sat", SITE.hours.saturday);
  fill("h-sun", SITE.hours.sunday, SITE.hours.sundayEn);

  // Dil
  let saved = "tr";
  try { saved = localStorage.getItem("snz-lang") || "tr"; } catch (e) {}
  setLang(saved);
  document.querySelectorAll(".lang-switch button").forEach((b) =>
    b.addEventListener("click", () => setLang(b.dataset.lang)));

  // Mobil menü
  const header = document.getElementById("header");
  document.getElementById("menuToggle").addEventListener("click", () => header.classList.toggle("menu-open"));
  header.querySelectorAll(".nav a").forEach((a) => a.addEventListener("click", () => header.classList.remove("menu-open")));

  // Header gölgesi
  const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 10);
  onScroll(); window.addEventListener("scroll", onScroll, { passive: true });

  // Görünme animasyonu
  const io = new IntersectionObserver((entries) => entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); }
  }), { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  // Sayaç
  document.querySelectorAll("[data-count]").forEach((el) => {
    const end = +el.dataset.count, suffix = el.dataset.suffix || "";
    const cio = new IntersectionObserver(([e]) => {
      if (!e.isIntersecting) return; cio.disconnect();
      const t0 = performance.now();
      const step = (t) => {
        const p = Math.min((t - t0) / 1400, 1);
        el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))).toLocaleString("tr-TR") + suffix;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
    cio.observe(el);
  });

  // SSS akordeon
  document.querySelectorAll(".faq-q").forEach((q) => q.addEventListener("click", () => {
    const item = q.parentElement, a = item.querySelector(".faq-a");
    const open = item.classList.toggle("open");
    q.setAttribute("aria-expanded", open);
    a.style.maxHeight = open ? a.scrollHeight + "px" : 0;
  }));

  // Ürün filtresi
  const filterBtns = document.querySelectorAll(".filter-bar button");
  const applyFilter = (cat) => {
    filterBtns.forEach((b) => b.classList.toggle("active", b.dataset.filter === cat));
    document.querySelectorAll(".product").forEach((p) =>
      p.classList.toggle("hidden", cat !== "all" && p.dataset.cat !== cat));
  };
  filterBtns.forEach((b) => b.addEventListener("click", () => applyFilter(b.dataset.filter)));
  if (filterBtns.length && location.hash) {
    const h = location.hash.slice(1);
    if ([...filterBtns].some((b) => b.dataset.filter === h)) applyFilter(h);
  }

  // Müşteri yorumları
  const rv = document.getElementById("reviews");
  if (rv) {
    const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
    if (REVIEWS.length) {
      rv.innerHTML = REVIEWS.map((r) => `<figure class="review card">
        <div class="stars" aria-label="${r.rating || 5}/5">${"★".repeat(r.rating || 5)}${"☆".repeat(5 - (r.rating || 5))}</div>
        <blockquote>${esc(r.text)}</blockquote>
        <figcaption><strong>${esc(r.name)}</strong>${r.source ? `<span>${esc(r.source)}</span>` : ""}</figcaption></figure>`).join("");
    } else rv.remove();
    document.querySelectorAll("[data-reviews-link]").forEach((a) => {
      if (SITE.googleReviewsUrl) a.href = SITE.googleReviewsUrl; else a.href = SITE.mapsUrl;
    });
  }

  // Galeri: büyütme penceresi (lightbox)
  const lbItems = () => [...document.querySelectorAll("[data-full]")].filter((el) => el.offsetParent !== null);
  if (document.querySelector("[data-full]")) {
    const lb = document.createElement("div");
    lb.className = "lightbox";
    lb.innerHTML = `<button class="lb-close" aria-label="Kapat">&times;</button>
      <button class="lb-prev" aria-label="Önceki">&#8249;</button>
      <figure><img alt=""><figcaption></figcaption></figure>
      <button class="lb-next" aria-label="Sonraki">&#8250;</button>`;
    document.body.appendChild(lb);
    const img = lb.querySelector("img"), cap = lb.querySelector("figcaption");
    let idx = 0;
    const show = (i) => {
      const items = lbItems(); if (!items.length) return;
      idx = (i + items.length) % items.length;
      const el = items[idx], t = el.querySelector("img");
      img.src = el.dataset.full; img.alt = t ? t.alt : "";
      cap.textContent = currentLang() === "en" ? (el.dataset.capEn || t.alt) : t.alt;
      lb.classList.add("open"); document.body.style.overflow = "hidden";
    };
    const close = () => { lb.classList.remove("open"); document.body.style.overflow = ""; };
    document.addEventListener("click", (e) => {
      const el = e.target.closest("[data-full]");
      if (el) { e.preventDefault(); show(lbItems().indexOf(el)); }
    });
    lb.querySelector(".lb-close").onclick = close;
    lb.querySelector(".lb-prev").onclick = () => show(idx - 1);
    lb.querySelector(".lb-next").onclick = () => show(idx + 1);
    lb.addEventListener("click", (e) => { if (e.target === lb) close(); });
    document.addEventListener("keydown", (e) => {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
  }

  // İletişim formu → WhatsApp
  const form = document.getElementById("contactForm");
  if (form) form.addEventListener("submit", (e) => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(form));
    const en = currentLang() === "en";
    const note = d.message ? "\n\n" + d.message : "";
    const msg = en
      ? `Hello, I'm ${d.name}.\nSubject: ${d.subject}\nVehicle: ${d.vehicle || "-"}${note}`
      : `Merhaba, ben ${d.name}.\nKonu: ${d.subject}\nAraç: ${d.vehicle || "-"}${note}`;
    window.open(waLink(msg), "_blank", "noopener");
    location.href = "tesekkurler.html";
  });
});
