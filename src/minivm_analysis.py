
import re


# MiniVM register names:
# A letter or underscore, followed by letters, digits or underscores.
REGISTER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

KEYWORDS = {
    "NULL", "TRUE", "FALSE",
    "ASC", "DESC", "NF", "NL", "NULLEQ"
}


def is_register(operand):
    """Check whether an operand represents a register."""

    operand = operand.strip()

    return (
        REGISTER_PATTERN.fullmatch(operand) is not None
        and operand.upper() not in KEYWORDS
    )


def get_dependencies(instruction):
    """
    Return registers read and written by one instruction.

    Returns:
        reads: Registers used by the instruction.
        writes: Registers defined by the instruction.
        supported: Whether the instruction's semantics are known.
    """

    op = instruction.opcode
    args = instruction.operands

    reads = set()
    writes = set()

    def add_read(value):
        value = value.strip()
        if is_register(value):
            reads.add(value)

    def add_sort_key(value):
        # Sort key syntax: register ASC|DESC NF|NL
        parts = value.split()
        if parts:
            add_read(parts[0])

    # Instructions that produce one register.
    if op == "LOAD":
        writes.add(args[0])

    elif op == "FILL":
        writes.add(args[0])
        add_read(args[2])

    elif op in {"IOTA", "IDX", "SLICE"}:
        writes.add(args[0])
        add_read(args[1])

    elif op == "GATHER":
        writes.add(args[0])
        add_read(args[1])
        add_read(args[2])

    elif op in {
        "ADD", "SUB", "MUL", "DIV", "IDIV", "MOD",
        "EQ", "NE", "LT", "LE", "GT", "GE",
        "IS", "AND", "OR", "NOT", "ISNULL",
        "NVL", "IF", "NULLIF", "NULLIFE",
        "NEG", "WRAP", "TRUNC",
        "UPPER", "RTRIM", "TRIM", "LEFT", "SUBSTR",
        "LEN", "CAT", "YEAR", "MONTH", "DAY", "DOW",
        "DATEADD", "DATEDIFF"
    }:
        writes.add(args[0])

        for operand in args[1:]:
            add_read(operand)

    elif op == "SORT":
        writes.add(args[0])

        for key in args[1:]:
            add_sort_key(key)

    elif op == "TOPK":
        writes.add(args[0])

        for key in args[2:]:
            add_sort_key(key)

    elif op in {"NLJOIN", "HJOIN"}:
        writes.add(args[0])
        writes.add(args[1])
        add_read(args[2])
        add_read(args[3])

    elif op == "GROUP":
        writes.add(args[0])

        for key in args[1:]:
            add_read(key)

    elif op == "GALL":
        writes.add(args[0])
        add_read(args[1])

    elif op in {
        "GID", "GFIRST", "GCOUNT"
    }:
        writes.add(args[0])
        add_read(args[1])

    elif op in {
        "GCOUNTV", "GSUM", "GMIN", "GMAX"
    }:
        writes.add(args[0])
        add_read(args[1])
        add_read(args[2])

    elif op == "OUT":
        for operand in args:
            add_read(operand)

    else:
        # Unknown instructions must never be removed.
        return set(), set(), False

    return reads, writes, True


def analyse_dependencies(instructions):
    """
    Analyse all instructions and return their dependencies.
    """

    results = []

    for instruction in instructions:

        reads, writes, supported = get_dependencies(
            instruction
        )

        results.append({
            "line_number": instruction.line_number,
            "opcode": instruction.opcode,
            "reads": sorted(reads),
            "writes": sorted(writes),
            "supported": supported
        })

    return results


def eliminate_dead_code(instructions):
    """
    Backward liveness analysis.

    Instructions whose outputs are never needed are removed.
    Unknown instructions  are preserved by returning the original program.
    """
    # If any instruction is unknown, avoid unsafe optimisation.
    for instruction in instructions:
        _, _, supported = get_dependencies(instruction)

        if not supported:
            return instructions
        
    live_registers = set()
    keep = [False] * len(instructions)

    for index in range(len(instructions) - 1, -1, -1):

        instruction = instructions[index]

        reads, writes, supported = get_dependencies(
            instruction
        )

        # Preserve instructions we cannot analyse safely.
        if not supported or not writes:
            keep[index] = True
            live_registers.update(reads)
            continue

        # An instruction is needed if any output is live.
        if writes.intersection(live_registers):

            keep[index] = True

            # Remove overwritten definitions, then add inputs.
            live_registers.difference_update(writes)
            live_registers.update(reads)

        else:
            # None of its outputs are required.
            keep[index] = False

    optimized = [
        instruction
        for index, instruction in enumerate(instructions)
        if keep[index]
    ]

    return optimized
