# SWR-CFG-001: Hardware target selection

> **Illustrative example — non-normative.**
>
> This file demonstrates the requirement format. It is not an accepted project
> requirement and does not serve as product authority. Its linked Software
> Requirement Verification Spec is also a non-normative example.

## Requirement metadata

### ID

`SWR-CFG-001`

### Type

`Configuration`

### Applicability

`SDK_HW_TARGET in {vanilla, nvidia, arm}`

## Requirement

> The software shall include exactly one hardware-target implementation selected by the canonical `SDK_HW_TARGET` value in each configured build.

## Rationale

Initial ticket: [ISSUE-22](https://github.com/myungjinlee-gmail/MJ_works/issues/22)

Each delivered software variant needs one unambiguous hardware implementation.
Excluding unselected implementations prevents accidental coupling to another
target and makes the contents of the build artifact predictable.

## Traceability

- Upstream:
    - [ISSUE-22](https://github.com/myungjinlee-gmail/MJ_works/issues/22)
- Downstream:
- Verification:
    - [SWRVS-CFG-001](software_requirement_verification_example_rule.md)
