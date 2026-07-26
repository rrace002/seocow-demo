#!/usr/bin/env python3
"""Generate the Near Me OS site: sales home + Gate 1 factory pages.

Gate 1 architecture:
- Shared chrome (utility bar, logo/phone, nav, footer) on every page including home
- Home keeps the sales narrative (hero, pricing, compare, FAQ) in factory styling
- 10 hubs × 10 children = 100 SVC-CHILD pages + about/contact/forms ≈ 117 pages
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://nearmeos.io"
PHONE = "(862) 295-0011"
PHONE_TEL = "+18622950011"
EMAIL = "hello@nearmeos.com"
HQ = "Elizabeth, NJ"
ADDRESS = "12 Sayre St, Elizabeth, NJ 07208"
OPERATOR = "Race Computer Services, LLC"
TAGLINE = "More Pages. More Searches. More Jobs."

PRICING = [
    {
        "name": "Local Launch",
        "pages": "40 pages",
        "one_time": "$2,495",
        "monthly": "$495 setup + $249/mo",
        "fit": "Single-town contractors who need the core service and location foundation online fast.",
    },
    {
        "name": "Service Area Pro",
        "pages": "80 pages",
        "one_time": "$4,495",
        "monthly": "$495 setup + $349/mo",
        "fit": "Growing service-area businesses covering multiple towns and high-value job types.",
    },
    {
        "name": "Market Dominator",
        "pages": "120 pages",
        "one_time": "$6,495",
        "monthly": "$495 setup + $499/mo",
        "fit": "Local operators ready to publish the deepest local search footprint in their market.",
    },
]


FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#0b1220;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#d97706;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.utility{background:#0b1220;color:#f4f6fa;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
header.main{background:#fff;border-bottom:3px solid #f59e0b;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#0b1220}.logo span{color:#f59e0b}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5b6779;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#0b1220}
.phone-cta small{display:block;color:#5b6779;font-size:11px}
nav.nav{background:#0b1220}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav>div.wrap>ul>li>a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav>div.wrap>ul>li>a:hover{background:#111c30;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(11,18,32,.18);border-top:3px solid #f59e0b;z-index:60}
nav.nav .dd a{display:block;color:#0b1220;padding:10px 15px;font-size:13.5px;font-weight:500;border-bottom:1px solid #e6eaf1;background:#fff}
nav.nav .dd a:hover{background:#f4f6fa;color:#0b1220;text-decoration:none}
.nav .em>a{background:#f59e0b;color:#0b1220}.nav .em>a:hover{background:#d97706;color:#fff}
.hero{background:linear-gradient(rgba(11,18,32,.86),rgba(11,18,32,.86)),repeating-linear-gradient(45deg,#0b1220 0 14px,#111c30 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#f4f6fa;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#f59e0b;color:#0b1220;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#d97706;color:#fff;text-decoration:none}
.btn.alt{background:#0b1220;color:#fff}.btn.alt:hover{background:#1b2a45}
section{padding:44px 0}
section.tint{background:#f4f6fa}
section h2{font-size:25px;color:#0b1220;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#d97706;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}.phone-cta{text-align:left}}
.card{background:#fff;border:1px solid #dfe5ee;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(11,18,32,.06)}
.card h3{color:#0b1220;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #dfe5ee;border-left:4px solid #f59e0b;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#0b1220}
.gcard p{font-size:14px;color:#5b6779;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#d97706}
.ctastrip{background:#0b1220;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #dfe5ee;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#f4f6fa}.vs .col.good{background:#fff8ed}
.vs h3{font-size:16px;margin-bottom:12px;color:#0b1220}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #dfe5ee}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#b42318;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#d97706;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #dfe5ee;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#0b1220;list-style:none}
details summary:before{content:"+ ";color:#f59e0b;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #dfe5ee;border-top:4px solid #f59e0b;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#5b6779;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #b8c2d1;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5b6779;padding:14px 0 0}
.crumb a{color:#5b6779}
footer{background:#0b1220;color:#cbd5e1;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#cbd5e1}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #24344f;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#94a3b8}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #dfe5ee;border-top:4px solid #f59e0b;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#0b1220}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5b6779;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #dfe5ee;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(11,18,32,.07)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#0b1220}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#f59e0b;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#f59e0b;color:#0b1220;text-align:center;padding:32px 0}
.audit h2{color:#0b1220;margin-bottom:8px}.audit a.btn{background:#fff;color:#0b1220}
.hero-home{text-align:left;padding:56px 0 48px;background:linear-gradient(160deg,#0b1220 0%,#111c31 55%,#16233c 100%)}
.hero-home .hero-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}
.hero-home h1{font-size:clamp(1.9rem,3.8vw,2.7rem);max-width:none;margin:0 0 16px;line-height:1.15;font-family:'Segoe UI',Arial,Helvetica,sans-serif}
.hero-home h1 em{color:#f59e0b;font-style:normal}
.hero-home .hero-sub{color:#b9c3d4;font:400 1.05rem Georgia,'Times New Roman',serif;letter-spacing:0;max-width:34rem;margin-bottom:22px;line-height:1.6}
.hero-home .hero-sub b{color:#fff}
.hero-home .eyebrow{display:inline-block;background:rgba(245,158,11,.14);color:#f59e0b;font:700 .78rem 'Segoe UI',sans-serif;letter-spacing:.08em;text-transform:uppercase;padding:6px 12px;border-radius:99px;margin-bottom:16px}
.hero-home .hero-ctas{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:14px}
.hero-home .hero-ctas .btn{margin-top:0}
.hero-home .btn.ghost{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.35)}
.hero-home .btn.ghost:hover{border-color:#fff;background:rgba(255,255,255,.06);color:#fff}
.hero-home .hero-note{font-size:.88rem;color:#8d99ad;margin:0}
.hero-home .hero-note strong{color:#c8d0dc}
.pagegrid-card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:22px;text-align:center}
.pagegrid-title{font:600 .78rem 'Segoe UI',sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#8d99ad;margin-bottom:14px}
.pg{display:grid;grid-template-columns:repeat(12,1fr);gap:4px;margin-bottom:12px}
.pg i{display:block;aspect-ratio:1;border-radius:2px;background:#f59e0b}
.pg i.dim{background:#2c3a52}
.pg-caption{font-size:.85rem;color:#b9c3d4;margin:0}
.pg-caption b{color:#fff}
.kicker{color:#d97706;font:700 .82rem 'Segoe UI',sans-serif;letter-spacing:.09em;text-transform:uppercase;margin-bottom:10px}
.center{text-align:center}.center .lead{margin-left:auto;margin-right:auto}
.search-demo{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px}
.search-card{background:#fff;border:1px solid #dfe5ee;border-radius:8px;padding:18px;text-align:left}
.search-pill{display:flex;align-items:center;gap:8px;background:#f4f6fa;border:1px solid #dfe5ee;border-radius:99px;padding:8px 14px;font:500 .88rem 'Segoe UI',sans-serif;color:#1a2436;margin-bottom:12px}
.search-verdict{font-size:.88rem;color:#5b6779;margin:0}
.search-verdict b.yes{color:#16a34a}.search-verdict b.no{color:#dc2626}
.step-num{width:36px;height:36px;border-radius:8px;background:#0b1220;color:#f59e0b;font:800 1rem 'Segoe UI',sans-serif;display:flex;align-items:center;justify-content:center;margin-bottom:12px}
.step .time{display:inline-block;margin-top:10px;font:700 .75rem 'Segoe UI',sans-serif;color:#d97706;background:rgba(245,158,11,.12);padding:4px 10px;border-radius:99px}
.tiers{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px;align-items:stretch}
.tier{background:#fff;border:1px solid #dfe5ee;border-radius:10px;padding:24px;display:flex;flex-direction:column;position:relative}
.tier.popular{border:2px solid #f59e0b;box-shadow:0 12px 28px rgba(245,158,11,.12)}
.pop-badge{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:#f59e0b;color:#0b1220;font:800 .7rem 'Segoe UI',sans-serif;letter-spacing:.06em;text-transform:uppercase;padding:5px 12px;border-radius:99px;white-space:nowrap}
.tier-name{font:800 1.15rem 'Segoe UI',sans-serif}
.tier-for{font-size:.85rem;color:#5b6779;margin:4px 0 14px}
.tier-pages{display:flex;align-items:baseline;gap:8px;margin-bottom:8px}
.tier-pages .n{font:800 2.6rem 'Segoe UI',sans-serif;letter-spacing:-.03em;line-height:1}
.tier-pages .l{font:600 .9rem 'Segoe UI',sans-serif;color:#5b6779}
.minigrid{display:grid;grid-template-columns:repeat(20,1fr);gap:2px;margin:12px 0 18px}
.minigrid i{display:block;aspect-ratio:1;border-radius:1px;background:#f59e0b}
.minigrid i.dim{background:#e3e8f0}
.price-row{display:flex;justify-content:space-between;gap:10px;font:600 .9rem 'Segoe UI',sans-serif;margin-bottom:6px}
.price-row .amt{font-weight:800}.price-row .amt small{font-weight:600;color:#5b6779}
.or-divider{text-align:center;font:700 .7rem 'Segoe UI',sans-serif;color:#5b6779;margin:8px 0;letter-spacing:.08em}
.tier ul{list-style:none;margin:14px 0 18px;flex:1}
.tier li{padding:6px 0 6px 22px;position:relative;font-size:.9rem;border-bottom:1px dashed #eef1f6}
.tier li:before{content:"\2713";position:absolute;left:0;color:#d97706;font-weight:800}
.tier li.hd{border:none;padding-top:12px;font:700 .78rem 'Segoe UI',sans-serif;color:#5b6779;text-transform:uppercase;letter-spacing:.04em}
.tier li.hd:before{content:""}
.tier .btn{text-align:center;margin-top:auto}
.own-note{margin-top:22px;font-size:.95rem;color:#5b6779;text-align:center}
.cmp-scroll{overflow-x:auto;margin-top:22px}
table.cmp{width:100%;border-collapse:collapse;font-size:.9rem;min-width:720px}
table.cmp th,table.cmp td{border:1px solid #dfe5ee;padding:12px 10px;text-align:left;vertical-align:top}
table.cmp th{background:#0b1220;color:#fff;font:700 .82rem 'Segoe UI',sans-serif}
table.cmp th.you,table.cmp td.you{background:#fff8ed}
table.cmp th.you{background:#f59e0b;color:#0b1220}
table.cmp .rowlbl{font-weight:700;font-family:'Segoe UI',sans-serif;background:#f4f6fa}
table.cmp .pos{color:#16a34a;font-weight:700}table.cmp .neg{color:#dc2626;font-weight:700}
@media(max-width:900px){.hero-home .hero-grid,.search-demo,.tiers{grid-template-columns:1fr}.hero-home{text-align:center}.hero-home .hero-sub{margin-left:auto;margin-right:auto}.hero-home .hero-ctas{justify-content:center}}
"""


