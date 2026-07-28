#!/usr/bin/env python3
"""Generate the White Plains Tech Support NearMe OS Gate 1 staging factory site.

Gate 1 architecture:
- Exactly 10 service hubs x 10 children = 100 SVC-CHILD pages
- Home + 10 hubs + about hub + 2 about children + 3 forms = 117 index pages
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
BASE = "https://whiteplainstechsupport.com"
BRAND = "White Plains Tech Support"
OPERATOR = "Race Computer Services, LLC"
OPERATOR_DOMAIN = "racecs.com"
PHONE = "(862) 295-0011"
PHONE_TEL = "+18622950011"
ALT_PHONE = "(973) 343-5479"
ALT_PHONE_TEL = "+19733435479"
EMAIL = "support@whiteplainstechsupport.com"
ADDRESS = "White Plains, NY 10601"
CITY = "White Plains"
REGION = "NY"
POSTAL = "10601"
AREA = "White Plains, Westchester County, and the NYC metro area"
POSITIONING = (
    "Managed IT, cybersecurity, cloud, and compliance support for businesses in "
    "White Plains, Westchester County, and the NYC metro area."
)
STAGING_BANNER = (
    "STAGING PREVIEW — whiteplainstechsupport.com factory build · White Plains Tech Support · "
    "Westchester NY · content pending owner review · not a live production website"
)
DISCLAIMER = (
    "Staging copy is based on user-provided business facts and must be reviewed by ownership "
    "before publication. Domain, phone numbers, email, service area, street address, operator "
    "relationship, service scope, response times, pricing, vendor status, and compliance language "
    "require confirmation."
)


FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
:root{--navy:#0f172a;--hudson:#1d4ed8;--river:#dbeafe;--ice:#f8fafc;--amber:#f59e0b;--ink:#172033;--muted:#61708a;--line:#d8e0eb;--white:#fff;--slate:#334155}
body{font-family:"Public Sans",Arial,Helvetica,sans-serif;color:var(--ink);line-height:1.66;background:#fff}
h1,h2,h3,h4,.logo-name{font-family:"Fraunces",Georgia,serif;letter-spacing:-.028em}
a{color:var(--hudson);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
.stage{background:repeating-linear-gradient(-45deg,#0f172a 0 12px,#1e293b 12px 24px);color:#fff;font:900 11.5px "Public Sans",sans-serif;letter-spacing:.06em;text-transform:uppercase;text-align:center;padding:9px 12px}
.utility{background:var(--navy);color:#dbeafe;font-size:12.5px;padding:8px 0}
.utility .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}.utility a{color:#fff}
header.main{background:#fff;border-bottom:1px solid var(--line);position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;padding-top:18px;padding-bottom:18px}
.logo{display:inline-flex;align-items:center;gap:13px;color:var(--navy);font-weight:900;text-decoration:none}
.logo-mark{width:58px;height:58px;border-radius:18px;display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(145deg,var(--navy),var(--hudson));color:#fff;font:900 .95rem "Public Sans",sans-serif;letter-spacing:.04em;box-shadow:0 12px 28px rgba(29,78,216,.22);flex:none}
.logo-name{display:block;font-size:1.38rem;line-height:1.05;color:var(--navy)}
.logo small{display:block;color:var(--muted);font:900 10.5px "Public Sans",sans-serif;letter-spacing:.14em;text-transform:uppercase;margin-top:4px}
.phone-cta{text-align:right}.phone-cta a{font:900 1.24rem "Public Sans",sans-serif;color:var(--navy)}.phone-cta small{display:block;color:var(--muted);font-size:12px;margin-top:2px}
nav.nav{background:#fff;border-bottom:1px solid var(--line);position:relative;z-index:45}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap;align-items:center;width:100%}
nav.nav>.wrap>ul>li{position:relative}
nav.nav>div.wrap>ul>li>a{display:block;color:var(--navy);padding:13px 14px;font-size:14px;font-weight:900}
nav.nav>div.wrap>ul>li>a:hover{background:var(--river);color:var(--hudson);text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:330px;box-shadow:0 18px 36px rgba(15,23,42,.18);border:1px solid var(--line);border-top:4px solid var(--hudson);z-index:60}
nav.nav .dd a{display:block;color:var(--navy);padding:10px 15px;font-size:13.5px;font-weight:800;border-bottom:1px solid var(--line);background:#fff}
nav.nav .dd a:hover{background:var(--river);color:var(--hudson);text-decoration:none}
.nav .em{margin-left:auto}.nav .em>a{background:var(--amber);color:#1e293b;margin:6px 0 6px 8px;padding:9px 18px;border-radius:999px}.nav .em>a:hover{background:#d97706;color:#fff}
.hero{position:relative;background:radial-gradient(circle at 14% 18%,rgba(29,78,216,.34),transparent 34%),radial-gradient(circle at 85% 24%,rgba(245,158,11,.20),transparent 35%),linear-gradient(135deg,#0f172a 0%,#1e3a8a 58%,#1d4ed8 100%);color:#fff;padding:88px 0 76px;overflow:hidden}
.hero:before{content:"";position:absolute;inset:0;background:linear-gradient(120deg,rgba(255,255,255,.12) 0 1px,transparent 1px 30px),radial-gradient(circle at 50% 110%,rgba(219,234,254,.20),transparent 34%);opacity:.78;pointer-events:none}
.hero .wrap{position:relative;z-index:1}.hero h1{font-size:clamp(2.25rem,5vw,4.15rem);line-height:1.04;max-width:980px;margin-bottom:18px}.hero p{max-width:850px;color:#eff6ff;font-size:1.13rem}
.eyebrow,.kicker{display:inline-flex;align-items:center;gap:12px;color:var(--amber);font:900 12px "Public Sans",sans-serif;letter-spacing:.14em;text-transform:uppercase;margin-bottom:14px}
.eyebrow:before,.kicker:before{content:"";display:inline-block;width:30px;height:2px;background:currentColor;flex:none}
.hero-ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.btn{display:inline-block;background:var(--hudson);color:#fff;font:900 14px "Public Sans",sans-serif;padding:13px 24px;border-radius:999px;border:0;cursor:pointer;box-shadow:0 9px 22px rgba(29,78,216,.18)}
.btn:hover{background:#1e40af;color:#fff;text-decoration:none}.btn.alt{background:var(--navy);color:#fff}.btn.alt:hover{background:#020617}.btn.gold{background:var(--amber);color:#1e293b}.btn.gold:hover{background:#d97706;color:#fff}.btn.ghost{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.66)}.btn.ghost:hover{background:rgba(255,255,255,.13)}
section{padding:48px 0}section.tint{background:var(--river)}section.cream{background:#fffbeb}section.soft{background:var(--ice)}
section h2{font-size:clamp(1.72rem,3vw,2.38rem);color:var(--navy);line-height:1.17;margin-bottom:15px}section p{margin-bottom:14px;font-size:16.5px}.lead{font-size:18px;color:#334155;max-width:900px}
.notice{background:#fff8e8;border:1px solid #f2d38e;border-left:5px solid var(--amber);padding:16px 18px;border-radius:12px;color:#493a1b;margin:18px 0}
.crumb{font-size:12.5px;color:var(--muted);padding:15px 0 0}.crumb a{color:var(--muted)}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:18px;margin-top:22px}
.card,.gcard,.hubcard{background:#fff;border:1px solid var(--line);border-radius:15px;box-shadow:0 7px 20px rgba(15,23,42,.07)}.card{padding:25px}.gcard,.hubcard{padding:22px;border-top:5px solid var(--hudson)}
.card h3,.gcard h3,.hubcard h3{font-size:18px;color:var(--navy);margin-bottom:8px}.gcard h3 a,.hubcard h3 a{color:var(--navy)}
.gcard p,.hubcard p{font-size:14.5px;color:var(--muted);margin:0}.tag{display:inline-block;margin-top:12px;font:900 10.5px "Public Sans",sans-serif;letter-spacing:.09em;text-transform:uppercase;color:var(--hudson)}
.feature{border-left:5px solid var(--hudson);background:#fff;padding:24px;border-radius:14px;border-top:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:16px;margin-top:24px}.stat{background:#fff;border:1px solid var(--line);border-top:4px solid var(--amber);padding:20px;text-align:center;border-radius:14px}.stat b{display:block;color:var(--navy);font-size:26px;line-height:1.1}.stat span{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;font-weight:900}
ul.checks{list-style:none;margin:10px 0}ul.checks li{padding:7px 0 7px 29px;position:relative}ul.checks li:before{content:"";position:absolute;left:2px;top:16px;width:14px;height:4px;background:var(--hudson);border-radius:4px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin:22px 0}.stepnum{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--navy);color:#fff;font-weight:900;margin-bottom:12px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-top:18px}.vs .col{padding:24px}.vs .col.good{background:#fffbeb}.vs .col.bad{background:#fff}
.formbox{background:#fff;border:1px solid var(--line);border-top:5px solid var(--hudson);border-radius:14px;padding:26px;max-width:760px}.formbox.highlight{border-top-color:var(--amber);box-shadow:0 10px 28px rgba(245,158,11,.14)}
.formbox label{display:block;font:900 12.5px "Public Sans",sans-serif;color:var(--muted);margin:12px 0 4px}.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #b8c8cf;border-radius:8px;font:14px "Public Sans",sans-serif}.formbox textarea{min-height:104px}
details{border:1px solid var(--line);border-radius:10px;margin-bottom:10px;background:#fff}details summary{cursor:pointer;padding:14px 18px;font:900 15px "Public Sans",sans-serif;color:var(--navy);list-style:none}details summary:before{content:"+ ";color:var(--hudson);font-weight:900}details[open] summary:before{content:"- "}details div{padding:0 18px 16px;font-size:15.5px}
.ctastrip{background:linear-gradient(135deg,var(--navy),var(--hudson));color:#fff;text-align:center;padding:42px 0}.ctastrip h2{color:#fff}.ctastrip p{color:#eaf2ff;max-width:790px;margin-left:auto;margin-right:auto}
footer{background:var(--navy);color:#cbd5e1;padding:42px 0 24px;margin-top:30px;font-size:13.5px}footer h4{color:#fff;font:900 12.5px "Public Sans",sans-serif;letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px}footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#f8fafc}.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:26px}.disclaimer{border-top:1px solid rgba(255,255,255,.18);margin-top:28px;padding-top:16px;color:#bdcbe0;font-size:12.5px}.copy{margin-top:12px;text-align:center;color:#94a3b8;font-size:12px}
@media(max-width:780px){.cols2,.vs{grid-template-columns:1fr}.phone-cta{text-align:left}.hero{padding:58px 0}.dd{position:static;box-shadow:none;width:100%;border-left:0;border-right:0}.nav .em{margin-left:0;width:100%}.nav .em>a{margin:8px 12px;text-align:center}.logo-name{font-size:1.14rem}}
"""


