@'
# MiniVM Optimiser

## Overview

This project implements a conservative Dead Code Elimination (DCE) optimiser for MiniVM programs.

The optimiser analyses instruction dependencies and removes instructions whose results are not required by program outputs, while preserving program behaviour.

## Project Structure

- `src/` – parser and static analysis implementation.
- `tools/` – optimiser, evaluator and test scripts.
- `examples/` – sample programs, input data, schema and expected outputs.
- `tests/` – additional MiniVM test programs.
- `docs/` – MiniVM documentation and project notes.
- `logs/` – test and performance results.
- `ai_sessions/` – AI-assisted development session records.

## Requirements

- Python 3
- MiniVM runtime supplied with the assessment
- Git Bash on Windows for the shell-based optimiser launcher.

## Running the Optimiser

From the project root:

```powershell
python tools\optimize.py examples\programs\q0001.mini examples\schema.json