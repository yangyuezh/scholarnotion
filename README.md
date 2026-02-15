# ScholarNotion

ScholarNotion is an OWID-inspired, data-first website deployed on Cloudflare.

## Local preview

```bash
cd /Users/jasper/Documents/codex/scholarnotion
python3 -m http.server 4173
```

Open `http://localhost:4173`.

## Deployment

This repo is connected to Cloudflare. Any push to `main` triggers automatic deployment.

## Release command (with timestamp tag)

```bash
cd /Users/jasper/Documents/codex/scholarnotion
./scripts/release.sh https://scholarnotion.com "feat: your update summary"
```

Each release auto-creates and pushes an annotated UTC tag:

- `rel-YYYYMMDD-HHMMSS-utc`

## Open-source aggregation pipeline

Primary mode:

- Use reusable RSS/Atom metadata feeds from approved sources.
- Deduplicate, archive, and generate draft insight files.

Secondary mode:

- Human-written summaries and commentary.
- Short attributed quotations only when needed.

Runbook:

- `/Users/jasper/Documents/codex/scholarnotion/NEWS_PIPELINE.md`

Source configuration:

- `/Users/jasper/Documents/codex/scholarnotion/data/open_sources.json`

## Hourly automation

GitHub Actions runs hourly via:

- `/Users/jasper/Documents/codex/scholarnotion/.github/workflows/hourly-growth.yml`

The job performs:

- open-source feed aggregation and dedupe
- internal link check
- sitemap regeneration
- SEO health report generation
