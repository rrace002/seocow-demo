#!/usr/bin/env python3
"""Generate Near Me OS site using the NearMe OS Website Factory template
(same HTML/CSS engine as the SEO Cow / Red Rabbit staging builds).

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 107).
Facts grounded from Near Me OS product landing + Race Computer Services S1.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://nearmeos.io"
PHONE = "(862) 295-0011"
PHONE_TEL = "+18622950011"
EMAIL = "info@nearmeos.io"  # [confirm]
HQ = "Elizabeth, NJ"
ADDRESS = "12 Sayre St, Elizabeth, NJ 07208"
OPERATOR = "Race Computer Services, LLC"
TAGLINE = "Stop Selling Services. Start Owning Markets."
STAGING_BANNER = (
    "STAGING PREVIEW — nearmeos.io factory build · content pending owner review "
    "· not the live Near Me OS website"
)

# NearMe factory CSS (SEO Cow template) with Near Me OS orange remap
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#1c1612;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#c24e14;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#1c1410;color:#f5c9a8;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#5c2e14;color:#f3ddd0;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #e86a2a;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#3d2418}.logo span{color:#e86a2a}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#3d2418}
.phone-cta small{display:block;color:#5a6b7b;font-size:11px}
nav.nav{background:#5c2e14}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#3d1e0c;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #e86a2a;z-index:60}
.dd a{color:#1c1612;padding:10px 15px;font-weight:500;border-bottom:1px solid #f1e8e0}
.dd a:hover{background:#faf3ee}
.nav .em a{background:#e86a2a}.nav .em a:hover{background:#c24e14}
.hero{background:linear-gradient(rgba(20,12,8,.82),rgba(20,12,8,.82)),repeating-linear-gradient(45deg,#5c2e14 0 14px,#6e3818 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#f5c9a8;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#e86a2a;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#f07a3a;text-decoration:none}
.btn.alt{background:#5c2e14;color:#fff}.btn.alt:hover{background:#7a3c1a}
section{padding:44px 0}
section.tint{background:#faf5f2}
section h2{font-size:25px;color:#3d2418;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#e86a2a;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #e6ddd6;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(40,20,10,.06)}
.card h3{color:#3d2418;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #e6ddd6;border-left:4px solid #e86a2a;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#3d2418}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#c24e14}
.ctastrip{background:#5c2e14;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #e6ddd6;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#faf5f2}.vs .col.good{background:#f8f2ee}
.vs h3{font-size:16px;margin-bottom:12px;color:#3d2418}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#c24e14;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #e6ddd6;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#3d2418;list-style:none}
details summary:before{content:"+ ";color:#e86a2a;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #e6ddd6;border-top:4px solid #e86a2a;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#44525f;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5a6b7b;padding:14px 0 0}
.crumb a{color:#5a6b7b}
footer{background:#2a180e;color:#c9b8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #4a3020;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #e6ddd6;border-top:4px solid #e86a2a;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#3d2418}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #e6ddd6;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(92,46,20,.07)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#3d2418}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#e86a2a;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#e86a2a;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#8a3c16}
"""

