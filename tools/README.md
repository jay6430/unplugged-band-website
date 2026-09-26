# Portfolio build scripts

Everything here reads `media/Portfolio/` and never writes to it. All output
goes to `assets/portfolio/`. Run from the repository root.

| script | what it does | when to run |
|---|---|---|
| `photos.py` | Stills to WebP at 700/1100/1700/2400 wide plus a 2800px lightbox copy | after changing the photo picks in `manifest.py` |
| `loops.py` | 8s muted grid loops, 1600x900 (or 810x1440 for vertical) at CRF 23, plus posters | after changing clip picks or start times |
| `members.py` | Band portraits, 4:5 crop, 420/760/1140/1520 wide plus a 2400px lightbox copy | rarely |
| `gen.py` | Renders `portfolio.html` from `portfolio.tpl.html` + the JSON files | **after any of the above, and after editing `youtube.json`** |

```bash
python3 tools/gen.py
```

## Adding a full video with sound

Grid loops are muted because browsers refuse to autoplay audio. The full cut
with sound lives on YouTube, and the lightbox switches to it automatically.

1. Upload the video to YouTube and set it to **Unlisted**. Private videos
   cannot be embedded on a website at all, so Private will not work here.
2. Paste the link or the 11 character id into `assets/portfolio/youtube.json`
   against the matching clip key.
3. Run `python3 tools/gen.py`.

That tile now opens the YouTube player with sound instead of the muted loop,
and it gets a "Full clip" badge. Clips left blank keep working exactly as they
are, so this can be done a few at a time.

## Live Instagram feed

`api/instagram.js` is a Vercel function. It needs an `INSTAGRAM_TOKEN`
environment variable set in the Vercel dashboard. Without it the endpoint
returns an empty list and the page falls back to the hand picked embeds in
`index.html`, so nothing breaks.
