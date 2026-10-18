"""One-off: register the custom dimensions/metrics sent by static/analytics.js in GA4.

Needs the service account to have the *Editor* role on the GA4 property.
Run from the Actions tab ("GA4 setup") or locally with the same env vars as ga4_fetch.py.
"""
from __future__ import annotations

import json
import os

DIMENSIONS = {
    "article_slug": "Article",
    "article_keyword": "Mot-clé de l'article",
    "article_tags": "Tags de l'article",
    "page_type": "Type de page",
    "link_zone": "Zone du lien",
    "link_text": "Texte du lien",
    "question": "Question FAQ",
    "percent": "Profondeur de défilement",
}
METRICS = {
    "engaged_seconds": ("Secondes de lecture active", "SECONDS"),
    "article_words": ("Nombre de mots", "STANDARD"),
    "article_age_days": ("Âge de l'article (jours)", "STANDARD"),
}


def main() -> None:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    info = json.loads(os.environ["GSC_SERVICE_ACCOUNT_JSON"])
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/analytics.edit"])
    admin = build("analyticsadmin", "v1beta", credentials=creds, cache_discovery=False)
    parent = f"properties/{os.environ['GA4_PROPERTY_ID']}"

    existing = {d["parameterName"] for d in
                admin.properties().customDimensions().list(parent=parent).execute().get("customDimensions", [])}
    for param, name in DIMENSIONS.items():
        if param not in existing:
            admin.properties().customDimensions().create(parent=parent, body={
                "parameterName": param, "displayName": name, "scope": "EVENT"}).execute()
            print(f"+ dimension {param}")

    existing = {m["parameterName"] for m in
                admin.properties().customMetrics().list(parent=parent).execute().get("customMetrics", [])}
    for param, (name, unit) in METRICS.items():
        if param not in existing:
            admin.properties().customMetrics().create(parent=parent, body={
                "parameterName": param, "displayName": name, "measurementUnit": unit,
                "scope": "EVENT"}).execute()
            print(f"+ metric {param}")
    print("GA4 custom definitions up to date")


if __name__ == "__main__":
    main()
