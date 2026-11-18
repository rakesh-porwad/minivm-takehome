
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from minivm_parser import parse_program
from minivm_analysis import get_dependencies


test_cases = [
    ("LOAD a, orders.amount", set(), {"a"}),
    ("ADD b, a, 10", {"a"}, {"b"}),
    ("IF c, a, b, 0", {"a", "b"}, {"c"}),
    ("GATHER d, a, b", {"a", "b"}, {"d"}),
    ("SORT e, a ASC NF", {"a"}, {"e"}),
    ("TOPK f, 10, a DESC NL", {"a"}, {"f"}),
    ("NLJOIN li, ri, lk, rk", {"lk", "rk"}, {"li", "ri"}),
    ("GROUP g, a, b", {"a", "b"}, {"g"}),
    ("GSUM total, g, amount", {"g", "amount"}, {"total"}),
    ("OUT a, b, c", {"a", "b", "c"}, set()),
]

failed = 0

for source, expected_reads, expected_writes in test_cases:
    instruction = parse_program(source)[0]
    reads, writes, supported = get_dependencies(instruction)

    passed = (
        supported
        and reads == expected_reads
        and writes == expected_writes
    )

    if passed:
        print(f"PASS: {source}")
    else:
        failed += 1
        print(f"FAIL: {source}")
        print(f"  Expected reads:  {expected_reads}")
        print(f"  Actual reads:    {reads}")
        print(f"  Expected writes: {expected_writes}")
        print(f"  Actual writes:   {writes}")
        print(f"  Supported:       {supported}")

print(f"\nResults: {len(test_cases) - failed}/{len(test_cases)} passed")

sys.exit(1 if failed else 0)
#This checks several important instruction categories, including arithmetic, conditional logic, sorting, joins, grouping and output.