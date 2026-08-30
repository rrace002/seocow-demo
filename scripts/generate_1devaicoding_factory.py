#!/usr/bin/env python3
"""Generate 1Dev AI Coding Services site using the NearMe OS Website Factory template.

Gate 1: 10 hubs × 10 children = 100 SVC-CHILD pages (+ chrome ≈ 117).
Category: AI-assisted software development / coding services
(apps, websites, automation, integrations, AI features) — not generic AI consulting.
Facts: Race Computer Services S1 defaults · [confirm] = needs owner verification.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://1devaicoding.com"  # [confirm] vs 1dev.ai
PHONE = "(862) 295-0011"
PHONE_TEL = "+18622950011"
EMAIL = "info@1devaicoding.com"  # [confirm]
HQ = "Elizabeth, NJ · Remote US"
ADDRESS = "12 Sayre St, Elizabeth, NJ 07208"  # Race CS default hub [confirm]
OPERATOR = "Race Computer Services, LLC"  # [confirm]
BRAND = "1Dev AI Coding Services"
TAGLINE = "AI-Assisted Software Development for Apps, Sites & Automations"
STAGING_BANNER = (
    "STAGING PREVIEW — 1Dev AI Coding Services factory build · Elizabeth, NJ / remote US · "
    "content pending owner review"
)

# Ink + electric aqua (distinct from AI Consulting slate-cyan and mover navy/orange)
FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:#0b1c24;line-height:1.65;background:#fff}
h1,h2,h3,.nav,.btn,.card h3,.utility{font-family:'Segoe UI',Arial,Helvetica,sans-serif}
a{color:#0891b2;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.demo-banner{background:#05080d;color:#99f6e4;text-align:center;font:600 12px 'Segoe UI',sans-serif;padding:6px;letter-spacing:.4px}
.utility{background:#0e1a24;color:#ccfbf1;font-size:12.5px;padding:5px 0}
.utility .wrap{display:flex;justify-content:space-between}
header.main{background:#fff;border-bottom:3px solid #00e8d0;position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;padding-top:14px;padding-bottom:14px;flex-wrap:wrap;gap:10px}
.logo{font:800 22px 'Segoe UI',sans-serif;color:#071018}.logo span{color:#00c4b4}
.logo small{display:block;font:600 10.5px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:1.5px;text-transform:uppercase}
.phone-cta{text-align:right;font-family:'Segoe UI',sans-serif}
.phone-cta a{font-size:19px;font-weight:800;color:#071018}
.phone-cta small{display:block;color:#5a6b7b;font-size:11px}
nav.nav{background:#071018}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap}
nav.nav>.wrap>ul>li{position:relative}
nav.nav>div.wrap>ul>li>a{display:block;color:#fff;padding:12px 15px;font-size:13.5px;font-weight:600}
nav.nav>div.wrap>ul>li>a:hover{background:#0e1a24;text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:270px;box-shadow:0 8px 22px rgba(0,0,0,.18);border-top:3px solid #00e8d0;z-index:60}
nav.nav .dd a{display:block;color:#071018;padding:10px 15px;font-size:13.5px;font-weight:500;border-bottom:1px solid #ccfbf1;background:#fff}
nav.nav .dd a:hover{background:#f0fdfa;color:#071018;text-decoration:none}
nav.nav>div.wrap>ul>li.em>a{background:#00e8d0;color:#071018}
nav.nav>div.wrap>ul>li.em>a:hover{background:#00c4b4;color:#071018}
.hero{background:linear-gradient(rgba(7,16,24,.88),rgba(7,16,24,.88)),repeating-linear-gradient(45deg,#071018 0 14px,#0e1a24 14px 28px);color:#fff;text-align:center;padding:74px 0 64px}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25}
.hero p{color:#99f6e4;font:600 15px 'Segoe UI',sans-serif;letter-spacing:.5px}
.hero .btn{margin-top:26px}
.btn{display:inline-block;background:#00e8d0;color:#071018;font:700 14px 'Segoe UI',sans-serif;padding:13px 28px;border-radius:4px;border:none;cursor:pointer}
.btn:hover{background:#00c4b4;text-decoration:none;color:#071018}
.btn.alt{background:#0e1a24;color:#fff}.btn.alt:hover{background:#152636}
section{padding:44px 0}
section.tint{background:#f0fdfa}
section h2{font-size:25px;color:#071018;margin-bottom:16px;line-height:1.3}
section p{margin-bottom:14px;font-size:16.5px}
.lead{font-size:17px}
ul.checks{list-style:none;margin:10px 0 6px}
ul.checks li{padding:7px 0 7px 30px;position:relative;font-size:16px}
ul.checks li:before{content:"\2713";position:absolute;left:4px;color:#00c4b4;font-weight:800;font-family:'Segoe UI',sans-serif}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}
@media(max-width:760px){.cols2{grid-template-columns:1fr}.hero h1{font-size:26px}}
.card{background:#fff;border:1px solid #ccfbf1;border-radius:6px;padding:24px;box-shadow:0 2px 6px rgba(7,16,24,.06)}
.card h3{color:#071018;font-size:18px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:20px}
.gcard{background:#fff;border:1px solid #ccfbf1;border-left:4px solid #00e8d0;border-radius:6px;padding:20px}
.gcard h3{font-size:16px;margin-bottom:8px}.gcard h3 a{color:#071018}
.gcard p{font-size:14px;color:#44525f;margin:0}
.gcard .tag{display:inline-block;margin-top:10px;font:600 10.5px 'Segoe UI',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#0f766e}
.ctastrip{background:#071018;color:#fff;text-align:center;padding:36px 0}
.ctastrip h2{color:#fff;margin-bottom:14px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #ccfbf1;border-radius:6px;overflow:hidden;margin-top:18px}
.vs .col{padding:24px}
.vs .col.bad{background:#f0fdfa}.vs .col.good{background:#f0fdfa}
.vs h3{font-size:16px;margin-bottom:12px;color:#071018}
.vs ul{list-style:none}.vs li{padding:8px 0 8px 26px;position:relative;font-size:15px;border-bottom:1px dashed #e2e2e2}
.vs .bad li:before{content:"\2717";position:absolute;left:2px;color:#c0392b;font-weight:800}
.vs .good li:before{content:"\2713";position:absolute;left:2px;color:#00c4b4;font-weight:800}
@media(max-width:760px){.vs{grid-template-columns:1fr}}
details{border:1px solid #ccfbf1;border-radius:5px;margin-bottom:10px;background:#fff}
details summary{cursor:pointer;padding:14px 18px;font:600 15px 'Segoe UI',sans-serif;color:#071018;list-style:none}
details summary:before{content:"+ ";color:#00c4b4;font-weight:800}
details[open] summary:before{content:"\2013 "}
details div{padding:0 18px 16px;font-size:15.5px}
.formbox{background:#fff;border:1px solid #ccfbf1;border-top:4px solid #00e8d0;border-radius:6px;padding:28px;max-width:640px}
.formbox label{display:block;font:600 12.5px 'Segoe UI',sans-serif;color:#44525f;margin:12px 0 4px}
.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #c4cdd5;border-radius:4px;font:14px 'Segoe UI',sans-serif}
.formbox textarea{min-height:90px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin:22px 0}
.crumb{font:12.5px 'Segoe UI',sans-serif;color:#5a6b7b;padding:14px 0 0}
.crumb a{color:#5a6b7b}
footer{background:#05080d;color:#9ca8b0;padding:44px 0 26px;margin-top:30px;font-size:13.5px}
footer h4{color:#fff;font:700 13px 'Segoe UI',sans-serif;letter-spacing:.8px;text-transform:uppercase;margin-bottom:12px}
footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#9ca8b0}
.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.copy{border-top:1px solid #0e1a24;margin-top:30px;padding-top:16px;text-align:center;font-size:12px;color:#6b7a82}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-top:8px}
.stat{background:#fff;border:1px solid #ccfbf1;border-top:4px solid #00e8d0;border-radius:6px;padding:18px;text-align:center}
.stat b{display:block;font:800 20px 'Segoe UI',sans-serif;color:#071018}
.stat span{font:600 12px 'Segoe UI',sans-serif;color:#5a6b7b;letter-spacing:.4px;text-transform:uppercase}
.hubcard{background:#fff;border:1px solid #ccfbf1;border-radius:8px;padding:22px;box-shadow:0 3px 10px rgba(0,232,208,.08)}
.hubcard h3{font-size:17px;margin-bottom:6px}.hubcard h3 a{color:#071018}
.hubcard ul{list-style:none;margin:10px 0}
.hubcard li{padding:4px 0 4px 22px;position:relative;font-size:13.5px}
.hubcard li:before{content:"\2192";position:absolute;left:2px;color:#00c4b4;font-weight:700}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.audit{background:#00e8d0;color:#071018;text-align:center;padding:32px 0}
.audit h2{color:#071018;margin-bottom:8px}.audit a.btn{background:#071018;color:#fff}
.audit a.btn:hover{background:#0e1a24;color:#fff}
"""

