import json, os, html

M = json.load(open("assets/portfolio/media.json"))
MEMBERS = json.load(open("assets/portfolio/members.json"))

# YouTube ids for the full, audio-bearing cut of a clip. Keys are the mp4
# basename; a blank value just means "no full version yet" and the tile keeps
# using its local muted loop. Accepts a bare id or any normal YouTube URL.
import re as _re
YT = {}
_ytp = "assets/portfolio/youtube.json"
if os.path.exists(_ytp):
    for k, v in json.load(open(_ytp)).items():
        if isinstance(v, dict):          # {"upload": <file to send to YouTube>, "youtube": <id or url>}
            v = v.get("youtube", "")
        v = (v or "").strip()
        if not v:
            continue
        mo = _re.search(r"(?:v=|youtu\.be/|/embed/|/shorts/|/live/)([A-Za-z0-9_-]{11})", v)
        YT[k] = mo.group(1) if mo else v


EV = [
 dict(id="saputara-2026", n="01", title='Saputara Monsoon Festival <span class="hl">2026</span>',
   bucket="saputara", photos_slice=(0, 4), loops_slice=(2, 3),
   chips=["Government of Gujarat", "Saputara, Dang", "14 August 2026", "Main stage"],
   accent=0,
   desc=[
     'Saputara is Gujarat’s only hill station, high in the Sahyadri hills of the Dang. Every August the '
     'state tourism department turns it into the Monsoon Festival, three weeks of music, tribal craft and '
     'culture that pulls visitors from across India. The 2026 edition ran from 8 to 29 August.',
     'We were invited back to the main stage and played on <strong>14 August</strong>, the night before '
     'Independence Day, on full festival production: LED wall, moving lights and a pavilion crowd.',
   ],
   note='Our second year running on the Monsoon Festival main stage.'),

 dict(id="saputara-2025", n="02", title='Saputara Monsoon Festival <span class="hl">2025</span>',
   bucket="saputara", photos_slice=(4, 11), loops_slice=(0, 2),
   chips=["Top 5 performing bands", "Saputara, Dang", "14 August 2025", "Festival debut"],
   accent=0,
   desc=[
     'The first time we played it. The 2025 festival ran from 26 July to 17 August and we took the main '
     'stage on 14 August, again on the eve of Independence Day.',
     'This was the show that changed what people expected of us: a government festival stage, a full '
     'pavilion, and a set that moved from Bollywood to Gujarati folk to fusion without losing the room.',
   ],
   note='Recognised among the top 5 performing bands of the 2025 festival.'),

 dict(id="hillside", n="03", title='Hillside Sunset Concert, <span class="hl">Dang</span>',
   chips=["With Lost Compass Motoclub", "Dang hills", "June 2026", "Open air"],
   accent=1,
   desc=[
     'No auditorium. No banquet hall. We carried the full rig up a hillside in the Dang and played as '
     'the sun went down, alongside <a href="https://www.instagram.com/lost.compass.motoclub/" '
     'target="_blank" rel="noopener">Lost Compass Motoclub</a>, a South Gujarat riders’ community '
     'who describe themselves as passionate riders living the spirit of freedom on two wheels.',
     'The audience rode in. There was no barricade and no stage, just a slope, the hills behind us and '
     'the light going orange. When it got dark, phone torches took over from the stage lights.',
   ],
   note='One of the most unusual and best-loved shows we have played.'),

 dict(id="cafes", n="04", title='Cafes and <span class="hl">Clubs</span>',
   chips=["AntiSocial, Lower Parel", "Mumbai &amp; Valsad", "2023 to 2025", "Live &amp; jamming"],
   accent=0,
   desc=[
     '<strong>AntiSocial, Lower Parel</strong> is one of the best venues in Mumbai for live music and '
     'jamming, part of the well known Social chain. Playing that room put us in front of a city crowd '
     'who had never heard of us and stayed anyway.',
     'Closer to home, <strong>Foodaholic Cafe in Valsad</strong> is the other end of the same craft: a '
     'small room, an attentive crowd and a stripped-back set where every mistake is audible. We have '
     'been playing rooms like it since 2023.',
   ],
   note=None),

 dict(id="corporate", n="05", title='Corporate <span class="hl">Events</span>',
   chips=["Annual days", "Brand nights", "May 2025", "Custom setlist"],
   accent=1,
   desc=[
     'Annual days, brand launches, offsites and company celebrations. These are the shows where the '
     'run-of-show matters as much as the music: we work to your schedule, keep the volume where the '
     'room needs it, and build the setlist around who is actually in the audience.',
     'Full nine-piece production or a stripped-back acoustic trio, with sound and setup included '
     'either way.',
   ],
   note=None),

 dict(id="diwali", n="06", title='Diwali, New Year and <span class="hl">Open Concerts</span>',
   chips=["Bestu Varas", "Tithal, Valsad", "Nov 2025 &amp; May 2026", "Free entry"],
   accent=0,
   desc=[
     'Instead of waiting to be invited, we started putting on our own. Every year we set up in the '
     'busiest part of town to welcome <strong>Bestu Varas</strong> with live music. No tickets, no '
     'passes, no guest list. Families, friends and children, music playing and fireworks overhead.',
     'The same thinking took us to open gigs on <strong>Tithal beach</strong> in Valsad, playing to '
     'whoever happened to be there that evening.',
   ],
   note='These nights are not really concerts. They are celebrations, and they are some of our favourites.'),

 dict(id="lineup", n="08", kind="lineup",
   title='The <span class="hl">Line-up</span>',
   chips=["Nine-plus musicians", "Valsad, Gujarat", "Since 2021", "One family"],
   accent=0,
   desc=[
     'None of the rooms on this page work without the people in them. This is the core crew, plus a '
     'rotating cast of guest musicians who step in depending on the gig.',
     'We have always wanted the band to be a platform, not a closed shop. If you play, and you are '
     'serious about it, there is a stage here for you.',
   ],
   note=None),

 dict(id="wedding", n="07", title='Weddings, Receptions and <span class="hl">Sangeet</span>',
   chips=["Sangeet nights", "Receptions", "Feb &amp; Nov 2025", "Across India"],
   accent=1,
   desc=[
     'The work that keeps us on the road. Instrumental lagna geet, DJ sets driven by live percussion, '
     'custom entry music, and a sangeet floor that does not sit down. Every family’s playlist is '
     'different, so every set is built from scratch.',
     'We travel anywhere in India for these, and overseas for destination weddings.',
   ],
   note=None),
]

