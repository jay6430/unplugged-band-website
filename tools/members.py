"""Regenerate band member portraits at honest resolution, with srcset ladders.
READ-ONLY on media/. Output goes to assets/portfolio/members/."""
import os, json
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
SRC = "media/Portfolio/Band_members_best_photos"
SC  = "/private/tmp/claude-501/-Users-jaykadam-jay-python-projects-Unpluggedbandwebsite/c2059a07-bc53-46f5-bbf4-95aa591ef6f3/scratchpad"
OUT = "assets/portfolio/members"
os.makedirs(OUT, exist_ok=True)

# aishan-1-rot.jpg is the ARW's embedded JPEG, already rotated 90 deg anticlockwise.
MEMBERS = [
 ("rajat",  "Rajat Lad",     "Lead vocals &amp; guitar", f"{SRC}/Rajat Lad/DSC04697.jpg",   0.50),
 ("vishal", "Vishal Patel",  "Singer",                   f"{SRC}/Vishal Patel/IMG_0260.JPEG",0.50),
 ("kunjan", "Kunjan Patel",  "Drums",                    f"{SRC}/Kunjan Patel/DSC04716.jpg", 0.50),
 ("aishan", "Aishan Mistry", "Lead percussion",          f"{SC}/raw/aishan-1-rot.jpg",       0.62),
 ("jay",    "Jay Patel",     "Bass &amp; guitar",        f"{SRC}/Jay Patel/DJI_20260814_195106_423.JPG", 0.50),
 ("dev",    "Dev Patel",     "Keys &amp; arrangement",   f"{SRC}/Dev Patel/IMG_2074.JPG",    0.50),
]

RATIO  = 4 / 5                 # cards are a 4:5 portrait crop
LADDER = [420, 760, 1140, 1520]
FULL_H = 2400

def crop_portrait(im, focus):
    w, h = im.size
    tw = min(w, int(h * RATIO))
    th = int(tw / RATIO)
    if th > h:
        th = h; tw = int(th * RATIO)
    cx = int(w * focus)
    left = max(0, min(w - tw, cx - tw // 2))
    top  = max(0, min(h - th, int(h * 0.5) - th // 2))
    return im.crop((left, top, left + tw, top + th))

out = []
for mid, name, role, src, focus in MEMBERS:
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    card_src = crop_portrait(im, focus)
    srcset = []
    for tw in LADDER:
        if tw > card_src.size[0] and srcset:
            break
        c = card_src.copy()
        c.thumbnail((tw, tw * 4), Image.LANCZOS)
        p = f"{OUT}/{mid}-{c.size[0]}.webp"
        c.save(p, "WEBP", quality=84, method=6)
        srcset.append({"src": "/" + p, "w": c.size[0], "h": c.size[1]})
    f = im.copy()
    f.thumbnail((FULL_H, FULL_H), Image.LANCZOS)
    pf = f"{OUT}/{mid}-full.webp"
    f.save(pf, "WEBP", quality=86, method=6)
    top = srcset[-1]
    out.append({"id": mid, "name": name, "role": role,
                "card": top["src"], "full": "/" + pf,
                "cw": top["w"], "ch": top["h"],
                "srcset": ", ".join(f'{r["src"]} {r["w"]}w' for r in srcset)})
    print(f"  {name:15} src {im.size[0]}x{im.size[1]}  card {top['w']}x{top['h']}"
          f" ({len(srcset)} widths)  full {f.size[0]}x{f.size[1]}"
          f" ({os.path.getsize(pf)//1024}KB)")

json.dump(out, open("assets/portfolio/members.json", "w"), indent=1)
