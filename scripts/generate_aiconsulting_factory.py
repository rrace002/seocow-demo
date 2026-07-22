#!/usr/bin/env python3
"""Generate AI Consulting Near Me site using the NearMe OS Website Factory template.

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: AI consulting / business automation / AI strategy.
Facts grounded from live aiconsultingnearme.com (fetched 2026-07-22).
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://aiconsultingnearme.com"
PHONE = "(555) 123-4567"  # placeholder on live site [confirm]
PHONE_TEL = "+15551234567"
EMAIL = "hello@aiconsultingnearme.com"
HQ = "Nationwide"
ADDRESS = "Serving businesses nationwide"
OPERATOR = "AI Consulting Near Me"
TAGLINE = "Unlock AI's Potential for Your Business"
FOUNDED = "2018"  # claimed on live About [confirm]
STAGING_BANNER = (
    "STAGING PREVIEW — aiconsultingnearme.com factory build · content pending owner review "
    "· not the live AI Consulting Near Me website"
)

# NearMe factory CSS (SEO Cow template) with AI Consulting Near Me cyan/slate remap
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#0f172a;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#0e7490;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#0c4a6e;color:#bae6fd;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#155e75;color:#e0f2fe;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #0891b2;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#0f172a}.logo span{color:#0891b2}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#0f172a}
.phone-cta small{display:block;color:#5a6b7b;font-size:11px}
nav.nav{background:#155e75}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav a:hover{background:#0e4a5c;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #0891b2;z-index:60}
.dd a{color:#0f172a;padding:10px 15px;font-weight:500;border-bottom:1px solid #e0f2fe}
.dd a:hover{background:#ecfeff}
.nav .em a{background:#0891b2}.nav .em a:hover{background:#0e7490}
.hero{background:linear-gradient(rgba(8,47,73,.82),rgba(8,47,73,.82)),repeating-linear-gradient(45deg,#155e75 0 14px,#0e7490 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#bae6fd;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#0891b2;color:#fff;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#06b6d4;text-decoration:none}
.btn.alt{background:#155e75;color:#fff}.btn.alt:hover{background:#0e4a5c}
section{padding:44px 0}
section.tint{background:#f0f9ff}
section h2{font-size:25px;color:#0f172a;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#0891b2;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #dbeafe;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(8,47,73,.06)}
.card h3{color:#0f172a;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #dbeafe;border-left:4px solid #0891b2;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#0f172a}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#0e7490}
.ctastrip{background:#155e75;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #dbeafe;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#f0f9ff}.vs .col.good{background:#f0f9ff}
.vs h3{font-size:16px;margin-bottom:12px;color:#0f172a}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#0e7490;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #dbeafe;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#0f172a;list-style:none}
details summary:before{content:"+ ";color:#0891b2;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #dbeafe;border-top:4px solid #0891b2;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#44525f;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5a6b7b;padding:14px 0 0}
.crumb a{color:#5a6b7b}
footer{background:#0c4a6e;color:#c9b8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#c9b8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #0f172a;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#8a7a74}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #dbeafe;border-top:4px solid #0891b2;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#0f172a}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #dbeafe;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(13,148,136,.08)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#0f172a}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#0891b2;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#0891b2;color:#fff;text-align:center;padding:32px 0}
.audit h2{color:#fff;margin-bottom:8px}.audit a.btn{background:#fff;color:#155e75}
"""

