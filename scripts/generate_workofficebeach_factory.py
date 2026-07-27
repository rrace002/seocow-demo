#!/usr/bin/env python3
"""Generate the Work Office at the Beach NearMe OS staging factory site.

Gate target:
- 7 service hubs x 10 children = 70 SVC-CHILD index pages
- Hub landing pages are root-level .html pages so the generated index.html count stays at 77
- Shared chrome, noindex staging controls, inventory, notes, questionnaire, and Netlify files
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://workofficeatthebeach.com"  # [confirm]
BRAND = "Work Office at the Beach"
SHORT_BRAND = "Work Office Beach"
PHONE = "(305) 555-0148 [confirm]"
PHONE_DISPLAY = "(305) 555-0148"
PHONE_TEL = "+13055550148"
EMAIL = "hello@workofficeatthebeach.com"  # [confirm]
ADDRESS = "South Beach, Miami Beach, FL 33139 [confirm] - street TBD"
LOCATION = "South Beach, Miami Beach, FL"
TAGLINE = "Work near the water. Enjoy the scenery."
OPERATOR_NOTE = "Race Computer Services factory staging defaults where NAP unconfirmed"
STAGING_BANNER = (
    "STAGING PREVIEW — Work Office at the Beach factory build · South Beach Miami FL · "
    "content pending owner review"
)


FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
:root{--teal:#0e7490;--deep:#0c4a6e;--sand:#f8f1e7;--gold:#d4a373;--coral:#e11d48;--ink:#0f2530;--muted:#647984;--line:#d7e5e7;--foam:#eef9fa;--white:#fff}
body{font-family:"Source Sans 3",Arial,Helvetica,sans-serif;color:var(--ink);line-height:1.68;background:#fff}
h1,h2,h3,h4,.logo-name{font-family:"Fraunces",Georgia,"Times New Roman",serif}
a{color:var(--deep);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1140px;margin:0 auto;padding:0 22px}
.stage{background:repeating-linear-gradient(-45deg,#083344 0 11px,#0c4a6e 11px 22px);color:#fff;font:800 11.5px "Source Sans 3",sans-serif;letter-spacing:.055em;text-transform:uppercase;text-align:center;padding:9px 12px}
.utility{background:var(--deep);color:#dff8fb;font-size:12.5px;padding:7px 0}
.utility .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}.utility a{color:#fff}
header.main{background:#fff;border-bottom:1px solid var(--line);position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-top:18px;padding-bottom:18px}
.logo{display:inline-flex;align-items:center;gap:13px;color:var(--deep);font-weight:800;text-decoration:none}
.logo-mark{width:54px;height:54px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(145deg,var(--teal),var(--deep));color:#fff;font:900 1.05rem "Fraunces",serif;letter-spacing:.04em;box-shadow:0 7px 18px rgba(14,116,144,.20);flex:none}
.logo-name{display:block;font-size:1.38rem;line-height:1.08;color:var(--deep)}
.logo small{display:block;color:var(--muted);font:800 10.5px "Source Sans 3",sans-serif;letter-spacing:.14em;text-transform:uppercase;margin-top:4px}
.phone-cta{text-align:right}.phone-cta a{font:900 1.25rem "Source Sans 3",sans-serif;color:var(--deep)}.phone-cta small{display:block;color:var(--muted);font-size:12px;margin-top:2px}
nav.nav{background:#fff;border-bottom:1px solid var(--line);position:relative;z-index:45}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap;align-items:center;width:100%}
nav.nav>.wrap>ul>li{position:relative}
nav.nav>div.wrap>ul>li>a{display:block;color:var(--deep);padding:13px 15px;font-size:14px;font-weight:900}
nav.nav>div.wrap>ul>li>a:hover{background:var(--foam);color:var(--teal);text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:300px;box-shadow:0 14px 28px rgba(12,74,110,.18);border:1px solid var(--line);border-top:4px solid var(--gold);z-index:60}
nav.nav .dd a{display:block;color:var(--ink);padding:10px 15px;font-size:13.5px;font-weight:700;border-bottom:1px solid var(--line);background:#fff}
nav.nav .dd a:hover{background:var(--foam);color:var(--deep);text-decoration:none}
.nav .em{margin-left:auto}.nav .em>a{background:var(--teal);color:#fff;margin:6px 0 6px 8px;padding:9px 18px;border-radius:999px}.nav .em>a:hover{background:var(--deep);color:#fff}
.hero{position:relative;background:radial-gradient(circle at 18% 22%,rgba(212,163,115,.28),transparent 32%),radial-gradient(circle at 82% 28%,rgba(14,116,144,.26),transparent 38%),linear-gradient(135deg,#063947 0%,#0c4a6e 54%,#0e7490 100%);color:#fff;padding:82px 0 70px;overflow:hidden}
.hero:before{content:"";position:absolute;inset:0;background:linear-gradient(120deg,rgba(255,255,255,.14) 0 1px,transparent 1px 24px),radial-gradient(circle at 50% 105%,rgba(248,241,231,.28),transparent 34%);opacity:.8;pointer-events:none}
.hero .wrap{position:relative;z-index:1}.hero h1{font-size:clamp(2.25rem,5vw,4rem);line-height:1.05;max-width:930px;margin-bottom:18px}.hero p{max-width:780px;color:#e8fbff;font-size:1.12rem}
.eyebrow,.kicker{display:inline-flex;align-items:center;gap:12px;color:var(--gold);font:900 12px "Source Sans 3",sans-serif;letter-spacing:.14em;text-transform:uppercase;margin-bottom:14px}
.eyebrow:before,.kicker:before{content:"";display:inline-block;width:30px;height:2px;background:currentColor;flex:none}
.hero-ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:27px}
.btn{display:inline-block;background:var(--teal);color:#fff;font:900 14px "Source Sans 3",sans-serif;padding:13px 24px;border-radius:999px;border:0;cursor:pointer;box-shadow:0 8px 18px rgba(14,116,144,.16)}
.btn:hover{background:var(--deep);color:#fff;text-decoration:none}.btn.alt{background:var(--gold);color:#173241}.btn.alt:hover{background:#bd8d5f;color:#fff}.btn.ghost{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.58)}.btn.ghost:hover{background:rgba(255,255,255,.12)}
section{padding:48px 0}section.tint{background:var(--foam)}section.cream{background:var(--sand)}
section h2{font-size:clamp(1.72rem,3vw,2.28rem);color:var(--deep);line-height:1.18;margin-bottom:15px}section p{margin-bottom:14px;font-size:16.5px}.lead{font-size:18px;color:#304e58;max-width:850px}
.crumb{font-size:12.5px;color:var(--muted);padding:15px 0 0}.crumb a{color:var(--muted)}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:18px;margin-top:22px}
.card,.gcard,.hubcard{background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:0 5px 18px rgba(12,74,110,.07)}.card{padding:25px}.gcard,.hubcard{padding:22px;border-top:5px solid var(--teal)}
.card h3,.gcard h3,.hubcard h3{font-size:18px;color:var(--deep);margin-bottom:8px}.gcard h3 a,.hubcard h3 a{color:var(--deep)}
.gcard p,.hubcard p{font-size:14.5px;color:var(--muted);margin:0}.tag{display:inline-block;margin-top:12px;font:900 10.5px "Source Sans 3",sans-serif;letter-spacing:.09em;text-transform:uppercase;color:var(--teal)}
.feature{border-left:5px solid var(--gold);background:#fff;padding:24px;border-radius:14px;border-top:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-top:24px}.stat{background:#fff;border:1px solid var(--line);border-top:4px solid var(--gold);padding:20px;text-align:center;border-radius:14px}.stat b{display:block;color:var(--deep);font-size:26px;line-height:1.1}.stat span{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;font-weight:900}
ul.checks{list-style:none;margin:10px 0}ul.checks li{padding:7px 0 7px 29px;position:relative}ul.checks li:before{content:"";position:absolute;left:2px;top:17px;width:14px;height:3px;background:var(--teal);border-radius:3px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin:22px 0}.stepnum{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--deep);color:#fff;font-weight:900;margin-bottom:12px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-top:18px}.vs .col{padding:24px}.vs .col.good{background:var(--sand)}.vs .col.bad{background:#fff}
.formbox{background:#fff;border:1px solid var(--line);border-top:5px solid var(--teal);border-radius:14px;padding:26px;max-width:720px}.formbox.highlight{border-top-color:var(--coral);box-shadow:0 10px 28px rgba(225,29,72,.10)}
.formbox label{display:block;font:900 12.5px "Source Sans 3",sans-serif;color:var(--muted);margin:12px 0 4px}.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #b8cbd0;border-radius:8px;font:14px "Source Sans 3",sans-serif}.formbox textarea{min-height:100px}
details{border:1px solid var(--line);border-radius:10px;margin-bottom:10px;background:#fff}details summary{cursor:pointer;padding:14px 18px;font:900 15px "Source Sans 3",sans-serif;color:var(--deep);list-style:none}details summary:before{content:"+ ";color:var(--teal);font-weight:900}details[open] summary:before{content:"- "}details div{padding:0 18px 16px;font-size:15.5px}
.ctastrip{background:linear-gradient(135deg,var(--deep),var(--teal));color:#fff;text-align:center;padding:40px 0}.ctastrip h2{color:#fff}.ctastrip p{color:#e2fbff;max-width:780px;margin-left:auto;margin-right:auto}
footer{background:#062f3d;color:#cde8ee;padding:42px 0 24px;margin-top:30px;font-size:13.5px}footer h4{color:#fff;font:900 12.5px "Source Sans 3",sans-serif;letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px}footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#ecfeff}.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:26px}.disclaimer{border-top:1px solid rgba(255,255,255,.18);margin-top:28px;padding-top:16px;color:#b7d3da;font-size:12.5px}.copy{margin-top:12px;text-align:center;color:#9fc4cc;font-size:12px}
@media(max-width:780px){.cols2,.vs{grid-template-columns:1fr}.phone-cta{text-align:left}.hero{padding:58px 0}.dd{position:static;box-shadow:none;width:100%;border-left:0;border-right:0}.nav .em{margin-left:0;width:100%}.nav .em>a{margin:8px 12px;text-align:center}.logo-name{font-size:1.15rem}}
"""


