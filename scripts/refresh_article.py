"""Rewrite under-performing articles using the queries they actually rank for."""
from __future__ import annotations

import json
import re
import sys

from lib import (PLAN_FILE, ask_claude, dump_markdown, load_config, load_json, load_posts,
                 load_state, parse_markdown, save_state, today)
from prompts import FORMAT, SYSTEM, existing_posts_block, learnings_block
from write_article import validate


def refresh_one(item: dict, post: dict, cfg: dict, posts: list[dict], state: dict) -> bool:
    current = dump_markdown(
        {k: post[k] for k in ("title", "description", "keyword", "tags", "faq") if k in post},
        post["body"],
    )
    queries = json.dumps(item["queries"], ensure_ascii=False, indent=1)
    prompt = f"""Voici un article de notre blog et ses performances Google Search Console \
sur les {cfg['seo']['gsc_days']} derniers jours.

Performances de la page : {json.dumps(item['metrics'], ensure_ascii=False)}
Requêtes pour lesquelles la page apparaît (ctr = taux de clic, position = position moyenne) :
{queries}

Comportement des lecteurs sur la page (Google Analytics, lecteurs ayant accepté les cookies) : \
{json.dumps(item.get('engagement', {}), ensure_ascii=False)}
(avgEngagedSeconds = temps de lecture active moyen ; readRate = part des vues lues à plus de 75 % ; \
internal_link_click = clics vers d'autres articles.)

Objectif : augmenter les clics organiques ET la lecture effective. Si le temps de lecture ou le \
taux de lecture est faible, rends l'introduction plus directe, la structure plus scannable et le \
contenu plus concret.
1. Réécris title et description pour améliorer le CTR sur les requêtes à fortes impressions \
(sans clickbait trompeur).
2. Couvre explicitement les requêtes à fortes impressions mais mal positionnées : ajoute ou \
renforce des sections qui y répondent, ajoute des questions à la FAQ si pertinent.
3. Mets à jour les informations datées (nous sommes le {today()}) en vérifiant via la recherche web.
4. Garde ce qui fonctionne : ne supprime pas les passages qui répondent aux requêtes déjà \
bien positionnées. Garde le même mot-clé principal.

Ce qui a fonctionné ou non lors de nos optimisations passées :
{learnings_block(state["learnings"])}

Articles existants du blog (pour les liens internes, n'inclus pas /{post['slug']}/) :
{existing_posts_block([p for p in posts if p['slug'] != post['slug']])}

Après le fichier Markdown, ajoute une dernière ligne au format exact :
CHANGEMENTS: <résumé en une phrase des modifications principales>

{FORMAT}

Article actuel :
{current}"""
    site = cfg["site"]
    system = SYSTEM.format(title=site["title"], author=site["author"], author_bio=site["author_bio"])
    text = ask_claude(system, prompt, web_search=True)

    changes = ""
    m = re.search(r"^CHANGEMENTS:\s*(.+)$", text, re.M)
    if m:
        changes = m.group(1).strip()
        text = text[: m.start()]
    text = re.sub(r"^```(?:markdown|md)?\s*\n|\n```\s*$", "", text.strip())
    meta, body = parse_markdown(text)
    errors = validate(meta, body)
    if errors:
        print(f"[{post['slug']}] refresh rejected: {errors}")
        return False

    updated = {
        "title": meta["title"],
        "description": meta["description"],
        "keyword": post.get("keyword", meta["keyword"]),
        "slug": post["slug"],
        "date": post["date"],
        "updated": today(),
        "tags": meta.get("tags", post.get("tags", [])),
        "faq": meta.get("faq", post.get("faq", [])),
    }
    post["path"].write_text(dump_markdown(updated, body), encoding="utf-8")
    state["refreshes"].append({
        "slug": post["slug"],
        "date": today(),
        "before": {**item["metrics"], **{f"ga4_{k}": v for k, v in item.get("engagement", {}).items()}},
        "old_title": post["title"],
        "new_title": meta["title"],
        "changes": changes,
    })
    print(f"Refreshed: {post['slug']} — {changes}")
    return True


def main() -> None:
    cfg = load_config()
    plan = load_json(PLAN_FILE, {"refresh": []})
    posts = load_posts()
    by_slug = {p["slug"]: p for p in posts}
    state = load_state()
    done = 0
    for item in plan["refresh"]:
        if done >= cfg["seo"]["refreshes_per_run"]:
            break
        post = by_slug.get(item["slug"])
        if not post:
            continue
        try:
            if refresh_one(item, post, cfg, posts, state):
                done += 1
        except Exception as e:
            print(f"[{item['slug']}] refresh failed: {e}", file=sys.stderr)
    save_state(state)
    print(f"{done} article(s) refreshed")


if __name__ == "__main__":
    main()
