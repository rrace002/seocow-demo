#!/usr/bin/env python3
"""Generate Elizabeth Decks and Additions site using the NearMe OS Website Factory template
(same HTML/CSS engine as the SEO Cow / Elizabeth Plumbing staging builds).

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: decks, porches, and home additions (Elizabeth, NJ local trade).
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
BASE = "https://elizabethdecksandadditions.com"  # [confirm]
PHONE = "(862) 295-0011"
PHONE_TEL = "+18622950011"
EMAIL = "info@elizabethdecksandadditions.com"  # [confirm]
HQ = "Elizabeth, NJ"
ADDRESS = "12 Sayre St, Elizabeth, NJ 07208"  # Race CS default [confirm]
OPERATOR = "Race Computer Services, LLC"  # [confirm]
BRAND = "Elizabeth Decks and Additions"
TAGLINE = "Your One-Stop Shop for Decks and Home Additions in Elizabeth, NJ"
STAGING_BANNER = (
    "STAGING PREVIEW — Elizabeth Decks and Additions factory build · Elizabeth NJ · "
    "content pending owner review"
)
ABOUT_SLUG = "about-elizabeth-decks-and-additions"

# NearMe factory CSS (SEO Cow template) with cedar / walnut remap
# Dropdown selectors use nav.nav .dd a so white-on-white menu text cannot recur.
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#431407;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#b45309;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#1c1917;color:#fed7aa;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#7c2d12;color:#ffedd5;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #d97706;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#431407}.logo span{color:#d97706}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#78716c;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#431407}
.phone-cta small{display:block;color:#78716c;font-size:11px}
nav.nav{background:#7c2d12}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#431407;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #d97706;z-index:60}
nav.nav .dd a{color:#431407;padding:10px 15px;font-weight:500;border-bottom:1px solid #fed7aa}
nav.nav .dd a:hover{background:#fff7ed;color:#431407}
.nav .em a{background:#d97706}.nav .em a:hover{background:#b45309}
.hero{background:linear-gradient(rgba(28,25,23,.82),rgba(28,25,23,.82)),repeating-linear-gradient(45deg,#7c2d12 0 14px,#b45309 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#fed7aa;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#d97706;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#b45309;text-decoration:none}
.btn.alt{background:#7c2d12;color:#fff}.btn.alt:hover{background:#431407}
section{padding:44px 0}
section.tint{background:#fff7ed}
section h2{font-size:25px;color:#431407;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#d97706;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #fed7aa;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(124,45,18,.06)}
.card h3{color:#431407;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #fed7aa;border-left:4px solid #d97706;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#431407}
.gcard p{font-size:14px;color:#57534e;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#b45309}
.ctastrip{background:#7c2d12;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #fed7aa;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#fff7ed}.vs .col.good{background:#fff7ed}
.vs h3{font-size:16px;margin-bottom:12px;color:#431407}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#b45309;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #fed7aa;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#431407;list-style:none}
details summary:before{content:"+ ";color:#d97706;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #fed7aa;border-top:4px solid #d97706;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#57534e;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#78716c;padding:14px 0 0}
.crumb a{color:#78716c}
footer{background:#1c1917;color:#c9b8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #7c2d12;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #fed7aa;border-top:4px solid #d97706;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#431407}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#78716c;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #fed7aa;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(217,119,6,.08)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#431407}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#d97706;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#d97706;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#431407}
"""

