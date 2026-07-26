#!/usr/bin/env python3
"""Generate Trade OS site using the NearMe OS Website Factory template.

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: trading systems, custom indicators, TradingView integration & crypto trade calls.
Product: Trade OS (trading systems / indicators service — NOT contractors or trade-market SEO).
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
PHONE = "(862) 295-0011"  # [confirm] — Race CS default
PHONE_TEL = "+18622950011"
EMAIL = "info@tradeos.io"  # [confirm]
HQ = "Elizabeth, NJ"  # [confirm]
ADDRESS = "12 Sayre St, Elizabeth, NJ 07208"  # [confirm]
OPERATOR = "Race Computer Services, LLC"  # [confirm]
TAGLINE = "Trading Systems, Custom Indicators & Crypto Trade Calls"
STAGING_BANNER = (
    "STAGING PREVIEW — Trade OS factory build · trading systems & indicators · "
    "content pending owner review · not investment advice"
)
RISK = (
    "Cryptocurrency trading involves substantial risk of loss and is not suitable for every "
    "investor. Trade OS provides trading systems, indicators, and informational trade calls — "
    "not financial, investment, or trading advice. Past performance is not indicative of future results."
)

# NearMe factory CSS — Trade OS navy + signal green (distinct from emerald consulting / gold foundation)
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#0b1220;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#15803d;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#0b1220;color:#86efac;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#111827;color:#bbf7d0;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #22c55e;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#0b1220}.logo span{color:#22c55e}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#0b1220}
.phone-cta small{display:block;color:#5a6b7b;font-size:11px}
nav.nav{background:#111827}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#0b1220;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #22c55e;z-index:60}
.dd a{color:#0b1220;padding:10px 15px;font-weight:500;border-bottom:1px solid #dcfce7}
.dd a:hover{background:#f0fdf4}
.nav .em a{background:#22c55e;color:#0b1220}.nav .em a:hover{background:#16a34a;color:#fff}
.hero{background:linear-gradient(rgba(11,18,32,.92),rgba(17,24,39,.90)),repeating-linear-gradient(45deg,#0b1220 0 14px,#111827 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:860px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#bbf7d0;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#22c55e;color:#0b1220;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#16a34a;color:#fff;text-decoration:none}
.btn.alt{background:#0b1220;color:#fff}.btn.alt:hover{background:#111827}
section{padding:44px 0}
section.tint{background:#f8fafc}
section h2{font-size:25px;color:#0b1220;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
.risk{font-size:13px;color:#5a6b7b;border-left:3px solid #eab308;padding:10px 14px;background:#fffbeb;margin:18px 0}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#22c55e;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #e2e8f0;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(11,18,32,.05)}
.card h3{color:#0b1220;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #e2e8f0;border-left:4px solid #22c55e;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#0b1220}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#15803d}
.ctastrip{background:#111827;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #e2e8f0;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#f8fafc}.vs .col.good{background:#f0fdf4}
.vs h3{font-size:16px;margin-bottom:12px;color:#0b1220}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#15803d;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #e2e8f0;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#0b1220;list-style:none}
details summary:before{content:"+ ";color:#22c55e;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #e2e8f0;border-top:4px solid #22c55e;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#44525f;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5a6b7b;padding:14px 0 0}
.crumb a{color:#5a6b7b}
footer{background:#0b1220;color:#94a3b8;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#94a3b8}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #1f2937;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#64748b}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #e2e8f0;border-top:4px solid #22c55e;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#0b1220}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(11,18,32,.06)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#0b1220}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#22c55e;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#22c55e;color:#0b1220;text-align:center;padding:32px 0}
.audit h2{color:#0b1220;margin-bottom:8px}.audit a.btn{background:#0b1220;color:#fff}
"""

