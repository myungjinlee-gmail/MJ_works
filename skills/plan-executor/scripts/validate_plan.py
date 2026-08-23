#!/usr/bin/env python3
"""Validate a version 3 issue execution plan."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


GOAL_ID = re.compile(r"G-[0-9]{3,}")
HASH = re.compile(r"[0-9a-f]{64}")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
GOAL_HEADING = re.compile(r"^(G-[0-9]{3,})\s*:\s*(.+)$")
FILE_ITEM = re.compile(r"^- `([^`]+)`\s*$")
CHILD_ITEM = re.compile(r"^ {4}- (.+?)\s*$")
OPERATION_ITEM = re.compile(r"^Operation:\s*([a-z]+)\s*$")
VERIFICATION_ITEM = re.compile(r"^- `(G-[0-9]{3,}-V-[0-9]{2,})`:\s*(.+?)\s*$")
PROPOSAL_MARKER = re.compile(
    r"(?m)^<!-- proposal:P-[0-9]{3,}:(?:start|end) -->\s*$"
)
VISIBLE_PROPOSAL = re.compile(
    r"(?m)^(?: {0,3}#{1,6}\s+|\*\*)\[(?:Proposal|Propose)\](?:\s|:|\*\*|$)"
)
GOAL_STATES = {"pending", "in_progress", "completed", "blocked"}
VERIFICATION_STATES = {"pending", "passed", "failed", "blocked"}
VERIFICATION_METHODS = {"review", "command", "manual"}
OPERATIONS = {"create", "modify", "delete"}


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate YAML mapping keys."""


def _construct_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _slug(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s\-]+", "-", value)
    return value.strip("-")


