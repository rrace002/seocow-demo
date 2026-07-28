#!/usr/bin/env python3
"""Generate the Online Psychiatrists NearMe OS Gate 1 staging factory site.

Gate 1 architecture:
- Exactly 10 service hubs x 10 children = 100 SVC-CHILD pages
- Home + about hub + 2 about children + contact + request + schedule = 117 index pages
- Shared chrome, noindex staging controls, inventory, notes, questionnaire, and Netlify files
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.onlinepsychiatrists.com"
BRAND = "Online Psychiatrists"
SHORT_BRAND = "Online Psychiatrists"
PHYSICIAN = "Dr. Zlatin Ivanov, MD"
PHONE = "(646) 713-0000"
PHONE_TEL = "+16467130000"
PRINCETON_PHONE = "(609) 722-3000"
PRINCETON_TEL = "+16097223000"
MIAMI_PHONE = "(305) 859-0509"
MIAMI_TEL = "+13058590509"
EMAIL = "info@onlinepsychiatrists.com"
ADDRESS = "Chrysler Building, 405 Lexington Ave, #2601, New York, NY 10174"
MANHATTAN = "Manhattan, New York"
PRINCETON = "Princeton, NJ"
MIAMI = "Miami, FL"
SERVICE_STATES = "New York, New Jersey, and Florida"
POSITIONING = (
    "Private telepsychiatry and video psychiatry with personalized integrative care, "
    "medication management, psychotherapy, and HIPAA-compliant video visits."
)
STAGING_BANNER = (
    "STAGING PREVIEW — onlinepsychiatrists.com factory build · Dr. Zlatin Ivanov / "
    "Online Psychiatrists · content pending owner review · not the live website"
)
CRISIS_LINE = (
    "This is not a crisis service. If you are in crisis, call 988 or go to the nearest emergency room."
)


FACTORY_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
:root{--teal:#0f4c5c;--navy:#1e3a5f;--sage:#7d9b8a;--cream:#f7f6f2;--gold:#b78b3a;--ink:#152332;--muted:#657481;--line:#d9e2df;--mist:#eef4f1;--white:#fff}
body{font-family:"Source Sans 3",Arial,Helvetica,sans-serif;color:var(--ink);line-height:1.68;background:#fff}
h1,h2,h3,h4,.logo-name{font-family:"Fraunces",Georgia,"Times New Roman",serif}
a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1140px;margin:0 auto;padding:0 22px}
.stage{background:repeating-linear-gradient(-45deg,#17324f 0 11px,#0f4c5c 11px 22px);color:#fff;font:800 11.5px "Source Sans 3",sans-serif;letter-spacing:.055em;text-transform:uppercase;text-align:center;padding:9px 12px}
.utility{background:#102b44;color:#e7f1ef;font-size:12.5px;padding:7px 0}
.utility .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}.utility a{color:#fff}
header.main{background:#fff;border-bottom:1px solid var(--line);position:relative;z-index:50}
header.main .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-top:18px;padding-bottom:18px}
.logo{display:inline-flex;align-items:center;gap:13px;color:var(--navy);font-weight:800;text-decoration:none}
.logo-mark{width:56px;height:56px;border-radius:14px;display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(145deg,var(--teal),var(--navy));color:#fff;font:900 1.02rem "Fraunces",serif;letter-spacing:.04em;box-shadow:0 7px 18px rgba(15,76,92,.18);flex:none}
.logo-name{display:block;font-size:1.42rem;line-height:1.08;color:var(--navy)}
.logo small{display:block;color:var(--muted);font:800 10.5px "Source Sans 3",sans-serif;letter-spacing:.14em;text-transform:uppercase;margin-top:4px}
.phone-cta{text-align:right}.phone-cta a{font:900 1.25rem "Source Sans 3",sans-serif;color:var(--teal)}.phone-cta small{display:block;color:var(--muted);font-size:12px;margin-top:2px}
nav.nav{background:#fff;border-bottom:1px solid var(--line);position:relative;z-index:45}
nav.nav ul{list-style:none;display:flex;flex-wrap:wrap;align-items:center;width:100%}
nav.nav>.wrap>ul>li{position:relative}
nav.nav>div.wrap>ul>li>a{display:block;color:var(--navy);padding:13px 15px;font-size:14px;font-weight:900}
nav.nav>div.wrap>ul>li>a:hover{background:var(--mist);color:var(--teal);text-decoration:none}
nav.nav li:hover>.dd{display:block}
.dd{display:none;position:absolute;top:100%;left:0;background:#fff;min-width:310px;box-shadow:0 14px 28px rgba(30,58,95,.18);border:1px solid var(--line);border-top:4px solid var(--sage);z-index:60}
nav.nav .dd a{display:block;color:var(--ink);padding:10px 15px;font-size:13.5px;font-weight:700;border-bottom:1px solid var(--line);background:#fff}
nav.nav .dd a:hover{background:var(--mist);color:var(--teal);text-decoration:none}
.nav .em{margin-left:auto}.nav .em>a{background:var(--teal);color:#fff;margin:6px 0 6px 8px;padding:9px 18px;border-radius:999px}.nav .em>a:hover{background:var(--navy);color:#fff}
.hero{position:relative;background:radial-gradient(circle at 16% 18%,rgba(125,155,138,.28),transparent 34%),radial-gradient(circle at 84% 32%,rgba(183,139,58,.14),transparent 36%),linear-gradient(135deg,#102b44 0%,#1e3a5f 54%,#0f4c5c 100%);color:#fff;padding:84px 0 72px;overflow:hidden}
.hero:before{content:"";position:absolute;inset:0;background:linear-gradient(120deg,rgba(255,255,255,.12) 0 1px,transparent 1px 26px),radial-gradient(circle at 50% 108%,rgba(247,246,242,.18),transparent 32%);opacity:.76;pointer-events:none}
.hero .wrap{position:relative;z-index:1}.hero h1{font-size:clamp(2.25rem,5vw,3.85rem);line-height:1.06;max-width:940px;margin-bottom:18px}.hero p{max-width:800px;color:#eef7f4;font-size:1.12rem}
.eyebrow,.kicker{display:inline-flex;align-items:center;gap:12px;color:var(--gold);font:900 12px "Source Sans 3",sans-serif;letter-spacing:.14em;text-transform:uppercase;margin-bottom:14px}
.eyebrow:before,.kicker:before{content:"";display:inline-block;width:30px;height:2px;background:currentColor;flex:none}
.hero-ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:27px}
.btn{display:inline-block;background:var(--teal);color:#fff;font:900 14px "Source Sans 3",sans-serif;padding:13px 24px;border-radius:999px;border:0;cursor:pointer;box-shadow:0 8px 18px rgba(15,76,92,.16)}
.btn:hover{background:var(--navy);color:#fff;text-decoration:none}.btn.alt{background:var(--sage);color:#102b44}.btn.alt:hover{background:#6e8b7c;color:#fff}.btn.gold{background:var(--gold);color:#102b44}.btn.gold:hover{background:#9b732f;color:#fff}.btn.ghost{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.58)}.btn.ghost:hover{background:rgba(255,255,255,.12)}
section{padding:48px 0}section.tint{background:var(--mist)}section.cream{background:var(--cream)}
section h2{font-size:clamp(1.72rem,3vw,2.28rem);color:var(--navy);line-height:1.18;margin-bottom:15px}section p{margin-bottom:14px;font-size:16.5px}.lead{font-size:18px;color:#334751;max-width:860px}
.notice{background:#fff8e8;border:1px solid #ead7a7;border-left:5px solid var(--gold);padding:16px 18px;border-radius:12px;color:#473a21;margin:18px 0}
.crumb{font-size:12.5px;color:var(--muted);padding:15px 0 0}.crumb a{color:var(--muted)}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:26px}.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:18px;margin-top:22px}
.card,.gcard,.hubcard{background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:0 5px 18px rgba(30,58,95,.07)}.card{padding:25px}.gcard,.hubcard{padding:22px;border-top:5px solid var(--sage)}
.card h3,.gcard h3,.hubcard h3{font-size:18px;color:var(--navy);margin-bottom:8px}.gcard h3 a,.hubcard h3 a{color:var(--navy)}
.gcard p,.hubcard p{font-size:14.5px;color:var(--muted);margin:0}.tag{display:inline-block;margin-top:12px;font:900 10.5px "Source Sans 3",sans-serif;letter-spacing:.09em;text-transform:uppercase;color:var(--teal)}
.feature{border-left:5px solid var(--sage);background:#fff;padding:24px;border-radius:14px;border-top:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-top:24px}.stat{background:#fff;border:1px solid var(--line);border-top:4px solid var(--gold);padding:20px;text-align:center;border-radius:14px}.stat b{display:block;color:var(--navy);font-size:26px;line-height:1.1}.stat span{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;font-weight:900}
ul.checks{list-style:none;margin:10px 0}ul.checks li{padding:7px 0 7px 29px;position:relative}ul.checks li:before{content:"";position:absolute;left:2px;top:17px;width:14px;height:3px;background:var(--sage);border-radius:3px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin:22px 0}.stepnum{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--navy);color:#fff;font-weight:900;margin-bottom:12px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-top:18px}.vs .col{padding:24px}.vs .col.good{background:var(--cream)}.vs .col.bad{background:#fff}
.formbox{background:#fff;border:1px solid var(--line);border-top:5px solid var(--teal);border-radius:14px;padding:26px;max-width:720px}.formbox.highlight{border-top-color:var(--gold);box-shadow:0 10px 28px rgba(183,139,58,.12)}
.formbox label{display:block;font:900 12.5px "Source Sans 3",sans-serif;color:var(--muted);margin:12px 0 4px}.formbox input,.formbox select,.formbox textarea{width:100%;padding:10px;border:1px solid #b8c8c2;border-radius:8px;font:14px "Source Sans 3",sans-serif}.formbox textarea{min-height:100px}
details{border:1px solid var(--line);border-radius:10px;margin-bottom:10px;background:#fff}details summary{cursor:pointer;padding:14px 18px;font:900 15px "Source Sans 3",sans-serif;color:var(--navy);list-style:none}details summary:before{content:"+ ";color:var(--teal);font-weight:900}details[open] summary:before{content:"- "}details div{padding:0 18px 16px;font-size:15.5px}
.ctastrip{background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff;text-align:center;padding:40px 0}.ctastrip h2{color:#fff}.ctastrip p{color:#e7f4f1;max-width:780px;margin-left:auto;margin-right:auto}
footer{background:#102b44;color:#cfe0dd;padding:42px 0 24px;margin-top:30px;font-size:13.5px}footer h4{color:#fff;font:900 12.5px "Source Sans 3",sans-serif;letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px}footer ul{list-style:none}footer li{margin-bottom:7px}footer a{color:#f2fffc}.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:26px}.disclaimer{border-top:1px solid rgba(255,255,255,.18);margin-top:28px;padding-top:16px;color:#b7cbc8;font-size:12.5px}.copy{margin-top:12px;text-align:center;color:#9eb7b3;font-size:12px}
@media(max-width:780px){.cols2,.vs{grid-template-columns:1fr}.phone-cta{text-align:left}.hero{padding:58px 0}.dd{position:static;box-shadow:none;width:100%;border-left:0;border-right:0}.nav .em{margin-left:0;width:100%}.nav .em>a{margin:8px 12px;text-align:center}.logo-name{font-size:1.15rem}}
"""


