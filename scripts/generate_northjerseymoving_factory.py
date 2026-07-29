#!/usr/bin/env python3
"""Generate North Jersey Moving Services site using the NearMe OS Website Factory template
(same HTML/CSS engine as the SEO Cow / Car Rental Near Me staging builds).

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: local & long-distance moving services (North Jersey).
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
BASE = "https://northjerseymovingservices.com"  # [confirm]
PHONE = "(862) 295-0011"
PHONE_TEL = "+18622950011"
EMAIL = "info@northjerseymovingservices.com"  # [confirm]
HQ = "North Jersey"
ADDRESS = "12 Sayre St, Elizabeth, NJ 07208"  # Race CS default hub [confirm]
OPERATOR = "Race Computer Services, LLC"  # [confirm]
TAGLINE = "Local & Long-Distance Moving Across North Jersey"
STAGING_BANNER = (
    "STAGING PREVIEW — North Jersey Moving Services factory build · North Jersey · "
    "content pending owner review"
)

# NearMe factory CSS (SEO Cow template) with navy / moving-orange remap
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#152238;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#c2410c;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#0f2744;color:#ffedd5;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#1e3a5f;color:#e2e8f0;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #ea580c;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#0f2744}.logo span{color:#ea580c}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#0f2744}
.phone-cta small{display:block;color:#5a6b7b;font-size:11px}
nav.nav{background:#0f2744}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav>div.wrap>ul>li>a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav>div.wrap>ul>li>a:hover{background:#1e3a5f;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #ea580c;z-index:60}
nav.nav .dd a{display:block;color:#0f2744;padding:10px 15px;font-size:13.5px;font-weight:500;border-bottom:1px solid #ffedd5;background:#fff}
nav.nav .dd a:hover{background:#fff7ed;color:#0f2744;text-decoration:none}
nav.nav>div.wrap>ul>li.em>a{background:#ea580c}
nav.nav>div.wrap>ul>li.em>a:hover{background:#c2410c}
.hero{background:linear-gradient(rgba(15,39,68,.86),rgba(15,39,68,.86)),repeating-linear-gradient(45deg,#0f2744 0 14px,#1e3a5f 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#ffedd5;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#ea580c;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#c2410c;text-decoration:none}
.btn.alt{background:#0f2744;color:#fff}.btn.alt:hover{background:#1e3a5f}
section{padding:44px 0}
section.tint{background:#fff7ed}
section h2{font-size:25px;color:#0f2744;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#ea580c;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #ffedd5;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(15,39,68,.06)}
.card h3{color:#0f2744;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #ffedd5;border-left:4px solid #ea580c;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#0f2744}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#c2410c}
.ctastrip{background:#0f2744;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #ffedd5;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#fff7ed}.vs .col.good{background:#fff7ed}
.vs h3{font-size:16px;margin-bottom:12px;color:#0f2744}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#ea580c;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #ffedd5;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#0f2744;list-style:none}
details summary:before{content:"+ ";color:#ea580c;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #ffedd5;border-top:4px solid #ea580c;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#44525f;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5a6b7b;padding:14px 0 0}
.crumb a{color:#5a6b7b}
footer{background:#0f2744;color:#c9b8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #1e3a5f;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #ffedd5;border-top:4px solid #ea580c;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#0f2744}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #ffedd5;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(234,88,12,.08)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#0f2744}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#ea580c;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#ea580c;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#0f2744}
"""

