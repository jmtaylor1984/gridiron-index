/* Gridiron Index — service worker
 * Strategy:
 *   - Precache the app shell (index.html + manifest + icons) on install.
 *   - For navigations: network-first, fall back to cached index.html so the
 *     app opens offline after first load.
 *   - For same-origin static assets: cache-first.
 *   - Cross-origin requests (Google Fonts, YouTube): network-only, never
 *     cached or intercepted in a way that breaks them.
 *
 * The archive data is embedded inline in index.html, so caching index.html
 * makes the entire library available offline.
 */

const CACHE_VERSION = "gridiron-index-v4";
const SHELL_CACHE = `${CACHE_VERSION}-shell`;

const SHELL_ASSETS = [
  "./",
  "./index.html",
  "./data.js",
  "./manifest.webmanifest",
  "./icon.svg",
  "./icon-192.png",
  "./icon-512.png",
  "./icon-maskable-512.png",
  "./apple-touch-icon.png",
  "./favicon-32.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE).then((cache) =>
      // Use individual adds so one missing asset doesn't fail the whole install.
      Promise.all(
        SHELL_ASSETS.map((url) =>
          cache.add(new Request(url, { cache: "reload" })).catch(() => {})
        )
      )
    )
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => (k.startsWith("coaching-archive-") || k.startsWith("gridiron-index-")) && k !== SHELL_CACHE)
          .map((k) => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  const sameOrigin = url.origin === self.location.origin;

  // Don't intercept cross-origin (YouTube clicks open in new tab; fonts are external).
  if (!sameOrigin) return;

  // App navigations -> network-first with cached fallback to index.html.
  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(SHELL_CACHE).then((cache) => cache.put("./index.html", copy)).catch(() => {});
          return res;
        })
        .catch(() =>
          caches.match("./index.html").then(
            (cached) =>
              cached ||
              new Response(
                "<h1>Offline</h1><p>Gridiron Index needs to be opened online once before it can run offline.</p>",
                { headers: { "Content-Type": "text/html; charset=utf-8" } }
              )
          )
        )
    );
    return;
  }

  // Same-origin static assets -> cache-first, refresh in background.
  event.respondWith(
    caches.match(req).then((cached) => {
      const fetched = fetch(req)
        .then((res) => {
          if (res && res.status === 200 && res.type === "basic") {
            const copy = res.clone();
            caches.open(SHELL_CACHE).then((cache) => cache.put(req, copy)).catch(() => {});
          }
          return res;
        })
        .catch(() => cached);
      return cached || fetched;
    })
  );
});
