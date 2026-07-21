#!/usr/bin/env python3
"""Generate a static Website Factory demo for Red Rabbit Security (redrabbitsec.com)."""

from __future__ import annotations

import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT  # write deployable site at repo root
BASE = "https://redrabbitsec.com"

PHONE = "(914) 281-5352"
PHONE_TEL = "+19142815352"
EMAIL = "info@redrabbitsec.com"
ADDRESS = "White Plains, NY"
LEGAL = "Red Rabbit Security"
FOUNDED = "2018"
TAGLINE = "Outsmart. Outpace. Outlast."
SLOGAN = "Enterprise-grade cybersecurity and managed IT for modern businesses"

# 9 hubs × 8 children
HUBS: list[dict] = [
    {
        "slug": "managed-cybersecurity-services",
        "name": "Managed Cybersecurity Services",
        "short": "Cybersecurity",
        "keyword": "managed cybersecurity services",
        "blurb": "24/7 monitoring, detection, and response across endpoints, email, identity, and cloud — layered defense without building an in-house SOC.",
        "children": [
            ("managed-siem-services", "Managed SIEM Services", "managed SIEM services", "Security information and event management with 24/7 analyst review and actionable alerting."),
            ("next-generation-antivirus-endpoint-protection", "Next-Gen Endpoint Protection", "next generation antivirus endpoint protection", "NGAV and EDR that stop ransomware and malware before they spread."),
            ("managed-anti-phishing-email-security", "Managed Email Security", "managed anti phishing email security", "Anti-phishing, anti-spam, and business-email-compromise defenses for every inbox."),
            ("identity-and-access-management", "Identity & Access Management", "identity and access management services", "MFA, least-privilege access, and identity hardening for users and admins."),
            ("vulnerability-scanning-and-assessment", "Vulnerability Scanning", "continuous vulnerability scanning services", "Continuous scanning, prioritized remediation, and proof for audits and insurers."),
            ("penetration-testing-services", "Penetration Testing", "professional penetration testing services", "Authorized offensive testing that finds exploitable gaps before attackers do."),
            ("incident-response-and-breach-recovery", "Incident Response", "rapid incident response services", "Rapid containment, investigation, and recovery when minutes matter."),
            ("virtual-ciso-services", "Virtual CISO (vCISO)", "virtual CISO services", "Executive security leadership on a subscription — strategy, boards, and roadmaps."),
        ],
    },
    {
        "slug": "managed-it-services",
        "name": "Managed IT Services",
        "short": "Managed IT",
        "keyword": "managed IT services",
        "blurb": "Proactive help desk, patching, monitoring, and administration that keep people productive while security stays built in.",
        "children": [
            ("unlimited-tech-support", "Unlimited Tech Support", "unlimited tech support services", "US-based help desk coverage for day-to-day user and workstation issues."),
            ("managed-help-desk-services", "Managed Help Desk", "managed help desk services", "Ticketed support with SLAs, documentation, and clear escalation paths."),
            ("patch-management-services", "Patch Management", "network security patch management", "Coordinated OS and application patching that reduces exploit windows."),
            ("it-asset-management", "IT Asset Management", "managed IT asset management", "Hardware and software inventory you can actually trust for audits and refreshes."),
            ("microsoft-365-administration", "Microsoft 365 Administration", "Microsoft 365 administration services", "Secure tenant setup, licensing hygiene, SharePoint/Teams, and ongoing admin."),
            ("co-managed-it-services", "Co-Managed IT", "co-managed IT services", "Augment your internal IT team with specialized security and operations support."),
            ("virtual-cio-services", "Virtual CIO Services", "virtual CIO services", "Technology planning and vendor oversight aligned to business goals."),
            ("onboarding-offboarding-services", "User Onboarding & Offboarding", "IT onboarding and offboarding services", "Secure joiner/mover/leaver workflows that protect access on day one and day last."),
        ],
    },
    {
        "slug": "ai-business-solutions",
        "name": "AI Business Solutions",
        "short": "AI Solutions",
        "keyword": "AI business solutions",
        "blurb": "Practical AI automation and governance that improve operations without creating new security blind spots.",
        "children": [
            ("ai-automation-consulting", "AI Automation Consulting", "AI automation consulting", "Identify high-ROI workflows ready for safe, governed automation."),
            ("secure-ai-adoption", "Secure AI Adoption", "secure AI adoption services", "Policies, tooling, and controls so AI tools do not leak company data."),
            ("ai-powered-security-operations", "AI-Powered Security Ops", "AI powered security operations", "Smarter triage and detection assistance layered onto your SOC stack."),
            ("business-process-ai", "Business Process AI", "business process AI solutions", "Document, ticket, and ops automation that frees staff for higher-value work."),
            ("ai-readiness-assessment", "AI Readiness Assessment", "AI readiness assessment", "A clear scorecard of data, tooling, and risk before you scale AI projects."),
            ("custom-ai-integrations", "Custom AI Integrations", "custom AI integrations", "Connect models and copilots to the systems your teams already use."),
            ("ai-governance-and-policy", "AI Governance & Policy", "AI governance and policy services", "Acceptable-use, retention, and oversight frameworks leadership can enforce."),
            ("employee-ai-training", "Employee AI Training", "employee AI training programs", "Practical training so staff use AI productively and safely."),
        ],
    },
    {
        "slug": "cloud-computing-services",
        "name": "Cloud Computing Services",
        "short": "Cloud",
        "keyword": "cloud computing services",
        "blurb": "Secure cloud design, migration, and management across Azure, AWS, and Google Cloud.",
        "children": [
            ("cloud-migration-services", "Cloud Migration Services", "expert cloud migration services", "Planned migrations with security baselines, not lift-and-hope cutovers."),
            ("microsoft-azure-consulting", "Microsoft Azure Consulting", "Microsoft Azure consulting services", "Landing zones, identity, and cost-aware Azure administration."),
            ("managed-aws-services", "Managed AWS Services", "managed AWS services", "Guardrails, monitoring, and operations for Amazon Web Services workloads."),
            ("google-cloud-platform-services", "Google Cloud Services", "managed Google Cloud Platform services", "GCP projects hardened for identity, networking, and billing clarity."),
            ("cloud-security-posture", "Cloud Security Posture", "cloud security posture management", "Misconfiguration hunting and continuous cloud security hygiene."),
            ("email-migration-services", "Email Migration Services", "email migration services for businesses", "Mailbox moves to Microsoft 365 or Google Workspace with minimal downtime."),
            ("cloud-backup-integration", "Cloud Backup Integration", "cloud backup integration services", "Backup architecture that matches your cloud footprint and RTO targets."),
            ("hybrid-cloud-architecture", "Hybrid Cloud Architecture", "hybrid cloud architecture services", "On-prem and cloud designs that stay operable and auditable."),
        ],
    },
    {
        "slug": "compliance-regulatory-services",
        "name": "Compliance & Regulatory Services",
        "short": "Compliance",
        "keyword": "compliance regulatory services",
        "blurb": "Audit-ready programs for HIPAA, PCI, NYDFS, CMMC, SOC 2, and more — with continuous evidence, not binder theater.",
        "children": [
            ("hipaa-compliance-services", "HIPAA Compliance Services", "HIPAA healthcare data protection compliance", "Security risk analysis, safeguards, and ongoing HIPAA program support."),
            ("pci-dss-compliance-services", "PCI-DSS Compliance", "PCI DSS compliance services", "Cardholder-data scoping, controls, and remediation guidance."),
            ("nydfs-500-compliance", "NYDFS 23 NYCRR 500", "NYDFS cybersecurity regulation compliance", "Cybersecurity program support for covered New York entities."),
            ("cmmc-compliance-services", "CMMC Compliance", "CMMC compliance services", "Defense-contractor readiness for Cybersecurity Maturity Model Certification."),
            ("soc-2-readiness", "SOC 2 Readiness", "SOC 2 readiness services", "Control design and evidence collection that prepare you for attestation."),
            ("cyber-insurance-readiness", "Cyber Insurance Readiness", "cyber security insurance readiness", "Close questionnaire gaps insurers actually care about before renewal."),
            ("compliance-gap-assessment", "Compliance Gap Assessment", "technology audit and compliance overview", "A prioritized map of what auditors will flag — and what to fix first."),
            ("ongoing-compliance-monitoring", "Ongoing Compliance Monitoring", "ongoing compliance management services", "Continuous control checks so you are not scrambling every audit season."),
        ],
    },
    {
        "slug": "backup-disaster-recovery",
        "name": "Backup & Disaster Recovery",
        "short": "Backup & DR",
        "keyword": "backup and disaster recovery",
        "blurb": "Tested backups and recovery plans that keep ransomware and outages from becoming business endings.",
        "children": [
            ("managed-backup-services", "Managed Backup Services", "managed backup services", "Automated backups across endpoints, servers, and cloud with restore testing."),
            ("disaster-recovery-planning", "Disaster Recovery Planning", "disaster recovery planning services", "Documented runbooks, owners, and recovery priorities leadership can execute."),
            ("draas-services", "DRaaS", "disaster recovery as a service", "Failover capacity when your primary site or cloud region is unavailable."),
            ("ransomware-recovery-services", "Ransomware Recovery", "ransomware recovery services", "Clean recovery paths that avoid paying — and avoid reinfection."),
            ("business-continuity-planning", "Business Continuity Planning", "business continuity planning services", "Keep critical operations running through outages and incidents."),
            ("backup-monitoring-reporting", "Backup Monitoring & Reporting", "backup monitoring and reporting", "Proof restores work — monthly reporting instead of hopeful green checks."),
            ("immutable-backup-solutions", "Immutable Backups", "immutable backup solutions", "Backup copies attackers cannot encrypt or delete."),
            ("cloud-data-backup", "Cloud Data Backup", "managed remote cloud data backup", "Protect Microsoft 365, Google Workspace, and SaaS data vendors do not fully cover."),
        ],
    },
    {
        "slug": "network-infrastructure-services",
        "name": "Network Infrastructure Services",
        "short": "Network",
        "keyword": "network infrastructure services",
        "blurb": "Design, secure, and operate the networks your business depends on — wired, wireless, and WAN.",
        "children": [
            ("network-design-and-implementation", "Network Design & Implementation", "managed network security design", "Secure architectures sized for growth, not yesterday’s headcount."),
            ("managed-wifi-services", "Managed Wi-Fi Services", "managed wifi wireless network services", "Business-grade wireless with segmentation and guest isolation."),
            ("firewall-management", "Firewall Management", "managed firewall services", "Configuration, monitoring, and change control for perimeter defenses."),
            ("network-cabling-services", "Network Cabling Services", "network data cabling services", "Clean copper and fiber plant that supports reliable throughput."),
            ("network-diagnostics-support", "Network Diagnostics", "network support diagnostic services", "Fast root-cause analysis when performance or connectivity fails."),
            ("secure-remote-access-vpn", "Secure Remote Access / VPN", "secure remote access VPN services", "Remote work access that does not punch holes in your security model."),
            ("sd-wan-services", "SD-WAN Services", "SD-WAN services for business", "Smarter site connectivity with policy-based routing and visibility."),
            ("network-segmentation", "Network Segmentation", "network segmentation services", "Contain breaches by limiting east-west movement across your environment."),
        ],
    },
    {
        "slug": "business-voip-services",
        "name": "Business VoIP Services",
        "short": "VoIP",
        "keyword": "business VoIP services",
        "blurb": "Fully managed cloud phone systems that keep teams reachable — with security and uptime built in.",
        "children": [
            ("managed-voip-phone-systems", "Managed VoIP Phone Systems", "fully managed VoIP phone systems", "Hosted PBX, devices, and administration under one accountable partner."),
            ("cloud-phone-system-setup", "Cloud Phone System Setup", "cloud based VoIP phone services", "Number porting, call flows, and go-live support with minimal disruption."),
            ("unified-communications", "Unified Communications", "unified communications services", "Voice, video, and messaging that follow users across devices."),
            ("call-center-voip", "Call Center VoIP", "call center VoIP services", "Queues, IVR, and reporting for customer-facing teams."),
            ("voip-security-hardening", "VoIP Security Hardening", "VoIP security hardening services", "Fraud controls, encryption, and abuse monitoring for phone systems."),
            ("microsoft-teams-calling", "Microsoft Teams Calling", "Microsoft Teams calling services", "Direct Routing / Calling Plans integrated with your M365 tenant."),
            ("voip-migration-services", "VoIP Migration Services", "VoIP migration services", "Leave aging PBXs without losing numbers or call quality."),
            ("business-sms-communications", "Business SMS & Communications", "business SMS communications services", "Compliant messaging channels connected to your contact workflows."),
        ],
    },
    {
        "slug": "software-application-development",
        "name": "Software & Application Development",
        "short": "Software",
        "keyword": "software application development",
        "blurb": "Custom software, integrations, and apps built with security and maintainability from the first commit.",
        "children": [
            ("custom-software-development", "Custom Software Development", "custom software development services", "Line-of-business applications tailored to how your teams actually work."),
            ("mobile-application-development", "Mobile App Development", "mobile application development services", "iOS and Android apps with secure auth and update paths."),
            ("web-application-development", "Web Application Development", "web application development services", "Modern web apps hardened against the OWASP risks that matter."),
            ("business-application-integration", "Business App Integration", "business application integration services", "Connect CRM, ERP, and SaaS tools without brittle spreadsheet glue."),
            ("api-development-services", "API Development", "API development services", "Stable APIs with auth, rate limits, and documentation your partners can use."),
            ("legacy-application-modernization", "Legacy App Modernization", "legacy application modernization", "Retire fragile stacks while preserving the workflows you cannot lose."),
            ("secure-sdlc-consulting", "Secure SDLC Consulting", "secure SDLC consulting", "Embed security reviews into build pipelines and release habits."),
            ("application-support-maintenance", "Application Support & Maintenance", "application support and maintenance", "Ongoing fixes, patches, and enhancements after launch."),
        ],
    },
]