HUB_DATA: list[tuple[str, str, str, list[str]]] = [
    (
        "telepsychiatry-video-visits",
        "Telepsychiatry & Video Visits",
        "Private video psychiatry visits for adults seeking secure evaluation, follow-up care, and continuity from home.",
        [
            "HIPAA-Compliant Video Psychiatry",
            "Same-Day Virtual Consultations",
            "Next-Day Psychiatry Appointments",
            "Secure Encrypted Sessions",
            "Smartphone Psychiatry Visits",
            "Computer Video Appointments",
            "First Virtual Evaluation",
            "Follow-Up Video Visits",
            "Private Home Telepsychiatry",
            "Integrative Online Psychiatry",
        ],
    ),
    (
        "medication-management",
        "Virtual Medication Management",
        "Medication planning and follow-up support through telepsychiatry, with prescribing rules and pharmacy coordination reviewed carefully.",
        [
            "Online Prescription Management",
            "Controlled Substance Telemedicine",
            "Ryan Haight Act Compliant Prescribing",
            "Pharmacy E-Prescriptions",
            "ADHD Medication Management",
            "Antidepressant Management",
            "Anxiety Medication Plans",
            "Mood Stabilizer Monitoring",
            "Refill Coordination Support",
            "Medication Follow-Up Visits",
        ],
    ),
    (
        "adhd-add-treatment",
        "ADHD & ADD Treatment",
        "Adult ADHD and ADD evaluation, diagnosis discussion, therapy support, and medication options through private telepsychiatry.",
        [
            "Adult ADHD Evaluation",
            "ADHD Diagnosis Online",
            "Focus And Attention Treatment",
            "Work Performance ADHD Care",
            "Student ADHD Support",
            "ADHD Medication Options",
            "ADHD Therapy Support",
            "Executive Function Coaching Psychiatry",
            "ADHD Follow-Up Care",
            "Telepsychiatry For ADHD",
        ],
    ),
    (
        "anxiety-panic-disorders",
        "Anxiety & Panic Disorders",
        "Evaluation and personalized care planning for anxiety, panic symptoms, phobias, worry, and related stress patterns.",
        [
            "Generalized Anxiety Disorder Care",
            "Panic Attack Treatment",
            "Social Anxiety Treatment",
            "Phobia-Related Anxiety Care",
            "Worry And Tension Management",
            "Anxiety Medication Management",
            "Anxiety Psychotherapy Online",
            "Performance Anxiety Support",
            "Acute Anxiety Evaluations",
            "Long-Term Anxiety Care",
        ],
    ),
    (
        "depression-mood-disorders",
        "Depression & Mood Disorders",
        "Telepsychiatry for depression and mood symptoms, including evaluation, psychotherapy, medication review, and follow-up monitoring.",
        [
            "Major Depression Treatment",
            "Mood Disorder Evaluation",
            "Persistent Depressive Symptoms",
            "Depression Medication Management",
            "Depression Psychotherapy Online",
            "Energy And Motivation Support",
            "Treatment-Resistant Depression Review",
            "Mood Fluctuation Care",
            "Telepsychiatry For Depression",
            "Follow-Up Mood Monitoring",
        ],
    ),
    (
        "bipolar-ocd-ptsd",
        "Bipolar, OCD & PTSD",
        "Specialty psychiatry support for complex conditions that may require careful medication monitoring, psychotherapy, and coordination.",
        [
            "Bipolar Disorder Management",
            "Mood Stabilization Care",
            "OCD Treatment Online",
            "Compulsion And Intrusive Thought Care",
            "PTSD Treatment Online",
            "Trauma-Informed Psychiatry",
            "Flashback And Hyperarousal Support",
            "Obsessive Thought Management",
            "Long-Term Specialty Follow-Up",
            "Complex Condition Coordination",
        ],
    ),
    (
        "addiction-psychiatry",
        "Addiction Psychiatry",
        "Confidential addiction psychiatry, substance use evaluation, dual diagnosis care, and medication-assisted treatment support where clinically appropriate.",
        [
            "Addiction Psychiatry Consults",
            "Buprenorphine Maintenance Support",
            "Substance Use Evaluation",
            "Dual Diagnosis Care",
            "Alcohol Use Disorder Support",
            "Opioid Use Disorder Care",
            "Relapse Prevention Planning",
            "Addiction Psychotherapy Online",
            "Medication-Assisted Treatment Support",
            "Confidential Addiction Follow-Up",
        ],
    ),
    (
        "psychotherapy-counseling",
        "Psychotherapy & Counseling",
        "One-on-one online psychotherapy and counseling integrated with psychiatric care when helpful for the patient's treatment plan.",
        [
            "One-On-One Video Psychotherapy",
            "Integrative Talk Therapy",
            "Relationship Stress Counseling",
            "Job Loss Coping Support",
            "Daily Stressor Therapy",
            "Personalized Therapy Plans",
            "Supportive Counseling Visits",
            "Insight-Oriented Psychotherapy",
            "Skills-Based Coping Sessions",
            "Continuity Of Care Therapy",
        ],
    ),
    (
        "ny-nj-fl-telehealth",
        "NY, NJ & FL Telehealth",
        "Telepsychiatry access for residents in New York, New Jersey, and Florida, with Manhattan, Princeton, and Miami references pending confirmation.",
        [
            "New York Telepsychiatry",
            "Manhattan Psychiatry Access",
            "Brooklyn Queens Bronx Care",
            "Long Island Telepsychiatry",
            "Westchester And Upstate NY Care",
            "New Jersey Telepsychiatry",
            "Princeton NJ Psychiatry Access",
            "Florida Telepsychiatry",
            "Miami Psychiatry Access",
            "Multi-State Licensed Care",
        ],
    ),
    (
        "scheduling-insurance-intake",
        "Scheduling, Insurance & Intake",
        "Private-practice intake, scheduling, out-of-network benefit guidance, superbill support, and visit preparation pathways.",
        [
            "Schedule Video Consultation",
            "Same-Day Appointment Requests",
            "Out-Of-Network Benefits Guidance",
            "Superbill Reimbursement Support",
            "New Patient Intake Process",
            "Insurance Verification Guidance",
            "Concierge Scheduling Support",
            "Urgent Evaluation Requests",
            "Continuity Of Care Onboarding",
            "Patient Portal Visit Prep",
        ],
    ),
]


