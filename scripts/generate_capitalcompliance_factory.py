#!/usr/bin/env python3
"""Generate Capital Compliance site using the NearMe OS Website Factory template.

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: industry / regulatory cybersecurity compliance (HIPAA, CMMC, NIST, etc.).
Positioning from owner brief (2026-07-22): “Rely on Capital Compliance, your one stop
shop for ALL your compliance needs.” NAP not confirmed for this vertical — marked [confirm].
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://capitalcompliance.co"  # [confirm domain for this vertical]
PHONE = ""  # [confirm]
PHONE_TEL = ""
EMAIL = "info@capitalcompliance.co"  # [confirm]
HQ = ""  # [confirm]
ADDRESS = ""  # [confirm]
TAGLINE = "Your one-stop shop for ALL your compliance needs."
STAGING_BANNER = (
    "STAGING PREVIEW — Capital Compliance industry compliance factory build "
    "· HIPAA · CMMC · NIST · content pending owner review"
)

# NearMe factory CSS — navy + teal (compliance / GRC; avoid purple & cream-terracotta)
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#0f172a;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#0f766e;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#0b1220;color:#99f6e4;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#0f172a;color:#ccfbf1;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #0d9488;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#0f172a}.logo span{color:#0d9488}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#0f172a}
.phone-cta small{display:block;color:#5a6b7b;font-size:11px}
nav.nav{background:#0f172a}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#020617;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #0d9488;z-index:60}
.dd a{color:#0f172a;padding:10px 15px;font-weight:500;border-bottom:1px solid #ccfbf1}
.dd a:hover{background:#f0fdfa}
.nav .em a{background:#0d9488}.nav .em a:hover{background:#0f766e}
.hero{background:linear-gradient(rgba(15,23,42,.9),rgba(15,23,42,.9)),repeating-linear-gradient(45deg,#0f172a 0 14px,#134e4a 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#99f6e4;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#0d9488;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#0f766e;text-decoration:none}
.btn.alt{background:#0f172a;color:#fff}.btn.alt:hover{background:#334155}
section{padding:44px 0}
section.tint{background:#f0fdfa}
section h2{font-size:25px;color:#0f172a;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#0d9488;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #d1e7e3;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(13,148,136,.06)}
.card h3{color:#0f172a;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #d1e7e3;border-left:4px solid #0d9488;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#0f172a}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#0f766e}
.ctastrip{background:#0f172a;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #d1e7e3;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#f8fafc}.vs .col.good{background:#f0fdfa}
.vs h3{font-size:16px;margin-bottom:12px;color:#0f172a}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#0f766e;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #d1e7e3;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#0f172a;list-style:none}
details summary:before{content:"+ ";color:#0d9488;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #d1e7e3;border-top:4px solid #0d9488;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#44525f;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5a6b7b;padding:14px 0 0}
.crumb a{color:#5a6b7b}
footer{background:#020617;color:#c9b8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #134e4a;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #d1e7e3;border-top:4px solid #0d9488;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#0f172a}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #d1e7e3;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(13,148,136,.08)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#0f172a}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#0d9488;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#0d9488;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#0f172a}
"""

