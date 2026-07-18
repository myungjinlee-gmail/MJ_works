#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
test_root="$(mktemp -d "${TMPDIR:-/tmp}/mj-setup-test.XXXXXX")"
fake_bin="${test_root}/bin"
venv_path="${test_root}/venv"

cleanup()
{
    rm -rf "${test_root}"
}
trap cleanup EXIT

mkdir -p "${fake_bin}"

cat >"${fake_bin}/clang-format-18" <<'EOF'
#!/usr/bin/env bash
echo "Ubuntu clang-format version 18.1.3"
EOF

cat >"${fake_bin}/clang-tidy-18" <<'EOF'
#!/usr/bin/env bash
echo "Ubuntu LLVM version 18.1.3"
EOF

cat >"${fake_bin}/clang++-18" <<'EOF'
#!/usr/bin/env bash
echo "Ubuntu clang version 18.1.3"
EOF

cat >"${fake_bin}/llvm-cov-18" <<'EOF'
#!/usr/bin/env bash
echo "Ubuntu LLVM version 18.1.3"
EOF

cat >"${fake_bin}/llvm-profdata-18" <<'EOF'
#!/usr/bin/env bash
echo "Ubuntu LLVM version 18.1.3"
EOF

chmod +x \
    "${fake_bin}/clang-format-18" \
    "${fake_bin}/clang-tidy-18" \
    "${fake_bin}/clang++-18" \
    "${fake_bin}/llvm-cov-18" \
    "${fake_bin}/llvm-profdata-18"
ln -s "$(command -v python3)" "${fake_bin}/python3"

cat >"${test_root}/os-release" <<'EOF'
ID=ubuntu
VERSION_ID="24.04"
EOF

cat >"${test_root}/versions.env" <<EOF
SUPPORTED_OS_ID=ubuntu
SUPPORTED_OS_VERSION=24.04
LLVM_VERSION=18.1.3
LLVM_PACKAGE_VERSION=1:18.1.3-1ubuntu1
PYTHON_MIN_VERSION=3.10
PYTHON_VENV=${venv_path}
EOF

cat >"${test_root}/requirements.txt" <<'EOF'
# No network-installed packages are needed for the bootstrap behavior test.
EOF

run_setup()
{
    PATH="${fake_bin}:/usr/bin:/bin" \
        MJ_DEV_VERSIONS_FILE="${test_root}/versions.env" \
        MJ_DEV_REQUIREMENTS_FILE="${test_root}/requirements.txt" \
        MJ_SETUP_OS_RELEASE="${test_root}/os-release" \
        MJ_SETUP_SKIP_HOOKS=1 \
        bash "${repo_root}/scripts/setup_dev.sh" "$@"
}

if run_setup --check >/dev/null 2>&1; then
    echo "A clean environment unexpectedly passed check mode." >&2
    exit 1
fi
if [[ -e "${venv_path}" ]]; then
    echo "Check mode mutated the Python environment." >&2
    exit 1
fi

first_output="$(run_setup)"
grep -Fq "Creating Python environment" <<<"${first_output}"
grep -Fq "Development environment is ready" <<<"${first_output}"

second_output="$(run_setup)"
grep -Fq "Python environment already exists" <<<"${second_output}"
grep -Fq "Pinned Python tools already satisfied" <<<"${second_output}"
if grep -Fq "Installing system packages" <<<"${second_output}"; then
    echo "Second setup run attempted to reinstall a system package." >&2
    exit 1
fi

check_output="$(run_setup --check)"
grep -Fq "no changes were made" <<<"${check_output}"

cat >"${test_root}/unsupported-os-release" <<'EOF'
ID=debian
VERSION_ID="12"
EOF

if PATH="${fake_bin}:/usr/bin:/bin" \
    MJ_DEV_VERSIONS_FILE="${test_root}/versions.env" \
    MJ_DEV_REQUIREMENTS_FILE="${test_root}/requirements.txt" \
    MJ_SETUP_OS_RELEASE="${test_root}/unsupported-os-release" \
    MJ_SETUP_SKIP_HOOKS=1 \
    bash "${repo_root}/scripts/setup_dev.sh" --check >/dev/null 2>&1; then
    echo "Unsupported host unexpectedly passed setup." >&2
    exit 1
fi

echo "setup_dev_test: PASS"
