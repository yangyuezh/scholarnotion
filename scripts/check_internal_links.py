#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        for key, value in attrs:
            if key == "href" and value:
                self.links.append(value)


def is_internal(href: str) -> bool:
    if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
        return False
    return href.startswith("/") or href.endswith(".html")


def resolve_target(href: str, current_file: Path) -> Path:
    clean = href.split("#", 1)[0].split("?", 1)[0]
    if clean.startswith("/"):
        return ROOT / clean.lstrip("/")
    return (current_file.parent / clean).resolve()


def main() -> int:
    html_files = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]
    missing = []
    for file in html_files:
        parser = LinkParser()
        parser.feed(file.read_text(encoding="utf-8"))
        for href in parser.links:
            if not is_internal(href):
                continue
            target = resolve_target(href, file)
            if not target.exists():
                missing.append((file.relative_to(ROOT), href))

    if missing:
        print("Broken internal links:")
        for page, href in missing:
            print(f"- {page}: {href}")
        return 1

    print("Internal link check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
