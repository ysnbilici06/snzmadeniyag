"""foto/adreskroki.png (Google Haritalar ekran görüntüsü) -> assets/img/kroki.webp (geniş) ve kroki-m.webp (telefon)
Google arayüzünü kırpar, görüntüyü canlandırır, SNZ işaretini ve bilgi kartını çizer.
    python -I -X utf8 _araclar/kroki.py
"""
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "foto", "adreskroki.png")
IMG = os.path.join(ROOT, "assets", "img")
RED, INK, WHITE = (215, 25, 32), (14, 17, 21), (255, 255, 255)
S = 2                       # çizimleri net olsun diye 2 kat büyük tuvalde çalış
PIN_SRC = (1180, 312)       # Google işaretinin ucu (ekran görüntüsündeki konum)

def font(size, style="Bold Condensed"):
    f = ImageFont.truetype("bahnschrift.ttf", size * S)
    try: f.set_variation_by_name(style)
    except Exception: pass
    return f

L1 = "SNZ MADENİ YAĞ & AKÜ MARKET"
L2 = "Madeni Yağ & Oto Market  ·  Akü Market"
L3 = "Sehaş Arena İş Merkezi · D Blok 1 · No:38"

def card_width():
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    return max(d.textlength(L1, font=font(25)), d.textlength(L2, font=font(17, "SemiBold")),
               d.textlength(L3, font=font(15, "Regular"))) / S + 44

def render(crop, out_name, out_scale):
    im = Image.open(SRC).convert("RGB").crop(crop)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.15)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    W, H = im.size
    im = im.resize((W * S, H * S), Image.LANCZOS)
    px, py = (PIN_SRC[0] - crop[0]) * S, (PIN_SRC[1] - crop[1]) * S

    # Kenarlara hafif koyu geçiş, işaretin çevresi aydınlık kalsın
    shade = Image.new("L", im.size, 0)
    ImageDraw.Draw(shade).ellipse((px - 900 * S, py - 600 * S, px + 900 * S, py + 600 * S), fill=255)
    shade = shade.filter(ImageFilter.GaussianBlur(160 * S))
    im = Image.composite(im, ImageEnhance.Brightness(im).enhance(0.62), shade)
    d = ImageDraw.Draw(im, "RGBA")

    # Konum halkaları
    for r, a in ((70, 40), (46, 70), (26, 110)):
        d.ellipse((px - r * S, py - r * 0.55 * S, px + r * S, py + r * 0.55 * S),
                  fill=(*RED, a), outline=(*WHITE, 150), width=S)

    # Bilgi kartı: işaretin sağında, Google'ın kendi etiketini örter
    cw, ch = int(card_width() * S), 104 * S
    cx0, cy0 = px + 18 * S, py - 92 * S
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((cx0 + 4 * S, cy0 + 8 * S, cx0 + cw + 4 * S, cy0 + ch + 8 * S), 14 * S, fill=(0, 0, 0, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(10 * S))
    im.paste(sh, (0, 0), sh)
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle((cx0, cy0, cx0 + cw, cy0 + ch), 14 * S, fill=(*INK, 238))
    d.rounded_rectangle((cx0, cy0, cx0 + 7 * S, cy0 + ch), 4 * S, fill=RED)
    d.text((cx0 + 24 * S, cy0 + 16 * S), L1, font=font(25), fill=WHITE)
    d.text((cx0 + 24 * S, cy0 + 50 * S), L2, font=font(17, "SemiBold"), fill=(255, 196, 198))
    d.text((cx0 + 24 * S, cy0 + 76 * S), L3, font=font(15, "Regular"), fill=(190, 198, 208))

    # Damla şeklinde SNZ işareti
    r = 21 * S; cy = py - int(21 * 2.1 * S)
    d.ellipse((px - r, cy - r, px + r, cy + r), fill=RED, outline=WHITE, width=3 * S)
    d.polygon([(px - r * 0.62, cy + r * 0.72), (px + r * 0.62, cy + r * 0.72), (px, py)], fill=RED)
    d.line([(px - r * 0.66, cy + r * 0.75), (px, py), (px + r * 0.66, cy + r * 0.75)], fill=WHITE, width=3 * S, joint="curve")
    d.ellipse((px - r + 3 * S, cy - r + 3 * S, px + r - 3 * S, cy + r - 3 * S), fill=RED)
    f = font(16); w = d.textlength("SNZ", font=f)
    d.text((px - w / 2, cy), "SNZ", font=f, fill=WHITE, anchor="lm")

    # Kaynak notu
    f = font(12, "Regular"); t = "Harita görüntüsü: © Google"; w = d.textlength(t, font=f)
    d.rounded_rectangle((W * S - w - 22 * S, H * S - 26 * S, W * S - 6 * S, H * S - 6 * S), 6 * S, fill=(0, 0, 0, 150))
    d.text((W * S - w - 14 * S, H * S - 16 * S), t, font=f, fill=(230, 230, 230), anchor="lm")

    out = im.resize((int(W * out_scale), int(H * out_scale)), Image.LANCZOS)
    path = os.path.join(IMG, out_name)
    out.save(path, "WEBP", quality=80, method=6)
    print("ok:", out_name, out.size, os.path.getsize(path) // 1024, "KB")

# Geniş: tüm harita alanı (üst düğmeler, sağ kontroller, alt "Toplu taşıma" kutusu ve katman düğmesi dışarıda)
render((574, 75, 1850, 740), "kroki.webp", 1.25)
# Telefon: işaret ve kart odakta, yaklaşık kare
x0 = PIN_SRC[0] - 60
x1 = PIN_SRC[0] + 18 + int(card_width()) + 26
h = int((x1 - x0) * 0.95)
y0 = PIN_SRC[1] - int(h * 0.42)
render((x0, y0, x1, y0 + h), "kroki-m.webp", 1.6)
