#!/usr/bin/env python3
"""One-page San Diego Tech Support replica using factory completeness chrome.

Structural quality bar: live san-diegotechsupport.com homepage modules.
Does not copy WordPress assets, blog posts, or copyrighted body copy.
Public NAP/stats from the live site are labeled as such.
"""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import factory_complete as fc  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "san-diego-tech-support-replica" / "index.html"

PHONE = "(619) 478-0455"
PHONE_TEL = "+16194780455"
EMAIL = "support@san-diegotechsupport.com"
HQ = "Chula Vista, CA"
ADDRESS = "310 3rd Ave, Chula Vista, CA 91911"  # [confirm]
TAGLINE = "Southern California IT consulting and cybersecurity"

SERVICES = [
    ("briefcase", "Managed IT", "Proactive monitoring, helpdesk, and a team instead of a single IT guy."),
    ("shield", "Cybersecurity", "Consulting or managed controls — firewall, endpoint, awareness, and response."),
    ("lock", "Compliance", "HIPAA, PCI-DSS, CMMC, and NIST-oriented IT security work [confirm scope]."),
    ("node", "Cloud & hosting", "Microsoft 365, backup, private cloud, and hosted infrastructure support."),
    ("people", "Enterprise IT", "Multi-office, vCIO, and project delivery for larger environments."),
    ("wallet", "Small business support", "Remote and onsite support sized for growing Southern California teams."),
    ("chain", "Network & servers", "Installs, virtualization, and ongoing server administration."),
    ("signal", "Microsoft 365", "Email, identity, and day-to-day Office 365 administration."),
]

STATS = [
    ("5 sec", "Avg. call wait (live site)"),
    ("94%", "Same-day resolution (live site)"),
    ("8,473", "Tickets resolved (live site)"),
    ("98.65%", "SLAs met (live site)"),
    ("96.99%", "Customer retention (live site)"),
    ("99%", "Customer satisfaction (live site)"),
]

BENEFITS = [
    ("chart", "Improved IT efficiency", "Managed support is meant to keep operations moving instead of waiting on a contractor’s next available hour."),
    ("shield", "Layered cybersecurity", "Security can ride along with managed services — consultative or ongoing — instead of a one-time tool install."),
    ("phone", "US-based 24/7 options", "Live site positions 24×7 support on managed offerings. Terms apply [confirm]."),
    ("briefcase", "Value over a bloated stack", "The public positioning is a step up from a one-person shop without enterprise MSP pricing theater."),
    ("people", "Time back for staff", "Employees stop burning the afternoon on printer and login loops."),
    ("node", "Enterprise-grade monitoring", "Managed clients are described as getting monitoring for alerting and security features [confirm product names]."),
]

INSIGHTS = [
    ("Access control is a habit", "Who can join Wi-Fi, email, and admin panels should be written down — not remembered."),
    ("Backup is not disaster recovery", "A copy in the cloud still needs a restore test and an owner who knows the login."),
    ("Phishing beats most firewalls", "Staff reporting weird invoices is a control. Fancy appliances do not replace that drill."),
    ("One-person IT does not scale", "When the only technician is on vacation, the SLA is a voicemail."),
    ("Compliance is evidence, not a poster", "HIPAA and PCI conversations fail when nobody can show policies, logs, or a risk assessment."),
    ("Patch windows need a calendar", "Unpatched servers are not a mystery; they are a missing operations habit."),
]


