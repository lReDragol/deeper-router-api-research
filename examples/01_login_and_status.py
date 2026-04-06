#!/usr/bin/env python3
from pathlib import Path
import json
import os
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from router_client import DeeperRouterClient

client = DeeperRouterClient(base_url="http://34.34.34.34", cookie_file=Path(__file__).resolve().parents[1] / "router_session.cookies")
username = os.environ.get("DEEPER_USER", "admin")
password = os.environ.get("DEEPER_PASSWORD")

if not password:
    raise SystemExit("Set DEEPER_PASSWORD before running this example. Optional: set DEEPER_USER as well.")

print('login...')
print(client.login(username, password))
print('validate token...')
print(client.validate_token())

for path in [
    "/api/admin/getDeviceId",
    "/api/info",
    "/api/dynamic-data",
    "/api/system-info/software-info",
    "/api/system-info/hardware-info",
]:
    out = client.request("GET", path)
    print(path, '->', out['status'])
    print(json.dumps(out['body'], ensure_ascii=False, indent=2)[:1200])
