# MJ_works

## Build

Default configuration:

```bash
cmake -S . -B build -DSDK_CONFIG=configuration/default.yaml
cmake --build build
```

Run the reference customer project executable:

```bash
./build/mj_reference_app
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
an alias for the canonical `vanilla` target.
