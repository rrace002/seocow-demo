#!/usr/bin/env python3
"""Generate Trade OS site using the NearMe OS Website Factory template
(same HTML/CSS engine as the SEO Cow / Near Me OS staging builds).

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Sibling product to Near Me OS for contractors & trades market ownership.
Facts grounded from Race Computer Services / Near Me OS operator defaults;
empty GitHub repo rrace002/Trade-OS — no live marketing site · [confirm] uncertain fields.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://tradeos.io"  # [confirm]
PHONE = "(862) 295-0011"
PHONE_TEL = "+18622950011"
EMAIL = "info@tradeos.io"  # [confirm]
HQ = "Elizabeth, NJ"
ADDRESS = "12 Sayre St, Elizabeth, NJ 07208"
OPERATOR = "Race Computer Services, LLC"
TAGLINE = "Stop Chasing Jobs. Start Owning Trade Markets."
STAGING_BANNER = (
    "STAGING PREVIEW — tradeos.io factory build · content pending owner review "
    "· not a live Trade OS website"
)

# NearMe factory CSS (SEO Cow template) with Trade OS industrial amber/steel remap
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#1c1917;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#b45309;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#1c1917;color:#fde68a;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#292524;color:#fef3c7;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #d97706;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#1c1917}.logo span{color:#d97706}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#78716c;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#1c1917}
.phone-cta small{display:block;color:#78716c;font-size:11px}
nav.nav{background:#292524}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#1c1917;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #d97706;z-index:60}
.dd a{color:#1c1917;padding:10px 15px;font-weight:500;border-bottom:1px solid #e7e5e4}
.dd a:hover{background:#fffbeb}
.nav .em a{background:#d97706}.nav .em a:hover{background:#b45309}
.hero{background:linear-gradient(rgba(28,25,23,.86),rgba(28,25,23,.86)),repeating-linear-gradient(45deg,#292524 0 14px,#44403c 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#fde68a;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#d97706;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#f59e0b;text-decoration:none}
.btn.alt{background:#292524;color:#fff}.btn.alt:hover{background:#44403c}
section{padding:44px 0}
section.tint{background:#fffbeb}
section h2{font-size:25px;color:#1c1917;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#d97706;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #e7e5e4;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(28,25,23,.06)}
.card h3{color:#1c1917;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #e7e5e4;border-left:4px solid #d97706;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#1c1917}
.gcard p{font-size:14px;color:#57534e;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#b45309}
.ctastrip{background:#292524;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #e7e5e4;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#fafaf9}.vs .col.good{background:#fffbeb}
.vs h3{font-size:16px;margin-bottom:12px;color:#1c1917}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#b45309;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #e7e5e4;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#1c1917;list-style:none}
details summary:before{content:"+ ";color:#d97706;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #e7e5e4;border-top:4px solid #d97706;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#57534e;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#78716c;padding:14px 0 0}
.crumb a{color:#78716c}
footer{background:#1c1917;color:#a8a29e;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#a8a29e}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #44403c;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#78716c}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #e7e5e4;border-top:4px solid #d97706;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#1c1917}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#78716c;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #e7e5e4;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(41,37,36,.07)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#1c1917}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#d97706;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#d97706;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#b45309}
"""

