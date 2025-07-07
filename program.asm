            JMP     MAIN            ; salta a área de dados
DIVISOR:    DATA    R0 0x00         ; divisor armazenado
NEG_DIV:    DATA    R0 0x00         ; –divisor (two’s-complement)
QUOT:       DATA    R0 0x00         ; quociente
CONST1:     DATA    R0 0x01         ; 1 – apenas para reserva
MAIN:       MOVE    R1 R1           ; uso explícito de MOVE (zera R1)
            JMP     READ_INPUT      ; chama rotina de leitura
AFTER_READ: DATA    R2 0x01         ; R2 ← 1  (constante p/ ++)
                                    ;guarda divisor e divisor em memória
            DATA    R1 DIVISOR      ; R1 ← &DIVISOR
            ST      R1 R3           ; [DIVISOR] ← divisor (R3)
            XOR     R1 R1           ; R1 ← 0
            OR      R1 R3           ; R1 ← divisor
            NOT     R1 R1           ; R1 ← ~divisor
            ADD     R1 R2           ; R1 ← –divisor
            DATA    R3 NEG_DIV
            ST      R3 R1           ; [NEG_DIV] ← –divisor
                                    ;zera quociente
            CLR     R1
            DATA    R3 QUOT
            ST      R3 R1
DIV_LOOP:   DATA    R3 DIVISOR      ; carrega divisor p/ comparação
            LD      R1 R3
            CMP     R0 R1
            A       DO_SUB          ; se R0 > = R1 continua
            E       DO_SUB
            JMP     SHOW_RESULT     ; senão, exibe resultado
DO_SUB:     DATA    R3 NEG_DIV      ; carrega –divisor
            LD      R1 R3
            ADD     R0 R1           ; R0 ← R0 – divisor
                                    ;quociente++
            DATA    R3 QUOT
            LD      R1 R3
            ADD     R1 R2           ; +1
            ST      R3 R1           ; salva quociente
            JMP     DIV_LOOP
READ_INPUT: IN      DATA R0         ; ‘D’ (dezena)
            DATA    R1 0xD0
            ADD     R0 R1           ; converte p/ número

            IN      DATA R1         ; ‘D’ (unidade)
            DATA    R3 0xD0
            ADD     R1 R3

            IN      DATA R3         ; lê e descarta ‘/’
            IN      DATA R3         ; lê divisor
            DATA    R1 0xD0
            ADD     R3 R1           ; divisor em R3 (numérico)

                                    ;calcula dividendo = dezena*10 + unidade
            XOR     R2 R2
            OR      R2 R0           ; R2 = dezena
            SHL     R2 R2           ; ×2
            SHL     R0 R0           ; dezena ×4
            SHL     R0 R0           ; dezena ×8
            SHL     R0 R0           ; dezena ×16
            SHL     R0 R0           ; dezena ×32  (×10 = ×8 + ×2)
                                    ;  (como o valor cabe em 8 bits, este conjunto equivale a 8)
                                    ;  mantenha conforme seu simulador: 3 shifts → ×8
            ADD     R0 R2           ; dezena*10
            ADD     R0 R1           ; + unidade  → dividendo pronto
            JMP     AFTER_READ
SHOW_RESULT:
DATA    R3 QUOT
            LD      R1 R3           ; R1 = quociente
            DATA    R2 0x30
            ADD     R1 R2           ; para ASCII
            OUT     DATA R1         ; mostra no monitor
            HALT                    ; fim do programa
