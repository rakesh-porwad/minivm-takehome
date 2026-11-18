
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT / "src"))

from minivm_parser import parse_program, validate_program
from minivm_analysis import eliminate_dead_code


def main():

    if len(sys.argv) != 3:
        print(
            "Usage: python tools/run_dce.py input.mini output.mini"
        )
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    try:

        source = input_file.read_text(encoding="utf-8")

        instructions = parse_program(source)
        validate_program(instructions)

        optimized = eliminate_dead_code(instructions)

        # Validate the rewritten program.
        validate_program(optimized)

        output_text = "\n".join(
            instruction.source for instruction in optimized
        ) + "\n"

        output_file.parent.mkdir(
            parents=True, exist_ok=True
        )

        output_file.write_text(
            output_text, encoding="utf-8"
        )

        print(f"Original instructions: {len(instructions)}")
        print(f"Optimized instructions: {len(optimized)}")
        print(
            f"Instructions removed: {len(instructions) - len(optimized)}"
        )
        print(f"Saved optimized program: {output_file}")

    except Exception as error:
        print(f"ERROR: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