HUB_DATA: list[tuple[str, str, str, list[str]]] = [
    (
        "beachside-coworking",
        "Beachside Coworking",
        "Coworking plans for remote professionals, founders, creatives, and travelers who want productive workspace close to the sand.",
        [
            "Hot Desk Memberships",
            "Dedicated Desk Plans",
            "Day Passes",
            "Ocean-View Workstations",
            "Quiet Focus Zones",
            "High-Speed WiFi Workspace",
            "Printing And Admin Support",
            "Member Networking Events",
            "Tourist Professional Day Access",
            "Flexible Monthly Memberships",
        ],
    ),
    (
        "private-offices-suites",
        "Private Offices & Suites",
        "Private offices and lockable suites for focused workdays, small teams, startup sprints, and executive beachside office needs.",
        [
            "Private Single Offices",
            "Team Office Suites",
            "Lockable Private Suites",
            "Furnished Office Options",
            "Window Offices",
            "Long-Term Office Leases",
            "Month-To-Month Private Offices",
            "Startup Team Suites",
            "Executive Corner Offices",
            "Secure Access Suites",
        ],
    ),
    (
        "meeting-rooms-events",
        "Meeting Rooms & Events",
        "Meeting rooms, presentation space, and hospitality-minded event support for teams gathering in South Beach.",
        [
            "Boardroom Rentals",
            "Small Huddle Rooms",
            "Client Presentation Rooms",
            "Zoom-Ready Meeting Rooms",
            "Half-Day Room Bookings",
            "Full-Day Event Spaces",
            "Workshop Hosting",
            "Networking Mixer Spaces",
            "Podcast Interview Rooms",
            "Hybrid Meeting Support",
        ],
    ),
    (
        "beach-amenities-lifestyle",
        "Beach Amenities & Lifestyle",
        "Lifestyle amenities that make a productive workday feel connected to Miami Beach without losing focus or professionalism.",
        [
            "Work With Ocean Views",
            "Steps To The Sand",
            "Sunrise Work Sessions",
            "Outdoor Patio Work Zones",
            "Cafe Break Areas",
            "Bike Storage Access",
            "Showers After Beach",
            "Wellness Break Spaces",
            "South Beach Location Perks",
            "Scenic Focus Environment",
        ],
    ),
    (
        "luxury-condo-residences",
        "Luxury Condo Residences",
        "Condominium support for owners, residents, and longer-stay guests who want a polished live-work base near the water.",
        [
            "Luxury Condo Listings Support",
            "Oceanfront Condo Living",
            "Designer Interior Condos",
            "Condo Concierge Services",
            "Resident Amenity Access",
            "Long-Stay Condo Options",
            "Furnished Luxury Condos",
            "Condo Owner Partnerships",
            "Move-In Ready Residences",
            "Premium Building Access",
        ],
    ),
    (
        "short-term-rentals",
        "Short-Term Rentals",
        "Short-term and furnished rental options for beach stays, business travel, extended stays, and flexible Miami Beach visits.",
        [
            "Short-Term Vacation Rentals",
            "Weekly Beach Stays",
            "Monthly Furnished Rentals",
            "Business Travel Stays",
            "Extended Stay Suites",
            "Weekend Getaway Rentals",
            "Fully Stocked Rentals",
            "Self Check-In Stays",
            "Group Travel Rentals",
            "Workcation Package Stays",
        ],
    ),
    (
        "workcation-packages",
        "Workcation Packages",
        "Bundled coworking, meeting, and stay concepts for remote workers, teams, advisors, and digital nomads visiting South Beach.",
        [
            "Work Plus Stay Bundles",
            "Condo Plus Coworking Packages",
            "Weekly Workcation Plans",
            "Monthly Remote-Work Packages",
            "Team Offsite Packages",
            "Advisor Retreat Packages",
            "Digital Nomad Memberships",
            "Fly-In Work Weeks",
            "Stay And Meet Packages",
            "Scenic Productivity Packages",
        ],
    ),
]