# Gate 1 — 10 × 10 decks & additions (Elizabeth NJ focus; no LOC doorway pages)
HUBS = [
    {
        "slug": "new-deck-construction",
        "name": "New Deck Construction",
        "short": "New Decks",
        "blurb": "Design and build new decks matched to Elizabeth, NJ yards, access, and how you use outdoor space.",
        "children": [
            ("custom-deck-design-build", "Custom Deck Design & Build", "A new deck planned around lot lines, doors, and how you gather outside."),
            ("ground-level-deck-construction", "Ground-Level Deck Construction", "Low-profile decks that expand a backyard without a tall structure."),
            ("elevated-deck-construction", "Elevated Deck Construction", "Second-story or walk-out decks with framing sized for the height."),
            ("multi-level-deck-construction", "Multi-Level Deck Construction", "Stepped decks that connect house, yard, and gathering zones."),
            ("small-yard-deck-build", "Small-Yard Deck Build", "Compact decks for tight Elizabeth lots that still feel usable."),
            ("wraparound-deck-construction", "Wraparound Deck Construction", "Decks that turn a corner and pick up more than one doorway."),
            ("deck-with-stairs-landing", "Deck with Stairs & Landing", "New decks that include a proper stair run and landing, not a bolted afterthought."),
            ("permit-ready-deck-planning", "Permit-Ready Deck Planning", "Layout and documentation support before you apply [confirm local process]."),
            ("deck-rebuild-in-place", "Deck Rebuild In Place", "Tear-down and rebuild on the same footprint when the old frame is spent."),
            ("new-deck-for-remodel", "New Deck for a Remodel", "Coordinate a new deck with a kitchen, door, or addition opening."),
        ],
    },
    {
        "slug": "deck-repair-restoration",
        "name": "Deck Repair & Restoration",
        "short": "Deck Repair",
        "blurb": "Stabilize, repair, and restore existing decks so Elizabeth homeowners are not living with bounce, rot, or loose rails.",
        "children": [
            ("soft-board-deck-repair", "Soft Board Deck Repair", "Replace spongy or rotten decking before it becomes a trip or fall risk."),
            ("loose-railing-deck-repair", "Loose Railing Deck Repair", "Re-secure or rebuild rails that move when you lean on them."),
            ("deck-joist-repair", "Deck Joist Repair", "Sister or replace joists that sag, twist, or no longer hold fasteners."),
            ("ledger-board-repair", "Ledger Board Repair", "Correct flashing and ledger connections at the house wall."),
            ("deck-footing-stabilization", "Deck Footing Stabilization", "Address sinking posts and undersized footings before the frame twists."),
            ("wobbly-deck-diagnosis", "Wobbly Deck Diagnosis", "Find why a deck bounces — posts, beams, or missing lateral support."),
            ("stair-stringer-repair", "Stair Stringer Repair", "Repair cracked or undersized stringers on deck stairs."),
            ("deck-hardware-upgrade", "Deck Hardware Upgrade", "Swap rusted fasteners and connectors for code-aware hardware."),
            ("weathered-deck-restoration", "Weathered Deck Restoration", "Clean, sand, and refinish wood decks that still have sound framing."),
            ("emergency-unsafe-deck-repair", "Emergency Unsafe Deck Repair", "Stabilize a deck that feels unsafe until a full repair can be scheduled."),
        ],
    },
    {
        "slug": "composite-wood-decking",
        "name": "Composite & Wood Decking",
        "short": "Decking",
        "blurb": "Choose and install wood or composite decking that fits Elizabeth weather, budget, and maintenance appetite.",
        "children": [
            ("composite-decking-install", "Composite Decking Installation", "Low-maintenance composite boards installed on a sound frame."),
            ("pressure-treated-decking-install", "Pressure-Treated Decking Installation", "Classic PT lumber decking for a cost-aware outdoor floor."),
            ("cedar-decking-install", "Cedar Decking Installation", "Cedar surface boards where appearance and milling matter."),
            ("hidden-fastener-decking", "Hidden Fastener Decking", "Clip or hidden-fastener systems for a cleaner walking surface."),
            ("deck-board-replacement", "Deck Board Replacement", "Swap worn boards without rebuilding the entire structure."),
            ("picture-frame-deck-border", "Picture-Frame Deck Border", "Border boards that finish the edge of a new or refreshed deck."),
            ("deck-inlay-pattern-install", "Deck Inlay & Pattern Install", "Diagonal, herringbone, or bordered patterns on a new surface."),
            ("composite-vs-wood-consult", "Composite vs Wood Consult", "A straight comparison of maintenance, cost, and look before you buy."),
            ("faded-composite-board-swap", "Faded Composite Board Swap", "Replace stained or faded composite boards in matching runs."),
            ("deck-surface-resurfacing", "Deck Surface Resurfacing", "New walking surface over framing that still has remaining life."),
        ],
    },
    {
        "slug": "deck-railings-stairs",
        "name": "Deck Railings & Stairs",
        "short": "Rails & Stairs",
        "blurb": "Code-aware rails, stairs, and gates that make Elizabeth decks safer to use every day.",
        "children": [
            ("wood-deck-railing-install", "Wood Deck Railing Installation", "Wood rail systems sized to the deck edge and stair runs."),
            ("aluminum-composite-railing", "Aluminum & Composite Railing", "Low-maintenance rail kits that still look finished from the yard."),
            ("cable-rail-deck-install", "Cable Rail Deck Installation", "Horizontal cable rails for a more open view [confirm local rules]."),
            ("glass-panel-rail-prep", "Glass Panel Rail Prep", "Framing and post layout for glass infill panels [confirm]."),
            ("deck-stair-building", "Deck Stair Building", "New stair runs with consistent rise, run, and landings."),
            ("stair-railing-rebuild", "Stair Railing Rebuild", "Replace shaky stair rails without rebuilding the whole deck."),
            ("deck-gate-install", "Deck Gate Installation", "Child- or pet-minded gates on deck openings [confirm hardware]."),
            ("code-height-rail-upgrade", "Code-Height Rail Upgrade", "Bring short or missing rails up to expected guard height."),
            ("lighting-ready-rail-posts", "Lighting-Ready Rail Posts", "Posts and channels prepped for future low-voltage lighting [confirm]."),
            ("ada-minded-stair-options", "ADA-Minded Stair Options", "Wider treads, landings, or ramp-adjacent stairs when access is a goal."),
        ],
    },
    {
        "slug": "covered-decks-porches",
        "name": "Covered Decks & Porches",
        "short": "Covered Decks",
        "blurb": "Add roofs, screens, and porch structure so Elizabeth decks stay usable in sun and light rain.",
        "children": [
            ("covered-deck-roof-add", "Covered Deck Roof Add-On", "A roof structure over an existing or new deck."),
            ("screened-porch-conversion", "Screened Porch Conversion", "Screen a deck or porch for bug-season use."),
            ("three-season-porch-build", "Three-Season Porch Build", "Enclosed porch space that extends the outdoor season [confirm insulation scope]."),
            ("front-porch-rebuild", "Front Porch Rebuild", "Repair or rebuild a street-facing porch that is part of the home’s first impression."),
            ("rear-covered-porch", "Rear Covered Porch", "A covered gathering porch off a kitchen or family room."),
            ("pergola-over-deck", "Pergola Over Deck", "Open-roof shade structure tied into deck posts or a new frame."),
            ("awning-ready-deck-frame", "Awning-Ready Deck Frame", "Framing prep for a future retractable awning [confirm product]."),
            ("porch-ceiling-beadboard", "Porch Ceiling & Beadboard", "Finished porch ceilings that hide structure and look complete."),
            ("screen-repair-porch", "Screen Repair for Porches", "Replace torn screens and splines without a full rebuild."),
            ("covered-entry-deck", "Covered Entry Deck", "A small covered landing at a side or rear door."),
        ],
    },
    {
        "slug": "room-additions",
        "name": "Room Additions",
        "short": "Room Additions",
        "blurb": "Plan and build room additions that expand Elizabeth homes without jumping to a full second story.",
        "children": [
            ("single-room-addition", "Single-Room Addition", "Add a bedroom, office, or flex room to the existing footprint."),
            ("family-room-addition", "Family Room Addition", "A new gathering room that opens to the yard or a future deck."),
            ("kitchen-expansion-addition", "Kitchen Expansion Addition", "Bump-out or addition space that lets a kitchen breathe."),
            ("primary-suite-addition", "Primary Suite Addition", "Bedroom-and-bath addition planning for a first-floor suite [confirm trades]."),
            ("home-office-addition", "Home Office Addition", "A dedicated work room with independent access when needed."),
            ("mudroom-addition", "Mudroom Addition", "A drop zone addition at a side or rear entry."),
            ("dining-room-bump-out", "Dining Room Bump-Out", "A modest bump-out when a full addition is more than you need."),
            ("addition-to-deck-connection", "Addition-to-Deck Connection", "Door, landing, and deck ties so the new room uses the yard."),
            ("small-footprint-addition", "Small-Footprint Addition", "Tight-lot additions that respect setbacks and neighbor spacing."),
            ("phased-room-addition", "Phased Room Addition", "Shell first, finish second — when budget or occupancy requires a sequence."),
        ],
    },
    {
        "slug": "second-story-additions",
        "name": "Second-Story Additions",
        "short": "Second Story",
        "blurb": "Go up when the Elizabeth lot cannot grow out — with honest scope on structure, access, and disruption.",
        "children": [
            ("second-story-addition-planning", "Second-Story Addition Planning", "Feasibility, access, and disruption planning before anyone opens a roof."),
            ("partial-second-story-add", "Partial Second-Story Add", "Add rooms over a portion of the first floor, not the whole house."),
            ("full-second-story-addition", "Full Second-Story Addition", "A complete upper level when the first floor footprint can carry it [confirm engineering]."),
            ("dormer-addition", "Dormer Addition", "Dormers that create headroom and usable attic or second-floor space."),
            ("stair-location-for-second-story", "Stair Location for Second Story", "Find a stair path that does not wreck the first-floor layout."),
            ("roof-removal-second-story", "Roof Removal for Second Story", "Sequence for opening a roof and keeping the house weather-tight."),
            ("second-story-deck-tie-in", "Second-Story Deck Tie-In", "An upper deck or balcony that belongs to the new floor."),
            ("load-bearing-review-support", "Load-Bearing Review Support", "Coordinate structural review before you commit to going up [confirm engineer]."),
            ("second-story-finish-package", "Second-Story Finish Package", "Trim, doors, and finishes that match the existing home."),
            ("occupied-home-second-story", "Occupied-Home Second Story", "Phasing ideas when the family stays in the house during work."),
        ],
    },
    {
        "slug": "garage-sunroom-additions",
        "name": "Garage, Sunroom & Conversions",
        "short": "Conversions",
        "blurb": "Turn unused garage, porch, or leftover volume into living space — or add a sunroom that lives like an extra room.",
        "children": [
            ("garage-conversion-living-space", "Garage Conversion Living Space", "Convert a garage into a room when parking can move [confirm zoning]."),
            ("attached-garage-addition", "Attached Garage Addition", "Add a garage volume that can later support a room above."),
            ("sunroom-addition", "Sunroom Addition", "A light-filled sunroom tied into existing walls and a future deck."),
            ("three-season-room-addition", "Three-Season Room Addition", "A glazed room for spring through fall use."),
            ("four-season-room-consult", "Four-Season Room Consult", "What it takes to condition a sunroom year-round [confirm HVAC partner]."),
            ("porch-to-room-conversion", "Porch-to-Room Conversion", "Enclose a porch into conditioned or three-season space."),
            ("breezeway-addition", "Breezeway Addition", "Connect house and garage with a finished or open breezeway."),
            ("in-law-suite-addition-shell", "In-Law Suite Addition Shell", "A suite-capable addition shell — finishes and trades coordinated [confirm]."),
            ("home-studio-addition", "Home Studio Addition", "A studio or shop addition with a separate entry when needed."),
            ("conversion-vs-new-addition", "Conversion vs New Addition", "When converting existing volume beats pouring a new foundation."),
        ],
    },
    {
        "slug": "addition-framing-shell",
        "name": "Addition Framing & Shell",
        "short": "Framing & Shell",
        "blurb": "Foundation prep, framing, and a weather-tight shell so Elizabeth additions stay square, dry, and ready to finish.",
        "children": [
            ("addition-foundation-prep", "Addition Foundation Prep", "Site and foundation work that a stable addition actually sits on."),
            ("addition-framing", "Addition Framing", "Walls, floors, and roof framing that line up with the existing house."),
            ("addition-sheathing-wrap", "Addition Sheathing & Wrap", "Weather-resistive shell before windows and siding go on."),
            ("addition-roof-tie-in", "Addition Roof Tie-In", "Roof planes that shed water away from the original house."),
            ("addition-window-door-rough", "Addition Window & Door Rough-In", "Openings sized for the units you actually ordered."),
            ("addition-exterior-siding-match", "Addition Exterior Siding Match", "Siding and trim that attempt a clean blend with existing elevations."),
            ("addition-insulation-air-seal", "Addition Insulation & Air Seal", "Cavities and joints detailed so the new rooms are not draft factories."),
            ("weather-tight-addition-milestone", "Weather-Tight Addition Milestone", "A defined dry-in point before interior finish starts."),
            ("addition-structural-beam-work", "Addition Structural Beam Work", "Openings and beams when you want the addition to feel like one house."),
            ("existing-house-tie-in-carpentry", "Existing-House Tie-In Carpentry", "Where new framing meets old — floors, walls, and ceilings aligned."),
        ],
    },
    {
        "slug": "outdoor-living-structures",
        "name": "Outdoor Living Structures",
        "short": "Outdoor Living",
        "blurb": "Pergolas, landings, and yard structures that complete a deck or addition project in Elizabeth, NJ.",
        "children": [
            ("attached-pergola-build", "Attached Pergola Build", "A pergola that shares posts or a ledger with the house or deck."),
            ("freestanding-pergola", "Freestanding Pergola", "A shade structure in the yard that does not depend on the house wall."),
            ("patio-cover-structure", "Patio Cover Structure", "A cover over an existing patio when a full deck is not the goal."),
            ("deck-adjacent-landing", "Deck-Adjacent Landing", "A landing that connects stairs, patio, and door without a full rebuild."),
            ("outdoor-kitchen-pad-prep", "Outdoor Kitchen Pad Prep", "Framing and pad prep for a future outdoor kitchen [confirm trades]."),
            ("privacy-screen-on-deck", "Privacy Screen on Deck", "Screen walls that block a neighbor view without boxing in the deck."),
            ("built-in-deck-bench-planter", "Built-In Deck Bench & Planter", "Seating and planters that are part of the rail or edge, not furniture."),
            ("hot-tub-deck-platform", "Hot Tub Deck Platform", "A reinforced bay or platform sized for spa loads [confirm specs]."),
            ("yard-steps-and-walk", "Yard Steps and Walk", "Connecting steps from deck grade to lawn or driveway."),
            ("outdoor-living-master-plan", "Outdoor Living Master Plan", "Sequence decks, covers, and additions so you do not rebuild twice."),
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
<div class="logo">Elizabeth <span>Decks &amp; Additions</span><small>Decks · Porches · Additions · Elizabeth, NJ</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Request a quote — no obligation</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}{ABOUT_SLUG}/index.html">About &#9662;</a><div class="dd">
<a href="{p}{ABOUT_SLUG}/index.html">About {escape(BRAND)}</a>
<a href="{p}{ABOUT_SLUG}/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}{ABOUT_SLUG}/service-areas/index.html">Service Areas</a>
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
<li><a href="{p}{ABOUT_SLUG}/index.html">About {escape(BRAND)}</a></li>
<li><a href="{p}{ABOUT_SLUG}/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}{ABOUT_SLUG}/service-areas/index.html">Service Areas</a></li>
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
<div class="copy">{escape(BRAND)} &middot; {escape(OPERATOR)} &middot; {escape(HQ)} &middot; {escape(PHONE)}<br>
Copyright &copy; 2026. {escape(BRAND)}. All rights reserved.<br>
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
<label>Service Needed</label><select><option>Please choose&hellip;</option>{opts}<option>General decks &amp; additions question</option><option>Other</option></select>
<label>Urgency</label><select><option>Please choose&hellip;</option><option>Unsafe structure — need help soon</option><option>This season</option><option>Planning / estimate only</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f95a8">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": BRAND,
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
            f"{BRAND} | Decks and Home Additions in Elizabeth, NJ",
            f"{BRAND} is your one-stop shop for decks and home additions in Elizabeth, NJ — new decks, repairs, porches, room additions, and more.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>{escape(BRAND)}</h1>
<p>Decks, porches, and home additions for Elizabeth NJ.</p>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>One-Stop</b><span>Decks &amp; Additions</span></div>
<div class="stat"><b>Local</b><span>Elizabeth, NJ Focus</span></div>
<div class="stat"><b>10</b><span>Service Families</span></div>
<div class="stat"><b>Quote</b><span>No Obligation</span></div>
</div></div></section>
<section><div class="wrap"><h2>Deck and addition services for Elizabeth, NJ</h2>
<p class="lead">Ten service families — from new decks and repairs through composite decking, rails, covered porches, room additions, second stories, conversions, framing shells, and outdoor living structures.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure whether you need a deck, a porch, or an addition? Start with a quote.</h2>
<p style="margin-bottom:14px">Describe the project — we help you choose the right outdoor or expansion path.</p>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a></div></div>
<section><div class="wrap"><h2>How to get started</h2><div class="cols3">
<div class="card"><h3>1. Request a quote</h3><p>Tell us whether this is a new deck, a repair, a porch cover, or a room addition — plus lot access notes.</p></div>
<div class="card"><h3>2. Scope the work</h3><p>We clarify structure, weather-tight sequence, and whether repair, rebuild, or a new footprint fits best.</p></div>
<div class="card"><h3>3. Schedule when ready</h3><p>Confirm next steps in writing before demolition or framing begins — no invented wait-time promises.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why {escape(BRAND)}</h2><div class="cols3">
<div class="card"><h3>Decks and additions under one roof</h3><p>Outdoor structures and home expansion planned so you are not coordinating two unrelated crews.</p></div>
<div class="card"><h3>Elizabeth, NJ focus</h3><p>Local copy and routing built around Elizabeth and nearby Union County communities.</p></div>
<div class="card"><h3>Clear next steps</h3><p>Quote and proposal paths that set expectations before you commit.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready for a deck or addition quote?</h2>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    f"What is {BRAND}?",
                    f"{BRAND} is a one-stop shop for decks and home additions in Elizabeth, NJ — from new decks and repairs to porches, room additions, and outdoor living structures.",
                ),
                (
                    f"Who operates {BRAND}?",
                    f"{BRAND} is operated by {OPERATOR}, with headquarters listed at {ADDRESS} [confirm].",
                ),
                (
                    "How do I request a quote?",
                    "Use the Request a Quote form or call us. Describe the project, property type, and timing — we follow up with next steps.",
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
            f"{h['name']} | {BRAND}",
            f"{h['name']} from {BRAND} in Elizabeth, NJ — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} in Elizabeth, NJ</h2>
<p class="lead">{escape(h["blurb"])} Part of {escape(BRAND)} — your one-stop shop for decks and home additions.</p>
<p><a class="btn" href="../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Services We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What a typical engagement can include</h2>
<ul class="checks">
<li>Clear description of the deck, porch, or addition goal</li>
<li>On-site look at structure, access, and weather exposure before major rebuild recommendations</li>
<li>Repair-vs-rebuild vs new-footprint options explained in plain language</li>
<li>Written next steps after the quote or proposal path</li>
<li>Elizabeth, NJ focus — no generic national boilerplate</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with Request a Quote. For larger additions or multi-phase outdoor work, use Request a Proposal.",
                ),
                (
                    f"Where is {BRAND} based?",
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
            f"{name} | {BRAND}",
            f"{name} from {BRAND} in Elizabeth, NJ — {blurb}",
        )
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(name)} for Elizabeth, NJ homes</h2>
<p class="lead">{escape(blurb)} At {escape(BRAND)}, {escape(name.lower())} is delivered as part of a local decks-and-additions shop — clear structure review, practical options, and a quote path before you commit.</p>
<p><a class="btn" href="../../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(name)} with {escape(BRAND)} can help you gain:</h2>
<ul class="checks">
<li>Faster clarity on whether repair, rebuild, or a new footprint is the smarter path</li>
<li>Local Elizabeth, NJ focus instead of generic national copy</li>
<li>One team for related decks, porches, and addition tie-ins</li>
<li>Written quote or proposal steps before demolition or framing</li>
<li>Honest scope — no invented testimonials or wait-time guarantees</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} path scoped to your property — not a one-size package</h2>
<p>No two lots need {escape(name.lower())} the same way. We match access, grade, existing structure, and how you use the space — then confirm next steps before work begins.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Homeowners avoid key risks with a developed local path for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with ad-hoc deck or addition work</h3><ul>
<li>Surface fixes that ignore rot in joists, ledgers, or footings</li>
<li>An addition that does not tie into a future deck or door</li>
<li>No written scope before tear-off or framing</li>
<li>National lead mills that do not know Elizabeth lot and access realities</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on {escape(BRAND)}</h3><ul>
<li>Decks and additions covered under one local page map</li>
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
                    "Timing depends on season, permits, and crew availability. Unsafe-structure paths are prioritized; planned builds are scheduled after the quote conversation — no invented same-week guarantees.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Price depends on size, materials, access, and whether you are repairing, rebuilding, or adding new volume. Use Request a Quote for an estimate path.",
                ),
                (
                    f"Why choose {BRAND} for {name.lower()}?",
                    f"We deliver {name.lower()} inside a local decks-and-additions shop focused on Elizabeth, NJ — with clear quote and proposal steps.",
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
<h2 style="font-size:20px">Initiate a request with {escape(BRAND)}</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us the project</h3><p>New deck, repair, porch cover, room addition, or conversion — plus property type and access.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>A quote path, a proposal for larger work, or honest advice on next steps.</p></div>
<div class="card"><h3>3. Schedule when ready</h3><p>Confirm scope in writing before demolition or framing begins.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>{escape(BRAND)}</strong><br>Operated by {escape(OPERATOR)} <em>[confirm]</em><br>Headquarters: {escape(ADDRESS)} <em>[confirm]</em><br>Phone: {escape(PHONE)}<br>Email: {escape(EMAIL)} <em>[confirm]</em></p>
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
        ["/", "HOME", "", "elizabeth decks and additions", "logo/home", "A1,A6,A10", ""],
        [
            f"/{ABOUT_SLUG}/",
            "COMP-HUB",
            "/",
            "about elizabeth decks and additions",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            f"/{ABOUT_SLUG}/why-choose-us/",
            "COMP-CHILD",
            f"/{ABOUT_SLUG}/",
            "why choose elizabeth decks and additions",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            f"/{ABOUT_SLUG}/service-areas/",
            "COMP-CHILD",
            f"/{ABOUT_SLUG}/",
            "elizabeth nj decks additions service areas",
            "About menu",
            "F1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact elizabeth decks and additions",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "decks additions proposal elizabeth nj",
            "nav utility",
            "I1",
            "Request for Proposal",
        ],
        [
            "/request-a-quote/",
            "FORM-CONSULT",
            "/",
            "decks additions quote elizabeth nj",
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
    with (ROOT / "ELIZABETHDECKS-PAGE-INVENTORY.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
        "ELIZABETHDECKS-QUESTIONNAIRE-ANSWERS.md",
        "ELIZABETHDECKS-PAGE-INVENTORY.csv",
        "ELIZABETHDECKS-NOTES.md",
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
        ROOT / ABOUT_SLUG / "index.html",
        head(
            f"About {BRAND} | Elizabeth, NJ",
            f"{BRAND} is your one-stop shop for decks and home additions in Elizabeth, NJ.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About {escape(BRAND)}</h2>
<p class="lead">{escape(BRAND)} is a one-stop shop for decks and home additions in Elizabeth, NJ — operated by {escape(OPERATOR)} from {escape(ADDRESS)} <em>[confirm]</em>.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>We focus on local outdoor-structure and expansion demand: new decks, repairs, composite and wood surfaces, rails and stairs, covered porches, room additions, second stories, conversions, framing shells, and outdoor living structures.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="service-areas/index.html">Service areas &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    f"Who operates {BRAND}?",
                    f"{BRAND} is operated by {OPERATOR}, headquartered at {ADDRESS} [confirm].",
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
    urls.append(f"/{ABOUT_SLUG}/")

    write(
        ROOT / ABOUT_SLUG / "why-choose-us" / "index.html",
        head(
            f"Why Choose {BRAND}",
            f"Why homeowners choose {BRAND} in Elizabeth, NJ.",
        )
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose {escape(BRAND)}</h2>
<p class="lead">A local decks-and-additions shop built to be the one stop for outdoor structures and home expansion — without invented testimonials.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>One-stop coverage</h3><p>Decks, repairs, decking, rails, porches, room additions, second stories, conversions, shells, and outdoor living.</p></div>
<div class="card"><h3>Elizabeth, NJ focus</h3><p>Pages and routing written for local intent — not national boilerplate.</p></div>
<div class="card"><h3>Quote-led intake</h3><p>Request a Quote first; larger additions can move to a written proposal.</p></div>
<div class="card"><h3>Clear service map</h3><p>Ten hubs × ten children so visitors land on the right project page.</p></div>
<div class="card"><h3>Honest staging copy</h3><p>No fabricated reviews, awards, or wait-time guarantees in this build.</p></div>
<div class="card"><h3>Named operator</h3><p>Race Computer Services accountability for this factory build [confirm].</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append(f"/{ABOUT_SLUG}/why-choose-us/")

    areas = "".join(
        f'<div class="gcard"><h3>{escape(a)}</h3><p>Deck and addition inquiries for {escape(a)} — coverage confirmed case by case.</p></div>'
        for a in SERVICE_AREAS
    )
    write(
        ROOT / ABOUT_SLUG / "service-areas" / "index.html",
        head(
            f"Service Areas | {BRAND}",
            f"Service areas for {BRAND} — Elizabeth, NJ and nearby communities.",
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
    urls.append(f"/{ABOUT_SLUG}/service-areas/")

    for slug, title, h2, lead in [
        (
            "contact",
            f"Contact Us | {BRAND}",
            "Contact Us for Deck & Addition Inquiries",
            "Tell us the project, your Elizabeth-area property type, and whether you need a repair path or a planned build estimate.",
        ),
        (
            "request-a-quote",
            f"Request a Quote | {BRAND}",
            "Request a Deck or Addition Quote",
            "Describe the deck, porch, or addition goal — we follow up with clear next steps.",
        ),
        (
            "request-a-proposal",
            f"Request a Proposal | {BRAND}",
            "Request a Proposal for Larger Deck or Addition Work",
            "Share multi-room, second-story, or multi-structure goals. We return a scoped proposal you can compare.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head(f"Page Not Found | {BRAND}", "Page not found.")
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
        ROOT / "ELIZABETHDECKS-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — {BRAND} (FACTORY BUILD · Gate 1 10×10)

**Build uses NearMe OS Website Factory instructions-template (SEO Cow staging engine) · category: decks and home additions · Elizabeth NJ local trade · Race Computer Services S1 defaults · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | {BRAND} (operated by Race Computer Services, LLC) | this build [confirm] |
| A2 domain | elizabethdecksandadditions.com | [confirm] |
| A3 phone | {PHONE} | Race CS / S1 (same operator) |
| A4 email | {EMAIL} | [confirm] |
| A5 address | {ADDRESS} | Race CS default [confirm] |
| A6 trade | Decks and home additions | this build |
| A7 founded | not stated — omitted | — |
| A10 value_proposition | One-stop shop for decks and home additions in Elizabeth, NJ | this build |
| A11 tagline | {TAGLINE} | this build |
| A12 competitor_type | national deck brands, marketplace lead-gen, unclassified local carpenters | [confirm] |
| A13 hours | not stated — omitted | — |

## B — Services: 10 categories × 10 children
{hub_slugs} — full map in ELIZABETHDECKS-PAGE-INVENTORY.csv.
FORM-CONSULT = `request-a-quote` · FORM-PRICING = `request-a-proposal`.

## C–I
- D1 audiences: homeowners, landlords, remodel partners
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
        ROOT / "ELIZABETHDECKS-NOTES.md",
        f"""# {BRAND} — Factory Build

Local trade category: **decks and home additions** (Elizabeth, NJ).

- Generator: `scripts/generate_elizabethdecks_factory.py`
- Gate 1: 10 × 10 = 100 SVC-CHILD (+ chrome ≈ 117 pages)
- Brand: {BRAND}
- FORM-CONSULT: `/request-a-quote/` (highlighted)
- FORM-PRICING: `/request-a-proposal/`
- About: `/{ABOUT_SLUG}/` · why-choose-us · service-areas
- Staging: noindex + STAGING PREVIEW banner
- Domain / email / NAP: elizabethdecksandadditions.com · {EMAIL} · {ADDRESS} *[confirm]*
- CSS: cedar / walnut (`#7c2d12` / `#431407` / `#d97706` / `#fff7ed`)
- Dropdown CSS uses `nav.nav .dd a` so Services menu text stays readable
- No invented testimonials; no LOC doorway pages
""",
    )

    factory_pages = list(ROOT.rglob("index.html"))
    print(f"Generated {len(factory_pages)} factory index pages")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)} · Children: {sum(len(h['children']) for h in HUBS)}")


if __name__ == "__main__":
    main()
