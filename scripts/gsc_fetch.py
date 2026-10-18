"""Fetch Search Console performance data and (re)submit the sitemap.

Env:
  GSC_SERVICE_ACCOUNT_JSON  service account key (JSON content)
  GSC_PROPERTY              e.g. "sc-domain:example.com" or "https://example.com/"
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

from lib import GSC_DIR, load_config, save_json

SCOPES = ["https://www.googleapis.com/auth/webmasters"]


def service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    info = json.loads(os.environ["GSC_SERVICE_ACCOUNT_JSON"])
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def query(svc, prop: str, start: str, end: str, dimensions: list[str]) -> list[dict]:
    rows, offset = [], 0
    while True:
        resp = svc.searchanalytics().query(siteUrl=prop, body={
            "startDate": start,
            "endDate": end,
            "dimensions": dimensions,
            "rowLimit": 25000,
            "startRow": offset,
        }).execute()
        batch = resp.get("rows", [])
        for r in batch:
            row = dict(zip(dimensions, r["keys"]))
            row.update(clicks=r["clicks"], impressions=r["impressions"],
                       ctr=round(r["ctr"], 4), position=round(r["position"], 1))
            rows.append(row)
        if len(batch) < 25000:
            return rows
        offset += 25000


def main() -> None:
    cfg = load_config()
    prop = os.environ.get("GSC_PROPERTY") or cfg["seo"].get("gsc_property")
    if not os.environ.get("GSC_SERVICE_ACCOUNT_JSON") or not prop:
        print("GSC credentials not configured — skipping fetch (cold-start mode).")
        return
    svc = service()

    # GSC data lags ~2-3 days.
    end = dt.date.today() - dt.timedelta(days=3)
    start = end - dt.timedelta(days=cfg["seo"]["gsc_days"] - 1)
    snapshot = {
        "property": prop,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "query_page": query(svc, prop, start.isoformat(), end.isoformat(), ["query", "page"]),
        "pages": query(svc, prop, start.isoformat(), end.isoformat(), ["page"]),
    }
    save_json(GSC_DIR / "latest.json", snapshot)

    # Lightweight daily history of page totals (used to measure refresh impact).
    save_json(GSC_DIR / f"pages-{end.isoformat()}.json", snapshot["pages"])
    cutoff = (end - dt.timedelta(days=180)).isoformat()
    for old in GSC_DIR.glob("pages-*.json"):
        if old.stem.removeprefix("pages-") < cutoff:
            old.unlink()
    print(f"GSC: {len(snapshot['query_page'])} query/page rows, {len(snapshot['pages'])} pages")

    sitemap = f"{cfg['site']['url']}/sitemap.xml"
    try:
        svc.sitemaps().submit(siteUrl=prop, feedpath=sitemap).execute()
        print(f"Sitemap submitted: {sitemap}")
    except Exception as e:  # non-fatal
        print(f"Sitemap submit failed: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
