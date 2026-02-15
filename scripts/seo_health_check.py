#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract(pattern: str, text: str):
    m = re.search(pattern, text, flags=re.I | re.S)
    return m.group(1).strip() if m else ""


def check_file(path: Path, domain: str):
    text = path.read_text(encoding="utf-8")
    title = extract(r"<title>(.*?)</title>", text)
    desc = extract(r'<meta\s+name="description"\s+content="(.*?)"', text)
    canonical = extract(r'<link\s+rel="canonical"\s+href="(.*?)"', text)

    issues = []
    if not title:
        issues.append("missing_title")
    if not desc:
        issues.append("missing_meta_description")
    if canonical and not canonical.startswith(domain):
        issues.append("canonical_not_on_primary_domain")

    return {
        "file": str(path.relative_to(ROOT)),
        "title": title,
        "has_description": bool(desc),
        "canonical": canonical,
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(description="Basic SEO health check for static HTML pages")
    parser.add_argument("--domain", required=True)
    parser.add_argument("--output", default="reports/seo-health.json")
    args = parser.parse_args()

    html_files = sorted([p for p in ROOT.rglob("*.html") if ".git" not in p.parts])
    results = [check_file(p, args.domain.rstrip("/")) for p in html_files]

    total = len(results)
    issue_pages = [r for r in results if r["issues"]]
    summary = {
        "total_pages": total,
        "pages_with_issues": len(issue_pages),
        "issue_rate": round((len(issue_pages) / total) * 100, 2) if total else 0,
    }

    out = {
        "summary": summary,
        "pages": results,
    }

    out_path = ROOT / args.output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(json.dumps(summary))
    if issue_pages:
        print("Pages with issues:")
        for p in issue_pages[:20]:
            print(f"- {p['file']}: {', '.join(p['issues'])}")


if __name__ == "__main__":
    main()
