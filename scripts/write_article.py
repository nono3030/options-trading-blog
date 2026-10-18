"""Write and save new articles for the top keywords in data/plan.json."""
from __future__ import annotations

import re
import sys

from lib import (PLAN_FILE, POSTS_DIR, ask_claude, dump_markdown, load_config, load_json,
                 load_keywords, load_posts, load_state, parse_markdown, save_keywords,
                 save_state, similarity, slugify, today)
from prompts import FORMAT, SYSTEM, existing_posts_block, learnings_block

MIN_WORDS = 1000


def validate(meta: dict, body: str) -> list[str]:
    errors = []
    for field in ("title", "description", "keyword"):
        if not meta.get(field):
            errors.append(f"missing {field}")
    if len(meta.get("title", "")) > 75:
        errors.append("title too long")
    if not 100 <= len(meta.get("description", "")) <= 170:
        errors.append("description length out of range")
    words = len(re.findall(r"\w+", body))
    if words < MIN_WORDS:
        errors.append(f"too short ({words} words)")
    if re.search(r"^# ", body, re.M):
        errors.append("body contains an H1")
    return errors


def write_one(target: dict, cfg: dict, posts: list[dict], state: dict) -> str | None:
    keyword = target["keyword"]
    context = ""
    if target.get("source") == "gsc":
        context = (f"\nCe mot-clé génère déjà {target['impressions']} impressions/mois sur Google "
                   f"mais nous sommes en position moyenne {target['position']} : il faut l'article "
                   "de référence sur ce sujet.")
    prompt = f"""Rédige un article de blog complet (1500 à 2500 mots) ciblant le mot-clé : « {keyword} ».{context}

Avant d'écrire, recherche sur le web les pages qui se classent en tête sur cette requête \
(en français et en anglais) pour comprendre l'intention de recherche et faire nettement mieux : \
plus précis, plus concret, plus à jour (nous sommes le {today()}).

Articles existants du blog (pour les liens internes) :
{existing_posts_block(posts)}

Ce qui a fonctionné ou non lors de nos optimisations passées :
{learnings_block(state["learnings"])}

{FORMAT}"""
    site = cfg["site"]
    system = SYSTEM.format(title=site["title"], author=site["author"], author_bio=site["author_bio"])

    for attempt in range(2):
        text = ask_claude(system, prompt, web_search=True)
        text = re.sub(r"^```(?:markdown|md)?\s*\n|\n```\s*$", "", text.strip())
        try:
            meta, body = parse_markdown(text)
        except Exception as e:
            print(f"[{keyword}] unparseable output ({e}), retrying")
            continue
        errors = validate(meta, body)
        if not errors:
            break
        print(f"[{keyword}] validation failed: {errors}")
        prompt += f"\n\nATTENTION, ta précédente version a été rejetée pour : {errors}. Corrige cela."
    else:
        return None

    # Guard against cannibalising an existing article.
    for p in posts:
        if similarity(meta["title"], p["title"]) >= 0.7:
            print(f"[{keyword}] too close to existing post '{p['title']}', skipped")
            return None

    slug = slugify(meta.get("keyword") or keyword)
    if (POSTS_DIR / f"{slug}.md").exists():
        slug = f"{slug}-{today()}"
    ordered = {
        "title": meta["title"],
        "description": meta["description"],
        "keyword": meta["keyword"],
        "slug": slug,
        "date": today(),
        "updated": today(),
        "tags": meta.get("tags", []),
        "faq": meta.get("faq", []),
    }
    (POSTS_DIR / f"{slug}.md").write_text(dump_markdown(ordered, body), encoding="utf-8")
    state["posts"][slug] = {"keyword": keyword, "source": target.get("source"), "date": today()}
    print(f"Published: {slug} — {meta['title']}")
    return slug


def main() -> None:
    cfg = load_config()
    plan = load_json(PLAN_FILE, {"new": []})
    posts = load_posts()
    state = load_state()
    keywords = load_keywords()
    wanted = cfg["seo"]["new_posts_per_run"]
    published = 0

    for target in plan["new"]:
        if published >= wanted:
            break
        kw = target["keyword"]
        try:
            slug = write_one(target, cfg, posts, state)
        except Exception as e:
            # API error (credits, auth, outage): keep the keyword for the next run and stop,
            # retrying every other keyword would fail the same way.
            print(f"[{kw}] failed: {e}", file=sys.stderr)
            break
        if kw in keywords["backlog"]:
            keywords["backlog"].remove(kw)
        keywords["done"].append(kw)
        if slug:
            published += 1
            posts = load_posts()

    save_keywords(keywords)
    save_state(state)
    print(f"{published} article(s) published")
    if wanted and not published:
        sys.exit(1)


if __name__ == "__main__":
    main()