HUB_DATA: list[tuple[str, str, str, list[str]]] = [
    (
        "website-build-packages",
        "Website Build Packages",
        "40, 80, and 120 page website builds for local service businesses that need more pages, more searches, and more jobs.",
        [
            "Local Launch 40 Pages",
            "Service Area Pro 80 Pages",
            "Market Dominator 120 Pages",
            "One-Time Ownership Buyout",
            "Setup Plus Monthly Plans",
            "Domain Content Ownership",
            "Days-Not-Months Launch",
            "Preview Before You Pay",
            "Quote Form On Every Page",
            "Contractor Website Packages",
        ],
    ),
    (
        "service-page-architecture",
        "Service Page Architecture",
        "Dedicated pages for the services, job types, questions, and proof that turn local searchers into quote requests.",
        [
            "Dedicated Service Pages",
            "High-Profit Job Landing Pages",
            "Emergency Same-Day Pages",
            "Seasonal Service Pages",
            "FAQ Buying Guide Pages",
            "Review Showcase Pages",
            "Project Photo Pages",
            "Competitor Gap Pages",
            "Service List Expansion",
            "How-Much-Does Pages",
        ],
    ),
    (
        "town-coverage-system",
        "Town Coverage System",
        "A service-area structure that covers real towns with useful local proof instead of thin doorway pages.",
        [
            "Home Town Service Area Pages",
            "Multi-Town Coverage",
            "Town Times Service Matrix",
            "Next Town Over Pages",
            "County-Wide Coverage",
            "Geo-Specific Quote CTAs",
            "Local Proof Blocks",
            "Service Area Map Pages",
            "Surrounding Suburb Pages",
            "Anti-Doorway Town Structure",
        ],
    ),
    (
        "local-seo-foundation",
        "Local SEO Foundation",
        "Technical and content foundations that help a larger local website get discovered, crawled, and converted.",
        [
            "Local Keyword Research",
            "On-Page SEO Architecture",
            "LocalBusiness Schema Markup",
            "Core Web Vitals Speed",
            "Mobile-First Builds",
            "Internal Linking Plans",
            "Title And Meta Systems",
            "Competitor SEO Gap Analysis",
            "Near Me Landing Optimization",
            "Technical SEO Checklist",
        ],
    ),
    (
        "google-business-profile",
        "Google Business Profile",
        "Google Business Profile setup and sync work that supports Maps visibility and sends searchers to deeper website pages.",
        [
            "GBP Setup",
            "Category Optimization",
            "Photo Strategy",
            "GBP Posts Cadence",
            "Review Request Setup",
            "Maps Visibility Basics",
            "NAP Consistency",
            "Services Attributes",
            "Local Pack Readiness",
            "GBP To Website Sync",
        ],
    ),
    (
        "lead-capture-tracking",
        "Lead Capture Tracking",
        "Forms, calls, routing, and reporting that show which pages create real local service leads.",
        [
            "Quote Forms Every Page",
            "Call Tracking Setup",
            "Lead Notification Routing",
            "Form To CRM Handoff",
            "Click-To-Call CTAs",
            "Thank-You Page Tracking",
            "Spam Protection Basics",
            "Multi-Location Lead Tags",
            "Page-Level Lead Attribution",
            "Monthly Lead Report",
        ],
    ),
    (
        "content-and-onboarding",
        "Content And Onboarding",
        "A questionnaire-first process that turns one business intake into professional pages without weeks of homework.",
        [
            "Business Questionnaire Intake",
            "Professional Page Writing",
            "Photo Integration",
            "Owner Review Workflow",
            "No Homework Content Model",
            "Brand Voice Capture",
            "FAQ Interview Process",
            "Service Scope Documentation",
            "Launch Checklist",
            "Revision Rounds",
        ],
    ),
    (
        "vertical-website-builds",
        "Vertical Website Builds",
        "Website factory patterns tuned for the local service trades that need calls, forms, photos, reviews, and town coverage.",
        [
            "Plumbing Website Builds",
            "Electrical Website Builds",
            "HVAC Website Builds",
            "Handyman Website Builds",
            "Roofing Website Builds",
            "Landscaping Website Builds",
            "Painting Website Builds",
            "Cleaning Services Websites",
            "Garage Door Websites",
            "Pest Control Websites",
        ],
    ),
    (
        "hosting-growth-plans",
        "Hosting Growth Plans",
        "Optional hosting, support, edit, reporting, and expansion plans for contractors who want the site managed after launch.",
        [
            "Managed Hosting Security",
            "Unlimited Content Edits",
            "Monthly Performance Reports",
            "Quarterly Page Expansion",
            "Monthly Page Expansion",
            "Review Request Automation",
            "Optional Hosting 49 Month",
            "Site Ownership Transfer",
            "Uptime Monitoring",
            "Post-Launch Support",
        ],
    ),
    (
        "migration-and-launch",
        "Migration And Launch",
        "Domain, DNS, migration, analytics, redirect, and launch QA support so a new 40/80/120 page site goes live cleanly.",
        [
            "Keep Existing Domain",
            "Fresh Domain Launch",
            "DNS Cutover Support",
            "Existing Site Migration",
            "Staging Preview Launch",
            "Go-Live QA Checklist",
            "404 Redirect Mapping",
            "Analytics Installation",
            "Search Console Setup",
            "Post-Launch Stabilization",
        ],
    ),
]