# Gate 1 — 10 × 10 (user revision request ~100 pages; grounded in live product themes)
HUBS = [{'slug': 'ai-strategy-consulting',
  'name': 'AI Strategy Consulting',
  'short': 'AI Strategy',
  'blurb': 'Tailored AI strategies — readiness, opportunity sizing, and roadmaps matched to your '
           'goals (from live site AI Strategy themes).',
  'children': [('ai-readiness-assessment',
                'AI Readiness Assessment',
                'Evaluate people, data, processes, and tooling before you buy or build AI.'),
               ('ai-opportunity-analysis',
                'AI Opportunity Analysis',
                'Rank use cases by value, feasibility, and risk — not hype.'),
               ('custom-ai-roadmap',
                'Custom AI Roadmap',
                'Prioritized initiatives, sequencing, and expected outcomes for your business.'),
               ('roi-projection-modeling',
                'ROI Projection Modeling',
                'Frame investment cases with assumptions you can revisit after pilots.'),
               ('technology-stack-selection',
                'Technology Stack Selection',
                'Choose platforms and vendors that fit constraints — not the loudest demo.'),
               ('executive-ai-briefings',
                'Executive AI Briefings',
                'Plain-English briefings so leadership can decide with shared context.'),
               ('competitive-ai-benchmarking',
                'Competitive AI Benchmarking',
                'See how peers apply AI without copying the wrong playbook.'),
               ('change-management-planning',
                'Change Management Planning',
                'Adoption plans so AI work survives contact with real teams.'),
               ('pilot-use-case-selection',
                'Pilot Use-Case Selection',
                'Pick a first pilot with clear success criteria and exit ramps.'),
               ('ai-budget-and-resourcing',
                'AI Budget and Resourcing',
                'Right-size budget, owners, and capacity for the roadmap ahead.')]},
 {'slug': 'process-automation-consulting',
  'name': 'Process Automation Consulting',
  'short': 'Automation',
  'blurb': 'Streamline operations with intelligent automation — workflow analysis through '
           'monitoring (live site Process Automation themes).',
  'children': [('workflow-analysis',
                'Workflow Analysis',
                "Map today's process so automation targets friction, not theater."),
               ('intelligent-document-processing',
                'Intelligent Document Processing',
                'Extract, classify, and route documents with human review where needed.'),
               ('rpa-plus-ai-automation',
                'RPA Plus AI Automation',
                'Combine RPA with AI judgment for messier, higher-value steps.'),
               ('operations-automation-design',
                'Operations Automation Design',
                'Design automations that fit how ops actually runs day to day.'),
               ('integration-with-existing-systems',
                'Integration with Existing Systems',
                'Connect AI and bots to the systems you already rely on.'),
               ('error-reduction-automation',
                'Error Reduction Automation',
                'Cut rework with checks, validations, and exception paths.'),
               ('employee-self-serve-bots',
                'Employee Self-Serve Bots',
                'Internal assistants that answer common questions and kick off tasks.'),
               ('automation-performance-monitoring',
                'Automation Performance Monitoring',
                'Track throughput, failures, and savings after go-live.'),
               ('exception-handling-playbooks',
                'Exception Handling Playbooks',
                'Define what happens when automation cannot finish the job.'),
               ('automation-roi-reporting',
                'Automation ROI Reporting',
                'Report hours saved and quality gains in language finance trusts.')]},
 {'slug': 'data-analytics-insights',
  'name': 'Data Analytics & Insights',
  'short': 'Analytics',
  'blurb': 'Turn data into actionable insight — assessment, platforms, dashboards, and governance '
           '(live site Data Analytics themes).',
  'children': [('data-assessment-and-audit',
                'Data Assessment and Audit',
                'Inventory sources, quality gaps, and what is decision-ready today.'),
               ('analytics-platform-setup',
                'Analytics Platform Setup',
                'Stand up reporting foundations without boiling the ocean.'),
               ('executive-dashboard-creation',
                'Executive Dashboard Creation',
                'Dashboards that answer leadership questions in one glance.'),
               ('predictive-analytics-models',
                'Predictive Analytics Models',
                'Forecast demand, risk, or churn with clear model limits.'),
               ('customer-insight-modeling',
                'Customer Insight Modeling',
                'Segment and understand customers beyond vanity metrics.'),
               ('operational-kpi-frameworks',
                'Operational KPI Frameworks',
                'Define KPIs that drive action — not dashboard clutter.'),
               ('self-serve-reporting-enablement',
                'Self-Serve Reporting Enablement',
                'Train teams to answer routine questions without a ticket queue.'),
               ('data-pipeline-reliability',
                'Data Pipeline Reliability',
                'Keep feeds timely, monitored, and recoverable when they break.'),
               ('insight-to-action-workshops',
                'Insight to Action Workshops',
                'Turn charts into owners, decisions, and next experiments.'),
               ('analytics-governance',
                'Analytics Governance',
                'Access, definitions, and quality rules so numbers stay trustworthy.')]},
 {'slug': 'ai-customer-experience',
  'name': 'AI Customer Experience',
  'short': 'Customer AI',
  'blurb': 'AI that improves service, personalization, and retention — with brand and quality '
           'guardrails.',
  'children': [('ai-customer-service-bots',
                'AI Customer Service Bots',
                'Assistants that resolve common asks and escalate cleanly.'),
               ('omnichannel-support-ai',
                'Omnichannel Support AI',
                'Consistent AI help across chat, email, and other channels.'),
               ('personalized-recommendation-engines',
                'Personalized Recommendation Engines',
                'Relevant next offers without creepy or off-brand suggestions.'),
               ('lead-qualification-assistants',
                'Lead Qualification Assistants',
                'Qualify inbound interest so sales time goes to real opportunities.'),
               ('voice-of-customer-analytics',
                'Voice of Customer Analytics',
                'Mine feedback and tickets for themes you can act on.'),
               ('knowledge-base-ai-search',
                'Knowledge Base AI Search',
                'Help customers and agents find the right answer faster.'),
               ('retention-and-winback-ai',
                'Retention and Winback AI',
                'Spot churn risk and trigger thoughtful save plays.'),
               ('appointment-booking-automation',
                'Appointment Booking Automation',
                'Reduce scheduling friction with AI-assisted booking flows.'),
               ('brand-voice-guardrails',
                'Brand Voice Guardrails',
                'Keep automated replies on-brand, safe, and reviewable.'),
               ('cx-ai-qa-and-training',
                'CX AI QA and Training',
                'Quality loops so bots improve instead of quietly degrading.')]},
 {'slug': 'ai-ethics-compliance',
  'name': 'AI Ethics & Compliance',
  'short': 'Ethics',
  'blurb': 'Responsible AI policy, risk, privacy, and oversight so innovation does not outrun '
           'trust.',
  'children': [('responsible-ai-policy',
                'Responsible AI Policy',
                'Written principles and rules teams can actually follow.'),
               ('model-risk-assessment',
                'Model Risk Assessment',
                'Identify where models can fail, bias, or create liability.'),
               ('data-privacy-for-ai',
                'Data Privacy for AI',
                'Minimize, protect, and govern data used in AI workflows.'),
               ('vendor-ai-due-diligence',
                'Vendor AI Due Diligence',
                'Score third-party AI tools before they touch sensitive work.'),
               ('ai-usage-guidelines',
                'AI Usage Guidelines',
                "Clear do/don't guidance for employees using generative tools."),
               ('audit-ready-documentation',
                'Audit-Ready Documentation',
                'Evidence trails for decisions, models, and oversight.'),
               ('industry-compliance-mapping',
                'Industry Compliance Mapping',
                'Map AI practices to sector obligations you already face.'),
               ('human-oversight-design',
                'Human Oversight Design',
                'Put humans in the loop where stakes demand it.'),
               ('incident-response-for-ai',
                'Incident Response for AI',
                'Playbooks when an AI system behaves badly in production.'),
               ('ethics-review-board-setup',
                'Ethics Review Board Setup',
                'Lightweight review structures for higher-risk AI use cases.')]},
 {'slug': 'ai-implementation-support',
  'name': 'AI Implementation & Support',
  'short': 'Implementation',
  'blurb': 'From pilot to production — integration, training, monitoring, and post-launch review '
           '(live site Implementation themes).',
  'children': [('pilot-implementation',
                'Pilot Implementation',
                'Ship a scoped pilot with success metrics and learning goals.'),
               ('systems-integration-support',
                'Systems Integration Support',
                'Wire AI into CRM, ERP, ticketing, and other core systems.'),
               ('mlops-and-monitoring',
                'MLOps and Monitoring',
                'Operate models and prompts with health checks after launch.'),
               ('user-training-and-enablement',
                'User Training and Enablement',
                'Train the people who will live with the new workflows.'),
               ('prompt-and-workflow-tuning',
                'Prompt and Workflow Tuning',
                'Iterate prompts and steps based on real usage, not demos.'),
               ('knowledge-transfer-handoff',
                'Knowledge Transfer Handoff',
                'Leave your team able to own what was built.'),
               ('sla-and-support-retainer',
                'SLA and Support Retainer',
                'Ongoing support terms when you need a named backstop.'),
               ('performance-optimization',
                'Performance Optimization',
                'Improve latency, cost, and quality after the first release.'),
               ('version-upgrade-planning',
                'Version Upgrade Planning',
                'Plan model and platform upgrades without surprise breakage.'),
               ('post-launch-roi-review',
                'Post-Launch ROI Review',
                'Compare outcomes to the original investment case.')]},
 {'slug': 'healthcare-ai-consulting',
  'name': 'Healthcare AI Consulting',
  'short': 'Healthcare',
  'blurb': 'AI for care ops, admin, and communication — designed with privacy-aware patterns (live '
           'Healthcare industry theme).',
  'children': [('patient-scheduling-automation',
                'Patient Scheduling Automation',
                'Reduce no-shows and phone tag with smarter scheduling flows.'),
               ('clinical-admin-automation',
                'Clinical Admin Automation',
                'Cut admin drag around intake, routing, and follow-ups.'),
               ('healthcare-document-ai',
                'Healthcare Document AI',
                'Assist with clinical and admin documents under clear controls.'),
               ('care-ops-analytics',
                'Care Ops Analytics',
                'Visibility into throughput, wait times, and operational bottlenecks.'),
               ('patient-communication-assistants',
                'Patient Communication Assistants',
                'Helpful outreach that stays appropriate and reviewable.'),
               ('revenue-cycle-ai-support',
                'Revenue Cycle AI Support',
                'Support coding, denials, and billing workflows carefully.'),
               ('hipaa-aware-ai-design',
                'HIPAA-Aware AI Design',
                'Design AI workflows with privacy and access discipline in mind.'),
               ('provider-knowledge-assistants',
                'Provider Knowledge Assistants',
                'Faster access to approved policies and operational knowledge.'),
               ('telehealth-ops-automation',
                'Telehealth Ops Automation',
                'Smooth virtual-visit logistics and patient prep steps.'),
               ('healthcare-ai-pilot-design',
                'Healthcare AI Pilot Design',
                'Scoped healthcare pilots with clear clinical/admin boundaries.')]},
 {'slug': 'finance-ai-consulting',
  'name': 'Finance AI Consulting',
  'short': 'Finance',
  'blurb': 'Risk, automation, personalization, and governance for financial services AI (live '
           'Finance industry theme).',
  'children': [('risk-management-analytics',
                'Risk Management Analytics',
                'Analytics that surface risk signals earlier for review.'),
               ('finance-process-automation',
                'Finance Process Automation',
                'Automate repetitive finance ops without losing controls.'),
               ('personalized-banking-experiences',
                'Personalized Banking Experiences',
                'Relevant next-best actions with compliance-aware design.'),
               ('fraud-signal-triage',
                'Fraud Signal Triage',
                'Prioritize alerts so investigators focus on real risk.'),
               ('compliance-document-review',
                'Compliance Document Review',
                'AI-assisted review with human ownership of decisions.'),
               ('wealth-ops-assistants',
                'Wealth Ops Assistants',
                'Assist advisors and ops with research and routine tasks.'),
               ('financial-forecasting-models',
                'Financial Forecasting Models',
                'Forecasting support with transparent assumptions.'),
               ('kyc-and-onboarding-assist',
                'KYC and Onboarding Assist',
                'Speed onboarding steps while preserving required checks.'),
               ('finance-ai-governance',
                'Finance AI Governance',
                'Oversight patterns suited to regulated finance environments.'),
               ('finance-ai-pilot-scoping',
                'Finance AI Pilot Scoping',
                'Define a finance pilot that can clear risk and compliance review.')]},
 {'slug': 'retail-manufacturing-ai',
  'name': 'Retail & Manufacturing AI',
  'short': 'Retail/Mfg',
  'blurb': 'Inventory, personalization, forecasting, maintenance, and supply visibility for retail '
           'and manufacturing (live industry themes).',
  'children': [('inventory-optimization-ai',
                'Inventory Optimization AI',
                'Balance stock levels against demand signals and lead times.'),
               ('retail-personalization',
                'Retail Personalization',
                'Personalize merchandising and offers without brand risk.'),
               ('demand-forecasting',
                'Demand Forecasting',
                'Improve planning with forecasts tied to operational decisions.'),
               ('predictive-maintenance',
                'Predictive Maintenance',
                'Spot equipment risk earlier to reduce unplanned downtime.'),
               ('production-efficiency-analytics',
                'Production Efficiency Analytics',
                'Find throughput and quality bottlenecks on the floor.'),
               ('supply-chain-visibility',
                'Supply Chain Visibility',
                'See delays and exceptions before they hit customers.'),
               ('quality-inspection-assist',
                'Quality Inspection Assist',
                'Assist inspectors with consistent defect detection support.'),
               ('store-ops-automation',
                'Store Ops Automation',
                'Automate repetitive store tasks and associate workflows.'),
               ('pricing-and-promo-analytics',
                'Pricing and Promo Analytics',
                'Measure promo lift and pricing moves with clearer evidence.'),
               ('industrial-iot-insight-layers',
                'Industrial IoT Insight Layers',
                'Turn machine and sensor data into actionable ops insight.')]},
 {'slug': 'small-business-ai-solutions',
  'name': 'Small Business AI Solutions',
  'short': 'SMB AI',
  'blurb': 'Affordable, practical AI for small and mid-sized businesses — starters, chat, CRM, and '
           '90-day plans (live SMB theme).',
  'children': [('smb-ai-starter-assessment',
                'SMB AI Starter Assessment',
                'A lightweight readiness check sized for smaller teams.'),
               ('affordable-automation-packages',
                'Affordable Automation Packages',
                'Right-sized automation packages that do not require an enterprise IT team.'),
               ('local-business-chat-assistants',
                'Local Business Chat Assistants',
                'Website and inbox assistants for common customer questions.'),
               ('review-and-reputation-automation',
                'Review and Reputation Automation',
                'Capture reviews and respond consistently without busywork.'),
               ('crm-and-follow-up-automation',
                'CRM and Follow-Up Automation',
                'Keep leads warm with automated, human-friendly follow-ups.'),
               ('content-ops-with-ai',
                'Content Ops with AI',
                'Speed drafting and repurposing with editorial guardrails.'),
               ('local-seo-ai-assist',
                'Local SEO AI Assist',
                'AI-assisted local presence tasks — not magic ranking promises.'),
               ('owner-dashboard-lite',
                'Owner Dashboard Lite',
                'A simple view of the metrics an owner actually needs.'),
               ('tool-stack-on-a-budget',
                'Tool Stack on a Budget',
                'Pick a lean tool stack that fits cash flow and capacity.'),
               ('ninety-day-smb-ai-plan',
                'Ninety-Day SMB AI Plan',
                'A 90-day plan with three milestones and clear owners.')]}]

