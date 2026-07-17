# Static Analysis

The project uses clang-tidy 18.1.3 to automate the requested MISRA C++:2023
safety themes where that version has a suitable check. This configuration is a
focused defect-detection policy; it is not proof of complete MISRA compliance.

## Execution policy

- `.clang-tidy` is the single rule configuration used locally and in CI.
- All clang-tidy and compiler diagnostics are treated as errors.
- First-party CMake targets compile with the project warning policy and
  warnings-as-errors; vendored third-party targets do not inherit that policy.
- Automatic fixes are never enabled by the project runner.
- Project and test translation units are read from `compile_commands.json`.
- Compiled first-party generated C/C++ code is analyzed.
- Directories in `configuration/clang-tidy-exclude.txt` are omitted from both
  translation-unit analysis and header diagnostics.
- Source macros are forbidden by `cppcoreguidelines-macro-usage`. Recognized
  include guards are the only source-code exception. Command-line build
  definitions are ignored because they are compilation inputs rather than
  source macro declarations.

## LLVM 18 substitutions and limits

The requested `clang-analyzer-security.ArrayBound` and `ArrayBoundV2` checks
are not available in clang-tidy 18.1.3. Array risks are instead covered by
`clang-analyzer-core.uninitialized.ArraySubscript`,
`cppcoreguidelines-pro-bounds-constant-array-index`, and `-Warray-bounds`.

The requested `bugprone-implicit-widening-of-multiplication` check is not
available. `bugprone-misplaced-widening-cast`, narrowing-conversion checks,
`-Wconversion`, and `-Wsign-conversion` provide partial coverage.

The requested `readability-math-missing-parentheses` check is not available.
`-Wparentheses` detects compiler-recognized precedence risks but does not
enforce parentheses for every expression allowed by MISRA.

The following themes remain only partially enforceable with this toolset:

- arbitrary changes to loop-control variables;
- virtual default-argument policy;
- complete control of pragmas and compiler extensions;
- all runtime bounds, lifetime, exception-boundary, and sequencing behavior.

These areas require design review, compiler policy, tests, or a dedicated
MISRA compliance analyzer in addition to clang-tidy.
