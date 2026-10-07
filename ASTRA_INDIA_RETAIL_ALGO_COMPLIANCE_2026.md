# ASTRA India Retail Algo Compliance Snapshot — 2026-10-08

Status: current research snapshot for design gating. Re-verify again before any live activation.

## Current applicability

SEBI's retail algo framework, together with exchange implementation standards and operational modalities, applies to all stock brokers from 1 April 2026.

Primary references:
- SEBI circular timeline extension dated 30 September 2025
- NSE Implementation Standards for safer participation of retail investors in Algorithmic trading
- NSE Client Direct API / Member Frontend guidance updated in 2026

## Static IP

For client API access, NSE implementation standards require the client to provide a static IP address mapped to API keys.

The standards allow:
- one primary static IP
- an additional secondary static IP for redundancy
- multiple API keys, subject to mapping rules

Static-IP changes are controlled and not intended to rotate dynamically.

ASTRA therefore must not assume consumer/dynamic-IP execution is production compliant.

## Daily session handling

API sessions must be logged out before the next trading day.

ASTRA production design therefore requires:
- explicit daily session lifecycle
- startup authentication
- broker-state reconciliation
- no assumption that a prior-day session remains valid

## Algo tagging / threshold

NSE audit guidance states that API-originated client algos below the exchange-defined threshold are still tagged as Algo using the generic algo identifier.

Client-developed algos above the defined Threshold Orders Per Second require exchange registration and a unique algo ID.

ASTRA must therefore:
- keep order-rate limiting
- retain audit tags/metadata
- never attempt to bypass exchange/broker tagging
- treat high-OPS operation as a separate registered deployment class

## Broker/cloud responsibilities

NSE audit guidance distinguishes client-developed, broker-generated and algo-provider systems, including hosting/static-IP obligations.

ASTRA must use only a broker/API path that explicitly supports the intended retail client-direct API deployment.

## Current deployment implication

Before LIMITED_LIVE can be considered, all of these must be true:

1. Broker explicitly supports compliant retail algo/API access.
2. Required API permissions are enabled for the user's account.
3. Static primary/secondary IP requirements are satisfied.
4. Daily API-session lifecycle is implemented.
5. Broker/exchange order tagging requirements are met.
6. Order-rate limits stay below the applicable unregistered threshold unless the strategy has completed required registration.
7. Startup and continuous reconciliation are proven in shadow/paper tests.
8. Kill switch and block-new-risk controls are tested.
9. CI, secret scanning and dependency auditing pass.
10. Exact broker/exchange rules are re-verified immediately before activation.

## Sources checked

- SEBI: Extension of timeline for implementation of the 4-Feb-2025 retail algo circular, 30-Sep-2025.
- NSE circular INVG67858: Implementation Standards for safer participation of retail investors in Algorithmic trading.
- NSE Client Direct API / Decision Support Tools pages updated in 2026.
- NSE inspection/audit guidance covering static-IP whitelisting, retail algo hosting and generic/unique algo IDs.

## Safety rule

This document is not authorization to trade.

ASTRA LIVE remains disabled until external broker readiness, infrastructure requirements and all promotion evidence are satisfied.