# Gate 1 — 10 × 10 (user revision request ~100 pages; grounded in product landing)
HUBS = [
    {
        "slug": "near-me-seo-services",
        "name": "Near Me SEO Services",
        "short": "Near Me SEO",
        "blurb": "Rank for high-intent 'X near me' searches with hub architecture, schema, and local authority that compounds.",
        "children": [
            ("local-near-me-keyword-research", "Local Near Me Keyword Research", "Map 50+ near-me terms by intent, CPC, and competition for your vertical."),
            ("on-page-seo-architecture", "On-Page SEO Architecture", "Title tags, H1/H2 structure, and internal linking plans for hub pages."),
            ("localbusiness-schema-markup", "LocalBusiness Schema Markup", "Structured data ready to paste so Google understands your offers."),
            ("google-business-profile-optimization", "Google Business Profile Optimization", "Category, attributes, posts, and photo strategy for Maps visibility."),
            ("core-web-vitals-optimization", "Core Web Vitals Optimization", "LCP, CLS, and INP fixes that keep ranking pages fast."),
            ("geo-authority-content-calendar", "Geo Authority Content Calendar", "90-day calendar of geo-targeted articles mapped to keyword clusters."),
            ("local-backlink-opportunity-list", "Local Backlink Opportunity List", "Directories, chambers, and niche sites that move local authority."),
            ("competitor-gap-analysis", "Competitor Gap Analysis", "What rivals rank for, what they miss, and where you win."),
            ("near-me-landing-page-optimization", "Near Me Landing Page Optimization", "Engagement-first pages that convert and send ranking signals."),
            ("multi-location-near-me-seo", "Multi-Location Near Me SEO", "Scale near-me coverage across metros without doorway dilution."),
        ],
    },
    {
        "slug": "local-ppc-services",
        "name": "Local PPC Services",
        "short": "Local PPC",
        "blurb": "Turn every ad dollar into a permanent SEO asset with campaigns built for the PPC-to-SEO flywheel.",
        "children": [
            ("google-ads-near-me-campaigns", "Google Ads Near Me Campaigns", "Ad groups for airport, city-level near-me, and competitor/brand intent."),
            ("ctr-engagement-framework", "CTR Engagement Framework", "Engagement signal strategy that compounds PPC into organic ranking."),
            ("retargeting-pixel-setup", "Retargeting Pixel Setup", "Meta + Google audiences auto-built from booking page visitors."),
            ("ppc-to-seo-signal-loop", "PPC-to-SEO Signal Loop", "The flywheel blueprint that drives CAC reduction over 12 months."),
            ("keyword-intelligence-extraction", "Keyword Intelligence Extraction", "n8n workflows that pull converting search terms into your SEO pipeline."),
            ("monthly-budget-optimization", "Monthly Budget Optimization", "When to increase, when to shift, and what to kill."),
            ("landing-page-conversion-audit", "Landing Page Conversion Audit", "Dwell time, scroll depth, and booking-start benchmarks."),
            ("retargeting-cpm-modeling", "Retargeting CPM Modeling", "Warm audience costs vs cold PPC, updated monthly."),
            ("local-service-ads-strategy", "Local Service Ads Strategy", "Where LSAs fit alongside Search for high-intent local capture."),
            ("competitor-conquest-campaigns", "Competitor Conquest Campaigns", "Brand and conquest structures that stay compliant and efficient."),
        ],
    },
    {
        "slug": "directory-platform-build",
        "name": "Directory Platform Build",
        "short": "Platform Build",
        "blurb": "Launch a branded Near Me directory — live, booking-ready, and built to compound authority.",
        "children": [
            ("brilliant-directories-deployment", "Brilliant Directories Deployment", "Custom directory on your vertical, brand, and domain."),
            ("operator-profile-pages", "Operator Profile Pages", "Provider profiles with embedded booking that stays on-domain."),
            ("embedded-booking-engine", "Embedded Booking Engine", "End-to-end booking UX that keeps engagement signals on your site."),
            ("backlink-flywheel-activation", "Backlink Flywheel Activation", "Dofollow profile links plus automated GBP posts per operator."),
            ("provider-onboarding-system", "Provider Onboarding System", "Self-serve signup, profile builder, and calendar sync."),
            ("territory-map-pricing", "Territory Map & Pricing", "Metro, mid-tier, and rural zones with tiered licensing."),
            ("stripe-connect-integration", "Stripe Connect Integration", "Split payments between platform and operators with automated payouts."),
            ("ghl-crm-pipeline-setup", "GoHighLevel CRM Pipeline", "Lead stages from assessment → call → pilot → active → MRR."),
            ("ai-readiness-assessment-build", "AI Readiness Assessment Build", "Custom 12-question quiz with scoring and CTAs for your vertical."),
            ("post-assessment-email-nurture", "Post-Assessment Email Nurture", "5-email GHL sequence from score to urgency."),
        ],
    },
    {
        "slug": "vip-full-system",
        "name": "VIP Full System",
        "short": "VIP System",
        "blurb": "The complete Near Me OS deployment — protected territory, automation suite, and launch support.",
        "children": [
            ("protected-local-territory", "Protected Local Territory", "Exclusive county/metro rights — no other operator in your zone."),
            ("ghl-automation-suite", "GoHighLevel Automation Suite", "Booking SMS, operator pipeline, review funnels, retargeting sync."),
            ("cross-referral-engine", "Cross-Referral Engine", "AI consultants and directories route leads both ways with rev-share."),
            ("n8n-production-workflows", "n8n Production Workflows", "10+ tested workflows for booking, payouts, backlinks, and alerts."),
            ("client-deployment-dashboard", "Client Deployment Dashboard", "9-step onboarding tracker for every operator you bring on."),
            ("sales-frameworks-training", "Sales Frameworks & Training", "Scripts, objections, territory pitch deck, and demo flow."),
            ("platform-revenue-share", "Platform Revenue Share", "20–25% of leads and closed deals routed through the network."),
            ("monthly-flywheel-review", "Monthly Flywheel Review", "CAC, organic share, and branded search with budget guidance."),
            ("ninety-day-launch-support", "90-Day Launch Support", "Weekly check-ins through your first three territory sales."),
            ("end-to-end-market-ownership", "End-to-End Market Ownership", "Own acquisition, conversion, and monetization in one system."),
        ],
    },
    {
        "slug": "os-license-enterprise",
        "name": "OS License & Enterprise",
        "short": "OS License",
        "blurb": "White-label Near Me OS with state-level rights and multi-vertical deployment.",
        "children": [
            ("state-wide-territory-rights", "State-Wide Territory Rights", "Lock an entire state; county operators roll up under your license."),
            ("white-label-platform", "White-Label Platform", "Your brand and domain — Near Me OS runs invisibly underneath."),
            ("multi-vertical-deployment", "Multi-Vertical Deployment", "Launch maid, tech support, car rental, contractors under one license."),
            ("methodology-documentation", "Methodology Documentation", "Full playbook: flywheel, territory pricing, scripts, funnels."),
            ("vertical-builder-toolkit", "Vertical Builder Toolkit", "Templates, schema, n8n library, and landing components."),
            ("custom-ai-development-access", "Custom AI Development Access", "Workflows for pricing engines, demand forecasting, competitor monitoring."),
            ("priority-lead-routing", "Priority Lead Routing", "First pick on inbound network leads before standard consultants."),
            ("quarterly-strategy-sessions", "Quarterly Strategy Sessions", "90-minute deep dives on expansion and scaling triggers."),
            ("platform-level-rev-share", "Platform-Level Rev Share", "Earn on bookings across licensed territories and verticals."),
            ("enterprise-onboarding", "Enterprise Onboarding", "Dedicated cutover plan for multi-market operators."),
        ],
    },
    {
        "slug": "ai-consultant-network",
        "name": "AI Consultant Network",
        "short": "Track A",
        "blurb": "Get certified, claim a territory, and deliver AI automation to local businesses with our stack and lead engine.",
        "children": [
            ("ai-consultant-certification", "AI Consultant Certification", "Proven methodology, tools, and delivery standards."),
            ("protected-consultant-territory", "Protected Consultant Territory", "Local exclusivity so you are not competing with network peers."),
            ("lead-routing-crm-pipeline", "Lead Routing & CRM Pipeline", "Inbound leads staged and assigned through GoHighLevel."),
            ("n8n-ghl-tech-stack", "n8n + GoHighLevel Tech Stack", "Automation backbone for delivery and retention."),
            ("rev-share-closed-deals", "Rev-Share on Closed Deals", "Earn when the network closes work in your territory."),
            ("sales-training-frameworks", "Sales Training Frameworks", "Call scripts and objection handling for local AI offers."),
            ("local-business-ai-automation", "Local Business AI Automation", "High-ROI automations SMBs will actually buy."),
            ("assessment-to-pilot-funnel", "Assessment-to-Pilot Funnel", "From AI readiness score to paid pilot in a repeatable path."),
            ("consultant-community-support", "Consultant Community Support", "Peer playbooks and office hours as the network grows."),
            ("cross-referral-to-directories", "Cross-Referral to Directories", "Route directory-ready clients into Track B platforms."),
        ],
    },
    {
        "slug": "vertical-builder-services",
        "name": "Vertical Builder Services",
        "short": "Track B",
        "blurb": "Launch a Near Me directory in any vertical — we provide the OS, you own the market.",
        "children": [
            ("car-rental-near-me-vertical", "Car Rental Near Me Vertical", "Flagship Track B with embedded booking and territory licensing."),
            ("tech-support-near-me-vertical", "Tech Support Near Me Vertical", "MSP-style near-me markets proven on RaceCS and San Diego."),
            ("maid-services-near-me", "Maid Services Near Me", "Home-services directory pattern with recurring booking loops."),
            ("contractor-near-me-directory", "Contractor Near Me Directory", "Trade-focused directories with lead routing and profiles."),
            ("jersey-service-providers", "Jersey Service Providers", "Geo-first NJ directory model with tiered territory pricing."),
            ("turnkey-directory-platform", "Turnkey Directory Platform", "Ship a branded vertical without rebuilding the stack."),
            ("operator-self-serve-dashboards", "Operator Self-Serve Dashboards", "Providers manage profiles, calendars, and payouts themselves."),
            ("vertical-pricing-models", "Vertical Pricing Models", "Metro vs mid-tier vs rural licensing structures that sell."),
            ("booking-to-review-loops", "Booking-to-Review Loops", "Automations that turn completed jobs into reputation assets."),
            ("cross-referral-with-track-a", "Cross-Referral with Track A", "Consultants feed directories; directories feed consulting demand."),
        ],
    },
    {
        "slug": "ppc-to-seo-flywheel",
        "name": "PPC-to-SEO Flywheel",
        "short": "Flywheel",
        "blurb": "Every PPC dollar becomes a permanent SEO asset — competitors keep renting clicks; you own the moat.",
        "children": [
            ("rank-capture-distribute-loop", "Rank → Capture → Distribute Loop", "The five-step engine: Rank, Capture, Distribute, Monetize, Reinvest."),
            ("engagement-signal-compounding", "Engagement Signal Compounding", "On-domain booking behavior that Google rewards."),
            ("organic-share-growth", "Organic Share Growth", "Move from paid-heavy acquisition to 55%+ organic share models."),
            ("cac-reduction-playbook", "CAC Reduction Playbook", "Operate toward the 64% CAC reduction trajectory over 12 months."),
            ("branded-search-acceleration", "Branded Search Acceleration", "Grow branded queries as the market learns your platform."),
            ("reinvest-loop-budgeting", "Reinvest Loop Budgeting", "How revenue funds the next wave of PPC → SEO compounding."),
            ("flywheel-math-modeling", "Flywheel Math Modeling", "Without vs with models your buyers can compare on a call."),
            ("signal-quality-monitoring", "Signal Quality Monitoring", "Track dwell, booking starts, and bounce so the loop stays healthy."),
            ("competitor-rent-vs-own", "Competitor Rent vs Own", "Positioning that explains why paid-only rivals stay trapped."),
            ("compounding-asset-reporting", "Compounding Asset Reporting", "Monthly proof that ad spend is becoming equity."),
        ],
    },
    {
        "slug": "territory-licensing",
        "name": "Territory Licensing",
        "short": "Territories",
        "blurb": "License protected markets — county, metro, or state — with pricing that matches demand density.",
        "children": [
            ("county-metro-exclusivity", "County & Metro Exclusivity", "One operator per zone so licensees can invest with confidence."),
            ("tier-1-territory-pricing", "Tier 1 Territory Pricing", "Metro pricing models (e.g. $7K + $1,200/mo patterns) [confirm]."),
            ("mid-tier-rural-zones", "Mid-Tier & Rural Zones", "Accessible entry points that still protect density."),
            ("territory-sales-scripts", "Territory Sales Scripts", "Pitch language that sells exclusivity without overpromising."),
            ("operator-roll-up-structure", "Operator Roll-Up Structure", "How county licenses nest under state OS licenses."),
            ("license-agreement-framework", "License Agreement Framework", "Commercial terms outline for founding members [confirm legal]."),
            ("market-density-scoring", "Market Density Scoring", "Choose zones with enough search demand to fuel the flywheel."),
            ("multi-territory-expansion", "Multi-Territory Expansion", "Sequencing second and third markets after first proof."),
            ("territory-performance-kpis", "Territory Performance KPIs", "Bookings, organic share, and MRR that prove ownership."),
            ("founding-member-cohort", "Founding Member Cohort", "First-10 pricing windows for Platform and VIP tiers."),
        ],
    },
    {
        "slug": "market-automation-stack",
        "name": "Market Automation Stack",
        "short": "Automation",
        "blurb": "n8n, GoHighLevel, Stripe, and assessment funnels that run the market while you sell territories.",
        "children": [
            ("n8n-workflow-library", "n8n Workflow Library", "Reusable automations for booking, backlinks, payouts, and alerts."),
            ("gohighlevel-lifecycle-sms", "GoHighLevel Lifecycle SMS", "Five-message booking sequences that reduce no-shows."),
            ("review-request-automation", "Review Request Automation", "Post-job prompts that build Maps and platform reputation."),
            ("payout-trigger-workflows", "Payout Trigger Workflows", "Automated operator payouts tied to completed bookings."),
            ("lead-routing-rules", "Lead Routing Rules", "Territory-aware assignment so the right operator gets the lead."),
            ("retargeting-audience-sync", "Retargeting Audience Sync", "Push booking visitors into Meta and Google audiences."),
            ("pricing-engine-automations", "Pricing Engine Automations", "Dynamic or rules-based pricing hooks for demand spikes."),
            ("demand-forecasting-hooks", "Demand Forecasting Hooks", "Signal when to raise ad spend or open a new zone."),
            ("competitor-monitoring-alerts", "Competitor Monitoring Alerts", "Watch rival ads and ranking moves without manual checks."),
            ("supabase-data-schema", "Supabase Data Schema", "Vertical builder data model for profiles, bookings, and zones."),
        ],
    },
]

