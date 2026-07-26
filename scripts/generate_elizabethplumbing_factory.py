#!/usr/bin/env python3
"""Generate The Elizabeth Plumbing Stop site using the NearMe OS Website Factory template
(same HTML/CSS engine as the SEO Cow / Car Rental Near Me staging builds).

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: plumbing & drain services (Elizabeth, NJ local trade).
Facts grounded from Race Computer Services S1 defaults · [confirm] = needs owner verification.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://elizabethplumbingstop.com"  # [confirm]
PHONE = "(862) 295-0011"
PHONE_TEL = "+18622950011"
EMAIL = "info@elizabethplumbingstop.com"  # [confirm]
HQ = "Elizabeth, NJ"
ADDRESS = "12 Sayre St, Elizabeth, NJ 07208"  # Race CS default [confirm]
OPERATOR = "Race Computer Services, LLC"  # [confirm]
TAGLINE = "Your One-Stop Shop for Plumbing & Drain Services in Elizabeth, NJ"
STAGING_BANNER = (
    "STAGING PREVIEW — The Elizabeth Plumbing Stop factory build · Elizabeth NJ · "
    "content pending owner review"
)

# NearMe factory CSS (SEO Cow template) with water-blue / slate remap
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#0c4a6e;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#0369a1;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#082f49;color:#bae6fd;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#0c4a6e;color:#e0f2fe;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #0284c7;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#0c4a6e}.logo span{color:#0284c7}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#0c4a6e}
.phone-cta small{display:block;color:#5a6b7b;font-size:11px}
nav.nav{background:#0c4a6e}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#082f49;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #0284c7;z-index:60}
.dd a{color:#0c4a6e;padding:10px 15px;font-weight:500;border-bottom:1px solid #bae6fd}
.dd a:hover{background:#f0f9ff}
.nav .em a{background:#0369a1}.nav .em a:hover{background:#0284c7}
.hero{background:linear-gradient(rgba(8,47,73,.82),rgba(8,47,73,.82)),repeating-linear-gradient(45deg,#0c4a6e 0 14px,#0369a1 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#bae6fd;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#0369a1;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#0284c7;text-decoration:none}
.btn.alt{background:#0c4a6e;color:#fff}.btn.alt:hover{background:#082f49}
section{padding:44px 0}
section.tint{background:#f0f9ff}
section h2{font-size:25px;color:#0c4a6e;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#0284c7;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #bae6fd;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(8,47,73,.06)}
.card h3{color:#0c4a6e;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #bae6fd;border-left:4px solid #0284c7;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#0c4a6e}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#0369a1}
.ctastrip{background:#0c4a6e;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #bae6fd;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#f0f9ff}.vs .col.good{background:#f0f9ff}
.vs h3{font-size:16px;margin-bottom:12px;color:#0c4a6e}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#0369a1;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #bae6fd;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#0c4a6e;list-style:none}
details summary:before{content:"+ ";color:#0284c7;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #bae6fd;border-top:4px solid #0284c7;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#44525f;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5a6b7b;padding:14px 0 0}
.crumb a{color:#5a6b7b}
footer{background:#082f49;color:#c9b8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #0c4a6e;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #bae6fd;border-top:4px solid #0284c7;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#0c4a6e}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #bae6fd;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(2,132,199,.08)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#0c4a6e}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#0284c7;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#0284c7;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#0c4a6e}
"""

