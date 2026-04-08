# Deeper Router API Research

Reverse-engineered API documentation and extraction artifacts for the local web interface exposed by Deeper routers at `http://34.34.34.34`.

This repository is intentionally documentation-only. It focuses on the discovered API surface, extracted frontend evidence, and sanitized sample responses.

A separate roadmap for the not-yet-published local companion tool, restore workflow, and optional telemetry backend is tracked in `TODO.md`.

## Current coverage

- `145` discovered API paths
- `156` method operations
- live authenticated read probes for the most relevant GET endpoints
- second-pass recovery of endpoints hidden behind dynamic path composition

## What is here

- `ROUTER_API_FULL.md` - human-readable reference grouped by category
- `router_api_catalog.json` - machine-readable catalog with methods, risk tags, source bundles, probe results, and notes
- `router_api_openapi_like.json` - OpenAPI-like export for automation and code generation experiments
- `router_api_calls_catalog.json` - extracted frontend call inventory
- `router_get_probe_results.json` - authenticated GET probe outputs used during cataloging
- `samples/` - sanitized example responses for successful GET endpoints
- `samples_index.json` - mapping between endpoint paths and sample files
- `raw_router/` - downloaded frontend assets and intermediate extraction artifacts
- `TODO.md` - roadmap for the planned local toolkit, restore bundles, and telemetry service

## Notable findings in this update

- additional endpoints were recovered from dynamically composed frontend paths, especially under `/api/security/*`
- extra routes were confirmed for `notifications`, `admin/downloadLog`, `admin/language`, `tproxy/rootCaCert`, `smartRoute` exports, and extended `sharingSecurity` date-range queries
- one raw extraction false positive was identified: `/api/wifi/getAPConfig request filed` is a frontend error string, not a real API path

## How to read the repo

- start with `ROUTER_API_FULL.md` if you want a quick category-by-category overview
- use `router_api_catalog.json` if you need structured metadata, source bundle references, or probe notes
- use `router_api_openapi_like.json` if you want to feed the catalog into tooling
- use `raw_router/` when you need to verify how a path was inferred from the shipped frontend

## Notes

- this is not an official SDK
- write-capable endpoints are documented, but many of them can change router state, interrupt connectivity, or reboot the device
- sample files were sanitized before publication; no live auth cookies or real device identifiers are included
- the API surface can differ across firmware versions and hardware revisions

## License

- Original documentation in this repository is released under the MIT license.
- Downloaded vendor/frontend assets kept for research in `raw_router/assets_full/` and `raw_router/index.*` are excluded from that grant and remain under their original terms.
