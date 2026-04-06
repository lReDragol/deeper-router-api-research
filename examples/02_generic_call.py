#!/usr/bin/env python3
from pathlib import Path
import json
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from router_client import DeeperRouterClient

client = DeeperRouterClient(base_url="http://34.34.34.34", cookie_file=Path(__file__).resolve().parents[1] / "router_session.cookies")

# Uses existing cookie; login first if needed.
result = client.request("GET", "/api/security/blockedCounts")
print(json.dumps(result, ensure_ascii=False, indent=2))

# Example of blocked write call (safety):
try:
    client.safe_request("POST", "/api/admin/reboot", json_data={"confirm": True})
except Exception as e:
    print('write blocked by default:', e)
