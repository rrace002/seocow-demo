#!/usr/bin/env python3
"""Shared completeness chrome for NearMe OS factory sites.

Implements FACTORY-INSTRUCTION-SET.md. Quality bar: live san-diegotechsupport.com
structure (hero, icon tiles, stats, benefits, how-it-works, home form, insights,
partners) without copying that site's copyrighted assets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from typing import Iterable


COMPLETE_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap');
:root{--ink:#0b1f33;--muted:#5b6b7c;--line:#d7e2ea;--paper:#f4f7fb;--accent:#0ea5a0;--accent-dark:#0b7c78;--navy:#0b3d5c;--navy-2:#082c42;--cta:#e38b2a;--cta-hover:#c6741c;--ok:#148f5c;--bad:#c0392b;--max:1160px}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Source Sans 3',Segoe UI,Arial,sans-serif;color:var(--ink);line-height:1.65;background:#fff}
h1,h2,h3,h4,.logo,.btn,.nav,summary{font-family:Sora,Segoe UI,sans-serif}
a{color:var(--accent-dark);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:var(--max);margin:0 auto;padding:0 22px}
.demo-banner{background:#071422;color:#9ee7e2;text-align:center;font:600 12px Sora,sans-serif;padding:8px 12px;letter-spacing:.3px}
.utility{background:var(--navy);color:#d7eef2;font-size:13px;padding:7px 0}
.utility .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.utility a{color:#fff}
header.main{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:80}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding:12px 22px;gap:16px}
.brand{display:flex;align-items:center;gap:12px;color:var(--ink);text-decoration:none}
.brand:hover{text-decoration:none}
.mark{width:46px;height:46px;flex:0 0 46px}
.logo{font:800 20px/1.1 Sora,sans-serif}
.logo span{color:var(--accent-dark)}
.logo small{display:block;font:600 10px Sora,sans-serif;color:var(--muted);letter-spacing:1.4px;text-transform:uppercase;margin-top:3px}
.phone-cta{text-align:right}
.phone-cta a{font:800 20px Sora,sans-serif;color:var(--navy);display:block}
.phone-cta small{color:var(--muted);font-size:12px}
nav.nav{background:var(--navy-2)}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap;align-items:center}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:13px 15px;font-size:13.5px;font-weight:650}
nav.nav a:hover{background:#061e2e;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:280px;max-height:70vh;overflow:auto;box-shadow:0 12px 28px rgba(8,44,66,.18);border-top:3px solid var(--accent);z-index:90}
.dd a{color:var(--ink)!important;padding:10px 16px;font-weight:600;border-bottom:1px solid #eef3f7}
.dd a:hover{background:#eef8f7}
.nav .em a{background:var(--accent)}.nav .em a:hover{background:var(--accent-dark)}
.search-mini{margin-left:auto;padding:8px 0 8px 12px}
.search-mini input{border:0;border-radius:4px;padding:8px 10px;min-width:160px;font:14px 'Source Sans 3',sans-serif}
.hero-photo{position:relative;color:#fff;padding:72px 0 68px;background:
  linear-gradient(105deg,rgba(8,24,40,.88) 8%,rgba(11,61,92,.55) 52%,rgba(8,24,40,.35) 100%),
  radial-gradient(1200px 420px at 80% 20%,rgba(14,165,160,.35),transparent 55%),
  linear-gradient(180deg,#0b3d5c,#134e4a);
overflow:hidden}
.hero-photo:after{content:"";position:absolute;inset:auto -40px -80px 40%;height:280px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 200'%3E%3Cpath fill='%23ffffff18' d='M0 160 L40 120 L80 150 L140 80 L180 110 L240 40 L300 90 L360 30 L420 100 L480 50 L540 110 L600 70 L660 130 L720 90 L800 140 L800 200 L0 200Z'/%3E%3C/svg%3E") no-repeat bottom right;background-size:cover;pointer-events:none}
.hero-photo .wrap{position:relative;z-index:1;display:grid;grid-template-columns:1.2fr .8fr;gap:28px;align-items:center}
.kicker{font:700 12px Sora,sans-serif;letter-spacing:1.6px;text-transform:uppercase;color:#9ee7e2;margin-bottom:10px}
.hero-photo h1{font-size:40px;line-height:1.15;max-width:640px;margin-bottom:14px}
.hero-photo p{font-size:18px;color:#e7f4f6;max-width:560px}
.hero-actions{margin-top:26px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.search-hero{display:flex;gap:8px;margin-top:22px;max-width:460px}
.search-hero input{flex:1;padding:12px 14px;border:0;border-radius:4px;font:15px 'Source Sans 3',sans-serif}
.hero-card{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);backdrop-filter:blur(6px);border-radius:10px;padding:22px}
.hero-card h3{font-size:16px;margin-bottom:8px}
.hero-card p{font-size:14px;color:#d7eef2;margin:0}
.btn{display:inline-block;background:var(--cta);color:#fff;font:700 14px Sora,sans-serif;padding:13px 24px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:var(--cta-hover);text-decoration:none;color:#fff}
.btn.alt{background:#fff;color:var(--navy)}.btn.alt:hover{background:#e8f4f3;color:var(--navy)}
.btn.navy{background:var(--navy)}
section{padding:52px 0}
section.tint{background:var(--paper)}
section.navy{background:var(--navy);color:#fff}section.navy h2{color:#fff}
section h2{font-size:28px;margin-bottom:14px;line-height:1.25}
section p{margin-bottom:14px;font-size:17px}
.lead{font-size:18.5px;color:#334155}
.inner-hero{padding:36px 0 10px}
.photo-panel{min-height:160px;border-radius:10px;background:
  linear-gradient(160deg,rgba(11,61,92,.2),rgba(14,165,160,.25)),
  linear-gradient(45deg,#0b3d5c 0%,#148f8c 100%);
box-shadow:inset 0 0 0 1px #ffffff22}
ul.checks{list-style:none;margin:10px 0}
ul.checks li{padding:8px 0 8px 30px;position:relative}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:var(--ok);font-weight:800}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.icon-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:16px;margin-top:22px}
.icon-tile{background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px;text-align:center;box-shadow:0 6px 18px rgba(11,61,92,.06);transition:transform .15s ease}
.icon-tile:hover{transform:translateY(-3px);text-decoration:none}
.icon-tile svg{width:48px;height:48px;margin-bottom:8px}
.icon-tile h3{font-size:15px;color:var(--ink);margin:0 0 6px}
.icon-tile p{font-size:13px;color:var(--muted);margin:0}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:22px;box-shadow:0 4px 14px rgba(11,61,92,.05)}
.card h3{font-size:17px;margin-bottom:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;margin-top:18px}
.gcard{background:#fff;border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:8px;padding:18px}
.gcard h3{font-size:16px;margin-bottom:6px}.gcard h3 a{color:var(--ink)}
.gcard p{font-size:14px;color:var(--muted);margin:0}
.ctastrip{background:var(--navy-2);color:#fff;text-align:center;padding:42px 0}
.ctastrip h2{color:#fff;margin-bottom:12px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--line);border-radius:8px;overflow:hidden;margin-top:16px}
.vs .col{padding:22px}
.vs .col.bad{background:#fff5f5}.vs .col.good{background:#f0faf6}
.vs h3{font-size:16px;margin-bottom:10px}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e5e7eb}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:var(--bad);font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:var(--ok);font-weight:800}
details{border:1px solid var(--line);border-radius:6px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px Sora,sans-serif;list-style:none}
details summary:before{content:"+ ";color:var(--accent-dark);font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px}
.formbox{background:#fff;border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:8px;padding:24px}
.formbox label{display:block;font:600 12.5px Sora,sans-serif;color:var(--muted);margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:11px;border:1px solid #c5d0d8;border-radius:4px;font:15px 'Source Sans 3',sans-serif}
.formbox textarea{min-height:96px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin:20px 0}
.step{position:relative;padding-top:8px}
.step b{display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:50%;background:var(--accent);color:#fff;margin-bottom:8px}
.crumb{font-size:13px;color:var(--muted);padding:16px 0 0}
.crumb a{color:var(--muted)}
footer{background:#071422;color:#b7c4ce;padding:48px 0 24px;margin-top:20px;font-size:14px}
footer h4{color:#fff;font:700 12px Sora,sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c5d4de}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:24px}
.copy{border-top:1px solid #1a3348;margin-top:28px;padding-top:16px;text-align:center;font-size:12px;color:#8aa0b0}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}
.stat{background:#fff;border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:8px;padding:18px;text-align:center}
.stat b{display:block;font:800 22px Sora,sans-serif}
.stat span{font:600 11.5px Sora,sans-serif;color:var(--muted);letter-spacing:.4px;text-transform:uppercase}
.navy .stat{background:rgba(255,255,255,.08);border-color:transparent;color:#fff}.navy .stat span{color:#b7e4e0}
.hubcard{background:#fff;border:1px solid var(--line);border-radius:10px;padding:20px;box-shadow:0 6px 16px rgba(11,61,92,.06)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:var(--ink)}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 18px;position:relative;font-size:14px}
.hubcard li:before{content:"\2192";position:absolute;left:0;color:var(--accent-dark)}
.partners{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.partner{border:1px solid var(--line);background:#fff;border-radius:6px;padding:10px 14px;font:700 13px Sora,sans-serif;color:var(--navy)}
.insight-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
.insight{background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.insight .thumb{height:92px;background:linear-gradient(120deg,#0b3d5c,#0ea5a0)}
.insight .pad{padding:16px}
.insight small{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.5px}
.insight h3{font-size:16px;margin:6px 0}
@media(max-width:860px){
  .hero-photo .wrap,.cols2,.vs{grid-template-columns:1fr}
  .hero-photo h1{font-size:30px}
  .search-mini{margin-left:0}
}
"""