INDUSTRIES = [
    "Healthcare",
    "Legal",
    "Finance",
    "Manufacturing",
    "Education",
    "Real Estate",
    "Retail",
    "Hospitality",
    "Construction",
    "Non-Profit",
    "Government",
    "Logistics",
]

CSS = """
:root{
  --ink:#141012;
  --muted:#5c5360;
  --paper:#f6f3f1;
  --paper-2:#ebe4df;
  --crimson:#c1121f;
  --crimson-deep:#8a0c16;
  --rabbit:#e8d5c4;
  --line:rgba(20,16,18,.12);
  --ok:#1f6b4a;
  --bad:#8a0c16;
  --max:1120px;
  --display:'Syne',sans-serif;
  --body:'Source Serif 4',Georgia,serif;
  --ui:'DM Sans',sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:var(--body);color:var(--ink);background:var(--paper);line-height:1.65;font-size:17px}
a{color:var(--crimson-deep);text-decoration:none}
a:hover{text-decoration:underline}
img{max-width:100%;display:block}
.skip-link{position:absolute;left:-999px;top:auto;width:1px;height:1px;overflow:hidden}
.skip-link:focus{position:static;width:auto;height:auto;display:inline-block;padding:8px 14px;background:var(--crimson);color:#fff;font:700 13px var(--ui);z-index:100}
.wrap{max-width:var(--max);margin:0 auto;padding:0 22px}
.utility{background:var(--ink);color:var(--rabbit);font:500 12.5px/1.4 var(--ui);padding:7px 0;letter-spacing:.02em}
.utility .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
header.main{background:rgba(246,243,241,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:40}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding:14px 22px;gap:16px;flex-wrap:wrap}
a.logo{font-family:var(--display);font-weight:800;font-size:1.35rem;color:var(--ink);letter-spacing:-.03em;text-decoration:none;display:flex;align-items:center;gap:10px}
a.logo .mark{width:34px;height:34px;border-radius:10px;background:linear-gradient(145deg,var(--crimson),var(--crimson-deep));display:grid;place-items:center;color:#fff;font-size:15px;box-shadow:0 6px 16px rgba(193,18,31,.28)}
a.logo small{display:block;font:600 10px/1.2 var(--ui);color:var(--muted);letter-spacing:.14em;text-transform:uppercase;margin-top:2px}
.phone-cta{text-align:right;font-family:var(--ui)}
.phone-cta a{font-size:1.15rem;font-weight:800;color:var(--ink);text-decoration:none}
.phone-cta small{display:block;color:var(--muted);font-size:11px}
nav.nav{background:var(--crimson-deep)}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 14px;font:600 13px var(--ui)}
nav.nav a:hover{background:rgba(0,0,0,.18);text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:260px;box-shadow:0 12px 30px rgba(20,16,18,.16);border-top:3px solid var(--crimson);z-index:50}
.dd a{color:var(--ink);padding:10px 14px;font-weight:500;border-bottom:1px solid #f0ebe8}
.dd a:hover{background:#f8efef}
.nav .em a{background:var(--crimson)}
.hero{position:relative;color:#fff;padding:78px 0 70px;overflow:hidden;background:
  radial-gradient(ellipse 80% 70% at 15% 20%,rgba(193,18,31,.55),transparent 55%),
  radial-gradient(ellipse 60% 50% at 85% 75%,rgba(232,213,196,.18),transparent 50%),
  linear-gradient(155deg,#1a1012 0%,#2a1518 42%,#141012 100%)}
.hero::after{content:"";position:absolute;inset:0;background:
  repeating-linear-gradient(-28deg,transparent 0 22px,rgba(255,255,255,.025) 22px 23px);pointer-events:none}
.hero .wrap{position:relative;z-index:1}
.hero .brand-kicker{font:800 13px/1 var(--ui);letter-spacing:.22em;text-transform:uppercase;color:#f0b7b7;margin-bottom:16px}
.hero h1{font-family:var(--display);font-weight:800;font-size:clamp(2rem,5vw,3.35rem);line-height:1.08;letter-spacing:-.035em;max-width:16ch;margin-bottom:18px}
.hero p{font:500 1.05rem/1.55 var(--ui);color:#f0e6e0;max-width:38rem}
.hero .actions{margin-top:28px;display:flex;flex-wrap:wrap;gap:12px}
.btn{display:inline-block;background:var(--crimson);color:#fff;font:700 14px var(--ui);padding:13px 24px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#d41424;text-decoration:none}
.btn.alt{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.45)}
.btn.alt:hover{background:rgba(255,255,255,.08)}
.btn.dark{background:var(--ink);color:#fff}
section{padding:52px 0}
section.tint{background:linear-gradient(180deg,var(--paper-2),var(--paper))}
section h1,section h2,.page-title{font-family:var(--display);font-weight:800;letter-spacing:-.03em;line-height:1.15;color:var(--ink);margin-bottom:14px}
section h2{font-size:clamp(1.55rem,3vw,2rem)}
h1.page-title{font-size:clamp(1.8rem,3.4vw,2.4rem)}
.lead{font-size:1.08rem;color:var(--muted);max-width:46rem}
p{margin-bottom:14px}
ul.checks{list-style:none;margin:12px 0}
ul.checks li{padding:8px 0 8px 30px;position:relative}
ul.checks li:before{content:"✓";position:absolute;left:0;color:var(--crimson);font-weight:800;font-family:var(--ui)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}
.stat{background:#fff;border:1px solid var(--line);border-top:4px solid var(--crimson);border-radius:8px;padding:18px;text-align:center}
.stat b{display:block;font:800 1.35rem var(--display);color:var(--ink)}
.stat span{font:600 11px var(--ui);color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.hubcard{background:#fff;border:1px solid var(--line);border-radius:10px;padding:22px;transition:transform .2s ease,box-shadow .2s ease}
.hubcard:hover{transform:translateY(-3px);box-shadow:0 14px 28px rgba(20,16,18,.08)}
.hubcard h3{font:800 1.05rem var(--display);margin-bottom:8px}
.hubcard h3 a{color:var(--ink);text-decoration:none}
.hubcard p{font-size:.95rem;color:var(--muted);margin:0 0 10px}
.hubcard ul{list-style:none;margin:8px 0 12px}
.hubcard li{padding:3px 0 3px 18px;position:relative;font-size:.88rem;font-family:var(--ui)}
.hubcard li:before{content:"→";position:absolute;left:0;color:var(--crimson);font-weight:700}
.hubcard .more{font:700 13px var(--ui);color:var(--crimson-deep)}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:22px}
.card h3{font:800 1.05rem var(--display);margin-bottom:8px}
.gcard{background:#fff;border:1px solid var(--line);border-left:4px solid var(--crimson);border-radius:8px;padding:18px}
.gcard h3{font:800 .98rem var(--display);margin-bottom:6px}
.gcard h3 a{color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;margin-top:18px}
.ctastrip{background:var(--ink);color:#fff;text-align:center;padding:48px 0}
.ctastrip h2{color:#fff}
.ctastrip p{color:#e8d5c4;max-width:40rem;margin:0 auto 18px;font-family:var(--ui)}
.audit{background:linear-gradient(120deg,var(--crimson-deep),var(--crimson));color:#fff;text-align:center;padding:40px 0}
.audit h2{color:#fff}
.audit .btn{background:#fff;color:var(--crimson-deep)}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-top:18px}
.vs .col{padding:22px}
.vs .col.bad{background:#faf2f2}
.vs .col.good{background:#f3f8f5}
.vs h3{font:800 .95rem var(--display);margin-bottom:10px}
.vs ul{list-style:none}
.vs li{padding:8px 0 8px 26px;position:relative;font-size:.95rem;border-bottom:1px dashed #e5ddd8;font-family:var(--ui)}
.vs .bad li:before{content:"✗";position:absolute;left:2px;color:var(--bad);font-weight:800}
.vs .good li:before{content:"✓";position:absolute;left:2px;color:var(--ok);font-weight:800}
details{border:1px solid var(--line);border-radius:8px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:700 15px var(--ui);color:var(--ink);list-style:none}
details summary:before{content:"+ ";color:var(--crimson);font-weight:800}
details[open] summary:before{content:"– "}
details div{padding:0 18px 16px;font-size:1rem}
.formbox{background:#fff;border:1px solid var(--line);border-top:4px solid var(--crimson);border-radius:10px;padding:26px;max-width:640px}
.formbox label{display:block;font:700 12px var(--ui);color:var(--muted);margin:12px 0 4px;letter-spacing:.04em;text-transform:uppercase}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:11px 12px;border:1px solid #d5cdc7;border-radius:6px;font:15px var(--ui);background:#fff}
.formbox textarea{min-height:100px}
.form-note{margin-top:12px;font:12px var(--ui);color:var(--muted)}
.form-success{display:none;background:#eef7f1;border:1px solid #1f6b4a;border-radius:6px;padding:12px 14px;margin-bottom:12px;font:600 14px var(--ui);color:var(--ok)}
.crumb{font:12.5px var(--ui);color:var(--muted);padding:16px 0 0}
.crumb a{color:var(--muted)}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:18px 0}
.pillrow{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.pillrow span{font:700 12px var(--ui);padding:7px 12px;border-radius:999px;background:#fff;border:1px solid var(--line);color:var(--ink)}
footer{background:#100c0e;color:#c9b8b0;padding:48px 0 28px;margin-top:20px;font:14px var(--ui)}
footer h4{color:#fff;font:800 12px var(--ui);letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}
footer li{margin-bottom:7px}
footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:24px}
.copy{border-top:1px solid rgba(255,255,255,.1);margin-top:28px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
@media(max-width:760px){
  .vs{grid-template-columns:1fr}
  .hero{padding:56px 0 48px}
}
"""