# Gate 1 — 10 × 10 (contractors & trades market ownership)
HUBS = [
    {
        "slug": "trade-seo-services",
        "name": "Trade SEO Services",
        "short": "Trade SEO",
        "blurb": "Rank for high-intent contractor searches — plumber near me, emergency HVAC, roofing estimates — with hub architecture and local authority that compounds.",
        "children": [
            ("trade-keyword-research", "Trade Keyword Research", "Map service + geo terms by intent, CPC, and competition for plumbing, electrical, HVAC, and more."),
            ("contractor-on-page-architecture", "Contractor On-Page Architecture", "Title tags, H1/H2 structure, and internal linking for trade service hubs."),
            ("localbusiness-schema-for-trades", "LocalBusiness Schema for Trades", "Structured data so Google understands your trade offers and service areas."),
            ("google-business-profile-for-contractors", "Google Business Profile for Contractors", "Categories, attributes, posts, and photo strategy for Maps visibility."),
            ("core-web-vitals-for-trade-sites", "Core Web Vitals for Trade Sites", "LCP, CLS, and INP fixes that keep estimate and booking pages fast."),
            ("geo-authority-content-calendar", "Geo Authority Content Calendar", "90-day calendar of geo-targeted trade articles mapped to keyword clusters."),
            ("local-trade-backlink-list", "Local Trade Backlink List", "Directories, supplier sites, and niche trade associations that move authority."),
            ("competitor-gap-analysis", "Competitor Gap Analysis", "What rival contractors rank for, what they miss, and where you win."),
            ("service-landing-page-optimization", "Service Landing Page Optimization", "Engagement-first pages that convert job seekers and send ranking signals."),
            ("multi-location-trade-seo", "Multi-Location Trade SEO", "Scale coverage across metros without doorway dilution."),
        ],
    },
    {
        "slug": "local-trade-ppc",
        "name": "Local Trade PPC",
        "short": "Trade PPC",
        "blurb": "Turn every ad dollar into a permanent SEO asset with campaigns built for emergency and estimate-intent trade search.",
        "children": [
            ("google-ads-trade-campaigns", "Google Ads Trade Campaigns", "Ad groups for emergency, estimate, and competitor/brand intent by trade."),
            ("ctr-engagement-framework", "CTR Engagement Framework", "Engagement signal strategy that compounds PPC into organic ranking."),
            ("retargeting-pixel-setup", "Retargeting Pixel Setup", "Meta + Google audiences auto-built from estimate and booking visitors."),
            ("ppc-to-seo-signal-loop", "PPC-to-SEO Signal Loop", "The flywheel blueprint that drives CAC reduction over 12 months."),
            ("keyword-intelligence-extraction", "Keyword Intelligence Extraction", "n8n workflows that pull converting search terms into your SEO pipeline."),
            ("monthly-budget-optimization", "Monthly Budget Optimization", "When to increase, when to shift, and what to kill for trade seasons."),
            ("landing-page-conversion-audit", "Landing Page Conversion Audit", "Dwell time, scroll depth, and estimate-start benchmarks."),
            ("local-service-ads-for-trades", "Local Service Ads for Trades", "Where LSAs fit alongside Search for high-intent contractor capture."),
            ("competitor-conquest-campaigns", "Competitor Conquest Campaigns", "Brand and conquest structures that stay compliant and efficient."),
            ("seasonal-trade-ad-calendars", "Seasonal Trade Ad Calendars", "HVAC peaks, roofing seasons, and landscaping windows planned in advance."),
        ],
    },
    {
        "slug": "contractor-directory-platform",
        "name": "Contractor Directory Platform",
        "short": "Directory",
        "blurb": "Launch a branded contractor directory — live, booking-ready, and built to compound authority across trades.",
        "children": [
            ("brilliant-directories-deployment", "Brilliant Directories Deployment", "Custom contractor directory on your brand, vertical mix, and domain."),
            ("contractor-profile-pages", "Contractor Profile Pages", "Trade profiles with services, service areas, and embedded booking."),
            ("embedded-estimate-booking", "Embedded Estimate & Booking", "End-to-end estimate UX that keeps engagement signals on your site."),
            ("backlink-flywheel-activation", "Backlink Flywheel Activation", "Dofollow profile links plus automated GBP posts per contractor."),
            ("contractor-onboarding-system", "Contractor Onboarding System", "Self-serve signup, profile builder, insurance docs, and calendar sync."),
            ("territory-map-pricing", "Territory Map & Pricing", "Metro, mid-tier, and rural zones with tiered licensing for trades."),
            ("stripe-connect-integration", "Stripe Connect Integration", "Split payments between platform and contractors with automated payouts."),
            ("ghl-crm-pipeline-setup", "GoHighLevel CRM Pipeline", "Lead stages from assessment → call → pilot → active → MRR."),
            ("trade-readiness-assessment-build", "Trade Readiness Assessment Build", "Custom quiz with scoring and CTAs for contractor market fit."),
            ("post-assessment-email-nurture", "Post-Assessment Email Nurture", "5-email GHL sequence from score to urgency."),
        ],
    },
    {
        "slug": "vip-trade-system",
        "name": "VIP Trade System",
        "short": "VIP System",
        "blurb": "The complete Trade OS deployment — protected metro territory, automation suite, and launch support for trade market owners.",
        "children": [
            ("protected-metro-territory", "Protected Metro Territory", "Exclusive metro/county rights — no other Trade OS operator in your zone."),
            ("ghl-automation-suite", "GoHighLevel Automation Suite", "Estimate SMS, contractor pipeline, review funnels, retargeting sync."),
            ("cross-trade-referral-engine", "Cross-Trade Referral Engine", "Plumbers, electricians, and HVAC route leads with rev-share rules."),
            ("n8n-production-workflows", "n8n Production Workflows", "10+ tested workflows for leads, dispatch alerts, payouts, and reviews."),
            ("contractor-deployment-dashboard", "Contractor Deployment Dashboard", "9-step onboarding tracker for every trade partner you bring on."),
            ("sales-frameworks-training", "Sales Frameworks & Training", "Scripts, objections, territory pitch deck, and demo flow for trades."),
            ("platform-revenue-share", "Platform Revenue Share", "Share of leads and closed jobs routed through the trade network."),
            ("monthly-flywheel-review", "Monthly Flywheel Review", "CAC, organic share, and branded search with budget guidance."),
            ("ninety-day-launch-support", "90-Day Launch Support", "Weekly check-ins through your first three territory sales."),
            ("end-to-end-trade-market-ownership", "End-to-End Trade Market Ownership", "Own acquisition, conversion, and monetization in one system."),
        ],
    },
    {
        "slug": "trade-os-license-enterprise",
        "name": "Trade OS License & Enterprise",
        "short": "OS License",
        "blurb": "White-label Trade OS with state-level rights and multi-trade deployment for enterprise operators.",
        "children": [
            ("state-wide-territory-rights", "State-Wide Territory Rights", "Lock an entire state; metro operators roll up under your license."),
            ("white-label-trade-platform", "White-Label Trade Platform", "Your brand and domain — Trade OS runs invisibly underneath."),
            ("multi-trade-deployment", "Multi-Trade Deployment", "Launch plumbing, electrical, HVAC, roofing, and more under one license."),
            ("methodology-documentation", "Methodology Documentation", "Full playbook: flywheel, territory pricing, scripts, funnels."),
            ("trade-builder-toolkit", "Trade Builder Toolkit", "Templates, schema, n8n library, and landing components for trades."),
            ("custom-ai-development-access", "Custom AI Development Access", "Workflows for estimate engines, demand forecasting, competitor monitoring."),
            ("priority-lead-routing", "Priority Lead Routing", "First pick on inbound network leads before standard licensees."),
            ("quarterly-strategy-sessions", "Quarterly Strategy Sessions", "90-minute deep dives on expansion and scaling triggers."),
            ("platform-level-rev-share", "Platform-Level Rev Share", "Earn on jobs across licensed territories and trade verticals."),
            ("enterprise-onboarding", "Enterprise Onboarding", "Dedicated cutover plan for multi-market trade operators."),
        ],
    },
    {
        "slug": "subcontractor-network",
        "name": "Subcontractor Network",
        "short": "Sub Network",
        "blurb": "Build and operate a vetted subcontractor network with dispatch, capacity, and rev-share that keeps jobs moving.",
        "children": [
            ("vetted-sub-onboarding", "Vetted Sub Onboarding", "Insurance, license, and skill checks before a sub hits the roster."),
            ("capacity-and-availability-calendar", "Capacity & Availability Calendar", "Know who can take the job before you promise the customer."),
            ("job-lead-routing", "Job Lead Routing", "Territory- and trade-aware assignment so the right sub gets the lead."),
            ("dispatch-notification-flows", "Dispatch Notification Flows", "SMS and app alerts that cut the phone-tag between GC and crew."),
            ("estimate-handoff-protocols", "Estimate Handoff Protocols", "Clean handoff from lead capture to field estimate without lost detail."),
            ("quality-score-tracking", "Quality Score Tracking", "Completion, callback, and review scores that protect the brand."),
            ("rev-share-settlement", "Rev-Share Settlement", "Transparent splits between platform, GC, and subs on closed jobs."),
            ("sub-performance-dashboards", "Sub Performance Dashboards", "Visibility into fill rate, response time, and customer scores."),
            ("insurance-compliance-reminders", "Insurance Compliance Reminders", "Automated renewals so coverage never silently expires."),
            ("overflow-capacity-pooling", "Overflow Capacity Pooling", "Route surge demand to backup subs without breaking exclusivity rules."),
        ],
    },
    {
        "slug": "trade-vertical-markets",
        "name": "Trade Vertical Markets",
        "short": "Verticals",
        "blurb": "Launch Trade OS in specific trades — plumbing, electrical, HVAC, roofing, landscaping, and more — with patterns tuned to how each buys and books.",
        "children": [
            ("plumbing-near-me-market", "Plumbing Near Me Market", "Emergency and planned plumbing demand with estimate and dispatch loops."),
            ("electrical-contractor-market", "Electrical Contractor Market", "Residential and light-commercial electrical directories and lead routing."),
            ("hvac-service-market", "HVAC Service Market", "Seasonal peaks, maintenance plans, and emergency HVAC capture."),
            ("roofing-contractor-market", "Roofing Contractor Market", "Storm and reroof demand with photo-estimate and review loops."),
            ("landscaping-outdoor-market", "Landscaping & Outdoor Market", "Recurring lawn and outdoor service booking patterns."),
            ("general-contractor-market", "General Contractor Market", "GC-focused lead capture with sub-network handoffs."),
            ("painting-remodeling-market", "Painting & Remodeling Market", "Project-based estimate funnels for interior/exterior trades."),
            ("pest-control-market", "Pest Control Market", "Recurring service plans with review and retargeting loops."),
            ("cleaning-janitorial-market", "Cleaning & Janitorial Market", "Recurring B2B and residential cleaning market patterns."),
            ("multi-trade-bundle-markets", "Multi-Trade Bundle Markets", "Own several trades in one metro under a single Trade OS license."),
        ],
    },
    {
        "slug": "ppc-to-seo-flywheel",
        "name": "PPC-to-SEO Flywheel",
        "short": "Flywheel",
        "blurb": "Every PPC dollar becomes a permanent SEO asset — competitors keep renting clicks; you own the trade-market moat.",
        "children": [
            ("rank-capture-distribute-loop", "Rank → Capture → Distribute Loop", "The five-step engine: Rank, Capture, Distribute, Monetize, Reinvest."),
            ("engagement-signal-compounding", "Engagement Signal Compounding", "On-domain estimate and booking behavior that Google rewards."),
            ("organic-share-growth", "Organic Share Growth", "Move from paid-heavy acquisition to majority organic share models."),
            ("cac-reduction-playbook", "CAC Reduction Playbook", "Operate toward lower cost-per-job as organic compounds over 12 months."),
            ("branded-search-acceleration", "Branded Search Acceleration", "Grow branded queries as the market learns your trade platform."),
            ("reinvest-loop-budgeting", "Reinvest Loop Budgeting", "How job revenue funds the next wave of PPC → SEO compounding."),
            ("flywheel-math-modeling", "Flywheel Math Modeling", "Without vs with models your buyers can compare on a call."),
            ("signal-quality-monitoring", "Signal Quality Monitoring", "Track dwell, estimate starts, and bounce so the loop stays healthy."),
            ("competitor-rent-vs-own", "Competitor Rent vs Own", "Positioning that explains why paid-only rivals stay trapped."),
            ("compounding-asset-reporting", "Compounding Asset Reporting", "Monthly proof that ad spend is becoming equity."),
        ],
    },
    {
        "slug": "territory-licensing",
        "name": "Territory Licensing",
        "short": "Territories",
        "blurb": "License protected trade markets — county, metro, or state — with pricing that matches demand density.",
        "children": [
            ("county-metro-exclusivity", "County & Metro Exclusivity", "One operator per zone so licensees can invest with confidence."),
            ("tier-1-territory-pricing", "Tier 1 Territory Pricing", "Metro pricing models for dense trade demand [confirm]."),
            ("mid-tier-rural-zones", "Mid-Tier & Rural Zones", "Accessible entry points that still protect density."),
            ("territory-sales-scripts", "Territory Sales Scripts", "Pitch language that sells exclusivity without overpromising."),
            ("operator-roll-up-structure", "Operator Roll-Up Structure", "How county licenses nest under state Trade OS licenses."),
            ("license-agreement-framework", "License Agreement Framework", "Commercial terms outline for founding members [confirm legal]."),
            ("market-density-scoring", "Market Density Scoring", "Choose zones with enough search demand to fuel the flywheel."),
            ("multi-territory-expansion", "Multi-Territory Expansion", "Sequencing second and third markets after first proof."),
            ("territory-performance-kpis", "Territory Performance KPIs", "Jobs booked, organic share, and MRR that prove ownership."),
            ("founding-member-cohort", "Founding Member Cohort", "First-cohort pricing windows for Platform and VIP tiers [confirm]."),
        ],
    },
    {
        "slug": "trade-automation-stack",
        "name": "Trade Automation Stack",
        "short": "Automation",
        "blurb": "n8n, GoHighLevel, Stripe, and assessment funnels that run the trade market while you sell territories.",
        "children": [
            ("n8n-workflow-library", "n8n Workflow Library", "Reusable automations for leads, dispatch, payouts, backlinks, and alerts."),
            ("gohighlevel-lifecycle-sms", "GoHighLevel Lifecycle SMS", "Estimate and appointment sequences that reduce no-shows."),
            ("review-request-automation", "Review Request Automation", "Post-job prompts that build Maps and platform reputation."),
            ("payout-trigger-workflows", "Payout Trigger Workflows", "Automated contractor payouts tied to completed jobs."),
            ("lead-routing-rules", "Lead Routing Rules", "Territory- and trade-aware assignment so the right pro gets the lead."),
            ("retargeting-audience-sync", "Retargeting Audience Sync", "Push estimate visitors into Meta and Google audiences."),
            ("estimate-engine-automations", "Estimate Engine Automations", "Rules-based estimate prompts and follow-ups for common trade jobs."),
            ("demand-forecasting-hooks", "Demand Forecasting Hooks", "Signal when to raise ad spend or open a new zone."),
            ("competitor-monitoring-alerts", "Competitor Monitoring Alerts", "Watch rival ads and ranking moves without manual checks."),
            ("supabase-data-schema", "Supabase Data Schema", "Trade builder data model for profiles, jobs, and zones."),
        ],
    },
]

