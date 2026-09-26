/* Live Instagram feed, client side.
   Site by Jay Kadam, kadamlabs.com

   Asks /api/instagram for the latest posts and swaps them in over the
   hand-picked embeds already in the HTML. If the endpoint is missing, has no
   token, or fails for any reason, nothing happens and the built-in embeds stay
   exactly as they are. The feed is refreshed on load and whenever the visitor
   comes back to the tab after 30 minutes away, so a long-lived tab does not go
   stale. */

(function () {
  "use strict";

  const wrap = document.querySelector(".gallery__embeds");
  if (!wrap) return;

  const STALE_MS = 30 * 60 * 1000;
  let lastFetch = 0;
  let live = false;

  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const REEL = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M9.5 8.8v6.4l5.5-3.2z"/><rect x="2.6" y="2.6" width="18.8" height="18.8" rx="5.2" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>';

  const render = (posts) => {
    wrap.classList.add("gallery__embeds--live");
    wrap.innerHTML = posts
      .map((p) => {
        const when = new Date(p.timestamp).toLocaleDateString("en-IN", {
          day: "numeric", month: "short", year: "numeric",
        });
        const isVideo = p.type === "VIDEO" || p.type === "CAROUSEL_ALBUM";
        return `<a class="ig-post" href="${esc(p.permalink)}" target="_blank" rel="noopener"
          aria-label="${esc(p.caption || "Instagram post")}, opens Instagram">
          <img src="${esc(p.thumb)}" alt="${esc(p.caption || "The Unplugged Band on Instagram")}"
               loading="lazy" decoding="async" referrerpolicy="no-referrer" />
          ${isVideo ? `<span class="ig-post__type">${REEL}</span>` : ""}
          <span class="ig-post__veil">
            <span class="ig-post__cap">${esc(p.caption || "")}</span>
            <time class="ig-post__date" datetime="${esc(p.timestamp)}">${when}</time>
          </span>
        </a>`;
      })
      .join("");
  };

  const load = () => {
    lastFetch = Date.now();
    fetch("/api/instagram", { headers: { Accept: "application/json" } })
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => {
        if (d && d.ok && Array.isArray(d.posts) && d.posts.length) {
          render(d.posts);
          live = true;
        }
      })
      .catch(() => { /* keep the built-in embeds */ });
  };

  load();

  // Refresh when the visitor returns to a tab that has been sitting open.
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible" && Date.now() - lastFetch > STALE_MS) load();
  });

  // And on a slow cadence for a tab left in the foreground.
  setInterval(() => {
    if (document.visibilityState === "visible") load();
  }, STALE_MS);
})();
