# MiniVM Optimiser — Initial Test Results

## Optimisation technique
Dead Code Elimination (DCE)

## Test summary
All eight supplied sample programs passed the initial equivalence tests.

| Program | Original cycles | Optimised cycles | Improvement |
|---|---:|---:|---:|
| q0001 | 13766 | 12495 | 9.23% |
| q0002 | 3617 | 3527 | 2.49% |
| q0003 | 8562 | 8496 | 0.77% |
| q0004 | 18442 | 13582 | 26.35% |
| q0005 | 5518 | 4723 | 14.41% |
| q0006 | 6338 | 6168 | 2.68% |
| q0007 | 2596 | 2170 | 16.41% |
| q0008 | 1524 | 1249 | 18.04% |

## Overall results
- Total original cycles: 60,363
- Total optimised cycles: 52,410
- Cycles saved: 7,953
- Overall cycle reduction: 13.18%
- Sample programs passing: 8 out of 8

## Current limitation
These results cover the supplied sample programs only. Further testing is required to establish correctness for other valid programs and schemas.