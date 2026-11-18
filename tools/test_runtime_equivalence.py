
import json
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT / "src"))
from minivm_parser import parse_program

MINIVM = PROJECT_ROOT / "bin" / "minivm-windows-x86_64.exe"
OPTIMIZER = PROJECT_ROOT / "tools" / "optimize.py"
PROGRAM_DIR = PROJECT_ROOT / "examples" / "programs"
DATA = PROJECT_ROOT / "examples" / "data.json"
SCHEMA = PROJECT_ROOT / "examples" / "schema.json"


def run_minivm(program_path):
    return subprocess.run(
        [str(MINIVM), str(program_path), str(DATA)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )


def canonical_rows(rows):
    return Counter(
        json.dumps(row, sort_keys=True, separators=(",", ":"))
        for row in rows
    )


def results_match(original, optimized, preserve_order):
    if original["ncols"] != optimized["ncols"]:
        return False

    if preserve_order:
        return original["rows"] == optimized["rows"]

    return canonical_rows(original["rows"]) == canonical_rows(
        optimized["rows"]
    )


passed = 0
failed = 0
skipped = 0

programs = sorted(PROGRAM_DIR.glob("q*.mini"))

if not programs:
    print("ERROR: No example programs found.")
    sys.exit(1)

with tempfile.TemporaryDirectory() as temp_dir:
    for program in programs:
        original_result = run_minivm(program)

        # If the original program errors, the assessment permits
        # anything for its optimised version.
        if original_result.returncode != 0:
            skipped += 1
            print(f"SKIP {program.name}: original program errors")
            continue

        optimized_path = Path(temp_dir) / f"{program.stem}_optimized.mini"

        start = time.perf_counter()

        try:
            optimizer_result = subprocess.run(
                [
                    sys.executable,
                    str(OPTIMIZER),
                    str(program),
                    str(SCHEMA),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=1,
            )
        except subprocess.TimeoutExpired:
            failed += 1
            print(f"FAIL {program.name}: optimizer exceeded 1 second")
            continue

        elapsed = time.perf_counter() - start

        if optimizer_result.returncode != 0:
            failed += 1
            print(f"FAIL {program.name}: optimizer returned an error")
            print(optimizer_result.stderr)
            continue

        optimized_path.write_text(
            optimizer_result.stdout,
            encoding="utf-8"
        )

        optimized_result = run_minivm(optimized_path)

        if optimized_result.returncode != 0:
            failed += 1
            print(f"FAIL {program.name}: optimized program errors")
            print(optimized_result.stderr)
            continue

        try:
            original_json = json.loads(original_result.stdout)
            optimized_json = json.loads(optimized_result.stdout)
        except json.JSONDecodeError as error:
            failed += 1
            print(f"FAIL {program.name}: invalid MiniVM JSON: {error}")
            continue

        instructions = parse_program(
            program.read_text(encoding="utf-8-sig")
        )

        preserve_order = any(
            instruction.opcode in {"SORT", "TOPK"}
            for instruction in instructions
        )

        if results_match(
            original_json,
            optimized_json,
            preserve_order
        ):
            passed += 1
            print(
                f"PASS {program.name}: "
                f"{elapsed:.3f}s optimizer time"
            )
        else:
            failed += 1
            print(f"FAIL {program.name}: output mismatch")
            print("Original:", original_json["rows"][:3])
            print("Optimized:", optimized_json["rows"][:3])

print("\nRuntime equivalence results")
print(f"Passed:  {passed}")
print(f"Failed:  {failed}")
print(f"Skipped: {skipped}")
print(f"Total:   {passed + failed + skipped}")

sys.exit(1 if failed else 0)
