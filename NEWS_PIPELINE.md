# Open-source Aggregation Pipeline

This pipeline supports compliant aggregation for ScholarNotion:

- Primary mode: ingest reusable RSS/Atom metadata from approved sources.
- Secondary mode: human-written summaries and commentary.

## Source configuration

Edit:

`/Users/jasper/Documents/codex/scholarnotion/data/open_sources.json`

Only include sources with terms that allow redistribution of metadata/snippets.

## Step 1: Aggregate and generate drafts

```bash
cd /Users/jasper/Documents/codex/scholarnotion
python3 scripts/aggregate_open_sources.py --max-per-source 5
```

Outputs:

- Archive: `/Users/jasper/Documents/codex/scholarnotion/data/aggregator/archive.jsonl`
- Latest batch: `/Users/jasper/Documents/codex/scholarnotion/data/aggregator/latest_batch.json`
- Drafts: `/Users/jasper/Documents/codex/scholarnotion/content/insight_drafts/YYYY-MM-DD/*.md`

## Step 2: Write commentary

For each generated draft:

- Fill in `Why it matters`
- Fill in `Commentary`
- Keep any quotation short and attributed

## Step 3: Build a publishable issue page

```bash
cd /Users/jasper/Documents/codex/scholarnotion
python3 scripts/build_insight_issue.py --date 2026-02-15
```

Outputs:

- Published page: `/Users/jasper/Documents/codex/scholarnotion/pages/insights-issue-2026-02-15.html`
- Issue record: `/Users/jasper/Documents/codex/scholarnotion/content/insight_issues/2026-02-15.md`

## Step 4: Release with timestamp tag

```bash
cd /Users/jasper/Documents/codex/scholarnotion
./scripts/release.sh https://scholarnotion.com "feat: publish insights issue"
```

Tag format is automatic:

- `rel-YYYYMMDD-HHMMSS-utc`