INDUSTRIES = [
    "Plumbing",
    "Electrical",
    "HVAC",
    "Handyman & Remodel",
    "Roofing",
    "Landscaping",
    "Painting",
    "Cleaning Services",
    "Garage Door",
    "Pest Control",
]


def slugify(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def child_blurb(hub_name: str, child_name: str) -> str:
    package_note = " built for 40/80/120-page local service websites"
    return (
        f"{child_name} planning and implementation from the {hub_name} track,"
        f"{package_note} that customers can own outright or run on a setup plus monthly plan."
    )


HUBS = [
    {
        "slug": slug,
        "name": name,
        "short": name,
        "blurb": blurb,
        "children": [(slugify(child), child, child_blurb(name, child)) for child in children],
    }
    for slug, name, blurb, children in HUB_DATA
]

assert len(HUBS) == 10
assert all(len(h["children"]) == 10 for h in HUBS)


def pfx(depth: int) -> str:
    return "" if depth == 0 else "../" * depth


def trunc(text: str, n: int = 155) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= n:
        return text
    return text[: n - 1].rsplit(" ", 1)[0].rstrip(" ,.;:") + "..."


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def head(title: str, desc: str, *, canonical: str | None = None) -> str:
    canon = canonical or ""
    canon_tag = (
        f'<link rel="canonical" href="{escape(canon)}">\n'
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:title" content="{escape(title)}">\n'
        f'<meta property="og:description" content="{escape(trunc(desc))}">\n'
        f'<meta property="og:url" content="{escape(canon)}">\n'
        f'<meta property="og:site_name" content="Near Me OS">\n'
        if canon
        else ""
    )
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="index, follow">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(trunc(desc))}">
{canon_tag}<style>
{FACTORY_CSS}
</style></head><body>
"""


def chrome(depth: int) -> str:
    p = pfx(depth)
    hub_dd = "".join(
        f'<a href="{p}{h["slug"]}/index.html">{escape(h["name"])}</a>' for h in HUBS
    )
    return f"""<div class="utility"><div class="wrap"><span>{escape(TAGLINE)}</span><span>{escape(HQ)} &middot; {escape(EMAIL)}</span></div></div>
<header class="main"><div class="wrap">
<a class="logo" href="{p}index.html" style="text-decoration:none">Near Me <span>OS</span><small>Local Service Website Factory</small></a>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>40/80/120-page websites for local service businesses</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Packages &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-near-me-os/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-near-me-os/index.html">About Near Me OS</a>
<a href="{p}about-near-me-os/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-near-me-os/verticals-we-serve/index.html">Industries We Serve</a>
</div></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li class="em"><a href="{p}book-a-call/index.html">Book a Free Call</a></li>
</ul></div></nav>
"""


def footer(depth: int) -> str:
    p = pfx(depth)
    hubs = "".join(
        f'<li><a href="{p}{h["slug"]}/index.html">{escape(h["short"])}</a></li>' for h in HUBS
    )
    return f"""<footer><div class="wrap"><div class="fcols">
