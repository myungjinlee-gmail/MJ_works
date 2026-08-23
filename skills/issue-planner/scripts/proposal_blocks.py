#!/usr/bin/env python3
"""Build and verify nearest-target [Proposal] insertions for issue planning."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass


PROPOSAL_ID = re.compile(r"P-[0-9]{3,}")
PROPOSAL_MARKER = re.compile(
    r"(?m)^<!-- proposal:(P-[0-9]{3,}):(start|end) -->\s*$"
)
PROPOSAL_ACTIONS = {"add", "replace", "remove"}


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    action: str
    target: str
    title: str
    content: str
    rationale: str

    def validate(self) -> None:
        if not PROPOSAL_ID.fullmatch(self.proposal_id):
            raise ValueError(f"invalid proposal id: {self.proposal_id}")
        if self.action not in PROPOSAL_ACTIONS:
            raise ValueError(
                f"invalid action for {self.proposal_id}: {self.action}"
            )
        if not self.target.strip():
            raise ValueError(f"empty target for {self.proposal_id}")
        if (
            not self.title.strip()
            or not self.content.strip()
            or not self.rationale.strip()
        ):
            raise ValueError(
                f"empty title, content, or rationale for {self.proposal_id}"
            )
        if self.action == "remove" and self.content.strip() != "None.":
            raise ValueError(
                f"remove proposal {self.proposal_id} must use content None."
            )
        if self.action in {"add", "replace"} and self.content.strip() == "None.":
            raise ValueError(
                f"{self.action} proposal {self.proposal_id} requires content"
            )

    @classmethod
    def from_dict(cls, value: dict[str, object]) -> "Proposal":
        if not isinstance(value, dict):
            raise ValueError("each proposal must be an object")
        required = ("id", "action", "target", "title", "content", "rationale")
        if any(not isinstance(value.get(key), str) for key in required):
            raise ValueError(
                "each proposal requires string id, action, target, title, "
                "content, and rationale"
            )
        proposal = cls(
            proposal_id=str(value["id"]),
            action=str(value["action"]),
            target=str(value["target"]),
            title=str(value["title"]),
            content=str(value["content"]),
            rationale=str(value["rationale"]),
        )
        proposal.validate()
        return proposal

    def insertion(self) -> str:
        quoted_target = self.quoted_target()
        return (
            f"\n\n<!-- proposal:{self.proposal_id}:start -->\n\n"
            f"**[Proposal] {self.proposal_id}: {self.title.strip()}**\n\n"
            f"**Action**\n\n{self.action}\n\n"
            f"**Target**\n\n{quoted_target}\n\n"
            f"**Proposed change**\n\n{self.content.strip()}\n\n"
            f"**Rationale**\n\n{self.rationale.strip()}\n\n"
            f"<!-- proposal:{self.proposal_id}:end -->\n"
        )

    def quoted_target(self) -> str:
        return "\n".join(
            f"> {line}" if line else ">" for line in self.target.splitlines()
        )


def parse_payload(payload: object) -> tuple[str, list[Proposal]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("original"), str):
        raise ValueError("payload requires an original string")
    raw_proposals = payload.get("proposals")
    if not isinstance(raw_proposals, list):
        raise ValueError("payload requires a proposals array")
    proposals = [Proposal.from_dict(value) for value in raw_proposals]
    return str(payload["original"]), proposals


def build_issue_document(title: str, body: str) -> str:
    if not title or "\n" in title or "\r" in title:
        raise ValueError("issue title must be a non-empty single line")
    return f"# {title}\n\n{body}"


def parse_issue_document_payload(payload: object) -> tuple[str, str]:
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")
    title = payload.get("title")
    body = payload.get("body")
    if not isinstance(title, str) or not isinstance(body, str):
        raise ValueError("payload requires title and body strings")
    return title, body


def verify_issue_document(title: str, body: str, candidate: str) -> None:
    if candidate != build_issue_document(title, body):
        raise ValueError("issue.md does not exactly preserve the title and body")


def proposal_spans(original: str) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    active: tuple[str, int] | None = None
    seen_ids: set[str] = set()
    for match in PROPOSAL_MARKER.finditer(original):
        proposal_id, boundary = match.groups()
        if boundary == "start":
            if active is not None:
                raise ValueError("proposal blocks must not be nested")
            active = (proposal_id, match.start())
            continue
        if active is None:
            raise ValueError(f"proposal end marker has no start: {proposal_id}")
        active_id, start = active
        if proposal_id != active_id:
            raise ValueError(
                f"proposal marker mismatch: {active_id} ends as {proposal_id}"
            )
        if proposal_id in seen_ids:
            raise ValueError(f"duplicate proposal markers: {proposal_id}")
        seen_ids.add(proposal_id)
        spans.append((start, match.end(), proposal_id))
        active = None
    if active is not None:
        raise ValueError(f"proposal start marker has no end: {active[0]}")
    return spans


def target_positions(
    original: str,
    target: str,
    spans: list[tuple[int, int, str]],
) -> list[int]:
    positions: list[int] = []
    start = 0
    while True:
        position = original.find(target, start)
        if position < 0:
            return positions
        end = position + len(target)
        if not any(
            span_start < end and position < span_end
            for span_start, span_end, _ in spans
        ):
            positions.append(position)
        start = position + 1


def validate_inputs(original: str, proposals: list[Proposal]) -> None:
    spans = proposal_spans(original)
    for proposal in proposals:
        proposal.validate()
    new_numbers = [
        int(proposal.proposal_id.split("-", 1)[1]) for proposal in proposals
    ]
    if new_numbers != sorted(new_numbers):
        raise ValueError("new proposal ids must be in ascending order")
    existing_numbers = [
        int(proposal_id.split("-", 1)[1]) for _, _, proposal_id in spans
    ]
    if existing_numbers and new_numbers and min(new_numbers) <= max(existing_numbers):
        raise ValueError("new proposal ids must continue after the highest existing id")
    ids: set[str] = set()
    signatures: set[tuple[str, str, str]] = set()
    targets: set[str] = set()
    for proposal in proposals:
        if proposal.proposal_id in ids:
            raise ValueError("proposal ids must be unique")
        ids.add(proposal.proposal_id)
        signature = (proposal.action, proposal.target, proposal.content.strip())
        if signature in signatures:
            raise ValueError("materially equivalent proposals are not allowed")
        signatures.add(signature)
        if proposal.target in targets:
            raise ValueError("each proposal must have an exclusive target")
        targets.add(proposal.target)
        positions = target_positions(original, proposal.target, spans)
        if len(positions) != 1:
            raise ValueError(
                f"target for {proposal.proposal_id} must occur exactly once "
                "outside Proposal blocks"
            )
        target_field = f"**Target**\n\n{proposal.quoted_target()}\n\n"
        if any(target_field in original[start:end] for start, end, _ in spans):
            raise ValueError("each proposal must have an exclusive target")
        markers = (
            f"<!-- proposal:{proposal.proposal_id}:start -->",
            f"**[Proposal] {proposal.proposal_id}:",
            f"#### [Proposal] {proposal.proposal_id}:",
            f"#### [Propose] {proposal.proposal_id}:",
        )
        if any(marker in original for marker in markers):
            raise ValueError(f"proposal id already exists: {proposal.proposal_id}")


def build_candidate(original: str, proposals: list[Proposal]) -> str:
    validate_inputs(original, proposals)
    spans = proposal_spans(original)
    grouped: dict[int, list[Proposal]] = {}
    for proposal in proposals:
        position = target_positions(original, proposal.target, spans)[0]
        position += len(proposal.target)
        grouped.setdefault(position, []).append(proposal)

    candidate = original
    for position in sorted(grouped, reverse=True):
        insertion = "".join(item.insertion() for item in grouped[position])
        candidate = candidate[:position] + insertion + candidate[position:]
    verify_candidate(original, proposals, candidate)
    return candidate


def verify_candidate(
    original: str, proposals: list[Proposal], candidate: str
) -> None:
    validate_inputs(original, proposals)
    restored = candidate
    for proposal in reversed(proposals):
        insertion = proposal.insertion()
        if restored.count(insertion) != 1:
            raise ValueError(
                f"candidate must contain {proposal.proposal_id} exactly once"
            )
        restored = restored.replace(insertion, "", 1)
    if restored != original:
        raise ValueError("candidate changes content outside proposal insertions")


def resolve_proposal(candidate: str, proposal: Proposal, decision: str) -> str:
    proposal.validate()
    if decision not in {"accept", "reject"}:
        raise ValueError("proposal decision must be accept or reject")
    spans = proposal_spans(candidate)
    insertion = proposal.insertion()
    if candidate.count(insertion) != 1:
        raise ValueError(
            f"candidate must contain {proposal.proposal_id} exactly once"
        )
    if candidate.count(proposal.target + insertion) != 1:
        raise ValueError(
            f"proposal {proposal.proposal_id} is not immediately after its target"
        )
    positions = target_positions(candidate, proposal.target, spans)
    if len(positions) != 1:
        raise ValueError(
            f"target for {proposal.proposal_id} must occur exactly once "
            "outside Proposal blocks"
        )
    if decision == "reject":
        resolved = candidate.replace(insertion, "", 1)
    elif proposal.action == "add":
        replacement = f"\n\n{proposal.content.strip()}\n"
        resolved = candidate.replace(insertion, replacement, 1)
    else:
        without_proposal = candidate.replace(insertion, "", 1)
        position = target_positions(
            without_proposal,
            proposal.target,
            proposal_spans(without_proposal),
        )[0]
        replacement = proposal.content.strip() if proposal.action == "replace" else ""
        resolved = (
            without_proposal[:position]
            + replacement
            + without_proposal[position + len(proposal.target) :]
        )
    proposal_spans(resolved)
    if f"<!-- proposal:{proposal.proposal_id}:" in resolved:
        raise ValueError(f"proposal {proposal.proposal_id} was not fully resolved")
    return resolved


def self_test() -> None:
    issue_document = build_issue_document("Example issue", "### Purpose\n\n- Work")
    verify_issue_document("Example issue", "### Purpose\n\n- Work", issue_document)
    assert issue_document == "# Example issue\n\n### Purpose\n\n- Work"

    original = "### One\n\n- Alpha\n- Beta\n\n### Two\n\n- Gamma"
    proposals = [
        Proposal(
            "P-001",
            "add",
            "- Alpha",
            "Complete alpha",
            "- Alpha detail",
            "Alpha is incomplete.",
        ),
        Proposal(
            "P-002",
            "replace",
            "- Beta",
            "Correct beta",
            "- Corrected beta",
            "Beta contradicts the current behavior.",
        ),
        Proposal(
            "P-003",
            "remove",
            "- Gamma",
            "Remove gamma",
            "None.",
            "Gamma is outside the issue scope.",
        ),
    ]
    candidate = build_candidate(original, proposals)
    verify_candidate(original, proposals, candidate)
    assert candidate.index("proposal:P-001:end") < candidate.index("- Beta")
    assert candidate.index("P-001") < candidate.index("### Two")
    assert candidate.index("P-003") > candidate.index("### Two")
    assert "**Action**\n\nremove" in candidate
    assert "**Target**\n\n> - Gamma" in candidate
    try:
        build_candidate(
            original,
            [
                Proposal(
                    "P-004",
                    "add",
                    "missing",
                    "T",
                    "Content",
                    "Rationale",
                )
            ],
        )
    except ValueError:
        pass
    else:
        raise AssertionError("missing targets must fail")

    nested_original = (
        "<!-- proposal:P-010:start -->\n"
        "Inside\n"
        "<!-- proposal:P-010:end -->"
    )
    try:
        build_candidate(
            nested_original,
            [
                Proposal(
                    "P-011",
                    "remove",
                    "Inside",
                    "T",
                    "None.",
                    "Rationale",
                )
            ],
        )
    except ValueError:
        pass
    else:
        raise AssertionError("targets inside proposals must fail")

    follow_up = Proposal(
        "P-004",
        "add",
        "### One",
        "Add section context",
        "Section context.",
        "The section context is missing.",
    )
    follow_up_candidate = build_candidate(candidate, [follow_up])
    verify_candidate(candidate, [follow_up], follow_up_candidate)

    try:
        Proposal.from_dict(
            {
                "id": "P-005",
                "action": "delete",
                "target": "- Alpha",
                "title": "T",
                "content": "Content",
                "rationale": "Rationale",
            }
        )
    except ValueError:
        pass
    else:
        raise AssertionError("unsupported proposal actions must fail")

    try:
        Proposal.from_dict(
            {
                "id": "P-006",
                "action": "remove",
                "target": "- Alpha",
                "title": "T",
                "content": "Replacement text",
                "rationale": "Rationale",
            }
        )
    except ValueError:
        pass
    else:
        raise AssertionError("remove proposals with replacement content must fail")

    duplicate_target = [
        Proposal("P-006", "replace", "- Beta", "T1", "- B1", "R1"),
        Proposal("P-007", "remove", "- Beta", "T2", "None.", "R2"),
    ]
    try:
        build_candidate(original, duplicate_target)
    except ValueError:
        pass
    else:
        raise AssertionError("proposal targets must be exclusive")

    add_only = build_candidate(original, [proposals[0]])
    accepted_add = resolve_proposal(add_only, proposals[0], "accept")
    assert "- Alpha\n\n- Alpha detail\n\n- Beta" in accepted_add
    assert "proposal:P-001" not in accepted_add

    resolved_one = resolve_proposal(candidate, proposals[0], "accept")
    assert proposals[1].insertion() in resolved_one
    assert proposals[2].insertion() in resolved_one

    replace_only = build_candidate(original, [proposals[1]])
    accepted_replace = resolve_proposal(replace_only, proposals[1], "accept")
    assert "- Beta" not in accepted_replace
    assert "- Corrected beta" in accepted_replace
    assert "proposal:P-002" not in accepted_replace

    remove_only = build_candidate(original, [proposals[2]])
    accepted_remove = resolve_proposal(remove_only, proposals[2], "accept")
    assert "- Gamma" not in accepted_remove
    assert "proposal:P-003" not in accepted_remove

    rejected = resolve_proposal(remove_only, proposals[2], "reject")
    assert rejected == original

    try:
        resolve_proposal(remove_only, proposals[2], "unknown")
    except ValueError:
        pass
    else:
        raise AssertionError("unsupported proposal decisions must fail")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        choices=(
            "issue-md",
            "verify-issue-md",
            "build",
            "verify",
            "resolve",
            "self-test",
        ),
    )
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

    if args.mode in ("issue-md", "verify-issue-md"):
        title, body = parse_issue_document_payload(payload)
        if args.mode == "issue-md":
            sys.stdout.write(build_issue_document(title, body))
            return 0
        candidate = payload.get("candidate")
        if not isinstance(candidate, str):
            raise ValueError("verify-issue-md requires a candidate string")
        verify_issue_document(title, body, candidate)
        print("issue.md verified")
        return 0

    if args.mode == "resolve":
        if not isinstance(payload, dict):
            raise ValueError("resolve payload must be an object")
        candidate = payload.get("candidate")
        raw_proposal = payload.get("proposal")
        decision = payload.get("decision")
        if not isinstance(candidate, str) or not isinstance(decision, str):
            raise ValueError("resolve requires candidate and decision strings")
        proposal = Proposal.from_dict(raw_proposal)
        sys.stdout.write(resolve_proposal(candidate, proposal, decision))
        return 0

    original, proposals = parse_payload(payload)
    if args.mode == "build":
        sys.stdout.write(build_candidate(original, proposals))
        return 0

    candidate = payload.get("candidate")
    if not isinstance(candidate, str):
        raise ValueError("verify payload requires a candidate string")
    verify_candidate(original, proposals, candidate)
    print("candidate verified")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
