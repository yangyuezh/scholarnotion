#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: ./scripts/release.sh <domain> <commit-message> [tag]"
  echo "Example: ./scripts/release.sh https://scholarnotion.com \"feat: add weekly news\" v0.1.1"
  exit 1
fi

DOMAIN="$1"
MESSAGE="$2"
TAG="${3:-}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python3 scripts/check_internal_links.py
python3 scripts/generate_sitemap.py --domain "$DOMAIN"

git add .
git commit -m "$MESSAGE"
git push origin main

if [[ -n "$TAG" ]]; then
  git tag -a "$TAG" -m "$MESSAGE"
  git push origin "$TAG"
fi

echo "Release complete."