<div><h4>Factory Pages</h4><ul>{hubs}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="{p}about-near-me-os/index.html">About Near Me OS</a></li>
<li><a href="{p}about-near-me-os/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-near-me-os/verticals-we-serve/index.html">Industries We Serve</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}book-a-call/index.html">Book a Free Call</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Ownership</h4><ul><li>You own the domain, content, and finished site files.</li><li>Operated by {escape(OPERATOR)}</li><li>{escape(ADDRESS)}</li></ul></div>
</div>
<div class="copy">Near Me OS &middot; {escape(OPERATOR)} &middot; {escape(HQ)} &middot; {escape(PHONE)}<br>
Copyright &copy; 2026. Near Me OS. All rights reserved.</div></div></footer>
</body></html>"""


def faqs(items: list[tuple[str, str]]) -> str:
    html = ['<section class="tint"><div class="wrap"><h2>Frequently Asked Questions</h2>']
    ents = []
    for q, a in items:
        html.append(
            f"<details><summary>{escape(q)}</summary><div><p>{escape(a)}</p></div></details>"
        )
        ents.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )
    html.append("</div></section>")
    html.append(
        '<script type="application/ld+json">'
        + json.dumps(
            {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ents},
            ensure_ascii=True,
        )
        + "</script>"
    )
    return "\n".join(html)


def form_shell(form_name: str = "Website Package Inquiry") -> str:
    opts = "".join(
        f'<option>{escape(p["name"])} - {escape(p["pages"])}</option>' for p in PRICING
    )
    industries = "".join(f"<option>{escape(i)}</option>" for i in INDUSTRIES)
    return f"""<div class="formbox">
<label>First Name</label><input type="text" name="first_name">
<label>Last Name</label><input type="text" name="last_name">
<label>Email</label><input type="email" name="email">
<label>Phone</label><input type="tel" name="phone">
<label>Business Type</label><select name="industry"><option>Please choose...</option>{industries}<option>Other Local Service Business</option></select>
<label>Package Interest</label><select name="package"><option>Please choose...</option>{opts}<option>Not sure yet</option></select>
<label>Current Website</label><input type="text" name="website" placeholder="https://">
<label>Message</label><textarea name="message" placeholder="Tell us your services, towns, and launch goal."></textarea><br><br>
<button class="btn">{escape(form_name)}</button>
<p style="margin-top:12px;font-size:12px;color:#5b6779">Form shell for launch wiring. Near Me OS uses one questionnaire to plan pages, services, towns, photos, and quote paths.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Near Me OS",
        "legalName": OPERATOR,
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "12 Sayre St",
            "addressLocality": "Elizabeth",
            "addressRegion": "NJ",
            "postalCode": "07208",
            "addressCountry": "US",
        },
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(data, ensure_ascii=True)
        + "</script>"
    )


def package_cards() -> str:
    cards = []
    for plan in PRICING:
        cards.append(
            f"""<div class="card"><h3>{escape(plan["name"])} - {escape(plan["pages"])}</h3>
<p><strong>{escape(plan["one_time"])}</strong> one-time ownership buyout, or <strong>{escape(plan["monthly"])}</strong>.</p>
<p>{escape(plan["fit"])}</p></div>"""
        )
    cards.append(
        """<div class="card"><h3>Optional Hosting - $49/mo</h3>
<p>One-time buyers can keep hosting with Near Me OS for $49/mo, or transfer the site to their own hosting after launch.</p></div>"""
    )
    return "".join(cards)