CONDITIONS = [
    "ADHD / ADD",
    "Anxiety, panic, and phobias",
    "Depression and mood disorders",
    "Bipolar disorder",
    "OCD",
    "PTSD and trauma symptoms",
    "Eating disorders",
    "Addiction and dual diagnosis",
    "PMDD",
    "Insomnia",
]


def slugify(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def child_blurb(hub_name: str, child_name: str) -> str:
    return (
        f"{child_name} through the {hub_name} pathway, framed for private telepsychiatry "
        "review, owner confirmation, and clinically appropriate follow-up."
    )


HUBS = [
    {
        "slug": slug,
        "name": name,
        "short": name.replace(" & ", " And "),
        "blurb": blurb,
        "children": [(slugify(child), child, child_blurb(name, child)) for child in children],
    }
    for slug, name, blurb, children in HUB_DATA
]

assert len(HUBS) == 10
assert all(len(h["children"]) == 10 for h in HUBS)


def pfx(depth: int) -> str:
    return "" if depth == 0 else "../" * depth


def trunc(text: str, n: int = 155) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= n:
        return text
    return text[: n - 1].rsplit(" ", 1)[0].rstrip(" ,.;:") + "..."


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def head(title: str, desc: str, *, canonical: str | None = None) -> str:
    canon = canonical or ""
    canon_tag = (
        f'<link rel="canonical" href="{escape(canon)}">\n'
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:title" content="{escape(title)}">\n'
        f'<meta property="og:description" content="{escape(trunc(desc))}">\n'
        f'<meta property="og:url" content="{escape(canon)}">\n'
        f'<meta property="og:site_name" content="{escape(BRAND)}">\n'
        if canon
        else ""
    )
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex,nofollow">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(trunc(desc))}">
{canon_tag}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700;800&family=Source+Sans+3:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
{FACTORY_CSS}
</style></head><body>
"""


def chrome(depth: int) -> str:
    p = pfx(depth)
    hub_dd = "".join(
        f'<a href="{p}{h["slug"]}/index.html">{escape(h["name"])}</a>' for h in HUBS
    )
    return f"""<div class="stage">{escape(STAGING_BANNER)}</div>
<div class="utility"><div class="wrap"><span>Private telepsychiatry · {escape(SERVICE_STATES)} · facts pending owner review [confirm]</span><span>{escape(CRISIS_LINE)}</span></div></div>
<header class="main"><div class="wrap">
<a class="logo" href="{p}index.html"><span class="logo-mark">OP</span><span><span class="logo-name">{escape(BRAND)}</span><small>Private video psychiatry</small></span></a>
<div class="phone-cta"><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><small>{escape(MANHATTAN)} · video visits for NY / NJ / FL [confirm]</small></div>
</div></header>
<nav class="nav"><div class="wrap"><ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}{HUBS[0]["slug"]}/index.html">Services &#9662;</a><div class="dd">{hub_dd}</div></li>
<li><a href="{p}about/index.html">About &#9662;</a><div class="dd">
<a href="{p}about/index.html">About {escape(BRAND)}</a>
<a href="{p}about/why-choose-online-psychiatrists/index.html">Why Choose {escape(BRAND)}</a>
<a href="{p}about/dr-zlatin-ivanov/index.html">{escape(PHYSICIAN)}</a>
</div></li>
<li><a href="{p}request-a-consultation/index.html">Request a Consultation</a></li>
<li><a href="{p}contact/index.html">Contact</a></li>
<li class="em"><a href="{p}schedule-a-visit/index.html">Schedule a Visit</a></li>
</ul></div></nav>
"""


def footer(depth: int) -> str:
    p = pfx(depth)
    hubs = "".join(
        f'<li><a href="{p}{h["slug"]}/index.html">{escape(h["short"])}</a></li>' for h in HUBS
    )
    return f"""<footer><div class="wrap"><div class="fcols">
