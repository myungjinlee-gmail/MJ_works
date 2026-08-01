# SWR-<DOMAIN>-<NNN>: <Requirement title>

<!--
Create this directory:
docs/design/requirement/<SWR-ID>/
Copy this file to that directory as:
SWR-<DOMAIN>-<NNN>-<kebab-case-title>.md
Replace <SWR-ID> with this requirement's canonical SWR ID.
This file represents exactly one requirement.
Replace every placeholder and remove instructional comments.
Read software_requirement_rule.md before authoring the requirement.
-->

## Requirement metadata

### ID

<!--
Write this requirement's canonical ID.
-->

`SWR-<DOMAIN>-<NNN>`

### Type

`<Functional / Quality / Interface / Constraint / Configuration>`

### Applicability

`<All, or a software configuration expression>`

## Requirement

<!--
State one necessary, unambiguous, and verifiable obligation.
Include every condition, numeric value, unit, tolerance, and time limit that
defines the software obligation in this requirement. An SWRVS shall not
introduce a new obligation or limit.
-->

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
Downstream and Verification may be empty at acceptance. Complete all applicable
relationships before treating the requirement as verifiable or adding it to a
release baseline.
-->

- Upstream:
    - [<ID>](<location>)
- Downstream:
    - [<ID>](<location>)
- Verification:
    - [<SWRVS-ID>](<location>)
