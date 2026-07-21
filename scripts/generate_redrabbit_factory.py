#!/usr/bin/env python3
"""Generate Red Rabbit Security site using the NearMe OS Website Factory template
(same HTML/CSS engine as the SEO Cow staging build on Netlify)."""

from __future__ import annotations

import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://redrabbitsec.com"
PHONE = "(914) 281-5352"
PHONE_TEL = "+19142815352"
EMAIL = "info@redrabbitsec.com"
HQ = "White Plains, NY"
TAGLINE = "Outsmart. Outpace. Outlast."
STAGING_BANNER = (
    "STAGING PREVIEW — redrabbitsec.com demo build · content pending owner review "
    "· not the live Red Rabbit Security website"
)

# NearMe factory CSS (SEO Cow template) with Red Rabbit crimson remap
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#1c1416;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#9b1c1c;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#1c1416;color:#f0b7b7;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#5c0a12;color:#f3d6d6;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #c1121f;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#5c0a12}.logo span{color:#c1121f}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#5c0a12}
.phone-cta small{display:block;color:#5a6b7b;font-size:11px}
nav.nav{background:#5c0a12}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#3d070c;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #c1121f;z-index:60}
.dd a{color:#1c1416;padding:10px 15px;font-weight:500;border-bottom:1px solid #f1e8e8}
.dd a:hover{background:#f8eeee}
.nav .em a{background:#c1121f}.nav .em a:hover{background:#9b1c1c}
.hero{background:linear-gradient(rgba(20,10,12,.82),rgba(20,10,12,.82)),repeating-linear-gradient(45deg,#5c0a12 0 14px,#6e0e18 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#f0b7b7;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#c1121f;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#d41424;text-decoration:none}
.btn.alt{background:#5c0a12;color:#fff}.btn.alt:hover{background:#7a101a}
section{padding:44px 0}
section.tint{background:#f7f2f2}
section h2{font-size:25px;color:#5c0a12;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#c1121f;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #e6dede;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(40,10,14,.06)}
.card h3{color:#5c0a12;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #e6dede;border-left:4px solid #c1121f;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#5c0a12}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#9b1c1c}
.ctastrip{background:#5c0a12;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #e6dede;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#faf5f2}.vs .col.good{background:#f8f2f2}
.vs h3{font-size:16px;margin-bottom:12px;color:#5c0a12}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#9b1c1c;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #e6dede;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#5c0a12;list-style:none}
details summary:before{content:"+ ";color:#c1121f;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #e6dede;border-top:4px solid #c1121f;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#44525f;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5a6b7b;padding:14px 0 0}
.crumb a{color:#5a6b7b}
footer{background:#2a0a0e;color:#c9b8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #4a2026;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #e6dede;border-top:4px solid #c1121f;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#5c0a12}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #e6dede;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(92,10,18,.07)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#5c0a12}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#c1121f;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#c1121f;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#8a0c16}
"""

HUBS = [
    {
        "slug": "managed-cybersecurity-services",
        "name": "Managed Cybersecurity Services",
        "short": "Cybersecurity",
        "blurb": "24/7 monitoring, detection, and response across endpoints, email, identity, and cloud.",
        "children": [
            ("managed-siem-services", "Managed SIEM Services", "Security information and event management with 24/7 analyst review."),
            ("next-generation-antivirus-endpoint-protection", "Next-Gen Endpoint Protection", "NGAV and EDR that stop ransomware before it spreads."),
            ("managed-anti-phishing-email-security", "Managed Email Security", "Anti-phishing and BEC defenses for every inbox."),
            ("identity-and-access-management", "Identity & Access Management", "MFA, least privilege, and identity hardening."),
            ("vulnerability-scanning-and-assessment", "Vulnerability Scanning", "Continuous scanning with prioritized remediation."),
            ("penetration-testing-services", "Penetration Testing", "Authorized offensive testing that finds exploitable gaps."),
            ("incident-response-and-breach-recovery", "Incident Response", "Rapid containment and recovery when minutes matter."),
            ("virtual-ciso-services", "Virtual CISO (vCISO)", "Executive security leadership on subscription."),
        ],
    },
    {
        "slug": "managed-it-services",
        "name": "Managed IT Services",
        "short": "Managed IT",
        "blurb": "Proactive help desk, patching, and administration with security built in.",
        "children": [
            ("unlimited-tech-support", "Unlimited Tech Support", "US-based help desk for day-to-day user issues."),
            ("managed-help-desk-services", "Managed Help Desk", "Ticketed support with SLAs and clear escalation."),
            ("patch-management-services", "Patch Management", "Coordinated OS and application patching."),
            ("it-asset-management", "IT Asset Management", "Hardware and software inventory you can trust."),
            ("microsoft-365-administration", "Microsoft 365 Administration", "Secure tenant setup and ongoing admin."),
            ("co-managed-it-services", "Co-Managed IT", "Augment your internal IT with specialists."),
            ("virtual-cio-services", "Virtual CIO Services", "Technology planning aligned to business goals."),
            ("onboarding-offboarding-services", "User Onboarding & Offboarding", "Secure joiner/mover/leaver workflows."),
        ],
    },
    {
        "slug": "ai-business-solutions",
        "name": "AI Business Solutions",
        "short": "AI Solutions",
        "blurb": "Practical AI automation and governance without new security blind spots.",
        "children": [
            ("ai-automation-consulting", "AI Automation Consulting", "High-ROI workflows ready for safe automation."),
            ("secure-ai-adoption", "Secure AI Adoption", "Controls so AI tools do not leak company data."),
            ("ai-powered-security-operations", "AI-Powered Security Ops", "Smarter triage layered onto your SOC stack."),
            ("business-process-ai", "Business Process AI", "Ops automation that frees staff for higher-value work."),
            ("ai-readiness-assessment", "AI Readiness Assessment", "Scorecard of data, tooling, and risk before you scale."),
            ("custom-ai-integrations", "Custom AI Integrations", "Connect models to systems your teams already use."),
            ("ai-governance-and-policy", "AI Governance & Policy", "Acceptable-use frameworks leadership can enforce."),
            ("employee-ai-training", "Employee AI Training", "Training so staff use AI productively and safely."),
        ],
    },
    {
        "slug": "cloud-computing-services",
        "name": "Cloud Computing Services",
        "short": "Cloud",
        "blurb": "Secure cloud design, migration, and management across Azure, AWS, and GCP.",
        "children": [
            ("cloud-migration-services", "Cloud Migration Services", "Planned migrations with security baselines."),
            ("microsoft-azure-consulting", "Microsoft Azure Consulting", "Landing zones, identity, and cost-aware admin."),
            ("managed-aws-services", "Managed AWS Services", "Guardrails and operations for AWS workloads."),
            ("google-cloud-platform-services", "Google Cloud Services", "GCP projects hardened for identity and networking."),
            ("cloud-security-posture", "Cloud Security Posture", "Misconfiguration hunting and continuous hygiene."),
            ("email-migration-services", "Email Migration Services", "Mailbox moves with minimal downtime."),
            ("cloud-backup-integration", "Cloud Backup Integration", "Backup architecture matched to your RTO."),
            ("hybrid-cloud-architecture", "Hybrid Cloud Architecture", "On-prem and cloud designs that stay operable."),
        ],
    },
    {
        "slug": "compliance-regulatory-services",
        "name": "Compliance & Regulatory Services",
        "short": "Compliance",
        "blurb": "Audit-ready programs for HIPAA, PCI, NYDFS, CMMC, SOC 2, and more.",
        "children": [
            ("hipaa-compliance-services", "HIPAA Compliance Services", "Security risk analysis and ongoing HIPAA support."),
            ("pci-dss-compliance-services", "PCI-DSS Compliance", "Cardholder-data scoping and remediation."),
            ("nydfs-500-compliance", "NYDFS 23 NYCRR 500", "Cybersecurity program support for covered NY entities."),
            ("cmmc-compliance-services", "CMMC Compliance", "Defense-contractor readiness for CMMC."),
            ("soc-2-readiness", "SOC 2 Readiness", "Control design and evidence for attestation."),
            ("cyber-insurance-readiness", "Cyber Insurance Readiness", "Close questionnaire gaps before renewal."),
            ("compliance-gap-assessment", "Compliance Gap Assessment", "Prioritized map of what auditors will flag."),
            ("ongoing-compliance-monitoring", "Ongoing Compliance Monitoring", "Continuous checks so audits are not a scramble."),
        ],
    },
    {
        "slug": "backup-disaster-recovery",
        "name": "Backup & Disaster Recovery",
        "short": "Backup & DR",
        "blurb": "Tested backups and recovery plans that keep ransomware from ending the business.",
        "children": [
            ("managed-backup-services", "Managed Backup Services", "Automated backups with restore testing."),
            ("disaster-recovery-planning", "Disaster Recovery Planning", "Documented runbooks leadership can execute."),
            ("draas-services", "DRaaS", "Failover when primary site or region is down."),
            ("ransomware-recovery-services", "Ransomware Recovery", "Clean recovery paths that avoid reinfection."),
            ("business-continuity-planning", "Business Continuity Planning", "Keep critical ops running through outages."),
            ("backup-monitoring-reporting", "Backup Monitoring & Reporting", "Proof restores work — monthly reporting."),
            ("immutable-backup-solutions", "Immutable Backups", "Copies attackers cannot encrypt or delete."),
            ("cloud-data-backup", "Cloud Data Backup", "Protect M365/Google Workspace data vendors under-cover."),
        ],
    },
    {
        "slug": "network-infrastructure-services",
        "name": "Network Infrastructure Services",
        "short": "Network",
        "blurb": "Design, secure, and operate wired, wireless, and WAN infrastructure.",
        "children": [
            ("network-design-and-implementation", "Network Design & Implementation", "Secure architectures sized for growth."),
            ("managed-wifi-services", "Managed Wi-Fi Services", "Business wireless with segmentation."),
            ("firewall-management", "Firewall Management", "Configuration and change control for perimeter defenses."),
            ("network-cabling-services", "Network Cabling Services", "Copper and fiber plant for reliable throughput."),
            ("network-diagnostics-support", "Network Diagnostics", "Fast root-cause when connectivity fails."),
            ("secure-remote-access-vpn", "Secure Remote Access / VPN", "Remote access without punching security holes."),
            ("sd-wan-services", "SD-WAN Services", "Policy-based site connectivity and visibility."),
            ("network-segmentation", "Network Segmentation", "Contain breaches by limiting east-west movement."),
        ],
    },
    {
        "slug": "business-voip-services",
        "name": "Business VoIP Services",
        "short": "VoIP",
        "blurb": "Fully managed cloud phone systems with security and uptime built in.",
        "children": [
            ("managed-voip-phone-systems", "Managed VoIP Phone Systems", "Hosted PBX and devices under one partner."),
            ("cloud-phone-system-setup", "Cloud Phone System Setup", "Number porting and go-live with minimal disruption."),
            ("unified-communications", "Unified Communications", "Voice, video, and messaging across devices."),
            ("call-center-voip", "Call Center VoIP", "Queues, IVR, and reporting for customer teams."),
            ("voip-security-hardening", "VoIP Security Hardening", "Fraud controls and abuse monitoring."),
            ("microsoft-teams-calling", "Microsoft Teams Calling", "Calling integrated with your M365 tenant."),
            ("voip-migration-services", "VoIP Migration Services", "Leave aging PBXs without losing numbers."),
            ("business-sms-communications", "Business SMS & Communications", "Compliant messaging connected to workflows."),
        ],
    },
    {
        "slug": "software-application-development",
        "name": "Software & Application Development",
        "short": "Software",
        "blurb": "Custom software and apps built with security from the first commit.",
        "children": [
            ("custom-software-development", "Custom Software Development", "Line-of-business apps tailored to your workflows."),
            ("mobile-application-development", "Mobile App Development", "iOS and Android with secure auth paths."),
            ("web-application-development", "Web Application Development", "Modern web apps hardened against OWASP risks."),
            ("business-application-integration", "Business App Integration", "Connect CRM/ERP/SaaS without brittle glue."),
            ("api-development-services", "API Development", "Stable APIs with auth and documentation."),
            ("legacy-application-modernization", "Legacy App Modernization", "Retire fragile stacks without losing workflows."),
            ("secure-sdlc-consulting", "Secure SDLC Consulting", "Embed security into build pipelines."),
            ("application-support-maintenance", "Application Support & Maintenance", "Fixes and enhancements after launch."),
        ],
    },
]

INDUSTRIES = [
    "Healthcare", "Legal", "Finance", "Manufacturing", "Education", "Real Estate",
    "Retail", "Hospitality", "Construction", "Non-Profit", "Government", "Logistics",
]


def pfx(depth: int) -> str:
    return "" if depth == 0 else "../" * depth


def trunc(text: str, n: int = 155) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= n:
        return text
    return text[: n - 1].rsplit(" ", 1)[0].rstrip(" ,.;:") + "…"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def head(title: str, desc: str) -> str:
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(trunc(desc))}">
<style>
{FACTORY_CSS}
</style></head><body>
<div class="demo-banner">{escape(STAGING_BANNER)}</div>
"""


def chrome(depth: int) -> str:
    p = pfx(depth)
    hub_dd = "".join(
        f'<a href="{p}{h["slug"]}/index.html">{escape(h["name"])}</a>' for h in HUBS
    )
    return f"""<div class="utility"><div class="wrap"><span>{escape(TAGLINE)}</span><span>{escape(HQ)} &middot; {escape(EMAIL)}</span></div></div>
<header class="main"><div class="wrap">
<div class="logo">Red <span>Rabbit</span><small>Security</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Free security assessment — no obligation</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-red-rabbit-security/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-red-rabbit-security/index.html">About Red Rabbit</a>
<a href="{p}about-red-rabbit-security/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-red-rabbit-security/industries-we-serve/index.html">Industries We Serve</a>
</div></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li class="em"><a href="{p}free-security-assessment/index.html">Free Assessment</a></li>
</ul></div></nav>
"""


def footer(depth: int) -> str:
    p = pfx(depth)
    hubs = "".join(
        f'<li><a href="{p}{h["slug"]}/index.html">{escape(h["short"])}</a></li>' for h in HUBS
    )
    return f"""<footer><div class="wrap"><div class="fcols">
<div><h4>Services</h4><ul>{hubs}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="{p}about-red-rabbit-security/index.html">About Red Rabbit</a></li>
<li><a href="{p}about-red-rabbit-security/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-red-rabbit-security/industries-we-serve/index.html">Industries</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}free-security-assessment/index.html">Free Security Assessment</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul><li>Headquarters: {escape(HQ)}</li><li>Serving clients nationwide across North America</li></ul></div>
</div>
<div class="copy">Red Rabbit Security &middot; {escape(HQ)} &middot; {escape(PHONE)}<br>
Copyright &copy; 2026. Red Rabbit Security. All rights reserved.</div></div></footer>
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


def form_shell() -> str:
    opts = "".join(
        f'<option>{escape(h["name"])}</option>' for h in HUBS
    )
    return f"""<div class="formbox">
<label>First Name</label><input type="text">
<label>Last Name</label><input type="text">
<label>Email</label><input type="text">
<label>Phone</label><input type="text">
<label>Service Interested In</label><select><option>Please choose&hellip;</option>{opts}<option>Free Security Assessment</option><option>Other</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f95a8">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Red Rabbit Security",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "White Plains",
            "addressRegion": "NY",
            "addressCountry": "US",
        },
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(data, ensure_ascii=True)
        + "</script>"
    )


def home() -> str:
    cards = []
    for h in HUBS:
        kids = "".join(
            f'<li><a href="{h["slug"]}/{s}/index.html">{escape(n)}</a></li>'
            for s, n, _ in h["children"][:3]
        )
        cards.append(
            f'<div class="hubcard"><h3><a href="{h["slug"]}/index.html">{escape(h["name"])}</a></h3>'
            f'<ul>{kids}</ul>'
            f'<a href="{h["slug"]}/index.html" style="font:600 13px \'Segoe UI\',sans-serif">All {escape(h["short"]).lower()} services &rarr;</a></div>'
        )
    return (
        head(
            "Red Rabbit Security | Managed Cybersecurity & IT Nationwide",
            "Red Rabbit Security delivers managed cybersecurity, IT, AI, cloud, and compliance services nationwide from White Plains, NY. Free security assessment.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>Cybersecurity, Managed IT, AI, and Cloud Solutions for Modern Business</h1>
<p>{escape(TAGLINE)}</p>
<a class="btn" href="free-security-assessment/index.html">Get Your Free Security Assessment</a> <a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>TOP 250</b><span>MSP Nationwide</span></div>
<div class="stat"><b>TOP 200</b><span>MSSP 2024</span></div>
<div class="stat"><b>24/7</b><span>SOC Monitoring</span></div>
<div class="stat"><b>99.9%</b><span>Uptime SLA</span></div>
</div></div></section>
<section><div class="wrap"><h2>What can Red Rabbit secure for you?</h2>
<p class="lead">Nine service families — every one delivered as part of a layered, managed security and IT program.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure where the gaps are? Start free.</h2>
<p style="margin-bottom:14px">The free security assessment shows your exposure and priorities — before you spend a dollar.</p>
<a class="btn" href="free-security-assessment/index.html">Request the Free Assessment</a></div></div>
<section><div class="wrap"><h2>How working with Red Rabbit goes</h2><div class="cols3">
<div class="card"><h3>1. Free security assessment</h3><p>We show where you stand — risks, gaps, and quick wins. No cost, no obligation.</p></div>
<div class="card"><h3>2. Fixed written proposal</h3><p>A scoped plan with one number and an honest timeline.</p></div>
<div class="card"><h3>3. Managed protection</h3><p>Expert execution plus 24/7 monitoring, reported in plain English.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why Red Rabbit Security</h2><div class="cols3">
<div class="card"><h3>People, not account numbers</h3><p>Personalized protection for SMBs — enterprise capability without enterprise indifference.</p></div>
<div class="card"><h3>Security in layers</h3><p>Endpoints, identity, email, cloud, backups, and compliance working as one system.</p></div>
<div class="card"><h3>Author-led expertise</h3><p>Founded by Marc Weathers, author of <em>Phishing, Vishing, and Smishing, Oh My!</em></p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready to outsmart risk?</h2>
<a class="btn" href="free-security-assessment/index.html">Free Security Assessment</a> <a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    "What does Red Rabbit Security do?",
                    "We deliver managed cybersecurity, managed IT, AI, cloud, compliance, backup/DR, networking, VoIP, and software services for SMBs — with 24/7 monitoring.",
                ),
                (
                    "Where are you located?",
                    "Headquarters in White Plains, New York (founded 2018), serving clients nationwide across the United States and North America.",
                ),
                (
                    "Is the security assessment really free?",
                    "Yes — we show gaps and a clear plan first, then let the proposal win the work.",
                ),
                (
                    "Do you only work with large enterprises?",
                    "No. We specialize in bringing enterprise-class security and IT to small and medium businesses.",
                ),
            ]
        )
        + org_schema()
        + footer(0)
    )


def hub_page(h: dict) -> str:
    cards = "".join(
        f'<div class="gcard"><h3><a href="{s}/index.html">{escape(n)}</a></h3><p>{escape(b)}</p></div>'
        for s, n, b in h["children"]
    )
    return (
        head(f"{h['name']} | Red Rabbit Security", f"{h['name']} from Red Rabbit Security — {h['blurb']}")
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} — From Red Rabbit Security</h2>
<p class="lead">{escape(h["blurb"])} Delivered as part of a managed, layered program rather than an isolated task.</p>
<p><a class="btn" href="../free-security-assessment/index.html">Get Your Free Security Assessment</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Services We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What Your Campaign Can Include</h2>
<ul class="checks">
<li>Scoped discovery tied to business risk</li>
<li>Implementation with change control</li>
<li>Monitoring and plain-English reporting</li>
<li>Compliance and insurance evidence when needed</li>
<li>One accountable partner across security and IT</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with a free security assessment. We map priorities and provide a written proposal before work begins.",
                ),
                (
                    "Do you work nationwide?",
                    "Yes. Headquartered in White Plains, NY, we support clients across the United States and North America.",
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
        head(f"{name} | Red Rabbit Security", f"{name} from Red Rabbit Security — {blurb}")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Rely on Red Rabbit Security as your go-to partner for {escape(name.lower())} and related services.</h2>
<p class="lead">{escape(blurb)} At Red Rabbit Security, {escape(name.lower())} is delivered as part of a managed, layered program — measured, reported, and pointed at risk reduction.</p>
<p><a class="btn" href="../../free-security-assessment/index.html">Get Your Free Security Assessment</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(name)} Combined with a Managed Program from Red Rabbit Can Help Your Business Gain:</h2>
<ul class="checks">
<li>Lower exposure from the threats that actually hit SMBs</li>
<li>Better visibility for leadership and insurers</li>
<li>Standardized operations with accountable response</li>
<li>Documentation ready for audits and due diligence</li>
<li>24/7 monitoring where it matters most</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} engagement scoped to your business — not a one-size package</h2>
<p>No two businesses need {escape(name.lower())} the same way. We design around your stack, compliance obligations, and what downtime costs — then put scope and price in writing before work begins.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Businesses avoid key risks by using a developed security partner for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with tools-only or break-fix approaches</h3><ul>
<li>Tools purchased without owners or tuning</li>
<li>Alerts nobody reviews until after an incident</li>
<li>Policies written once and never tested</li>
<li>Reporting that shows activity, not risk reduction</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on Red Rabbit Security</h3><ul>
<li>Layered controls operated as one system</li>
<li>Clear escalation and response paths</li>
<li>Evidence-friendly reporting for leadership</li>
<li>Subscription accountability with a named team</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>See where you stand first — free</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} would look like for your business? Start with our free security assessment.</p>
<a class="btn" href="../../free-security-assessment/index.html">Get Your Free Security Assessment</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} shows results?",
                    "Timelines depend on your environment. Your proposal includes an honest schedule, and reporting tracks progress against it.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Scope drives price. After the free assessment we provide a fixed written proposal.",
                ),
                (
                    f"Why choose Red Rabbit for {name.lower()}?",
                    f"We deliver {name.lower()} inside a layered managed program — White Plains accountability with nationwide reach.",
                ),
            ]
        )
        + f'<section><div class="wrap"><h2>Related {escape(h["short"])} Services</h2><div class="grid">{related}</div></div></section>'
        + footer(2)
    )


def cta_page(slug: str, title: str, h2: str, lead: str) -> str:
    return (
        head(title, lead)
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h2)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:29px">{escape(h2)}</h2>
<h2 style="font-size:20px">Initiate a request with Red Rabbit Security</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us what's happening</h3><p>A few sentences is plenty — we'll ask the right follow-ups.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>An assessment, a proposal, or honest advice — whichever fits.</p></div>
<div class="card"><h3>3. Decide with the full picture</h3><p>Plan and price in writing before you commit anything.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>Red Rabbit Security</strong><br>Headquarters: {escape(HQ)}<br>Phone: {escape(PHONE)}<br>Email: {escape(EMAIL)}</p>
</div></section>
"""
        + (org_schema() if slug == "contact" else "")
        + footer(1)
    )


def main() -> None:
    # wipe prior generated site trees (keep scripts / git)
    keep = {".git", "scripts", "REDRABBIT-QUESTIONNAIRE-ANSWERS.md"}
    for child in list(ROOT.iterdir()):
        if child.name in keep or child.name.startswith("."):
            continue
        if child.is_file():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)

    urls = ["/"]
    write(ROOT / "index.html", home())

    for h in HUBS:
        write(ROOT / h["slug"] / "index.html", hub_page(h))
        urls.append(f"/{h['slug']}/")
        for child in h["children"]:
            write(ROOT / h["slug"] / child[0] / "index.html", leaf_page(h, child))
            urls.append(f"/{h['slug']}/{child[0]}/")

    write(
        ROOT / "about-red-rabbit-security" / "index.html",
        head("About Red Rabbit Security | White Plains, NY", "Red Rabbit Security was founded in 2018 in White Plains, NY.")
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About Red Rabbit Security</h2>
<p class="lead">Established in 2018 and headquartered in {escape(HQ)}, Red Rabbit Security delivers enterprise-class cybersecurity, managed IT, cloud, compliance, backup, VoIP, AI, and software services to small and medium-sized businesses.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>We started Red Rabbit Security because growing businesses need the same protection as larger enterprises — without inflated pricing. Founder Marc Weathers is the author of <em>Phishing, Vishing, and Smishing, Oh My!</em></p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="industries-we-serve/index.html">Industries &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                ("When was Red Rabbit founded?", "Red Rabbit Security was established in 2018 and is headquartered in White Plains, NY."),
                ("Do you work outside New York?", "Yes — nationwide across the United States and throughout North America."),
            ]
        )
        + org_schema()
        + footer(1),
    )
    urls.append("/about-red-rabbit-security/")

    write(
        ROOT / "about-red-rabbit-security" / "why-choose-us" / "index.html",
        head("Why Choose Red Rabbit Security", "Why businesses choose Red Rabbit for managed cybersecurity and IT.")
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose Red Rabbit Security</h2>
<p class="lead">A strategic technology partner built to help SMBs outsmart risk, outpace disruption, and outlast the unexpected.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Layered by design</h3><p>Endpoints, identity, email, cloud, backups, and compliance operated together.</p></div>
<div class="card"><h3>SMB-first economics</h3><p>Enterprise-class controls through accessible subscription models.</p></div>
<div class="card"><h3>Named humans</h3><p>People who know your environment — not a faceless queue.</p></div>
<div class="card"><h3>Assessment-led sales</h3><p>Free assessment first; written scope before you commit.</p></div>
<div class="card"><h3>Nationwide reach</h3><p>White Plains HQ with delivery across the U.S. and North America.</p></div>
<div class="card"><h3>Author-informed training</h3><p>Awareness grounded in real phishing, vishing, and smishing patterns.</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-red-rabbit-security/why-choose-us/")

    ind = "".join(
        f'<div class="gcard"><h3>{escape(i)}</h3><p>Security and IT tuned to {escape(i.lower())} operations and compliance.</p></div>'
        for i in INDUSTRIES
    )
    write(
        ROOT / "about-red-rabbit-security" / "industries-we-serve" / "index.html",
        head("Industries We Serve | Red Rabbit Security", "Industry-focused cybersecurity and managed IT from Red Rabbit Security.")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Industries</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Industries We Serve</h2>
<p class="lead">Specialized solutions tailored to your industry's compliance and operational requirements.</p>
<div class="grid">{ind}</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-red-rabbit-security/industries-we-serve/")

    for slug, title, h2, lead in [
        ("contact", "Contact Us | Red Rabbit Security", "Contact Us for Security & IT Inquiries", "Tell us what's going on — security concern, IT friction, or compliance deadline."),
        ("free-security-assessment", "Free Security Assessment | Red Rabbit Security", "Get Your Free Security Assessment", "See your exposure, priorities, and a clear plan — before you spend."),
        ("request-a-proposal", "Request a Proposal | Red Rabbit Security", "Request a Proposal", "Share your goals. We'll return a scoped proposal you can compare anywhere."),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | Red Rabbit Security", "Page not found.")
        + chrome(0)
        + """
<section style="padding:72px 0"><div class="wrap"><h2 style="font-size:28px">Page not found</h2>
<p class="lead">That URL isn't in our burrow. Try home or the free security assessment.</p>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn alt" href="free-security-assessment/index.html">Free Assessment</a></p>
</div></section>
"""
        + footer(0),
    )

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
""",
    )
    write(
        ROOT / "_redirects",
        "/*    /404.html  404\n",
    )
    write(
        ROOT / "REDRABBIT-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — Red Rabbit Security (DEMO BUILD · Factory Template)

**Build uses NearMe OS Website Factory instructions-template (SEO Cow staging engine) · facts from live redrabbitsec.com**

| Field | Value |
|---|---|
| business_name | Red Rabbit Security |
| domain | redrabbitsec.com |
| phone | {PHONE} |
| email | {EMAIL} |
| hq | {HQ} |
| founded | 2018 |
| founder | Marc Weathers |
| tagline | {TAGLINE} |
| hubs | {len(HUBS)} |
| children | {sum(len(h['children']) for h in HUBS)} |
| staging | noindex + STAGING PREVIEW banner (matches seocow Netlify pattern) |
""",
    )

    pages = list(ROOT.rglob("index.html"))
    print(f"Generated {len(pages)} pages (factory template)")
    print(f"Sitemap URLs: {len(urls)}")


if __name__ == "__main__":
    main()
