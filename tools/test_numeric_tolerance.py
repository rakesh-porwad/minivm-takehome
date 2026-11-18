
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from evaluate import values_equal, rows_equal, outputs_match


tests = [
    ("Exact numeric match", 100, 100, True),
    ("Within relative tolerance", "100.000000", "100.000050", True),
    ("Outside relative tolerance", "100", "100.001", False),
    ("Exact zero match", "0", "0", True),
    ("Zero versus non-zero", "0", "0.00000001", False),
    ("Exact text match", "hello", "hello", True),
    ("Different text", "hello", "world", False),
    ("Boolean values", True, True, True),
    ("Boolean versus number", True, 1, False),
    ("Negative numbers", "-100.000000", "-100.000050", True),
]

failed = 0

for name, a, b, expected in tests:
    actual = values_equal(a, b)

    if actual == expected:
        print(f"PASS: {name}")
    else:
        failed += 1
        print(f"FAIL: {name} (expected {expected}, got {actual})")


# Test row comparison.
if rows_equal([1, "100.000000"], [1, "100.000050"]):
    print("PASS: Row comparison with numeric tolerance")
else:
    failed += 1
    print("FAIL: Row comparison with numeric tolerance")


# Test unordered output rows and duplicate preservation.
original = {
    "ncols": 1,
    "rows": [["10.000000"], ["20.000000"], ["10.000000"]],
}

optimized = {
    "ncols": 1,
    "rows": [["20.000000"], ["10.000005"], ["10.000000"]],
}

if outputs_match(original, optimized, preserve_order=False):
    print("PASS: Unordered rows with duplicates")
else:
    failed += 1
    print("FAIL: Unordered rows with duplicates")


print(f"\nResults: {len(tests) + 2 - failed}/{len(tests) + 2} passed")

sys.exit(1 if failed else 0)