def slugify(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def child_blurb(hub_name: str, child_name: str) -> str:
    focus = {
        "Beachside Coworking": "workspace access, visitor-friendly terms, and everyday productivity near the water",
        "Private Offices & Suites": "private workspace, secure access, and flexible office planning in South Beach",
        "Meeting Rooms & Events": "host-ready rooms, presentation needs, and guest arrivals close to Miami Beach hospitality",
        "Beach Amenities & Lifestyle": "focus, comfort, and beach-adjacent routines that support a better workday",
        "Luxury Condo Residences": "polished residence support, owner coordination, and longer-stay live-work comfort",
        "Short-Term Rentals": "furnished stays, flexible booking windows, and work-ready beach lodging",
        "Workcation Packages": "bundled work, stay, and meeting options for productive time in Miami Beach",
    }[hub_name]
    return f"{child_name} for {focus}. Details, availability, rates, and final NAP are pending owner confirmation."


HUBS = [
    {
        "slug": slug,
        "name": name,
        "short": name.replace(" & ", " And "),
        "blurb": blurb,
        "children": [(slugify(child), child, child_blurb(name, child)) for child in children],
    }
    for slug, name, blurb, children in HUB_DATA
]

assert len(HUBS) == 7
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
        f'<meta property="og:site_name" content="{escape(BRAND)}">\n'
        if canon
        else ""
    )
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex,nofollow">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(trunc(desc))}">
{canon_tag}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700;800&family=Source+Sans+3:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
{FACTORY_CSS}
</style></head><body>
"""


def chrome(depth: int) -> str:
    p = pfx(depth)
    hub_dd = "".join(
        f'<a href="{p}{h["slug"]}.html">{escape(h["name"])}</a>' for h in HUBS
    )
    return f"""<div class="stage">{escape(STAGING_BANNER)}</div>
<div class="utility"><div class="wrap"><span>{escape(TAGLINE)} · {escape(LOCATION)} · NAP pending owner review [confirm]</span><span><a href="mailto:{escape(EMAIL)}">{escape(EMAIL)} [confirm]</a></span></div></div>
<header class="main"><div class="wrap">
<a class="logo" href="{p}index.html"><span class="logo-mark">WB</span><span><span class="logo-name">{escape(BRAND)}</span><small>Beachside coworking · stays · residences</small></span></a>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE_DISPLAY)}</a><small>South Beach, Miami Beach · demo staging number [confirm]</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about/index.html">About &#9662;</a><div class="dd">
<a href="{p}about/index.html">About {escape(BRAND)}</a>
<a href="{p}about/why-work-near-the-water/index.html">Why Work Near the Water</a>
<a href="{p}about/south-beach-location/index.html">South Beach Location</a>
</div></li>
<li><a href="{p}request-a-tour/index.html">Request a Tour</a></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li class="em"><a href="{p}book-a-tour/index.html">Book a Tour</a></li>
</ul></div></nav>
"""


def footer(depth: int) -> str:
    p = pfx(depth)
    hubs = "".join(
        f'<li><a href="{p}{h["slug"]}.html">{escape(h["short"])}</a></li>' for h in HUBS
    )
    return f"""<footer><div class="wrap"><div class="fcols">
