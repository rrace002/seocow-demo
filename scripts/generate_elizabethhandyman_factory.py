#!/usr/bin/env python3
"""Generate Elizabeth Handyman Home Improvements site using the NearMe OS Website Factory template
(same HTML/CSS engine as the SEO Cow / Car Rental Near Me staging builds).

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: home additions, decks, remodels & handyman services (Elizabeth, NJ local trade).
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
BASE = "https://elizabethhandyman.com"  # [confirm]
PHONE = "(862) 295-0011"
PHONE_TEL = "+18622950011"
EMAIL = "info@elizabethhandyman.com"  # [confirm]
HQ = "Elizabeth, NJ"
ADDRESS = "12 Sayre St, Elizabeth, NJ 07208"  # Race CS default [confirm]
OPERATOR = "Race Computer Services, LLC"  # [confirm]
TAGLINE = "Additions, Decks, Remodels & Handyman Services in Elizabeth, NJ"
STAGING_BANNER = (
    "STAGING PREVIEW — Elizabeth Handyman Home Improvements factory build · Elizabeth NJ · "
    "content pending owner review"
)

# NearMe factory CSS (SEO Cow template) with forest green / wood amber remap
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#1a2e1a;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#b45309;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#14532d;color:#fef3c7;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#166534;color:#ecfccb;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #b45309;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#14532d}.logo span{color:#b45309}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b5a;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#14532d}
.phone-cta small{display:block;color:#5a6b5a;font-size:11px}
nav.nav{background:#14532d}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#166534;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #b45309;z-index:60}
.dd a{color:#14532d;padding:10px 15px;font-weight:500;border-bottom:1px solid #d9f99d}
.dd a:hover{background:#f7fee7}
.nav .em a{background:#b45309}.nav .em a:hover{background:#92400e}
.hero{background:linear-gradient(rgba(20,83,45,.82),rgba(20,83,45,.82)),repeating-linear-gradient(45deg,#14532d 0 14px,#166534 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#fef3c7;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#b45309;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#92400e;text-decoration:none}
.btn.alt{background:#14532d;color:#fff}.btn.alt:hover{background:#166534}
section{padding:44px 0}
section.tint{background:#f7fee7}
section h2{font-size:25px;color:#14532d;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#b45309;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #d9f99d;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(20,83,45,.06)}
.card h3{color:#14532d;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #d9f99d;border-left:4px solid #b45309;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#14532d}
.gcard p{font-size:14px;color:#44524a;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#b45309}
.ctastrip{background:#14532d;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #d9f99d;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#fffbeb}.vs .col.good{background:#f7fee7}
.vs h3{font-size:16px;margin-bottom:12px;color:#14532d}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#b45309;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #d9f99d;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#14532d;list-style:none}
details summary:before{content:"+ ";color:#b45309;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #d9f99d;border-top:4px solid #b45309;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#44524a;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5a6b5a;padding:14px 0 0}
.crumb a{color:#5a6b5a}
footer{background:#14532d;color:#c9b8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #166534;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #d9f99d;border-top:4px solid #b45309;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#14532d}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b5a;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #d9f99d;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(180,83,9,.08)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#14532d}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#b45309;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#b45309;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#14532d}
"""

