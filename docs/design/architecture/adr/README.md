# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for decisions that
need to remain understandable after the related issue or Pull Request is closed.

## When to write an ADR

Write an ADR when a decision:

- affects multiple components or establishes a project-wide rule;
- changes a public interface, configuration, supported platform, or dependency;
- selects between meaningful architectural alternatives; or
- would be costly to reverse.

Keep local implementation details in the relevant design, issue, or Pull
Request. One ADR shall describe one decision.

## File naming

Copy [`adr_template.md`](adr_template.md) and name the new file:

```text
ADR-NNNN-kebab-case-title.md
```

Use the next unused four-digit number. Do not renumber an existing ADR.

## Simple status model

This is a personal project, so ADRs do not use a separate approval workflow or
a detailed status-transition process. The Pull Request is the proposal and
self-review stage.

Only two stored status forms are needed:

- `Accepted`: the decision is current.
- `Superseded by ADR-NNNN`: the named ADR replaces the decision.

A rejected proposal is not merged as an ADR. Its relevant alternatives and
trade-offs are summarized in the accepted ADR instead. When a decision changes,
create a new ADR and update the old ADR status with a link to the replacement.
Merge both changes in the same Pull Request.

## When to supersede an ADR

Do not delete an accepted ADR. Supersede it when:

- the decision stated in its `Decision` section is changed or withdrawn;
- a changed requirement or architecture constraint makes the decision invalid;
- another architectural approach replaces the selected option; or
- the component or capability governed by the decision is removed.

The replacement ADR shall explain why the old decision no longer applies. This
includes removal without a direct technical replacement: the new ADR records
the decision to remove the governed scope.

Do not supersede an ADR for wording, link, or formatting corrections, additional
evidence, or implementation details that remain within the accepted decision.

The new ADR shall set `Supersedes` to the old ADR. The old ADR shall set
`Status` to `Superseded by ADR-NNNN`. These reciprocal links preserve the
decision history without a separate lifecycle process.

## Workflow

1. Open or identify the issue that requires the decision.
2. Copy the template and record the context, alternatives, decision, and
   consequences.
3. Set the status to `Accepted` and open a Pull Request.
4. Perform the normal self-review defined by the Pull Request template.
5. Merge the ADR before or with the implementation that depends on it.

The repository owner is the decision maker and reviewer. Separate author,
approver, and decision-owner fields are therefore unnecessary.

Minor corrections may update the existing ADR through the normal Pull Request
workflow.
