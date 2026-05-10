; -------------------------------------------------------
;  MiniASM Sample Program
;  Computes: result = x + y - z
; -------------------------------------------------------

; -- Data Section ----------------------------------------
DATA X, 10          ; declare variable X = 10
DATA Y, 20          ; declare variable Y = 20
DATA Z, 5           ; declare variable Z = 5
DATA RESULT, 0      ; declare variable RESULT = 0

; -- Code Section ----------------------------------------
START:  LOAD  R1, (X)       ; R1 = X
        LOAD  R2, (Y)       ; R2 = Y
        ADD   R1, R2        ; R1 = R1 + R2  (X + Y)
        LOAD  R3, (Z)       ; R3 = Z
        SUB   R1, R3        ; R1 = R1 - R3  (X + Y - Z)
        STORE R1, (RESULT)  ; RESULT = R1
        HALT                ; stop execution

; -- Intentional Errors (commented out -- uncomment to test) --
; DATA X, 10          ; ERROR: duplicate label X
; LOAD R1             ; ERROR: missing second operand
; ADD  R1, (X)        ; ERROR: (X) is not a register for ADD
; STORE R9, (GHOST)   ; ERROR: undefined symbol GHOST
; JUMP START          ; ERROR: unknown mnemonic JUMP
