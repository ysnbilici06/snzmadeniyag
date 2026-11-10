"""Site görsellerini WebP'ye çevirir, küçültür ve sayfalardaki bağlantıları günceller.
    python _araclar/optimize.py
og/ klasörü (sosyal medya görselleri), logo ve favicon'lar JPEG/PNG olarak kalır.
"""
import os, re, glob
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
VID = os.path.join(ROOT, "assets", "video")

def rel(p): return os.path.relpath(p, ROOT).replace("\\", "/")

def settings(path):
    r = rel(path)
    if r.endswith("hero.jpg") and "page" not in r: return 1920, 70
    if "page-hero" in r:                           return 1600, 62   # üstüne koyu katman geliyor
    if r.endswith("-k.jpg"):                       return 600, 70    # küçük resimler
    if "/galeri/" in r:                            return 1400, 72   # büyütülen görseller
    if "/video/" in r:                             return 900, 70    # video kapakları
    return 1200, 74

before = after = 0
converted = []
files = [p for p in glob.glob(os.path.join(IMG, "**", "*.jpg"), recursive=True) if os.sep + "og" + os.sep not in p]
files += glob.glob(os.path.join(VID, "*.jpg"))
for p in files:
    mx, q = settings(p)
    im = Image.open(p).convert("RGB")
    im.thumbnail((mx, mx), Image.LANCZOS)
    out = p[:-4] + ".webp"
    im.save(out, "WEBP", quality=q, method=6)
    before += os.path.getsize(p); after += os.path.getsize(out)
    os.remove(p); converted.append(rel(p))

# OG görsellerini yeniden sıkıştır (JPEG kalır)
for p in glob.glob(os.path.join(IMG, "og", "*.jpg")):
    b = os.path.getsize(p)
    Image.open(p).convert("RGB").save(p, "JPEG", quality=78, optimize=True, progressive=True)
    before += b; after += os.path.getsize(p)

# Bağlantıları güncelle (og/ hariç)
pat = re.compile(r"(assets/(?:img|video)/(?!og/)[^\"'()\s<>]+?)\.jpg")
for f in glob.glob(os.path.join(ROOT, "*.html")) + [os.path.join(ROOT, "assets", "css", "style.css"),
                                                    os.path.join(ROOT, "assets", "js", "main.js"),
                                                    os.path.join(ROOT, "_araclar", "seo.py")]:
    s = open(f, encoding="utf-8").read()
    s2 = pat.sub(r"\1.webp", s).replace('url("../img/hero.jpg")', 'url("../img/hero.webp")') \
                               .replace('url("../img/page-hero.jpg")', 'url("../img/page-hero.webp")')
    if s2 != s: open(f, "w", encoding="utf-8").write(s2)

# og.py kaynaklarını güncelle
f = os.path.join(ROOT, "_araclar", "og.py"); s = open(f, encoding="utf-8").read()
s = re.sub(r'^( \(")([^"]+)\.jpg(", "og-)', r"\1\2.webp\3", s, flags=re.M)
open(f, "w", encoding="utf-8").write(s)

print(f"{len(converted)} görsel WebP'ye çevrildi: {before/1e6:.1f} MB -> {after/1e6:.1f} MB")