def home() -> str:
    hub_cards = []
    for h in HUBS:
        kids = "".join(
            f'<li><a href="{h["slug"]}/{s}/index.html">{escape(n)}</a></li>'
            for s, n, _ in h["children"][:3]
        )
        hub_cards.append(
            f'<div class="hubcard"><h3><a href="{h["slug"]}/index.html">{escape(h["name"])}</a></h3>'
            f"<p>{escape(h['blurb'])}</p><ul>{kids}</ul>"
            f'<a href="{h["slug"]}/index.html" style="font:600 13px \'Segoe UI\',sans-serif">'
            f"Explore {escape(h['short']).lower()} &rarr;</a></div>"
        )

    tiers = []
    tier_meta = [
        (
            "Local Launch",
            "One town, full service list",
            "40",
            "$2,495",
            "$495 + $249",
            False,
            [
                "A dedicated page for every service you offer",
                "Service-area pages for your home town",
                "Quote form on every single page",
                "Schema markup, mobile-first, fast-loading",
                "Google Business Profile setup",
                "hd:Monthly plan adds:",
                "Hosting, security & unlimited edits",
                "Monthly performance report",
            ],
        ),
        (
            "Service Area Pro",
            "Multiple towns, high-value jobs",
            "80",
            "$4,495",
            "$495 + $349",
            True,
            [
                "Everything in Local Launch, plus:",
                "Town × service pages across your service area",
                "Landing pages for highest-profit jobs",
                "FAQ & buying-guide pages",
                "Review & project-photo showcase pages",
                "hd:Monthly plan adds:",
                "Hosting, edits, monthly report",
                "Quarterly new-page expansion",
            ],
        ),
        (
            "Market Dominator",
            "Own your whole county",
            "120",
            "$6,495",
            "$495 + $499",
            False,
            [
                "Everything in Service Area Pro, plus:",
                "Full town × service coverage matrix",
                "Emergency & same-day service pages",
                "Seasonal and competitor-gap pages",
                "hd:Monthly plan adds:",
                "Hosting, edits, monthly report",
                "Monthly new-page expansion",
                "Review-request automation",
            ],
        ),
    ]
    for name, fit, pages, one_time, monthly, popular, bullets in tier_meta:
        lis = []
        for b in bullets:
            if b.startswith("hd:"):
                lis.append(f'<li class="hd">{escape(b[3:])}</li>')
            else:
                lis.append(f"<li>{escape(b)}</li>")
        pop = ' popular' if popular else ""
        badge = '<span class="pop-badge">Most Popular</span>' if popular else ""
        tiers.append(
            f"""<div class="tier{pop}">{badge}
<div class="tier-name">{escape(name)}</div>
<div class="tier-for">{escape(fit)}</div>
<div class="tier-pages"><span class="n">{escape(pages)}</span><span class="l">pages</span></div>
<div class="minigrid" data-count="{escape(pages)}"></div>
<div class="price-row"><span class="lbl">Own it outright</span><span class="amt">{escape(one_time)} <small>one-time</small></span></div>
<div class="or-divider"><span>OR</span></div>
<div class="price-row alt"><span class="lbl">Setup + monthly</span><span class="amt">{escape(monthly)}<small>/mo</small></span></div>
<ul>{''.join(lis)}</ul>
<a class="btn" href="book-a-call/index.html">Start with {escape(pages)} Pages</a>
</div>"""
        )

    desc = (
        "Near Me OS builds 40, 80, or 120-page websites for local service businesses — "
        "a page for every service in every town you serve. You own everything. Live in days."
    )
    return (
        head(
            "Near Me OS — More Pages. More Searches. More Jobs.",
            desc,
            canonical=f"{BASE}/",
        )
        + chrome(0)
        + f"""
<div class="hero hero-home"><div class="wrap hero-grid">
<div>
<span class="eyebrow">Near Me OS · Websites for Local Service Businesses</span>
<h1>Your competitor has 5 pages on Google.<br>You're about to have <em>120</em>.</h1>
<p class="hero-sub">Homeowners don't search "handyman" — they search <b>"drywall repair in your town."</b> Google sends that call to whoever has a page for it. We build you a page for every service you offer, in every town you serve.</p>
<div class="hero-ctas">
<a class="btn" href="#pricing">See Plans &amp; Pricing</a>
<a class="btn ghost" href="#how">How It Works</a>
<a class="btn alt" href="book-a-call/index.html">Book a Free Call</a>
</div>
<p class="hero-note"><strong>You own everything</strong> — domain, content, site. Live in days, not months.</p>
</div>
<div class="pagegrid-card">
<div class="pagegrid-title">Every square = a page that can win a search</div>
<div class="pg" id="heroGrid"></div>
<p class="pg-caption"><b>Their site</b> (gray) vs. <b>your site</b> (gold)</p>
</div>
</div></div>

<section class="tint" id="problem"><div class="wrap center">
<div class="kicker">Why size wins</div>
<h2>Google matches searches to pages — not to businesses.</h2>
<p class="lead">Every job you do is a search someone types. If your site doesn't have a page answering that exact search in that exact town, the competitor who does gets the call.</p>
<div class="search-demo">
<div class="search-card"><div class="search-pill">water heater replacement [your town]</div>
<p class="search-verdict">Typical 5-page site: <b class="no">no page = invisible</b><br>Your site: <b class="yes">dedicated page, quote form included</b></p></div>
<div class="search-card"><div class="search-pill">deck repair near me</div>
<p class="search-verdict">Typical 5-page site: <b class="no">buried in a services list</b><br>Your site: <b class="yes">full page with photos &amp; FAQs</b></p></div>
<div class="search-card"><div class="search-pill">emergency drywall patch [next town over]</div>
<p class="search-verdict">Typical 5-page site: <b class="no">wrong town, no page</b><br>Your site: <b class="yes">town-specific service page</b></p></div>
</div></div></section>

<section id="how"><div class="wrap center">
<div class="kicker">How it works</div>
<h2>You answer questions once. We build everything.</h2>
<p class="lead">No homework, no writing, no "send us content" limbo. The Near Me OS engine does what agencies do by hand — which is why we deliver in days at a fraction of agency prices.</p>
<div class="steps" style="text-align:left;margin-top:28px">
<div class="card"><div class="step-num">1</div><h3>Tell us about your business</h3><p>One guided questionnaire: your services, your towns, your photos, how you want the phone answered.</p><span class="time">~45 minutes of your time</span></div>
<div class="card"><div class="step-num">2</div><h3>We build your entire site</h3><p>Every service page and town page — professionally written with schema, speed, and mobile structure Google rewards. You review before launch.</p><span class="time">Days — not months</span></div>
<div class="card"><div class="step-num">3</div><h3>Launch, track, own</h3><p>Live on your domain with a quote form on every page and lead tracking. It's all yours from day one.</p><span class="time">You own 100% of it</span></div>
</div></div></section>

<section class="tint" id="pricing"><div class="wrap">
<div class="center">
<div class="kicker">Plans &amp; pricing</div>
<h2>Pick your footprint. Pay once — or start small and go monthly.</h2>
<p class="lead">Every tier includes the same build quality. The difference is how much of your market you cover.</p>
</div>
<div class="tiers">{''.join(tiers)}</div>
<p class="own-note"><b>Every plan:</b> you own the domain, the content, and the site — in writing. Monthly plans are 12 months, then month-to-month. One-time buyers: optional hosting &amp; updates, $49/mo.</p>
</div></section>

<section id="packages"><div class="wrap">
<div class="center"><div class="kicker">Factory map</div>
<h2>Explore the full Near Me OS package library</h2>
<p class="lead">Same navigation as every other page — packages, industries, and launch paths under one factory.</p></div>
<div class="cols3" style="margin-top:28px">{''.join(hub_cards)}</div>
</div></section>

<section class="tint" id="compare"><div class="wrap">
<div class="center"><div class="kicker">The honest comparison</div>
<h2>Where the money goes everywhere else</h2></div>
<div class="cmp-scroll"><table class="cmp">
<thead><tr><th></th><th>DIY Builder<br><small>(Wix / Squarespace)</small></th><th>Traditional Agency</th><th>Big Marketing Firms</th><th class="you">Near Me OS</th></tr></thead>
<tbody>
<tr><td class="rowlbl">Upfront cost</td><td>$0–$500 + 20–40 hrs of your time</td><td>$5,000–$10,000+</td><td>$0–$3,000</td><td class="you">$495 – $6,495</td></tr>
<tr><td class="rowlbl">Ongoing cost</td><td>$20–$50/mo</td><td>Hourly for every change</td><td><span class="neg">$1,500–$5,000/mo</span></td><td class="you">$0 – $499/mo</td></tr>
<tr><td class="rowlbl">Pages you end up with</td><td>5–10 (you write them)</td><td>10–20</td><td>10–30</td><td class="you">40 / 80 / 120</td></tr>
<tr><td class="rowlbl">Time to launch</td><td>Whenever you finish it</td><td>2–4 months</td><td>4–8 weeks</td><td class="you"><span class="pos">Days</span></td></tr>
<tr><td class="rowlbl">Who owns the site?</td><td>You (locked to their platform)</td><td>Usually you</td><td><span class="neg">Often them</span></td><td class="you"><span class="pos">You. Always. In writing.</span></td></tr>
</tbody></table></div>
</div></section>
"""
        + faqs(
            [
                (
                    "Why would I need 80 or 120 pages?",
                    "You don't read them — Google does. Each page answers one specific search. More pages means you're entered in more races. Your workload is identical at every tier: one questionnaire.",
                ),
                (
                    "Do I have to write anything?",
                    "No. You answer questions about your business once (about 45 minutes). We produce every page. You review and approve before anything goes live.",
                ),
                (
                    "Who owns the website?",
                    "You do — domain, content, design, everything, whether you paid one-time or monthly. It's written into the agreement.",
                ),
                (
                    "Will it guarantee me leads?",
                    "No honest company guarantees rankings. We guarantee the infrastructure: pages built the way Google rewards, a quote form on every one, and tracking so you can see which pages produce calls.",
                ),
                (
                    "What if I already have a website?",
                    "We can build on your existing domain or launch fresh. If your current site is under 10 pages, you now know why the phone is quiet.",
                ),
            ]
        )
        + f"""
<div class="ctastrip" id="contact"><div class="wrap">
<h2>The next "near me" search in your town is going somewhere.</h2>
<p style="max-width:720px;margin:0 auto 18px;color:#cbd5e1">One recovered job a month pays for the site. Tell us your services and towns — we'll show you a live preview before you pay a dollar.</p>
<a class="btn" href="book-a-call/index.html">Book a Free 15-Minute Call</a>
<a class="btn alt" href="tel:{PHONE_TEL}" style="margin-left:8px">Call {escape(PHONE)}</a>
<p style="margin-top:14px;font-size:.9rem;color:#94a3b8"><a href="mailto:{EMAIL}" style="color:#f4f6fa">{escape(EMAIL)}</a></p>
</div></div>
<script>
(function(){{
  var g=document.getElementById('heroGrid');
  if(g){{for(var i=0;i<120;i++){{var s=document.createElement('i');if(i<6)s.classList.add('dim');g.appendChild(s);}}}}
  document.querySelectorAll('.minigrid').forEach(function(el){{
    var lit=parseInt(el.getAttribute('data-count'),10)||0;
    for(var i=0;i<120;i++){{var s=document.createElement('i');if(i>=lit)s.classList.add('dim');el.appendChild(s);}}
  }});
}})();
</script>
"""
        + org_schema()
        + footer(0)
    )


