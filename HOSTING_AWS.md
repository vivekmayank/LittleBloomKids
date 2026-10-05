# Hosting LittleBloomKids on AWS

LittleBloomKids is currently a Node.js website with:

- a custom `server.js` backend
- `/api/*` account endpoints
- protected `/downloads/*` PDF access
- SQLite account storage in `data/accounts.sqlite`

Because of this, do not deploy only the `public` folder as a static Amplify site unless you intentionally want to disable login and protected downloads.

## Recommended AWS option: App Runner

Use AWS App Runner for the fastest production-style deployment from GitHub.

### 1. Create the App Runner service

1. Open AWS Console.
2. Search for **App Runner**.
3. Choose **Create service**.
4. Source: **Source code repository**.
5. Connect GitHub and select:
   - Repository: `vivekmayank/LittleBloomKids`
   - Branch: `main`
6. Deployment trigger: **Automatic**.

### 2. Build settings

Use these settings:

- Runtime: **Node.js 22**
- Build command: `npm ci`
- Start command: `npm start`
- Port: `3000`

Add environment variables:

```text
PORT=3000
TRUST_PROXY=1
DATABASE_PATH=/app/data/accounts.sqlite
```

Important: App Runner file storage is not ideal for long-term SQLite persistence. For a real public launch, move accounts/subscriptions to a managed database such as DynamoDB, RDS PostgreSQL, or Aurora Serverless.

## Domain: littlebloom-kids.com from GoDaddy

After App Runner deploys, it gives a default AWS URL. Then:

1. Open the App Runner service.
2. Go to **Custom domains**.
3. Add:
   - `littlebloom-kids.com`
   - `www.littlebloom-kids.com`
4. AWS will show DNS records to create.
5. Open GoDaddy DNS for `littlebloom-kids.com`.
6. Add the exact records AWS gives you.
7. Wait for validation and SSL certificate creation.

Typical DNS shape:

```text
www  CNAME  <aws-app-runner-domain>
@    A/ALIAS or GoDaddy forwarding depending on the AWS record shown
```

Always copy the exact records shown by AWS App Runner, because AWS may generate unique validation records.

## If you still want AWS Amplify

Amplify can host the public frontend, but this repo is not currently a pure static site. A direct static Amplify setup would break:

- sign up
- sign in
- saved plan selection
- protected PDF downloads

To use Amplify properly, convert the backend to AWS services:

- Amplify Hosting for frontend
- API Gateway + Lambda for `/api/*`
- DynamoDB for accounts and sessions
- S3 private bucket for PDFs
- CloudFront signed URLs or Lambda authorization for downloads
- Razorpay webhooks handled by Lambda

That is a bigger but more scalable architecture.

## Lowest-cost practical path

For the current code, start with App Runner or a small EC2/Lightsail instance. Once Razorpay and subscriptions are live, move account and payment state to DynamoDB or PostgreSQL before spending on ads or public launch traffic.