# Gate 1 — 10 × 10 moving services (North Jersey focus; no LOC doorway pages)
HUBS = [{'slug': 'local-moving', 'name': 'Local Moving', 'short': 'Local', 'blurb': 'Same-day and short-haul moves across North Jersey towns and counties.', 'children': [('same-day-local-moves', 'Same-Day Local Moves', 'Tight local schedules when the move window is short [confirm availability].'), ('in-town-apartment-moves', 'In-Town Apartment Moves', 'Efficient apartment moves within the same North Jersey town.'), ('house-to-house-local-moves', 'House-to-House Local Moves', 'Full-home local relocates with truck, crew, and load planning.'), ('cross-county-north-jersey-moves', 'Cross-County North Jersey Moves', 'Bergen, Essex, Hudson, Passaic, Morris, and nearby county hops.'), ('studio-one-bedroom-local-moves', 'Studio & One-Bedroom Local Moves', 'Right-sized crews for smaller local inventories.'), ('multi-stop-local-moves', 'Multi-Stop Local Moves', 'Pickup, drop, and intermediate stops planned into one day.'), ('last-minute-local-moves', 'Last-Minute Local Moves', 'Urgent local help when leases or closings move up [confirm].'), ('weekend-local-moving', 'Weekend Local Moving', 'Saturday and Sunday local move windows when weekdays are tight.'), ('hourly-local-moving', 'Hourly Local Moving', 'Hourly local crew options for flexible small jobs [confirm].'), ('local-move-planning', 'Local Move Planning', 'Inventory, access, and timing planned before truck day.')]}, {'slug': 'long-distance-moving', 'name': 'Long-Distance Moving', 'short': 'Long Distance', 'blurb': 'Interstate and longer hauls originating from North Jersey homes and offices.', 'children': [('interstate-moving-from-north-jersey', 'Interstate Moving from North Jersey', 'State-to-state moves starting in North Jersey [confirm licensing].'), ('northeast-corridor-moves', 'Northeast Corridor Moves', 'NY, PA, CT, and regional corridor relocates.'), ('long-distance-home-moves', 'Long-Distance Home Moves', 'Full household packing and transport for longer routes.'), ('long-distance-apartment-moves', 'Long-Distance Apartment Moves', 'Apartment inventories planned for longer transit windows.'), ('partial-load-long-distance', 'Partial-Load Long Distance', 'Shared or partial-load options when timing allows [confirm].'), ('dedicated-truck-long-distance', 'Dedicated Truck Long Distance', 'Dedicated truck routing for tighter delivery windows.'), ('long-distance-move-estimates', 'Long-Distance Move Estimates', 'Inventory-based estimates before you commit to a long haul.'), ('vehicle-transport-coordination', 'Vehicle Transport Coordination', 'Coordinate car shipping alongside household goods [confirm partner].'), ('long-distance-delivery-windows', 'Long-Distance Delivery Windows', 'Clear delivery window expectations for interstate jobs.'), ('storage-in-transit', 'Storage-in-Transit', 'Short holds when origin and destination dates do not align.')]}, {'slug': 'residential-moving', 'name': 'Residential Moving', 'short': 'Residential', 'blurb': 'Home moves for houses, townhomes, and family households across North Jersey.', 'children': [('full-service-home-moving', 'Full-Service Home Moving', 'Pack, load, transport, and unload for whole-home relocates.'), ('bedroom-by-bedroom-moves', 'Bedroom-by-Bedroom Moves', 'Room-sequenced packing and loading that keeps inventory organized.'), ('family-home-relocation', 'Family Home Relocation', 'School-year and family schedule aware move planning.'), ('townhouse-moving', 'Townhouse Moving', 'Narrow access and shared-wall townhome logistics.'), ('basement-attic-move-help', 'Basement & Attic Move Help', 'Clear storage zones that often delay truck day.'), ('garage-and-outdoor-moves', 'Garage & Outdoor Moves', 'Tools, patio furniture, and yard gear loaded safely.'), ('downsizing-home-moves', 'Downsizing Home Moves', 'Right-size the truck when the new home is smaller.'), ('upsizing-home-moves', 'Upsizing Home Moves', 'Extra volume planning when the destination is larger.'), ('estate-cleanout-moves', 'Estate Cleanout Moves', 'Coordinate moves with estate or cleanout timelines [confirm].'), ('residential-move-checklists', 'Residential Move Checklists', 'Practical checklists so nothing critical is left behind.')]}, {'slug': 'commercial-office-moving', 'name': 'Commercial & Office Moving', 'short': 'Commercial', 'blurb': 'Office, retail, and light commercial moves with after-hours options for North Jersey businesses.', 'children': [('office-relocation', 'Office Relocation', 'Desks, IT staging, and phased office moves with less downtime.'), ('small-business-moving', 'Small Business Moving', 'Storefront and suite moves sized for local operators.'), ('retail-store-moving', 'Retail Store Moving', 'Fixtures, inventory, and display moves for retail spaces.'), ('medical-office-moving', 'Medical Office Moving', 'Careful handling for clinics and professional suites [confirm specialty needs].'), ('weekend-office-moves', 'Weekend Office Moves', 'Weekend windows that protect weekday operations.'), ('after-hours-commercial-moves', 'After-Hours Commercial Moves', 'Evening commercial moves when daytime access is limited.'), ('cubicle-and-furniture-moves', 'Cubicle & Furniture Moves', 'Disassemble, protect, and reassemble office furniture.'), ('file-and-records-moving', 'File & Records Moving', 'Labeled records moves that keep retrieval sane.'), ('it-equipment-move-support', 'IT Equipment Move Support', 'Protect monitors, servers, and peripherals during transit.'), ('commercial-move-project-planning', 'Commercial Move Project Planning', 'Floor plans, elevators, and loading dock timing before truck day.')]}, {'slug': 'packing-services', 'name': 'Packing Services', 'short': 'Packing', 'blurb': 'Full and partial packing so North Jersey moves load faster and arrive intact.', 'children': [('full-home-packing', 'Full-Home Packing', 'Room-by-room packing before the truck arrives.'), ('partial-packing-services', 'Partial Packing Services', 'Pack only kitchens, fragile rooms, or priority zones.'), ('fragile-item-packing', 'Fragile Item Packing', 'Dishes, glass, art, and fragile inventory packed with care.'), ('kitchen-packing', 'Kitchen Packing', 'Cabinets, pantry, and dish packing that protects glassware.'), ('wardrobe-packing', 'Wardrobe Packing', 'Hanging clothes packed to reduce wrinkles and rehang time.'), ('packing-supplies-delivery', 'Packing Supplies Delivery', 'Boxes, tape, and paper delivered ahead of pack day [confirm].'), ('custom-crate-packing', 'Custom Crate Packing', 'Crating for high-value or awkward items [confirm].'), ('labeling-and-inventory-packing', 'Labeling & Inventory Packing', 'Room labels and inventory notes for faster unloading.'), ('same-day-packing-help', 'Same-Day Packing Help', 'Packing labor when the move date is already set.'), ('eco-friendly-packing-options', 'Eco-Friendly Packing Options', 'Reusable bin and reduced-waste packing options [confirm].')]}, {'slug': 'loading-unloading', 'name': 'Loading & Unloading', 'short': 'Loading', 'blurb': 'Labor-focused loading and unloading when you already have a truck or portable container.', 'children': [('loading-help-only', 'Loading Help Only', 'Crew loads your truck or container at origin.'), ('unloading-help-only', 'Unloading Help Only', 'Crew unloads at destination into the right rooms.'), ('pod-and-container-loading', 'POD & Container Loading', 'Load portable storage containers efficiently and safely.'), ('truck-loading-services', 'Truck Loading Services', 'Weight-balanced truck loading that protects freight.'), ('furniture-wrapping-loading', 'Furniture Wrapping & Loading', 'Pads, wrap, and secure furniture before it rolls.'), ('stair-carry-loading', 'Stair Carry Loading', 'Walk-up and stair carries planned for crew size.'), ('elevator-building-loading', 'Elevator Building Loading', 'Elevator reservations and building rules respected.'), ('heavy-item-loading', 'Heavy Item Loading', 'Appliances and dense items loaded with proper equipment.'), ('rental-truck-labor', 'Rental Truck Labor', 'Labor for U-Haul-style rental trucks [brand-agnostic].'), ('origin-and-destination-labor', 'Origin & Destination Labor', 'Load at one address and unload at another without driving your truck.')]}, {'slug': 'apartment-condo-moving', 'name': 'Apartment & Condo Moving', 'short': 'Apartments', 'blurb': 'High-rise and walk-up apartment and condo moves across North Jersey cities.', 'children': [('high-rise-apartment-moves', 'High-Rise Apartment Moves', 'Elevator timing and loading dock rules for tall buildings.'), ('walk-up-apartment-moves', 'Walk-Up Apartment Moves', 'Stair-heavy walk-ups with the right crew count.'), ('condo-association-moves', 'Condo Association Moves', 'HOA windows, certificates, and building requirements [confirm].'), ('studio-apartment-moving', 'Studio Apartment Moving', 'Compact inventories moved without over-trucking.'), ('luxury-condo-moving', 'Luxury Condo Moving', 'Protective floor and doorway care for finished condo spaces.'), ('jersey-city-apartment-moves', 'Jersey City Apartment Moves', 'Jersey City building access and street loading realities.'), ('newark-apartment-moves', 'Newark Apartment Moves', 'Newark apartment moves with urban access planning.'), ('certificate-of-insurance-moves', 'Certificate of Insurance Moves', 'COI-ready building moves when management requires proof [confirm].'), ('short-notice-apartment-moves', 'Short-Notice Apartment Moves', 'Lease-driven apartment moves on compressed timelines.'), ('furniture-placement-condo-moves', 'Furniture Placement Condo Moves', 'Unload into rooms with basic placement — not full design staging.')]}, {'slug': 'specialty-item-moving', 'name': 'Specialty Item Moving', 'short': 'Specialty', 'blurb': 'Pianos, safes, antiques, and awkward specialty items that need extra care.', 'children': [('piano-moving', 'Piano Moving', 'Upright and grand piano moves with proper equipment [confirm].'), ('safe-moving', 'Safe Moving', 'Heavy safe relocation with floor protection and gear.'), ('antique-furniture-moving', 'Antique Furniture Moving', 'Older furniture protected against scratches and stress points.'), ('art-and-mirror-moving', 'Art & Mirror Moving', 'Framed art and mirrors packed and transported upright.'), ('gym-equipment-moving', 'Gym Equipment Moving', 'Treadmills, racks, and weight gear disassembled as needed.'), ('pool-table-moving', 'Pool Table Moving', 'Slate and frame pool table moves with specialty handling [confirm].'), ('hot-tub-spa-moving', 'Hot Tub & Spa Moving', 'Exterior path planning for spas and hot tubs [confirm].'), ('gun-safe-appliance-moves', 'Gun Safe & Appliance Moves', 'Dense safes and large appliances moved with straps and dollies.'), ('fragile-collectibles-moving', 'Fragile Collectibles Moving', 'Collectibles packed and labeled for careful transit.'), ('single-item-specialty-moves', 'Single-Item Specialty Moves', 'One hard item when you do not need a full household crew.')]}, {'slug': 'storage-solutions', 'name': 'Storage Solutions', 'short': 'Storage', 'blurb': 'Short-term storage and hold options that bridge gaps between move dates.', 'children': [('short-term-moving-storage', 'Short-Term Moving Storage', 'Hold household goods between lease or closing dates.'), ('warehouse-storage-holds', 'Warehouse Storage Holds', 'Secure warehouse holds for staged deliveries [confirm facility].'), ('storage-then-delivery', 'Storage-Then-Delivery', 'Store first, deliver when the new address is ready.'), ('partial-inventory-storage', 'Partial Inventory Storage', 'Store overflow while essential rooms are set up.'), ('climate-consideration-storage', 'Climate-Consideration Storage', 'Guidance when items need better environmental care [confirm].'), ('business-inventory-storage', 'Business Inventory Storage', 'Short commercial inventory holds during suite transitions.'), ('seasonal-item-storage-moves', 'Seasonal Item Storage Moves', 'Move seasonal gear into and out of storage cleanly.'), ('storage-unit-loading', 'Storage Unit Loading', 'Load or unload third-party storage units with a crew.'), ('move-delay-storage', 'Move-Delay Storage', 'Bridge unexpected delays without leaving goods roadside.'), ('inventory-documented-storage', 'Inventory-Documented Storage', 'Labeled holds so retrieval is faster at delivery.')]}, {'slug': 'senior-assisted-moving', 'name': 'Senior & Assisted Moving', 'short': 'Senior', 'blurb': 'Patient, paced moves for seniors, downsizing, and assisted living transitions.', 'children': [('senior-home-moving', 'Senior Home Moving', 'Lower-stress senior household moves with clearer pacing.'), ('downsizing-for-seniors', 'Downsizing for Seniors', 'Sort, pack, and move what matters — leave the rest planned.'), ('assisted-living-moves', 'Assisted Living Moves', 'Moves into assisted living with room-size awareness.'), ('independent-living-community-moves', 'Independent Living Community Moves', 'Community move-in rules and elevator timing handled upfront.'), ('family-coordinated-senior-moves', 'Family-Coordinated Senior Moves', 'Keep adult children and caregivers aligned on timing.'), ('packing-help-for-seniors', 'Packing Help for Seniors', 'Packing labor that reduces lifting for older adults.'), ('furniture-placement-senior-moves', 'Furniture Placement Senior Moves', 'Basic placement so the new room is usable on day one.'), ('estate-to-senior-housing-moves', 'Estate-to-Senior-Housing Moves', 'Coordinate moves out of a family home into senior housing.'), ('accessible-path-move-planning', 'Accessible Path Move Planning', 'Plan paths, stairs, and access for safer carries.'), ('compassionate-move-day-support', 'Compassionate Move-Day Support', 'Calm move-day communication when the transition is emotional.')]}]