def hub_page(h: dict) -> str:
    cards = "".join(
        f'<div class="gcard"><h3><a href="{s}/index.html">{escape(n)}</a></h3><p>{escape(b)}</p><span class="tag">SVC-CHILD</span></div>'
        for s, n, b in h["children"]
    )
    return (
        head(
            f"{h['name']} | Near Me OS",
            f"{h['name']} from Near Me OS - {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} for 40/80/120-page local websites</h2>
<p class="lead">{escape(h["blurb"])} Near Me OS builds the service pages, town pages, quote paths, and launch assets together so the site can go live in days, not months.</p>
<p><a class="btn" href="../book-a-call/index.html">Book a Free Call</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Pages</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>How this fits the Near Me OS factory</h2>
<ul class="checks">
<li>Choose Local Launch, Service Area Pro, or Market Dominator based on page depth.</li>
<li>Complete one questionnaire for services, towns, photos, reviews, FAQs, and offer details.</li>
<li>Preview the finished structure before you pay the full one-time buyout or monthly plan.</li>
<li>Own the domain, written content, page structure, and finished site files.</li>
<li>Add optional $49/mo hosting, monthly edits, reporting, and page expansion after launch.</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What is included in {h['name']}?", h["blurb"]),
                (
                    "How fast can pages launch?",
                    "Near Me OS is built for days-not-months launches after the questionnaire, photos, service list, and town coverage are approved.",
                ),
                (
                    "Do we own the website?",
                    "Yes. One-time buyers own the content, domain, page structure, and finished site files. Optional hosting is available for $49/mo.",
                ),
            ]
        )
        + footer(1)
    )


def leaf_page(h: dict, child: tuple[str, str, str]) -> str:
    slug, name, blurb = child
    related = "".join(
        f'<div class="gcard"><h3><a href="../{s}/index.html">{escape(n)}</a></h3></div>'
        for s, n, _ in h["children"]
        if s != slug
    )
    return (
        head(f"{name} | Near Me OS", f"{name} from Near Me OS - {blurb}")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(name)} for local service websites that need more search coverage.</h2>
<p class="lead">{escape(blurb)} It is scoped for contractors and local service businesses that want a larger website without a months-long agency process.</p>
<p><a class="btn" href="../../book-a-call/index.html">Book a Free Call</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>What {escape(name)} helps create</h2>
<ul class="checks">
<li>More relevant pages for high-intent service and town searches.</li>
<li>Quote forms and click-to-call CTAs on every important page.</li>
<li>Local proof blocks, service details, FAQs, and review-ready page sections.</li>
<li>A site structure that supports 40, 80, or 120 pages without thin duplication.</li>
<li>Ownership clarity so you can keep hosting with us or transfer the site later.</li>
</ul></div></section>
<section><div class="wrap"><h2>Built from one questionnaire, then reviewed before launch</h2>
<p>Near Me OS collects your services, towns, job types, offers, photos, reviews, and preferences once. We use that intake to draft the page map and content, then you review the site before final launch or ownership buyout.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Why this is different from a small brochure site</h2>
<div class="vs">
<div class="col bad"><h3>Typical small website limitations</h3><ul>
<li>Five to ten pages trying to cover every service and town.</li>
<li>Generic copy that does not match how customers search.</li>
<li>Quote forms hidden on one contact page.</li>
<li>No plan for expansion after launch.</li>
</ul></div>
<div class="col good"><h3>Near Me OS factory approach</h3><ul>
<li>40/80/120-page packages mapped to services, towns, and jobs.</li>
<li>Professional page writing from your business questionnaire.</li>
<li>Quote forms, calls, and tracking paths across the site.</li>
<li>Optional hosting, edits, reports, and page expansion.</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Want {escape(name.lower())} in your build?</h2>
<p style="max-width:720px;margin:0 auto 16px">Book a free call and we will map the right page count, ownership option, and launch path for your service area.</p>
<a class="btn" href="../../book-a-call/index.html">Book a Free Call</a> <a class="btn alt" href="../../contact/index.html">Contact Near Me OS</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"Can {name.lower()} be part of a 40-page site?",
                    "Yes when it fits the page map. Local Launch starts at 40 pages, Service Area Pro at 80 pages, and Market Dominator at 120 pages.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Pricing depends on the selected package: Local Launch is $2,495 or $495 + $249/mo; Service Area Pro is $4,495 or $495 + $349/mo; Market Dominator is $6,495 or $495 + $499/mo.",
                ),
                (
                    "Do I have to keep hosting with Near Me OS?",
                    "No. One-time buyers can use optional $49/mo hosting or transfer the finished site files to their own hosting.",
                ),
            ]
        )
        + f'<section><div class="wrap"><h2>Related {escape(h["short"])} Pages</h2><div class="grid">{related}</div></div></section>'
        + footer(2)
    )