<div><h4>Workspace &amp; Stay Hubs</h4><ul>{hubs}</ul></div>
<div><h4>About</h4><ul>
<li><a href="{p}about/index.html">About {escape(BRAND)}</a></li>
<li><a href="{p}about/why-work-near-the-water/index.html">Why Work Near the Water</a></li>
<li><a href="{p}about/south-beach-location/index.html">South Beach Location</a></li>
<li><a href="{p}contact/index.html">Contact</a></li>
</ul></div>
<div><h4>Plan a Visit</h4><ul>
<li><a href="{p}book-a-tour/index.html">Book a Tour</a></li>
<li><a href="{p}request-a-tour/index.html">Request a Stay</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE_DISPLAY)} [confirm]</a></li>
<li><a href="mailto:{escape(EMAIL)}">{escape(EMAIL)} [confirm]</a></li>
</ul></div>
<div><h4>South Beach</h4><ul><li>{escape(ADDRESS)}</li><li>Domain: {escape(BASE)} [confirm]</li><li>{escape(OPERATOR_NOTE)}</li></ul></div>
</div>
<div class="disclaimer"><strong>Staging note:</strong> This noindex preview is a NearMe OS Website Factory build for owner review. Phone, email, domain, address, rates, availability, workspace amenities, condominium details, rental rules, licensing, taxes, and booking workflows must be confirmed before launch. Content avoids availability guarantees and uses hospitality copy for staging only.</div>
<div class="copy">Copyright &copy; 2026 {escape(BRAND)}. Staging preview; not a live public website.</div>
</div></footer>
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


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": BRAND,
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Miami Beach",
            "addressRegion": "FL",
            "postalCode": "33139",
            "addressCountry": "US",
        },
        "areaServed": "South Beach, Miami Beach, FL",
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(data, ensure_ascii=True)
        + "</script>"
    )


def form_shell(form_name: str, *, highlight: bool = False) -> str:
    space_options = [
        "Beachside coworking",
        "Private office or suite",
        "Meeting room or event",
        "Condo residence",
        "Short-term rental",
        "Workcation package",
        "Not sure yet",
    ]
    options = "".join(f"<option>{escape(o)}</option>" for o in space_options)
    klass = "formbox highlight" if highlight else "formbox"
    return f"""<div class="{klass}">
<label>First Name</label><input type="text" name="first_name">
<label>Last Name</label><input type="text" name="last_name">
<label>Email</label><input type="email" name="email">
<label>Phone</label><input type="tel" name="phone">
<label>Interest</label><select name="interest"><option>Please choose...</option>{options}</select>
<label>Preferred Timing</label><input type="text" name="timing" placeholder="Today, this week, monthly, event date, or stay dates">
<label>Message</label><textarea name="message" placeholder="Tell us what you want to tour, book, or confirm. Please do not submit sensitive payment details in staging."></textarea><br><br>
<button class="btn">{escape(form_name)}</button>
<p style="margin-top:12px;font-size:12px;color:#647984">Form shell for staging review. Final booking, payment, privacy, rental, condo, and lead-routing details must be confirmed by the owner. [confirm]</p>
</div>"""


def stats_block() -> str:
    stats = [
        ("7", "Factory hubs"),
        ("70", "SVC-child pages"),
        ("South Beach", "Location [confirm]"),
        ("3", "Staging form paths"),
    ]
    return (
        '<div class="stats">'
        + "".join(
            f'<div class="stat"><b>{escape(num)}</b><span>{escape(label)}</span></div>'
            for num, label in stats
        )
        + "</div>"
    )


