"""Fetch GA4 audience + behaviour data and write a readable report.

Env:
  GSC_SERVICE_ACCOUNT_JSON  same service account as Search Console (needs Viewer on GA4)
  GA4_PROPERTY_ID           numeric GA4 property id (Admin > Property details)
Outputs:
  data/ga4/latest.json      per-page metrics + events (used by strategy.py)
  data/reports/latest.md    audience / acquisition / content report
"""
from __future__ import annotations

import datetime as dt
import json
import os

from urllib.parse import urlparse

from lib import DATA_DIR, GSC_DIR, load_config, load_json, load_posts, save_json

GA4_DIR = DATA_DIR / "ga4"
REPORTS_DIR = DATA_DIR / "reports"
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
TRACKED_EVENTS = ["article_read", "internal_link_click", "outbound_click", "faq_open", "copy_text"]


def service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    info = json.loads(os.environ["GSC_SERVICE_ACCOUNT_JSON"])
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("analyticsdata", "v1beta", credentials=creds, cache_discovery=False)


def report(svc, prop, days, dimensions, metrics, limit=1000, dim_filter=None, order_metric=None):
    body = {
        "dateRanges": [{"startDate": f"{days}daysAgo", "endDate": "yesterday"}],
        "dimensions": [{"name": d} for d in dimensions],
        "metrics": [{"name": m} for m in metrics],
        "limit": limit,
    }
    if dim_filter:
        body["dimensionFilter"] = dim_filter
    if order_metric:
        body["orderBys"] = [{"metric": {"metricName": order_metric}, "desc": True}]
    resp = svc.properties().runReport(property=f"properties/{prop}", body=body).execute()
    rows = []
    for r in resp.get("rows", []):
        row = {d: v["value"] for d, v in zip(dimensions, r["dimensionValues"])}
        for m, v in zip(metrics, r["metricValues"]):
            row[m] = round(float(v["value"]), 4)
        rows.append(row)
    return rows


def in_list(field, values):
    return {"filter": {"fieldName": field, "inListFilter": {"values": values}}}


def table(rows, cols, headers, n=10) -> str:
    if not rows:
        return "_Pas encore de données._\n"
    out = "| " + " | ".join(headers) + " |\n|" + "---|" * len(headers) + "\n"
    for r in rows[:n]:
        cells = []
        for c in cols:
            v = r.get(c, "")
            if isinstance(v, float):
                v = f"{v:.0%}" if "Rate" in c or c == "ctr" else f"{v:,.0f}".replace(",", " ")
            cells.append(str(v))
        out += "| " + " | ".join(cells) + " |\n"
    return out


