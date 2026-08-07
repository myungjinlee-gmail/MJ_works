# Software Requirement — Release Baseline Quality Checklist

- [ ] Every item in the
      [PR Review Checklist](software_requirement_review_checklist_pr.md) is
      satisfied.

- [ ] `Upstream` links the initial ticket and any applicable direct parent
      requirement or authoritative input.

- [ ] `Downstream` links the closest architecture or design artifact that
      realizes the requirement.

- [ ] `Verification` links at least one SWRVS that verifies the requirement.

- [ ] Each linked design artifact and SWRVS provides reverse traceability to the
      SWR.

- [ ] Every trace link targets a file in the release baseline or an immutable
      external target, and no link targets a broken or obsolete artifact.

- [ ] No `Pending`, `TBD`, placeholder, or authoring instruction remains.

- [ ] The requirement's `Applicability` is consistent with the release
      configuration and determines whether the requirement applies to this
      release.

- [ ] The requirement neither contradicts another requirement in the baseline
      nor duplicates the same obligation.