INDUSTRIES = [
    "Plumbing",
    "Electrical",
    "HVAC",
    "Roofing",
    "Landscaping & Outdoor",
    "General Contracting",
    "Painting & Remodeling",
    "Pest Control",
    "Cleaning & Janitorial",
    "Multi-Trade Operators",
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
<div class="logo">Trade <span>OS</span><small>Markets for Contractors &amp; Trades</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Free Trade Readiness Assessment — no obligation</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Solutions &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-trade-os/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-trade-os/index.html">About Trade OS</a>
<a href="{p}about-trade-os/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-trade-os/verticals-we-serve/index.html">Verticals We Serve</a>
</div></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li><a href="{p}request-a-proposal/index.html">Apply / Proposal</a></li>
<li class="em"><a href="{p}trade-readiness-assessment/index.html">Free Assessment</a></li>
</ul></div></nav>
"""


def footer(depth: int) -> str:
    p = pfx(depth)
    hubs = "".join(
        f'<li><a href="{p}{h["slug"]}/index.html">{escape(h["short"])}</a></li>' for h in HUBS
    )
    return f"""<footer><div class="wrap"><div class="fcols">
<div><h4>Solutions</h4><ul>{hubs}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="{p}about-trade-os/index.html">About Trade OS</a></li>
<li><a href="{p}about-trade-os/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-trade-os/verticals-we-serve/index.html">Verticals</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}trade-readiness-assessment/index.html">Trade Readiness Assessment</a></li>
<li><a href="{p}request-a-proposal/index.html">Apply / Request Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul><li>{escape(ADDRESS)}</li><li>Operated by {escape(OPERATOR)}</li><li>Remote deployment nationwide</li></ul></div>
</div>
<div class="copy">Trade OS &middot; {escape(OPERATOR)} &middot; {escape(HQ)} &middot; {escape(PHONE)}<br>
Copyright &copy; 2026. Trade OS. All rights reserved.</div></div></footer>
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
<label>Primary Trade / Vertical</label><select><option>Please choose&hellip;</option><option>Plumbing</option><option>Electrical</option><option>HVAC</option><option>Roofing</option><option>Landscaping</option><option>General Contracting</option><option>Multi-trade / Other</option></select>
<label>Ad Spend Capacity</label><select><option>Please choose&hellip;</option><option>$1,500+/month (required for flywheel tiers)</option><option>Under $1,500/month</option><option>Not sure yet</option></select>
<label>Interest</label><select><option>Please choose&hellip;</option>{opts}<option>Trade Readiness Assessment</option><option>Founding Member / VIP</option><option>OS License</option><option>Other</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#78716c">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Trade OS",
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
            f'<a href="{h["slug"]}/index.html" style="font:600 13px \'Segoe UI\',sans-serif">All {escape(h["short"]).lower()} solutions &rarr;</a></div>'
        )
    return (
        head(
            "Trade OS | Own Local Contractor & Trade Markets",
            "Trade OS is the operating system for building, ranking, and monetizing local contractor and trade markets — AI automation, territory licensing, and a PPC-to-SEO flywheel.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>Stop Chasing Jobs. Start Owning Trade Markets.</h1>
<p>{escape(TAGLINE)}</p>
<a class="btn" href="trade-readiness-assessment/index.html">Take the Trade Readiness Assessment</a> <a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>10</b><span>Solution Families</span></div>
<div class="stat"><b>PPC→SEO</b><span>Flywheel Model</span></div>
<div class="stat"><b>Exclusive</b><span>Metro Territories</span></div>
<div class="stat"><b>GHL + n8n</b><span>Automation Stack</span></div>
</div></div></section>
<section><div class="wrap"><h2>What can Trade OS build for you?</h2>
<p class="lead">Ten solution families — from trade SEO/PPC through directory, VIP, OS license, sub networks, verticals, flywheel, territories, and automation.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure which path fits? Start free.</h2>
<p style="margin-bottom:14px">The Trade Readiness Assessment shows where you stand — then we map territory and tier.</p>
<a class="btn" href="trade-readiness-assessment/index.html">Take the Free Assessment</a></div></div>
<section><div class="wrap"><h2>How founding members get started</h2><div class="cols3">
<div class="card"><h3>1. Free Trade Readiness Assessment</h3><p>Score gaps, capacity, and fit for directory, VIP, or OS license paths.</p></div>
<div class="card"><h3>2. Strategy call &amp; tier fit</h3><p>Confirm ad spend capacity, then choose SEO, PPC, Platform, VIP, or OS License.</p></div>
<div class="card"><h3>3. Deploy the flywheel</h3><p>Launch the contractor market and compound PPC into SEO equity.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why Trade OS</h2><div class="cols3">
<div class="card"><h3>Built for trades</h3><p>Job leads, estimates, dispatch, GBP, and reviews — not generic agency retainers.</p></div>
<div class="card"><h3>PPC that becomes equity</h3><p>Competitors keep renting clicks. Your flywheel turns spend into organic share.</p></div>
<div class="card"><h3>One OS, many trades</h3><p>Plumbing, electrical, HVAC, roofing, landscaping, and multi-trade bundles under one system.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready to own your trade market?</h2>
<a class="btn" href="trade-readiness-assessment/index.html">Trade Readiness Assessment</a> <a class="btn alt" href="request-a-proposal/index.html">Apply / Request Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    "What is Trade OS?",
                    "Trade OS is the operating system for building, ranking, and monetizing local contractor and trade markets — with AI automation, territory licensing, and a compounding PPC-to-SEO flywheel.",
                ),
                (
                    "Who operates Trade OS?",
                    f"Trade OS is operated by {OPERATOR}, headquartered at {ADDRESS}.",
                ),
                (
                    "What is the Trade Readiness Assessment?",
                    "A free assessment that scores where you stand, then routes you toward the right tier and founding path.",
                ),
                (
                    "Do I need ad spend capacity?",
                    "Flywheel tiers require confirmation of $1,500+/month ad spend capacity so the PPC-to-SEO loop has enough fuel to compound.",
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
            f"{h['name']} | Trade OS",
            f"{h['name']} from Trade OS — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} — From Trade OS</h2>
<p class="lead">{escape(h["blurb"])} Delivered as part of the Trade OS stack rather than an isolated task.</p>
<p><a class="btn" href="../trade-readiness-assessment/index.html">Take the Trade Readiness Assessment</a> <a class="btn alt" href="../request-a-proposal/index.html">Apply / Request Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Solutions We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What Your Engagement Can Include</h2>
<ul class="checks">
<li>Scoped discovery tied to trade demand and ad capacity</li>
<li>Implementation with the PPC-to-SEO flywheel in mind</li>
<li>Territory and licensing clarity where exclusivity applies</li>
<li>Automation hooks in n8n + GoHighLevel where included</li>
<li>One accountable OS — not a pile of disconnected freelancers</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with the free Trade Readiness Assessment. We map fit and provide a written proposal before work begins.",
                ),
                (
                    "Where is Trade OS based?",
                    f"Headquartered in {HQ} ({ADDRESS}), with remote deployment nationwide.",
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
        head(f"{name} | Trade OS", f"{name} from Trade OS — {blurb}")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Rely on Trade OS as your partner for {escape(name.lower())} and related trade-market systems.</h2>
<p class="lead">{escape(blurb)} At Trade OS, {escape(name.lower())} is delivered inside a compounding trade-market OS — measured, automated, and pointed at ownership, not one-off billables.</p>
<p><a class="btn" href="../../trade-readiness-assessment/index.html">Take the Trade Readiness Assessment</a> <a class="btn alt" href="../../request-a-proposal/index.html">Apply / Request Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(name)} Combined with Trade OS Can Help You Gain:</h2>
<ul class="checks">
<li>Higher-intent job demand that lands on your platform</li>
<li>Lower CAC as organic share compounds against paid</li>
<li>Territory clarity so investment is protected</li>
<li>Automation that keeps contractors and subs fed</li>
<li>Reporting that proves the flywheel is working</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} engagement scoped to your market — not a one-size package</h2>
<p>No two trade markets need {escape(name.lower())} the same way. We design around your vertical, territory density, and ad capacity — then put scope and founding price in writing before work begins.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Operators avoid key risks by using a developed trade-market OS for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with services-only approaches</h3><ul>
<li>PPC that never becomes an SEO asset</li>
<li>Directories with no booking or backlink loop</li>
<li>Territories sold without exclusivity or density math</li>
<li>Reporting that shows activity, not market ownership</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on Trade OS</h3><ul>
<li>PPC-to-SEO flywheel operated as one system</li>
<li>Clear territory and licensing paths</li>
<li>Evidence-friendly flywheel reporting</li>
<li>Founding-member accountability with a named team</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>See where you stand first — free</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} would look like for your trade market? Start with the Trade Readiness Assessment.</p>
<a class="btn" href="../../trade-readiness-assessment/index.html">Take the Trade Readiness Assessment</a> <a class="btn alt" href="../../request-a-proposal/index.html">Apply / Request Proposal</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} shows results?",
                    "Timelines depend on trade vertical and ad capacity. Platform builds follow a structured production path; your proposal includes an honest schedule.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Scope drives price. Founding tiers span SEO/PPC layers through Platform, VIP, and OS License — confirmed after assessment.",
                ),
                (
                    f"Why choose Trade OS for {name.lower()}?",
                    f"We deliver {name.lower()} inside a trade-market OS — Race Computer Services accountability with a compounding flywheel stack.",
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
<h2 style="font-size:20px">Initiate a request with Trade OS</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us your market</h3><p>Trade vertical, geography, and whether you lean directory, VIP, or OS license.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>An assessment, a tier recommendation, or honest advice — whichever fits.</p></div>
<div class="card"><h3>3. Decide with the full picture</h3><p>Plan and founding price in writing before you commit anything.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>Trade OS</strong><br>Operated by {escape(OPERATOR)}<br>Headquarters: {escape(ADDRESS)}<br>Phone: {escape(PHONE)}<br>Email: {escape(EMAIL)}</p>
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
        ["/", "HOME", "", "trade os", "logo/home", "A1,A6,A10", ""],
        [
            "/about-trade-os/",
            "COMP-HUB",
            "/",
            "about trade os",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-trade-os/why-choose-us/",
            "COMP-CHILD",
            "/about-trade-os/",
            "why choose trade os",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-trade-os/verticals-we-serve/",
            "COMP-CHILD",
            "/about-trade-os/",
            "trade verticals",
            "About menu",
            "D1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact trade os",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "trade os proposal",
            "nav utility",
            "I1",
            "Request for Proposal",
        ],
        [
            "/trade-readiness-assessment/",
            "FORM-CONSULT",
            "/",
            "trade readiness assessment",
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
    with (ROOT / "TRADEOS-PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "TRADEOS-QUESTIONNAIRE-ANSWERS.md",
        "TRADEOS-PAGE-INVENTORY.csv",
        "TRADEOS-NOTES.md",
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
        ROOT / "about-trade-os" / "index.html",
        head(
            "About Trade OS | Elizabeth, NJ",
            "Trade OS is operated by Race Computer Services, LLC in Elizabeth, NJ.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About Trade OS</h2>
<p class="lead">Trade OS is the operating system for building, ranking, and monetizing local contractor and trade markets — operated by {escape(OPERATOR)} from {escape(ADDRESS)}.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>We built Trade OS because contractors keep chasing the next job while agencies sell hours. Market ownership compounds for operators who own demand — SEO, PPC, directories, territory licensing, and automation under one OS. Sibling product to Near Me OS from the same operator.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="verticals-we-serve/index.html">Verticals &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "Who operates Trade OS?",
                    f"Trade OS is operated by {OPERATOR}, headquartered at {ADDRESS}.",
                ),
                (
                    "Do you work outside New Jersey?",
                    "Yes — remote deployment nationwide, with HQ in Elizabeth, NJ.",
                ),
            ]
        )
        + org_schema()
        + footer(1),
    )
    urls.append("/about-trade-os/")

    write(
        ROOT / "about-trade-os" / "why-choose-us" / "index.html",
        head("Why Choose Trade OS", "Why operators choose Trade OS to own contractor and trade markets.")
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose Trade OS</h2>
<p class="lead">A trade-market OS built to help operators stop chasing jobs and start owning local demand.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Flywheel by design</h3><p>PPC, SEO, estimates, booking, and territory licensing operated as one compounding system.</p></div>
<div class="card"><h3>Built for contractors</h3><p>Job leads, dispatch, GBP, reviews, and sub networks — not generic agency retainers.</p></div>
<div class="card"><h3>Multi-trade ready</h3><p>Plumbing, electrical, HVAC, roofing, landscaping, and bundles under one OS.</p></div>
<div class="card"><h3>Assessment-led sales</h3><p>Free Trade Readiness Assessment first; written scope before you commit.</p></div>
<div class="card"><h3>Founding economics</h3><p>Founding-cohort pricing on Platform and VIP while the cohort fills [confirm].</p></div>
<div class="card"><h3>Elizabeth HQ</h3><p>Race Computer Services accountability with nationwide remote delivery.</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-trade-os/why-choose-us/")

    ind = "".join(
        f'<div class="gcard"><h3>{escape(i)}</h3><p>Trade OS patterns tuned to {escape(i.lower())} demand, estimates, and booking loops.</p></div>'
        for i in INDUSTRIES
    )
    write(
        ROOT / "about-trade-os" / "verticals-we-serve" / "index.html",
        head("Verticals We Serve | Trade OS", "Trade verticals Trade OS helps operators own.")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Verticals</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Verticals We Serve</h2>
<p class="lead">Directory and territory deployments tailored to how each trade buys and books.</p>
<div class="grid">{ind}</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-trade-os/verticals-we-serve/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | Trade OS",
            "Contact Us for Trade OS Inquiries",
            "Tell us your trade vertical, geography, and whether you are exploring directory, VIP, or a full OS license.",
        ),
        (
            "trade-readiness-assessment",
            "Trade Readiness Assessment | Trade OS",
            "Take the Free Trade Readiness Assessment",
            "See where you stand — then book a strategy call to claim your trade territory.",
        ),
        (
            "request-a-proposal",
            "Apply / Request a Proposal | Trade OS",
            "Apply or Request a Proposal",
            "Share your goals and ad capacity. We'll return a scoped founding proposal you can compare anywhere.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | Trade OS", "Page not found.")
        + chrome(0)
        + """
<section style="padding:72px 0"><div class="wrap"><h2 style="font-size:28px">Page not found</h2>
<p class="lead">That URL isn't in this market. Try home or the Trade Readiness Assessment.</p>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn alt" href="trade-readiness-assessment/index.html">Free Assessment</a></p>
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
        ROOT / "TRADEOS-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — Trade OS (FACTORY BUILD · Gate 1 10×10)

**Build uses NearMe OS Website Factory instructions-template (SEO Cow staging engine) · facts from Race Computer Services / Near Me OS operator defaults · empty GitHub repo rrace002/Trade-OS (no live marketing site) · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | Trade OS (operated by Race Computer Services, LLC) | operator default / sibling to Near Me OS |
| A2 domain | tradeos.io | [confirm] |
| A3 phone | {PHONE} | Race CS / Near Me OS operator default |
| A4 email | {EMAIL} | [confirm] |
| A5 address | {ADDRESS} | Race CS / Near Me OS operator default |
| A6 trade | Contractor & trades market OS / territory licensing / AI automation | product brief |
| A7 founded | not stated — omitted | — |
| A10 value_proposition | Build, rank, and monetize local contractor/trade markets with AI automation, territory licensing, and a PPC-to-SEO flywheel | product brief |
| A11 tagline | {TAGLINE} | product brief |
| A12 competitor_type | agencies selling hours, lead-gen portals, paid-only media buyers, generic directory platforms | [confirm] |
| A13 hours | not stated — omitted | — |

## B — Services: 10 categories × 10 children (Gate 1 for ~117-page build)
{hub_slugs} — full map in TRADEOS-PAGE-INVENTORY.csv.
All Standard class → RFP booking (proposal), with FORM-CONSULT `trade-readiness-assessment` as the primary funnel entry.
FORM-PRICING=`request-a-proposal`.

## C–I
- C2 do_not_rank: n/a (trade-market OS is the trade)
- D1 industries/verticals: Trade Vertical Markets hub + About > Verticals (plumbing, electrical, HVAC, roofing, landscaping, etc.)
- E1 platforms: OFF as separate PLAT area — Brilliant Directories / GHL / n8n / Stripe live as SVC-CHILDs
- F1 service_area: Elizabeth NJ HQ, nationwide remote
- F2/F3: no LOC pages (anti-doorway)
- G1/G2: no invented testimonials — empty repo / no live site proof pages yet
- I1 form_destination: OPEN — demo shells; assessment CTA adopted as FORM-CONSULT
- Budget qualification: $1,500+/month ad spend for flywheel tiers (Near Me OS sibling pattern)

| Metric | Value |
|---|---|
| hubs | {len(HUBS)} |
| svc children | {svc_children} |
| staging | noindex + STAGING PREVIEW banner |
""",
    )

    write(
        ROOT / "TRADEOS-NOTES.md",
        f"""# Trade OS — Factory Gate 1 Notes

## Status
- Empty GitHub repo `rrace002/Trade-OS` — no live marketing site at write time.
- Staging factory build only: `noindex` + STAGING PREVIEW banner.
- Generator: `scripts/generate_tradeos_factory.py`.

## Grounding
- Operator defaults from Race Computer Services / Near Me OS sibling: phone, HQ, address.
- Domain `{BASE}` and email `{EMAIL}` marked **[confirm]**.
- Founded date: not stated — omitted.
- No invented testimonials.

## Brand
- Tagline: {TAGLINE}
- Logo chrome: Trade OS / Markets for Contractors & Trades
- Palette: industrial amber/steel (`#d97706` / `#b45309` accents; `#1c1917` / `#292524` dark chrome; `#fffbeb` tints)

## Page math (expected)
- HOME 1 + SVC-HUB 10 + SVC-CHILD 100 + COMP-HUB 1 + COMP-CHILD 2 + COMP-CONTACT 1 + FORM-CONSULT 1 + FORM-PRICING 1 = **117** `index.html` pages
- Plus `404.html`, `sitemap.xml`, `robots.txt`, Netlify headers, inventory/questionnaire/notes

## Primary CTAs
- FORM-CONSULT: `/trade-readiness-assessment/` (highlighted nav)
- FORM-PRICING: `/request-a-proposal/`
""",
    )

    pages = list(ROOT.rglob("index.html"))
    factory_pages = list(pages)
    print(f"Generated {len(factory_pages)} factory index pages")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)} · Children: {sum(len(h['children']) for h in HUBS)}")


if __name__ == "__main__":
    main()
