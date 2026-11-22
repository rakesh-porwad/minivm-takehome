# Session notes — Dependency analysis

## File
- `src/minivm_analysis.py`
- `tools/analyse_dependencies.py`

## Implemented approach recorded
- Register pattern and reserved-keyword handling.
- Instruction-level read/write dependency analysis.
- Sort-key register extraction.
- Unknown instruction handling that marks unsupported cases rather than treating them as known removable operations.
- Dependency report tooling.

## Caveat
The dependency model was a prototype and needs review against instruction documentation for operand arity, roles, multi-output instructions and error/side-effect safety before it can be considered generally correct.

## Git evidence
Commit `87d3799` — 2026-11-18 14:02 +1100.
