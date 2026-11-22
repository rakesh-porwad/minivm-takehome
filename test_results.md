# MiniVM Optimiser Test Results

Date: 2026-11-22 23:08

Command: `python .\tools\evaluate.py .\optimize`

## Evaluation Output

```text

Testing q0001.mini...
FAIL q0001.mini: optimizer timed out (limit: 1 seconds)

Testing q0002.mini...
FAIL q0002.mini: optimizer timed out (limit: 1 seconds)

Testing q0003.mini...
PASS q0003.mini | Original: 8,562 | Optimized: 8,496 | Saved: 66 | Reduction: 0.77%

Testing q0004.mini...
PASS q0004.mini | Original: 18,442 | Optimized: 13,582 | Saved: 4,860 | Reduction: 26.35%

Testing q0005.mini...
PASS q0005.mini | Original: 5,518 | Optimized: 4,723 | Saved: 795 | Reduction: 14.41%

Testing q0006.mini...
FAIL q0006.mini: optimizer timed out (limit: 1 seconds)

Testing q0007.mini...
PASS q0007.mini | Original: 2,596 | Optimized: 2,170 | Saved: 426 | Reduction: 16.41%

Testing q0008.mini...
PASS q0008.mini | Original: 1,524 | Optimized: 1,249 | Saved: 275 | Reduction: 18.04%

=================================================================
MINIVM OPTIMISATION EVALUATION SUMMARY
=================================================================
Passed programs:  5
Failed programs:  3
Skipped programs: 0

OVERALL CYCLE PERFORMANCE
-----------------------------------------------------------------
Programs compared:       5
Original total cycles:   36,642
Optimized total cycles:  30,220
Total cycles saved:      6,422
Overall cycle reduction: 17.53%
=================================================================
Evaluation failed.
```

Exit code: 1
