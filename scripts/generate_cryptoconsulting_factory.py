#!/usr/bin/env python3
"""Generate Cryptocurrency Consulting site using the NearMe OS Website Factory template.

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: cryptocurrency / blockchain consulting & development.
Facts grounded from live cryptocurrencyconsulting.io (fetched 2026-07-22).
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.cryptocurrencyconsulting.io"
PHONE = "+1 (555) 123-4567"  # on live site — looks placeholder; [confirm]
PHONE_TEL = "+15551234567"
EMAIL = "info@cryptocurrencyconsulting.io"
HQ = "San Francisco, CA"  # on live site — street looks placeholder; [confirm]
ADDRESS = "123 Blockchain Avenue, San Francisco, CA 94105"  # [confirm placeholder]
FOUNDED = "2018"
TAGLINE = "Expert Blockchain Solutions"
STAGING_BANNER = (
    "STAGING PREVIEW — cryptocurrencyconsulting.io factory build · content pending owner review "
    "· not the live Cryptocurrency Consulting website"
)

# NearMe factory CSS (SEO Cow template) with Cryptocurrency Consulting orange remap
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#0f172a;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#059669;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#020617;color:#a7f3d0;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#0f172a;color:#d1fae5;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #10b981;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#0f172a}.logo span{color:#10b981}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#0f172a}
.phone-cta small{display:block;color:#5a6b7b;font-size:11px}
nav.nav{background:#0f172a}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#020617;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #10b981;z-index:60}
.dd a{color:#0f172a;padding:10px 15px;font-weight:500;border-bottom:1px solid #d1fae5}
.dd a:hover{background:#ecfdf5}
.nav .em a{background:#10b981}.nav .em a:hover{background:#059669}
.hero{background:linear-gradient(rgba(2,6,23,.88),rgba(2,6,23,.88)),repeating-linear-gradient(45deg,#0f172a 0 14px,#134e4a 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#a7f3d0;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#10b981;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#f07a3a;text-decoration:none}
.btn.alt{background:#0f172a;color:#fff}.btn.alt:hover{background:#7a3c1a}
section{padding:44px 0}
section.tint{background:#f0fdf4}
section h2{font-size:25px;color:#0f172a;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#10b981;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #d1e7dd;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(16,185,129,.06)}
.card h3{color:#0f172a;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #d1e7dd;border-left:4px solid #10b981;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#0f172a}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#059669}
.ctastrip{background:#0f172a;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #d1e7dd;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#f0fdf4}.vs .col.good{background:#f0fdf4}
.vs h3{font-size:16px;margin-bottom:12px;color:#0f172a}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#059669;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #d1e7dd;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#0f172a;list-style:none}
details summary:before{content:"+ ";color:#10b981;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #d1e7dd;border-top:4px solid #10b981;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#44525f;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5a6b7b;padding:14px 0 0}
.crumb a{color:#5a6b7b}
footer{background:#020617;color:#c9b8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #134e4a;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #d1e7dd;border-top:4px solid #10b981;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#0f172a}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #d1e7dd;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(16,185,129,.08)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#0f172a}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#10b981;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#10b981;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#0f172a}
"""

