#!/usr/bin/env python3
"""Generate the AHB NearMe OS Gate 1 staging factory site.

Gate 1 architecture:
- Shared chrome on every page including home
- Exactly 10 hubs x 10 children = 100 SVC-CHILD pages
- Staging-only noindex controls across HTML, robots.txt, and Netlify headers
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://ahbi.com"
LEGAL_NAME = "Abner Herrman & Brock LLC"
BRAND = "Abner Herrman & Brock"
SHORT_BRAND = "AHB"
PHONE = "(201) 484-2000"
PHONE_TEL = "+12014842000"
EMAIL = "info@ahbi.com"
ADDRESS = "Harborside 5, 185 Hudson Street, Suite 1640, Jersey City, NJ 07311"
HQ = "Jersey City, NJ"
FOUNDED = "1981"
TRADE = "Investment management / separately managed accounts (SMAs)"
STAGING_BANNER = (
    "STAGING PREVIEW — ahbi.com factory build · Abner Herrman & Brock · "
    "content pending owner review · not the live AHB website"
)


FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
:root{--navy:#0b1f3a;--navy2:#12345a;--gold:#c9a227;--gold2:#a8841f;--cream:#f8f4ea;--mist:#eef3f5;--ink:#172033;--muted:#607086;--line:#d8e0e6}
body{font-family:Arial,Helvetica,sans-serif;color:var(--ink);line-height:1.65;background:#fff}
h1,h2,h3,h4,.nav,.utility,.btn,.logo{font-family:"Segoe UI",Arial,Helvetica,sans-serif}
a{color:var(--navy2);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px}
.stage{background:#6b1f1f;color:#fff;font:800 12px "Segoe UI",sans-serif;letter-spacing:.04em;text-transform:uppercase;text-align:center;padding:8px 12px}
.utility{background:#071629;color:#dfe8f0;font-size:12.5px;padding:6px 0}
.utility .wrap{display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap}
header.main{background:#fff;border-bottom:3px solid var(--gold);position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-top:16px;padding-bottom:16px}
.logo{display:inline-flex;align-items:center;gap:12px;color:var(--navy);font-weight:850;font-size:25px;letter-spacing:.02em;text-decoration:none}
.logo-mark{display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border:2px solid var(--gold);border-radius:2px;background:var(--navy);color:var(--gold);font-weight:900}
.logo small{display:block;font-size:10.5px;color:var(--muted);font-weight:700;letter-spacing:1.4px;text-transform:uppercase;margin-top:1px}
.phone-cta{text-align:right;font-family:"Segoe UI",Arial,sans-serif}
.phone-cta a{font-size:19px;font-weight:850;color:var(--navy)}
.phone-cta small{display:block;color:var(--muted);font-size:11.5px}
nav.nav{background:var(--navy)}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav>div.wrap>ul>li>a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:700}
nav.nav>div.wrap>ul>li>a:hover{background:#142c4d;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:292px;box-shadow:0 12px 26px rgba(8,22,41,.22);border-top:3px solid var(--gold);z-index:60}
nav.nav .dd a{display:block;color:var(--ink);padding:10px 15px;font-size:13.5px;font-weight:600;border-bottom:1px solid var(--line);background:#fff}
nav.nav .dd a:hover{background:var(--mist);color:var(--navy);text-decoration:none}
.nav .em>a{background:var(--gold);color:#071629}.nav .em>a:hover{background:var(--gold2);color:#fff}
.hero{background:linear-gradient(135deg,rgba(11,31,58,.94),rgba(11,31,58,.87)),linear-gradient(45deg,#0b1f3a,#173b62);color:#fff;padding:72px 0 62px}
.hero h1{font-size:clamp(2rem,4vw,3.05rem);line-height:1.12;max-width:850px;margin-bottom:18px}
.hero p{max-width:780px;color:#dfe8f0;font-size:17px}
.hero .eyebrow,.kicker{display:inline-block;color:var(--gold);font:800 12px "Segoe UI",sans-serif;letter-spacing:.12em;text-transform:uppercase;margin-bottom:12px}
.hero-ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
.btn{display:inline-block;background:var(--gold);color:#071629;font:800 14px "Segoe UI",sans-serif;padding:12px 24px;border-radius:3px;border:0;cursor:pointer}
.btn:hover{background:var(--gold2);color:#fff;text-decoration:none}
.btn.alt{background:var(--navy);color:#fff}.btn.alt:hover{background:#173b62}
.btn.ghost{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.45)}.btn.ghost:hover{background:rgba(255,255,255,.08);color:#fff}
section{padding:46px 0}
section.tint{background:var(--mist)}
section.cream{background:var(--cream)}
section h2{font-size:27px;color:var(--navy);line-height:1.25;margin-bottom:15px}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:18px;color:#334155;max-width:840px}
.crumb{font-size:12.5px;color:var(--muted);padding:15px 0 0}.crumb a{color:var(--muted)}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:24px}.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:18px;margin-top:22px}
.card,.gcard,.hubcard{background:#fff;border:1px solid var(--line);border-radius:6px;box-shadow:0 3px 9px rgba(11,31,58,.06)}
.card{padding:24px}.gcard,.hubcard{padding:22px;border-left:5px solid var(--gold)}
.card h3,.gcard h3,.hubcard h3{font-size:18px;color:var(--navy);margin-bottom:8px}.gcard h3 a,.hubcard h3 a{color:var(--navy)}
.gcard p,.hubcard p{font-size:14.5px;color:var(--muted);margin:0}
.tag{display:inline-block;margin-top:12px;font:800 10.5px "Segoe UI",sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--gold2)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:24px}
.stat{background:#fff;border:1px solid var(--line);border-top:4px solid var(--gold);padding:20px;text-align:center;border-radius:6px}
.stat b{display:block;color:var(--navy);font-size:25px;line-height:1.1}.stat span{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;font-weight:800}
ul.checks{list-style:none;margin:10px 0}ul.checks li{padding:7px 0 7px 28px;position:relative}ul.checks li:before{content:"";position:absolute;left:1px;top:17px;width:12px;height:3px;background:var(--gold)}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin-top:22px}
.stepnum{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--navy);color:var(--gold);font-weight:900;margin-bottom:12px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--line);border-radius:6px;overflow:hidden;margin-top:18px}.vs .col{padding:24px}.vs .col.bad{background:#fff}.vs .col.good{background:var(--cream)}
.formbox{background:#fff;border:1px solid var(--line);border-top:4px solid var(--gold);border-radius:6px;padding:26px;max-width:680px}
.formbox label{display:block;font:800 12.5px "Segoe UI",sans-serif;color:var(--muted);margin:12px 0 4px}.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #b9c5cf;border-radius:3px;font:14px Arial,sans-serif}.formbox textarea{min-height:96px}
details{border:1px solid var(--line);border-radius:5px;margin-bottom:10px;background:#fff}details summary{cursor:pointer;padding:14px 18px;font:800 15px "Segoe UI",sans-serif;color:var(--navy);list-style:none}details summary:before{content:"+ ";color:var(--gold);font-weight:900}details[open] summary:before{content:"- "}details div{padding:0 18px 16px;font-size:15.5px}
.ctastrip{background:var(--navy);color:#fff;text-align:center;padding:38px 0}.ctastrip h2{color:#fff}.ctastrip p{color:#dfe8f0;max-width:760px;margin-left:auto;margin-right:auto}
footer{background:#071629;color:#c5d0dc;padding:42px 0 24px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:800 12.5px "Segoe UI",sans-serif;letter-spacing:.09em;text-transform:uppercase;margin-bottom:12px}footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#dfe8f0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:26px}.disclaimer{border-top:1px solid #223955;margin-top:28px;padding-top:16px;color:#aebdca;font-size:12.5px}.copy{margin-top:12px;text-align:center;color:#8fa0b2;font-size:12px}
@media(max-width:780px){.cols2,.vs{grid-template-columns:1fr}.phone-cta{text-align:left}.hero{padding:54px 0}.dd{position:static;box-shadow:none}.nav.nav li:hover>.dd{display:block}}
"""


