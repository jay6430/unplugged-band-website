# The Unplugged Band, Official Website

> "We create moments"
> Live Bollywood · Fusion · Gujarati Folk, serving soulful beats in multiple cities.

A fast, fully static, single-page website for [The Unplugged Band](https://www.instagram.com/theunplugged_band/).
No build step, no framework, no dependencies, just HTML, CSS and vanilla JS.

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

The site is deployed from `main` and redeploys on every push.

| URL | Role |
|---|---|
| **https://theunpluggedband.com/** | **Live site. This is the URL to share.** |
| https://www.theunpluggedband.com/ | 308 redirect to the apex |
| https://theunpluggedband.vercel.app/ | 308 redirect to the apex |
| https://jay6430.github.io/unplugged-band-website/ | Backup mirror, also built from `main` |

Vercel serves the repo as-is (no build step); `vercel.json` sets `cleanUrls`,
long-lived caching for `assets/`, and basic security headers.

### Domain and DNS

`theunpluggedband.com` was registered through GoDaddy on 11 August 2026 and renews
annually. DNS stays at GoDaddy (nameservers `ns57`/`ns58.domaincontrol.com`); only the
apex `A` record points at Vercel:

| Type | Name | Value |
|---|---|---|
| A | `@` | `216.198.79.1` |
| CNAME | `www` | `theunpluggedband.com` |

Vercel issues and renews the Let's Encrypt certificate automatically. GoDaddy asks for
SMS verification before saving any DNS change.

**Renewal matters:** a lapsed domain can be taken by someone else, so keep auto-renew on
and make sure the billing card stays valid.

If the apex ever needs repointing, change that one `A` record. Any change of domain also
means updating the `canonical` / `og:url` / `og:image` tags and the JSON-LD block in
`index.html` and `story.html`, plus `robots.txt` and `sitemap.xml`.

## Contacts

| | |
|---|---|
| Bookings (band) | Rajat Lad, +91 75677 54103 |
| Bookings (manager) | Kunj Desai, +91 70690 01861 |
| Instagram | [@theunplugged_band](https://www.instagram.com/theunplugged_band/) |

## The Band

- **Kunj Desai** - Band Manager (bookings), +91 70690 01861
- **Rajat Lad** - Lead Singer & Guitar, [@ladrajat_live](https://www.instagram.com/ladrajat_live/)
- **Vishal Patel** - Musician, [@vishal6050.vp](https://www.instagram.com/vishal6050.vp/)
- **Kunjan Patel** - Drummer, [@ftw.kunju_](https://www.instagram.com/ftw.kunju_/)
- **Aishan Mistry** - Lead Percussionist, [@aishanmistry](https://www.instagram.com/aishanmistry/)
- **Jay Patel** - Guitarist / Bassist, [@jordan_jayp](https://www.instagram.com/jordan_jayp/)
- **Dev Patel** - Theater Keyboardist & Arranger, [@dev_keysss](https://www.instagram.com/dev_keysss/)

---

Developed & managed by **Jay Kadam**.
Band name, logo and all photography © The Unplugged Band.
