#!/usr/bin/env python3
"""Generate Car Rental Near Me site using the NearMe OS Website Factory template
(same HTML/CSS engine as the SEO Cow / Red Rabbit / Car Rental Near Me staging builds).

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: car rental / local mobility (Track B vertical demo).
Facts grounded from Car Rental Near Me product landing + Race Computer Services S1.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://carrentalnearme.com"
PHONE = "(862) 295-0011"
PHONE_TEL = "+18622950011"
EMAIL = "info@carrentalnearme.com"  # [confirm]
HQ = "Elizabeth, NJ"
ADDRESS = "12 Sayre St, Elizabeth, NJ 07208"
OPERATOR = "Race Computer Services, LLC"
TAGLINE = "Cars Near You. Booked in Minutes."
STAGING_BANNER = (
    "STAGING PREVIEW — carrentalnearme.com factory build · content pending owner review "
    "· not the live Car Rental Near Me website"
)

# NearMe factory CSS (SEO Cow template) with Car Rental Near Me orange remap
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#134e4a;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#0f766e;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#042f2e;color:#99f6e4;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#115e59;color:#ccfbf1;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #0d9488;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#134e4a}.logo span{color:#0d9488}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#134e4a}
.phone-cta small{display:block;color:#5a6b7b;font-size:11px}
nav.nav{background:#115e59}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#0f3d3a;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #0d9488;z-index:60}
.dd a{color:#134e4a;padding:10px 15px;font-weight:500;border-bottom:1px solid #d1fae5}
.dd a:hover{background:#ecfdf5}
.nav .em a{background:#0d9488}.nav .em a:hover{background:#0f766e}
.hero{background:linear-gradient(rgba(6,40,38,.82),rgba(6,40,38,.82)),repeating-linear-gradient(45deg,#115e59 0 14px,#0f766e 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#99f6e4;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#0d9488;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#f07a3a;text-decoration:none}
.btn.alt{background:#115e59;color:#fff}.btn.alt:hover{background:#7a3c1a}
section{padding:44px 0}
section.tint{background:#f0fdfa}
section h2{font-size:25px;color:#134e4a;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#0d9488;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #d1e7e3;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(6,40,38,.06)}
.card h3{color:#134e4a;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #d1e7e3;border-left:4px solid #0d9488;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#134e4a}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#0f766e}
.ctastrip{background:#115e59;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #d1e7e3;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#f0fdfa}.vs .col.good{background:#f0fdfa}
.vs h3{font-size:16px;margin-bottom:12px;color:#134e4a}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#0f766e;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #d1e7e3;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#134e4a;list-style:none}
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
footer{background:#042f2e;color:#c9b8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #134e4a;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #d1e7e3;border-top:4px solid #0d9488;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#134e4a}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #d1e7e3;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(13,148,136,.08)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#134e4a}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#0d9488;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#0d9488;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#115e59}
"""