# Gate 1 — 10 × 10 AI-assisted coding services (no LOC doorway pages)
HUBS = [
    {
        "slug": "custom-software-development",
        "name": "Custom Software Development",
        "short": "Custom Software",
        "blurb": "Purpose-built applications for how your business actually operates — not a bolted-on template.",
        "children": [
            ("custom-business-applications", "Custom Business Applications", "Line-of-business apps that match your workflows, permissions, and data — not a generic SaaS clone."),
            ("desktop-application-development", "Desktop Application Development", "Windows or cross-desktop tools when a browser app is the wrong fit."),
            ("internal-tools-and-admin-panels", "Internal Tools & Admin Panels", "Ops consoles, staff tools, and admin UIs that keep teams out of spreadsheets."),
            ("saas-product-development", "SaaS Product Development", "Multi-user product builds with tenancy, billing hooks, and a deployable codebase."),
            ("legacy-system-replacement", "Legacy System Replacement", "Replace aging desktop or custom stacks with a maintainable rewrite path [confirm scope]."),
            ("domain-specific-software-builds", "Domain-Specific Software Builds", "Software shaped around your industry process instead of a one-size module."),
            ("multi-tenant-application-development", "Multi-Tenant Application Development", "Shared platforms with tenant isolation, roles, and configuration boundaries."),
            ("workflow-centric-custom-software", "Workflow-Centric Custom Software", "Apps centered on statuses, assignments, and handoffs your staff already use."),
            ("data-heavy-application-development", "Data-Heavy Application Development", "Apps that ingest, validate, and present large operational datasets without melting."),
            ("custom-software-architecture", "Custom Software Architecture", "Architecture and module boundaries before you pour months into the wrong shape."),
        ],
    },
    {
        "slug": "web-application-development",
        "name": "Web Application Development",
        "short": "Web Apps",
        "blurb": "Browser-based products — portals, dashboards, and full-stack web apps shipped as working software.",
        "children": [
            ("full-stack-web-applications", "Full-Stack Web Applications", "Front end plus API plus data layer as one delivery, not three disconnected vendors."),
            ("customer-portals-and-dashboards", "Customer Portals & Dashboards", "Logged-in portals where customers see status, files, and next actions."),
            ("progressive-web-apps", "Progressive Web Apps", "Installable, resilient web apps when a native store listing is not required."),
            ("admin-consoles-and-back-offices", "Admin Consoles & Back Offices", "Staff-facing consoles for content, users, orders, or cases."),
            ("authentication-and-user-accounts", "Authentication & User Accounts", "Sign-up, login, roles, and session handling wired into the product."),
            ("real-time-web-applications", "Real-Time Web Applications", "Live updates, presence, or event streams when polling is not enough."),
            ("ecommerce-web-applications", "E-Commerce Web Applications", "Catalog, cart, and checkout flows as a custom web app [confirm payment processor]."),
            ("content-driven-web-platforms", "Content-Driven Web Platforms", "Editorial or knowledge platforms with structured content and publishing controls."),
            ("single-page-application-development", "Single-Page Application Development", "SPA front ends when the UX needs client-side routing and state."),
            ("server-side-rendered-web-apps", "Server-Side Rendered Web Apps", "SSR or hybrid rendering when SEO and first paint matter for the product."),
        ],
    },
    {
        "slug": "mobile-app-development",
        "name": "Mobile App Development",
        "short": "Mobile",
        "blurb": "iOS, Android, and companion apps with a backend you can actually operate after launch.",
        "children": [
            ("ios-app-development", "iOS App Development", "Native or Swift-first iOS apps scoped to the features you need in v1."),
            ("android-app-development", "Android App Development", "Android apps built against current store and device realities."),
            ("cross-platform-mobile-apps", "Cross-Platform Mobile Apps", "Shared-code mobile apps when one codebase is the right tradeoff."),
            ("mobile-backend-apis", "Mobile Backend APIs", "APIs, auth, and push plumbing that the mobile client depends on."),
            ("push-notifications-and-messaging", "Push Notifications & Messaging", "Push, in-app alerts, and messaging hooks with opt-in and targeting controls."),
            ("offline-capable-mobile-apps", "Offline-Capable Mobile Apps", "Local cache and sync so field or travel use still works."),
            ("mobile-app-ui-implementation", "Mobile App UI Implementation", "Screen flows implemented from a design or a practical spec — not endless mockups."),
            ("app-store-submission-support", "App Store Submission Support", "Build, signing, and store listing support for first submission [confirm accounts]."),
            ("mobile-app-rebuilds", "Mobile App Rebuilds", "Rescue or rewrite a stalled mobile codebase instead of starting from a blank repo."),
            ("companion-mobile-apps", "Companion Mobile Apps", "Mobile clients that sit beside an existing web or ops system."),
        ],
    },
    {
        "slug": "ai-feature-integration",
        "name": "AI Feature Integration",
        "short": "AI Features",
        "blurb": "Ship useful AI inside real products — retrieval, assistants, and guarded generation — not a slide deck.",
        "children": [
            ("llm-features-in-existing-apps", "LLM Features in Existing Apps", "Add language-model features to software you already run, with logging and fallbacks."),
            ("chat-and-assistant-interfaces", "Chat & Assistant Interfaces", "In-product assistants that call tools and hand off when they should not guess."),
            ("document-qa-features", "Document Q&A Features", "Ask-your-files features grounded in your documents, not the open internet."),
            ("ai-search-and-retrieval", "AI Search & Retrieval", "Retrieval-augmented search over tickets, docs, or product catalogs."),
            ("prompt-to-action-workflows", "Prompt-to-Action Workflows", "Turn a prompt into a structured action your app can execute and audit."),
            ("ai-content-generation-features", "AI Content Generation Features", "Draft, rewrite, or summarize features with review steps before anything publishes."),
            ("recommendation-features", "Recommendation Features", "Next-item or next-step recommendations tied to your data, not a black-box vendor toy."),
            ("speech-and-transcription-features", "Speech & Transcription Features", "Speech-to-text and related pipelines wired into your product flow."),
            ("ai-feature-guardrails-and-evals", "Guardrails & Evals for AI Features", "Eval sets, refusal behavior, and logging so AI features do not silently degrade."),
            ("human-in-the-loop-ai-features", "Human-in-the-Loop AI Features", "Queues and approvals so people stay in control of high-stakes outputs."),
        ],
    },
    {
        "slug": "automation-and-workflows",
        "name": "Automation & Workflows",
        "short": "Automation",
        "blurb": "Code-backed automations that move data and tasks — with owners, logs, and a way to change them later.",
        "children": [
            ("business-process-automation", "Business Process Automation", "Encode a repeatable process so staff are not copy-pasting between tools."),
            ("scheduled-job-and-batch-automation", "Scheduled Job & Batch Automation", "Nightly and interval jobs that process files, reports, or queues on a clock."),
            ("data-sync-automation", "Data Sync Automation", "Keep two systems aligned without a person exporting CSVs every Friday."),
            ("notification-and-alert-workflows", "Notification & Alert Workflows", "Alerts that fire on real conditions — not noisy spam nobody trusts."),
            ("approval-workflow-automation", "Approval Workflow Automation", "Request, review, and approve steps with an audit trail."),
            ("spreadsheet-and-form-automation", "Spreadsheet & Form Automation", "Replace fragile sheet macros with scripts and forms that survive the next hire."),
            ("ops-runbook-automation", "Ops Runbook Automation", "Turn a runbook into scripts and checks a person can still override."),
            ("lead-and-crm-automation", "Lead & CRM Automation", "Create, enrich, and route records in the CRM you already use [confirm system]."),
            ("invoice-and-billing-automation", "Invoice & Billing Automation", "Generate, send, or reconcile billing artifacts with a human checkpoint."),
            ("custom-webhook-automation", "Custom Webhook Automation", "Inbound and outbound webhooks that trigger the next step in your stack."),
        ],
    },
    {
        "slug": "api-and-systems-integration",
        "name": "API & Systems Integration",
        "short": "Integrations",
        "blurb": "Connect the systems you already pay for — APIs, webhooks, identity, and data movement you can maintain.",
        "children": [
            ("rest-api-development", "REST API Development", "Stable HTTP APIs with auth, versioning, and error shapes your clients can rely on."),
            ("third-party-api-integrations", "Third-Party API Integrations", "Wire vendor APIs into your product with retries, mapping, and failure handling."),
            ("payment-processor-integrations", "Payment Processor Integrations", "Checkout, webhooks, and reconciliation against a named processor [confirm]."),
            ("crm-and-erp-integrations", "CRM & ERP Integrations", "Sync customers, orders, or inventory with the system of record you already run."),
            ("webhook-and-event-pipelines", "Webhook & Event Pipelines", "Event in, transform, persist, and notify — with dead-letter handling."),
            ("sso-and-identity-integrations", "SSO & Identity Integrations", "SSO, OAuth, and directory hooks so users do not keep another password [confirm IdP]."),
            ("data-warehouse-connectors", "Data Warehouse Connectors", "Extract and load operational data into the warehouse your analysts already use."),
            ("file-and-storage-integrations", "File & Storage Integrations", "S3, drive, and file-drop integrations with size, type, and virus-scan considerations."),
            ("legacy-system-adapters", "Legacy System Adapters", "Adapters around older databases or SOAP/file drops so new apps can talk to them."),
            ("api-documentation-and-sdks", "API Documentation & SDKs", "Docs and thin client helpers so the next developer is not reverse-engineering calls."),
        ],
    },
    {
        "slug": "code-review-and-rescue",
        "name": "Code Review & Rescue",
        "short": "Code Rescue",
        "blurb": "Independent review, hotfixes, and rescue of stalled or AI-generated codebases you cannot ship as-is.",
        "children": [
            ("independent-code-review", "Independent Code Review", "A second set of eyes on architecture, tests, and merge risk before you scale the team."),
            ("security-minded-code-review", "Security-Minded Code Review", "Auth, secrets, injection, and access-control review — not a penetration-test substitute [confirm]."),
            ("performance-bottleneck-review", "Performance Bottleneck Review", "Find the slow queries, N+1s, and payload bloat that make the app feel stuck."),
            ("abandoned-project-rescue", "Abandoned Project Rescue", "Take over a half-finished repo, document it, and define a shippable next increment."),
            ("technical-debt-assessment", "Technical Debt Assessment", "A written map of debt vs. risk so you know what to pay down first."),
            ("hotfix-and-production-firefighting", "Hotfix & Production Firefighting", "Stabilize a production incident, then leave a note so it does not recur the same way."),
            ("architecture-recovery-reviews", "Architecture Recovery Reviews", "Recover the intended shape of a codebase after months of unreviewed AI or contractor churn."),
            ("dependency-and-upgrade-rescue", "Dependency & Upgrade Rescue", "Unstick blocked framework or library upgrades that froze the project."),
            ("test-coverage-rescue", "Test Coverage Rescue", "Add the tests that actually protect the risky paths — not vanity coverage numbers."),
            ("handoff-documentation-rescue", "Handoff Documentation Rescue", "README, runbooks, and env docs so the next person can run the project locally."),
        ],
    },
    {
        "slug": "mvp-and-startup-builds",
        "name": "MVP & Startup Builds",
        "short": "MVPs",
        "blurb": "First-ship products for founders — scoped, deployable, and structured so a pivot does not mean a rewrite from zero.",
        "children": [
            ("startup-mvp-development", "Startup MVP Development", "A first production build limited to the features that prove the business question."),
            ("prototype-to-production", "Clickable Prototype to Production", "Turn a Figma or click-dummy into a deployed app with real accounts and data."),
            ("founder-led-product-scoping", "Founder-Led Product Scoping", "Cut the backlog to a v1 you can actually finish with current budget and time."),
            ("first-customer-feature-builds", "First-Customer Feature Builds", "Build the slice a design partner needs without boiling the whole product."),
            ("landing-page-plus-app-mvp", "Landing Page Plus App MVP", "Marketing site plus the core app loop so waitlists can convert into users."),
            ("stripe-ready-mvp-billing", "Stripe-Ready MVP Billing", "Plans, checkout, and customer portal basics when billing is part of the proof [confirm]."),
            ("auth-and-onboarding-for-mvps", "Auth & Onboarding for MVPs", "Sign-up, empty states, and first-run flows that do not leak users."),
            ("analytics-ready-mvp-instrumentation", "Analytics-Ready MVP Instrumentation", "Events that answer whether people finish the core loop — not vanity pageviews."),
            ("pivot-friendly-mvp-architecture", "Pivot-Friendly MVP Architecture", "Sensible module boundaries so the second version is not a total rewrite."),
            ("post-mvp-hardening", "Post-MVP Hardening", "Tests, backups, and ops basics after the first users show up."),
        ],
    },
    {
        "slug": "maintenance-and-support",
        "name": "Maintenance & Support",
        "short": "Maintenance",
        "blurb": "Keep shipped software running — patches, small features, deploys, and documented handoffs.",
        "children": [
            ("ongoing-application-maintenance", "Ongoing Application Maintenance", "A defined cadence for bugs, small changes, and dependency hygiene."),
            ("bug-fix-retainers", "Bug-Fix Retainers", "A reserved hours block for defects instead of starting a new SOW for every ticket [confirm]."),
            ("dependency-and-security-updates", "Dependency & Security Updates", "Patch cadence for libraries and runtime CVEs that actually apply to your stack."),
            ("hosting-and-deploy-support", "Hosting & Deploy Support", "CI, hosting, and release help for the environment you already use [confirm provider]."),
            ("performance-monitoring-support", "Performance Monitoring Support", "Basic uptime and error visibility so issues are noticed before customers email you."),
            ("feature-increment-retainers", "Feature Increment Retainers", "Small, scoped feature batches on a retainer instead of a full rebuild."),
            ("incident-support-windows", "Incident Support Windows", "Agreed response windows for production issues — hours to be confirmed in writing [confirm]."),
            ("database-maintenance-support", "Database Maintenance Support", "Migrations, backups, and index hygiene for the database the app depends on."),
            ("documentation-upkeep", "Documentation Upkeep", "Keep runbooks and env docs current as the product changes."),
            ("vendor-handoff-maintenance", "Vendor Handoff Maintenance", "Take over a prior vendor’s repo with a written baseline before new work starts."),
        ],
    },
    {
        "slug": "ai-pair-programming-and-training",
        "name": "AI Pair Programming & Training",
        "short": "Pair & Train",
        "blurb": "Hands-on AI coding sessions, team playbooks, and short staff-augmented sprints — teaching while shipping.",
        "children": [
            ("ai-pair-programming-sessions", "AI Pair Programming Sessions", "Live pairing with AI-assisted tooling on your actual repo, not a toy kata."),
            ("cursor-and-copilot-workflow-training", "Cursor & Copilot Workflow Training", "Practical workflows for AI editors so the team gets speed without silent breakage."),
            ("team-ai-coding-playbooks", "Team AI Coding Playbooks", "Written conventions: when to accept, when to rewrite, what must be reviewed."),
            ("prompt-engineering-for-developers", "Prompt Engineering for Developers", "Repo-specific prompting so the model sees the right files, tests, and constraints."),
            ("codebase-onboarding-with-ai", "Codebase Onboarding with AI", "Use AI to map a legacy repo faster — with a human still owning the mental model."),
            ("ai-assisted-test-writing-training", "AI-Assisted Test Writing Training", "Teach the team to generate useful tests and then verify they actually fail for the right reason."),
            ("ai-code-review-coaching", "AI Code Review Coaching", "How to use AI as a review aid without rubber-stamping generated diffs."),
            ("staff-augmented-ai-coding-sprints", "Staff-Augmented AI Coding Sprints", "A time-boxed coding burst where 1Dev contributes as an extra senior pair [confirm availability]."),
            ("engineering-manager-ai-briefings", "Engineering Manager AI Briefings", "Plain briefings on what AI coding changes in process, review, and risk."),
            ("safe-ai-coding-policy-workshops", "Safe AI Coding Policy Workshops", "Secrets, licenses, and data-handling rules for AI tools in your environment [confirm]."),
        ],
    },
]

