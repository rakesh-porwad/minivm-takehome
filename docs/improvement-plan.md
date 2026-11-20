# MiniVM Optimiser – Future Improvement Plan

## 1. Current Implementation

The current implementation focuses on conservative Dead Code Elimination (DCE).

It includes:
- MiniVM instruction parsing and validation.
- Instruction dependency analysis.
- Read and write tracking for supported instructions.
- Backward liveness analysis.
- Conservative handling of unsupported instructions.
- Removal of instructions whose results are not required.
- Runtime equivalence testing.

The initial evaluation of the eight supplied programs achieved a total cycle reduction of 13.18%, while preserving the tested outputs.

Correctness and predictable behaviour take priority over aggressive optimisation.

## 2. Proposed Development Plan

With a few additional days and unlimited compute and tokens, I would extend the optimiser in the following stages.

### Stage 1 – Improve Language Understanding and Static Analysis

- Review every instruction in the MiniVM documentation.
- Build a complete instruction metadata table covering operands, outputs, side effects and dependencies.
- Identify instructions that modify state or have observable side effects.
- Improve handling of multi-output instructions and control-flow behaviour.
- Add register definition and usage analysis.
- Handle unknown or unsupported instructions conservatively.

Expected outcome: A more complete and reliable foundation for further optimisation.

### Stage 2 – Implement Additional Optimisations

Implement the following transformations incrementally:

**Constant Folding:** Evaluate expressions at optimisation time when all operands are known constants.

**Common Subexpression Elimination:** Identify repeated expressions and reuse previous computations when safe.

**Algebraic Simplification:** Apply safe mathematical identities while respecting MiniVM numeric and NULL semantics.

**Redundant Instruction Elimination:** Remove unnecessary computations that do not contribute to observable results.

**Copy Propagation:** Replace references to copied values with their original values where safe.

Each optimisation would have independent correctness tests and performance measurements.

### Stage 3 – Schema-Aware Optimisation

- Analyse field types and explicitly guaranteed constraints.
- Use known value ranges where the schema guarantees them.
- Apply type-aware transformations.
- Avoid assumptions about unconstrained values.
- Preserve NULL and numeric precision behaviour.

Expected outcome: More optimisation opportunities without compromising correctness.

### Stage 4 – Expand Correctness Testing

Develop tests covering:

- All documented instruction types.
- Empty and minimal programs.
- NULL values and missing fields.
- Duplicate values and repeated expressions.
- Numeric boundary values and precision.
- Multiple outputs and instruction dependencies.
- Sorting, grouping and joins.
- Unsupported instructions.
- Different valid schemas and datasets.

Introduce property-based and randomly generated MiniVM programs. Compare original and optimised execution results, respecting row-order rules and numerical tolerance.

### Stage 5 – Differential and Stress Testing

With unlimited compute, I would:

- Generate large numbers of valid programs.
- Generate datasets satisfying their schemas.
- Execute original and optimised versions.
- Detect and record behavioural differences.
- Minimise failing examples to find reproducible issues.
- Maintain regression tests for every discovered issue.

I would also test malformed programs and unsupported instructions to verify safe failure handling.

### Stage 6 – Performance Profiling and Benchmarking

Measure:

- Optimiser execution time.
- Original and optimised MiniVM cycle counts.
- Percentage reduction in execution cycles.
- Optimised instruction count.
- Memory usage.
- Performance across different program sizes.

Use profiling to identify expensive analysis operations and improve efficiency.

### Stage 7 – Engineering and Delivery Improvements

- Document each optimisation.
- Improve error reporting and diagnostics.
- Add automated regression testing.
- Ensure consistent command-line behaviour across supported platforms.
- Review timeout handling and resource limits.
- Maintain reproducible benchmark results.
- Document limitations and unsupported cases.

## 3. Prioritisation

1. Complete language and instruction analysis.
2. Strengthen correctness and regression testing.
3. Implement constant folding and copy propagation.
4. Implement common subexpression elimination and other safe transformations.
5. Explore schema-aware optimisation.
6. Run large-scale differential and stress testing.
7. Profile and refine performance.
8. Finalise documentation and delivery.

## 4. Success Criteria

The improved optimiser should:

- Preserve required observable behaviour for valid programs.
- Handle NULL values and numeric precision correctly.
- Safely support the documented instruction set.
- Meet the one-second per-program optimisation limit.
- Produce measurable improvements in execution cycles.
- Pass an extensive automated regression and differential test suite.

## 5. Final Approach

Correctness would remain the highest priority. I would introduce transformations incrementally, validate their safety against MiniVM semantics, and use automated differential testing.

Unlimited compute would primarily support broader test coverage, edge-case discovery and performance benchmarking, rather than being treated as a substitute for correctness.
