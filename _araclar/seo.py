"""
SNZ sitesi — SEO derleyici.
Tüm sayfaların <head> bölümünü, sitemap.xml ve robots.txt dosyalarını üretir.
Alan adı değişirse yalnızca SITE_URL'i güncelleyip çalıştırın:
    python _araclar/seo.py
"""
import json, os, re, html, hashlib
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://www.snzmadeniyag.com"   # TODO: gerçek alan adı
BASE_PATH = "/snzmadeniyag/"                # GitHub Pages önizlemesi; kendi alan adında "/" yapın
GSC_CODE = ""                                # Google Search Console doğrulama kodu (content="..." değeri)

PHONE1, PHONE2 = "+90-543-488-22-53", "+90-541-334-22-51"
EMAIL = "snzmadeniyag@hotmail.com"
STREET = "Sehaş Arena İş Merkezi, Ahi Evran, 225. Cd. Sincan Sanayi Sitesi No:38D Blok1"
CITY, REGION = "Sincan", "Ankara"
POSTAL = "06935"
GEO = {"@type": "GeoCoordinates", "latitude": 39.9672737, "longitude": 32.562601}
MAP_URL = "https://www.google.com/maps/place/SNZ+MADEN%C4%B0+YA%C4%9E/@39.9672737,32.562601,17z/data=!4m6!3m5!1s0x14d33120fec1f999:0xb1a20a6dd8406cb8!8m2!3d39.9672737!4d32.562601!16s%2Fg%2F11xzzy9mgh"
HOURS = [{"@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
          "opens": "08:30", "closes": "19:00"}]

# sayfa: (başlık, açıklama, og görseli, işaret yolu adı, indexlensin mi, sitemap önceliği)
PAGES = {
 "index.html": ("SNZ Madeni Yağ & Akü Market Ankara | Motor Yağı, Akü, AdBlue",
   "Ankara Sincan Sanayi Sitesi'nde SNZ Madeni Yağ & Oto Market ve SNZ Akü Market: Castrol, Shell, Mobil, Motul, Petrol Ofisi motor yağları, aküler, hidrolik ve gres yağları, AdBlue. Yağ değişimi ve ücretsiz akü testi.",
   "og-index.jpg", None, True, "1.0"),
 "hakkimizda.html": ("Hakkımızda | SNZ Madeni Yağ & Akü Market Ankara",
   "SNZ Madeni Yağ & Oto Market ve SNZ Akü Market: Sincan Sanayi Sitesi, Sehaş Arena İş Merkezi'nde yan yana iki mağaza. Orijinal ürün, uzman tavsiye ve uygun fiyatla madeni yağ ve akü.",
   "og-hakkimizda.jpg", "Hakkımızda", True, "0.8"),
 "urunler.html": ("Ürünler: Motor Yağı, Akü, Gres, AdBlue | SNZ Ankara",
   "Tam sentetik ve mineral motor yağları, binek ve ağır vasıta aküleri, hidrolik, şanzıman ve gres yağları, AdBlue, antifriz ve bakım ürünleri. Ankara'da stoktan teslim.",
   "og-urunler.jpg", "Ürünler", True, "0.9"),
 "hizmetler.html": ("Yağ Değişimi, Akü Montajı, Sahada Yağlama | SNZ Ankara",
   "Lift üzerinde yağ değişimi, ücretsiz akü testi ve montajı, vinç ve iş makinelerinde sahada endüstriyel yağlama, toptan satış ve filo tedariki.",
   "og-hizmetler.jpg", "Hizmetler", True, "0.9"),
 "projeler.html": ("Örnek İşlerimiz: Saha Yağlama, Yağ Değişimi, Akü | SNZ",
   "Vinç ve platform yağlama, doğru normla yağ değişimi ve ağır vasıta akü montajı: SNZ'nin atölyeden ve sahadan gerçek iş örnekleri.",
   "og-projeler.jpg", "Projeler", True, "0.7"),
 "galeri.html": ("Galeri: Mağaza, Atölye ve Saha Fotoğrafları | SNZ Ankara",
   "SNZ Madeni Yağ ve Akü Market fotoğraf ve video galerisi: mağazalarımız, yağ değişimi, akü reyonu ve sahada vinç yağlama çalışmaları.",
   "og-galeri.jpg", "Galeri", True, "0.6"),
 "markalar.html": ("Markalar: Castrol, Shell, Mobil, Motul, Turbo Akü | SNZ",
   "Castrol, Shell, Mobil, Total, Elf, Opet, Motul ve Petrol Ofisi motor yağları ile Turbo Akü. Tüm araç markalarına uygun orijinal ürünler.",
   "og-markalar.jpg", "Markalar", True, "0.6"),
 "sss.html": ("Sıkça Sorulan Sorular: Motor Yağı ve Akü | SNZ Ankara",
   "Hangi motor yağı uygun, yağ ne sıklıkla değişir, akü ne zaman değişmeli, AdBlue nedir? Motor yağı ve akü hakkında kısa ve net cevaplar.",
   "og-sss.jpg", "SSS", True, "0.6"),
 "iletisim.html": ("İletişim ve Yol Tarifi | SNZ Madeni Yağ & Akü Market Ankara",
   "SNZ Madeni Yağ & Oto Market ve SNZ Akü Market adres, telefon, WhatsApp ve çalışma saatleri. Sehaş Arena İş Merkezi, Sincan Sanayi Sitesi, Ankara. Pzt–Cmt 08:30–19:00.",
   "og-iletisim.jpg", "İletişim", True, "0.8"),
 "gizlilik.html": ("Gizlilik Politikası ve KVKK Aydınlatma Metni | SNZ",
   "SNZ Madeni Yağ Ltd. Şti. kısa KVKK aydınlatma metni: yalnızca adınızı ve telefonunuzu size dönüş yapmak için alırız; satmaz, paylaşmayız.",
   "og-index.jpg", "Gizlilik Politikası ve KVKK", True, "0.2"),
 "site-haritasi.html": ("Site Haritası | SNZ Madeni Yağ & Akü Market",
   "SNZ Madeni Yağ & Akü Market internet sitesindeki tüm sayfalar: ürünler, hizmetler, örnek işler, galeri, SSS ve iletişim.",
   "og-index.jpg", "Site Haritası", True, "0.3"),
 "tesekkurler.html": ("Teşekkürler | SNZ Madeni Yağ & Akü Market",
   "Mesajınız için teşekkür ederiz. En kısa sürede dönüş yapacağız.",
   "og-index.jpg", None, False, None),
 "404.html": ("Sayfa Bulunamadı | SNZ Madeni Yağ & Akü Market",
   "Aradığınız sayfa bulunamadı. Ana sayfaya, ürünlere veya iletişim sayfasına dönebilirsiniz.",
   "og-index.jpg", None, False, None),
}

