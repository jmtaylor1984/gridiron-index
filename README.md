# Gridiron Index

Gridiron Index is a static football learning library for players, parents, and coaches. It organizes curated, open-access football instruction videos by position, topic, and source so users can find useful training content faster.

## Overview

This project is a front-end web app that can be hosted as a static site. It does not require a backend, login system, database, cookies, or local storage.

The app includes:

- A landing page for Gridiron Index
- A searchable football video library
- Filters by football category and position
- Pricing/subscribe section
- Gumroad subscription link
- PWA assets and icons

## Files

After extracting the ZIP, the important files are:

```text
index.html
data.js
archive-data.json
manifest.webmanifest
service-worker.js
icon.svg
icon-maskable.svg
icon-192.png
icon-512.png
icon-maskable-512.png
apple-touch-icon.png
favicon-32.png
```

## How to run locally

Because this is a static web app, you can open `index.html` directly in a browser.

For best results, run it through a local static server:

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

## How to deploy

You can deploy this project to any static hosting provider, including:

- GitHub Pages
- Netlify
- Vercel
- Cloudflare Pages
- Render static site hosting

For GitHub Pages:

1. Create a new GitHub repository.
2. Upload all extracted files into the repository root.
3. Go to **Settings → Pages**.
4. Under **Build and deployment**, choose:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/root`
5. Save.
6. GitHub will publish the app at your GitHub Pages URL.

## Gumroad link

The current subscription link points to:

```text
https://taylorverse737.gumroad.com/l/gridiron-index
```

If you need to update it, search inside `index.html` for:

```text
taylorverse737.gumroad.com/l/gridiron-index
```

Replace it with the new Gumroad product URL.

## Product positioning

**Gridiron Index** is the position library every football family wishes existed.

It helps users avoid random YouTube searching by giving them a structured archive of hand-picked football learning resources.

## Who it is for

- Football parents helping their athlete learn the game
- Youth and high school football players
- Coaches looking for teaching clips and drill ideas
- Anyone trying to understand football positions and techniques

## Important note

Gridiron Index does not host or claim ownership of third-party football videos. It organizes and links to publicly available football instruction content.

## License

All original app code and structure belong to the project owner. Third-party videos and linked resources remain the property of their respective owners.
