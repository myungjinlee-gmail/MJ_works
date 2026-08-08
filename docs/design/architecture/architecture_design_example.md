# Hardware Target Selection Architecture

> **Illustrative example — non-normative.**
>
> This file demonstrates the architecture design format. It is not the
> software's accepted architecture and does not serve as product authority. The
> component diagram asset paths illustrate the required source-and-render links;
> the assets are not part of this example.

## Scope

- Build-time selection of the SDK hardware-target implementation
- The target-independent boundary between the SDK core and hardware-specific
  behavior

## Design Purpose

Provide one stable hardware-service boundary while allowing each configured
build to contain exactly one target-specific implementation. The architecture
prevents the SDK core from depending directly on a hardware variant.

## Context

- External dependencies:
    - CMake consumes the canonical `SDK_HW_TARGET` value and selects the source
      set for the configured build.
    - The selected hardware platform provides the resources used by its
      target-specific implementation.

## Design

### Component Diagram

[PlantUML source](diagrams/hardware-target-components.puml)

![Hardware target component diagram](diagrams/hardware-target-components.svg)

### Dynamic Behavior

#### Component-level Sequence

```mermaid
sequenceDiagram
    participant Core as SDK Core
    participant Boundary as Hardware Service Boundary
    participant Target as Selected Hardware Implementation
    Core->>Boundary: Request hardware behavior
    Boundary->>Target: Delegate request
    Target-->>Boundary: Return target-independent result
    Boundary-->>Core: Return result
```

The selected implementation performs the interaction in the caller's execution
context. The participants show component ordering and do not represent one
thread per component.

#### Data Flow

The SDK core passes abstract hardware requests to Hardware Service Boundary and
receives target-independent results. The boundary passes the request to the
selected implementation. Concrete request types, result types, and data-flow
details will move to the dedicated hardware-service component design when it is
introduced.

#### Control Flow

Not applicable: build configuration selects the implementation before runtime,
and runtime requests do not branch between target implementations.

#### State Machine

Not applicable: the selection is immutable for the configured build and this
architecture introduces no component-level state machine.

### Components

<a id="swad-component-01"></a>

#### SDK Core

- Responsibility:
    - Initiate target-independent hardware requests needed by SDK behavior.
    - Remain independent of all concrete hardware-target implementations.
- Input:
    - Application or SDK operation requiring hardware behavior
- Output:
    - Target-independent SDK result
- Relationships:
    - Inherits from:
    - Uses:
        - [swad-component-02](#swad-component-02)
- Traceability:
    - Upstream:
        <!--
        Illustrative exception: this example has no companion SWR for SDK Core.
        Every component in an accepted architecture shall have at least one
        concrete SWR link under Upstream.
        -->
    - Downstream:
    - Configuration:

<a id="swad-component-02"></a>

#### Hardware Service Boundary

- Responsibility:
    - Present target-independent hardware behavior to SDK Core.
    - Delegate each request to the implementation included in the configured
      build.
- Input:
    - Target-independent hardware request
- Output:
    - Target-independent hardware result or error
- Relationships:
    - Inherits from:
    - Uses:
        - [swad-component-03](#swad-component-03)
        - [swad-component-04](#swad-component-04)
        - [swad-component-05](#swad-component-05)
- Traceability:
    - Upstream:
        - [SWR-CFG-001](../requirement/software_requirement_example.md)
    - Downstream:
    - Configuration:

The three `Uses` relationships are mutually exclusive configured alternatives;
they are not simultaneous runtime dependencies.

<a id="swad-component-03"></a>

#### Vanilla Hardware Implementation

- Responsibility:
    - Provide Hardware Service Boundary behavior for `SDK_HW_TARGET=vanilla`.
- Input:
    - Target-independent hardware request
- Output:
    - Target-independent hardware result or error
- Relationships:
    - Inherits from:
    - Uses:
- Traceability:
    - Upstream:
        - [SWR-CFG-001](../requirement/software_requirement_example.md)
    - Downstream:
    - Configuration:

<a id="swad-component-04"></a>

#### NVIDIA Hardware Implementation

- Responsibility:
    - Provide Hardware Service Boundary behavior for `SDK_HW_TARGET=nvidia`.
- Input:
    - Target-independent hardware request
- Output:
    - Target-independent hardware result or error
- Relationships:
    - Inherits from:
    - Uses:
- Traceability:
    - Upstream:
        - [SWR-CFG-001](../requirement/software_requirement_example.md)
    - Downstream:
    - Configuration:

<a id="swad-component-05"></a>

#### Arm Hardware Implementation

- Responsibility:
    - Provide Hardware Service Boundary behavior for `SDK_HW_TARGET=arm`.
- Input:
    - Target-independent hardware request
- Output:
    - Target-independent hardware result or error
- Relationships:
    - Inherits from:
    - Uses:
- Traceability:
    - Upstream:
        - [SWR-CFG-001](../requirement/software_requirement_example.md)
    - Downstream:
    - Configuration:

### Interfaces

This architecture introduces no external software interface. Hardware Service
Boundary is internal to the SDK. If the SDK later exposes a public hardware
interface, this section will retain its conceptual boundary and link the owning
external interface specification.

- External interface specifications:

### Execution Architecture

#### Threads

Hardware requests execute in the caller's conceptual execution context. The
architecture does not assign one thread to each component. Detailed thread
ownership and synchronization will move to a dedicated execution component if
one is introduced.

#### Pipelines

This design contains no processing pipeline. The section remains so a future
conceptual pipeline can be described here, while buffering, backpressure,
scheduling, and implementation move to a dedicated pipeline component.

#### Timing Constraints

Not applicable: the linked illustrative requirement defines no timing
constraint.

#### Shared Resources

Each selected hardware implementation owns its target-private resources. The
detailed resource types, handles, lifetime, and synchronization will be defined
in its downstream SWCD.

#### Hardware/Core Mapping

The vanilla, NVIDIA, and Arm implementations map to their corresponding
configured hardware targets. Core affinity is not specified because the linked
illustrative requirement defines no processor-core allocation.
