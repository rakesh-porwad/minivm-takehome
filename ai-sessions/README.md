Note: the account data export was requested and is pending to be received as raw session prompts from ChatGPT.

# AI Sessions — MiniVM Take-Home Assessment

This directory documents the AI-assisted work for the MiniVM optimiser assessment, organised by development stage and aligned against the available Git commit report.

## Record integrity

These notes and prompt collections are **reconstructed summaries**, not original raw ChatGPT exports. `prompts/prompts` are reconstructed from the available conversation history and project milestones; they are not guaranteed verbatim. `prompts/subagent_prompt.md` is a proposed reusable review prompt and **was not evidence that a subagent was run**. Keep raw transcripts separately if they are later recovered.

## Git timeline used to reconcile milestones

| Commit | Date/time (local, +1100) | Milestone |
|---|---|---|
| `418eb40` | 2026-11-18 13:14 | Initial project setup |
| `60592c2` | 2026-11-18 13:21 | Parser and validation |
| `87d3799` | 2026-11-18 14:02 | Dependency analysis and DCE |
| `f92f6ca` | 2026-11-18 22:27 | Optimiser and evaluation tests |
| `be29498` | 2026-11-20 14:34 | Evaluator validation and Windows compatibility |
| `6e971c0` | 2026-11-20 20:02 | Submission docs and final-review work |
| `ca43b59` | 2026-11-20 20:05 | Remove MiniVM binaries from tracked submission |


## Session index

1. Assessment understanding
2. Environment and project setup
3. MiniVM parser
4. Dependency analysis
5. Dead code elimination
6. Testing and validation
7. Optimiser integration
8. Performance analysis
9. Evaluator development
10. Advanced optimisation exploration
11. Final review and submission

Each stage includes `prompts.md` (reconstructed prompt outline) and `session.md` (milestone summary). Additional prompt artefacts are in `prompts/`.


## Evidence and limitations

- Timeline is based on the user-provided `git-review.txt` report.
- Commit messages and file-change lists confirm milestone names and artifact presence; they do not independently prove every implementation detail or test passed.
- Test cycle figures are transcribed from the reported DCE test output and project logs in the conversation.
- The working tree report shows `ai-sessions/`, `bin/`, and `git-review.txt` untracked at the time of capture. The `bin/` folder was local and excluded from the tracked final submission; the report indicates binary files were removed from Git.
- Review each status against the actual current files before submission, and preserve genuine AI transcripts if available.
