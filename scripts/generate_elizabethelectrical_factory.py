#!/usr/bin/env python3
"""Generate Elizabeth Electrical Services site using the NearMe OS Website Factory template
(same HTML/CSS engine as the SEO Cow / Car Rental Near Me staging builds).

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: local electrical contractor (Elizabeth NJ + surrounding areas).
Facts grounded from owner positioning + Race Computer Services S1 defaults [confirm].
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://elizabethelectricalservices.com"  # [confirm]
PHONE = "(862) 295-0011"
PHONE_TEL = "+18622950011"
EMAIL = "info@elizabethelectricalservices.com"  # [confirm]
HQ = "Elizabeth, NJ"
ADDRESS = "12 Sayre St, Elizabeth, NJ 07208"  # Race CS default [confirm]
OPERATOR = "Race Computer Services, LLC"  # operator default [confirm]
TAGLINE = "Your One-Stop Shop for Electrical Needs in Elizabeth, NJ"
STAGING_BANNER = (
    "STAGING PREVIEW — Elizabeth Electrical Services factory build · Elizabeth NJ · "
    "content pending owner review"
)

# NearMe factory CSS (SEO Cow template) with electric blue + amber accent remap
# (distinct from Trade OS amber/steel and car teal)
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#0f172a;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#1d4ed8;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#0f172a;color:#fde68a;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#1e3a5f;color:#dbeafe;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #f59e0b;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#0f172a}.logo span{color:#f59e0b}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#0f172a}
.phone-cta small{display:block;color:#5a6b7b;font-size:11px}
nav.nav{background:#0f172a}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#1e3a5f;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #f59e0b;z-index:60}
.dd a{color:#0f172a;padding:10px 15px;font-weight:500;border-bottom:1px solid #eff6ff}
.dd a:hover{background:#fffbeb}
.nav .em a{background:#f59e0b;color:#0f172a}.nav .em a:hover{background:#d97706;color:#fff}
.hero{background:linear-gradient(rgba(15,23,42,.88),rgba(30,58,95,.85)),repeating-linear-gradient(45deg,#1e3a5f 0 14px,#1d4ed8 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#fde68a;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#f59e0b;color:#0f172a;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#d97706;color:#fff;text-decoration:none}
.btn.alt{background:#1e3a5f;color:#fff}.btn.alt:hover{background:#0f172a}
section{padding:44px 0}
section.tint{background:#fffbeb}
section h2{font-size:25px;color:#0f172a;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#f59e0b;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #dbeafe;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(15,23,42,.06)}
.card h3{color:#0f172a;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #dbeafe;border-left:4px solid #f59e0b;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#0f172a}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#1d4ed8}
.ctastrip{background:#1e3a5f;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #dbeafe;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#eff6ff}.vs .col.good{background:#fffbeb}
.vs h3{font-size:16px;margin-bottom:12px;color:#0f172a}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#f59e0b;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #dbeafe;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#0f172a;list-style:none}
details summary:before{content:"+ ";color:#f59e0b;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #dbeafe;border-top:4px solid #f59e0b;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#44525f;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5a6b7b;padding:14px 0 0}
.crumb a{color:#5a6b7b}
footer{background:#0f172a;color:#c9b8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #1e3a5f;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #dbeafe;border-top:4px solid #f59e0b;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#0f172a}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #dbeafe;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(29,78,216,.08)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#0f172a}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#f59e0b;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#f59e0b;color:#0f172a;text-align:center;padding:32px 0}
.audit h2{color:#0f172a;margin-bottom:8px}.audit a.btn{background:#0f172a;color:#fff}
"""

