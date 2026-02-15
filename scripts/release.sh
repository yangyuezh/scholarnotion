#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: ./scripts/release.sh <domain> <commit-message> [tag-prefix]"
  echo "Example: ./scripts/release.sh https://scholarnotion.com \"feat: add weekly news\" rel"
  exit 1
fi

DOMAIN="$1"
MESSAGE="$2"
TAG_PREFIX="${3:-rel}"
TS_UTC="$(date -u +%Y%m%d-%H%M%S)"
TAG="${TAG_PREFIX}-${TS_UTC}-utc"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python3 scripts/check_internal_links.py
python3 scripts/generate_sitemap.py --domain "$DOMAIN"

git add .
git commit -m "$MESSAGE"
git push origin main

git tag -a "$TAG" -m "$MESSAGE | tag_time_utc=$TS_UTC"
git push origin "$TAG"

echo "Release complete: $TAG"
