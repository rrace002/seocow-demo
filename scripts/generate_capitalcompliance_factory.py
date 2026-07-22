#!/usr/bin/env python3
"""Generate Capital Compliance site using the NearMe OS Website Factory template.

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: trucking / motor-carrier compliance services.
Facts grounded from live capitalcompliance.co (fetched 2026-07-22 via search index;
direct fetch returned 403 — NAP/services from indexed page content).
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://capitalcompliance.co"
PHONE = "(360) 566-5798"
PHONE_TEL = "+13605665798"
EMAIL = "safety@capitalcompliance.co"
HQ = "Vancouver, WA"
ADDRESS = "222 NE Park Plaza Dr, Vancouver, WA"
TAGLINE = "Your one-stop shop for ALL your compliance needs."
STAGING_BANNER = (
    "STAGING PREVIEW — capitalcompliance.co factory build · content pending owner review "
    "· not the live Capital Compliance website"
)

# NearMe factory CSS (SEO Cow template) with Capital Compliance navy + safety amber
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#0f172a;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#b45309;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#0b1220;color:#fde68a;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#0f172a;color:#fef3c7;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #d97706;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#0f172a}.logo span{color:#d97706}
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
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #d97706;z-index:60}
.dd a{color:#0f172a;padding:10px 15px;font-weight:500;border-bottom:1px solid #fef3c7}
.dd a:hover{background:#fffbeb}
.nav .em a{background:#d97706}.nav .em a:hover{background:#b45309}
.hero{background:linear-gradient(rgba(15,23,42,.9),rgba(15,23,42,.9)),repeating-linear-gradient(45deg,#0f172a 0 14px,#1e293b 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#fde68a;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#d97706;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#b45309;text-decoration:none}
.btn.alt{background:#0f172a;color:#fff}.btn.alt:hover{background:#334155}
section{padding:44px 0}
section.tint{background:#fffbeb}
section h2{font-size:25px;color:#0f172a;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#d97706;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #e7e5e4;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(217,119,6,.06)}
.card h3{color:#0f172a;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #e7e5e4;border-left:4px solid #d97706;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#0f172a}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#b45309}
.ctastrip{background:#0f172a;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #e7e5e4;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#fff7ed}.vs .col.good{background:#fffbeb}
.vs h3{font-size:16px;margin-bottom:12px;color:#0f172a}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#b45309;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #e7e5e4;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#0f172a;list-style:none}
details summary:before{content:"+ ";color:#d97706;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #e7e5e4;border-top:4px solid #d97706;border-radius:6px;padding:28px;max-width:640px}
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
.copy{border-top:1px solid #334155;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #e7e5e4;border-top:4px solid #d97706;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#0f172a}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #e7e5e4;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(217,119,6,.08)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#0f172a}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#d97706;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#d97706;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#0f172a}
"""

