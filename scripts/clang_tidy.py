#!/usr/bin/env python3
"""Run the pinned clang-tidy over selected compilation database entries."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence


CPP_EXTENSIONS = {".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx"}
SOURCE_EXTENSIONS = {".c", ".cc", ".cpp", ".cxx"}


class AnalysisError(RuntimeError):
    """Raised for an invalid static-analysis configuration."""


def resolve_path(path: Path, base: Path) -> Path:
    if not path.is_absolute():
        path = base / path
    return path.resolve(strict=False)


def is_within(path: Path, directory: Path) -> bool:
    return path == directory or directory in path.parents


def read_dev_versions(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        key, separator, value = line.partition("=")
        if not separator or not key.strip() or not value.strip():
            raise AnalysisError(f"Invalid development version entry: {line}")
        values[key.strip()] = value.strip()
    return values


def load_excluded_directories(path: Path, repo_root: Path) -> list[Path]:
    excluded: list[Path] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        entry = line.split("#", 1)[0].strip()
        if not entry:
            continue
        relative = Path(entry)
        if relative.is_absolute():
            raise AnalysisError(
                f"{path}:{line_number}: exclusion must be repository-relative: {entry}"
            )
        resolved = resolve_path(relative, repo_root)
        if not is_within(resolved, repo_root):
            raise AnalysisError(
                f"{path}:{line_number}: exclusion escapes the repository: {entry}"
            )
        excluded.append(resolved)
    return excluded


def is_excluded(path: Path, excluded_directories: Iterable[Path]) -> bool:
    resolved = path.resolve(strict=False)
    return any(is_within(resolved, directory) for directory in excluded_directories)


def load_translation_units(
    database_path: Path, excluded_directories: Iterable[Path]
) -> list[Path]:
    try:
        entries = json.loads(database_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise AnalysisError(f"Cannot read compilation database: {database_path}: {error}") from error

    if not isinstance(entries, list):
        raise AnalysisError(f"Compilation database must contain a JSON array: {database_path}")

    sources: set[Path] = set()
    for entry in entries:
        if not isinstance(entry, dict) or "file" not in entry or "directory" not in entry:
            raise AnalysisError(f"Invalid compilation database entry: {entry!r}")
        directory = Path(str(entry["directory"]))
        source = resolve_path(Path(str(entry["file"])), directory)
        if source.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        if not is_excluded(source, excluded_directories):
            sources.add(source)
    return sorted(sources)


def collect_diagnostic_files(
    roots: Iterable[Path], excluded_directories: Iterable[Path]
) -> list[Path]:
    files: set[Path] = set()
    visited_roots: list[Path] = []
    for root in roots:
        root = root.resolve(strict=False)
        if any(is_within(root, visited) for visited in visited_roots):
            continue
        visited_roots.append(root)
        if not root.exists():
            continue
        for directory, names, filenames in os.walk(root):
            current = Path(directory).resolve(strict=False)
            names[:] = [
                name
                for name in names
                if not is_excluded(current / name, excluded_directories)
            ]
            if is_excluded(current, excluded_directories):
                names[:] = []
                continue
            for filename in filenames:
                path = current / filename
                if path.suffix.lower() in CPP_EXTENSIONS:
                    files.add(path)
    return sorted(files)


def read_cache_value(cache_path: Path, name: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(name)}:[^=]*=(.*)$")
    for line in cache_path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1)
    return None


def find_clang_tidy(requested: str | None, expected_version: str) -> str:
    major = expected_version.split(".", 1)[0]
    candidates = [requested] if requested else [f"clang-tidy-{major}", "clang-tidy"]
    for candidate in candidates:
        if not candidate:
            continue
        executable = shutil.which(candidate)
        if executable is None:
            continue
        result = subprocess.run(
            [executable, "--version"],
            check=False,
            capture_output=True,
            text=True,
        )
        output = f"{result.stdout}\n{result.stderr}"
        match = re.search(r"version ([0-9]+\.[0-9]+\.[0-9]+)", output)
        if result.returncode == 0 and match and match.group(1) == expected_version:
            return executable
    requested_text = requested or f"clang-tidy-{major} or clang-tidy"
    raise AnalysisError(
        f"Required clang-tidy {expected_version} was not found via {requested_text}"
    )


def make_line_filter(files: Iterable[Path]) -> str:
    return json.dumps(
        [{"name": str(path)} for path in files],
        separators=(",", ":"),
    )


def make_command(
    executable: str,
    source: Path,
    build_dir: Path,
    config_file: Path,
    line_filter: str,
) -> list[str]:
    return [
        executable,
        str(source),
        f"-p={build_dir}",
        f"--config-file={config_file}",
        "--header-filter=.*",
        f"--line-filter={line_filter}",
        "--quiet",
    ]


def parse_arguments(arguments: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", default="build", help="CMake build directory")
    parser.add_argument(
        "--exclude-file",
        default="configuration/clang-tidy-exclude.txt",
        help="Repository-relative directory exclusion list",
    )
    parser.add_argument("--clang-tidy", help="clang-tidy executable override")
    return parser.parse_args(arguments)


def run(arguments: Sequence[str]) -> int:
    args = parse_arguments(arguments)
    repo_root = Path(__file__).resolve().parent.parent
    build_dir = resolve_path(Path(args.build_dir), repo_root)
    exclude_file = resolve_path(Path(args.exclude_file), repo_root)
    config_file = repo_root / ".clang-tidy"
    versions_file = repo_root / "configuration" / "dev-tools.env"
    database_path = build_dir / "compile_commands.json"
    cache_path = build_dir / "CMakeCache.txt"

    for required in (exclude_file, config_file, versions_file, database_path, cache_path):
        if not required.is_file():
            raise AnalysisError(f"Required file does not exist: {required}")

    if read_cache_value(cache_path, "SDK_GTEST") != "ON":
        raise AnalysisError(
            f"SDK_GTEST must be ON in the analysis build: {cache_path}"
        )

    versions = read_dev_versions(versions_file)
    expected_version = versions.get("LLVM_VERSION")
    if not expected_version:
        raise AnalysisError(f"LLVM_VERSION is not defined in {versions_file}")
    executable = find_clang_tidy(args.clang_tidy, expected_version)
    excluded = load_excluded_directories(exclude_file, repo_root)
    sources = load_translation_units(database_path, excluded)
    if not sources:
        raise AnalysisError("No C/C++ translation units remain after exclusions")

    diagnostic_files = collect_diagnostic_files((repo_root, build_dir), excluded)
    line_filter = make_line_filter(diagnostic_files)
    failures = 0
    for source in sources:
        print(f"[clang-tidy] {source}", flush=True)
        result = subprocess.run(
            make_command(executable, source, build_dir, config_file, line_filter),
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            sys.stdout.write(result.stdout)
            sys.stderr.write(result.stderr)
            failures += 1

    if failures:
        print(
            f"[clang-tidy] ERROR: {failures} translation unit(s) failed analysis.",
            file=sys.stderr,
        )
        return 1
    print(f"[clang-tidy] PASS: analyzed {len(sources)} translation unit(s).")
    return 0


def main() -> int:
    try:
        return run(sys.argv[1:])
    except (AnalysisError, OSError) as error:
        print(f"[clang-tidy] ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
