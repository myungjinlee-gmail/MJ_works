# Software Requirement Authoring Rule

## Purpose

This rule defines how to write requirements that are readable by people,
consistently interpretable by language models, and traceable through design and
verification.

## Requirement boundary

One requirement file owns:

- one requirement ID;
- one normative requirement statement;
- its type and applicability;
- its rationale and initial ticket; and
- its upstream, downstream, and Software Requirement Verification Spec links.

It shall not contain:

- acceptance criteria;
- verification methods or procedures;
- expected verification results;
- verification implementation details; or
- verification results and evidence.

Acceptance criteria and the detailed definition of how to verify the
requirement belong to a separately identified Software Requirement
Verification Spec.

## File and identifier rules

- Store exactly one normative requirement in each authored requirement file.
- Create one `docs/design/requirement/<SWR-ID>/` directory for each authored
  SWR, using the canonical SWR ID as the directory name.
- Store exactly one SWR file in that directory.
- Name the file `SWR-<DOMAIN>-<NNN>-<kebab-case-title>.md`.
- Make the title heading ID, `Requirement metadata` > `ID` value, and filename
  ID agree.
- Use a short, stable uppercase domain. Do not encode a component name in the
  domain when the requirement applies to the software as a whole.
- Allocate IDs monotonically within a domain.
- Do not reuse or renumber an accepted or removed requirement ID.
- Use one `Requirement metadata` section with `ID`, `Type`, and `Applicability`
  subsections instead of a summary table.
- Preserve the skeleton heading order and section and subsection names. This
  makes files comparable and supports reliable automated extraction.

The README, rules, skeletons, examples, and review checklists in
`docs/design/requirement/` are control documents and are exceptions to the
authored SWR directory and filename rules.

## Acceptance through the Pull Request workflow

Do not store a status field in a requirement:

- content on an unmerged working branch is a draft;
- content merged through the required Pull Request workflow is accepted; and
- rejected content is not merged.

Git history records revisions and removals. If a requirement is replaced or
removed, update all current trace links in the same Pull Request. Do not leave a
current design or verification artifact pointing to an obsolete requirement.

## Requirement metadata

### ID

The ID is the permanent reference to the requirement. The title is a short noun
phrase that helps a reader find it; the title does not replace the normative
statement.

Write the canonical ID as the standalone value in the `ID` subsection.

Good:

```markdown
# SWR-CFG-001: Hardware target selection

## Requirement metadata

### ID

`SWR-CFG-001`
```

Avoid encoding status, implementation, priority, or a date in the ID.

### Type

Use the single type that best describes the obligation:

- `Functional`: externally observable behavior.
- `Quality`: a measurable performance, reliability, security, portability, or
  other quality level.
- `Interface`: behavior or compatibility at a software boundary.
- `Constraint`: a mandatory limitation on the solution or environment.
- `Configuration`: selection, inclusion, exclusion, or validity of a software
  variant.

Do not combine types in one field. Split requirements when they contain
independent obligations.

Write the selected type as the standalone value in the `Type` subsection.

### Applicability

`Applicability` identifies the software or build configurations in which the
requirement applies. Its current scope is configuration applicability only. It
does not describe requirement priority, implementation ownership, release
schedule, stakeholder scope, or verification environment.

Use `All` when the requirement applies to every supported configuration.
Otherwise, write an explicit expression using canonical configuration
dimensions and values.

Write `All` or the explicit expression as the standalone value in the
`Applicability` subsection.

Examples:

```text
SDK_HW_TARGET in {vanilla, nvidia, arm}
SDK_COVERAGE == ON
SDK_OS_TARGET == linux AND SDK_HW_TARGET == nvidia
```

Do not use phrases such as "where applicable" or "on supported systems" without
also identifying the exact applicability rule.

`Applicability` does not define which configuration values or combinations the
software supports. A Configuration requirement defines those obligations; this
field only selects the configurations in which the current requirement is
active.

## Requirement statement

Write exactly one normative statement in the `Requirement` section.

The statement shall:

- start with `The software shall`;
- express one necessary outcome, behavior, or measurable quality;
- identify the relevant condition and observable response;
- be sufficiently precise for a Software Requirement Verification Spec to derive
  acceptance criteria without changing its meaning;
- remain independent of classes, functions, filenames, and algorithms unless
  those implementation details are themselves mandated constraints; and
- use defined terms consistently.

Split a statement when separate parts can be implemented, changed, or verified
independently. A list joined by `and` usually indicates multiple requirements.

Avoid subjective or weak terms such as:

- appropriate;
- adequate;
- user-friendly;
- as needed;
- normally;
- if possible;
- should; and
- may, when it is intended as an obligation.

