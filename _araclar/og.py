"""Sosyal medya paylaşım görselleri (1200x630), favicon ve logo üretir.
    python _araclar/og.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
OUT = os.path.join(IMG, "og"); os.makedirs(OUT, exist_ok=True)
RED, INK = (215, 25, 32), (14, 17, 21)

def font(size, style="Bold Condensed"):
    f = ImageFont.truetype("bahnschrift.ttf", size)
    try: f.set_variation_by_name(style)
    except Exception: pass
    return f

def logo_mark(d, x, y, size):
    f = font(size, "Bold Condensed")
    d.text((x, y), "SNZ", font=f, fill=RED)
    w = d.textlength("SNZ", font=f)
    d.polygon([(x + size * .1, y + size * 1.08), (x + w + size * .02, y + size * 1.08),
               (x + w - size * .06, y + size * 1.2), (x + size * .02, y + size * 1.2)], fill=RED)
    return w

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = word
    lines.append(cur); return lines

def og(src, name, title, sub):
    im = ImageOps.fit(Image.open(os.path.join(IMG, src)).convert("RGB"), (1200, 630), Image.LANCZOS, centering=(0.6, 0.5))
    grad = Image.new("L", (1200, 1))
    for x in range(1200):
        grad.putpixel((x, 0), int(245 * max(0, 1 - x / 1000) ** 0.9 + 60))
    grad = grad.resize((1200, 630))
    im = Image.composite(Image.new("RGB", im.size, INK), im, grad)
    d = ImageDraw.Draw(im)
    w = logo_mark(d, 64, 52, 74)
    fs = font(26, "SemiBold Condensed")
    d.text((64 + w + 18, 62), "Madeni Yağ & Oto Market", font=fs, fill="white")
    d.text((64 + w + 18, 94), "Akü Market · Ankara", font=font(22, "Regular"), fill=(190, 196, 204))
    ft = font(78)
    y = 210
    for line in wrap(d, title.replace("i", "İ").upper(), ft, 700)[:3]:
        d.text((64, y), line, font=ft, fill="white"); y += 84
    d.rectangle([64, y + 14, 140, y + 20], fill=RED)
    d.text((64, y + 36), sub, font=font(30, "Regular"), fill=(214, 219, 225))
    d.rectangle([0, 600, 1200, 630], fill=RED)
    d.text((64, 603), "0543 488 22 53  ·  0541 334 22 51  ·  snzmadeniyag.com", font=font(22, "SemiBold"), fill="white")
    im.save(os.path.join(OUT, name), "JPEG", quality=85, optimize=True, progressive=True)

JOBS = [
 ("hero.webp", "og-index.jpg", "Her Motora Uygun Yağ ve Akü", "Motor yağı · Akü · AdBlue · Gres"),
 ("bina.webp", "og-hakkimizda.jpg", "Yan Yana İki Mağaza", "Madeni Yağ & Oto Market · Akü Market"),
 ("magaza-a10.webp", "og-urunler.jpg", "Motor Yağı, Akü ve Bakım Ürünleri", "Dünya markaları, orijinal ürün"),
 ("hizmet-yag.webp", "og-hizmetler.jpg", "Yağ Değişimi, Akü Montajı", "Sahada endüstriyel yağlama"),
 ("galeri/ga5.webp", "og-projeler.jpg", "Örnek İşlerimiz", "Atölyeden ve sahadan gerçek işler"),
 ("galeri/ga2.webp", "og-galeri.jpg", "Galeri", "Mağaza, atölye ve saha fotoğrafları"),
 ("galeri/g53.webp", "og-markalar.jpg", "Dünya Markaları Tek Çatı Altında", "Castrol · Shell · Mobil · Motul · Turbo Akü"),
 ("magaza-ic.webp", "og-sss.jpg", "Sıkça Sorulan Sorular", "Motor yağı ve akü hakkında net cevaplar"),
 ("bina-genis.webp", "og-iletisim.jpg", "İletişim ve Yol Tarifi", "Sincan Sanayi Sitesi · Pzt–Cmt 08:30–19:00"),
]
for j in JOBS: og(*j)

# Favicon / logo
def square(size, pad=0.12):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * .22), fill=RED)
    f = font(int(size * .5))
    tw = d.textlength("SNZ", font=f)
    d.text(((size - tw) / 2, size * .2), "SNZ", font=f, fill="white")
    return im
square(180).save(os.path.join(IMG, "apple-touch-icon.png"))
square(32).save(os.path.join(IMG, "favicon-32.png"))
logo = Image.new("RGB", (600, 200), "white"); d = ImageDraw.Draw(logo)
w = logo_mark(d, 30, 40, 100)
d.text((50 + w, 58), "Madeni Yağ & Oto Market", font=font(40, "SemiBold Condensed"), fill=INK)
d.text((50 + w, 106), "Akü Market", font=font(32, "Regular"), fill=(107, 115, 128))
logo.save(os.path.join(IMG, "logo.png"))
open(os.path.join(IMG, "favicon.svg"), "w", encoding="utf-8").write(
 '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#d71920"/>'
 '<text x="32" y="42" text-anchor="middle" font-family="Arial Narrow,Arial,sans-serif" font-weight="700" font-style="italic" font-size="27" fill="#fff">SNZ</text></svg>')
print("ok")
