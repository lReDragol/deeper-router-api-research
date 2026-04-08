# Toolkit Roadmap

This file tracks the planned companion tool and optional telemetry service around the documented Deeper router API. No collector binaries or telemetry client code are published in this repository yet.

## Current Scope

- Keep this repository documentation-first.
- Publish API research, sanitized samples, and future implementation notes separately from local experimental tooling.
- Do not publish tray collectors, background telemetry, or state-changing automation until the safety model is finished.

## Local Companion Tool

- Add a stable `top-10` tunnel view based on the latest completed measurement run, not blended lifetime averages.
- Keep full-tunnel scans and quick scans separate, with clear labeling of what was actually measured.
- Support adding tunnels from known presets and manual `regionCode + countryCode`.
- Support deleting tunnels with automatic migration of affected domain rules before tunnel removal.
- Add restore-bundle import with a dry-run preview before any router changes are applied.
- Always save a local rollback snapshot before state-changing actions.

## Background Collector

- Add an opt-in tray mode that starts with Windows and runs minimized.
- Prefer Windows Task Scheduler for autostart over a raw `Run` key.
- Keep collector state in a local SQLite queue, not in volatile JSON files.
- Run light measurements frequently and deeper scans less often, with backoff and cooldown.
- Upload batched statistics every 6 hours.
- Never upload auth cookies, plaintext credentials, or raw browsing history.
- Make domain-level telemetry opt-in and disabled by default.

## Telemetry Payload

- Primary payload: tunnel code, region, country, active IP, measured Mbps, latency, score, scan mode, firmware, timestamp, and app version.
- Include local batch ids and sequence numbers so the server can deduplicate uploads.
- Include a client installation id that is separate from the router device id.
- Bind uploads to the router by device id on the server side, but avoid storing raw device ids long-term.

## Device Binding

- During first enrollment, read the router `deviceId` from the local API over the user-approved local session.
- Send the raw `deviceId` only during enrollment over HTTPS.
- On the server, replace the raw value with a salted one-way hash and discard the raw identifier after binding.
- Allow multiple client installations to map to the same bound router record.
- Expose only the salted router binding id in later APIs and restore bundles.

## Enrollment And Auth

- Generate an Ed25519 keypair locally on first install.
- Register the public key with the server during enrollment.
- Require a short-lived enrollment token issued from the website before the collector can start uploading.
- Make enrollment tokens one-time-use and short-lived.
- Sign every upload payload locally with the private key.
- Reject uploads with invalid signatures, bad timestamps, reused idempotency keys, or non-monotonic sequence numbers.

## Anti-Abuse Model

- Accept telemetry only from enrolled clients with registered public keys.
- Put the API behind HTTPS and a reverse proxy with strict request size limits.
- Rate-limit by client id and by source IP.
- Add jitter and exponential backoff on the client.
- Require idempotency keys on upload requests.
- Use a website-side CAPTCHA or equivalent human gate for enrollment, not for every upload.
- Log failed verification attempts and auto-ban noisy sources.

## Privacy Defaults

- Default upload set should be tunnel performance only.
- Do not upload whitelist domains, app lists, or `inform` browsing-like activity by default.
- If domain intelligence is ever added, send it only after explicit opt-in and document it clearly.
- Strip or hash any data that could reveal personal network structure unless absolutely required.

## Server Stack

- Verified on April 8, 2026 via SSH:
- Target host: `server-X99`
- OS: Ubuntu `24.04.4 LTS`
- Docker: `29.3.0`
- Docker Compose: `v5.1.0`
- Planned stack:
- Reverse proxy with HTTPS termination
- API service for enrollment, upload, restore bundles, and signed recommendations
- PostgreSQL for telemetry and router binding data
- Redis for rate limiting, job queues, and short-lived replay protection
- Optional worker service for aggregation and recommendation generation

## Suggested Services

- `proxy`: Caddy or Nginx with TLS, request size limits, and per-route rate limits.
- `api`: FastAPI service for enrollment, upload, bundle download, and recommendation APIs.
- `worker`: background jobs for aggregation, top tunnel generation, and future routing recommendations.
- `postgres`: primary relational store.
- `redis`: replay cache, rate-limit counters, and queue coordination.

## Database Shape

- `installations`: installation id, public key, router binding id, created at, last seen, status.
- `routers`: salted router binding id, firmware family, first seen, last seen.
- `upload_batches`: installation id, sequence number, idempotency key, received at, payload hash.
- `tunnel_measurements`: installation id, router binding id, timestamp, tunnel code, region, country, IP, Mbps, latency, score, scan mode.
- `restore_bundles`: bundle id, target scope, payload json, signature, expiry, created at.
- `recommendation_plans`: plan id, target scope, rollout policy, status, created at.

## Restore Bundle Format

- Provide downloadable signed bundle files from the website.
- Bundle should include:
- bundle id
- issued at
- expires at
- target router binding id or target scope
- tunnel candidates
- fallback tunnel order
- smart-route rules to restore
- signature over the canonical payload
- The local app must verify the signature before import.
- Import flow must be:
- preview
- add missing tunnels
- test candidate tunnels
- switch domain rules
- verify connectivity
- rollback automatically on failure

## Config Recovery Goal

- Main recovery use case: a user loses working IPs inside configured tunnels and cannot bootstrap normal routing again.
- The website should provide fresh signed tunnel candidates that are known to be alive.
- The local tool should import the signed file, rebuild at least a minimal tunnel set, and then restore domain routing on top of that.
- Recovery must work without requiring the user to hand-edit router API requests.

## Future Network Coordination

- Phase 1: read-only recommendations only.
- Phase 2: opt-in background rebalancing with strict cooldowns and rollback.
- Phase 3: region-aware load shaping that spreads domains across healthy tunnels without visible user disruption.
- Recommendations should move traffic gradually, never all at once.
- Keep policy conservative:
- prefer same-region moves first
- avoid churn for stable domains
- cap the number of domain migrations per cycle
- record the previous plan so rollback is always possible

## Implementation Order

- Finalize measurement parity between the local app and browser-side experiments.
- Finish local tunnel management and restore-bundle import UX.
- Implement tray mode and local queueing without any server dependency.
- Stand up the Docker stack on the server.
- Implement enrollment, signatures, idempotent uploads, and rate limiting.
- Add server-side aggregation and a simple internal dashboard.
- Only then publish the collector to outside users.