# Gate 1 — 10 × 10 local electrical services (service children; no doorway LOC pages)
HUBS = [
    {
        "slug": "residential-electrical",
        "name": "Residential Electrical",
        "short": "Residential",
        "blurb": "Home wiring, upgrades, and safety work for Elizabeth NJ houses and surrounding neighborhoods.",
        "children": [
            ("home-wiring-installation", "Home Wiring Installation", "New and replacement wiring for Elizabeth-area homes."),
            ("kitchen-electrical-upgrades", "Kitchen Electrical Upgrades", "Circuits, outlets, and appliance feeds for remodeled kitchens."),
            ("bathroom-electrical-upgrades", "Bathroom Electrical Upgrades", "GFCI protection, lighting, and vent-fan circuits."),
            ("basement-electrical-wiring", "Basement Electrical Wiring", "Finished and unfinished basement power and lighting."),
            ("attic-electrical-work", "Attic Electrical Work", "Safe attic circuits, junction cleanup, and fixture feeds."),
            ("smoke-carbon-monoxide-detectors", "Smoke & CO Detector Wiring", "Hardwired detector installs and interconnects."),
            ("doorbell-transformer-wiring", "Doorbell & Transformer Wiring", "Traditional and smart doorbell power solutions."),
            ("home-electrical-safety-inspection", "Home Electrical Safety Inspection", "Panel, outlet, and grounding checks for older homes."),
            ("code-compliance-residential", "Residential Code Compliance", "Bring outdated residential work up to current code [confirm]."),
            ("new-home-electrical-rough-in", "New Home Electrical Rough-In", "Rough-in and trim for new construction and additions."),
        ],
    },
    {
        "slug": "commercial-electrical",
        "name": "Commercial Electrical",
        "short": "Commercial",
        "blurb": "Storefront, office, and light-industrial electrical for Elizabeth and the Newark corridor.",
        "children": [
            ("retail-storefront-electrical", "Retail Storefront Electrical", "Lighting, signage feeds, and tenant fit-out power."),
            ("office-suite-electrical", "Office Suite Electrical", "Workstations, conference rooms, and shared-space circuits."),
            ("warehouse-shop-power", "Warehouse & Shop Power", "Equipment circuits and shop lighting for light industrial."),
            ("restaurant-kitchen-electrical", "Restaurant Kitchen Electrical", "Appliance circuits and grease-hood related electrical [confirm]."),
            ("tenant-fit-out-electrical", "Tenant Fit-Out Electrical", "Build-outs timed to lease and inspection schedules."),
            ("commercial-lighting-retrofit", "Commercial Lighting Retrofit", "LED upgrades that cut energy and maintenance."),
            ("three-phase-power-service", "Three-Phase Power Service", "Three-phase installs and troubleshooting where available."),
            ("commercial-panel-maintenance", "Commercial Panel Maintenance", "Panel labeling, torque checks, and capacity reviews."),
            ("signage-and-exterior-power", "Signage & Exterior Power", "Building signs, parking lights, and outdoor receptacles."),
            ("small-business-electrical-upgrades", "Small Business Electrical Upgrades", "Practical upgrades for Union County small businesses."),
        ],
    },
    {
        "slug": "panel-service-upgrades",
        "name": "Panel & Service Upgrades",
        "short": "Panels",
        "blurb": "Service upgrades, panel replacements, and capacity work for growing electrical loads.",
        "children": [
            ("electrical-panel-replacement", "Electrical Panel Replacement", "Swap outdated or unsafe panels for modern load centers."),
            ("100-amp-to-200-amp-upgrade", "100-Amp to 200-Amp Upgrade", "Common service upgrade for homes adding major loads."),
            ("main-breaker-replacement", "Main Breaker Replacement", "Replace failing main breakers and related hardware."),
            ("subpanel-installation", "Subpanel Installation", "Add a subpanel for garages, additions, or workshops."),
            ("federal-pacific-panel-replacement", "Federal Pacific Panel Replacement", "Priority replacement for known problem panel types."),
            ("zinsco-panel-replacement", "Zinsco Panel Replacement", "Replace Zinsco/Sylvania panels with safer equipment."),
            ("meter-socket-upgrade", "Meter Socket Upgrade", "Meter base and related service-entrance updates [confirm utility]."),
            ("circuit-breaker-upgrades", "Circuit Breaker Upgrades", "AFCI/GFCI breaker installs and circuit labeling."),
            ("load-calculation-service", "Load Calculation Service", "Capacity math before EV, HVAC, or generator adds."),
            ("service-entrance-cable-upgrade", "Service Entrance Cable Upgrade", "Replace undersized or damaged service conductors."),
        ],
    },
    {
        "slug": "lighting-installation",
        "name": "Lighting Installation",
        "short": "Lighting",
        "blurb": "Interior and exterior lighting installs that improve safety, comfort, and curb appeal.",
        "children": [
            ("recessed-lighting-installation", "Recessed Lighting Installation", "Can lights for kitchens, living rooms, and basements."),
            ("led-lighting-conversion", "LED Lighting Conversion", "Swap inefficient fixtures for LED without a full remodel."),
            ("outdoor-landscape-lighting", "Outdoor Landscape Lighting", "Path, accent, and yard lighting for evening safety."),
            ("security-lighting-installation", "Security Lighting Installation", "Motion and flood lighting for driveways and yards."),
            ("under-cabinet-kitchen-lighting", "Under-Cabinet Kitchen Lighting", "Task lighting that makes counters usable."),
            ("chandelier-pendant-hanging", "Chandelier & Pendant Hanging", "Safe mounting and box reinforcement for heavy fixtures."),
            ("dimmer-switch-lighting-control", "Dimmer & Lighting Control", "Dimmers and multi-location lighting controls."),
            ("garage-workshop-lighting", "Garage & Workshop Lighting", "Bright, even light for workbenches and parking."),
            ("porch-entryway-lighting", "Porch & Entryway Lighting", "Welcoming, code-aware entry lighting."),
            ("commercial-interior-lighting", "Commercial Interior Lighting", "Office and retail lighting layouts that look professional."),
        ],
    },
    {
        "slug": "outlets-switches",
        "name": "Outlets & Switches",
        "short": "Outlets",
        "blurb": "Outlet and switch work for convenience, code compliance, and everyday reliability.",
        "children": [
            ("gfci-outlet-installation", "GFCI Outlet Installation", "Kitchen, bath, garage, and outdoor GFCI protection."),
            ("usb-outlet-installation", "USB Outlet Installation", "Built-in USB charging at desks and nightstands."),
            ("dedicated-appliance-circuits", "Dedicated Appliance Circuits", "Separate circuits for microwaves, freezers, and more."),
            ("outdoor-weatherproof-outlets", "Outdoor Weatherproof Outlets", "In-use covers and outdoor receptacles for yards."),
            ("three-way-switch-installation", "Three-Way Switch Installation", "Control lights from two locations — stairs and hallways."),
            ("smart-switch-installation", "Smart Switch Installation", "Wi-Fi and app-controlled switches wired correctly."),
            ("outlet-relocation-addition", "Outlet Relocation & Addition", "Add or move receptacles during furniture or remodel changes."),
            ("tamper-resistant-outlet-upgrade", "Tamper-Resistant Outlet Upgrade", "Child-safer receptacles for family homes."),
            ("floor-outlet-installation", "Floor Outlet Installation", "Power in open floor plans and island seating areas."),
            ("switch-plate-dimmer-upgrades", "Switch Plate & Dimmer Upgrades", "Cleaner controls and modern wall plates."),
        ],
    },
    {
        "slug": "ceiling-fans-fixtures",
        "name": "Ceiling Fans & Fixtures",
        "short": "Fans",
        "blurb": "Ceiling fans, fixture swaps, and mounting work done safely and level.",
        "children": [
            ("ceiling-fan-installation", "Ceiling Fan Installation", "New fans with proper bracing and rated boxes."),
            ("ceiling-fan-replacement", "Ceiling Fan Replacement", "Swap old fans for quieter, more efficient models."),
            ("fan-rated-box-upgrade", "Fan-Rated Box Upgrade", "Reinforce boxes so fans stay secure."),
            ("remote-control-fan-wiring", "Remote Control Fan Wiring", "Receiver installs and wall-control options."),
            ("light-fixture-replacement", "Light Fixture Replacement", "Update dated fixtures throughout the home."),
            ("flush-mount-fixture-install", "Flush-Mount Fixture Install", "Low-profile fixtures for smaller rooms and hallways."),
            ("bathroom-vanity-light-install", "Bathroom Vanity Light Install", "Even vanity lighting for mirrors and grooming."),
            ("dining-room-fixture-hanging", "Dining Room Fixture Hanging", "Centered, securely hung dining fixtures."),
            ("garage-shop-fan-install", "Garage & Shop Fan Install", "Air movement for unfinished and shop spaces."),
            ("outdoor-ceiling-fan-install", "Outdoor Ceiling Fan Install", "Damp/wet-rated fans for porches and patios."),
        ],
    },
    {
        "slug": "electrical-repairs",
        "name": "Electrical Repairs & Troubleshooting",
        "short": "Repairs",
        "blurb": "Diagnose and fix flickering lights, dead outlets, breaker trips, and mystery electrical issues.",
        "children": [
            ("breaker-trip-troubleshooting", "Breaker Trip Troubleshooting", "Find why a breaker keeps tripping and fix the cause."),
            ("flickering-lights-repair", "Flickering Lights Repair", "Track loose connections, bad dimmers, and load issues."),
            ("dead-outlet-repair", "Dead Outlet Repair", "Restore power to outlets that stopped working."),
            ("burning-smell-electrical-check", "Burning Smell Electrical Check", "Urgent inspection when you smell hot wiring."),
            ("aluminum-wiring-remediation", "Aluminum Wiring Remediation", "COPALUM/AlumiConn-style remediation options [confirm]."),
            ("grounding-bonding-repairs", "Grounding & Bonding Repairs", "Correct grounding and bonding for safer systems."),
            ("junction-box-repairs", "Junction Box Repairs", "Cover open splices and overcrowded boxes."),
            ("knob-and-tube-assessment", "Knob-and-Tube Assessment", "Evaluate remaining K&T and plan safe upgrades."),
            ("power-surge-damage-assessment", "Power Surge Damage Assessment", "Inspect after storms or utility surges."),
            ("electrical-noise-interference-fix", "Electrical Noise / Interference Fix", "Track nuisance trips and odd appliance behavior."),
        ],
    },
    {
        "slug": "ev-charger-installation",
        "name": "EV Charger Installation",
        "short": "EV Chargers",
        "blurb": "Level 2 home and small-business EV charger installs with panel capacity in mind.",
        "children": [
            ("level-2-home-ev-charger", "Level 2 Home EV Charger", "240V charger installs for overnight home charging."),
            ("garage-ev-charger-install", "Garage EV Charger Install", "Wall-mount chargers in attached or detached garages."),
            ("driveway-ev-charger-install", "Driveway EV Charger Install", "Exterior charger mounts with weatherproofing."),
            ("tesla-wall-connector-install", "Tesla Wall Connector Install", "Tesla-compatible Wall Connector wiring and mount."),
            ("universal-evse-install", "Universal EVSE Install", "J1772 and other universal Level 2 EVSE units."),
            ("ev-charger-circuit-run", "EV Charger Circuit Run", "Dedicated circuit from panel to charger location."),
            ("panel-upgrade-for-ev", "Panel Upgrade for EV", "Service/panel work when the existing panel cannot support EV loads."),
            ("dual-ev-charger-prep", "Dual EV Charger Prep", "Load management and prep for two vehicles."),
            ("condo-hoa-ev-charger-consult", "Condo / HOA EV Charger Consult", "Guidance for shared parking and approval paths [confirm]."),
            ("commercial-workplace-ev-charging", "Workplace EV Charging", "Small-lot charger installs for local employers."),
        ],
    },
    {
        "slug": "generator-installation",
        "name": "Generator Installation",
        "short": "Generators",
        "blurb": "Standby and portable generator transfer solutions for storm readiness in Union County.",
        "children": [
            ("standby-generator-installation", "Standby Generator Installation", "Whole-home standby generator wiring and transfer setup."),
            ("automatic-transfer-switch", "Automatic Transfer Switch", "ATS installs so standby power switches cleanly."),
            ("manual-transfer-switch", "Manual Transfer Switch", "Manual transfer for portable generator use."),
            ("portable-generator-interlock", "Portable Generator Interlock", "Interlock kits that keep utility and generator isolated."),
            ("generator-subpanel-critical-loads", "Critical Loads Subpanel", "Power essentials without sizing for the whole house."),
            ("generator-pad-and-wiring", "Generator Pad & Wiring", "Conduit, conductors, and pad-adjacent electrical work."),
            ("generator-maintenance-electrical", "Generator Electrical Maintenance", "Transfer switch checks and connection inspections."),
            ("natural-gas-generator-hookup-electrical", "Natural Gas Generator Electrical", "Electrical side of gas-fueled standby installs [confirm gas partner]."),
            ("propane-generator-electrical", "Propane Generator Electrical", "Electrical work for propane standby systems."),
            ("storm-preparedness-generator-plan", "Storm Preparedness Generator Plan", "Size and circuit planning before the next outage."),
        ],
    },
    {
        "slug": "emergency-electrical",
        "name": "Emergency Electrical Services",
        "short": "Emergency",
        "blurb": "Urgent electrical help for outages, hazards, and after-hours problems in Elizabeth and nearby towns.",
        "children": [
            ("no-power-emergency-call", "No Power Emergency Call", "Diagnose whole-house or partial outages fast."),
            ("sparking-outlet-emergency", "Sparking Outlet Emergency", "Shut down and repair hazardous outlets."),
            ("burning-panel-emergency", "Burning Panel Emergency", "Urgent panel inspection when heat or odor appears."),
            ("storm-damage-electrical", "Storm Damage Electrical", "Post-storm repairs for damaged service and wiring."),
            ("water-damage-electrical-safety", "Water Damage Electrical Safety", "Make-safe after leaks, floods, or appliance failures."),
            ("exposed-wiring-make-safe", "Exposed Wiring Make-Safe", "Immediate covering and isolation of open conductors."),
            ("after-hours-electrician", "After-Hours Electrician", "After-hours response when waiting until morning is not safe [confirm]."),
            ("landlord-tenant-electrical-emergency", "Landlord / Tenant Electrical Emergency", "Urgent make-safe for rental properties."),
            ("commercial-emergency-electrical", "Commercial Emergency Electrical", "Keep a storefront or office safe after an electrical failure."),
            ("temporary-power-restoration", "Temporary Power Restoration", "Safe temporary power while permanent repairs are planned."),
        ],
    },
]