# Gate 1 — 10 × 10 grounded in live Capital Compliance trucking services
HUBS = [
    {
        "slug": "business-formation-and-ein",
        "name": "Business Formation & EIN",
        "short": "Formation",
        "blurb": "LLC and EIN setup so your trucking company has a clean legal foundation before authority filings.",
        "children": [
            ("llc-formation-for-carriers", "LLC Formation for Carriers", "Form the entity structure carriers commonly use before authority work."),
            ("ein-application-support", "EIN Application Support", "Secure your Employer Identification Number for banking, tax, and filings."),
            ("operating-name-and-dba-setup", "Operating Name & DBA Setup", "Align legal and trade names before MC/DOT applications."),
            ("owner-operator-entity-options", "Owner-Operator Entity Options", "Choose a structure matched to solo vs small-fleet operations."),
            ("bank-ready-business-paperwork", "Bank-Ready Business Paperwork", "Docs lenders and insurers typically expect at kickoff."),
            ("multi-owner-carrier-setup", "Multi-Owner Carrier Setup", "Clarify ownership before authority and insurance conversations."),
            ("state-registration-basics", "State Registration Basics", "State-level business registration steps that unblock federal filings."),
            ("address-and-mailing-setup", "Address & Mailing Setup", "Physical and mailing addresses that satisfy filing requirements."),
            ("formation-checklist-handoff", "Formation Checklist Handoff", "A clear checklist so nothing is missing before MC/DOT work."),
            ("formation-to-authority-handoff", "Formation-to-Authority Handoff", "Move cleanly from entity setup into MC/DOT applications."),
        ],
    },
    {
        "slug": "mc-dot-authority",
        "name": "MC / DOT Authority",
        "short": "MC/DOT",
        "blurb": "Motor Carrier (MC) and Department of Transportation (DOT) permits for legal interstate commercial operation.",
        "children": [
            ("new-dot-number-setup", "New DOT Number Setup", "Obtain a USDOT number for commercial vehicle operations."),
            ("mc-authority-applications", "MC Authority Applications", "File for operating authority when interstate for-hire work requires it."),
            ("interstate-authority-guidance", "Interstate Authority Guidance", "Clarify when interstate authority is required for your lanes."),
            ("authority-application-prep", "Authority Application Prep", "Gather the answers and documents filings actually ask for."),
            ("carrier-type-selection", "Carrier Type Selection", "Match application type to how you haul and get paid."),
            ("insurance-filing-coordination", "Insurance Filing Coordination", "Align coverage filings with authority timelines."),
            ("authority-status-tracking", "Authority Status Tracking", "Watch application status so surprises do not strand trucks."),
            ("reactivation-after-inactive-status", "Reactivation After Inactive Status", "Path back when DOT status has gone inactive."),
            ("authority-revocation-response", "Authority Revocation Response", "Structured next steps when authority is at risk or revoked."),
            ("mc-dot-compliance-handoff", "MC/DOT Compliance Handoff", "Hand off into monitoring and ongoing compliance after grant."),
        ],
    },
    {
        "slug": "boc-3-and-process-agents",
        "name": "BOC-3 & Process Agents",
        "short": "BOC-3",
        "blurb": "BOC-3 process-agent filings so legal documents can be served in each required state.",
        "children": [
            ("boc-3-filing-support", "BOC-3 Filing Support", "Complete BOC-3 designation so authority stays compliant."),
            ("process-agent-coverage-map", "Process Agent Coverage Map", "Understand where process agents are designated for your company."),
            ("multi-state-process-agent-setup", "Multi-State Process Agent Setup", "Coverage designed for interstate carriers, not one-state thinking."),
            ("boc-3-updates-after-moves", "BOC-3 Updates After Moves", "Refresh designations when addresses or structure change."),
            ("new-authority-boc-3-timing", "New Authority BOC-3 Timing", "Sequence BOC-3 with MC/DOT so filings do not stall."),
            ("process-agent-vendor-coordination", "Process Agent Vendor Coordination", "Work with agent networks without losing ownership of the filing."),
            ("boc-3-status-verification", "BOC-3 Status Verification", "Confirm the filing is active before you rely on it."),
            ("legal-service-readiness", "Legal Service Readiness", "Keep process-agent coverage ready for real legal traffic."),
            ("boc-3-for-fleet-growth", "BOC-3 for Fleet Growth", "Revisit coverage as lanes and operating footprint expand."),
            ("boc-3-recordkeeping", "BOC-3 Recordkeeping", "Keep a clean trail of designations and updates."),
        ],
    },
    {
        "slug": "ucr-compliance",
        "name": "UCR Compliance",
        "short": "UCR",
        "blurb": "Unified Carrier Registration support so interstate carriers maintain required UCR compliance.",
        "children": [
            ("annual-ucr-registration", "Annual UCR Registration", "Complete yearly UCR registration on time."),
            ("ucr-fleet-size-reporting", "UCR Fleet-Size Reporting", "Report fleet size accurately so fees and records match reality."),
            ("ucr-fee-guidance", "UCR Fee Guidance", "Understand fee brackets tied to fleet size."),
            ("ucr-for-new-carriers", "UCR for New Carriers", "First-year UCR steps after authority is granted."),
            ("ucr-renewal-reminders", "UCR Renewal Reminders", "Stay ahead of renewal windows instead of scrambling."),
            ("ucr-after-fleet-changes", "UCR After Fleet Changes", "Update when power-unit counts change mid-cycle."),
            ("ucr-compliance-verification", "UCR Compliance Verification", "Confirm registration status before roadside or audit surprises."),
            ("ucr-and-interstate-ops", "UCR and Interstate Ops", "How UCR fits the broader interstate credential stack."),
            ("ucr-record-retention", "UCR Record Retention", "Keep proof of registration where ops can find it."),
            ("ucr-plan-onboarding", "UCR Plan Onboarding", "Fold UCR into a monthly compliance plan."),
        ],
    },
    {
        "slug": "irp-registration",
        "name": "IRP Registration",
        "short": "IRP",
        "blurb": "International Registration Plan support for proportional registration across jurisdictions.",
        "children": [
            ("irp-account-setup", "IRP Account Setup", "Open and organize IRP registration for interstate fleets."),
            ("proportional-registration-basics", "Proportional Registration Basics", "How distance-based apportionment works in plain English."),
            ("irp-mileage-reporting", "IRP Mileage Reporting", "Capture jurisdiction miles cleanly for renewals."),
            ("irp-plate-and-cab-card-support", "IRP Plate & Cab Card Support", "Credentials your drivers need in the truck."),
            ("irp-renewals", "IRP Renewals", "Renewal prep so plates and cab cards do not lapse."),
            ("irp-fleet-additions", "IRP Fleet Additions", "Add units without breaking the account calendar."),
            ("irp-fleet-deletions", "IRP Fleet Deletions", "Remove units and keep records consistent."),
            ("irp-for-owner-operators", "IRP for Owner-Operators", "IRP paths sized for solo and small fleets."),
            ("irp-audit-readiness", "IRP Audit Readiness", "Mileage and record hygiene that survives questions."),
            ("irp-and-ucr-coordination", "IRP and UCR Coordination", "Keep IRP and UCR calendars from colliding."),
        ],
    },
    {
        "slug": "dot-monitoring-and-alerts",
        "name": "DOT Monitoring & Alerts",
        "short": "Monitoring",
        "blurb": "Proactive monitoring for DOT out-of-service orders, inactive DOT status, and authority revocations.",
        "children": [
            ("daily-dot-status-monitoring", "Daily DOT Status Monitoring", "Watch DOT status so inactive flags are not discovered roadside."),
            ("out-of-service-order-alerts", "Out-of-Service Order Alerts", "Daily alerts when OOS orders appear on your record."),
            ("inactive-dot-status-alerts", "Inactive DOT Status Alerts", "Catch inactive DOT status before it stops revenue."),
            ("authority-revocation-alerts", "Authority Revocation Alerts", "Early notice when authority revocation risk shows up."),
            ("safety-score-watch", "Safety Score Watch", "Track safety indicators that tend to precede enforcement pain."),
            ("monitoring-for-small-fleets", "Monitoring for Small Fleets", "Alert coverage sized for owner-operators and small fleets."),
            ("monitoring-for-growing-fleets", "Monitoring for Growing Fleets", "Scale monitoring as units and drivers multiply."),
            ("alert-escalation-playbooks", "Alert Escalation Playbooks", "Who gets called and what happens when an alert fires."),
            ("compliance-issue-triage", "Compliance Issue Triage", "Sort noise from issues that need same-day action."),
            ("monitoring-plan-onboarding", "Monitoring Plan Onboarding", "Plug monitoring into your monthly compliance plan."),
        ],
    },
    {
        "slug": "monthly-compliance-plans",
        "name": "Monthly Compliance Plans",
        "short": "Monthly Plans",
        "blurb": "Tailored monthly plans that keep small fleets and larger operations compliant without DIY chaos.",
        "children": [
            ("owner-operator-monthly-plans", "Owner-Operator Monthly Plans", "Ongoing support sized for single-truck operators."),
            ("small-fleet-monthly-plans", "Small Fleet Monthly Plans", "Plans for fleets that outgrew DIY spreadsheets."),
            ("large-fleet-monthly-plans", "Large Fleet Monthly Plans", "Support patterns for larger-scale operations."),
            ("customized-compliance-retainers", "Customized Compliance Retainers", "Monthly scope matched to your authority and lanes."),
            ("compliance-calendar-management", "Compliance Calendar Management", "Renewals and filings on one shared calendar."),
            ("document-vault-organization", "Document Vault Organization", "Keep filings, insurance, and credentials findable."),
            ("monthly-status-reviews", "Monthly Status Reviews", "Regular check-ins so issues do not compound."),
            ("roadside-readiness-checks", "Roadside Readiness Checks", "Cab credentials and paperwork ready for inspection."),
            ("plan-upgrades-as-you-grow", "Plan Upgrades as You Grow", "Adjust plan scope when fleet size changes."),
            ("onboarding-to-monthly-support", "Onboarding to Monthly Support", "Start a plan without losing track of open filings."),
        ],
    },
    {
        "slug": "safety-and-fmcsa-readiness",
        "name": "Safety & FMCSA Readiness",
        "short": "Safety",
        "blurb": "Safety and FMCSA readiness so your operation can withstand scrutiny — not just file paperwork once.",
        "children": [
            ("fmcsa-portal-hygiene", "FMCSA Portal Hygiene", "Keep portal access and company data accurate."),
            ("driver-qualification-file-basics", "Driver Qualification File Basics", "DQ file habits that reduce roadside and audit risk."),
            ("hours-of-service-awareness", "Hours of Service Awareness", "HOS basics that keep drivers and dispatch aligned."),
            ("vehicle-maintenance-record-basics", "Vehicle Maintenance Record Basics", "Maintenance records that support safety conversations."),
            ("drug-and-alcohol-program-basics", "Drug & Alcohol Program Basics", "Program foundations carriers are expected to maintain."),
            ("accident-register-hygiene", "Accident Register Hygiene", "Keep incident records organized and current."),
            ("new-entrant-safety-prep", "New Entrant Safety Prep", "Prep themes for carriers early in their authority life."),
            ("audit-response-support", "Audit Response Support", "Structured help when FMCSA asks hard questions."),
            ("corrective-action-plans", "Corrective Action Plans", "Documented fixes after findings — not verbal promises."),
            ("safety-culture-for-small-fleets", "Safety Culture for Small Fleets", "Practical habits when you do not have a full safety department."),
        ],
    },
    {
        "slug": "interstate-permits-and-credentials",
        "name": "Interstate Permits & Credentials",
        "short": "Permits",
        "blurb": "Interstate permits and credentials that keep trucks legal across state lines alongside UCR and IRP.",
        "children": [
            ("interstate-credential-stack", "Interstate Credential Stack", "See how MC/DOT, UCR, IRP, and BOC-3 fit together."),
            ("cab-card-and-plate-readiness", "Cab Card & Plate Readiness", "Credentials drivers must have in the truck."),
            ("insurance-certificate-tracking", "Insurance Certificate Tracking", "Keep proof of coverage current and findable."),
            ("state-permit-coordination", "State Permit Coordination", "Coordinate state-level credentials with federal filings."),
            ("oversize-overweight-awareness", "Oversize/Overweight Awareness", "When specialized permits enter the picture."),
            ("hazmat-credential-awareness", "Hazmat Credential Awareness", "Awareness for carriers whose freight triggers extra rules."),
            ("credential-expiration-tracking", "Credential Expiration Tracking", "Stop surprise expirations from grounding trucks."),
            ("multi-jurisdiction-ops-checklist", "Multi-Jurisdiction Ops Checklist", "A checklist for fleets that cross many states."),
            ("new-lane-credential-review", "New Lane Credential Review", "Review credentials before entering new lanes."),
            ("permits-plan-integration", "Permits Plan Integration", "Fold permits into monthly compliance support."),
        ],
    },
    {
        "slug": "fleet-compliance-operations",
        "name": "Fleet Compliance Operations",
        "short": "Fleet Ops",
        "blurb": "Day-to-day compliance operations that keep dispatch, drivers, and paperwork moving together.",
        "children": [
            ("compliance-ops-playbooks", "Compliance Ops Playbooks", "Written steps for common compliance tasks."),
            ("dispatch-compliance-handoffs", "Dispatch Compliance Handoffs", "Keep dispatch from sending trucks with missing credentials."),
            ("driver-onboarding-compliance", "Driver Onboarding Compliance", "Compliance steps when a new driver joins."),
            ("unit-onboarding-compliance", "Unit Onboarding Compliance", "Bring a new truck online without missing filings."),
            ("offboarding-drivers-and-units", "Offboarding Drivers & Units", "Close loops when people or trucks leave."),
            ("vendor-and-broker-paperwork", "Vendor & Broker Paperwork", "Packets brokers and shippers ask for repeatedly."),
            ("compliance-kpi-tracking", "Compliance KPI Tracking", "Simple metrics so leadership sees risk early."),
            ("owner-operator-ops-support", "Owner-Operator Ops Support", "Ops help when the owner is also the safety department."),
            ("growth-ready-compliance-systems", "Growth-Ready Compliance Systems", "Systems that survive adding the next five trucks."),
            ("road-to-success-planning", "Road to Success Planning", "Customized compliance planning — live site contact theme."),
        ],
    },
]

