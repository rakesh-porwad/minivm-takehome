
import re
from dataclasses import dataclass, asdict

@dataclass
class Instruction:
    line_number: int
    opcode: str
    operands: list
    source: str

def remove_comment(line):
    """
    Remove comments beginning with ;
    while preserving semicolons inside quoted strings.
    """

    inside_string = False
    i = 0

    while i < len(line):
        char = line[i]

        if char == "'":
            if inside_string and i + 1 < len(line) and line[i + 1] == "'":
                i += 2
                continue

            inside_string = not inside_string

        elif char == ";" and not inside_string:
            return line[:i]

        i += 1

    return line

def split_operands(text, line_number):
    """
    Split operands on commas outside string literals.
    Handles escaped single quotes represented by two quotes.
    """

    if not text.strip():
        return []

    operands = []
    current = []
    inside_string = False
    i = 0

    while i < len(text):
        char = text[i]

        if char == "'":
            current.append(char)

            if inside_string and i + 1 < len(text) and text[i + 1] == "'":
                current.append("'")
                i += 2
                continue

            inside_string = not inside_string

        elif char == "," and not inside_string:
            operand = "".join(current).strip()

            if not operand:
                raise ValueError(
                    f"Line {line_number}: Empty operand"
                )

            operands.append(operand)
            current = []

        else:
            current.append(char)

        i += 1

    if inside_string:
        raise ValueError(
            f"Line {line_number}: Unterminated string literal"
        )

    operand = "".join(current).strip()

    if not operand:
        raise ValueError(
            f"Line {line_number}: Empty operand"
        )

    operands.append(operand)

    return operands

def parse_program(program_text):
    """
    Convert MiniVM source code into structured instructions.
    """

    instructions = []

    for line_number, original_line in enumerate(
        program_text.splitlines(), start=1
    ):

        line = remove_comment(original_line).strip()

        # Ignore blank lines and comment-only lines.
        if not line:
            continue

        parts = line.split(None, 1)

        opcode = parts[0].upper()

        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", parts[0]):
            raise ValueError(
                f"Line {line_number}: Invalid opcode"
            )

        operand_text = parts[1] if len(parts) > 1 else ""

        operands = split_operands(
            operand_text, line_number
        )

        instruction = Instruction(
            line_number=line_number,
            opcode=opcode,
            operands=operands,
            source=line
        )

        instructions.append(instruction)

    return instructions

def validate_program(instructions):
    """
    Validate the basic MiniVM program structure.
    """

    if not instructions:
        raise ValueError("Program is empty")

    if len(instructions) > 20000:
        raise ValueError("Program exceeds 20,000 instructions")

    out_positions = [
        i for i, instruction in enumerate(instructions)
        if instruction.opcode == "OUT"
    ]

    if len(out_positions) != 1:
        raise ValueError("Program must contain exactly one OUT")

    if out_positions[0] != len(instructions) - 1:
        raise ValueError("OUT must be the final instruction")

    if not instructions[-1].operands:
        raise ValueError("OUT must contain at least one operand")

    return True