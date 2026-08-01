# Software Requirement Verification Spec — PR Review Checklist

## Identification and requirement linkage

- [ ] The filename, the SWRVS ID in the document title, and the `ID` value are
      identical.

- [ ] The parent directory name is the SWR ID linked by `Covers`.

- [ ] `Covers` links exactly one SWR verified by this SWRVS.

## Acceptance Criteria

- [ ] Every Acceptance Criterion is derived only from the conditions and
      obligations in the linked SWR.

- [ ] Each Acceptance Criterion is expressed as an observable pass/fail
      condition.

- [ ] No Acceptance Criterion introduces behavior, applicability,
      configuration, threshold, tolerance, or time limit absent from the SWR.

- [ ] The Acceptance Criteria completely represent the SWR's mandatory
      conditions and outcomes.

- [ ] Each Acceptance Criterion has a stable AC ID and a matching anchor.

## Verification Measures

- [ ] Every Acceptance Criterion is linked to at least one Verification
      Measure.

- [ ] Each Verification Measure uses a method appropriate for its verification
      target: `Dynamic test`, `Analysis`, `Review`, or `Static analysis`.

- [ ] Each Verification Measure's `Scope`, `Environment`, and `Preconditions`
      make the verification target and execution conditions understandable.

- [ ] `Inputs` defines the values, ranges, boundary values, or analyzed
      artifacts needed for verification.

- [ ] `Procedure or Analysis Steps` is detailed enough for another person or
      tool to repeat.

- [ ] `Expected Results` is defined in observable or measurable terms.

- [ ] `Pass/Fail Rule` objectively determines whether every mandatory expected
      result is satisfied.

- [ ] Each VM's `Covers` links exactly the ACs that the VM evaluates.

## Requirement satisfaction

- [ ] `Requirement Satisfaction Rule` requires complete AC coverage, execution
      and passage of every mandatory VM, and the absence of a blocking anomaly.
