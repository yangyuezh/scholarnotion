#!/usr/bin/env python3
import argparse
import datetime as dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT_ROOT = ROOT / "content" / "insight_drafts"
ISSUE_ROOT = ROOT / "content" / "insight_issues"
PAGES_ROOT = ROOT / "pages"


def parse_markdown(path: Path):
    text = path.read_text(encoding="utf-8")
    title = "Untitled"
    for line in text.splitlines():
      if line.startswith("# "):
        title = line[2:].strip()
        break
    def section(name):
        pat = rf"## {re.escape(name)}\n(.*?)(\n## |\Z)"
        m = re.search(pat, text, flags=re.S)
        if not m:
            return ""
        return m.group(1).strip()
    return {
        "title": title,
        "what": section("What happened"),
        "why": section("Why it matters"),
        "commentary": section("Commentary"),
        "source": section("Source"),
        "path": str(path),
    }


def escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def md_to_html_block(md_text: str) -> str:
    lines = [l.strip() for l in md_text.splitlines() if l.strip()]
    out = []
    for ln in lines:
        if ln.startswith("- "):
            out.append(f"<li>{escape_html(ln[2:])}</li>")
        else:
            out.append(f"<p>{escape_html(ln)}</p>")
    if out and out[0].startswith("<li>"):
        return "<ul class=\"list\">" + "".join(out) + "</ul>"
    return "".join(out)


def build_issue_html(issue_date: str, items):
    cards = []
    for i, item in enumerate(items, start=1):
        cards.append(
            f"""
      <section class=\"section\">
        <article class=\"card\">
          <h3>{i}) {escape_html(item['title'])}</h3>
          <h4>What happened</h4>
          {md_to_html_block(item['what'])}
          <h4>Why it matters</h4>
          {md_to_html_block(item['why'])}
          <h4>Commentary</h4>
          {md_to_html_block(item['commentary'])}
          <h4>Source</h4>
          {md_to_html_block(item['source'])}
          <p class=\"metric\">Draft source: {escape_html(item['path'])}</p>
        </article>
      </section>
      """
        )

    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>Insights Issue {issue_date} | ScholarNotion</title>
    <link rel=\"stylesheet\" href=\"/assets/css/styles.css\" />
  </head>
  <body>
    <header class=\"site-header\">
      <div class=\"container nav\">
        <a class=\"brand\" href=\"/\">ScholarNotion</a>
        <nav class=\"menu\">
          <a href=\"/pages/topics.html\">Topics</a>
          <a href=\"/pages/charts.html\">Charts</a>
          <a href=\"/pages/insights.html\">Insights</a>
          <a href=\"/pages/explorer.html\">Explorer</a>
          <a href=\"/pages/methodology.html\">Methodology</a>
        </nav>
        <a class=\"search-chip\" href=\"/pages/charts.html\">Search data</a>
      </div>
    </header>
    <main class=\"container\">
      <section class=\"page-title\">
        <h1>Insights Issue {issue_date}</h1>
        <p>Generated from reviewed drafts with source attribution.</p>
      </section>
      {''.join(cards)}
    </main>
  </body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Build an issue page from reviewed insight drafts.")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--draft-dir", default="")
    args = parser.parse_args()

    draft_dir = Path(args.draft_dir) if args.draft_dir else DRAFT_ROOT / args.date
    if not draft_dir.exists():
        raise SystemExit(f"Draft directory not found: {draft_dir}")

    drafts = sorted(draft_dir.glob("*.md"))
    if not drafts:
        raise SystemExit(f"No drafts found in: {draft_dir}")

    items = [parse_markdown(d) for d in drafts]

    issue_name = f"insights-issue-{args.date}.html"
    page_path = PAGES_ROOT / issue_name
    issue_index_path = ISSUE_ROOT / f"{args.date}.md"
    ISSUE_ROOT.mkdir(parents=True, exist_ok=True)

    page_path.write_text(build_issue_html(args.date, items), encoding="utf-8")

    lines = [f"# Insights issue {args.date}", "", "Drafts included:"]
    for d in drafts:
        lines.append(f"- {d}")
    lines.append("")
    lines.append(f"Published page: {page_path}")
    issue_index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"published_page={page_path}")
    print(f"issue_record={issue_index_path}")


if __name__ == "__main__":
    main()