# Gate 1 — 10 × 10 (user revision request ~100 pages; grounded in product landing)
HUBS = [
    {
        "slug": "trading-bot-development",
        "name": "Trading Bot Development",
        "short": "Trading Bots",
        "blurb": "Custom trading bot solutions to automate cryptocurrency strategies — from live site core services.",
        "children": [
            ("custom-crypto-trading-bots", "Custom Crypto Trading Bots", "Bots built around your rules, venues, and risk limits."),
            ("spot-trading-bot-development", "Spot Trading Bot Development", "Automate spot entries and exits without babysitting charts."),
            ("futures-bot-development", "Futures Bot Development", "Automation patterns for perpetual/futures workflows where supported."),
            ("grid-trading-bot-systems", "Grid Trading Bot Systems", "Grid-style automation for ranging market conditions."),
            ("dca-bot-strategies", "DCA Bot Strategies", "Dollar-cost averaging automation with schedule and size controls."),
            ("exchange-api-integrations", "Exchange API Integrations", "Connect bots to exchange APIs with key hygiene and permissions."),
            ("paper-trading-bot-modes", "Paper Trading Bot Modes", "Test logic in simulation before real capital."),
            ("bot-monitoring-and-alerts", "Bot Monitoring & Alerts", "Uptime, fill, and error alerts so failures are not silent."),
            ("risk-controls-for-bots", "Risk Controls for Bots", "Kill switches, max drawdown stops, and position caps."),
            ("bot-maintenance-and-tuning", "Bot Maintenance & Tuning", "Ongoing parameter updates as markets and APIs change."),
        ],
    },
    {
        "slug": "signals-and-webhooks",
        "name": "Signals and Webhooks",
        "short": "Signals",
        "blurb": "Real-time trading signals and webhook integration for timely market actions — from live site services.",
        "children": [
            ("realtime-trading-signals", "Real-Time Trading Signals", "Signal delivery designed for actionable timing, not noise."),
            ("webhook-strategy-execution", "Webhook Strategy Execution", "Push signals into bots and execution stacks via webhooks."),
            ("tradingview-webhook-bridges", "TradingView Webhook Bridges", "Bridge chart alerts into automated or semi-automated workflows."),
            ("multi-channel-signal-delivery", "Multi-Channel Signal Delivery", "Route alerts to the channels your desk actually watches."),
            ("signal-filtering-and-scoring", "Signal Filtering & Scoring", "Reduce alert spam with filters matched to your risk profile."),
            ("latency-aware-signal-pipelines", "Latency-Aware Signal Pipelines", "Design for the delay between signal and fill."),
            ("signal-audit-logging", "Signal Audit Logging", "Keep a trail of what fired, when, and what happened next."),
            ("webhook-security-hardening", "Webhook Security Hardening", "Auth, signing, and endpoint hygiene for inbound webhooks."),
            ("fail-safe-signal-handling", "Fail-Safe Signal Handling", "What the system does when a webhook fails mid-flight."),
            ("signal-to-bot-orchestration", "Signal-to-Bot Orchestration", "Connect signal sources to bot fleets cleanly."),
        ],
    },
    {
        "slug": "blockchain-node-deployment",
        "name": "Blockchain Node Deployment",
        "short": "Nodes",
        "blurb": "Professional setup and maintenance of blockchain nodes for network participation and security.",
        "children": [
            ("full-node-deployment", "Full Node Deployment", "Stand up full nodes with sensible defaults and monitoring."),
            ("validator-node-setup", "Validator Node Setup", "Validator-oriented setup guidance where the network requires it."),
            ("rpc-node-infrastructure", "RPC Node Infrastructure", "RPC endpoints for apps and internal tooling."),
            ("node-monitoring-and-uptime", "Node Monitoring & Uptime", "Watch sync, peers, disk, and process health."),
            ("node-security-hardening", "Node Security Hardening", "Firewalling, key handling, and least-privilege ops."),
            ("backup-and-recovery-for-nodes", "Backup & Recovery for Nodes", "Recovery plans when a disk or host fails."),
            ("multi-chain-node-operations", "Multi-Chain Node Operations", "Operate more than one chain without tribal knowledge silos."),
            ("cloud-vs-bare-metal-nodes", "Cloud vs Bare-Metal Nodes", "Host choices matched to cost, latency, and control."),
            ("node-upgrade-playbooks", "Node Upgrade Playbooks", "Version upgrades without surprise downtime."),
            ("network-participation-support", "Network Participation Support", "Ongoing ops so participation stays reliable."),
        ],
    },
    {
        "slug": "trade-strategy-and-indicators",
        "name": "Trade Strategy and Indicators",
        "short": "Strategy",
        "blurb": "Custom trading strategies and technical indicators tailored to your risk profile.",
        "children": [
            ("custom-crypto-trade-strategies", "Custom Crypto Trade Strategies", "Strategy design matched to horizon, liquidity, and risk."),
            ("technical-indicator-development", "Technical Indicator Development", "Custom indicators that encode your rules clearly."),
            ("risk-profile-strategy-fit", "Risk Profile Strategy Fit", "Match aggression to what the account can actually survive."),
            ("backtesting-frameworks", "Backtesting Frameworks", "Test ideas against history before they touch live size."),
            ("walk-forward-validation", "Walk-Forward Validation", "Reduce curve-fit risk with out-of-sample checks."),
            ("portfolio-level-crypto-strategy", "Portfolio-Level Crypto Strategy", "Think beyond one pair — correlation and concentration matter."),
            ("market-regime-playbooks", "Market Regime Playbooks", "Different rules for trend, range, and panic regimes."),
            ("execution-quality-review", "Execution Quality Review", "Slippage and fill quality as part of strategy truth."),
            ("strategy-documentation", "Strategy Documentation", "Written rules so the desk is not tribal knowledge."),
            ("indicator-to-automation-handoff", "Indicator-to-Automation Handoff", "Move from chart logic into bots and webhooks cleanly."),
        ],
    },
    {
        "slug": "smart-contract-development",
        "name": "Smart Contract Development",
        "short": "Smart Contracts",
        "blurb": "Creation and auditing of secure, efficient smart contracts for blockchain applications.",
        "children": [
            ("solidity-smart-contract-development", "Solidity Smart Contract Development", "Contract design and implementation for EVM environments."),
            ("token-contract-development", "Token Contract Development", "Token standards implemented with clear ownership and mint rules."),
            ("defi-contract-prototyping", "DeFi Contract Prototyping", "Prototype DeFi mechanics with security in mind from day one."),
            ("nft-contract-development", "NFT Contract Development", "NFT contract patterns when the product requires them."),
            ("upgradeable-contract-patterns", "Upgradeable Contract Patterns", "Upgrade paths with explicit governance and risk tradeoffs."),
            ("smart-contract-testing", "Smart Contract Testing", "Unit and integration tests before mainnet."),
            ("gas-efficiency-reviews", "Gas Efficiency Reviews", "Cut wasteful patterns that inflate user costs."),
            ("contract-deployment-pipelines", "Contract Deployment Pipelines", "Repeatable deploy steps across testnets and mainnet."),
            ("smart-contract-documentation", "Smart Contract Documentation", "Interfaces and assumptions written for auditors and integrators."),
            ("post-deploy-monitoring", "Post-Deploy Monitoring", "Watch events and anomalies after launch."),
        ],
    },
    {
        "slug": "crypto-security-audits",
        "name": "Crypto Security Audits",
        "short": "Security Audits",
        "blurb": "Comprehensive security audits to protect digital assets against threats and vulnerabilities.",
        "children": [
            ("smart-contract-security-audits", "Smart Contract Security Audits", "Review contracts for common and protocol-specific failure modes."),
            ("wallet-and-key-management-review", "Wallet & Key Management Review", "How keys are stored, rotated, and accessed."),
            ("exchange-account-security-review", "Exchange Account Security Review", "API keys, withdrawals, and operational hygiene."),
            ("infrastructure-security-for-crypto", "Infrastructure Security for Crypto", "Hosts, RPC, and bot infrastructure threat modeling."),
            ("incident-response-readiness", "Incident Response Readiness", "What to do in the first hour of a compromise."),
            ("penetration-testing-for-dapps", "Penetration Testing for dApps", "App-layer testing around wallet connects and privileged actions."),
            ("dependency-and-supply-chain-review", "Dependency & Supply-Chain Review", "Third-party libraries and deploy tooling risks."),
            ("access-control-reviews", "Access Control Reviews", "Who can pause, upgrade, mint, or move funds."),
            ("security-remediation-support", "Security Remediation Support", "Fix guidance after findings — not just a PDF."),
            ("ongoing-security-monitoring", "Ongoing Security Monitoring", "Keep watching after the audit engagement ends."),
        ],
    },
    {
        "slug": "digital-asset-consulting",
        "name": "Digital Asset Consulting",
        "short": "Digital Assets",
        "blurb": "Guidance for businesses and individuals navigating digital asset management — mission from live About copy.",
        "children": [
            ("crypto-portfolio-strategy-consulting", "Crypto Portfolio Strategy Consulting", "Structure exposure with risk awareness, not hype cycles."),
            ("market-volatility-navigation", "Market Volatility Navigation", "Process for volatile regimes instead of reactive panic."),
            ("digital-asset-onboarding", "Digital Asset Onboarding", "First wallets, venues, and operational basics done safely."),
            ("custody-options-overview", "Custody Options Overview", "Self-custody vs third-party tradeoffs explained clearly."),
            ("treasury-crypto-policy-basics", "Treasury Crypto Policy Basics", "High-level policy framing for teams holding digital assets."),
            ("risk-minimization-playbooks", "Risk Minimization Playbooks", "Practical controls that reduce operational foot-guns."),
            ("exchange-and-venue-selection", "Exchange & Venue Selection", "Choose venues based on needs, not Twitter momentum."),
            ("reporting-and-recordkeeping-basics", "Reporting & Recordkeeping Basics", "Keep a trail that ops and advisors can follow."),
            ("education-for-new-investors", "Education for New Investors", "Live testimonials highlight education for newcomers — structured onboarding."),
            ("ongoing-advisory-retainers", "Ongoing Advisory Retainers", "Continuing guidance as markets and tooling change."),
        ],
    },
    {
        "slug": "blockchain-implementation",
        "name": "Blockchain Implementation",
        "short": "Implementation",
        "blurb": "Help organizations implement blockchain where it creates real operational value — not theater.",
        "children": [
            ("blockchain-use-case-assessment", "Blockchain Use-Case Assessment", "Decide whether a chain is the right tool before you build."),
            ("supply-chain-tracking-implementations", "Supply Chain Tracking Implementations", "Live testimonial theme — tracking capabilities via blockchain services."),
            ("enterprise-blockchain-pilots", "Enterprise Blockchain Pilots", "Scoped pilots with success criteria and exit ramps."),
            ("integration-with-existing-systems", "Integration with Existing Systems", "Connect chain components to the software you already run."),
            ("permissioned-vs-public-chain-choice", "Permissioned vs Public Chain Choice", "Pick the network model that matches governance needs."),
            ("data-model-and-oracle-design", "Data Model & Oracle Design", "What belongs on-chain vs off-chain — and how truth enters."),
            ("stakeholder-training-for-rollouts", "Stakeholder Training for Rollouts", "Operators need to understand the new workflow."),
            ("governance-and-upgrade-planning", "Governance & Upgrade Planning", "Who decides changes after launch."),
            ("implementation-project-management", "Implementation Project Management", "Milestones, owners, and risk logs for delivery."),
            ("post-launch-optimization", "Post-Launch Optimization", "Tune after real usage shows where friction is."),
        ],
    },
    {
        "slug": "crypto-security-operations",
        "name": "Crypto Security Operations",
        "short": "SecOps",
        "blurb": "Operational security for teams whose fintech and cybersecurity experience must protect real assets.",
        "children": [
            ("secure-ops-runbooks", "Secure Ops Runbooks", "Documented steps for deposits, withdrawals, and deploys."),
            ("multi-sig-operations", "Multi-Sig Operations", "Multi-party approvals for high-value actions."),
            ("secrets-management-for-crypto-stacks", "Secrets Management for Crypto Stacks", "API keys, seed material, and env secrets handled as hazards."),
            ("employee-access-lifecycle", "Employee Access Lifecycle", "Joiners/movers/leavers for crypto tooling access."),
            ("phishing-and-social-engineering-defense", "Phishing & Social Engineering Defense", "Human-layer attacks are still the shortest path to funds."),
            ("cold-storage-procedures", "Cold Storage Procedures", "Offline custody workflows when appropriate."),
            ("hot-wallet-limits", "Hot Wallet Limits", "Cap online balances so a breach has a ceiling."),
            ("vendor-risk-for-crypto-tools", "Vendor Risk for Crypto Tools", "Assess SaaS and infra vendors that touch keys or funds."),
            ("security-awareness-for-crypto-teams", "Security Awareness for Crypto Teams", "Training tuned to wallet and signing threats."),
            ("compliance-minded-security-controls", "Compliance-Minded Security Controls", "Controls that help conversations with counsel and auditors."),
        ],
    },
    {
        "slug": "fintech-consulting-engagements",
        "name": "Fintech Consulting Engagements",
        "short": "Engagements",
        "blurb": "Engagement models for getting started, expanding a portfolio, or shipping blockchain work — from live About copy.",
        "children": [
            ("discovery-and-scoping-workshops", "Discovery & Scoping Workshops", "Clarify goals, constraints, and a realistic first milestone."),
            ("fixed-scope-delivery-projects", "Fixed-Scope Delivery Projects", "Clear deliverables for bots, contracts, nodes, or audits."),
            ("retainer-advisory-support", "Retainer Advisory Support", "Ongoing access for decisions that do not wait for a new SOW."),
            ("technical-due-diligence", "Technical Due Diligence", "Independent eyes on a protocol, stack, or vendor claim."),
            ("architecture-reviews", "Architecture Reviews", "Design reviews before expensive build mistakes."),
            ("team-augmentation-for-crypto-builds", "Team Augmentation for Crypto Builds", "Specialists alongside your internal team."),
            ("vendor-selection-support", "Vendor Selection Support", "Compare tools and partners with a scorecard."),
            ("executive-briefings", "Executive Briefings", "Plain-English updates for non-technical stakeholders."),
            ("roadmap-and-prioritization", "Roadmap & Prioritization", "Sequence work so risk and value move together."),
            ("handoff-and-knowledge-transfer", "Handoff & Knowledge Transfer", "Leave your team able to operate what was built."),
        ],
    },
]

