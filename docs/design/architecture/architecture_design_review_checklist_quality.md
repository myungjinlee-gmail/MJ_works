# Architecture Design — Release Baseline Quality Checklist

Evaluate this checklist against the exact release candidate commit. Component
and unit design and software component and integration verification lifecycles
are not yet defined, so this checklist does not require those future artifacts
or their verification results. Extend this checklist when those lifecycle
rules and templates are introduced. The release rule remains the authority for
the final release decision and full-test evidence.

- [ ] Every applicable item in the
      [PR Review Checklist](architecture_design_review_checklist_pr.md) is
      satisfied for the architecture and every applicable ADR in the release
      baseline.

- [ ] The candidate contains exactly one current architecture document, and
      the candidate commit or release tag identifies its exact revision and all
      linked diagram sources and rendered assets.

- [ ] The architecture scope and applicable configuration agree with the
      project, platform, dependencies, and software contents selected for the
      release.

- [ ] Every architecture-significant component, interface, dependency,
      configuration, dynamic behavior, and execution change in the release is
      reflected in the architecture.

- [ ] The component diagram, component descriptions, dynamic behavior,
      interfaces, and execution architecture are mutually consistent and do
      not contradict the release implementation or build configuration.

- [ ] Every applicable accepted SWR is allocated to the component or components
      that realize it, and every architecture-to-SWR relationship and reverse
      relationship resolves within the release baseline or to an immutable
      external target.

- [ ] Every concrete link to an existing SWCD, configuration specification, or
      external-interface specification resolves within the release baseline
      and is consistent in both directions.

- [ ] When no applicable SWCD, configuration specification, or
      external-interface specification exists at the current lifecycle stage,
      the corresponding relationship remains empty without `None`, `TBD`, a
      placeholder, a prospective link, or a false completeness claim. The
      absence of a future artifact is not a defect.

- [ ] No unresolved inconsistency or blocking anomaly remains between the
      release architecture, requirements, existing downstream artifacts,
      implementation, build configuration, and release documentation.

## Architecture Decision Records

- [ ] Every ADR governing the release scope is present in the baseline,
      applicable to the selected configuration, accepted through the required
      Pull Request workflow, and not linked to a replacement through
      `Superseded by`.

- [ ] No ADR with a `Superseded by` link is used as the governing decision, and
      every supersession chain has valid reciprocal links and resolves to one
      current ADR.

- [ ] Each governing ADR's decision and boundaries are consistently applied in
      the architecture, existing downstream artifacts, implementation, and
      build configuration.

- [ ] No current ADR conflicts with another current ADR, an accepted SWR, the
      architecture, or the selected release configuration.

- [ ] The completed checklist and its evidence are linked from the release
      record as the detailed evidence for the release rule's `TRACE` readiness
      criterion.
