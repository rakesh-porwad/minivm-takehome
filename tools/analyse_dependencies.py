
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT / "src"))

from minivm_parser import parse_program, validate_program
from minivm_analysis import analyse_dependencies


def main():

    if len(sys.argv) != 2:
        print(
            "Usage: python tools/analyse_dependencies.py program.mini"
        )
        sys.exit(1)

    program_path = Path(sys.argv[1])

    try:

        source = program_path.read_text(encoding="utf-8")

        instructions = parse_program(source)
        validate_program(instructions)

        results = analyse_dependencies(instructions)

        print("\nMINIVM INSTRUCTION DEPENDENCY REPORT\n")

        for item in results:

            reads = ", ".join(item["reads"]) or "-"
            writes = ", ".join(item["writes"]) or "-"

            print(
                f"Line {item['line_number']:3} | "
                f"{item['opcode']:10} | "
                f"Reads: {reads:20} | "
                f"Writes: {writes}"
            )

        print(
            f"\nTotal instructions: {len(instructions)}"
        )

        print("Analysis completed successfully.")

    except Exception as error:
        print(f"ERROR: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