SERVICE_AREAS = [
    "Elizabeth, NJ (hub)",
    "Jersey City, NJ",
    "Newark, NJ",
    "Hoboken, NJ",
    "Union, NJ",
    "Westfield, NJ",
    "Summit, NJ",
    "Morristown, NJ",
    "Montclair, NJ",
    "Hackensack, NJ",
    "North Jersey (in-person / hybrid) [confirm]",
    "Remote (United States) [confirm]",
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
<div class="logo">1Dev <span>AI</span><small>Coding Services · Elizabeth, NJ</small></div>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>Request a coding quote</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about-1dev/index.html">About &#9662;</a><div class="dd">
<a href="{p}about-1dev/index.html">About 1Dev AI Coding Services</a>
<a href="{p}about-1dev/why-choose-us/index.html">Why Choose Us</a>
<a href="{p}about-1dev/service-areas/index.html">Service Areas</a>
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
<li><a href="{p}about-1dev/index.html">About 1Dev AI Coding Services</a></li>
<li><a href="{p}about-1dev/why-choose-us/index.html">Why Choose Us</a></li>
<li><a href="{p}about-1dev/service-areas/index.html">Service Areas</a></li>
<li><a href="{p}contact/index.html">Contact Us</a></li>
</ul></div>
<div><h4>Get Started</h4><ul>
<li><a href="{p}request-a-quote/index.html">Request a Quote</a></li>
<li><a href="{p}request-a-proposal/index.html">Request a Proposal</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Visit</h4><ul><li>{escape(ADDRESS)} <em>[confirm]</em></li><li>Operated by {escape(OPERATOR)} <em>[confirm]</em></li><li>North Jersey hub · remote US work <em>[confirm]</em></li></ul></div>
</div>
<div class="copy">1Dev AI Coding Services &middot; {escape(OPERATOR)} &middot; {escape(HQ)} &middot; {escape(PHONE)}<br>
Copyright &copy; 2026. 1Dev AI Coding Services. All rights reserved.<br>
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
<label>Project Type</label><select><option>Please choose&hellip;</option><option>New build / MVP</option><option>Add features to existing software</option><option>AI feature in an existing app</option><option>Integration / automation</option><option>Code review or rescue</option><option>Maintenance retainer</option><option>Training / pair programming</option><option>Not sure</option></select>
<label>Service Needed</label><select><option>Please choose&hellip;</option>{opts}<option>General coding question</option><option>Other</option></select>
<label>Timing</label><select><option>Please choose&hellip;</option><option>Exploring / quote only</option><option>Within 2–6 weeks</option><option>This quarter</option><option>Ongoing retainer</option></select>
<label>Message</label><textarea></textarea><br><br>
<button class="btn">Submit Now</button>
<p style="margin-top:12px;font-size:12px;color:#7f9588">Demo form shell — submission destination wired at rollout.</p>
</div>"""


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": BRAND,
        "legalName": OPERATOR,
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "url": BASE + "/",
        "slogan": TAGLINE,
        "areaServed": [
            {
                "@type": "AdministrativeArea",
                "name": "North Jersey",
                "containedInPlace": {"@type": "State", "name": "New Jersey"},
            },
            {"@type": "Country", "name": "United States"},
        ],
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
            "1Dev AI Coding Services | AI-Assisted Software Development",
            "1Dev AI Coding Services builds apps, websites, automations, integrations, and AI features for North Jersey and remote US teams — operated by Race Computer Services, LLC [confirm].",
        )
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap"><h1>1Dev AI Coding Services</h1>
<p>Custom software, web and mobile apps, AI features, automations, and code rescue — shipped as working code, not a strategy deck.</p>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a></div></div>
<section class="tint"><div class="wrap"><div class="stats">
<div class="stat"><b>Apps</b><span>Web, Mobile, Custom</span></div>
<div class="stat"><b>AI Features</b><span>Inside Real Products</span></div>
<div class="stat"><b>Integrations</b><span>APIs &amp; Automations</span></div>
<div class="stat"><b>Rescue</b><span>Review &amp; Recover</span></div>
</div></div></section>
<section><div class="wrap"><h2>Coding services for teams that need software shipped</h2>
<p class="lead">Ten service families — custom software, web and mobile, AI feature work, automations, integrations, code review and rescue, MVPs, maintenance, and AI pair-programming training.</p>
<div class="cols3">{''.join(cards)}</div></div></section>
<div class="audit"><div class="wrap"><h2>Not sure which build path you need? Start with a quote.</h2>
<p style="margin-bottom:14px">Tell us the stack, the repo (or lack of one), and the outcome you need in the next increment — we help you choose a coding path.</p>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a></div></div>
<section><div class="wrap"><h2>How to get started</h2><div class="cols3">
<div class="card"><h3>1. Request a quote</h3><p>Share the product, current stack or repo, and whether this is a new build, a feature add, or a rescue.</p></div>
<div class="card"><h3>2. Scope the work</h3><p>We clarify constraints, integrations, AI vs. conventional code, and whether a quote or a written proposal fits.</p></div>
<div class="card"><h3>3. Agree the increment</h3><p>Confirm scope in writing before build hours start — no invented delivery-date guarantees.</p></div>
</div></div></section>
<section class="tint"><div class="wrap"><h2>Why 1Dev AI Coding Services</h2><div class="cols3">
<div class="card"><h3>Code, not consulting theater</h3><p>We write, review, and ship software. Strategy exists to size the next increment — not to replace delivery.</p></div>
<div class="card"><h3>AI where it belongs</h3><p>AI features and AI-assisted coding are tools inside a maintainable codebase, with review and tests.</p></div>
<div class="card"><h3>Elizabeth hub, remote US</h3><p>North Jersey in-person / hybrid when it helps; remote delivery across the US [confirm].</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ready for a coding quote?</h2>
<a class="btn" href="request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (
                    "What is 1Dev AI Coding Services?",
                    "1Dev AI Coding Services is an AI-assisted software development shop: custom software, web and mobile apps, AI features inside products, automations, API integrations, code review and rescue, MVPs, maintenance, and pair-programming training.",
                ),
                (
                    "Who operates 1Dev AI Coding Services?",
                    f"1Dev AI Coding Services is operated by {OPERATOR}, with headquarters listed at {ADDRESS} [confirm].",
                ),
                (
                    "How do I get a quote?",
                    "Use Request a Quote or call us. Share the product, stack or repo, and timing — we follow up with next steps. Larger or multi-phase work can move to Request a Proposal.",
                ),
                (
                    "Do you only work in New Jersey?",
                    "Elizabeth, NJ is the listed hub. Local / hybrid work in North Jersey and remote US delivery are both in scope [confirm coverage for your project].",
                ),
                (
                    "Are you licensed for this work?",
                    "Business licensing and insurance status are listed as [confirm] pending owner verification — ask during your quote conversation. This is software development, not a regulated professional license like medicine or law.",
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
            f"{h['name']} | 1Dev AI Coding Services",
            f"{h['name']} from 1Dev AI Coding Services in Elizabeth, NJ and remote US — {h['blurb']}",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(h["name"])}</h2>
<p class="lead">{escape(h["blurb"])} Part of 1Dev AI Coding Services — AI-assisted development with a quote path before hours start.</p>
<p><a class="btn" href="../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Services We Provide</h2>
<div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>What a typical engagement can include</h2>
<ul class="checks">
<li>Clear description of the product, repo, and success for the next increment</li>
<li>Stack, hosting, and integration constraints named before build</li>
<li>AI-assisted coding with human review — not unreviewed generated dumps</li>
<li>Written next steps after the quote or proposal path</li>
<li>Elizabeth, NJ hub with remote US delivery [confirm]</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What are {h['name']}?", h["blurb"]),
                (
                    "How do we get started?",
                    "Begin with Request a Quote. For larger or multi-phase builds, use Request a Proposal.",
                ),
                (
                    "Where is 1Dev AI Coding Services based?",
                    f"Headquartered in {HQ} ({ADDRESS}) [confirm]. Coding work is delivered locally/hybrid in North Jersey and remotely across the US [confirm].",
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
            f"{name} | 1Dev AI Coding Services",
            f"{name} from 1Dev AI Coding Services — {blurb}",
        )
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">{escape(name)} from 1Dev AI Coding Services</h2>
<p class="lead">{escape(blurb)} At 1Dev, {escape(name.lower())} is delivered as working software work — scoped, reviewed, and quote-led before you commit hours.</p>
<p><a class="btn" href="../../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></p>
</div></section>
<section class="tint"><div class="wrap"><h2>{escape(name)} with 1Dev can help you gain:</h2>
<ul class="checks">
<li>A defined increment instead of an open-ended “we’ll figure it out in code”</li>
<li>AI-assisted speed with human review, tests, and a repo you can keep</li>
<li>Integrations and automations named against the systems you already run</li>
<li>Written quote or proposal steps before major build spend</li>
<li>Honest scope — no invented testimonials, awards, or wait-time guarantees</li>
</ul></div></section>
<section><div class="wrap"><h2>A {escape(name.lower())} path scoped to your repo — not a one-size package</h2>
<p>No two teams need {escape(name.lower())} the same way. We match the current codebase (or greenfield), constraints, and the next shippable increment — then confirm next steps before build hours start.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Teams avoid key risks with a developed coding path for {escape(name.lower())}</h2>
<div class="vs">
<div class="col bad"><h3>Common failure modes with ad-hoc or unreviewed AI coding</h3><ul>
<li>Generated code nobody on the team can operate</li>
<li>Features that demo well and fail on real data</li>
<li>No tests, no deploy path, no handoff docs</li>
<li>Strategy decks that never become a running application</li>
</ul></div>
<div class="col good"><h3>Improvements when relying on 1Dev AI Coding Services</h3><ul>
<li>Custom software, AI features, and integrations under one service map</li>
<li>Quote and proposal paths before you commit</li>
<li>North Jersey hub with remote US delivery [confirm]</li>
<li>Race Computer Services accountability for this factory build [confirm]</li>
</ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>See next steps first — request a quote</h2>
<p style="max-width:720px;margin:0 auto 16px">Curious what {escape(name.lower())} looks like for your product? Start with a quote request.</p>
<a class="btn" href="../../request-a-quote/index.html">Request a Quote</a> <a class="btn alt" href="../../request-a-proposal/index.html">Request a Proposal</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"How long until {name.lower()} is scheduled?",
                    "Timing depends on repo state, integrations, and current capacity. We discuss windows after the quote — no invented same-week ship guarantees.",
                ),
                (
                    f"What does {name.lower()} cost?",
                    "Price depends on scope, existing codebase quality, and integrations. Use Request a Quote for an estimate path; larger work can use Request a Proposal.",
                ),
                (
                    f"Why choose 1Dev AI Coding Services for {name.lower()}?",
                    f"We deliver {name.lower()} as part of an AI-assisted coding shop — apps, automations, and AI features with a clear quote and proposal path.",
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
<h2 style="font-size:20px">Initiate a request with 1Dev AI Coding Services</h2>
<p class="lead">{escape(lead)}</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="card"><h3>1. Tell us the work</h3><p>Product, stack or repo, and whether this is a build, feature, rescue, or retainer.</p></div>
<div class="card"><h3>2. Get a straight answer</h3><p>A quote path, a proposal for larger work, or honest advice on next steps.</p></div>
<div class="card"><h3>3. Confirm the increment</h3><p>Confirm scope in writing before coding hours start.</p></div>
</div>{form_shell()}</div></section>
<section class="tint"><div class="wrap"><h2>Contact Details</h2>
<p><strong>1Dev AI Coding Services</strong><br>Operated by {escape(OPERATOR)} <em>[confirm]</em><br>Headquarters: {escape(ADDRESS)} <em>[confirm]</em><br>Phone: {escape(PHONE)}<br>Email: {escape(EMAIL)} <em>[confirm]</em></p>
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
        ["/", "HOME", "", "1dev ai coding services", "logo/home", "A1,A6,A10", ""],
        [
            "/about-1dev/",
            "COMP-HUB",
            "/",
            "about 1dev ai coding services",
            "About menu",
            "A1,A10",
            "",
        ],
        [
            "/about-1dev/why-choose-us/",
            "COMP-CHILD",
            "/about-1dev/",
            "why choose 1dev ai coding",
            "About menu",
            "A10,A12",
            "",
        ],
        [
            "/about-1dev/service-areas/",
            "COMP-CHILD",
            "/about-1dev/",
            "1dev coding service areas",
            "About menu",
            "F1",
            "",
        ],
        [
            "/contact/",
            "COMP-CONTACT",
            "/",
            "contact 1dev ai coding",
            "Contact menu",
            "A3,A4,A5,I1",
            "Phone Request",
        ],
        [
            "/request-a-proposal/",
            "FORM-PRICING",
            "/",
            "ai coding proposal",
            "nav utility",
            "I1",
            "Request for Proposal",
        ],
        [
            "/request-a-quote/",
            "FORM-CONSULT",
            "/",
            "ai coding quote",
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
                h["name"].lower() + " 1dev",
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
                    n.lower() + " 1dev",
                    "Services menu > hub grid",
                    "B row",
                    "Request for Proposal",
                ]
            )
    with (ROOT / "1DEVAICODING-PAGE-INVENTORY.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    keep = {
        ".git",
        "scripts",
        "seocow-demo-site.zip",
        "1DEVAICODING-QUESTIONNAIRE-ANSWERS.md",
        "1DEVAICODING-PAGE-INVENTORY.csv",
        "1DEVAICODING-NOTES.md",
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
        ROOT / "about-1dev" / "index.html",
        head(
            "About 1Dev AI Coding Services | AI-Assisted Software Development",
            "1Dev AI Coding Services builds custom software, web and mobile apps, AI features, automations, and integrations from Elizabeth, NJ with remote US delivery [confirm].",
        )
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">About 1Dev AI Coding Services</h2>
<p class="lead">1Dev AI Coding Services is an AI-assisted software development shop for custom software, web and mobile apps, AI features, automations, integrations, code rescue, MVPs, maintenance, and pair-programming training — operated by {escape(OPERATOR)} from {escape(ADDRESS)} <em>[confirm]</em>.</p>
</div></section>
<section class="tint"><div class="wrap"><h2>Who we are</h2>
<p>We focus on shipping code: applications, sites, automations, and AI features inside products. Consulting-style roadmaps exist only to size the next increment — this brand is a coding services shop, not a generic AI strategy firm.</p>
<p><a href="why-choose-us/index.html">Why choose us &rarr;</a> &middot; <a href="service-areas/index.html">Service areas &rarr;</a></p>
</div></section>
"""
        + faqs(
            [
                (
                    "Who operates 1Dev AI Coding Services?",
                    f"1Dev AI Coding Services is operated by {OPERATOR}, headquartered at {ADDRESS} [confirm].",
                ),
                (
                    "Do you work outside New Jersey?",
                    "Elizabeth is the listed hub. North Jersey hybrid and remote US delivery are both in this Gate 1 map [confirm].",
                ),
            ]
        )
        + org_schema()
        + footer(1),
    )
    urls.append("/about-1dev/")

    write(
        ROOT / "about-1dev" / "why-choose-us" / "index.html",
        head(
            "Why Choose 1Dev AI Coding Services",
            "Why teams choose 1Dev AI Coding Services for AI-assisted software development.",
        )
        + chrome(2)
        + """
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Us</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Why Choose 1Dev AI Coding Services</h2>
<p class="lead">A coding shop built around shipping software with AI-assisted development — without invented testimonials.</p></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Software, not slideware</h3><p>Custom apps, web/mobile, AI features, and integrations land as code in a repo you can keep.</p></div>
<div class="card"><h3>AI-assisted, human-reviewed</h3><p>We use AI coding tools to move faster, then review, test, and document like a senior pair.</p></div>
<div class="card"><h3>Rescue is a first-class path</h3><p>Abandoned, over-generated, or stalled codebases get a review-and-recover track.</p></div>
<div class="card"><h3>Quote-led intake</h3><p>Request a Quote first; larger jobs can move to a written proposal.</p></div>
<div class="card"><h3>Honest staging copy</h3><p>No fabricated reviews, awards, or wait-time guarantees. Licensing noted as [confirm].</p></div>
<div class="card"><h3>Named operator</h3><p>Race Computer Services accountability for this factory build [confirm].</p></div>
</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-1dev/why-choose-us/")

    areas = "".join(
        f'<div class="gcard"><h3>{escape(a)}</h3><p>Coding inquiries for {escape(a)} — coverage confirmed case by case.</p></div>'
        for a in SERVICE_AREAS
    )
    write(
        ROOT / "about-1dev" / "service-areas" / "index.html",
        head(
            "Service Areas | 1Dev AI Coding Services",
            "Service areas for 1Dev AI Coding Services — North Jersey hub and remote US [confirm].",
        )
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Service Areas</div>
<section style="padding-top:20px"><div class="wrap"><h2 style="font-size:28px">Service Areas</h2>
<p class="lead">Primary hub: Elizabeth, NJ. North Jersey hybrid and remote US delivery listed below may be served case by case — no LOC doorway city pages in this Gate 1 build.</p>
<div class="grid">{areas}</div></div></section>
"""
        + footer(2),
    )
    urls.append("/about-1dev/service-areas/")

    for slug, title, h2, lead in [
        (
            "contact",
            "Contact Us | 1Dev AI Coding Services",
            "Contact Us for Coding Inquiries",
            "Tell us the product, stack or repo, and whether you need a quote or a written proposal.",
        ),
        (
            "request-a-quote",
            "Request a Quote | 1Dev AI Coding Services",
            "Request a Coding Quote",
            "Describe the work — product, stack, AI vs. conventional code, and timing — we follow up with clear next steps.",
        ),
        (
            "request-a-proposal",
            "Request a Proposal | 1Dev AI Coding Services",
            "Request a Proposal for Larger Builds",
            "Share multi-phase, MVP, or rescue goals. We return a scoped proposal you can compare.",
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head("Page Not Found | 1Dev AI Coding Services", "Page not found.")
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
        ROOT / "1DEVAICODING-QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire — 1Dev AI Coding Services (FACTORY BUILD · Gate 1 10×10)

**Build uses NearMe OS Website Factory instructions-template (SEO Cow staging engine) · category: AI-assisted software development / coding services · Race Computer Services S1 defaults · [confirm] = needs owner verification**

## A — Business identity
| Field | Value | Source |
|---|---|---|
| A1 business_name | 1Dev AI Coding Services (operated by Race Computer Services, LLC) | this build [confirm] |
| A2 domain | 1devaicoding.com (alt: 1dev.ai) | [confirm] |
| A3 phone | {PHONE} | Race CS / S1 (same operator) |
| A4 email | {EMAIL} | [confirm] |
| A5 address | {ADDRESS} | Race CS default [confirm] |
| A6 trade | AI-assisted software development / coding services (apps, websites, automation, integrations, AI features) | this build |
| A7 founded | not stated — omitted | — |
| A10 value_proposition | AI-assisted custom software, web/mobile apps, AI features, automations, and code rescue | this build |
| A11 tagline | {TAGLINE} | this build |
| A12 competitor_type | generic AI consultancies, offshore body shops, unreviewed AI codegen, freelance marketplaces | [confirm] |
| A13 hours | not stated — omitted | — |
| licensed_insured | Business license / insurance | [confirm] |

## B — Services: 10 categories × 10 children
{hub_slugs} — full map in 1DEVAICODING-PAGE-INVENTORY.csv.
FORM-CONSULT = `request-a-quote` · FORM-PRICING = `request-a-proposal`.

## C–I
- D1 audiences: founders, product owners, small/mid teams needing software shipped, teams with stalled or AI-generated codebases
- F1 service_area: Elizabeth NJ hub; North Jersey hybrid; remote US [confirm]; listed cities case by case (no LOC doorway pages)
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
        ROOT / "1DEVAICODING-NOTES.md",
        f"""# 1Dev AI Coding Services — Factory Build

Local service category: **AI-assisted software development / coding services**.

- Generator: `scripts/generate_1devaicoding_factory.py`
- Gate 1: 10 × 10 = 100 SVC-CHILD (+ chrome ≈ 117 pages)
- Brand: 1Dev AI Coding Services (logo: 1Dev + AI)
- FORM-CONSULT: `/request-a-quote/` (highlighted)
- FORM-PRICING: `/request-a-proposal/`
- About: `/about-1dev/` · why-choose-us · service-areas
- Staging: noindex + STAGING PREVIEW banner + robots Disallow + Netlify X-Robots-Tag
- Domain / email / NAP: 1devaicoding.com · {EMAIL} · {ADDRESS} *[confirm]* (alt domain 1dev.ai [confirm])
- CSS: ink / electric aqua (`#071018` / `#0e1a24` / `#00e8d0` / `#00c4b4` / `#f0fdfa`)
- Nav CSS scoped: `nav.nav>div.wrap>ul>li>a` white; `nav.nav .dd a` dark on white
- No invented testimonials; licensed/insured only as [confirm]; no LOC doorway pages
- Not generic AI consulting — coding/delivery vertical
""",
    )

    pages = list(ROOT.rglob("index.html"))
    factory_pages = list(pages)
    print(f"Generated {len(factory_pages)} factory index pages")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Hubs: {len(HUBS)} · Children: {sum(len(h['children']) for h in HUBS)}")


if __name__ == "__main__":
    main()