def main() -> None:
    if not os.environ.get("GSC_SERVICE_ACCOUNT_JSON") or not os.environ.get("GA4_PROPERTY_ID"):
        print("GA4 not configured — skipping.")
        return
    cfg = load_config()
    prop, days = os.environ["GA4_PROPERTY_ID"], cfg["seo"]["gsc_days"]
    svc = service()

    pages = report(svc, prop, days, ["pagePath"],
                   ["screenPageViews", "activeUsers", "engagementRate", "userEngagementDuration", "bounceRate"],
                   order_metric="screenPageViews")
    for p in pages:
        p["avgEngagedSeconds"] = round(p["userEngagementDuration"] / max(p["activeUsers"], 1), 1)
    events = report(svc, prop, days, ["pagePath", "eventName"], ["eventCount"],
                    dim_filter=in_list("eventName", TRACKED_EVENTS))
    by_page = {p["pagePath"]: p for p in pages}
    for e in events:
        if e["pagePath"] in by_page:
            by_page[e["pagePath"]][e["eventName"]] = e["eventCount"]
    base = urlparse(cfg["site"]["url"]).path.rstrip("/")
    slugs = {p["slug"] for p in load_posts()}
    for p in pages:
        path = p["pagePath"]
        p["slug"] = path[len(base):].strip("/") if path.startswith(base) else None
        p["readRate"] = round(p.get("article_read", 0) / max(p["screenPageViews"], 1), 3)

    audience = {
        name: report(svc, prop, days, dims, ["activeUsers", "sessions", "engagementRate"],
                     limit=50, order_metric="activeUsers")
        for name, dims in {
            "channels": ["sessionDefaultChannelGroup"],
            "sources": ["sessionSourceMedium"],
            "countries": ["country"],
            "cities": ["city"],
            "devices": ["deviceCategory"],
            "browsers": ["browser"],
            "new_vs_returning": ["newVsReturning"],
            "landing_pages": ["landingPage"],
        }.items()
    }
    totals = report(svc, prop, days, [], ["activeUsers", "newUsers", "sessions", "screenPageViews",
                                          "engagementRate", "userEngagementDuration"])
    # FAQ questions opened (needs the custom dimension registered by ga4_setup.py).
    try:
        audience["faq_questions"] = report(svc, prop, days, ["customEvent:question"], ["eventCount"],
                                           limit=50, dim_filter={"filter": {"fieldName": "eventName",
                                           "stringFilter": {"value": "faq_open"}}}, order_metric="eventCount")
    except Exception:
        audience["faq_questions"] = []

    save_json(GA4_DIR / "latest.json", {"days": days, "totals": totals[0] if totals else {},
                                        "pages": pages, "audience": audience})

    # --- markdown report (GA4 + GSC) ---------------------------------------
    t = totals[0] if totals else {}
    gsc = load_json(GSC_DIR / "latest.json", {"query_page": []})
    queries = {}
    for r in gsc["query_page"]:
        q = queries.setdefault(r["query"], {"query": r["query"], "clicks": 0, "impressions": 0})
        q["clicks"] += r["clicks"]
        q["impressions"] += r["impressions"]
    top_q = sorted(queries.values(), key=lambda q: q["impressions"], reverse=True)
    articles = [p for p in pages if p["slug"] in slugs]
    weak = sorted([p for p in articles if p["screenPageViews"] >= 30], key=lambda p: p["avgEngagedSeconds"])

    md = f"""# Rapport d'audience — {dt.date.today().isoformat()} ({days} derniers jours)

## Vue d'ensemble
| Utilisateurs | Nouveaux | Sessions | Pages vues | Taux d'engagement | Temps moyen engagé |
|---|---|---|---|---|---|
| {t.get('activeUsers', 0):.0f} | {t.get('newUsers', 0):.0f} | {t.get('sessions', 0):.0f} | {t.get('screenPageViews', 0):.0f} | {t.get('engagementRate', 0):.0%} | {t.get('userEngagementDuration', 0) / max(t.get('activeUsers', 1), 1):.0f} s |

## Acquisition
{table(audience['channels'], ['sessionDefaultChannelGroup', 'activeUsers', 'engagementRate'], ['Canal', 'Utilisateurs', 'Engagement'])}
{table(audience['sources'], ['sessionSourceMedium', 'activeUsers', 'engagementRate'], ['Source / support', 'Utilisateurs', 'Engagement'])}
## Requêtes Google (Search Console)
{table(top_q, ['query', 'impressions', 'clicks'], ['Requête', 'Impressions', 'Clics'], 20)}
## Audience
{table(audience['countries'], ['country', 'activeUsers', 'engagementRate'], ['Pays', 'Utilisateurs', 'Engagement'])}
{table(audience['cities'], ['city', 'activeUsers'], ['Ville', 'Utilisateurs'])}
{table(audience['devices'], ['deviceCategory', 'activeUsers', 'engagementRate'], ['Appareil', 'Utilisateurs', 'Engagement'])}
{table(audience['new_vs_returning'], ['newVsReturning', 'activeUsers', 'engagementRate'], ['Type', 'Utilisateurs', 'Engagement'])}
## Contenus les plus lus
{table(articles, ['pagePath', 'screenPageViews', 'avgEngagedSeconds', 'readRate', 'internal_link_click'], ['Page', 'Vues', 'Temps engagé (s)', 'Taux de lecture', 'Clics internes'], 20)}
## Contenus qui retiennent mal (candidats à la réécriture)
{table(weak, ['pagePath', 'screenPageViews', 'avgEngagedSeconds', 'bounceRate'], ['Page', 'Vues', 'Temps engagé (s)', 'Rebond'])}
## Questions FAQ les plus ouvertes
{table(audience['faq_questions'], ['customEvent:question', 'eventCount'], ['Question', 'Ouvertures'])}
_Comportement détaillé (cartes de chaleur, relectures de sessions) : tableau de bord Microsoft Clarity._
"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "latest.md").write_text(md, encoding="utf-8")
    print(f"GA4: {len(pages)} pages, {t.get('activeUsers', 0):.0f} users — report written")


if __name__ == "__main__":
    main()
