
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from minivm_parser import parse_program
from minivm_analysis import eliminate_dead_code


test_cases = [
    {
        "name": "Basic dependency",
        "program": [
            "LOAD a, orders.amount",
            "ADD b, a, 10",
            "OUT b",
        ],
        "expected": [
            "LOAD a, orders.amount",
            "ADD b, a, 10",
            "OUT b",
        ],
    },
    {
        "name": "Register overwritten",
        "program": [
            "LOAD a, orders.amount",
            "ADD a, a, 10",
            "OUT a",
        ],
        "expected": [
            "LOAD a, orders.amount",
            "ADD a, a, 10",
            "OUT a",
        ],
    },
    {
        "name": "Earlier calculation becomes dead",
        "program": [
            "LOAD a, orders.amount",
            "ADD b, a, 10",
            "ADD b, a, 20",
            "OUT b",
        ],
        "expected": [
            "LOAD a, orders.amount",
            "ADD b, a, 20",
            "OUT b",
        ],
    },
    {
        "name": "Unused calculations removed",
        "program": [
            "LOAD a, orders.amount",
            "ADD b, a, 10",
            "ADD c, b, 20",
            "OUT a",
        ],
        "expected": [
            "LOAD a, orders.amount",
            "OUT a",
        ],
    },
    {
        "name": "Earlier LOAD overwritten",
        "program": [
            "LOAD a, orders.amount",
            "LOAD a, orders.quantity",
            "OUT a",
        ],
        "expected": [
            "LOAD a, orders.quantity",
            "OUT a",
        ],
    },
    {
        "name": "Unused JOIN removed",
        "program": [
            "LOAD lk, orders.customer_id",
            "LOAD rk, customers.customer_id",
            "NLJOIN li, ri, lk, rk",
            "OUT lk",
        ],
        "expected": [
            "LOAD lk, orders.customer_id",
            "OUT lk",
        ],
    },
    {
        "name": "JOIN retained when one output is used",
        "program": [
            "LOAD lk, orders.customer_id",
            "LOAD rk, customers.customer_id",
            "NLJOIN li, ri, lk, rk",
            "OUT li",
        ],
        "expected": [
            "LOAD lk, orders.customer_id",
            "LOAD rk, customers.customer_id",
            "NLJOIN li, ri, lk, rk",
            "OUT li",
        ],
    },
    {
        "name": "Unknown instruction prevents optimisation",
        "program": [
            "LOAD a, orders.amount",
            "UNKNOWN b, a",
            "OUT a",
        ],
        "expected": [
            "LOAD a, orders.amount",
            "UNKNOWN b, a",
            "OUT a",
        ],
    },
]

failed = 0

for test in test_cases:
    instructions = parse_program("\n".join(test["program"]))
    optimized = eliminate_dead_code(instructions)

    actual = [instruction.source for instruction in optimized]
    expected = test["expected"]

    if actual == expected:
        print(f"PASS: {test['name']}")
    else:
        failed += 1
        print(f"FAIL: {test['name']}")
        print("Expected:")
        print("\n".join(expected))
        print("Actual:")
        print("\n".join(actual))

print(f"\nResults: {len(test_cases) - failed}/{len(test_cases)} passed")

sys.exit(1 if failed else 0)
#It checks whether the optimiser keeps necessary instructions and removes instructions whose results are never used.