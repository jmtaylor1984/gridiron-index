# Gridiron Index Render Deployment Steps

This package is the responsive app version of Gridiron Index. It works on phone, tablet, and desktop. It includes a backend login, so do not host it as a static-only website.

## Files included

- `index.html`: responsive app interface
- `server.py`: Python backend for login and protected archive access
- `archive-data.json`: protected archive data returned only after login
- `render.yaml`: Render deployment settings
- `manifest.webmanifest`, `service-worker.js`, and icon files: installable app support

## Current test login

Email:

```text
member@gridironindex.com
```

Password:

```text
GI-MAY-2026
```

This is a shared first-launch login. For a larger launch, upgrade to unique accounts per buyer.

## Deploy on Render

1. Create or log in to your Render account.
2. Create or log in to your GitHub account.
3. Create a new private GitHub repository named:

```text
gridiron-index
```

4. Upload all files from this package into that repository.
5. In Render, click **New**.
6. Choose **Web Service**.
7. Connect your GitHub account if asked.
8. Select the `gridiron-index` repository.
9. Use these settings:

```text
Name: gridiron-index
Runtime: Python
Build Command: leave blank
Start Command: python3 server.py
Instance Type: Free
```

10. Add or confirm these environment variables:

```text
GI_MEMBER_EMAIL=member@gridironindex.com
GI_MEMBER_PASSWORD=GI-MAY-2026
GI_TOKEN_TTL_SECONDS=28800
```

11. Click **Deploy Web Service**.
12. Wait for Render to finish deploying.
13. Copy the public Render URL.
14. Open the Render URL on your phone and desktop.
15. Log in with the test login above.
16. Confirm the 128-video archive opens.

## Update Gumroad

In Gumroad, go to your product content page called **Member Access Link**.

Replace the Perplexity preview link with your new Render URL.

Keep this login text for the first test:

```text
Email: member@gridironindex.com
Password: GI-MAY-2026
```

## Important free-hosting note

Render free services can spin down when idle. The first visitor after idle time may wait while the service wakes up. This is acceptable for testing, but once you have paying customers, upgrade to a paid always-on service.

## What to do before a real public launch

Before selling to many customers, upgrade from the shared login to one of these:

- unique email/password accounts
- magic email login links
- Gumroad license validation
- Gumroad webhooks that activate and deactivate users automatically

The current version is good enough for private testing and early validation, not a fully automated membership platform.