def rel_prefix(depth: int) -> str:
    return "" if depth == 0 else "../" * depth


def home_href(depth: int) -> str:
    return "index.html" if depth == 0 else f"{rel_prefix(depth)}index.html"


def page_url(path: str) -> str:
    if path in ("", "/"):
        return f"{BASE}/"
    return f"{BASE}/{path.strip('/')}/"


def truncate(text: str, limit: int = 155) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0]
    return cut.rstrip(" ,.;:") + "…"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def head(
    title: str,
    description: str,
    canonical: str,
    depth: int,
    extra: str = "",
) -> str:
    p = rel_prefix(depth)
    desc = truncate(description)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{escape(canonical)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{escape(canonical)}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="{BASE}/assets/images/og-default.svg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;700;800&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=Syne:wght@700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/css/site.css">
{extra}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
"""


def chrome_top(depth: int) -> str:
    p = rel_prefix(depth)
    h = home_href(depth)
    service_links = "".join(
        f'<a href="{p}{hub["slug"]}/index.html">{escape(hub["name"])}</a>' for hub in HUBS
    )
    return f"""
<div class="utility"><div class="wrap"><span>{escape(TAGLINE)}</span><span>{escape(ADDRESS)} · {escape(PHONE)}</span></div></div>
<header class="main"><div class="wrap">
<a class="logo" href="{h}"><span class="mark" aria-hidden="true">R</span><span>Red Rabbit<small>Security</small></span></a>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Free security assessment</small></div>
</div></header>
<nav class="nav" aria-label="Primary"><div class="wrap"><ul>
<li><a href="{h}">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services ▾</a><div class="dd">{service_links}</div></li>
<li><a href="{p}about-red-rabbit-security/index.html">About ▾</a><div class="dd">
<a href="{p}about-red-rabbit-security/index.html">About Red Rabbit</a>
<a href="{p}about-red-rabbit-security/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-red-rabbit-security/industries-we-serve/index.html">Industries We Serve</a>
</div></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li class="em"><a href="{p}free-security-assessment/index.html">Free Assessment</a></li>
</ul></div></nav>
<main id="main">
"""


def chrome_bottom(depth: int) -> str:
    p = rel_prefix(depth)
    hubs = "".join(
        f'<li><a href="{p}{hub["slug"]}/index.html">{escape(hub["short"])}</a></li>'
        for hub in HUBS
    )
    return f"""
</main>
<footer><div class="wrap"><div class="fcols">
<div><h4>Services</h4><ul>{hubs}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="{p}about-red-rabbit-security/index.html">About</a></li>
<li><a href="{p}about-red-rabbit-security/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-red-rabbit-security/industries-we-serve/index.html">Industries</a></li>
<li><a href="{p}contact/index.html">Contact</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}free-security-assessment/index.html">Free Security Assessment</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul>
<li>Headquarters: {escape(ADDRESS)}</li>
<li>Serving clients nationwide across North America</li>
<li>Founded {FOUNDED}</li>
</ul></div>
</div>
<div class="copy">{escape(LEGAL)} · {escape(ADDRESS)} · {escape(PHONE)}<br>
Copyright © 2026. Red Rabbit Security. All rights reserved.</div></div></footer>
<script src="{p}assets/js/forms.js" defer></script>
</body></html>
"""


def faq_block(items: list[tuple[str, str]]) -> str:
    parts = ['<section class="tint"><div class="wrap"><h2>Frequently Asked Questions</h2>']
    entities = []
    for q, a in items:
        parts.append(
            f"<details><summary>{escape(q)}</summary><div><p>{escape(a)}</p></div></details>"
        )
        entities.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )
    parts.append("</div></section>")
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }
    parts.append(
        '<script type="application/ld+json">'
        + json.dumps(schema, ensure_ascii=True)
        + "</script>"
    )
    return "\n".join(parts)


def form_box(form_id: str, submit: str) -> str:
    opts = ['<option value="">Please choose…</option>']
    for hub in HUBS:
        opts.append(f'<option value="{hub["slug"]}">{escape(hub["name"])}</option>')
    opts.append('<option value="free-security-assessment">Free Security Assessment</option>')
    opts.append('<option value="other">Other / Not sure</option>')
    return f"""
