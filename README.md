# MJ_works

## Build

The development setup script runs during CMake configure by default and
configures the repository Git hooks.

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

Skip development setup during configure:

```bash
cmake -S . -B build -DSDK_RUN_DEV_SETUP=OFF
```

## Configuration

The default YAML file is `configuration/default.yaml`.

```yaml
SDK_HW_TARGET : vanila
SDK_OS_TARGET : linux
SDK_PROJECT_TARGET : reference
SDK_CAPTURE_TARGET : raw
SDK_DISPLAY_TARGET : raw
```

Values passed with `-D` override values loaded from YAML. `vanila` is accepted as
an alias for the canonical `vanilla` target. `raw` is accepted as an alias for
the canonical `raw_file` capture and display target.

## Development Setup

Run setup manually:

```bash
bash scripts/setup_dev.sh
```

The commit message rule is defined in `docs/process/git_workflow.md`. Local
commits are checked by `githooks/commit-msg`.

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
