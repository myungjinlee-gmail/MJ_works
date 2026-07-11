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
SDK_ENABLE_TESTS : OFF
EOF

cmake -S "${repo_root}" -B "${test_root}/yaml-build" \
    -DSDK_CONFIG="${config_file}" >/dev/null

grep -Fq "SDK_RUN_DEV_SETUP:BOOL=OFF" "${test_root}/yaml-build/CMakeCache.txt"
grep -Fq "SDK_ENABLE_TESTS:BOOL=OFF" "${test_root}/yaml-build/CMakeCache.txt"

cat >"${config_file}" <<'EOF'
SDK_HW_TARGET : vanilla
SDK_OS_TARGET : linux
SDK_PROJECT_TARGET : reference
SDK_CAPTURE_TARGET : raw_file
SDK_DISPLAY_TARGET : raw_file
SDK_RUN_DEV_SETUP : OFF
SDK_ENABLE_TESTS : ON
EOF

cmake -S "${repo_root}" -B "${test_root}/yaml-build" \
    -DSDK_CONFIG="${config_file}" >/dev/null

grep -Fq "SDK_ENABLE_TESTS:BOOL=ON" "${test_root}/yaml-build/CMakeCache.txt"

cmake -S "${repo_root}" -B "${test_root}/override-build" \
    -DSDK_CONFIG="${config_file}" \
    -DSDK_ENABLE_TESTS=OFF >/dev/null

grep -Fq "SDK_ENABLE_TESTS:BOOL=OFF" "${test_root}/override-build/CMakeCache.txt"

# Simulate a cache created before YAML values were tracked internally.
sed -i '/^SDK_YAML_VALUE_SDK_ENABLE_TESTS:/d' \
    "${test_root}/override-build/CMakeCache.txt"
cmake -S "${repo_root}" -B "${test_root}/override-build" \
    -DSDK_CONFIG="${config_file}" >/dev/null

grep -Fq "SDK_ENABLE_TESTS:BOOL=ON" "${test_root}/override-build/CMakeCache.txt"

echo "cmake_configuration_test: PASS"
