# Software Component Design — Release Baseline Quality Checklist

Evaluate this checklist against the exact release candidate commit and the
selected project and configuration. This checklist confirms release-baseline
completeness of the SWCDs and consistency among related artifacts. The owning
quality checklist for each verification artifact and the release rule remain
authoritative for the full-test decision and the final pass decision for each
verification result.

Evaluate unit-design and software component or integration verification
artifacts only when their owning lifecycle rules are defined and make those
artifacts applicable to the current release stage.

- [ ] Every SWCD in the release baseline satisfies every applicable item in the
      [PR Review Checklist](component_design_review_checklist_pr.md).

- [ ] The candidate commit contains every current SWCD under evaluation and
      its PlantUML source and rendered SVG.

- [ ] Each SWCD's scope, unit composition, internal collaboration, and
      configuration effects agree with the architecture, project contents, and
      configuration selected for the release.

- [ ] Every applicable SWR can be traced through its allocated architecture
      component to the SWCD that realizes that component, and all required
      forward and reverse links are consistent.

- [ ] When the unit-design lifecycle is applicable, every constituent unit
      links its current unit design, every unit design links back to the stable
      `swcd-unit-NN`, and the unit design refines the SWCD without contradiction.

- [ ] The implementation and build configuration included in the release do
      not contradict the SWCD's unit structure, responsibilities, interface
      responsibilities, collaboration, error propagation, concurrency, or
      configuration effects.

- [ ] When the software component or integration verification lifecycle is
      applicable, the trace relationships required by that lifecycle resolve
      through the authoritative verification specifications to results or
      evidence, and the evidence identifies the exact candidate commit and
      selected configuration.

- [ ] Every concrete trace link resolves to a target in the release baseline or
      to an immutable external target, and no unresolved inconsistency or
      blocking anomaly remains among applicable requirements, architecture,
      SWCDs, downstream designs, implementation, and verification artifacts.

- [ ] The completed checklist and supporting evidence are linked from the
      release record as detailed evidence for the release rule's `TRACE`
      readiness criterion.
