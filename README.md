# The Unplugged Band — Official Website

> "We create moments"
> Live Bollywood · Fusion · Gujarati Folk — serving soulful beats in multiple cities.

A fast, fully static, single-page website for [The Unplugged Band](https://www.instagram.com/theunplugged_band/).
No build step, no framework, no dependencies — just HTML, CSS and vanilla JS.

## Features

- Responsive single-page layout with animated hero, sticky nav and scroll reveals
- Band line-up cards with live Instagram links and click-to-call numbers
- Live Instagram post/reel embeds pulled straight from `@theunplugged_band`
- Booking form that composes a pre-filled WhatsApp enquiry to the band manager
- Brand assets generated from the band's official logo (favicon, PWA icons, OG image)
- SEO: Open Graph tags, `MusicGroup` JSON-LD structured data, sitemap and robots.txt
- Accessible: skip link, ARIA labels, keyboard-friendly nav, `prefers-reduced-motion` support

## Structure

```
.
├── index.html              # the whole page
├── css/style.css           # design system + all styles
├── js/main.js              # nav, reveals, counters, booking form
├── assets/images/          # logo derivatives, favicon, OG image
│   └── source/             # raw logo extracted from the original PDF
├── theunpluggedband_logo.pdf
├── site.webmanifest
└── sitemap.xml · robots.txt
```

## Running locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000

## Deployment

Hosted on GitHub Pages from the `main` branch.

To point a custom domain (e.g. `theunpluggedband.com`) at it:

1. Create a `CNAME` file in the repo root containing just the domain (one line, no protocol).
2. At your DNS registrar add either:
   - four `A` records for the apex domain → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - or a `CNAME` record for `www` → `<username>.github.io`
3. In the repo: **Settings → Pages → Custom domain**, enter the domain and tick **Enforce HTTPS**.

## Contacts

| | |
|---|---|
| Bookings (band) | Rajat Lad — +91 75677 54103 |
| Bookings (manager) | Kunj Desai — +91 70690 01861 |
| Instagram | [@theunplugged_band](https://www.instagram.com/theunplugged_band/) |

## The Band

- **Rajat Lad** — Lead Singer & Guitar — [@ladrajat_live](https://www.instagram.com/ladrajat_live/)
- **Vishal Patel** — Musician — [@vishal6050.vp](https://www.instagram.com/vishal6050.vp/)
- **Kunjan Patel** — Drummer — [@ftw.kunju_](https://www.instagram.com/ftw.kunju_/)
- **Aishan Mistry** — Lead Percussionist — [@aishanmistry](https://www.instagram.com/aishanmistry/)
- **Jay Patel** — Guitarist / Bassist — [@jordan_jayp](https://www.instagram.com/jordan_jayp/)
- **Dev** — Theater Keyboardist & Arranger — [@dev_keysss](https://www.instagram.com/dev_keysss/)
- **Kunj Desai** — Band Manager

---

Developed & managed by **Jay Kadam**.
Band name, logo and all photography © The Unplugged Band.
