# MJ_works

## Build

Development setup is explicit and is not run by a normal CMake configure.

Default configuration:

```bash
cmake -S . -B build -DSDK_CONFIG=configuration/default.yaml
cmake --build build
```

Run the reference customer project executable:

```bash
./build/customer_project/reference/mj_reference_app
```

Preset:

```bash
cmake --preset default
cmake --build --preset default
```

Override selected values from the command line:

```bash
cmake -S . -B build \
  -DSDK_CONFIG=configuration/default.yaml \
  -DSDK_HW_TARGET=vanilla \
  -DSDK_CAPTURE_TARGET=opencv \
  -DSDK_DISPLAY_TARGET=opencv
cmake --build build
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
SDK_ENABLE_TESTS : ON
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
| `SDK_ENABLE_TESTS` | Configure and register tests |

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
commits are checked by `githooks/commit-msg`.

### Optional PlantUML

PlantUML is documentation-only and is not installed by the bootstrap script.
The pinned JAR download, checksum verification, Java check, and future SVG
generation commands are documented in
[`third_party/plantuml/README.md`](third_party/plantuml/README.md).

## Folder Tree

- `docs/design`: design documents such as SWRS, SWAD, and coding guideline.
- `docs/template`: skeleton, example, and rule documents for design docs, C++ code, and test code.
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