<div><h4>Telepsychiatry Hubs</h4><ul>{hubs}</ul></div>
<div><h4>About</h4><ul>
<li><a href="{p}about/index.html">About {escape(BRAND)}</a></li>
<li><a href="{p}about/why-choose-online-psychiatrists/index.html">Why Choose {escape(BRAND)}</a></li>
<li><a href="{p}about/dr-zlatin-ivanov/index.html">{escape(PHYSICIAN)}</a></li>
<li><a href="{p}contact/index.html">Contact</a></li>
</ul></div>
<div><h4>Start Care</h4><ul>
<li><a href="{p}schedule-a-visit/index.html">Schedule a Visit</a></li>
<li><a href="{p}request-a-consultation/index.html">Request a Consultation</a></li>
<li><a href="tel:{PHONE_TEL}">{escape(PHONE)}</a></li>
<li><a href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a></li>
</ul></div>
<div><h4>Offices / Service Areas</h4><ul>
<li>{escape(ADDRESS)}</li>
<li>{escape(PRINCETON)}: <a href="tel:{PRINCETON_TEL}">{escape(PRINCETON_PHONE)}</a> [confirm]</li>
<li>{escape(MIAMI)}: <a href="tel:{MIAMI_TEL}">{escape(MIAMI_PHONE)}</a> [confirm]</li>
</ul></div>
</div>
<div class="disclaimer"><strong>Crisis disclaimer:</strong> {escape(CRISIS_LINE)}</div>
<div class="disclaimer"><strong>Medical disclaimer:</strong> This noindex staging content is educational factory copy pending owner and clinician review. It is not medical advice, not emergency care, not a diagnosis, and not a substitute for in-person emergency evaluation or a clinician-patient relationship. Call 988 or go to the nearest emergency room for crisis or emergency needs.</div>
<div class="disclaimer"><strong>Compliance and payment notes:</strong> HIPAA-compliant video and Ryan Haight Act prescribing language is presented conceptually for owner/legal review and is not legal advice. Out-of-network and Superbill reimbursement references are public-site positioning items that require confirmation before publication. [confirm]</div>
<div class="copy">Copyright &copy; 2026 {escape(BRAND)}. Staging preview for onlinepsychiatrists.com; not the live website.</div>
</div></footer>
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


def org_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "MedicalBusiness",
        "name": BRAND,
        "url": BASE + "/",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "medicalSpecialty": ["Psychiatry", "Addiction Psychiatry"],
        "founder": {
            "@type": "Physician",
            "name": PHYSICIAN,
            "medicalSpecialty": ["Psychiatry", "Addiction Psychiatry"],
        },
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "405 Lexington Ave, #2601",
            "addressLocality": "New York",
            "addressRegion": "NY",
            "postalCode": "10174",
            "addressCountry": "US",
        },
        "areaServed": ["New York", "New Jersey", "Florida"],
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(data, ensure_ascii=True)
        + "</script>"
    )


def form_shell(form_name: str, *, highlight: bool = False) -> str:
    conditions = "".join(f"<option>{escape(c)}</option>" for c in CONDITIONS)
    states = "".join(f"<option>{escape(s)}</option>" for s in ["New York", "New Jersey", "Florida", "Other / not sure"])
    klass = "formbox highlight" if highlight else "formbox"
    return f"""<div class="{klass}">
<label>First Name</label><input type="text" name="first_name">
<label>Last Name</label><input type="text" name="last_name">
<label>Email</label><input type="email" name="email">
<label>Phone</label><input type="tel" name="phone">
<label>State of Residence</label><select name="state"><option>Please choose...</option>{states}</select>
<label>Main Concern</label><select name="condition"><option>Please choose...</option>{conditions}<option>Medication follow-up</option><option>Psychotherapy / counseling</option><option>Not sure yet</option></select>
<label>Preferred Visit Type</label><select name="visit_type"><option>Please choose...</option><option>Initial video evaluation</option><option>Follow-up video visit</option><option>Medication management</option><option>Psychotherapy visit</option><option>Insurance / superbill question</option></select>
<label>Message</label><textarea name="message" placeholder="Tell us what you would like help scheduling. Please do not submit emergency information, medical records, or highly sensitive details in this staging form."></textarea><br><br>
<button class="btn">{escape(form_name)}</button>
<p style="margin-top:12px;font-size:12px;color:#657481">Form shell for staging review. Final routing, privacy language, consent, payment, clinical screening, and emergency instructions must be approved before launch. {escape(CRISIS_LINE)}</p>
</div>"""


def stats_block() -> str:
    stats = [
        ("4.9", "Google rating claim [confirm]"),
        ("3", "NY / NJ / FL states [confirm]"),
        ("3", "Office markets cited [confirm]"),
        ("100", "SVC-child pages"),
    ]
    return (
        '<div class="stats">'
        + "".join(
            f'<div class="stat"><b>{escape(num)}</b><span>{escape(label)}</span></div>'
            for num, label in stats
        )
        + "</div><p style=\"font-size:12.5px;color:#657481;margin-top:10px\">Rating and office/service-area claims are cited from the public site/business facts for owner confirmation. No testimonials or outcomes are invented. [confirm]</p>"
    )


def condition_cards() -> str:
    return "".join(
        f'<div class="gcard"><h3>{escape(condition)}</h3><p>Referenced as a public-site condition or service topic for owner/clinician confirmation. [confirm]</p><span class="tag">Clinical topic</span></div>'
        for condition in CONDITIONS
    )