INDUSTRIES = [
    "Investment & Asset Managers",
    "Logistics & Supply Chain",
    "Private Investors",
    "Fintech Startups",
    "Trading Desks",
    "Web3 Builders",
    "Enterprise IT Leaders",
    "Security-Conscious Teams",
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
<div class="logo">Crypto <span>Consulting</span><small>Blockchain Solutions</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Mon–Fri 9am–6pm · Sat 10am–2pm *[confirm]*</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-cryptocurrency-consulting/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-cryptocurrency-consulting/index.html">About Cryptocurrency Consulting</a>
<a href="{p}about-cryptocurrency-consulting/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-cryptocurrency-consulting/who-we-serve/index.html">Who We Serve</a>
</div></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li><a href="{p}request-a-proposal/index.html">Contact</a></li>
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
<li><a href="{p}about-cryptocurrency-consulting/index.html">About Cryptocurrency Consulting</a></li>
<li><a href="{p}about-cryptocurrency-consulting/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-cryptocurrency-consulting/who-we-serve/index.html">Verticals</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}request-a-consultation/index.html">Request a Consultation</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul><li>{escape(ADDRESS)} <em>[confirm]</em></li><li>Founded {escape(FOUNDED)}</li><li>Hours on contact page</li></ul></div>
</div>
<div class="copy">Cryptocurrency Consulting &middot; {escape(HQ)} &middot; {escape(PHONE)} <em>[confirm NAP]</em><br>
Copyright &copy; 2026. Cryptocurrency Consulting. All rights reserved. Crypto assets involve risk of loss.</div></div></footer>
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
<label>I am a…</label><select><option>Please choose&hellip;</option><option>Business / Enterprise</option><option>Trading Desk / Fund</option><option>Builder / Startup</option><option>Individual</option></select>
<label>Interest</label><select><option>Please choose&hellip;</option>{opts}<option>Consultation</option><option>Security Audit</option><option>Smart Contracts</option><option>Other</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f95a8">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Cryptocurrency Consulting",
        "email": EMAIL,
        "telephone": PHONE_TEL,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "foundingDate": FOUNDED,
        "description": "Cryptocurrency and blockchain consulting — trading bots, signals, nodes, strategies, smart contracts, and security audits.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "123 Blockchain Avenue",
            "addressLocality": "San Francisco",
            "addressRegion": "CA",
            "postalCode": "94105",
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
            "Cryptocurrency Consulting | Expert Blockchain Solutions",
            "Cryptocurrency Consulting helps businesses and individuals navigate blockchain and digital assets — bots, signals, nodes, strategies, smart contracts, and security audits.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>Expert Cryptocurrency Consulting Services</h1>
