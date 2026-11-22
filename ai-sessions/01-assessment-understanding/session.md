# Session notes — Assessment understanding

## Goal
Understand the MiniVM optimiser take-home requirements and sequence implementation work.

## Requirements captured from the brief/conversation
- `optimize PROGRAM.mini SCHEMA.json` emits an optimised MiniVM program.
- Preserve results for data satisfying schema constraints, when the original program succeeds.
- Row ordering can be disregarded unless specified; numerical results use the assessment's relative tolerance of 1e-6.
- Optimiser execution budget: 1 second per program.
- `evaluate OPTIMIZER` checks candidate optimisers, reports defects through a non-zero exit status, and has a 2-minute runtime budget.
- Submission should include implementation source, scripts, docs, prompts/session material, logs and Git history, but not supplied binary executables.

## Approach agreed
Begin with parser and basic validation, then dependency analysis and backward liveness/DCE, test against the provided sample suite, implement the required command interfaces and evaluator, record cycle results, and document further optimization ideas.

## Evidence / status
The Git report shows commits for setup, parser, dependency analysis/DCE, optimizer/evaluation tests, evaluator fixes, submission documentation and binary removal. Commit hashes and dates are listed in the root `ai-sessions/README.md`.