def home() -> str:
    hub_cards = []
    for h in HUBS:
        kids = "".join(
            f'<li><a href="{h["slug"]}/{s}/index.html">{escape(n)}</a></li>'
            for s, n, _ in h["children"][:3]
        )
        hub_cards.append(
            f'<div class="hubcard"><h3><a href="{h["slug"]}/index.html">{escape(h["name"])}</a></h3>'
            f"<p>{escape(h['blurb'])}</p><ul class=\"checks\">{kids}</ul>"
            f'<a href="{h["slug"]}/index.html" style="font-weight:900">Explore {escape(h["short"]).lower()} &rarr;</a></div>'
        )
    desc = (
        "Online Psychiatrists is a private telepsychiatry practice associated with Dr. Zlatin Ivanov, MD, "
        "serving New York, New Jersey, and Florida residents through video psychiatry. [confirm]"
    )
    return (
        head(f"{BRAND} | Private Telepsychiatry & Video Psychiatry", desc, canonical=f"{BASE}/")
        + chrome(0)
        + f"""
<div class="hero"><div class="wrap">
<span class="eyebrow">Private telepsychiatry staging preview</span>
<h1>Video psychiatry with personalized medication management and psychotherapy pathways.</h1>
<p>{escape(POSITIONING)} This staging build is based on public-site facts for {escape(PHYSICIAN)} and must be reviewed before publication. [confirm]</p>
<div class="hero-ctas">
<a class="btn gold" href="schedule-a-visit/index.html">Schedule a Visit</a>
<a class="btn ghost" href="request-a-consultation/index.html">Request a Consultation</a>
<a class="btn ghost" href="tel:{PHONE_TEL}">Call {escape(PHONE)}</a>
</div></div></div>
<section class="cream"><div class="wrap"><div class="kicker">Public site claims to confirm</div><h2>Private-practice telepsychiatry, not a generic marketplace.</h2>
<p class="lead">The positioning emphasizes direct private care, HIPAA-compliant video, integrative treatment, out-of-network Superbill reimbursement, and Ryan Haight Act prescribing compliance. Each claim requires owner review. [confirm]</p>
{stats_block()}</div></section>
<section><div class="wrap"><div class="cols2">
<div><div class="kicker">Clinical approach</div><h2>Medication management and psychotherapy can be planned together.</h2>
<p>The staging copy frames care as personalized and integrative: psychiatric evaluation, medication review, therapy support, follow-up visits, and coordination where clinically appropriate.</p>
<ul class="checks"><li>Video psychiatry visits for NY / NJ / FL residents. [confirm]</li><li>Adult ADHD, anxiety, depression, bipolar, OCD, PTSD, addiction, PMDD, eating disorders, phobias, and insomnia topics.</li><li>Private-pay / out-of-network positioning with Superbill references pending confirmation.</li><li>No guaranteed outcomes, testimonials, or cure claims.</li></ul></div>
<div class="feature"><h3>{escape(PHYSICIAN)}</h3><p>Business facts cite Dr. Ivanov as double board-certified by the American Board of Psychiatry and Neurology, with addiction psychiatry specialty, American Academy of Addiction Psychiatry membership, and Harvard certification as claimed on the public site. [confirm]</p><p><strong>Manhattan:</strong> {escape(ADDRESS)}<br><strong>Email:</strong> <a href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a></p></div>
</div><div class="notice"><strong>{escape(CRISIS_LINE)}</strong></div></div></section>
<section class="tint"><div class="wrap"><div class="kicker">Condition and service topics</div><h2>Common clinical topics referenced by the staging map</h2><div class="grid">{condition_cards()}</div></div></section>
<section><div class="wrap"><div class="kicker">Factory map</div><h2>Explore the 10-hub telepsychiatry taxonomy</h2><p class="lead">Gate 1 organizes the service surface into 10 hubs and 100 SVC-CHILD pages for owner review.</p><div class="cols3">{''.join(hub_cards)}</div></div></section>
"""
        + faqs(
            [
                (
                    "Is this the live Online Psychiatrists website?",
                    "No. This is a noindex staging preview for owner review and is not the live onlinepsychiatrists.com website.",
                ),
                (
                    "Can this site handle emergencies?",
                    CRISIS_LINE,
                ),
                (
                    "Are rating and credential claims final?",
                    "No. The approximately 4.9 Google rating and credential references are cited from public-site/business facts and must be confirmed before publication. [confirm]",
                ),
            ]
        )
        + f"""
<div class="ctastrip"><div class="wrap"><h2>Request a private video psychiatry consultation.</h2><p>Use the staging forms to review the lead flow for telepsychiatry, medication management, psychotherapy, and intake questions.</p><a class="btn gold" href="schedule-a-visit/index.html">Schedule a Visit</a> <a class="btn" href="contact/index.html">Contact</a></div></div>
"""
        + org_schema()
        + footer(0)
    )