# Gate 1 — 10 × 10 (Trade OS: systems, indicators, TradingView, order books, crypto calls)
HUBS = [
    {
        "slug": "tradingview-integration",
        "name": "TradingView Integration",
        "short": "TradingView",
        "blurb": "Connect Trade OS indicators, alerts, and workflows to TradingView charts and alert pipelines.",
        "children": [
            ("tradingview-indicator-overlays", "TradingView Indicator Overlays", "Custom overlays that encode Trade OS rules on TradingView charts."),
            ("tradingview-alert-setup", "TradingView Alert Setup", "Alert configuration that maps chart events to actionable notifications."),
            ("pine-script-indicator-hooks", "Pine Script Indicator Hooks", "Pine-oriented hooks so custom logic can live inside TradingView."),
            ("multi-timeframe-tv-layouts", "Multi-Timeframe TV Layouts", "Layouts that keep higher- and lower-timeframe context visible."),
            ("tv-webhook-alert-bridges", "TV Webhook Alert Bridges", "Bridge TradingView alerts into external notification or automation paths."),
            ("watchlist-and-symbol-sync", "Watchlist & Symbol Sync", "Keep major crypto pairs aligned across TradingView and Trade OS views."),
            ("chart-template-standardization", "Chart Template Standardization", "Shared templates so the desk reads the same structure every session."),
            ("tv-to-trade-call-handoff", "TV-to-Trade-Call Handoff", "Move from chart context into published trade-call workflows cleanly."),
            ("indicator-visibility-controls", "Indicator Visibility Controls", "Show only the layers that matter for the current market regime."),
            ("tradingview-workspace-onboarding", "TradingView Workspace Onboarding", "Get new users oriented on the Trade OS + TradingView stack."),
        ],
    },
    {
        "slug": "custom-trading-indicators",
        "name": "Custom Trading Indicators",
        "short": "Indicators",
        "blurb": "Purpose-built indicators for crypto markets — clarity on charts without invented win-rate claims.",
        "children": [
            ("momentum-and-trend-indicators", "Momentum & Trend Indicators", "Trend and momentum readouts tuned for major crypto pairs."),
            ("volatility-band-indicators", "Volatility Band Indicators", "Band-style tools for expansion and compression regimes."),
            ("volume-profile-style-reads", "Volume Profile–Style Reads", "Volume-context layers to frame where participation clusters."),
            ("order-flow-aware-indicators", "Order-Flow-Aware Indicators", "Indicators that respect book and flow context, not price alone."),
            ("multi-asset-indicator-packs", "Multi-Asset Indicator Packs", "Shared logic across BTC, ETH, XRP, SOL, SUI, and other majors."),
            ("alertable-custom-signals", "Alertable Custom Signals", "Indicators designed so alerts fire on defined, documented rules."),
            ("indicator-parameter-playbooks", "Indicator Parameter Playbooks", "Documented defaults and adjustment guidance — no black-box mystery."),
            ("regime-filter-indicators", "Regime Filter Indicators", "Filters that help separate trend, range, and high-noise conditions."),
            ("indicator-qa-and-versioning", "Indicator QA & Versioning", "Versioned releases so chart logic does not silently drift."),
            ("desk-ready-indicator-docs", "Desk-Ready Indicator Docs", "Plain-language docs so the whole desk reads the same definition."),
        ],
    },
    {
        "slug": "order-book-analysis",
        "name": "Order Book Analysis",
        "short": "Order Book",
        "blurb": "Order book analysis to frame liquidity, depth, and short-horizon pressure around major crypto markets.",
        "children": [
            ("depth-and-liquidity-reads", "Depth & Liquidity Reads", "See where resting size sits before size goes on."),
            ("bid-ask-imbalance-views", "Bid-Ask Imbalance Views", "Imbalance framing for short-horizon pressure."),
            ("wall-and-spoof-awareness", "Wall & Spoof Awareness", "Context for large visible levels that may not be sticky."),
            ("spread-and-microstructure-basics", "Spread & Microstructure Basics", "Understand spread behavior without overclaiming edge."),
            ("book-heatmaps-for-majors", "Book Heatmaps for Majors", "Visual depth context on Bitcoin, Ethereum, and other majors."),
            ("liquidity-void-identification", "Liquidity Void Identification", "Spot thin zones where moves can accelerate."),
            ("session-liquidity-comparisons", "Session Liquidity Comparisons", "Compare book conditions across sessions and venues."),
            ("order-book-plus-indicator-stack", "Order Book + Indicator Stack", "Combine book context with Trade OS custom indicators."),
            ("book-alert-triggers", "Book Alert Triggers", "Alerts when depth or imbalance crosses defined thresholds."),
            ("order-book-research-notes", "Order Book Research Notes", "Structured notes that turn book observations into research, not hype."),
        ],
    },
    {
        "slug": "cryptocurrency-trade-calls",
        "name": "Cryptocurrency Trade Calls",
        "short": "Trade Calls",
        "blurb": "Informational crypto trade calls grounded in systems and indicators — not guaranteed outcomes.",
        "children": [
            ("structured-crypto-trade-calls", "Structured Crypto Trade Calls", "Calls with clear thesis, levels, and invalidation — not vague tips."),
            ("entry-and-invalidation-framing", "Entry & Invalidation Framing", "Every call framed with what would prove the idea wrong."),
            ("multi-timeframe-call-context", "Multi-Timeframe Call Context", "Higher-timeframe bias plus lower-timeframe timing notes."),
            ("risk-size-and-position-notes", "Risk Size & Position Notes", "Sizing commentary as process — never as a promise of profit."),
            ("bitcoin-and-alt-call-coverage", "Bitcoin & Alt Call Coverage", "Calls across BTC and major alts when conditions warrant."),
            ("call-delivery-channels", "Call Delivery Channels", "Delivery paths matched to how your desk actually watches markets."),
            ("post-call-review-process", "Post-Call Review Process", "Review what fired and what changed — learning without win-rate theater."),
            ("trade-call-alert-hygiene", "Trade Call Alert Hygiene", "Reduce noise so calls stay actionable."),
            ("indicator-backed-call-rationale", "Indicator-Backed Call Rationale", "Calls tied to documented indicators and book context."),
            ("disclaimer-forward-call-comms", "Disclaimer-Forward Call Comms", "Risk language and non-advice framing built into delivery."),
        ],
    },
    {
        "slug": "bitcoin-trading-systems",
        "name": "Bitcoin Trading Systems",
        "short": "Bitcoin",
        "blurb": "Trading systems and indicator stacks oriented to Bitcoin market structure and liquidity.",
        "children": [
            ("btc-trend-following-systems", "BTC Trend-Following Systems", "System rules for Bitcoin trend regimes with clear exits."),
            ("btc-range-and-mean-reversion", "BTC Range & Mean Reversion", "Range-oriented frameworks when Bitcoin is chopping."),
            ("btc-volatility-breakout-rules", "BTC Volatility Breakout Rules", "Breakout logic tied to expansion in Bitcoin volatility."),
            ("bitcoin-indicator-suite", "Bitcoin Indicator Suite", "BTC-focused custom indicators for TradingView workflows."),
            ("btc-order-book-context", "BTC Order Book Context", "Depth and imbalance reads around Bitcoin books."),
            ("btc-session-and-event-playbooks", "BTC Session & Event Playbooks", "Process around high-impact sessions and known event windows."),
            ("bitcoin-alert-stacks", "Bitcoin Alert Stacks", "Alert trees that escalate from watch to actionable levels."),
            ("btc-system-parameter-guides", "BTC System Parameter Guides", "Documented parameters — adjustable, not mystical."),
            ("bitcoin-research-briefs", "Bitcoin Research Briefs", "Short research notes that feed systems — not price targets as prophecy."),
            ("btc-to-alt-correlation-notes", "BTC-to-Alt Correlation Notes", "How Bitcoin regime often sets the tone for alt coverage."),
        ],
    },
    {
        "slug": "ethereum-trading-systems",
        "name": "Ethereum Trading Systems",
        "short": "Ethereum",
        "blurb": "Ethereum-focused systems, indicators, and trade-call context for ETH market participants.",
        "children": [
            ("eth-trend-system-frameworks", "ETH Trend System Frameworks", "Trend rules tailored to Ethereum liquidity and pace."),
            ("eth-btc-relative-strength", "ETH/BTC Relative Strength", "Relative views that matter when ETH leads or lags Bitcoin."),
            ("ethereum-indicator-overlays", "Ethereum Indicator Overlays", "Custom ETH indicators for TradingView and desk templates."),
            ("eth-order-book-analysis", "ETH Order Book Analysis", "Book depth and imbalance context for Ethereum."),
            ("eth-volatility-and-expansion", "ETH Volatility & Expansion", "Tools for expansion/compression regimes in ETH."),
            ("ethereum-trade-call-coverage", "Ethereum Trade Call Coverage", "Informational ETH calls with invalidation and risk framing."),
            ("eth-multi-timeframe-layouts", "ETH Multi-Timeframe Layouts", "Layouts that keep ETH structure readable across timeframes."),
            ("gas-and-network-context-notes", "Gas & Network Context Notes", "Optional network-context notes when they affect trading workflow."),
            ("eth-alert-and-research-loop", "ETH Alert & Research Loop", "Alerts that feed research reviews, not chase every tick."),
            ("ethereum-system-documentation", "Ethereum System Documentation", "Written rules so ETH systems stay operable by the desk."),
        ],
    },
    {
        "slug": "xrp-sol-sui-markets",
        "name": "XRP, Solana & Sui Markets",
        "short": "XRP · SOL · SUI",
        "blurb": "Coverage for XRP, Solana, and Sui — indicators, books, and systems where liquidity supports process.",
        "children": [
            ("xrp-trading-systems", "XRP Trading Systems", "System frameworks for XRP when structure and liquidity align."),
            ("solana-trading-systems", "Solana Trading Systems", "SOL-oriented systems and indicator packs."),
            ("sui-market-frameworks", "Sui Market Frameworks", "SUI coverage with the same process discipline as majors."),
            ("xrp-sol-sui-indicator-packs", "XRP / SOL / SUI Indicator Packs", "Custom indicators tuned per asset without copy-paste laziness."),
            ("alt-order-book-reads", "Alt Order Book Reads", "Book analysis for these alts when depth is meaningful."),
            ("cross-asset-rotation-notes", "Cross-Asset Rotation Notes", "Research notes when capital rotates among XRP, SOL, and SUI."),
            ("alt-volatility-playbooks", "Alt Volatility Playbooks", "Process for sharper alt volatility without overconfidence."),
            ("tradingview-alt-layouts", "TradingView Alt Layouts", "TV layouts dedicated to XRP, SOL, and SUI workflows."),
            ("alt-trade-call-coverage", "Alt Trade Call Coverage", "Informational calls on these markets when setups meet criteria."),
            ("liquidity-aware-alt-sizing", "Liquidity-Aware Alt Sizing", "Sizing notes that respect thinner books — not bravado."),
        ],
    },
    {
        "slug": "multi-crypto-coverage",
        "name": "Multi-Crypto Market Coverage",
        "short": "Multi-Crypto",
        "blurb": "Broader major-cryptocurrency coverage beyond the core set — systems and research with liquidity awareness.",
        "children": [
            ("major-pair-universe-design", "Major Pair Universe Design", "Define which majors belong on the active desk universe."),
            ("cross-market-indicator-consistency", "Cross-Market Indicator Consistency", "Same indicator definitions across assets so comparisons are fair."),
            ("multi-asset-watchlist-ops", "Multi-Asset Watchlist Ops", "Watchlist hygiene so coverage stays intentional."),
            ("correlation-and-beta-context", "Correlation & Beta Context", "Context for when alts move with or against Bitcoin."),
            ("liquidity-tiering-for-coverage", "Liquidity Tiering for Coverage", "Tier markets so thin names do not get major-pair treatment."),
            ("multi-crypto-alert-routing", "Multi-Crypto Alert Routing", "Route alerts by asset priority and desk attention."),
            ("coverage-research-cadence", "Coverage Research Cadence", "A repeatable research rhythm across the covered universe."),
            ("new-asset-onboarding-checklist", "New Asset Onboarding Checklist", "Add a market only when books, data, and process are ready."),
            ("weekend-and-offhours-coverage", "Weekend & Off-Hours Coverage", "Crypto never sleeps — process for thin off-hours sessions."),
            ("universe-review-governance", "Universe Review Governance", "Periodic review of what stays on coverage — and what drops."),
        ],
    },
    {
        "slug": "trading-system-automation",
        "name": "Trading System Automation",
        "short": "Automation",
        "blurb": "Automate alerts, handoffs, and system routines — with kill switches and human oversight, not blind robots.",
        "children": [
            ("alert-to-action-pipelines", "Alert-to-Action Pipelines", "Move from indicator alert to a defined next step."),
            ("semi-automated-execution-hooks", "Semi-Automated Execution Hooks", "Hooks that assist execution without removing human judgment."),
            ("webhook-and-notification-bridges", "Webhook & Notification Bridges", "Bridge TradingView and Trade OS alerts into desk channels."),
            ("system-runbook-automation", "System Runbook Automation", "Automate the boring checklist steps so process is consistent."),
            ("kill-switch-and-fail-safes", "Kill Switch & Fail-Safes", "Hard stops when feeds, books, or logic misbehave."),
            ("paper-mode-system-rehearsal", "Paper-Mode System Rehearsal", "Rehearse automation before live size."),
            ("parameter-update-workflows", "Parameter Update Workflows", "Controlled updates when market regimes change."),
            ("uptime-and-feed-monitoring", "Uptime & Feed Monitoring", "Know when data or alert paths go dark."),
            ("automation-audit-logging", "Automation Audit Logging", "A trail of what fired, when, and what happened next."),
            ("human-in-the-loop-controls", "Human-in-the-Loop Controls", "Keep accountability on the desk — automation assists, not absolves."),
        ],
    },
    {
        "slug": "strategy-research-alerts",
        "name": "Strategy, Research & Alerts",
        "short": "Research",
        "blurb": "Strategy research, structured alerts, and review loops that support Trade OS systems — without performance theater.",
        "children": [
            ("strategy-research-briefs", "Strategy Research Briefs", "Short, structured briefs that feed system design."),
            ("hypothesis-and-invalidation-logs", "Hypothesis & Invalidation Logs", "Write the thesis and the kill criteria before size."),
            ("alert-taxonomy-design", "Alert Taxonomy Design", "Name and tier alerts so the desk is not drowned."),
            ("multi-channel-alert-delivery", "Multi-Channel Alert Delivery", "Deliver research and system alerts where they will be seen."),
            ("regime-change-monitoring", "Regime Change Monitoring", "Watch for trend/range shifts that invalidate playbooks."),
            ("post-trade-and-post-call-reviews", "Post-Trade & Post-Call Reviews", "Review process for learning — not scoreboard vanity."),
            ("indicator-research-collaboration", "Indicator Research Collaboration", "Collaborate on indicator ideas before they hit production charts."),
            ("desk-playbook-documentation", "Desk Playbook Documentation", "Playbooks the team can run without tribal knowledge."),
            ("research-to-system-handoff", "Research-to-System Handoff", "Promote research into systems only after criteria are met."),
            ("compliance-minded-comms", "Compliance-Minded Comms", "Keep research and calls clearly non-advisory and risk-forward."),
        ],
    },
]

