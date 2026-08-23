# Software Component Design — PR Review Checklist

Apply this checklist to every Software Component Design (SWCD) added or
changed in a Pull Request and to related artifacts that must be updated with
that change. Do not require a unit design, implementation, verification
specification, verification implementation, or verification result before the
lifecycle rule that owns the artifact makes it applicable.

## Document and lifecycle

- [ ] The changed artifact is the only SWCD for its accepted owning
      architecture component; its location, filename, and title follow the
      component design rule, and it stores neither a separate design ID nor an
      approval status.

- [ ] The SWCD preserves the skeleton heading order and field labels, omits
      only an optional section or field whose omission condition is satisfied,
      and contains no authoring instruction, unresolved placeholder, or
      example-only content.

- [ ] `Scope` identifies the target, design level, meaningful inclusions, and
      applicable exclusions without repeating the owning architecture
      component description, and `Design Method` contains only methods or rules
      that apply to the component as a whole.

- [ ] `Traceability` links exactly one owning `swad-component-NN`, and when the
      relationship is added or changed, the architecture component provides a
      reciprocal `Downstream` link directly to the SWCD file in the same Pull
      Request. The link does not require the SWCD title or a separate design ID
      as a trace identifier.

## Component and unit design

- [ ] The component diagram's PlantUML source and rendered SVG are committed
      together, both links resolve, both representations agree, and they show
      the same constituent units and direct internal interactions as the SWCD
      text.

- [ ] Every constituent unit has one unique, stable, lowercase
      `swcd-unit-NN` anchor; accepted or removed anchors are not renumbered or
      reused, and every unit in the diagram has exactly one matching unit
      entry.

- [ ] Each unit states a distinct implementation-neutral responsibility and
      semantic inputs and outputs that remain valid if its detailed design or
      implementation changes; together they completely explain the provided
      or required interface responsibilities applicable to the component
      without defining detailed interface contracts.

- [ ] Each `Uses` entry records only a direct relationship to another unit in
      the same component, uses its stable unit ID as the link label, and does
      not duplicate a transitive, cross-component, or architecture-significant
      relationship.

- [ ] When an internal `Uses` relationship exists, `Unit-level Sequence` shows
      significant ordering between the connected units; otherwise the
      subsection is omitted. Error propagation or component-wide concurrency
      constraints are described when they affect collaboration, without
      defining detailed handling or synchronization.

- [ ] `Configuration Effects` accurately describes relevant effects on the
      component or unit composition and collaboration without duplicating
      authoritative architecture relationships or detailed configuration
      contracts.

## Boundaries, traceability, and consistency

- [ ] When an accepted unit design applicable to a unit exists, the unit's
      `Downstream` links that design, and when the relationship is added or
      changed, the unit design links back to the unit in the same Pull Request.
      When the artifact does not exist or is not applicable, `Downstream`
      remains empty without a prospective link.

- [ ] Scope, methods, diagram, sequence, unit descriptions, relationships,
      configuration effects, and trace links use consistent component and unit
      names, IDs, boundaries, and behavior and agree with the owning
      architecture component.

- [ ] The SWCD contains no detailed unit behavior, algorithm, state, error
      handling, synchronization, concrete contract, namespace, class,
      function, source file, library, executable, build target, concrete data
      type, or function signature owned by a later artifact.
