        ;CARREGANDO VALORES

        DATA R0, 0xF9
        DATA R2, 0x01
        ST   R0,R2       
        DATA R0, 0xFA
        DATA R2, 0x02
        ST   R0,R2
        DATA R0, 0xFB
        DATA R2, 0x03
        ST   R0,R2
        DATA R0, 0xFC
        DATA R2, 0x04
        ST   R0,R2
        DATA R0, 0xFD
        DATA R2, 0x05
        ST   R0,R2      
        DATA R0, 0xFE
        DATA R2, 0x06
        ST   R0,R2       
        DATA R0, 0xFF
        DATA R2, 0x07
        ST   R0,R2
        DATA R0, 0xF9
        DATA R1, 0xFF 
LOOP:   LD   R0,R2
        LD   R1,R3
        CMP  R2,R3
        JAE  FIM   
        MOVE R2,R3
        ST   R0,R2
        ST   R1,R3
        DATA R2, 0x01
        ADD  R2,R0
        DATA R2, 0xFF
        ADD  R2,R1
        JMP  0x27 
FIM:    HALT
