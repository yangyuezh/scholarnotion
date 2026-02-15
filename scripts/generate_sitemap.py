#!/usr/bin/env python3
from pathlib import Path
import argparse
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True, help="example: https://scholarnotion.com")
    args = parser.parse_args()

    domain = args.domain.rstrip("/")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    html_files = sorted(ROOT.rglob("*.html"))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for file in html_files:
        rel = file.relative_to(ROOT).as_posix()
        path = "/" if rel == "index.html" else f"/{rel}"
        lines.append("  <url>")
        lines.append(f"    <loc>{domain}{path}</loc>")
        lines.append(f"    <lastmod>{now}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")

    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Generated sitemap.xml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
