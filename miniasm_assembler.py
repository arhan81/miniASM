"""
MiniASM Two-Pass Assembler

"""

import re

# ── Opcode table ──────────────────────────────────────────────────────────────
OPCODES = {
    "LOAD":  {"code": 0x01, "operands": 2},   # LOAD  Rx, (label)
    "STORE": {"code": 0x02, "operands": 2},   # STORE Rx, (label)
    "ADD":   {"code": 0x03, "operands": 2},   # ADD   Rx, Ry
    "SUB":   {"code": 0x04, "operands": 2},   # SUB   Rx, Ry
    "HALT":  {"code": 0xFF, "operands": 0},   # HALT
}

REGISTER_RE = re.compile(r'^R[0-9]$', re.IGNORECASE)
MEM_REF_RE = re.compile(r'^\((\w+)\)$')       # (label)
LABEL_DEF = re.compile(r'^([A-Za-z_]\w*):$')  # LABEL:


def _parse_line(raw: str):
    """Strip comments, return (label_def | None, tokens[])."""
    line = raw.split(';')[0].strip()
    if not line:
        return None, []

    # Replace commas with spaces for uniform splitting
    line = line.replace(',', ' ')
    tokens = line.split()

    label = None
    if tokens and LABEL_DEF.match(tokens[0]):
        label = tokens[0].rstrip(':').upper()
        tokens = tokens[1:]

    return label, [t.upper() for t in tokens]


# ── Pass 1 ────────────────────────────────────────────────────────────────────
def pass1(source_lines: list[str]):
    """
    Build Symbol Table and intermediate representation.
    Returns (symbol_table, intermediate, errors)
      intermediate: list of (line_no, address, label, tokens)
    """
    symbol_table = {}
    intermediate = []
    errors = []
    lc = 0   # location counter (word address)

    for lineno, raw in enumerate(source_lines, 1):
        label, tokens = _parse_line(raw)

        if not tokens:
            continue  # blank / comment-only line

        mnemonic = tokens[0]

        # ── DATA statement ────────────────────────────────────────────────
        if mnemonic == "DATA":
            if len(tokens) != 3:
                errors.append(
                    (lineno, "DATA requires exactly 2 operands: DATA <label>, <value>"))
                continue
            data_label = tokens[1]
            try:
                int(tokens[2])
            except ValueError:
                errors.append(
                    (lineno, f"DATA value must be an integer, got '{tokens[2]}'"))
                continue
            if data_label in symbol_table:
                errors.append((lineno, f"Duplicate label '{data_label}'"))
                continue
            symbol_table[data_label] = lc
            intermediate.append((lineno, lc, data_label, tokens))
            lc += 1

        # ── Executable statement ──────────────────────────────────────────
        elif mnemonic in OPCODES:
            if label:
                if label in symbol_table:
                    errors.append((lineno, f"Duplicate label '{label}'"))
                else:
                    symbol_table[label] = lc
            expected = OPCODES[mnemonic]["operands"]
            actual = len(tokens) - 1
            if actual != expected:
                errors.append(
                    (lineno, f"'{mnemonic}' expects {expected} operand(s), got {actual}"))
                continue
            intermediate.append((lineno, lc, label, tokens))
            lc += 1

        else:
            errors.append((lineno, f"Unknown mnemonic '{mnemonic}'"))

    return symbol_table, intermediate, errors


# ── Pass 2 ────────────────────────────────────────────────────────────────────
def pass2(intermediate: list, symbol_table: dict):
    """
    Resolve symbols, generate machine code.
    Returns (machine_code, errors)
      machine_code: list of (address, hex_string, annotation)
    """
    machine_code = []
    errors = []

    for lineno, addr, label, tokens in intermediate:
        mnemonic = tokens[0]

        if mnemonic == "DATA":
            value = int(tokens[2])
            machine_code.append(
                (addr, f"DAT {value:04X}", f"; {tokens[1]} = {value}"))
            continue

        opcode = OPCODES[mnemonic]["code"]

        if mnemonic == "HALT":
            machine_code.append((addr, f"{opcode:02X} 00 00", "; HALT"))
            continue

        op1, op2 = tokens[1], tokens[2]

        # Validate first operand (always a register for our ISA)
        if not REGISTER_RE.match(op1):
            errors.append(
                (lineno, f"Expected register as first operand, got '{op1}'"))
            continue

        reg1 = int(op1[1])

        # Resolve second operand
        mem_match = MEM_REF_RE.match(op2)
        if mem_match:                          # memory reference (label)
            sym = mem_match.group(1).upper()
            if sym not in symbol_table:
                errors.append((lineno, f"Undefined symbol '{sym}'"))
                continue
            operand2 = symbol_table[sym]
            machine_code.append((addr, f"{opcode:02X} {reg1:02X} {operand2:04X}",
                                 f"; {mnemonic} R{reg1}, ({sym}) -> addr {operand2}"))
        elif REGISTER_RE.match(op2):           # register-to-register
            reg2 = int(op2[1])
            machine_code.append((addr, f"{opcode:02X} {reg1:02X} {reg2:04X}",
                                 f"; {mnemonic} R{reg1}, R{reg2}"))
        else:
            errors.append(
                (lineno, f"Invalid second operand '{op2}': expected register or (label)"))

    return machine_code, errors


# ── Public API ────────────────────────────────────────────────────────────────
def assemble(source: str):
    lines = source.splitlines()
    sym_table, intermediate, p1_errors = pass1(lines)
    machine_code, p2_errors = pass2(intermediate, sym_table)
    return sym_table, intermediate, machine_code, p1_errors + p2_errors
