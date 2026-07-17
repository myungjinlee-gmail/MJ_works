#!/usr/bin/env python3
"""Unit tests for the project clang-tidy runner."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = REPO_ROOT / "scripts" / "clang_tidy.py"
SPEC = importlib.util.spec_from_file_location("mj_clang_tidy", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot import {MODULE_PATH}")
CLANG_TIDY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLANG_TIDY)


class ClangTidyRunnerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory(
            prefix="mj-clang-tidy-test."
        )
        self.repo = Path(self.temporary_directory.name) / "repo"
        self.build = self.repo / "build"
        self.repo.mkdir()
        self.build.mkdir()

        self.source = self.repo / "src" / "main.cpp"
        self.source.parent.mkdir()
        self.source.write_text("int main() { return 0; }\n", encoding="utf-8")

        self.third_party = self.repo / "third_party" / "library.cpp"
        self.third_party.parent.mkdir()
        self.third_party.write_text("int library() { return 0; }\n", encoding="utf-8")

        self.generated = self.build / "generated" / "generated.cpp"
        self.generated.parent.mkdir()
        self.generated.write_text("int generated() { return 0; }\n", encoding="utf-8")
        self.generated_header = self.generated.with_suffix(".hpp")
        self.generated_header.write_text("int generated();\n", encoding="utf-8")

        self.optional = self.repo / "customer_project" / "excluded" / "skip.cpp"
        self.optional.parent.mkdir(parents=True)
        self.optional.write_text("int skip() { return 0; }\n", encoding="utf-8")

        self.database = self.build / "compile_commands.json"
        entries = [
            {"directory": str(self.repo), "file": str(self.source), "command": "c++"},
            {
                "directory": str(self.repo),
                "file": str(self.third_party),
                "command": "c++",
            },
            {
                "directory": str(self.build),
                "file": str(self.generated),
                "command": "c++",
            },
            {"directory": str(self.repo), "file": str(self.optional), "command": "c++"},
        ]
        self.database.write_text(json.dumps(entries), encoding="utf-8")

        self.exclude_file = self.repo / "configuration" / "clang-tidy-exclude.txt"
        self.exclude_file.parent.mkdir()
        self.exclude_file.write_text(
            "# Default and project-specific exclusions\n"
            "third_party\n"
            "customer_project/excluded\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_compiled_generated_source_is_included(self) -> None:
        excluded = CLANG_TIDY.load_excluded_directories(
            self.exclude_file, self.repo
        )
        selected = CLANG_TIDY.load_translation_units(self.database, excluded)

        self.assertEqual(selected, [self.generated, self.source])

    def test_adding_one_directory_excludes_it_without_code_changes(self) -> None:
        with self.exclude_file.open("a", encoding="utf-8") as stream:
            stream.write("build/generated\n")
        excluded = CLANG_TIDY.load_excluded_directories(
            self.exclude_file, self.repo
        )
        selected = CLANG_TIDY.load_translation_units(self.database, excluded)

        self.assertEqual(selected, [self.source])

    def test_header_diagnostics_follow_the_same_exclusions(self) -> None:
        third_party_header = self.third_party.with_suffix(".hpp")
        third_party_header.write_text("int library();\n", encoding="utf-8")
        excluded = CLANG_TIDY.load_excluded_directories(
            self.exclude_file, self.repo
        )

        files = CLANG_TIDY.collect_diagnostic_files(
            (self.repo, self.build), excluded
        )

        self.assertIn(self.generated_header, files)
        self.assertNotIn(third_party_header, files)
        self.assertNotIn(self.optional, files)

    def test_command_never_enables_automatic_fixes(self) -> None:
        command = CLANG_TIDY.make_command(
            "clang-tidy-18",
            self.source,
            self.build,
            self.repo / ".clang-tidy",
            "[]",
        )

        self.assertNotIn("--fix", command)
        self.assertNotIn("--fix-errors", command)
        self.assertNotIn("--fix-notes", command)

    def test_pinned_clang_tidy_version_is_enforced(self) -> None:
        executable = self.repo / "clang-tidy-test"
        executable.write_text(
            "#!/bin/sh\n"
            "echo 'LLVM version 18.1.3'\n",
            encoding="utf-8",
        )
        executable.chmod(0o755)

        selected = CLANG_TIDY.find_clang_tidy(str(executable), "18.1.3")

        self.assertEqual(selected, str(executable))
        with self.assertRaises(CLANG_TIDY.AnalysisError):
            CLANG_TIDY.find_clang_tidy(str(executable), "18.1.4")


if __name__ == "__main__":
    unittest.main()
