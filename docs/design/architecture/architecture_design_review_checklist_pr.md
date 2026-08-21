# Architecture Design — PR Review Checklist

This checklist evaluates an architecture document and every ADR added or
changed with it. It does not require a downstream component or unit design,
software component or integration verification specification, verification
implementation, or verification result before the lifecycle stage that owns
that artifact has been defined and performed.

## Document scope and lifecycle

- [ ] The change maintains one current software architecture document and does
      not add an architecture document ID, stored approval status, or a separate
      architecture document per component.

- [ ] The architecture document preserves the skeleton heading order and exact
      section names, retains every optional section, and explains each
      inapplicable section with `Not applicable: <reason>`.

- [ ] No `TBD`, unresolved placeholder, authoring instruction, prospective
      link, or example-only content remains in an accepted architecture.

- [ ] `Scope` identifies the owned software boundary and meaningful inclusions
      and exclusions without becoming a task list, release plan, or
      configuration-applicability field.

- [ ] `Design Purpose` explains the architecture-level problem and outcome
      without introducing a software obligation, threshold, or compatibility
      promise absent from an accepted SWR.

- [ ] `Context` identifies every architecture-significant external dependency,
      why it is needed, what information or control crosses the boundary, and
      the governing contract when one exists.

- [ ] The architecture remains at component abstraction level and does not own
      units, classes, functions, algorithms, source files, concrete data types,
      detailed scheduling, test procedures, or executed verification results.

## Static architecture and components

- [ ] The component diagram has committed PlantUML source and rendered SVG;
      both are linked from the architecture document and are updated together.

- [ ] Every component in the diagram has exactly one matching component
      subsection, and the diagram shows the same direct
      architecture-significant relationships as the component descriptions.

- [ ] Every component has a unique `swad-component-NN` anchor, and an accepted
      or removed component ID is neither renumbered nor reused.

- [ ] Each component responsibility states distinct architecture-level
      ownership or guarantees that remain meaningful when implementation units
      change.

- [ ] Each component input and output is expressed abstractly as information,
      an event, a request, a response, or control, with one distinct item per
      list entry.

- [ ] Each `Inherits from` and `Uses` entry records only a direct,
      architecture-significant relationship and links the target by its stable
      component ID.

- [ ] An omitted global or cross-cutting component satisfies every exclusion
      criterion in the architecture rule, and every unusual inclusion or
      exclusion is explained.

## Dynamic behavior, interfaces, and execution

- [ ] Component-level sequences show architecture-significant ordering and
      meaningful concurrency without treating a component as one thread,
      process, task, pipeline stage, or processor core.

- [ ] `Data Flow` identifies the relevant producer, consumer, and meaning of
      exchanged information without concrete transformations, queues, buffers,
      or implementation design.

- [ ] `Control Flow` and `State Machine` describe architecture-level behavior
      when needed and otherwise contain a justified `Not applicable` statement.

- [ ] `Interfaces` summarizes each external interface and its architecture
      boundary, links every existing interface specification, or records a
      justified `Not applicable` statement.

- [ ] Each architecture-significant configuration choice describes its effect
      on component selection, inclusion, exclusion, relationship, or behavior
      and links an existing governing SWR or configuration specification.

- [ ] `Execution Architecture` describes applicable conceptual threads,
      pipelines, timing constraints, shared resources, and hardware or core
      mapping without introducing downstream ownership, scheduling,
      synchronization, or implementation details.

- [ ] Every architecture timing constraint comes from an accepted SWR and
      identifies the affected components and interaction.

## Traceability and consistency

- [ ] Every component links at least one accepted SWR; every affected accepted
      SWR is linked from each component to which it is wholly or partly
      allocated, and the SWR provides the reverse component link in the same
      Pull Request.

- [ ] When an applicable SWCD or configuration specification already exists,
      the component links it through `Downstream` or `Configuration`, and the
      target provides the reverse link. Both directions are updated in the same
      Pull Request when the association is added or changed.

- [ ] When no applicable SWCD or configuration specification exists at the
      current lifecycle stage, the corresponding relationship remains empty
      without `None`, `TBD`, a placeholder, or a prospective link. The absence
      of a future artifact is not a defect.

- [ ] Every concrete relationship resolves to an existing target and is
      consistent in both directions. A target with a stable ID uses canonical
      `[ID](location)` form; an SWCD relationship links its file directly and
      does not require a title or separate design ID as its label.

- [ ] Scope, context, component diagram, component descriptions, dynamic
      behavior, interfaces, execution architecture, configuration links, and
      requirement allocation use consistent component names, IDs, boundaries,
      and relationships.

## Architecture Decision Records

Evaluate every ADR added or changed in the Pull Request. Record a justified
`N/A` for this section when the change contains no ADR and does not introduce or
alter a decision that meets the ADR criteria.

- [ ] A change that selects between meaningful alternatives, establishes a
      project-wide rule, changes a public interface, configuration, platform,
      or dependency, or would be costly to reverse adds or supersedes an ADR in
      the same Pull Request.

- [ ] A new ADR's filename, title ID, and every ADR reference use the same next
      unused `ADR-NNNN` identifier. An existing ADR's filename, title ID, and
      every ADR reference preserve and consistently use its allocated
      identifier. Every ADR records exactly one decision.

- [ ] The ADR has a valid decision date, does not store an approval status, and
      uses `Supersedes` and `Superseded by` only for decision-history links.

- [ ] Every related requirement, architecture element, design, or supersession
      relationship uses a canonical `[ID](location)` link to an existing target
      and stable anchor.

- [ ] `Context` states the problem, constraints, and material trade-offs, and
      `Considered options` contains realistic alternatives with their relevant
      advantages and disadvantages.

- [ ] `Decision` states the selected option and its important boundaries, and
      `Consequences` records benefits, accepted costs or limitations, and
      remaining risks and mitigations.

- [ ] A superseded ADR and its replacement provide reciprocal links, the
      replacement explains why the prior decision no longer applies, and the
      old ADR is not deleted or rewritten as if the new decision had always
      applied.

- [ ] The architecture document states the current design and links the
      governing ADR without duplicating the ADR's decision history,
      alternatives, or detailed rationale.

- [ ] Every governing ADR link in the architecture document resolves to the
      current applicable ADR, and the documented architecture does not
      contradict that ADR's `Decision` or its stated boundaries.
