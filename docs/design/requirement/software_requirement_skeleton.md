# SWR-<DOMAIN>-<NNN>: <Requirement title>

<!--
Copy this file to SWR-<DOMAIN>-<NNN>-<kebab-case-title>.md.
This file represents exactly one requirement.
Replace every placeholder and remove instructional comments.
Read software_requirement_rule.md before authoring the requirement.
-->

| Field | Value |
| --- | --- |
| ID | `SWR-<DOMAIN>-<NNN>` |
| Type | `<Functional / Quality / Interface / Constraint / Configuration>` |
| Applicability | `<All, or a software configuration expression>` |

## Requirement

<!-- State one necessary, unambiguous, and verifiable obligation. -->

> The software shall <required behavior or quality>.

## Rationale

<!--
Link exactly one ticket that directly caused this requirement to be created.
Explain why the requirement is needed, not how it will be implemented.
-->

Initial ticket: [<TICKET-ID>](<location>)

<Reason this requirement is needed>

## Traceability

<!--
Use [ID](location) for every target and one target per nested list item.
Upstream includes the initial ticket and any direct parent requirement.
Downstream identifies design artifacts that realize this requirement.
Verification identifies Software Requirement Verification Specs, not tests or
evidence.
All three relationships require at least one link before the requirement is
accepted through the Pull Request workflow.
-->

- Upstream:
    - [<ID>](<location>)
- Downstream:
    - [<ID>](<location>)
- Verification:
    - [<SWRVS-ID>](<location>)
