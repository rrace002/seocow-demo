# NearMe OS Website Factory — Completeness Instruction Set

**Quality bar:** live [san-diegotechsupport.com](https://www.san-diegotechsupport.com/) (WordPress/Elementor MSP), **not** the thin Gate 1 hatch-hero template.

Gate 1 still means **10 hubs × 10 children = 100 SVC-CHILD pages**. Completeness is **how those pages look and what modules they carry**, plus a small chrome set (insights, search, partners). A 117-page site that repeats five generic bullets is a fail. A site that feels like a finished local-service business website is a pass.

This file is the instruction set for every factory build (new verticals and regenerations). Code that implements it lives in `scripts/factory_complete.py` and the site generator.

---

## 1. What “complete” means (SDT checklist)

A visitor who knows the live San Diego Tech Support site should recognize the **same kind of site**, even when the trade, colors, and copy change.

| Module | Live SDT does this | Factory must do this |
|---|---|---|
| Logo | Real image logo in header | SVG wordmark + mark (not unstyled text only) |
| Utility bar | Phone, email, location, social | Phone, email, city, hours |
| Navigation | Deep mega-menu (hubs, children, about, industries) | Hub dropdown listing **all 10 hubs**; About dropdown; **distinct** Contact vs Proposal vs Consultation |
| Search | “Search / Find Now” on home and inner pages | Search field in hero **and** a `/search/` results page |
| Hero | Full-bleed photographic band, kicker, H1, support line, CTAs | Photo-style hero (image panel or photo treatment — **never** repeating CSS hatch), kicker, H1, sub, two CTAs, search |
| Service tiles | Icon + title cards for core lines | Icon tiles for all 10 hubs (SVG icons, not empty cards) |
| Proof stats | Named KPIs (wait time, SLA, tickets, CSAT) | 4–6 stats from **public facts only**; unlabeled invention is forbidden |
| Benefits | “Why choose us” icon boxes | 6 benefit cards unique to the business |
| How it works | 3-step engagement path + form | 3 steps **and** a homepage contact form |
| Partners | Logo strip of platforms | Partner/platform strip from public facts or `[confirm]` |
| Insights | Blog / Tech Advisory cards | `/insights/` hub + at least **6** articles (factory-written, owner-review) |
| Service pages | Long unique copy, included lists, comparison, form, FAQ, related, glossary/articles | See §4 |
| Footer | Dense link columns + NAP | Services, Company, Insights, Get started, NAP |
| Photos | Dozens of images | Photo panels or SVG scenes on home, about, hubs — not a text-only document |

---

## 2. Visual system (do not ship the old template)

**Forbidden (old Gate 1 look):**

- `repeating-linear-gradient` hatch heroes
- Georgia body + generic “SEO Cow” orange hover leftovers
- Duplicate nav items (two “Contact” links)
- Leftover vertical copy (“ad capacity”, “coaching-led curriculum”, wrong city/trade)
- Empty form shells with no surrounding process copy
- Leaf pages that only swap the H1 and reuse the same five bullets

**Required look:**

- Sans-serif UI: **Sora** (headlines) + **Source Sans 3** (body), with system fallbacks
- Full-width sections, max content ~1160px
- Dark utility bar, white header, solid primary nav
- Photographic or illustrated heroes (`.hero-photo`), split layouts, icon tiles, card shadows
- Category accent color is allowed; **navy + one accent** reads more complete than a single neon fill
- Click-to-call and form CTAs on **every** important page (home, hub, child, about, contact)

---

## 3. Homepage required sections (in order)

1. Staging banner (if staging) + utility bar + header + nav  
2. **Hero** — kicker, H1, 1–2 sentence value prop, Consultation + Proposal (or Call), search  
3. **Service icon grid** — all hubs  
4. **Stats / by-the-numbers** — only FACT or clearly labeled staging counts (page map size is OK)  
5. **Why choose us / benefits** — six cards  
6. **How it works** — three steps  
7. **Homepage form** — same fields as `/contact/`  
8. **Insights teaser** — three latest articles  
9. **Partners / platforms**  
10. **FAQ** (business-specific)  
11. Closing CTA strip  
12. Footer  

---

## 4. Service hub and child pages

### Hub (`SVC-HUB`)

- Photo-style inner hero or split intro (not a bare H2)  
- 120–200 words unique to **this** hub  
- Grid of 10 children with one-line blurbs  
- “What’s included” checklist (hub-specific, not global boilerplate)  
- Inline request form  
- 3 hub-specific FAQs  
- Links to related hubs  

### Child (`SVC-CHILD`) — completeness bar vs SDT inner pages

Each child must be **unique enough to stand alone**. Minimum:

- Breadcrumb  
- Unique H1 (not “Engage {Brand} for {service}…” on every page)  
- **≥ 3 unique paragraphs** derived from that child’s blurb + hub (no identical body across siblings)  
- Two lists: “What this engagement includes” and “Problems this replaces”  
- Comparison block (DIY / one-person shop vs this firm) — **worded for this trade**  
- Inline form (Name, Email, Phone, Company, Service, Message)  
- Related children  
- 4 FAQs with answers that mention the **child service name** and do not reuse PPC/ad leftover phrases  
- Insights teaser (optional but preferred)  

Copy rules:

- Ground in questionnaire + live-site public facts.  
- Mark unverified NAP, hours, partner badges, headcount, and KPIs with `[confirm]`.  
- **Never invent** testimonials, awards, client names, ticket counts, or guaranteed outcomes.  
- **Never** leave factory leftovers from a previous vertical.

---

## 5. Chrome pages beyond 10×10

Every Gate 1 build also ships:

| URL | Type | Notes |
|---|---|---|
| `/` | HOME | §3 |
| `/about…/` + why-choose + who-we-serve | COMP | Team/mission/proof; still no fake bios |
| `/contact/` | COMP-CONTACT | NAP + form |
| `/request-a-consultation/` | FORM-CONSULT | Process + form |
| `/request-a-proposal/` | FORM-PRICING | Process + form |
| `/insights/` + ≥6 articles | RESOURCE | Factory advisory; banner “pending owner review” |
| `/search/` | UTILITY | Client-side filter of the page inventory |
| `404.html` | ERROR | Search + home + consult |

Insights articles are **original** category explainers (200–400 words), not scraped blog posts and not SDT HIPAA posts copied onto other trades.

---

## 6. Navigation and IA

- **One** Contact item. Proposal and Consultation are separate labels.  
- Services dropdown = all hubs.  
- About dropdown = About, Why choose us, Who we serve.  
- Insights in nav.  
- Footer repeats hubs + company + insights + NAP.  
- Phone in header is always `tel:`.  

---

## 7. Photos and icons

1. Prefer **owner photos** from intake.  
2. If none: **SVG illustrations + photo-treatment CSS** in `factory_complete.py` (gradients, grain, silhouettes). Do not hotlink another company’s WordPress uploads.  
3. Every hub gets a distinct icon from the shared SVG set.  
4. Partner names may be text badges until real logos are supplied.

---

## 8. Generator contract

A site generator in `scripts/generate_*_factory.py` **must**:

1. Import chrome/CSS/modules from `scripts/factory_complete.py` (do not paste the old hatch CSS).  
2. Fill `SiteConfig` (identity, NAP, colors, stats, benefits, partners, insights).  
3. Emit unique hub/child copy (per-child blurbs are not optional).  
4. Write `PAGE-INVENTORY.csv` (or vertical-prefixed inventory) including insights + search.  
5. Keep staging `noindex` + banner until the owner turns them off.  
6. Pass `scripts/test_factory_completeness.py` before the PR is called done.

---

## 9. Definition of done (agent)

- [ ] Instruction modules present on home (hero-photo, icon grid, stats, benefits, how-it-works, home form, insights, partners).  
- [ ] No hatch-hero CSS, no duplicate Contact nav, no leftover phrases from other verticals.  
- [ ] Child pages have unique H1 + ≥3 paragraphs + inline form.  
- [ ] Insights hub + 6 articles.  
- [ ] Search page finds hub/child titles.  
- [ ] Completeness test script exits 0.  
- [ ] Visual pass: homepage and one child page look like a finished service business site, not a markdown dump.

**Reference while building:** https://www.san-diegotechsupport.com/ (structure, density, trust modules). **Do not copy** their copyrighted copy, images, or client stats onto other brands.