INDUSTRIES = [
    "Car Rental",
    "Tech Support / MSP",
    "Maid & Home Services",
    "Contractors & Trades",
    "Local Service Directories",
    "AI Consultants",
    "Multi-Location Operators",
    "Franchise Territories",
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
<div class="logo">Near Me <span>OS</span><small>Market Operating System</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Free AI Readiness Assessment — no obligation</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Solutions &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-near-me-os/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-near-me-os/index.html">About Near Me OS</a>
<a href="{p}about-near-me-os/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-near-me-os/verticals-we-serve/index.html">Verticals We Serve</a>
</div></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li><a href="{p}request-a-proposal/index.html">Apply / Proposal</a></li>
<li class="em"><a href="{p}ai-readiness-assessment/index.html">Free Assessment</a></li>
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
<li><a href="{p}about-near-me-os/index.html">About Near Me OS</a></li>
<li><a href="{p}about-near-me-os/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-near-me-os/verticals-we-serve/index.html">Verticals</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}ai-readiness-assessment/index.html">AI Readiness Assessment</a></li>
<li><a href="{p}request-a-proposal/index.html">Apply / Request Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul><li>{escape(ADDRESS)}</li><li>Operated by {escape(OPERATOR)}</li><li>Remote deployment nationwide</li></ul></div>
</div>
<div class="copy">Near Me OS &middot; {escape(OPERATOR)} &middot; {escape(HQ)} &middot; {escape(PHONE)}<br>
Copyright &copy; 2026. Near Me OS. All rights reserved.</div></div></footer>
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
<label>Ad Spend Capacity</label><select><option>Please choose&hellip;</option><option>$1,500+/month (required for flywheel tiers)</option><option>Under $1,500/month</option><option>Not sure yet</option></select>
<label>Interest</label><select><option>Please choose&hellip;</option>{opts}<option>AI Readiness Assessment</option><option>Founding Member / VIP</option><option>OS License</option><option>Other</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f95a8">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Near Me OS",
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
            "Near Me OS | Own Local Near Me Markets",
            "Near Me OS is the operating system for building, ranking, and monetizing local near-me markets — AI automation, territory licensing, and a PPC-to-SEO flywheel.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>Stop Selling Services. Start Owning Markets.</h1>
