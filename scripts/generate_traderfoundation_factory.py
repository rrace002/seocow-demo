#!/usr/bin/env python3
"""Generate Trader Foundation site using the NearMe OS Website Factory template.

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: trading education / options coaching for busy professionals.
Facts grounded from live trader.foundation (fetched 2026-07-22).
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.trader.foundation"
PHONE = ""
PHONE_TEL = ""
EMAIL = "hello@trader.foundation"  # [confirm]
HQ = ""
ADDRESS = ""
FOUNDER = "Vlad Tayman"
PARTNER = "Erin Chawla"
TAGLINE = "Works with your career, not against it."
STAGING_BANNER = (
    "STAGING PREVIEW — trader.foundation factory build · content pending owner review "
    "· not the live Trader Foundation website"
)

# NearMe factory CSS (SEO Cow template) with Trader Foundation orange remap
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#0f2744;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#a8861f;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#0a1524;color:#e8d5a3;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#0f2744;color:#efe6c8;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #c9a227;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#0f2744}.logo span{color:#c9a227}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#0f2744}
.phone-cta small{display:block;color:#5a6b7b;font-size:11px}
nav.nav{background:#0f2744}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#0a1a2e;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #c9a227;z-index:60}
.dd a{color:#0f2744;padding:10px 15px;font-weight:500;border-bottom:1px solid #ebe6d8}
.dd a:hover{background:#f4f1e8}
.nav .em a{background:#c9a227}.nav .em a:hover{background:#a8861f}
.hero{background:linear-gradient(rgba(10,21,36,.88),rgba(10,21,36,.88)),repeating-linear-gradient(45deg,#0f2744 0 14px,#1a3354 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#e8d5a3;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#c9a227;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#f07a3a;text-decoration:none}
.btn.alt{background:#0f2744;color:#fff}.btn.alt:hover{background:#7a3c1a}
section{padding:44px 0}
section.tint{background:#f7f5ef}
section h2{font-size:25px;color:#0f2744;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#c9a227;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #e5e0d2;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(15,39,68,.06)}
.card h3{color:#0f2744;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #e5e0d2;border-left:4px solid #c9a227;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#0f2744}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#a8861f}
.ctastrip{background:#0f2744;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #e5e0d2;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#f7f5ef}.vs .col.good{background:#f7f5ef}
.vs h3{font-size:16px;margin-bottom:12px;color:#0f2744}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#a8861f;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #e5e0d2;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#0f2744;list-style:none}
details summary:before{content:"+ ";color:#c9a227;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #e5e0d2;border-top:4px solid #c9a227;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#44525f;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5a6b7b;padding:14px 0 0}
.crumb a{color:#5a6b7b}
footer{background:#0a1524;color:#c9b8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #1a3354;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #e5e0d2;border-top:4px solid #c9a227;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#0f2744}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #e5e0d2;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(15,39,68,.08)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#0f2744}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#c9a227;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#c9a227;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#0f2744}
"""

