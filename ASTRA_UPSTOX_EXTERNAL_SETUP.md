# ASTRA Upstox External Setup

Complete these once. After that ASTRA can continue automatically into sandbox validation.

## Required account setup
1. Have an active Upstox account.
2. Create an official Upstox developer app.
3. Configure the redirect URI.
4. Keep credentials only in environment variables or a secure secret store.
5. Never commit API secrets, OTPs, MPINs, access tokens or refresh tokens to GitHub.

Required environment names:
- UPSTOX_CLIENT_ID
- UPSTOX_CLIENT_SECRET
- UPSTOX_REDIRECT_URI

## Static IP
1. Provision one public static IPv4 address.
2. A secondary public static IPv4 is recommended for redundancy.
3. Register the allowed IP address(es) in the official broker flow.
4. Do not use private LAN addresses, localhost, or dynamically changing residential IPs.

## Authentication verification
After credentials and IPs are configured:
1. complete the official Upstox authentication flow,
2. verify read-only access first,
3. fetch account profile/funds,
4. fetch positions/orders,
5. run ASTRA startup reconciliation,
6. only then proceed to sandbox order lifecycle validation.

## Security policy
- No browser scraping.
- No unofficial credential capture.
- No plaintext secrets in repository files.
- No live-money order route during this setup.
- Automatic CI remains disabled unless explicitly re-enabled by the user.

## Completion condition
Phase 10B is complete only when credentials, static IP and read-only broker snapshots are verified.