def hub_page(h: dict) -> str:
    cards = "".join(
        f'<div class="gcard"><h3><a href="{s}/index.html">{escape(n)}</a></h3><p>{escape(b)}</p><span class="tag">SVC-CHILD</span></div>'
        for s, n, b in h["children"]
    )
    return (
        head(f"{h['name']} | {BRAND}", f"{h['name']} from {BRAND}. {h['blurb']}", canonical=f"{BASE}/{h['slug']}/")
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h["name"])}</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Service hub</div><h2>{escape(h["name"])} through private online psychiatry</h2>
<p class="lead">{escape(h["blurb"])} This noindex hub is written for owner and clinician review and should be checked against current clinical, prescribing, insurance, and intake workflows. [confirm]</p>
<p><a class="btn gold" href="../schedule-a-visit/index.html">Schedule a Visit</a> <a class="btn" href="../request-a-consultation/index.html">Request a Consultation</a></p>
<div class="notice"><strong>{escape(CRISIS_LINE)}</strong></div></div></section>
<section class="tint"><div class="wrap"><h2>{escape(h["short"])} Pages</h2><div class="grid">{cards}</div></div></section>
<section><div class="wrap"><h2>How this fits the Online Psychiatrists model</h2><ul class="checks">
<li>Visits are framed as private telepsychiatry rather than a generic marketplace listing.</li>
<li>Medication management and psychotherapy language avoids guarantees and requires clinical appropriateness.</li>
<li>Controlled-substance and Ryan Haight Act references require current legal and clinical confirmation. [confirm]</li>
<li>Out-of-network and Superbill references should be confirmed before public launch. [confirm]</li>
<li>Every page includes crisis and medical disclaimers.</li>
</ul></div></section>
"""
        + faqs(
            [
                (f"What is included in {h['name']}?", h["blurb"]),
                (
                    "Does this page promise a prescription or outcome?",
                    "No. This staging content does not promise medication, diagnosis, clinical outcomes, or appointment availability.",
                ),
                (
                    "Who should review this page before launch?",
                    "Online Psychiatrists ownership, clinical reviewers, legal/compliance reviewers, and form-routing owners should confirm all details.",
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
        head(f"{name} | {BRAND}", f"{name} from {BRAND}. {blurb}", canonical=f"{BASE}/{h['slug']}/{slug}/")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">{escape(h["name"])}</a> &rsaquo; {escape(name)}</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">SVC-CHILD</div><h2>{escape(name)} with private telepsychiatry review</h2>
<p class="lead">{escape(blurb)} Final copy must be checked by the practice before public use. [confirm]</p>
<p><a class="btn gold" href="../../schedule-a-visit/index.html">Schedule a Visit</a> <a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a></p>
<div class="notice"><strong>{escape(CRISIS_LINE)}</strong></div></div></section>
<section class="tint"><div class="wrap"><h2>Good-fit conversations for {escape(name.lower())}</h2><ul class="checks">
<li>Whether an initial evaluation, follow-up visit, medication management, psychotherapy, or coordination is appropriate.</li>
<li>State of residence and telehealth eligibility for New York, New Jersey, or Florida residents. [confirm]</li>
<li>Current medications, pharmacy questions, and refill timing without promising prescriptions.</li>
<li>Out-of-network reimbursement and Superbill expectations that need practice confirmation. [confirm]</li>
<li>Safety planning, urgent symptoms, and crisis escalation instructions when needed.</li>
</ul></div></section>
<section><div class="wrap"><h2>Clinical positioning for {escape(name.lower())}</h2><p>This staging page keeps the language careful: it describes a topic for evaluation and treatment planning, not a guaranteed diagnosis, medication, outcome, or appointment slot. Online Psychiatrists should reconcile final copy with current intake screening, prescribing rules, telehealth consent, and state licensure requirements. [confirm]</p></div></section>
<section class="cream"><div class="wrap"><div class="vs">
<div class="col bad"><h3>Generic marketplace framing</h3><ul class="checks"><li>Impersonal provider matching language.</li><li>Overbroad treatment promises.</li><li>Little attention to state-specific telehealth and prescribing workflows.</li></ul></div>
<div class="col good"><h3>Online Psychiatrists framing</h3><ul class="checks"><li>Private care associated with {escape(PHYSICIAN)}. [confirm]</li><li>Medication management and psychotherapy pathways.</li><li>HIPAA, Ryan Haight, and Superbill language marked for review. [confirm]</li></ul></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Ask about {escape(name.lower())}.</h2><p>Use the staging form to request a consultation review path. {escape(CRISIS_LINE)}</p><a class="btn gold" href="../../schedule-a-visit/index.html">Schedule a Visit</a> <a class="btn" href="../../contact/index.html">Contact</a></div></div>
"""
        + faqs(
            [
                (f"What is {name}?", blurb),
                (
                    f"Does {name.lower()} guarantee treatment results?",
                    "No. This page is educational staging copy only and does not guarantee diagnosis, medication, treatment response, or clinical outcome.",
                ),
                (
                    "Is this page for emergencies?",
                    CRISIS_LINE,
                ),
            ]
        )
        + f'<section><div class="wrap"><h2>Related {escape(h["short"])} Pages</h2><div class="grid">{related}</div></div></section>'
        + footer(2)
    )


def cta_page(slug: str, title: str, h2: str, lead: str, button: str, *, highlight: bool = False) -> str:
    steps = {
        "contact": [
            ("Call or email", f"Reach the Manhattan number at {PHONE} or email {EMAIL}. Princeton and Miami numbers are listed for confirmation."),
            ("Share only non-emergency context", "Use the staging form for appointment questions, insurance questions, or general intake needs."),
            ("Confirm the right next step", "The practice must confirm routing, response times, privacy language, and clinical screening before launch."),
        ],
        "request-a-consultation": [
            ("Describe the care need", "Choose a concern such as ADHD, anxiety, depression, addiction psychiatry, medication management, or therapy support."),
            ("Confirm state and visit type", "Telepsychiatry eligibility depends on state, clinical fit, technology, and practice policies. [confirm]"),
            ("Review intake expectations", "Final forms should include approved consent, privacy, payment, and emergency instructions."),
        ],
        "schedule-a-visit": [
            ("Choose an initial or follow-up path", "The highlighted staging form captures visit intent without reserving a live appointment."),
            ("Prepare practical details", "Patients may need residence state, pharmacy, current medications, and prior treatment context."),
            ("Complete approved intake", "Live scheduling must connect to the practice's approved calendar, portal, consent, and screening workflow."),
        ],
    }[slug]
    step_cards = "".join(
        f'<div class="card"><div class="stepnum">{i}</div><h3>{escape(title_text)}</h3><p>{escape(body)}</p></div>'
        for i, (title_text, body) in enumerate(steps, 1)
    )
    return (
        head(title, lead, canonical=f"{BASE}/{slug}/")
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; {escape(h2)}</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Start a private telepsychiatry conversation</div><h2>{escape(h2)}</h2><p class="lead">{escape(lead)}</p><div class="notice"><strong>{escape(CRISIS_LINE)}</strong></div></div></section>
<section><div class="wrap"><div class="steps">{step_cards}</div>{form_shell(button, highlight=highlight)}</div></section>
<section class="tint"><div class="wrap"><h2>{escape(BRAND)} contact details</h2><p><strong>{escape(PHYSICIAN)} / {escape(BRAND)}</strong><br>{escape(ADDRESS)}<br>Phone: <a href="tel:{PHONE_TEL}">{escape(PHONE)}</a><br>Email: <a href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a><br>{escape(PRINCETON)}: <a href="tel:{PRINCETON_TEL}">{escape(PRINCETON_PHONE)}</a> [confirm]<br>{escape(MIAMI)}: <a href="tel:{MIAMI_TEL}">{escape(MIAMI_PHONE)}</a> [confirm]</p></div></section>
"""
        + (org_schema() if slug == "contact" else "")
        + footer(1)
    )


def about_page() -> str:
    return (
        head(f"About {BRAND} | Private Telepsychiatry", f"About {BRAND} and {PHYSICIAN}, private video psychiatry for NY, NJ, and FL residents. [confirm]", canonical=f"{BASE}/about/")
        + chrome(1)
        + f"""
<div class="wrap crumb"><a href="../index.html">Home</a> &rsaquo; About</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">About the practice</div><h2>{escape(BRAND)} is positioned as a private telepsychiatry practice.</h2>
<p class="lead">Public-site facts associate the practice with {escape(PHYSICIAN)} and video psychiatry for {escape(SERVICE_STATES)} residents. This staging content must be confirmed before launch. [confirm]</p><div class="notice"><strong>{escape(CRISIS_LINE)}</strong></div></div></section>
<section class="cream"><div class="wrap"><h2>Facts for owner confirmation</h2>{stats_block()}</div></section>
<section><div class="wrap"><div class="cols2"><div><h2>Personalized integrative care</h2><p>The staging narrative combines medication management, psychotherapy, privacy, continuity, and telehealth convenience while avoiding clinical guarantees or invented testimonials.</p><ul class="checks"><li>HIPAA-compliant video language pending confirmation. [confirm]</li><li>Ryan Haight Act prescribing compliance language pending confirmation. [confirm]</li><li>Out-of-network / Superbill reimbursement note pending confirmation. [confirm]</li></ul></div><div class="card"><h3>About pages</h3><ul class="checks"><li><a href="why-choose-online-psychiatrists/index.html">Why Choose Online Psychiatrists</a></li><li><a href="dr-zlatin-ivanov/index.html">Dr. Zlatin Ivanov</a></li></ul></div></div></div></section>
"""
        + faqs(
            [
                ("Where is the Manhattan office?", f"The Manhattan address listed for confirmation is {ADDRESS}."),
                ("Which states are referenced?", f"The staging site references telepsychiatry for {SERVICE_STATES} residents. [confirm]"),
                ("What needs confirmation?", "All facts, credentials, review/rating claims, clinical scope, licensure, prescribing, payment, privacy, and form routing language require owner review."),
            ]
        )
        + org_schema()
        + footer(1)
    )


def why_page() -> str:
    return (
        head(f"Why Choose {BRAND} | Private Video Psychiatry", "Why patients may consider Online Psychiatrists for private telepsychiatry, pending owner confirmation.", canonical=f"{BASE}/about/why-choose-online-psychiatrists/")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; Why Choose Online Psychiatrists</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Why choose the practice</div><h2>Private telepsychiatry with continuity, privacy, and careful clinical review.</h2><p class="lead">This staging page summarizes differentiators without outcomes, testimonials, or guarantees.</p><div class="notice"><strong>{escape(CRISIS_LINE)}</strong></div></div></section>
<section class="tint"><div class="wrap"><div class="cols3">
<div class="card"><h3>Private practice model</h3><p>Positioned as direct private telepsychiatry rather than a broad provider marketplace. [confirm]</p></div>
<div class="card"><h3>Medication plus psychotherapy</h3><p>Care language supports both medication management and psychotherapy pathways when clinically appropriate.</p></div>
<div class="card"><h3>Experienced specialty background</h3><p>Credential claims for {escape(PHYSICIAN)} require final owner confirmation. [confirm]</p></div>
<div class="card"><h3>Secure video visits</h3><p>HIPAA-compliant video and secure session language must be confirmed against the actual technology stack. [confirm]</p></div>
<div class="card"><h3>Prescribing compliance</h3><p>Ryan Haight Act language is conceptual staging copy and requires legal/clinical review. [confirm]</p></div>
<div class="card"><h3>Out-of-network support</h3><p>Superbill reimbursement and insurance benefit guidance references require confirmation. [confirm]</p></div>
</div></div></section>
<div class="ctastrip"><div class="wrap"><h2>Review whether private telepsychiatry is a fit.</h2><a class="btn gold" href="../../schedule-a-visit/index.html">Schedule a Visit</a> <a class="btn" href="../../request-a-consultation/index.html">Request a Consultation</a></div></div>
"""
        + footer(2)
    )


