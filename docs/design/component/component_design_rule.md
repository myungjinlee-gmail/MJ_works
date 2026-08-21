# Software Component Design Authoring Rule

## Purpose

This rule defines how to author a Software Component Design (SWCD) that
connects one architecture component to its constituent units without making
unit-design or implementation decisions.

## Artifact boundary

Architecture design owns component boundaries, architecture-significant
component relationships, and allocation of software requirements to
components. An SWCD owns the implementation-neutral decomposition of one
architecture component into abstract constituent units. It defines:

- the document target, design level, included design perspectives, and
  applicable exclusions;
- component-wide design methods and rules;
- abstract unit responsibilities, semantic inputs and outputs, and direct unit
  usage relationships within the component;
- component-level collaboration, error propagation, concurrency constraints,
  and configuration effects; and
- traceability to the owning architecture component and later unit designs.

A unit's Software Detailed Design (SWDD) is the unit-design artifact governed
by issue #31. It owns detailed unit behavior, algorithms, states, error
handling, synchronization, and concrete contracts. Implementation owns
namespaces, classes, functions, source files, libraries, executables, build
targets, concrete data types, and function signatures. An SWCD may name these
categories only to assign their ownership; it shall not prescribe a decision
in any of them.

Keep architecture-significant component relationships authoritative in the
architecture document. Do not repeat them as unit dependencies. Record only
direct collaboration between constituent units needed to explain how the
component fulfills its responsibility.

## Artifact identity and location

Do not maintain more than one SWCD for an owning `swad-component-NN`
architecture component. An accepted architecture component may have no SWCD
before its component-design stage begins; the release-baseline requirement is
defined under Acceptance and lifecycle. Store an authored SWCD alongside the
component source files at
`src/<component-name>/<component-name>.md`. The Markdown filename stem shall
exactly match the containing component directory name.

Use `# <Component name> Component Design` as the document title. Do not assign
an SWCD document a separate design ID or explicit document anchor. The owning
architecture component links its `Downstream` relationship directly to the
SWCD file. That link's label is descriptive and is not a traceability identity;
it need not match the SWCD title. The SWCD uses the owning `swad-component-NN`
ID as the label for its `Upstream` link.

The skeleton, this rule, and the example under `docs/design/component/` are
control documents. They are not accepted SWCDs and do not satisfy the
one-document-per-component requirement.

## Acceptance and lifecycle

Do not store an approval status in an SWCD:

- content on an unmerged working branch is a draft;
- content merged through the required Pull Request workflow is accepted; and
- rejected content is not merged.

Preserve the same SWCD document as its component design evolves. When the
owning architecture component is renamed, keep its stable
`swad-component-NN` identity and update affected links and titles in the same
Pull Request.

Before a release baseline is approved, every architecture component included
in the selected project and configuration shall have exactly one current SWCD
in the candidate commit. The candidate shall also contain the SWCD's PlantUML
source and rendered SVG. The SWCD, included implementation, and build
configuration shall not contradict one another.

A later unit design or software component or integration verification artifact
is required at release only after its owning lifecycle rule is defined and
makes that artifact applicable. Until an accepted unit design applicable to the
constituent unit exists, keep its `Downstream` relationship empty. Do not add
`None`, `TBD`, a placeholder, a prospective link, or a completeness claim for
an artifact that is not yet applicable.

## Scope

Use Scope to define what this document covers, not to repeat the owning
architecture component description. Preserve these fields as applicable:

- `Target` identifies the design target covered by the SWCD.
- `Design level` states the level of detail provided by the SWCD.
- `Included scope` lists the primary design perspectives owned by the SWCD.
- `Excluded scope` lists meaningful design perspectives outside the SWCD when
  exclusions exist. Omit this field when there is no meaningful exclusion.

Do not repeat the owning architecture component's responsibilities, semantic
inputs and outputs, or architecture-significant relationships. Keep those
authoritative in the architecture document linked by `Upstream`.

## Document-level traceability

Keep a document-level `Traceability` section immediately after `Scope`. Under
`Upstream`, link exactly one owning architecture component using:

```markdown
- Upstream:
    - [swad-component-NN](/PATH/TO/ARCHITECTURE-DOCUMENT.md#swad-component-NN)
```

The owning architecture component's `Downstream` relationship links directly
to the SWCD file. Its link label is descriptive and need not match the document
title. Do not introduce a separate SWCD ID. Add or update both the SWCD
`Upstream` link and the reciprocal architecture `Downstream` link in the same
Pull Request.