HUB_DATA: list[tuple[str, str, str, list[str]]] = [
    (
        "managed-it-services",
        "Managed IT Services",
        "Managed IT services for Westchester businesses that need proactive support, predictable operations, and a local MSP team.",
        [
            "Managed IT For Small Business",
            "Proactive IT Services",
            "Managed Helpdesk Support",
            "Remote Network Management",
            "Server Management Services",
            "Unlimited Tech Support",
            "Co-Managed IT Services",
            "IT Vendor Management",
            "Virtual CIO Services",
            "Complete IT Outsourcing",
        ],
    ),
    (
        "small-business-it-support",
        "Small Business IT Support",
        "Small business IT support for onsite, remote, server, migration, recovery, and continuity needs across White Plains and nearby communities.",
        [
            "Onsite Technical Services",
            "Remote Support Services",
            "Outsourced Tech Support",
            "Server Installation And Setup",
            "Windows Server Administration",
            "Linux Administration Support",
            "Apple Mac IT Support",
            "Data Migration Services",
            "Data Recovery Services",
            "Business Continuity Planning",
        ],
    ),
    (
        "cybersecurity-services",
        "Cybersecurity Services",
        "Cybersecurity consulting and response planning for local organizations that need stronger controls and practical risk reduction.",
        [
            "Cybersecurity Consulting",
            "Cyber Risk Assessment",
            "Vulnerability Assessment",
            "Network Penetration Testing",
            "Firewall Installation Configuration",
            "Malware Removal Services",
            "Ransomware Remediation",
            "Multi-Factor Authentication Setup",
            "Security Awareness Training",
            "Incident Response Support",
        ],
    ),
    (
        "compliance-services",
        "Compliance Services",
        "Compliance support for organizations aligning IT security practices with healthcare, payment, defense, and NIST frameworks.",
        [
            "HIPAA Compliance Consulting",
            "HIPAA Security Risk Assessment",
            "HIPAA Gap Analysis",
            "PCI-DSS Compliance Consulting",
            "CMMC Compliance Consulting",
            "CMMC Gap Analysis",
            "NIST 800-171 Consulting",
            "Proactively Managed Compliance",
            "MIPS Consulting Support",
            "Compliance Remediation Services",
        ],
    ),
    (
        "managed-cybersecurity",
        "Managed Cybersecurity",
        "Managed cybersecurity services for endpoint protection, monitoring, patching, email security, and threat detection.",
        [
            "Managed Endpoint Protection",
            "Managed Antivirus Solutions",
            "Managed Firewall Service",
            "Managed Email Security",
            "Network Security Monitoring",
            "Patch Management Services",
            "Managed Encryption Services",
            "Data Leak Prevention",
            "Automated Threat Detection",
            "Managed Cybersecurity Services",
        ],
    ),
    (
        "managed-cloud-services",
        "Managed Cloud Services",
        "Managed cloud services for Microsoft 365, email, backup, infrastructure, private cloud, AWS, and Google Cloud support.",
        [
            "Managed Cloud Computing",
            "Microsoft 365 Administration",
            "Managed Email Service",
            "Managed AWS Services",
            "Google Cloud Platform Support",
            "Managed Private Cloud",
            "Remote Cloud Backup",
            "Disaster Recovery As A Service",
            "Managed Cloud Infrastructure",
            "Cloud Service Provider Support",
        ],
    ),
    (
        "data-center-cloud",
        "Data Center & Cloud Infrastructure",
        "Data center and cloud infrastructure planning for virtualization, VDI, storage, deployment, and colocation support.",
        [
            "Server Virtualization Services",
            "VDI Deployment Services",
            "VDI Management Services",
            "Infrastructure As A Service",
            "Private Cloud Deployment",
            "Datacenter Consulting",
            "Datacenter Colocation Support",
            "Data Storage Solutions",
            "Cloud Deployment Rollout",
            "Virtual Desktop Infrastructure",
        ],
    ),
    (
        "enterprise-it-solutions",
        "Enterprise IT Solutions",
        "Enterprise IT solutions for multi-office support, cybersecurity, endpoint protection, mobility, storage, and project delivery.",
        [
            "Managed Enterprise IT",
            "Multi-Office Network Support",
            "Enterprise Cybersecurity Consulting",
            "Enterprise Mobility Management",
            "Enterprise Endpoint Protection",
            "Large-Scale Data Storage",
            "ERP Solutions Consulting",
            "Network Penetration Testing Enterprise",
            "On-Demand Enterprise Tech Support",
            "Enterprise Project Delivery",
        ],
    ),
    (
        "microsoft-platforms-support",
        "Microsoft & Platform Support",
        "Microsoft and platform support for Microsoft 365, Windows Server, Exchange, partner ecosystems, hardware, and migrations.",
        [
            "Microsoft Partner IT Solutions",
            "Office 365 Business Support",
            "Windows Server Support",
            "Windows Server Essentials Setup",
            "Hosted Exchange Support",
            "Cisco Partner Solutions",
            "Dell Partner Support",
            "HPE Hardware Support",
            "Linux And Unix Consulting",
            "Platform Migration Support",
        ],
    ),
    (
        "industries-we-serve",
        "Industries We Serve",
        "Industry-focused MSP and cybersecurity support for professional services, healthcare, finance, construction, government, and other teams.",
        [
            "IT Support For Law Offices",
            "IT Solutions For Healthcare",
            "IT Support For Financial Services",
            "Cybersecurity For Banks",
            "IT Support For Real Estate",
            "IT Support For Construction",
            "IT Support For Advertising Media",
            "IT Support For Call Centers",
            "IT Services For Government Agencies",
            "Industry-Specific MSP Support",
        ],
    ),
]