def doctor_page() -> str:
    return (
        head(f"{PHYSICIAN} | {BRAND}", f"{PHYSICIAN} profile staging page for Online Psychiatrists, with credentials pending confirmation.", canonical=f"{BASE}/about/dr-zlatin-ivanov/")
        + chrome(2)
        + f"""
<div class="wrap crumb"><a href="../../index.html">Home</a> &rsaquo; <a href="../index.html">About</a> &rsaquo; {escape(PHYSICIAN)}</div>
<section style="padding-top:22px"><div class="wrap"><div class="kicker">Physician profile</div><h2>{escape(PHYSICIAN)} and private online psychiatry.</h2><p class="lead">Public-site/business facts describe Dr. Ivanov as double board-certified by the American Board of Psychiatry and Neurology, with addiction psychiatry specialty, American Academy of Addiction Psychiatry membership, and Harvard certification as claimed on the site. All details require confirmation. [confirm]</p><div class="notice"><strong>{escape(CRISIS_LINE)}</strong></div></div></section>
<section class="cream"><div class="wrap"><div class="cols2"><div><h2>Profile notes to verify</h2><ul class="checks"><li>Board certification status and specialty wording. [confirm]</li><li>Professional memberships and certificate language. [confirm]</li><li>Current state licensure and telehealth eligibility. [confirm]</li><li>Public rating claim of approximately 4.9 on Google reviews. [confirm]</li></ul></div><div class="feature"><h3>No testimonial invention</h3><p>This staging profile intentionally does not add patient quotes, case stories, outcomes, or guarantees. Final copy should use only approved, substantiated claims.</p></div></div></div></section>
<section><div class="wrap"><h2>Clinical focus areas referenced</h2><div class="grid">{condition_cards()}</div></div></section>
"""
        + footer(2)
    )


