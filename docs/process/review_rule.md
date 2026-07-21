# Review Rule

## Approval model

This repository is a personal project. The author performs the review, and a
passing self-review is the required approval. A GitHub `APPROVED` review from a
second person is not required.

The approval shall be recorded as a Pull Request conversation comment using
the [review comment template](../template/review/review_comment_template.md).
The checklist shall not be completed in the Pull Request description.

## Workflow

1. Open a Pull Request linked to the issue and keep it unmerged while changes
   are in progress.
2. Complete the implementation, documentation, and applicable verification.
3. Immediately before merge, review the current Pull Request head commit using
   the [review checklist](review_checklist.md).
4. Post the completed review comment with the reviewed head SHA, evidence,
   findings, and one decision.
5. Merge only when the decision is `MERGE` or `MERGE WITH FOLLOW-UP`.

Any commit added after the review comment invalidates its decision. The current
head shall be reviewed again and a new comment shall be posted.

## Decision criteria

- `MERGE`: every required checklist item is `PASS` or justified `N/A`, the
  `Release` and `Coverage` checks pass, and no blocking finding remains.
- `DO NOT MERGE`: a required item fails, required evidence is missing, a
  required check fails, or a blocking finding remains.
- `MERGE WITH FOLLOW-UP`: the current issue acceptance criteria pass and only
  non-blocking findings remain. Every deferred finding shall link a separate
  GitHub Issue before merge.

## Findings

Each finding shall have an identifier, be marked `BLOCKING` or `NON-BLOCKING`,
and record its resolution or follow-up issue. A finding is non-blocking only
when it does not violate the current issue acceptance criteria, introduce a
correctness or safety risk, or leave required verification incomplete.

## Completion states

- **Review complete**: a valid review comment exists for the current head.
- **Merge ready**: review is complete with `MERGE` or `MERGE WITH FOLLOW-UP`,
  required checks pass, and required follow-up issues exist.
- **Complete**: the Pull Request is merged and its issue is closed.

Release policy and architecture decision record policy are outside this rule.
