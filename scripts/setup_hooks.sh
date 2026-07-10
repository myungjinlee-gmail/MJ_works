#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(git -C "${script_dir}" rev-parse --show-toplevel 2>/dev/null || true)"

if [[ -z "${repo_root}" ]]; then
  echo "Not inside a Git repository; skipping hook setup."
  exit 0
fi

git -C "${repo_root}" config core.hooksPath githooks
chmod +x "${repo_root}/githooks/commit-msg"

echo "Git hooks path set to githooks."
