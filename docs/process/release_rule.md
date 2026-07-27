# Release Rule

> Draft for issue #20. Release automation is outside this document's scope.

## Purpose and scope

This document defines how independently versioned projects in this repository
become releases. Each independently published SDK, application, or customer
project has its own branch, version, tag, evidence, and artifacts.

All included changes shall follow [`git_workflow.md`](git_workflow.md) and the
review process in the default Pull Request description. A release does not
replace or weaken those requirements.

## Projects

A project identifier shall be unique, lowercase, and use hyphens when needed.
Examples are `reference` and `customer1`. A reference or example project follows
this release process only when it is independently published.

A release decision shall cover exactly one project. A commit may carry tags for
more than one project only when each project has a separate release decision
and project-scoped verification record.

## Release branches

Create one long-lived release branch for each supported major version of each
project:

```text
release/<project>/<major>.x
```

Examples:

```text
release/reference/1.x
release/reference/2.x
release/customer1/1.x
```

- Create a new major release branch from an identified commit on `main`.
- Develop all updates within an existing major version on the corresponding
  release branch.
- Create release work branches from the target release branch and name them
  `dev/<project>/<issue>-<description>`.
- Merge a release work branch into its release branch only through a Pull
  Request and only with Squash Merge.
- Protect `main` and every `release/**` branch. Prohibit direct pushes, force
  pushes, history rewrites, and deletion.
- Require linear history on `release/**` branches. Do not require linear history
  on `main`, because release branches enter `main` through merge commits.
- Do not merge `main` wholesale into an existing release branch. Apply each
  required change through a scoped, reviewed Pull Request targeting that
  release branch.

When a major version reaches end of support, retain its protected release
branch as read-only historical evidence. Do not delete or reuse it.

## Integration with main

Integrate every release branch change back into `main` through a Pull Request.
The release branch shall enter `main` with a merge commit; Squash Merge and
Rebase Merge are prohibited for this direction. This preserves every tagged
release commit with the same hash in the ancestry of `main`.

Normal working branches entering `main` should use Squash Merge. The release
branch exception is the only routine reason to create a merge commit on
`main`.

If a change affects other supported projects or major versions, create a
separate linked Pull Request for each affected branch. Do not merge one
project's branch wholesale into another project's branch. Record why an
affected supported branch does not receive the change.

## Versioning and tags

Each project shall use the version form `MAJOR.MINOR`. Version numbers are
independent between projects.

For the `reference` project:

- Increment `MAJOR` for an incompatible public interface, configuration, data
  format, or supported behavior change.
- Increment `MINOR` for every backward-compatible feature, correction, or
  re-release.

For a customer project:

- Increment `MAJOR` for each newly agreed regular delivery schedule or customer
  baseline.
- Start each new major version at `MAJOR.0`.
- Increment `MINOR` for corrections, additions, or re-deliveries within the
  same agreed delivery baseline.
- Do not reuse a major number when an agreed delivery is cancelled.

The release branch major and version major shall match. The project version
recorded in the source and artifacts shall match the release version.

Tag every published release using:

```text
<project>-v<major>.<minor>
```

Examples are `reference-v1.2`, `customer1-v2.0`, and `customer1-v2.1`. A
pre-release may append an identifier such as `-rc.1`.

Release tags shall be annotated and identify the exact approved commit on the
release branch. Do not move, reuse, or delete a published tag. A correction
shall use the next `MINOR` version on the same major branch.

## Release source and dependencies

The release branch tip after all release work Pull Requests are squash-merged
is the release candidate. The tag, source, artifacts, evidence, and release
notes shall identify that exact commit.

Every included change shall be traceable to a reviewed Pull Request and linked
issue. Unmerged, locally modified, or otherwise unreviewed content shall not be
included.

For a customer project or application, record the exact SDK or shared-component
baseline included in the build. Shared code changes shall follow the owning
project's release process before they are adopted by another project.

## Project-scoped full test

Every tagged release shall pass the full test scope for its project.
Every tag uses the same test requirement.

The test scope includes the project and the shared components included in its
delivered artifact. It excludes unrelated projects unless an interface or
compatibility impact requires their verification.

The full test scope shall include every applicable:

- clean Release build;
- static-analysis check;
- unit test;
- integration test;
- requirement or acceptance test;
- coverage build and report;
- supported configuration and platform check; and
- performance or regression test defined for the project.