# layout patterns, so the grid never looks like a plain gallery
SPANS_PHOTO = ["pf-item--hero", "pf-item--half", "pf-item--half", "pf-item--third",
               "pf-item--third", "pf-item--third", "pf-item--wide", "pf-item--half",
               "pf-item--half", "pf-item--third", "pf-item--third"]

# Container is min(1180px, 90vw) on a 12-col grid with a 14px gap; under 760px
# every tile becomes full width. These `sizes` mirror that exactly, so the
# browser downloads the rendition it will actually paint and no more.
SIZES = {
  "pf-item--hero":  "(max-width: 760px) 90vw, (max-width: 1311px) 90vw, 1180px",
  "pf-item--wide":  "(max-width: 760px) 90vw, (max-width: 1311px) 60vw, 782px",
  "pf-item--half":  "(max-width: 760px) 90vw, (max-width: 1311px) 45vw, 583px",
  "pf-item--third": "(max-width: 760px) 90vw, (max-width: 1311px) 30vw, 384px",
  "pf-item--tall":  "(max-width: 760px) 90vw, (max-width: 1311px) 30vw, 384px",
}

VID_BADGE = ('<span class="pf-item__badge"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
             '<path d="M8 5v14l11-7z"/></svg>Clip</span>')

VID_BADGE_SOUND = ('<span class="pf-item__badge pf-item__badge--sound">'
    '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
    '<path d="M3 9v6h4l5 4V5L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4z'
    'M14 3.2v2.1a6.8 6.8 0 0 1 0 13.4v2.1a8.9 8.9 0 0 0 0-17.6z"/></svg>Full clip</span>')

def esc(s): return html.escape(s, quote=True)

def srcset(m):
    return ", ".join(f'{r["src"]} {r["w"]}w' for r in m.get("srcset", []))