def cta_page(slug: str, title: str, h2: str, lead: str, button: str) -> str:
    steps = {
        "book-a-call": [
            ("Pick the package range", "We compare 40, 80, and 120-page paths against your services and towns."),
            ("Review ownership options", "Choose one-time ownership buyout or setup plus monthly plan."),
            ("Leave with a next step", "You get the questionnaire path, pricing fit, and launch expectations."),
        ],
        "request-a-proposal": [
            ("Tell us your market", "Share services, towns, competitors, current website, and growth goals."),
            ("Get a scoped page map", "We recommend Local Launch, Service Area Pro, or Market Dominator."),
            ("Decide with numbers", "Pricing, ownership, hosting, and launch timing are put in writing."),
        ],
        "contact": [
            ("Call, email, or use the form", "Reach Near Me OS directly for package, launch, or support questions."),
            ("Confirm your fit", "We serve local service businesses that need more useful pages online."),
            ("Move into onboarding", "When ready, the one-time questionnaire starts the build."),
        ],
    }[slug]
    step_cards = "".join(
        f'<div class="card"><h3>{escape(title_text)}</h3><p>{escape(body)}</p></div>'
        for title_text, body in steps
    )
    return (
        head(title, lead)
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h2)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:29px">{escape(h2)}</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">{step_cards}</div>{form_shell(button)}</div></section>
<section class="tint"><div class="wrap"><h2>Package Pricing Reference</h2><div class="cols3">{package_cards()}</div></div></section>
<section><div class="wrap"><h2>Contact Details</h2>
<p><strong>Near Me OS</strong><br>Operated by {escape(OPERATOR)}<br>Headquarters: {escape(ADDRESS)}<br>Phone: <a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><br>Email: <a href="mailto:{EMAIL}">{escape(EMAIL)}</a></p>
</div></section>
"""
        + (org_schema() if slug == "contact" else "")
        + footer(1)
    )


def about_page() -> str:
    return (
        head(
            "About Near Me OS | Elizabeth, NJ",
            "Near Me OS builds 40, 80, and 120-page websites for local service businesses.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About Near Me OS</h2>
<p class="lead">Near Me OS helps local service businesses publish larger, useful websites built around services, towns, job types, and quote paths. The company is operated by {escape(OPERATOR)} from {escape(ADDRESS)}.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(TAGLINE)}</h2>
<p>Most contractors are sold small brochure sites, then expected to compete in search with a handful of pages. Near Me OS packages the planning, writing, structure, forms, launch support, and ownership model needed for 40, 80, and 120-page local service websites.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="verticals-we-serve/index.html">Industries we serve &rarr;</a></p>
</div></section>
<section><div class="wrap"><h2>Package Options</h2><div class="cols3">{package_cards()}</div></div></section>
"""
        + faqs(
            [
                (
                    "Who operates Near Me OS?",
                    f"Near Me OS is operated by {OPERATOR}, headquartered at {ADDRESS}.",
                ),
                (
                    "What does Near Me OS sell?",
                    "40-page Local Launch, 80-page Service Area Pro, and 120-page Market Dominator website packages for local service businesses.",
                ),
                (
                    "Do clients own the site?",
                    "Yes. One-time buyers own the domain, content, page structure, and finished site files.",
                ),
            ]
        )
        + org_schema()
        + footer(1)
    )


def why_page() -> str:
    return (
        head("Why Choose Near Me OS", "Why local service businesses choose Near Me OS for larger owned websites.")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose Near Me OS</h2>
<p class="lead">A website factory for contractors who need more than a small brochure site and want clear ownership after launch.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>More pages from the start</h3><p>40, 80, and 120-page packages give services, towns, FAQs, proof, and quote paths room to work.</p></div>
<div class="card"><h3>Ownership built in</h3><p>One-time buyers own the domain, content, structure, and finished files. Optional hosting is $49/mo.</p></div>
<div class="card"><h3>Questionnaire once</h3><p>One intake captures the business details needed for page maps, writing, CTAs, and launch QA.</p></div>
<div class="card"><h3>Preview before you pay</h3><p>Review the structure and direction before the full buyout or monthly plan is finalized.</p></div>
<div class="card"><h3>Built for local services</h3><p>Plumbing, electrical, HVAC, roofing, landscaping, cleaning, pest control, and related trades.</p></div>
<div class="card"><h3>Elizabeth HQ</h3><p>{escape(OPERATOR)} accountability with remote deployment for local service businesses nationwide.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready to compare packages?</h2>
<a class="btn" href="../../book-a-call/index.html">Book a Free Call</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + footer(2)
    )