def home() -> str:
    hub_cards = []
    for h in HUBS:
        kids = "".join(
            f'<li><a href="{h["slug"]}/{s}/index.html">{escape(n)}</a></li>'
            for s, n, _ in h["children"][:3]
        )
        hub_cards.append(
            f'<div class="hubcard"><h3><a href="{h["slug"]}.html">{escape(h["name"])}</a></h3>'
            f"<p>{escape(h['blurb'])}</p><ul class=\"checks\">{kids}</ul>"
            f'<a href="{h["slug"]}.html" style="font-weight:900">Explore {escape(h["short"]).lower()} &rarr;</a></div>'
        )
    desc = (
        "Work Office at the Beach is a South Beach staging concept for coworking, beachside offices, "
        "luxury condominiums, short-term rentals, and workcation packages."
    )
    return (
        head(f"{BRAND} | South Beach Coworking, Offices & Stays", desc, canonical=f"{BASE}/")
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap">
<span class="eyebrow">South Beach workspace and stays</span>
<h1>{escape(TAGLINE)}</h1>
<p>{escape(BRAND)} is a factory staging build for productive coworking, private office time, meeting rooms, luxury condominium support, short-term rentals, and workcation packages in {escape(LOCATION)}.</p>
<div class="hero-ctas">
<a class="btn alt" href="book-a-tour/index.html">Book a Tour</a>
<a class="btn ghost" href="request-a-tour/index.html">Request a Stay</a>
<a class="btn ghost" href="tel:{PHONE_TEL}">Call {escape(PHONE_DISPLAY)} [confirm]</a>
</div></div></div>
<section class="cream"><div class="wrap"><div class="kicker">Factory preview</div><h2>Workspace hospitality with a Miami Beach point of view.</h2>
<p class="lead">The staging site positions {escape(BRAND)} as a polished live-work destination: serious enough for focus, light enough to feel like South Beach, and careful to mark all NAP and availability details for confirmation.</p>
{stats_block()}</div></section>
<section><div class="wrap"><div class="cols2">
<div><div class="kicker">Positioning</div><h2>Beachside productivity, private rooms, and stay options in one owner-review map.</h2>
<p>This preview combines coworking and beachside office space with luxury condominium and short-term rental content. The tone is inviting Miami Beach hospitality without promising specific views, inventory, or amenities before the owner confirms them.</p>
<ul class="checks"><li>Hot desks, private offices, quiet work zones, and meeting rooms.</li><li>Condo residence, furnished stay, and short-term rental pathways.</li><li>Workcation packages for remote workers, advisors, and teams.</li><li>NAP, street address, pricing, and booking policies marked [confirm].</li></ul></div>
<div class="feature"><h3>Owner review reminder</h3><p>{escape(OPERATOR_NOTE)}.</p><p><strong>Address:</strong> {escape(ADDRESS)}<br><strong>Email:</strong> {escape(EMAIL)} [confirm]<br><strong>Phone:</strong> {escape(PHONE_DISPLAY)} [confirm]</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><div class="kicker">Factory map</div><h2>Explore the 7-hub service taxonomy</h2><p class="lead">Each hub leads to ten SVC-CHILD pages for focused staging review.</p><div class="cols3">{''.join(hub_cards)}</div></div></section>
"""
        + faqs(
            [
                (
                    "Is this the live Work Office at the Beach website?",
                    "No. This is a noindex staging preview for owner review and is not ready for public booking traffic.",
                ),
                (
                    "Are the phone number and address final?",
                    "No. The phone is a demo staging number and the South Beach street address is TBD. Both are marked [confirm].",
                ),
                (
                    "Can the site support workspace and stay inquiries?",
                    "Yes. The staging forms are structured for tours, workspace needs, condo interest, short-term stays, and workcation packages, pending final routing and policy review.",
                ),
            ]
        )
        + f"""
<div class="ctastrip"><div class="wrap"><h2>Tour the workspace or request stay details.</h2><p>Use the staging forms to review the lead flow for coworking, office, meeting, condo, rental, and workcation inquiries.</p><a class="btn alt" href="book-a-tour/index.html">Book a Tour</a> <a class="btn" href="request-a-tour/index.html">Request a Stay</a></div></div>
"""
        + org_schema()
        + footer(0)
    )


def hub_page(h: dict) -> str:
    cards = "".join(
        f'<div class="gcard"><h3><a href="{h["slug"]}/{s}/index.html">{escape(n)}</a></h3><p>{escape(b)}</p><span class="tag">SVC-CHILD</span></div>'
        for s, n, b in h["children"]
    )
    return (
        head(f"{h['name']} | {BRAND}", f"{h['name']} in South Beach from {BRAND}. {h['blurb']}", canonical=f"{BASE}/{h['slug']}.html")
        + chrome(0)
        + f"""
<div class="wrap crumb"><a href="index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Service hub</div><h2>{escape(h["name"])} in South Beach</h2>
<p class="lead">{escape(h["blurb"])} This hub is written for staging review; availability, rates, building access, and final NAP must be confirmed. [confirm]</p>
<p><a class="btn" href="book-a-tour/index.html">Book a Tour</a> <a class="btn alt" href="request-a-tour/index.html">Request a Stay</a></p></div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Pages</h2><div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>How this fits the factory positioning</h2><ul class="checks">
<li>Copy stays hospitality-forward while avoiding unconfirmed luxury, view, or availability guarantees.</li>
<li>Workspace, residence, and rental pathways can all route to owner-approved inquiry handling.</li>
<li>South Beach location language remains broad until street-level NAP is confirmed.</li>
<li>Every related child page is marked as SVC-CHILD in the inventory.</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What is included in {h['name']}?", h["blurb"]),
                (
                    "Can visitors book directly from this staging page?",
                    "No. The forms are staging shells. Final booking, payment, and policy systems must be connected after owner approval.",
                ),
                (
                    "What still needs owner confirmation?",
                    "NAP details, unit inventory, workspace rates, access rules, photography, rental policies, taxes, and form routing require confirmation.",
                ),
            ]
        )
        + footer(0)
    )


def leaf_page(h: dict, child: tuple[str, str, str]) -> str:
    slug, name, blurb = child
    related = "".join(
        f'<div class="gcard"><h3><a href="../{s}/index.html">{escape(n)}</a></h3></div>'
        for s, n, _ in h["children"]
        if s != slug
    )
    return (
        head(f"{name} | {BRAND}", f"{name} in South Beach from {BRAND}. {blurb}", canonical=f"{BASE}/{h['slug']}/{slug}/")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../../{h["slug"]}.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">SVC-CHILD</div><h2>{escape(name)} near the water</h2>
<p class="lead">{escape(blurb)} This staging copy should be checked against actual space, stay, condo, and rental availability before launch. [confirm]</p>
<p><a class="btn" href="../../book-a-tour/index.html">Book a Tour</a> <a class="btn alt" href="../../request-a-tour/index.html">Request a Stay</a></p></div></section>
<section class="tint"><div class="wrap"><h2>Good-fit conversations for {escape(name.lower())}</h2><ul class="checks">
<li>Whether the visitor needs a workspace day, private office, meeting room, stay, residence, or bundled workcation.</li>
<li>Preferred dates, group size, length of stay, work setup, and privacy needs.</li>
<li>Desired proximity to the beach, views, showers, bike storage, patio areas, or cafe-style breaks where available.</li>
<li>Any accessibility, security, building access, or guest arrival requirements.</li>
<li>Owner-approved pricing, rental rules, deposits, taxes, and cancellation terms. [confirm]</li>
</ul></div></section>
<section><div class="wrap"><h2>South Beach staging angle</h2><p>The page frames {escape(name.lower())} as part of a professional beachside hospitality experience: focused work, scenic breaks, and stay options in {escape(LOCATION)}. Final copy should use real photography, confirmed amenities, and owner-approved claims before public use.</p></div></section>
<section class="cream"><div class="wrap"><div class="vs">
<div class="col bad"><h3>Generic coworking copy</h3><ul class="checks"><li>Promises amenities without confirming them.</li><li>Ignores stay, condo, and visitor use cases.</li><li>Sounds like any office space in any city.</li></ul></div>
<div class="col good"><h3>Work Office at the Beach framing</h3><ul class="checks"><li>Connects productive work with Miami Beach hospitality.</li><li>Routes workspace and stay intent to the right form.</li><li>Marks all NAP, availability, and policy details [confirm].</li></ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ask about {escape(name.lower())}.</h2><p>Use the staging form to review how this inquiry should be handled once details are confirmed.</p><a class="btn alt" href="../../book-a-tour/index.html">Book a Tour</a> <a class="btn" href="../../contact/index.html">Contact</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"Is {name.lower()} guaranteed to be available?",
                    "No. This is staging copy only. Availability, rates, rules, and inclusions must be confirmed by the owner.",
                ),
                (
                    "Is this page indexed by search engines?",
                    "No. The staging site uses noindex meta tags, robots.txt Disallow, and Netlify X-Robots-Tag headers.",
                ),
            ]
        )
        + f'<section><div class="wrap"><h2>Related {escape(h["short"])} Pages</h2><div class="grid">{related}</div></div></section>'
        + footer(2)
    )


