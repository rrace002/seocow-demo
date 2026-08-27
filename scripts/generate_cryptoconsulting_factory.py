#!/usr/bin/env python3
"""Generate Cryptocurrency Consulting site using the NearMe OS Website Factory template.

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: cryptocurrency / blockchain consulting & development.
Facts grounded from live cryptocurrencyconsulting.io (fetched 2026-07-22).
"""

from __future__ import annotations

import csv
import json
import shutil
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import factory_complete as fc  # noqa: E402

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
HOURS = "Mon–Fri 9am–6pm · Sat 10am–2pm *[confirm]*"

# Gate 1 — 10 × 10 (user revision request ~100 pages; grounded in product landing)
HUBS = [
    {
        "slug": "trading-bot-development",
        "name": "Trading Bot Development",
        "short": "Trading Bots",
        "icon": "bot",
        "intro": "Bots fail quietly when nobody owns kill switches, keys, or fill alerts. We design automation around your venues, size limits, and who gets paged when something breaks.",
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
        "icon": "signal",
        "intro": "A signal is only useful if it arrives, authenticates, and can be ignored when it should be ignored. We treat webhooks as production plumbing — not a Discord screenshot.",
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
        "icon": "node",
        "intro": "Nodes are infrastructure. We plan deployment, monitoring, upgrades, and recovery so participation is not a laptop under a desk.",
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
        "icon": "chart",
        "intro": "Indicators and playbooks only help if they match your risk profile and can be handed to automation without tribal knowledge.",
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
        "icon": "contract",
        "intro": "Contracts are production software. We prototype, test, document, and plan upgrades before mainnet — not after a surprise pause.",
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
        "icon": "shield",
        "intro": "Audits are only useful if findings get owners and deadlines. We review contracts, wallets, keys, and the path to remediate — not a PDF that sits in Drive.",
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
        "icon": "wallet",
        "intro": "Policy, education, and treasury basics so digital assets are treated like an operational program instead of a weekend experiment.",
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
        "icon": "chain",
        "intro": "Implementation starts with a use-case that survives contact with existing systems, data, and governance — then a pilot with an owner.",
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
        "icon": "lock",
        "intro": "Hot wallets, vendor access, and phishing are operations problems. We write the runbooks and limits your team can actually follow.",
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
        "icon": "briefcase",
        "intro": "Discovery, retainers, and fixed-scope delivery so blockchain work has a commercial shape — not an endless Slack thread.",
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

SITE = fc.SiteConfig(
    name="Cryptocurrency Consulting",
    logo_html='Crypto <span>Consulting</span>',
    tagline=TAGLINE,
    domain="cryptocurrencyconsulting.io",
    base=BASE,
    phone=PHONE,
    phone_tel=PHONE_TEL,
    email=EMAIL,
    hq=HQ,
    address=ADDRESS + " [confirm]",
    hours=HOURS,
    founded=FOUNDED,
    staging_banner=STAGING_BANNER,
    about_href="about-cryptocurrency-consulting/",
    consult_href="request-a-consultation/",
    proposal_href="request-a-proposal/",
    contact_href="contact/",
    disclaimer="Crypto assets involve risk of loss. Consulting is not investment advice or a profit guarantee.",
    partners=[
        "Exchange APIs",
        "EVM / Solidity",
        "Node operators",
        "Wallet & key hygiene",
        "Webhook automation",
        "Audit-ready delivery",
    ],
)

STATS = [
    (FOUNDED, "Founded (live site)"),
    ("10", "Service hubs in this map"),
    ("100", "Specialist service pages"),
    ("SF", "Published HQ *[confirm]*"),
    ("24/7", "Markets don't sleep"),
    ("6", "Core live-site lines"),
]

BENEFITS = [
    ("briefcase", "Since 2018", "Live site: founded in 2018 at the forefront of blockchain innovation."),
    ("chain", "Full-stack crypto services", "Bots, signals, nodes, strategy, smart contracts, and security audits on one consulting path."),
    ("people", "Businesses and individuals", "From first wallet questions to enterprise implementation support."),
    ("lock", "Security in the critical path", "Keys, tests, monitoring, and handoff are scoped before go-live — not as an afterthought."),
    ("phone", "Consultation-led", "A conversation first. We recommend a first milestone or an honest no."),
    ("shield", "Risk realism", "Crypto assets involve loss. Delivery is not a profit guarantee."),
]

STEPS = [
    ("Choose a service", "Pick the hub that matches — bots, signals, nodes, contracts, audits, or advisory."),
    ("Let’s communicate", "Share how you trade, build, or custody assets today and where it hurts."),
    ("Start with a scoped first step", "A written milestone, owners, and controls — then build and harden."),
]

INSIGHTS = [
    {
        "slug": "kill-switches-before-live-keys",
        "kicker": "Automation",
        "title": "Put kill switches on the calendar before live keys",
        "excerpt": "Bots without a documented stop condition are an operations incident waiting for volatility.",
        "body": "Most automation failures are not clever strategy bugs. They are missing owners: who can halt a bot, where the keys live, and what alert fires when an exchange API errors for ten minutes. Cryptocurrency Consulting treats kill switches, position caps, and paper modes as part of the build — not a later enhancement. If your team cannot describe the halt path in one paragraph, you are not ready for live capital.",
    },
    {
        "slug": "webhooks-are-production-plumbing",
        "kicker": "Signals",
        "title": "Treat TradingView webhooks like production plumbing",
        "excerpt": "Unauthenticated callbacks and silent retries turn a signal into a surprise order.",
        "body": "Webhook strategy execution fails in boring ways: replayed payloads, shared secrets in a chart alert, no audit log, and no rule for when not to trade. Harden the callback, score the signal, and keep a fail-safe that does nothing when data is stale. That is the difference between a demo bridge and something you can defend to a risk committee.",
    },
    {
        "slug": "nodes-need-recovery-not-just-uptime",
        "kicker": "Infrastructure",
        "title": "Nodes need recovery plans, not just uptime dashboards",
        "excerpt": "A synced node is not a backup. Know how you rebuild state after disk or key events.",
        "body": "Full nodes, validators, and RPC endpoints are only as good as the runbook next to them. Snapshot policy, key ceremony, upgrade windows, and who is on call matter more than the cloud logo. We scope node work as operations: monitoring, hardening, and recovery — because “it was synced yesterday” is not a restore test.",
    },
    {
        "slug": "contracts-without-tests-are-press-releases",
        "kicker": "Smart contracts",
        "title": "Contracts without tests are press releases",
        "excerpt": "Mainnet is not the place to discover you had no deployment pipeline.",
        "body": "Token, NFT, and DeFi prototypes need the unglamorous path: tests, gas review, upgrade plan, and monitoring after deploy. Cryptocurrency Consulting writes that path into the engagement so “we shipped” includes who watches events and how you pause. Audits help; they do not replace an owner for remediation.",
    },
    {
        "slug": "hot-wallet-limits-are-a-policy",
        "kicker": "SecOps",
        "title": "Hot-wallet limits are a policy, not a spreadsheet cell",
        "excerpt": "If anyone can raise a limit in Discord, you do not have a limit.",
        "body": "Treasury and trading desks leak through convenience: shared hot wallets, vendor laptops, and phishing that looks like a legit support ticket. Set limits, multi-sig paths, and access lifecycle in writing. Then practice the boring drills. Security operations is the habit of treating crypto like it can disappear this afternoon.",
    },
    {
        "slug": "implementation-is-not-a-whitepaper",
        "kicker": "Implementation",
        "title": "Blockchain implementation is not a whitepaper",
        "excerpt": "If the use case does not survive your current data model, stop before the pilot theater.",
        "body": "Permissioned vs public, oracles, and governance are only interesting after the operational question is honest: what process improves, who enters data, and who is liable when it is wrong. We start with use-case assessment and existing-system integration so a pilot has a success definition other than a slide.",
    },
]


def write(path: Path, content: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


def head(title: str, desc: str) -> str:
    return fc.head(SITE, title, desc)


def chrome(depth: int) -> str:
    return fc.chrome(SITE, HUBS, depth)


def footer(depth: int) -> str:
    return fc.footer(SITE, HUBS, depth)


def faqs(items: list[tuple[str, str]]) -> str:
    return fc.faqs_html(items)


def form_shell() -> str:
    return fc.form_shell(
        HUBS,
        extra_options=("Security Audit", "Smart Contracts", "Consultation", "Other"),
    )


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
            f'<a href="{h["slug"]}/index.html">All {escape(h["short"]).lower()} services &rarr;</a></div>'
        )
    return (
        head(
            "Cryptocurrency Consulting | Expert Blockchain Solutions",
            "Cryptocurrency Consulting helps businesses and individuals navigate blockchain and digital assets — bots, signals, nodes, strategies, smart contracts, and security audits.",
        )
        + chrome(0)
        + f"""
<div class="hero-photo"><div class="wrap">
<div>
<p class="kicker">A reliable blockchain consulting partner</p>
<h1>Expert cryptocurrency consulting for teams that need more than a brochure.</h1>
<p>Navigate bots, signals, nodes, strategy, smart contracts, and security audits with a consultation-led practice founded in {escape(FOUNDED)}.</p>
<div class="hero-actions">
<a class="btn" href="request-a-consultation/index.html">Request a Consultation</a>
<a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a>
</div>
<form class="search-hero" action="search/index.html" method="get">
<input type="search" name="q" placeholder="Search services, hubs, insights…" aria-label="Search">
<button class="btn navy" type="submit">Find Now</button>
</form>
</div>
<div class="hero-card">
<h3>Let us help you resolve the operational gaps</h3>
<p>Tell us whether you need automation, custody discipline, implementation, or an audit path. A specialist follows up — this is a staging form until rollout.</p>
</div>
</div></div>
<section class="navy"><div class="wrap">
<p class="kicker">Cryptocurrency Consulting by the numbers</p>
<h2>Public facts and this factory map — not invented ticket counts.</h2>
{fc.stats_html(STATS)}
</div></section>
<section><div class="wrap">
<p class="kicker">Our services</p>
<h2>We engage across the crypto stack, not a single product SKU.</h2>
<p class="lead">Ten service families with specialist pages underneath — the same density pattern as a complete local-service site, mapped to this trade.</p>
{fc.icon_tiles(HUBS, 0)}
</div></section>
<section class="tint"><div class="wrap">
<p class="kicker">Your benefits</p>
<h2>Why teams choose Cryptocurrency Consulting</h2>
{fc.benefits_html(BENEFITS)}
</div></section>
<section><div class="wrap">
<p class="kicker">How it works</p>
<h2>Are you ready to take the next step?</h2>
{fc.how_it_works(STEPS)}
<div class="cols2" style="margin-top:28px">
<div>
<h2>Contact form</h2>
<p>Fill in the form and let the team know what you are building or protecting. A representative follows up after rollout wiring.</p>
</div>
{form_shell()}
</div>
</div></section>
<section class="tint"><div class="wrap">
<p class="kicker">Insights</p>
<h2>Factory-written advisory for owner review</h2>
{fc.insights_cards(INSIGHTS, 0, 3)}
<p style="margin-top:18px"><a class="btn navy" href="insights/index.html">All insights</a></p>
</div></section>
<section><div class="wrap">
<p class="kicker">Platforms we work with</p>
<h2>Technology partners and stack themes</h2>
<p>Badges from public service lines pending owner logo files. Not a claim of certification unless confirmed.</p>
{fc.partners_html(SITE.partners)}
</div></section>
<section class="tint"><div class="wrap">
<h2>Explore the 10-hub map</h2>
<div class="cols3">{''.join(cards)}</div>
</div></section>
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
    intro = h.get("intro", h["blurb"])
    return (
        head(
            f"{h['name']} | Cryptocurrency Consulting",
            f"{h['name']} from Cryptocurrency Consulting — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section class="inner-hero"><div class="wrap cols2">
<div>
<p class="kicker">{escape(h["short"])}</p>
<h1>{escape(h["name"])}</h1>
<p class="lead">{escape(h["blurb"])}</p>
<p>{escape(intro)} Delivered as part of the Cryptocurrency Consulting stack rather than an isolated task.</p>
<p><a class="btn" href="../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div>
<div class="photo-panel" role="img" aria-label="Illustrated service panel"></div>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} solutions we provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap cols2">
<div>
<h2>What your engagement can include</h2>
<ul class="checks">
<li>Discovery tied to your real operational goals for {escape(h["short"].lower())}</li>
<li>Security design before mainnet or live keys</li>
<li>Implementation with monitoring and handoff</li>
<li>Documentation your team can run</li>
<li>One accountable consulting partner across the stack</li>
</ul>
</div>
<div>
<h2>Request this service</h2>
{form_shell()}
</div>
</div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"] + " " + intro),
                (
                    f"How do we start {h['short'].lower()} work?",
                    f"Begin with a consultation. We map goals for {h['name'].lower()} and recommend a first milestone before build work starts.",
                ),
                (
                    "Where is Cryptocurrency Consulting based?",
                    "Remote-friendly consulting with published business hours on the live site. Street NAP from the live site looks placeholder and is marked for confirmation.",
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
    p1 = (
        f"{blurb} Cryptocurrency Consulting scopes {name.lower()} inside {h['name']} "
        "so the work has an owner, a security bar, and a handoff — not a one-off script."
    )
    p2 = (
        f"Teams usually ask for {name.lower()} after a near-miss: keys in chat, automation without a halt path, "
        f"or {h['short'].lower()} work that nobody monitors. We start with how you actually operate — venues, chains, who signs, who gets paged."
    )
    p3 = (
        f"Delivery for {name.lower()} is consultation-led. You get a written first milestone, the controls that belong "
        f"in the critical path for {h['name'].lower()}, and documentation your staff can run after we step back."
    )
    return (
        head(f"{name} | Cryptocurrency Consulting", f"{name} from Cryptocurrency Consulting — {blurb}")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section class="inner-hero"><div class="wrap">
<p class="kicker">{escape(h["name"])}</p>
<h1>{escape(name)}</h1>
<p class="lead">{escape(blurb)}</p>
<p>{escape(p1)}</p>
<p>{escape(p2)}</p>
<p>{escape(p3)}</p>
<p><a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap cols2">
<div>
<h2>What this {escape(name.lower())} engagement includes</h2>
<ul class="checks">
<li>Scope written around {escape(name.lower())} — not a generic package</li>
<li>Security and risk controls designed in early</li>
<li>Documented runbooks your team can operate</li>
<li>Integrations with the tools you already use</li>
<li>Monitoring and handoff so work does not die at delivery</li>
</ul>
</div>
<div>
<h2>Problems this replaces</h2>
<ul class="checks">
<li>Forum DIY with no owner after launch</li>
<li>Silent failures in {escape(h["short"].lower())} workflows</li>
<li>Keys and API secrets treated casually</li>
<li>No path from prototype to operations</li>
</ul>
</div>
</div></section>
<section><div class="wrap"><h2>A specialist path vs. one-person crypto DIY</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes without a developed partner</h3><ul>
<li>Bots without kill switches</li>
<li>Contracts shipped without tests or audits</li>
<li>Nodes without monitoring or recovery plans</li>
<li>Keys and API secrets treated casually</li>
</ul></div>
<div class="col good"><h3>When {escape(name.lower())} is scoped with Cryptocurrency Consulting</h3><ul>
<li>Scoped delivery with security in the critical path</li>
<li>Documented handoff and ops ownership for {escape(name.lower())}</li>
<li>Monitoring after go-live</li>
<li>A named consulting path instead of forum DIY</li>
</ul></div>
</div></div></section>
<section class="tint"><div class="wrap cols2">
<div>
<h2>Talk to us about {escape(name.lower())}</h2>
<p>Share stack, constraints, and timing. Pricing is scoped after consultation — the live site does not publish a public rate card.</p>
</div>
{form_shell()}
</div></section>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} is in production?",
                    f"Timelines depend on scope. {name} sits under {h['name']} — bots, contracts, nodes, and audits have different critical paths. We estimate after consultation.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    f"Pricing for {name.lower()} is scoped after consultation — the live site does not publish a public rate card.",
                ),
                (
                    f"Why choose Cryptocurrency Consulting for {name.lower()}?",
                    f"We deliver {name.lower()} as part of Cryptocurrency Consulting's blockchain services stack founded in {FOUNDED} — with handoff, not a throwaway prototype.",
                ),
            ]
        )
        + f'<section><div class="wrap"><h2>Related {escape(h["short"])} solutions</h2><div class="grid">{related}</div></div></section>'
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
        [
            "/insights/",
            "RESOURCE-HUB",
            "/",
            "cryptocurrency consulting insights",
            "Insights menu",
            "completeness",
            "",
        ],
        [
            "/search/",
            "UTILITY-SEARCH",
            "/",
            "search cryptocurrency consulting",
            "nav search",
            "completeness",
            "",
        ],
    ]
    for a in INSIGHTS:
        rows.append(
            [
                f"/insights/{a['slug']}/",
                "RESOURCE-CHILD",
                "/insights/",
                a["title"].lower(),
                "Insights",
                "completeness",
                "",
            ]
        )
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


def search_catalog() -> list[dict]:
    items = [{"title": "Home", "url": "/", "type": "HOME"}]
    for h in HUBS:
        items.append({"title": h["name"], "url": f"/{h['slug']}/", "type": "SVC-HUB"})
        for s, n, _ in h["children"]:
            items.append({"title": n, "url": f"/{h['slug']}/{s}/", "type": "SVC-CHILD"})
    for a in INSIGHTS:
        items.append({"title": a["title"], "url": f"/insights/{a['slug']}/", "type": "RESOURCE"})
    items.append({"title": "About Cryptocurrency Consulting", "url": "/about-cryptocurrency-consulting/", "type": "COMP"})
    items.append({"title": "Contact", "url": "/contact/", "type": "COMP-CONTACT"})
    return items


def search_page() -> str:
    payload = json.dumps(search_catalog(), ensure_ascii=True)
    return (
        head("Search | Cryptocurrency Consulting", "Search Cryptocurrency Consulting services and insights.")
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; Search</div>
<section class="inner-hero"><div class="wrap">
<p class="kicker">Looking for something?</p>
<h1>Search Find Now</h1>
<p class="lead">Filter this factory map the way a complete service site offers on-page find.</p>
<form class="search-hero" id="sf" action="index.html" method="get">
<input id="q" type="search" name="q" placeholder="Search services and insights…" aria-label="Search">
<button class="btn" type="submit">Find Now</button>
</form>
<ul id="results" class="checks" style="margin-top:22px"></ul>
</div></section>
<script>
const CATALOG = {payload};
function rel(url) {{
  if (url === "/") return "../index.html";
  return ".." + url + "index.html";
}}
function run() {{
  const q = (new URLSearchParams(location.search).get("q") || "").trim().toLowerCase();
  document.getElementById("q").value = new URLSearchParams(location.search).get("q") || "";
  const hits = !q ? CATALOG.slice(0, 20) : CATALOG.filter(x => x.title.toLowerCase().includes(q) || x.type.toLowerCase().includes(q));
  document.getElementById("results").innerHTML = hits.length
    ? hits.map(x => "<li><a href=\\"" + rel(x.url) + "\\">" + x.title + "</a> — " + x.type + "</li>").join("")
    : "<li>No matching pages. Try bots, audit, node, or insights.</li>";
}}
run();
</script>
"""
        + footer(1)
    )


def insight_index() -> str:
    return (
        head("Insights | Cryptocurrency Consulting", "Factory-written crypto operations insights pending owner review.")
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; Insights</div>
<section class="inner-hero"><div class="wrap">
<p class="kicker">Tech advisory</p>
<h1>Insights for crypto operators</h1>
<p class="lead">Original factory articles for this staging site — not scraped posts, and not invented client case studies. Owner review before launch.</p>
{fc.insights_cards(INSIGHTS, 1)}
</div></section>
"""
        + footer(1)
    )


def insight_article(a: dict) -> str:
    return (
        head(f"{a['title']} | Cryptocurrency Consulting", a["excerpt"])
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">Insights</a> &rsaquo; {escape(a["title"])}</div>
<section class="inner-hero"><div class="wrap">
<p class="kicker">{escape(a["kicker"])}</p>
<h1>{escape(a["title"])}</h1>
<p class="lead">{escape(a["excerpt"])}</p>
<div class="photo-panel" style="margin:18px 0 22px"></div>
<p>{escape(a["body"])}</p>
<p><a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a></p>
</div></section>
"""
        + footer(2)
    )


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
        "CRYPTOCONSULTING-QUESTIONNAIRE-ANSWERS.md",
        "CRYPTOCONSULTING-PAGE-INVENTORY.csv",
        "CRYPTOCONSULTING-NOTES.md",
        "FACTORY-INSTRUCTION-SET.md",
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
            "Questions about trading bots, smart contracts, node deployment, security audits, or digital asset consulting.",
        ),
        (
            "request-a-consultation",
            "Request a Consultation | Cryptocurrency Consulting",
            "Request a Consultation",
            "Tell us what you are building or protecting — we will recommend a practical first step.",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | Cryptocurrency Consulting",
            "Request a Proposal",
            "Share scope and constraints. We will return a scoped proposal you can compare.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(ROOT / "insights" / "index.html", insight_index())
    urls.append("/insights/")
    for a in INSIGHTS:
        write(ROOT / "insights" / a["slug"] / "index.html", insight_article(a))
        urls.append(f"/insights/{a['slug']}/")
    write(ROOT / "search" / "index.html", search_page())
    urls.append("/search/")

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
- Completeness chrome: `/insights/` + `/search/` (see FACTORY-INSTRUCTION-SET.md)
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