ICONS: dict[str, str] = {
    "bot": "M8 14h2M14 14h2M12 8V4M8 18h8a4 4 0 0 0 4-4V9a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v5a4 4 0 0 0 4 4z",
    "signal": "M5 19v-6M9 19V9M13 19V5M17 19v-9",
    "node": "M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3zM12 12l8-4.5M12 12v9M12 12L4 7.5",
    "chart": "M4 19h16M7 16V9M12 16V5M17 16v-7",
    "contract": "M7 3h8l4 4v14H7zM15 3v4h4M9 13h6M9 17h6M9 9h2",
    "shield": "M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z",
    "wallet": "M4 7h16v12H4zM4 7l2-3h10l2 3M16 13h2",
    "chain": "M9 12a4 4 0 0 1 0-6l2-2a4 4 0 1 1 6 6l-1 1M15 12a4 4 0 0 1 0 6l-2 2a4 4 0 1 1-6-6l1-1",
    "lock": "M8 11V8a4 4 0 1 1 8 0v3M6 11h12v9H6z",
    "briefcase": "M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M4 7h16v12H4zM4 12h16",
    "search": "M11 19a8 8 0 1 1 0-16 8 8 0 0 1 0 16zM21 21l-4.3-4.3",
    "people": "M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75",
    "phone": "M6 3h4l2 5-2 1a12 12 0 0 0 5 5l1-2 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 4 5a2 2 0 0 1 2-2z",
}


