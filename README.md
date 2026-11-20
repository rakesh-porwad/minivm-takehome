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
```

The optimised MiniVM program is written to standard output.

## Running the Evaluator

```powershell
python tools\evaluate.py tools\optimize.py
```

The evaluator compares original and optimised program execution.

## Running Tests

```powershell
python tools\test_dependencies.py
python tools\test_dce_logic.py
python tools\test_numeric_tolerance.py
python tools\test_runtime_equivalence.py
python tools\test_evaluator_failures.py
```

## Optimisation Results

Evaluation of the eight supplied sample programs showed:

- Original total cycles: 60,363
- Optimised total cycles: 52,410
- Cycles saved: 7,953
- Overall cycle reduction: 13.18%
- Supplied sample programs passing: 8/8

See `logs/test-results.md` for detailed results.

## Current Scope and Limitations

The current implementation focuses on conservative Dead Code Elimination. It does not yet implement advanced optimisations such as constant folding, common subexpression elimination or schema-driven value analysis.

The supplied examples provide initial evidence of correctness and performance. Broader testing across additional valid programs and schemas is required for stronger confidence.