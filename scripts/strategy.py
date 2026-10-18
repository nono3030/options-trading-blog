"""Decide what to write and what to improve, from Search Console data.

Outputs data/plan.json:
  new:     keywords to target with a new article (best first)
  refresh: existing articles to rewrite, with the queries they rank for
Also measures the impact of past refreshes (the feedback loop) and keeps the
keyword backlog topped up.
"""
from __future__ import annotations

import datetime as dt
import os
from collections import defaultdict

from lib import (GSC_DIR, PLAN_FILE, ask_claude, extract_json, load_config, load_json,
                 load_keywords, load_posts, load_state, normalize_query, save_json,
                 save_keywords, save_state, similarity)

# Rough organic CTR by position — used to spot titles/descriptions that under-perform.
EXPECTED_CTR = {1: .28, 2: .15, 3: .10, 4: .07, 5: .05, 6: .04, 7: .03, 8: .025, 9: .02, 10: .018}


def expected_ctr(pos: float) -> float:
    return EXPECTED_CTR.get(max(1, round(pos)), 0.01)


def slug_from_url(url: str, site_url: str) -> str | None:
    if not url.startswith(site_url):
        return None
    path = url[len(site_url):].split("#")[0].split("?")[0].strip("/")
    return path or None


def is_covered(query: str, posts: list[dict], threshold: float = 0.5) -> bool:
    return any(similarity(query, p.get("keyword", p["title"])) >= threshold for p in posts)


def measure_refreshes(state: dict, site_url: str) -> None:
    """Compare page metrics ~28 days after a refresh with the metrics before it."""
    snaps = sorted(GSC_DIR.glob("pages-*.json"))
    if not snaps:
        return
    latest = {slug_from_url(r["page"], site_url): r for r in load_json(snaps[-1], [])}
    horizon = (dt.date.today() - dt.timedelta(days=31)).isoformat()
    for ref in state["refreshes"]:
        if ref.get("measured") or ref["date"] > horizon:
            continue
        after = latest.get(ref["slug"])
        before = ref.get("before") or {}
        if not after:
            continue
        verdict = "neutre"
        if after["clicks"] > before.get("clicks", 0) * 1.15:
            verdict = "positif"
        elif after["clicks"] < before.get("clicks", 0) * 0.85:
            verdict = "négatif"
        state["learnings"].append({
            "slug": ref["slug"],
            "date": ref["date"],
            "changes": ref.get("changes", ""),
            "before": before,
            "after": {k: after[k] for k in ("clicks", "impressions", "ctr", "position")},
            "verdict": verdict,
        })
        ref["measured"] = True
    state["learnings"] = state["learnings"][-50:]


def expand_backlog(keywords: dict, posts: list[dict], top_queries: list[str]) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return
    existing = [p["title"] for p in posts] + keywords["backlog"] + keywords["done"]
    reply = ask_claude(
        "Tu es un consultant SEO francophone spécialisé dans la finance et le trading d'options.",
        "Propose 25 nouveaux mots-clés longue traîne en français, à forte intention informationnelle, "
        "pour un blog sur le trading d'options (débutant à avancé, marché US et fiscalité française). "
        "Utilise la recherche web pour repérer ce que les francophones cherchent réellement "
        "(suggestions Google, forums, questions fréquentes).\n\n"
        f"Requêtes qui nous apportent déjà des impressions : {top_queries[:30]}\n"
        f"Sujets déjà couverts ou prévus (à ne pas répéter) : {existing}\n\n"
        'Réponds uniquement avec un tableau JSON de chaînes, ex. ["mot clé 1", "mot clé 2"].',
        web_search=True, max_tokens=16000,
    )
    ideas = [k for k in extract_json(reply) if isinstance(k, str)]
    for kw in ideas:
        if not any(similarity(kw, e) >= 0.6 for e in existing):
            keywords["backlog"].append(kw.strip().lower())
            existing.append(kw)
    print(f"Backlog expanded with Claude: {len(keywords['backlog'])} keywords pending")


