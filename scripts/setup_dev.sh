#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
versions_file="${MJ_DEV_VERSIONS_FILE:-${repo_root}/configuration/dev-tools.env}"
requirements_file="${MJ_DEV_REQUIREMENTS_FILE:-${repo_root}/configuration/requirements-dev.txt}"
os_release_file="${MJ_SETUP_OS_RELEASE:-/etc/os-release}"
check_only=0

usage()
{
    cat <<'EOF'
Usage: scripts/setup_dev.sh [--check]

Prepare the supported development environment. Use --check to report missing
dependencies without changing the system, Python environment, or Git config.
EOF
}

log()
{
    printf '[setup] %s\n' "$*"
}

fail()
{
    printf '[setup] ERROR: %s\n' "$*" >&2
    exit 1
}

if [[ "${1:-}" == "--check" ]]; then
    check_only=1
    shift
fi

if [[ $# -ne 0 ]]; then
    usage >&2
    exit 2
fi

[[ -r "${versions_file}" ]] || fail "Version metadata not found: ${versions_file}"
[[ -r "${requirements_file}" ]] || fail "Python requirements not found: ${requirements_file}"

# shellcheck disable=SC1090
source "${versions_file}"

: "${SUPPORTED_OS_ID:?SUPPORTED_OS_ID is required}"
: "${SUPPORTED_OS_VERSION:?SUPPORTED_OS_VERSION is required}"
: "${LLVM_VERSION:?LLVM_VERSION is required}"
: "${LLVM_PACKAGE_VERSION:?LLVM_PACKAGE_VERSION is required}"
: "${PYTHON_MIN_VERSION:?PYTHON_MIN_VERSION is required}"
: "${PYTHON_VENV:?PYTHON_VENV is required}"

[[ -r "${os_release_file}" ]] || fail "OS metadata not found: ${os_release_file}"

# shellcheck disable=SC1090
source "${os_release_file}"

if [[ "${ID:-}" != "${SUPPORTED_OS_ID}" || "${VERSION_ID:-}" != "${SUPPORTED_OS_VERSION}" ]]; then
    fail "Unsupported host ${ID:-unknown} ${VERSION_ID:-unknown}; supported host is ${SUPPORTED_OS_ID} ${SUPPORTED_OS_VERSION} (native or WSL)."
fi

version_at_least()
{
    local actual="$1"
    local required="$2"

    printf '%s\n%s\n' "${required}" "${actual}" | sort -V -C
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

python_version_is_supported()
{
    local python_command="$1"
    local actual

    actual="$(${python_command} -c 'import platform; print(platform.python_version())')"
    version_at_least "${actual}" "${PYTHON_MIN_VERSION}"
}

python_dependencies_satisfied()
{
    local python_command="$1"

    "${python_command}" - "${requirements_file}" <<'PY'
import importlib.metadata
import pathlib
import sys

requirements = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
for raw_requirement in requirements:
    requirement = raw_requirement.strip()
    if not requirement or requirement.startswith("#"):
        continue
    if "==" not in requirement:
        raise SystemExit(f"Unpinned requirement: {requirement}")
    package, expected = requirement.split("==", 1)
    try:
        actual = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        raise SystemExit(1)
    if actual != expected:
        raise SystemExit(1)
PY
}

install_system_packages()
{
    local packages=("$@")
    local privilege=()

    if [[ ${#packages[@]} -eq 0 ]]; then
        return
    fi

    if [[ ${EUID} -ne 0 ]]; then
        command -v sudo >/dev/null 2>&1 || fail "sudo is required to install: ${packages[*]}"
        privilege=(sudo)
    fi

    log "Installing system packages: ${packages[*]}"
    "${privilege[@]}" apt-get update
    "${privilege[@]}" apt-get install -y "${packages[@]}"
}

missing_packages=()

if clang_format_path="$(find_llvm_tool clang-format)"; then
    log "clang-format ${LLVM_VERSION} already satisfied: ${clang_format_path}"
else
    log "clang-format ${LLVM_VERSION} is missing"
    missing_packages+=("clang-format-${LLVM_VERSION%%.*}=${LLVM_PACKAGE_VERSION}")
fi

if clang_tidy_path="$(find_llvm_tool clang-tidy)"; then
    log "clang-tidy ${LLVM_VERSION} already satisfied: ${clang_tidy_path}"
else
    log "clang-tidy ${LLVM_VERSION} is missing"
    missing_packages+=("clang-tidy-${LLVM_VERSION%%.*}=${LLVM_PACKAGE_VERSION}")
fi

if clang_cxx_path="$(find_llvm_tool clang++)"; then
    log "clang++ ${LLVM_VERSION} already satisfied: ${clang_cxx_path}"
else
    log "clang++ ${LLVM_VERSION} is missing"
    missing_packages+=("clang-${LLVM_VERSION%%.*}=${LLVM_PACKAGE_VERSION}")
fi

llvm_coverage_tools_available=1
for llvm_tool in llvm-cov llvm-profdata; do
    if llvm_tool_path="$(find_llvm_tool "${llvm_tool}")"; then
        log "${llvm_tool} ${LLVM_VERSION} already satisfied: ${llvm_tool_path}"
    else
        log "${llvm_tool} ${LLVM_VERSION} is missing"
        llvm_coverage_tools_available=0
    fi
done

if [[ ${llvm_coverage_tools_available} -eq 0 ]]; then
    missing_packages+=("llvm-${LLVM_VERSION%%.*}=${LLVM_PACKAGE_VERSION}")
fi

if command -v python3 >/dev/null 2>&1 && python_version_is_supported python3; then
    log "Python ${PYTHON_MIN_VERSION}+ already satisfied: $(python3 --version 2>&1)"
else
    fail "Python ${PYTHON_MIN_VERSION} or newer is required. Install python3 before running setup."
fi

if ! python3 -m venv --help >/dev/null 2>&1; then
    log "Python venv support is missing"
    missing_packages+=(python3-venv)
fi

if [[ "${PYTHON_VENV}" == /* ]]; then
    venv_path="${PYTHON_VENV}"
else
    venv_path="${repo_root}/${PYTHON_VENV}"
fi
venv_python="${venv_path}/bin/python"

if [[ ${check_only} -eq 1 ]]; then
    if [[ ${#missing_packages[@]} -ne 0 ]]; then
        fail "Missing system packages: ${missing_packages[*]}"
    fi
    [[ -x "${venv_python}" ]] || fail "Python environment is missing: ${venv_path}"
    python_dependencies_satisfied "${venv_python}" || fail "Pinned Python tools are not satisfied."
    log "Pinned Python tools already satisfied"
    log "Development environment check passed; no changes were made."
    exit 0
fi

install_system_packages "${missing_packages[@]}"

find_llvm_tool clang-format >/dev/null || fail "clang-format ${LLVM_VERSION} was not available after installation."
find_llvm_tool clang-tidy >/dev/null || fail "clang-tidy ${LLVM_VERSION} was not available after installation."
find_llvm_tool clang++ >/dev/null || fail "clang++ ${LLVM_VERSION} was not available after installation."
find_llvm_tool llvm-cov >/dev/null || fail "llvm-cov ${LLVM_VERSION} was not available after installation."
find_llvm_tool llvm-profdata >/dev/null || fail "llvm-profdata ${LLVM_VERSION} was not available after installation."

if [[ ! -x "${venv_python}" ]]; then
    log "Creating Python environment: ${venv_path}"
    python3 -m venv "${venv_path}"
else
    log "Python environment already exists: ${venv_path}"
fi

if python_dependencies_satisfied "${venv_python}"; then
    log "Pinned Python tools already satisfied"
else
    log "Installing pinned Python tools"
    "${venv_python}" -m pip install --disable-pip-version-check --requirement "${requirements_file}"
    python_dependencies_satisfied "${venv_python}" || fail "Pinned Python tool verification failed."
fi

if [[ "${MJ_SETUP_SKIP_HOOKS:-0}" == "1" ]]; then
    log "Git hook setup skipped by MJ_SETUP_SKIP_HOOKS"
else
    bash "${script_dir}/setup_hooks.sh"
fi

log "Development environment is ready."
