# User prompts — MiniVM optimiser assessment

## Provenance notice
This is a **reconstructed prompt inventory** compiled from available ChatGPT conversation context, project milestones, and the Git-review report. These are not raw exported transcripts

## 01 — Assessment understanding
- Help me understand the MiniVM take-home requirements and break the work into beginner-friendly steps.
- Explain the `optimize` and `evaluate` interfaces, equivalence requirements, tolerances, time limits, and submission artifacts.
- Propose a staged plan and explain what I need to be able to defend in an interview.

## 02 — Environment and project setup
- Walk me through setting up Python, VS Code, Git and the project on Windows, step by step.
- Help create/activate a virtual environment, project directories, `.gitignore`, and initial commits.
- Explain PowerShell commands and troubleshoot errors as they occur.

## 03 — MiniVM parser
- Help implement a parser for MiniVM source that handles comments, commas in operands, quoted strings, and doubled single-quote escapes.
- Explain the parser and provide a utility to inspect/validate sample programs.

## 04 — Dependency analysis
- Help determine register reads and writes for MiniVM instructions for backward dependency/liveness analysis.
- Explain how sort-key operands and multi-output instructions should be handled.
- Keep unsupported/unknown instructions conservative.

## 05 — Dead code elimination
- Implement backward liveness to remove instructions whose results are not needed by `OUT`.
- Explain q0007's removals, the 49-to-31 instruction reduction, and the role of index registers such as `r39`/`r40`.
- Review the DCE logic and discuss safety limitations.

## 06 — Testing and validation
- Create a test harness that runs original and optimized MiniVM programs against expected outputs.
- Compare equivalence and report cycles and percentage improvements for q0001–q0008.
- Identify where exact row comparison differs from assessment rules for ordering and numeric tolerance.

## 07 — Optimizer integration
- Connect the Python optimization code to the required `optimize PROGRAM.mini SCHEMA.json` command.
- Ensure stdout contains program text and errors are reported separately.
- Help test generated optimized output by executing it with MiniVM.

## 08 — Performance analysis
- Summarize cycle savings across the sample suite and calculate aggregate reduction.
- Explain why instruction count reduction is not the same as cycle reduction.
- Distinguish MiniVM cycles from optimizer wall-clock runtime.

## 09 — Evaluator development
- Implement the required `evaluate OPTIMIZER` interface to test a candidate optimizer and exit non-zero for defects.
- Add validation, runtime/equivalence, numeric tolerance, malformed output, and failure-case tests.
- Troubleshoot evaluator behavior and Windows compatibility.

## 10 — Advanced optimization ideas
- Explore constant folding, redundant calculations, filter pushdown, and SORT/TOPK transformations.
- Prioritize semantic safety; consult instruction docs and test equivalence before implementing rewrites.
- Identify q0007 as a potential TOPK/filter optimization case without claiming an unverified rewrite.

## 11 — Final documentation and submission
- Review README, improvement plan, AI usage disclosure, logs, tests and Git history.
- Check submission requirements, remove binary executables from tracked files, and prepare a final checklist.
- Be transparent about AI assistance and reconstructed prompts/transcripts.

