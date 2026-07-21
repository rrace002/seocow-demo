#!/usr/bin/env python3
"""Apply launch-readiness fixes across the SEO Cow static site."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://seocow.com"

SERVICE_OPTIONS = [
    ("local-seo-services", "Local SEO Services"),
    ("technical-seo-services", "Technical SEO Services"),
    ("link-building-services", "Link Building Services"),
    ("content-marketing-services", "Content Marketing Services"),
    ("ecommerce-seo-services", "Ecommerce SEO Services"),
    ("ppc-management-services", "PPC Management Services"),
    ("social-media-marketing-services", "Social Media Marketing Services"),
    ("seo-web-design-services", "SEO Web Design Services"),
    ("seo-consulting-services", "SEO Consulting Services"),
    ("small-business-seo-services", "Small Business SEO Services"),
    ("free-website-audit", "Free Website Audit"),
    ("other", "Other / Not sure"),
]

CONFIRM_REPLACEMENTS = [
    (
        "month-to-month accountability [confirm terms]",
        "clear written terms and monthly accountability reporting",
    ),
    (
        "Month-to-month accountability, no lock-in [confirm terms]",
        "Clear scope, written terms, and monthly accountability reporting",
    ),
    (
        " [confirm wording]",
        "",
    ),
    (
        "Clients stay because campaigns perform. Your profiles, content, and data remain yours. [confirm contract terms]",
        "Clients stay because campaigns perform. Your profiles, content, and data remain yours, and engagement terms are agreed in writing before work begins.",
    ),
    (
        "We keep clients by performing, not by contract lock-in. [confirm contract terms]",
        "We keep clients by performing. Engagement terms are agreed in writing before work begins.",
    ),
]

LOCAL_BUSINESS_SCHEMA = {
    "@context": "https://schema.org",
    "@type": ["ProfessionalService", "LocalBusiness"],
    "name": "SEO Cow",
    "legalName": "Race Computer Services, LLC",
    "telephone": "+1-862-295-0011",
    "email": "info@seocow.com",
    "url": "https://seocow.com/",
    "slogan": "Specialist software, expert knowledge, what's not to like?!",
    "image": "https://seocow.com/assets/images/og-default.svg",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "12 Sayre St",
        "addressLocality": "Elizabeth",
        "addressRegion": "NJ",
        "postalCode": "07208",
        "addressCountry": "US",
    },
    "areaServed": [
        {"@type": "AdministrativeArea", "name": "New Jersey"},
        {"@type": "AdministrativeArea", "name": "New York"},
        {"@type": "Country", "name": "United States"},
    ],
    "priceRange": "$$",
}


def page_depth(path: Path) -> int:
    rel = path.relative_to(ROOT)
    return len(rel.parts) - 1


def rel_prefix(depth: int) -> str:
    return "" if depth == 0 else "../" * depth


def canonical_path(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    return "/" + str(Path(rel).parent).replace("\\", "/") + "/"


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def truncate_meta(text: str, limit: int = 158) -> str:
    from html import unescape

    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(" ,.;:-") + "…"


def extract_shared_css(sample: str) -> str:
    match = re.search(r"<style>(.*?)</style>", sample, re.S)
    if not match:
        raise SystemExit("Could not extract shared CSS")
    css = match.group(1)
    extras = """