def build_grid(ev, ev_title_plain):
    media = M[ev.get("bucket", ev["id"])]
    out = []
    ps = ev.get("photos_slice"); ls = ev.get("loops_slice")
    photos = media["photos"][ps[0]:ps[1]] if ps else media["photos"][:]
    loops  = media["loops"][ls[0]:ls[1]]  if ls else media["loops"][:]
    for m2 in loops:
        key = os.path.basename(m2["mp4"]).replace(".mp4", "")
        if YT.get(key): m2["yt"] = YT[key]
    seq = []
    # interleave: lead with a photo if we have one, then alternate
    while photos or loops:
        if photos: seq.append(("photo", photos.pop(0)))
        if loops:  seq.append(("loop",  loops.pop(0)))
    for i, (kind, m) in enumerate(seq):
        if kind == "photo":
            span = SPANS_PHOTO[i % len(SPANS_PHOTO)]
            if m["ratio"] < 0.85: span = "pf-item--tall"
            out.append(
f'''        <figure class="pf-item {span} reveal" tabindex="0" role="button"
          data-type="image" data-full="{m['full']['src']}"
          data-caption="{esc(m['caption'])}" data-event="{esc(ev_title_plain)}"
          aria-label="{esc(m['caption'])}, open larger">
          <img src="{m['card']['src']}" srcset="{srcset(m)}" sizes="{SIZES[span]}" alt="{esc(m['caption'])}" width="{m['card']['w']}" height="{m['card']['h']}" loading="lazy" decoding="async" />
          <span class="pf-item__glow" aria-hidden="true"></span>
          <figcaption class="pf-item__cap">{esc(m['caption'])}</figcaption>
        </figure>''')
        else:
            span = "pf-item--tall" if m["vertical"] else ("pf-item--half" if i % 3 else "pf-item--wide")
            yt = m.get("yt", "")
            badge = VID_BADGE_SOUND if yt else VID_BADGE
            out.append(
f'''        <figure class="pf-item {span} reveal" tabindex="0" role="button"
          data-type="video" data-full="{m['mp4']}"{f' data-yt="{yt}"' if yt else ""}{' data-yt-vertical="1"' if yt and m["vertical"] else ""}
          data-caption="{esc(m['caption'])}" data-event="{esc(ev_title_plain)}"
          aria-label="{esc(m['caption'])}, {"play with sound" if yt else "play larger"}">
          <video data-src="{m['mp4']}" poster="{m['poster']}" muted loop playsinline preload="none"
                 width="{m['w']}" height="{m['h']}" aria-hidden="true"></video>
          {badge}
          <span class="pf-item__glow" aria-hidden="true"></span>
          <figcaption class="pf-item__cap">{esc(m['caption'])}</figcaption>
        </figure>''')
    return "\n".join(out)

EV = [e for e in EV if e["id"] != "lineup"] + [e for e in EV if e["id"] == "lineup"]

chapters, jump = [], []
for ev in EV:
    plain = ev["title"].replace('<span class="hl">','').replace('</span>','')
    jump.append(f'      <a href="#{ev["id"]}">{ev["n"]} &nbsp;{plain}</a>')
    if ev.get("kind") == "lineup":
        cards = "\n".join(
f'''          <figure class="pf-member reveal" tabindex="0" role="button"
            data-type="image" data-full="{m["full"]}"
            data-caption="{m["role"].replace("&amp;", "and")}" data-event="{m["name"]}"
            aria-label="{m["name"]}, open larger">
            <img src="{m["card"]}" srcset="{m.get("srcset", "")}" sizes="(max-width: 520px) 90vw, (max-width: 900px) 45vw, (max-width: 1311px) 30vw, 384px" alt="{m["name"]}, {m["role"].replace("&amp;", "and")}" width="{m["cw"]}" height="{m["ch"]}" loading="lazy" decoding="async" />
            <span class="pf-item__glow" aria-hidden="true"></span>
            <figcaption class="pf-member__cap"><b>{m["name"]}</b><span>{m["role"]}</span></figcaption>
          </figure>''' for m in MEMBERS)
        grid_html = f'<div class="pf-lineup">\n{cards}\n      </div>'
    else:
        grid_html = f'<div class="pf-grid">\n{build_grid(ev, plain)}\n      </div>'
    descs = "\n".join(f'          <p class="pf-event__desc reveal">{d}</p>' for d in ev["desc"])
    note  = f'\n          <p class="pf-event__note reveal">{ev["note"]}</p>' if ev["note"] else ""
    chips = "\n".join(
        f'            <span class="pf-chip{" pf-chip--accent" if i == ev["accent"] else ""}">{c}</span>'
        for i, c in enumerate(ev["chips"]))
    chapters.append(f'''  <section class="pf-event" id="{ev["id"]}">
    <div class="container">
      <div class="pf-event__head">
        <span class="pf-event__index reveal">{ev["n"]} / 08</span>
        <h2 class="pf-event__title reveal">{ev["title"]}</h2>
        <div class="pf-event__meta reveal">
{chips}
        </div>
{descs}{note}
      </div>

      {grid_html}
    </div>
  </section>''')

n_photos = sum(len(M[e["id"]]["photos"]) for e in EV if e["id"] in M) + 11
n_loops  = sum(len(M[e["id"]]["loops"]) for e in EV if e["id"] in M) + 3

TPL = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "portfolio.tpl.html")).read()
out = (TPL.replace("{{JUMP}}", "\n".join(jump))
          .replace("{{CHAPTERS}}", "\n\n".join(chapters))
          .replace("{{N_PHOTOS}}", str(n_photos))
          .replace("{{N_CLIPS}}", str(n_loops)))
open("portfolio.html", "w").write(out)
print(f"portfolio.html written: {len(EV)} chapters, {n_photos} photos, {n_loops} clips, {len(out)/1024:.0f} KB")