def ver(rel):
    """Dosya içeriğinden kısa sürüm kodu: dosya değişince tarayıcı yenisini indirir."""
    return hashlib.md5(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()[:8]

def url(page):
    return SITE_URL + "/" + ("" if page == "index.html" else page)

def stores():
    addr = {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY,
            "addressRegion": REGION, "postalCode": POSTAL, "addressCountry": "TR"}
    org = {"@type": "Organization", "@id": SITE_URL + "/#org", "name": "SNZ Madeni Yağ Ltd. Şti.",
           "url": SITE_URL + "/", "logo": SITE_URL + "/assets/img/logo.png",
           "telephone": PHONE1, "email": EMAIL, "sameAs": []}
    s1 = {"@type": "AutoPartsStore", "@id": SITE_URL + "/#madeni-yag", "name": "SNZ Madeni Yağ & Oto Market",
          "image": SITE_URL + "/assets/img/bina.webp", "url": SITE_URL + "/", "telephone": PHONE1,
          "address": addr, "geo": GEO, "hasMap": MAP_URL, "openingHoursSpecification": HOURS, "priceRange": "₺₺",
          "parentOrganization": {"@id": SITE_URL + "/#org"},
          "description": "Motor yağı, hidrolik ve gres yağları, AdBlue, antifriz; yağ değişimi ve sahada endüstriyel yağlama."}
    s2 = {"@type": "AutoPartsStore", "@id": SITE_URL + "/#aku-market", "name": "SNZ Akü Market",
          "image": SITE_URL + "/assets/img/galeri/ga9.webp", "url": SITE_URL + "/", "telephone": PHONE2,
          "address": addr, "geo": GEO, "hasMap": MAP_URL, "openingHoursSpecification": HOURS, "priceRange": "₺₺",
          "parentOrganization": {"@id": SITE_URL + "/#org"},
          "description": "Binek, ticari ve ağır vasıta aküleri; ücretsiz akü testi ve montaj."}
    return [org, s1, s2]

def faq_schema(body):
    qs = re.findall(r'<button class="faq-q"[^>]*><span[^>]*>(.*?)</span></button>\s*<div class="faq-a"><p[^>]*>(.*?)</p>', body, re.S)
    strip = lambda t: html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qs]}

