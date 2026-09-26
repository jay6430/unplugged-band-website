/* Live Instagram feed for The Unplugged Band.
   Site by Jay Kadam, kadamlabs.com

   The old Basic Display API was retired in December 2024, so this uses the
   Instagram API with Instagram Login (graph.instagram.com), which needs a
   Business or Creator account and a long-lived token.

   The token is read from the INSTAGRAM_TOKEN environment variable and never
   reaches the browser. If it is missing or rejected, this returns an empty
   list and the page keeps showing its built-in embeds, so the section can
   never break the site.

   Responses are cached at the edge for an hour and served stale for a day
   while revalidating, which keeps us far inside Instagram's rate limits. */

const FIELDS = "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp";
const LIMIT = 12;

module.exports = async function handler(req, res) {
  res.setHeader("Cache-Control", "public, s-maxage=3600, stale-while-revalidate=86400");

  const token = process.env.INSTAGRAM_TOKEN;
  if (!token) {
    return res.status(200).json({ ok: false, reason: "no-token", posts: [] });
  }

  try {
    const url = `https://graph.instagram.com/me/media?fields=${FIELDS}&limit=${LIMIT}&access_token=${token}`;
    const r = await fetch(url);
    if (!r.ok) {
      const body = await r.text();
      console.error("instagram api error", r.status, body.slice(0, 300));
      return res.status(200).json({ ok: false, reason: "api-" + r.status, posts: [] });
    }
    const json = await r.json();
    const posts = (json.data || [])
      .filter((p) => p.media_type !== "VIDEO" || p.thumbnail_url)
      .map((p) => ({
        id: p.id,
        permalink: p.permalink,
        thumb: p.media_type === "VIDEO" ? p.thumbnail_url : p.media_url,
        type: p.media_type,
        caption: (p.caption || "").split("\n")[0].slice(0, 140),
        timestamp: p.timestamp,
      }))
      .slice(0, 6);
    return res.status(200).json({ ok: true, posts });
  } catch (e) {
    console.error("instagram fetch failed", e);
    return res.status(200).json({ ok: false, reason: "fetch-failed", posts: [] });
  }
}