HUB_DATA: list[tuple[str, str, str, list[str]]] = [
    (
        "core-equity-sma",
        "Core Equity SMA",
        "Large-cap equity account management focused on individual companies, disciplined research, and client-specific guidelines.",
        [
            "Large-Cap Core Equity",
            "High-Quality Value Stocks",
            "Growth Stock Selection",
            "Dividend Growth Equities",
            "Equity Concentration Limits",
            "Sector Allocation Oversight",
            "Equity Risk Parameters",
            "Equity Research Process",
            "Equity Rebalancing Discipline",
            "Equity Separate Accounts",
        ],
    ),
    (
        "taxable-bond-portfolios",
        "Taxable Bond Portfolios",
        "Investment-grade taxable fixed income portfolios built around income needs, credit quality, duration, and account-level customization.",
        [
            "Investment-Grade Taxable Bonds",
            "Corporate Bond Portfolios",
            "Government Bond Strategies",
            "Income Generation Focus",
            "Capital Preservation Bonds",
            "Duration Management",
            "Credit Quality Screening",
            "Laddered Bond Portfolios",
            "Taxable Fixed Income SMAs",
            "Bond Portfolio Customization",
        ],
    ),
    (
        "municipal-bond-strategies",
        "Municipal Bond Strategies",
        "Tax-exempt municipal bond portfolio management with attention to credit quality, after-tax income, and state-specific considerations.",
        [
            "Tax-Exempt Municipal Bonds",
            "State-Specific Muni Portfolios",
            "National Muni Strategies",
            "High-Quality Muni Credit",
            "Muni Income Planning",
            "After-Tax Yield Focus",
            "Muni Duration Control",
            "Essential-Service Munis",
            "Muni Ladder Construction",
            "Municipal Bond SMAs",
        ],
    ),
    (
        "core-balanced-solutions",
        "Core Balanced Solutions",
        "Balanced mandates combining equity and fixed income disciplines for clients seeking a coordinated risk and income framework.",
        [
            "Equity And Bond Blends",
            "Balanced Asset Allocation",
            "Risk-Targeted Balanced Portfolios",
            "Municipal Balanced Options",
            "Taxable Balanced Options",
            "Income Plus Growth Balance",
            "Conservative Balanced Mix",
            "Moderate Balanced Mix",
            "Dynamic Rebalancing",
            "Custom Balanced Mandates",
        ],
    ),
    (
        "separately-managed-accounts",
        "Separately Managed Accounts",
        "Customized SMA portfolio construction using individual stocks and bonds, transparent holdings, and account-specific guidelines.",
        [
            "Customized SMA Portfolios",
            "Direct Stock And Bond Ownership",
            "Discretionary Account Management",
            "Non-Discretionary Advisory Options",
            "Wrap Platform Availability",
            "SMA Minimum Account Guidance",
            "Transparent Holdings Reporting",
            "Personalized Investment Guidelines",
            "Multi-Account Household Management",
            "SMA Onboarding Process",
        ],
    ),
    (
        "financial-advisor-solutions",
        "Financial Advisor Solutions",
        "Advisor-focused SMA access, proposal support, transition planning, and nationwide availability through wrap platform relationships.",
        [
            "Advisor SMA Partnerships",
            "Broker-Dealer Wrap Access",
            "RIA Platform Availability",
            "Advisor Model Portfolios",
            "Advisor Client Proposals",
            "Existing Portfolio Reviews For Advisors",
            "Tax-Efficient Transitions For Advisors",
            "Advisor Support Desk",
            "Co-Branded Client Experience",
            "Nationwide Advisor Coverage",
        ],
    ),
    (
        "high-net-worth-wealth-management",
        "High-Net-Worth Wealth Management",
        "SMA portfolio management for high-net-worth individuals and families needing customization, tax awareness, and dedicated service.",
        [
            "High-Net-Worth SMAs",
            "Family Portfolio Customization",
            "Trust And Estate Accounts",
            "Concentrated Stock Management",
            "Tax-Sensitive HNW Portfolios",
            "Multi-Generational Wealth Mandates",
            "Charitable Giving Coordination",
            "Liquidity Planning Support",
            "Personalized Risk Budgets",
            "Dedicated Client Service Model",
        ],
    ),
    (
        "institutional-nonprofit-portfolios",
        "Institutional & Nonprofit Portfolios",
        "Portfolio management for nonprofits, foundations, corporations, retirement plans, and fiduciary committees.",
        [
            "Nonprofit Endowment Management",
            "Foundation Investment Mandates",
            "Corporate Treasury Portfolios",
            "Pension And Profit-Sharing Plans",
            "Fiduciary-Focused Portfolios",
            "Board And Trustee Reporting",
            "Spending Policy Alignment",
            "Institutional Fixed Income",
            "Institutional Equity Mandates",
            "Organization Portfolio Reviews",
        ],
    ),
    (
        "tax-efficient-portfolio-management",
        "Tax-Efficient Portfolio Management",
        "Tax-aware portfolio transition and ongoing management practices for taxable investors and advisor relationships.",
        [
            "Tax-Lot Awareness",
            "Tax-Efficient Security Transitions",
            "Municipal Vs Taxable Placement",
            "After-Tax Outcome Focus",
            "Realized Gain Budgeting",
            "Loss Harvesting Discipline",
            "Tax Transition Proposals",
            "Wash-Sale Awareness Process",
            "Custodial Tax Reporting Support",
            "Year-End Tax Coordination",
        ],
    ),
    (
        "portfolio-review-transition-services",
        "Portfolio Review & Transition Services",
        "Review, proposal, transition, and onboarding support for clients moving from existing holdings into AHB-managed mandates.",
        [
            "Existing Portfolio Review",
            "Formal Investment Proposal",
            "Custodian Transition Support",
            "Security-In-Kind Transfers",
            "Cash Raise Planning",
            "Benchmark And Mandate Fit",
            "Risk Tolerance Alignment",
            "Investment Policy Guidelines",
            "Onboarding Timeline Planning",
            "Ongoing Portfolio Monitoring",
        ],
    ),
]


