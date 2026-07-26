# Near Me OS — Integrated Sales Home + Factory

Publishable Near Me OS site with one shared chrome across home and all factory pages.

## Production notes

- **Canonical / sitemap:** `https://nearmeos.io/`
- **Staging Netlify:** https://near-me-os.netlify.app/
- **Phone:** `(862) 295-0011` → `tel:+18622950011`
- **Email:** `hello@nearmeos.com`
- **Home:** sales narrative (hero, pricing, compare, FAQ) using the same utility bar / logo / Packages nav / footer as every inner page
- **Factory:** Gate 1 10×10 (~117 pages) via `scripts/generate_nearmeos_factory.py`

## Regenerate

```bash
python3 scripts/generate_nearmeos_factory.py
```
