; vector_swap.asm - preenche os ultimos sete enderecos da memoria com a sequencia
; 7,6,5,4,3,2,1 e depois reverte a ordem in-place para 1,2,3,4,5,6,7.
; Montado com montador.py

; ----- Etapa 1: grava valores 1..7 a partir do fim -----
DATA R0 0xFF      ; ponteiro para o ultimo endereco
DATA R1 1         ; valor inicial
DATA R2 7         ; contador de elementos

ST R0 R1          ; [0xFF] = 1
DATA R3 -1
ADD R0 R3         ; ponteiro--
DATA R3 1
ADD R1 R3         ; proximo valor
DATA R3 -1
ADD R2 R3         ; contador--
JZ 0x14           ; se contador==0, fim da inicializacao
JMP 0x06          ; volta para ST R0 R1

; ----- Etapa 2: inverte elementos -----
DATA R0 0xF9      ; inicio do vetor
DATA R1 0xFF      ; fim do vetor

CMP R0 R1
JAE 0x27          ; sai quando inicio >= fim
LD R2 R0
LD R3 R1
ST R0 R3
ST R1 R2
DATA R2 1
ADD R0 R2         ; inicio++
DATA R2 -1
ADD R1 R2         ; fim--
JMP 0x18          ; repete o loop

JMP 0x27          ; loop infinito (halt)
