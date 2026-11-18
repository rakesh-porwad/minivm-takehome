
import json
import re
import subprocess
import sys
import tempfile

from decimal import Decimal, InvalidOperation
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROGRAM_DIR = PROJECT_ROOT / "examples" / "programs"
DATA = PROJECT_ROOT / "examples" / "data.json"
SCHEMA = PROJECT_ROOT / "examples" / "schema.json"

# Support both the Windows development executable and the
# Linux executable expected in the assessment environment.
WINDOWS_MINIVM = PROJECT_ROOT / "bin" / "minivm-windows-x86_64.exe"
LINUX_MINIVM = PROJECT_ROOT / "bin" / "minivm"

if sys.platform == "win32":
    MINIVM = WINDOWS_MINIVM
else:
    MINIVM = LINUX_MINIVM


def run_command(command, timeout=30):
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout,
    )


def optimizer_command(optimizer, program, schema):
    if optimizer.suffix.lower() == ".py":
        return [
            sys.executable,
            str(optimizer),
            str(program),
            str(schema),
        ]

    return [
        str(optimizer),
        str(program),
        str(schema),
    ]


NUMERIC_PATTERN = re.compile(
    r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$"
)

RELATIVE_TOLERANCE = Decimal("1e-6")


def as_numeric(value):
    """
    Convert numeric JSON values or numeric-looking strings to Decimal.
    Return None for non-numeric values.
    """
    if isinstance(value, bool) or value is None:
        return None

    if isinstance(value, (int, float)):
        try:
            return Decimal(str(value))
        except InvalidOperation:
            return None

    if isinstance(value, str) and NUMERIC_PATTERN.fullmatch(value):
        try:
            return Decimal(value)
        except InvalidOperation:
            return None

    return None


def values_equal(a, b):
    """
    Compare two values using the assessment's numerical tolerance.
    Non-numeric values must match exactly.
    """
    number_a = as_numeric(a)
    number_b = as_numeric(b)

    if number_a is not None and number_b is not None:
        difference = abs(number_a - number_b)
        scale = max(abs(number_a), abs(number_b))

        if scale == 0:
            return difference == 0

        return difference <= RELATIVE_TOLERANCE * scale

    return type(a) is type(b) and a == b


def rows_equal(row_a, row_b):
    if not isinstance(row_a, list) or not isinstance(row_b, list):
        return False

    if len(row_a) != len(row_b):
        return False

    return all(
        values_equal(a, b)
        for a, b in zip(row_a, row_b)
    )


def outputs_match(original, optimized, preserve_order):
    if original.get("ncols") != optimized.get("ncols"):
        return False

    original_rows = original.get("rows")
    optimized_rows = optimized.get("rows")

    if not isinstance(original_rows, list):
        return False

    if not isinstance(optimized_rows, list):
        return False

    if len(original_rows) != len(optimized_rows):
        return False

    if preserve_order:
        return all(
            rows_equal(a, b)
            for a, b in zip(original_rows, optimized_rows)
        )

    # Match rows without requiring the same row order.
    # Remove each matched row so duplicate rows are counted correctly.
    unmatched = list(optimized_rows)

    for original_row in original_rows:
        match_index = next(
            (
                index
                for index, optimized_row in enumerate(unmatched)
                if rows_equal(original_row, optimized_row)
            ),
            None,
        )

        if match_index is None:
            return False

        unmatched.pop(match_index)

    return not unmatched

def main():
    if len(sys.argv) != 2:
        print("Usage: evaluate OPTIMIZER", file=sys.stderr)
        return 1

    optimizer = Path(sys.argv[1]).resolve()

    if not optimizer.exists():
        print(f"ERROR: Optimizer not found: {optimizer}", file=sys.stderr)
        return 1

    if not MINIVM.exists():
        print("ERROR: MiniVM executable not found.", file=sys.stderr)
        return 1

    if not DATA.exists() or not SCHEMA.exists():
        print("ERROR: Example data or schema file not found.", file=sys.stderr)
        return 1

    programs = sorted(PROGRAM_DIR.glob("q*.mini"))

    if not programs:
        print("ERROR: No test programs found.", file=sys.stderr)
        return 1

    passed = 0
    failed = 0

    with tempfile.TemporaryDirectory() as temp_dir:
        for program in programs:
            print(f"Testing {program.name}...", flush=True)

            try:
                # Run the original program.
                original_result = run_command(
                    [str(MINIVM), str(program), str(DATA)]
                )

                # An original program that errors is outside the
                # equivalence requirement.
                if original_result.returncode != 0:
                    print(f"SKIP {program.name}: original program errors")
                    continue

                original_json = json.loads(original_result.stdout)

                # Run the supplied optimiser.
                optimized_source = run_command(
                    optimizer_command(optimizer, program, SCHEMA),
                    timeout=1,
                )

                if optimized_source.returncode != 0:
                    raise RuntimeError(
                        "Optimizer failed: " + optimized_source.stderr
                    )

                if not optimized_source.stdout.strip():
                    raise RuntimeError("Optimizer returned empty output")

                optimized_path = (
                    Path(temp_dir) / f"{program.stem}_optimized.mini"
                )

                optimized_path.write_text(
                    optimized_source.stdout,
                    encoding="utf-8",
                )

                # Run the optimised program.
                optimized_result = run_command(
                    [str(MINIVM), str(optimized_path), str(DATA)]
                )

                if optimized_result.returncode != 0:
                    raise RuntimeError(
                        "Optimised program failed: "
                        + optimized_result.stderr
                    )

                optimized_json = json.loads(optimized_result.stdout)

                # Preserve output order when the program explicitly sorts.
                source = program.read_text(encoding="utf-8-sig")
                has_sort = any(
                    line.strip().split(None, 1)[0].upper() in {"SORT", "TOPK"}
                    for line in source.splitlines()
                    if line.strip() and not line.strip().startswith(";")
                )

                if not outputs_match(
                    original_json,
                    optimized_json,
                    has_sort,
                ):
                    raise RuntimeError("Original and optimised outputs differ")

                passed += 1
                print(f"PASS {program.name}")

            except subprocess.TimeoutExpired:
                failed += 1
                print(f"FAIL {program.name}: timeout")

            except Exception as error:
                failed += 1
                print(f"FAIL {program.name}: {error}")

    print("\nEvaluation summary")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed:
        print("Evaluation failed.")
        return 1

    print("Evaluation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
