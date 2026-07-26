# S1 Business Questionnaire - AHB Factory Pages

Home page and factory pages share one chrome: utility bar, AHB logo/phone, Services dropdown, About dropdown, Contact, and highlighted Schedule a Call CTA.

## A - Business identity
| Field | Value | Source |
|---|---|---|
| A1 legal_name | Abner Herrman & Brock LLC | user-provided business facts |
| A2 brand | AHB / Abner Herrman & Brock | user-provided business facts |
| A3 domain | https://ahbi.com | user-provided business facts |
| A4 phone | (201) 484-2000 / tel:+12014842000 | user-provided business facts |
| A5 email | info@ahbi.com | user-provided business facts |
| A6 address | Harborside 5, 185 Hudson Street, Suite 1640, Jersey City, NJ 07311 | user-provided business facts |
| A7 HQ | Jersey City, NJ (Harborside) | user-provided business facts |
| A8 founded | 1981 | user-provided business facts |
| A9 trade | Investment management / separately managed accounts (SMAs) | user-provided business facts |
| A10 differentiator | Actively managed customized SMAs; individual stocks and bonds; Investment Policy Committee team approach; tax-efficient transitions; nationwide via wrap platforms | user-provided business facts |

## B - Public site claims to confirm
- Cited from ahbi.com as of Mar 31, 2026:
  - ~$3B AUM
  - 4 strategies
  - $250K minimum account size
  - ~30 average years industry experience
- These require owner/compliance confirmation before publication. [confirm]

## C - Core strategies
- Large-Cap Core Equity
- Taxable Bond
- Municipal Bond
- Core Balanced

## D - Audiences served
- Financial advisors
- High-net-worth individuals and families
- Nonprofits and corporations

## E - Gate 1 taxonomy
- Hubs: 10
- SVC-CHILD pages: 100
- Hub slugs: core-equity-sma | taxable-bond-portfolios | municipal-bond-strategies | core-balanced-solutions | separately-managed-accounts | financial-advisor-solutions | high-net-worth-wealth-management | institutional-nonprofit-portfolios | tax-efficient-portfolio-management | portfolio-review-transition-services
- Full URL map: `AHBI-PAGE-INVENTORY.csv`

## F - Forms and CTAs
- Primary CTA: `schedule-a-call` (FORM-CONSULT)
- Secondary CTA: `request-a-proposal`
- Company/contact CTA: `contact`
- Form shells must be wired with AHB-approved privacy, retention, and compliance language before public use.

## G - Staging and compliance
- HTML uses `<meta name="robots" content="noindex,nofollow">`.
- `robots.txt` disallows all crawling.
- `netlify.toml` sends `X-Robots-Tag: noindex, nofollow`.
- Every footer includes SEC registration, past performance, and Form CRS / ADV Part 2A conceptual disclosure text.
- No performance returns, rankings, or testimonials are invented.