INDUSTRIES = ['Healthcare',
 'Finance & Banking',
 'Retail & E-commerce',
 'Real Estate',
 'Manufacturing',
 'Small Business',
 'Logistics & Transportation',
 'Education']


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
<div class="logo">AI Consulting <span>Near Me</span><small>Strategy · Automation · Growth</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Free consultation · Response within 24 hours *[confirm]*</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-ai-consulting-near-me/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-ai-consulting-near-me/index.html">About AI Consulting Near Me</a>
<a href="{p}about-ai-consulting-near-me/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-ai-consulting-near-me/who-we-serve/index.html">Who We Serve</a>
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
<li><a href="{p}about-ai-consulting-near-me/index.html">About AI Consulting Near Me</a></li>
<li><a href="{p}about-ai-consulting-near-me/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-ai-consulting-near-me/who-we-serve/index.html">Verticals</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}request-a-consultation/index.html">Request a Consultation</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul><li>{escape(ADDRESS)} <em>[confirm]</em></li><li>Founded {escape(FOUNDED)} *[confirm]*</li><li>Nationwide coverage</li></ul></div>
</div>
<div class="copy">AI Consulting Near Me &middot; {escape(HQ)} &middot; {escape(PHONE)} <em>[confirm NAP]</em><br>
Copyright &copy; 2026. AI Consulting Near Me. All rights reserved. AI outcomes vary; engagements are scoped after consultation.</div></div></footer>
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
<label>I am a…</label><select><option>Please choose&hellip;</option><option>Business / Enterprise</option><option>Operations / Ops Leader</option><option>Small Business Owner</option><option>Individual</option></select>
<label>Interest</label><select><option>Please choose&hellip;</option>{opts}<option>Consultation</option><option>AI Ethics / Compliance</option><option>Implementation Support</option><option>Other</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f95a8">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "AI Consulting Near Me",
        "email": EMAIL,
        "telephone": PHONE_TEL,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "foundingDate": FOUNDED,
        "description": "AI consulting for strategy, automation, analytics, customer experience, ethics, and implementation across industries.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Nationwide (no public street address on live site)",
            "addressLocality": "United States",
            "addressRegion": "US",
            "postalCode": "",
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
            "AI Consulting Near Me | Unlock AI's Potential for Your Business",
            "Helping businesses of all sizes unlock AI's potential to improve efficiency, productivity, and growth.",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>Expert AI Consulting for Growing Businesses</h1>
