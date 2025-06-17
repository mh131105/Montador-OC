; vector_swap.asm - reverse a 7-element vector in place
; The vector occupies memory addresses 0xF9..0xFF (249..255).
; Program written for the assembler in this repository.

; ---------- Stage 1: initialize vector ----------

DATA R0 0xF9       ; start address
DATA R1 1
ST R0 R1           ; element 1 -> [0xF9]

DATA R1 2
DATA R2 1
ADD R0 R2          ; address 0xFA
ST R0 R1

DATA R1 3
ADD R0 R2          ; address 0xFB
ST R0 R1

DATA R1 4
ADD R0 R2          ; address 0xFC
ST R0 R1

DATA R1 5
ADD R0 R2          ; address 0xFD
ST R0 R1

DATA R1 6
ADD R0 R2          ; address 0xFE
ST R0 R1

DATA R1 7
ADD R0 R2          ; address 0xFF
ST R0 R1

; ---------- Stage 2: reverse vector ----------

DATA R0 0xF9       ; reset start pointer
DATA R1 0xFF       ; reset end pointer

; swap first and last
LD R2 R0
LD R3 R1
ST R0 R3
ST R1 R2
DATA R2 1
ADD R0 R2
DATA R2 -1
ADD R1 R2

; swap second and second-last
LD R2 R0
LD R3 R1
ST R0 R3
ST R1 R2
DATA R2 1
ADD R0 R2
DATA R2 -1
ADD R1 R2

; swap third and third-last
LD R2 R0
LD R3 R1
ST R0 R3
ST R1 R2

; End: loop forever
JMP 0x00