SERVES = [
    "Financial advisors",
    "High-net-worth individuals and families",
    "Nonprofits and corporations",
]


STRATEGIES = [
    "Large-Cap Core Equity",
    "Taxable Bond",
    "Municipal Bond",
    "Core Balanced",
]


def slugify(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def child_blurb(hub_name: str, child_name: str) -> str:
    return (
        f"{child_name} support within the {hub_name} discipline, framed for customized "
        "separately managed accounts and client-specific investment guidelines."
    )


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
        f'<meta property="og:site_name" content="{escape(BRAND)}">\n'
        if canon
        else ""
    )
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex,nofollow">
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
    return f"""<div class="stage">{escape(STAGING_BANNER)}</div>
<div class="utility"><div class="wrap"><span>SEC-registered investment adviser · {escape(HQ)} · Founded {escape(FOUNDED)}</span><span><a style="color:#dfe8f0" href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a></span></div></div>
<header class="main"><div class="wrap">
<a class="logo" href="{p}index.html"><span class="logo-mark">AHB</span><span>{escape(BRAND)}<small>Customized SMA portfolio management</small></span></a>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Harborside, Jersey City · Nationwide via advisor platforms</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-ahb/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-ahb/index.html">About AHB</a>
<a href="{p}about-ahb/why-choose-ahb/index.html">Why Choose AHB</a>
<a href="{p}about-ahb/who-we-serve/index.html">Who We Serve</a>
</div></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li class="em"><a href="{p}schedule-a-call/index.html">Schedule a Call</a></li>
</ul></div></nav>
"""