# Gate 1 — 10 × 10 industry compliance (HIPAA, CMMC, NIST, multi-framework GRC)
HUBS = [
    {
        "slug": "hipaa-compliance",
        "name": "HIPAA Compliance",
        "short": "HIPAA",
        "blurb": "HIPAA privacy and security program support for covered entities and business associates handling ePHI.",
        "children": [
            ("hipaa-security-rule-readiness", "HIPAA Security Rule Readiness", "Map administrative, physical, and technical safeguards to your environment."),
            ("hipaa-privacy-rule-support", "HIPAA Privacy Rule Support", "Policies and workflows for PHI use, disclosure, and patient rights."),
            ("hipaa-risk-analysis", "HIPAA Risk Analysis", "Documented risk analysis that stands up to scrutiny."),
            ("hipaa-gap-assessments", "HIPAA Gap Assessments", "Find control and documentation gaps before an investigation or audit."),
            ("business-associate-agreements", "Business Associate Agreements", "BAA inventory, templates, and vendor follow-through."),
            ("hipaa-policies-and-procedures", "HIPAA Policies & Procedures", "Written P&Ps matched to how your organization actually operates."),
            ("hipaa-workforce-training", "HIPAA Workforce Training", "Role-aware training that people complete and remember."),
            ("breach-notification-readiness", "Breach Notification Readiness", "Playbooks for assessment, notification, and documentation timelines."),
            ("hipaa-audit-preparation", "HIPAA Audit Preparation", "Evidence packs and walkthroughs before OCR or customer audits."),
            ("ongoing-hipaa-program-support", "Ongoing HIPAA Program Support", "Retainers so HIPAA does not become a once-a-year scramble."),
        ],
    },
    {
        "slug": "cmmc-compliance",
        "name": "CMMC Compliance",
        "short": "CMMC",
        "blurb": "CMMC readiness for defense contractors — DFARS/NIST 800-171 alignment through assessment prep.",
        "children": [
            ("cmmc-level-1-readiness", "CMMC Level 1 Readiness", "Foundational practices for Level 1 self-assessment paths."),
            ("cmmc-level-2-readiness", "CMMC Level 2 Readiness", "Level 2 program build against NIST 800-171 requirements."),
            ("cmmc-scoping-and-boundaries", "CMMC Scoping & Boundaries", "Define CUI boundaries so you do not over- or under-scope."),
            ("dfars-7012-alignment", "DFARS 7012 Alignment", "Contract clause expectations mapped to your security program."),
            ("sprs-score-improvement", "SPRS Score Improvement", "Improve and document your SPRS posture with evidence."),
            ("cmmc-gap-assessments", "CMMC Gap Assessments", "Control-by-control gaps before you spend on the wrong fixes."),
            ("cui-handling-programs", "CUI Handling Programs", "Handling, marking, and storage practices for CUI."),
            ("cmmc-assessment-preparation", "CMMC Assessment Preparation", "Walkthroughs, evidence, and interview prep for assessors."),
            ("cmmc-for-supply-chain-partners", "CMMC for Supply Chain Partners", "Help subcontractors meet prime-flow-down expectations."),
            ("cmmc-program-retainers", "CMMC Program Retainers", "Ongoing support so readiness does not decay between assessments."),
        ],
    },
    {
        "slug": "nist-frameworks",
        "name": "NIST Frameworks",
        "short": "NIST",
        "blurb": "NIST-aligned programs — 800-171, CSF, and 800-53 control families mapped to your real systems.",
        "children": [
            ("nist-800-171-implementation", "NIST 800-171 Implementation", "Implement and evidence the 800-171 control families for CUI."),
            ("nist-csf-alignment", "NIST CSF Alignment", "Identify, Protect, Detect, Respond, Recover — tuned to your risk."),
            ("nist-800-53-control-mapping", "NIST 800-53 Control Mapping", "Map 800-53 families when contracts or customers require it."),
            ("nist-control-inheritance", "NIST Control Inheritance", "Reuse inherited controls from cloud and shared services cleanly."),
            ("nist-baseline-selection", "NIST Baseline Selection", "Pick a baseline that matches impact level — not vanity compliance."),
            ("nist-to-cmmc-crosswalks", "NIST to CMMC Crosswalks", "Show how NIST work feeds CMMC without duplicate projects."),
            ("nist-to-hipaa-crosswalks", "NIST to HIPAA Crosswalks", "Reuse technical work across healthcare and federal frameworks."),
            ("secure-configuration-baselines", "Secure Configuration Baselines", "Hardening baselines that auditors can actually verify."),
            ("nist-documentation-packages", "NIST Documentation Packages", "SSP-ready narratives and control descriptions."),
            ("nist-program-maintenance", "NIST Program Maintenance", "Keep mappings current as systems and frameworks change."),
        ],
    },
    {
        "slug": "gap-assessments-and-readiness",
        "name": "Gap Assessments & Readiness",
        "short": "Assessments",
        "blurb": "Structured gap assessments so you know what fails — and what to fix first — across frameworks.",
        "children": [
            ("multi-framework-gap-assessments", "Multi-Framework Gap Assessments", "One assessment pass across HIPAA, CMMC, NIST, and related regimes."),
            ("control-maturity-scoring", "Control Maturity Scoring", "Score maturity so leadership sees priority, not just pass/fail."),
            ("technical-control-validation", "Technical Control Validation", "Validate that controls work in the environment — not only on paper."),
            ("policy-vs-practice-reviews", "Policy vs Practice Reviews", "Catch where written policy does not match daily operations."),
            ("vendor-and-saas-gap-reviews", "Vendor & SaaS Gap Reviews", "Third-party tools that create silent compliance holes."),
            ("readiness-roadmaps", "Readiness Roadmaps", "Sequenced remediation with owners and dates."),
            ("executive-readiness-briefings", "Executive Readiness Briefings", "Plain-English risk and readiness for leadership."),
            ("pre-audit-dress-rehearsals", "Pre-Audit Dress Rehearsals", "Practice interviews and evidence pulls before the real day."),
            ("reassessment-after-remediation", "Reassessment After Remediation", "Confirm fixes closed the gap before you claim ready."),
            ("assessment-evidence-packages", "Assessment Evidence Packages", "Assessor-friendly packs organized by control."),
        ],
    },
    {
        "slug": "policies-ssp-and-documentation",
        "name": "Policies, SSP & Documentation",
        "short": "Documentation",
        "blurb": "Policies, System Security Plans, and documentation packages assessors and customers expect to see.",
        "children": [
            ("system-security-plan-development", "System Security Plan Development", "SSP content that describes the real system boundary and controls."),
            ("policy-suite-development", "Policy Suite Development", "Core security and privacy policies without copy-paste theater."),
            ("procedure-and-runbook-writing", "Procedure & Runbook Writing", "Step-level procedures operators can follow under pressure."),
            ("standards-and-baselines-docs", "Standards & Baselines Docs", "Configuration and hardening standards in writing."),
            ("roles-and-responsibilities-matrices", "Roles & Responsibilities Matrices", "Who owns each control — named, not implied."),
            ("data-flow-and-boundary-diagrams", "Data Flow & Boundary Diagrams", "Diagrams that make scope and data movement obvious."),
            ("policy-exception-management", "Policy Exception Management", "Documented exceptions with expiry and compensating controls."),
            ("document-control-and-versioning", "Document Control & Versioning", "Version hygiene so auditors see the current truth."),
            ("customer-questionnaire-response-support", "Customer Questionnaire Response Support", "Consistent answers to security questionnaires and RFPs."),
            ("documentation-refresh-retainers", "Documentation Refresh Retainers", "Keep docs current as people, tools, and scope change."),
        ],
    },
    {
        "slug": "poam-and-remediation",
        "name": "POA&M and Remediation",
        "short": "POA&M",
        "blurb": "Plans of Action & Milestones and remediation programs that close gaps with owners, dates, and evidence.",
        "children": [
            ("poam-development", "POA&M Development", "Build a living POA&M from assessment findings."),
            ("remediation-prioritization", "Remediation Prioritization", "Fix what reduces the most risk and assessment friction first."),
            ("technical-remediation-coordination", "Technical Remediation Coordination", "Coordinate IT/security workstreams against control IDs."),
            ("compensating-controls-design", "Compensating Controls Design", "Document compensating controls when perfect fixes take time."),
            ("milestone-tracking-and-reporting", "Milestone Tracking & Reporting", "Status reporting leadership and primes can trust."),
            ("evidence-of-closure", "Evidence of Closure", "Proof that closed items stay closed."),
            ("risk-acceptance-workflows", "Risk Acceptance Workflows", "Formal acceptance when residual risk is intentional."),
            ("finding-lifecycle-management", "Finding Lifecycle Management", "Open → fix → verify → close without spreadsheet chaos."),
            ("retest-and-validation-cycles", "Retest & Validation Cycles", "Validate remediation before the next assessment window."),
            ("poam-program-retainers", "POA&M Program Retainers", "Ongoing POA&M hygiene between formal assessments."),
        ],
    },
    {
        "slug": "evidence-and-audit-readiness",
        "name": "Evidence & Audit Readiness",
        "short": "Audit Ready",
        "blurb": "Evidence libraries and audit readiness so you are not scrambling the week before assessors arrive.",
        "children": [
            ("evidence-library-design", "Evidence Library Design", "One library mapped to multiple frameworks and control IDs."),
            ("continuous-evidence-collection", "Continuous Evidence Collection", "Collect proof year-round instead of once a year."),
            ("control-to-artifact-mapping", "Control-to-Artifact Mapping", "Every control points to the artifact that proves it."),
            ("audit-interview-coaching", "Audit Interview Coaching", "Prepare control owners for assessor questions."),
            ("sample-set-preparation", "Sample Set Preparation", "Clean samples for testing windows."),
            ("customer-and-regulator-audits", "Customer & Regulator Audits", "Support for customer security reviews and regulatory asks."),
            ("soc2-adjacent-evidence-reuse", "SOC 2-Adjacent Evidence Reuse", "Reuse technical evidence when SOC 2 enters the picture."),
            ("pci-adjacent-evidence-reuse", "PCI-Adjacent Evidence Reuse", "Reuse relevant controls when card data scope appears."),
            ("audit-war-room-support", "Audit War-Room Support", "Live support during assessment windows."),
            ("post-audit-response-support", "Post-Audit Response Support", "Respond to findings with clear remediation paths."),
        ],
    },
    {
        "slug": "risk-management-and-governance",
        "name": "Risk Management & Governance",
        "short": "Risk & GRC",
        "blurb": "Risk management and governance so compliance is owned — not rented from a binder on a shelf.",
        "children": [
            ("enterprise-risk-assessments", "Enterprise Risk Assessments", "Risk registers tied to business impact, not jargon."),
            ("governance-committee-support", "Governance Committee Support", "Cadence and reporting for security/compliance oversight."),
            ("vendor-risk-management", "Vendor Risk Management", "Third-party risk reviews, BAAs, and ongoing monitoring."),
            ("access-governance-reviews", "Access Governance Reviews", "Joiner/mover/leaver and privileged access hygiene."),
            ("incident-response-governance", "Incident Response Governance", "IR plans tested enough to be usable."),
            ("change-and-configuration-governance", "Change & Configuration Governance", "Change control that auditors can follow."),
            ("metrics-and-compliance-kpis", "Metrics & Compliance KPIs", "Simple KPIs that show program health."),
            ("board-and-executive-reporting", "Board & Executive Reporting", "Risk reporting without drowning leadership in control IDs."),
            ("policy-exception-governance", "Policy Exception Governance", "Exceptions tracked, expired, or converted to fixes."),
            ("grc-operating-model-design", "GRC Operating Model Design", "Who does what across IT, security, legal, and ops."),
        ],
    },
    {
        "slug": "security-controls-implementation",
        "name": "Security Controls Implementation",
        "short": "Controls",
        "blurb": "Hands-on control implementation guidance so frameworks become working safeguards — not slideware.",
        "children": [
            ("identity-and-access-controls", "Identity & Access Controls", "MFA, least privilege, and access reviews that satisfy multiple frameworks."),
            ("endpoint-and-malware-protections", "Endpoint & Malware Protections", "Endpoint controls mapped to HIPAA, CMMC, and NIST expectations."),
            ("logging-and-monitoring-controls", "Logging & Monitoring Controls", "Logging that produces usable evidence and detection."),
            ("encryption-and-data-protection", "Encryption & Data Protection", "Encryption in transit/at rest with key-handling clarity."),
            ("backup-and-recovery-controls", "Backup & Recovery Controls", "Backups tested enough to count as a control."),
            ("network-segmentation-for-scope", "Network Segmentation for Scope", "Segment CUI/ePHI environments to shrink assessment scope."),
            ("secure-remote-access", "Secure Remote Access", "Remote work patterns that do not break control intent."),
            ("vulnerability-management-programs", "Vulnerability Management Programs", "Scan → prioritize → patch → evidence cycles."),
            ("email-and-collaboration-hardening", "Email & Collaboration Hardening", "Hardening for the tools people actually use daily."),
            ("control-implementation-playbooks", "Control Implementation Playbooks", "Repeatable build guides tied to control IDs."),
        ],
    },
    {
        "slug": "multi-framework-compliance-programs",
        "name": "Multi-Framework Compliance Programs",
        "short": "One-Stop GRC",
        "blurb": "One program across HIPAA, CMMC, NIST, and related frameworks — map once, reuse evidence, stop paying twice.",
        "children": [
            ("unified-control-framework-mapping", "Unified Control Framework Mapping", "One control set mapped to HIPAA, CMMC, NIST, and more."),
            ("cross-framework-evidence-reuse", "Cross-Framework Evidence Reuse", "One artifact satisfying multiple control IDs."),
            ("program-build-for-regulated-industries", "Program Build for Regulated Industries", "Healthcare, defense, and professional services program patterns."),
            ("compliance-calendar-and-cadence", "Compliance Calendar & Cadence", "Assessments, training, reviews, and renewals on one calendar."),
            ("managed-compliance-retainers", "Managed Compliance Retainers", "Ongoing program ownership support — not a one-time binder."),
            ("framework-expansion-planning", "Framework Expansion Planning", "Add SOC 2, PCI, or privacy laws without restarting from zero."),
            ("msp-and-mssp-compliance-partnerships", "MSP & MSSP Compliance Partnerships", "Partner with existing IT/security providers without gaps."),
            ("compliance-for-growth-and-contracts", "Compliance for Growth & Contracts", "Get ready for the next RFP, prime, or payer requirement."),
            ("training-and-awareness-programs", "Training & Awareness Programs", "Workforce awareness that supports multiple frameworks."),
            ("one-stop-compliance-onboarding", "One-Stop Compliance Onboarding", "Start with discovery and leave with a sequenced program plan."),
        ],
    },
]