def svg_icon(name: str, size: int = 48) -> str:
    d = ICONS.get(name, ICONS["briefcase"])
    return (
        f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
        f'stroke="#0b7c78" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<path d="{d}"/></svg>'
    )


def logo_mark() -> str:
    return """<svg class="mark" viewBox="0 0 46 46" aria-hidden="true">
<rect width="46" height="46" rx="9" fill="#0b3d5c"/>
<circle cx="23" cy="23" r="10" fill="none" stroke="#0ea5a0" stroke-width="3"/>
<circle cx="23" cy="23" r="4" fill="#e38b2a"/>
</svg>"""


@dataclass
class SiteConfig:
    name: str
    logo_html: str
    tagline: str
    domain: str
    base: str
    phone: str
    phone_tel: str
    email: str
    hq: str
    address: str
    hours: str
    founded: str
    staging_banner: str
    about_href: str
    consult_href: str
    proposal_href: str
    contact_href: str
    insights_href: str = "insights/"
    search_href: str = "search/"
    disclaimer: str = ""
    partners: list[str] = field(default_factory=list)


def pfx(depth: int) -> str:
    return "" if depth == 0 else "../" * depth


def trunc(text: str, n: int = 155) -> str:
    import re

    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= n:
        return text
    return text[: n - 1].rsplit(" ", 1)[0].rstrip(" ,.;:") + "…"


