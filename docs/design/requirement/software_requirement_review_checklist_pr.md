# Software Requirement — PR Review Checklist

## Identification and classification

- [ ] The parent directory name, the SWR ID in the filename and document title,
      and the value under `Requirement metadata` > `ID` are identical.

- [ ] `Type` expresses one primary characteristic of the requirement:
      `Functional`, `Quality`, `Interface`, `Constraint`, or `Configuration`.

- [ ] `Applicability` is expressed as `All` or an explicit configuration
      expression that determines the configurations in which the requirement
      applies.

## Requirement content

- [ ] `Requirement` contains exactly one independent obligation beginning with
      `The software shall`.

- [ ] The applicable conditions and the behavior or outcome the software shall
      provide are clear.

- [ ] The requirement contains no ambiguous or subjective language and cannot
      reasonably be interpreted in different ways.

- [ ] The requirement does not combine multiple obligations that can be
      implemented, changed, or verified independently.

- [ ] The requirement does not unnecessarily mandate an implementation method,
      class, function, file, or algorithm, unless that implementation constraint
      is itself required.

## Quantitative and boundary conditions

- [ ] When requirement satisfaction depends on a quantity, the requirement
      defines the value, unit, range, tolerance, or time limit.

- [ ] When normal conditions alone are insufficient, the requirement defines
      the necessary boundary, maximum, minimum, or error conditions.

## Verifiability

- [ ] Requirement satisfaction can be determined objectively through an
      observable result.

- [ ] An SWRVS can derive Acceptance Criteria without adding new behavior,
      conditions, or quantitative limits.

- [ ] A requirement for which testing is unsuitable can be verified through
      `Review`, `Analysis`, or `Static analysis`.

## Rationale and artifact boundary

- [ ] `Rationale` explains why the requirement is needed and links exactly one
      initial ticket.

- [ ] The requirement file contains no Acceptance Criteria, verification
      procedure, expected test result, executed result, or evidence.