def _heading_map(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for line in text.splitlines():
        match = HEADING.fullmatch(line)
        if match:
            result.setdefault(_slug(match.group(2)), []).append(match.group(2))
    return result


def _heading_sections(text: str) -> list[tuple[int, str, list[str]]]:
    lines = text.splitlines()
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = HEADING.fullmatch(line)
        if match:
            headings.append((index, len(match.group(1)), match.group(2)))
    sections: list[tuple[int, str, list[str]]] = []
    for position, (start, level, title) in enumerate(headings):
        end = len(lines)
        for next_start, next_level, _ in headings[position + 1 :]:
            if next_level <= level:
                end = next_start
                break
        sections.append((level, title, lines[start + 1 : end]))
    return sections


def _named_section(text: str, title: str, errors: list[str]) -> list[str]:
    matches = [
        lines
        for _, candidate, lines in _heading_sections(text)
        if candidate.strip().casefold() == title.casefold()
    ]
    if len(matches) != 1:
        errors.append(f"{title} heading must occur exactly once")
        return []
    return matches[0]


def _goal_sections(
    text: str, errors: list[str]
) -> dict[str, tuple[str, str, list[str]]]:
    result: dict[str, tuple[str, str, list[str]]] = {}
    for _, heading, lines in _heading_sections(text):
        match = GOAL_HEADING.fullmatch(heading)
        if not match:
            continue
        goal_id, title = match.groups()
        if goal_id in result:
            errors.append(f"duplicate Goal heading in plan.md: {goal_id}")
            continue
        result[goal_id] = (title, _slug(heading), lines)
    return result


def _subsection(lines: list[str], title: str, label: str, errors: list[str]) -> list[str]:
    text = "\n".join(lines)
    matches = [
        section_lines
        for _, candidate, section_lines in _heading_sections(text)
        if candidate.strip().casefold() == title.casefold()
    ]
    if len(matches) != 1:
        errors.append(f"{label} must contain exactly one {title} heading")
        return []
    return matches[0]


def _parse_backticked_list(
    lines: list[str], label: str, errors: list[str]
) -> list[str]:
    values: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        match = FILE_ITEM.fullmatch(line)
        if not match:
            errors.append(f"{label} contains invalid list item: {line.strip()}")
            continue
        values.append(match.group(1))
    if not values:
        errors.append(f"{label} must contain at least one item")
    if len(values) != len(set(values)):
        errors.append(f"{label} contains duplicates")
    return values


def _parse_dependencies(
    lines: list[str], label: str, errors: list[str]
) -> list[str]:
    content = [line for line in lines if line.strip()]
    if content == ["None."]:
        return []
    return _parse_backticked_list(content, label, errors)


def _unquote_backticks(value: str, label: str, errors: list[str]) -> str:
    if len(value) < 2 or not value.startswith("`") or not value.endswith("`"):
        errors.append(f"{label} must be enclosed in backticks")
        return value
    return value[1:-1]


def _parse_verification(
    lines: list[str], label: str, errors: list[str]
) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line in lines:
        if not line.strip():
            continue
        match = VERIFICATION_ITEM.fullmatch(line)
        if match:
            verification_id, title = match.groups()
            current = {
                "id": verification_id,
                "title": title,
                "requirement_refs": [],
                "targets": [],
            }
            values.append(current)
            continue
        child = CHILD_ITEM.fullmatch(line)
        if child is None or current is None or ":" not in child.group(1):
            errors.append(f"{label} contains invalid verification line: {line.strip()}")
            continue
        field, raw_value = child.group(1).split(":", 1)
        field = field.strip()
        raw_value = raw_value.strip()
        if field == "Requirement":
            current["requirement_refs"].append(
                _unquote_backticks(raw_value, f"{label} Requirement", errors)
            )
        elif field == "Target":
            current["targets"].append(
                _unquote_backticks(raw_value, f"{label} Target", errors)
            )
        else:
            key = {
                "Method": "method",
                "Procedure": "procedure",
                "Command": "command",
                "Working directory": "working_directory",
                "Pass condition": "pass_condition",
            }.get(field)
            if key is None:
                errors.append(f"{label} contains unknown field: {field}")
                continue
            if key in current:
                errors.append(f"{label} repeats field: {field}")
                continue
            if key in {"command", "working_directory"}:
                current[key] = _unquote_backticks(
                    raw_value, f"{label} {field}", errors
                )
            else:
                current[key] = raw_value
    if not values:
        errors.append(f"{label} must contain at least one verification item")
    ids = [item["id"] for item in values]
    if len(ids) != len(set(ids)):
        errors.append(f"{label} contains duplicate verification IDs")
    for item in values:
        item_label = f"{label} {item['id']}"
        method = item.get("method")
        if method not in VERIFICATION_METHODS:
            errors.append(f"{item_label} has invalid Method")
        if not item["requirement_refs"]:
            errors.append(f"{item_label} requires at least one Requirement")
        if not str(item.get("pass_condition", "")).strip():
            errors.append(f"{item_label} requires Pass condition")
        if method in {"review", "manual"}:
            if not str(item.get("procedure", "")).strip():
                errors.append(f"{item_label} requires Procedure")
            if "command" in item or "working_directory" in item:
                errors.append(f"{item_label} forbids Command fields")
        elif method == "command":
            if not str(item.get("command", "")).strip():
                errors.append(f"{item_label} requires Command")
            if not str(item.get("working_directory", "")).strip():
                errors.append(f"{item_label} requires Working directory")
            if "procedure" in item:
                errors.append(f"{item_label} forbids Procedure")
    return values


def _valid_path(path: object, label: str, errors: list[str]) -> bool:
    if not isinstance(path, str) or not path or path != path.strip():
        errors.append(f"{label} must be a non-empty exact file path")
        return False
    if (
        path.startswith("/")
        or path.endswith("/")
        or "\\" in path
        or re.search(r"[*?\[\]{}<>]", path)
    ):
        errors.append(f"{label} must be an exact repository-relative file path")
        return False
    parts = PurePosixPath(path).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        errors.append(f"{label} contains invalid path traversal or segments")
        return False
    return True


def _valid_working_directory(
    value: object, label: str, errors: list[str]
) -> bool:
    if value == ".":
        return True
    return _valid_path(value, label, errors)


def _parse_file_changes(
    lines: list[str], label: str, errors: list[str]
) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    current_path: str | None = None
    for line in lines:
        if HEADING.fullmatch(line):
            current_path = None
            continue

        file_match = FILE_ITEM.fullmatch(line)
        if file_match:
            current_path = file_match.group(1)
            _valid_path(current_path, f"{label} path", errors)
            entries.setdefault(
                current_path,
                {"operations": set(), "points": [], "point_counts": {}},
            )
            continue

        child_match = CHILD_ITEM.fullmatch(line)
        if child_match and current_path is not None:
            value = child_match.group(1).strip()
            operation_match = OPERATION_ITEM.fullmatch(value)
            if operation_match:
                entries[current_path]["operations"].add(operation_match.group(1))
            elif value:
                entries[current_path]["points"].append(value)
                counts = entries[current_path]["point_counts"]
                counts[value] = counts.get(value, 0) + 1

    normalized: dict[str, dict[str, Any]] = {}
    for path, entry in entries.items():
        operations = entry["operations"]
        if len(operations) != 1:
            errors.append(f"{label} {path} must declare exactly one Operation")
            operation = ""
        else:
            operation = next(iter(operations))
            if operation not in OPERATIONS:
                errors.append(f"{label} {path} has invalid Operation: {operation}")
        points = entry["points"]
        if not points:
            errors.append(f"{label} {path} must contain modification points")
        for point, count in entry["point_counts"].items():
            if count > 1:
                errors.append(f"{label} {path} repeats modification point: {point}")
        normalized[path] = {"operation": operation, "points": points}
    if not normalized:
        errors.append(f"{label} must declare at least one exact file path")
    return normalized


def _mapping(value: object, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be a mapping")
        return {}
    return value


def _check_keys(
    value: dict[str, Any],
    required: set[str],
    optional: set[str],
    label: str,
    errors: list[str],
) -> None:
    for key in sorted(required - set(value)):
        errors.append(f"{label} is missing required key: {key}")
    for key in sorted(set(value) - required - optional):
        errors.append(f"{label} has unknown key: {key}")


def _strings(value: object, label: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) for item in value
    ):
        errors.append(f"{label} must be a list of strings")
        return []
    return value


def _check_ref(
    ref: object,
    expected_file: str,
    headings: dict[str, list[str]],
    label: str,
    errors: list[str],
) -> None:
    if not isinstance(ref, str) or "#" not in ref:
        errors.append(f"{label} must be a Markdown file#heading reference")
        return
    filename, fragment = ref.split("#", 1)
    if filename != expected_file:
        errors.append(f"{label} must reference {expected_file}")
    if not fragment or fragment not in headings:
        errors.append(f"{label} does not resolve: {ref}")
    elif len(headings[fragment]) != 1:
        errors.append(f"{label} resolves to an ambiguous heading: {ref}")


def validate_plan(plan_path: Path, execution_ready: bool = False) -> list[str]:
    errors: list[str] = []
    try:
        yaml_text = plan_path.read_text(encoding="utf-8")
        payload = yaml.load(yaml_text, Loader=UniqueKeyLoader)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as error:
        return [f"cannot load plan.yaml: {error}"]
    if "\t" in yaml_text:
        errors.append("plan.yaml must not contain tabs")

    root = _mapping(payload, "plan.yaml", errors)
    _check_keys(
        root,
        {"schema_version", "issue", "plan", "goals"},
        set(),
        "plan.yaml",
        errors,
    )
    if root.get("schema_version") != 3:
        errors.append("schema_version must be integer 3")

    issue = _mapping(root.get("issue"), "issue", errors)
    plan = _mapping(root.get("plan"), "plan", errors)
    _check_keys(
        issue,
        {"number", "requirements_file", "sha256"},
        set(),
        "issue",
        errors,
    )
    _check_keys(
        plan,
        {"human_file", "sha256", "status"},
        set(),
        "plan",
        errors,
    )

    issue_number = issue.get("number")
    if (
        isinstance(issue_number, bool)
        or not isinstance(issue_number, int)
        or issue_number <= 0
    ):
        errors.append("issue.number must be a positive integer")
    parent_name = plan_path.parent.name
    if not parent_name.isdigit():
        errors.append("plan.yaml parent directory must be the decimal issue number")
    elif isinstance(issue_number, int) and not isinstance(issue_number, bool):
        if int(parent_name) != issue_number:
            errors.append("issue.number does not match the plan directory")

    if issue.get("requirements_file") != "issue.md":
        errors.append("issue.requirements_file must be issue.md")
    if plan.get("human_file") != "plan.md":
        errors.append("plan.human_file must be plan.md")

    base = plan_path.parent
    issue_path = base / "issue.md"
    human_path = base / "plan.md"
    issue_text = ""
    plan_text = ""
    for path, expected_hash, label in (
        (issue_path, issue.get("sha256"), "issue.sha256"),
        (human_path, plan.get("sha256"), "plan.sha256"),
    ):
        if not path.is_file():
            errors.append(f"missing referenced file: {path.name}")
            continue
        if not isinstance(expected_hash, str) or not HASH.fullmatch(expected_hash):
            errors.append(f"{label} must be 64 lowercase hexadecimal characters")
        elif _sha256(path) != expected_hash:
            errors.append(f"{label} does not match {path.name}")
    try:
        if issue_path.is_file():
            issue_text = issue_path.read_text(encoding="utf-8")
        if human_path.is_file():
            plan_text = human_path.read_text(encoding="utf-8")
    except UnicodeError as error:
        errors.append(f"cannot decode Markdown input as UTF-8: {error}")

    plan_status = plan.get("status")
    if plan_status not in {"draft", "approved"}:
        errors.append("plan.status must be draft or approved")
    if execution_ready and plan_status != "approved":
        errors.append("execution requires plan.status approved")

    issue_headings = _heading_map(issue_text)
    plan_headings = _heading_map(plan_text)
    if PROPOSAL_MARKER.search(issue_text) or VISIBLE_PROPOSAL.search(issue_text):
        errors.append("issue.md contains unresolved Proposal blocks")
    _named_section(issue_text, "Purpose", errors)
    _named_section(issue_text, "Detailed requirements", errors)
    known_lines = _named_section(issue_text, "Known impact", errors)
    known_changes = _parse_file_changes(known_lines, "Known impact", errors)
    _named_section(issue_text, "Verification and acceptance", errors)
    markdown_goals = _goal_sections(plan_text, errors)

    raw_goals = root.get("goals")
    if not isinstance(raw_goals, list) or not raw_goals:
        errors.append("goals must be a non-empty list")
        raw_goals = []

    goals: dict[str, dict[str, Any]] = {}
    dependencies_by_goal: dict[str, list[str]] = {}
    covered_points: dict[tuple[str, str], str] = {}
    change_ids: set[str] = set()
    verification_ids: set[str] = set()
    in_progress = 0

    for index, raw_goal in enumerate(raw_goals):
        label = f"goals[{index}]"
        goal = _mapping(raw_goal, label, errors)
        _check_keys(
            goal,
            {
                "id",
                "title",
                "plan_ref",
                "requirement_refs",
                "depends_on",
                "status",
                "changes",
                "verification",
            },
            {"blocker"},
            label,
            errors,
        )
        goal_id = goal.get("id")
        if not isinstance(goal_id, str) or not GOAL_ID.fullmatch(goal_id):
            errors.append(f"{label}.id must match G-NNN")
            continue
        if goal_id in goals:
            errors.append(f"duplicate Goal ID: {goal_id}")
            continue
        goals[goal_id] = goal

        title = goal.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append(f"{goal_id}.title must be non-empty")
        markdown_goal = markdown_goals.get(goal_id)
        markdown_refs: list[str] = []
        markdown_dependencies: list[str] = []
        markdown_changes: dict[str, dict[str, Any]] = {}
        markdown_verification: list[dict[str, Any]] = []
        if markdown_goal is None:
            errors.append(f"{goal_id} is missing from plan.md headings")
        else:
            markdown_title, markdown_slug, goal_lines = markdown_goal
            if title != markdown_title:
                errors.append(f"{goal_id} title differs between plan.yaml and plan.md")
            if goal.get("plan_ref") != f"plan.md#{markdown_slug}":
                errors.append(f"{goal_id}.plan_ref does not target its Goal heading")
            requirement_lines = _subsection(
                goal_lines, "Requirements", f"plan.md {goal_id}", errors
            )
            markdown_refs = _parse_backticked_list(
                requirement_lines, f"plan.md {goal_id} Requirements", errors
            )
            dependency_lines = _subsection(
                goal_lines, "Dependencies", f"plan.md {goal_id}", errors
            )
            markdown_dependencies = _parse_dependencies(
                dependency_lines, f"plan.md {goal_id} Dependencies", errors
            )
            change_lines = _subsection(
                goal_lines, "Changes", f"plan.md {goal_id}", errors
            )
            markdown_changes = _parse_file_changes(
                change_lines, f"plan.md {goal_id} Changes", errors
            )
            verification_lines = _subsection(
                goal_lines,
                "Verification and acceptance",
                f"plan.md {goal_id}",
                errors,
            )
            markdown_verification = _parse_verification(
                verification_lines,
                f"plan.md {goal_id} Verification and acceptance",
                errors,
            )

        _check_ref(
            goal.get("plan_ref"),
            "plan.md",
            plan_headings,
            f"{goal_id}.plan_ref",
            errors,
        )
        refs = _strings(
            goal.get("requirement_refs"),
            f"{goal_id}.requirement_refs",
            errors,
        )
        if not refs:
            errors.append(f"{goal_id}.requirement_refs must not be empty")
        if refs != markdown_refs:
            errors.append(
                f"{goal_id} requirement references differ between "
                "plan.yaml and plan.md"
            )
        for ref_index, ref in enumerate(refs):
            _check_ref(
                ref,
                "issue.md",
                issue_headings,
                f"{goal_id}.requirement_refs[{ref_index}]",
                errors,
            )

        dependencies = _strings(
            goal.get("depends_on"), f"{goal_id}.depends_on", errors
        )
        dependencies_by_goal[goal_id] = dependencies
        if dependencies != markdown_dependencies:
            errors.append(
                f"{goal_id} dependencies differ between plan.yaml and plan.md"
            )
        if len(dependencies) != len(set(dependencies)):
            errors.append(f"{goal_id}.depends_on contains duplicates")
        if goal_id in dependencies:
            errors.append(f"{goal_id} cannot depend on itself")

        yaml_goal_changes: dict[str, dict[str, Any]] = {}
        raw_changes = goal.get("changes")
        if not isinstance(raw_changes, list) or not raw_changes:
            errors.append(f"{goal_id}.changes must be a non-empty list")
            raw_changes = []
        for change_index, raw_change in enumerate(raw_changes):
            change_label = f"{goal_id}.changes[{change_index}]"
            change = _mapping(raw_change, change_label, errors)
            _check_keys(
                change,
                {"id", "path", "operation", "points"},
                set(),
                change_label,
                errors,
            )
            change_id = change.get("id")
            change_pattern = re.compile(rf"{re.escape(goal_id)}-C-[0-9]{{2,}}")
            if not isinstance(change_id, str) or not change_pattern.fullmatch(change_id):
                errors.append(f"{change_label}.id must match {goal_id}-C-NN")
            elif change_id in change_ids:
                errors.append(f"duplicate change ID: {change_id}")
            else:
                change_ids.add(change_id)

            path = change.get("path")
            valid_path = _valid_path(path, f"{change_label}.path", errors)
            operation = change.get("operation")
            if operation not in OPERATIONS:
                errors.append(f"{change_label}.operation is invalid")
            points = _strings(change.get("points"), f"{change_label}.points", errors)
            if not points or any(not point.strip() for point in points):
                errors.append(f"{change_label}.points must contain concrete text")
            if len(points) != len(set(points)):
                errors.append(f"{change_label}.points contains duplicates")
            if valid_path and isinstance(path, str):
                if path in yaml_goal_changes:
                    errors.append(f"{goal_id} repeats change path: {path}")
                yaml_goal_changes[path] = {
                    "operation": operation,
                    "points": points,
                }
                known = known_changes.get(path)
                if known is None:
                    errors.append(f"{change_label}.path is absent from Known impact")
                else:
                    if operation != known["operation"]:
                        errors.append(
                            f"{change_label}.operation differs from Known impact"
                        )
                    for point in points:
                        if point not in known["points"]:
                            errors.append(
                                f"{change_label} point is absent from Known impact: {point}"
                            )
                        key = (path, point)
                        if key in covered_points:
                            errors.append(
                                f"Known impact point mapped more than once: {path}: {point}"
                            )
                        else:
                            covered_points[key] = str(change_id)

        if yaml_goal_changes != markdown_changes:
            errors.append(f"{goal_id} changes differ between plan.yaml and plan.md")

        status = goal.get("status")
        if status not in GOAL_STATES:
            errors.append(f"{goal_id}.status is invalid")
        if status == "in_progress":
            in_progress += 1
        if status == "blocked" and not str(goal.get("blocker", "")).strip():
            errors.append(f"{goal_id} is blocked without a blocker")
        if status != "blocked" and str(goal.get("blocker", "")).strip():
            errors.append(f"{goal_id} has a blocker but is not blocked")

        raw_verification = goal.get("verification")
        if not isinstance(raw_verification, list) or not raw_verification:
            errors.append(f"{goal_id}.verification must be a non-empty list")
            raw_verification = []
        all_passed = bool(raw_verification)
        yaml_verification: list[dict[str, Any]] = []
        for verification_index, raw_item in enumerate(raw_verification):
            item_label = f"{goal_id}.verification[{verification_index}]"
            item = _mapping(raw_item, item_label, errors)
            _check_keys(
                item,
                {
                    "id",
                    "title",
                    "method",
                    "requirement_refs",
                    "targets",
                    "pass_condition",
                    "status",
                    "evidence",
                },
                {"procedure", "command", "working_directory"},
                item_label,
                errors,
            )
            verification_id = item.get("id")
            pattern = re.compile(rf"{re.escape(goal_id)}-V-[0-9]{{2,}}")
            if not isinstance(verification_id, str) or not pattern.fullmatch(
                verification_id
            ):
                errors.append(f"{item_label}.id must match {goal_id}-V-NN")
            elif verification_id in verification_ids:
                errors.append(f"duplicate verification ID: {verification_id}")
            else:
                verification_ids.add(verification_id)

            title = item.get("title")
            if not isinstance(title, str) or not title.strip():
                errors.append(f"{item_label}.title must be non-empty")
            method = item.get("method")
            if method not in VERIFICATION_METHODS:
                errors.append(f"{item_label}.method is invalid")
            verification_refs = _strings(
                item.get("requirement_refs"),
                f"{item_label}.requirement_refs",
                errors,
            )
            if not verification_refs:
                errors.append(f"{item_label}.requirement_refs must not be empty")
            for ref_index, ref in enumerate(verification_refs):
                _check_ref(
                    ref,
                    "issue.md",
                    issue_headings,
                    f"{item_label}.requirement_refs[{ref_index}]",
                    errors,
                )
            if "issue.md#verification-and-acceptance" not in verification_refs:
                errors.append(
                    f"{item_label} must reference Verification and acceptance"
                )

            targets = _strings(item.get("targets"), f"{item_label}.targets", errors)
            if len(targets) != len(set(targets)):
                errors.append(f"{item_label}.targets contains duplicates")
            for target_index, target in enumerate(targets):
                _valid_path(target, f"{item_label}.targets[{target_index}]", errors)

            pass_condition = item.get("pass_condition")
            if not isinstance(pass_condition, str) or not pass_condition.strip():
                errors.append(f"{item_label}.pass_condition must be non-empty")

            static_item: dict[str, Any] = {
                "id": verification_id,
                "title": title,
                "method": method,
                "requirement_refs": verification_refs,
                "targets": targets,
            }
            if method in {"review", "manual"}:
                procedure = item.get("procedure")
                if not isinstance(procedure, str) or not procedure.strip():
                    errors.append(f"{item_label}.procedure must be non-empty")
                if "command" in item or "working_directory" in item:
                    errors.append(f"{item_label} forbids command fields")
                static_item["procedure"] = procedure
            elif method == "command":
                command = item.get("command")
                working_directory = item.get("working_directory")
                if not isinstance(command, str) or not command.strip():
                    errors.append(f"{item_label}.command must be non-empty")
                _valid_working_directory(
                    working_directory,
                    f"{item_label}.working_directory",
                    errors,
                )
                if "procedure" in item:
                    errors.append(f"{item_label} forbids procedure")
                static_item["command"] = command
                static_item["working_directory"] = working_directory
            static_item["pass_condition"] = pass_condition
            yaml_verification.append(static_item)

            verification_status = item.get("status")
            if verification_status not in VERIFICATION_STATES:
                errors.append(f"{item_label}.status is invalid")
            evidence = _strings(
                item.get("evidence"), f"{item_label}.evidence", errors
            )
            if verification_status in {"passed", "failed"} and not any(
                entry.strip() for entry in evidence
            ):
                errors.append(f"{item_label} {verification_status} without evidence")
            if status == "pending" and verification_status != "pending":
                errors.append(
                    f"{item_label} has runtime progress while {goal_id} is pending"
                )
            if verification_status == "blocked" and status != "blocked":
                errors.append(
                    f"{item_label} is blocked while {goal_id} is not blocked"
                )
            if verification_status != "passed":
                all_passed = False
        if status == "completed" and not all_passed:
            errors.append(
                f"{goal_id} is completed before every verification item passed"
            )
        if yaml_verification != markdown_verification:
            errors.append(
                f"{goal_id} verification differs between plan.yaml and plan.md"
            )

    if in_progress > 1:
        errors.append("at most one Goal may be in_progress")
    for goal_id in markdown_goals:
        if goal_id not in goals:
            errors.append(f"plan.md Goal is missing from plan.yaml: {goal_id}")

    for path, known in known_changes.items():
        for point in known["points"]:
            if (path, point) not in covered_points:
                errors.append(f"Known impact point is not mapped: {path}: {point}")

    for goal_id, goal in goals.items():
        for dependency in dependencies_by_goal.get(goal_id, []):
            if dependency not in goals:
                errors.append(f"{goal_id} has unknown dependency: {dependency}")
            elif (
                goal.get("status") in {"in_progress", "blocked", "completed"}
                and goals[dependency].get("status") != "completed"
            ):
                errors.append(
                    f"{goal_id} started before dependency completed: {dependency}"
                )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(goal_id: str) -> None:
        if goal_id in visiting:
            errors.append(f"Goal dependency cycle includes {goal_id}")
            return
        if goal_id in visited:
            return
        visiting.add(goal_id)
        for dependency in dependencies_by_goal.get(goal_id, []):
            if dependency in goals:
                visit(dependency)
        visiting.remove(goal_id)
        visited.add(goal_id)

    for goal_id in goals:
        visit(goal_id)
    return errors


def self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "1"
        root.mkdir()
        issue = root / "issue.md"
        human = root / "plan.md"
        issue.write_text(
            "# Issue\n\n"
            "### Purpose\n\n- Deliver the work.\n\n"
            "### Known impact\n\n"
            "- `docs/example.md`\n"
            "    - Operation: modify\n"
            "    - Add the required relationship.\n\n"
            "### Detailed requirements\n\n- Add the relationship.\n\n"
            "### Verification and acceptance\n\n"
            "- Review the relationship and run the tests.\n",
            encoding="utf-8",
        )
        human.write_text(
            "# Plan\n\n"
            "## G-001: Do the work\n\n"
            "### Requirements\n\n"
            "- `issue.md#detailed-requirements`\n\n"
            "### Dependencies\n\n"
            "None.\n\n"
            "### Changes\n\n"
            "- `docs/example.md`\n"
            "    - Operation: modify\n"
            "    - Add the required relationship.\n\n"
            "### Verification and acceptance\n\n"
            "- `G-001-V-01`: Review the relationship\n"
            "    - Method: review\n"
            "    - Requirement: `issue.md#verification-and-acceptance`\n"
            "    - Target: `docs/example.md`\n"
            "    - Procedure: Inspect the documented relationship.\n"
            "    - Pass condition: The required relationship is present.\n"
            "- `G-001-V-02`: Run the tests\n"
            "    - Method: command\n"
            "    - Requirement: `issue.md#verification-and-acceptance`\n"
            "    - Command: `python3 -m pytest`\n"
            "    - Working directory: `.`\n"
            "    - Pass condition: The command exits with status 0.\n"
            "- `G-001-V-03`: Confirm the rendered result\n"
            "    - Method: manual\n"
            "    - Requirement: `issue.md#verification-and-acceptance`\n"
            "    - Procedure: Ask the user to inspect the rendered result.\n"
            "    - Pass condition: The user confirms the result.\n",
            encoding="utf-8",
        )
        payload = {
            "schema_version": 3,
            "issue": {
                "number": 1,
                "requirements_file": "issue.md",
                "sha256": _sha256(issue),
            },
            "plan": {
                "human_file": "plan.md",
                "sha256": _sha256(human),
                "status": "approved",
            },
            "goals": [
                {
                    "id": "G-001",
                    "title": "Do the work",
                    "plan_ref": "plan.md#g-001-do-the-work",
                    "requirement_refs": ["issue.md#detailed-requirements"],
                    "depends_on": [],
                    "status": "pending",
                    "changes": [
                        {
                            "id": "G-001-C-01",
                            "path": "docs/example.md",
                            "operation": "modify",
                            "points": ["Add the required relationship."],
                        }
                    ],
                    "verification": [
                        {
                            "id": "G-001-V-01",
                            "title": "Review the relationship",
                            "method": "review",
                            "requirement_refs": [
                                "issue.md#verification-and-acceptance"
                            ],
                            "targets": ["docs/example.md"],
                            "procedure": "Inspect the documented relationship.",
                            "pass_condition": "The required relationship is present.",
                            "status": "pending",
                            "evidence": [],
                        },
                        {
                            "id": "G-001-V-02",
                            "title": "Run the tests",
                            "method": "command",
                            "requirement_refs": [
                                "issue.md#verification-and-acceptance"
                            ],
                            "targets": [],
                            "command": "python3 -m pytest",
                            "working_directory": ".",
                            "pass_condition": "The command exits with status 0.",
                            "status": "pending",
                            "evidence": [],
                        },
                        {
                            "id": "G-001-V-03",
                            "title": "Confirm the rendered result",
                            "method": "manual",
                            "requirement_refs": [
                                "issue.md#verification-and-acceptance"
                            ],
                            "targets": [],
                            "procedure": (
                                "Ask the user to inspect the rendered result."
                            ),
                            "pass_condition": "The user confirms the result.",
                            "status": "pending",
                            "evidence": [],
                        }
                    ],
                }
            ],
        }
        plan_path = root / "plan.yaml"
        plan_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        assert validate_plan(plan_path, execution_ready=True) == []

        payload["goals"][0]["changes"][0]["path"] = "docs/other.md"
        plan_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        path_errors = validate_plan(plan_path)
        assert any("absent from Known impact" in error for error in path_errors)
        payload["goals"][0]["changes"][0]["path"] = "docs/example.md"

        payload["goals"][0]["changes"][0]["operation"] = "unsupported"
        plan_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        operation_errors = validate_plan(plan_path)
        assert any("operation is invalid" in error for error in operation_errors)
        payload["goals"][0]["changes"][0]["operation"] = "modify"

        command_item = payload["goals"][0]["verification"][1]
        command_item.pop("working_directory")
        plan_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        command_errors = validate_plan(plan_path)
        assert any("working_directory" in error for error in command_errors)
        command_item["working_directory"] = "."

        payload["goals"][0]["verification"][0]["pass_condition"] = (
            "Different condition."
        )
        plan_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        parity_errors = validate_plan(plan_path)
        assert any("verification differs" in error for error in parity_errors)
        payload["goals"][0]["verification"][0]["pass_condition"] = (
            "The required relationship is present."
        )

        payload["goals"][0]["requirement_refs"] = ["issue.md#purpose"]
        plan_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        requirement_errors = validate_plan(plan_path)
        assert any("requirement references differ" in error for error in requirement_errors)
        payload["goals"][0]["requirement_refs"] = [
            "issue.md#detailed-requirements"
        ]

        payload["goals"][0]["depends_on"] = ["G-999"]
        plan_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        dependency_errors = validate_plan(plan_path)
        assert any("dependencies differ" in error for error in dependency_errors)
        payload["goals"][0]["depends_on"] = []

        payload["goals"][0]["status"] = "completed"
        for item in payload["goals"][0]["verification"]:
            item["status"] = "passed"
        plan_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        evidence_errors = validate_plan(plan_path)
        assert any("passed without evidence" in error for error in evidence_errors)
        payload["goals"][0]["status"] = "pending"
        for item in payload["goals"][0]["verification"]:
            item["status"] = "pending"

        first_item = payload["goals"][0]["verification"][0]
        first_item["status"] = "blocked"
        payload["goals"][0]["status"] = "in_progress"
        plan_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        blocked_errors = validate_plan(plan_path)
        assert any(
            "is blocked while G-001 is not blocked" in error
            for error in blocked_errors
        )
        first_item["status"] = "passed"
        first_item["evidence"] = ["Reviewed docs/example.md."]
        payload["goals"][0]["status"] = "pending"
        plan_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        pending_errors = validate_plan(plan_path)
        assert any("runtime progress while G-001 is pending" in error for error in pending_errors)
        first_item["status"] = "pending"
        first_item["evidence"] = []

        original_issue = issue.read_text(encoding="utf-8")
        issue.write_text(
            original_issue
            + "\n<!-- proposal:P-001:start -->\n"
            + "<!-- proposal:P-001:end -->\n",
            encoding="utf-8",
        )
        payload["issue"]["sha256"] = _sha256(issue)
        plan_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        proposal_errors = validate_plan(plan_path)
        assert any("unresolved Proposal" in error for error in proposal_errors)
        issue.write_text(original_issue, encoding="utf-8")
        payload["issue"]["sha256"] = _sha256(issue)

        payload["plan"]["status"] = "draft"
        plan_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        assert any(
            "execution requires" in error
            for error in validate_plan(plan_path, execution_ready=True)
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", nargs="?", type=Path)
    parser.add_argument("--execution-ready", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("self-test passed")
        return 0
    if args.plan is None:
        parser.error("plan path is required unless --self-test is used")
    errors = validate_plan(args.plan, execution_ready=args.execution_ready)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("plan.yaml verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
