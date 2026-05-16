#!/usr/bin/env python3
"""
Gridiron Index member login server.

This keeps the coaching archive JSON off the public HTML page and returns it
only after a successful member login. It is intentionally dependency-light so
it can run in the deployment sandbox with Python's standard library.
"""

from __future__ import annotations

import json
import mimetypes
import os
import secrets
import time
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent
ARCHIVE_PATH = ROOT / "archive-data.json"

MEMBER_EMAIL = os.environ.get("GI_MEMBER_EMAIL", "member@gridironindex.com").strip().lower()
MEMBER_PASSWORD = os.environ.get("GI_MEMBER_PASSWORD", "GI-MAY-2026")
TOKEN_TTL_SECONDS = int(os.environ.get("GI_TOKEN_TTL_SECONDS", str(60 * 60 * 8)))

TOKENS: dict[str, float] = {}


def json_response(handler: SimpleHTTPRequestHandler, status: int, payload: dict[str, Any]) -> None:
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def read_json_body(handler: SimpleHTTPRequestHandler) -> dict[str, Any]:
    raw_len = handler.headers.get("Content-Length", "0")
    try:
        length = min(int(raw_len), 10_000)
    except ValueError:
        length = 0
    if length <= 0:
        return {}
    raw = handler.rfile.read(length)
    try:
        parsed = json.loads(raw.decode("utf-8"))
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def valid_token(handler: SimpleHTTPRequestHandler) -> bool:
    auth = handler.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return False
    token = auth.removeprefix("Bearer ").strip()
    expires_at = TOKENS.get(token)
    if not expires_at:
        return False
    if expires_at < time.time():
        TOKENS.pop(token, None)
        return False
    return True


class Handler(SimpleHTTPRequestHandler):
    server_version = "GridironIndex/1.0"

    def end_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()

    def do_POST(self) -> None:
        if self.path == "/api/login":
            data = read_json_body(self)
            email = str(data.get("email", "")).strip().lower()
            password = str(data.get("password", ""))
            if email == MEMBER_EMAIL and secrets.compare_digest(password, MEMBER_PASSWORD):
                token = secrets.token_urlsafe(32)
                TOKENS[token] = time.time() + TOKEN_TTL_SECONDS
                json_response(
                    self,
                    HTTPStatus.OK,
                    {
                        "ok": True,
                        "token": token,
                        "member": {"email": MEMBER_EMAIL},
                        "expires_in_seconds": TOKEN_TTL_SECONDS,
                    },
                )
                return
            json_response(
                self,
                HTTPStatus.UNAUTHORIZED,
                {"ok": False, "error": "Email or password did not match an active member account."},
            )
            return

        if self.path == "/api/logout":
            auth = self.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                TOKENS.pop(auth.removeprefix("Bearer ").strip(), None)
            json_response(self, HTTPStatus.OK, {"ok": True})
            return

        json_response(self, HTTPStatus.NOT_FOUND, {"ok": False, "error": "Not found"})

    def do_GET(self) -> None:
        if self.path == "/api/archive":
            if not valid_token(self):
                json_response(self, HTTPStatus.UNAUTHORIZED, {"ok": False, "error": "Login required"})
                return
            with ARCHIVE_PATH.open("r", encoding="utf-8") as f:
                payload = json.load(f)
            json_response(self, HTTPStatus.OK, {"ok": True, **payload})
            return

        if self.path == "/api/health":
            json_response(self, HTTPStatus.OK, {"ok": True})
            return

        self.serve_static()

    def serve_static(self) -> None:
        clean_path = unquote(self.path.split("?", 1)[0]).lstrip("/")
        if clean_path in ("", "/"):
            clean_path = "index.html"
        target = (ROOT / clean_path).resolve()
        if not str(target).startswith(str(ROOT)) or not target.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        body = target.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        if target.name in {"index.html", "archive-data.json"}:
            self.send_header("Cache-Control", "no-store")
        else:
            self.send_header("Cache-Control", "public, max-age=3600")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Gridiron Index server listening on 0.0.0.0:{port}")
    print(f"Seed member login: {MEMBER_EMAIL}")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
