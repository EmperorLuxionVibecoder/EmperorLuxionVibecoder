"""Optionally refresh data/*.json from the Lyra operator API.

Expects two environment variables (set as GitHub Actions secrets):

    LYRA_API_URL   base URL of the operator API
    LYRA_API_KEY   bearer token

Expected response of GET {LYRA_API_URL}/profile/register:

    {
      "synced":  "2026-07-09T06:00:00Z",
      "entries": [{"t": "07-08 14:02", "agent": "Solaris",
                   "action": "Recentre", "venue": "Meteora DLMM",
                   "note": "range re-set around price"}, ...],
      "agents":  [{"name": "Solaris", "status": "live"}, ...]   // optional
    }

Without the env vars (or on any error) this exits 0 and leaves the
committed data untouched, so the daily workflow never breaks and the
plates simply keep their last honest state.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"


def main() -> None:
    url = os.environ.get("LYRA_API_URL")
    key = os.environ.get("LYRA_API_KEY")
    if not url or not key:
        print("fetch_register: LYRA_API_URL/LYRA_API_KEY not set — keeping committed data")
        return

    req = urllib.request.Request(
        url.rstrip("/") + "/profile/register",
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # never fail the workflow over a fetch
        print(f"fetch_register: fetch failed ({exc}) — keeping committed data")
        return

    register = {"synced": payload.get("synced"),
                "entries": payload.get("entries", [])}
    (DATA / "register.json").write_text(
        json.dumps(register, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"fetch_register: register.json updated ({len(register['entries'])} entries)")

    if payload.get("agents"):
        agents_path = DATA / "agents.json"
        current = json.loads(agents_path.read_text(encoding="utf-8"))
        status_by_name = {a["name"]: a.get("status") for a in payload["agents"]}
        for agent in current["agents"]:
            if status_by_name.get(agent["name"]):
                agent["status"] = status_by_name[agent["name"]]
        current["updated"] = payload.get("synced")
        agents_path.write_text(
            json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("fetch_register: agents.json statuses updated")


if __name__ == "__main__":
    main()
    sys.exit(0)
