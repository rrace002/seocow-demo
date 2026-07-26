# Near Me OS — Product Landing (publishable)

Single-page sales site from the Near Me OS landing page (`More Pages. More Searches. More Jobs.`).

## Production notes

- **Canonical / sitemap:** `https://nearmeos.io/`
- **Staging Netlify:** https://near-me-os.netlify.app/ (indexable; no staging banner)
- **Phone:** `(862) 295-0011` → `tel:+18622950011`
- **Email:** `hello@nearmeos.com` — confirm mailbox/DNS before go-live on custom domain
- **CTA:** primary contact button dials the phone number; pricing CTAs scroll to `#contact`
- **Factory pages:** `scripts/generate_nearmeos_factory.py` now preserves this landing at `/index.html` byte-for-byte and adds the 40/80/120-page product factory pages beneath it.

## Go-live checklist

1. Point `nearmeos.io` DNS to this Netlify site
2. Confirm `hello@nearmeos.com` (or swap to final inbox)
3. Optional: replace tel CTA with a calendar booking URL when ready
