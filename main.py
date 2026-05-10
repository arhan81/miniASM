"""
main.py  

"""

from miniasm_assembler import assemble

DIVIDER = "-" * 60


def print_section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('=' * 60)


def run(source_path: str):
    with open(source_path) as f:
        source = f.read()

    print("\n" + DIVIDER)
    print("  MiniASM Assembler  -  Two-Pass Demo")
    print(DIVIDER)
    print("\n[Source Program]\n")
    for i, line in enumerate(source.splitlines(), 1):
        print(f"  {i:>3}  {line}")

    sym_table, intermediate, machine_code, errors = assemble(source)

    # ── Symbol Table ──────────────────────────────────────────────────────
    print_section("PASS 1 — Symbol Table")
    print(f"  {'Symbol':<12} {'Address':>8}")
    print(f"  {'-'*12} {'-'*8}")
    for sym, addr in sym_table.items():
        print(f"  {sym:<12} {addr:>8}")

    # ── Intermediate Representation ───────────────────────────────────────
    print_section("PASS 1 — Intermediate Representation")
    print(f"  {'Line':>4}  {'Addr':>4}  {'Label':<10}  Tokens")
    print(f"  {'----':>4}  {'----':>4}  {'-----':<10}  ------")
    for lineno, addr, label, tokens in intermediate:
        lbl = label or ""
        print(f"  {lineno:>4}  {addr:>4}  {lbl:<10}  {tokens}")

    # ── Machine Code ──────────────────────────────────────────────────────
    print_section("PASS 2 — Generated Machine Code")
    print(f"  {'Addr':>4}  {'Machine Code':<18}  Annotation")
    print(f"  {'----':>4}  {'------------':<18}  ----------")
    for addr, code, annotation in machine_code:
        print(f"  {addr:>4}  {code:<18}  {annotation}")

    # ── Errors ────────────────────────────────────────────────────────────
    print_section("Error Report")
    if errors:
        for lineno, msg in errors:
            print(f"  [Line {lineno:>3}] ERROR: {msg}")
    else:
        print("  No errors found. Assembly successful.")

    print("\n" + DIVIDER + "\n")


# ── Error demo ────────────────────────────────────────────────────────────────
ERROR_DEMO = """\
DATA X, 10
DATA X, 20
LOAD R1
ADD  R1, (X)
STORE R9, (GHOST)
JUMP START
DATA BADVAL, abc
"""


def run_error_demo():
    print_section("ERROR DEMO — Intentional Bad Program")
    print("\n[Erroneous Source]\n")
    for i, line in enumerate(ERROR_DEMO.splitlines(), 1):
        print(f"  {i:>3}  {line}")

    _, _, _, errors = assemble(ERROR_DEMO)
    print("\n[Detected Errors]\n")
    if errors:
        for lineno, msg in errors:
            print(f"  [Line {lineno:>3}] ERROR: {msg}")
    else:
        print("  (none)")
    print()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run(sys.argv[1])          # python main.py yourfile.asm
    else:
        run("sample_program.asm")  # default
        run_error_demo()