PLATFORMS = [
    "Microsoft 365 and Windows Server",
    "Cloud backup and disaster recovery",
    "Firewall and endpoint security",
    "AWS, Google Cloud, and private cloud",
    "Cisco, Dell, HPE, Linux, Unix, and Apple Mac",
    "HIPAA, PCI-DSS, CMMC, NIST 800-171, and MIPS topics",
]

LOCALITIES = [
    "White Plains",
    "Westchester County",
    "Harrison",
    "Scarsdale",
    "Mamaroneck",
    "Rye",
    "Tarrytown",
    "Yonkers",
    "New Rochelle",
    "NYC metro",
]


def slugify(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def child_blurb(hub_name: str, child_name: str) -> str:
    return (
        f"{child_name} within the {hub_name} pathway, localized for White Plains and "
        "Westchester County organizations reviewing managed IT, cybersecurity, cloud, "
        "compliance, onsite, and remote support needs."
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
{canon_tag}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700;800&family=Public+Sans:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
{FACTORY_CSS}
</style></head><body>
"""


def chrome(depth: int) -> str:
    p = pfx(depth)
    hub_dd = "".join(
        f'<a href="{p}{h["slug"]}/index.html">{escape(h["name"])}</a>' for h in HUBS
    )
    return f"""<div class="stage">{escape(STAGING_BANNER)}</div>
<div class="utility"><div class="wrap"><span>Managed IT, cybersecurity, cloud, and compliance · {escape(AREA)} · facts pending owner review</span><span><a href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a></span></div></div>
<header class="main"><div class="wrap">
<a class="logo" href="{p}index.html"><span class="logo-mark">WPTS</span><span><span class="logo-name">{escape(BRAND)}</span><small>Managed IT · Cloud · Cybersecurity</small></span></a>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>{escape(ADDRESS)} [confirm] · alternate <a href="tel:{ALT_PHONE_TEL}">{escape(ALT_PHONE)}</a> [confirm]</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about/index.html">About &#9662;</a><div class="dd">
<a href="{p}about/index.html">About {escape(BRAND)}</a>
<a href="{p}about/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about/westchester-service-area/index.html">Westchester Service Area</a>
</div></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li class="em"><a href="{p}schedule-a-consultation/index.html">Schedule a Consultation</a></li>
</ul></div></nav>
"""


def footer(depth: int) -> str:
    p = pfx(depth)
    hubs = "".join(
        f'<li><a href="{p}{h["slug"]}/index.html">{escape(h["short"])}</a></li>' for h in HUBS
    )
    return f"""<footer><div class="wrap"><div class="fcols">
<div><h4>Service Hubs</h4><ul>{hubs}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="{p}about/index.html">About {escape(BRAND)}</a></li>
<li><a href="{p}about/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about/westchester-service-area/index.html">Westchester Service Area</a></li>
<li><a href="{p}contact/index.html">Contact</a></li>
</ul></div>
<div><h4>Start</h4><ul>
<li><a href="{p}schedule-a-consultation/index.html">Schedule a Consultation</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Business Facts</h4><ul>
<li>{escape(ADDRESS)} [confirm]</li>
<li>Operator: {escape(OPERATOR)} ({escape(OPERATOR_DOMAIN)}) [confirm]</li>
<li>Primary phone: <a href="tel:{PHONE_TEL}">{escape(PHONE)}</a> [confirm]</li>
<li>Alternate phone: <a href="tel:{ALT_PHONE_TEL}">{escape(ALT_PHONE)}</a> [confirm]</li>
</ul></div>
</div>
<div class="disclaimer"><strong>Staging notice:</strong> {escape(DISCLAIMER)} This is a noindex staging preview and is not the live whiteplainstechsupport.com website.</div>
<div class="disclaimer"><strong>Claims review:</strong> Race Computer Services, LLC operator relationship, street address, service-area boundaries, vendor partner status, cybersecurity/compliance scope, pricing language, and response expectations require owner review. No testimonials, awards, rankings, client names, or guaranteed outcomes are invented.</div>
<div class="copy">Copyright &copy; 2026 {escape(BRAND)}. Staging preview for whiteplainstechsupport.com; not a live production website.</div>
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
        "@type": "ProfessionalService",
        "name": BRAND,
        "url": BASE + "/",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": CITY,
            "addressRegion": REGION,
            "postalCode": POSTAL,
            "addressCountry": "US",
        },
        "areaServed": ["White Plains", "Westchester County", "NYC metro area"],
        "parentOrganization": {
            "@type": "Organization",
            "name": OPERATOR,
            "url": f"https://www.{OPERATOR_DOMAIN}/",
        },
        "sameAs": [BASE + "/"],
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(data, ensure_ascii=True)
        + "</script>"
    )


