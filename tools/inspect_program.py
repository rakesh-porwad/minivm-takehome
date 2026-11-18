
import argparse
import json
import sys

from pathlib import Path
from dataclasses import asdict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from minivm_parser import parse_program, validate_program

def main():

    parser = argparse.ArgumentParser(
        description="Parse a MiniVM program"
    )

    parser.add_argument(
        "program",
        help="Path to MiniVM program"
    )

    args = parser.parse_args()

    program_path = Path(args.program)

    try:
        program_text = program_path.read_text(
            encoding="utf-8"
        )

        instructions = parse_program(program_text)

        validate_program(instructions)

        result = [asdict(item) for item in instructions]

        print(json.dumps(result, indent=4))

        print(
            f"\nSUCCESS: Parsed {len(instructions)} instructions"
        )

    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()