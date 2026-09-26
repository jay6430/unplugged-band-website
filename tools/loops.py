"""Re-encode the grid loops at a resolution that matches the slots they fill.
READ-ONLY on media/. Output goes to assets/portfolio/video/ and img/.

Grid loops stay muted: browsers refuse to autoplay audio, so a muted loop is
the only thing that can play unprompted. Sound lives in the lightbox instead.
"""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifest import EVENTS, SRC
from PIL import Image

OUT = "assets/portfolio"

def slug(s):
    keep = "".join(c if c.isalnum() else "-" for c in os.path.splitext(os.path.basename(s))[0].lower())
    while "--" in keep: keep = keep.replace("--", "-")
    return keep.strip("-")[:40]

def loop(srcrel, start, eid, idx):
    src = os.path.join(SRC, srcrel)
    base = f"{eid}-{idx:02d}-{slug(srcrel)}"
    mp4 = f"{OUT}/video/{base}.mp4"
    poster = f"{OUT}/img/{base}-poster.webp"
    pr = subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream=width,height","-of","csv=p=0:s=x",src],
        capture_output=True, text=True).stdout.strip().split("x")
    w, h = int(pr[0]), int(pr[1])
    # Phone footage stores landscape pixels plus a rotation flag; ffmpeg applies
    # that flag on decode, so orientation has to come from stored dims + rotation,
    # not from stored dims alone.
    rot = subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream_side_data=rotation","-of","default=nw=1:nk=1",src],
        capture_output=True, text=True).stdout.strip().splitlines()
    rot = int(float(rot[0])) if rot else 0
    if abs(rot) % 180 == 90:
        w, h = h, w
    vertical = h > w
    # widest slot a clip can land in is --wide (782 CSS px) -> 1564 at 2x DPR
    scale = "scale=810:-2" if vertical else "scale=-2:900"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(start),"-t","8","-i",src,
        "-an","-vf",f"{scale},fps=25","-c:v","libx264","-crf","23","-preset","slow",
        "-profile:v","high","-pix_fmt","yuv420p","-movflags","+faststart", mp4], check=True)
    tmp = "/tmp/_poster.png"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(start+1),"-i",src,"-vframes","1",
        "-vf", scale, tmp], check=True)
    Image.open(tmp).convert("RGB").save(poster, "WEBP", quality=86, method=6)
    os.remove(tmp)
    out = subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream=width,height","-of","csv=p=0:s=x",mp4],
        capture_output=True, text=True).stdout.strip().split("x")
    return {"mp4": "/" + mp4, "poster": "/" + poster, "vertical": vertical,
            "kb": round(os.path.getsize(mp4)/1024), "w": int(out[0]), "h": int(out[1])}

if __name__ == "__main__":
    mpath = f"{OUT}/media.json"
    data = json.load(open(mpath))
    for e in EVENTS:
        eid = e["id"]
        for i, (v, st, cap) in enumerate(e["loops"], 1):
            r = loop(v, st, eid, i); r["caption"] = cap
            # preserve any youtube id already attached to this clip
            prev = data[eid]["loops"][i-1]
            if prev.get("yt"): r["yt"] = prev["yt"]
            data[eid]["loops"][i-1] = r
            print(f"  [vid] {eid} {i}/{len(e['loops'])}  {r['w']}x{r['h']} {r['kb']}KB", flush=True)
    json.dump(data, open(mpath, "w"), indent=1)
    tot = sum(os.path.getsize(os.path.join(dp,f)) for dp,_,fs in os.walk(f"{OUT}/video") for f in fs)
    print(f"\nvideo/ total: {tot/1048576:.1f} MB")
