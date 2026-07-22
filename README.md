# MJ_works

[![CI](https://github.com/myungjinlee-gmail/MJ_works/actions/workflows/ci.yml/badge.svg)](https://github.com/myungjinlee-gmail/MJ_works/actions/workflows/ci.yml)

## Build

Development setup is explicit and is not run by a normal CMake configure.

Configure and build Debug or Release in a directory selected by the user:

```bash
cmake --preset debug -B build/debug
cmake --build build/debug --parallel

cmake --preset release -B build/release
cmake --build build/release --parallel
```

Both presets load `configuration/default.yaml` and enable GoogleTest with
`SDK_GTEST : ON`. Debug and Release use GCC without coverage instrumentation.
All project C++ targets compile as C++17 without compiler extensions.

Run the reference customer project executable:

```bash
./build/debug/customer_project/reference/mj_reference_app
```

Override selected values from the command line:

```bash
cmake -S . -B build \
  -DSDK_CONFIG=configuration/default.yaml \
  -DSDK_HW_TARGET=vanilla \
  -DSDK_CAPTURE_TARGET=opencv \
  -DSDK_DISPLAY_TARGET=opencv
cmake --build build --parallel
```

Run development setup during configure only when explicitly requested:

```bash
cmake -S . -B build -DSDK_RUN_DEV_SETUP=ON
```

The option is ignored when `CI` or `GITHUB_ACTIONS` is set so configuration
cannot install packages or change Git settings in CI.

## Configuration

The default YAML file is `configuration/default.yaml`.

```yaml
SDK_HW_TARGET : vanila
SDK_OS_TARGET : linux
SDK_PROJECT_TARGET : reference
SDK_CAPTURE_TARGET : raw
SDK_DISPLAY_TARGET : raw
SDK_RUN_DEV_SETUP : OFF
SDK_GTEST : ON
SDK_COVERAGE : OFF
```

Values passed with `-D` override values loaded from YAML. `vanila` is accepted as
an alias for the canonical `vanilla` target. `raw` is accepted as an alias for
the canonical `raw_file` capture and display target. Boolean values must be
written as `ON` or `OFF`.

All SDK build parameters are read from the selected YAML file:

| Parameter | Purpose |
| --- | --- |
| `SDK_HW_TARGET` | Hardware implementation |
| `SDK_OS_TARGET` | OS abstraction implementation |
| `SDK_PROJECT_TARGET` | Customer project |
| `SDK_CAPTURE_TARGET` | Capture implementation |
| `SDK_DISPLAY_TARGET` | Display implementation |
| `SDK_RUN_DEV_SETUP` | Run the development bootstrap during configure |
| `SDK_GTEST` | Configure and register GoogleTest-based tests |
| `SDK_COVERAGE` | Enable LLVM coverage instrumentation for Debug builds |

`SDK_CONFIG` is the only bootstrap parameter that cannot be supplied by the
selected YAML file because it identifies which YAML file CMake must read. It
can be selected with `-DSDK_CONFIG=<path>` or a CMake preset.

Changes to the YAML file are applied on the next CMake configure. A value
explicitly overridden with `-D` remains an override in that build directory;
remove its cache entry with `cmake -U <parameter> -S . -B build` to return
control to the YAML file.

## Development Setup

The supported development host is Ubuntu 24.04, either native or under WSL.
Other host operating systems fail before any installation is attempted. SDK
build targets such as `SDK_OS_TARGET=windows` do not change the supported
development host.

| Dependency | Required version | Installation |
| --- | --- | --- |
| clang-format | 18.1.3 | Ubuntu package `clang-format-18` |
| clang-tidy | 18.1.3 | Ubuntu package `clang-tidy-18` |
| Clang C++ compiler | 18.1.3 | Ubuntu package `clang-18` |
| llvm-cov and llvm-profdata | 18.1.3 | Ubuntu package `llvm-18` |
| Python | 3.10 or newer | Host `python3` |
| cmakelang | 0.6.13 | Project virtual environment |
| yamllint | 1.35.1 | Project virtual environment |

Prepare a clean development environment with one command:

```bash
bash scripts/setup_dev.sh
```

The script installs missing Ubuntu packages, creates `.venv`, installs the
exact Python tool versions from `configuration/requirements-dev.txt`, and
configures the repository Git hooks. It checks versions before each operation,
so running the command again does not reinstall satisfied dependencies.

Package installation may request `sudo`. Inspect the environment without
making changes:

```bash
bash scripts/setup_dev.sh --check
```

Activate the Python environment when invoking its tools directly:

```bash
source .venv/bin/activate
cmake-format --version
yamllint --version
```

Pinned environment versions are recorded in `configuration/dev-tools.env`.
The commit message rule is defined in `docs/process/git_workflow.md`. Local
commit messages are checked by `githooks/commit-msg`. Staged C/C++ content is
automatically formatted by `githooks/pre-commit` before the commit is created.

Check or automatically fix C/C++ formatting with the shared local and CI
script:

```bash
bash scripts/format.sh --check
bash scripts/format.sh --fix
```

Run the same clang-tidy analysis used by CI after configuring and building the
test-enabled project:

```bash
cmake --preset release -B build/release
cmake --build build/release --parallel
python3 scripts/clang_tidy.py --build-dir build/release
```

Build the Clang-based Coverage preset, run the tests with LLVM profiling
enabled, and then generate a detailed source-based HTML coverage report:

```bash
cmake --preset coverage -B build/coverage
cmake --build build/coverage --parallel

mkdir -p build/coverage/profiles
find build/coverage -type f -name '*.profraw' -delete

LLVM_PROFILE_FILE="$(pwd)/build/coverage/profiles/%p.profraw" \
    ctest --test-dir build/coverage --output-on-failure

bash scripts/generate_coverage_report.sh build/coverage
```

The Coverage preset explicitly uses `-g` and `-O0`. CMake adds
`-fprofile-instr-generate` and `-fcoverage-mapping` only when
`SDK_COVERAGE=ON`. The report script only merges existing raw profiles with
`llvm-profdata` and writes the `llvm-cov` HTML report to
`build/coverage/coverage/index.html`.

CMake always writes `compile_commands.json` to the selected build directory.
Static-analysis directory exclusions are listed one repository-relative path
per line in `configuration/clang-tidy-exclude.txt`. Compiled generated C/C++
code remains included unless its directory is explicitly listed. The enabled
checks, compiler-warning supplements, and known coverage limits are documented
in [`docs/process/static_analysis.md`](docs/process/static_analysis.md).

## Development Process

- [`docs/process/coding_guideline.md`](docs/process/coding_guideline.md) defines
  the project coding rules.
- [`docs/process/git_workflow.md`](docs/process/git_workflow.md) defines branch,
  commit, Pull Request, and merge rules.
- [`.github/pull_request_template.md`](.github/pull_request_template.md)
  contains the reviewer workflow, required checks, and review-summary format.

### Optional PlantUML

PlantUML is documentation-only and is not installed by the bootstrap script.
The pinned JAR download, checksum verification, Java check, and future SVG
generation commands are documented in
[`third_party/plantuml/README.md`](third_party/plantuml/README.md).

## Folder Tree

- `docs/design`: requirements and architecture design documents.
- `docs/process`: coding, Git, review, and analysis policies.
- `docs/template`: reusable design, implementation, test, and review templates.
- `.github`: GitHub issue and pull request configuration.
- `cmake`: common CMake functions and helpers.
- `configuration`: YAML-based CMake configuration files.
- `customer_project`: customer-facing integration projects.
- `githooks`: version-controlled Git hooks.
- `include`: public SDK headers.
- `scripts`: development setup and validation scripts.
- `src`: internal SDK library implementation.
- `testcases`: GoogleTest-based test skeletons.
- `tools`: development helper tools.
