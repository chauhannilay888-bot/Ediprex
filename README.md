# EditForge — Video Editor Portfolio

Professional portfolio website for **Krishna Mishra** (EditForge).

Single Next.js application: frontend + `/api/contact` under one domain.

## Stack

- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS v4
- Nodemailer (server-side email)
- Zod (validation)

## Quick start

```bash
cd editforge-portfolio
npm install
cp .env.example .env.local
# edit .env.local with your SMTP credentials
npm run dev
```

Open http://localhost:3000

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SMTP_HOST` | Yes (prod) | e.g. `smtp.gmail.com` |
| `SMTP_PORT` | No | Default `587` |
| `SMTP_SECURE` | No | `true` for port 465 |
| `SMTP_USER` | Yes (prod) | Gmail address |
| `SMTP_PASS` | Yes (prod) | Gmail App Password |
| `SMTP_FROM` | No | From address |
| `CONTACT_TO` | No | Default: chauhannilay888@gmail.com |
| `NEXT_PUBLIC_SITE_URL` | No | For sitemap / OG |

### Gmail setup

1. Enable 2-Step Verification on the Gmail account.
2. Create an App Password: Google Account → Security → App passwords.
3. Use that 16-character password as `SMTP_PASS`.

Never commit real credentials. Use `.env.local` (gitignored).

## Content & assets

All copy and portfolio items live in:

```
src/content/site.ts
```

Update:

- Name, bio, email, WhatsApp, YouTube URL
- Services list
- Portfolio items (title, category, description, video path)
- Workflow steps / “Why work with me” points

### Assets

```
public/assets/banner/editforge-banner.png
public/assets/portfolio/reel-7.mp4
public/assets/portfolio/reel-10.mp4
public/assets/profile/   ← optional profile photo
```

Add new videos under `public/assets/portfolio/` and register them in `site.ts`.

## Contact form

- Client + server validation
- Honeypot field
- Simple IP rate limit (5 / hour)
- Sends email to `CONTACT_TO` with reply-to set to the visitor’s address
- In development without SMTP, the form still succeeds and logs the payload

## Scripts

```bash
npm run dev      # local development
npm run build    # production build
npm run start    # run production server
npm run lint     # eslint
```

## Deployment (one domain)

Recommended: **Vercel** (native Next.js support, serverless API routes).

1. Push the repo to GitHub.
2. Import project in Vercel.
3. Add the environment variables in the Vercel dashboard.
4. Deploy. Your site + `/api/contact` live on the same domain.

Other platforms that support Next.js server routes (Netlify, Railway, Render, etc.) also work as long as you do **not** split frontend and backend into separate deployments.

## Custom domain

Point your domain to the host (Vercel / Netlify / …) and set `NEXT_PUBLIC_SITE_URL` to the final URL.

## Notes

- No fabricated clients, testimonials, or stats.
- Pricing is discussed after a free short demo or conversation.
- WhatsApp prefill message is configured in the Contact component.


---

## Important notes for first run

1. Run `npm install` on your local machine (Windows / Mac / Linux). The sandbox used to build this project had intermittent filesystem and registry issues; a normal local install works fine.

2. Copy `.env.example` → `.env.local` and fill in Gmail App Password for SMTP.

3. Place any additional reels in `public/assets/portfolio/` and register them in `src/content/site.ts`.

4. Optional profile photo: put a file in `public/assets/profile/` and set `profileImage` in `site.ts`.

5. Deploy to Vercel (or any Next.js-compatible host). Add the same env vars in the dashboard. One domain = website + `/api/contact`.

