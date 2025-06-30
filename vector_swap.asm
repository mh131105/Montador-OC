jc fim

loop: add r1,r2

         shl r2,r2

         jmp loop

fim:  halt
ADD R1 R2         ; fim--
JMP 0x18          ; repete o loop

JMP 0x27          ; loop infinito (halt)