<p>{escape(TAGLINE)}</p>
<a class="btn" href="request-a-consultation/index.html">Get Started</a> <a class="btn alt" href="ai-strategy-consulting/index.html">Explore Services</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>2018</b><span>Founded *[confirm]*</span></div>
<div class="stat"><b>10</b><span>Service Families</span></div>
<div class="stat"><b>Free</b><span>Initial Consultation</span></div>
<div class="stat"><b>24h</b><span>Typical Response *[confirm]*</span></div>
</div></div></section>
<section><div class="wrap"><h2>What can AI Consulting Near Me do for you?</h2>
<p class="lead">Ten service families — strategy, automation, analytics, customer AI, ethics, implementation, healthcare, finance, retail/manufacturing, and SMB solutions.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure where to start? Begin with a consultation.</h2>
<p style="margin-bottom:14px">Schedule a free consultation — tell us whether you need strategy, automation, analytics, or implementation support.</p>
<a class="btn" href="request-a-consultation/index.html">Request a Consultation</a></div></div>
<section><div class="wrap"><h2>How engagements get started</h2><div class="cols3">
<div class="card"><h3>1. Request a consultation</h3><p>Share goals — strategy, automation, analytics, or industry-specific AI.</p></div>
<div class="card"><h3>2. Scoped recommendation</h3><p>We map readiness, a prioritized roadmap, and a clear first pilot.</p></div>
<div class="card"><h3>3. Build &amp; harden</h3><p>Implement, integrate, train, and hand off with ongoing optimization options.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why AI Consulting Near Me</h2><div class="cols3">
<div class="card"><h3>Strategy before tools</h3><p>Live site focus: tailored AI strategies — not one-size-fits-all installs.</p></div>
<div class="card"><h3>End-to-end support</h3><p>Discovery → roadmap → implementation → ongoing optimization.</p></div>
<div class="card"><h3>Industry coverage</h3><p>Healthcare, finance, retail, real estate, manufacturing, and small business.</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready to get started?</h2>
<a class="btn" href="request-a-consultation/index.html">Consultation</a> <a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    "What is AI Consulting Near Me?",
                    "AI Consulting Near Me helps businesses unlock AI's potential for efficiency, productivity, and growth — strategy, automation, analytics, and implementation.",
                ),
                (
                    "When was AI Consulting Near Me founded?",
                    f"The live About page claims the firm was founded in {FOUNDED} [confirm].",
                ),
                (
                    "How do I get started?",
                    "Use Request a Consultation — share whether you need strategy, automation, analytics, or implementation.",
                ),
                (
                    "Who is it for?",
                    "Businesses of all sizes nationwide — healthcare, finance, retail, manufacturing, real estate, education, logistics, and SMBs.",
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
            f"{h['name']} | AI Consulting Near Me",
            f"{h['name']} from AI Consulting Near Me — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])} — From AI Consulting Near Me</h2>
<p class="lead">{escape(h["blurb"])} Delivered as part of the AI Consulting Near Me stack rather than an isolated task.</p>
<p><a class="btn" href="../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Solutions We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What Your Engagement Can Include</h2>
<ul class="checks">
<li>Discovery tied to your real operational goals</li>
<li>Responsible AI and privacy design before production</li>
<li>Implementation with monitoring and handoff</li>
<li>Documentation your team can run</li>
<li>One accountable consulting partner across strategy and delivery</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with a free consultation. We map goals and recommend the right service line before build work starts.",
                ),
                (
                    "Where is AI Consulting Near Me based?",
                    f"Nationwide consulting — live site positions coverage as serving businesses nationwide.",
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
        head(f"{name} | AI Consulting Near Me", f"{name} from AI Consulting Near Me — {blurb}")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Engage AI Consulting Near Me for {escape(name.lower())} and related AI consulting services.</h2>
<p class="lead">{escape(blurb)} At AI Consulting Near Me, {escape(name.lower())} is delivered as part of a consultation-led engagement — process, risk, and accountability for growing businesses.</p>
<p><a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>How {escape(name)} from AI Consulting Near Me Can Help You:</h2>
<ul class="checks">
<li>Clearer AI ownership and success criteria</li>
<li>Ethics, privacy, and risk controls designed in early</li>
<li>Documented runbooks your team can operate</li>
<li>Integrations with the tools you already use</li>
<li>Monitoring and handoff so work does not die at delivery</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} engagement scoped to your stack — not a one-size package</h2>
<p>No two organizations need {escape(name.lower())} the same way. We scope around your systems, data readiness, risk limits, and internal owners — after a consultation.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Teams avoid key risks by using a developed partner for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with DIY AI projects</h3><ul>
<li>Tool installs without a business use case</li>
<li>No success metrics or pilot exit criteria</li>
<li>Data quality and privacy ignored until production</li>
<li>No owner for adoption after the vendor demo</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on AI Consulting Near Me</h3><ul>
<li>Scoped delivery with strategy before tooling</li>
<li>Documented handoff and ops ownership</li>
<li>Monitoring and optimization after go-live</li>
<li>A named consulting path instead of ad-hoc DIY</li>
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
                    "Timelines depend on scope — strategy, automation, analytics, and implementation have different critical paths.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Pricing is scoped after consultation — the live site does not publish a public rate card.",
                ),
                (
                    f"Why choose AI Consulting Near Me for {name.lower()}?",
                    f"We deliver {name.lower()} as part of AI Consulting Near Me's AI consulting stack (founded claim {FOUNDED} [confirm]).",
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
<h2 style="font-size:20px">Initiate a request with AI Consulting Near Me</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us the project</h3><p>Strategy, automation, analytics, ethics, or industry AI.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>A scoped recommendation — or an honest no.</p></div>
<div class="card"><h3>3. Decide with the full picture</h3><p>AI outcomes vary by data, adoption, and scope; consulting is not a guaranteed ROI promise.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>AI Consulting Near Me</strong><br>Address: {escape(ADDRESS)} <em>[confirm — no street NAP on live site]</em><br>Phone: {escape(PHONE)} <em>[confirm]</em><br>Email: {escape(EMAIL)}<br>Hours: Response within 24 hours *[confirm]* · Free initial consultation</p>
<p style="font-size:13px;color:#5a6b7b">AI outcomes vary. Consulting and delivery are scoped after discovery — promotional ROI claims on the live site are not treated as verified facts here.</p>
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
        ["/", "HOME", "", "AI consulting", "logo/home", "A1,A6,A10", ""],
        [
            "/about-ai-consulting-near-me/",
            "COMP-HUB",
            "/",
            "about AI consulting",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-ai-consulting-near-me/why-choose-us/",
            "COMP-CHILD",
            "/about-ai-consulting-near-me/",
            "why choose AI consulting",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-ai-consulting-near-me/who-we-serve/",
            "COMP-CHILD",
            "/about-ai-consulting-near-me/",
            "who AI consulting serves",
            "About menu",
            "D1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact AI consulting",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "AI consulting proposal",
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
    with (ROOT / "AICNEARME-PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
        "AICNEARME-QUESTIONNAIRE-ANSWERS.md",
        "AICNEARME-PAGE-INVENTORY.csv",
        "AICNEARME-NOTES.md",
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
        ROOT / "about-ai-consulting-near-me" / "index.html",
        head(
            "About AI Consulting Near Me",
            "About AI Consulting Near Me — AI strategy, automation, and implementation. Founded claim 2018 [confirm].",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About AI Consulting Near Me</h2>
<p class="lead">Founded in {escape(FOUNDED)}, AI Consulting Near Me helps businesses unlock AI's potential to improve efficiency, productivity, and growth.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>Live site mission: help businesses of all sizes unlock AI's potential to improve efficiency, productivity, and growth.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="who-we-serve/index.html">Verticals &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "When was AI Consulting Near Me founded?",
                    f"The live About page claims the firm was founded in {FOUNDED} [confirm].",
                ),
                (
                    "What services do you offer?",
                    "Live-site services emphasize AI strategy, process automation, data analytics, implementation support, ethics/compliance, and industry solutions.",
                ),
            ]
        )
        + org_schema()
        + footer(1),
    )
    urls.append("/about-ai-consulting-near-me/")

    write(
        ROOT / "about-ai-consulting-near-me" / "why-choose-us" / "index.html",
        head("Why Choose AI Consulting Near Me", "Why teams choose AI Consulting Near Me.")
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose AI Consulting Near Me</h2>
<p class="lead">Strategic, results-driven AI consulting — from readiness assessment to ongoing optimization.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Founded 2018</h3><p>Live About page positions the firm as founded in 2018 with fresh methods [confirm stats].</p></div>
<div class="card"><h3>Ten Gate-1 service families</h3><p>Strategy, automation, analytics, CX AI, ethics, implementation, and industry lines.</p></div>
<div class="card"><h3>Industry breadth</h3><p>Live site lists healthcare, finance, retail, real estate, manufacturing, and small business.</p></div>
<div class="card"><h3>Consultation-led</h3><p>Free initial consultation CTA on the live site; forms are demo shells here.</p></div>
<div class="card"><h3>End-to-end path</h3><p>Discovery, roadmap, implementation support, ongoing optimization.</p></div>
<div class="card"><h3>No invented team bios</h3><p>Live site lists named consultants; omitted pending owner verification.</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-ai-consulting-near-me/why-choose-us/")

    ind = "".join(
        f'<div class="gcard"><h3>{escape(i)}</h3><p>AI use-case emphasis tuned for {escape(i.lower())}.</p></div>'
        for i in INDUSTRIES
    )
    write(
        ROOT / "about-ai-consulting-near-me" / "who-we-serve" / "index.html",
        head("Who We Serve | AI Consulting Near Me", "Who AI Consulting Near Me serves.")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Verticals</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Who We Serve</h2>
<p class="lead">Engagements tailored to how different industries buy and adopt AI.</p>
<div class="grid">{ind}</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-ai-consulting-near-me/who-we-serve/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | AI Consulting Near Me",
            "Contact AI Consulting Near Me",
            "Questions about AI strategy, automation, analytics, ethics, or industry solutions.",
        ),
        (
            "request-a-consultation",
            "Request a Consultation | AI Consulting Near Me",
            "Request a Consultation",
            "Tell us about your business and AI goals — we will recommend a practical first step.",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | AI Consulting Near Me",
            "Request a Proposal",
            "Share scope, systems, and constraints. We will return a scoped proposal you can compare.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | AI Consulting Near Me", "Page not found.")
        + chrome(0)
        + """
<section style="padding:72px 0"><div class="wrap"><h2 style="font-size:28px">Page not found</h2>
<p class="lead">That page isn't in this service map. Try home or request a free consultation.</p>
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
        ROOT / "AICNEARME-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — AI Consulting Near Me (FACTORY BUILD · Gate 1 10×10)

**NearMe OS Website Factory staging engine · category: AI consulting · facts from live aiconsultingnearme.com (2026-07-22) · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | AI Consulting Near Me | live site |
| A2 domain | aiconsultingnearme.com | live site |
| A3 phone | {PHONE} | live site — **looks like placeholder (555)** [confirm] |
| A4 email | {EMAIL} | live site |
| A5 address | {ADDRESS} | live site (no street NAP published) |
| A6 trade | AI consulting / business automation / AI strategy | live site |
| A7 founded | {FOUNDED} | live About — [confirm] |
| A10 value_proposition | Unlock AI potential for efficiency, productivity, and growth with tailored consulting | live site |
| A11 tagline | {TAGLINE} | live site title |
| A12 hours | Response within 24 hours (live contact) | live site |
| A13 services_core | AI strategy; process automation; data analytics; implementation; ethics/compliance; industry solutions | live site |

## B — Services: 10 × 10
{hub_slugs}
FORM-CONSULT=`request-a-consultation` · FORM-PRICING=`request-a-proposal`

## Notes
- Phone (555) marked [confirm] — placeholder pattern on live site
- Named team bios on live About omitted (pending owner verification)
- Promotional stats (500+ projects / 300% ROI) not treated as verified FACTs
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