def cta_page(slug: str, title: str, h2: str, lead: str, button: str, *, highlight: bool = False) -> str:
    steps = {
        "contact": [
            ("Call or email", f"Reach the staging contact at {PHONE_DISPLAY} or {EMAIL}; both require owner confirmation."),
            ("Share the inquiry type", "Workspace, office, meeting, residence, rental, or workcation interest can be selected in the form."),
            ("Confirm routing", "Lead delivery, notifications, privacy text, and response expectations must be finalized before launch."),
        ],
        "request-a-tour": [
            ("Describe your visit or stay", "Tell us whether you are exploring coworking, a private office, a short stay, or a bundled workcation."),
            ("Add timing and group size", "Preferred dates, number of guests, meeting needs, and workspace setup help qualify the request."),
            ("Owner confirms details", "Rates, inventory, rental policies, building access, and NAP details remain pending owner review."),
        ],
        "book-a-tour": [
            ("Choose what to tour", "Workspace, office suites, meeting rooms, condo concepts, or workcation packages can be reviewed."),
            ("Pick a preferred window", "The staging form captures timing only; it does not reserve a live appointment yet."),
            ("Review the handoff", "Final scheduling, calendar sync, and confirmation messages need owner approval before launch."),
        ],
    }[slug]
    step_cards = "".join(
        f'<div class="card"><div class="stepnum">{i}</div><h3>{escape(title_text)}</h3><p>{escape(body)}</p></div>'
        for i, (title_text, body) in enumerate(steps, 1)
    )
    return (
        head(title, lead, canonical=f"{BASE}/{slug}/")
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h2)}</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Plan a South Beach workday</div><h2>{escape(h2)}</h2><p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">{step_cards}</div>{form_shell(button, highlight=highlight)}</div></section>
<section class="tint"><div class="wrap"><h2>{escape(BRAND)} contact details</h2><p><strong>{escape(BRAND)}</strong><br>{escape(ADDRESS)}<br>Phone: <a href="tel:{PHONE_TEL}">{escape(PHONE_DISPLAY)}</a> [confirm]<br>Email: <a href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a> [confirm]</p></div></section>
"""
        + (org_schema() if slug == "contact" else "")
        + footer(1)
    )


def about_page() -> str:
    return (
        head(f"About {BRAND} | South Beach Miami", f"About {BRAND}, a South Beach staging concept for coworking, offices, stays, and residences.", canonical=f"{BASE}/about/")
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">About the concept</div><h2>{escape(BRAND)} brings productive work closer to the water.</h2>
<p class="lead">This owner-review staging site presents beachside coworking, private offices, meeting rooms, luxury condominium support, short-term rentals, and workcation packages in {escape(LOCATION)}.</p></div></section>
<section class="cream"><div class="wrap"><h2>Facts pending confirmation</h2><p>{escape(OPERATOR_NOTE)}.</p>{stats_block()}</div></section>
<section><div class="wrap"><div class="cols2"><div><h2>Hospitality with practical workspace intent.</h2><p>The brand voice is welcoming and scenic, but the conversion paths stay practical: book a tour, request a stay, contact the operator, and confirm the right workspace or lodging fit.</p></div><div class="card"><h3>About pages</h3><ul class="checks"><li><a href="why-work-near-the-water/index.html">Why Work Near the Water</a></li><li><a href="south-beach-location/index.html">South Beach Location</a></li></ul></div></div></div></section>
"""
        + faqs(
            [
                ("Where is the business located?", f"The staging address is {ADDRESS}. Street-level NAP is TBD and marked [confirm]."),
                ("What does the brand offer?", "The staging taxonomy covers coworking, private offices, meetings, lifestyle amenities, condo residences, short-term rentals, and workcation packages."),
                ("What needs confirmation?", "All NAP, availability, rates, building access, booking, rental, tax, licensing, and policy details need owner review."),
            ]
        )
        + org_schema()
        + footer(1)
    )


