# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Static corporate site (plain HTML/CSS/JS, no build step, no framework, no tests) for two neighbouring stores in an Ankara sanayi sitesi: **SNZ Madeni Yağ & Oto Market** and **SNZ Akü Market**. The site is bilingual, with Turkish as the source language and English via `data-en`. The user communicates in Turkish.

- Repo: `ysnbilici06/snzmadeniyag`, branch `main`. GitHub Pages serves it at https://ysnbilici06.github.io/snzmadeniyag/ and every push to `main` redeploys.
- The planned domain `https://www.snzmadeniyag.com` is not bought yet. Canonicals, OG URLs and the sitemap already point at it.

## Commands

All Python tools need Pillow. On this Windows machine, run them with `-I -X utf8` to avoid cp1254 encoding errors.

```bash
python -m http.server 5500                  # local preview (from repo root)
python -I -X utf8 _araclar/seo.py           # regenerate every page <head>, sitemap.xml, robots.txt
python -I -X utf8 _araclar/og.py            # regenerate OG images (assets/img/og/*.jpg), favicons, logo.png
python -I -X utf8 _araclar/optimize.py      # convert new assets/img/**/*.jpg to WebP and rewrite references
```

Video re-encoding uses ffmpeg from `imageio_ffmpeg.get_ffmpeg_exe()` (libx264, `-movflags +faststart`, crf ~29).

## Architecture

**Shared layout is injected by JS.** Each page has only `<div id="site-header">` and `<div id="site-footer">`. `assets/js/main.js` `renderLayout()` builds the header, nav (the `NAV` array), footer, floating buttons and the mobile bottom bar (`.mobile-bar`). To add a page, add it to `NAV` in main.js and to `PAGES` in `_araclar/seo.py`.

**Contact data lives in one place.** The `SITE` object at the top of main.js holds phones, WhatsApp, email, address, `mapsUrl` and `googleReviewsUrl`. Markup uses placeholders that main.js fills in: `<a data-site="phone1|phone2|whatsapp|email|...">` and `<i data-icon="name">`, with SVGs taken from the `ICONS` map. Never hardcode phone numbers or addresses in the HTML. `seo.py` keeps its own copies (`PHONE1/2`, `STREET`, `HOURS`) for JSON-LD, so keep both in sync.

**i18n.** Turkish text sits in the markup. Translations use these attributes:
- `data-en` holds the English innerHTML.
- `data-en-ph` holds the English placeholder.
- `<body data-title-en>` holds the English page title.
- `data-cap-en` holds the English lightbox caption.

`setLang()` swaps these and stores the choice in `localStorage` as `snz-lang`. Every new user-visible string needs a `data-en`.

**`<head>` is generated; don't hand-edit it.** `seo.py` replaces each page's whole `<head>…</head>` from the `PAGES` dict. Each entry holds the title, description, OG image, breadcrumb name, an indexable flag and the sitemap priority. The generated head includes canonical, OG/Twitter tags and JSON-LD:
- Two `AutoPartsStore` entries on the index, iletisim and hakkimizda pages.
- A `FAQPage` parsed from the sss.html body.
- A `BreadcrumbList` on every page that has a breadcrumb name.

`seo.py` also adds `defer` to main.js, plus `decoding="async"` and real width/height to `<img>` tags. Head-level changes (meta, preload, fonts, CSS link) go into `build_head()`, then rerun the script.

**Domain switch.** In `seo.py`:
1. Set `SITE_URL`.
2. Set `BASE_PATH = "/"`. It is currently `/snzmadeniyag/` for Pages and is only used as `<base>` in 404.html.
3. Optionally set `GSC_CODE`.

Then add a `CNAME` file and rerun `seo.py` and `og.py`.

**Reusable UI patterns.** These are in main.js and style.css:
- Filters: `.filter-bar button[data-filter]` toggles `.product[data-cat]`. Used on both urunler and galeri.
- Lightbox: opens on any `[data-full]` element.
- Scroll animation: `.reveal` elements animate via IntersectionObserver.
- Reviews: `REVIEWS = []` removes the `#reviews` section and points `[data-reviews-link]` at Google.
- Contact form: it opens WhatsApp with the message prefilled, then redirects to `tesekkurler.html`.

## Assets and content rules

- Raw photos and videos live in `foto/`, which is gitignored and never deployed. Processed outputs go to `assets/img/` (WebP), `assets/img/galeri/` (`gNN.webp` plus `gNN-k.webp` thumbnails) and `assets/video/` (mp4 plus `.webp` poster).
- OG images stay JPEG. Favicons and `logo.png` stay PNG.
- Blur or crop every visible licence plate in photos.
- Only add real customer reviews. Don't invent reviews, metrics or case-study numbers.
- When uppercasing Turkish text, map `i` to `İ` before `.upper()`. og.py already does this.
- `gizlilik.html` (KVKK and cookie text) is a draft that still needs legal review.

## Open TODOs (waiting on owner input)

- Full address: `SITE.address`/`mapQuery` and `seo.py` `STREET`.
- Real email.
- Google Maps share links (`SITE.mapsUrl`) and a two-store map visual for iletisim.html.
- `googleReviewsUrl` and real reviews.
- Domain and Search Console code.