# Gate 1 — 10 × 10 home improvements & handyman (Elizabeth NJ focus; no LOC doorway pages)
HUBS = [
    {
        "slug": "home-additions",
        "name": "Home Additions",
        "short": "Additions",
        "blurb": "Plan and build room additions that expand living space for Elizabeth, NJ homes.",
        "children": [
            ("room-addition-planning", "Room Addition Planning", "Layout, access, and scope planning before framing begins."),
            ("single-room-addition", "Single-Room Addition", "Add a bedroom, office, or multipurpose room to the footprint."),
            ("family-room-addition", "Family Room Addition", "Expand gathering space with a new family or great room."),
            ("sunroom-addition", "Sunroom Addition", "Light-filled sunroom additions tied into existing structure."),
            ("second-story-addition", "Second-Story Addition", "Upward expansion when yard space is limited [confirm scope]."),
            ("garage-conversion-addition", "Garage Conversion Addition", "Convert unused garage volume into finished living space."),
            ("addition-foundation-prep", "Addition Foundation Prep", "Site and foundation prep that supports a stable addition."),
            ("addition-framing-shell", "Addition Framing & Shell", "Structural framing, sheathing, and weather-tight shell work."),
            ("addition-finish-carpentry", "Addition Finish Carpentry", "Trim, doors, and finish details that blend with the home."),
            ("addition-remodel-coordination", "Addition Remodel Coordination", "Coordinate trades so the addition connects cleanly to existing rooms."),
        ],
    },
    {
        "slug": "deck-building-repair",
        "name": "Deck Building & Repair",
        "short": "Decks",
        "blurb": "Build, repair, and refresh outdoor decks for Elizabeth, NJ properties.",
        "children": [
            ("new-deck-construction", "New Deck Construction", "Design and build a new deck matched to your yard and access."),
            ("deck-repair", "Deck Repair", "Fix soft boards, loose rails, and failing connections."),
            ("deck-board-replacement", "Deck Board Replacement", "Replace worn or warped decking without rebuilding the whole frame."),
            ("deck-railing-install-repair", "Deck Railing Install & Repair", "Safe, code-aware rail systems for stairs and edges."),
            ("deck-stair-building", "Deck Stair Building", "Sturdy stairs that connect yard levels cleanly."),
            ("composite-deck-install", "Composite Deck Installation", "Low-maintenance composite decking installs [material options]."),
            ("wood-deck-refinishing", "Wood Deck Refinishing", "Clean, stain, and seal wood decks to extend life."),
            ("deck-footing-framing-repair", "Deck Footing & Framing Repair", "Stabilize footings and joists before surface work."),
            ("deck-lighting-prep", "Deck Lighting Prep", "Prep and rough openings for outdoor lighting runs [confirm]."),
            ("small-porch-deck-refresh", "Small Porch & Deck Refresh", "Compact porch and deck updates for everyday outdoor use."),
        ],
    },
    {
        "slug": "basement-finishing",
        "name": "Basement Finishing",
        "short": "Basements",
        "blurb": "Finish and refresh Elizabeth basements into usable living and work space.",
        "children": [
            ("basement-finishing-planning", "Basement Finishing Planning", "Layout, egress, and moisture checks before finish work."),
            ("basement-framing", "Basement Framing", "Partition framing that creates rooms without blocking access."),
            ("basement-drywall-finish", "Basement Drywall & Finish", "Hang, tape, and finish walls ready for paint."),
            ("basement-ceiling-options", "Basement Ceiling Options", "Drop, drywall, or hybrid ceiling approaches for utilities."),
            ("basement-flooring-install", "Basement Flooring Installation", "Moisture-aware flooring choices for below-grade rooms."),
            ("basement-bathroom-rough-in-support", "Basement Bathroom Rough-In Support", "Coordinate finish carpentry around a new basement bath [confirm plumbing partner]."),
            ("basement-egress-window-prep", "Basement Egress Window Prep", "Prep and finish work around egress openings [confirm]."),
            ("basement-storage-built-ins", "Basement Storage Built-Ins", "Shelving and built-ins that keep finished space organized."),
            ("basement-rec-room-finish", "Basement Rec Room Finish", "Family rec rooms with durable finishes for daily use."),
            ("partial-basement-refresh", "Partial Basement Refresh", "Phase one finishing when a full gut is not required."),
        ],
    },
    {
        "slug": "kitchen-remodeling",
        "name": "Kitchen Remodeling",
        "short": "Kitchens",
        "blurb": "Remodel Elizabeth kitchens with practical layouts, cabinetry, and finish work.",
        "children": [
            ("kitchen-remodel-planning", "Kitchen Remodel Planning", "Scope cabinets, layout, and finish sequence before demo."),
            ("kitchen-cabinet-install", "Kitchen Cabinet Installation", "Level, secure, and align cabinet runs for a clean fit."),
            ("kitchen-countertop-prep", "Kitchen Countertop Prep", "Prep tops and supports for stone, laminate, or butcher block."),
            ("kitchen-backsplash-install", "Kitchen Backsplash Installation", "Tile or panel backsplash installs that finish the cooking wall."),
            ("kitchen-island-build", "Kitchen Island Build", "Add or rebuild an island for prep and seating space."),
            ("kitchen-flooring-remodel", "Kitchen Flooring Remodel", "Durable kitchen flooring tied into adjoining rooms."),
            ("kitchen-trim-finish-work", "Kitchen Trim & Finish Work", "Crown, toe-kicks, and trim that close visual gaps."),
            ("kitchen-appliance-opening-prep", "Kitchen Appliance Opening Prep", "Frame and finish openings for fridge, range, and dishwasher."),
            ("small-kitchen-refresh", "Small Kitchen Refresh", "Targeted updates when a full gut remodel is not needed."),
            ("kitchen-pantry-carpentry", "Kitchen Pantry Carpentry", "Pantry shelving and doors that maximize storage."),
        ],
    },
    {
        "slug": "bathroom-remodeling",
        "name": "Bathroom Remodeling",
        "short": "Bathrooms",
        "blurb": "Remodel Elizabeth bathrooms with tile, vanities, and finish carpentry.",
        "children": [
            ("bathroom-remodel-planning", "Bathroom Remodel Planning", "Layout, moisture, and finish sequence planned before demo."),
            ("bathroom-vanity-install", "Bathroom Vanity Installation", "Set and secure vanities with clean trim transitions."),
            ("bathroom-tile-install", "Bathroom Tile Installation", "Floor and wall tile for wet areas done with care."),
            ("shower-surround-refresh", "Shower Surround Refresh", "Update shower walls without a full structural rebuild."),
            ("bathroom-flooring-remodel", "Bathroom Flooring Remodel", "Water-resistant flooring tied into thresholds correctly."),
            ("bathroom-trim-finish", "Bathroom Trim & Finish", "Base, casing, and finish details after fixture work."),
            ("half-bath-remodel", "Half-Bath Remodel", "Powder-room updates that maximize a small footprint."),
            ("master-bath-refresh", "Master Bath Refresh", "Primary bath updates focused on layout and finishes."),
            ("bathroom-accessibility-updates", "Bathroom Accessibility Updates", "Grab-ready framing and finish updates for easier access."),
            ("bathroom-lighting-vent-prep", "Bathroom Lighting & Vent Prep", "Prep openings and trim for lighting and ventilation [confirm]."),
        ],
    },
    {
        "slug": "general-handyman-services",
        "name": "General Handyman Services",
        "short": "Handyman",
        "blurb": "Everyday repairs and punch-list handyman work for Elizabeth homes and small businesses.",
        "children": [
            ("punch-list-repairs", "Punch-List Repairs", "Close out the small fixes that never make a full remodel day."),
            ("furniture-assembly-mounting", "Furniture Assembly & Mounting", "Assemble and securely mount furniture and fixtures."),
            ("tv-shelf-mounting", "TV & Shelf Mounting", "Locate studs and mount TVs, shelves, and brackets safely."),
            ("door-hinge-hardware-fixes", "Door Hinge & Hardware Fixes", "Adjust sticky doors, hinges, and everyday hardware."),
            ("caulking-weatherstripping", "Caulking & Weatherstripping", "Seal drafts and moisture paths at windows, baths, and trim."),
            ("drywall-patch-small-repairs", "Drywall Patch & Small Repairs", "Patch holes and blend small wall repairs before paint."),
            ("closet-organizer-install", "Closet Organizer Installation", "Shelving and rod systems that reclaim closet space."),
            ("gutter-downspout-touch-ups", "Gutter & Downspout Touch-Ups", "Minor gutter and downspout adjustments [confirm height/scope]."),
            ("seasonal-home-prep", "Seasonal Home Prep", "Pre-season punch lists for weather and wear items."),
            ("property-walkthrough-fix", "Property Walkthrough Fixes", "Landlord and homeowner walkthrough repair lists completed cleanly."),
        ],
    },
    {
        "slug": "drywall-painting",
        "name": "Drywall & Painting",
        "short": "Drywall",
        "blurb": "Hang, patch, and paint walls and ceilings for Elizabeth interiors.",
        "children": [
            ("drywall-hanging", "Drywall Hanging", "Hang new board for additions, basements, and remodel zones."),
            ("drywall-taping-finishing", "Drywall Taping & Finishing", "Tape, mud, and sand for a paint-ready surface."),
            ("drywall-water-damage-repair", "Drywall Water-Damage Repair", "Cut out and replace damaged board after leaks are resolved."),
            ("ceiling-drywall-repair", "Ceiling Drywall Repair", "Fix cracks, sagging patches, and ceiling penetrations."),
            ("interior-painting", "Interior Painting", "Clean prep and even coats for rooms and hallways."),
            ("trim-door-painting", "Trim & Door Painting", "Crisp paint on casings, base, and doors."),
            ("accent-wall-painting", "Accent Wall Painting", "Feature walls that update a room without a full remodel."),
            ("texture-match-repairs", "Texture Match Repairs", "Blend patches into existing wall texture where practical."),
            ("primer-stain-blocking", "Primer & Stain Blocking", "Seal stains and odors before finish coats."),
            ("paint-refresh-packages", "Paint Refresh Packages", "Room packages for move-in, rental turn, or sale prep."),
        ],
    },
    {
        "slug": "flooring-carpentry",
        "name": "Flooring & Carpentry",
        "short": "Flooring",
        "blurb": "Install flooring and deliver finish carpentry for Elizabeth homes.",
        "children": [
            ("laminate-flooring-install", "Laminate Flooring Installation", "Floating laminate installs with clean transitions."),
            ("vinyl-plank-flooring-install", "Vinyl Plank Flooring Installation", "Durable LVP installs for kitchens, baths, and living areas."),
            ("hardwood-floor-repair", "Hardwood Floor Repair", "Board replacement and localized hardwood repairs."),
            ("subfloor-repair", "Subfloor Repair", "Stabilize soft spots before finish flooring goes down."),
            ("baseboard-casing-install", "Baseboard & Casing Installation", "Finish trim that frames floors and openings."),
            ("custom-shelving-carpentry", "Custom Shelving Carpentry", "Built-in and freestanding shelving matched to the room."),
            ("stair-tread-riser-work", "Stair Tread & Riser Work", "Repair or refresh treads and risers for safer stairs."),
            ("closet-carpentry", "Closet Carpentry", "Rods, shelves, and framing that organize storage."),
            ("trim-carpentry-packages", "Trim Carpentry Packages", "Coordinated trim packages after remodel drywall."),
            ("threshold-transition-install", "Threshold & Transition Installation", "Smooth transitions between flooring types and rooms."),
        ],
    },
    {
        "slug": "doors-windows-trim",
        "name": "Doors, Windows & Trim",
        "short": "Doors",
        "blurb": "Install and adjust doors, windows, and trim for Elizabeth properties.",
        "children": [
            ("interior-door-installation", "Interior Door Installation", "Hang prehung or slab doors with clean swings and latches."),
            ("exterior-door-installation", "Exterior Door Installation", "Entry and side doors set with weather seal attention."),
            ("door-frame-repair", "Door Frame Repair", "Repair damaged jambs and stops that cause sticking."),
            ("window-trim-casing", "Window Trim & Casing", "Interior casing that finishes window openings."),
            ("window-sill-repair", "Window Sill Repair", "Fix soft or damaged sills before finish paint."),
            ("storm-screen-door-service", "Storm & Screen Door Service", "Adjust or replace storm and screen doors [confirm]."),
            ("closet-bifold-door-install", "Closet & Bifold Door Install", "Track and bifold systems that operate smoothly."),
            ("door-hardware-upgrades", "Door Hardware Upgrades", "Locks, handles, and hinges refreshed for daily use."),
            ("trim-molding-install", "Trim & Molding Installation", "Chair rail, crown, and accent molding installs."),
            ("window-door-weatherseal", "Window & Door Weatherseal", "Stops drafts with seals, sweeps, and adjustments."),
        ],
    },
    {
        "slug": "outdoor-home-improvements",
        "name": "Outdoor Home Improvements",
        "short": "Outdoor",
        "blurb": "Outdoor carpentry and curb-appeal improvements for Elizabeth homes.",
        "children": [
            ("fence-repair-sections", "Fence Repair Sections", "Replace damaged fence sections and stabilize posts."),
            ("gate-install-repair", "Gate Install & Repair", "Gates that latch and swing without binding."),
            ("outdoor-steps-railings", "Outdoor Steps & Railings", "Safe exterior steps and rail updates."),
            ("pergola-shade-structure", "Pergola & Shade Structure", "Simple shade structures for patios and decks [confirm]."),
            ("shed-repair-refresh", "Shed Repair & Refresh", "Doors, trim, and minor structural shed fixes."),
            ("exterior-trim-repair", "Exterior Trim Repair", "Fascia, corner, and trim repairs that stop water intrusion."),
            ("porch-post-beam-repair", "Porch Post & Beam Repair", "Stabilize porch structure before cosmetic refresh."),
            ("outdoor-bench-built-ins", "Outdoor Bench Built-Ins", "Built-in seating for decks and small yards."),
            ("curb-appeal-carpentry", "Curb Appeal Carpentry", "Entry and facade carpentry that cleans up first impressions."),
            ("patio-transition-carpentry", "Patio Transition Carpentry", "Steps, borders, and transitions between house and patio."),
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
<div class="logo">Elizabeth <span>Handyman</span><small>Home Improvements · Elizabeth, NJ</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Request a quote — no obligation</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-elizabeth-handyman/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-elizabeth-handyman/index.html">About Elizabeth Handyman Home Improvements</a>
<a href="{p}about-elizabeth-handyman/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-elizabeth-handyman/service-areas/index.html">Service Areas</a>
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
<li><a href="{p}about-elizabeth-handyman/index.html">About Elizabeth Handyman Home Improvements</a></li>
<li><a href="{p}about-elizabeth-handyman/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-elizabeth-handyman/service-areas/index.html">Service Areas</a></li>
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
<div class="copy">Elizabeth Handyman Home Improvements &middot; {escape(OPERATOR)} &middot; {escape(HQ)} &middot; {escape(PHONE)}<br>
Copyright &copy; 2026. Elizabeth Handyman Home Improvements. All rights reserved.<br>
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
<label>Service Needed</label><select><option>Please choose&hellip;</option>{opts}<option>General handyman question</option><option>Other</option></select>
<label>Urgency</label><select><option>Please choose&hellip;</option><option>Urgent — need help soon</option><option>Within a few days</option><option>Planning / estimate only</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f9588">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": "Elizabeth Handyman Home Improvements",
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
            "Elizabeth Handyman Home Improvements | Additions, Decks & Remodels in Elizabeth, NJ",
            "Elizabeth Handyman Home Improvements specializes in additions, decks, basement finishing, kitchen remodeling, bathroom remodeling, and general handyman services in Elizabeth, NJ.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>Elizabeth Handyman Home Improvements</h1>
<p>Specializing in additions, decks, basement finishing, kitchen remodeling, bathroom remodeling, and general handyman services in Elizabeth, NJ.</p>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>Additions</b><span>Rooms &amp; Expansions</span></div>
<div class="stat"><b>Decks</b><span>Build &amp; Repair</span></div>
<div class="stat"><b>Remodels</b><span>Kitchen &amp; Bath</span></div>
<div class="stat"><b>Handyman</b><span>Everyday Fixes</span></div>
</div></div></section>
<section><div class="wrap"><h2>Home improvements &amp; handyman services for Elizabeth, NJ</h2>
<p class="lead">Ten service families — from home additions and deck building through basement finishing, kitchen and bathroom remodeling, general handyman work, drywall, flooring, doors, and outdoor improvements.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure which service you need? Start with a quote.</h2>
<p style="margin-bottom:14px">Describe the project — we help you choose the right addition, remodel, or handyman path.</p>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a></div></div>
<section><div class="wrap"><h2>How to get started</h2><div class="cols3">
<div class="card"><h3>1. Request a quote</h3><p>Tell us about the addition, deck, remodel, or handyman list — residential or light commercial.</p></div>
<div class="card"><h3>2. Scope the work</h3><p>We clarify access, materials, and whether a focused fix or fuller remodel fits best.</p></div>
<div class="card"><h3>3. Schedule service</h3><p>Confirm next steps in writing before work begins — no invented wait-time promises.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why Elizabeth Handyman Home Improvements</h2><div class="cols3">
<div class="card"><h3>Six owner specialties</h3><p>Additions, decks, basement finishing, kitchen remodeling, bathroom remodeling, and general handyman services.</p></div>
<div class="card"><h3>Elizabeth, NJ focus</h3><p>Local copy and routing built around Elizabeth and nearby Union County communities.</p></div>
<div class="card"><h3>Clear next steps</h3><p>Quote and proposal paths that set expectations before you commit.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready for a home improvement quote?</h2>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    "What is Elizabeth Handyman Home Improvements?",
                    "Elizabeth Handyman Home Improvements specializes in additions, decks, basement finishing, kitchen remodeling, bathroom remodeling, and general handyman services in Elizabeth, NJ — plus drywall, flooring, doors, and outdoor improvements.",
                ),
                (
                    "Who operates Elizabeth Handyman Home Improvements?",
                    f"Elizabeth Handyman Home Improvements is operated by {OPERATOR}, with headquarters listed at {ADDRESS} [confirm].",
                ),
                (
                    "How do I request a quote?",
                    "Use the Request a Quote form or call us. Describe the project, property type, and urgency — we follow up with next steps.",
                ),
                (
                    "Do you serve areas outside Elizabeth?",
                    "Elizabeth, NJ is the primary focus. Nearby communities may be served case by case — see Service Areas [confirm coverage].",
                ),
                (
                    "Are you licensed and insured?",
                    "Licensed and insured status is listed as [confirm] pending owner verification — ask during your quote conversation.",
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
            f"{h['name']} | Elizabeth Handyman Home Improvements",
            f"{h['name']} from Elizabeth Handyman Home Improvements in Elizabeth, NJ — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} in Elizabeth, NJ</h2>
<p class="lead">{escape(h["blurb"])} Part of Elizabeth Handyman Home Improvements — additions, decks, remodels, and handyman services under one local roof.</p>
<p><a class="btn" href="../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Services We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What a typical engagement can include</h2>
<ul class="checks">
<li>Clear description of the addition, remodel, or handyman scope</li>
<li>On-site review before major tear-out recommendations</li>
<li>Repair-vs-remodel options explained in plain language</li>
<li>Written next steps after the quote or proposal path</li>
<li>Elizabeth, NJ focus — no generic national boilerplate</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with Request a Quote. For larger additions or multi-room remodels, use Request a Proposal.",
                ),
                (
                    "Where is Elizabeth Handyman Home Improvements based?",
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
            f"{name} | Elizabeth Handyman Home Improvements",
            f"{name} from Elizabeth Handyman Home Improvements in Elizabeth, NJ — {blurb}",
        )
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(name)} for Elizabeth, NJ homes and businesses</h2>
<p class="lead">{escape(blurb)} At Elizabeth Handyman Home Improvements, {escape(name.lower())} is delivered as part of a local home-improvement shop — clear scope, practical options, and a quote path before you commit.</p>
<p><a class="btn" href="../../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(name)} with Elizabeth Handyman Home Improvements can help you gain:</h2>
<ul class="checks">
<li>Faster clarity on whether a focused fix or fuller remodel is the smarter path</li>
<li>Local Elizabeth, NJ focus instead of generic national copy</li>
<li>One team for related additions, decks, remodel, and handyman work</li>
<li>Written quote or proposal steps before major work</li>
<li>Honest scope — no invented testimonials or wait-time guarantees</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} path scoped to your property — not a one-size package</h2>
<p>No two homes need {escape(name.lower())} the same way. We match access, materials, and project goals — then confirm next steps before work begins.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Homeowners avoid key risks with a developed local path for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with ad-hoc handyman fixes</h3><ul>
<li>Symptom fixes that ignore the real structural or finish cause</li>
<li>Surprise upsells after walls or decks are already opened</li>
<li>No written scope before major remodel spend</li>
<li>National call centers that do not know Elizabeth access realities</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on Elizabeth Handyman Home Improvements</h3><ul>
<li>Additions, decks, remodels, and handyman coverage under local pages</li>
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
                    "Timing depends on project size and crew availability. Urgent punch-list work is prioritized; larger additions and remodels are scheduled after the quote conversation — no invented same-day guarantees.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Price depends on materials, access, and whether repair or fuller remodel is required. Use Request a Quote for an estimate path.",
                ),
                (
                    f"Why choose Elizabeth Handyman Home Improvements for {name.lower()}?",
                    f"We deliver {name.lower()} inside a local home-improvement shop focused on Elizabeth, NJ — with clear quote and proposal steps.",
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
<h2 style="font-size:20px">Initiate a request with Elizabeth Handyman Home Improvements</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us the project</h3><p>Addition, deck, basement, kitchen, bath, or handyman list — plus property type.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>A quote path, a proposal for larger work, or honest advice on next steps.</p></div>
<div class="card"><h3>3. Schedule when ready</h3><p>Confirm scope in writing before work begins.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>Elizabeth Handyman Home Improvements</strong><br>Operated by {escape(OPERATOR)} <em>[confirm]</em><br>Headquarters: {escape(ADDRESS)} <em>[confirm]</em><br>Phone: {escape(PHONE)}<br>Email: {escape(EMAIL)} <em>[confirm]</em></p>
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
        ["/", "HOME", "", "elizabeth handyman home improvements", "logo/home", "A1,A6,A10", ""],
        [
            "/about-elizabeth-handyman/",
            "COMP-HUB",
            "/",
            "about elizabeth handyman home improvements",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-elizabeth-handyman/why-choose-us/",
            "COMP-CHILD",
            "/about-elizabeth-handyman/",
            "why choose elizabeth handyman home improvements",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-elizabeth-handyman/service-areas/",
            "COMP-CHILD",
            "/about-elizabeth-handyman/",
            "elizabeth nj handyman service areas",
            "About menu",
            "F1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact elizabeth handyman",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "home improvement proposal elizabeth nj",
            "nav utility",
            "I1",
            "Request for Proposal",
        ],
        [
            "/request-a-quote/",
            "FORM-CONSULT",
            "/",
            "handyman quote elizabeth nj",
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
    with (ROOT / "ELIZABETHHANDYMAN-PAGE-INVENTORY.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
        "ELIZABETHHANDYMAN-QUESTIONNAIRE-ANSWERS.md",
        "ELIZABETHHANDYMAN-PAGE-INVENTORY.csv",
        "ELIZABETHHANDYMAN-NOTES.md",
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
        ROOT / "about-elizabeth-handyman" / "index.html",
        head(
            "About Elizabeth Handyman Home Improvements | Elizabeth, NJ",
            "Elizabeth Handyman Home Improvements specializes in additions, decks, basement finishing, kitchen and bathroom remodeling, and general handyman services in Elizabeth, NJ.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About Elizabeth Handyman Home Improvements</h2>
<p class="lead">Elizabeth Handyman Home Improvements specializes in additions, decks, basement finishing, kitchen remodeling, bathroom remodeling, and general handyman services in Elizabeth, NJ — operated by {escape(OPERATOR)} from {escape(ADDRESS)} <em>[confirm]</em>.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>We focus on local home-improvement demand: room additions, deck building and repair, basement finishing, kitchen and bathroom remodeling, general handyman work, drywall and painting, flooring and carpentry, doors and windows, and outdoor improvements.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="service-areas/index.html">Service areas &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "Who operates Elizabeth Handyman Home Improvements?",
                    f"Elizabeth Handyman Home Improvements is operated by {OPERATOR}, headquartered at {ADDRESS} [confirm].",
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
    urls.append("/about-elizabeth-handyman/")

    write(
        ROOT / "about-elizabeth-handyman" / "why-choose-us" / "index.html",
        head(
            "Why Choose Elizabeth Handyman Home Improvements",
            "Why homeowners choose Elizabeth Handyman Home Improvements in Elizabeth, NJ.",
        )
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose Elizabeth Handyman Home Improvements</h2>
<p class="lead">A local home-improvement shop built around additions, decks, basement finishing, kitchen and bathroom remodeling, and general handyman services — without invented testimonials.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Owner specialties</h3><p>Additions, decks, basement finishing, kitchen remodeling, bathroom remodeling, and general handyman work.</p></div>
<div class="card"><h3>Elizabeth, NJ focus</h3><p>Pages and routing written for local intent — not national boilerplate.</p></div>
<div class="card"><h3>Quote-led intake</h3><p>Request a Quote first; larger jobs can move to a written proposal.</p></div>
<div class="card"><h3>Clear service map</h3><p>Ten hubs × ten children so visitors land on the right project page.</p></div>
<div class="card"><h3>Honest staging copy</h3><p>No fabricated reviews, awards, or wait-time guarantees in this build. Licensed &amp; insured noted as [confirm].</p></div>
<div class="card"><h3>Named operator</h3><p>Race Computer Services accountability for this factory build [confirm].</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-elizabeth-handyman/why-choose-us/")

    areas = "".join(
        f'<div class="gcard"><h3>{escape(a)}</h3><p>Home improvement and handyman inquiries for {escape(a)} — coverage confirmed case by case.</p></div>'
        for a in SERVICE_AREAS
    )
    write(
        ROOT / "about-elizabeth-handyman" / "service-areas" / "index.html",
        head(
            "Service Areas | Elizabeth Handyman Home Improvements",
            "Service areas for Elizabeth Handyman Home Improvements — Elizabeth, NJ and nearby communities.",
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
    urls.append("/about-elizabeth-handyman/service-areas/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | Elizabeth Handyman Home Improvements",
            "Contact Us for Home Improvement Inquiries",
            "Tell us the project, your Elizabeth-area property type, and whether you need a soon path or a planned estimate.",
        ),
        (
            "request-a-quote",
            "Request a Quote | Elizabeth Handyman Home Improvements",
            "Request a Home Improvement or Handyman Quote",
            "Describe the addition, deck, remodel, or handyman list — we follow up with clear next steps.",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | Elizabeth Handyman Home Improvements",
            "Request a Proposal for Larger Remodel or Addition Work",
            "Share multi-room remodel, addition, or multi-unit goals. We return a scoped proposal you can compare.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | Elizabeth Handyman Home Improvements", "Page not found.")
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
        ROOT / "ELIZABETHHANDYMAN-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — Elizabeth Handyman Home Improvements (FACTORY BUILD · Gate 1 10×10)

**Build uses NearMe OS Website Factory instructions-template (SEO Cow staging engine) · category: home additions, decks, remodels & handyman services · Elizabeth NJ local trade · Race Computer Services S1 defaults · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | Elizabeth Handyman Home Improvements (operated by Race Computer Services, LLC) | this build [confirm] |
| A2 domain | elizabethhandyman.com | [confirm] |
| A3 phone | {PHONE} | Race CS / S1 (same operator) |
| A4 email | {EMAIL} | [confirm] |
| A5 address | {ADDRESS} | Race CS default [confirm] |
| A6 trade | Home additions, decks, remodels & handyman services | this build |
| A7 founded | not stated — omitted | — |
| A10 value_proposition | Specializing in additions, decks, basement finishing, kitchen remodeling, bathroom remodeling, and general handyman services in Elizabeth, NJ | this build |
| A11 tagline | {TAGLINE} | this build |
| A12 competitor_type | national handyman brands, marketplace lead-gen, unclassified local contractors | [confirm] |
| A13 hours | not stated — omitted | — |
| licensed_insured | Licensed & insured | [confirm] |

## B — Services: 10 categories × 10 children
{hub_slugs} — full map in ELIZABETHHANDYMAN-PAGE-INVENTORY.csv.
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
        ROOT / "ELIZABETHHANDYMAN-NOTES.md",
        f"""# Elizabeth Handyman Home Improvements — Factory Build

Local trade category: **home additions, decks, remodels & handyman services** (Elizabeth, NJ).

- Generator: `scripts/generate_elizabethhandyman_factory.py`
- Gate 1: 10 × 10 = 100 SVC-CHILD (+ chrome ≈ 117 pages)
- Brand: Elizabeth Handyman Home Improvements
- FORM-CONSULT: `/request-a-quote/` (highlighted)
- FORM-PRICING: `/request-a-proposal/`
- About: `/about-elizabeth-handyman/` · why-choose-us · service-areas
- Staging: noindex + STAGING PREVIEW banner
- Domain / email / NAP: elizabethhandyman.com · {EMAIL} · {ADDRESS} *[confirm]*
- CSS: forest green / wood amber (`#b45309` / `#14532d` / `#166534` / `#f7fee7` / `#fffbeb`)
- No invented testimonials; licensed & insured only as [confirm]; no LOC doorway pages
""",
    )

    pages = list(ROOT.rglob("index.html"))
    factory_pages = list(pages)
    print(f"Generated {len(factory_pages)} factory index pages")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)} · Children: {sum(len(h['children']) for h in HUBS)}")


if __name__ == "__main__":
    main()
