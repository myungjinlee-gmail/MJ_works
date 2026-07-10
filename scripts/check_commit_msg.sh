#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 1 ]]; then
  echo "Usage: $0 <commit-message-file>" >&2
  exit 2
fi

commit_msg_file="$1"

if [[ ! -f "${commit_msg_file}" ]]; then
  echo "Commit message file not found: ${commit_msg_file}" >&2
  exit 2
fi

first_line="$(sed -n '1p' "${commit_msg_file}")"
commit_msg_regex='^\(#[0-9]+\) .+'

if [[ "${first_line}" =~ ${commit_msg_regex} ]]; then
  exit 0
fi

cat >&2 <<'EOF'
Invalid commit message.

Expected format:
  (#<issue-no>) <summary>

Examples:
  (#12) add cmake hardware target selection
  (#18) handle null display backend

See docs/process/git_workflow.md for the commit message rule.
EOF

exit 1