def footer(depth: int) -> str:
    p = pfx(depth)
    hubs = "".join(
        f'<li><a href="{p}{h["slug"]}/index.html">{escape(h["short"])}</a></li>' for h in HUBS
    )
    return f"""<footer><div class="wrap"><div class="fcols">
<div><h4>Strategies &amp; Services</h4><ul>{hubs}</ul></div>
<div><h4>About</h4><ul>
<li><a href="{p}about-ahb/index.html">About AHB</a></li>
<li><a href="{p}about-ahb/why-choose-ahb/index.html">Why Choose AHB</a></li>
<li><a href="{p}about-ahb/who-we-serve/index.html">Who We Serve</a></li>
<li><a href="{p}contact/index.html">Contact</a></li>
</ul></div>
<div><h4>Start a Conversation</h4><ul>
<li><a href="{p}schedule-a-call/index.html">Schedule a Call</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Office</h4><ul><li>{escape(LEGAL_NAME)}</li><li>{escape(ADDRESS)}</li><li>{escape(TRADE)}</li></ul></div>
</div>
<div class="disclaimer"><strong>Important information:</strong> {escape(LEGAL_NAME)} is described here as an SEC-registered investment adviser. Registration with the SEC does not imply a certain level of skill or training. Past performance is not a guarantee of future results. This staging preview references Form CRS and ADV Part 2A conceptually for owner review only; it does not provide, replace, or link to legal disclosure documents. Content is pending AHB compliance review before any public use.</div>
<div class="copy">Copyright &copy; 2026 {escape(BRAND)}. Staging preview for ahbi.com; not the live AHB website.</div>
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
        "@type": "FinancialService",
        "name": BRAND,
        "legalName": LEGAL_NAME,
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "url": BASE + "/",
        "foundingDate": FOUNDED,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Harborside 5, 185 Hudson Street, Suite 1640",
            "addressLocality": "Jersey City",
            "addressRegion": "NJ",
            "postalCode": "07311",
            "addressCountry": "US",
        },
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(data, ensure_ascii=True)
        + "</script>"
    )


def strategy_cards() -> str:
    return "".join(
        f'<div class="gcard"><h3>{escape(strategy)}</h3><p>One of the four core strategies cited from ahbi.com as of Mar 31, 2026.</p><span class="tag">Core strategy</span></div>'
        for strategy in STRATEGIES
    )


def form_shell(form_name: str) -> str:
    strategy_options = "".join(f"<option>{escape(s)}</option>" for s in STRATEGIES)
    audience_options = "".join(f"<option>{escape(s)}</option>" for s in SERVES)
    return f"""<div class="formbox">
