
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT / "src"))

from minivm_parser import parse_program, validate_program
from minivm_analysis import eliminate_dead_code


def main():

    # The assessment requires exactly two arguments:
    # optimize program.mini schema.json

    if len(sys.argv) != 3:
        print(
            "Usage: optimize program.mini schema.json",
            file=sys.stderr
        )
        return 1

    program_path = Path(sys.argv[1])
    schema_path = Path(sys.argv[2])

    try:
        # Read the original program.
        source = program_path.read_text(
            encoding="utf-8-sig"
        )

        # Read and validate the schema JSON.
        schema_text = schema_path.read_text(
            encoding="utf-8-sig"
        )

        json.loads(schema_text)

        # Parse and validate the program.
        instructions = parse_program(source)
        validate_program(instructions)

        # Apply dead code elimination.
        optimized = eliminate_dead_code(instructions)

        # Validate the resulting program.
        validate_program(optimized)

        # Print ONLY the optimised MiniVM program to stdout.
        output = "\n".join(
            instruction.source
            for instruction in optimized
        ) + "\n"

        sys.stdout.write(output)

        return 0

    except Exception as error:
        print(
            f"Optimizer error: {error}",
            file=sys.stderr
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())


#A few things to understand:
#- The program accepts the original .mini file and the schema JSON.
#- It parses and validates the program.
#- It applies DCE.
#- It prints only MiniVM instructions to standard output.
#- It reports errors to standard error.
#- It reads UTF-8 files, including files with a UTF-8 BOM, and writes plain text without a BOM.