<div class="formbox">
<div class="form-success" role="status" hidden>Thanks — your email app should open with the message ready. If not, email {escape(EMAIL)}.</div>
<form id="{form_id}" class="lead-form" action="mailto:{EMAIL}" method="post" enctype="text/plain">
<label for="{form_id}-first">First Name</label>
<input id="{form_id}-first" name="first_name" type="text" autocomplete="given-name" required>
<label for="{form_id}-last">Last Name</label>
<input id="{form_id}-last" name="last_name" type="text" autocomplete="family-name" required>
<label for="{form_id}-email">Email</label>
<input id="{form_id}-email" name="email" type="email" autocomplete="email" required>
<label for="{form_id}-phone">Phone</label>
<input id="{form_id}-phone" name="phone" type="tel" autocomplete="tel">
<label for="{form_id}-company">Company</label>
<input id="{form_id}-company" name="company" type="text" autocomplete="organization">
<label for="{form_id}-service">Service Interested In</label>
<select id="{form_id}-service" name="service" required>{''.join(opts)}</select>
<label for="{form_id}-message">Message</label>
<textarea id="{form_id}-message" name="message" required></textarea>
<div style="margin-top:16px"><button class="btn" type="submit">{escape(submit)}</button></div>
<p class="form-note">Submits via your email app to {escape(EMAIL)}. Replace with a server endpoint at rollout.</p>
</form>
</div>
"""


ORG_SCHEMA = {
    "@context": "https://schema.org",
    "@type": ["ProfessionalService", "LocalBusiness"],
    "name": "Red Rabbit Security",
    "url": BASE + "/",
    "telephone": PHONE_TEL,
    "email": EMAIL,
    "foundingDate": FOUNDED,
    "slogan": TAGLINE,
    "image": BASE + "/assets/images/og-default.svg",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "White Plains",
        "addressRegion": "NY",
        "addressCountry": "US",
    },
    "areaServed": ["United States", "Canada", "Mexico"],
    "priceRange": "$$",
}


def org_script() -> str:
    return (
        '<script type="application/ld+json">'
        + json.dumps(ORG_SCHEMA, ensure_ascii=True)
        + "</script>"
    )


def render_home() -> str:
    hubs_html = []
    for hub in HUBS:
        kids = "".join(
            f'<li><a href="{hub["slug"]}/{slug}/index.html">{escape(name)}</a></li>'
            for slug, name, _, _ in hub["children"][:3]
        )
        hubs_html.append(
            f"""<div class="hubcard">
