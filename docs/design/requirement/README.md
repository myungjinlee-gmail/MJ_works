# Software Requirements and Verification

This directory contains templates, rules, examples, and authored artifacts for
software requirements and their verification specifications.

## Software requirement(SWR) documents

- [Software requirement rule](software_requirement_rule.md) is the
  authoritative policy for SWR ownership, identifiers, lifecycle, wording, and
  traceability.
- [Software requirement skeleton](software_requirement_skeleton.md) is copied
  to create one SWR file.
- [Software requirement example](software_requirement_example.md) demonstrates
  one non-normative SWR for configurable software.

## Software requirement verification(SWRVS) documents

- [Software requirement verification spec rule](software_requirement_verification_spec_rule.md)
  is the authoritative policy for SWRVS ownership, acceptance criteria,
  verification measures, requirement satisfaction, and local traceability.
- [Software requirement verification spec skeleton](software_requirement_verification_spec_skeleton.md)
  is copied to create one SWRVS file.
- [Software requirement verification example](software_requirement_verification_example_rule.md)
  demonstrates one non-normative SWRVS linked to the SWR example.

## Review checklists

- [Software requirement PR review checklist](software_requirement_review_checklist_pr.md)
  evaluates an SWR during Pull Request review.
- [Software requirement verification spec PR review checklist](software_requirement_verification_spec_review_checklist_pr.md)
  evaluates an SWRVS during Pull Request review.
- [Software requirement release baseline quality checklist](software_requirement_review_checklist_quality.md)
  evaluates an SWR after the release baseline is established.
- [Software requirement verification spec release baseline quality checklist](software_requirement_verification_spec_review_checklist_quality.md)
  evaluates an SWRVS after the release baseline is established.

## Requirement development sequence

This personal project treats an SWR and the SWRVS artifacts needed to verify it
as one requirement-definition change.

- Add and accept a new SWR and all SWRVS artifacts needed to cover it in the
  same Pull Request. Include the bidirectional SWR-to-SWRVS trace, but do not add
  downstream design, software implementation, or verification implementation.
- When an accepted SWR changes semantically, update every affected Acceptance
  Criterion and Verification Measure in the same Pull Request. An SWRVS-only
  correction may omit the SWR when the software obligation does not change.
- Add downstream design and software implementation in a later Pull Request.
  Update the SWR and the design artifact's reverse trace in that Pull Request.
- Add test cases, analysis scripts, review checklists, static-analysis
  configuration, or other verification implementations in a later Pull
  Request. Update the affected SWRVS implementation links in that Pull Request.
- Keep trace-only updates required by the current stage in that stage's Pull
  Request. Do not change an accepted SWR, Acceptance Criterion, or Verification
  Measure merely to match implementation behavior.

## Usage

1. Read the authoritative SWR and SWRVS rules.
2. Create `docs/design/requirement/<SWR-ID>/` for an authored SWR.
3. Copy the SWR skeleton into that directory and create exactly one SWR file.
4. Copy the SWRVS skeleton into the same directory for every SWRVS needed to
   cover the SWR.
5. Complete the bidirectional SWR-to-SWRVS trace and review both artifacts in
   the same Pull Request.
6. Use the examples only as formatting references.

This README owns the requirement Pull Request sequence. The linked rules own
the content and lifecycle policy of each artifact.
