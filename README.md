# Little Bloom
Original, portable kids-resource website with parent/teacher accounts, 12 original downloadable PDFs and a coming-soon section for premium packs and Razorpay checkout.

## Run on your own host
Requires Node.js 22.13 or newer (built-in SQLite). Run `npm start` and open http://localhost:3000. No production npm packages are needed. Dev dependencies are only used to generate database migrations.

Accounts are stored in `data/accounts.sqlite`. Mount a persistent disk when deploying; ephemeral disk loses accounts. Set DATABASE_PATH to change the database location. Use HTTPS through a trusted reverse proxy. Set TRUST_PROXY=1 only if that proxy overwrites X-Forwarded-Proto. Password hashes use PBKDF2-SHA256 with a random salt; sessions use random tokens, server-side hashes and HttpOnly cookies. Authentication endpoints reject cross-origin writes and limit attempts.

PDFs live in private/downloads, outside the public folder. Server authorization is required for every download. Do not deploy public as a standalone static site: the account API and protected downloads need the backend.

## Hosted review copy
Uses a Worker with D1 for persistent accounts. `npm run build` packages the server, public assets and protected PDFs. The deployment workflow applies the generated Drizzle migration. Site access remains private for review.

## Included
- 12 resource PDFs: 2 stories, 2 coloring pages and 8 activities/learning sheets
- Search, category and age filters, story readers and worksheet previews
- Adult sign-up, sign-in, session restoration and sign-out
- Required sign-in before PDF downloads
- Coming soon: premium activity packs, personalized stories, seasonal collections

## Razorpay status
Checkout is intentionally coming soon. The current sample PDFs remain free after sign-up. There is no live or test payment integration yet. Configure your merchant account and choose products/prices before implementation. Never put the Razorpay secret in browser code. A real checkout must create orders on the server, verify signatures and confirmed payment status, and grant entitlements server-side. Environment variable names in .env.example are placeholders, not active code.

## Before public launch
Replace the temporary brand, add business contact details and finalized privacy/terms, and add email verification and password recovery using your selected email service. Those email workflows are not enabled in this version. Accounts are restricted to parents, guardians or teachers aged 18 or above; do not ask children to register. Fonts load from Google Fonts; self-host them if preferred.

## Checks
`npm run check`, `node check-ui.cjs` and `node check-auth.mjs` validate syntax, resource readers/filters and auth/session behavior. Browser visual QA was unavailable in the authoring environment.

## PDFs
Already included. To regenerate, install Python reportlab and Pillow, then run `python generate_samples.py` and `python generate_extra.py`. Source artwork is original. Two story PDFs reuse decorative garden artwork rather than scene-specific images.

## Monthly subscription packages
Proposed INR plans: Little Sprout INR 199/month (10 premium PDFs), Growing Bloom INR 299/month (25 premium PDFs), Wonder Garden INR 399/month (unlimited premium PDFs). Prices are stored in paise in public/plans.js. All plans are coming soon. The 12 existing free samples remain free after registration. Choosing a plan persists an account preference only; it does not create a paid subscription or grant premium access.

GET /api/plans returns the catalog. POST /api/plan-selection saves the signed-in user's valid plan preference. A production subscription integration still needs Razorpay plan/subscription creation, signed webhooks, subscription state and entitlements, download-quota enforcement and cancellation management. No recurring charges are initiated by this version.
# LittleBloomKids
