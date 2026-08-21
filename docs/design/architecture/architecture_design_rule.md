# Architecture Design Authoring Rule

## Purpose

This rule defines how to write one software architecture that is readable by
people, consistently interpretable by language models, and traceable from
software requirements to component design and configuration.

## Artifact boundary

The architecture document owns:

- the scope and purpose of the software architecture;
- external dependencies and the software boundary;
- the component structure and architecture-significant interactions;
- component-level dynamic behavior;
- component responsibilities, abstract inputs and outputs, relationships, and
  traceability;
- an abstract view of external interfaces; and
- conceptual execution architecture.

The architecture document does not own:

- software requirements or acceptance criteria;
- abstract constituent-unit decomposition or detailed unit design;
- detailed data-flow, thread, or pipeline design;
- detailed external-interface specifications;
- the history and rationale of significant decisions;
- test procedures; or
- executed verification results and release evidence.

Requirements define what the software shall do. The architecture defines the
components and interactions that realize those obligations. Content below a
component boundary belongs to its owning downstream design artifacts.
Configuration and interface specifications own their respective detailed
contracts. ADRs record why significant choices were made.

## Single architecture document

Maintain one current architecture document for the software. Do not allocate a
separate architecture document ID and do not split the architecture into one
document per component. Use the software architecture title as the top-level
heading and describe components under `Design` > `Components`.

Preserve the skeleton heading order and exact section names. Repeat component
subsections as needed. Keep optional sections and write
`Not applicable: <reason>` when their subject does not apply.

The skeleton, rule, example, README, and files below `adr/` are control or
supporting documents and are not the software's accepted architecture.

## Acceptance through the Pull Request workflow

Do not store a status field in the architecture document:

- content on an unmerged working branch is a draft;
- content merged through the required Pull Request workflow is accepted; and
- rejected content is not merged.

Git history records revisions. Update the same architecture document when the
architecture changes. Do not create a second current document for a replacement
design. Update affected forward and reverse trace links in the same Pull
Request.

Create or supersede an ADR according to
[the ADR rule](/docs/design/architecture/adr/README.md) when the
change alters a significant accepted decision. The architecture document owns
the current result; the ADR chain preserves decision history.

## Scope

State the architecture boundary as one or more concise list items. Identify the
software, subsystem, capability, or cross-cutting concerns covered by the
document. Because one architecture document covers the software, use the Scope
section to make inclusions and meaningful exclusions explicit, not to create
independent architecture artifacts.

Do not use Scope as a task list, release plan, or applicability field.
Configuration applicability remains owned by SWRs and configuration
specifications.

## Design Purpose

Explain the problem addressed by the architecture and the intended
architecture-level outcome. Purpose is informative and shall not add behavior,
thresholds, compatibility promises, or other software obligations that are
absent from accepted SWRs.

Do not repeat requirement statements or decision history. Link the owning SWR
from the relevant component and link an ADR from the relevant explanation when
the choice rationale is needed.

## Context

List external dependencies, including external systems, libraries, services,
hardware, and build or runtime infrastructure outside the owned architecture.
For each dependency, state:

- why the software needs it;
- what information or control crosses the boundary; and
- the contract or specification that governs the relationship, when one
  exists.

Do not list internal components as external dependencies. Do not make a diagram
the only definition of an external boundary.

## Design

### Component Diagram

The component diagram defines the static component structure and
architecture-significant relationships.

- Author the component diagram in PlantUML.
- Store the PlantUML source and rendered SVG in the repository.
- Link the PlantUML source and embed the SVG in the architecture document.
- Update and commit the source and SVG together.
- Treat the PlantUML source as authoritative when the source and SVG differ.

The diagram should show components and direct architecture relationships. It
shall not show units, classes, functions, files, or generic utilities that do
not affect component boundaries. Define relationship details once in each
component's `Relationships` list; do not repeat them below the diagram.

### Dynamic Behavior

Dynamic Behavior describes ordering and architecture-level flow between
components. It does not allocate each component to one thread or imply that a
component is an execution unit.

#### Component-level Sequence