<label>First Name</label><input type="text" name="first_name">
<label>Last Name</label><input type="text" name="last_name">
<label>Email</label><input type="email" name="email">
<label>Phone</label><input type="tel" name="phone">
<label>I am a</label><select name="audience"><option>Please choose...</option>{audience_options}<option>Other [confirm]</option></select>
<label>Strategy Interest</label><select name="strategy"><option>Please choose...</option>{strategy_options}<option>Portfolio review / transition</option><option>Not sure yet</option></select>
<label>Current Custodian or Platform [confirm]</label><input type="text" name="platform" placeholder="Optional">
<label>Message</label><textarea name="message" placeholder="Tell us what you would like AHB to review. Please do not submit account numbers or sensitive personal information."></textarea><br><br>
<button class="btn">{escape(form_name)}</button>
<p style="margin-top:12px;font-size:12px;color:#607086">Form shell for staging review. Final routing, privacy language, and compliance disclosures must be confirmed by AHB before public launch.</p>
</div>"""


def stats_block() -> str:
    stats = [
        ("~$3B", "AUM"),
        ("4", "Core strategies"),
        ("$250K", "Minimum account size"),
        ("~30", "Average years industry experience"),
    ]
    return (
        '<div class="stats">'
        + "".join(
            f'<div class="stat"><b>{escape(num)}</b><span>{escape(label)}</span></div>'
            for num, label in stats
        )
        + "</div><p style=\"font-size:12.5px;color:#607086;margin-top:10px\">Public site claims cited from ahbi.com as of Mar 31, 2026; owner/compliance confirmation required before publication. [confirm]</p>"
    )


def home() -> str:
    hub_cards = []
    for h in HUBS:
        kids = "".join(
            f'<li><a href="{h["slug"]}/{s}/index.html">{escape(n)}</a></li>'
            for s, n, _ in h["children"][:3]
        )
        hub_cards.append(
            f'<div class="hubcard"><h3><a href="{h["slug"]}/index.html">{escape(h["name"])}</a></h3>'
            f"<p>{escape(h['blurb'])}</p><ul class=\"checks\">{kids}</ul>"
            f'<a href="{h["slug"]}/index.html" style="font-weight:800">Explore {escape(h["short"]).lower()} &rarr;</a></div>'
        )
    desc = (
        "Abner Herrman & Brock is an SEC-registered investment adviser in Jersey City, "
        "focused on customized separately managed accounts."
    )
    return (
        head(f"{BRAND} | Customized SMA Portfolio Management", desc, canonical=f"{BASE}/")
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap">
<span class="eyebrow">Customized separately managed accounts</span>
<h1>{escape(BRAND)} builds actively managed portfolios around client guidelines.</h1>
<p>{escape(SHORT_BRAND)} is a Jersey City investment management firm founded in {escape(FOUNDED)}, serving financial advisors, high-net-worth families, nonprofits, and corporations with individual stock and bond portfolios rather than mutual funds or ETFs as primary vehicles.</p>
<div class="hero-ctas">
<a class="btn" href="schedule-a-call/index.html">Schedule a Call</a>
<a class="btn ghost" href="request-a-proposal/index.html">Request a Proposal</a>
<a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a>
</div></div></div>
<section class="cream"><div class="wrap">
<div class="kicker">Public site claims</div>
<h2>AHB at a glance</h2>
<p class="lead">The figures below are cited from ahbi.com as of Mar 31, 2026 and should be confirmed by AHB before publication. [confirm]</p>
{stats_block()}
</div></section>
<section><div class="wrap"><div class="cols2">
<div><div class="kicker">Approach</div><h2>Individual securities, customized mandates, and a team investment process.</h2>
<p>AHB's differentiated positioning is active management of customized SMAs, with portfolios invested in individual stocks and bonds. Client guidelines, tax considerations, account restrictions, and transition needs can be reflected directly in the account.</p>
<ul class="checks"><li>Investment Policy Committee team approach.</li><li>Tax-efficient transition planning for existing holdings.</li><li>Separate account transparency and individual security ownership.</li><li>Nationwide availability through advisor and wrap platform relationships.</li></ul></div>
<div class="card"><h3>Who AHB serves</h3><p>AHB works with advisors and end clients who need institutional discipline with account-level customization.</p><ul class="checks"><li>Financial advisors and platform partners.</li><li>High-net-worth individuals and families.</li><li>Nonprofits, foundations, corporations, and fiduciary committees.</li></ul></div>
</div></div></section>
<section class="tint"><div class="wrap"><div class="kicker">Core strategies</div><h2>Four core strategy areas</h2><div class="grid">{strategy_cards()}</div></div></section>
<section><div class="wrap"><div class="kicker">Factory map</div><h2>Explore AHB service pages</h2><p class="lead">Gate 1 organizes AHB's service surface into 10 hubs and 100 child pages for owner review.</p><div class="cols3">{''.join(hub_cards)}</div></div></section>
"""
        + faqs(
            [
                (
                    "Is this the live AHB website?",
                    "No. This is a staging preview for ahbi.com factory build review and is intentionally marked noindex,nofollow.",
                ),
                (
                    "What is AHB's account minimum?",
                    "The staging content cites a $250K minimum account size from ahbi.com as of Mar 31, 2026; AHB should confirm this before publication.",
                ),
                (
                    "Does SEC registration imply investment skill?",
                    "No. Registration with the SEC does not imply a certain level of skill or training.",
                ),
            ]
        )
        + f"""
<div class="ctastrip"><div class="wrap"><h2>Discuss an AHB-managed account or advisor relationship.</h2><p>Contact the Jersey City office or request a proposal for a customized SMA review.</p><a class="btn" href="schedule-a-call/index.html">Schedule a Call</a> <a class="btn alt" href="contact/index.html">Contact AHB</a></div></div>
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
        head(f"{h['name']} | {BRAND}", f"{h['name']} from {BRAND}. {h['blurb']}", canonical=f"{BASE}/{h['slug']}/")
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Service hub</div><h2>{escape(h["name"])} for customized AHB account mandates</h2>
<p class="lead">{escape(h["blurb"])} This hub is written for owner review and should be confirmed against AHB's advisory, platform, and compliance language. [confirm]</p>
<p><a class="btn" href="../schedule-a-call/index.html">Schedule a Call</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p></div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Pages</h2><div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>How this fits AHB's SMA model</h2><ul class="checks">
<li>Portfolio guidelines can be reflected in a separately managed account mandate.</li>
<li>Individual securities support transparency and customization.</li>
<li>The Investment Policy Committee team approach supports consistent review.</li>
<li>Tax-aware transitions can be discussed before replacing existing holdings.</li>
<li>Advisor and wrap platform availability should be confirmed for each relationship. [confirm]</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What is included in {h['name']}?", h["blurb"]),
                (
                    "Is this a performance claim?",
                    "No. This staging page describes service capabilities only and does not include performance returns, rankings, or testimonials.",
                ),
                (
                    "Who should review this page before launch?",
                    "AHB ownership and compliance reviewers should confirm service scope, disclosures, platform references, and form handling before publication.",
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
        head(f"{name} | {BRAND}", f"{name} from {BRAND}. {blurb}", canonical=f"{BASE}/{h['slug']}/{slug}/")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">SVC-CHILD</div><h2>{escape(name)} within AHB's customized SMA framework</h2>
<p class="lead">{escape(blurb)} AHB's model emphasizes direct ownership of individual securities, active management, and account-level customization.</p>
<p><a class="btn" href="../../schedule-a-call/index.html">Schedule a Call</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p></div></section>
<section class="tint"><div class="wrap"><h2>Client conversations this page supports</h2><ul class="checks">
<li>Whether the mandate should be equity, fixed income, municipal, balanced, or transition-focused.</li>
<li>How tax sensitivity, cash flow, risk tolerance, and restrictions affect account construction.</li>
<li>How existing holdings may transition into an AHB-managed account over time.</li>
<li>Whether an advisor, family, nonprofit, corporation, or fiduciary committee is the decision maker.</li>
<li>Which custodian, wrap platform, or reporting pathway needs to be confirmed.</li>
</ul></div></section>
<section><div class="wrap"><h2>AHB positioning for {escape(name.lower())}</h2><p>Rather than treating this topic as a generic model portfolio, the AHB staging content frames it as a customized separate account discussion. Final copy should be checked against current Form CRS, ADV Part 2A, platform availability, fee language, and any client-specific suitability requirements. [confirm]</p></div></section>
<section class="cream"><div class="wrap"><div class="vs">
<div class="col bad"><h3>Generic pooled-fund framing</h3><ul class="checks"><li>One-size-fits-all vehicle language.</li><li>Limited account-level tax and restriction discussion.</li><li>Little visibility into individual security ownership.</li></ul></div>
<div class="col good"><h3>AHB separate account framing</h3><ul class="checks"><li>Individual stocks and bonds as primary implementation vehicles.</li><li>Investment Policy Committee review discipline.</li><li>Tax-aware transitions and client-specific guidelines.</li></ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Review {escape(name.lower())} with AHB.</h2><p>Use the staging form to request a proposal or schedule an introductory call with the Jersey City office.</p><a class="btn" href="../../schedule-a-call/index.html">Schedule a Call</a> <a class="btn alt" href="../../contact/index.html">Contact AHB</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"Does {name.lower()} guarantee an investment result?",
                    "No. This page describes a service topic only. Past performance is not a guarantee of future results.",
                ),
                (
                    "Is the content ready for publication?",
                    "No. This is a noindex staging page pending owner and compliance review.",
                ),
            ]
        )
        + f'<section><div class="wrap"><h2>Related {escape(h["short"])} Pages</h2><div class="grid">{related}</div></div></section>'
        + footer(2)
    )


def cta_page(slug: str, title: str, h2: str, lead: str, button: str) -> str:
    steps = {
        "contact": [
            ("Call or email Jersey City", f"Reach AHB at {PHONE} or {EMAIL}."),
            ("Use the staging inquiry form", "Share the strategy, audience, and review need without sensitive account information."),
            ("Confirm next steps", "AHB must confirm routing, privacy language, and disclosure language before launch."),
        ],
        "request-a-proposal": [
            ("Describe the mandate", "Identify equity, taxable bond, municipal bond, balanced, or transition needs."),
            ("Review existing holdings", "Discuss tax, risk, and restriction considerations before proposing a transition."),
            ("Document assumptions", "Proposal copy should align with current disclosure documents and approved platform language."),
        ],
        "schedule-a-call": [
            ("Choose a discussion topic", "Advisor relationship, family account, nonprofit portfolio, or transition review."),
            ("Prepare key constraints", "Bring objectives, risk considerations, tax sensitivity, and current custody details."),
            ("Leave with a review path", "AHB can confirm whether a proposal or portfolio review is the right next step."),
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
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Start a conversation</div><h2>{escape(h2)}</h2><p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">{step_cards}</div>{form_shell(button)}</div></section>
<section class="tint"><div class="wrap"><h2>AHB contact details</h2><p><strong>{escape(LEGAL_NAME)}</strong><br>{escape(ADDRESS)}<br>Phone: <a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><br>Email: <a href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a></p></div></section>
"""
        + (org_schema() if slug == "contact" else "")
        + footer(1)
    )