def why_page() -> str:
    return (
        head(f"Why Work Near the Water | {BRAND}", "Why beach-adjacent workspace can support focus, hospitality, and South Beach workdays.", canonical=f"{BASE}/about/why-work-near-the-water/")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Work Near the Water</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Work near the water</div><h2>Scenery can support the rhythm of a better workday.</h2><p class="lead">The staging concept balances focused work with South Beach breaks, walkability, and hospitality touchpoints.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Focus first</h3><p>Quiet zones, private rooms, and meeting spaces keep the workday productive where available. [confirm]</p></div>
<div class="card"><h3>Scenic resets</h3><p>Beach proximity, patio concepts, and cafe breaks give guests a way to step away without losing the day.</p></div>
<div class="card"><h3>Stay options</h3><p>Condo and short-term rental pathways can support longer visits, workcations, and remote-work travel.</p></div>
<div class="card"><h3>Team use cases</h3><p>Offsites, workshops, advisor retreats, and fly-in work weeks can combine rooms, workspace, and stays.</p></div>
<div class="card"><h3>Owner clarity</h3><p>Every operational promise remains marked for confirmation until real inventory and policies are approved.</p></div>
<div class="card"><h3>Miami Beach tone</h3><p>Ocean teal, sand, white, and restrained coral accents create a polished hospitality look.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Review the beachside work experience.</h2><a class="btn alt" href="../../book-a-tour/index.html">Book a Tour</a> <a class="btn" href="../../request-a-tour/index.html">Request a Stay</a></div></div>
"""
        + footer(2)
    )


def location_page() -> str:
    return (
        head(f"South Beach Location | {BRAND}", "South Beach Miami Beach staging location information for Work Office at the Beach.", canonical=f"{BASE}/about/south-beach-location/")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; South Beach Location</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">South Beach Miami</div><h2>A broad South Beach location placeholder pending final NAP.</h2><p class="lead">The current staging address is {escape(ADDRESS)}. Street address, building name, parking, access, transit, and arrival instructions require owner confirmation.</p></div></section>
<section class="cream"><div class="wrap"><div class="cols2"><div><h2>Location perks to verify</h2><ul class="checks"><li>Proximity to the sand and oceanfront routes.</li><li>Nearby cafes, hotels, restaurants, and wellness breaks.</li><li>Bike storage, showers, and building access if available.</li><li>Guest arrival, parking, rideshare, and concierge instructions.</li></ul></div><div class="feature"><h3>NAP status</h3><p><strong>Domain:</strong> {escape(BASE)} [confirm]<br><strong>Phone:</strong> {escape(PHONE_DISPLAY)} demo staging number [confirm]<br><strong>Email:</strong> {escape(EMAIL)} [confirm]<br><strong>Address:</strong> {escape(ADDRESS)}</p></div></div></div></section>
"""
        + footer(2)
    )


