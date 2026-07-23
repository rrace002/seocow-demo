# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **fully static website** (Cryptocurrency Consulting factory build) deployed on **Netlify** (`netlify.toml`, `publish = "."`). There is no application server, database, or backend — pages are pre-generated HTML committed to the repo.

### Services
- **Static site** — the only "service". Serve the repo root over HTTP for development.

### Build / generate
- The HTML is produced by `scripts/generate_cryptoconsulting_factory.py` (Python 3 standard library only — no pip dependencies).
- Regenerate with `python3 scripts/generate_cryptoconsulting_factory.py`. It writes into the repo root and is **idempotent**: on a clean checkout it reproduces the committed files exactly (`git status` stays clean). Only run it if you intend to change generated output — otherwise it is a no-op.

### Run (development)
- Serve statically from the repo root, e.g. `python3 -m http.server 8888`, then open `http://localhost:8888/index.html`.
- Optional: `netlify dev` reproduces Netlify redirects/headers (`_redirects`, `netlify.toml`) but requires installing `netlify-cli` (`npm i -g netlify-cli`); it is **not** needed for normal page development. Plain `http.server` does not apply the `_redirects` 404 rewrite.

### Lint / test
- There is **no** configured linter or test suite. The closest check is a Python byte-compile of the generator: `python3 -m py_compile scripts/generate_cryptoconsulting_factory.py`.

### Notes
- The contact / consultation / proposal forms are **demo shells** ("submission destination wired at rollout") — they have no backend and do not POST anywhere.
- NAP details (phone `555…`, `123 Blockchain Avenue`) are placeholder values marked `[confirm]` in the source.
