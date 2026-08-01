# SWRVS-CFG-001: Hardware target selection verification

> **Illustrative example — non-normative.**
>
> This file demonstrates the Software Requirement Verification Spec format and
> does not serve as project verification authority.

## ID

`SWRVS-CFG-001`

- Covers:
    - [SWR-CFG-001](software_requirement_example.md)

## Acceptance Criteria

<a id="ac-01"></a>

### AC-01

Configuring with `SDK_HW_TARGET=vanilla` includes the vanilla hardware-target
implementation and excludes the NVIDIA and Arm implementations.

<a id="ac-02"></a>

### AC-02

Configuring with `SDK_HW_TARGET=nvidia` includes the NVIDIA hardware-target
implementation and excludes the vanilla and Arm implementations.

<a id="ac-03"></a>

### AC-03

Configuring with `SDK_HW_TARGET=arm` includes the Arm hardware-target
implementation and excludes the vanilla and NVIDIA implementations.

## Verification Measures

<a id="vm-01"></a>

### VM-01: Canonical hardware-target build selection

| Field | Value |
| --- | --- |
| Method | `Dynamic test` |
| Scope | Configuration and build-source selection for each canonical `SDK_HW_TARGET` value |
| Environment | Supported Ubuntu development host with CMake |
| Preconditions | Fixed source revision and development tool versions; one clean build directory per input |

#### Inputs

- `SDK_HW_TARGET=vanilla`
- `SDK_HW_TARGET=nvidia`
- `SDK_HW_TARGET=arm`

#### Procedure or Analysis Steps

1. Configure a separate clean build directory with each input.
2. Inspect the configured build sources for included hardware-target
   implementations in each directory.
3. Record the source revision, input, configuration result, and selected-source
   evidence for every input.

#### Expected Results

- The `vanilla` input includes the vanilla implementation and excludes the
  NVIDIA and Arm implementations.
- The `nvidia` input includes the NVIDIA implementation and excludes the
  vanilla and Arm implementations.
- The `arm` input includes the Arm implementation and excludes the vanilla and
  NVIDIA implementations.
- Evidence identifies the source revision, input, and observed result for every
  configuration.

#### Pass/Fail Rule

- Pass when every expected result is satisfied and the required evidence is
  produced.
- Fail when any selected implementation is incorrect, any unselected
  implementation is included, or required evidence is missing.

#### Traceability

- Covers:
    - [AC-01](#ac-01)
    - [AC-02](#ac-02)
    - [AC-03](#ac-03)
- Verification implementation:
    - `TBD`

## Requirement Satisfaction Rule

The linked requirement is satisfied when:

- every acceptance criterion is covered by at least one mandatory verification
  measure;
- every mandatory verification measure has been executed;
- every mandatory verification measure has passed; and
- no unresolved blocking anomaly invalidates the verification result.
