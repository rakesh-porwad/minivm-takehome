# Session notes — Advanced optimisation exploration

## Ideas discussed
- Constant folding when all operands are known and operation semantics permit evaluation at compile time.
- Redundant computation elimination only with proven equivalence and understood register effects.
- Filter pushdown only when row filtering/sort/null/tie semantics are preserved.
- SORT/TOPK rewrite opportunities when the output requires only a bounded prefix.

## q0007 investigation
q0007 sorts rows, filters to July 2023, then selects a limited prefix. This was identified as a possible future rewrite candidate. No advanced rewrite is evidenced in the supplied commit report.

## Status
Exploration/planning only. Do not list these transformations as implemented or tested.