# Gate 1 — 10 × 10 (user revision request ~100 pages; grounded in product landing)
HUBS = [
    {
        "slug": "airport-car-rental",
        "name": "Airport Car Rental",
        "short": "Airport",
        "blurb": "Fast pickup near major airports with clear pricing and on-domain booking.",
        "children": [
            ("newark-airport-car-rental", "Newark Airport Car Rental", "EWR-focused pickup and drop-off options for travelers."),
            ("jfk-airport-car-rental", "JFK Airport Car Rental", "JFK area rentals with shuttle and meet-point guidance."),
            ("lga-airport-car-rental", "LaGuardia Airport Car Rental", "LGA-convenient cars for short and multi-day trips."),
            ("airport-shuttle-pickup", "Airport Shuttle Pickup", "Coordinated shuttle or meet-and-greet to your vehicle."),
            ("flight-delay-flexible-pickup", "Flight-Delay Flexible Pickup", "Hold windows that absorb common airline delays."),
            ("after-hours-airport-pickup", "After-Hours Airport Pickup", "Late arrival options when flights land after the counter closes."),
            ("one-way-airport-dropoff", "One-Way Airport Drop-Off", "Return at a different airport or city location."),
            ("airport-weekend-getaway-rentals", "Airport Weekend Getaway Rentals", "Friday–Monday packages priced for short escapes."),
            ("family-airport-suv-rental", "Family Airport SUV Rental", "Room for luggage and passengers after landing."),
            ("business-traveler-airport-cars", "Business Traveler Airport Cars", "Reliable midsize and full-size cars for work trips."),
        ],
    },
    {
        "slug": "city-car-rental",
        "name": "City Car Rental",
        "short": "City",
        "blurb": "Neighborhood and downtown rentals for errands, visits, and short local trips.",
        "children": [
            ("downtown-car-rental", "Downtown Car Rental", "Central city pickup points with walkable return options."),
            ("neighborhood-car-rental", "Neighborhood Car Rental", "Local lots closer to home than the airport counter."),
            ("same-day-city-rental", "Same-Day City Rental", "Book and drive when plans change at the last minute."),
            ("hourly-city-car-rental", "Hourly City Car Rental", "Short-duration rentals for appointments and errands."),
            ("overnight-city-rental", "Overnight City Rental", "Evening pickup with morning return for local stays."),
            ("grocery-run-car-rental", "Grocery & Errand Rentals", "Compact cars priced for quick local loops."),
            ("visiting-family-city-cars", "Visiting Family City Cars", "Extra seats when relatives are in town."),
            ("city-suv-rental", "City SUV Rental", "Higher clearance and cargo for urban + suburb trips."),
            ("compact-economy-city-cars", "Compact Economy City Cars", "Lower daily rates for light local driving."),
            ("parking-friendly-city-rentals", "Parking-Friendly City Rentals", "Smaller footprints that fit tight urban parking."),
        ],
    },
    {
        "slug": "one-way-car-rental",
        "name": "One-Way Car Rental",
        "short": "One-Way",
        "blurb": "Pick up in one city and drop off in another without doubling back.",
        "children": [
            ("one-way-city-to-city", "One-Way City-to-City", "Intercity drop-offs across the metro corridor."),
            ("one-way-airport-to-city", "One-Way Airport to City", "Land, drive inland, and leave the car at a city lot."),
            ("one-way-city-to-airport", "One-Way City to Airport", "Start local and return at the terminal area."),
            ("relocation-one-way-rentals", "Relocation One-Way Rentals", "Move cities without owning a second vehicle."),
            ("college-move-one-way", "College Move One-Way", "Dorm and apartment moves with flexible drop-off."),
            ("road-trip-one-way", "Road Trip One-Way", "End the trip where the trip ends — not where it started."),
            ("one-way-suv-rental", "One-Way SUV Rental", "Cargo-friendly one-ways for longer hauls."),
            ("one-way-van-rental", "One-Way Van Rental", "Cargo vans for moves and deliveries."),
            ("low-fee-one-way-options", "Low-Fee One-Way Options", "Transparent drop fees before you book."),
            ("multi-stop-one-way-planning", "Multi-Stop One-Way Planning", "Itinerary help when the drop city is not the first stop."),
        ],
    },
    {
        "slug": "suv-truck-van-rental",
        "name": "SUV, Truck & Van Rental",
        "short": "SUV & Truck",
        "blurb": "Larger vehicles for families, moves, and gear-heavy trips.",
        "children": [
            ("suv-rental-near-me", "SUV Rental Near Me", "Local SUVs for weather, passengers, and cargo."),
            ("full-size-suv-rental", "Full-Size SUV Rental", "Three-row options for larger groups."),
            ("pickup-truck-rental", "Pickup Truck Rental", "Open beds for materials and weekend projects."),
            ("cargo-van-rental", "Cargo Van Rental", "Enclosed space for moves and deliveries."),
            ("passenger-van-rental", "Passenger Van Rental", "Group transport for events and teams."),
            ("moving-truck-alternatives", "Moving Truck Alternatives", "Van and truck options when a full mover is overkill."),
            ("ski-trip-suv-rental", "Ski Trip SUV Rental", "AWD-friendly SUVs for mountain weekends [confirm availability]."),
            ("furniture-pickup-truck-rental", "Furniture Pickup Truck Rental", "Short-term trucks for marketplace hauls."),
            ("contractor-day-truck-rental", "Contractor Day Truck Rental", "Workday rentals for job-site runs."),
            ("family-road-trip-suv", "Family Road Trip SUV", "Comfort-first SUVs for multi-day drives."),
        ],
    },
    {
        "slug": "luxury-specialty-rentals",
        "name": "Luxury & Specialty Rentals",
        "short": "Luxury",
        "blurb": "Upscale and specialty vehicles for events, clients, and milestone trips.",
        "children": [
            ("luxury-car-rental-near-me", "Luxury Car Rental Near Me", "Premium sedans for arrivals that need to look sharp."),
            ("convertible-rental", "Convertible Rental", "Open-top weekends when the weather cooperates."),
            ("sports-car-rental", "Sports Car Rental", "Performance cars for special occasions."),
            ("wedding-car-rental", "Wedding Car Rental", "Ceremony and reception transportation packages."),
            ("executive-sedan-rental", "Executive Sedan Rental", "Quiet, polished cars for client meetings."),
            ("exotic-car-rental-inquiry", "Exotic Car Rental Inquiry", "Specialty requests routed to matching operators."),
            ("black-car-style-rentals", "Black-Car Style Rentals", "Dark luxury sedans for formal events."),
            ("anniversary-weekend-luxury", "Anniversary Weekend Luxury", "Two-day luxury packages for celebrations."),
            ("chauffeur-optional-add-on", "Chauffeur Optional Add-On", "Driver add-ons where partner operators offer them."),
            ("photo-shoot-vehicle-rental", "Photo Shoot Vehicle Rental", "Hourly or half-day specialty cars for content."),
        ],
    },
    {
        "slug": "business-fleet-rentals",
        "name": "Business & Fleet Rentals",
        "short": "Business",
        "blurb": "Corporate accounts, fleet surge capacity, and employee travel cars.",
        "children": [
            ("corporate-car-rental-accounts", "Corporate Car Rental Accounts", "Centralized billing and preferred rates for teams."),
            ("employee-travel-car-rental", "Employee Travel Car Rental", "Simple booking paths for staff on the road."),
            ("fleet-surge-capacity", "Fleet Surge Capacity", "Extra vehicles when your own fleet is maxed out."),
            ("client-visit-car-rental", "Client Visit Car Rental", "Presentable cars for on-site client days."),
            ("tradeshow-event-rentals", "Tradeshow & Event Rentals", "Multi-day cars for booth teams and vendors."),
            ("insurance-replacement-rentals", "Insurance Replacement Rentals", "Temporary cars while a claim vehicle is in shop."),
            ("nonprofit-group-rentals", "Nonprofit Group Rentals", "Group-friendly options for mission travel."),
            ("contractor-crew-rentals", "Contractor Crew Rentals", "Shared vehicles for crews across job sites."),
            ("monthly-business-lease-alts", "Monthly Business Rental Alternatives", "Longer-term rentals without a full lease."),
            ("expense-ready-invoicing", "Expense-Ready Invoicing", "Receipts and invoices your finance team can process."),
        ],
    },
    {
        "slug": "booking-protection-services",
        "name": "Booking & Protection Services",
        "short": "Booking",
        "blurb": "Clear booking, protection choices, and support so renters know what they are paying for.",
        "children": [
            ("online-car-rental-booking", "Online Car Rental Booking", "On-domain booking that keeps the full flow on your site."),
            ("instant-quote-car-rental", "Instant Quote Car Rental", "Price and availability before you commit."),
            ("damage-waiver-options", "Damage Waiver Options", "Protection tiers explained in plain English."),
            ("additional-driver-add-on", "Additional Driver Add-On", "Share the wheel without surprise counter fees."),
            ("child-seat-add-on", "Child Seat Add-On", "Request seats when you book, not at the lot."),
            ("gps-navigation-add-on", "GPS Navigation Add-On", "Navigation options for unfamiliar cities."),
            ("roadside-assistance-add-on", "Roadside Assistance Add-On", "Towing and lockout help as an optional layer."),
            ("prepaid-fuel-options", "Prepaid Fuel Options", "Fuel choices shown before pickup."),
            ("cancellation-and-change-help", "Cancellation & Change Help", "How to modify dates without a scavenger hunt."),
            ("rental-agreement-explained", "Rental Agreement Explained", "Key terms summarized so nothing is a surprise at the desk."),
        ],
    },
    {
        "slug": "local-seo-ppc-growth",
        "name": "Local SEO & PPC Growth",
        "short": "Growth",
        "blurb": "Rank for car rental near me searches and turn paid clicks into compounding organic demand.",
        "children": [
            ("car-rental-near-me-seo", "Car Rental Near Me SEO", "Hub pages built for high-intent local rental queries."),
            ("google-business-profile-rentals", "Google Business Profile for Rentals", "Maps visibility for lots and operator locations."),
            ("airport-keyword-campaigns", "Airport Keyword Campaigns", "Paid search structured around terminal intent."),
            ("ppc-to-seo-rental-flywheel", "PPC-to-SEO Rental Flywheel", "Ad spend that builds permanent ranking assets."),
            ("retargeting-for-rental-shoppers", "Retargeting for Rental Shoppers", "Bring back visitors who compared but did not book."),
            ("local-landing-pages-rentals", "Local Landing Pages for Rentals", "City and airport pages that convert and rank."),
            ("review-generation-for-lots", "Review Generation for Lots", "Post-rental review loops that lift Maps trust."),
            ("competitor-rental-gap-analysis", "Competitor Rental Gap Analysis", "Where national brands are weak locally."),
            ("seasonal-demand-campaigns", "Seasonal Demand Campaigns", "Budget shifts for holidays, storms, and travel spikes."),
            ("booking-conversion-optimization", "Booking Conversion Optimization", "Faster paths from quote to confirmed reservation."),
        ],
    },
    {
        "slug": "operator-territory-licensing",
        "name": "Operator & Territory Licensing",
        "short": "Operators",
        "blurb": "License a protected car-rental near-me territory and run it on the Car Rental Near Me stack.",
        "children": [
            ("become-a-rental-operator", "Become a Rental Operator", "Join the directory with profile, calendar, and payouts."),
            ("protected-rental-territory", "Protected Rental Territory", "County/metro exclusivity so you are not undercut next door."),
            ("tiered-territory-pricing", "Tiered Territory Pricing", "Metro, mid-tier, and rural licensing structures."),
            ("operator-profile-pages", "Operator Profile Pages", "Dofollow profiles with embedded booking on-domain."),
            ("fleet-onboarding-checklist", "Fleet Onboarding Checklist", "Vehicle, insurance, and calendar setup steps."),
            ("stripe-connect-payouts", "Stripe Connect Payouts", "Split payments between platform and operators."),
            ("operator-self-serve-dashboard", "Operator Self-Serve Dashboard", "Manage availability, pricing, and bookings yourself."),
            ("cross-referral-ai-consultants", "Cross-Referral with AI Consultants", "Track A consultants route local demand into your lots."),
            ("founding-operator-cohort", "Founding Operator Cohort", "Early territory pricing while the vertical launches."),
            ("multi-lot-expansion-playbook", "Multi-Lot Expansion Playbook", "Add a second lot after the first market proves out."),
        ],
    },
    {
        "slug": "rental-automation-stack",
        "name": "Rental Automation Stack",
        "short": "Automation",
        "blurb": "n8n, GoHighLevel, and booking automations that keep lots full without manual chase-downs.",
        "children": [
            ("booking-to-crm-automation", "Booking-to-CRM Automation", "Every reservation lands in a staged pipeline."),
            ("rental-sms-lifecycle", "Rental SMS Lifecycle", "Pickup reminders, return nudges, and delay notices."),
            ("review-request-after-return", "Review Request After Return", "Automate reputation capture when the trip ends."),
            ("no-show-reduction-workflows", "No-Show Reduction Workflows", "Confirmations that cut empty lot time."),
            ("dynamic-pricing-hooks", "Dynamic Pricing Hooks", "Rules for weekends, storms, and airport spikes."),
            ("fleet-availability-sync", "Fleet Availability Sync", "Keep calendars honest across channels."),
            ("lead-routing-by-territory", "Lead Routing by Territory", "Send inquiries to the operator who owns the zone."),
            ("payout-trigger-automations", "Payout Trigger Automations", "Pay operators when trips complete cleanly."),
            ("retargeting-audience-sync", "Retargeting Audience Sync", "Push quote abandoners into Meta and Google audiences."),
            ("demand-forecast-alerts", "Demand Forecast Alerts", "Know when to raise spend or open surge inventory."),
        ],
    },
]