# Gate 1 — 10 × 10 plumbing & drain (Elizabeth NJ focus; no LOC doorway pages)
HUBS = [
    {
        "slug": "drain-cleaning",
        "name": "Drain Cleaning",
        "short": "Drains",
        "blurb": "Clear clogged sinks, tubs, and main lines serving homes and businesses in Elizabeth, NJ.",
        "children": [
            ("clogged-sink-drain-cleaning", "Clogged Sink Drain Cleaning", "Kitchen and bath sink clogs cleared without guesswork."),
            ("bathtub-shower-drain-cleaning", "Bathtub & Shower Drain Cleaning", "Hair and soap buildup removed from tub and shower lines."),
            ("main-line-drain-cleaning", "Main Line Drain Cleaning", "Whole-home main drain clearing when multiple fixtures back up."),
            ("floor-drain-cleaning", "Floor Drain Cleaning", "Basement and utility floor drains restored to flow."),
            ("grease-trap-drain-cleaning", "Grease Trap Drain Cleaning", "Restaurant and commercial grease-related drain clearing."),
            ("hydro-jetting-drain-cleaning", "Hydro Jetting Drain Cleaning", "High-pressure water jetting for stubborn scale and debris."),
            ("camera-inspection-drain-cleaning", "Camera Inspection Drain Cleaning", "Video camera scoping before and after drain work."),
            ("slow-drain-diagnosis", "Slow Drain Diagnosis", "Find the real cause when drains crawl but do not fully clog."),
            ("recurring-clog-solutions", "Recurring Clog Solutions", "Root-cause fixes when the same drain keeps backing up."),
            ("emergency-drain-cleaning", "Emergency Drain Cleaning", "Same-day clog response when water will not go down."),
        ],
    },
    {
        "slug": "emergency-plumbing",
        "name": "Emergency Plumbing",
        "short": "Emergency",
        "blurb": "Fast response for bursts, backups, and no-water emergencies across Elizabeth, NJ.",
        "children": [
            ("burst-pipe-emergency", "Burst Pipe Emergency", "Shutoff guidance and rapid repair when a pipe fails."),
            ("sewer-backup-emergency", "Sewer Backup Emergency", "Urgent help when sewage backs into fixtures or floors."),
            ("no-water-emergency", "No Water Emergency", "Diagnose sudden loss of water supply to the property."),
            ("overflowing-toilet-emergency", "Overflowing Toilet Emergency", "Stop overflow damage and restore a working toilet."),
            ("water-heater-leak-emergency", "Water Heater Leak Emergency", "Contain tank leaks and restore hot water options."),
            ("frozen-pipe-emergency", "Frozen Pipe Emergency", "Thaw and repair risk lines during cold snaps [seasonal]."),
            ("gas-smell-plumbing-response", "Gas Smell Plumbing Response", "Coordinate safe response for suspected gas line issues [confirm scope]."),
            ("after-hours-plumber-elizabeth", "After-Hours Plumber Elizabeth", "Evening and weekend dispatch for urgent plumbing calls."),
            ("flooding-fixture-shutdown", "Flooding Fixture Shutdown", "Locate shutoffs and stop active fixture flooding."),
            ("same-day-emergency-dispatch", "Same-Day Emergency Dispatch", "Priority scheduling when waiting overnight is not an option."),
        ],
    },
    {
        "slug": "water-heater-services",
        "name": "Water Heater Services",
        "short": "Water Heaters",
        "blurb": "Repair, replace, and maintain tank and tankless water heaters for Elizabeth homes.",
        "children": [
            ("tank-water-heater-repair", "Tank Water Heater Repair", "Restore heat, pilot, and thermostat issues on traditional tanks."),
            ("tankless-water-heater-repair", "Tankless Water Heater Repair", "Diagnose error codes and flow problems on tankless units."),
            ("water-heater-installation", "Water Heater Installation", "Code-aware install of a new tank or tankless unit."),
            ("water-heater-replacement", "Water Heater Replacement", "Swap aging or leaking heaters before they flood the space."),
            ("water-heater-flush-maintenance", "Water Heater Flush & Maintenance", "Sediment flush and anode checks that extend heater life."),
            ("hot-water-not-working", "Hot Water Not Working", "Trace why there is no hot water at one or all fixtures."),
            ("water-heater-expansion-tank", "Water Heater Expansion Tank", "Add or replace expansion tanks for closed-system pressure."),
            ("electric-water-heater-service", "Electric Water Heater Service", "Element, thermostat, and breaker-side electric heater work."),
            ("gas-water-heater-service", "Gas Water Heater Service", "Burner, thermocouple, and venting checks on gas units."),
            ("commercial-water-heater-service", "Commercial Water Heater Service", "Higher-capacity heaters for small commercial spaces."),
        ],
    },
    {
        "slug": "leak-detection-repair",
        "name": "Leak Detection & Repair",
        "short": "Leaks",
        "blurb": "Find and fix hidden and visible water leaks before they damage Elizabeth properties.",
        "children": [
            ("slab-leak-detection", "Slab Leak Detection", "Locate under-slab leaks with less exploratory demolition."),
            ("wall-ceiling-leak-detection", "Wall & Ceiling Leak Detection", "Trace stains and drips to the real source."),
            ("faucet-leak-repair", "Faucet Leak Repair", "Stop drip waste at kitchen and bath faucets."),
            ("toilet-leak-repair", "Toilet Leak Repair", "Silent tank leaks and base seepage repaired correctly."),
            ("pipe-joint-leak-repair", "Pipe Joint Leak Repair", "Seal or replace failing couplings and soldered joints."),
            ("water-meter-leak-check", "Water Meter Leak Check", "Confirm if a meter spin means a hidden leak."),
            ("irrigation-leak-repair", "Irrigation Leak Repair", "Outdoor line leaks that spike the water bill [confirm]."),
            ("appliance-supply-line-leaks", "Appliance Supply Line Leaks", "Washer, fridge, and dishwasher supply line fixes."),
            ("pressure-related-leak-diagnosis", "Pressure-Related Leak Diagnosis", "High pressure that stresses joints and fixtures."),
            ("emergency-leak-containment", "Emergency Leak Containment", "Stop active leaks fast, then schedule the permanent fix."),
        ],
    },
    {
        "slug": "toilet-fixture-plumbing",
        "name": "Toilet & Fixture Plumbing",
        "short": "Fixtures",
        "blurb": "Install, repair, and replace toilets, faucets, and everyday fixtures in Elizabeth, NJ.",
        "children": [
            ("toilet-installation", "Toilet Installation", "New toilet set, wax ring, and supply line done right."),
            ("toilet-replacement", "Toilet Replacement", "Swap a cracked or inefficient toilet for a modern unit."),
            ("running-toilet-repair", "Running Toilet Repair", "Stop continuous fill that wastes water and money."),
            ("toilet-clog-removal", "Toilet Clog Removal", "Clear stubborn toilet blockages without damaging the bowl."),
            ("faucet-installation", "Faucet Installation", "Kitchen and bath faucet installs with shutoff checks."),
            ("faucet-cartridge-repair", "Faucet Cartridge Repair", "Replace worn cartridges that cause drips and stiff handles."),
            ("shower-valve-repair", "Shower Valve Repair", "Fix scalding, cold spikes, and leaky shower valves."),
            ("garbage-disposal-install-repair", "Garbage Disposal Install & Repair", "Reset, replace, or install under-sink disposals."),
            ("shutoff-valve-replacement", "Shutoff Valve Replacement", "Replace seized angle stops before the next emergency."),
            ("fixture-upgrade-packages", "Fixture Upgrade Packages", "Coordinated faucet, toilet, and trim updates in one visit."),
        ],
    },
    {
        "slug": "sewer-line-services",
        "name": "Sewer Line Services",
        "short": "Sewer",
        "blurb": "Inspect, clear, and repair sewer lines serving Elizabeth properties.",
        "children": [
            ("sewer-line-camera-inspection", "Sewer Line Camera Inspection", "See roots, breaks, and belly spots on video."),
            ("sewer-line-cleaning", "Sewer Line Cleaning", "Clear roots and debris from the building sewer."),
            ("sewer-line-repair", "Sewer Line Repair", "Targeted repair when a section of sewer fails."),
            ("sewer-line-replacement", "Sewer Line Replacement", "Full or partial sewer replacement when repair is not enough."),
            ("root-intrusion-sewer-clearing", "Root Intrusion Sewer Clearing", "Cut and clear roots that invade older clay or cast lines."),
            ("sewer-cleanout-install", "Sewer Cleanout Installation", "Add cleanouts that make future maintenance easier."),
            ("collapsed-sewer-diagnosis", "Collapsed Sewer Diagnosis", "Confirm collapse or offset before digging."),
            ("sewer-smell-investigation", "Sewer Smell Investigation", "Find trap, vent, or line issues behind foul odors."),
            ("commercial-sewer-service", "Commercial Sewer Service", "Sewer clearing and inspection for local businesses."),
            ("preventive-sewer-maintenance", "Preventive Sewer Maintenance", "Scheduled cleaning for properties with known root history."),
        ],
    },
    {
        "slug": "pipe-repair-repiping",
        "name": "Pipe Repair & Repiping",
        "short": "Pipes",
        "blurb": "Repair damaged supply lines or plan whole-home repiping for Elizabeth homes.",
        "children": [
            ("copper-pipe-repair", "Copper Pipe Repair", "Patch or replace failed copper sections."),
            ("pex-pipe-repair", "PEX Pipe Repair", "Fix PEX fittings, crimps, and damaged runs."),
            ("galvanized-pipe-replacement", "Galvanized Pipe Replacement", "Replace corroded galvanized lines that restrict flow."),
            ("whole-home-repiping", "Whole-Home Repiping", "Phased or full repipe when pinholes keep returning."),
            ("partial-repiping", "Partial Repiping", "Replace the worst zones without gutting every wall."),
            ("pipe-insulation-freeze-protection", "Pipe Insulation & Freeze Protection", "Reduce freeze risk on exposed or attic runs."),
            ("water-supply-line-reroute", "Water Supply Line Reroute", "Move lines for remodels or better access."),
            ("pin-hole-leak-pipe-repair", "Pinhole Leak Pipe Repair", "Address recurring pinhole patterns in aging copper."),
            ("basement-pipe-repair", "Basement Pipe Repair", "Accessible basement and crawlspace piping fixes."),
            ("code-upgrade-repiping", "Code-Upgrade Repiping", "Bring materials and layouts up to current local practice."),
        ],
    },
    {
        "slug": "bathroom-plumbing",
        "name": "Bathroom Plumbing",
        "short": "Bathroom",
        "blurb": "Rough-in, remodel support, and fixture plumbing for Elizabeth bathrooms.",
        "children": [
            ("bathroom-remodel-plumbing", "Bathroom Remodel Plumbing", "Rough-in and finish plumbing coordinated with your remodel."),
            ("bathtub-installation-plumbing", "Bathtub Installation Plumbing", "Drain, overflow, and supply connections for a new tub."),
            ("shower-installation-plumbing", "Shower Installation Plumbing", "Valve, drain, and trim plumbing for new showers."),
            ("bathroom-sink-install", "Bathroom Sink Installation", "Vanity sink, P-trap, and supply setup."),
            ("bathroom-drain-repair", "Bathroom Drain Repair", "Fix slow or leaking bath drains and traps."),
            ("toilet-flange-repair", "Toilet Flange Repair", "Stabilize rocking toilets and seal floor leaks."),
            ("bathroom-shutoff-upgrades", "Bathroom Shutoff Upgrades", "Add or replace local shutoffs for easier future service."),
            ("accessible-bathroom-plumbing", "Accessible Bathroom Plumbing", "Fixture layouts that support accessibility goals."),
            ("half-bath-plumbing", "Half-Bath Plumbing", "Powder-room sink and toilet plumbing packages."),
            ("master-bath-fixture-package", "Master Bath Fixture Package", "Multi-fixture installs for larger primary baths."),
        ],
    },
    {
        "slug": "kitchen-plumbing",
        "name": "Kitchen Plumbing",
        "short": "Kitchen",
        "blurb": "Sinks, disposals, dishwashers, and supply lines for Elizabeth kitchens.",
        "children": [
            ("kitchen-sink-installation", "Kitchen Sink Installation", "Drop-in or undermount sink plumbing and sealing."),
            ("kitchen-faucet-upgrade", "Kitchen Faucet Upgrade", "Pull-down and standard faucet installs with shutoffs."),
            ("dishwasher-install-hookup", "Dishwasher Install & Hookup", "Drain, supply, and air-gap connections done cleanly."),
            ("garbage-disposal-kitchen-service", "Garbage Disposal Kitchen Service", "Jam clearing, motor issues, and full replacements."),
            ("kitchen-drain-repair", "Kitchen Drain Repair", "Clear and repair under-sink drain assemblies."),
            ("instant-hot-water-faucet", "Instant Hot Water Faucet", "Point-of-use hot water faucet installs [confirm]."),
            ("reverse-osmosis-faucet-hookup", "Reverse Osmosis Faucet Hookup", "RO faucet and drain saddle connections."),
            ("kitchen-supply-line-replacement", "Kitchen Supply Line Replacement", "Replace brittle or leaking under-sink supplies."),
            ("island-sink-plumbing", "Island Sink Plumbing", "Island sink drain and vent solutions for remodels."),
            ("commercial-kitchen-plumbing", "Commercial Kitchen Plumbing", "Light commercial kitchen drain and fixture service."),
        ],
    },
    {
        "slug": "water-main-pressure",
        "name": "Water Main & Pressure Services",
        "short": "Water Main",
        "blurb": "Main shutoffs, pressure problems, and service-line issues for Elizabeth properties.",
        "children": [
            ("water-main-shutoff-repair", "Water Main Shutoff Repair", "Repair or replace seized curb and house main valves."),
            ("low-water-pressure-diagnosis", "Low Water Pressure Diagnosis", "Find whether pressure loss is fixture, pipe, or main related."),
            ("high-water-pressure-regulation", "High Water Pressure Regulation", "Install or service pressure-reducing valves."),
            ("pressure-reducing-valve-service", "Pressure Reducing Valve Service", "PRV adjustment, rebuild, or replacement."),
            ("water-service-line-repair", "Water Service Line Repair", "Repair the line from meter area toward the building."),
            ("water-meter-area-issues", "Water Meter Area Issues", "Coordinate meter-adjacent leaks and access problems."),
            ("whole-home-pressure-boost", "Whole-Home Pressure Boost", "Booster options when municipal pressure is chronically low [confirm]."),
            ("outdoor-spigot-main-tie-in", "Outdoor Spigot & Main Tie-In", "Hose bibbs and outdoor lines tied cleanly to supply."),
            ("water-hammer-arrestor-install", "Water Hammer Arrestor Install", "Stop banging pipes from sudden valve closures."),
            ("main-line-leak-investigation", "Main Line Leak Investigation", "Suspect service-line leaks before landscaping is opened."),
        ],
    },
]

