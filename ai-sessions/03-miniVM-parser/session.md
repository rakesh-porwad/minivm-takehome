# Session notes — MiniVM parser

## Files recorded in Git
- `src/minivm_parser.py`
- `tools/inspect_program.py`

## Implementation recorded
- `Instruction` dataclass stores line number, opcode, operands and source text.
- Comment removal respects semicolons inside quoted strings.
- Operand splitting handles commas outside strings and doubled single-quote escaping.
- Opcode names are normalised to uppercase.
- Basic validation checks empty programs, instruction-count limit, one final `OUT`, and non-empty OUT operands.

## Validation caveat
The available history confirms the parser files were added and Python compilation was reported in conversation. A complete parser edge-case suite is not evidenced by this Git report alone.

## Git evidence
Commit `60592c2` — 2026-11-18 13:21 +1100.
