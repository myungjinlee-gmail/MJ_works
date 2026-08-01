# Software Requirement Verification Spec (SWRVS) Authoring Rule

## Purpose

This rule defines how to write a Software Requirement Verification Spec
(SWRVS) that contains acceptance criteria, verification measures, and the rule
for determining whether one linked software requirement is satisfied.

## Artifact boundary

One SWRVS owns:

- one stable SWRVS ID;
- one link to the software requirement it verifies;
- acceptance criteria derived from that requirement;
- one or more verification measures that cover those acceptance criteria; and
- the rule for determining requirement satisfaction.

An SWRVS does not own software requirements, architecture decisions,
implementation design, test source code, or executed verification results.

## File and identifier rules

- Store each authored SWRVS in the
  `docs/design/requirement/<SWR-ID>/` directory of the SWR linked by `Covers`.
- Store only SWRVS artifacts that cover that directory's SWR in the directory.
- Name an authored file `SWRVS-<DOMAIN>-<NNN>-<kebab-case-title>.md`.
- Use `SWRVS-<DOMAIN>-<NNN>` as its canonical ID.
- Make the title heading ID, `ID` section value, and filename ID agree.
- Allocate SWRVS IDs monotonically within a domain.
- Do not reuse or renumber an accepted or removed SWRVS ID.
- Use `AC-<NN>` for acceptance criterion IDs local to one SWRVS.
- Use `VM-<NN>` for verification measure IDs local to one SWRVS.
- Place an explicit lowercase anchor immediately before every AC and VM heading.
- Allocate AC and VM IDs monotonically within the SWRVS. Do not reuse or
  renumber an accepted or removed local ID.
- Preserve the skeleton heading order and exact field labels.

The README, rules, skeletons, examples, and review checklists in
`docs/design/requirement/` are control documents and are exceptions to the
authored SWRVS directory and filename rules.

## ID

Write the canonical SWRVS ID as the standalone value in the `ID` section.

Place one `Covers` list immediately below the ID. Link exactly one software
requirement using `[ID](location)`:

```markdown
## ID

`SWRVS-CFG-001`

- Covers:
    - [SWR-CFG-001](software_requirement_example.md)
```

The linked requirement shall provide the reverse SWRVS link in its
`Traceability` > `Verification` list.

The linked requirement owns configuration applicability. An SWRVS inherits
that applicability and shall not restate or redefine it. Verification measures
identify the concrete coverage needed to verify the requirement.

## Acceptance Criteria

Acceptance criteria define the observable conditions under which the linked
requirement is satisfied.

Write each criterion under a stable `### AC-<NN>` heading. Place the lowercase
AC ID in an explicit anchor immediately before the heading:

```markdown
<a id="ac-01"></a>

### AC-01
```

Each criterion shall:

- be derived only from the linked requirement;
- express an observable pass/fail condition;
- use conditions, values, units, tolerances, and time limits already defined by
  the requirement;
- avoid implementation tasks or design choices; and
- contain no new software obligation.

Create or correct the requirement when an acceptance criterion would expand
required behavior, quality, applicability, or a quantitative limit.

One acceptance criterion may be covered by multiple verification measures. One
verification measure may cover multiple acceptance criteria. Every acceptance
criterion shall be covered by at least one mandatory verification measure.

## Verification Measures

A verification measure (VM) defines one independently evaluated body of
verification work. Write each measure under a stable
`### VM-<NN>: <Verification measure title>` heading.

Place the lowercase VM ID in an explicit anchor immediately before the heading:

```markdown
<a id="vm-01"></a>

### VM-01: Canonical hardware-target build selection
```

Each VM owns:

- method, scope, environment, and preconditions;
- inputs;
- procedure or analysis steps;
- expected results;
- one pass/fail rule; and
- local traceability to acceptance criteria and verification implementation.

Every VM in an accepted SWRVS is mandatory whenever its declared scope applies.
Add only measures required to establish satisfaction of the linked requirement.

### Summary fields

#### Method

Use the primary method that determines the VM result:

- `Dynamic test` executes software and compares observations with expected
  results.
- `Analysis` evaluates calculations, models, reports, or accumulated evidence.
- `Review` evaluates a defined artifact against review criteria.
- `Static analysis` evaluates software artifacts with an analysis tool without
  executing the target software behavior.

Use another method only when it is defined by an authoritative project rule.

#### Scope

Identify what the VM includes and excludes. Scope describes the boundary of the
verification work; it shall not narrow or redefine the linked requirement's
behavior or applicability.

#### Environment

Identify hardware, operating system, toolchain, external service, resource,
timing, or data constraints needed to reproduce the VM. Link a separately
controlled environment specification when one exists.

#### Preconditions

Identify the state, configuration, data, dependencies, and setup that must be
true before the VM begins. Do not hide a verification action in a precondition.

### Inputs

Use a separate `#### Inputs` heading for each VM. Write one input, parameter, or
analyzed artifact per list item. Use concrete values, sets, ranges, boundaries,
invalid values, or data properties required by the covered acceptance criteria.

### Procedure or Analysis Steps

Write ordered, reproducible actions or analysis steps. Each step shall have one
primary action and enough detail for another person or tool to repeat it.
Implementation-specific commands may be linked rather than duplicated.

### Expected Results

Write observable or measurable expected results that are concrete enough to
distinguish pass from fail. Keep one expected result per list item and make its
relationship to the procedure or analysis steps unambiguous.

### Pass/Fail Rule

Define one unambiguous VM decision:

- `Pass` requires every mandatory expected result to be satisfied.
- `Fail` results when any mandatory expected result is not satisfied or required
  evidence cannot be produced.

Do not treat a skipped mandatory action or missing result as passing.

### Traceability

Acceptance of an SWRVS approves its Acceptance Criteria and Verification
Measures; it does not mean that their verification implementations are
complete. Keep traceability local to each VM:

- `Covers` links every acceptance criterion evaluated by the VM using its stable
  local anchor. Because these criteria are owned by the same SWRVS, complete
  these links before accepting the SWRVS.
- `Verification implementation` links test cases, analysis scripts, review
  checklists, or other verification implementations that already exist. It may
  have no targets while those implementation artifacts do not yet exist.

Use `[ID](location)` and one target per nested list item. Do not duplicate VM
trace links in a global SWRVS traceability section.

Keep the `Verification implementation` label when it has no target. Do not use
`None`, `TBD`, a placeholder, or a link to a planned location in an accepted
SWRVS. Add concrete implementation links incrementally as test cases, analysis
scripts, review checklists, or other implementations are added.

A VM is ready for verification when the implementations needed to reproduce
its procedure or analysis exist. Before treating a VM as ready or performing
its verification, link each of those implementations. Before evaluating an
SWRVS against a release baseline, every VM shall link its actual verification
implementation.

## Requirement Satisfaction Rule

This section defines how the linked requirement receives its final satisfaction
judgment. It defines the rule only; the actual judgment belongs to a recorded
verification result or release evidence artifact.

The rule shall require:

- every acceptance criterion to be covered by at least one mandatory VM;
- every mandatory VM to be executed;
- every mandatory VM to pass; and
- no unresolved blocking anomaly to invalidate the verification result.

## Human and language-model readability

- Preserve the skeleton heading order and exact field labels.
- Keep one fact, input, action, expected result, or trace target per item.
- Use canonical IDs instead of descriptive link labels.
- Keep requirement statements out of the SWRVS.
- Keep acceptance conditions separate from VM procedure and expected results.
- Keep each VM's traceability inside that VM.
- Use explicit values instead of "appropriate", "normal", or "as needed".