SERVICE_AREAS = [
    "Elizabeth, NJ",
    "Linden, NJ",
    "Roselle, NJ",
    "Roselle Park, NJ",
    "Union, NJ",
    "Hillside, NJ",
    "Kenilworth, NJ",
    "Cranford, NJ",
    "Rahway, NJ",
    "Newark, NJ (nearby)",
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
<div class="logo">Elizabeth <span>Plumbing Stop</span><small>Plumbing &amp; Drains · Elizabeth, NJ</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Request a quote — no obligation</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-elizabeth-plumbing-stop/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-elizabeth-plumbing-stop/index.html">About The Elizabeth Plumbing Stop</a>
<a href="{p}about-elizabeth-plumbing-stop/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-elizabeth-plumbing-stop/service-areas/index.html">Service Areas</a>
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
<li><a href="{p}about-elizabeth-plumbing-stop/index.html">About The Elizabeth Plumbing Stop</a></li>
<li><a href="{p}about-elizabeth-plumbing-stop/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-elizabeth-plumbing-stop/service-areas/index.html">Service Areas</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}request-a-quote/index.html">Request a Quote</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul><li>{escape(ADDRESS)} <em>[confirm]</em></li><li>Operated by {escape(OPERATOR)} <em>[confirm]</em></li><li>Serving Elizabeth, NJ &amp; nearby</li></ul></div>
</div>
<div class="copy">The Elizabeth Plumbing Stop &middot; {escape(OPERATOR)} &middot; {escape(HQ)} &middot; {escape(PHONE)}<br>
Copyright &copy; 2026. The Elizabeth Plumbing Stop. All rights reserved.<br>
Domain, email, and NAP marked [confirm] pending owner review.</div></div></footer>
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
<label>Property Type</label><select><option>Please choose&hellip;</option><option>Residential</option><option>Small commercial</option><option>Multi-family</option><option>Not sure</option></select>
<label>Service Needed</label><select><option>Please choose&hellip;</option>{opts}<option>General plumbing question</option><option>Other</option></select>
<label>Urgency</label><select><option>Please choose&hellip;</option><option>Emergency — need help today</option><option>Within a few days</option><option>Planning / estimate only</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f95a8">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "PlumbingService",
        "name": "The Elizabeth Plumbing Stop",
        "legalName": OPERATOR,
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "areaServed": {
            "@type": "City",
            "name": "Elizabeth",
            "containedInPlace": {
                "@type": "State",
                "name": "New Jersey",
            },
        },
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
            "The Elizabeth Plumbing Stop | Plumbing & Drain Services in Elizabeth, NJ",
            "The Elizabeth Plumbing Stop is your one-stop shop for plumbing and drain services in Elizabeth, NJ — drains, emergencies, water heaters, leaks, and more.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>The Elizabeth Plumbing Stop</h1>
