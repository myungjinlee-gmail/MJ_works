#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
versions_file="${repo_root}/configuration/dev-tools.env"

fail()
{
    printf '[coverage] ERROR: %s\n' "$*" >&2
    exit 1
}

usage()
{
    cat <<'EOF'
Usage: scripts/generate_coverage_report.sh <build-directory>

Merge existing LLVM raw profiles and generate an HTML coverage report.
The build directory must already contain the built SDK and profiles/*.profraw.
EOF
}

find_llvm_tool()
{
    local tool="$1"
    local candidate
    local output
    local actual
    local llvm_major="${LLVM_VERSION%%.*}"

    for candidate in "${tool}-${llvm_major}" "${tool}"; do
        if ! command -v "${candidate}" >/dev/null 2>&1; then
            continue
        fi

        output="$("${candidate}" --version 2>/dev/null | head -n 1)"
        actual="$(sed -nE 's/.*version ([0-9]+\.[0-9]+\.[0-9]+).*/\1/p' <<<"${output}")"
        if [[ "${actual}" == "${LLVM_VERSION}" ]]; then
            command -v "${candidate}"
            return 0
        fi
    done

    return 1
}

[[ -r "${versions_file}" ]] || fail "Version metadata not found: ${versions_file}"

# shellcheck disable=SC1090
source "${versions_file}"
: "${LLVM_VERSION:?LLVM_VERSION is required}"

llvm_cov="$(find_llvm_tool llvm-cov)" \
    || fail "llvm-cov ${LLVM_VERSION} is required; run scripts/setup_dev.sh."
llvm_profdata="$(find_llvm_tool llvm-profdata)" \
    || fail "llvm-profdata ${LLVM_VERSION} is required; run scripts/setup_dev.sh."

if [[ $# -ne 1 ]]; then
    usage >&2
    exit 2
fi

if [[ "$1" == /* ]]; then
    build_dir="$1"
else
    build_dir="${repo_root}/$1"
fi

[[ -d "${build_dir}" ]] || fail "Build directory not found: ${build_dir}"
build_dir="$(cd "${build_dir}" && pwd)"
profile_dir="${build_dir}/profiles"
profile_data="${build_dir}/coverage.profdata"
report_dir="${build_dir}/coverage"

[[ -d "${profile_dir}" ]] || fail "Profile directory not found: ${profile_dir}"

mapfile -d '' profile_files < <(
    find "${profile_dir}" -type f -name '*.profraw' -print0
)
[[ ${#profile_files[@]} -ne 0 ]] || fail "Tests did not produce LLVM coverage profiles."

"${llvm_profdata}" merge \
    --sparse \
    --output="${profile_data}" \
    "${profile_files[@]}"

mkdir -p "${report_dir}"
find "${report_dir}" -mindepth 1 -delete

coverage_object="${build_dir}/src/libmj_sdk.so"
[[ -r "${coverage_object}" ]] || fail "Coverage object not found: ${coverage_object}"

"${llvm_cov}" show "${coverage_object}" \
    --instr-profile="${profile_data}" \
    --format=html \
    --output-dir="${report_dir}" \
    --show-branches=count \
    --show-line-counts-or-regions \
    --ignore-filename-regex='(^|/)(build|customer_project|testcases|third_party)/'

"${llvm_cov}" report "${coverage_object}" \
    --instr-profile="${profile_data}" \
    --show-branch-summary \
    --ignore-filename-regex='(^|/)(build|customer_project|testcases|third_party)/'

printf '[coverage] HTML report: %s\n' "${report_dir}/index.html"
