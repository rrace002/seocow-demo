# S1 Business Questionnaire - San Diego Tech Support Factory Pages

Home page and all factory pages share one chrome: staging banner, utility bar, logo/phone header, Services dropdown, About dropdown, Contact, Request a Proposal, and highlighted Schedule a Consultation CTA.

## A - Business identity
| Field | Value | Source |
|---|---|---|
| A1 brand | San Diego Tech Support | user-provided business facts |
| A2 parent / affiliated | Race Computer Services (racecs.com) | public-site facts; confirm wording [confirm] |
| A3 related affiliate | Pop Quiz Computers | user-provided; confirm as needed [confirm] |
| A4 domain | https://www.san-diegotechsupport.com | user-provided business facts |
| A5 primary_phone | (619) 478-0455 / tel:+16194780455 | homepage title / user-provided facts |
| A6 alternate_phone | (619) 536-1986 / tel:+16195361986 | site/LinkedIn listing; confirm [confirm] |
| A7 email | support@san-diegotechsupport.com | user-provided business facts |
| A8 address | 310 3rd Ave, Chula Vista, CA 91911 | schema uses 91911; some listings show 91910; use 91911 with confirmation [confirm] |
| A9 service_area | San Diego County and Southern California | user-provided business facts [confirm] |
| A10 positioning | Local managed IT, IT consulting, cloud, cybersecurity, and compliance support for small businesses and growing organizations across Southern California. | user-provided business facts [confirm] |

## B - Gate 1 taxonomy
- Hubs: 10
- SVC-CHILD pages: 100
- Total generated `index.html` pages: 117
- Hub slugs: managed-it-services | small-business-it-support | cybersecurity-services | compliance-services | managed-cybersecurity | managed-cloud-services | data-center-cloud | enterprise-it-solutions | microsoft-platforms-support | industries-we-serve
- Full URL map: `PAGE-INVENTORY.csv`

## C - Platform and compliance topics to confirm
- Microsoft 365 and Windows Server
- Cloud backup and disaster recovery
- Firewall and endpoint security
- AWS, Google Cloud, and private cloud
- Cisco, Dell, HPE, Linux, Unix, Apple Mac
- HIPAA, PCI-DSS, CMMC, NIST 800-171, and MIPS topics

## D - Claims to confirm
- Microsoft partner positioning from public site/navigation. [confirm]
- Parent / affiliated relationship with Race Computer Services. [confirm]
- Affiliation with Pop Quiz Computers. [confirm]
- Address ZIP 91911 vs occasional listing differences. [confirm]
- Pricing and service quality claims. [confirm]
- Cybersecurity and compliance service scope; no legal, breach-prevention, or certification guarantees.

## E - Forms and CTAs
- Primary CTA: `schedule-a-consultation` (highlighted)
- Secondary CTA: `request-a-proposal`
- Company/contact CTA: `contact`
- Form shells must be wired with owner-approved privacy, spam protection, CRM/ticket routing, scheduling, response expectations, and follow-up language before public launch.

## F - Staging and compliance
- HTML uses `<meta name="robots" content="noindex,nofollow">`.
- `robots.txt` disallows all crawling.
- `netlify.toml` sends `X-Robots-Tag: noindex, nofollow`.
- Staging banner text: `STAGING PREVIEW — san-diegotechsupport.com factory build · San Diego Tech Support · content pending owner review · not the live website`
- No testimonials, awards, rankings, client logos, certifications, or guaranteed outcomes are invented.
