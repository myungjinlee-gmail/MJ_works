# Component Design

This directory contains the skeleton, rule, and example used to author Software
Component Design (SWCD) documents.

## Component design documents

- [Component design rule](component_design_rule.md) is the authoritative policy
  for SWCD ownership, location, lifecycle, content, unit anchors, and
  traceability.
- [Component design skeleton](component_design_skeleton.md) defines the required
  structure of an SWCD.
- [Component design example](component_design_example.md) demonstrates the
  structure with a non-normative Hardware Service Boundary design.

## Review checklists

- [Component design PR review checklist](component_design_review_checklist_pr.md)
  evaluates every SWCD added or changed during Pull Request review.
- [Component design release baseline quality checklist](component_design_review_checklist_quality.md)
  evaluates every applicable SWCD against the exact release candidate.

Pull Request review selects only the PR checklist. Release-baseline evaluation
selects the quality checklist, which first requires every applicable PR
checklist item to be satisfied. Implementation and build configuration included
in the candidate shall agree with the SWCD. Later unit-design, software
component verification, and integration verification artifacts are required
only when their owning lifecycle rules make them applicable to the evaluated
release stage. The quality checklist confirms their required trace and candidate
identity; their detailed review, execution, and pass or fail judgment remain in
their owning checklists and the release rule.

These files are control documents rather than accepted SWCDs. Store each
authored SWCD alongside its owning component at
`src/<component-name>/<component-name>.md`.

## Design ownership

- [Architecture design](/docs/design/architecture/README.md) owns component boundaries,
  architecture-significant relationships, and requirement allocation.
- An SWCD owns one component's implementation-neutral constituent-unit
  decomposition, internal unit collaboration, document scope, and
  component-wide design methods and constraints.
- A unit's Software Detailed Design (SWDD), governed by issue #31, owns detailed
  unit behavior and contracts. Implementation artifacts own concrete code
  structure and build decisions.
- Keep conceptual data flow, execution context, and external-interface
  boundaries in architecture design. Move internal unit collaboration, error
  propagation, and component-wide concurrency constraints to the SWCD. Keep
  cross-component unit usage and detailed unit or external-interface contracts
  in their owning SWDD or interface specification.

## Component development sequence

- Accept the owning architecture component before adding its SWCD.
- Copy the component design skeleton alongside the component source files and
  name the Markdown file after the component directory.
- Store each component diagram as `.pu` PlantUML source and a rendered SVG, and
  link both assets from the SWCD. The non-normative control example may instead
  state explicitly that both assets are omitted.
- Link the owning architecture component's `Downstream` directly to the SWCD
  file, and add the SWCD's reciprocal `swad-component-NN` `Upstream` link in the
  same Pull Request. The link label is descriptive rather than a traceability
  identity; do not require the SWCD title or assign a separate design ID.
- Allocate each abstract constituent unit a stable component-local
  `swcd-unit-NN` anchor and keep its unit-design `Downstream` relationship empty
  until an accepted and applicable unit-design artifact exists.
- When a unit design is added, update its forward and reverse trace links in the
  same Pull Request.
- Define software component and integration verification specifications and
  implementations only after the component and unit boundaries needed by
  verification are available.

## Usage

1. Read the component design rule and the owning architecture component.
2. Copy the skeleton to the owning component directory and remove instructional
   comments after replacing its placeholders.
3. Define the document target, design level, included and excluded scope,
   traceability, component-wide design methods and rules, diagrams, abstract
   units, internal `Uses` relationships, and configuration effects.
4. Omit `Unit-level Sequence` when the component has no internal unit
   connection or `Uses` relationship. Otherwise, use it to show significant
   ordering across the connected units.
5. Use the example only as a formatting reference.

This README owns the component-design workflow. The linked rule owns the
content and lifecycle policy of each SWCD.
