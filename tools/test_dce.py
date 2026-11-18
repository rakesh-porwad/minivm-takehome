
import json
import subprocess
import sys
import tempfile

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT / "src"))

from minivm_parser import parse_program, validate_program
from minivm_analysis import eliminate_dead_code


MINIVM = (
    PROJECT_ROOT / "bin" / "minivm-windows-x86_64.exe"
)

DATA = PROJECT_ROOT / "examples" / "data.json"
PROGRAMS = PROJECT_ROOT / "examples" / "programs"
EXPECTED = PROJECT_ROOT / "examples" / "expected"


def run_minivm(program_path):

    result = subprocess.run(
        [
            str(MINIVM),
            str(program_path),
            str(DATA)
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=30
    )

    return json.loads(result.stdout)


def main():

    passed = 0

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_dir = Path(temp_dir)

        for program_path in sorted(PROGRAMS.glob("*.mini")):

            instructions = parse_program(
                program_path.read_text(encoding="utf-8")
            )

            validate_program(instructions)

            optimized = eliminate_dead_code(instructions)

            optimized_path = (
                temp_dir / program_path.name
            )

            optimized_path.write_text(
                "\n".join(
                    item.source for item in optimized
                ) + "\n",
                encoding="utf-8"
            )

            original_result = run_minivm(program_path)
            optimized_result = run_minivm(optimized_path)

            expected_path = (
                EXPECTED / f"{program_path.stem}.json"
            )

            expected_result = json.loads(
                expected_path.read_text(encoding="utf-8")
            )

            # Compare results, excluding execution cycles.
            original_correct = (
                original_result["ncols"] == expected_result["ncols"]
                and original_result["rows"] == expected_result["rows"]
            )

            equivalent = (
                original_result["ncols"] == optimized_result["ncols"]
                and original_result["rows"] == optimized_result["rows"]
            )

            if original_correct and equivalent:

                saved = (
                    original_result["cycles"]
                    - optimized_result["cycles"]
                )

                improvement = (
                    saved / original_result["cycles"] * 100
                    if original_result["cycles"] else 0
                )

                print(
                    f"PASS {program_path.stem}: "
                    f"{original_result['cycles']} -> "
                    f"{optimized_result['cycles']} cycles "
                    f"({improvement:.2f}% improvement)"
                )

                passed += 1

            else:

                print(f"FAIL {program_path.stem}")

                if not original_correct:
                    print("Original program differs from expected output")

                if not equivalent:
                    print("Optimized output differs from original output")

    print(f"\nResults: {passed}/8 programs passed")

    if passed != 8:
        sys.exit(1)


if __name__ == "__main__":
    main()