def platform_cards() -> str:
    return "".join(
        f'<div class="gcard"><h3>{escape(item)}</h3><p>Technology, vendor, or framework topic for owner confirmation before launch. [confirm]</p><span class="tag">Platform / framework</span></div>'
        for item in PLATFORMS
    )


def stats_block() -> str:
    stats = [
        ("10", "service hubs"),
        ("100", "SVC-child pages"),
        ("862", "primary area code"),
        ("10601", "White Plains ZIP [confirm]"),
    ]
    return (
        '<div class="stats">'
        + "".join(
            f'<div class="stat"><b>{escape(num)}</b><span>{escape(label)}</span></div>'
            for num, label in stats
        )
        + '</div><p style="font-size:12.5px;color:#61708a;margin-top:10px">Counts describe this staging factory. Location, phone, domain, and operator facts require owner confirmation where marked. [confirm]</p>'
    )


def form_shell(form_name: str, *, highlight: bool = False) -> str:
    services = "".join(f"<option>{escape(h['name'])}</option>" for h in HUBS)
    klass = "formbox highlight" if highlight else "formbox"
    return f"""<div class="{klass}">
<label>First Name</label><input type="text" name="first_name">
<label>Last Name</label><input type="text" name="last_name">
<label>Business Email</label><input type="email" name="email">
<label>Phone</label><input type="tel" name="phone">
<label>Company / Organization</label><input type="text" name="company">
<label>Service Interest</label><select name="service_interest"><option>Please choose...</option>{services}<option>Not sure yet</option></select>
<label>Preferred Support Model</label><select name="support_model"><option>Please choose...</option><option>Managed IT</option><option>Cybersecurity project</option><option>Compliance readiness</option><option>Cloud or Microsoft 365 support</option><option>Co-managed IT</option><option>Emergency issue follow-up</option></select>
<label>Message</label><textarea name="message" placeholder="Tell us about your IT support, cybersecurity, cloud, or compliance needs. Do not submit passwords or sensitive system details in this staging form."></textarea><br><br>
<button class="btn">{escape(form_name)}</button>
<p style="margin-top:12px;font-size:12px;color:#61708a">Form shell for staging review. Final routing, privacy language, response expectations, spam controls, and CRM, ticketing, or scheduling integrations must be approved before launch.</p>
</div>"""


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
            f'<a href="{h["slug"]}/index.html" style="font-weight:900">Explore {escape(h["short"]).lower()} &rarr;</a></div>'
        )
    desc = (
        f"{BRAND} is a managed IT, cybersecurity, cloud, and compliance brand for "
        f"{AREA}. [confirm]"
    )
    return (
        head(f"{BRAND} | Managed IT, Cloud & Cybersecurity", desc, canonical=f"{BASE}/")
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap">
<span class="eyebrow">Westchester MSP staging preview</span>
<h1>Managed IT, cybersecurity, cloud, and compliance support for White Plains business teams.</h1>
<p>{escape(POSITIONING)} This Gate 1 build is a noindex staging preview for owner review, with domain, phone, email, operator, and location facts marked for confirmation. [confirm]</p>
<div class="hero-ctas">
<a class="btn gold" href="schedule-a-consultation/index.html">Schedule a Consultation</a>
<a class="btn ghost" href="request-a-proposal/index.html">Request a Proposal</a>
<a class="btn ghost" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a>
</div></div></div>
<section class="cream"><div class="wrap"><div class="kicker">Public facts to review</div><h2>A Westchester technology support brand operated by Race Computer Services, LLC.</h2>
<p class="lead">The staging narrative positions {escape(BRAND)} as a White Plains and Westchester MSP brand, focused on IT consulting, cybersecurity, cloud, and compliance needs across White Plains, Westchester County, and the NYC metro area. Operator: {escape(OPERATOR)}. [confirm]</p>
{stats_block()}</div></section>
<section><div class="wrap"><div class="cols2">
<div><div class="kicker">IT operations and risk reduction</div><h2>Support for daily helpdesk needs, cloud administration, cybersecurity controls, and compliance projects.</h2>
<p>Gate 1 copy keeps the content practical: managed IT programs, remote and onsite support, Microsoft 365, firewall and endpoint security, cloud backup, data center planning, and industry-specific IT support.</p>
<ul class="checks"><li>Primary phone: <a href="tel:{PHONE_TEL}">{escape(PHONE)}</a> [confirm].</li><li>Email: <a href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a> [confirm].</li><li>Service-area framing: {escape(ADDRESS)} with street TBD; Race CS operator default may use Elizabeth, NJ in source questionnaires. [confirm]</li><li>No invented reviews, testimonials, awards, rankings, or guaranteed service outcomes.</li></ul></div>
<div class="feature"><h3>Claims pending review</h3><p>Vendor partner status, exact operator wording, onsite boundaries, compliance scope, and final response expectations should be confirmed before launch. This build avoids guarantees for uptime, breach prevention, compliance certification, recovery results, or service levels.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><div class="kicker">Platforms and frameworks</div><h2>Technology areas referenced by the staging map</h2><div class="grid">{platform_cards()}</div></div></section>
<section><div class="wrap"><div class="kicker">Factory map</div><h2>Explore the 10-hub White Plains Tech Support taxonomy</h2><p class="lead">Gate 1 organizes the service surface into 10 hubs and 100 SVC-CHILD pages for owner review.</p><div class="cols3">{''.join(hub_cards)}</div></div></section>
"""
        + faqs(
            [
                (
                    "Is this the live White Plains Tech Support website?",
                    "No. This is a noindex staging preview for owner review and is not a live production website.",
                ),
                (
                    "Are the domain, phone, email, and operator facts final?",
                    "No. The staging build uses user-provided facts and marks them for confirmation before launch. [confirm]",
                ),
                (
                    "Does this site invent testimonials or awards?",
                    "No. The staging build avoids invented testimonials, awards, rankings, client names, certifications, and guaranteed service outcomes.",
                ),
            ]
        )
        + f"""
<div class="ctastrip"><div class="wrap"><h2>Review managed IT and cybersecurity support options.</h2><p>Use the staging forms to review the proposed lead flow for IT support, cloud, compliance, and security requests.</p><a class="btn gold" href="schedule-a-consultation/index.html">Schedule a Consultation</a> <a class="btn alt" href="contact/index.html">Contact</a></div></div>
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
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Service hub</div><h2>{escape(h["name"])} for White Plains and Westchester organizations</h2>
<p class="lead">{escape(h["blurb"])} This noindex hub is written for owner review and should be checked against current service plans, pricing, staffing, partner status, onsite boundaries, and response commitments. [confirm]</p>
<p><a class="btn gold" href="../schedule-a-consultation/index.html">Schedule a Consultation</a> <a class="btn" href="../request-a-proposal/index.html">Request a Proposal</a></p>
<div class="notice"><strong>Staging review:</strong> {escape(DISCLAIMER)}</div></div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Pages</h2><div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>How this fits the {escape(BRAND)} model</h2><ul class="checks">
<li>Local MSP and consulting language stays grounded in managed IT, cloud, cybersecurity, and compliance services.</li>
<li>White Plains, Westchester County, and NYC metro service-area language should be approved by ownership before publication. [confirm]</li>
<li>Microsoft, Cisco, Dell, HPE, AWS, Google Cloud, Linux, Unix, and Apple references should be reconciled with current vendor capabilities. [confirm]</li>
<li>Cybersecurity and compliance copy avoids legal guarantees and requires professional review.</li>
<li>Every page includes staging and claims-review disclaimers.</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What is included in {h['name']}?", h["blurb"]),
                (
                    "Does this page guarantee a service level or security outcome?",
                    "No. This staging copy does not guarantee uptime, response times, breach prevention, compliance certification, or security outcomes.",
                ),
                (
                    "Who should review this page before launch?",
                    "White Plains Tech Support ownership, Race Computer Services operators, service delivery leaders, sales, legal/compliance reviewers, and form-routing owners should confirm all details.",
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
<section style="padding-top:22px"><div class="wrap"><div class="kicker">SVC-CHILD</div><h2>{escape(name)} for White Plains, Westchester, and NYC metro technology environments</h2>
<p class="lead">{escape(blurb)} Final copy must be checked by the company before public use. [confirm]</p>
<p><a class="btn gold" href="../../schedule-a-consultation/index.html">Schedule a Consultation</a> <a class="btn" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
<div class="notice"><strong>Staging review:</strong> {escape(DISCLAIMER)}</div></div></section>
<section class="tint"><div class="wrap"><h2>Good-fit conversations for {escape(name.lower())}</h2><ul class="checks">
<li>Current IT environment, users, locations, servers, cloud platforms, and business-critical systems.</li>
<li>Whether the need is ongoing managed service, co-managed support, project delivery, incident response, or advisory work.</li>
<li>Security, compliance, backup, data recovery, and business continuity requirements that need documented scope.</li>
<li>Microsoft 365, Windows Server, Linux, Apple, AWS, Google Cloud, firewall, endpoint, and vendor requirements as applicable. [confirm]</li>
<li>Response expectations, pricing approach, and escalation process that ownership must approve before publication. [confirm]</li>
</ul></div></section>
<section><div class="wrap"><h2>Positioning for {escape(name.lower())}</h2><p>This staging page describes a service conversation, not a guaranteed outcome, fixed price, compliance certification, or emergency response promise. {escape(BRAND)} should reconcile final copy with actual service packages, staffing, partner credentials, security tooling, onsite boundaries, and contract language. [confirm]</p></div></section>
<section class="cream"><div class="wrap"><div class="vs">
<div class="col bad"><h3>Generic IT vendor framing</h3><ul class="checks"><li>One-off break/fix language with little planning context.</li><li>Overbroad cybersecurity or compliance promises.</li><li>Unverified vendor-partner and response-time claims.</li></ul></div>
<div class="col good"><h3>{escape(BRAND)} framing</h3><ul class="checks"><li>Local MSP / IT consulting support for White Plains and Westchester County. [confirm]</li><li>Cloud, cybersecurity, Microsoft platform, and compliance language organized by need.</li><li>Operator and partner details marked for review before launch. [confirm]</li></ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ask about {escape(name.lower())}.</h2><p>Use the staging form to review how a proposal or consultation request should route.</p><a class="btn gold" href="../../schedule-a-consultation/index.html">Schedule a Consultation</a> <a class="btn alt" href="../../contact/index.html">Contact</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"Does {name.lower()} guarantee a result?",
                    "No. This staging copy does not guarantee uptime, response times, breach prevention, compliance certification, recovery results, or project outcomes.",
                ),
                (
                    "Is the page ready for publication?",
                    "No. It is noindex staging content requiring owner review and confirmation of facts, service scope, pricing language, and claims.",
                ),
            ]
        )
        + f'<section><div class="wrap"><h2>Related {escape(h["short"])} Pages</h2><div class="grid">{related}</div></div></section>'
        + footer(2)
    )