a.logo{text-decoration:none}
a.logo:hover{text-decoration:none}
.skip-link{position:absolute;left:-999px;top:auto;width:1px;height:1px;overflow:hidden}
.skip-link:focus{position:static;left:auto;width:auto;height:auto;display:inline-block;padding:8px 14px;background:#8bc53f;color:#173f2a;font:700 13px 'Segoe UI',sans-serif;z-index:100}
h1{font-family:'Segoe UI',Arial,Helvetica,sans-serif;font-size:28px;color:#173f2a;margin-bottom:16px;line-height:1.3}
.hero h1{font-size:34px;max-width:820px;margin:0 auto 14px;line-height:1.25;color:#fff}
@media(max-width:760px){.hero h1{font-size:26px}}
.formbox .form-actions{margin-top:16px}
.formbox .form-note{margin-top:12px;font-size:12px;color:#7f95a8}
.form-success{display:none;background:#eef7e2;border:1px solid #8bc53f;border-radius:5px;padding:14px 16px;margin-bottom:14px;font:600 14px 'Segoe UI',sans-serif;color:#3c6318}
.hero-visual{min-height:42vh;background:
  radial-gradient(ellipse at 20% 30%,rgba(139,197,63,.28),transparent 55%),
  radial-gradient(ellipse at 80% 70%,rgba(46,125,50,.22),transparent 50%),
  linear-gradient(165deg,#0a1a2a 0%,#173f2a 48%,#1b4a32 100%);
  position:relative;overflow:hidden}
.hero-visual::after{content:"";position:absolute;inset:0;background:
  repeating-linear-gradient(120deg,transparent 0 18px,rgba(255,255,255,.03) 18px 19px);
  pointer-events:none}
.hero.hero-visual{padding:86px 0 72px}
"""
    # Ensure h1 is in the font stack rule
    css = css.replace(
        "h1,h2,h3,.nav,.btn,.card h3,.utility",
        "h1,h2,h3,.nav,.btn,.card h3,.utility",
    )
    return css + extras


def build_head_extras(path: Path, title: str, description: str, depth: int) -> str:
    prefix = rel_prefix(depth)
    canon = BASE + canonical_path(path)
    desc = truncate_meta(description)
    og_title = strip_tags(title).replace("&amp;", "&")
    return "\n".join(
        [
            f'<link rel="canonical" href="{escape(canon, quote=True)}">',
            f'<meta property="og:type" content="website">',
            f'<meta property="og:url" content="{escape(canon, quote=True)}">',
            f'<meta property="og:title" content="{escape(og_title, quote=True)}">',
            f'<meta property="og:description" content="{escape(desc, quote=True)}">',
            f'<meta property="og:image" content="{BASE}/assets/images/og-default.svg">',
            f'<meta name="twitter:card" content="summary_large_image">',
            f'<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">',
            f'<link rel="stylesheet" href="{prefix}assets/css/site.css">',
        ]
    )


def promote_h1(html: str) -> str:
    if re.search(r"<h1\b", html, re.I):
        return html

    # Styled title H2 used as page title
    styled = re.search(
        r'<h2 style="font-size:(2[89]|3\d)px">(.*?)</h2>',
        html,
        re.S,
    )
    if styled:
        return html.replace(styled.group(0), f"<h1>{styled.group(2)}</h1>", 1)

    # Hub / first content H2 after crumb or section
    first_h2 = re.search(r"<h2>(.*?)</h2>", html, re.S)
    if first_h2:
        return html.replace(first_h2.group(0), f"<h1>{first_h2.group(1)}</h1>", 1)
    return html


def fix_logo(html: str, depth: int) -> str:
    prefix = rel_prefix(depth)
    home = f"{prefix}index.html" if depth else "index.html"
    # Prefer clean directory home link for depth 0 too
    home_href = f"{prefix}" if depth else "./"
    # Keep index.html for file-open compatibility at nested levels where ./ is current dir
    if depth == 0:
        home_href = "index.html"
    else:
        home_href = f"{prefix}index.html"

    pattern = re.compile(
        r'<div class="logo">SEO <span>Cow</span><small>ROI-Driven Search Marketing</small></div>'
    )
    replacement = (
        f'<a class="logo" href="{home_href}">SEO <span>Cow</span>'
        f"<small>ROI-Driven Search Marketing</small></a>"
    )
    return pattern.sub(replacement, html, count=1)


def remove_demo_banner(html: str) -> str:
    return re.sub(
        r'<div class="demo-banner">.*?</div>\s*',
        "",
        html,
        count=1,
        flags=re.S,
    )


def resolve_confirms(html: str) -> str:
    for old, new in CONFIRM_REPLACEMENTS:
        html = html.replace(old, new)
    # Catch any remaining markers
    html = re.sub(r"\s*\[confirm[^\]]*\]", "", html)
    return html


def shorten_meta_description(html: str) -> str:
    def repl(match: re.Match[str]) -> str:
        desc = match.group(1)
        short = truncate_meta(desc)
        return f'<meta name="description" content="{escape(short, quote=True)}">'

    return re.sub(
        r'<meta name="description" content="([^"]*)">',
        repl,
        html,
        count=1,
    )


def inject_head(html: str, path: Path, depth: int) -> str:
    title_m = re.search(r"<title>(.*?)</title>", html, re.S)
    desc_m = re.search(
        r'<meta name="description" content="([^"]*)">',
        html,
    )
    title = title_m.group(1) if title_m else "SEO Cow"
    description = desc_m.group(1) if desc_m else ""

    # Remove inline style block
    html = re.sub(r"<style>.*?</style>", "", html, count=1, flags=re.S)

    extras = build_head_extras(path, title, description, depth)
    html = html.replace("</head>", extras + "\n</head>", 1)
    return html


def inject_skip_and_main(html: str) -> str:
    if 'class="skip-link"' in html:
        return html
    html = html.replace(
        "<body>",
        '<body>\n<a class="skip-link" href="#main">Skip to main content</a>',
        1,
    )
    # Open main after nav
    html = re.sub(
        r"(</nav>\s*)",
        r'\1<main id="main">\n',
        html,
        count=1,
    )
    html = html.replace("<footer>", "</main>\n<footer>", 1)
    return html


def enhance_home_hero(html: str, path: Path) -> str:
    if path.name != "index.html" or path.parent != ROOT:
        return html
    html = html.replace('<div class="hero">', '<div class="hero hero-visual">', 1)
    return html


def replace_business_schema(html: str) -> str:
    # Replace existing ProfessionalService-only blocks with richer schema
    pattern = re.compile(
        r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "ProfessionalService".*?</script>',
        re.S,
    )
    block = (
        '<script type="application/ld+json">'
        + json.dumps(LOCAL_BUSINESS_SCHEMA, ensure_ascii=True)
        + "</script>"
    )
    if pattern.search(html):
        return pattern.sub(block, html, count=1)
    # Home may only have FAQ; append business schema before </body>
    if "ProfessionalService" not in html and "LocalBusiness" not in html:
        return html.replace("</body>", block + "\n</body>", 1)
    return html


def option_html() -> str:
    opts = ['<option value="">Please choose…</option>']
    for value, label in SERVICE_OPTIONS:
        opts.append(f'<option value="{value}">{escape(label)}</option>')
    return "".join(opts)


def rebuild_formbox(html: str, form_id: str, submit_label: str) -> str:
    if "formbox" not in html:
        return html

    prefix_depth = 0  # unused; script linked in head/body separately
    new_form = f'''<div class="formbox">
<div class="form-success" role="status" hidden>Thanks — your message is ready in your email app. If nothing opened, email info@seocow.com.</div>
<form id="{form_id}" class="lead-form" action="mailto:info@seocow.com" method="post" enctype="text/plain">
<label for="{form_id}-first">First Name</label>
<input id="{form_id}-first" name="first_name" type="text" autocomplete="given-name" required>
<label for="{form_id}-last">Last Name</label>
<input id="{form_id}-last" name="last_name" type="text" autocomplete="family-name" required>
<label for="{form_id}-email">Email</label>
<input id="{form_id}-email" name="email" type="email" autocomplete="email" required>
<label for="{form_id}-phone">Phone</label>
<input id="{form_id}-phone" name="phone" type="tel" autocomplete="tel">
<label for="{form_id}-service">Service Interested In</label>
<select id="{form_id}-service" name="service" required>{option_html()}</select>
<label for="{form_id}-message">Message</label>
<textarea id="{form_id}-message" name="message" required></textarea>
<div class="form-actions"><button class="btn" type="submit">{escape(submit_label)}</button></div>
<p class="form-note">Submits via your email app to info@seocow.com. A server endpoint can replace this at rollout.</p>
</form>
</div>'''

    return re.sub(
        r'<div class="formbox">.*?</div>(?=\s*</div>\s*</section>)',
        new_form,
        html,
        count=1,
        flags=re.S,
    )


def fix_forms(html: str, path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "contact/index.html":
        return rebuild_formbox(html, "contact-form", "Send Message")
    if rel == "request-a-proposal/index.html":
        return rebuild_formbox(html, "proposal-form", "Request Proposal")
    if rel == "free-website-audit/index.html":
        return rebuild_formbox(html, "audit-form", "Request Free Audit")
    return html


def inject_form_script(html: str, depth: int) -> str:
    if "lead-form" not in html:
        return html
    if "assets/js/forms.js" in html:
        return html
    prefix = rel_prefix(depth)
    tag = f'<script src="{prefix}assets/js/forms.js" defer></script>'
    return html.replace("</body>", tag + "\n</body>", 1)


def sync_faq_json_ld(html: str) -> str:
    """After confirm replacements, keep FAQ JSON-LD text in sync if markers remain in scripts."""
    # Already handled by resolve_confirms on full file; ensure escaped variants too
    html = html.replace(
        "month-to-month accountability [confirm terms]",
        "clear written terms and monthly accountability reporting",
    )
    html = html.replace(" [confirm wording]", "")
    html = re.sub(r"\\u0020\[confirm[^\]]*\]", "", html)
    html = re.sub(r"\s*\[confirm[^\]]*\]", "", html)
    return html


def process_page(path: Path, shared_css_written: bool) -> None:
    raw = path.read_text(encoding="utf-8")
    depth = page_depth(path)

    if not shared_css_written:
        raise RuntimeError("CSS must be written first")

    html = raw
    html = remove_demo_banner(html)
    html = resolve_confirms(html)
    html = sync_faq_json_ld(html)
    html = shorten_meta_description(html)
    html = promote_h1(html)
    html = fix_logo(html, depth)
    html = inject_head(html, path, depth)
    html = inject_skip_and_main(html)
    html = enhance_home_hero(html, path)
    html = fix_forms(html, path)
    html = inject_form_script(html, depth)

    rel = path.relative_to(ROOT).as_posix()
    if rel in {"index.html", "contact/index.html", "about-seo-company/index.html"}:
        html = replace_business_schema(html)

    # Clean doubled whitespace from style removal in head
    html = re.sub(r"\n{3,}", "\n\n", html)
    path.write_text(html, encoding="utf-8")


def write_assets(sample_html: str) -> None:
    css_dir = ROOT / "assets" / "css"
    js_dir = ROOT / "assets" / "js"
    img_dir = ROOT / "assets" / "images"
    css_dir.mkdir(parents=True, exist_ok=True)
    js_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)

    (css_dir / "site.css").write_text(extract_shared_css(sample_html), encoding="utf-8")

    (ROOT / "assets" / "favicon.svg").write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="SEO Cow">
  <rect width="64" height="64" rx="12" fill="#173f2a"/>
  <circle cx="32" cy="34" r="16" fill="#8bc53f"/>
  <path d="M20 28c2-8 8-12 12-12s10 4 12 12" fill="none" stroke="#c9e89a" stroke-width="3" stroke-linecap="round"/>
  <text x="32" y="40" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="800" fill="#173f2a">SC</text>
</svg>
""",
        encoding="utf-8",
    )

    (img_dir / "og-default.svg").write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-label="SEO Cow">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0a1a2a"/>
      <stop offset="55%" stop-color="#173f2a"/>
      <stop offset="100%" stop-color="#1b4a32"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#g)"/>
  <circle cx="980" cy="120" r="180" fill="#8bc53f" fill-opacity=".22"/>
  <circle cx="160" cy="520" r="220" fill="#2e7d32" fill-opacity=".25"/>
  <text x="80" y="290" font-family="Segoe UI, Arial, sans-serif" font-size="92" font-weight="800" fill="#ffffff">SEO <tspan fill="#8bc53f">Cow</tspan></text>
  <text x="80" y="370" font-family="Georgia, serif" font-size="36" fill="#c9e89a">ROI-driven search marketing from Elizabeth, NJ</text>
</svg>
""",
        encoding="utf-8",
    )

    (js_dir / "forms.js").write_text(
        """(function () {
  function buildBody(form) {
    var data = new FormData(form);
    var lines = [];
    data.forEach(function (value, key) {
      lines.push(key + ": " + value);
    });
    return lines.join("\\n");
  }

  document.querySelectorAll("form.lead-form").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;

      var subject = "SEO Cow inquiry";
      if (form.id === "audit-form") subject = "Free website audit request";
      if (form.id === "proposal-form") subject = "Proposal request";
      if (form.id === "contact-form") subject = "Contact request";

      var body = buildBody(form);
      var mailto =
        "mailto:info@seocow.com?subject=" +
        encodeURIComponent(subject) +
        "&body=" +
        encodeURIComponent(body);

      var success = form.parentElement.querySelector(".form-success");
      if (success) {
        success.hidden = false;
        success.style.display = "block";
      }
      window.location.href = mailto;
    });
  });
})();
""",
        encoding="utf-8",
    )

    (ROOT / "robots.txt").write_text(
        """User-agent: *
Allow: /

Sitemap: https://seocow.com/sitemap.xml
""",
        encoding="utf-8",
    )


def main() -> None:
    pages = sorted(ROOT.rglob("index.html"))
    # Ignore anything under scripts or .git
    pages = [p for p in pages if ".git" not in p.parts and "scripts" not in p.parts]
    if not pages:
        raise SystemExit("No pages found")

    home = ROOT / "index.html"
    write_assets(home.read_text(encoding="utf-8"))

    for page in pages:
        process_page(page, shared_css_written=True)

    # Verify
    remaining_banners = 0
    remaining_confirms = 0
    missing_h1 = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        if "demo-banner" in text:
            remaining_banners += 1
        if "[confirm" in text:
            remaining_confirms += 1
        if "<h1" not in text:
            missing_h1 += 1

    print(f"Processed {len(pages)} pages")
    print(f"Remaining demo banners: {remaining_banners}")
    print(f"Remaining [confirm]: {remaining_confirms}")
    print(f"Missing H1: {missing_h1}")


if __name__ == "__main__":
    main()
