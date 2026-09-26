"""Regenerate portfolio stills at honest resolution, with srcset ladders.
READ-ONLY on media/. Output goes to assets/portfolio/img/."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifest import EVENTS, SRC
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
OUT = "assets/portfolio"
os.makedirs(f"{OUT}/img", exist_ok=True)

# Card ladder covers a 384px third-slot up to a 1180px hero slot at 2x DPR.
LADDER = [700, 1100, 1700, 2400]
FULL   = 2800          # lightbox stage is min(1400px, 94vw) -> 2800 at 2x

def slug(s):
    keep = "".join(c if c.isalnum() else "-" for c in os.path.splitext(os.path.basename(s))[0].lower())
    while "--" in keep: keep = keep.replace("--", "-")
    return keep.strip("-")[:40]

def photo(srcrel, eid, idx):
    src = os.path.join(SRC, srcrel)
    base = f"{eid}-{idx:02d}-{slug(srcrel)}"
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    srcset = []
    for target in LADDER:
        if target > w and srcset:      # never upscale past the source
            break
        c = im.copy()
        c.thumbnail((target, target * 4), Image.LANCZOS)   # constrain on width
        p = f"{OUT}/img/{base}-{c.size[0]}.webp"
        c.save(p, "WEBP", quality=82, method=6)
        srcset.append({"src": "/" + p, "w": c.size[0], "h": c.size[1],
                       "kb": round(os.path.getsize(p) / 1024)})
    f = im.copy()
    f.thumbnail((FULL, FULL), Image.LANCZOS)
    pf = f"{OUT}/img/{base}-full.webp"
    f.save(pf, "WEBP", quality=85, method=6)
    card = srcset[-1]
    return {
        "card": card,                       # largest rendition, used as src fallback
        "srcset": srcset,
        "full": {"src": "/" + pf, "w": f.size[0], "h": f.size[1],
                 "kb": round(os.path.getsize(pf) / 1024)},
        "ratio": round(w / h, 4),
        "srcw": w, "srch": h,
    }

if __name__ == "__main__":
    mpath = f"{OUT}/media.json"
    data = json.load(open(mpath))
    for e in EVENTS:
        eid = e["id"]
        for i, (p, cap) in enumerate(e["photos"], 1):
            r = photo(p, eid, i); r["caption"] = cap
            data[eid]["photos"][i - 1] = r
            print(f"  [img] {eid} {i}/{len(e['photos'])}  src {r['srcw']}x{r['srch']}"
                  f" -> {len(r['srcset'])} widths, top {r['card']['w']}px"
                  f" ({r['card']['kb']}KB), full {r['full']['w']}px ({r['full']['kb']}KB)", flush=True)
    json.dump(data, open(mpath, "w"), indent=1)
    tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(f"{OUT}/img") for f in fs)
    print(f"\nimg/ total: {tot/1048576:.1f} MB")