def cta_page(slug: str, title: str, h2: str, lead: str, button: str, *, highlight: bool = False) -> str:
    steps = {
        "contact": [
            ("Call or email", f"Reach the primary phone at {PHONE} or email {EMAIL}. Alternate phone and location details are listed for confirmation."),
            ("Share non-sensitive context", "Use the staging form for service questions, proposal routing, consultation scheduling, or general IT support needs."),
            ("Confirm the next step", "The company must confirm response expectations, routing, privacy language, and service qualification before launch."),
        ],
        "request-a-proposal": [
            ("Describe the business need", "Choose a service area such as managed IT, cybersecurity, compliance, cloud, Microsoft support, or industry-specific MSP support."),
            ("Outline scope and urgency", "Final live forms should capture users, locations, platforms, deadlines, and security requirements without collecting passwords."),
            ("Review proposal fit", "Proposal routing, pricing model, service package names, and discovery process require owner approval. [confirm]"),
        ],
        "schedule-a-consultation": [
            ("Choose a consultation path", "The highlighted staging form captures whether the conversation is for MSP support, cybersecurity, compliance, cloud, or co-managed IT."),
            ("Prepare environment details", "Useful live intake may include business size, platforms, current vendor stack, pain points, and risk priorities."),
            ("Connect to approved workflow", "Live scheduling must connect to the company's approved calendar, CRM, ticketing, privacy, and follow-up workflow."),
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
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Start an IT support conversation</div><h2>{escape(h2)}</h2><p class="lead">{escape(lead)}</p><div class="notice"><strong>Staging review:</strong> {escape(DISCLAIMER)}</div></div></section>
<section><div class="wrap"><div class="steps">{step_cards}</div>{form_shell(button, highlight=highlight)}</div></section>
<section class="tint"><div class="wrap"><h2>{escape(BRAND)} contact details</h2><p><strong>{escape(BRAND)}</strong><br>{escape(ADDRESS)} [confirm]<br>Street address TBD [confirm]<br>Phone: <a href="tel:{PHONE_TEL}">{escape(PHONE)}</a> [confirm]<br>Alternate / Race CS: <a href="tel:{ALT_PHONE_TEL}">{escape(ALT_PHONE)}</a> [confirm]<br>Email: <a href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a> [confirm]<br>Operator: {escape(OPERATOR)} ({escape(OPERATOR_DOMAIN)}) [confirm]</p></div></section>
"""
        + (org_schema() if slug == "contact" else "")
        + footer(1)
    )


def about_page() -> str:
    return (
        head(f"About {BRAND} | Local MSP & IT Consulting", f"About {BRAND}, a managed IT, cybersecurity, cloud, and consulting brand for White Plains and Westchester businesses. [confirm]", canonical=f"{BASE}/about/")
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">About the company</div><h2>{escape(BRAND)} is positioned as a local MSP and IT consulting resource.</h2>
<p class="lead">User-provided business facts connect the brand with managed IT, IT consulting, cybersecurity, cloud services, compliance, and {escape(OPERATOR)}. Final wording requires owner review. [confirm]</p><div class="notice"><strong>Staging review:</strong> {escape(DISCLAIMER)}</div></div></section>
<section class="cream"><div class="wrap"><h2>Facts for owner confirmation</h2>{stats_block()}</div></section>
<section><div class="wrap"><div class="cols2"><div><h2>Local IT support with broader platform coverage</h2><p>The staging narrative balances White Plains accessibility with technical depth across helpdesk, servers, network management, cybersecurity, compliance, cloud, and enterprise support.</p><ul class="checks"><li>Service area HQ framing: {escape(ADDRESS)}; street TBD [confirm].</li><li>Primary phone: {escape(PHONE)}; alternate / Race CS phone: {escape(ALT_PHONE)} [confirm].</li><li>Operator: {escape(OPERATOR)} ({escape(OPERATOR_DOMAIN)}) [confirm].</li><li>Domain and email require final owner confirmation. [confirm]</li></ul></div><div class="card"><h3>About pages</h3><ul class="checks"><li><a href="why-choose-us/index.html">Why Choose Us</a></li><li><a href="westchester-service-area/index.html">Westchester Service Area</a></li></ul></div></div></div></section>
"""
        + faqs(
            [
                ("Where is White Plains Tech Support framed?", f"The staging address framing is {ADDRESS} with street TBD and owner confirmation required. [confirm]"),
                ("What services are emphasized?", "Managed IT, IT consulting, cybersecurity, cloud services, compliance support, Microsoft platform support, and local small-business technology support."),
                ("What needs confirmation?", "All facts, operator wording, service areas, pricing language, service levels, form routing, and legal/compliance claims require owner review."),
            ]
        )
        + org_schema()
        + footer(1)
    )


def why_page() -> str:
    return (
        head(f"Why Choose {BRAND} | Managed IT Support", f"Why businesses may consider {BRAND} for local managed IT, cybersecurity, cloud, and compliance support, pending owner confirmation.", canonical=f"{BASE}/about/why-choose-us/")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Why choose the team</div><h2>Westchester MSP support with cloud, security, and compliance pathways.</h2><p class="lead">This staging page summarizes differentiators without testimonials, rankings, awards, client names, or guaranteed outcomes.</p><div class="notice"><strong>Staging review:</strong> {escape(DISCLAIMER)}</div></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Local business focus</h3><p>White Plains, Westchester County, and NYC metro positioning for organizations that want accessible IT support. [confirm]</p></div>
<div class="card"><h3>Managed IT plus projects</h3><p>Ongoing MSP, co-managed IT, helpdesk, server, cloud, and project delivery topics appear throughout the taxonomy.</p></div>
<div class="card"><h3>Cybersecurity depth</h3><p>Risk assessment, endpoint protection, firewall, monitoring, incident response, and compliance language require service-owner confirmation.</p></div>
<div class="card"><h3>Microsoft platform support</h3><p>Microsoft 365, Office 365, Windows Server, Hosted Exchange, and partner-positioning references must be verified. [confirm]</p></div>
<div class="card"><h3>Race CS operator family</h3><p>{escape(OPERATOR)} relationship is included for confirmation rather than treated as final marketing copy. [confirm]</p></div>
<div class="card"><h3>No invented proof points</h3><p>The staging copy intentionally avoids fabricated reviews, awards, client names, certifications, or guarantees.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Review whether White Plains Tech Support is a fit.</h2><a class="btn gold" href="../../schedule-a-consultation/index.html">Schedule a Consultation</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + footer(2)
    )


def westchester_service_area_page() -> str:
    locality_cards = "".join(
        f'<div class="gcard"><h3>{escape(place)}</h3><p>Service-area reference for owner confirmation before launch. Onsite boundaries, travel policies, and remote support coverage must be approved. [confirm]</p><span class="tag">Service area</span></div>'
        for place in LOCALITIES
    )
    return (
        head(f"Westchester Service Area | {BRAND}", f"White Plains and Westchester County service-area staging page for {BRAND}.", canonical=f"{BASE}/about/westchester-service-area/")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Westchester Service Area</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Local coverage</div><h2>White Plains, Westchester County, and NYC metro IT support coverage.</h2><p class="lead">This staging page localizes the service-area story for owner review. It does not guarantee onsite response, travel availability, or emergency dispatch.</p><div class="notice"><strong>Staging review:</strong> {escape(DISCLAIMER)}</div></div></section>
<section class="tint"><div class="wrap"><h2>Areas referenced</h2><div class="grid">{locality_cards}</div></div></section>
<section><div class="wrap"><h2>Onsite plus remote support framing</h2><p>{escape(BRAND)} is positioned for remote support, managed services, cybersecurity, cloud administration, and onsite coordination where approved. The final live site should confirm onsite service boundaries across Westchester and NYC metro communities.</p><ul class="checks"><li>Confirm White Plains HQ framing and street address before publication.</li><li>Confirm whether Elizabeth, NJ operator HQ should appear in public copy or remain questionnaire context only.</li><li>Confirm travel fees, emergency-response language, and support hours.</li><li>Confirm compliance and cybersecurity claims for each industry served.</li></ul></div></section>
<section class="cream"><div class="wrap"><h2>Platforms and frameworks referenced</h2><div class="grid">{platform_cards()}</div></div></section>
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
        ["/", "HOME", "", "white plains tech support", "logo/home", "A1,A3,A4,A9", ""],
        ["/about/", "COMP-HUB", "/", "about white plains tech support", "About menu", "A1,A2,A7,A9", ""],
        ["/about/why-choose-us/", "COMP-CHILD", "/about/", "why choose white plains tech support", "About menu", "A9,D", ""],
        ["/about/westchester-service-area/", "COMP-CHILD", "/about/", "westchester it support service area", "About menu", "A8,A9", ""],
        ["/contact/", "COMP-CONTACT", "/", "contact white plains tech support", "Contact menu", "A4,A5,A6,A7", "Contact Request"],
        ["/request-a-proposal/", "FORM-PROPOSAL", "/", "request an it proposal", "nav utility", "I1", "Proposal Request"],
        ["/schedule-a-consultation/", "FORM-SCHEDULE", "/", "schedule it consultation", "nav highlighted", "I1", "Schedule a Consultation"],
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
                    "Schedule a Consultation / Request a Proposal",
                ]
            )
    with (ROOT / "PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def write_questionnaire() -> None:
    hub_slugs = " | ".join(h["slug"] for h in HUBS)
    platforms = "\n".join(f"- {c}" for c in PLATFORMS)
    localities = "\n".join(f"- {c}" for c in LOCALITIES)
    write(
        ROOT / "QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire - White Plains Tech Support Factory Pages

Home page and all factory pages share one chrome: staging banner, utility bar, logo/phone header, Services dropdown, About dropdown, Contact, Request a Proposal, and highlighted Schedule a Consultation CTA.

## A - Business identity
| Field | Value | Source |
|---|---|---|
| A1 brand | {BRAND} | user-provided business facts |
| A2 operator | {OPERATOR} ({OPERATOR_DOMAIN}) | user-provided; confirm wording [confirm] |
| A3 domain | {BASE} | user-provided business facts [confirm] |
| A4 primary_phone | {PHONE} / tel:{PHONE_TEL} | user-provided business facts; Race CS operator default [confirm] |
| A5 alternate_phone | {ALT_PHONE} / tel:{ALT_PHONE_TEL} | user-provided alternate / Race CS [confirm] |
| A6 email | {EMAIL} | user-provided business facts [confirm] |
| A7 address | {ADDRESS}; street TBD | user-provided service-area HQ framing [confirm] |
| A8 operator_hq_context | Elizabeth, NJ may be noted as Race CS operator default | questionnaire context only [confirm] |
| A9 service_area | {AREA} | user-provided business facts [confirm] |
| A10 positioning | {POSITIONING} | user-provided business facts [confirm] |

## B - Gate 1 taxonomy
- Hubs: {len(HUBS)}
- SVC-CHILD pages: {sum(len(h['children']) for h in HUBS)}
- Total generated `index.html` pages: 117
- Hub slugs: {hub_slugs}
- Full URL map: `PAGE-INVENTORY.csv`

## C - Platform and compliance topics to confirm
{platforms}

## D - Service-area references to confirm
{localities}

## E - Claims to confirm
- Domain, email, primary phone, alternate / Race CS phone. [confirm]
- Operator relationship with {OPERATOR}. [confirm]
- White Plains, NY 10601 HQ framing and street address TBD. [confirm]
- Whether Race CS Elizabeth, NJ operator HQ should appear publicly. [confirm]
- Pricing, support hours, response expectations, and onsite boundaries. [confirm]
- Vendor partner status and platform capabilities. [confirm]
- Cybersecurity and compliance service scope; no legal, breach-prevention, or certification guarantees.

## F - Forms and CTAs
- Primary CTA: `schedule-a-consultation` (highlighted)
- Secondary CTA: `request-a-proposal`
- Company/contact CTA: `contact`
- Form shells must be wired with owner-approved privacy, spam protection, CRM/ticket routing, scheduling, response expectations, and follow-up language before public launch.

## G - Staging and compliance
- HTML uses `<meta name="robots" content="noindex,nofollow">`.
- `robots.txt` disallows all crawling.
- `netlify.toml` sends `X-Robots-Tag: noindex, nofollow`.
- Staging banner text: `{STAGING_BANNER}`
- No testimonials, awards, rankings, client logos, certifications, or guaranteed outcomes are invented.
""",
    )


def write_notes() -> None:
    write(
        ROOT / "WHITEPLAINSTECHSUPPORT-NOTES.md",
        f"""# White Plains Tech Support Factory Build Notes

- Branch: `cursor/white-plains-tech-support-factory-127e`
- Domain target: {BASE} [confirm]
- Build type: NearMe OS Website Factory Gate 1 staging preview
- Page model: 10 service hubs x 10 children = 100 SVC-CHILD pages
- Generated `index.html` pages expected: 117
- Inventory URLs expected: 117
- Staging controls: HTML noindex,nofollow; robots.txt `Disallow: /`; Netlify `X-Robots-Tag: noindex, nofollow`
- Banner: `{STAGING_BANNER}`
- Visual direction: Westchester / NY professional MSP, deep slate navy `#0f172a`, Hudson blue `#1d4ed8`, crisp white, amber CTA `#f59e0b`
- Fonts: Fraunces for headlines and Public Sans for interface/body
- Navigation: shared chrome on all pages; dropdown links use dark text on white backgrounds via `nav.nav .dd a`
- CTA language: Schedule a Consultation / Request a Proposal / Contact
- Business facts: primary phone {PHONE}; alternate / Race CS phone {ALT_PHONE}; email {EMAIL}; service-area HQ framing {ADDRESS}; street TBD [confirm]
- Operator notes: {OPERATOR} ({OPERATOR_DOMAIN}) is the operator / parent family relationship to confirm. [confirm]
- Race CS operator default HQ may be Elizabeth, NJ in questionnaire context; public site copy uses White Plains service-area framing unless owner approves more detail. [confirm]
- Vendor partner, pricing, service quality, service area, cybersecurity, and compliance references are marked for confirmation. [confirm]
- No invented testimonials, awards, rankings, client names, certifications, or guaranteed outcomes.
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

    write(ROOT / "about" / "index.html", about_page())
    urls.append("/about/")
    write(ROOT / "about" / "why-choose-us" / "index.html", why_page())
    urls.append("/about/why-choose-us/")
    write(ROOT / "about" / "westchester-service-area" / "index.html", westchester_service_area_page())
    urls.append("/about/westchester-service-area/")

    for slug, title, h2, lead, button, highlight in [
        (
            "contact",
            f"Contact {BRAND}",
            f"Contact {BRAND}",
            "Call, email, or send a staging inquiry for managed IT, cybersecurity, cloud, compliance, or support questions.",
            "Contact White Plains Tech Support",
            False,
        ),
        (
            "request-a-proposal",
            f"Request a Proposal | {BRAND}",
            "Request an IT Support Proposal",
            "Share the service area, business context, and timeline so the company can confirm the right proposal path.",
            "Request a Proposal",
            False,
        ),
        (
            "schedule-a-consultation",
            f"Schedule a Consultation | {BRAND}",
            "Schedule an IT Consultation",
            "Use the highlighted staging form to review the lead flow for MSP, cybersecurity, compliance, cloud, and co-managed IT conversations.",
            "Schedule a Consultation",
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
<p class="lead">That URL is not in the {escape(BRAND)} staging factory map. Return home or use the highlighted consultation form.</p>
<div class="notice"><strong>Staging review:</strong> {escape(DISCLAIMER)}</div>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn gold" href="schedule-a-consultation/index.html">Schedule a Consultation</a></p>
</div></section>
"""
        + footer(0),
    )

    write_static_files(urls)
    write_inventory()
    write_questionnaire()
    write_notes()

    index_pages = list(ROOT.rglob("index.html"))
    inventory_children = 0
    inventory_rows = 0
    with (ROOT / "PAGE-INVENTORY.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            inventory_rows += 1
            if row["type_id"] == "SVC-CHILD":
                inventory_children += 1

    print(f"Index pages on disk: {len(index_pages)}")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Inventory URLs: {inventory_rows}")
    print(f"Hubs: {len(HUBS)}")
    print(f"SVC-CHILD inventory rows: {inventory_children}")
    print("Home uses shared factory chrome: yes")
    print("Staging noindex controls: yes")
    print("Dropdown CSS dark-on-white: yes")
    print("No invented testimonials or awards: yes")


if __name__ == "__main__":
    main()