<p>{escape(TAGLINE)}</p>
<a class="btn" href="request-a-consultation/index.html">Get Started</a> <a class="btn alt" href="trading-bot-development/index.html">Explore Services</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>2018</b><span>Founded</span></div>
<div class="stat"><b>6</b><span>Core Service Lines</span></div>
<div class="stat"><b>SF</b><span>Based *[confirm]*</span></div>
<div class="stat"><b>24/7</b><span>Markets Don't Sleep</span></div>
</div></div></section>
<section><div class="wrap"><h2>What can Cryptocurrency Consulting build for you?</h2>
<p class="lead">Ten service families — trading bots, signals/webhooks, nodes, strategy, smart contracts, audits, digital assets, implementation, secops, and engagements.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure where to start? Begin with a consultation.</h2>
<p style="margin-bottom:14px">Request a consultation — tell us whether you need bots, contracts, nodes, audits, or strategy.</p>
<a class="btn" href="request-a-consultation/index.html">Request a Consultation</a></div></div>
<section><div class="wrap"><h2>How engagements get started</h2><div class="cols3">
<div class="card"><h3>1. Request a consultation</h3><p>Share goals — automation, security, implementation, or advisory.</p></div>
<div class="card"><h3>2. Scoped recommendation</h3><p>We map the right service line and a clear first milestone.</p></div>
<div class="card"><h3>3. Build &amp; harden</h3><p>Deliver bots, contracts, nodes, or audits with operational handoff.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why Cryptocurrency Consulting</h2><div class="cols3">
<div class="card"><h3>Since 2018</h3><p>Live site: founded in 2018 at the forefront of blockchain innovation.</p></div>
<div class="card"><h3>Full-stack crypto services</h3><p>Bots, signals, nodes, strategy, smart contracts, and security audits.</p></div>
<div class="card"><h3>Businesses &amp; individuals</h3><p>From first wallet to enterprise implementation support.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready to get started?</h2>
<a class="btn" href="request-a-consultation/index.html">Consultation</a> <a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    "What is Cryptocurrency Consulting?",
                    "Cryptocurrency Consulting provides blockchain and digital asset consulting — including trading bots, signals/webhooks, node deployment, trade strategy, smart contracts, and security audits.",
                ),
                (
                    "When was Cryptocurrency Consulting founded?",
                    f"The live site states Cryptocurrency Consulting was founded in {FOUNDED}.",
                ),
                (
                    "How do I get started?",
                    "Use Request a Consultation or Request a Proposal — share whether you need automation, security, implementation, or advisory support.",
                ),
                (
                    "Who is it for?",
                    "Businesses and individuals navigating cryptocurrency, blockchain implementation, or digital asset operations.",
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
            f"{h['name']} | Cryptocurrency Consulting",
            f"{h['name']} from Cryptocurrency Consulting — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} — From Cryptocurrency Consulting</h2>
<p class="lead">{escape(h["blurb"])} Delivered as part of the Cryptocurrency Consulting stack rather than an isolated task.</p>
<p><a class="btn" href="../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Solutions We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What Your Engagement Can Include</h2>
<ul class="checks">
<li>Discovery tied to your real operational goals</li>
<li>Security design before mainnet or live keys</li>
<li>Implementation with monitoring and handoff</li>
<li>Documentation your team can run</li>
<li>One accountable consulting partner across the stack</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with a consultation. We map goals and recommend the right service line before build work starts.",
                ),
                (
                    "Where is Cryptocurrency Consulting based?",
                    f"Remote-friendly consulting with published business hours on the live site.",
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
        head(f"{name} | Cryptocurrency Consulting", f"{name} from Cryptocurrency Consulting — {blurb}")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Engage Cryptocurrency Consulting for {escape(name.lower())} and related blockchain services.</h2>
<p class="lead">{escape(blurb)} At Cryptocurrency Consulting, {escape(name.lower())} is delivered inside a coaching-led curriculum — process, risk, and accountability for busy professionals.</p>
<p><a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>How {escape(name)} from Cryptocurrency Consulting Can Help You:</h2>
<ul class="checks">
<li>Clearer automation or implementation ownership</li>
<li>Security and risk controls designed in early</li>
<li>Documented runbooks your team can operate</li>
<li>Integrations with the tools you already use</li>
<li>Monitoring and handoff so work does not die at delivery</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} engagement scoped to your stack — not a one-size package</h2>
<p>No two organizations need {escape(name.lower())} the same way. We scope around your venues, chains, risk limits, and internal owners — after a consultation.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Teams avoid key risks by using a developed partner for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with DIY crypto builds</h3><ul>
<li>Bots without kill switches</li>
<li>Contracts shipped without tests or audits</li>
<li>Nodes without monitoring or recovery plans</li>
<li>Keys and API secrets treated casually</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on Cryptocurrency Consulting</h3><ul>
<li>Scoped delivery with security in the critical path</li>
<li>Documented handoff and ops ownership</li>
<li>Monitoring after go-live</li>
<li>A named consulting path instead of forum DIY</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>See where you stand first — free</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} would look like for your stack? Start with a consultation.</p>
<a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} shows results?",
                    "Timelines depend on vertical and ad capacity. Timelines depend on scope — bots, contracts, nodes, and audits have different critical paths.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Pricing is scoped after consultation — the live site does not publish a public rate card.",
                ),
                (
                    f"Why choose Cryptocurrency Consulting for {name.lower()}?",
                    f"We deliver {name.lower()} as part of Cryptocurrency Consulting's blockchain services stack founded in 2018.",
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
<h2 style="font-size:20px">Initiate a request with Cryptocurrency Consulting</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us the project</h3><p>Bots, signals, nodes, contracts, audits, or advisory.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>A scoped recommendation — or an honest no.</p></div>
<div class="card"><h3>3. Decide with the full picture</h3><p>Crypto assets and on-chain systems involve risk of loss; consulting is not a profit guarantee.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>Cryptocurrency Consulting</strong><br>Address: {escape(ADDRESS)} <em>[confirm — live site text looks placeholder]</em><br>Phone: {escape(PHONE)} <em>[confirm]</em><br>Email: {escape(EMAIL)}<br>Hours: Mon–Fri 9:00 AM–6:00 PM; Sat 10:00 AM–2:00 PM; Sun closed</p>
<p style="font-size:13px;color:#5a6b7b">Cryptocurrency and blockchain systems involve risk of loss. Consulting and software delivery are not investment advice or a profit guarantee.</p>
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
        ["/", "HOME", "", "cryptocurrency consulting", "logo/home", "A1,A6,A10", ""],
        [
            "/about-cryptocurrency-consulting/",
            "COMP-HUB",
            "/",
            "about cryptocurrency consulting",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-cryptocurrency-consulting/why-choose-us/",
            "COMP-CHILD",
            "/about-cryptocurrency-consulting/",
            "why choose cryptocurrency consulting",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-cryptocurrency-consulting/who-we-serve/",
            "COMP-CHILD",
            "/about-cryptocurrency-consulting/",
            "who cryptocurrency consulting serves",
            "About menu",
            "D1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact cryptocurrency consulting",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "cryptocurrency consulting proposal",
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
    with (ROOT / "CRYPTOCONSULTING-PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
        "CRYPTOCONSULTING-QUESTIONNAIRE-ANSWERS.md",
        "CRYPTOCONSULTING-PAGE-INVENTORY.csv",
        "CRYPTOCONSULTING-NOTES.md",
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
        ROOT / "about-cryptocurrency-consulting" / "index.html",
        head(
            "About Cryptocurrency Consulting",
            "Cryptocurrency Consulting — expert blockchain solutions. Founded in 2018.",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About Cryptocurrency Consulting</h2>
<p class="lead">Founded in {escape(FOUNDED)}, Cryptocurrency Consulting helps businesses and individuals navigate blockchain technology and digital assets with professional guidance.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>Live site mission: help businesses and individuals navigate this complex landscape with confidence — whether beginning a cryptocurrency journey or expanding an existing portfolio or blockchain implementation.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="who-we-serve/index.html">Verticals &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "When was Cryptocurrency Consulting founded?",
                    f"The live site states Cryptocurrency Consulting was founded in {FOUNDED}.",
                ),
                (
                    "What services do you offer?",
                    "Core live-site services include trading bots, signals/webhooks, node deployment, trade strategy/indicators, smart contracts, and security audits.",
                ),
            ]
        )
        + org_schema()
        + footer(1),
    )
    urls.append("/about-cryptocurrency-consulting/")

    write(
        ROOT / "about-cryptocurrency-consulting" / "why-choose-us" / "index.html",
        head("Why Choose Cryptocurrency Consulting", "Why teams choose Cryptocurrency Consulting.")
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose Cryptocurrency Consulting</h2>
<p class="lead">Professional guidance across automation, implementation, and security for digital assets.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Founded 2018</h3><p>Live site positions the firm at the forefront of blockchain innovation since 2018.</p></div>
<div class="card"><h3>Six core service lines</h3><p>Bots, signals, nodes, strategy, smart contracts, and security audits.</p></div>
<div class="card"><h3>Fintech + security lens</h3><p>About copy cites combined experience in fintech, cybersecurity, and investment management.</p></div>
<div class="card"><h3>Businesses and individuals</h3><p>From first investments to enterprise implementation themes on the live site.</p></div>
<div class="card"><h3>Consultation-led</h3><p>Start with a conversation before build or audit work.</p></div>
<div class="card"><h3>Risk realism</h3><p>Crypto assets involve loss; delivery is not a profit guarantee.</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-cryptocurrency-consulting/why-choose-us/")

    ind = "".join(
        f'<div class="gcard"><h3>{escape(i)}</h3><p>Service emphasis tuned for {escape(i.lower())}.</p></div>'
        for i in INDUSTRIES
    )
    write(
        ROOT / "about-cryptocurrency-consulting" / "who-we-serve" / "index.html",
        head("Who We Serve | Cryptocurrency Consulting", "Who Cryptocurrency Consulting serves.")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Verticals</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Who We Serve</h2>
<p class="lead">Engagements tailored to how different organizations buy and operate crypto infrastructure.</p>
<div class="grid">{ind}</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-cryptocurrency-consulting/who-we-serve/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | Cryptocurrency Consulting",
            "Contact Cryptocurrency Consulting",
            "Questions about coaching, the Paycheck Collector, or whether the academy fits your career schedule.",
        ),
        (
            "request-a-consultation",
            "Request a Consultation | Cryptocurrency Consulting",
            "Request a Consultation",
            "No pressure pitch — a transparent conversation to see if Cryptocurrency Consulting is the right fit. Application required for professionals ready to trade with $15,000+.",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | Cryptocurrency Consulting",
            "Request a Proposalrmation",
            "Share your background and goals. We will point you to the right next step — usually a strategy call.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | Cryptocurrency Consulting", "Page not found.")
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
        ROOT / "CRYPTOCONSULTING-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — Cryptocurrency Consulting (FACTORY BUILD · Gate 1 10×10)

**NearMe OS Website Factory staging engine · category: cryptocurrency / blockchain consulting · facts from live cryptocurrencyconsulting.io (2026-07-22) · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | Cryptocurrency Consulting | live site |
| A2 domain | cryptocurrencyconsulting.io | live site |
| A3 phone | {PHONE} | live site — **looks like placeholder (555)** [confirm] |
| A4 email | {EMAIL} | live site |
| A5 address | {ADDRESS} | live site — **street looks placeholder** [confirm] |
| A6 trade | Cryptocurrency / blockchain consulting & development | live site |
| A7 founded | {FOUNDED} | live site |
| A10 value_proposition | Expert cryptocurrency consulting — navigate blockchain and digital assets with professional guidance | live site |
| A11 tagline | {TAGLINE} | live site title |
| A12 hours | Mon–Fri 9–6; Sat 10–2; Sun closed | live site |
| A13 services_core | Trading bots; signals/webhooks; node deployment; trade strategy/indicators; smart contracts; security audits | live site |

## B — Services: 10 × 10
{hub_slugs}
FORM-CONSULT=`request-a-consultation` · FORM-PRICING=`request-a-proposal`

## Notes
- NAP from live site marked [confirm] due to placeholder pattern
- Testimonials on live site not copied as invented FACTs beyond existence note
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