def write_inventory() -> None:
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
        ["/", "HOME", "", "work office at the beach", "logo/home", "A1,A2,A3,A10", ""],
        ["/about/", "COMP-HUB", "/", "about work office at the beach", "About menu", "A1,A6,A10", ""],
        ["/about/why-work-near-the-water/", "COMP-CHILD", "/about/", "why work near the water", "About menu", "A10,D", ""],
        ["/about/south-beach-location/", "COMP-CHILD", "/about/", "south beach location", "About menu", "A6,D", ""],
        ["/contact/", "COMP-CONTACT", "/", "contact work office at the beach", "Contact menu", "A3,A4,A5", "Contact Request"],
        ["/request-a-tour/", "FORM-STAY", "/", "request a stay south beach", "nav utility", "I1", "Request a Stay"],
        ["/book-a-tour/", "FORM-TOUR", "/", "book a tour work office beach", "nav highlighted", "I1", "Book a Tour"],
    ]
    for h in HUBS:
        rows.append(
            [
                f"/{h['slug']}.html",
                "SVC-HUB",
                "/",
                h["name"].lower(),
                "Services menu",
                "B (category)",
                "",
            ]
        )
        for s, n, _ in h["children"]:
            rows.append(
                [
                    f"/{h['slug']}/{s}/",
                    "SVC-CHILD",
                    f"/{h['slug']}.html",
                    n.lower(),
                    "Services menu > hub grid",
                    "B row",
                    "Book a Tour / Request a Stay",
                ]
            )
    with (ROOT / "WORKOFFICEBEACH-PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def write_questionnaire() -> None:
    hub_slugs = " | ".join(h["slug"] for h in HUBS)
    write(
        ROOT / "WORKOFFICEBEACH-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire - Work Office at the Beach Factory Pages

Home page and all factory pages share one chrome: staging banner, utility bar, logo/phone header, white top navigation, Services dropdown, About dropdown, Contact, Request a Tour, and highlighted Book a Tour CTA.

## A - Business identity
| Field | Value | Source |
|---|---|---|
| A1 brand | {BRAND} | user-provided business facts |
| A2 domain | {BASE} [confirm] | user-provided business facts |
| A3 phone | {PHONE_DISPLAY} / tel:{PHONE_TEL} - demo staging number [confirm] | user-provided business facts |
| A4 email | {EMAIL} [confirm] | user-provided business facts |
| A5 address | {ADDRESS} | user-provided business facts |
| A6 location | {LOCATION} | user-provided business facts |
| A7 tagline | {TAGLINE} | user-provided business facts |
| A8 positioning | Coworking / beachside office space plus luxury condominiums and short-term rentals | user-provided business facts |
| A9 operator_note | {OPERATOR_NOTE} | user-provided business facts |
| A10 tone | Inviting Miami Beach hospitality plus productive work; luxury without hype guarantees | user-provided business facts |

## B - Gate taxonomy
- Hubs: {len(HUBS)}
- Hub landing pages: root-level `.html` pages to keep index count near 80
- SVC-CHILD pages: {sum(len(h['children']) for h in HUBS)}
- Hub slugs: {hub_slugs}
- Full URL map: `WORKOFFICEBEACH-PAGE-INVENTORY.csv`

## C - Visual system
- Ocean teal `#0e7490`
- Deep sea `#0c4a6e`
- Sand cream `#f8f1e7`
- Warm sand-gold `#d4a373`
- Coral / sunset accent `#e11d48` used sparingly on highlighted form treatment
- Fonts: Fraunces headlines + Source Sans 3 body and navigation

## D - Forms and CTAs
- Primary CTA: `book-a-tour` (FORM-TOUR, highlighted)
- Secondary CTA: `request-a-tour` / Request a Stay
- Company/contact CTA: `contact`
- Form shells must be wired with owner-approved privacy, booking, rental, condo, tax, cancellation, and lead-routing language before public launch.

## E - Staging controls
- HTML uses `<meta name="robots" content="noindex,nofollow">`.
- `robots.txt` disallows all crawling.
- `netlify.toml` sends `X-Robots-Tag: noindex, nofollow`.
- Staging banner text: `{STAGING_BANNER}`
- Netlify password protection: not requested; deploy should be public noindex staging.

## F - Confirmation flags
- Domain: {BASE} [confirm]
- Phone: {PHONE_DISPLAY} [confirm] / tel:{PHONE_TEL}
- Email: {EMAIL} [confirm]
- Address: {ADDRESS}
- Workspace inventory, condo details, short-term rental policies, taxes, fees, photos, amenities, and booking workflows: [confirm]
""",
    )


def write_notes() -> None:
    write(
        ROOT / "WORKOFFICEBEACH-NOTES.md",
        f"""# Work Office at the Beach Factory Build Notes

- Branch: `cursor/work-office-beach-factory-127e`
- Domain target: {BASE} [confirm]
- Build type: NearMe OS Website Factory staging preview
- Page model: 7 service hubs x 10 children = 70 SVC-CHILD pages
- Generated `index.html` pages expected: 77
- Service hub landing pages: 7 root-level `.html` pages
- Inventory URLs expected: 84
- Staging controls: HTML noindex,nofollow; robots.txt `Disallow: /`; Netlify `X-Robots-Tag: noindex, nofollow`
- Banner: `{STAGING_BANNER}`
- Visual direction: Miami Beach ocean teal `#0e7490`, deep sea `#0c4a6e`, sand cream `#f8f1e7`, white, warm sand-gold `#d4a373`, restrained coral `#e11d48`
- Fonts: Fraunces for headlines and Source Sans 3 for interface/body
- Navigation: white top nav; dropdown links use dark text on white backgrounds
- CTA language: Book a Tour / Request a Stay
- Forms: contact, request-a-tour, book-a-tour highlighted
- NAP status: domain, phone, email, and street address require owner confirmation. {OPERATOR_NOTE}.
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
    write(ROOT / "robots.txt", "User-agent: *\nDisallow: /\n")
    write(
        ROOT / "netlify.toml",
        """[build]
  publish = "."

[[headers]]
  for = "/*"
  [headers.values]
    X-Robots-Tag = "noindex, nofollow"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "SAMEORIGIN"
""",
    )
    write(ROOT / "_redirects", "/*    /404.html  404\n")


def cleanup_generated_site() -> None:
    keep_names = {".git", ".gitignore", "scripts"}
    for child in list(ROOT.iterdir()):
        if child.name in keep_names:
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
        write(ROOT / f"{h['slug']}.html", hub_page(h))
        urls.append(f"/{h['slug']}.html")
        for child in h["children"]:
            write(ROOT / h["slug"] / child[0] / "index.html", leaf_page(h, child))
            urls.append(f"/{h['slug']}/{child[0]}/")

    write(ROOT / "about" / "index.html", about_page())
    urls.append("/about/")
    write(ROOT / "about" / "why-work-near-the-water" / "index.html", why_page())
    urls.append("/about/why-work-near-the-water/")
    write(ROOT / "about" / "south-beach-location" / "index.html", location_page())
    urls.append("/about/south-beach-location/")

    for slug, title, h2, lead, button, highlight in [
        (
            "contact",
            f"Contact {BRAND}",
            f"Contact {BRAND}",
            "Call, email, or send a staging inquiry for workspace, offices, meetings, residences, rentals, and workcations.",
            "Contact Work Office at the Beach",
            False,
        ),
        (
            "request-a-tour",
            f"Request a Stay or Tour | {BRAND}",
            "Request a Stay or Tour",
            "Share your South Beach stay, workspace, meeting, or residence interest so the owner can confirm the right path.",
            "Request a Stay",
            False,
        ),
        (
            "book-a-tour",
            f"Book a Tour | {BRAND}",
            "Book a Tour",
            "Use the highlighted staging form to request a tour of coworking, office, meeting, residence, or workcation options.",
            "Book a Tour",
            True,
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead, button, highlight=highlight))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head(f"Page Not Found | {BRAND}", "Page not found.")
        + chrome(0)
        + f"""
<section style="padding:72px 0"><div class="wrap"><h2>Page not found</h2>
<p class="lead">That URL is not in the {escape(BRAND)} staging factory map. Return home or use the highlighted tour form.</p>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn alt" href="book-a-tour/index.html">Book a Tour</a></p>
</div></section>
"""
        + footer(0),
    )

    write_static_files(urls)
    write_inventory()
    write_questionnaire()
    write_notes()

    index_pages = list(ROOT.rglob("index.html"))
    hub_html = list(ROOT.glob("*.html"))
    inventory_children = 0
    inventory_rows = 0
    with (ROOT / "WORKOFFICEBEACH-PAGE-INVENTORY.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            inventory_rows += 1
            if row["type_id"] == "SVC-CHILD":
                inventory_children += 1

    print(f"Index pages on disk: {len(index_pages)}")
    print(f"Root-level .html pages (includes 7 hubs + 404): {len(hub_html)}")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Inventory URLs: {inventory_rows}")
    print(f"Hubs: {len(HUBS)}")
    print(f"SVC-CHILD inventory rows: {inventory_children}")
    print("Home uses shared factory chrome: yes")
    print("Staging noindex controls: yes")
    print("Dropdown CSS dark-on-white: yes")


if __name__ == "__main__":
    main()