INDUSTRIES = [
    "Healthcare Providers & Covered Entities",
    "Business Associates & Health Tech",
    "Defense Contractors & Subcontractors",
    "Professional Services Firms",
    "SaaS & Cloud Vendors",
    "Manufacturing & Supply Chain",
    "Financial & Mortgage Services",
    "MSPs Supporting Regulated Clients",
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


def contact_bits() -> tuple[str, str, str]:
    """Return (utility_right, phone_cta_html, footer_visit_li)."""
    util = escape(EMAIL) if EMAIL else "Contact via form"
    if PHONE and PHONE_TEL:
        phone = (
            f'<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a>'
            f"<small>HIPAA · CMMC · NIST</small></div>"
        )
    else:
        phone = (
            '<div class="phone-cta"><a href="request-a-consultation/index.html">Request a consult</a>'
            "<small>HIPAA · CMMC · NIST · *[confirm phone]*</small></div>"
        )
    visit = (
        f"<li>{escape(ADDRESS)}</li><li>{escape(HQ)}</li>"
        if ADDRESS
        else "<li>Location *[confirm]*</li><li>Hours *[confirm]*</li>"
    )
    return util, phone, visit


def chrome(depth: int) -> str:
    p = pfx(depth)
    hub_dd = "".join(
        f'<a href="{p}{h["slug"]}/index.html">{escape(h["name"])}</a>' for h in HUBS
    )
    util, phone_html, _ = contact_bits()
    # phone_html uses relative consult link — fix depth
    if not PHONE:
        phone_html = (
            f'<div class="phone-cta"><a href="{p}request-a-consultation/index.html">Request a consult</a>'
            "<small>HIPAA · CMMC · NIST · *[confirm phone]*</small></div>"
        )
    return f"""<div class="utility"><div class="wrap"><span>{escape(TAGLINE)}</span><span>{util}</span></div></div>
<header class="main"><div class="wrap">
<div class="logo">Capital <span>Compliance</span><small>Industry Compliance</small></div>
{phone_html}
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-capital-compliance/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-capital-compliance/index.html">About Capital Compliance</a>
<a href="{p}about-capital-compliance/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-capital-compliance/who-we-serve/index.html">Who We Serve</a>
</div></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li><a href="{p}request-a-proposal/index.html">Get a Proposal</a></li>
<li class="em"><a href="{p}request-a-consultation/index.html">Get Started</a></li>
</ul></div></nav>
"""


def footer(depth: int) -> str:
    p = pfx(depth)
    hubs = "".join(
        f'<li><a href="{p}{h["slug"]}/index.html">{escape(h["short"])}</a></li>' for h in HUBS
    )
    _, _, visit = contact_bits()
    phone_li = (
        f'<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>'
        if PHONE and PHONE_TEL
        else "<li>Phone *[confirm]*</li>"
    )
    email_li = f'<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>' if EMAIL else ""
    return f"""<footer><div class="wrap"><div class="fcols">
<div><h4>Services</h4><ul>{hubs}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="{p}about-capital-compliance/index.html">About Capital Compliance</a></li>
<li><a href="{p}about-capital-compliance/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-capital-compliance/who-we-serve/index.html">Who We Serve</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}request-a-consultation/index.html">Request a Consultation</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
{phone_li}
{email_li}
</ul></div>
<div><h4>Visit</h4><ul>{visit}</ul></div>
</div>
<div class="copy">Capital Compliance &middot; Industry compliance · HIPAA · CMMC · NIST<br>
Copyright &copy; 2026. Capital Compliance. All rights reserved. Compliance support is not a certification guarantee.</div></div></footer>
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
    opts = "".join(f'<option>{escape(h["name"])}</option>' for h in HUBS)
    return f"""<div class="formbox">
<label>First Name</label><input type="text">
<label>Last Name</label><input type="text">
<label>Email</label><input type="text">
<label>Phone</label><input type="text">
<label>I am a…</label><select><option>Please choose&hellip;</option><option>Healthcare / Covered Entity / BA</option><option>Defense Contractor / Subcontractor</option><option>SaaS / Technology Vendor</option><option>MSP / MSSP</option><option>Other regulated business</option></select>
<label>Interest</label><select><option>Please choose&hellip;</option>{opts}<option>Multi-framework program</option><option>Gap assessment</option><option>Other</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f95a8">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Capital Compliance",
        "email": EMAIL or None,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "description": (
            "Capital Compliance — one-stop industry compliance for HIPAA, CMMC, NIST, "
            "and multi-framework GRC programs."
        ),
        "areaServed": "US",
        "knowsAbout": ["HIPAA", "CMMC", "NIST 800-171", "NIST CSF", "GRC"],
    }
    data = {k: v for k, v in data.items() if v is not None}
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
            f"<ul>{kids}</ul>"
            f'<a href="{h["slug"]}/index.html" style="font:600 13px \'Segoe UI\',sans-serif">All {escape(h["short"]).lower()} services &rarr;</a></div>'
        )
    return (
        head(
            "Capital Compliance | HIPAA, CMMC & NIST Compliance",
            "Rely on Capital Compliance — your one-stop shop for ALL your compliance needs. "
            "HIPAA, CMMC, NIST, gap assessments, SSP/POA&M, and multi-framework GRC.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>Rely on Capital Compliance</h1>
<p>{escape(TAGLINE)}</p>
<a class="btn" href="request-a-consultation/index.html">Get Started</a> <a class="btn alt" href="multi-framework-compliance-programs/index.html">See Frameworks</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>HIPAA</b><span>Healthcare</span></div>
<div class="stat"><b>CMMC</b><span>Defense</span></div>
<div class="stat"><b>NIST</b><span>800-171 · CSF</span></div>
<div class="stat"><b>1</b><span>Unified Program</span></div>
</div></div></section>
<section><div class="wrap"><h2>What can Capital Compliance handle for your compliance program?</h2>
<p class="lead">HIPAA, CMMC, NIST, assessments, documentation, POA&amp;M, evidence, risk governance, control implementation, and multi-framework programs — one accountable partner.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure which framework comes first? Start with a gap assessment.</h2>
<p style="margin-bottom:14px">Tell us whether you need HIPAA, CMMC, NIST, or a multi-framework program — we will sequence the work.</p>
<a class="btn" href="request-a-consultation/index.html">Request a Consultation</a></div></div>
<section><div class="wrap"><h2>How engagements get started</h2><div class="cols3">
<div class="card"><h3>1. Discovery</h3><p>Frameworks, contracts, systems, and who owns compliance today.</p></div>
<div class="card"><h3>2. Gap &amp; roadmap</h3><p>Control gaps, prioritized remediation, and an evidence plan.</p></div>
<div class="card"><h3>3. Build &amp; maintain</h3><p>Policies, controls, POA&amp;M, and ongoing readiness — not a binder that dies.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why Capital Compliance</h2><div class="cols3">
<div class="card"><h3>One-stop industry compliance</h3><p>HIPAA, CMMC, NIST, and related frameworks under one program model.</p></div>
<div class="card"><h3>Map once, reuse evidence</h3><p>Crosswalk controls so you stop paying for the same proof three times.</p></div>
<div class="card"><h3>Audit-ready operating cadence</h3><p>Assessments, documentation, POA&amp;M, and evidence that survive real assessors.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready to simplify compliance?</h2>
<a class="btn" href="request-a-consultation/index.html">Consultation</a> <a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    "What is Capital Compliance?",
                    "Capital Compliance is an industry compliance partner for HIPAA, CMMC, NIST, and multi-framework GRC — "
                    "assessments, documentation, remediation, evidence, and ongoing program support.",
                ),
                (
                    "Which frameworks do you cover?",
                    "Primary focus: HIPAA, CMMC, and NIST (including 800-171 and CSF). Multi-framework programs can expand toward adjacent regimes such as SOC 2 or PCI when needed.",
                ),
                (
                    "Do you certify organizations?",
                    "We help you build readiness and evidence. Formal certification or assessment outcomes depend on authorized assessors and your implemented controls — not on advisory work alone.",
                ),
                (
                    "How do I get started?",
                    "Request a consultation or proposal — share your industry, frameworks in scope, and any upcoming audit or contract deadline.",
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
        head(
            f"{h['name']} | Capital Compliance",
            f"{h['name']} from Capital Compliance — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} — From Capital Compliance</h2>
<p class="lead">{escape(h["blurb"])} Delivered as part of Capital Compliance’s one-stop industry compliance stack.</p>
<p><a class="btn" href="../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Solutions We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What Your Engagement Can Include</h2>
<ul class="checks">
<li>Discovery tied to contracts, systems, and frameworks in scope</li>
<li>Gap analysis with prioritized remediation</li>
<li>Policies, SSP, and evidence mapped to control IDs</li>
<li>POA&amp;M tracking with owners and closure proof</li>
<li>One accountable compliance partner across frameworks</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with a consultation. We map frameworks, deadlines, and recommend assessment vs program build first.",
                ),
                (
                    "Can this connect to other frameworks?",
                    "Yes — Capital Compliance is built for multi-framework programs so HIPAA, CMMC, and NIST work can share controls and evidence.",
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
        head(f"{name} | Capital Compliance", f"{name} from Capital Compliance — {blurb}")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Engage Capital Compliance for {escape(name.lower())} and related industry compliance services.</h2>
<p class="lead">{escape(blurb)} At Capital Compliance, {escape(name.lower())} sits inside a one-stop HIPAA · CMMC · NIST program — not an isolated binder project.</p>
<p><a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>How {escape(name)} from Capital Compliance Can Help You:</h2>
<ul class="checks">
<li>Clearer ownership of controls and evidence</li>
<li>Less duplicate work across frameworks</li>
<li>Documentation assessors and customers can follow</li>
<li>Remediation sequenced to risk and deadlines</li>
<li>Ongoing cadence so readiness does not decay</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} engagement scoped to your environment — not a one-size package</h2>
<p>No two organizations need {escape(name.lower())} the same way. We scope around your frameworks, system boundaries, contracts, and who owns compliance inside the company.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Teams avoid key risks by using a developed partner for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with DIY compliance</h3><ul>
<li>Policies that do not match practice</li>
<li>Evidence gathered the week before an audit</li>
<li>Separate projects for HIPAA, CMMC, and NIST</li>
<li>POA&amp;Ms with no owners or closure proof</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on Capital Compliance</h3><ul>
<li>Unified control mapping across frameworks</li>
<li>Living evidence libraries and documentation</li>
<li>Prioritized remediation with verification</li>
<li>One named compliance path instead of spreadsheet chaos</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>See where you stand — start with a consultation</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} would look like for your program? Start with a consultation.</p>
<a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} shows results?",
                    "Timelines depend on framework scope, current maturity, and upcoming assessment or contract deadlines — we map a realistic sequence after consultation.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Pricing is scoped after consultation based on frameworks, environment size, and whether you need assessment, build, or ongoing retainer support.",
                ),
                (
                    f"Why choose Capital Compliance for {name.lower()}?",
                    f"We deliver {name.lower()} as part of Capital Compliance’s one-stop industry compliance stack for HIPAA, CMMC, NIST, and related frameworks.",
                ),
            ]
        )
        + f'<section><div class="wrap"><h2>Related {escape(h["short"])} Solutions</h2><div class="grid">{related}</div></div></section>'
        + footer(2)
    )


