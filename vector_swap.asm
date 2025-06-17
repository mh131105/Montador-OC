; vector_swap.asm - initialize and reverse a 7-element vector in place
; The vector uses the last seven memory addresses (0xF9..0xFF).
; Program assembled with montador.py

; ----- Stage 1: write numbers 1..7 starting from 0xFF -----

DATA R0 0xFF      ; pointer to last address
DATA R1 1         ; current value
ST R0 R1          ; [0xFF] = 1
DATA R2 -1        ; decrement step
ADD R0 R2         ; -> 0xFE

DATA R1 2
ST R0 R1          ; [0xFE] = 2
ADD R0 R2         ; -> 0xFD

DATA R1 3
ST R0 R1          ; [0xFD] = 3
ADD R0 R2         ; -> 0xFC

DATA R1 4
ST R0 R1          ; [0xFC] = 4
ADD R0 R2         ; -> 0xFB

DATA R1 5
ST R0 R1          ; [0xFB] = 5
ADD R0 R2         ; -> 0xFA

DATA R1 6
ST R0 R1          ; [0xFA] = 6
ADD R0 R2         ; -> 0xF9

DATA R1 7
ST R0 R1          ; [0xF9] = 7

; ----- Stage 2: reverse vector using a loop -----

DATA R0 0xF9      ; start pointer
DATA R1 0xFF      ; end pointer
CMP R0 R1         ; compare pointers
JAE 0x32           ; stop when start >= end

LD R2 R0          ; value at start
LD R3 R1          ; value at end
ST R0 R3
ST R1 R2

DATA R2 1
ADD R0 R2         ; start++
DATA R2 -1
ADD R1 R2         ; end--
JMP 0x23

JMP 0x00          ; halt (infinite loop)