# Gate 1 — 10 × 10 (user revision request ~100 pages; grounded in product landing)
HUBS = [
    {
        "slug": "paycheck-collector-strategy",
        "name": "Paycheck Collector Strategy",
        "short": "Paycheck Collector",
        "blurb": "Monthly options income with defined risk — the core Trader Foundation method for busy professionals.",
        "children": [
            ("paycheck-collector-overview", "Paycheck Collector Overview", "How the strategy aims to collect premium on a predictable monthly cycle."),
            ("defined-risk-options-income", "Defined-Risk Options Income", "Know your maximum loss before the trade is placed."),
            ("monthly-premium-collection", "Monthly Premium Collection", "Structure trades around a paycheck-like income cadence."),
            ("selling-options-on-liquid-names", "Selling Options on Liquid Names", "Focus on liquid stocks and indices suited to premium selling."),
            ("bull-and-bear-market-premium", "Bull & Bear Market Premium", "Premium collection framed around selling time, not calling direction."),
            ("discount-stock-accumulation", "Discount Stock Accumulation", "How downturns can set up discounted acquisition levels while collecting premium."),
            ("position-sizing-for-income", "Position Sizing for Income", "Size trades so one loss does not wreck the month."),
            ("paycheck-collector-trade-examples", "Paycheck Collector Trade Examples", "Walkthrough-style education on how setups are selected and managed."),
            ("time-efficient-trade-management", "Time-Efficient Trade Management", "Designed for professionals who cannot watch the screen all day."),
            ("compounding-the-paycheck-collector", "Compounding the Paycheck Collector", "Turn a single method into a repeatable portfolio process."),
        ],
    },
    {
        "slug": "options-trading-education",
        "name": "Options Trading Education",
        "short": "Options Education",
        "blurb": "Learn options as a defined-risk toolkit — not lottery tickets — with coaching support.",
        "children": [
            ("options-basics-for-professionals", "Options Basics for Professionals", "Calls, puts, and premium selling explained without fluff."),
            ("credit-spread-education", "Credit Spread Education", "Defined-risk structures commonly used for income-style setups."),
            ("calendar-spread-education", "Calendar Spread Education", "Time-based structures discussed in Trader Foundation education."),
            ("options-vs-stock-trading", "Options vs Stock Trading", "When options can help smaller accounts express a plan with defined risk."),
            ("implied-volatility-basics", "Implied Volatility Basics", "Why premium expands and contracts — and what that means for sellers."),
            ("expiration-and-assignment-basics", "Expiration & Assignment Basics", "What happens near expiration and how students are taught to prepare."),
            ("options-greeks-overview", "Options Greeks Overview", "Delta, theta, and the greeks that matter for income trading."),
            ("wheel-adjacent-concepts", "Wheel-Adjacent Concepts", "Related premium and share-accumulation ideas taught in context."),
            ("index-options-education", "Index Options Education", "Liquid index products as an education focus for premium strategies."),
            ("options-mistakes-to-avoid", "Options Mistakes to Avoid", "Common beginner errors coaches flag early."),
        ],
    },
    {
        "slug": "swing-trading-for-professionals",
        "name": "Swing Trading for Professionals",
        "short": "Swing Trading",
        "blurb": "Swing-timeframe process built to fit a full-time career — not day-trading addiction.",
        "children": [
            ("swing-trading-overview", "Swing Trading Overview", "Multi-day to multi-week holds that respect a busy calendar."),
            ("career-friendly-trading-schedule", "Career-Friendly Trading Schedule", "How students batch analysis around work hours."),
            ("setup-selection-framework", "Setup Selection Framework", "Specialize in A+ setups instead of chasing every ticker."),
            ("entry-and-exit-planning", "Entry & Exit Planning", "Plan the trade before you place it."),
            ("trade-journaling-habits", "Trade Journaling Habits", "Review loops that turn experience into skill."),
            ("watchlist-building", "Watchlist Building", "Keep a focused list instead of scanning the whole market."),
            ("multi-timeframe-analysis", "Multi-Timeframe Analysis", "Align higher-timeframe context with execution timeframe."),
            ("holding-through-noise", "Holding Through Noise", "Stay with a plan when intraday headlines get loud."),
            ("part-time-trader-routines", "Part-Time Trader Routines", "Morning/evening routines that fit professionals."),
            ("when-not-to-trade", "When Not to Trade", "Standing aside is part of the edge."),
        ],
    },
    {
        "slug": "risk-management-training",
        "name": "Risk Management Training",
        "short": "Risk Management",
        "blurb": "Defined risk, position sizing, and portfolio rules that protect the account while you learn.",
        "children": [
            ("defined-risk-first-principles", "Defined Risk First Principles", "Maximum loss known before entry — a core teaching theme."),
            ("position-sizing-rules", "Position Sizing Rules", "Size for survival and consistency, not for dopamine."),
            ("portfolio-heat-limits", "Portfolio Heat Limits", "How much total risk is too much across open trades."),
            ("avoiding-margin-call-scenarios", "Avoiding Margin-Call Scenarios", "Education oriented around staying out of surprise leverage traps."),
            ("trade-invalidation-levels", "Trade Invalidation Levels", "Where the thesis is wrong — and what to do then."),
            ("drawdown-recovery-process", "Drawdown Recovery Process", "Process over panic when a streak goes cold."),
            ("capital-requirements-guidance", "Capital Requirements Guidance", "Live site notes application for professionals ready to trade with $15,000+."),
            ("risk-reward-framing", "Risk/Reward Framing", "Think in distributions and process, not one heroic winner."),
            ("correlation-and-concentration", "Correlation & Concentration", "Avoid stacking the same bet five different ways."),
            ("rules-based-risk-checklist", "Rules-Based Risk Checklist", "A pre-trade checklist students can reuse."),
        ],
    },
    {
        "slug": "one-on-one-trading-coaching",
        "name": "One-on-One Trading Coaching",
        "short": "1:1 Coaching",
        "blurb": "Personalized coaching so you are not left alone with a course video and a blank platform.",
        "children": [
            ("one-on-one-coaching-overview", "One-on-One Coaching Overview", "Personal sessions with coaches who know the system."),
            ("90-day-coaching-support", "90-Day Coaching Support", "Live site frames 90 days of one-on-one coaching in the guarantee offer."),
            ("pay-when-profitable-guarantee", "Pay When Profitable Framing", "Program messaging: do the work; coaching continues until profitable under stated terms."),
            ("coach-erin-chawla", "Coach Erin Chawla", "Partner and coach — former GE corporate finance background, now teaching."),
            ("founder-vlad-tayman", "Founder Vlad Tayman", "Founder & CEO who built the Trader Foundation system and community."),
            ("coaches-elliot-and-leo", "Coaches Elliot & Leo", "Live-site coaching team carrying the system forward with Erin."),
            ("personalized-trade-reviews", "Personalized Trade Reviews", "Bring your chart and get direct feedback."),
            ("accountability-check-ins", "Accountability Check-Ins", "Stay consistent when work and life compete for attention."),
            ("strategy-call-fit-check", "Strategy Call Fit Check", "Application-led path — confirm fit before you enroll."),
            ("coaching-for-busy-schedules", "Coaching for Busy Schedules", "Designed around professionals who already have a career."),
        ],
    },
    {
        "slug": "live-market-coaching",
        "name": "Live Market Coaching",
        "short": "Live Coaching",
        "blurb": "Live sessions and real-time review so education stays connected to the market.",
        "children": [
            ("daily-live-coaching-sessions", "Daily Live Coaching Sessions", "Student reviews mention daily live sessions where stocks are reviewed in real time."),
            ("live-trade-idea-review", "Live Trade Idea Review", "See how coaches evaluate setups as the market moves."),
            ("market-open-preparation", "Market Open Preparation", "Prep routines before the bell without living on Level 2."),
            ("weekly-market-recaps", "Weekly Market Recaps", "Close the loop on what worked and what did not."),
            ("student-chart-reviews", "Student Chart Reviews", "Learn from real student examples, not only textbook charts."),
            ("qa-with-coaches", "Q&A with Coaches", "Ask the question you would not put in a public comment."),
            ("real-time-risk-discussion", "Real-Time Risk Discussion", "Talk through risk while a trade is still open."),
            ("earnings-and-event-awareness", "Earnings & Event Awareness", "Respect catalysts that can blow up a premium thesis."),
            ("replay-and-notes-habits", "Replay & Notes Habits", "Capture live lessons into a personal playbook."),
            ("community-live-support", "Community Live Support", "Combine live coaching with peer discussion."),
        ],
    },
    {
        "slug": "technical-analysis-training",
        "name": "Technical Analysis Training",
        "short": "Technical Analysis",
        "blurb": "Read charts with a process — specialize in patterns that fit the Paycheck Collector approach.",
        "children": [
            ("technical-analysis-foundations", "Technical Analysis Foundations", "Structure, levels, and trend context without indicator overload."),
            ("support-and-resistance-skills", "Support & Resistance Skills", "Map levels that matter for entries, invalidation, and targets."),
            ("candlestick-context", "Candlestick Context", "Candles as context, not magic signals."),
            ("trend-vs-range-identification", "Trend vs Range Identification", "Match the strategy to the market condition."),
            ("pattern-specialization", "Pattern Specialization", "Master one A+ pattern family before expanding."),
            ("volume-and-liquidity-checks", "Volume & Liquidity Checks", "Avoid illiquid names that punish premium sellers."),
            ("chart-timeframe-alignment", "Chart Timeframe Alignment", "Keep higher-timeframe bias and lower-timeframe timing consistent."),
            ("indicator-minimalism", "Indicator Minimalism", "Use fewer tools with clearer rules."),
            ("scanning-with-intent", "Scanning with Intent", "Scan for your setup — not for entertainment."),
            ("from-analysis-to-execution", "From Analysis to Execution", "Bridge the gap between a good read and a placed trade."),
        ],
    },
    {
        "slug": "trading-psychology-discipline",
        "name": "Trading Psychology & Discipline",
        "short": "Psychology",
        "blurb": "Mindset and process so a good strategy is not undone by impatience or revenge trading.",
        "children": [
            ("trading-psychology-basics", "Trading Psychology Basics", "Emotions are part of the system — manage them on purpose."),
            ("discipline-over-prediction", "Discipline Over Prediction", "Process beats being right about the next headline."),
            ("avoiding-revenge-trading", "Avoiding Revenge Trading", "Rules for what happens after a loss."),
            ("impatience-and-overtrading", "Impatience & Overtrading", "Why more trades is often worse performance."),
            ("building-a-trading-identity", "Building a Trading Identity", "From tip-follower to rules-based operator."),
            ("career-stress-and-trading", "Career Stress & Trading", "Keep work stress from leaking into risk decisions."),
            ("patience-as-an-edge", "Patience as an Edge", "Waiting for your setup is a skill."),
            ("confidence-without-ego", "Confidence Without Ego", "Confidence from reps and rules, not bravado."),
            ("perfect-student-habits", "Perfect-Student Habits", "Podcast themes on what separates students who stick."),
            ("long-term-consistency-mindset", "Long-Term Consistency Mindset", "Think in years of process, not one viral win."),
        ],
    },
    {
        "slug": "retirement-account-trading",
        "name": "Retirement Account Trading",
        "short": "IRA & HSA",
        "blurb": "Education around managing tax-advantaged accounts with a long-term, rules-based process.",
        "children": [
            ("roth-ira-trading-education", "Roth IRA Trading Education", "Live site highlights a Roth IRA case study (+142% over 3 years); individual results vary."),
            ("hsa-trading-education", "HSA Trading Education", "Live site highlights an HSA case study (+83% over 3 years); individual results vary."),
            ("passive-management-around-a-career", "Passive Management Around a Career", "Account examples framed as passively managed alongside full-time work."),
            ("long-term-compounding-focus", "Long-Term Compounding Focus", "Multi-year process over get-rich-quick noise."),
            ("tax-advantaged-account-basics", "Tax-Advantaged Account Basics", "High-level education — not personalized tax advice."),
            ("fidelity-account-examples", "Fidelity Account Examples", "Live site references actual Fidelity account screenshots as illustrations."),
            ("risk-inside-retirement-accounts", "Risk Inside Retirement Accounts", "Defined-risk thinking still applies when the account is tax-advantaged."),
            ("contribution-and-growth-mindset", "Contribution & Growth Mindset", "Pair savings habits with a trading process."),
            ("past-performance-disclaimer-education", "Past Performance Disclaimer Education", "Past results do not guarantee future results — taught as part of realism."),
            ("patient-wealth-building", "Patient Wealth Building", "Build skills that can compound across market cycles."),
        ],
    },
    {
        "slug": "community-podcast-resources",
        "name": "Community, Podcast & Resources",
        "short": "Community",
        "blurb": "Skool community, podcast, and ongoing education that keep students connected between sessions.",
        "children": [
            ("trader-foundation-community", "Trader Foundation Community", "Skool membership community for professionals on the same path."),
            ("trader-foundation-podcast", "The Trader Foundation Podcast", "Market insights, education, and mindset episodes."),
            ("strategy-vault-access", "Strategy Vault Access", "Community framing includes access to the Paycheck Collector strategy materials."),
            ("student-reviews-and-social-proof", "Student Reviews & Social Proof", "Trustpilot and on-site reviews — verify current ratings on Trustpilot."),
            ("bbb-accredited-business", "BBB Accredited Business", "Live site highlights BBB Accredited Business with A+ rating messaging."),
            ("application-and-fit-process", "Application & Fit Process", "Application required — not an open impulse checkout."),
            ("book-a-strategy-call", "Book a Strategy Call", "Primary next step: transparent conversation to assess fit."),
            ("six-years-in-business", "Six Years in Business", "Live site references six years in business in review context."),
            ("student-success-stories", "Student Success Stories", "On-site testimonials from students at different starting points."),
            ("continuing-education-habits", "Continuing Education Habits", "Stay sharp after the first strategy clicks."),
        ],
    },
]