def cta_page(slug: str, title: str, h2: str, lead: str) -> str:
    nap = (
        f"Phone: {escape(PHONE)}<br>" if PHONE else "Phone: *[confirm]*<br>"
    ) + (f"Email: {escape(EMAIL)}<br>" if EMAIL else "") + (
        f"Address: {escape(ADDRESS)}<br>" if ADDRESS else "Address: *[confirm]*<br>"
    )
    return (
        head(title, lead)
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h2)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:29px">{escape(h2)}</h2>
<h2 style="font-size:20px">Initiate a request with Capital Compliance</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us the frameworks</h3><p>HIPAA, CMMC, NIST, multi-framework, or a specific audit deadline.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>A scoped recommendation — assessment, build, or retainer.</p></div>
<div class="card"><h3>3. Decide with the full picture</h3><p>Advisory and program support help readiness; they do not guarantee certification outcomes.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>Capital Compliance</strong><br>{nap}Hours: *[confirm with owner]*</p>
<p style="font-size:13px;color:#5a6b7b">Compliance support builds readiness and evidence. Formal assessment or certification outcomes depend on implemented controls and authorized assessors.</p>
</div></section>
"""
        + (org_schema() if slug == "contact" else "")
        + footer(1)
    )


def write_inventory(_urls: list[str]) -> None:
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
        ["/", "HOME", "", "capital compliance hipaa cmmc nist", "logo/home", "A1,A6,A10", ""],
        [
            "/about-capital-compliance/",
            "COMP-HUB",
            "/",
            "about capital compliance",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-capital-compliance/why-choose-us/",
            "COMP-CHILD",
            "/about-capital-compliance/",
            "why choose capital compliance",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-capital-compliance/who-we-serve/",
            "COMP-CHILD",
            "/about-capital-compliance/",
            "who capital compliance serves",
            "About menu",
            "D1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact capital compliance",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "capital compliance proposal",
            "nav utility",
            "I1",
            "Request for Proposal",
        ],
        [
            "/request-a-consultation/",
            "FORM-CONSULT",
            "/",
            "request a consultation",
            "nav utility (highlighted)",
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
                    "Request for Proposal",
                ]
            )
    with (ROOT / "CAPITALCOMPLIANCE-PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
        "CAPITALCOMPLIANCE-QUESTIONNAIRE-ANSWERS.md",
        "CAPITALCOMPLIANCE-PAGE-INVENTORY.csv",
        "CAPITALCOMPLIANCE-NOTES.md",
    }
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
        ROOT / "about-capital-compliance" / "index.html",
        head(
            "About Capital Compliance",
            "Capital Compliance — one-stop industry compliance for HIPAA, CMMC, and NIST.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About Capital Compliance</h2>
<p class="lead">Rely on Capital Compliance — your one-stop shop for ALL your compliance needs. We help regulated organizations build and maintain programs across HIPAA, CMMC, NIST, and related frameworks.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>Industry compliance — not a generic IT shop. Gap assessments, documentation (SSP/policies), POA&amp;M remediation, evidence libraries, control implementation guidance, and multi-framework program retainers.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="who-we-serve/index.html">Who we serve &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "What does Capital Compliance do?",
                    "Industry compliance support for HIPAA, CMMC, NIST, and multi-framework GRC programs.",
                ),
                (
                    "How do I contact you?",
                    "Use the contact or consultation form. Phone, address, and hours pending owner confirmation.",
                ),
            ]
        )
        + org_schema()
        + footer(1),
    )
    urls.append("/about-capital-compliance/")

    write(
        ROOT / "about-capital-compliance" / "why-choose-us" / "index.html",
        head("Why Choose Capital Compliance", "Why organizations choose Capital Compliance.")
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose Capital Compliance</h2>
<p class="lead">One-stop industry compliance with cross-framework mapping for HIPAA, CMMC, and NIST.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>One-stop shop</h3><p>Assessments through remediation and evidence — not a scatter of vendors.</p></div>
<div class="card"><h3>HIPAA ready</h3><p>Privacy and security program support for covered entities and business associates.</p></div>
<div class="card"><h3>CMMC ready</h3><p>Defense contractor readiness aligned to DFARS / NIST 800-171 expectations.</p></div>
<div class="card"><h3>NIST aligned</h3><p>800-171, CSF, and control mapping that feeds multiple regimes.</p></div>
<div class="card"><h3>Evidence reuse</h3><p>Map controls once; stop rebuilding the same proof for every framework.</p></div>
<div class="card"><h3>Operating cadence</h3><p>Retainers and calendars so readiness survives after the project ends.</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-capital-compliance/why-choose-us/")

    ind = "".join(
        f'<div class="gcard"><h3>{escape(i)}</h3><p>Service emphasis tuned for {escape(i.lower())}.</p></div>'
        for i in INDUSTRIES
    )
    write(
        ROOT / "about-capital-compliance" / "who-we-serve" / "index.html",
        head("Who We Serve | Capital Compliance", "Who Capital Compliance serves.")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Who We Serve</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Who We Serve</h2>
<p class="lead">Engagements tailored to how different regulated organizations buy and operate compliance.</p>
<div class="grid">{ind}</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-capital-compliance/who-we-serve/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | Capital Compliance",
            "Contact Capital Compliance",
            "Questions about HIPAA, CMMC, NIST, gap assessments, SSP/POA&M, or multi-framework programs.",
        ),
        (
            "request-a-consultation",
            "Request a Consultation | Capital Compliance",
            "Request a Consultation",
            "Tell us which frameworks and deadlines you have — we will recommend a practical first step.",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | Capital Compliance",
            "Request a Proposal",
            "Share frameworks, environment size, and timeline. We will return a scoped proposal you can compare.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | Capital Compliance", "Page not found.")
        + chrome(0)
        + """