<h3><a href="{hub["slug"]}/index.html">{escape(hub["name"])}</a></h3>
<p>{escape(hub["blurb"])}</p>
<ul>{kids}</ul>
<a class="more" href="{hub["slug"]}/index.html">All {escape(hub["short"]).lower()} services →</a>
</div>"""
        )
    faqs = [
        (
            "What does Red Rabbit Security do?",
            "We deliver managed cybersecurity, managed IT, AI, cloud, compliance, backup/DR, networking, VoIP, and software services for SMBs — with 24/7 monitoring and practical, subscription-friendly delivery.",
        ),
        (
            "Where is Red Rabbit Security located?",
            "We are headquartered in White Plains, New York (founded 2018) and serve clients nationwide across the United States, with support also available in Canada and Mexico.",
        ),
        (
            "Do you offer a free security assessment?",
            "Yes. Start with a free security assessment — we review your environment, risks, and priorities, then provide a clear recommendation and pricing path.",
        ),
        (
            "Is Red Rabbit only for large enterprises?",
            "No. We specialize in bringing enterprise-class security and IT to small and medium businesses at accessible subscription rates.",
        ),
    ]
    return (
        head(
            "Red Rabbit Security | Managed Cybersecurity & IT Nationwide",
            "Red Rabbit Security delivers managed cybersecurity, IT, AI, cloud, and compliance services nationwide from White Plains, NY. Free security assessment.",
            page_url("/"),
            0,
        )
        + chrome_top(0)
        + f"""
<div class="hero"><div class="wrap">
<p class="brand-kicker">Red Rabbit Security</p>
<h1>Cybersecurity and managed IT that outlasts the threat</h1>
<p>{escape(SLOGAN)}. 24/7 protection, practical guidance, and subscription services built for growing businesses.</p>
<div class="actions">
<a class="btn" href="free-security-assessment/index.html">Get a Free Security Assessment</a>
<a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a>
</div>
</div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>TOP 250</b><span>MSP nationwide</span></div>
<div class="stat"><b>TOP 200</b><span>MSSP 2024</span></div>
<div class="stat"><b>24/7</b><span>SOC monitoring</span></div>
<div class="stat"><b>99.9%</b><span>Uptime SLA</span></div>
</div></div></section>
<section><div class="wrap">
<h2>What can Red Rabbit secure for you?</h2>
<p class="lead">Nine service families — cybersecurity through software — delivered as measured, layered protection rather than one-off projects.</p>
<div class="cols3">{''.join(hubs_html)}</div>
</div></section>
<div class="audit"><div class="wrap">
<h2>Not sure where the gaps are? Start free.</h2>
<p style="margin:0 auto 16px;max-width:36rem;font-family:var(--ui)">A free security assessment shows your exposure, priorities, and a clear next step — before you spend a dollar.</p>
<a class="btn" href="free-security-assessment/index.html">Request the Free Assessment</a>
</div></div>
<section><div class="wrap">
<h2>How engagement works</h2>
<div class="steps">
<div class="card"><h3>1. Assess</h3><p>We evaluate your current security posture, IT stack, and business risks.</p></div>
<div class="card"><h3>2. Plan</h3><p>A tailored roadmap with scope and pricing in writing.</p></div>
<div class="card"><h3>3. Deploy</h3><p>Implementations designed for minimal disruption.</p></div>
<div class="card"><h3>4. Protect</h3><p>Monitor, maintain, and respond around the clock.</p></div>
</div>
</div></section>
<section class="tint"><div class="wrap">
<h2>Why Red Rabbit</h2>
<div class="cols3">
<div class="card"><h3>People, not account numbers</h3><p>Personalized protection for SMBs — enterprise capability without enterprise indifference.</p></div>
<div class="card"><h3>Security built in layers</h3><p>Endpoints, identity, email, cloud, backups, and compliance working as one system.</p></div>
<div class="card"><h3>Author-led expertise</h3><p>Founded by Marc Weathers, author of <em>Phishing, Vishing, and Smishing, Oh My!</em> — practical security leadership.</p></div>
</div>
</div></section>
<section><div class="wrap">
<h2>Industries we serve</h2>
<p class="lead">Specialized support for organizations with real compliance and uptime stakes.</p>
<div class="pillrow">{''.join(f'<span>{escape(i)}</span>' for i in INDUSTRIES)}</div>
<p style="margin-top:18px"><a href="about-red-rabbit-security/industries-we-serve/index.html">Explore industry focus →</a></p>
</div></section>
<div class="ctastrip"><div class="wrap">
<h2>Ready to outsmart risk?</h2>
<p>{escape(TAGLINE)}</p>
<a class="btn" href="free-security-assessment/index.html">Free Security Assessment</a>
<a class="btn alt" href="contact/index.html">Contact Us</a>
</div></div>
"""
        + faq_block(faqs)
        + org_script()
        + chrome_bottom(0)
    )


def render_hub(hub: dict) -> str:
    depth = 1
    cards = "".join(
        f"""<div class="gcard"><h3><a href="{slug}/index.html">{escape(name)}</a></h3>
