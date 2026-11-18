
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MINIVM = ROOT / "bin" / "minivm-windows-x86_64.exe"
DATA = ROOT / "examples" / "data.json"
SCHEMA = ROOT / "examples" / "schema.json"
PROGRAMS = ROOT / "examples" / "programs"
EXPECTED = ROOT / "examples" / "expected"


def run_minivm(program_path):
    result = subprocess.run(
        [str(MINIVM), str(program_path), str(DATA)],
        capture_output=True,
        text=True,
        check=True,
        timeout=30
    )
    return json.loads(result.stdout)


def main():
    passed = 0

    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)

        for original_path in sorted(PROGRAMS.glob("*.mini")):
            optimized_path = temp / original_path.name

            try:
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "tools" / "optimize.py"),
                        str(original_path),
                        str(SCHEMA)
                    ],
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True,
                    timeout=1,
                    stdout=optimized_path.open("w", encoding="utf-8")
                )

                original = run_minivm(original_path)
                optimized = run_minivm(optimized_path)

                expected_path = (
                    EXPECTED / f"{original_path.stem}.json"
                )
                expected = json.loads(
                    expected_path.read_text(encoding="utf-8")
                )

                equivalent = (
                    original["ncols"] == optimized["ncols"]
                    and original["rows"] == optimized["rows"]
                )

                expected_correct = (
                    original["ncols"] == expected["ncols"]
                    and original["rows"] == expected["rows"]
                )

                if equivalent and expected_correct:
                    saved = original["cycles"] - optimized["cycles"]
                    improvement = (
                        saved / original["cycles"] * 100
                        if original["cycles"] else 0
                    )

                    print(
                        f"PASS {original_path.stem}: "
                        f"{original['cycles']} -> "
                        f"{optimized['cycles']} cycles "
                        f"({improvement:.2f}% improvement)"
                    )
                    passed += 1
                else:
                    print(f"FAIL {original_path.stem}")
                    print("Original and optimised or expected results differ")

            except Exception as error:
                print(f"FAIL {original_path.stem}: {error}")

    print(f"\nResults: {passed}/8 programs passed")

    if passed != 8:
        sys.exit(1)


if __name__ == "__main__":
    main()