def main() -> None:
    cfg = load_config()
    seo, site_url = cfg["seo"], cfg["site"]["url"]
    posts = load_posts()
    by_slug = {p["slug"]: p for p in posts}
    state = load_state()
    keywords = load_keywords()
    gsc = load_json(GSC_DIR / "latest.json", {"query_page": [], "pages": []})

    measure_refreshes(state, site_url)

    # --- aggregate queries --------------------------------------------------
    queries = defaultdict(lambda: {"impressions": 0, "clicks": 0, "pos_w": 0.0, "pages": set()})
    page_queries = defaultdict(list)
    for r in gsc["query_page"]:
        q = queries[r["query"]]
        q["impressions"] += r["impressions"]
        q["clicks"] += r["clicks"]
        q["pos_w"] += r["position"] * r["impressions"]
        q["pages"].add(r["page"])
        slug = slug_from_url(r["page"], site_url)
        if slug in by_slug:
            page_queries[slug].append(r)

    # --- new article opportunities -----------------------------------------
    new = []
    for query, q in queries.items():
        pos = q["pos_w"] / max(q["impressions"], 1)
        if q["impressions"] < seo["min_impressions_new"] or len(normalize_query(query).split()) < 2:
            continue
        # Already ranking well, or a post already targets it: improve instead of duplicating.
        if pos <= 8 or is_covered(query, posts):
            continue
        new.append({"keyword": query, "source": "gsc", "impressions": q["impressions"],
                    "position": round(pos, 1), "score": q["impressions"] * min(pos, 50) / 10})
    new.sort(key=lambda x: x["score"], reverse=True)

    # Fall back on the backlog (cold start, or when GSC has nothing new).
    for kw in list(keywords["backlog"]):
        if is_covered(kw, posts) or kw in keywords["done"]:
            keywords["backlog"].remove(kw)
            keywords["done"].append(kw)
            continue
        if not any(similarity(kw, n["keyword"]) >= 0.5 for n in new):
            new.append({"keyword": kw, "source": "backlog", "score": 0})

    # --- refresh opportunities ---------------------------------------------
    cooldown = (dt.date.today() - dt.timedelta(days=seo["refresh_cooldown_days"])).isoformat()
    recently = {r["slug"] for r in state["refreshes"] if r["date"] > cooldown}
    refresh = []
    for page in gsc["pages"]:
        slug = slug_from_url(page["page"], site_url)
        post = by_slug.get(slug)
        if not post or slug in recently or post["date"] > cooldown:
            continue
        if page["impressions"] < seo["min_impressions_refresh"]:
            continue
        ctr_gap = max(0.0, expected_ctr(page["position"]) - page["ctr"])
        striking = 4 <= page["position"] <= 25  # page 1 bottom / page 2-3
        if not striking and ctr_gap < 0.01:
            continue
        top = sorted(page_queries[slug], key=lambda r: r["impressions"], reverse=True)[:20]
        refresh.append({
            "slug": slug,
            "metrics": {k: page[k] for k in ("clicks", "impressions", "ctr", "position")},
            "queries": [{k: r[k] for k in ("query", "clicks", "impressions", "ctr", "position")}
                        for r in top],
            "score": page["impressions"] * (ctr_gap + (0.05 if striking else 0)),
        })
    refresh.sort(key=lambda x: x["score"], reverse=True)

    # Push promising GSC queries into the backlog so they are never lost.
    for n in new:
        if n["source"] == "gsc" and n["keyword"] not in keywords["backlog"]:
            keywords["backlog"].insert(0, n["keyword"])

    if len(keywords["backlog"]) < 10:
        top_queries = sorted(queries, key=lambda k: queries[k]["impressions"], reverse=True)
        try:
            expand_backlog(keywords, posts, top_queries)
        except Exception as e:  # never block publishing on backlog expansion
            print(f"Backlog expansion failed: {e}")
        for kw in keywords["backlog"]:
            if not any(similarity(kw, n["keyword"]) >= 0.5 for n in new) and not is_covered(kw, posts):
                new.append({"keyword": kw, "source": "claude", "score": 0})

    save_json(PLAN_FILE, {"date": dt.date.today().isoformat(), "new": new[:30], "refresh": refresh[:15]})
    save_keywords(keywords)
    save_state(state)
    print(f"Plan: {len(new)} new candidates, {len(refresh)} refresh candidates")


if __name__ == "__main__":
    main()
