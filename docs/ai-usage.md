# AI models used and spend

All AI assistance for this assessment was provided through the **ChatGPT Desktop application** on a Windows computer, using the **ChatGPT Free plan**.

ChatGPT was used as an assistant throughout the assessment for understanding requirements, planning the implementation, discussing optimisation approaches, reviewing code, debugging issues, preparing tests and improving documentation.

The exact model identifiers, request counts, token consumption and per-session usage statistics were not recorded in a form that could be independently verified. Therefore, no estimated usage or cost figures are presented.

## AI tools and usage

| Metric | Details |
|---|---|
| Interface | Desktop application |
| Tool / Model | OpenAI GPT-5.4 |
| Plan | Free |
| Operating System | Windows |
| Requests | 73 |
| Approx. Input Tokens | ~2M |
| Approx. Output Tokens | ~20K |
| Credits / Cost | N/A (Free plan; no API credits used) |

**Note:** Requests, Input/output tokens and credits are just based on guess because Free plan of Tool has been used so not having all exact stats.

**Spend:** The assessment work was performed using the ChatGPT Free plan. No separately billed API usage or paid AI subscription was used for this work. A monetary cost estimate is therefore not applicable.

## Rough split by phase

| Phase | AI assistance provided | Developer contribution |
|---|---|---|
| Requirements understanding and planning | Helped interpret the MiniVM assessment requirements, identify deliverables and break the work into implementation stages. | Reviewed the assessment requirements and determined the implementation priorities. |
| Design and implementation | Discussed parser design, instruction dependencies, register usage and backward liveness analysis for Dead Code Elimination (DCE). Provided coding guidance and suggestions. | Implemented and integrated the Python modules, reviewed the suggested logic and adapted the solution to the project. |
| Optimisation development | Assisted with understanding safe dead-code removal, supported and unsupported instructions, and optimisation boundaries. | Developed and refined the optimiser and ensured unsupported instructions were handled conservatively. |
| Testing and debugging | Helped interpret test failures, Python errors, runtime output and optimiser behaviour. Suggested debugging steps and test improvements. | Ran the MiniVM runtime, investigated errors, corrected code and executed equivalence and optimiser tests. |
| Performance analysis | Helped add per-program and overall cycle-reduction reporting and interpret the results. | Ran the evaluator and reviewed the original versus optimised cycle counts. |
| Documentation and submission | Assisted with README content, improvement plan, AI usage disclosure, test results and Git commands. | Reviewed and maintained the project documentation and prepared the repository for submission. |

## Key AI-assisted activities

The main areas where ChatGPT provided assistance were:

- Understanding the assessment instructions and expected `optimize` and `evaluate` interfaces.
- Designing the parser and instruction dependency analysis.
- Understanding and implementing backward liveness analysis for Dead Code Elimination.
- Reviewing handling of instruction types and register dependencies.
- Debugging Python implementation and runtime issues.
- Preparing runtime-equivalence and optimiser test workflows.
- Improving the evaluator to report individual and aggregate cycle reductions.
- Preparing technical documentation and submission materials.

## Developer verification and responsibility

AI assistance was used as a development and learning aid. It did not replace the need to run and verify the implementation.

The developer was responsible for:

- Reviewing and adapting AI-generated suggestions.
- Integrating the implementation into the assessment repository.
- Running the MiniVM executable and Python test scripts.
- Investigating and correcting implementation and test failures.
- Checking runtime equivalence between original and optimised programs.
- Reviewing cycle-reduction results.
- Maintaining the final source code and documentation.

All reported test results should be understood as results obtained from the actual local test runs, rather than results assumed from AI-generated suggestions.

## Session records and transparency

The `ai-sessions/` directory contains reconstructed session summaries and prompt inventories prepared to document the AI-assisted development process.

These files are not raw ChatGPT conversation exports and should not be interpreted as complete transcripts or independently verified usage records.

A ChatGPT account data export was requested on 22 November 2026. It was still pending at the time this disclosure was prepared. No raw conversation records or usage statistics have been fabricated to fill that gap.

This disclosure aims to accurately describe the AI assistance used during the assessment and distinguish that assistance from the developer's own implementation, testing and verification work.