def head(site: SiteConfig, title: str, desc: str) -> str:
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(trunc(desc))}">
<style>
{COMPLETE_CSS}
</style></head><body>
<div class="demo-banner">{escape(site.staging_banner)}</div>
"""


def chrome(site: SiteConfig, hubs: list[dict], depth: int) -> str:
    p = pfx(depth)
    hub_dd = "".join(
        f'<a href="{p}{h["slug"]}/index.html">{escape(h["name"])}</a>' for h in hubs
    )
    return f"""<div class="utility"><div class="wrap">
<span>{escape(site.tagline)} · {escape(site.hq)}</span>
<span><a href="tel:{site.phone_tel}">{escape(site.phone)}</a> · <a href="mailto:{site.email}">{escape(site.email)}</a></span>
</div></div>
<header class="main"><div class="wrap">
<a class="brand" href="{p}index.html">{logo_mark()}<div class="logo">{site.logo_html}<small>{escape(site.tagline)}</small></div></a>
<div class="phone-cta"><a href="tel:{site.phone_tel}">{escape(site.phone)}</a><small>{escape(site.hours)}</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{hubs[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}{site.about_href}index.html">About &#9662;</a><div class="dd">
<a href="{p}{site.about_href}index.html">About {escape(site.name)}</a>
<a href="{p}{site.about_href}why-choose-us/index.html">Why Choose Us</a>
<a href="{p}{site.about_href}who-we-serve/index.html">Who We Serve</a>
</div></li>
<li><a href="{p}{site.insights_href}index.html">Insights</a></li>
<li><a href="{p}{site.contact_href}index.html">Contact</a></li>
<li><a href="{p}{site.proposal_href}index.html">Request a Proposal</a></li>
<li class="em"><a href="{p}{site.consult_href}index.html">Consultation</a></li>
<li class="search-mini"><form action="{p}{site.search_href}index.html" method="get"><input type="search" name="q" placeholder="Search Find Now" aria-label="Search the site"></form></li>
</ul></div></nav>
"""


def footer(site: SiteConfig, hubs: list[dict], depth: int) -> str:
    p = pfx(depth)
    hubs_html = "".join(
        f'<li><a href="{p}{h["slug"]}/index.html">{escape(h["short"])}</a></li>' for h in hubs
    )
    disc = f"<br>{escape(site.disclaimer)}" if site.disclaimer else ""
    return f"""<footer><div class="wrap"><div class="fcols">
<div><h4>Services</h4><ul>{hubs_html}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="{p}{site.about_href}index.html">About {escape(site.name)}</a></li>
<li><a href="{p}{site.about_href}why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}{site.about_href}who-we-serve/index.html">Who We Serve</a></li>
<li><a href="{p}{site.contact_href}index.html">Contact Us</a></li>
</ul></div>
<div><h4>Insights</h4><ul>
<li><a href="{p}{site.insights_href}index.html">All insights</a></li>
<li><a href="{p}{site.search_href}index.html">Search</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}{site.consult_href}index.html">Request a Consultation</a></li>
<li><a href="{p}{site.proposal_href}index.html">Request a Proposal</a></li>
<li><a href="tel:{site.phone_tel}">{escape(site.phone)}</a></li>
<li><a href="mailto:{site.email}">{escape(site.email)}</a></li>
<li>{escape(site.address)}</li>
</ul></div>
</div>
<div class="copy">{escape(site.name)} · {escape(site.hq)} · {escape(site.phone)}
<br>Copyright &copy; 2026. {escape(site.name)}. All rights reserved.{disc}</div></div></footer>
</body></html>"""


def form_shell(hubs: Iterable[dict], extra_options: Iterable[str] = ()) -> str:
    opts = "".join(f'<option>{escape(h["name"])}</option>' for h in hubs)
    extra = "".join(f"<option>{escape(o)}</option>" for o in extra_options)
    return f"""<div class="formbox">
