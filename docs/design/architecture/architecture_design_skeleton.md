# <Software architecture design title>

<!--
Copy this file to the architecture design document for the software.
Replace every placeholder and remove instructional comments.

Describe software architecture at the component level. Keep source-level units,
classes, functions, and files in the downstream Software Component Design
(SWCD), not in this document.
-->

## Scope

- <Architecture scope>

## Design Purpose

<Problem addressed by the architecture and intended architectural outcome>

## Context

<!--
Identify external systems, libraries, services, hardware, and other dependencies
outside the owned architecture. State why each dependency is needed and which
boundary or contract governs the interaction.
-->

- External dependencies:
    - <External dependency and its relationship to the software>

## Design

### Component Diagram

<!--
Show components and architecture-significant relationships. Define relationship
details in each component's `Relationships` list; do not repeat them below the
diagram.
-->

[PlantUML source](<component-diagram.puml-location>)

![Component diagram](<component-diagram.svg-location>)

### Dynamic Behavior

#### Component-level Sequence

<!--
Use sequence diagrams to show ordering between components. Interactions may run
concurrently. A sequence-diagram participant represents an architecture
component, not necessarily one thread, process, task, or other execution unit.
Describe execution allocation separately under Execution Architecture.
-->

```mermaid
sequenceDiagram
    participant A as <Component A>
    participant B as <Component B>
    A->>B: <Interaction>
```

#### Data Flow

<!--
Keep this subsection. Describe only the conceptual data movement between
architecture components. Detailed data-flow diagrams, transformations, queues,
and implementation will move to a dedicated component when that component is
introduced.
-->

<Conceptual data flow and planned transfer to the dedicated component>

#### Control Flow

<!--
Describe architecture-level triggers, decisions, and response propagation only
when control flow needs clarification. Otherwise write
`Not applicable: <reason>`.
-->

<Control-flow description, or Not applicable: reason>

#### State Machine

<!--
Describe component-level states, transitions, and state-dependent behavior only
when a state machine is needed. Otherwise write `Not applicable: <reason>`.
-->

<State-machine description and diagram, or Not applicable: reason>

### Components

<!--
Repeat the following subsection for every architecture component.

Replace `nn` in `swad-component-nn` with the component's zero-padded two-digit
sequence number. Preserve an accepted component ID when its name or description
changes. Do not reuse or renumber an accepted component ID. In each relationship
link, replace `nn` with the target component's sequence number.

Write one architecture-level responsibility per list item and add as many
items as the component needs.

Describe inputs and outputs abstractly in terms of information, events, or
control. Do not include concrete data types, parameters, messages, or function
signatures.

Record inherited components and directly used components only when the
relationship affects an architecture responsibility, boundary, data or control
flow, ownership, lifetime, substitutability, or failure propagation. Exclude a
globally available component when all of these are true:

- it provides cross-cutting infrastructure uniformly to unrelated components;
- its use does not change the using component's architecture responsibility or
  boundary; and
- omitting the relationship does not hide required data flow, control flow,
  ownership, lifetime, failure propagation, or requirement allocation.

Logging, diagnostics, and generic utility components commonly meet this
exclusion rule. Include them when any criterion is not satisfied.

Do not identify implementation units, classes, functions, or source files.
Link the downstream SWCD that owns those details.
-->

<a id="swad-component-nn"></a>

#### <Component name>

- Responsibility:
    - <Architecture-level responsibility>
    - <Additional architecture-level responsibility>
- Input:
    - <Abstract input information, event, or control>
- Output:
    - <Abstract output information, event, or control>
- Relationships:
    - Inherits from:
        - [swad-component-nn](#swad-component-nn)
    - Uses:
        - [swad-component-nn](#swad-component-nn)
- Traceability:
    - Upstream:
        - [<SWR-ID>](<location>)
    - Downstream:
        - [<SWCD-ID>](<location>)
    - Configuration:
        - [<CONFIGURATION-SPEC-ID>](<location>)

### Interfaces

<!--
Keep this section. Briefly describe each external interface's conceptual
purpose and architecture boundary. Detailed operations, data definitions,
protocols, error behavior, timing, compatibility, and implementation will move
to the owning external interface specification.
-->

<Conceptual external-interface summary>

<How and when the details transfer to the external interface specifications>

- External interface specifications:
    - [<INTERFACE-SPEC-ID>](<location>)

### Execution Architecture

#### Threads

<!--
Keep this subsection. Describe only the conceptual execution contexts,
concurrency needs, and their relationship to architecture components. Detailed
thread ownership, scheduling, synchronization, lifecycle, and implementation
will move to a dedicated component when that component is introduced.
-->

<Conceptual thread model and planned transfer to the dedicated component>

#### Pipelines

<!--
Keep this subsection. Describe only the conceptual processing stages, ordering,
and concurrency between stages. Detailed pipeline ownership, buffering,
backpressure, scheduling, and implementation will move to a dedicated component
when that component is introduced.
-->

<Conceptual pipeline model and planned transfer to the dedicated component>

#### Timing Constraints

<!-- Describe architecture-level timing constraints when applicable. -->

<Timing constraint, or Not applicable: reason>

#### Shared Resources

<!--
Describe shared resource ownership and architecture-level access or
synchronization constraints when applicable.
-->

<Shared resource and ownership model, or Not applicable: reason>

#### Hardware/Core Mapping

<!--
Describe allocation to hardware devices or processor cores when applicable.
-->

<Hardware or core allocation, or Not applicable: reason>
