
import json
import re
import subprocess
import sys
import tempfile

from decimal import Decimal, InvalidOperation
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
    # Python optimizer: run using the current Python interpreter.
    if optimizer.suffix.lower() == ".py":
        return [
            sys.executable,
            str(optimizer),
            str(program),
            str(schema),
        ]

    # Unix shell launcher: use Git Bash's sh.exe on Windows.
    if sys.platform == "win32" and optimizer.name == "optimize":
        return [
            r"C:\Program Files\Git\bin\sh.exe",
            str(optimizer),
            str(program),
            str(schema),
        ]

    # Unix shell launcher on Linux.
    if optimizer.name == "optimize":
        return [
            "sh",
            str(optimizer),
            str(program),
            str(schema),
        ]

    # Native executable optimizer.
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


def validate_output(result, label="output"):
    """
    Validate the JSON structure returned by MiniVM.
    """
    if not isinstance(result, dict):
        raise ValueError(f"{label}: output must be a JSON object")

    if "ncols" not in result:
        raise ValueError(f"{label}: missing 'ncols'")

    ncols = result["ncols"]

    if not isinstance(ncols, int) or isinstance(ncols, bool) or ncols < 0:
        raise ValueError(f"{label}: 'ncols' must be a non-negative integer")

    if "rows" not in result:
        raise ValueError(f"{label}: missing 'rows'")

    rows = result["rows"]

    if not isinstance(rows, list):
        raise ValueError(f"{label}: 'rows' must be a list")

    for row_index, row in enumerate(rows):
        if not isinstance(row, list):
            raise ValueError(
                f"{label}: row {row_index} must be a list"
            )

        if len(row) != ncols:
            raise ValueError(
                f"{label}: row {row_index} has {len(row)} columns; "
                f"expected {ncols}"
            )

    if "cycles" in result:
        cycles = result["cycles"]

        if (
            not isinstance(cycles, int)
            or isinstance(cycles, bool)
            or cycles < 0
        ):
            raise ValueError(
                f"{label}: 'cycles' must be a non-negative integer"
            )

    return result


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
    skipped = 0

    # Overall cycle statistics.
    total_original_cycles = 0
    total_optimized_cycles = 0
    cycle_comparisons = 0

    with tempfile.TemporaryDirectory() as temp_dir:
        for program in programs:
            print(f"\nTesting {program.name}...", flush=True)

            stage = "original MiniVM"

            try:
                # Run the original program.
                original_result = run_command(
                    [str(MINIVM), str(program), str(DATA)]
                )

                # An original program that errors is outside the
                # equivalence requirement.
                if original_result.returncode != 0:
                    skipped += 1
                    print(
                        f"SKIP {program.name}: original program errors"
                    )
                    continue

                original_json = validate_output(
                    json.loads(original_result.stdout),
                    f"{program.name} original output",
                )

                # Run the supplied optimizer.
                stage = "optimizer"

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

                # Run the optimized program.
                stage = "optimized MiniVM"

                optimized_result = run_command(
                    [str(MINIVM), str(optimized_path), str(DATA)]
                )

                if optimized_result.returncode != 0:
                    raise RuntimeError(
                        "Optimized program failed: "
                        + optimized_result.stderr
                    )

                optimized_json = validate_output(
                    json.loads(optimized_result.stdout),
                    f"{program.name} optimized output",
                )

                # Preserve output order when the program explicitly sorts.
                source = program.read_text(encoding="utf-8-sig")

                has_sort = any(
                    line.strip().split(None, 1)[0].upper()
                    in {"SORT", "TOPK"}
                    for line in source.splitlines()
                    if line.strip() and not line.strip().startswith(";")
                )

                # Check original and optimized output equivalence.
                if not outputs_match(
                    original_json,
                    optimized_json,
                    has_sort,
                ):
                    raise RuntimeError(
                        "Original and optimized outputs differ"
                    )

                # Collect and display individual cycle statistics.
                original_cycles = original_json.get("cycles")
                optimized_cycles = optimized_json.get("cycles")

                if (
                    isinstance(original_cycles, int)
                    and not isinstance(original_cycles, bool)
                    and isinstance(optimized_cycles, int)
                    and not isinstance(optimized_cycles, bool)
                ):
                    total_original_cycles += original_cycles
                    total_optimized_cycles += optimized_cycles
                    cycle_comparisons += 1

                    cycles_saved = (
                        original_cycles - optimized_cycles
                    )

                    if original_cycles > 0:
                        reduction = (
                            cycles_saved / original_cycles
                        ) * 100

                        reduction_text = f"{reduction:.2f}%"
                    else:
                        reduction_text = "N/A"

                    print(
                        f"PASS {program.name} | "
                        f"Original: {original_cycles:,} | "
                        f"Optimized: {optimized_cycles:,} | "
                        f"Saved: {cycles_saved:,} | "
                        f"Reduction: {reduction_text}"
                    )

                else:
                    print(
                        f"PASS {program.name} | "
                        "Cycle information unavailable"
                    )

                passed += 1

            except subprocess.TimeoutExpired as error:
                failed += 1
                print(
                    f"FAIL {program.name}: {stage} timed out "
                    f"(limit: {error.timeout} seconds)"
                )

            except Exception as error:
                failed += 1
                print(f"FAIL {program.name}: {error}")

    # Final evaluation summary.
    print("\n" + "=" * 65)
    print("MINIVM OPTIMISATION EVALUATION SUMMARY")
    print("=" * 65)

    print(f"Passed programs:  {passed}")
    print(f"Failed programs:  {failed}")
    print(f"Skipped programs: {skipped}")

    # Overall cycle performance.
    if cycle_comparisons > 0:
        total_cycles_saved = (
            total_original_cycles - total_optimized_cycles
        )

        print("\nOVERALL CYCLE PERFORMANCE")
        print("-" * 65)

        print(f"Programs compared:       {cycle_comparisons}")
        print(f"Original total cycles:   {total_original_cycles:,}")
        print(f"Optimized total cycles:  {total_optimized_cycles:,}")
        print(f"Total cycles saved:      {total_cycles_saved:,}")

        if total_original_cycles > 0:
            overall_reduction = (
                total_cycles_saved / total_original_cycles
            ) * 100

            print(
                f"Overall cycle reduction: {overall_reduction:.2f}%"
            )
        else:
            print("Overall cycle reduction: N/A")

    else:
        print("\nCycle comparison unavailable.")

    print("=" * 65)

    if failed:
        print("Evaluation failed.")
        return 1

    if passed == 0:
        print("Evaluation failed: no programs passed.")
        return 1

    print("Evaluation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