Replace them with a measurable condition or a defined term.

## Rationale and initial ticket

Explain the need, risk, or stakeholder value that justifies the requirement.
Do not repeat the statement and do not prescribe the design. A reviewer should
be able to use the rationale to judge whether a proposed change preserves the
original intent.

Record exactly one initial ticket before the explanatory prose:

```markdown
Initial ticket: [ISSUE-22](https://github.com/myungjinlee-gmail/MJ_works/issues/22)
```

The initial ticket:

- identifies the direct event that caused the requirement to be created;
- uses the canonical ticket ID as its link label;
- remains unchanged for corrections that preserve the obligation; and
- is not a chronological list of every later change request.

Use Git and Pull Request history for corrections and non-semantic changes.
When a change request materially changes the obligation, scope, or
applicability, create a new requirement ID and record that change request as the
new requirement's initial ticket.

The same initial-ticket link also appears under `Upstream`. The Rationale owns
the human explanation; the `Traceability` section owns the machine-readable
relationship.

## Traceability

Place `Traceability` as the final section, after `Rationale`. Use a nested list,
not a table:

```markdown
## Traceability

- Upstream:
    - [ISSUE-22](https://github.com/myungjinlee-gmail/MJ_works/issues/22)
    - [SWR-SYS-001](SWR-SYS-001-system-configuration.md)
- Downstream:
    - [COMP-HW-001](../architecture/architecture.md#comp-hw-001)
- Verification:
    - [SWRVS-CFG-001](software_requirement_verification_example_rule.md)
```

Every target shall use:

```markdown
[<ID>](<location>)
```

The link label is the target's canonical ID, not a title or description. Write
one target per nested list item. Use repository-relative links for live
repository artifacts and external URLs for external artifacts.

Use a stable ID anchor, implemented as a heading or explicit anchor, when a file
contains multiple identified targets. Use a commit-specific permalink when
immutable line-level evidence is needed; do not use mutable branch line numbers
as durable trace locations.

### Upstream

`Upstream` identifies the direct reason or higher-level obligation from which
the requirement originates:

- repeat the initial ticket link from `Rationale`; and
- add direct parent requirements, contracts, or other identified authoritative
  inputs when applicable.

Upstream is not a change log. Do not append every Pull Request or later change
request.

### Downstream

`Downstream` identifies architecture or lower-level design artifacts that
realize the requirement. Link the closest owned design level rather than every
transitive implementation file.

Architecture and lower-level design artifacts shall provide the reverse link
to this requirement.

### Verification

`Verification` links only Software Requirement Verification Specs. Do not link
test code, commands, reports, or result evidence directly from the software
requirement. The ownership and acceptance rules are defined in
[the SWRVS authoring rule](software_requirement_verification_spec_rule.md).

### Missing relationships

Acceptance of a requirement approves the software obligation; it does not mean
that development or verification is complete. At acceptance, `Upstream` shall
link the initial ticket and every other authoritative input that already
exists. `Verification` shall link the SWRVS artifacts accepted with the SWR,
and each SWRVS shall link back to the SWR. `Downstream` may have no targets
while its design artifacts do not yet exist.

Keep the `Upstream`, `Downstream`, and `Verification` relationship labels even
when a relationship has no target. Do not use `None`, `TBD`, a placeholder, or
a link to a planned location in an accepted requirement. Add concrete
`[ID](location)` links incrementally as the corresponding artifacts are added,
and add the reverse link in the same Pull Request.

A requirement becomes verification-ready when the software implementation,
downstream design, and verification implementations needed to evaluate its
satisfaction exist. Before treating the requirement as verification-ready, and
before it enters a release baseline, each relationship shall contain at least
one concrete target, every applicable direct relationship shall be recorded,
and all required reverse links shall exist.

## Configuration requirements

A configuration requirement shall distinguish:

- a variation point from each selectable variant;
- canonical values from accepted aliases;
- build-time selection from runtime configuration;
- exactly-one selection from optional or independent feature selection;
- supported combinations from invalid combinations; and
- source inclusion from behavior that is merely disabled at runtime.

Do not assume that a build option guarantees source exclusion. State artifact
or inclusion behavior explicitly when it is required.

## Human and language-model readability

- Keep the skeleton heading order and exact section and subsection names.
- Use explicit IDs instead of pronouns such as "the above requirement".
- Write one trace target per nested list item.
- Use `[ID](location)` for every trace and initial-ticket link.
- Keep the normative statement separate from rationale.
- Keep acceptance criteria and verification details out of the requirement.
- Define project-specific abbreviations in the owning document.
- Do not make a diagram or external issue the only place where an obligation is
  stated.