All tests shall run against the exact candidate commit. A placeholder, skipped
required test, or result from a different commit is not passing evidence.

## Release contents and notes

Release notes shall contain:

- the project, version, release branch, and candidate commit;
- the branch point from `main`;
- the included SDK or shared-component baseline;
- a concise description and links to included issues or Pull Requests;
- added, changed, fixed, deprecated, and removed behavior, where applicable;
- compatibility or migration instructions;
- known limitations and linked follow-up issues; and
- links to the release decision and full-test evidence.

An intentional compatibility break or project-wide technical choice shall link
the accepted Architecture Decision Record that authorizes it.

## Readiness

The release owner shall complete this checklist for the exact candidate commit:

| ID | Readiness criterion | Required evidence |
| --- | --- | --- |
| SOURCE | The candidate is on the correct protected release branch, and all included changes were squash-merged through reviewed Pull Requests. | Project, branch, branch point, candidate commit, and Pull Request links |
| VERSION | The source version, branch major, and unused project tag agree. | Source version, proposed tag, and existing-tag check |
| FULL-TEST | Every required test in the project scope passes on the candidate. | Results with commit, configuration, platform, and pass/fail totals |
| DEPENDENCY | Included SDK and shared-component baselines are identified and verified. | Tags or commits and compatibility evidence |
| TRACE | Requirements, design, ADRs, source, tests, and documentation are consistent. | Linked artifacts and review evidence |
| COMPAT | Compatibility impact and required migration are documented. | Release-note section or `N/A` rationale |
| FINDINGS | No blocking finding remains; each accepted deferral has a linked follow-up issue. | Review summaries and follow-up links |
| MAIN | The candidate is preserved unchanged in `main` through a release-branch merge commit. | Merged release-to-main Pull Request and ancestry check |
| ARTIFACTS | Required artifacts were produced from the candidate. | Artifact names, checksums, and build record |

A criterion may be `N/A` only when it cannot apply to the project. Explain
every `N/A` in the release decision.

## Artifacts

The release record shall publish or link:

- project-scoped release notes and source archives;
- supported binaries or packages for the project;
- a SHA-256 checksum for every uploaded binary or package;
- build metadata identifying the project, version, candidate commit,
  configuration, compiler, platform, and tool versions;
- all project-scoped test and coverage results; and
- the completed release decision.

Name artifacts with the project and version. Generated artifacts shall not
be committed solely to publish a release.

## Approval

The repository owner is the release owner and sole release approver. Record the
completed checklist and exactly one decision in a release issue:

```markdown
### Release decision

Project: <project>
Candidate version: <project>-v<MAJOR.MINOR>
Release branch: <release/project/MAJOR.x>
Candidate commit: <full commit SHA>
Release-to-main PR: <Pull Request link>

| ID | Result | Evidence or N/A reason |
| --- | --- | --- |
| SOURCE | PASS / FAIL / N/A | |
| VERSION | PASS / FAIL / N/A | |
| FULL-TEST | PASS / FAIL / N/A | |
| DEPENDENCY | PASS / FAIL / N/A | |
| TRACE | PASS / FAIL / N/A | |
| COMPAT | PASS / FAIL / N/A | |
| FINDINGS | PASS / FAIL / N/A | |
| MAIN | PASS / FAIL / N/A | |
| ARTIFACTS | PASS / FAIL / N/A | |

- [ ] RELEASE
- [ ] DO NOT RELEASE

Rationale: <why the candidate is or is not releasable>

Follow-up issues: <issue links, or None>
```

`RELEASE` is valid only when every required criterion passes and no blocking
finding remains. If the candidate commit changes, rerun the full project scope
and record a new decision.

## Publication and completion

After a `RELEASE` decision:

1. Create the annotated project tag at the approved candidate commit.
2. Push the tag without moving or replacing an existing tag.
3. Create the GitHub Release using the approved project-scoped notes.
4. Upload the required artifacts and checksums.
5. Verify that the tag, artifacts, checksums, and links identify the candidate.
6. Close the release issue with links to the tag and GitHub Release.

A release is complete only after all six steps succeed. Preserve a failed or
incorrectly published release and issue the next `MINOR` version; do not
silently replace its tag or artifacts.