<p>{escape(blurb)}</p></div>"""
        for slug, name, _, blurb in hub["children"]
    )
    faqs = [
        (
            f"What are {hub['name']}?",
            hub["blurb"],
        ),
        (
            f"Who is {hub['name']} for?",
            "Small and medium businesses that need enterprise-grade capability with clear pricing and accountable delivery — whether you have an internal IT team or need a fully managed partner.",
        ),
        (
            "How do we get started?",
            "Begin with a free security assessment. We map priorities, recommend scope, and provide a written proposal before work begins.",
        ),
        (
            "Does Red Rabbit work nationwide?",
            "Yes. Headquartered in White Plains, NY, we support clients across the United States and throughout North America via remote and onsite engagements as needed.",
        ),
    ]
    return (
        head(
            f"{hub['name']} | Red Rabbit Security",
            f"{hub['name']} from Red Rabbit Security — {hub['blurb']}",
            page_url(hub["slug"]),
            depth,
        )
        + chrome_top(depth)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> › {escape(hub["name"])}</div>
<section style="padding-top:20px"><div class="wrap">
<h1 class="page-title">{escape(hub["name"])}</h1>
<p class="lead">{escape(hub["blurb"])}</p>
<p><a class="btn" href="../free-security-assessment/index.html">Free Security Assessment</a>
<a class="btn dark" href="../request-a-proposal/index.html" style="margin-left:8px">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap">
<h2>{escape(hub["short"])} services we provide</h2>
<div class="grid">{cards}</div>
</div></section>
<section><div class="wrap">
<h2>What a campaign can include</h2>
<ul class="checks">
<li>Scoped discovery tied to business risk — not a generic checklist</li>
<li>Implementation with change control and clear owners</li>
<li>Monitoring and reporting your leadership can understand</li>
<li>Compliance and insurance evidence when regulators or carriers ask</li>
<li>A single accountable partner across security and IT operations</li>
</ul>
</div></section>
"""
        + faq_block(faqs)
        + chrome_bottom(depth)
    )


def render_leaf(hub: dict, child: tuple[str, str, str, str]) -> str:
    slug, name, keyword, blurb = child
    depth = 2
    p = rel_prefix(depth)
    related = "".join(
        f'<div class="gcard"><h3><a href="../{s}/index.html">{escape(n)}</a></h3><p>{escape(b)}</p></div>'
        for s, n, _, b in hub["children"]
        if s != slug
    )
    faqs = [
        (f"What is {name}?", blurb),
        (
            f"How long until {name.lower()} shows results?",
            "Timelines depend on your environment and starting point. Your proposal includes an honest schedule, and monthly reporting tracks progress against it.",
        ),
        (
            f"What does {name.lower()} cost?",
            "Scope drives price. After the free assessment we provide a fixed written proposal — project or monthly subscription — so the number you approve is the number you pay.",
        ),
        (
            f"Why Red Rabbit for {name.lower()}?",
            f"We deliver {keyword} as part of a layered, managed program — not a one-off task — with White Plains accountability and nationwide reach.",
        ),
    ]
    return (
        head(
            f"{name} | Red Rabbit Security",
            f"{name} from Red Rabbit Security — {blurb}",
            page_url(f"{hub['slug']}/{slug}"),
            depth,
        )
        + chrome_top(depth)
        + f"""
<div class="wrap crumb"><a href="{p}index.html">Home</a> › <a href="../index.html">{escape(hub["name"])}</a> › {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap">
<h1 class="page-title">{escape(name)}</h1>
<p class="lead">{escape(blurb)} At Red Rabbit Security, {escape(keyword)} is delivered inside a managed program measured on risk reduction and uptime — not activity reports.</p>
<p><a class="btn" href="{p}free-security-assessment/index.html">Free Security Assessment</a>
<a class="btn dark" href="{p}request-a-proposal/index.html" style="margin-left:8px">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap">
<h2>How {escape(name)} helps your business</h2>
<ul class="checks">
<li>Reduce exposure from the threats that actually hit SMBs</li>
<li>Improve visibility for leadership and insurers</li>
<li>Standardize operations so support is repeatable</li>
<li>Pair expert execution with 24/7 monitoring where it matters</li>
<li>Keep documentation ready for audits and due diligence</li>
</ul>
</div></section>
<section><div class="wrap">
<h2>Engagement shaped to your environment</h2>
<p>No two businesses need {escape(keyword)} the same way. We scope around your stack, compliance obligations, and what downtime costs you — then put price and timeline in writing before work begins.</p>
</div></section>
<section class="tint"><div class="wrap">
<h2>{escape(name)}: DIY gaps versus a managed partner</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes</h3><ul>
<li>Tools purchased without owners or tuning</li>
<li>Alerts that nobody reviews until after an incident</li>
<li>Policies written once and never tested</li>
<li>Reporting that shows activity, not risk reduction</li>
</ul></div>
<div class="col good"><h3>With Red Rabbit</h3><ul>
<li>Layered controls operated as one system</li>
<li>Clear escalation and response paths</li>
<li>Evidence-friendly reporting for leadership</li>
<li>Subscription accountability with a named team</li>
</ul></div>
</div>
</div></section>
<div class="ctastrip"><div class="wrap">
<h2>See where you stand — free</h2>
<p>Curious what {escape(name.lower())} should look like for your business? Start with the free security assessment.</p>
<a class="btn" href="{p}free-security-assessment/index.html">Get the Free Assessment</a>
</div></div>
"""
        + faq_block(faqs)
        + f"""
<section><div class="wrap">
<h2>Related {escape(hub["short"])} services</h2>
<div class="grid">{related}</div>
</div></section>
"""
        + chrome_bottom(depth)
    )


def render_simple(
    path: str,
    title: str,
    h1: str,
    description: str,
    body: str,
    depth: int,
    include_form: str | None = None,
    include_org: bool = False,
) -> str:
    form = form_box(*include_form) if include_form else ""
    return (
        head(title, description, page_url(path), depth)
        + chrome_top(depth)
        + body.replace("{{FORM}}", form)
        + (org_script() if include_org else "")
        + chrome_bottom(depth)
    )