<p>{escape(TAGLINE)}</p>
<a class="btn" href="ai-readiness-assessment/index.html">Take the AI Readiness Assessment</a> <a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>9</b><span>Revenue Streams</span></div>
<div class="stat"><b>64%</b><span>CAC Reduction Model</span></div>
<div class="stat"><b>45%</b><span>Target Margins</span></div>
<div class="stat"><b>14</b><span>Weeks to Launch</span></div>
</div></div></section>
<section><div class="wrap"><h2>What can Near Me OS build for you?</h2>
<p class="lead">Ten solution families — from SEO/PPC layers through platform, VIP, OS license, Track A/B, flywheel, territories, and automation.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure which track fits? Start free.</h2>
<p style="margin-bottom:14px">The AI Readiness Assessment shows where you stand — then we map territory and tier.</p>
<a class="btn" href="ai-readiness-assessment/index.html">Take the Free Assessment</a></div></div>
<section><div class="wrap"><h2>How founding members get started</h2><div class="cols3">
<div class="card"><h3>1. Free AI Readiness Assessment</h3><p>Score gaps, capacity, and fit for Track A, Track B, or a stacked offer.</p></div>
<div class="card"><h3>2. Strategy call &amp; tier fit</h3><p>Confirm $1,500+/mo ad spend capacity, then choose SEO, PPC, Platform, VIP, or OS License.</p></div>
<div class="card"><h3>3. Deploy the flywheel</h3><p>Launch the directory or consultant territory and compound PPC into SEO equity.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why Near Me OS</h2><div class="cols3">
<div class="card"><h3>Proof, not promises</h3><p>Live deployments on RaceCS.net and San Diego Tech Support — methodology already ranking and generating revenue.</p></div>
<div class="card"><h3>PPC that becomes equity</h3><p>Competitors keep renting clicks. Your flywheel turns spend into organic share.</p></div>
<div class="card"><h3>Two tracks, one OS</h3><p>AI Consultant Network (Track A) and Vertical Builders (Track B) with cross-referral built in.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready to own your market?</h2>
<a class="btn" href="ai-readiness-assessment/index.html">AI Readiness Assessment</a> <a class="btn alt" href="request-a-proposal/index.html">Apply / Request Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    "What is Near Me OS?",
                    "Near Me OS is the operating system for building, ranking, and monetizing local near-me markets — with AI automation, territory licensing, and a compounding PPC-to-SEO flywheel.",
                ),
                (
                    "Who operates Near Me OS?",
                    f"Near Me OS is operated by {OPERATOR}, headquartered at {ADDRESS}.",
                ),
                (
                    "What is the AI Readiness Assessment?",
                    "A free assessment that scores where you stand, then routes you toward the right track and founding tier.",
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
            f"{h['name']} | Near Me OS",
            f"{h['name']} from Near Me OS — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} — From Near Me OS</h2>
<p class="lead">{escape(h["blurb"])} Delivered as part of the Near Me OS stack rather than an isolated task.</p>
<p><a class="btn" href="../ai-readiness-assessment/index.html">Take the AI Readiness Assessment</a> <a class="btn alt" href="../request-a-proposal/index.html">Apply / Request Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Solutions We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What Your Engagement Can Include</h2>
<ul class="checks">
<li>Scoped discovery tied to market demand and ad capacity</li>
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
                    "Begin with the free AI Readiness Assessment. We map track fit and provide a written proposal before work begins.",
                ),
                (
                    "Where is Near Me OS based?",
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
        head(f"{name} | Near Me OS", f"{name} from Near Me OS — {blurb}")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Rely on Near Me OS as your partner for {escape(name.lower())} and related market systems.</h2>
<p class="lead">{escape(blurb)} At Near Me OS, {escape(name.lower())} is delivered inside a compounding market OS — measured, automated, and pointed at ownership, not one-off billables.</p>
<p><a class="btn" href="../../ai-readiness-assessment/index.html">Take the AI Readiness Assessment</a> <a class="btn alt" href="../../request-a-proposal/index.html">Apply / Request Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(name)} Combined with Near Me OS Can Help You Gain:</h2>
<ul class="checks">
<li>Higher-intent near-me demand that lands on your platform</li>
<li>Lower CAC as organic share compounds against paid</li>
<li>Territory clarity so investment is protected</li>
<li>Automation that keeps operators and consultants fed</li>
<li>Reporting that proves the flywheel is working</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} engagement scoped to your market — not a one-size package</h2>
<p>No two markets need {escape(name.lower())} the same way. We design around your vertical, territory density, and ad capacity — then put scope and founding price in writing before work begins.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Operators avoid key risks by using a developed market OS for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with services-only approaches</h3><ul>
<li>PPC that never becomes an SEO asset</li>
<li>Directories with no booking or backlink loop</li>
<li>Territories sold without exclusivity or density math</li>
<li>Reporting that shows activity, not market ownership</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on Near Me OS</h3><ul>
<li>PPC-to-SEO flywheel operated as one system</li>
<li>Clear territory and licensing paths</li>
<li>Evidence-friendly flywheel reporting</li>
<li>Founding-member accountability with a named team</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>See where you stand first — free</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} would look like for your market? Start with the AI Readiness Assessment.</p>
<a class="btn" href="../../ai-readiness-assessment/index.html">Take the AI Readiness Assessment</a> <a class="btn alt" href="../../request-a-proposal/index.html">Apply / Request Proposal</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} shows results?",
                    "Timelines depend on vertical and ad capacity. Platform builds target a 14-week production path; your proposal includes an honest schedule.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Scope drives price. Founding tiers start at SEO/PPC layers ($997) through Platform, VIP, and OS License — confirmed after assessment.",
                ),
                (
                    f"Why choose Near Me OS for {name.lower()}?",
                    f"We deliver {name.lower()} inside a market OS — Race Computer Services accountability with a live proof stack.",
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
<h2 style="font-size:20px">Initiate a request with Near Me OS</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us your market</h3><p>Vertical, geography, and whether you lean Track A or Track B.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>An assessment, a tier recommendation, or honest advice — whichever fits.</p></div>
<div class="card"><h3>3. Decide with the full picture</h3><p>Plan and founding price in writing before you commit anything.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>Near Me OS</strong><br>Operated by {escape(OPERATOR)}<br>Headquarters: {escape(ADDRESS)}<br>Phone: {escape(PHONE)}<br>Email: {escape(EMAIL)}</p>
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
        ["/", "HOME", "", "near me os", "logo/home", "A1,A6,A10", ""],
        [
            "/about-near-me-os/",
            "COMP-HUB",
            "/",
            "about near me os",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-near-me-os/why-choose-us/",
            "COMP-CHILD",
            "/about-near-me-os/",
            "why choose near me os",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-near-me-os/verticals-we-serve/",
            "COMP-CHILD",
            "/about-near-me-os/",
            "near me verticals",
            "About menu",
            "D1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact near me os",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "near me os proposal",
            "nav utility",
            "I1",
            "Request for Proposal",
        ],
        [
            "/ai-readiness-assessment/",
            "FORM-CONSULT",
            "/",
            "ai readiness assessment",
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
    with (ROOT / "NEARMEOS-PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "nearmeos",  # keep marketing SPA landing
        "NEARMEOS-LANDING.md",
        "seocow-demo-site.zip",
        "NEARMEOS-QUESTIONNAIRE-ANSWERS.md",
        "NEARMEOS-PAGE-INVENTORY.csv",
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
        ROOT / "about-near-me-os" / "index.html",
        head(
            "About Near Me OS | Elizabeth, NJ",
            "Near Me OS is operated by Race Computer Services, LLC in Elizabeth, NJ.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About Near Me OS</h2>
<p class="lead">Near Me OS is the operating system for building, ranking, and monetizing local near-me markets — operated by {escape(OPERATOR)} from {escape(ADDRESS)}.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>We built Near Me OS because agencies keep selling hours while markets compound for the operators who own demand. The methodology is already live on RaceCS.net and San Diego Tech Support, with Track B verticals in production.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="verticals-we-serve/index.html">Verticals &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "Who operates Near Me OS?",
                    f"Near Me OS is operated by {OPERATOR}, headquartered at {ADDRESS}.",
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
    urls.append("/about-near-me-os/")

    write(
        ROOT / "about-near-me-os" / "why-choose-us" / "index.html",
        head("Why Choose Near Me OS", "Why operators choose Near Me OS to own local markets.")
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose Near Me OS</h2>
<p class="lead">A market OS built to help operators stop renting attention and start owning local demand.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Flywheel by design</h3><p>PPC, SEO, booking, and territory licensing operated as one compounding system.</p></div>
<div class="card"><h3>Proof assets live</h3><p>RaceCS.net and San Diego Tech Support already demonstrate the model.</p></div>
<div class="card"><h3>Two tracks</h3><p>AI Consultant Network and Vertical Builders with cross-referral.</p></div>
<div class="card"><h3>Assessment-led sales</h3><p>Free AI Readiness Assessment first; written scope before you commit.</p></div>
<div class="card"><h3>Founding economics</h3><p>First-10 pricing on Platform and VIP while the cohort fills.</p></div>
<div class="card"><h3>Elizabeth HQ</h3><p>Race Computer Services accountability with nationwide remote delivery.</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-near-me-os/why-choose-us/")

    ind = "".join(
        f'<div class="gcard"><h3>{escape(i)}</h3><p>Near Me OS patterns tuned to {escape(i.lower())} demand and booking loops.</p></div>'
        for i in INDUSTRIES
    )
    write(
        ROOT / "about-near-me-os" / "verticals-we-serve" / "index.html",
        head("Verticals We Serve | Near Me OS", "Vertical markets Near Me OS helps operators own.")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Verticals</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Verticals We Serve</h2>
<p class="lead">Directory and consultant deployments tailored to how each vertical buys and books.</p>
<div class="grid">{ind}</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-near-me-os/verticals-we-serve/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | Near Me OS",
            "Contact Us for Near Me OS Inquiries",
            "Tell us your vertical, geography, and whether you are exploring Track A, Track B, or a full OS license.",
        ),
        (
            "ai-readiness-assessment",
            "AI Readiness Assessment | Near Me OS",
            "Take the Free AI Readiness Assessment",
            "See where you stand — then book a strategy call to claim your territory.",
        ),
        (
            "request-a-proposal",
            "Apply / Request a Proposal | Near Me OS",
            "Apply or Request a Proposal",
            "Share your goals and ad capacity. We'll return a scoped founding proposal you can compare anywhere.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | Near Me OS", "Page not found.")
        + chrome(0)
        + """
<section style="padding:72px 0"><div class="wrap"><h2 style="font-size:28px">Page not found</h2>
<p class="lead">That URL isn't in this market. Try home or the AI Readiness Assessment.</p>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn alt" href="ai-readiness-assessment/index.html">Free Assessment</a></p>
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
        ROOT / "NEARMEOS-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — Near Me OS (FACTORY BUILD · Gate 1 10×10)

**Build uses NearMe OS Website Factory instructions-template (SEO Cow staging engine) · facts from product landing + Race Computer Services S1 · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | Near Me OS (operated by Race Computer Services, LLC) | product landing |
| A2 domain | nearmeos.io | product / DNS |
| A3 phone | {PHONE} | Race CS / SEO Cow S1 (same operator) |
| A4 email | {EMAIL} | [confirm] |
| A5 address | {ADDRESS} | Race CS / SEO Cow S1 |
| A6 trade | Local near-me market OS / territory licensing / AI automation | product landing |
| A7 founded | not stated — omitted | — |
| A10 value_proposition | Build, rank, and monetize local near-me markets with AI automation, territory licensing, and a compounding PPC-to-SEO flywheel | product landing |
| A11 tagline | {TAGLINE} | product landing |
| A12 competitor_type | agencies selling hours, paid-only media buyers, generic directory platforms | [confirm] |
| A13 hours | not stated — omitted | — |

## B — Services: 10 categories × 10 children (Gate 1 for ~100-page revision)
{hub_slugs} — full map in NEARMEOS-PAGE-INVENTORY.csv.
All Standard class → RFP booking (proposal), with FORM-CONSULT `ai-readiness-assessment` as the primary funnel entry.

## C–I
- C2 do_not_rank: n/a (market OS is the trade)
- D1 industries/verticals: Track B children + About > Verticals (car rental, tech support, maid, contractors, etc.)
- E1 platforms: OFF as separate PLAT area — Brilliant Directories / GHL / n8n / Stripe live as SVC-CHILDs
- F1 service_area: Elizabeth NJ HQ, nationwide remote
- F2/F3: no LOC pages (anti-doorway)
- G1/G2: proof assets named (RaceCS.net, San Diego Tech Support) — no invented testimonials
- I1 form_destination: OPEN — demo shells; assessment CTA adopted as FORM-CONSULT
- Budget qualification: $1,500+/month ad spend for flywheel tiers (product landing)

| Metric | Value |
|---|---|
| hubs | {len(HUBS)} |
| svc children | {svc_children} |
| staging | noindex + STAGING PREVIEW banner |
""",
    )

    pages = list(ROOT.rglob("index.html"))
    # exclude marketing spa under nearmeos/
    factory_pages = [p for p in pages if "nearmeos/" not in str(p).replace(str(ROOT) + "/", "")]
    print(f"Generated {len(factory_pages)} factory index pages")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)} · Children: {sum(len(h['children']) for h in HUBS)}")


if __name__ == "__main__":
    main()