MARKETS = [
    "Bitcoin (BTC)",
    "Ethereum (ETH)",
    "XRP",
    "Solana (SOL)",
    "Sui (SUI)",
    "Other major cryptocurrencies",
    "TradingView-centric desks",
    "Systematic / indicator-led traders",
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
    return f"""<div class="utility"><div class="wrap"><span>{escape(TAGLINE)}</span><span>{escape(HQ)} &middot; {escape(EMAIL)} <em>[confirm]</em></span></div></div>
<header class="main"><div class="wrap">
<div class="logo">Trade <span>OS</span><small>Systems · Indicators · Crypto Calls</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Trading systems &amp; indicators · *[confirm]*</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-trade-os/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-trade-os/index.html">About Trade OS</a>
<a href="{p}about-trade-os/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-trade-os/markets-we-cover/index.html">Markets We Cover</a>
</div></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li><a href="{p}request-a-proposal/index.html">Proposal</a></li>
<li class="em"><a href="{p}request-a-consultation/index.html">Consultation</a></li>
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
<li><a href="{p}about-trade-os/index.html">About Trade OS</a></li>
<li><a href="{p}about-trade-os/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-trade-os/markets-we-cover/index.html">Markets We Cover</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}request-a-consultation/index.html">Request a Consultation</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul><li>{escape(ADDRESS)} <em>[confirm]</em></li><li>Operated by {escape(OPERATOR)} <em>[confirm]</em></li><li>{escape(HQ)}</li></ul></div>
</div>
<div class="copy">Trade OS &middot; {escape(HQ)} &middot; {escape(PHONE)} <em>[confirm NAP / domain]</em><br>
Copyright &copy; 2026. Trade OS / {escape(OPERATOR)}. All rights reserved.<br>
{escape(RISK)}</div></div></footer>
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
<label>I am a…</label><select><option>Please choose&hellip;</option><option>Active Trader</option><option>Trading Desk / Fund</option><option>Systematic / Indicator User</option><option>New to crypto systems</option><option>Other</option></select>
<label>Interest</label><select><option>Please choose&hellip;</option>{opts}<option>Consultation / Demo</option><option>Custom Indicators</option><option>Trade Calls</option><option>Other</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f95a8">Demo form shell — submission destination wired at rollout. Not investment advice.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Trade OS",
        "email": EMAIL,
        "telephone": PHONE_TEL,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "description": (
            "Trade OS — trading systems and indicators with TradingView integration, "
            "cryptocurrency trade calls, custom indicators, and order book analysis across "
            "Bitcoin, Ethereum, XRP, Solana, Sui, and other major cryptocurrencies."
        ),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "12 Sayre St",
            "addressLocality": "Elizabeth",
            "addressRegion": "NJ",
            "postalCode": "07208",
            "addressCountry": "US",
        },
        "areaServed": "US",
        "parentOrganization": {
            "@type": "Organization",
            "name": OPERATOR,
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
            "Trade OS | Trading Systems, Custom Indicators & Crypto Trade Calls",
            "Trade OS — trading systems and indicators with TradingView integration, crypto trade calls, "
            "custom indicators, and order book analysis across Bitcoin, Ethereum, XRP, Solana, Sui, and more.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>Trade OS — Trading systems and indicators with TradingView integration, crypto trade calls, custom indicators, and order book analysis</h1>
<p>{escape(TAGLINE)} · Bitcoin, Ethereum, XRP, Solana, Sui &amp; other majors</p>
<a class="btn" href="request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="tradingview-integration/index.html">Explore Services</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>TV</b><span>TradingView Ready</span></div>
<div class="stat"><b>10</b><span>Service Families</span></div>
<div class="stat"><b>Majors</b><span>BTC · ETH · XRP · SOL · SUI</span></div>
<div class="stat"><b>NJ</b><span>{escape(HQ)} *[confirm]*</span></div>
</div>
<p class="risk">{escape(RISK)}</p>
</div></section>
<section><div class="wrap"><h2>What can Trade OS deliver for your desk?</h2>
<p class="lead">Ten service families — TradingView integration, custom indicators, order book analysis, crypto trade calls, Bitcoin &amp; Ethereum systems, XRP/SOL/SUI markets, multi-crypto coverage, automation, and research alerts.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure where to start? Begin with a consultation.</h2>
<p style="margin-bottom:14px">Tell us whether you need TradingView wiring, custom indicators, order book tools, or trade-call workflows.</p>
<a class="btn" href="request-a-consultation/index.html">Request a Consultation</a></div></div>
<section><div class="wrap"><h2>How engagements get started</h2><div class="cols3">
<div class="card"><h3>1. Request a consultation</h3><p>Share markets, tools (especially TradingView), and whether you need systems, indicators, or calls.</p></div>
<div class="card"><h3>2. Scoped recommendation</h3><p>We map the right service line — no invented performance claims.</p></div>
<div class="card"><h3>3. Build &amp; document</h3><p>Indicators, books, alerts, and handoff so your desk can operate the stack.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why Trade OS</h2><div class="cols3">
<div class="card"><h3>Systems + indicators</h3><p>Trading systems and custom indicators designed for crypto market structure.</p></div>
<div class="card"><h3>TradingView integration</h3><p>Chart, alert, and overlay workflows that live where traders already work.</p></div>
<div class="card"><h3>Risk-forward</h3><p>Trade calls and research with clear non-advice framing — crypto involves risk of loss.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready to review the Trade OS stack?</h2>
<a class="btn" href="request-a-consultation/index.html">Consultation</a> <a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a>
<p class="risk" style="max-width:720px;margin:18px auto 0;text-align:left">{escape(RISK)}</p>
</div></div>
"""
        + faqs(
            [
                (
                    "What is Trade OS?",
                    "Trade OS is a trading systems and indicator service — TradingView integration, custom indicators, "
                    "order book analysis, and informational cryptocurrency trade calls across Bitcoin, Ethereum, "
                    "XRP, Solana, Sui, and other major cryptocurrencies.",
                ),
                (
                    "Is Trade OS financial advice?",
                    "No. Trade OS provides systems, indicators, and informational trade calls. Cryptocurrency trading "
                    "involves risk of loss. Nothing on this site is investment, financial, or trading advice.",
                ),
                (
                    "How do I get started?",
                    "Use Request a Consultation or Request a Proposal — share your markets, TradingView setup, and goals.",
                ),
                (
                    "Which markets do you cover?",
                    "Core coverage includes Bitcoin, Ethereum, XRP, Solana, Sui, and many other major cryptocurrencies — "
                    "subject to liquidity and process readiness.",
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
<p class="lead">{escape(h["blurb"])} Delivered as part of the Trade OS trading-systems stack rather than an isolated tip.</p>
<p><a class="btn" href="../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
<p class="risk">{escape(RISK)}</p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Solutions We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What Your Engagement Can Include</h2>
<ul class="checks">
<li>Discovery tied to your markets and TradingView workflow</li>
<li>Documented indicator and system rules — no black-box theater</li>
<li>Order book and alert context where it matters</li>
<li>Risk and non-advice framing on calls and research</li>
<li>One accountable Trade OS path across systems and indicators</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with a consultation. We map markets, tools, and the right Trade OS service line before build work starts.",
                ),
                (
                    "Does this guarantee profits?",
                    "No. Cryptocurrency trading involves risk of loss. Trade OS does not guarantee results or publish invented win rates.",
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
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Engage Trade OS for {escape(name.lower())} and related trading-system services.</h2>
<p class="lead">{escape(blurb)} At Trade OS, {escape(name.lower())} sits inside a systems-and-indicators stack — TradingView, books, and documented process for crypto markets.</p>
<p><a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
<p class="risk">{escape(RISK)}</p>
</div></section>
<section class="tint"><div class="wrap"><h2>How {escape(name)} from Trade OS Can Help You:</h2>
<ul class="checks">
<li>Clearer indicator or system ownership on the desk</li>
<li>TradingView-ready overlays, alerts, or handoffs where relevant</li>
<li>Documented rules your team can operate</li>
<li>Order book and multi-crypto context when the market warrants it</li>
<li>Risk-forward framing — no invented performance claims</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} engagement scoped to your markets — not a one-size package</h2>
<p>No two desks need {escape(name.lower())} the same way. We scope around your pairs, TradingView setup, risk limits, and how you consume trade calls or alerts — after a consultation.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Traders avoid key risks by using a developed partner for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with DIY crypto tooling</h3><ul>
<li>Indicators without documented rules or versioning</li>
<li>Alerts that spam until everyone ignores them</li>
<li>Trade tips without invalidation or risk framing</li>
<li>Automation without kill switches or human oversight</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on Trade OS</h3><ul>
<li>Scoped systems and indicators with clear definitions</li>
<li>TradingView and alert hygiene built into delivery</li>
<li>Order book and research context where it adds signal</li>
<li>Explicit non-advice and risk-of-loss language</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>See how {escape(name.lower())} fits your stack</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} would look like for your markets? Start with a consultation.</p>
<a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} is ready?",
                    "Timelines depend on scope — TradingView wiring, custom indicators, book tools, and call workflows have different critical paths.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Pricing is scoped after consultation — no public rate card is invented for this staging build.",
                ),
                (
                    f"Why choose Trade OS for {name.lower()}?",
                    f"We deliver {name.lower()} as part of Trade OS — trading systems, custom indicators, TradingView integration, "
                    "order book analysis, and crypto trade calls across major cryptocurrencies.",
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
<p class="lead">{escape(lead)}</p>
<p class="risk">{escape(RISK)}</p>
</div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us the project</h3><p>TradingView, indicators, order books, trade calls, or automation.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>A scoped recommendation — or an honest no.</p></div>
<div class="card"><h3>3. Decide with risk in view</h3><p>Crypto trading involves risk of loss; systems and calls are not a profit guarantee.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>Trade OS</strong><br>Operator: {escape(OPERATOR)} <em>[confirm]</em><br>Address: {escape(ADDRESS)} <em>[confirm]</em><br>Phone: {escape(PHONE)} <em>[confirm]</em><br>Email: {escape(EMAIL)} <em>[confirm]</em><br>Domain: tradeos.io <em>[confirm]</em></p>
<p class="risk">{escape(RISK)}</p>
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
        ["/", "HOME", "", "trade os trading systems", "logo/home", "A1,A6,A10", ""],
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
            "/about-trade-os/markets-we-cover/",
            "COMP-CHILD",
            "/about-trade-os/",
            "markets trade os covers",
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
    with (ROOT / "TRADEOS-PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
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
            "About Trade OS",
            "Trade OS — trading systems, custom indicators, TradingView integration, and crypto trade calls.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About Trade OS</h2>
<p class="lead">Trade OS is a trading systems and indicator service — TradingView integration, custom indicators, order book analysis, and informational cryptocurrency trade calls across Bitcoin, Ethereum, XRP, Solana, Sui, and other major cryptocurrencies.</p>
<p class="risk">{escape(RISK)}</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>Operated by {escape(OPERATOR)} <em>[confirm]</em>. Based in {escape(HQ)} <em>[confirm]</em>. We help desks and traders put systems, indicators, and research process around crypto markets — without contractor, SEO, or territory-licensing language, and without invented performance claims.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="markets-we-cover/index.html">Markets we cover &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "What does Trade OS offer?",
                    "Trading systems, custom indicators, TradingView integration, order book analysis, and informational crypto trade calls.",
                ),
                (
                    "Is this investment advice?",
                    "No. Crypto trading involves risk of loss. Trade OS content and calls are informational and not financial advice.",
                ),
            ]
        )
        + org_schema()
        + footer(1),
    )
    urls.append("/about-trade-os/")

    write(
        ROOT / "about-trade-os" / "why-choose-us" / "index.html",
        head("Why Choose Trade OS", "Why traders and desks choose Trade OS.")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose Trade OS</h2>
<p class="lead">Systems, indicators, and TradingView-ready workflows for crypto markets — with risk realism.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Trading systems focus</h3><p>Built around systems and indicators — not contractor marketing or SEO packaging.</p></div>
<div class="card"><h3>TradingView integration</h3><p>Overlays, alerts, and layouts where traders already work.</p></div>
<div class="card"><h3>Custom indicators</h3><p>Documented, versioned indicator logic for major crypto pairs.</p></div>
<div class="card"><h3>Order book analysis</h3><p>Depth and imbalance context alongside chart tools.</p></div>
<div class="card"><h3>Consultation-led</h3><p>Start with a conversation before build or call workflows.</p></div>
<div class="card"><h3>Risk realism</h3><p>Crypto involves loss; we do not invent win rates or promise profits.</p></div>
</div>
<p class="risk">{escape(RISK)}</p>
</div></section>
"""
        + footer(2),
    )
    urls.append("/about-trade-os/why-choose-us/")

    mkt = "".join(
        f'<div class="gcard"><h3>{escape(i)}</h3><p>Coverage and tooling emphasis for {escape(i)}.</p></div>'
        for i in MARKETS
    )
    write(
        ROOT / "about-trade-os" / "markets-we-cover" / "index.html",
        head("Markets We Cover | Trade OS", "Cryptocurrency markets covered by Trade OS.")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Markets We Cover</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Markets We Cover</h2>
<p class="lead">Bitcoin, Ethereum, XRP, Solana, Sui, and many other major cryptocurrencies — with liquidity-aware process.</p>
<div class="grid">{mkt}</div>
<p class="risk">{escape(RISK)}</p>
</div></section>
"""
        + footer(2),
    )
    urls.append("/about-trade-os/markets-we-cover/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | Trade OS",
            "Contact Trade OS",
            "Questions about trading systems, TradingView integration, custom indicators, order book analysis, or crypto trade calls.",
        ),
        (
            "request-a-consultation",
            "Request a Consultation | Trade OS",
            "Request a Consultation",
            "Tell us your markets and tools — we will recommend a practical first step for systems, indicators, or trade calls.",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | Trade OS",
            "Request a Proposal",
            "Share scope and constraints. We will return a scoped proposal you can compare.",
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
        ROOT / "TRADEOS-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — Trade OS (FACTORY BUILD · Gate 1 10×10)

**NearMe OS Website Factory staging engine · category: trading systems / indicators / crypto trade calls · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | Trade OS | owner correction |
| A2 domain | tradeos.io | **[confirm]** |
| A3 phone | {PHONE} | Race CS default **[confirm]** |
| A4 email | {EMAIL} | **[confirm]** |
| A5 address | {ADDRESS} | **[confirm]** |
| A6 trade | Trading systems, custom indicators, TradingView integration & crypto trade calls | owner correction |
| A7 operator | {OPERATOR} | **[confirm]** |
| A10 value_proposition | Trading systems and indicators with TradingView integration, crypto trade calls, custom indicators, and order book analysis across major cryptocurrencies | owner |
| A11 tagline | {TAGLINE} | owner brief |
| A12 markets | Bitcoin, Ethereum, XRP, Solana, Sui, and many other major cryptocurrencies | owner |
| A13 services_core | TradingView integration; custom indicators; order book analysis; crypto trade calls; BTC/ETH/XRP/SOL/SUI systems; multi-crypto coverage; automation; research & alerts | owner |

## B — Services: 10 × 10
{hub_slugs}
FORM-CONSULT=`request-a-consultation` · FORM-PRICING=`request-a-proposal`

## Notes
- Product is trading systems/indicators — **not** contractors, tradespeople, or Near Me territory licensing
- NAP / domain / operator marked [confirm]
- No invented win rates or performance claims
- Risk disclaimer: crypto trading involves risk of loss; not financial advice
- Staging: noindex + STAGING PREVIEW
| hubs | {len(HUBS)} | children | {svc_children} |
""",
    )

    write(
        ROOT / "TRADEOS-NOTES.md",
        f"""# Trade OS — Factory Notes (Gate 1)

- Generator: `scripts/generate_tradeos_factory.py`
- Product: trading systems & indicators (TradingView, trade calls, order books, major cryptos)
- CSS: navy `#0b1220` / `#111827` + signal green `#22c55e` + tint `#f8fafc`
- Staging banner + robots noindex
- Inventory: `TRADEOS-PAGE-INVENTORY.csv`
- Questionnaire: `TRADEOS-QUESTIONNAIRE-ANSWERS.md`
- Hubs: {len(HUBS)} · Children: {svc_children}
- Confirm before go-live: domain, phone, email, address, operator NAP
""",
    )

    factory_pages = list(ROOT.rglob("index.html"))
    print(f"Generated {len(factory_pages)} factory index pages")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)} · Children: {sum(len(h['children']) for h in HUBS)}")


if __name__ == "__main__":
    main()