INDUSTRIES = [
    "Busy Professionals",
    "Corporate Finance Backgrounds",
    "Career Changers",
    "Beginner Options Students",
    "Part-Time Traders",
    "Retirement Account Builders",
    "Skool Community Members",
    "Podcast Learners",
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
    return f"""<div class="utility"><div class="wrap"><span>{escape(TAGLINE)}</span><span>Home of the Paycheck Collector &middot; {escape(EMAIL)}</span></div></div>
<header class="main"><div class="wrap">
<div class="logo">Trader <span>Foundation</span><small>Academy · Paycheck Collector</small></div>
<div class="phone-cta"><a href="{p}book-a-strategy-call/index.html">Book a Strategy Call</a><small>For professionals ready to trade with $15,000+ · application required</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Learn &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-trader-foundation/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-trader-foundation/index.html">About Trader Foundation</a>
<a href="{p}about-trader-foundation/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-trader-foundation/who-we-teach/index.html">Who We Teach</a>
</div></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li><a href="{p}request-a-proposal/index.html">Apply / Call</a></li>
<li class="em"><a href="{p}book-a-strategy-call/index.html">Strategy Call</a></li>
</ul></div></nav>
"""


def footer(depth: int) -> str:
    p = pfx(depth)
    hubs = "".join(
        f'<li><a href="{p}{h["slug"]}/index.html">{escape(h["short"])}</a></li>' for h in HUBS
    )
    return f"""<footer><div class="wrap"><div class="fcols">
<div><h4>Learn</h4><ul>{hubs}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="{p}about-trader-foundation/index.html">About Trader Foundation</a></li>
<li><a href="{p}about-trader-foundation/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-trader-foundation/who-we-teach/index.html">Verticals</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}book-a-strategy-call/index.html">Book a Strategy Call</a></li>
<li><a href="{p}request-a-proposal/index.html">Request Program Info</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
<li><a href="https://www.trader.foundation/" rel="noopener">trader.foundation</a></li>
</ul></div>
<div><h4>Next Step</h4><ul><li>Application required</li><li>Professionals ready to trade with $15,000+</li><li>Online coaching &amp; community</li></ul></div>
</div>
<div class="copy">Trader Foundation Academy &middot; Founded by {escape(FOUNDER)} &middot; Partner {escape(PARTNER)}<br>
Copyright &copy; 2026. Trader Foundation. All rights reserved. Trading involves risk of loss.</div></div></footer>
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
<label>Trading Capital Readiness</label><select><option>Please choose&hellip;</option><option>$15,000+ ready to trade</option><option>Under $15,000</option><option>Not sure yet</option></select>
<label>Interest</label><select><option>Please choose&hellip;</option>{opts}<option>Strategy Call</option><option>Paycheck Collector</option><option>1:1 Coaching</option><option>Other</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f95a8">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": "Trader Foundation",
        "alternateName": "Trader Foundation Academy",
        "email": EMAIL,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "founder": {"@type": "Person", "name": FOUNDER},
        "description": "Trading education and coaching for busy professionals — home of the Paycheck Collector strategy.",
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
            f'<a href="{h["slug"]}/index.html" style="font:600 13px \'Segoe UI\',sans-serif">All {escape(h["short"]).lower()} topics &rarr;</a></div>'
        )
    return (
        head(
            "Trader Foundation | Options Trading Education for Professionals",
            "Trader Foundation Academy teaches busy professionals defined-risk options income through the Paycheck Collector strategy, coaching, and community.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>Take Control of Your Financial Future</h1>
<p>{escape(TAGLINE)}</p>
<a class="btn" href="book-a-strategy-call/index.html">Book a Free Strategy Call</a> <a class="btn alt" href="paycheck-collector-strategy/index.html">See the Paycheck Collector</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>6+</b><span>Years in Business</span></div>
<div class="stat"><b>1000+</b><span>Students Mentored</span></div>
<div class="stat"><b>A+</b><span>BBB Rating (site)</span></div>
<div class="stat"><b>$15k+</b><span>Capital Ready Filter</span></div>
</div></div></section>
<section><div class="wrap"><h2>What can you learn at Trader Foundation?</h2>
<p class="lead">Ten education families — Paycheck Collector, options, swing trading, risk, coaching, live markets, technical analysis, psychology, retirement accounts, and community.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure if it fits your career? Start with a call.</h2>
<p style="margin-bottom:14px">Book a free strategy call — a transparent conversation to see if Trader Foundation is the right fit.</p>
<a class="btn" href="book-a-strategy-call/index.html">Book a Free Strategy Call</a></div></div>
<section><div class="wrap"><h2>How students get started</h2><div class="cols3">
<div class="card"><h3>1. Book a strategy call</h3><p>Transparent conversation to check fit and readiness.</p></div>
<div class="card"><h3>2. Application review</h3><p>For professionals ready to trade with $15,000+.</p></div>
<div class="card"><h3>3. Learn the Paycheck Collector</h3><p>Coaching, live sessions, and community around defined-risk income.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why Trader Foundation</h2><div class="cols3">
<div class="card"><h3>Built for careers</h3><p>Works with your schedule — swing process, not all-day screen watching.</p></div>
<div class="card"><h3>Paycheck Collector core</h3><p>Defined-risk options income education with coaching, not tip spam.</p></div>
<div class="card"><h3>Human coaches</h3><p>Erin, Elliot, Leo, and the system founded by Vlad Tayman.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready to talk strategy?</h2>
<a class="btn" href="book-a-strategy-call/index.html">Strategy Call</a> <a class="btn alt" href="request-a-proposal/index.html">Request Program Info</a></div></div>
"""
        + faqs(
            [
                (
                    "What is Trader Foundation?",
                    "Trader Foundation Academy is a trading education and coaching organization — home of the Paycheck Collector strategy for busy professionals learning defined-risk options income.",
                ),
                (
                    "Who founded Trader Foundation?",
                    f"{FOUNDER} founded Trader Foundation. Partner {PARTNER} coaches alongside a team including Elliot and Leo.",
                ),
                (
                    "What is the strategy call?",
                    "A free, application-linked conversation to see if the program fits your schedule, capital readiness, and goals.",
                ),
                (
                    "Who is it for?",
                    "Professionals ready to trade with $15,000+ who want a career-compatible swing/options process — not day-trading noise.",
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
            f"{h['name']} | Trader Foundation",
            f"{h['name']} from Trader Foundation — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} — From Trader Foundation</h2>
<p class="lead">{escape(h["blurb"])} Taught as part of the Trader Foundation curriculum rather than an isolated tip.</p>
<p><a class="btn" href="../book-a-strategy-call/index.html">Book a Free Strategy Call</a> <a class="btn alt" href="../request-a-proposal/index.html">Request Program Info</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Solutions We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What Your Engagement Can Include</h2>
<ul class="checks">
<li>Education tied to the Paycheck Collector process</li>
<li>Risk framing before capital is committed</li>
<li>Coaching and live session support</li>
<li>Career-compatible swing routines</li>
<li>Community accountability between sessions</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with a free strategy call. We discuss fit, capital readiness, and whether coaching is appropriate.",
                ),
                (
                    "Where is Trader Foundation based?",
                    f"Online academy and coaching — join from anywhere after application.",
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
        head(f"{name} | Trader Foundation", f"{name} from Trader Foundation — {blurb}")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Learn {escape(name.lower())} with Trader Foundation coaching and a rules-based education path.</h2>
<p class="lead">{escape(blurb)} At Trader Foundation, {escape(name.lower())} is delivered inside a coaching-led curriculum — process, risk, and accountability for busy professionals.</p>
<p><a class="btn" href="../../book-a-strategy-call/index.html">Book a Free Strategy Call</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request Program Info</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>How {escape(name)} Training at Trader Foundation Can Help You:</h2>
<ul class="checks">
<li>A clearer rules-based process instead of tip-chasing</li>
<li>Defined-risk framing before capital is at risk</li>
<li>Coaching feedback when a trade plan is unclear</li>
<li>Routines that fit a full-time career</li>
<li>Community and live sessions that keep you accountable</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} path scoped to your experience level — not a one-size course dump</h2>
<p>No two students need {escape(name.lower())} the same way. Coaching adapts to your schedule, account type, and starting point — after a fit conversation.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Students avoid key risks learning {escape(name.lower())} with a system</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with DIY tip culture</h3><ul>
<li>Signals without risk rules</li>
<li>Day-trading advice that fights your career</li>
<li>Courses with no live coaching loop</li>
<li>Overtrading after one win or one loss</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on Trader Foundation</h3><ul>
<li>Paycheck Collector process with defined-risk framing</li>
<li>1:1 and live coaching support</li>
<li>Career-compatible swing timeframe</li>
<li>Community and accountability between sessions</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>See where you stand first — free</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} would look like for your schedule? Start with a free strategy call.</p>
<a class="btn" href="../../book-a-strategy-call/index.html">Book a Free Strategy Call</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request Program Info</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} shows results?",
                    "Timelines depend on vertical and ad capacity. Timelines depend on your experience and how consistently you show up to coaching.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Program fit and pricing are discussed on the strategy call after application — not published as a public menu on the live site.",
                ),
                (
                    f"Why choose Trader Foundation for {name.lower()}?",
                    f"We deliver {name.lower()} inside a coaching academy founded by Vlad Tayman — with partner Erin Chawla and the coaching team.",
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
<h2 style="font-size:20px">Initiate a request with Trader Foundation</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us your situation</h3><p>Career schedule, experience level, and capital readiness.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>Fit for the Paycheck Collector path — or an honest no.</p></div>
<div class="card"><h3>3. Decide with the full picture</h3><p>Trading involves risk of loss; education is not a profit guarantee.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>Trader Foundation Academy</strong><br>Founder: {escape(FOUNDER)}<br>Partner / Coach: {escape(PARTNER)}<br>Website: <a href="https://www.trader.foundation/">trader.foundation</a><br>Email: {escape(EMAIL)} <em>[confirm]</em></p>
<p style="font-size:13px;color:#5a6b7b">Trading involves risk of loss. Past performance does not guarantee future results. Education and coaching are not individualized investment advice.</p>
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
        ["/", "HOME", "", "trader foundation", "logo/home", "A1,A6,A10", ""],
        [
            "/about-trader-foundation/",
            "COMP-HUB",
            "/",
            "about trader foundation",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-trader-foundation/why-choose-us/",
            "COMP-CHILD",
            "/about-trader-foundation/",
            "why choose trader foundation",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-trader-foundation/who-we-teach/",
            "COMP-CHILD",
            "/about-trader-foundation/",
            "who trader foundation teaches",
            "About menu",
            "D1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact trader foundation",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "trader foundation program info",
            "nav utility",
            "I1",
            "Request for Proposal",
        ],
        [
            "/book-a-strategy-call/",
            "FORM-CONSULT",
            "/",
            "book a strategy call",
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
                "Learn menu",
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
                    "Learn menu > hub grid",
                    "B row",
                    "Request for Proposal",
                ]
            )
    with (ROOT / "TRADERFOUNDATION-PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
        "TRADERFOUNDATION-QUESTIONNAIRE-ANSWERS.md",
        "TRADERFOUNDATION-PAGE-INVENTORY.csv",
        "TRADERFOUNDATION-NOTES.md",
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
        ROOT / "about-trader-foundation" / "index.html",
        head(
            "About Trader Foundation Academy",
            "Trader Foundation Academy — home of the Paycheck Collector. Founded by Vlad Tayman.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About Trader Foundation</h2>
<p class="lead">Trader Foundation Academy helps hardworking professionals learn defined-risk options income through the Paycheck Collector strategy, coaching, and community — founded by {escape(FOUNDER)}.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>Built on the foundation created by founder {escape(FOUNDER)}, taught by coaches including {escape(PARTNER)}, Elliot, and Leo. The academy is positioned for professionals who want trading to work with a career — not against it.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="who-we-teach/index.html">Verticals &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "Who founded Trader Foundation?",
                    f"{FOUNDER} founded Trader Foundation. Partner {PARTNER} coaches alongside a team including Elliot and Leo.",
                ),
                (
                    "Is this day trading?",
                    "No — the academy emphasizes career-compatible swing/options process and the Paycheck Collector method.",
                ),
            ]
        )
        + org_schema()
        + footer(1),
    )
    urls.append("/about-trader-foundation/")

    write(
        ROOT / "about-trader-foundation" / "why-choose-us" / "index.html",
        head("Why Choose Trader Foundation", "Why busy professionals choose Trader Foundation Academy.")
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose Trader Foundation</h2>
<p class="lead">An education path built so trading can work with your career — not against it.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Paycheck Collector core</h3><p>Monthly options income education with defined-risk framing.</p></div>
<div class="card"><h3>Career-compatible</h3><p>Swing process designed around hectic professional schedules.</p></div>
<div class="card"><h3>Human coaching</h3><p>1:1 and live sessions — not a content dump alone.</p></div>
<div class="card"><h3>Application-led</h3><p>Fit conversation first for capital-ready professionals.</p></div>
<div class="card"><h3>Community + podcast</h3><p>Skool community and The Trader Foundation Podcast.</p></div>
<div class="card"><h3>Risk realism</h3><p>Trading involves loss; past results do not guarantee future results.</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-trader-foundation/why-choose-us/")

    ind = "".join(
        f'<div class="gcard"><h3>{escape(i)}</h3><p>Curriculum emphasis tuned for {escape(i.lower())}.</p></div>'
        for i in INDUSTRIES
    )
    write(
        ROOT / "about-trader-foundation" / "who-we-teach" / "index.html",
        head("Who We Teach | Trader Foundation", "Who Trader Foundation Academy teaches.")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Verticals</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Who We Teach</h2>
<p class="lead">Education paths tailored to how different professionals learn and trade part-time.</p>
<div class="grid">{ind}</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-trader-foundation/who-we-teach/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | Trader Foundation",
            "Contact Trader Foundation",
            "Questions about coaching, the Paycheck Collector, or whether the academy fits your career schedule.",
        ),
        (
            "book-a-strategy-call",
            "Book a Free Strategy Call | Trader Foundation",
            "Book a Free Strategy Call",
            "No pressure pitch — a transparent conversation to see if Trader Foundation is the right fit. Application required for professionals ready to trade with $15,000+.",
        ),
        (
            "request-a-proposal",
            "Request Program Info | Trader Foundation",
            "Request Program Information",
            "Share your background and goals. We will point you to the right next step — usually a strategy call.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | Trader Foundation", "Page not found.")
        + chrome(0)
        + """
<section style="padding:72px 0"><div class="wrap"><h2 style="font-size:28px">Page not found</h2>
<p class="lead">That page isn't in the academy map. Try home or book a strategy call.</p>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn alt" href="book-a-strategy-call/index.html">Strategy Call</a></p>
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
        ROOT / "TRADERFOUNDATION-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — Trader Foundation (FACTORY BUILD · Gate 1 10×10)

**NearMe OS Website Factory staging engine · category: trading education / options coaching · facts from live trader.foundation (2026-07-22) · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | Trader Foundation / Trader Foundation Academy | live site |
| A2 domain | trader.foundation | live site |
| A3 phone | not published — omitted | — |
| A4 email | {EMAIL} | [confirm] |
| A5 address | not published — omitted | — |
| A6 trade | Trading education / options coaching for busy professionals | live site |
| A7 founded | ~6 years in business (site review copy) | live site |
| A8 founder | {FOUNDER} | live / Skool |
| A9 partner_coach | {PARTNER}; coaches Elliot & Leo | live site |
| A10 value_proposition | Home of the Paycheck Collector — monthly options income, defined risk, career-compatible | live site |
| A11 tagline | {TAGLINE} | live site |
| A12 audience | Professionals ready to trade with $15,000+; application required | live site |

## B — Services: 10 × 10
{hub_slugs}
FORM-CONSULT=`book-a-strategy-call` · FORM-PRICING=`request-a-proposal`

## Notes
- No invented phone/address
- Risk disclaimer required on marketing claims
- Staging: noindex + STAGING PREVIEW
| hubs | {len(HUBS)} | children | {svc_children} |
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