def write_inventory() -> None:
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
        ["/", "HOME", "", "online psychiatrists", "logo/home", "A1,A2,A3,A10", ""],
        ["/about/", "COMP-HUB", "/", "about online psychiatrists", "About menu", "A1,A6,A10", ""],
        ["/about/why-choose-online-psychiatrists/", "COMP-CHILD", "/about/", "why choose online psychiatrists", "About menu", "A10,D", ""],
        ["/about/dr-zlatin-ivanov/", "COMP-CHILD", "/about/", "dr zlatin ivanov", "About menu", "A2,A8", ""],
        ["/contact/", "COMP-CONTACT", "/", "contact online psychiatrists", "Contact menu", "A3,A4,A5", "Contact Request"],
        ["/request-a-consultation/", "FORM-CONSULT", "/", "request psychiatric consultation", "nav utility", "I1", "Consultation Request"],
        ["/schedule-a-visit/", "FORM-SCHEDULE", "/", "schedule psychiatry visit", "nav highlighted", "I1", "Schedule a Visit"],
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
                    "Schedule a Visit / Request a Consultation",
                ]
            )
    with (ROOT / "PAGE-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def write_questionnaire() -> None:
    hub_slugs = " | ".join(h["slug"] for h in HUBS)
    conditions = "\n".join(f"- {c}" for c in CONDITIONS)
    write(
        ROOT / "QUESTIONNAIRE-ANSWERS.md",
        f"""# S1 Business Questionnaire - Online Psychiatrists Factory Pages

Home page and all factory pages share one chrome: staging banner, utility bar with crisis text, logo/phone header, Services dropdown, About dropdown, Contact, Request a Consultation, and highlighted Schedule a Visit CTA.

## A - Business identity
| Field | Value | Source |
|---|---|---|
| A1 brand | {BRAND} | user-provided business facts |
| A2 physician | {PHYSICIAN} | public-site facts; confirm credential wording [confirm] |
| A3 domain | {BASE} | user-provided business facts |
| A4 primary_phone | {PHONE} / tel:{PHONE_TEL} | user-provided business facts |
| A5 additional_phones | {PRINCETON_PHONE} Princeton NJ; {MIAMI_PHONE} Miami FL | user-provided business facts [confirm] |
| A6 email | {EMAIL} | user-provided business facts |
| A7 Manhattan address | {ADDRESS} | user-provided business facts |
| A8 service states | {SERVICE_STATES} | user-provided business facts [confirm] |
| A9 positioning | {POSITIONING} | user-provided business facts [confirm] |
| A10 insurance | Out-of-network with Superbill reimbursement support | user-provided business facts [confirm] |

## B - Credential and public-site claims to confirm
- Double board-certified by the American Board of Psychiatry and Neurology. [confirm]
- Addiction psychiatry specialty. [confirm]
- Member, American Academy of Addiction Psychiatry. [confirm]
- Harvard certified as claimed on public site. [confirm]
- Approximately 4.9 Google reviews rating cited as a public-site claim; no new testimonials invented. [confirm]

## C - Conditions and service topics
{conditions}

## D - Gate 1 taxonomy
- Hubs: {len(HUBS)}
- SVC-CHILD pages: {sum(len(h['children']) for h in HUBS)}
- Total generated `index.html` pages: 117
- Hub slugs: {hub_slugs}
- Full URL map: `PAGE-INVENTORY.csv`

## E - Forms and CTAs
- Primary CTA: `schedule-a-visit` (highlighted)
- Secondary CTA: `request-a-consultation`
- Company/contact CTA: `contact`
- Form shells must be wired with owner-approved privacy, consent, intake, scheduling, payment, clinical screening, emergency, and follow-up language before public launch.

## F - Staging and compliance
- HTML uses `<meta name="robots" content="noindex,nofollow">`.
- `robots.txt` disallows all crawling.
- `netlify.toml` sends `X-Robots-Tag: noindex, nofollow`.
- Staging banner text: `{STAGING_BANNER}`
- Every generated HTML page includes crisis, medical, HIPAA/Ryan Haight conceptual, and out-of-network/Superbill confirmation disclaimers.
- No clinical outcomes, guarantees, or new testimonials are invented.
""",
    )


def write_notes() -> None:
    write(
        ROOT / "ONLINEPSYCHIATRISTS-NOTES.md",
        f"""# Online Psychiatrists Factory Build Notes

- Branch: `cursor/online-psychiatrists-factory-127e`
- Domain target: {BASE}
- Build type: NearMe OS Website Factory Gate 1 staging preview
- Page model: 10 service hubs x 10 children = 100 SVC-CHILD pages
- Generated `index.html` pages expected: 117
- Inventory URLs expected: 117
- Staging controls: HTML noindex,nofollow; robots.txt `Disallow: /`; Netlify `X-Robots-Tag: noindex, nofollow`
- Banner: `{STAGING_BANNER}`
- Visual direction: calm clinical telehealth, deep teal `#0f4c5c`, soft clinical navy `#1e3a5f`, sage `#7d9b8a`, warm off-white `#f7f6f2`, restrained gold accent `#b78b3a`
- Fonts: Fraunces for headlines and Source Sans 3 for interface/body
- Navigation: shared chrome on all pages; dropdown links use dark text on white backgrounds via `nav.nav .dd a`
- CTA language: Schedule a Visit / Request a Consultation / Contact
- Medical and crisis disclaimers appear in every footer. Crisis text: `{CRISIS_LINE}`
- Credential, rating, service area, HIPAA, Ryan Haight, and Superbill references are marked for confirmation. [confirm]
""",
    )


def write_static_files(urls: list[str]) -> None:
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
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "SAMEORIGIN"
""",
    )
    write(ROOT / "_redirects", "/*    /404.html  404\n")


def cleanup_generated_site() -> None:
    keep_names = {".git", ".gitignore", "scripts"}
    for child in list(ROOT.iterdir()):
        if child.name in keep_names:
            continue
        if child.name.startswith("."):
            continue
        if child.is_file() or child.is_symlink():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)


def main() -> None:
    urls = ["/"]
    cleanup_generated_site()

    write(ROOT / "index.html", home())

    for h in HUBS:
        write(ROOT / h["slug"] / "index.html", hub_page(h))
        urls.append(f"/{h['slug']}/")
        for child in h["children"]:
            write(ROOT / h["slug"] / child[0] / "index.html", leaf_page(h, child))
            urls.append(f"/{h['slug']}/{child[0]}/")

    write(ROOT / "about" / "index.html", about_page())
    urls.append("/about/")
    write(ROOT / "about" / "why-choose-online-psychiatrists" / "index.html", why_page())
    urls.append("/about/why-choose-online-psychiatrists/")
    write(ROOT / "about" / "dr-zlatin-ivanov" / "index.html", doctor_page())
    urls.append("/about/dr-zlatin-ivanov/")

    for slug, title, h2, lead, button, highlight in [
        (
            "contact",
            f"Contact {BRAND}",
            f"Contact {BRAND}",
            "Call, email, or send a staging inquiry for telepsychiatry, medication management, psychotherapy, or scheduling questions.",
            "Contact Online Psychiatrists",
            False,
        ),
        (
            "request-a-consultation",
            f"Request a Consultation | {BRAND}",
            "Request a Private Psychiatry Consultation",
            "Share the concern, state of residence, and preferred visit type so the practice can confirm the right next step.",
            "Request a Consultation",
            False,
        ),
        (
            "schedule-a-visit",
            f"Schedule a Visit | {BRAND}",
            "Schedule a Video Psychiatry Visit",
            "Use the highlighted staging form to review the lead flow for initial evaluations and follow-up video psychiatry visits.",
            "Schedule a Visit",
            True,
        ),
    ]:
        write(ROOT / slug / "index.html", cta_page(slug, title, h2, lead, button, highlight=highlight))
        urls.append(f"/{slug}/")

    write(
        ROOT / "404.html",
        head(f"Page Not Found | {BRAND}", "Page not found.")
        + chrome(0)
        + f"""
<section style="padding:72px 0"><div class="wrap"><h2>Page not found</h2>
<p class="lead">That URL is not in the {escape(BRAND)} staging factory map. Return home or use the highlighted scheduling form.</p>
<div class="notice"><strong>{escape(CRISIS_LINE)}</strong></div>
<p><a class="btn" href="index.html">Back to Home</a> <a class="btn gold" href="schedule-a-visit/index.html">Schedule a Visit</a></p>
</div></section>
"""
        + footer(0),
    )

    write_static_files(urls)
    write_inventory()
    write_questionnaire()
    write_notes()

    index_pages = list(ROOT.rglob("index.html"))
    inventory_children = 0
    inventory_rows = 0
    with (ROOT / "PAGE-INVENTORY.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            inventory_rows += 1
            if row["type_id"] == "SVC-CHILD":
                inventory_children += 1

    print(f"Index pages on disk: {len(index_pages)}")
    print(f"Sitemap URLs: {len(urls)}")
    print(f"Inventory URLs: {inventory_rows}")
    print(f"Hubs: {len(HUBS)}")
    print(f"SVC-CHILD inventory rows: {inventory_children}")
    print("Home uses shared factory chrome: yes")
    print("Staging noindex controls: yes")
    print("Dropdown CSS dark-on-white: yes")
    print("Crisis disclaimer on every generated page: yes")


if __name__ == "__main__":
    main()
