"""Shared helpers: paths, config, front matter, state, Claude client."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "content" / "posts"
PAGES_DIR = ROOT / "content" / "pages"
DATA_DIR = ROOT / "data"
GSC_DIR = DATA_DIR / "gsc"
STATE_FILE = DATA_DIR / "state.json"
KEYWORDS_FILE = DATA_DIR / "keywords.yaml"
PLAN_FILE = DATA_DIR / "plan.json"


def load_config() -> dict:
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    if os.environ.get("SITE_URL"):
        cfg["site"]["url"] = os.environ["SITE_URL"]
    cfg["site"]["url"] = cfg["site"]["url"].rstrip("/")
    cfg["site"]["gsc_verification"] = os.environ.get("GSC_VERIFICATION", "")
    cfg["site"]["analytics"] = {
        "ga4": os.environ.get("GA4_MEASUREMENT_ID", ""),
        "clarity": os.environ.get("CLARITY_PROJECT_ID", ""),
    }
    cfg["site"]["analytics_enabled"] = any(cfg["site"]["analytics"].values())
    return cfg


def today() -> str:
    return dt.date.today().isoformat()


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text[:80].rstrip("-")


# --- front matter -----------------------------------------------------------

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.S)


def parse_markdown(text: str) -> tuple[dict, str]:
    m = FM_RE.match(text.lstrip("﻿").strip() + "\n")
    if not m:
        raise ValueError("missing front matter")
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, m.group(2).strip() + "\n"


def dump_markdown(meta: dict, body: str) -> str:
    fm = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=1000)
    return f"---\n{fm}---\n\n{body.strip()}\n"


def load_posts() -> list[dict]:
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        meta, body = parse_markdown(path.read_text(encoding="utf-8"))
        meta.setdefault("slug", path.stem)
        meta["date"] = str(meta.get("date", today()))
        meta["updated"] = str(meta.get("updated", meta["date"]))
        meta["path"] = path
        meta["body"] = body
        posts.append(meta)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


# --- state ------------------------------------------------------------------

def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_state() -> dict:
    return load_json(STATE_FILE, {"posts": {}, "refreshes": [], "learnings": []})


def save_state(state: dict) -> None:
    save_json(STATE_FILE, state)


def load_keywords() -> dict:
    data = yaml.safe_load(KEYWORDS_FILE.read_text(encoding="utf-8")) or {}
    data.setdefault("backlog", [])
    data.setdefault("done", [])
    return data


def save_keywords(data: dict) -> None:
    header = (
        "# Backlog de mots-clés. Alimenté automatiquement par Search Console et Claude.\n"
    )
    KEYWORDS_FILE.write_text(
        header + yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )


def normalize_query(q: str) -> str:
    q = unicodedata.normalize("NFKD", q.lower()).encode("ascii", "ignore").decode()
    return " ".join(re.findall(r"[a-z0-9]+", q))


def similarity(a: str, b: str) -> float:
    """Jaccard similarity on word sets — cheap duplicate/cannibalisation check."""
    sa, sb = set(normalize_query(a).split()), set(normalize_query(b).split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


# --- Claude -----------------------------------------------------------------

def ask_claude(system: str, prompt: str, *, web_search: bool = False, max_tokens: int = 32000) -> str:
    """Single Claude request (with optional web search), returns the final text."""
    import anthropic

    cfg = load_config()["llm"]
    client = anthropic.Anthropic()
    tools = []
    if web_search:
        tools.append({
            "type": "web_search_20260209",
            "name": "web_search",
            "max_uses": cfg["max_web_searches"],
        })
    messages = [{"role": "user", "content": prompt}]

    # Server tools can pause a long turn; resume until the model finishes.
    for _ in range(5):
        with client.beta.messages.stream(
            model=cfg["model"],
            max_tokens=max_tokens,
            system=system,
            messages=messages,
            tools=tools,
            thinking={"type": "adaptive"},
            output_config={"effort": cfg["effort"]},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        ) as stream:
            response = stream.get_final_message()
        if response.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": response.content})
            continue
        break

    if response.stop_reason == "refusal":
        raise RuntimeError(f"Claude refused: {response.stop_details}")
    if response.stop_reason == "max_tokens":
        raise RuntimeError("Claude hit max_tokens; output truncated")
    return "".join(b.text for b in response.content if b.type == "text").strip()


def extract_json(text: str):
    """Pull the first JSON object/array out of a model reply."""
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        text = m.group(1)
    start = min([i for i in (text.find("{"), text.find("[")) if i >= 0], default=-1)
    if start < 0:
        raise ValueError("no JSON in reply")
    return json.JSONDecoder().raw_decode(text[start:])[0]