def verticals_page() -> str:
    ind = "".join(
        f'<div class="gcard"><h3>{escape(i)}</h3><p>40/80/120-page website planning tuned to {escape(i.lower())} services, towns, photos, FAQs, and quote requests.</p></div>'
        for i in INDUSTRIES
    )
    return (
        head("Industries We Serve | Near Me OS", "Industries served by Near Me OS local service website packages.")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Industries</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Industries We Serve</h2>
<p class="lead">Near Me OS focuses on local service businesses where service pages, town pages, calls, quote forms, photos, reviews, and seasonal demand matter.</p>
<div class="grid">{ind}</div></div></section>
"""
        + footer(2)
    )


def write_inventory(urls: list[str]) -> None:
    rows = [
        [
            "url",
            "type_id",
            "parent_url",
            "target_keyword",
            "menu_location",
            "source_intake_field",
            "booking_type",
        ],
        ["/", "HOME", "", "near me os", "logo/home", "A1,A6,A10", ""],
        [
            "/about-near-me-os/",
            "COMP-HUB",
            "/",
            "about near me os",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-near-me-os/why-choose-us/",
            "COMP-CHILD",
            "/about-near-me-os/",
            "why choose near me os",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-near-me-os/verticals-we-serve/",
            "COMP-CHILD",
            "/about-near-me-os/",
            "local service website industries",
            "About menu",
            "D1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact near me os",
            "Contact menu",
            "A3,A4,A5,I1",
            "Contact Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PROPOSAL",
            "/",
            "near me os proposal",
            "nav utility",
            "I1",
            "Request for Proposal",
        ],
        [
            "/book-a-call/",
            "FORM-CONSULT",
            "/",
            "book a free call near me os",
            "nav highlighted",
            "I1",
            "Consultation Request",
        ],
    ]
    for h in HUBS:
        rows.append(
            [
                f"/{h['slug']}/",
                "SVC-HUB",
                "/",
                h["name"].lower(),
                "Packages menu",
                "B (category)",
                "",
            ]
        )
        for s, n, _ in h["children"]:
            rows.append(
                [
                    f"/{h['slug']}/{s}/",
                    "SVC-CHILD",
                    f"/{h['slug']}/",
                    n.lower(),
                    "Packages menu > hub grid",
                    "B row",
                    "Book a Free Call",
                ]
            )
    with (ROOT / "NEARMEOS-PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def write_questionnaire() -> None:
    hub_slugs = " | ".join(h["slug"] for h in HUBS)
    price_lines = "\n".join(
        f"- {p['name']} ({p['pages']}): {p['one_time']} one-time or {p['monthly']}"
        for p in PRICING
    )
    industry_lines = ", ".join(INDUSTRIES)
    write(
        ROOT / "NEARMEOS-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire - Near Me OS Factory Pages

Home page and factory pages share one chrome (utility bar, logo/phone, Packages nav, footer).

## A - Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | Near Me OS (operated by Race Computer Services, LLC) | product landing |
| A2 domain | nearmeos.io | product landing |
| A3 phone | {PHONE} | product landing |
| A4 email | {EMAIL} | product landing |
| A5 address | {ADDRESS} | product landing |
| A6 trade | 40/80/120-page websites for local service businesses | product landing |
| A10 value_proposition | More pages, more searches, more jobs; clients own the domain, content, page structure, and finished site files | product landing |
| A11 tagline | {TAGLINE} | product landing |
| A12 competitor_type | Small brochure website agencies, generic template providers, rented landing-page funnels | product positioning |

## B - Product packages and services
{price_lines}
- Optional hosting for one-time buyers: $49/mo
- Questionnaire once; page map, writing, forms, and launch QA are built from that intake.
- Preview before full payment; one-time ownership buyout or setup plus monthly plans.

## C - Gate 1 taxonomy
- Hubs: {len(HUBS)}
- SVC-CHILD pages: {sum(len(h['children']) for h in HUBS)}
- Hub slugs: {hub_slugs}
- Full URL map: `NEARMEOS-PAGE-INVENTORY.csv`

## D - Industries
{industry_lines}

## E - Forms and CTAs
- Primary CTA: `book-a-call` (FORM-CONSULT)
- Secondary CTA: `request-a-proposal`
- Company/contact CTA: `contact`
- Quote form message appears throughout page copy; final form destination to be wired at launch.

## F - Indexing and launch
- Factory pages use `index, follow`.
- `robots.txt` allows crawling and points to the sitemap.
- `netlify.toml` contains security headers only; no X-Robots-Tag indexing block.
- Home is generated with the same chrome as hub/leaf pages so navigation is seamless site-wide.
""",
    )


def write_static_files(urls: list[str]) -> None:
    body = "".join(
        f"<url><loc>{BASE}/</loc></url>" if u == "/" else f"<url><loc>{BASE}{u}</loc></url>"
        for u in urls
    )
    write(
        ROOT / "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + body
        + "</urlset>\n",
    )
    write(ROOT / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    write(
        ROOT / "netlify.toml",
        """[build]
  publish = "."

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "SAMEORIGIN"
""",
    )
    write(ROOT / "_redirects", "/*    /404.html  404\n")


def cleanup_generated_site() -> None:
    keep_names = {".git", ".gitignore", "scripts", "NEARMEOS-LANDING.md"}
    for child in list(ROOT.iterdir()):
        if child.name in keep_names:
            continue
        if child.name.startswith("."):
            continue
        if child.is_file() or child.is_symlink():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)


def main() -> None:
    urls = ["/"]
    cleanup_generated_site()

    write(ROOT / "index.html", home())

    for h in HUBS:
        write(ROOT / h["slug"] / "index.html", hub_page(h))
        urls.append(f"/{h['slug']}/")
        for child in h["children"]:
            write(ROOT / h["slug"] / child[0] / "index.html", leaf_page(h, child))
            urls.append(f"/{h['slug']}/{child[0]}/")

    write(ROOT / "about-near-me-os" / "index.html", about_page())
    urls.append("/about-near-me-os/")
    write(ROOT / "about-near-me-os" / "why-choose-us" / "index.html", why_page())
    urls.append("/about-near-me-os/why-choose-us/")
    write(ROOT / "about-near-me-os" / "verticals-we-serve" / "index.html", verticals_page())
    urls.append("/about-near-me-os/verticals-we-serve/")

    for slug, title, h2, lead, button in [
        (
            "contact",
            "Contact Us | Near Me OS",
            "Contact Near Me OS",
            "Call, email, or send a message about 40/80/120-page website packages for your local service business.",
            "Contact Near Me OS",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | Near Me OS",
            "Request a Near Me OS Proposal",
            "Tell us your services, towns, and current website. We will recommend Local Launch, Service Area Pro, or Market Dominator with pricing in writing.",
            "Request a Proposal",
        ),
        (
            "book-a-call",
            "Book a Free Call | Near Me OS",
            "Book a Free Call",
            "Talk through your service area, page count, ownership option, and launch timing before you commit.",
            "Book a Free Call",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead, button))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | Near Me OS", "Page not found.")
        + chrome(0)
        + """
<section style="padding:72px 0"><div class="wrap"><h2 style="font-size:28px">Page not found</h2>
<p class="lead">That URL is not in the Near Me OS factory map. Head home or book a free call.</p>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn alt" href="book-a-call/index.html">Book a Free Call</a></p>
</div></section>
"""
        + footer(0),
    )

    write_static_files(urls)
    write_inventory(urls)
    write_questionnaire()

    pages = list(ROOT.rglob("index.html"))
    inventory_children = 0
    with (ROOT / "NEARMEOS-PAGE-INVENTORY.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["type_id"] == "SVC-CHILD":
                inventory_children += 1

    print(f"Index pages on disk: {len(pages)}")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)}")
    print(f"SVC-CHILD inventory rows: {inventory_children}")
    print("Home uses shared factory chrome: yes")


if __name__ == "__main__":
    main()
