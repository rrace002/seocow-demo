# Online Psychiatrists Factory Build Notes

- Branch: `cursor/online-psychiatrists-factory-127e`
- Domain target: https://www.onlinepsychiatrists.com
- Build type: NearMe OS Website Factory Gate 1 staging preview
- Page model: 10 service hubs x 10 children = 100 SVC-CHILD pages
- Generated `index.html` pages expected: 117
- Inventory URLs expected: 117
- Staging controls: HTML noindex,nofollow; robots.txt `Disallow: /`; Netlify `X-Robots-Tag: noindex, nofollow`
- Banner: `STAGING PREVIEW — onlinepsychiatrists.com factory build · Dr. Zlatin Ivanov / Online Psychiatrists · content pending owner review · not the live website`
- Visual direction: calm clinical telehealth, deep teal `#0f4c5c`, soft clinical navy `#1e3a5f`, sage `#7d9b8a`, warm off-white `#f7f6f2`, restrained gold accent `#b78b3a`
- Fonts: Fraunces for headlines and Source Sans 3 for interface/body
- Navigation: shared chrome on all pages; dropdown links use dark text on white backgrounds via `nav.nav .dd a`
- CTA language: Schedule a Visit / Request a Consultation / Contact
- Medical and crisis disclaimers appear in every footer. Crisis text: `This is not a crisis service. If you are in crisis, call 988 or go to the nearest emergency room.`
- Credential, rating, service area, HIPAA, Ryan Haight, and Superbill references are marked for confirmation. [confirm]
