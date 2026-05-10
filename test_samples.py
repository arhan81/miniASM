"""
test_samples.py  -  Sample inputs to test MiniASM assembler
Run: python test_samples.py
"""

from miniasm_assembler import assemble

samples = {

    "Test 1: Basic LOAD and HALT": """\
DATA A, 5
LOAD R1, (A)
HALT
""",

    "Test 2: Addition (A + B -> RESULT)": """\
DATA A, 15
DATA B, 25
DATA RESULT, 0
LOAD  R1, (A)
LOAD  R2, (B)
ADD   R1, R2
STORE R1, (RESULT)
HALT
""",

    "Test 3: Subtraction (A - B -> RESULT)": """\
DATA A, 50
DATA B, 30
DATA RESULT, 0
LOAD  R1, (A)
LOAD  R2, (B)
SUB   R1, R2
STORE R1, (RESULT)
HALT
""",

    "Test 4: With labels": """\
DATA X, 100
DATA Y, 0
BEGIN: LOAD  R1, (X)
       STORE R1, (Y)
       HALT
""",

    "Test 5: ERROR - undefined symbol": """\
DATA A, 10
LOAD R1, (A)
STORE R1, (MISSING)
HALT
""",

    "Test 6: ERROR - duplicate label + unknown mnemonic": """\
DATA A, 1
DATA A, 2
MUL R1, R2
HALT
""",

}


def run_all():
    for name, source in samples.items():
        print(f"\n{'='*55}")
        print(f"  {name}")
        print('='*55)

        # print source
        for i, line in enumerate(source.strip().splitlines(), 1):
            print(f"  {i:>2}  {line}")

        sym_table, _, machine_code, errors = assemble(source)

        # symbol table
        print(f"\n  Symbol Table : {sym_table}")

        # machine code
        print(f"\n  {'Addr':>4}  Machine Code")
        print(f"  {'----':>4}  ------------")
        for addr, code, annotation in machine_code:
            print(f"  {addr:>4}  {code}  {annotation}")

        # errors
        if errors:
            print(f"\n  Errors:")
            for lineno, msg in errors:
                print(f"    [Line {lineno}] {msg}")
        else:
            print(f"\n  Status: Assembly successful, no errors.")


if __name__ == "__main__":
    run_all()
