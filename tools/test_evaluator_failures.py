
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALUATOR = ROOT / "tools" / "evaluate.py"


def run_evaluator(*args):
    return subprocess.run(
        [sys.executable, str(EVALUATOR), *map(str, args)],
        capture_output=True,
        text=True,
        timeout=30,
    )


def check(name, condition, output=""):
    if condition:
        print(f"PASS {name}")
        return True

    print(f"FAIL {name}")
    if output:
        print(output)
    return False


def main():
    passed = 0
    total = 0

    # 1. Missing optimizer argument
    result = run_evaluator()
    total += 1
    passed += check(
        "Missing optimizer argument",
        result.returncode != 0,
        result.stderr or result.stdout,
    )

    # 2. Optimizer path does not exist
    result = run_evaluator(ROOT / "does_not_exist_optimizer")
    total += 1
    passed += check(
        "Invalid optimizer path",
        result.returncode != 0,
        result.stderr or result.stdout,
    )

    # 3. Optimizer produces invalid output
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)

        bad_optimizer = temp / "bad_optimizer.py"
        bad_optimizer.write_text(
            "print('this is not a valid MiniVM program')\n",
            encoding="utf-8",
        )

        result = run_evaluator(bad_optimizer)
        total += 1
        passed += check(
            "Invalid optimizer output",
            result.returncode != 0,
            result.stderr or result.stdout,
        )

    # 4. Optimizer produces empty output
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)

        empty_optimizer = temp / "empty_optimizer.py"
        empty_optimizer.write_text(
            "pass\n",
            encoding="utf-8",
        )

        result = run_evaluator(empty_optimizer)
        total += 1
        passed += check(
            "Empty optimizer output",
            result.returncode != 0,
            result.stderr or result.stdout,
        )

    # 5. Optimizer exceeds the one-second limit
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)

        slow_optimizer = temp / "slow_optimizer.py"
        slow_optimizer.write_text(
            "import time\ntime.sleep(5)\n",
            encoding="utf-8",
        )

        result = run_evaluator(slow_optimizer)
        total += 1
        passed += check(
            "Optimizer timeout",
            result.returncode != 0,
            result.stderr or result.stdout,
        )

    print(f"\nResults: {passed}/{total} tests passed")

    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
