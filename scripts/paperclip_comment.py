#!/usr/bin/env python3
"""Post a markdown comment to a Paperclip issue."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    api = os.environ.get("PAPERCLIP_API_URL", "").rstrip("/")
    key = os.environ.get("PAPERCLIP_API_KEY", "").strip()
    issue = os.environ.get("PAPERCLIP_ISSUE_ID", "").strip()
    run_id = os.environ.get("PAPERCLIP_RUN_ID", "").strip()
    body = os.environ.get("PAPERCLIP_COMMENT_BODY") or sys.stdin.read()
    if not api or not key or not issue:
        print(
            "Paperclip comment skipped: missing PAPERCLIP_API_URL, PAPERCLIP_API_KEY, or PAPERCLIP_ISSUE_ID",
            file=sys.stderr,
        )
        return 0
    if not body.strip():
        print("Paperclip comment skipped: empty body", file=sys.stderr)
        return 0
    url = f"{api}/api/issues/{issue}/comments"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if run_id:
        headers["X-Paperclip-Run-Id"] = run_id
    req = urllib.request.Request(
        url,
        data=json.dumps({"body": body}).encode(),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print("Paperclip comment status", resp.status)
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:400]
        print(f"Paperclip comment failed: HTTP {exc.code} {detail}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 — surface any transport failure
        print(f"Paperclip comment failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
