# Deeper Router API Research Toolkit

Reverse-engineered documentation, extracted frontend artifacts, sample responses, and Python tooling for exploring the local web API exposed by Deeper routers at `http://34.34.34.34`.

This is useful if you want to understand undocumented endpoints, automate router tasks, inspect what the web UI is doing, or build your own scripts and dashboards on top of the router API.

## What this project can do

- Map the router's internal HTTP API from the shipped frontend bundle.
- Show which endpoints are read-only, write-capable, or higher-risk.
- Log in from Python and reuse the router's cookie-based session.
- Call endpoints directly from a CLI instead of the web UI.
- Provide sanitized sample responses for offline analysis and tooling development.
- Offer a PySide6 desktop utility for experimenting with tunnel selection / optimization.

## Repository contents

- `ROUTER_API_FULL.md` - human-readable endpoint reference grouped by category.
- `router_api_catalog.json` - machine-readable catalog with methods, risk tags, payload hints, sources, and probe results.
- `router_api_openapi_like.json` - OpenAPI-like export for automation or code generation experiments.
- `router_api_calls_catalog.json` - extracted call inventory from the frontend bundle.
- `router_client.py` - Python API client and CLI.
- `deeper_optimizer_ui/deeper_optimizer.py` - desktop GUI for tunnel-focused workflows.
- `examples/` - minimal CLI usage examples.
- `samples/` - sanitized example JSON responses from successful GET endpoints.
- `raw_router/` - downloaded frontend bundle plus extraction artifacts used to build the catalogs.

## Typical use cases

- Reverse engineering the Deeper web interface without repeatedly clicking through the UI.
- Building custom automation for status checks, diagnostics, or configuration export.
- Auditing undocumented endpoints before deciding what is safe to call.
- Comparing firmware / frontend versions to spot new API surface.
- Prototyping third-party integrations around DPN, sharing, Wi-Fi, traffic, or system-info endpoints.

## Safety notes

- This is not an official SDK.
- Write endpoints can change router state, interrupt connectivity, or reboot the device.
- `router_client.py` blocks write methods by default unless `--allow-write` is passed.
- Login uses RSA-OAEP encrypted password exchange, matching the frontend behavior.
- Session cookies are stored locally in `router_session.cookies`, which is intentionally excluded from git.
- Sample files in this repository were sanitized before publication; no live auth cookies or real device identifiers are included.

## Quick start

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Login and store a local session cookie:

```bash
python router_client.py login --username <USERNAME> --password <PASSWORD>
```

List all discovered endpoints:

```bash
python router_client.py list --catalog router_api_catalog.json
```

Call a read endpoint:

```bash
python router_client.py call GET /api/info
```

Call a write endpoint explicitly:

```bash
python router_client.py call POST /api/admin/reboot --json "{\"confirm\": true}" --allow-write
```

Run the GUI utility:

```bash
python -m pip install PySide6
python deeper_optimizer_ui/deeper_optimizer.py
```

## Project structure for researchers

- `raw_router/index.gHG1NCGy.js` and `raw_router/assets_full/` are the original frontend assets.
- `raw_router/extracted_endpoints*.json` and `raw_router/extracted_calls_with_payloads.json` are extraction artifacts derived from those assets.
- `router_get_probe_results.json` records authenticated GET probe outcomes used to populate the sample catalog.
- `samples_index.json` maps endpoint paths to sample files and top-level keys.

## Limitations

- The API surface may vary across hardware revisions and firmware versions.
- Some endpoints require authentication, wallet unlock state, or specific router features to be enabled.
- Frontend extraction identifies likely behavior, but a few payload shapes may still need manual verification on-device.

## License

- Original code and documentation in this repository are released under the MIT license.
- Downloaded vendor/frontend assets kept for research in `raw_router/assets_full/` and `raw_router/index.*` are excluded from that grant and remain under their original terms.
