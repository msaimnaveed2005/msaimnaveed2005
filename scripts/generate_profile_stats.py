#!/usr/bin/env python3
"""Generate repository-owned contribution graphics for the profile README."""

import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = "https://api.github.com/graphql"
OUT = Path("output")
QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount } }
      }
    }
  }
}
"""


def fetch_calendar(login, token):
    today = datetime.now(timezone.utc).date()
    start = today - timedelta(days=364)
    variables = {
        "login": login,
        "from": f"{start.isoformat()}T00:00:00Z",
        "to": f"{today.isoformat()}T23:59:59Z",
    }
    body = json.dumps({"query": QUERY, "variables": variables}).encode()
    request = urllib.request.Request(
        API,
        data=body,
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": f"{login}-profile",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise SystemExit(f"GitHub GraphQL error: {payload['errors']}")
    user = (payload.get("data") or {}).get("user")
    if not user:
        raise SystemExit(f"GitHub user not found: {login}")
    return user["contributionsCollection"]["contributionCalendar"]


def stats_svg(total, weekly):
    peak = max(weekly) or 1
    bars = []
    for index, value in enumerate(weekly):
        height = max(2, round(48 * value / peak))
        x = round(index * 620 / max(len(weekly) - 1, 1), 1)
        bars.append(
            f'<rect x="{x}" y="{112 - height}" width="4" height="{height}" '
            'rx="1" class="bar"/>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="620" height="148"
viewBox="0 0 620 148"><style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#24292f}}
.bar{{fill:#57606a}}.rule{{stroke:#d0d7de}}
@media(prefers-color-scheme:dark){{text{{fill:#f0f6fc}}.bar{{fill:#8b949e}}.rule{{stroke:#30363d}}}}
</style><text x="0" y="52" font-size="52" font-weight="600">{total}</text>
<text x="0" y="74" font-size="12">contributions in the last year</text>
<line x1="0" y1="122" x2="620" y2="122" class="rule"/>{"".join(bars)}</svg>
"""


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is not set")
    OUT.mkdir(exist_ok=True)
    calendar = fetch_calendar(os.environ.get("GH_LOGIN", "msaimnaveed2005"), token)
    weekly = [
        sum(day["contributionCount"] for day in week["contributionDays"])
        for week in calendar["weeks"]
    ]
    target = OUT / "stats.svg"
    target.write_text(stats_svg(calendar["totalContributions"], weekly), encoding="utf-8")
    print(f"Updated {target}: {calendar['totalContributions']} contributions")


if __name__ == "__main__":
    main()