Use Mermaid sequence diagrams to show significant ordering between components.
A participant represents an architecture component. It does not necessarily
represent one thread, process, task, pipeline stage, or core.

Interactions shown in sequence may execute concurrently. Express meaningful
parallelism in the diagram or accompanying text, and describe execution
allocation separately under `Execution Architecture`.

Do not use the sequence diagram for source-level calls or complete test
procedures.

#### Data Flow

Keep this subsection in the architecture document. Briefly describe the
conceptual data movement between architecture components, including the
producer, consumer, and meaning of the exchanged information when relevant.

Do not place a detailed data-flow diagram, concrete type, transformation,
queue, buffer, or implementation design here. Keep those details in their
owning downstream design or implementation artifacts, and leave a brief
conceptual summary in this subsection.

#### Control Flow

Describe architecture-level triggers, decisions, and response propagation only
when a separate control-flow explanation materially clarifies the design.
Otherwise write `Not applicable: <reason>`.

Do not duplicate a component-level sequence diagram. Use this subsection to
explain branching, orchestration, cancellation, or error propagation that is
not sufficiently clear from the sequence.

#### State Machine

Describe component-level states, transition triggers, and state-dependent
behavior only when the architecture requires a state machine. Otherwise write
`Not applicable: <reason>`.

Keep details below architecture-level states and transitions in their owning
downstream design artifacts.

### Components

Create one `#### <Component name>` subsection for every architecture
component. A component name shall be unique within the architecture document.
Give every component a stable explicit ID anchor immediately before its
heading.

#### Component ID

Use `swad-component-NN`, where `NN` is a zero-padded two-digit sequence number
allocated monotonically within the architecture document. Start with
`swad-component-01` and use the next unused number for each new component.

Write the lowercase explicit anchor immediately before the component heading:

```markdown
<a id="swad-component-01"></a>

#### Hardware Service Boundary
```

The component ID is permanent. Do not reuse or renumber an accepted or removed
component ID. Preserve the ID when the component is renamed or its description
changes. When one component is replaced by a semantically different component,
allocate a new ID and update all current trace links in the same Pull Request.

Use the component ID as the link label for component relationships and external
traceability. A link to a component in the same architecture document has this
form:

```markdown
[swad-component-01](#swad-component-01)
```

Do not describe constituent units. In particular, do not list namespaces,
classes, functions, source files, libraries, executables, or build targets as
units owned by the architecture component. Content below the component boundary
belongs to its owning downstream design artifacts.

#### Responsibility

Write `Responsibility` as a list. Use one complete architecture-level
responsibility per list item and add as many items as needed. Each item shall:

- state what the component owns or guarantees;
- distinguish that ownership from adjacent components; and
- remain meaningful if its implementation units change.

Do not combine unrelated ownership merely to reduce the number of components.

#### Input and Output

Describe inputs and outputs abstractly as information, events, requests,
responses, or control. Use one item for each distinct input or output.

Do not specify concrete data types, parameters, function signatures, wire
formats, or implementation messages. The component's `Input` and `Output`
entries are the authoritative architecture-level boundary description.
Detailed contracts belong to their owning downstream design or interface
specification.

#### Relationships

Record only direct `Inherits from` and `Uses` relationships that are
architecture-significant:

- `Inherits from` identifies an architecture component whose defined role or
  contract is specialized by the current component.
- `Uses` identifies an architecture component required to fulfill the current
  component's responsibilities.

Use component IDs as link labels and link to their explicit anchors. Do not
duplicate transitive relationships.

Exclude a globally available component when all of these criteria are met:

- it provides cross-cutting infrastructure uniformly to unrelated components;
- using it does not change the current component's architecture responsibility
  or boundary; and
- omitting it does not hide required data flow, control flow, ownership,
  lifetime, substitutability, failure propagation, or requirement allocation.

Logging, diagnostics, metrics, and generic utilities commonly meet the
exclusion criteria. Include a global component whenever any criterion is not
met. Explain an unusual inclusion or exclusion in the component description.

#### Traceability

Keep traceability local to each component:

- `Upstream` links every SWR allocated wholly or partly to the component. Every
  accepted architecture component shall link at least one accepted SWR.
- `Downstream` links directly to the owning SWCD document.
- `Configuration` links configuration specifications that select, include,
  exclude, or change the component.

Use `[ID](/PATH/TO/TARGET)` and one target per nested list item when a target
has a stable ID. Use a project-root absolute path when the target is outside
the current document's directory. A target in the same directory may use a
relative filename, and a target in the same document may use its local anchor.
The linked SWR shall provide the reverse downstream link using the component ID
and explicit anchor. An SWCD has no separate design ID: link the SWCD file
directly from the architecture `Downstream` relationship. Its link label is
descriptive and need not match the SWCD title. The SWCD shall provide the
reverse `Upstream` link using the owning `swad-component-NN` ID and explicit
anchor. Add or update both links in the same Pull Request. A linked
configuration specification shall provide its applicable reverse link.

Keep all three relationship labels. When no concrete target exists, leave the
label without a nested item. Do not write `None`, `TBD`, a placeholder, or a
planned location in an accepted architecture document.

### Interfaces

Keep this section and provide only a brief conceptual summary of each external
interface and its architecture boundary. Link every external interface
specification that already exists.

Keep detailed operations, data definitions, protocols, error behavior, timing,
compatibility, and implementation constraints in their owning downstream
design or external interface specification. Do not duplicate those details in
the architecture document.

When the software has no external interface, retain the section and write
`Not applicable: <reason>`.

### Execution Architecture

Execution Architecture explains the conceptual relationship between components
and execution resources. It does not make a component equivalent to one thread,
process, pipeline stage, or processor core.

#### Threads

Keep this subsection. Describe conceptual execution contexts, concurrency
needs, and their relationship to components. Keep detailed thread ownership,
scheduling, synchronization, lifecycle, priority, and implementation in their
owning downstream design or implementation artifacts. Retain only the
conceptual architecture summary and applicable downstream links.

#### Pipelines

Keep this subsection. Describe conceptual processing stages, stage ordering,
and concurrency. Keep detailed collaboration, buffering, backpressure,
scheduling, and implementation in their owning downstream design or
implementation artifacts. Retain only the conceptual architecture summary and
applicable downstream links.

#### Timing Constraints

Describe architecture-level timing constraints only when an accepted SWR
defines them. Identify the affected components and interaction. Otherwise write
`Not applicable: <reason>`.

Do not introduce a new deadline, period, timeout, tolerance, or performance
obligation in the architecture document.

#### Shared Resources

Describe shared resources when they affect component ownership, lifetime,
access rules, synchronization, or failure containment. Otherwise write
`Not applicable: <reason>`.

Keep detailed ownership, synchronization, source-level locks, containers,
handles, and allocation algorithms in their owning downstream design or
implementation artifacts.

#### Hardware/Core Mapping

Describe allocation to hardware devices or processor cores when the mapping is
architecture-significant. Link the SWR or configuration specification that
governs the mapping. Otherwise write `Not applicable: <reason>`.

Do not infer that one component occupies one core or execution unit merely
because it appears as one component or sequence participant.

## Architecture Decision Records

Create an ADR when a choice meets the criteria in
[the ADR rule](/docs/design/architecture/adr/README.md#when-to-write-an-adr).
State the current design in
the applicable architecture section and link the accepted ADR from that
explanation. The ADR owns context, alternatives, decision rationale, and
consequences.

Do not add an ADR-specific section to the architecture skeleton and do not turn
the architecture document into a decision log.

## Human and language-model readability

- Preserve the skeleton heading order and exact field labels.
- Keep normative obligations in SWRs and detailed design in owning
  specifications.
- Use component names consistently and component IDs for relationships and
  trace links.
- Keep one responsibility, input, output, relationship, or trace target per
  list item.
- Keep component relationship details in each component's `Relationships`
  list instead of repeating them below the component diagram.
- State abstract data and control semantics without implementation types.
- Write `Not applicable: <reason>` for an inapplicable optional section.
- Do not leave `TBD` or unresolved placeholders in an accepted architecture.
