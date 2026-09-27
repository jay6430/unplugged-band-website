/* The Unplugged Band, portfolio interactions
   Site by Jay Kadam, kadamlabs.com, jay@kadamlabs.com

   Architecture note: every expensive effect (pointer glow, tilt, tracing
   beam, parallax) is gated behind FX. Phones and reduced-motion users get
   plain fades and still images instead, which keeps the frame rate intact
   on the devices most likely to be viewing this. */

(function () {
  "use strict";

  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));

  const reduced   = window.matchMedia("(prefers-reduced-motion: reduce)");
  const fineWide  = window.matchMedia("(min-width: 900px) and (pointer: fine)");
  const saveData  = navigator.connection && navigator.connection.saveData;
  const FX = fineWide.matches && !reduced.matches;

  if (FX) document.documentElement.classList.add("fx-on");

  /* ---------- video loops: only decode what is on screen ---------- */
  const vids = $$(".pf-item video");
  if (vids.length) {
    if (saveData) {
      // Respect Data Saver: never fetch the clips, leave the poster showing.
      vids.forEach((v) => { v.removeAttribute("src"); v.load(); });
    } else {
      const vio = new IntersectionObserver(
        (entries) => {
          entries.forEach((en) => {
            const v = en.target;
            if (en.isIntersecting) {
              if (!v.dataset.loaded) {
                v.src = v.dataset.src;
                v.dataset.loaded = "1";
              }
              const p = v.play();
              if (p) p.catch(() => {});
            } else if (!v.paused) {
              v.pause();
            }
          });
        },
        { threshold: 0.25 }
      );
      vids.forEach((v) => vio.observe(v));
    }
  }

  /* ---------- pointer glow + subtle tilt (desktop only) ---------- */
  if (FX) {
    $$(".pf-item, .pf-member").forEach((card) => {
      card.addEventListener("pointermove", (e) => {
        const r = card.getBoundingClientRect();
        const x = e.clientX - r.left, y = e.clientY - r.top;
        card.style.setProperty("--mx", x + "px");
        card.style.setProperty("--my", y + "px");
        const rx = ((y / r.height) - 0.5) * -3.2;
        const ry = ((x / r.width) - 0.5) * 3.2;
        card.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg)`;
      });
      card.addEventListener("pointerleave", () => { card.style.transform = ""; });
    });
  }

  /* ---------- tracing beam ---------- */
  const beam = $("#pfBeam");
  if (beam && FX) {
    const fill = $(".pf-beam__fill", beam);
    const dot  = $(".pf-beam__dot", beam);
    let ticking = false;
    const draw = () => {
      const r = beam.getBoundingClientRect();
      const vh = window.innerHeight;
      const total = r.height;
      const progressed = Math.min(Math.max(vh * 0.5 - r.top, 0), total);
      fill.style.height = progressed + "px";
      dot.style.top = progressed + "px";
      dot.style.opacity = progressed > 0 && progressed < total ? "1" : "0";
      ticking = false;
    };
    const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(draw); } };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    draw();
  }

  /* ---------- jump nav active state ---------- */
  const jumpLinks = $$("#pfJump a");
  const chapters  = $$(".pf-event[id]");
  if (jumpLinks.length && chapters.length) {
    const setActive = (id) =>
      jumpLinks.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === "#" + id));
    const cio = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => { if (en.isIntersecting) setActive(en.target.id); });
      },
      { rootMargin: "-45% 0px -50% 0px" }
    );
    chapters.forEach((c) => cio.observe(c));

    // keep the active chip scrolled into view on narrow screens
    const track = $("#pfJump .pf-jump__track");
    if (track) {
      const mo = new MutationObserver(() => {
        const on = track.querySelector("a.is-active");
        if (on) {
          const t = track.getBoundingClientRect(), a = on.getBoundingClientRect();
          if (a.left < t.left || a.right > t.right) {
            track.scrollTo({ left: on.offsetLeft - track.clientWidth / 2 + on.clientWidth / 2, behavior: "smooth" });
          }
        }
      });
      jumpLinks.forEach((a) => mo.observe(a, { attributes: true, attributeFilter: ["class"] }));
    }
  }

  /* ---------- lightbox ---------- */
  const lb      = $("#pfLightbox");
  if (!lb) return;
  const stage   = $(".pf-lb__stage", lb);
  const capEl   = $(".pf-lb__cap", lb);
  const countEl = $(".pf-lb__count", lb);
  const items   = $$(".pf-item, .pf-member");
  let index = -1, lastFocus = null;

  const render = (i) => {
    const el = items[i];
    if (!el) return;
    index = i;
    const type    = el.dataset.type;
    const full    = el.dataset.full;
    const caption = el.dataset.caption || "";
    const event   = el.dataset.event || "";
    stage.querySelectorAll("img,video,iframe").forEach((n) => n.remove());

    let node;
    if (el.dataset.yt) {
      /* A full-length cut with sound lives on YouTube. Local clips are muted
         by necessity (autoplay), so the lightbox hands over to YouTube when a
         video id exists, and falls back to the muted loop when it does not. */
      node = document.createElement("iframe");
      node.src = "https://www.youtube-nocookie.com/embed/" + el.dataset.yt +
                 "?autoplay=1&rel=0&modestbranding=1&playsinline=1";
      node.title = caption || "The Unplugged Band, live";
      node.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      node.allowFullscreen = true;
      node.className = "pf-lb__yt" + (el.dataset.ytVertical ? " pf-lb__yt--tall" : "");
      node.setAttribute("frameborder", "0");
    } else if (type === "video") {
      node = document.createElement("video");
      node.src = full;
      node.autoplay = true; node.loop = true; node.playsInline = true;
      node.controls = true; node.muted = true;
    } else {
      node = document.createElement("img");
      node.src = full;
      node.alt = caption;
    }
    stage.insertBefore(node, stage.firstChild);
    capEl.innerHTML = `<b>${event}</b>${caption ? " &nbsp;·&nbsp; " + caption : ""}`;
    countEl.textContent = `${i + 1} / ${items.length}`;
  };

  const open = (i) => {
    lastFocus = document.activeElement;
    render(i);
    lb.classList.add("is-open");
    lb.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    $(".pf-lb__close", lb).focus();
  };
  const close = () => {
    lb.classList.remove("is-open");
    lb.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    stage.querySelectorAll("video").forEach((v) => v.pause());
    stage.querySelectorAll("iframe").forEach((f) => f.remove());
    if (lastFocus) lastFocus.focus();
  };
  const step = (d) => render((index + d + items.length) % items.length);

  items.forEach((el, i) => {
    el.addEventListener("click", () => open(i));
    el.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(i); }
    });
  });

  $(".pf-lb__close", lb).addEventListener("click", close);
  $(".pf-lb__prev", lb).addEventListener("click", (e) => { e.stopPropagation(); step(-1); });
  $(".pf-lb__next", lb).addEventListener("click", (e) => { e.stopPropagation(); step(1); });
  lb.addEventListener("click", (e) => { if (e.target === lb) close(); });

  document.addEventListener("keydown", (e) => {
    if (!lb.classList.contains("is-open")) return;
    if (e.key === "Escape") close();
    else if (e.key === "ArrowRight") step(1);
    else if (e.key === "ArrowLeft") step(-1);
    else if (e.key === "Tab") {
      // simple focus trap
      const f = $$('button, [href], video[controls], iframe', lb).filter((n) => n.offsetParent !== null);
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  /* ---------- swipe on touch ---------- */
  let sx = 0;
  lb.addEventListener("touchstart", (e) => { sx = e.changedTouches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", (e) => {
    const dx = e.changedTouches[0].clientX - sx;
    if (Math.abs(dx) > 55) step(dx < 0 ? 1 : -1);
  }, { passive: true });
})();
