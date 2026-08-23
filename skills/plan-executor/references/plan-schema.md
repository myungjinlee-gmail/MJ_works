# Plan YAML Schema Version 3

`plan.yaml` is the machine execution contract paired with human-readable
`plan.md`. Use four spaces for YAML indentation and quote string values.

```yaml
schema_version: 3

issue:
    number: 123
    requirements_file: "issue.md"
    sha256: "<64 lowercase hexadecimal characters>"

plan:
    human_file: "plan.md"
    sha256: "<64 lowercase hexadecimal characters>"
    status: "approved"

goals:
    - id: "G-001"
      title: "Create the required artifact structure"
      plan_ref: "plan.md#g-001-create-the-required-artifact-structure"
      requirement_refs:
          - "issue.md#detailed-requirements"
      depends_on: []
      status: "pending"
      changes:
          - id: "G-001-C-01"
            path: "docs/example.md"
            operation: "modify"
            points:
                - "Add the required artifact relationship."
      verification:
          - id: "G-001-V-01"
            title: "Review the artifact relationship"
            method: "review"
            requirement_refs:
                - "issue.md#verification-and-acceptance"
            targets:
                - "docs/example.md"
            procedure: "Inspect the documented artifact relationship."
            pass_condition: "Every required artifact relationship is present."
            status: "pending"
            evidence: []
          - id: "G-001-V-02"
            title: "Run the documentation tests"
            method: "command"
            requirement_refs:
                - "issue.md#verification-and-acceptance"
            targets: []
            command: "python3 -m pytest"
            working_directory: "."
            pass_condition: "The command exits with status 0."
            status: "pending"
            evidence: []
```

## Static fields

- `schema_version` shall be integer `3`.
- `issue.number` shall be a positive integer matching the plan directory.
- `requirements_file` and `human_file` shall be `issue.md` and `plan.md`.
- Each SHA-256 value shall hash the referenced file's exact bytes.
- `plan.status` shall be `draft` or `approved`; execution requires `approved`.
- `issue.md` shall contain exactly one `Purpose`, `Detailed requirements`,
  `Known impact`, and `Verification and acceptance` section.
- Goal IDs shall be unique, stable `G-NNN` identifiers. Do not renumber them
  after approval.
- Each Goal shall have the same ID and title in a `plan.md` heading.
- Each `plan.md` Goal shall contain `Requirements`, `Dependencies`, `Changes`,
  and `Verification and acceptance` subsections. Their static values shall
  exactly match `plan.yaml`.
- `plan_ref` and every `requirement_ref` shall resolve to existing headings.
- `depends_on` shall contain existing Goal IDs, contain no duplicates, and form
  an acyclic graph.
- Every Goal shall contain at least one file change and one verification item.
- Change IDs shall be unique and use `G-NNN-C-NN`.
- Change `path` shall be an exact repository-relative file path declared in
  `issue.md` Known impact. Reject directories, globs, parent traversal,
  absolute paths, backslashes, and placeholders.
- Change `operation` shall be `create`, `modify`, or `delete` and match Known
  impact. Represent a file move with a `delete` change for the old path and a
  `create` change for the new path; each point shall name the counterpart path.
- Change `points` shall be a non-empty list of unique, concrete strings copied
  from that file's Known impact children.
- Every Known impact modification point shall occur in exactly one `changes`
  item. A path may occur in multiple Goals only with non-overlapping points.
- Verification IDs shall be unique and use `G-NNN-V-NN`.
- Every verification item shall contain a title, method, at least one
  requirement reference, a `targets` list, and an objective `pass_condition`.
- Every verification item shall reference the resolved `issue.md` Verification
  and acceptance section.
- Verification `method` shall be `review`, `command`, or `manual`.
- A `review` item requires `procedure` and forbids `command` and
  `working_directory`.
- A `command` item requires an exact approved local `command` and
  repository-relative `working_directory`, and forbids `procedure`.
- A `manual` item requires `procedure` and forbids `command` and
  `working_directory`.
- Every target shall be an exact repository-relative path. Targets may include
  unchanged files that must be inspected.

## Runtime fields

- Goal `status` shall be `pending`, `in_progress`, `completed`, or `blocked`.
- At most one Goal may be `in_progress`.
- An `in_progress`, `blocked`, or `completed` Goal requires every dependency to
  be `completed`.
- A `blocked` Goal requires a non-empty `blocker` string.
- Verification `status` shall be `pending`, `passed`, `failed`, or `blocked`.
- A `pending` Goal requires every verification item to remain `pending`.
- A `blocked` verification item requires its Goal to be `blocked`.
- A `passed` or `failed` verification item requires at least one non-empty
  evidence string.
- A `completed` Goal requires every verification item to be `passed` with
  evidence.

The executor may update only runtime fields. Any static-field change requires
a new human review and approval through `issue-planner`.
