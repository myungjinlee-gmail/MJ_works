# Coding Guideline

## Scope

- All project C++ code shall compile as C++17 without compiler extensions.
- `.clang-format` is the formatting source of truth.
- `.clang-tidy` and `static_analysis.md` define automated enforcement. This
  document remains the policy source of truth, including rules that tools
  enforce only partially or cannot enforce.

## Naming

| Item | Convention | Example |
| --- | --- | --- |
| Namespace, function, variable, file | `snake_case` | `capture_frame` |
| Class, struct, enum | `PascalCase` | `FrameBuffer` |
| Constant | `kPascalCase` | `kMaximumFrames` |
| Private data member | `snake_case_` | `frame_count_` |
| Include guard | `PROJECT_PATH_FILE_HPP` | `MJ_SDK_TYPES_HPP` |

Abbreviations shall be treated as words, and one term shall use one spelling
throughout an interface.

## Interfaces

- Public SDK declarations belong in `include/`; implementation details belong
  in `src/` or the owning component.
- Each interface shall make input validity, output, ownership, lifetime, error
  behavior, and thread-safety expectations clear in its type or documentation.
- A public-interface change shall link the affected requirement or design and
  identify compatibility impact.
- Headers shall include what they use and shall not depend on include order.

## Ownership and lifetime

- Resource ownership shall use RAII.
- Every resource acquisition shall have a matching release. Acquisition and
  release shall be owned by the same abstraction and placed at corresponding
  lifecycle boundaries.
- Owning raw pointers and direct owning `new` or `delete` are prohibited.
- After the project allocator implementation is introduced, dynamic allocation
  outside that implementation shall be prohibited.
- Raw pointers and references are non-owning; nullable pointers and borrowed
  lifetimes shall be explicit at the interface.
- A returned pointer, reference, view, or callback shall not outlive the object
  that owns the referenced state.

## Error handling

- Expected failures shall be represented explicitly by a return value or
  project status type and shall not be ignored.
- Every detected error shall be logged before it is handled, returned, or
  propagated.
- Exceptions are prohibited. Code shall not use `try`, `catch`, `throw`, or
  exception-based control flow.
- Error handling shall preserve enough context to identify the failed operation
  without exposing secrets or leaving partially updated state.

## Concurrency

- Multithreading synchronization mechanisms shall be used only by the owning
  framework or a dedicated control unit. General feature code shall not use
  synchronization mechanisms.
- Within an allowed framework or control unit, the owner of mutable shared state
  and its synchronization mechanism shall be identifiable from the design or
  implementation.
- Within those units, access to shared mutable state shall be synchronized;
  lock ordering shall be documented when more than one lock can be held.
- Code shall not call an external callback while holding an internal lock.
- Every started thread shall have an owner and a defined stop and join path;
  detached threads are prohibited.

## Classes and variables

- Classes shall not declare static data variables.
- Namespace-scope global variables are prohibited. A variable that semantically
  represents one unique resource across the entire system may be allowed only
  through explicit review approval.

## Control flow

- Every function shall have a single entry and a single exit.
- An explicit `return` shall appear only once, as the final statement of a
  function. Early and intermediate returns are prohibited.
- Unstructured jumps, including `goto`, are prohibited.

## Preprocessor

- Source macros are prohibited. Include guards are the only permitted source
  macro use.

## Traceability and verification

- Each change shall link its issue and keep requirements, design, source, tests,
  and user documentation consistent where they are affected.
- Changed behavior shall have a defined pass/fail verification criterion and
  objective evidence from an applicable test, analysis, build, or review.
- Verification and review evidence shall be recorded with the reviewed commit.

These rules are informed by Automotive SPICE 4.0 SWE.3 and SWE.4 and the
published scope of ISO 26262-6:2018. They do not claim conformity to either
standard.

## References

- [Automotive SPICE 4.0 Process Assessment Model](https://vda-qmc.de/wp-content/uploads/2023/12/Automotive-SPICE-PAM-v40.pdf)
- [ISO 26262-6:2018 overview](https://www.iso.org/standard/68388.html)
- [Static analysis policy](static_analysis.md)
