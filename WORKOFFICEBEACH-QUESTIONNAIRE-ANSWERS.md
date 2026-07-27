# S1 Business Questionnaire - Work Office at the Beach Factory Pages

Home page and all factory pages share one chrome: staging banner, utility bar, logo/phone header, white top navigation, Services dropdown, About dropdown, Contact, Request a Tour, and highlighted Book a Tour CTA.

## A - Business identity
| Field | Value | Source |
|---|---|---|
| A1 brand | Work Office at the Beach | user-provided business facts |
| A2 domain | https://workofficeatthebeach.com [confirm] | user-provided business facts |
| A3 phone | (305) 555-0148 / tel:+13055550148 - demo staging number [confirm] | user-provided business facts |
| A4 email | hello@workofficeatthebeach.com [confirm] | user-provided business facts |
| A5 address | South Beach, Miami Beach, FL 33139 [confirm] - street TBD | user-provided business facts |
| A6 location | South Beach, Miami Beach, FL | user-provided business facts |
| A7 tagline | Work near the water. Enjoy the scenery. | user-provided business facts |
| A8 positioning | Coworking / beachside office space plus luxury condominiums and short-term rentals | user-provided business facts |
| A9 operator_note | Race Computer Services factory staging defaults where NAP unconfirmed | user-provided business facts |
| A10 tone | Inviting Miami Beach hospitality plus productive work; luxury without hype guarantees | user-provided business facts |

## B - Gate taxonomy
- Hubs: 7
- Hub landing pages: root-level `.html` pages to keep index count near 80
- SVC-CHILD pages: 70
- Hub slugs: beachside-coworking | private-offices-suites | meeting-rooms-events | beach-amenities-lifestyle | luxury-condo-residences | short-term-rentals | workcation-packages
- Full URL map: `WORKOFFICEBEACH-PAGE-INVENTORY.csv`

## C - Visual system
- Ocean teal `#0e7490`
- Deep sea `#0c4a6e`
- Sand cream `#f8f1e7`
- Warm sand-gold `#d4a373`
- Coral / sunset accent `#e11d48` used sparingly on highlighted form treatment
- Fonts: Fraunces headlines + Source Sans 3 body and navigation

## D - Forms and CTAs
- Primary CTA: `book-a-tour` (FORM-TOUR, highlighted)
- Secondary CTA: `request-a-tour` / Request a Stay
- Company/contact CTA: `contact`
- Form shells must be wired with owner-approved privacy, booking, rental, condo, tax, cancellation, and lead-routing language before public launch.

## E - Staging controls
- HTML uses `<meta name="robots" content="noindex,nofollow">`.
- `robots.txt` disallows all crawling.
- `netlify.toml` sends `X-Robots-Tag: noindex, nofollow`.
- Staging banner text: `STAGING PREVIEW — Work Office at the Beach factory build · South Beach Miami FL · content pending owner review`
- Netlify password protection: not requested; deploy should be public noindex staging.

## F - Confirmation flags
- Domain: https://workofficeatthebeach.com [confirm]
- Phone: (305) 555-0148 [confirm] / tel:+13055550148
- Email: hello@workofficeatthebeach.com [confirm]
- Address: South Beach, Miami Beach, FL 33139 [confirm] - street TBD
- Workspace inventory, condo details, short-term rental policies, taxes, fees, photos, amenities, and booking workflows: [confirm]