SERVICE_AREAS = ['Jersey City, NJ', 'Newark, NJ', 'Paterson, NJ', 'Elizabeth, NJ', 'Clifton, NJ', 'Passaic, NJ', 'Hackensack, NJ', 'Morristown, NJ', 'Paramus, NJ', 'Montclair, NJ', 'Hoboken, NJ', 'Union City, NJ']



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
<div class="logo">North Jersey <span>Moving</span><small>Moving Services · North Jersey</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Request a free move quote</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-north-jersey-moving/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-north-jersey-moving/index.html">About North Jersey Moving Services</a>
<a href="{p}about-north-jersey-moving/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-north-jersey-moving/service-areas/index.html">Service Areas</a>
</div></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li class="em"><a href="{p}request-a-quote/index.html">Get a Free Quote</a></li>
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
<li><a href="{p}about-north-jersey-moving/index.html">About North Jersey Moving Services</a></li>
<li><a href="{p}about-north-jersey-moving/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-north-jersey-moving/service-areas/index.html">Service Areas</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}request-a-quote/index.html">Get a Free Quote</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul><li>{escape(ADDRESS)} <em>[confirm]</em></li><li>Operated by {escape(OPERATOR)} <em>[confirm]</em></li><li>Serving North Jersey &amp; nearby</li></ul></div>
</div>
<div class="copy">North Jersey Moving Services &middot; {escape(OPERATOR)} &middot; {escape(HQ)} &middot; {escape(PHONE)}<br>
Copyright &copy; 2026. North Jersey Moving Services. All rights reserved.<br>
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
<label>Move Type</label><select><option>Please choose&hellip;</option><option>Local residential</option><option>Apartment / condo</option><option>Long distance</option><option>Commercial / office</option><option>Labor only</option><option>Not sure</option></select>
<label>Service Needed</label><select><option>Please choose&hellip;</option>{opts}<option>General moving question</option><option>Other</option></select>
<label>Move Timing</label><select><option>Please choose&hellip;</option><option>ASAP / this week</option><option>Within 2–4 weeks</option><option>Planning / estimate only</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f9588">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "MovingCompany",
        "name": "North Jersey Moving Services",
        "legalName": OPERATOR,
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "areaServed": {
            "@type": "AdministrativeArea",
            "name": "North Jersey",
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
            "North Jersey Moving Services | Local & Long-Distance Movers",
            "North Jersey Moving Services helps homeowners and businesses with local moves, apartment relocates, packing, loading, specialty items, storage, and long-distance moves across North Jersey.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>North Jersey Moving Services</h1>
<p>Local movers, apartment specialists, packing crews, and long-distance planning for North Jersey homes and businesses.</p>
<a class="btn" href="request-a-quote/index.html">Get a Free Quote</a> <a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>Local</b><span>Same-Town &amp; County</span></div>
<div class="stat"><b>Apartments</b><span>Walk-Ups &amp; High-Rises</span></div>
<div class="stat"><b>Packing</b><span>Full &amp; Partial</span></div>
<div class="stat"><b>Long Haul</b><span>Interstate Planning</span></div>
</div></div></section>
<section><div class="wrap"><h2>Moving services built for North Jersey access realities</h2>
<p class="lead">Ten service families — from local and residential moves through apartments, commercial relocates, packing, loading labor, specialty items, storage holds, senior moves, and long-distance planning.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure which move type you need? Start with a free quote.</h2>
<p style="margin-bottom:14px">Tell us origin, destination, inventory size, and timing — we help you choose the right crew path.</p>
<a class="btn" href="request-a-quote/index.html">Get a Free Quote</a></div></div>
<section><div class="wrap"><h2>How to get started</h2><div class="cols3">
<div class="card"><h3>1. Request a quote</h3><p>Share addresses, approximate rooms or inventory, and your preferred move window.</p></div>
<div class="card"><h3>2. Scope the move</h3><p>We clarify stairs, elevators, packing needs, and whether labor-only or full-service fits best.</p></div>
<div class="card"><h3>3. Lock the plan</h3><p>Confirm crew size and next steps in writing before move day — no invented arrival-time promises.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why North Jersey Moving Services</h2><div class="cols3">
<div class="card"><h3>North Jersey focus</h3><p>Urban access, building rules, and short-haul county moves written into the service map.</p></div>
<div class="card"><h3>Full move toolkit</h3><p>Local, long-distance, packing, loading, specialty items, storage, and senior-assisted paths.</p></div>
<div class="card"><h3>Clear quote path</h3><p>Free quote and proposal routes that set expectations before you commit.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready for a move quote?</h2>
<a class="btn" href="request-a-quote/index.html">Get a Free Quote</a> <a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    "What is North Jersey Moving Services?",
                    "North Jersey Moving Services is a local moving company covering local moves, apartments, packing, loading labor, specialty items, storage, senior-assisted moves, commercial relocates, and long-distance planning across North Jersey.",
                ),
                (
                    "Who operates North Jersey Moving Services?",
                    f"North Jersey Moving Services is operated by {OPERATOR}, with headquarters listed at {ADDRESS} [confirm].",
                ),
                (
                    "How do I get a free quote?",
                    "Use the Get a Free Quote form or call us. Share origin, destination, inventory size, and timing — we follow up with next steps.",
                ),
                (
                    "Do you only serve North Jersey?",
                    "North Jersey is the primary focus for local work. Long-distance routes may originate here and continue interstate — confirm coverage on your quote.",
                ),
                (
                    "Are you licensed and insured?",
                    "Licensed and insured status is listed as [confirm] pending owner verification — ask during your quote conversation. Interstate authority also marked [confirm].",
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
            f"{h['name']} | North Jersey Moving Services",
            f"{h['name']} from North Jersey Moving Services in North Jersey — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} in North Jersey</h2>
<p class="lead">{escape(h["blurb"])} Part of North Jersey Moving Services — local crews, packing options, and clear quote paths under one roof.</p>
<p><a class="btn" href="../request-a-quote/index.html">Get a Free Quote</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Services We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What a typical engagement can include</h2>
<ul class="checks">
<li>Clear description of inventory, access, and timing</li>
<li>Stairs, elevator, and loading-zone planning before truck day</li>
<li>Packing vs labor-only options explained in plain language</li>
<li>Written next steps after the quote or proposal path</li>
<li>North Jersey focus — no generic national boilerplate</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with Get a Free Quote. For larger commercial or multi-day jobs, use Request a Proposal.",
                ),
                (
                    "Where is North Jersey Moving Services based?",
                    f"Headquartered in {HQ} ({ADDRESS}) [confirm], focused on North Jersey and nearby communities.",
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
            f"{name} | North Jersey Moving Services",
            f"{name} from North Jersey Moving Services in North Jersey — {blurb}",
        )
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(name)} for North Jersey homes and businesses</h2>
<p class="lead">{escape(blurb)} At North Jersey Moving Services, {escape(name.lower())} is delivered as part of a local moving shop — clear scope, practical options, and a quote path before you commit.</p>
<p><a class="btn" href="../../request-a-quote/index.html">Get a Free Quote</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(name)} with North Jersey Moving Services can help you gain:</h2>
<ul class="checks">
<li>Faster clarity on crew size, packing needs, and truck day timing</li>
<li>Local North Jersey access planning instead of generic national copy</li>
<li>One team for related packing, loading, storage, and specialty work</li>
<li>Written quote or proposal steps before major move spend</li>
<li>Honest scope — no invented testimonials or arrival-time guarantees</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} path scoped to your addresses — not a one-size package</h2>
<p>No two moves need {escape(name.lower())} the same way. We match inventory, stairs/elevators, and timing — then confirm next steps before move day.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Households avoid key risks with a developed local path for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with ad-hoc moving help</h3><ul>
<li>Under-crewed trucks that blow the move window</li>
<li>Surprise packing fees after the truck is already booked</li>
<li>No written scope before a long-distance commitment</li>
<li>National call centers that do not know North Jersey building realities</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on North Jersey Moving Services</h3><ul>
<li>Local, apartment, packing, and specialty coverage under local pages</li>
<li>Quote and proposal paths before you commit</li>
<li>North Jersey service-area focus</li>
<li>Race Computer Services accountability for this factory build [confirm]</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>See next steps first — get a free quote</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} looks like for your move? Start with a free quote request.</p>
<a class="btn" href="../../request-a-quote/index.html">Get a Free Quote</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} is scheduled?",
                    "Timing depends on inventory size, access, and crew availability. Urgent local jobs are prioritized when possible; larger and long-distance moves are scheduled after the quote conversation — no invented same-day guarantees.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Price depends on inventory, stairs/elevators, packing needs, and distance. Use Get a Free Quote for an estimate path.",
                ),
                (
                    f"Why choose North Jersey Moving Services for {name.lower()}?",
                    f"We deliver {name.lower()} inside a local moving shop focused on North Jersey — with clear quote and proposal steps.",
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
<h2 style="font-size:20px">Initiate a request with North Jersey Moving Services</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us the move</h3><p>Origin, destination, approximate rooms/inventory, and timing.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>A quote path, a proposal for larger work, or honest advice on next steps.</p></div>
<div class="card"><h3>3. Schedule when ready</h3><p>Confirm crew plan in writing before move day.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>North Jersey Moving Services</strong><br>Operated by {escape(OPERATOR)} <em>[confirm]</em><br>Headquarters: {escape(ADDRESS)} <em>[confirm]</em><br>Phone: {escape(PHONE)}<br>Email: {escape(EMAIL)} <em>[confirm]</em></p>
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
        ["/", "HOME", "", "north jersey moving services", "logo/home", "A1,A6,A10", ""],
        [
            "/about-north-jersey-moving/",
            "COMP-HUB",
            "/",
            "about north jersey moving services",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-north-jersey-moving/why-choose-us/",
            "COMP-CHILD",
            "/about-north-jersey-moving/",
            "why choose north jersey moving services",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-north-jersey-moving/service-areas/",
            "COMP-CHILD",
            "/about-north-jersey-moving/",
            "north jersey movers service areas",
            "About menu",
            "F1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact north jersey moving services",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "moving proposal north jersey",
            "nav utility",
            "I1",
            "Request for Proposal",
        ],
        [
            "/request-a-quote/",
            "FORM-CONSULT",
            "/",
            "moving quote north jersey",
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
                h["name"].lower() + " north jersey",
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
                    n.lower() + " north jersey",
                    "Services menu > hub grid",
                    "B row",
                    "Request for Proposal",
                ]
            )
    with (ROOT / "NORTHJERSEYMOVING-PAGE-INVENTORY.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
        "NORTHJERSEYMOVING-QUESTIONNAIRE-ANSWERS.md",
        "NORTHJERSEYMOVING-PAGE-INVENTORY.csv",
        "NORTHJERSEYMOVING-NOTES.md",
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
        ROOT / "about-north-jersey-moving" / "index.html",
        head(
            "About North Jersey Moving Services | North Jersey Movers",
            "North Jersey Moving Services helps with local moves, apartments, packing, loading, specialty items, storage, senior moves, commercial relocates, and long-distance planning.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About North Jersey Moving Services</h2>
<p class="lead">North Jersey Moving Services is a local moving company for residential, apartment, commercial, packing, loading, specialty, storage, senior-assisted, and long-distance paths — operated by {escape(OPERATOR)} from {escape(ADDRESS)} <em>[confirm]</em>.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>We focus on North Jersey move demand: local house and apartment relocates, commercial office moves, packing and loading labor, specialty item handling, short-term storage holds, senior-assisted transitions, and long-distance planning from a North Jersey origin.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="service-areas/index.html">Service areas &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "Who operates North Jersey Moving Services?",
                    f"North Jersey Moving Services is operated by {OPERATOR}, headquartered at {ADDRESS} [confirm].",
                ),
                (
                    "Do you work outside North Jersey?",
                    "North Jersey is the primary local focus. Long-distance routes may continue interstate — confirm on your quote.",
                ),
            ]
        )
        + org_schema()
        + footer(1),
    )
    urls.append("/about-north-jersey-moving/")

    write(
        ROOT / "about-north-jersey-moving" / "why-choose-us" / "index.html",
        head(
            "Why Choose North Jersey Moving Services",
            "Why homeowners choose North Jersey Moving Services in North Jersey.",
        )
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose North Jersey Moving Services</h2>
<p class="lead">A local moving shop built around North Jersey access realities — without invented testimonials.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Local + long-distance map</h3><p>Short-haul county moves and interstate planning under one service surface.</p></div>
<div class="card"><h3>Apartment-ready</h3><p>Walk-ups, high-rises, COI buildings, and elevator timing called out explicitly.</p></div>
<div class="card"><h3>Quote-led intake</h3><p>Get a Free Quote first; larger jobs can move to a written proposal.</p></div>
<div class="card"><h3>Clear service map</h3><p>Ten hubs × ten children so visitors land on the right project page.</p></div>
<div class="card"><h3>Honest staging copy</h3><p>No fabricated reviews, awards, or arrival-time guarantees in this build. Licensed &amp; insured noted as [confirm].</p></div>
<div class="card"><h3>Named operator</h3><p>Race Computer Services accountability for this factory build [confirm].</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-north-jersey-moving/why-choose-us/")

    areas = "".join(
        f'<div class="gcard"><h3>{escape(a)}</h3><p>Moving inquiries for {escape(a)} — coverage confirmed case by case.</p></div>'
        for a in SERVICE_AREAS
    )
    write(
        ROOT / "about-north-jersey-moving" / "service-areas" / "index.html",
        head(
            "Service Areas | North Jersey Moving Services",
            "Service areas for North Jersey Moving Services — major North Jersey cities and nearby communities.",
        )
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Service Areas</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Service Areas</h2>
<p class="lead">Primary focus: North Jersey. Communities listed below may be served case by case — no LOC doorway pages in this Gate 1 build.</p>
<div class="grid">{areas}</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-north-jersey-moving/service-areas/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | North Jersey Moving Services",
            "Contact Us for Moving Inquiries",
            "Tell us origin, destination, inventory size, and whether you need a soon path or a planned estimate.",
        ),
        (
            "request-a-quote",
            "Get a Free Quote | North Jersey Moving Services",
            "Get a Free Moving Quote",
            "Describe the move — addresses, rooms or inventory, packing needs, and timing — we follow up with clear next steps.",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | North Jersey Moving Services",
            "Request a Proposal for Larger or Commercial Moves",
            "Share multi-day, commercial, or complex specialty goals. We return a scoped proposal you can compare.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | North Jersey Moving Services", "Page not found.")
        + chrome(0)
        + """
<section style="padding:72px 0"><div class="wrap"><h2 style="font-size:28px">Page not found</h2>
<p class="lead">That URL is not on this site. Try home or get a free quote.</p>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn alt" href="request-a-quote/index.html">Get a Free Quote</a></p>
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
        ROOT / "NORTHJERSEYMOVING-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — North Jersey Moving Services (FACTORY BUILD · Gate 1 10×10)

**Build uses NearMe OS Website Factory instructions-template (SEO Cow staging engine) · category: local & long-distance moving · North Jersey · Race Computer Services S1 defaults · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | North Jersey Moving Services (operated by Race Computer Services, LLC) | this build [confirm] |
| A2 domain | northjerseymovingservices.com | [confirm] |
| A3 phone | {PHONE} | Race CS / S1 (same operator) |
| A4 email | {EMAIL} | [confirm] |
| A5 address | {ADDRESS} | Race CS default [confirm] |
| A6 trade | Local & long-distance moving services | this build |
| A7 founded | not stated — omitted | — |
| A10 value_proposition | Local movers, apartment specialists, packing crews, and long-distance planning for North Jersey | this build |
| A11 tagline | {TAGLINE} | this build |
| A12 competitor_type | national van lines, marketplace lead-gen, unclassified local movers | [confirm] |
| A13 hours | not stated — omitted | — |
| licensed_insured | Licensed & insured / interstate authority | [confirm] |

## B — Services: 10 categories × 10 children
{hub_slugs} — full map in NORTHJERSEYMOVING-PAGE-INVENTORY.csv.
FORM-CONSULT = `request-a-quote` · FORM-PRICING = `request-a-proposal`.

## C–I
- D1 audiences: homeowners, renters, landlords, small commercial, seniors/families
- F1 service_area: North Jersey primary; listed cities case by case (no LOC doorway pages)
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
        ROOT / "NORTHJERSEYMOVING-NOTES.md",
        f"""# North Jersey Moving Services — Factory Build

Local service category: **moving services** (North Jersey).

- Generator: `scripts/generate_northjerseymoving_factory.py`
- Gate 1: 10 × 10 = 100 SVC-CHILD (+ chrome ≈ 117 pages)
- Brand: North Jersey Moving Services
- FORM-CONSULT: `/request-a-quote/` (highlighted — Get a Free Quote)
- FORM-PRICING: `/request-a-proposal/`
- About: `/about-north-jersey-moving/` · why-choose-us · service-areas
- Staging: noindex + STAGING PREVIEW banner
- Domain / email / NAP: northjerseymovingservices.com · {EMAIL} · {ADDRESS} *[confirm]*
- CSS: navy / moving orange (`#0f2744` / `#1e3a5f` / `#ea580c` / `#fff7ed` / `#ffedd5`)
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
