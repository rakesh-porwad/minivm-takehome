# Session notes — Performance analysis

## Measured sample cycle results
The sample test output reported cycle reductions for all eight programs. Overall, 7,953 cycles were saved from a baseline of 60,363, corresponding to a 13.18% aggregate reduction.
- Best sample reduction: q0004, 26.35%.
- Lowest sample reduction: q0003, 0.77%.
- q0007 instruction count fell 49 to 31 (36.73%); its cycle reduction was 16.41%, so instruction count and cycle savings are different measures.

## Limits
These are MiniVM execution-cycle counts from the sample run, not elapsed-time measurements of the optimizer. A 1-second per-program optimizer runtime benchmark is not shown in the supplied Git review report.
