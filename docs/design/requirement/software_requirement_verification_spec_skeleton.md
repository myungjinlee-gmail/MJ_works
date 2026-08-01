# SWRVS-<DOMAIN>-<NNN>: <Verification title>

<!--
Copy this file into the directory named for the SWR linked by `Covers`:
docs/design/requirement/<SWR-ID>/
Name the copied file:
SWRVS-<DOMAIN>-<NNN>-<kebab-case-title>.md
This file defines the verification of exactly one software requirement.

Replace every placeholder and remove instructional comments.
Read software_requirement_verification_spec_rule.md before authoring.

The Software Requirement Verification Spec shall not introduce new software
behavior, applicability, thresholds, tolerances, or timing constraints.
These obligations shall already be defined in the linked requirement.

Applicability is inherited from the linked requirement and is not repeated
in this document.
-->

## ID

`SWRVS-<DOMAIN>-<NNN>`

- Covers:
    - [<SWR-ID>](<location>)

## Acceptance Criteria

<!--
Define observable conditions used to determine whether the linked
requirement is satisfied.

Each acceptance criterion shall:
- be derived only from the linked requirement;
- have an observable Pass/Fail outcome;
- not introduce a new software obligation;
- have a stable local identifier.

One acceptance criterion may be verified by multiple verification measures.
One verification measure may cover multiple acceptance criteria.
-->

<a id="ac-01"></a>

### AC-01

<Observable acceptance condition>

<a id="ac-02"></a>

### AC-02

<Observable acceptance condition>

## Verification Measures

<!--
Define the measures needed to provide sufficient verification coverage
for the acceptance criteria.

A verification measure may be realized by a dynamic test, analysis,
review, static analysis, or another defined verification method.

Detailed test case formats and executed result formats are defined
separately.
-->

<a id="vm-01"></a>

### VM-01: <Verification measure title>

| Field | Value |
| --- | --- |
| Method | `<Dynamic test / Analysis / Review / Static analysis>` |
| Scope | `<What is included and excluded>` |
| Environment | `<Required verification environment>` |
| Preconditions | `<Required initial state and conditions>` |

#### Inputs

- <Input data, parameter, or analyzed artifact>

#### Procedure or Analysis Steps

1. <Verification step>
2. <Verification step>

#### Expected Results

- <Expected observable result>
- <Expected observable result>

#### Pass/Fail Rule

- Pass when <all required expected results are satisfied>.
- Fail when <any mandatory expected result is not satisfied>.

#### Traceability

- Covers:
    - [AC-01](#ac-01)
- Verification implementation:
    - [<TEST-CASE-OR-ANALYSIS-ID>](<location>)

<a id="vm-02"></a>

### VM-02: <Verification measure title>

| Field | Value |
| --- | --- |
| Method | `<Dynamic test / Analysis / Review / Static analysis>` |
| Scope | `<What is included and excluded>` |
| Environment | `<Required verification environment>` |
| Preconditions | `<Required initial state and conditions>` |

#### Inputs

- <Input data, parameter, or analyzed artifact>

#### Procedure or Analysis Steps

1. <Verification step>

#### Expected Results

- <Expected observable result>

#### Pass/Fail Rule

- Pass when <pass condition>.
- Fail when <fail condition>.

#### Traceability

- Covers:
    - [AC-01](#ac-01)
    - [AC-02](#ac-02)
- Verification implementation:
    - [<TEST-CASE-OR-ANALYSIS-ID>](<location>)

## Requirement Satisfaction Rule

<!--
Define the rule for making the final judgment on the linked requirement.
This section defines the rule only. The actual judgment belongs to the
verification result or release evidence.
-->

The linked requirement is satisfied when:

- every acceptance criterion is covered by at least one mandatory
  verification measure;
- every mandatory verification measure has been executed;
- every mandatory verification measure has passed; and
- no unresolved blocking anomaly invalidates the verification result.