INDUSTRIES = [
    "Owner-Operators",
    "Small Fleets (2–10 trucks)",
    "Growing Regional Carriers",
    "Large-Scale Fleet Operations",
    "New Authority Startups",
    "Interstate For-Hire Carriers",
    "Private Fleets Expanding Lanes",
    "Carriers Returning from Inactive Status",
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
<div class="logo">Capital <span>Compliance</span><small>Trucking Compliance</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Road to Success · Monthly plans available</small></div>
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
<li><a href="{p}request-a-proposal/index.html">Get a Plan</a></li>
<li class="em"><a href="{p}request-a-consultation/index.html">Get Started</a></li>
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
<li><a href="{p}about-capital-compliance/index.html">About Capital Compliance</a></li>
<li><a href="{p}about-capital-compliance/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-capital-compliance/who-we-serve/index.html">Who We Serve</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}request-a-consultation/index.html">Request a Consultation</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul><li>{escape(ADDRESS)}</li><li>{escape(HQ)}</li><li>Hours on contact page *[confirm]*</li></ul></div>
</div>
<div class="copy">Capital Compliance &middot; {escape(HQ)} &middot; {escape(PHONE)}<br>
Copyright &copy; 2026. Capital Compliance. All rights reserved. Compliance support is not a guarantee of FMCSA outcomes.</div></div></footer>
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
<label>I am a…</label><select><option>Please choose&hellip;</option><option>Owner-Operator</option><option>Small Fleet</option><option>Growing / Large Fleet</option><option>Starting a New Authority</option></select>
<label>Interest</label><select><option>Please choose&hellip;</option>{opts}<option>Monthly Compliance Plan</option><option>New Authority Setup</option><option>Other</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f95a8">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Capital Compliance",
        "email": EMAIL,
        "telephone": PHONE_TEL,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "description": (
            "Capital Compliance — one-stop trucking compliance support including LLC/EIN setup, "
            "MC/DOT authority, BOC-3, UCR, IRP, DOT monitoring, and monthly compliance plans."
        ),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "222 NE Park Plaza Dr",
            "addressLocality": "Vancouver",
            "addressRegion": "WA",
            "addressCountry": "US",
        },
        "areaServed": "US",
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
            f"<ul>{kids}</ul>"
            f'<a href="{h["slug"]}/index.html" style="font:600 13px \'Segoe UI\',sans-serif">All {escape(h["short"]).lower()} services &rarr;</a></div>'
        )
    return (
        head(
            "Capital Compliance | One-Stop Trucking Compliance",
            "Rely on Capital Compliance — your one-stop shop for ALL your compliance needs. "
            "LLC/EIN, MC/DOT, BOC-3, UCR, IRP, DOT monitoring, and monthly plans.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>Rely on Capital Compliance</h1>
<p>{escape(TAGLINE)}</p>
<a class="btn" href="request-a-consultation/index.html">Get Started</a> <a class="btn alt" href="monthly-compliance-plans/index.html">See Monthly Plans</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>WA</b><span>Vancouver Based</span></div>
<div class="stat"><b>DOT</b><span>Monitoring Alerts</span></div>
<div class="stat"><b>MC</b><span>Authority Support</span></div>
<div class="stat"><b>24/7</b><span>Compliance Pressure</span></div>
</div></div></section>
<section><div class="wrap"><h2>What can Capital Compliance handle for your trucking business?</h2>
<p class="lead">From LLC and EIN setup through MC/DOT, BOC-3, UCR, IRP, monitoring, and monthly plans — one accountable compliance partner.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure where you stand? Start with a customized compliance plan.</h2>
<p style="margin-bottom:14px">Tell us whether you are launching authority, fixing inactive status, or need monthly monitoring.</p>
<a class="btn" href="request-a-consultation/index.html">Request a Consultation</a></div></div>
<section><div class="wrap"><h2>How engagements get started</h2><div class="cols3">
<div class="card"><h3>1. Tell us your operation</h3><p>Owner-operator, small fleet, or growing carrier — and what is due now.</p></div>
<div class="card"><h3>2. Get a clear plan</h3><p>Setup filings, monitoring, or a monthly retainer scoped to your authority.</p></div>
<div class="card"><h3>3. Stay road-ready</h3><p>Alerts and calendar support so compliance does not interrupt revenue.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why Capital Compliance</h2><div class="cols3">
<div class="card"><h3>One-stop compliance</h3><p>Formation, authority, BOC-3, UCR, IRP, and monitoring under one roof.</p></div>
<div class="card"><h3>Proactive monitoring</h3><p>Daily alerts for out-of-service orders, inactive DOT status, and authority revocations.</p></div>
<div class="card"><h3>Plans for every fleet size</h3><p>Tailored monthly plans for small fleets and large-scale operations.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready for your Road to Success?</h2>
<a class="btn" href="request-a-consultation/index.html">Consultation</a> <a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    "What is Capital Compliance?",
                    "Capital Compliance supports trucking businesses with compliance services — including LLC/EIN setup, "
                    "MC/DOT authority, BOC-3, UCR, IRP, DOT monitoring, and monthly compliance plans.",
                ),
                (
                    "Where is Capital Compliance located?",
                    f"Published contact details list {ADDRESS}. Phone {PHONE}. Email {EMAIL}.",
                ),
                (
                    "Do you offer monthly plans?",
                    "Yes. Live site messaging emphasizes tailored monthly plans for small fleets and large-scale operations.",
                ),
                (
                    "How do I get started?",
                    "Request a consultation or proposal — share whether you need new authority setup, monitoring, or an ongoing plan.",
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
<p class="lead">{escape(h["blurb"])} Delivered as part of Capital Compliance’s one-stop trucking compliance stack.</p>
<p><a class="btn" href="../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Solutions We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What Your Engagement Can Include</h2>
<ul class="checks">
<li>Discovery tied to your fleet size and authority status</li>
<li>Filing and credential sequencing that avoids stalls</li>
<li>Monitoring and alerts for issues that stop trucks</li>
<li>Documentation your team can find under pressure</li>
<li>One accountable compliance partner — not five vendors</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with a consultation. We map your authority status and recommend setup, monitoring, or a monthly plan.",
                ),
                (
                    "Where is Capital Compliance based?",
                    f"{HQ} — {ADDRESS}. Call {PHONE} or email {EMAIL}.",
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
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Engage Capital Compliance for {escape(name.lower())} and related trucking compliance services.</h2>
<p class="lead">{escape(blurb)} At Capital Compliance, {escape(name.lower())} is delivered inside a one-stop compliance stack — filings, monitoring, and monthly support.</p>
<p><a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>How {escape(name)} from Capital Compliance Can Help You:</h2>
<ul class="checks">
<li>Clearer ownership of filings and renewals</li>
<li>Fewer roadside surprises from expired or inactive credentials</li>
<li>Documented steps your team can follow</li>
<li>Coordination across MC/DOT, BOC-3, UCR, and IRP</li>
<li>Monitoring after setup so work does not die at filing</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} engagement scoped to your fleet — not a one-size package</h2>
<p>No two carriers need {escape(name.lower())} the same way. We scope around your authority status, fleet size, lanes, and who owns compliance inside the company.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Carriers avoid key risks by using a developed partner for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with DIY compliance</h3><ul>
<li>Inactive DOT status discovered too late</li>
<li>Missing BOC-3 or expired credentials</li>
<li>UCR/IRP calendars managed in someone’s head</li>
<li>No alerts when authority risk appears</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on Capital Compliance</h3><ul>
<li>Sequenced filings with clear next steps</li>
<li>Daily monitoring for OOS, inactive DOT, and revocations</li>
<li>Monthly plans matched to fleet size</li>
<li>One named compliance path instead of forum DIY</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>See where you stand — start with a plan conversation</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} would look like for your fleet? Start with a consultation.</p>
<a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} shows results?",
                    "Timelines depend on authority status, insurance filings, and agency processing — we map a realistic sequence after consultation.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Pricing is scoped after consultation — monthly plans vary by fleet size and scope. The live site does not publish a public rate card.",
                ),
                (
                    f"Why choose Capital Compliance for {name.lower()}?",
                    f"We deliver {name.lower()} as part of Capital Compliance’s one-stop trucking compliance services from {HQ}.",
                ),
            ]
        )
        + f'<section><div class="wrap"><h2>Related {escape(h["short"])} Solutions</h2><div class="grid">{related}</div></div></section>'
        + footer(2)
    )