INDUSTRIES = [
    "Airport Travelers",
    "Local Residents",
    "Business Travelers",
    "Moving & Relocation",
    "Wedding & Events",
    "Contractors & Crews",
    "Insurance Replacement",
    "Territory Operators",
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
<div class="logo">Car Rental <span>Near Me</span><small>Local Mobility Directory</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Free rental quote — no obligation</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Rent &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-car-rental-near-me/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-car-rental-near-me/index.html">About Car Rental Near Me</a>
<a href="{p}about-car-rental-near-me/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-car-rental-near-me/who-we-serve/index.html">Who We Serve</a>
</div></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li><a href="{p}request-a-proposal/index.html">Book / Partner</a></li>
<li class="em"><a href="{p}get-a-rental-quote/index.html">Free Quote</a></li>
</ul></div></nav>
"""


def footer(depth: int) -> str:
    p = pfx(depth)
    hubs = "".join(
        f'<li><a href="{p}{h["slug"]}/index.html">{escape(h["short"])}</a></li>' for h in HUBS
    )
    return f"""<footer><div class="wrap"><div class="fcols">
<div><h4>Rent</h4><ul>{hubs}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="{p}about-car-rental-near-me/index.html">About Car Rental Near Me</a></li>
<li><a href="{p}about-car-rental-near-me/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-car-rental-near-me/who-we-serve/index.html">Verticals</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}get-a-rental-quote/index.html">Free Rental Quote</a></li>
<li><a href="{p}request-a-proposal/index.html">Operator / Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul><li>{escape(ADDRESS)}</li><li>Operated by {escape(OPERATOR)}</li><li>Remote deployment nationwide</li></ul></div>
</div>
<div class="copy">Car Rental Near Me &middot; {escape(OPERATOR)} &middot; {escape(HQ)} &middot; {escape(PHONE)}<br>
Copyright &copy; 2026. Car Rental Near Me. All rights reserved.</div></div></footer>
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
<label>Interest</label><select><option>Please choose&hellip;</option>{opts}<option>Rental Quote</option><option>Founding Member / VIP</option><option>OS License</option><option>Other</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f95a8">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Car Rental Near Me",
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
            f'<a href="{h["slug"]}/index.html" style="font:600 13px \'Segoe UI\',sans-serif">All {escape(h["short"]).lower()} options &rarr;</a></div>'
        )
    return (
        head(
            "Car Rental Near Me | Airport, City & Local Rentals",
            "Car Rental Near Me helps travelers book local cars fast — and helps operators run protected rental territories on the Near Me OS stack.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>Car Rental Near Me — Book Local. Drive Today.</h1>
<p>{escape(TAGLINE)}</p>
<a class="btn" href="get-a-rental-quote/index.html">Take the Rental Quote</a> <a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>24/7</b><span>Online Booking</span></div>
<div class="stat"><b>Local</b><span>Lots Near You</span></div>
<div class="stat"><b>14</b><span>Week Vertical Launch</span></div>
<div class="stat"><b>1</b><span>Protected Territory Model</span></div>
</div></div></section>
<section><div class="wrap"><h2>What can Car Rental Near Me build for you?</h2>
<p class="lead">Ten solution families — from airport and city cars through one-way, SUV/truck, luxury, business, booking, growth, operators, and automation.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure which car fits? Start with a free quote.</h2>
<p style="margin-bottom:14px">The Rental Quote shows where you stand — then we map territory and tier.</p>
<a class="btn" href="get-a-rental-quote/index.html">Get a Free Quote</a></div></div>
<section><div class="wrap"><h2>How renters and operators get started</h2><div class="cols3">
<div class="card"><h3>1. Free rental quote</h3><p>Score gaps, capacity, and fit for Track A, Track B, or a stacked offer.</p></div>
<div class="card"><h3>2. Strategy call &amp; tier fit</h3><p>Confirm $1,500+/mo ad spend capacity, then choose SEO, PPC, Platform, VIP, or OS License.</p></div>
<div class="card"><h3>3. Deploy the flywheel</h3><p>Launch the directory or consultant territory and compound PPC into SEO equity.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why Car Rental Near Me</h2><div class="cols3">
<div class="card"><h3>Local lots, not just brands</h3><p>Neighborhood and airport operators listed with real booking paths.</p></div>
<div class="card"><h3>Built on Near Me OS</h3><p>PPC-to-SEO flywheel, territory licensing, and automation from the same stack.</p></div>
<div class="card"><h3>Renters + operators</h3><p>Travelers book cars; operators license protected markets.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready to book — or run a territory?</h2>
<a class="btn" href="get-a-rental-quote/index.html">Rental Quote</a> <a class="btn alt" href="request-a-proposal/index.html">Request Operator Info</a></div></div>
"""
        + faqs(
            [
                (
                    "What is Car Rental Near Me?",
                    "Car Rental Near Me is the operating system for building, ranking, and monetizing local near-me markets — with AI automation, territory licensing, and a compounding PPC-to-SEO flywheel.",
                ),
                (
                    "Who operates Car Rental Near Me?",
                    f"Car Rental Near Me is operated by {OPERATOR}, headquartered at {ADDRESS}.",
                ),
                (
                    "What is the Rental Quote?",
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
            f"{h['name']} | Car Rental Near Me",
            f"{h['name']} from Car Rental Near Me — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} — From Car Rental Near Me</h2>
<p class="lead">{escape(h["blurb"])} Delivered as part of the Car Rental Near Me stack rather than an isolated task.</p>
<p><a class="btn" href="../get-a-rental-quote/index.html">Take the Rental Quote</a> <a class="btn alt" href="../request-a-proposal/index.html">Request Operator Info</a></p>
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
                    "Begin with the free Rental Quote. We map track fit and provide a written proposal before work begins.",
                ),
                (
                    "Where is Car Rental Near Me based?",
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
        head(f"{name} | Car Rental Near Me", f"{name} from Car Rental Near Me — {blurb}")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Rely on Car Rental Near Me as your partner for {escape(name.lower())} and related market systems.</h2>
<p class="lead">{escape(blurb)} At Car Rental Near Me, {escape(name.lower())} is delivered inside a local rental marketplace — clear pricing, on-domain booking, and operator routing where it applies.</p>
<p><a class="btn" href="../../get-a-rental-quote/index.html">Take the Rental Quote</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request Operator Info</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(name)} Combined with Car Rental Near Me Can Help You Gain:</h2>
<ul class="checks">
<li>Faster booking for airport and city trips</li>
<li>Clear vehicle-class options without counter surprises</li>
<li>Territory clarity for operators who invest in local demand</li>
<li>Automation that cuts no-shows and chase-downs</li>
<li>Growth loops that turn ads into organic near-me rankings</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} path scoped to your trip or territory — not a one-size package</h2>
<p>No two trips or territories need {escape(name.lower())} the same way. We match vehicle class, location, and operator capacity — then confirm price before you commit.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Renters and operators avoid key risks with a developed marketplace for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with services-only approaches</h3><ul>
<li>PPC that never becomes an SEO asset</li>
<li>Directories with no booking or backlink loop</li>
<li>Territories sold without exclusivity or density math</li>
<li>Reporting that shows activity, not market ownership</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on Car Rental Near Me</h3><ul>
<li>PPC-to-SEO flywheel operated as one system</li>
<li>Clear territory and licensing paths</li>
<li>Evidence-friendly flywheel reporting</li>
<li>Founding-member accountability with a named team</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>See where you stand first — free</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} looks like for your dates? Start with a free rental quote.</p>
<a class="btn" href="../../get-a-rental-quote/index.html">Take the Rental Quote</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request Operator Info</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} shows results?",
                    "Timelines depend on vertical and ad capacity. Vertical launch targets a 14-week production path for operator markets; renter quotes are same-day when inventory allows.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Trip price depends on class, dates, and location. Operator territory pricing is scoped after an inquiry call.",
                ),
                (
                    f"Why choose Car Rental Near Me for {name.lower()}?",
                    f"We deliver {name.lower()} inside a rental marketplace — Race Computer Services accountability with a Near Me OS vertical stack.",
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
<h2 style="font-size:20px">Initiate a request with Car Rental Near Me</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us the trip</h3><p>Airport/city, dates, and vehicle class — or your operator goals.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>A quote, an operator path, or honest advice — whichever fits.</p></div>
<div class="card"><h3>3. Book or apply</h3><p>Confirm the reservation or territory next step in writing.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>Car Rental Near Me</strong><br>Operated by {escape(OPERATOR)}<br>Headquarters: {escape(ADDRESS)}<br>Phone: {escape(PHONE)}<br>Email: {escape(EMAIL)}</p>
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
        ["/", "HOME", "", "car rental near me", "logo/home", "A1,A6,A10", ""],
        [
            "/about-car-rental-near-me/",
            "COMP-HUB",
            "/",
            "about car rental near me",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-car-rental-near-me/why-choose-us/",
            "COMP-CHILD",
            "/about-car-rental-near-me/",
            "why choose car rental near me",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-car-rental-near-me/who-we-serve/",
            "COMP-CHILD",
            "/about-car-rental-near-me/",
            "car rental audiences",
            "About menu",
            "D1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact car rental near me",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "car rental operator proposal",
            "nav utility",
            "I1",
            "Request for Proposal",
        ],
        [
            "/get-a-rental-quote/",
            "FORM-CONSULT",
            "/",
            "car rental quote",
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
    with (ROOT / "CARRENTAL-PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
        "CARRENTAL-QUESTIONNAIRE-ANSWERS.md",
        "CARRENTAL-PAGE-INVENTORY.csv",
        "CARRENTAL-NOTES.md",
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
        ROOT / "about-car-rental-near-me" / "index.html",
        head(
            "About Car Rental Near Me | Elizabeth, NJ",
            "Car Rental Near Me is operated by Race Computer Services, LLC in Elizabeth, NJ.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About Car Rental Near Me</h2>
<p class="lead">Car Rental Near Me is a local car rental directory and operator territory platform — operated by {escape(OPERATOR)} from {escape(ADDRESS)}.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>Car Rental Near Me is the flagship Track B vertical from Near Me OS — embedded booking, territory licensing, and a 14-week production path for local mobility markets.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="who-we-serve/index.html">Verticals &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "Who operates Car Rental Near Me?",
                    f"Car Rental Near Me is operated by {OPERATOR}, headquartered at {ADDRESS}.",
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
    urls.append("/about-car-rental-near-me/")

    write(
        ROOT / "about-car-rental-near-me" / "why-choose-us" / "index.html",
        head("Why Choose Car Rental Near Me", "Why travelers and operators choose Car Rental Near Me.")
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose Car Rental Near Me</h2>
<p class="lead">A rental marketplace built to help operators stop renting attention and start owning local demand.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Flywheel by design</h3><p>PPC, SEO, booking, and territory licensing operated as one compounding system.</p></div>
<div class="card"><h3>Proof assets live</h3><p>RaceCS.net and San Diego Tech Support already demonstrate the model.</p></div>
<div class="card"><h3>Two tracks</h3><p>AI Consultant Network and Vertical Builders with cross-referral.</p></div>
<div class="card"><h3>Assessment-led sales</h3><p>Free rental quote first; written scope before you commit.</p></div>
<div class="card"><h3>Founding economics</h3><p>First-10 pricing on Platform and VIP while the cohort fills.</p></div>
<div class="card"><h3>Elizabeth HQ</h3><p>Race Computer Services accountability with nationwide remote delivery.</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-car-rental-near-me/why-choose-us/")

    ind = "".join(
        f'<div class="gcard"><h3>{escape(i)}</h3><p>Inventory and booking flows tuned to {escape(i.lower())} needs.</p></div>'
        for i in INDUSTRIES
    )
    write(
        ROOT / "about-car-rental-near-me" / "who-we-serve" / "index.html",
        head("Who We Serve | Car Rental Near Me", "Who Car Rental Near Me serves — renters and operators.")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Verticals</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Who We Serve</h2>
<p class="lead">Rental patterns tailored to how each traveler type books — and how operators staff lots.</p>
<div class="grid">{ind}</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-car-rental-near-me/who-we-serve/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | Car Rental Near Me",
            "Contact Us for Car Rental Near Me Inquiries",
            "Tell us your vertical, geography, and whether you are exploring Track A, Track B, or a full OS license.",
        ),
        (
            "get-a-rental-quote",
            "Rental Quote | Car Rental Near Me",
            "Take the Free rental quote",
            "See where you stand — then book a strategy call to claim your territory.",
        ),
        (
            "request-a-proposal",
            "Apply / Request a Proposal | Car Rental Near Me",
            "Request a Proposal or Operator Info",
            "Share your goals and ad capacity. We'll return a scoped founding proposal you can compare anywhere.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | Car Rental Near Me", "Page not found.")
        + chrome(0)
        + """
<section style="padding:72px 0"><div class="wrap"><h2 style="font-size:28px">Page not found</h2>
<p class="lead">That URL isn't on this lot. Try home or a free rental quote.</p>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn alt" href="get-a-rental-quote/index.html">Free Quote</a></p>
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
        ROOT / "CARRENTAL-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — Car Rental Near Me (FACTORY BUILD · Gate 1 10×10)

**Build uses NearMe OS Website Factory instructions-template (SEO Cow staging engine) · category: car rental / local mobility · facts from Near Me OS Track B + Race Computer Services S1 · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | Car Rental Near Me (operated by Race Computer Services, LLC) | Near Me OS Track B flagship |
| A2 domain | carrentalnearme.com | [confirm] |
| A3 phone | {PHONE} | Race CS / SEO Cow S1 (same operator) |
| A4 email | {EMAIL} | [confirm] |
| A5 address | {ADDRESS} | Race CS / SEO Cow S1 |
| A6 trade | Car rental / local mobility directory + territory licensing | product landing |
| A7 founded | not stated — omitted | — |
| A10 value_proposition | Book local and airport cars fast; operators license protected rental territories on Near Me OS | product landing |
| A11 tagline | {TAGLINE} | this build |
| A12 competitor_type | national rental brands, OTAs, unclassified local lots | [confirm] |
| A13 hours | not stated — omitted | — |

## B — Services: 10 categories × 10 children
{hub_slugs} — full map in CARRENTAL-PAGE-INVENTORY.csv.
FORM-CONSULT = `get-a-rental-quote` · FORM-PRICING = `request-a-proposal` (operator / partnership).

## C–I
- D1 audiences: airport travelers, residents, business, movers, events, contractors, insurance replacement, operators
- F1 service_area: Elizabeth NJ HQ, metro airport corridor focus, expandable territories
- F2/F3: no LOC doorway pages in this build
- I1 form_destination: OPEN — demo shells
- Staging: noindex + STAGING PREVIEW banner

| Metric | Value |
|---|---|
| hubs | {len(HUBS)} |
| svc children | {svc_children} |
| staging | noindex + STAGING PREVIEW banner |
""",
    )

    pages = list(ROOT.rglob("index.html"))
    # exclude marketing spa under nearmeos/
    factory_pages = list(pages)
    print(f"Generated {len(factory_pages)} factory index pages")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)} · Children: {sum(len(h['children']) for h in HUBS)}")


if __name__ == "__main__":
    main()