<label>First Name *</label><input type="text" name="first" required>
<label>Last Name *</label><input type="text" name="last" required>
<label>Email *</label><input type="email" name="email" required>
<label>Phone *</label><input type="tel" name="phone" required>
<label>Company</label><input type="text" name="company">
<label>Which services are you interested in? *</label>
<select name="service" required><option value="">-- Select a service --</option>{opts}{extra}<option>Not sure / consultation</option></select>
<label>Message</label><textarea name="message"></textarea><br><br>
<button class="btn" type="submit">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#5b6b7c">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def stats_html(items: list[tuple[str, str]]) -> str:
    inner = "".join(
        f'<div class="stat"><b>{escape(v)}</b><span>{escape(l)}</span></div>' for v, l in items
    )
    return f'<div class="stats">{inner}</div>'


def icon_tiles(hubs: list[dict], depth: int) -> str:
    p = pfx(depth)
    tiles = []
    for h in hubs:
        tiles.append(
            f'<a class="icon-tile" href="{p}{h["slug"]}/index.html">'
            f'{svg_icon(h.get("icon", "briefcase"))}'
            f'<h3>{escape(h["short"])}</h3>'
            f'<p>{escape(h["blurb"][:90])}</p></a>'
        )
    return f'<div class="icon-grid">{"".join(tiles)}</div>'


def partners_html(names: list[str]) -> str:
    if not names:
        return ""
    badges = "".join(f'<span class="partner">{escape(n)}</span>' for n in names)
    return f'<div class="partners">{badges}</div>'


def insights_cards(articles: list[dict], depth: int, limit: int | None = None) -> str:
    p = pfx(depth)
    rows = articles[:limit] if limit else articles
    cards = []
    for a in rows:
        cards.append(
            f'<article class="insight"><div class="thumb"></div><div class="pad">'
            f'<small>{escape(a["kicker"])}</small>'
            f'<h3><a href="{p}insights/{a["slug"]}/index.html">{escape(a["title"])}</a></h3>'
            f'<p>{escape(a["excerpt"])}</p></div></article>'
        )
    return f'<div class="insight-grid">{"".join(cards)}</div>'


def how_it_works(steps: list[tuple[str, str]]) -> str:
    blocks = []
    for i, (title, body) in enumerate(steps, 1):
        blocks.append(
            f'<div class="card step"><b>{i}</b><h3>{escape(title)}</h3><p>{escape(body)}</p></div>'
        )
    return f'<div class="steps">{"".join(blocks)}</div>'


def benefits_html(items: list[tuple[str, str, str]]) -> str:
    cards = []
    for icon, title, body in items:
        cards.append(
            f'<div class="card">{svg_icon(icon, 36)}<h3>{escape(title)}</h3><p>{escape(body)}</p></div>'
        )
    return f'<div class="cols3">{"".join(cards)}</div>'


def faqs_html(items: list[tuple[str, str]]) -> str:
    import json

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