<p>Your one stop shop for your plumbing and drain services in Elizabeth NJ.</p>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>One-Stop</b><span>Plumbing &amp; Drains</span></div>
<div class="stat"><b>Local</b><span>Elizabeth, NJ Focus</span></div>
<div class="stat"><b>10</b><span>Service Families</span></div>
<div class="stat"><b>Quote</b><span>No Obligation</span></div>
</div></div></section>
<section><div class="wrap"><h2>Plumbing &amp; drain services for Elizabeth, NJ</h2>
<p class="lead">Ten service families — from drain cleaning and emergency plumbing through water heaters, leak detection, fixtures, sewer lines, repiping, bathroom, kitchen, and water-main work.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure which service you need? Start with a quote.</h2>
<p style="margin-bottom:14px">Describe the issue — we help you choose the right plumbing or drain path.</p>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a></div></div>
<section><div class="wrap"><h2>How to get started</h2><div class="cols3">
<div class="card"><h3>1. Request a quote</h3><p>Tell us the fixture, leak, drain, or heater issue — residential or light commercial.</p></div>
<div class="card"><h3>2. Scope the work</h3><p>We clarify urgency, access, and whether repair or replacement fits best.</p></div>
<div class="card"><h3>3. Schedule service</h3><p>Confirm next steps in writing before work begins — no invented wait-time promises.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why The Elizabeth Plumbing Stop</h2><div class="cols3">
<div class="card"><h3>One-stop plumbing &amp; drains</h3><p>Clogs, leaks, heaters, fixtures, and sewer work under one local roof.</p></div>
<div class="card"><h3>Elizabeth, NJ focus</h3><p>Local copy and routing built around Elizabeth and nearby Union County communities.</p></div>
<div class="card"><h3>Clear next steps</h3><p>Quote and proposal paths that set expectations before you commit.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready for a plumbing or drain quote?</h2>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    "What is The Elizabeth Plumbing Stop?",
                    "The Elizabeth Plumbing Stop is a one-stop shop for plumbing and drain services in Elizabeth, NJ — from clogged drains and emergencies to water heaters, leaks, fixtures, and sewer work.",
                ),
                (
                    "Who operates The Elizabeth Plumbing Stop?",
                    f"The Elizabeth Plumbing Stop is operated by {OPERATOR}, with headquarters listed at {ADDRESS} [confirm].",
                ),
                (
                    "How do I request a quote?",
                    "Use the Request a Quote form or call us. Describe the issue, property type, and urgency — we follow up with next steps.",
                ),
                (
                    "Do you serve areas outside Elizabeth?",
                    "Elizabeth, NJ is the primary focus. Nearby communities may be served case by case — see Service Areas [confirm coverage].",
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
            f"{h['name']} | The Elizabeth Plumbing Stop",
            f"{h['name']} from The Elizabeth Plumbing Stop in Elizabeth, NJ — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} in Elizabeth, NJ</h2>
<p class="lead">{escape(h["blurb"])} Part of The Elizabeth Plumbing Stop — your one-stop shop for plumbing and drain services.</p>
<p><a class="btn" href="../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Services We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What a typical engagement can include</h2>
<ul class="checks">
<li>Clear description of the plumbing or drain issue</li>
<li>On-site diagnosis before major replacement recommendations</li>
<li>Repair-vs-replace options explained in plain language</li>
<li>Written next steps after the quote or proposal path</li>
<li>Elizabeth, NJ focus — no generic national boilerplate</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with Request a Quote. For larger or multi-unit work, use Request a Proposal.",
                ),
                (
                    "Where is The Elizabeth Plumbing Stop based?",
                    f"Headquartered in {HQ} ({ADDRESS}) [confirm], focused on Elizabeth and nearby communities.",
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
            f"{name} | The Elizabeth Plumbing Stop",
            f"{name} from The Elizabeth Plumbing Stop in Elizabeth, NJ — {blurb}",
        )
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(name)} for Elizabeth, NJ homes and businesses</h2>
<p class="lead">{escape(blurb)} At The Elizabeth Plumbing Stop, {escape(name.lower())} is delivered as part of a one-stop plumbing and drain shop — clear diagnosis, practical options, and a quote path before you commit.</p>
<p><a class="btn" href="../../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(name)} with The Elizabeth Plumbing Stop can help you gain:</h2>
<ul class="checks">
<li>Faster clarity on whether repair or replacement is the smarter path</li>
<li>Local Elizabeth, NJ focus instead of generic national copy</li>
<li>One team for related drains, fixtures, and supply-line issues</li>
<li>Written quote or proposal steps before major work</li>
<li>Honest scope — no invented testimonials or wait-time guarantees</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} path scoped to your property — not a one-size package</h2>
<p>No two homes or businesses need {escape(name.lower())} the same way. We match access, urgency, and fixture or line condition — then confirm next steps before work begins.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Homeowners avoid key risks with a developed local path for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with ad-hoc plumbing fixes</h3><ul>
<li>Symptom fixes that ignore the real drain or supply cause</li>
<li>Surprise upsells after walls are already open</li>
<li>No written scope before major replacement</li>
<li>National call centers that do not know Elizabeth access realities</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on The Elizabeth Plumbing Stop</h3><ul>
<li>One-stop plumbing and drain coverage under local pages</li>
<li>Quote and proposal paths before you commit</li>
<li>Elizabeth, NJ service-area focus</li>
<li>Race Computer Services accountability for this factory build [confirm]</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>See next steps first — request a quote</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} looks like for your property? Start with a free quote request.</p>
<a class="btn" href="../../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} is scheduled?",
                    "Timing depends on urgency and crew availability. Emergency paths are prioritized; planned work is scheduled after the quote conversation — no invented same-hour guarantees.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Price depends on access, parts, and whether repair or replacement is required. Use Request a Quote for an estimate path.",
                ),
                (
                    f"Why choose The Elizabeth Plumbing Stop for {name.lower()}?",
                    f"We deliver {name.lower()} inside a one-stop plumbing and drain shop focused on Elizabeth, NJ — with clear quote and proposal steps.",
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
<h2 style="font-size:20px">Initiate a request with The Elizabeth Plumbing Stop</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us the issue</h3><p>Drain, leak, heater, fixture, sewer, or pressure — plus property type.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>A quote path, a proposal for larger work, or honest advice on next steps.</p></div>
<div class="card"><h3>3. Schedule when ready</h3><p>Confirm scope in writing before work begins.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>The Elizabeth Plumbing Stop</strong><br>Operated by {escape(OPERATOR)} <em>[confirm]</em><br>Headquarters: {escape(ADDRESS)} <em>[confirm]</em><br>Phone: {escape(PHONE)}<br>Email: {escape(EMAIL)} <em>[confirm]</em></p>
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
            "source_questionnaire_field",
            "booking_type",
        ],
        ["/", "HOME", "", "elizabeth plumbing stop", "logo/home", "A1,A6,A10", ""],
        [
            "/about-elizabeth-plumbing-stop/",
            "COMP-HUB",
            "/",
            "about the elizabeth plumbing stop",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-elizabeth-plumbing-stop/why-choose-us/",
            "COMP-CHILD",
            "/about-elizabeth-plumbing-stop/",
            "why choose the elizabeth plumbing stop",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-elizabeth-plumbing-stop/service-areas/",
            "COMP-CHILD",
            "/about-elizabeth-plumbing-stop/",
            "elizabeth nj plumbing service areas",
            "About menu",
            "F1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact elizabeth plumbing stop",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "plumbing proposal elizabeth nj",
            "nav utility",
            "I1",
            "Request for Proposal",
        ],
        [
            "/request-a-quote/",
            "FORM-CONSULT",
            "/",
            "plumbing quote elizabeth nj",
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
                h["name"].lower() + " elizabeth nj",
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
                    n.lower() + " elizabeth nj",
                    "Services menu > hub grid",
                    "B row",
                    "Request for Proposal",
                ]
            )
    with (ROOT / "ELIZABETHPLUMBING-PAGE-INVENTORY.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
        "seocow-demo-site.zip",
        "ELIZABETHPLUMBING-QUESTIONNAIRE-ANSWERS.md",
        "ELIZABETHPLUMBING-PAGE-INVENTORY.csv",
        "ELIZABETHPLUMBING-NOTES.md",
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
        ROOT / "about-elizabeth-plumbing-stop" / "index.html",
        head(
            "About The Elizabeth Plumbing Stop | Elizabeth, NJ",
            "The Elizabeth Plumbing Stop is your one-stop shop for plumbing and drain services in Elizabeth, NJ.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About The Elizabeth Plumbing Stop</h2>
<p class="lead">The Elizabeth Plumbing Stop is a one-stop shop for plumbing and drain services in Elizabeth, NJ — operated by {escape(OPERATOR)} from {escape(ADDRESS)} <em>[confirm]</em>.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>We focus on local plumbing and drain demand: clogs, emergencies, water heaters, leaks, fixtures, sewer lines, repiping, bathrooms, kitchens, and water-main pressure work.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="service-areas/index.html">Service areas &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "Who operates The Elizabeth Plumbing Stop?",
                    f"The Elizabeth Plumbing Stop is operated by {OPERATOR}, headquartered at {ADDRESS} [confirm].",
                ),
                (
                    "Do you work outside Elizabeth?",
                    "Elizabeth, NJ is the primary focus. Nearby communities may be available case by case — see Service Areas [confirm].",
                ),
            ]
        )
        + org_schema()
        + footer(1),
    )
    urls.append("/about-elizabeth-plumbing-stop/")

    write(
        ROOT / "about-elizabeth-plumbing-stop" / "why-choose-us" / "index.html",
        head(
            "Why Choose The Elizabeth Plumbing Stop",
            "Why homeowners and businesses choose The Elizabeth Plumbing Stop in Elizabeth, NJ.",
        )
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose The Elizabeth Plumbing Stop</h2>
<p class="lead">A local plumbing and drain shop built to be the one stop for everyday fixes and urgent calls — without invented testimonials.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>One-stop coverage</h3><p>Drains, emergencies, heaters, leaks, fixtures, sewer, pipes, bath, kitchen, and pressure.</p></div>
<div class="card"><h3>Elizabeth, NJ focus</h3><p>Pages and routing written for local intent — not national boilerplate.</p></div>
<div class="card"><h3>Quote-led intake</h3><p>Request a Quote first; larger jobs can move to a written proposal.</p></div>
<div class="card"><h3>Clear service map</h3><p>Ten hubs × ten children so visitors land on the right problem page.</p></div>
<div class="card"><h3>Honest staging copy</h3><p>No fabricated reviews, awards, or wait-time guarantees in this build.</p></div>
<div class="card"><h3>Named operator</h3><p>Race Computer Services accountability for this factory build [confirm].</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-elizabeth-plumbing-stop/why-choose-us/")

    areas = "".join(
        f'<div class="gcard"><h3>{escape(a)}</h3><p>Plumbing and drain service inquiries for {escape(a)} — coverage confirmed case by case.</p></div>'
        for a in SERVICE_AREAS
    )
    write(
        ROOT / "about-elizabeth-plumbing-stop" / "service-areas" / "index.html",
        head(
            "Service Areas | The Elizabeth Plumbing Stop",
            "Service areas for The Elizabeth Plumbing Stop — Elizabeth, NJ and nearby communities.",
        )
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Service Areas</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Service Areas</h2>
<p class="lead">Primary focus: Elizabeth, NJ. Nearby communities listed below may be served case by case — no LOC doorway pages in this Gate 1 build.</p>
<div class="grid">{areas}</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-elizabeth-plumbing-stop/service-areas/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | The Elizabeth Plumbing Stop",
            "Contact Us for Plumbing & Drain Inquiries",
            "Tell us the issue, your Elizabeth-area property type, and whether you need a same-day path or a planned estimate.",
        ),
        (
            "request-a-quote",
            "Request a Quote | The Elizabeth Plumbing Stop",
            "Request a Plumbing or Drain Quote",
            "Describe the clog, leak, heater, fixture, or sewer issue — we follow up with clear next steps.",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | The Elizabeth Plumbing Stop",
            "Request a Proposal for Larger Plumbing Work",
            "Share multi-fixture, remodel, or multi-unit goals. We return a scoped proposal you can compare.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | The Elizabeth Plumbing Stop", "Page not found.")
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
        ROOT / "ELIZABETHPLUMBING-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — The Elizabeth Plumbing Stop (FACTORY BUILD · Gate 1 10×10)

**Build uses NearMe OS Website Factory instructions-template (SEO Cow staging engine) · category: plumbing & drain services · Elizabeth NJ local trade · Race Computer Services S1 defaults · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | The Elizabeth Plumbing Stop (operated by Race Computer Services, LLC) | this build [confirm] |
| A2 domain | elizabethplumbingstop.com | [confirm] |
| A3 phone | {PHONE} | Race CS / S1 (same operator) |
| A4 email | {EMAIL} | [confirm] |
| A5 address | {ADDRESS} | Race CS default [confirm] |
| A6 trade | Plumbing & drain services | this build |
| A7 founded | not stated — omitted | — |
| A10 value_proposition | One-stop shop for plumbing and drain services in Elizabeth, NJ | this build |
| A11 tagline | {TAGLINE} | this build |
| A12 competitor_type | national plumbing brands, marketplace lead-gen, unclassified local plumbers | [confirm] |
| A13 hours | not stated — omitted | — |

## B — Services: 10 categories × 10 children
{hub_slugs} — full map in ELIZABETHPLUMBING-PAGE-INVENTORY.csv.
FORM-CONSULT = `request-a-quote` · FORM-PRICING = `request-a-proposal`.

## C–I
- D1 audiences: homeowners, landlords, small commercial, remodel partners
- F1 service_area: Elizabeth NJ primary; nearby Union County communities listed (no LOC doorway pages)
- F2/F3: no LOC doorway pages in this build
- I1 form_destination: OPEN — demo shells
- Staging: noindex + STAGING PREVIEW banner
- Domain / email / NAP: marked [confirm]

| Metric | Value |
|---|---|
| hubs | {len(HUBS)} |
| svc children | {svc_children} |
| staging | noindex + STAGING PREVIEW banner |
""",
    )

    write(
        ROOT / "ELIZABETHPLUMBING-NOTES.md",
        f"""# The Elizabeth Plumbing Stop — Factory Build

Local trade category: **plumbing & drain services** (Elizabeth, NJ).

- Generator: `scripts/generate_elizabethplumbing_factory.py`
- Gate 1: 10 × 10 = 100 SVC-CHILD (+ chrome ≈ 117 pages)
- Brand: The Elizabeth Plumbing Stop
- FORM-CONSULT: `/request-a-quote/` (highlighted)
- FORM-PRICING: `/request-a-proposal/`
- About: `/about-elizabeth-plumbing-stop/` · why-choose-us · service-areas
- Staging: noindex + STAGING PREVIEW banner
- Domain / email / NAP: elizabethplumbingstop.com · {EMAIL} · {ADDRESS} *[confirm]*
- CSS: water blue / slate (`#0284c7` / `#0c4a6e` / `#f0f9ff` / `#0369a1`)
- No invented testimonials; no LOC doorway pages
""",
    )

    pages = list(ROOT.rglob("index.html"))
    factory_pages = list(pages)
    print(f"Generated {len(factory_pages)} factory index pages")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)} · Children: {sum(len(h['children']) for h in HUBS)}")


if __name__ == "__main__":
    main()