Use `[ID](/PATH/TO/TARGET)` whenever the target has a stable ID. Use a
project-root absolute path when the target is outside the current document's
directory. A target in the same directory may use a relative filename, and a
target in the same document may use its local anchor. Every such link shall
resolve to an existing explicit anchor, and every bidirectional relationship
shall contain its applicable reverse link.

## Design Method

List the design methods and rules that apply throughout the component. Use one
method or rule per list item. Include only guidance that governs the component
as a whole; keep unit-specific decisions in the owning unit's Software Detailed
Design (SWDD).

## Design

### Component Diagram

Author one `.pu` PlantUML source file showing the constituent units and their
direct interactions inside the owning component. Commit its rendered SVG with
the source. Link the PlantUML source and embed the SVG in the SWCD using the
skeleton fields. Update and commit both files together, and treat the PlantUML
source as authoritative when they differ. Do not repeat the architecture
component diagram or introduce relationships owned by the architecture
document.

The non-normative control example may omit both diagram assets when its
`Component Diagram` section explicitly states that they are omitted. This
exception does not apply to an authored SWCD.

### Dynamic Behavior

`Unit-level Sequence` is optional when there is no connection between
constituent units in the component. Omit it when no internal `Uses`
relationship exists. When an internal `Uses` relationship exists, include a
fenced Mermaid sequence diagram showing the significant ordering across the
connected units. Participants represent abstract units, not execution
resources. Describe component-level error propagation and concurrency
constraints when they affect collaboration, while leaving detailed handling
and synchronization to the owning SWDD.

### Units

Create one unit entry for every constituent unit. Describe its responsibility,
semantic input, semantic output, direct internal `Uses` relationships, and
local traceability.

When a unit owns collaboration at the component boundary, state its provided
or required interface responsibility abstractly under `Responsibility`. A
provided interface responsibility explains what the unit accepts or makes
available on behalf of the component. A required interface responsibility
explains what capability the unit needs beyond the component boundary. Do not
repeat the architecture-level input and output definitions, add a
cross-component unit relationship, or define a detailed interface contract.

Assign each unit one stable, lowercase `swcd-unit-NN` explicit anchor. Allocate
numbers monotonically within the SWCD, starting at `swcd-unit-01`. Preserve an
accepted anchor when its unit is renamed or refined. Never reuse or renumber an
accepted or removed anchor. Use unit IDs as link labels for relationships
between units in the same SWCD.

Record only direct `Uses` relationships to units owned by the same component.
Do not record inheritance, transitive dependencies, architecture-significant
component relationships, or relationships to units owned by another component.
Define cross-component unit usage in the Software Detailed Design (SWDD). A
unit description shall remain valid if its later detailed design or
implementation changes.

#### Unit-design traceability

Give every unit a `Traceability` subsection with a `Downstream` relationship.
Keep `Downstream` empty until an accepted unit-design artifact governed by
issue #31 exists and applies to the unit. Do not write `None`, `TBD`, a
placeholder, or a prospective link for a missing or inapplicable artifact.

Store a unit-design document alongside its unit source files at
`src/<component-name>/<unit-name>/<unit-name>.md`. Its Markdown filename stem
shall exactly match the containing unit directory name.

When an accepted unit-design document exists and applies to the unit, link it
from the SWCD as
`[<unit-design-ID>](/src/<component-name>/<unit-name>/<unit-name>.md)`. Add the
reverse `[swcd-unit-NN](/src/<component-name>/<component-name>.md#swcd-unit-NN)`
link to the unit-design document in the same Pull Request.

### Configuration Effects

Describe how configuration affects the component and its abstract unit
composition. Include effects on unit selection, collaboration, responsibility,
error propagation, or concurrency only when needed to explain the component.
Do not duplicate authoritative architecture relationships or detailed
configuration contracts.

## Human and language-model readability

- Preserve the skeleton heading order and exact field labels.
- Use one responsibility, input, output, relationship, or trace target per list
  item.
- Use component and unit names consistently and stable IDs for links to
  explicit anchors.
- Keep normative statements objective and implementation-neutral.
- Keep a missing later unit-design relationship empty without placeholder
  text.
- Remove instructional comments and replace every applicable skeleton
  placeholder before an SWCD is accepted.