def page() -> str:
    tiles = []
    for icon, title, blurb in SERVICES:
        tiles.append(
            f'<a class="icon-tile" href="#contact">{fc.svg_icon(icon)}'
            f"<h3>{escape(title)}</h3><p>{escape(blurb)}</p></a>"
        )
    stats = fc.stats_html(STATS)
    benefits = fc.benefits_html(BENEFITS)
    steps = fc.how_it_works(
        [
            ("Choose a service", "Managed IT, cybersecurity, cloud, compliance, or a mix."),
            ("Let’s communicate", "How you use technology today — offices, Microsoft 365, who gets paged."),
            ("Start with a scoped first step", "A service model you can live with, then monitoring and support."),
        ]
    )
    hubs_as_opts = [
        {"name": n}
        for n in (
            "Managed Services",
            "Business Continuity",
            "Cyber Security",
            "Cloud Services",
            "vCIO Services",
            "Network Support",
            "Microsoft 365",
            "HIPAA / compliance consulting",
        )
    ]
    form = fc.form_shell(hubs_as_opts)
    insights = []
    for title, excerpt in INSIGHTS:
        insights.append(
            f'<article class="insight"><div class="thumb"></div><div class="pad">'
            f"<small>Factory advisory</small><h3>{escape(title)}</h3>"
            f"<p>{escape(excerpt)}</p></div></article>"
        )
    partners = fc.partners_html(
        [
            "Microsoft 365",
            "Windows Server",
            "Cisco [confirm]",
            "Dell [confirm]",
            "HPE [confirm]",
            "AWS / GCP [confirm]",
        ]
    )
    faqs = fc.faqs_html(
        [
            (
                "Is this the live San Diego Tech Support website?",
                "No. This is a one-page factory replica for layout and module completeness. The live site is san-diegotechsupport.com.",
            ),
            (
                "Where do the numbers come from?",
                "Call wait, same-day resolution, tickets, SLA, retention, and CSAT figures are copied as published on the live homepage and should be reconfirmed before any launch.",
            ),
            (
                "How do I get support?",
                f"Call {PHONE} or use the form. Email {EMAIL}. Street address from public listings may need confirmation.",
            ),
        ]
    )
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>San Diego Tech Support | One-page factory replica</title>
<meta name="description" content="One-page completeness replica of San Diego Tech Support homepage modules — not the live website.">
<style>
{fc.COMPLETE_CSS}
:root{{--navy:#0a3d73;--navy-2:#072c54;--accent:#1a8cff;--accent-dark:#0d6ad4;--cta:#f5a623}}
</style></head><body>
<div class="demo-banner">STAGING REPLICA — one page · structure based on san-diegotechsupport.com · not the live San Diego Tech Support website</div>
<div class="utility"><div class="wrap">
<span>{escape(TAGLINE)}</span>
<span><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a> · <a href="mailto:{EMAIL}">{escape(EMAIL)}</a></span>
</div></div>
<header class="main"><div class="wrap">
<a class="brand" href="#top">{fc.logo_mark()}<div class="logo">San Diego <span>Tech Support</span><small>Managed IT · Cyber · Cloud</small></div></a>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Southern California MSP replica</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="#top">Home</a></li>
<li><a href="#services">Services</a></li>
<li><a href="#why">Why us</a></li>
<li><a href="#how">How it works</a></li>
<li><a href="#insights">Insights</a></li>
<li><a href="#contact">Contact</a></li>
<li class="em"><a href="#contact">Schedule a Consultation</a></li>
</ul></div></nav>

<div class="hero-photo" id="top"><div class="wrap">
<div>
<p class="kicker">San Diego IT support</p>
<h1>A reliable IT support partner you can trust.</h1>
<p>Managed services positioned as a step up from a single IT guy, without defaulting to the most expensive MSP in the room — for businesses across Southern California.</p>
<div class="hero-actions">
<a class="btn" href="#contact">Request a Consultation</a>
<a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a>
</div>
<form class="search-hero" action="#services" method="get">
<input type="search" name="q" placeholder="Search Find Now" aria-label="Search this page" id="q">
<button class="btn navy" type="submit">Find Now</button>
</form>
</div>
<div class="hero-card">
<h3>Let us help you resolve your technology challenges</h3>
<p>Tell the team how you use IT today. This replica form is a shell until rollout wiring.</p>
</div>
</div></div>

<section class="navy" id="numbers"><div class="wrap">
<p class="kicker">By the numbers</p>
<h2>San Diego Tech Support figures as published on the live homepage</h2>
<p style="color:#cfe6ff;margin-bottom:18px">Reconfirm before launch. This replica does not invent extra KPIs.</p>
{stats}
</div></section>

<section id="services"><div class="wrap">
<p class="kicker">Our services</p>
<h2>Expert IT support across managed, cyber, cloud, and compliance.</h2>
<p class="lead">The live site spans several IT lanes. Smaller clients are described as using entry-level managed services such as unlimited remote support. This page keeps that map on one screen.</p>
<div class="icon-grid">{''.join(tiles)}</div>
</div></section>

<section class="tint" id="why"><div class="wrap">
<p class="kicker">Your benefits</p>
<h2>Why choose San Diego Tech Support?</h2>
<p class="lead">Collaborative IT partner language from the public site: managed services and complete technology outsourcing — rewritten here so we are not pasting their WordPress copy.</p>
{benefits}
</div></section>

<section id="how"><div class="wrap">
<p class="kicker">How it works</p>
<h2>Are you ready to take your IT support to the next level?</h2>
{steps}
<div class="cols2" style="margin-top:28px" id="contact">
<div>
<h2>Contact form</h2>
<p>Fill this in with IT needs. On the live site a representative follows up. Address: {escape(ADDRESS)} <em>[confirm]</em>. Parent/affiliate notes (Race Computer Services) stay off this replica until confirmed.</p>
<p><strong>San Diego Tech Support</strong><br>{escape(PHONE)}<br>{escape(EMAIL)}<br>{escape(HQ)}</p>
</div>
{form}
</div>
</div></section>

<section class="tint" id="insights"><div class="wrap">
<p class="kicker">Insights</p>
<h2>Factory-written advisory cards (not scraped Tech Advisory posts)</h2>
<div class="insight-grid">{''.join(insights)}</div>
</div></section>

<section id="partners"><div class="wrap">
<p class="kicker">Technology partners</p>
<h2>Platforms referenced in public navigation</h2>
<p>Badges only — not a certification claim unless the owner confirms partner status.</p>
{partners}
</div></section>

{faqs}

<footer><div class="wrap"><div class="fcols">
<div><h4>Services</h4><ul>
<li><a href="#services">Managed IT</a></li>
<li><a href="#services">Cybersecurity</a></li>
<li><a href="#services">Cloud</a></li>
<li><a href="#services">Compliance</a></li>
</ul></div>
<div><h4>Company</h4><ul>
<li><a href="#why">Why choose us</a></li>
<li><a href="#contact">Contact</a></li>
<li><a href="https://www.san-diegotechsupport.com/">Live website</a></li>
</ul></div>
<div><h4>Visit</h4><ul>
<li>{escape(ADDRESS)} [confirm]</li>
<li>{escape(PHONE)}</li>
<li>{escape(EMAIL)}</li>
</ul></div>
<div><h4>Replica note</h4><ul>
<li>One-page factory completeness demo</li>
<li>noindex staging</li>
</ul></div>
</div>
<div class="copy">San Diego Tech Support one-page replica · not the live website<br>
Copyright &copy; 2026. Structural demo only. Public stats attributed to the live homepage.</div></div></footer>
<script>
document.querySelector(".search-hero")?.addEventListener("submit", function(e) {{
  e.preventDefault();
  const q = (document.getElementById("q").value || "").toLowerCase();
  const tiles = [...document.querySelectorAll(".icon-tile")];
  tiles.forEach(t => {{
    const hit = !q || t.innerText.toLowerCase().includes(q);
    t.style.opacity = hit ? "1" : "0.35";
  }});
  document.getElementById("services").scrollIntoView({{behavior:"smooth"}});
}});
</script>
</body></html>
"""


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page(), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
