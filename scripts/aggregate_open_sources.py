#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "open_sources.json"
ARCHIVE_PATH = ROOT / "data" / "aggregator" / "archive.jsonl"
BATCH_PATH = ROOT / "data" / "aggregator" / "latest_batch.json"
DRAFT_DIR = ROOT / "content" / "insight_drafts"


def load_config():
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def fetch_xml(url: str, timeout: int) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ScholarNotionBot/1.0 (+https://scholarnotion.com)"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _text(elem, tag, default=""):
    found = elem.find(tag)
    if found is None:
        return default
    return (found.text or "").strip()


def _sanitize(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_rss(root: ET.Element):
    out = []
    channel = root.find("channel")
    if channel is None:
        return out
    for item in channel.findall("item"):
        title = _sanitize(_text(item, "title"))
        link = _text(item, "link")
        pub = _text(item, "pubDate")
        summary = _sanitize(_text(item, "description"))
        author = _text(item, "author")
        out.append(
            {
                "title": title,
                "url": link,
                "published": pub,
                "summary": summary,
                "authors": author,
            }
        )
    return out


def parse_atom(root: ET.Element):
    out = []
    ns = {"a": "http://www.w3.org/2005/Atom"}
    entries = root.findall("a:entry", ns)
    for entry in entries:
        title = _sanitize(_text(entry, "{http://www.w3.org/2005/Atom}title"))
        link = ""
        for l in entry.findall("a:link", ns):
            if l.get("rel") in (None, "alternate"):
                link = l.get("href", "")
                if link:
                    break
        pub = _text(entry, "{http://www.w3.org/2005/Atom}updated") or _text(
            entry, "{http://www.w3.org/2005/Atom}published"
        )
        summary = _sanitize(
            _text(entry, "{http://www.w3.org/2005/Atom}summary")
            or _text(entry, "{http://www.w3.org/2005/Atom}content")
        )
        authors = []
        for a in entry.findall("a:author", ns):
            n = _text(a, "{http://www.w3.org/2005/Atom}name")
            if n:
                authors.append(n)
        out.append(
            {
                "title": title,
                "url": link,
                "published": pub,
                "summary": summary,
                "authors": ", ".join(authors),
            }
        )
    return out


def parse_feed(xml_bytes: bytes):
    root = ET.fromstring(xml_bytes)
    tag = root.tag.lower()
    if tag.endswith("rss"):
        return parse_rss(root)
    if tag.endswith("feed"):
        return parse_atom(root)
    return []


def dedupe_key(source_id: str, url: str, title: str):
    raw = f"{source_id}|{url.strip()}|{title.strip()}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()


def load_archive_keys():
    if not ARCHIVE_PATH.exists():
        return set()
    keys = set()
    with ARCHIVE_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            k = obj.get("dedupe_key")
            if k:
                keys.add(k)
    return keys


def append_archive(records):
    ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ARCHIVE_PATH.open("a", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def slugify(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:70] or "item"


def create_draft(rec):
    day = dt.date.today().isoformat()
    folder = DRAFT_DIR / day
    folder.mkdir(parents=True, exist_ok=True)
    filename = f"{slugify(rec['title'])}-{rec['dedupe_key'][:8]}.md"
    path = folder / filename
    if path.exists():
        return str(path)

    summary = rec.get("summary", "")[:400]
    text = f"""---
source_id: {rec['source_id']}
source_name: {rec['source_name']}
source_url: {rec['url']}
published_at: \"{rec.get('published', '')}\"
license_note: \"{rec.get('license_note', '')}\"
dedupe_key: {rec['dedupe_key']}
created_at_utc: \"{dt.datetime.utcnow().isoformat()}Z\"
status: draft
---

# {rec['title']}

## What happened
{summary if summary else 'TODO: add a factual summary based on metadata and source context.'}

## Why it matters
TODO: add your analysis in your own words.

## Commentary
TODO: add your editorial perspective and link to related charts.

## Source
- Original link: {rec['url']}
- Attribution: {rec['source_name']}
- License/terms note: {rec.get('license_note','')}

## Quotation rule
Use short quotations only when necessary; keep each quote under policy limits and always attribute.
"""
    path.write_text(text, encoding="utf-8")
    return str(path)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch open-license feeds, dedupe, archive, and generate insight drafts."
    )
    parser.add_argument("--max-per-source", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cfg = load_config()
    existing = load_archive_keys()
    added = []

    for src in cfg.get("sources", []):
        try:
            xml_bytes = fetch_xml(src["feed_url"], args.timeout)
            entries = parse_feed(xml_bytes)
        except Exception as e:
            print(f"[warn] {src['id']}: fetch/parse failed: {e}")
            continue

        count = 0
        for e in entries:
            if count >= args.max_per_source:
                break
            k = dedupe_key(src["id"], e.get("url", ""), e.get("title", ""))
            if not e.get("url") or k in existing:
                continue
            rec = {
                "dedupe_key": k,
                "source_id": src["id"],
                "source_name": src["name"],
                "license_note": src.get("license_note", ""),
                "fetched_at_utc": dt.datetime.utcnow().isoformat() + "Z",
                **e,
            }
            added.append(rec)
            existing.add(k)
            count += 1

    BATCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    BATCH_PATH.write_text(json.dumps(added, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.dry_run:
        print(f"dry-run: {len(added)} new items")
        return

    if added:
        append_archive(added)

    drafts = [create_draft(r) for r in added]
    print(f"new_items={len(added)}")
    print(f"drafts_created={len(drafts)}")
    for d in drafts:
        print(f"- {d}")


if __name__ == "__main__":
    main()