def about_page() -> str:
    return (
        head(f"About {BRAND} | Jersey City, NJ", f"About {LEGAL_NAME}, founded in {FOUNDED} and headquartered in Jersey City.", canonical=f"{BASE}/about-ahb/")
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About AHB</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">About AHB</div><h2>{escape(BRAND)} is a Jersey City investment management firm focused on customized SMAs.</h2>
<p class="lead">{escape(LEGAL_NAME)} was founded in {escape(FOUNDED)} and is headquartered at Harborside in {escape(HQ)}. The firm serves advisors, high-net-worth investors, families, nonprofits, and corporations through actively managed separate account strategies.</p></div></section>
<section class="cream"><div class="wrap"><h2>Facts for owner confirmation</h2>{stats_block()}</div></section>
<section><div class="wrap"><div class="cols2"><div><h2>Investment approach</h2><p>AHB emphasizes individual stock and bond portfolios, customized guidelines, tax-efficient transitions, and Investment Policy Committee oversight. Final published language should be reconciled to current disclosure materials.</p></div><div class="card"><h3>About pages</h3><ul class="checks"><li><a href="why-choose-ahb/index.html">Why Choose AHB</a></li><li><a href="who-we-serve/index.html">Who We Serve</a></li></ul></div></div></div></section>
"""
        + faqs(
            [
                ("Where is AHB headquartered?", f"AHB is headquartered at {ADDRESS}."),
                ("When was AHB founded?", f"This staging site lists AHB as founded in {FOUNDED}."),
                ("What needs confirmation?", "All facts, disclosure language, form routing, platform references, and any regulatory references require AHB owner/compliance review."),
            ]
        )
        + org_schema()
        + footer(1)
    )


def why_page() -> str:
    return (
        head(f"Why Choose {SHORT_BRAND} | {BRAND}", "Why advisors and clients may consider AHB for customized SMA management.", canonical=f"{BASE}/about-ahb/why-choose-ahb/")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About AHB</a> &rsaquo; Why Choose AHB</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Why choose AHB</div><h2>Customization, individual securities, and a disciplined team process.</h2><p class="lead">This staging page summarizes AHB differentiators without performance claims, rankings, or testimonials.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Customized SMAs</h3><p>Separate account mandates can reflect restrictions, risk preferences, income needs, and tax considerations.</p></div>
<div class="card"><h3>Individual securities</h3><p>AHB positions portfolios around individual stocks and bonds rather than mutual funds or ETFs as primary vehicles.</p></div>
<div class="card"><h3>IPC team process</h3><p>An Investment Policy Committee team approach supports consistency across research, allocation, and review.</p></div>
<div class="card"><h3>Tax-aware transitions</h3><p>Existing holdings can be reviewed with attention to realized gains, tax lots, and transition pacing.</p></div>
<div class="card"><h3>Advisor access</h3><p>Nationwide advisor relationships and wrap platform references should be confirmed before publication. [confirm]</p></div>
<div class="card"><h3>Jersey City roots</h3><p>AHB is headquartered at Harborside in Jersey City, NJ.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Discuss whether AHB fits a mandate.</h2><a class="btn" href="../../schedule-a-call/index.html">Schedule a Call</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + footer(2)
    )


def who_page() -> str:
    groups = [
        ("Financial Advisors", "SMA access, proposal support, existing portfolio reviews, tax-efficient transition planning, and platform availability conversations."),
        ("Individuals & Families", "High-net-worth and family mandates that may involve tax sensitivity, concentrated positions, trusts, estates, and multi-account coordination."),
        ("Nonprofits & Corporations", "Endowment, foundation, treasury, pension, profit-sharing, and fiduciary-focused portfolio conversations."),
    ]
    cards = "".join(
        f'<div class="card"><h3>{escape(name)}</h3><p>{escape(body)}</p></div>'
        for name, body in groups
    )
    return (
        head(f"Who We Serve | {BRAND}", "Financial advisors, individuals and families, nonprofits, and corporations served by AHB.", canonical=f"{BASE}/about-ahb/who-we-serve/")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About AHB</a> &rsaquo; Who We Serve</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Who we serve</div><h2>Advisor, family, nonprofit, and corporate portfolio relationships.</h2><p class="lead">AHB's audience includes financial advisors, high-net-worth individuals and families, nonprofits, and corporations.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">{cards}</div></div></section>
<section><div class="wrap"><h2>Common needs</h2><ul class="checks"><li>Customized investment policy guidelines.</li><li>Direct stock and bond ownership in separate accounts.</li><li>Tax-efficient transitions from existing portfolios.</li><li>Reporting and communication appropriate to the client or committee.</li></ul></div></section>
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
        ["/", "HOME", "", "abner herrman brock", "logo/home", "A1,A6,A10", ""],
        ["/about-ahb/", "COMP-HUB", "/", "about abner herrman brock", "About menu", "A1,A5,A6", ""],
        ["/about-ahb/why-choose-ahb/", "COMP-CHILD", "/about-ahb/", "why choose ahb", "About menu", "A10,A12", ""],
        ["/about-ahb/who-we-serve/", "COMP-CHILD", "/about-ahb/", "who ahb serves", "About menu", "C1,C2,C3", ""],
        ["/contact/", "COMP-CONTACT", "/", "contact ahb", "Contact menu", "A3,A4,A5", "Contact Request"],
        ["/request-a-proposal/", "FORM-PROPOSAL", "/", "ahb proposal", "nav utility", "I1", "Request for Proposal"],
        ["/schedule-a-call/", "FORM-CONSULT", "/", "schedule call ahb", "nav highlighted", "I1", "Consultation Request"],
    ]
    for h in HUBS:
        rows.append(
            [
                f"/{h['slug']}/",
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
                    f"/{h['slug']}/",
                    n.lower(),
                    "Services menu > hub grid",
                    "B row",
                    "Schedule a Call",
                ]
            )
    with (ROOT / "AHBI-PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def write_questionnaire() -> None:
    hub_slugs = " | ".join(h["slug"] for h in HUBS)
    strategies = "\n".join(f"- {s}" for s in STRATEGIES)
    serve = "\n".join(f"- {s}" for s in SERVES)
    write(
        ROOT / "AHBI-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire - AHB Factory Pages

Home page and factory pages share one chrome: utility bar, AHB logo/phone, Services dropdown, About dropdown, Contact, and highlighted Schedule a Call CTA.

## A - Business identity
| Field | Value | Source |
|---|---|---|
| A1 legal_name | {LEGAL_NAME} | user-provided business facts |
| A2 brand | AHB / {BRAND} | user-provided business facts |
| A3 domain | {BASE} | user-provided business facts |
| A4 phone | {PHONE} / tel:{PHONE_TEL} | user-provided business facts |
| A5 email | {EMAIL} | user-provided business facts |
| A6 address | {ADDRESS} | user-provided business facts |
| A7 HQ | {HQ} (Harborside) | user-provided business facts |
| A8 founded | {FOUNDED} | user-provided business facts |
| A9 trade | {TRADE} | user-provided business facts |
| A10 differentiator | Actively managed customized SMAs; individual stocks and bonds; Investment Policy Committee team approach; tax-efficient transitions; nationwide via wrap platforms | user-provided business facts |

## B - Public site claims to confirm
- Cited from ahbi.com as of Mar 31, 2026:
  - ~$3B AUM
  - 4 strategies
  - $250K minimum account size
  - ~30 average years industry experience
- These require owner/compliance confirmation before publication. [confirm]

## C - Core strategies
{strategies}

## D - Audiences served
{serve}

## E - Gate 1 taxonomy
- Hubs: {len(HUBS)}
- SVC-CHILD pages: {sum(len(h['children']) for h in HUBS)}
- Hub slugs: {hub_slugs}
- Full URL map: `AHBI-PAGE-INVENTORY.csv`

## F - Forms and CTAs
- Primary CTA: `schedule-a-call` (FORM-CONSULT)
- Secondary CTA: `request-a-proposal`
- Company/contact CTA: `contact`
- Form shells must be wired with AHB-approved privacy, retention, and compliance language before public use.

## G - Staging and compliance
- HTML uses `<meta name="robots" content="noindex,nofollow">`.
- `robots.txt` disallows all crawling.
- `netlify.toml` sends `X-Robots-Tag: noindex, nofollow`.
- Every footer includes SEC registration, past performance, and Form CRS / ADV Part 2A conceptual disclosure text.
- No performance returns, rankings, or testimonials are invented.
""",
    )


