#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from http.cookiejar import MozillaCookieJar

import requests

PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxZ9YwQ1CVM4zNHVNPxoD
Sz6uFGEcyHUOFkoA2hnijjJccCNRGnYlQmnCmaKPtCPiJ26ibXcL9BpfputJpE7Q
cJcJx8CN0Pr/MceYQraFS3UG+zNdI6tGzLDGrBoB+5WFSbK6aOdHFJfcoBfdULHb
g2eGp2IJwSPal3lFNwE/oTL3K1z7EiwbDq0LrY7FcwMGmG3EFaGtMxRy/cq3r0xR
M1V7WIu1I6gw463luLs6NFCdrY/fiXoSrXRf6sOTZClXeRhKjA6c0wLIxizgw6ll
4EeffYVBQSKlEjJJR2y7cxxbp1XkC19evxe0DYbnsemogDcSkmDCj75hsgwuzoTM
FwIDAQAB
-----END PUBLIC KEY-----
"""


class DeeperRouterClient:
    def __init__(self, base_url: str = "http://34.34.34.34", cookie_file: str | Path = "router_session.cookies"):
        self.base_url = base_url.rstrip("/")
        self.cookie_file = Path(cookie_file)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
            }
        )
        self.session.cookies = MozillaCookieJar(str(self.cookie_file))
        self._load_cookies()

    def _load_cookies(self):
        if self.cookie_file.exists():
            try:
                self.session.cookies.load(ignore_discard=True, ignore_expires=True)
            except Exception:
                pass

    def _save_cookies(self):
        self.cookie_file.parent.mkdir(parents=True, exist_ok=True)
        self.session.cookies.save(ignore_discard=True, ignore_expires=True)

    def _encrypt_password(self, password: str) -> str:
        # Preferred path: Python cryptography package.
        try:
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import padding

            public_key = serialization.load_pem_public_key(PUBLIC_KEY_PEM.encode("utf-8"))
            encrypted = public_key.encrypt(
                password.encode("utf-8"),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None,
                ),
            )
            import base64

            return base64.b64encode(encrypted).decode("ascii")
        except Exception:
            pass

        # Fallback: Node.js crypto.publicEncrypt, matches frontend behavior.
        node_script = """
const crypto=require('crypto');
const key=process.argv[1];
const pwd=process.argv[2];
const out=crypto.publicEncrypt(key, Buffer.from(pwd)).toString('base64');
process.stdout.write(out);
"""
        try:
            proc = subprocess.run(
                ["node", "-e", node_script, PUBLIC_KEY_PEM, password],
                check=True,
                capture_output=True,
                text=True,
            )
            return proc.stdout.strip()
        except Exception as exc:
            raise RuntimeError(
                "Failed to encrypt password. Install 'cryptography' or ensure node is available."
            ) from exc

    def login(self, username: str = "admin", password: str = "admin") -> dict:
        encrypted = self._encrypt_password(password)
        payload = {"username": username, "password": encrypted}
        resp = self.session.post(f"{self.base_url}/api/admin/login", json=payload, timeout=20)
        resp.raise_for_status()
        self._save_cookies()
        return resp.json()

    def validate_token(self) -> dict:
        resp = self.session.post(f"{self.base_url}/api/admin/validateToken", timeout=20)
        resp.raise_for_status()
        return resp.json()

    def request(self, method: str, path: str, params=None, json_data=None, data=None, timeout: int = 30):
        m = method.upper()
        if not path.startswith("/"):
            path = "/" + path
        url = f"{self.base_url}{path}"
        resp = self.session.request(m, url, params=params, json=json_data, data=data, timeout=timeout)
        ctype = resp.headers.get("Content-Type", "")
        if "application/json" in ctype or resp.text[:1] in "[{":
            try:
                body = resp.json()
            except Exception:
                body = resp.text
        else:
            body = resp.text
        return {"status": resp.status_code, "headers": dict(resp.headers), "body": body}

    def safe_request(self, method: str, path: str, *, allow_write: bool = False, **kwargs):
        write_methods = {"POST", "PUT", "PATCH", "DELETE"}
        if method.upper() in write_methods and not allow_write:
            raise PermissionError(
                "Write request is blocked by default. Pass allow_write=True to execute state-changing calls."
            )
        return self.request(method, path, **kwargs)


def _load_catalog(catalog_path: Path):
    if not catalog_path.exists():
        return []
    try:
        return json.loads(catalog_path.read_text(encoding="utf-8"))
    except Exception:
        return []


def cmd_list(args):
    catalog = _load_catalog(Path(args.catalog))
    if not catalog:
        print("Catalog is empty or missing:", args.catalog)
        return
    for item in catalog:
        methods = ",".join(sorted(item.get("methods", {}).keys()))
        print(f"{methods:20} {item.get('risk',''):14} {item['path']}")


def cmd_login(args):
    client = DeeperRouterClient(base_url=args.base_url, cookie_file=args.cookie_file)
    out = client.login(args.username, args.password)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    try:
        v = client.validate_token()
        print("validateToken:", json.dumps(v, ensure_ascii=False))
    except Exception as exc:
        print("validateToken failed:", exc)


def cmd_call(args):
    client = DeeperRouterClient(base_url=args.base_url, cookie_file=args.cookie_file)
    params = json.loads(args.params) if args.params else None
    body = json.loads(args.json) if args.json else None
    out = client.safe_request(
        args.method,
        args.path,
        allow_write=args.allow_write,
        params=params,
        json_data=body,
        timeout=args.timeout,
    )
    print(json.dumps(out, ensure_ascii=False, indent=2))


def build_parser():
    p = argparse.ArgumentParser(description="Deeper Router API client")
    p.add_argument("--base-url", default="http://34.34.34.34", help="Router base URL")
    p.add_argument("--cookie-file", default="router_session.cookies", help="Cookie jar file")

    sub = p.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("list", help="List endpoints from catalog")
    s1.add_argument("--catalog", default="router_api_catalog.json")
    s1.set_defaults(func=cmd_list)

    s2 = sub.add_parser("login", help="Login and save session cookies")
    s2.add_argument("--username", default="admin")
    s2.add_argument("--password", default="admin")
    s2.set_defaults(func=cmd_login)

    s3 = sub.add_parser("call", help="Call API endpoint")
    s3.add_argument("method", help="HTTP method")
    s3.add_argument("path", help="API path, e.g. /api/info")
    s3.add_argument("--params", help='JSON query params, e.g. {"pageNo":1,"pageSize":20}')
    s3.add_argument("--json", help='JSON request body, e.g. {"value":true}')
    s3.add_argument("--allow-write", action="store_true", help="Allow non-GET calls")
    s3.add_argument("--timeout", type=int, default=30)
    s3.set_defaults(func=cmd_call)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
