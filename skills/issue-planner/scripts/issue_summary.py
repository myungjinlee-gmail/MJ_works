#!/usr/bin/env python3
"""Build and verify a compact managed summary in a GitHub issue body."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass


START_MARKER = "<!-- issue-planner:summary:start -->"
END_MARKER = "<!-- issue-planner:summary:end -->"
REQUIREMENTS_PATH = re.compile(r"plan/[1-9][0-9]*/issue\.md")
SUMMARY_HEADING = re.compile(r"(?m)^## Planning summary\s*$")
PLACEHOLDER = re.compile(r"<[^>\n]+>|\b(?:TBD|TODO|Pending)\b", re.IGNORECASE)


def _items(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a non-empty array")
    if any(
        not isinstance(item, str) or not item.strip() or "\n" in item
        for item in value
    ):
        raise ValueError(f"{label} items must be non-empty single-line strings")
    items = tuple(item.strip() for item in value)
    if len(items) != len(set(items)):
        raise ValueError(f"{label} items must be unique")
    return items


@dataclass(frozen=True)
class IssueSummary:
    purpose: str
    scope: tuple[str, ...]
    expected_outcomes: tuple[str, ...]
    acceptance_summary: tuple[str, ...]
    detailed_requirements: str

    @classmethod
    def from_dict(cls, value: object) -> "IssueSummary":
        if not isinstance(value, dict):
            raise ValueError("summary must be an object")
        purpose = value.get("purpose")
        detailed_requirements = value.get("detailed_requirements")
        if not isinstance(purpose, str) or not purpose.strip():
            raise ValueError("summary.purpose must be a non-empty string")
        if (
            not isinstance(detailed_requirements, str)
            or not REQUIREMENTS_PATH.fullmatch(detailed_requirements)
        ):
            raise ValueError(
                "summary.detailed_requirements must match plan/ISSUE_NUMBER/issue.md"
            )
        summary = cls(
            purpose=purpose.strip(),
            scope=_items(value.get("scope"), "summary.scope"),
            expected_outcomes=_items(
                value.get("expected_outcomes"),
                "summary.expected_outcomes",
            ),
            acceptance_summary=_items(
                value.get("acceptance_summary"),
                "summary.acceptance_summary",
            ),
            detailed_requirements=detailed_requirements,
        )
        summary.validate()
        return summary

    def validate(self) -> None:
        if not self.purpose.strip():
            raise ValueError("summary.purpose must be non-empty")
        if not REQUIREMENTS_PATH.fullmatch(self.detailed_requirements):
            raise ValueError("summary.detailed_requirements path is invalid")
        for label, items in (
            ("scope", self.scope),
            ("expected_outcomes", self.expected_outcomes),
            ("acceptance_summary", self.acceptance_summary),
        ):
            if (
                not items
                or any(not item.strip() or "\n" in item for item in items)
                or len(items) != len(set(items))
            ):
                raise ValueError(f"summary.{label} contains invalid items")
        combined = "\n".join(
            (
                self.purpose,
                *self.scope,
                *self.expected_outcomes,
                *self.acceptance_summary,
            )
        )
        if START_MARKER in combined or END_MARKER in combined:
            raise ValueError("summary content must not contain managed markers")
        if PLACEHOLDER.search(combined):
            raise ValueError("summary content must not contain placeholders")

    def render(self) -> str:
        self.validate()
        return (
            f"{START_MARKER}\n\n"
            "## Planning summary\n\n"
            "### Purpose\n\n"
            f"{self.purpose}\n\n"
            "### Scope\n\n"
            f"{_markdown_list(self.scope)}\n\n"
            "### Expected outcomes\n\n"
            f"{_markdown_list(self.expected_outcomes)}\n\n"
            "### Acceptance summary\n\n"
            f"{_markdown_list(self.acceptance_summary)}\n\n"
            "### Detailed requirements\n\n"
            f"See `{self.detailed_requirements}` in the related Pull Request.\n\n"
            f"{END_MARKER}"
        )


def _markdown_list(items: tuple[str, ...]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _managed_span(body: str) -> tuple[int, int] | None:
    start_count = body.count(START_MARKER)
    end_count = body.count(END_MARKER)
    if start_count == 0 and end_count == 0:
        return None
    if start_count != 1 or end_count != 1:
        raise ValueError("managed summary markers must occur exactly once as a pair")
    start = body.index(START_MARKER)
    end_start = body.index(END_MARKER)
    if end_start < start:
        raise ValueError("managed summary end marker precedes its start marker")
    return start, end_start + len(END_MARKER)


def build_candidate(body: str, summary: IssueSummary) -> str:
    block = summary.render()
    span = _managed_span(body)
    if span is not None:
        start, end = span
        return body[:start] + block + body[end:]
    if SUMMARY_HEADING.search(body):
        raise ValueError("unmanaged Planning summary heading already exists")
    if not body:
        return block
    if body.endswith("\n\n"):
        separator = ""
    elif body.endswith("\n"):
        separator = "\n"
    else:
        separator = "\n\n"
    return body + separator + block


def verify_candidate(body: str, summary: IssueSummary, candidate: str) -> None:
    expected = build_candidate(body, summary)
    if candidate != expected:
        raise ValueError("candidate changes content outside the managed summary")
    _managed_span(candidate)


def parse_payload(payload: object) -> tuple[str, IssueSummary]:
    if not isinstance(payload, dict) or not isinstance(payload.get("body"), str):
        raise ValueError("payload requires a body string")
    return str(payload["body"]), IssueSummary.from_dict(payload.get("summary"))


def self_test() -> None:
    body = "## Purpose\n\nKeep the web issue concise."
    summary = IssueSummary.from_dict(
        {
            "purpose": "Keep planning details local while preserving review scope.",
            "scope": ["Maintain a concise issue-level contract."],
            "expected_outcomes": ["The Pull Request traces to local requirements."],
            "acceptance_summary": ["SCOPE, TRACE, and VERIFY have evidence."],
            "detailed_requirements": "plan/45/issue.md",
        }
    )
    candidate = build_candidate(body, summary)
    verify_candidate(body, summary, candidate)
    assert candidate.startswith(body)
    assert candidate.count(START_MARKER) == 1

    revised = IssueSummary.from_dict(
        {
            "purpose": "Keep the issue abstract and reviewable.",
            "scope": ["Publish only externally meaningful outcomes."],
            "expected_outcomes": ["Detailed requirements remain local."],
            "acceptance_summary": ["The PR remains traceable to the issue."],
            "detailed_requirements": "plan/45/issue.md",
        }
    )
    updated = build_candidate(candidate, revised)
    verify_candidate(candidate, revised, updated)
    assert updated.startswith(body)
    assert summary.purpose not in updated
    assert revised.purpose in updated

    malformed = body + "\n\n" + START_MARKER
    try:
        build_candidate(malformed, summary)
    except ValueError:
        pass
    else:
        raise AssertionError("malformed managed markers must fail")

    try:
        build_candidate(body + "\n\n## Planning summary\n", summary)
    except ValueError:
        pass
    else:
        raise AssertionError("unmanaged summary headings must fail")

    try:
        IssueSummary.from_dict(
            {
                "purpose": "Purpose",
                "scope": ["Scope"],
                "expected_outcomes": ["Outcome"],
                "acceptance_summary": ["Acceptance"],
                "detailed_requirements": "issue.md",
            }
        )
    except ValueError:
        pass
    else:
        raise AssertionError("invalid detailed requirement paths must fail")

    try:
        IssueSummary.from_dict(
            {
                "purpose": "<purpose>",
                "scope": ["Scope"],
                "expected_outcomes": ["Outcome"],
                "acceptance_summary": ["Acceptance"],
                "detailed_requirements": "plan/45/issue.md",
            }
        )
    except ValueError:
        pass
    else:
        raise AssertionError("summary placeholders must fail")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("build", "verify", "self-test"))
    parser.add_argument(
        "--payload-hex",
        help="UTF-8 JSON payload encoded as hexadecimal; otherwise read stdin",
    )
    args = parser.parse_args()
    if args.mode == "self-test":
        self_test()
        print("self-test passed")
        return 0
    if args.payload_hex:
        payload = json.loads(bytes.fromhex(args.payload_hex).decode("utf-8"))
    else:
        payload = json.load(sys.stdin)
    body, summary = parse_payload(payload)
    if args.mode == "build":
        sys.stdout.write(build_candidate(body, summary))
        return 0
    candidate = payload.get("candidate")
    if not isinstance(candidate, str):
        raise ValueError("verify payload requires a candidate string")
    verify_candidate(body, summary, candidate)
    print("candidate verified")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