def write_notes() -> None:
    write(
        ROOT / "AHBI-NOTES.md",
        f"""# AHBI Factory Build Notes

- Branch: `cursor/ahbi-factory-127e`
- Domain target: {BASE}
- Build type: NearMe OS Website Factory Gate 1 staging preview
- Page model: 10 service hubs x 10 children = 100 SVC-CHILD pages
- Total generated `index.html` pages: 117 expected
- Staging controls: HTML noindex,nofollow; robots.txt `Disallow: /`; Netlify `X-Robots-Tag: noindex, nofollow`
- Visual direction: professional RIA / wealth management, deep navy `#0b1f3a`, gold `#c9a227`, cream/mist backgrounds
- Compliance note: Footer disclosure appears on every generated HTML page. Final content requires AHB owner/compliance approval before public launch.
- Public claims are cited as from ahbi.com as of Mar 31, 2026 and marked for confirmation where needed. [confirm]
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

    write(ROOT / "about-ahb" / "index.html", about_page())
    urls.append("/about-ahb/")
    write(ROOT / "about-ahb" / "why-choose-ahb" / "index.html", why_page())
    urls.append("/about-ahb/why-choose-ahb/")
    write(ROOT / "about-ahb" / "who-we-serve" / "index.html", who_page())
    urls.append("/about-ahb/who-we-serve/")

    for slug, title, h2, lead, button in [
        (
            "contact",
            f"Contact {BRAND}",
            f"Contact {BRAND}",
            "Call, email, or send a staging inquiry to the AHB Jersey City office.",
            "Contact AHB",
        ),
        (
            "request-a-proposal",
            f"Request a Proposal | {BRAND}",
            "Request an AHB Proposal",
            "Share the mandate, audience, strategy interest, and current portfolio context for an AHB proposal conversation.",
            "Request a Proposal",
        ),
        (
            "schedule-a-call",
            f"Schedule a Call | {BRAND}",
            "Schedule a Call with AHB",
            "Discuss advisor access, family wealth, nonprofit, corporate, or transition needs with AHB.",
            "Schedule a Call",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead, button))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head(f"Page Not Found | {BRAND}", "Page not found.")
        + chrome(0)
        + f"""
<section style="padding:72px 0"><div class="wrap"><h2>Page not found</h2>
<p class="lead">That URL is not in the AHB staging factory map. Return home or contact the Jersey City office.</p>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn alt" href="schedule-a-call/index.html">Schedule a Call</a></p>
</div></section>
"""
        + footer(0),
    )

    write_static_files(urls)
    write_inventory()
    write_questionnaire()
    write_notes()

    pages = list(ROOT.rglob("index.html"))
    inventory_children = 0
    with (ROOT / "AHBI-PAGE-INVENTORY.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["type_id"] == "SVC-CHILD":
                inventory_children += 1

    print(f"Index pages on disk: {len(pages)}")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)}")
    print(f"SVC-CHILD inventory rows: {inventory_children}")
    print("Home uses shared factory chrome: yes")
    print("Staging noindex controls: yes")


if __name__ == "__main__":
    main()