def build_assets() -> None:
    css_dir = OUT / "assets" / "css"
    js_dir = OUT / "assets" / "js"
    img_dir = OUT / "assets" / "images"
    css_dir.mkdir(parents=True, exist_ok=True)
    js_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)
    (css_dir / "site.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets" / "favicon.svg").write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Red Rabbit Security">
  <rect width="64" height="64" rx="14" fill="#141012"/>
  <path d="M20 38c2-14 8-22 12-22s10 8 12 22c-4 8-20 8-24 0z" fill="#c1121f"/>
  <circle cx="28" cy="34" r="2.2" fill="#fff"/><circle cx="36" cy="34" r="2.2" fill="#fff"/>
  <path d="M18 18c4 2 6 8 6 12M46 18c-4 2-6 8-6 12" stroke="#e8d5c4" stroke-width="3" fill="none" stroke-linecap="round"/>
</svg>
""",
        encoding="utf-8",
    )
    (img_dir / "og-default.svg").write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#1a1012"/><stop offset="55%" stop-color="#2a1518"/><stop offset="100%" stop-color="#141012"/>
  </linearGradient></defs>
  <rect width="1200" height="630" fill="url(#g)"/>
  <circle cx="980" cy="120" r="200" fill="#c1121f" fill-opacity=".28"/>
  <text x="80" y="290" font-family="Arial Black, sans-serif" font-size="84" fill="#fff">Red Rabbit</text>
  <text x="80" y="370" font-family="Georgia, serif" font-size="40" fill="#e8d5c4">Security — Outsmart. Outpace. Outlast.</text>
</svg>
""",
        encoding="utf-8",
    )
    (js_dir / "forms.js").write_text(
        """(function () {
  function buildBody(form) {
    var data = new FormData(form);
    var lines = [];
    data.forEach(function (value, key) { lines.push(key + ": " + value); });
    return lines.join("\\n");
  }
  document.querySelectorAll("form.lead-form").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;
      var subject = "Red Rabbit Security inquiry";
      if (form.id === "assessment-form") subject = "Free security assessment request";
      if (form.id === "proposal-form") subject = "Proposal request";
      if (form.id === "contact-form") subject = "Contact request";
      var mailto = "mailto:info@redrabbitsec.com?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(buildBody(form));
      var success = form.parentElement.querySelector(".form-success");
      if (success) { success.hidden = false; success.style.display = "block"; }
      window.location.href = mailto;
    });
  });
})();
""",
        encoding="utf-8",
    )
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n",
        encoding="utf-8",
    )


