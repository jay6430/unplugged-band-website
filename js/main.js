/* The Unplugged Band, site interactions
   Developed & managed by Jay Kadam

   Shared by every page, so each block guards for the elements it needs.
   The story page, for example, has no booking form. */

(function () {
  "use strict";

  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  /* ---------- preloader ---------- */
  const preloader = $("#preloader");
  if (preloader) {
    const hide = () => preloader.classList.add("is-done");
    window.addEventListener("load", () => setTimeout(hide, 250));
    setTimeout(hide, 2000);
  }

  /* ---------- sticky nav ---------- */
  const nav = $("#nav");
  const toTop = $("#toTop");
  if (nav || toTop) {
    const onScroll = () => {
      const y = window.scrollY;
      if (nav) nav.classList.toggle("is-stuck", y > 40);
      if (toTop) toTop.classList.toggle("is-visible", y > 600);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  if (toTop) {
    toTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------- mobile menu ---------- */
  const toggle = $("#navToggle");
  const links = $("#navLinks");
  if (toggle && links) {
    const closeMenu = () => {
      toggle.classList.remove("is-open");
      links.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    };
    toggle.addEventListener("click", () => {
      const open = links.classList.toggle("is-open");
      toggle.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      document.body.style.overflow = open ? "hidden" : "";
    });
    $$("#navLinks a").forEach((a) => a.addEventListener("click", closeMenu));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeMenu();
    });
  }

  /* ---------- scroll reveal ---------- */
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, i) => {
        if (!entry.isIntersecting) return;
        setTimeout(() => entry.target.classList.add("is-visible"), Math.min(i, 5) * 70);
        revealObserver.unobserve(entry.target);
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -60px 0px" }
  );
  $$(".reveal").forEach((el) => revealObserver.observe(el));

  /* ---------- animated stat counters ---------- */
  const countObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = parseInt(el.dataset.count, 10);
        const suffix = el.dataset.suffix || "";
        const duration = 1600;
        const start = performance.now();
        const tick = (now) => {
          const p = Math.min((now - start) / duration, 1);
          const eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * eased) + (p === 1 ? suffix : "");
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
        countObserver.unobserve(el);
      });
    },
    { threshold: 0.5 }
  );
  $$("[data-count]").forEach((el) => countObserver.observe(el));

  /* ---------- active nav link on scroll ---------- */
  const sections = $$("main section[id]");
  const navLinks = $$('#navLinks a[href^="#"]');
  if (sections.length && navLinks.length) {
    const sectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const id = entry.target.id;
          navLinks.forEach((a) =>
            a.classList.toggle("is-active", a.getAttribute("href") === "#" + id)
          );
        });
      },
      { rootMargin: "-45% 0px -50% 0px" }
    );
    sections.forEach((s) => sectionObserver.observe(s));
  }

  /* ---------- member card spotlight ---------- */
  $$(".member").forEach((card) => {
    card.addEventListener("pointermove", (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty("--mx", `${e.clientX - r.left}px`);
      card.style.setProperty("--my", `${e.clientY - r.top}px`);
    });
  });

  /* ---------- booking form to WhatsApp ---------- */
  const MANAGER_WHATSAPP = "917069001861";
  const form = $("#bookingForm");

  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();

      const name = $("#bf-name");
      const phone = $("#bf-phone");
      let valid = true;

      [name, phone].forEach((input) => {
        const ok = input.value.trim().length > 0;
        input.classList.toggle("is-invalid", !ok);
        if (!ok) valid = false;
      });
      if (!valid) {
        name.value.trim() ? phone.focus() : name.focus();
        return;
      }

      const lines = [
        "Hi! I'd like to book The Unplugged Band.",
        "",
        `Name: ${name.value.trim()}`,
        `Phone: ${phone.value.trim()}`,
      ];
      const date = $("#bf-date").value;
      const city = $("#bf-city").value.trim();
      const msg = $("#bf-msg").value.trim();

      lines.push(`Event type: ${$("#bf-type").value}`);
      if (date) lines.push(`Date: ${date}`);
      if (city) lines.push(`City: ${city}`);
      if (msg) lines.push("", `Details: ${msg}`);

      const url = `https://wa.me/${MANAGER_WHATSAPP}?text=${encodeURIComponent(lines.join("\n"))}`;
      window.open(url, "_blank", "noopener");
    });

    $$("#bookingForm input").forEach((input) => {
      input.addEventListener("input", () => input.classList.remove("is-invalid"));
    });
  }

  /* ---------- footer year ---------- */
  const year = $("#year");
  if (year) year.textContent = new Date().getFullYear();
})();