def cta_page(slug: str, title: str, h2: str, lead: str) -> str:
    return (
        head(title, lead)
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h2)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:29px">{escape(h2)}</h2>
<h2 style="font-size:20px">Initiate a request with Capital Compliance</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us the operation</h3><p>New authority, monitoring, monthly plan, or a specific filing.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>A scoped recommendation — or an honest no.</p></div>
<div class="card"><h3>3. Decide with the full picture</h3><p>Compliance support helps you operate legally; it is not a guarantee of FMCSA outcomes.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>Capital Compliance</strong><br>Address: {escape(ADDRESS)}<br>Phone: {escape(PHONE)}<br>Email: {escape(EMAIL)}<br>Hours: *[confirm with owner]*</p>
<p style="font-size:13px;color:#5a6b7b">Compliance filings and monitoring support carriers; they do not guarantee inspection outcomes or authority approval timelines.</p>
</div></section>
"""
        + (org_schema() if slug == "contact" else "")
        + footer(1)
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
        ["/", "HOME", "", "capital compliance trucking", "logo/home", "A1,A6,A10", ""],
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
            "Capital Compliance — one-stop trucking compliance from Vancouver, WA.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About Capital Compliance</h2>
<p class="lead">Rely on Capital Compliance — your one-stop shop for ALL your compliance needs. We help trucking businesses run smoothly with tailored monthly plans and proactive monitoring.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>Live site mission: keep trucking businesses compliant and efficient — from LLC/EIN and MC/DOT setup through BOC-3, UCR, IRP, and daily DOT alerts.</p>
<p>Based in {escape(HQ)} at {escape(ADDRESS)}. Contact {escape(PHONE)} or {escape(EMAIL)}.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="who-we-serve/index.html">Who we serve &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "What does Capital Compliance do?",
                    "Trucking compliance support: business formation, MC/DOT authority, BOC-3, UCR, IRP, DOT monitoring, and monthly plans.",
                ),
                (
                    "How do I contact you?",
                    f"Call {PHONE}, email {EMAIL}, or use the contact form. Address: {ADDRESS}.",
                ),
            ]
        )
        + org_schema()
        + footer(1),
    )
    urls.append("/about-capital-compliance/")

    write(
        ROOT / "about-capital-compliance" / "why-choose-us" / "index.html",
        head("Why Choose Capital Compliance", "Why carriers choose Capital Compliance.")
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose Capital Compliance</h2>
<p class="lead">One-stop trucking compliance with proactive monitoring and monthly plans for every fleet size.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>One-stop shop</h3><p>Formation through credentials and monitoring — not a scatter of vendors.</p></div>
<div class="card"><h3>Daily alerts</h3><p>Out-of-service orders, inactive DOT status, and authority revocation monitoring.</p></div>
<div class="card"><h3>Monthly plans</h3><p>Tailored support for small fleets and large-scale operations.</p></div>
<div class="card"><h3>Authority launch support</h3><p>LLC/EIN, MC/DOT, and BOC-3 sequenced so you can hit the road.</p></div>
<div class="card"><h3>Interstate credentials</h3><p>UCR and IRP support for carriers that cross state lines.</p></div>
<div class="card"><h3>Road to Success</h3><p>Customized compliance planning — not a generic checklist dump.</p></div>
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
<p class="lead">Engagements tailored to how different carriers buy and operate compliance support.</p>
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
            "Questions about monthly plans, MC/DOT authority, BOC-3, UCR, IRP, or DOT monitoring.",
        ),
        (
            "request-a-consultation",
            "Request a Consultation | Capital Compliance",
            "Request a Consultation",
            "Tell us what your fleet needs — we will recommend a practical first step.",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | Capital Compliance",
            "Request a Proposal",
            "Share fleet size and scope. We will return a scoped proposal you can compare.",
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

**NearMe OS Website Factory staging engine · category: trucking / motor-carrier compliance · facts from live capitalcompliance.co (2026-07-22; direct fetch 403 — NAP/services from indexed content) · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | Capital Compliance | live site |
| A2 domain | capitalcompliance.co | live site |
| A3 phone | {PHONE} | live site |
| A4 email | {EMAIL} | live site |
| A5 address | {ADDRESS} | live site |
| A6 trade | Trucking / motor-carrier compliance services | live site |
| A10 value_proposition | Rely on Capital Compliance — your one-stop shop for ALL your compliance needs | user + live site |
| A11 tagline | {TAGLINE} | user / live positioning |
| A12 hours | *[confirm]* | not confirmed in indexed snapshot |
| A13 services_core | LLC/EIN; MC/DOT; BOC-3; UCR; IRP; DOT monitoring/alerts; monthly compliance plans | live site |

## B — Services: 10 × 10
{hub_slugs}
FORM-CONSULT=`request-a-consultation` · FORM-PRICING=`request-a-proposal`

## Notes
- Direct site fetch returned 403; NAP/services taken from search-indexed page content [confirm]
- Staging: noindex + STAGING PREVIEW
| hubs | {len(HUBS)} | children | {svc_children} |
""",
    )

    write(
        ROOT / "CAPITALCOMPLIANCE-NOTES.md",
        """# Capital Compliance — Factory Build

Category: **trucking / motor-carrier compliance**.

- Live source: https://capitalcompliance.co/
- Generator: `scripts/generate_capitalcompliance_factory.py`
- Gate 1: 10 × 10 = 100 SVC-CHILD (+ chrome = 117 pages)
- FORM-CONSULT: `/request-a-consultation/`
- FORM-PRICING: `/request-a-proposal/`
- NAP from live site: 222 NE Park Plaza Dr, Vancouver, WA · (360) 566-5798 · safety@capitalcompliance.co
- Direct fetch returned 403 on 2026-07-22 — facts from indexed content [confirm]
""",
    )

    factory_pages = list(ROOT.rglob("index.html"))
    print(f"Generated {len(factory_pages)} factory index pages")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)} · Children: {sum(len(h['children']) for h in HUBS)}")


if __name__ == "__main__":
    main()