def build_head(page, body):
    title, desc, og, crumb, index, _ = PAGES[page]
    e = lambda t: html.escape(t, quote=True)
    graph = []
    if page == "index.html":
        graph.append({"@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/",
                      "name": "SNZ Madeni Yağ & Akü Market", "inLanguage": ["tr", "en"],
                      "publisher": {"@id": SITE_URL + "/#org"}})
    if page in ("index.html", "iletisim.html", "hakkimizda.html"):
        graph += stores()
    if page == "sss.html":
        graph.append(faq_schema(body))
    if crumb:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": crumb, "item": url(page)}]})
    ld = ""
    if graph:
        ld = ('\n  <script type="application/ld+json">\n  '
              + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1).replace("\n", "\n  ")
              + "\n  </script>")
    base = f'\n  <base href="{BASE_PATH}">' if page == "404.html" else ""
    preload = ('\n  <link rel="preload" as="image" href="assets/img/hero.webp" fetchpriority="high">'
               if page == "index.html" else
               '\n  <link rel="preload" as="image" href="assets/img/page-hero.webp">' if crumb else "")
    gsc = (f'\n  <meta name="google-site-verification" content="{GSC_CODE}">' if GSC_CODE else
           '\n  <!-- Google Search Console: doğrulama kodunu _araclar/seo.py içindeki GSC_CODE alanına yazın -->')
    return f'''<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">{base}
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="robots" content="{'index, follow' if index else 'noindex, follow'}">
  <link rel="canonical" href="{url(page)}">{gsc}
  <meta name="theme-color" content="#d71920">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="SNZ Madeni Yağ &amp; Akü Market">
  <meta property="og:locale" content="tr_TR">
  <meta property="og:locale:alternate" content="en_US">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{url(page)}">
  <meta property="og:image" content="{SITE_URL}/assets/img/og/{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(desc)}">
  <meta name="twitter:image" content="{SITE_URL}/assets/img/og/{og}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css?v={ver('assets/css/style.css')}">{preload}{ld}
</head>'''

def main():
    for page in PAGES:
        p = os.path.join(ROOT, page)
        s = open(p, encoding="utf-8").read()
        s = re.sub(r"<head>.*?</head>", lambda m: build_head(page, s), s, count=1, flags=re.S)
        s = re.sub(r'<script src="assets/js/main\.js(\?v=\w+)?"( defer)?></script>',
                   f'<script src="assets/js/main.js?v={ver("assets/js/main.js")}" defer></script>', s)
        # Boyutu bilinen görsellere width/height ve decoding ekle (CLS'yi önler)
        def dims(m):
            tag = m.group(0)
            if "decoding=" not in tag:
                tag = tag.replace("<img ", '<img decoding="async" ', 1)
            if "width=" in tag:
                return tag
            src = re.search(r'src="([^"]+)"', tag).group(1)
            fp = os.path.join(ROOT, src)
            if os.path.exists(fp):
                from PIL import Image
                w, h = Image.open(fp).size
                tag = tag.replace(">", f' width="{w}" height="{h}">', 1) if tag.endswith(">") else tag
            return tag
        s = re.sub(r"<img [^>]+>", dims, s)
        open(p, "w", encoding="utf-8").write(s)
    today = date.today().isoformat()
    urls = "".join(
        f"  <url><loc>{url(p)}</loc><lastmod>{today}</lastmod><priority>{v[5]}</priority></url>\n"
        for p, v in PAGES.items() if v[4])
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\nDisallow: /tesekkurler.html\nDisallow: /foto/\nDisallow: /_araclar/\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("ok:", len(PAGES), "sayfa")

if __name__ == "__main__":
    main()