SERVICE_AREAS = [
    "Elizabeth, NJ",
    "Union County",
    "Hillside",
    "Roselle / Roselle Park",
    "Linden",
    "Rahway",
    "Cranford",
    "Westfield",
    "Newark corridor",
    "Surrounding communities",
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
<div class="logo">Elizabeth <span>Electrical</span><small>Elizabeth, NJ &amp; Surrounding Areas</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Free electrical quote — no obligation</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-elizabeth-electrical-services/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-elizabeth-electrical-services/index.html">About Elizabeth Electrical Services</a>
<a href="{p}about-elizabeth-electrical-services/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-elizabeth-electrical-services/service-areas/index.html">Service Areas</a>
</div></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li class="em"><a href="{p}request-a-quote/index.html">Request a Quote</a></li>
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
<li><a href="{p}about-elizabeth-electrical-services/index.html">About Elizabeth Electrical Services</a></li>
<li><a href="{p}about-elizabeth-electrical-services/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-elizabeth-electrical-services/service-areas/index.html">Service Areas</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}request-a-quote/index.html">Request a Quote</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul><li>{escape(ADDRESS)} <em style="font-size:11px">[confirm]</em></li><li>Operated by {escape(OPERATOR)} <em style="font-size:11px">[confirm]</em></li><li>Elizabeth, NJ &amp; surrounding areas</li></ul></div>
</div>
<div class="copy">Elizabeth Electrical Services &middot; {escape(OPERATOR)} &middot; {escape(HQ)} &middot; {escape(PHONE)}<br>
Copyright &copy; 2026. Elizabeth Electrical Services. All rights reserved.</div></div></footer>
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
<label>Property Type</label><select><option>Please choose&hellip;</option><option>Residential</option><option>Commercial</option><option>Multi-family / Rental</option><option>Not sure</option></select>
<label>Service Needed</label><select><option>Please choose&hellip;</option>{opts}<option>Emergency Electrical</option><option>Other</option></select>
<label>Project Details / Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f95a8">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Electrician",
        "name": "Elizabeth Electrical Services",
        "legalName": OPERATOR,  # [confirm]
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "areaServed": "Elizabeth, NJ and surrounding areas",
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
            f'<a href="{h["slug"]}/index.html" style="font:600 13px \'Segoe UI\',sans-serif">All {escape(h["short"]).lower()} services &rarr;</a></div>'
        )
    return (
        head(
            "Elizabeth Electrical Services | Electrician in Elizabeth, NJ",
            "Elizabeth Electrical Services is your one-stop shop for electrical needs in Elizabeth NJ and the surrounding areas — residential, commercial, panels, EV, generators, and more.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>Elizabeth Electrical Services</h1>
<p>Your one stop shop for your electrical needs in Elizabeth NJ and the surrounding areas.</p>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>Local</b><span>Elizabeth, NJ</span></div>
<div class="stat"><b>One-Stop</b><span>Full Electrical</span></div>
<div class="stat"><b>Licensed</b><span>&amp; Insured [confirm]</span></div>
<div class="stat"><b>Nearby</b><span>Surrounding Areas</span></div>
</div></div></section>
<section><div class="wrap"><h2>What can Elizabeth Electrical Services do for you?</h2>
<p class="lead">Ten service families — from residential and commercial work through panels, lighting, outlets, fans, repairs, EV chargers, generators, and emergency electrical.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure where to start? Request a free quote.</h2>
<p style="margin-bottom:14px">Tell us about the job — we will recommend the right path for your home or business.</p>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a></div></div>
<section><div class="wrap"><h2>How we get started</h2><div class="cols3">
<div class="card"><h3>1. Request a quote</h3><p>Share the address, symptoms, or project goals for Elizabeth NJ or nearby towns.</p></div>
<div class="card"><h3>2. Clear scope &amp; options</h3><p>We outline the work, materials, and any panel or permit considerations [confirm].</p></div>
<div class="card"><h3>3. Schedule the job</h3><p>Book the install or repair with one accountable electrical team.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why Elizabeth Electrical Services</h2><div class="cols3">
<div class="card"><h3>One-stop electrical</h3><p>Wiring, panels, lighting, EV, generators, and emergencies under one roof.</p></div>
<div class="card"><h3>Elizabeth + nearby</h3><p>Focused on Elizabeth, NJ and the surrounding Union County communities.</p></div>
<div class="card"><h3>Straightforward process</h3><p>Quote first, clear scope, then schedule — no runaround.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready for safer, cleaner electrical work?</h2>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    "What is Elizabeth Electrical Services?",
                    "Elizabeth Electrical Services is a local electrical contractor focused on Elizabeth, NJ and surrounding areas — a one-stop shop for residential and commercial electrical needs.",
                ),
                (
                    "Who operates Elizabeth Electrical Services?",
                    f"Staging build lists operation by {OPERATOR} from {ADDRESS} [confirm]. Final ownership and NAP pending owner review.",
                ),
                (
                    "What areas do you serve?",
                    "Elizabeth, NJ and surrounding areas including communities across Union County and the nearby Newark corridor. Exact coverage confirmed at quote time.",
                ),
                (
                    "Are you licensed and insured?",
                    "Licensed and insured [confirm] — credentials will be verified with the owner before go-live.",
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
            f"{h['name']} | Elizabeth Electrical Services",
            f"{h['name']} from Elizabeth Electrical Services in Elizabeth, NJ — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} — Elizabeth Electrical Services</h2>
<p class="lead">{escape(h["blurb"])} Part of our one-stop electrical offering for Elizabeth NJ and surrounding areas.</p>
<p><a class="btn" href="../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Services We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What Your Job Can Include</h2>
<ul class="checks">
<li>On-site assessment for Elizabeth NJ and nearby communities</li>
<li>Clear scope for materials, labor, and any panel capacity needs</li>
<li>Code-aware workmanship with licensed &amp; insured crews [confirm]</li>
<li>Coordination for permits or inspections when required [confirm]</li>
<li>One accountable electrician — not a stack of disconnected subcontractors</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with a free quote. We confirm scope and provide clear next steps before work begins.",
                ),
                (
                    "Where is Elizabeth Electrical Services based?",
                    f"Headquartered in {HQ} ({ADDRESS}) [confirm], serving Elizabeth and surrounding areas.",
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
        head(
            f"{name} | Elizabeth Electrical Services",
            f"{name} from Elizabeth Electrical Services in Elizabeth, NJ — {blurb}",
        )
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Rely on Elizabeth Electrical Services for {escape(name.lower())} in Elizabeth NJ and nearby towns.</h2>
<p class="lead">{escape(blurb)} As your local one-stop electrical shop, we deliver {escape(name.lower())} with clear quotes and dependable follow-through.</p>
<p><a class="btn" href="../../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(name)} with Elizabeth Electrical Services Helps You Gain:</h2>
<ul class="checks">
<li>Safer, code-aware electrical work for homes and businesses</li>
<li>A single local team for related electrical needs</li>
<li>Straightforward pricing before work begins</li>
<li>Support across Elizabeth, Union County, and surrounding areas</li>
<li>Follow-through from diagnosis through final cleanup</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} plan scoped to your property — not a one-size package</h2>
<p>Every home and storefront has different panels, loads, and access. We match {escape(name.lower())} to your building, then confirm materials and timeline before we start.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Homeowners and businesses avoid key risks with a developed plan for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common problems with patchwork electrical work</h3><ul>
<li>Temporary fixes that trip breakers again next week</li>
<li>Unclear pricing until the job is half done</li>
<li>Panels that cannot support new loads (EV, HVAC, generators)</li>
<li>No single accountable electrician for follow-up</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on Elizabeth Electrical Services</h3><ul>
<li>Root-cause diagnosis before parts go in</li>
<li>Written quote path for residential and commercial jobs</li>
<li>Capacity planning when upgrades are needed</li>
<li>Local Elizabeth NJ accountability with surrounding-area coverage</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Get a clear answer first — free quote</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} looks like for your property? Start with a free quote.</p>
<a class="btn" href="../../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} is completed?",
                    "Timelines depend on scope, parts, and any panel or permit needs. Many outlet, switch, and fixture jobs are same-day or next-visit; larger upgrades are scheduled after assessment.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Price depends on materials, access, and existing panel capacity. We quote before work begins.",
                ),
                (
                    f"Why choose Elizabeth Electrical Services for {name.lower()}?",
                    f"We deliver {name.lower()} as part of a one-stop electrical offering for Elizabeth NJ and surrounding areas — clear quotes and local follow-through.",
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
<h2 style="font-size:20px">Initiate a request with Elizabeth Electrical Services</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us the job</h3><p>Address in Elizabeth NJ or nearby, symptoms, and photos if you have them.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>A quote, a proposal, or honest advice on whether a panel upgrade is needed first.</p></div>
<div class="card"><h3>3. Schedule the work</h3><p>Confirm timing and scope in writing before tools come out.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>Elizabeth Electrical Services</strong><br>Operated by {escape(OPERATOR)} <em>[confirm]</em><br>Headquarters: {escape(ADDRESS)} <em>[confirm]</em><br>Phone: {escape(PHONE)}<br>Email: {escape(EMAIL)} <em>[confirm]</em></p>
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
        ["/", "HOME", "", "elizabeth electrical services", "logo/home", "A1,A6,A10", ""],
        [
            "/about-elizabeth-electrical-services/",
            "COMP-HUB",
            "/",
            "about elizabeth electrical services",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-elizabeth-electrical-services/why-choose-us/",
            "COMP-CHILD",
            "/about-elizabeth-electrical-services/",
            "why choose elizabeth electrical services",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-elizabeth-electrical-services/service-areas/",
            "COMP-CHILD",
            "/about-elizabeth-electrical-services/",
            "elizabeth nj electrical service areas",
            "About menu",
            "F1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact elizabeth electrical services",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "electrical proposal elizabeth nj",
            "nav utility",
            "I1",
            "Request for Proposal",
        ],
        [
            "/request-a-quote/",
            "FORM-CONSULT",
            "/",
            "electrical quote elizabeth nj",
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
    with (ROOT / "ELIZABETHELECTRICAL-PAGE-INVENTORY.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
        "seocow-demo-site.zip",
        "ELIZABETHELECTRICAL-QUESTIONNAIRE-ANSWERS.md",
        "ELIZABETHELECTRICAL-PAGE-INVENTORY.csv",
        "ELIZABETHELECTRICAL-NOTES.md",
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
        ROOT / "about-elizabeth-electrical-services" / "index.html",
        head(
            "About Elizabeth Electrical Services | Elizabeth, NJ",
            "Elizabeth Electrical Services is your one-stop shop for electrical needs in Elizabeth, NJ and surrounding areas.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About Elizabeth Electrical Services</h2>
<p class="lead">Elizabeth Electrical Services is a local electrical contractor serving Elizabeth, NJ and the surrounding areas — your one-stop shop for residential and commercial electrical needs.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>We help homeowners and businesses with wiring, panels, lighting, outlets, fans, repairs, EV chargers, generators, and emergency electrical work. Staging NAP lists {escape(ADDRESS)} and operation by {escape(OPERATOR)} <em>[confirm]</em>.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="service-areas/index.html">Service areas &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "Who operates Elizabeth Electrical Services?",
                    f"Staging build lists {OPERATOR} at {ADDRESS} [confirm]. Final ownership pending owner review.",
                ),
                (
                    "Do you work outside Elizabeth?",
                    "Yes — surrounding areas across Union County and the nearby Newark corridor, confirmed at quote time.",
                ),
            ]
        )
        + org_schema()
        + footer(1),
    )
    urls.append("/about-elizabeth-electrical-services/")

    write(
        ROOT / "about-elizabeth-electrical-services" / "why-choose-us" / "index.html",
        head(
            "Why Choose Elizabeth Electrical Services",
            "Why homeowners and businesses choose Elizabeth Electrical Services in Elizabeth, NJ.",
        )
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose Elizabeth Electrical Services</h2>
<p class="lead">A local one-stop electrical shop built for Elizabeth NJ homes and businesses — clear quotes, safer work, and follow-through.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>One-stop shop</h3><p>From outlets and lighting to panels, EV chargers, and generators.</p></div>
<div class="card"><h3>Local focus</h3><p>Elizabeth, NJ and surrounding Union County communities.</p></div>
<div class="card"><h3>Licensed &amp; insured</h3><p>Credentials marked [confirm] until owner verification at go-live.</p></div>
<div class="card"><h3>Quote-led process</h3><p>Request a quote first; written scope before work begins.</p></div>
<div class="card"><h3>Residential + commercial</h3><p>Homes, storefronts, offices, and light industrial spaces.</p></div>
<div class="card"><h3>Emergency-aware</h3><p>Urgent electrical make-safe when waiting is not an option [confirm hours].</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-elizabeth-electrical-services/why-choose-us/")

    areas = "".join(
        f'<div class="gcard"><h3>{escape(a)}</h3><p>Electrical service coverage discussed at quote time for {escape(a)}.</p></div>'
        for a in SERVICE_AREAS
    )
    write(
        ROOT / "about-elizabeth-electrical-services" / "service-areas" / "index.html",
        head(
            "Service Areas | Elizabeth Electrical Services",
            "Elizabeth Electrical Services covers Elizabeth, NJ and surrounding areas across Union County.",
        )
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Service Areas</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Service Areas</h2>
<p class="lead">Based in Elizabeth, NJ — serving surrounding communities. Exact travel radius confirmed when you request a quote. No doorway city landing pages in this Gate 1 build.</p>
<div class="grid">{areas}</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-elizabeth-electrical-services/service-areas/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | Elizabeth Electrical Services",
            "Contact Us for Elizabeth Electrical Services Inquiries",
            "Tell us your address, the electrical issue or project, and the best time to reach you.",
        ),
        (
            "request-a-quote",
            "Request a Quote | Elizabeth Electrical Services",
            "Request a Free Electrical Quote",
            "See scope and next steps for residential or commercial electrical work in Elizabeth NJ and surrounding areas.",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | Elizabeth Electrical Services",
            "Request a Proposal",
            "Share larger project goals — panel upgrades, multi-unit work, EV or generator installs — and we will return a scoped proposal.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | Elizabeth Electrical Services", "Page not found.")
        + chrome(0)
        + """
<section style="padding:72px 0"><div class="wrap"><h2 style="font-size:28px">Page not found</h2>
<p class="lead">That URL is not on this site. Try home or request a quote.</p>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn alt" href="request-a-quote/index.html">Request a Quote</a></p>
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
        ROOT / "ELIZABETHELECTRICAL-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — Elizabeth Electrical Services (FACTORY BUILD · Gate 1 10×10)

**Build uses NearMe OS Website Factory instructions-template (SEO Cow staging engine) · category: local electrical contractor · facts from owner positioning + Race CS S1 defaults · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | Elizabeth Electrical Services | owner positioning |
| A2 domain | elizabethelectricalservices.com | [confirm] |
| A3 phone | {PHONE} | Race CS / SEO Cow S1 (same operator default) |
| A4 email | {EMAIL} | [confirm] |
| A5 address | {ADDRESS} | Race CS default [confirm] |
| A6 trade | Local electrical contractor (residential + commercial) | owner |
| A7 founded | not stated — omitted | — |
| A10 value_proposition | Your one stop shop for electrical needs in Elizabeth NJ and the surrounding areas | owner |
| A11 tagline | {TAGLINE} | this build |
| A12 competitor_type | national home-services brands, local electrician shops | [confirm] |
| A13 hours | not stated — omitted / emergency hours [confirm] | — |
| Operator note | Operated by {OPERATOR} | Race CS default [confirm] — omit if awkward at go-live |

## B — Services: 10 categories × 10 children
{hub_slugs} — full map in ELIZABETHELECTRICAL-PAGE-INVENTORY.csv.
FORM-CONSULT = `request-a-quote` · FORM-PRICING = `request-a-proposal`.

## C–I
- D1 audiences: homeowners, landlords, small commercial, property managers
- F1 service_area: Elizabeth NJ + surrounding Union County / Newark corridor (service-areas page; no LOC doorway pages)
- F2/F3: no LOC doorway pages in this build
- I1 form_destination: OPEN — demo shells
- Licensed & insured: stated as [confirm]
- Staging: noindex + STAGING PREVIEW banner

| Metric | Value |
|---|---|
| hubs | {len(HUBS)} |
| svc children | {svc_children} |
| staging | noindex + STAGING PREVIEW banner |
""",
    )

    write(
        ROOT / "ELIZABETHELECTRICAL-NOTES.md",
        """# Elizabeth Electrical Services — Factory Build

Category: **local electrical contractor** (Elizabeth, NJ + surrounding areas).

- Positioning: “Your one stop shop for your electrical needs in Elizabeth NJ and the surrounding areas.”
- Generator: `scripts/generate_elizabethelectrical_factory.py`
- Gate 1: 10 × 10 = 100 SVC-CHILD (+ chrome ≈ 117 pages)
- FORM-CONSULT: `/request-a-quote/` (highlighted)
- FORM-PRICING: `/request-a-proposal/`
- About: `/about-elizabeth-electrical-services/` (+ why-choose-us, service-areas)
- Domain / email / NAP / operator / licensed-insured: marked **[confirm]**
- No invented testimonials or license numbers
- No doorway LOC city pages — geographic mentions stay in service copy + service-areas
- Visual: electric blue (#1d4ed8 / #1e3a5f / #0f172a) + amber accent (#f59e0b)
""",
    )

    factory_pages = list(ROOT.rglob("index.html"))
    print(f"Generated {len(factory_pages)} factory index pages")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)} · Children: {sum(len(h['children']) for h in HUBS)}")


if __name__ == "__main__":
    main()
