; Error Demo Program - triggers all 7 errors

; Error 1: Wrong number of DATA operands (only 1 operand)
DATA X

; Error 2: Non-integer DATA value
DATA Y, abc

; Error 3: Duplicate label (X already defined above... but since X failed, use a fresh one)
DATA Z, 10
DATA Z, 20

; Error 4: Unknown mnemonic
JUMP START

; Error 5: Wrong operand count (LOAD needs 2 operands, giving only 1)
LOAD R1

; Error 6: First operand is not a register
DATA ADDR, 5
LOAD ADDR, (Z)

; Error 7: Undefined symbol (GHOST was never declared)
STORE R1, (GHOST)

HALT
