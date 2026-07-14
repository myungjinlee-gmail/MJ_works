#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
versions_file="${MJ_DEV_VERSIONS_FILE:-${repo_root}/configuration/dev-tools.env}"

usage()
{
    cat <<'EOF'
Usage:
  scripts/format.sh --check
  scripts/format.sh --fix
  scripts/format.sh --staged
  scripts/format.sh --fix-staged
  scripts/format.sh --changed <base> <head>

  --check                 Check all tracked project C/C++ files.
  --fix                   Format all tracked project C/C++ files.
  --staged                Check C/C++ content staged for commit.
  --fix-staged            Format staged C/C++ content for commit.
  --changed <base> <head> Check C/C++ files changed between revisions.
EOF
}

fail()
{
    printf '[format] ERROR: %s\n' "$*" >&2
    exit 1
}

is_cpp_file()
{
    case "$1" in
        *.c | *.cc | *.cpp | *.cxx | *.h | *.hh | *.hpp | *.hxx)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

is_excluded_path()
{
    case "/$1/" in
        */third_party/* | */build/* | */generated/*)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

find_clang_format()
{
    local actual
    local candidate
    local llvm_major="${LLVM_VERSION%%.*}"
    local output

    for candidate in "clang-format-${llvm_major}" clang-format; do
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

collect_tracked_files()
{
    local path

    while IFS= read -r -d '' path; do
        if ! is_excluded_path "${path}"; then
            files+=("${path}")
        fi
    done < <(
        git -C "${repo_root}" ls-files -z -- \
            '*.c' '*.cc' '*.cpp' '*.cxx' \
            '*.h' '*.hh' '*.hpp' '*.hxx'
    )
}

collect_staged_files()
{
    local path

    while IFS= read -r -d '' path; do
        if is_cpp_file "${path}" && ! is_excluded_path "${path}"; then
            files+=("${path}")
        fi
    done < <(
        git -C "${repo_root}" diff --cached \
            --name-only --diff-filter=ACMR -z
    )
}

collect_changed_files()
{
    local base="$1"
    local head="$2"
    local path

    git -C "${repo_root}" cat-file -e "${base}^{commit}" 2>/dev/null \
        || fail "Base revision is not available: ${base}"
    git -C "${repo_root}" cat-file -e "${head}^{commit}" 2>/dev/null \
        || fail "Head revision is not available: ${head}"

    while IFS= read -r -d '' path; do
        if is_cpp_file "${path}" && ! is_excluded_path "${path}"; then
            files+=("${path}")
        fi
    done < <(
        git -C "${repo_root}" diff "${base}...${head}" \
            --name-only --diff-filter=ACMR -z
    )
}

check_worktree_files()
{
    local failed=0
    local path

    for path in "${files[@]}"; do
        if ! "${clang_format}" --dry-run --Werror --style=file \
            "${repo_root}/${path}"; then
            printf '[format] Incorrect format: %s\n' "${path}" >&2
            failed=1
        fi
    done

    return "${failed}"
}

check_staged_files()
{
    local failed=0
    local path

    for path in "${files[@]}"; do
        if ! git -C "${repo_root}" show ":${path}" \
            | "${clang_format}" --dry-run --Werror --style=file \
                --assume-filename="${repo_root}/${path}"; then
            printf '[format] Incorrect staged format: %s\n' "${path}" >&2
            failed=1
        fi
    done

    return "${failed}"
}

format_staged_files()
{
    local blob
    local entry
    local formatted
    local mode
    local original
    local path
    local update_worktree
    local worktree_path
    local temporary_dir

    temporary_dir="$(mktemp -d "${TMPDIR:-/tmp}/mj-format-staged.XXXXXX")"
    trap 'rm -rf "${temporary_dir}"' EXIT

    for path in "${files[@]}"; do
        original="${temporary_dir}/original"
        formatted="${temporary_dir}/formatted"
        worktree_path="${repo_root}/${path}"

        git -C "${repo_root}" show ":${path}" >"${original}"
        "${clang_format}" --style=file \
            --assume-filename="${worktree_path}" \
            <"${original}" >"${formatted}"

        if cmp -s "${original}" "${formatted}"; then
            continue
        fi

        update_worktree=0
        if [[ -f "${worktree_path}" ]] \
            && cmp -s "${original}" "${worktree_path}"; then
            update_worktree=1
        fi

        entry="$(git -C "${repo_root}" ls-files --stage -- "${path}")"
        mode="${entry%% *}"
        [[ "${mode}" =~ ^[0-9]{6}$ ]] \
            || fail "Unable to read staged file mode: ${path}"

        blob="$(git -C "${repo_root}" hash-object -w "${formatted}")"
        git -C "${repo_root}" update-index \
            --cacheinfo "${mode}" "${blob}" "${path}"

        if [[ ${update_worktree} -eq 1 ]]; then
            cp "${formatted}" "${worktree_path}"
        fi

        printf '[format] Formatted staged content: %s\n' "${path}"
    done

    rm -rf "${temporary_dir}"
    trap - EXIT
}

if [[ $# -eq 0 ]]; then
    usage >&2
    exit 2
fi

mode="$1"
case "${mode}" in
    --check | --fix | --staged | --fix-staged)
        if [[ $# -ne 1 ]]; then
            usage >&2
            exit 2
        fi
        ;;
    --changed)
        if [[ $# -ne 3 ]]; then
            usage >&2
            exit 2
        fi
        base_revision="$2"
        head_revision="$3"
        ;;
    *)
        usage >&2
        exit 2
        ;;
esac

[[ -r "${versions_file}" ]] || fail "Version metadata not found: ${versions_file}"

# shellcheck disable=SC1090
source "${versions_file}"
: "${LLVM_VERSION:?LLVM_VERSION is required}"

clang_format="$(find_clang_format)" \
    || fail "clang-format ${LLVM_VERSION} is required; run scripts/setup_dev.sh."

declare -a files=()
if [[ "${mode}" == "--staged" || "${mode}" == "--fix-staged" ]]; then
    collect_staged_files
elif [[ "${mode}" == "--changed" ]]; then
    collect_changed_files "${base_revision}" "${head_revision}"
else
    collect_tracked_files
fi

if [[ ${#files[@]} -eq 0 ]]; then
    printf '[format] No C/C++ files to process.\n'
    exit 0
fi

case "${mode}" in
    --check | --changed)
        if [[ "${mode}" == "--changed" ]]; then
            printf '[format] Checking %d changed C/C++ files.\n' "${#files[@]}"
        else
            printf '[format] Checking %d tracked C/C++ files.\n' "${#files[@]}"
        fi
        if ! check_worktree_files; then
            fail "Formatting check failed; run scripts/format.sh --fix."
        fi
        ;;
    --fix)
        printf '[format] Formatting %d tracked C/C++ files.\n' "${#files[@]}"
        for path in "${files[@]}"; do
            "${clang_format}" -i --style=file "${repo_root}/${path}"
        done
        ;;
    --staged)
        printf '[format] Checking %d staged C/C++ files.\n' "${#files[@]}"
        if ! check_staged_files; then
            fail "Staged formatting check failed; run scripts/format.sh --fix and stage the result."
        fi
        ;;
    --fix-staged)
        printf '[format] Formatting %d staged C/C++ files.\n' "${#files[@]}"
        format_staged_files
        if ! check_staged_files; then
            fail "Staged formatting failed."
        fi
        ;;
esac

printf '[format] PASS\n'
