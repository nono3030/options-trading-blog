"""Static site generator: content/ -> dist/ (HTML, sitemap, RSS, robots)."""
from __future__ import annotations

import json
import math
import re
import shutil
from collections import defaultdict
from email.utils import format_datetime
from datetime import datetime, timezone
from html import escape
from urllib.parse import urlparse

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

from lib import PAGES_DIR, ROOT, load_config, load_posts, parse_markdown, similarity, slugify

DIST = ROOT / "dist"


def render_md(text: str) -> tuple[str, str]:
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"],
                           extension_configs={"toc": {"toc_depth": "2-3", "permalink": False}})
    html = md.convert(text)
    return html, md.toc


def rewrite_links(html: str, base_path: str) -> str:
    """Root-relative links (/slug/) -> base path; external links open safely."""
    html = re.sub(r'href="/(?!/)', f'href="{base_path}/', html)
    return re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" rel="noopener" target="_blank"', html)


def related(post: dict, posts: list[dict], n: int = 4) -> list[dict]:
    scored = []
    for other in posts:
        if other["slug"] == post["slug"]:
            continue
        score = len(set(post.get("tags", [])) & set(other.get("tags", [])))
        score += 3 * similarity(post.get("keyword", post["title"]), other.get("keyword", other["title"]))
        if score > 0:
            scored.append((score, other))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [o for _, o in scored[:n]]


def json_ld(post: dict, site: dict, url: str) -> str:
    graph = [
        {
            "@type": "BlogPosting",
            "headline": post["title"],
            "description": post["description"],
            "datePublished": post["date"],
            "dateModified": post["updated"],
            "inLanguage": site["lang"],
            "mainEntityOfPage": url,
            "author": {"@type": "Person", "name": site["author"], "url": f"{site['url']}/a-propos/"},
            "publisher": {"@type": "Organization", "name": site["title"], "url": site["url"]},
            "keywords": ", ".join([post.get("keyword", "")] + post.get("tags", [])),
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": site["url"] + "/"},
                {"@type": "ListItem", "position": 2, "name": post["title"], "item": url},
            ],
        },
    ]
    if post.get("faq"):
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                for f in post["faq"] if f.get("q") and f.get("a")
            ],
        })
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return data.replace("</", "<\\/")


def write(path: str, content: str) -> None:
    out = DIST / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")


def main() -> None:
    cfg = load_config()
    site = cfg["site"]
    base_path = urlparse(site["url"]).path.rstrip("/")
    site["base_path"] = base_path

    env = Environment(loader=FileSystemLoader(ROOT / "templates"),
                      autoescape=select_autoescape(["html"]))
    env.globals.update(site=site, year=datetime.now().year)

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "static", DIST / "static")

    posts = load_posts()
    tags = defaultdict(list)
    for p in posts:
        html, toc = render_md(p["body"])
        p["html"] = rewrite_links(html, base_path)
        p["toc"] = toc
        p["url"] = f"{site['url']}/{p['slug']}/"
        p["href"] = f"{base_path}/{p['slug']}/"
        p["reading_time"] = max(1, math.ceil(len(re.findall(r"\w+", p["body"])) / 220))
        for t in p.get("tags", []):
            tags[t].append(p)

    tag_slugs = {t: slugify(t) for t in tags}
    env.globals["tag_slugs"] = tag_slugs

    for p in posts:
        write(f"{p['slug']}/index.html", env.get_template("post.html").render(
            post=p, related=related(p, posts), canonical=p["url"],
            title=p["title"], description=p["description"], json_ld=json_ld(p, site, p["url"]),
            og_type="article"))

    pages = []
    for path in sorted(PAGES_DIR.glob("*.md")):
        meta, body = parse_markdown(path.read_text(encoding="utf-8"))
        slug = meta.get("slug", path.stem)
        html, _ = render_md(body)
        url = f"{site['url']}/{slug}/"
        pages.append({"slug": slug, "url": url, "updated": str(meta.get("updated", ""))})
        write(f"{slug}/index.html", env.get_template("page.html").render(
            page=meta, html=rewrite_links(html, base_path), canonical=url,
            title=meta["title"], description=meta.get("description", site["description"])))

    for t, tposts in tags.items():
        ts = tag_slugs[t]
        url = f"{site['url']}/tag/{ts}/"
        write(f"tag/{ts}/index.html", env.get_template("list.html").render(
            posts=tposts, heading=f"Articles : {t}", canonical=url,
            title=f"{t.capitalize()} — {site['title']}",
            description=f"Tous nos articles sur {t} : guides et stratégies d'options."))
    write("index.html", env.get_template("list.html").render(
        posts=posts, heading=None, canonical=site["url"] + "/",
        title=f"{site['title']} — {site['tagline']}", description=site["description"],
        top_tags=sorted(tags, key=lambda t: len(tags[t]), reverse=True)[:12]))
    write("404.html", env.get_template("page.html").render(
        page={"title": "Page introuvable"}, canonical=site["url"] + "/",
        html=f'<p>Cette page n\'existe pas. <a href="{base_path}/">Retour à l\'accueil</a>.</p>',
        title="Page introuvable", description=site["description"], noindex=True))

    # sitemap.xml
    urls = [(site["url"] + "/", posts[0]["updated"] if posts else "")]
    urls += [(p["url"], p["updated"]) for p in posts]
    urls += [(pg["url"], pg["updated"]) for pg in pages]
    urls += [(f"{site['url']}/tag/{ts}/", "") for ts in tag_slugs.values()]
    items = "".join(
        f"<url><loc>{escape(u)}</loc>{f'<lastmod>{d}</lastmod>' if d else ''}</url>" for u, d in urls)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>'
          f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>')

    # RSS
    def rfc822(d: str) -> str:
        return format_datetime(datetime.fromisoformat(d).replace(tzinfo=timezone.utc))

    rss_items = "".join(
        f"<item><title>{escape(p['title'])}</title><link>{p['url']}</link><guid>{p['url']}</guid>"
        f"<pubDate>{rfc822(p['date'])}</pubDate><description>{escape(p['description'])}</description></item>"
        for p in posts[:30])
    write("feed.xml", '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>'
          f"<title>{escape(site['title'])}</title><link>{site['url']}/</link>"
          f"<description>{escape(site['description'])}</description><language>{site['lang']}</language>"
          f"{rss_items}</channel></rss>")

    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {site['url']}/sitemap.xml\n")
    write(".nojekyll", "")
    print(f"Built {len(posts)} posts, {len(pages)} pages, {len(tags)} tags -> dist/")


if __name__ == "__main__":
    main()
