#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
test_root="$(mktemp -d "${TMPDIR:-/tmp}/mj-cmake-config-test.XXXXXX")"
config_file="${test_root}/test.yaml"

cleanup()
{
    rm -rf "${test_root}"
}
trap cleanup EXIT

cat >"${config_file}" <<'EOF'
SDK_HW_TARGET : vanilla
SDK_OS_TARGET : linux
SDK_PROJECT_TARGET : reference
SDK_CAPTURE_TARGET : raw_file
SDK_DISPLAY_TARGET : raw_file
SDK_RUN_DEV_SETUP : OFF
SDK_GTEST : OFF
SDK_COVERAGE : OFF
EOF

cmake -S "${repo_root}" -B "${test_root}/yaml-build" \
    -DSDK_CONFIG="${config_file}" >/dev/null

test -f "${test_root}/yaml-build/compile_commands.json"
grep -Fq -- "-Werror" "${test_root}/yaml-build/compile_commands.json"
grep -Fq -- "-std=c++17" "${test_root}/yaml-build/compile_commands.json"
grep -Fq "SDK_RUN_DEV_SETUP:BOOL=OFF" "${test_root}/yaml-build/CMakeCache.txt"
grep -Fq "SDK_GTEST:BOOL=OFF" "${test_root}/yaml-build/CMakeCache.txt"
grep -Fq "SDK_COVERAGE:BOOL=OFF" "${test_root}/yaml-build/CMakeCache.txt"

cat >"${config_file}" <<'EOF'
SDK_HW_TARGET : vanilla
SDK_OS_TARGET : linux
SDK_PROJECT_TARGET : reference
SDK_CAPTURE_TARGET : raw_file
SDK_DISPLAY_TARGET : raw_file
SDK_RUN_DEV_SETUP : OFF
SDK_GTEST : ON
SDK_COVERAGE : OFF
EOF

cmake -S "${repo_root}" -B "${test_root}/yaml-build" \
    -DSDK_CONFIG="${config_file}" >/dev/null

grep -Fq "SDK_GTEST:BOOL=ON" "${test_root}/yaml-build/CMakeCache.txt"
grep -Fq "SDK_COVERAGE:BOOL=OFF" "${test_root}/yaml-build/CMakeCache.txt"
python3 - "${test_root}/yaml-build/compile_commands.json" <<'PY'
import json
import pathlib
import sys

compile_commands_path = pathlib.Path(sys.argv[1])
compile_commands = json.loads(compile_commands_path.read_text(encoding="utf-8"))
missing_standard = [
    entry["file"]
    for entry in compile_commands
    if "-std=c++17" not in entry.get("command", "")
]

if missing_standard:
    print("C++17 without extensions is missing from:", file=sys.stderr)
    for source_file in missing_standard:
        print(f"  {source_file}", file=sys.stderr)
    sys.exit(1)
PY

cmake -S "${repo_root}" -B "${test_root}/override-build" \
    -DSDK_CONFIG="${config_file}" \
    -DSDK_GTEST=OFF >/dev/null

test -f "${test_root}/override-build/compile_commands.json"
grep -Fq "SDK_GTEST:BOOL=OFF" "${test_root}/override-build/CMakeCache.txt"

# Simulate a cache created before YAML values were tracked internally.
sed -i '/^SDK_YAML_VALUE_SDK_GTEST:/d' \
    "${test_root}/override-build/CMakeCache.txt"
cmake -S "${repo_root}" -B "${test_root}/override-build" \
    -DSDK_CONFIG="${config_file}" >/dev/null

grep -Fq "SDK_GTEST:BOOL=ON" "${test_root}/override-build/CMakeCache.txt"

cmake -S "${repo_root}" -B "${test_root}/debug-coverage-build" \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_CXX_COMPILER=clang++-18 \
    -DSDK_CONFIG="${config_file}" \
    -DSDK_GTEST=OFF \
    -DSDK_COVERAGE=ON >/dev/null

grep -Fq "SDK_GTEST:BOOL=OFF" "${test_root}/debug-coverage-build/CMakeCache.txt"
grep -Fq "SDK_COVERAGE:BOOL=ON" "${test_root}/debug-coverage-build/CMakeCache.txt"
grep -Fq -- "-fprofile-instr-generate" \
    "${test_root}/debug-coverage-build/compile_commands.json"

if cmake -S "${repo_root}" -B "${test_root}/release-coverage-build" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_COMPILER=clang++-18 \
    -DSDK_CONFIG="${config_file}" \
    -DSDK_GTEST=OFF \
    -DSDK_COVERAGE=ON >"${test_root}/release-coverage.log" 2>&1; then
    echo "Release coverage configuration unexpectedly succeeded." >&2
    exit 1
fi

grep -Fq "SDK_COVERAGE=ON is supported only for Debug builds" \
    "${test_root}/release-coverage.log"

echo "cmake_configuration_test: PASS"
