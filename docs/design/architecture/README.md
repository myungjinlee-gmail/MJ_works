# Architecture Design

This directory contains the skeleton, rule, example, and Architecture Decision
Records (ADRs) used to maintain one software architecture for the software.

## Architecture design documents

- [Architecture design rule](architecture_design_rule.md) is the authoritative
  policy for architecture scope, content, diagrams, component descriptions,
  execution views, and traceability.
- [Architecture design skeleton](architecture_design_skeleton.md) defines the
  required structure of the software architecture document.
- [Architecture design example](architecture_design_example.md) demonstrates
  the structure with a non-normative hardware-target design.

## Review checklists

- [Architecture design PR review checklist](architecture_design_review_checklist_pr.md)
  evaluates the architecture document and every applicable ADR during Pull
  Request review.
- [Architecture design release baseline quality checklist](architecture_design_review_checklist_quality.md)
  evaluates the architecture document and applicable ADRs against the exact
  release candidate after its baseline is established.

Pull Request review selects only the PR checklist. Release-baseline evaluation
selects the quality checklist, which first requires every applicable PR
checklist item to be satisfied.

The software's single current architecture document shall be authored and
maintained at `docs/design/architecture/software_architecture_design.md`. Do
not allocate a separate architecture document ID or create one architecture
document per component. Components are described as subsections of the single
architecture document and receive stable `swad-component-NN` IDs for
traceability.

## Related design artifacts

- An SWR defines a software obligation allocated to an architecture component.
- An SWCD defines the units, classes, functions, files, and other detailed
  design that realize one architecture component.
- A configuration specification defines configuration values and their effect
  on a component.
- An external interface specification owns detailed operations, data formats,
  protocols, errors, timing, compatibility, and implementation constraints.
- An ADR records why a significant architecture option was selected. The
  architecture document describes the current result and links an ADR from the
  relevant explanation when its rationale is needed.

The [`adr/`](adr/) directory defines the ADR workflow and template.

## Architecture development sequence

- Accept an SWR and its Software Requirement Verification Spec before adding
  architecture that realizes the obligation.
- Update the single architecture document in a later Pull Request. Add the SWR
  to the owning component's `Traceability` > `Upstream` list and add the reverse
  `swad-component-NN` link to the SWR in the same Pull Request.
- Add or update an ADR in the same Pull Request when the design selects between
  meaningful alternatives, establishes a project-wide rule, or would be costly
  to reverse.
- Add an SWCD or configuration specification later and link it from the owning
  component's `Downstream` or `Configuration` list in the same Pull Request.
- Define component and unit design after the architecture is accepted. Define
  software component and integration verification specifications and
  implementations in their later lifecycle stage after the component and unit
  boundaries needed by verification are available. Architecture authoring does
  not require those future artifacts.
- Keep only conceptual descriptions of data flow, threads, and pipelines in the
  architecture document. Move their detailed design to the dedicated component
  when that component is introduced.
- Keep only an abstract external-interface summary in the architecture
  document. Move details to the owning external interface specification.

Do not change an accepted requirement merely to match a preferred architecture
or an existing implementation. Correct the artifact that is wrong, and create
or change a requirement when the software obligation must change.

## Usage

1. Read the architecture design rule and the accepted SWRs and SWRVSs.
2. Copy the skeleton to
   `docs/design/architecture/software_architecture_design.md`. Do not assign an
   architecture document ID.
3. Define Scope, Design Purpose, Context, and every required Design subsection.
4. Maintain the component diagram as PlantUML source and a rendered SVG. Keep
   component-level sequence diagrams in Mermaid.
5. Allocate each component the next zero-padded `swad-component-NN` ID and
   preserve that ID for the component's lifetime.
6. Describe every component's responsibilities, abstract inputs and outputs,
   architecture-significant relationships, and local traceability.
7. Link detailed SWCD, configuration, and external-interface artifacts only
   when they exist.
8. Use the example only as a formatting reference.

This README owns the architecture development sequence. The linked rule owns
the content and lifecycle policy of the architecture document.