def main() -> None:
    # Clear prior seocow deployables from this branch root (keep zip archived optionally)
    for stale in ["index.html", "sitemap.xml", "robots.txt", "404.html", "assets", "about-seo-company",
                  "contact", "content-marketing-services", "ecommerce-seo-services", "free-website-audit",
                  "link-building-services", "local-seo-services", "ppc-management-services",
                  "request-a-proposal", "seo-consulting-services", "seo-web-design-services",
                  "small-business-seo-services", "social-media-marketing-services",
                  "technical-seo-services", "about-red-rabbit-security", "free-security-assessment",
                  "managed-cybersecurity-services", "managed-it-services", "ai-business-solutions",
                  "cloud-computing-services", "compliance-regulatory-services", "backup-disaster-recovery",
                  "network-infrastructure-services", "business-voip-services",
                  "software-application-development"]:
        p = OUT / stale
        if p.is_file():
            p.unlink()
        elif p.is_dir():
            shutil.rmtree(p)

    build_assets()
    urls = ["/"]

    write(OUT / "index.html", render_home())

    for hub in HUBS:
        write(OUT / hub["slug"] / "index.html", render_hub(hub))
        urls.append(f"/{hub['slug']}/")
        for child in hub["children"]:
            slug = child[0]
            write(OUT / hub["slug"] / slug / "index.html", render_leaf(hub, child))
            urls.append(f"/{hub['slug']}/{slug}/")

    # About pages
    write(
        OUT / "about-red-rabbit-security" / "index.html",
        render_simple(
            "about-red-rabbit-security",
            "About Red Rabbit Security | White Plains, NY",
            "About Red Rabbit Security",
            "Red Rabbit Security was founded in 2018 in White Plains, NY to deliver enterprise-class cybersecurity and managed IT to SMBs nationwide.",
            f"""
<div class="wrap crumb"><a href="../index.html">Home</a> › About</div>
<section style="padding-top:20px"><div class="wrap">
<h1 class="page-title">About Red Rabbit Security</h1>
<p class="lead">Established in {FOUNDED} and headquartered in {escape(ADDRESS)}, Red Rabbit Security delivers enterprise-class cybersecurity, managed IT, cloud, compliance, backup, VoIP, AI, and software services to small and medium-sized businesses.</p>
</div></section>
<section class="tint"><div class="wrap">
<h2>Who we are</h2>
<p>We started Red Rabbit Security because growing businesses need the same protection and reliability as larger enterprises — without the complexity or inflated pricing of traditional enterprise providers. Today we help organizations modernize technology, secure systems, improve resilience, and operate with confidence across the United States, Canada, and Mexico.</p>
<p>Our founder, Marc Weathers, is the author of <em>Phishing, Vishing, and Smishing, Oh My!</em> — a practical guide to social-engineering awareness that reflects how we teach and operate: clear, actionable, and grounded in real attacks.</p>
</div></section>
<section><div class="wrap">
<h2>What we believe</h2>
<ul class="checks">
<li>Security is layered — not a single product purchase</li>
<li>SMBs deserve enterprise-grade outcomes at accessible rates</li>
<li>Reporting should be plain English, not fear theater</li>
<li>Long-term partnerships beat short-term ticket chasing</li>
</ul>
<p style="margin-top:16px"><a href="why-choose-us/index.html">Why choose us →</a> · <a href="industries-we-serve/index.html">Industries →</a></p>
</div></section>
"""
            + faq_block(
                [
                    (
                        "When was Red Rabbit Security founded?",
                        f"Red Rabbit Security was established in {FOUNDED} and is headquartered in {ADDRESS}.",
                    ),
                    (
                        "Do you work outside New York?",
                        "Yes. We serve clients nationwide and across North America through remote delivery and onsite work when needed.",
                    ),
                    (
                        "Who leads Red Rabbit Security?",
                        "Marc Weathers founded Red Rabbit Security and is a published cybersecurity author focused on practical awareness and defense.",
                    ),
                ]
            ),
            1,
            include_org=True,
        ),
    )
    urls.append("/about-red-rabbit-security/")

    write(
        OUT / "about-red-rabbit-security" / "why-choose-us" / "index.html",
        render_simple(
            "about-red-rabbit-security/why-choose-us",
            "Why Choose Red Rabbit Security",
            "Why Choose Us",
            "Why businesses choose Red Rabbit Security for managed cybersecurity and IT: layered defense, SMB focus, and accountable delivery.",
            f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> › <a href="../index.html">About</a> › Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap">
<h1 class="page-title">Why choose Red Rabbit Security</h1>
<p class="lead">We are not another ticket mill. We are a strategic technology partner built to help SMBs outsmart risk, outpace disruption, and outlast the unexpected.</p>
</div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Layered by design</h3><p>Endpoints, identity, email, cloud, backups, and compliance operated together.</p></div>
<div class="card"><h3>SMB-first economics</h3><p>Enterprise-class controls through subscription models that fit growing businesses.</p></div>
<div class="card"><h3>Named humans</h3><p>People who know your environment — not a faceless queue that resets every call.</p></div>
<div class="card"><h3>Assessment-led sales</h3><p>Free assessment first; written scope and pricing before you commit.</p></div>
<div class="card"><h3>Nationwide reach</h3><p>White Plains HQ with delivery across the U.S. and North America.</p></div>
<div class="card"><h3>Author-informed training</h3><p>Awareness programs grounded in real phishing, vishing, and smishing patterns.</p></div>
</div></div></section>
""",
            2,
        ),
    )
    urls.append("/about-red-rabbit-security/why-choose-us/")

    industry_cards = "".join(
        f'<div class="gcard"><h3>{escape(i)}</h3><p>Security, compliance, and IT operations tuned to how {escape(i.lower())} organizations actually run.</p></div>'
        for i in INDUSTRIES
    )
    write(
        OUT / "about-red-rabbit-security" / "industries-we-serve" / "index.html",
        render_simple(
            "about-red-rabbit-security/industries-we-serve",
            "Industries We Serve | Red Rabbit Security",
            "Industries We Serve",
            "Red Rabbit Security supports healthcare, legal, finance, manufacturing, and more with compliance-aware cybersecurity and managed IT.",
            f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> › <a href="../index.html">About</a> › Industries</div>
<section style="padding-top:20px"><div class="wrap">
<h1 class="page-title">Industries we serve</h1>
<p class="lead">Specialized IT and cybersecurity solutions tailored to your industry’s compliance and operational requirements.</p>
<div class="grid" style="margin-top:22px">{industry_cards}</div>
</div></section>
""",
            2,
        ),
    )
    urls.append("/about-red-rabbit-security/industries-we-serve/")

    # CTA pages
    for path, title, h1, desc, heading, form_id, submit, urlsuffix in [
        (
            "contact",
            "Contact Red Rabbit Security",
            "Contact Us",
            "Contact Red Rabbit Security in White Plains, NY for managed cybersecurity and IT. Call (914) 281-5352 or send a message.",
            "Tell us what’s going on — security concern, IT friction, or compliance deadline. We respond promptly on business days.",
            "contact-form",
            "Send Message",
            "/contact/",
        ),
        (
            "free-security-assessment",
            "Free Security Assessment | Red Rabbit Security",
            "Free Security Assessment",
            "Request a free security assessment from Red Rabbit Security. See your risks, priorities, and a clear plan before you spend.",
            "The free assessment shows exposure, quick wins, and what a right-sized program looks like — no obligation.",
            "assessment-form",
            "Request Free Assessment",
            "/free-security-assessment/",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | Red Rabbit Security",
            "Request a Proposal",
            "Request a written Red Rabbit Security proposal with scope, timeline, and pricing for cybersecurity or managed IT.",
            "Share your goals and constraints. We’ll return a scoped proposal you can compare anywhere.",
            "proposal-form",
            "Request Proposal",
            "/request-a-proposal/",
        ),
    ]:
        write(
            OUT / path / "index.html",
            render_simple(
                path,
                title,
                h1,
                desc,
                f"""
<div class="wrap crumb"><a href="../index.html">Home</a> › {escape(h1)}</div>
<section style="padding-top:20px"><div class="wrap">
<h1 class="page-title">{escape(h1)}</h1>
<p class="lead">{escape(heading)}</p>
<div class="steps">
<div class="card"><h3>1. Share context</h3><p>A few sentences is enough — we’ll ask smart follow-ups.</p></div>
<div class="card"><h3>2. Get a clear answer</h3><p>Assessment findings, a proposal, or honest advice if we’re not the fit.</p></div>
<div class="card"><h3>3. Decide with numbers</h3><p>Scope and price in writing before you commit.</p></div>
</div>
{{{{FORM}}}}
</div></section>
<section class="tint"><div class="wrap">
<h2>Reach us directly</h2>
<p><strong>Red Rabbit Security</strong><br>Headquarters: {escape(ADDRESS)}<br>Phone: <a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><br>Email: <a href="mailto:{EMAIL}">{escape(EMAIL)}</a></p>
</div></section>
""",
                1,
                include_form=(form_id, submit),
                include_org=(path == "contact"),
            ),
        )
        urls.append(urlsuffix)

    # 404
    write(
        OUT / "404.html",
        head("Page Not Found | Red Rabbit Security", "Page not found.", page_url("/404"), 0)
        + chrome_top(0)
        + """
<section style="padding:72px 0"><div class="wrap">
<h1 class="page-title">This trail went cold</h1>
<p class="lead">That page isn’t in our burrow. Head home or request a free security assessment.</p>
<p><a class="btn" href="index.html">Back to Home</a>
<a class="btn dark" href="free-security-assessment/index.html" style="margin-left:8px">Free Assessment</a></p>
</div></section>
"""
        + chrome_bottom(0),
    )

    # sitemap
    body = "".join(f"<url><loc>{page_url(u if u != '/' else '/')}</loc></url>" for u in urls)
    # fix homepage loc
    body = "".join(
        f"<url><loc>{BASE}/</loc></url>"
        if u == "/"
        else f"<url><loc>{BASE}{u}</loc></url>"
        for u in urls
    )
    write(
        OUT / "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + body
        + "</urlset>\n",
    )

    # questionnaire
    write(
        OUT / "REDRABBIT-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — Red Rabbit Security (DEMO BUILD)

**Facts grounded from live redrabbitsec.com · generated for Website Factory demo**

| Field | Value |
|---|---|
| business_name | Red Rabbit Security |
| domain | redrabbitsec.com |
| phone | {PHONE} |
| email | {EMAIL} |
| hq | White Plains, NY |
| founded | {FOUNDED} |
| founder | Marc Weathers |
| tagline | {TAGLINE} |
| value_prop | Enterprise-grade cybersecurity, managed IT, AI, cloud, and compliance for SMBs |
| service_area | Nationwide US + North America |
| hubs | {len(HUBS)} |
| children | {sum(len(h['children']) for h in HUBS)} |
""",
    )

    pages = list(OUT.rglob("index.html"))
    print(f"Generated {len(pages)} pages + assets")
    print(f"Sitemap URLs: {len(urls)}")


if __name__ == "__main__":
    main()