<section style="padding:72px 0"><div class="wrap"><h2 style="font-size:28px">Page not found</h2>
<p class="lead">That page isn't in this service map. Try home or request a consultation.</p>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn alt" href="request-a-consultation/index.html">Consultation</a></p>
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
    write(ROOT / "_redirects", "/*    /404.html  404\n")
    write_inventory(urls)

    hub_slugs = " · ".join(h["slug"] for h in HUBS)
    svc_children = sum(len(h["children"]) for h in HUBS)
    write(
        ROOT / "CAPITALCOMPLIANCE-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — Capital Compliance (FACTORY BUILD · Gate 1 10×10)

**NearMe OS Website Factory staging engine · category: industry / regulatory compliance (HIPAA, CMMC, NIST) · owner brief 2026-07-22 · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | Capital Compliance | owner brief |
| A2 domain | capitalcompliance.co | [confirm — may differ for this vertical] |
| A3 phone | *[confirm]* | not provided |
| A4 email | {EMAIL or "*[confirm]*"} | [confirm] |
| A5 address | *[confirm]* | not provided |
| A6 trade | Industry / regulatory cybersecurity compliance (HIPAA, CMMC, NIST, multi-framework GRC) | owner brief |
| A10 value_proposition | Rely on Capital Compliance — your one-stop shop for ALL your compliance needs | owner brief |
| A11 tagline | {TAGLINE} | owner brief |
| A12 hours | *[confirm]* | not provided |
| A13 services_core | HIPAA; CMMC; NIST (800-171/CSF); gap assessments; SSP/policies; POA&M; evidence/audit readiness; risk/GRC; control implementation; multi-framework programs | owner brief |

## B — Services: 10 × 10
{hub_slugs}
FORM-CONSULT=`request-a-consultation` · FORM-PRICING=`request-a-proposal`

## Notes
- Prior trucking-compliance draft was incorrect for this brand brief — rebuilt for industry compliance
- NAP pending owner confirmation
- Staging: noindex + STAGING PREVIEW
| hubs | {len(HUBS)} | children | {svc_children} |
""",
    )

    write(
        ROOT / "CAPITALCOMPLIANCE-NOTES.md",
        """# Capital Compliance — Factory Build

Category: **industry / regulatory cybersecurity compliance** (HIPAA, CMMC, NIST, multi-framework GRC).

- Positioning: “Rely on Capital Compliance, your one stop shop for ALL your compliance needs.”
- Generator: `scripts/generate_capitalcompliance_factory.py`
- Gate 1: 10 × 10 = 100 SVC-CHILD (+ chrome = 117 pages)
- FORM-CONSULT: `/request-a-consultation/`
- FORM-PRICING: `/request-a-proposal/`
- NAP: pending owner confirmation (phone/address/hours)
- Note: an earlier draft incorrectly used trucking compliance from capitalcompliance.co — corrected per owner
""",
    )

    factory_pages = list(ROOT.rglob("index.html"))
    print(f"Generated {len(factory_pages)} factory index pages")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)} · Children: {sum(len(h['children']) for h in HUBS)}")


if __name__ == "__main__":
    main()
