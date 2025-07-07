import argparse

# Autor: Matheus Henrique de Oliveira Garcia 22450747

# Memoria com 256 bytes em texto hexadecimal
memory = 256*["00"]

# Mapeamento de registradores e opcodes
intruções = {"R0" : "00",
             "R1" : "01",
             "R2" : "10",
             "R3" : "11",
             "LD" : "0000",
             "ST" : "0001",
             "DATA" : "0010",
             "IN"  : "0111",
             "OUT" : "0111",
             "JMPR" : "0011",
             "JMP" : "01000000",
             "CLF" : "0110",
             "ADD" : "1000",
             "SHR" : "1001",
             "SHL" : "1010",
             "NOT" : "1011",
             "AND" : "1100",
             "OR" : "1101",
             "XOR" : "1110",
            "CMP" : "1111"
           }

# Mascara para saltos condicionais
jcaez = {"C" : 0b1000,
         "A" : 0b0100,
         "E" : 0b0010,
         "Z" : 0b0001
        }

# Parametros das instrucoes de I/O
InOut = {"DATA" : "0",
         "ADDR" : "1"
}
# Converte binario para dois digitos hexadecimais
def hexa(bin_str):
    if bin_str.lower().startswith("0b"):
        bin_str = bin_str[2:]
    value = int(bin_str, 2)
    return f"{value:02x}"[-2:]
# Retorna binario com largura definida
def bin(n, width: int = 4, twos_complement: bool = False):
    if twos_complement:
        n &= (1 << width) - 1
    return "0b" + format(n, f"0{width}b")
# Decimal para binario de 8 bits
def decBin(n):
    n = int(n)
    if n < -128 or n > 255:
        raise ValueError("Valor decimal fora do intervalo permitido [-128, 255]")
    return "0b" + format(n & 0xFF, "08b")
# Padroniza numeros em hexadecimal
def normalizaNumero (s):
    if (s[0] == "-"):
        s = decBin(s)
        s = hexa(s)
        return s
    if (len(s) > 1) and ((s[1] == "b") or (s[1] == "B")):
        s = hexa(s)
        return s
    if (len(s) > 1) and ((s[1] == "x") or (s[1] == "X")):
        return s[2:]
    else:
        s = decBin(s)
        s = hexa(s)
        return s

# Elimina sublistas vazias
def removeListasVazias(list_of_lists: list[list]) -> list[list]:
    return [sub for sub in list_of_lists if sub]


# Retorna verdadeiro para strings numericas
def is_numero(s: str) -> bool:
    try:
        int(s, 0)
        return True
    except ValueError:
        return False


# Calcula o tamanho da instrucao em bytes
def tamanho_instrucao(tokens: list[str]) -> int:
    if not tokens:
        return 0
    op = tokens[0]
    if op in {"LD", "ST", "JMPR", "ADD", "SHR", "SHL", "NOT", "AND", "OR", "XOR", "CMP", "IN", "OUT", "CLF"}:
        return 1
    if op in {"DATA", "JMP"}:
        return 2
    if op.startswith("J"):
        return 2
    if op == "HALT":
        return 2
    if op == "MOVE":
        # MOVE é considerado uma instrução única
        return 1
    if op == "CLR":
        # CLR gera apenas um XOR registrador consigo mesmo
        return 1
    return 1


# Le o codigo assembly e remove comentarios
def ler_arquivo_asm(arquivo):
    try:
        with open(arquivo, "r") as f:
            content = f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Arquivo '{arquivo}' não encontrado.") from e
    programa_asm = content.upper().split("\n")
    for i in range(len(programa_asm)):
        programa_asm[i] = programa_asm[i].rstrip("\n").split(";", 1)[0].strip()
        programa_asm[i] = programa_asm[i].replace(","," ")
        programa_asm[i] = programa_asm[i].split()
    programa_asm = list(filter(bool, programa_asm))
    return programa_asm


# Calcula enderecos e registra labels
def primeira_passagem(programa: list[list[str]]):
    pc = 0
    labels: dict[str, int] = {}
    for linha in programa:
        tokens = linha
        if tokens[0].endswith(":"):
            rotulo = tokens[0][:-1]
            if rotulo in intruções:
                raise ValueError(f"nome de label invalido: {rotulo}")
            if rotulo in labels:
                raise ValueError("label duplicada")
            labels[rotulo] = pc
            tokens = tokens[1:]
            if not tokens:
                continue
        pc += tamanho_instrucao(tokens)
        if pc > 255:
            raise ValueError("programa excede 256 bytes")
    return pc, labels

# Transforma cada instrucao em codigo de maquina
def conversao(programa_asm, labels: dict[str, int]):
    tam = len(programa_asm)
    mem = 0
    i = 0
    while i < tam:
        tokens = programa_asm[i]
        if tokens[0].endswith(":"):
            tokens = tokens[1:]
            if not tokens:
                i += 1
                continue
        op = tokens[0]
        if op == "LD":
            inst = "0b" + intruções[op] + intruções[tokens[1]] + intruções[tokens[2]]   
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "ST":
            inst = "0b" + intruções[op] + intruções[tokens[1]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "DATA":
            inst = "0b" + intruções[op] + "00" + intruções[tokens[1]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            inst = tokens[2]
            if not is_numero(inst):
                if inst not in labels:
                    raise ValueError("label indefinida")
                inst = str(labels[inst])
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "JMPR":
            inst = "0b" + intruções[op] + "00" + intruções[tokens[1]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            i += 1
        elif op == "JMP":
            inst = "0b" + intruções[op]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            inst = tokens[1]
            if not is_numero(inst):
                if inst not in labels:
                    raise ValueError("label indefinida")
                inst = str(labels[inst])
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            i += 1
        elif op == "IN":
            inst = "0b" + intruções[op] + "0" + InOut[tokens[1]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            i += 1
        elif op == "OUT":
            inst = "0b" + intruções[op] + "1" + InOut[tokens[1]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            i += 1
        elif op == "ADD":
            inst = "0b" + intruções[op] + intruções[tokens[1]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "SHR":
            inst = "0b" + intruções[op] + intruções[tokens[1]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "SHL":
            inst = "0b" + intruções[op] + intruções[tokens[1]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "NOT":
            inst = "0b" + intruções[op] + intruções[tokens[1]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "AND":
            inst = "0b" + intruções[op] + intruções[tokens[1]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "OR":
            inst = "0b" + intruções[op] + intruções[tokens[1]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "XOR":
            inst = "0b" + intruções[op] + intruções[tokens[1]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "CMP":
            inst = "0b" + intruções[op] + intruções[tokens[1]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "CLF":
            memory[mem] = "60"
            mem += 1
            i += 1
        elif op == "HALT":
            op = "JMP"
            inst = "0b" + intruções[op]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            if len(tokens) > 1:
                inst = tokens[1]
                if not is_numero(inst):
                    if inst not in labels:
                        raise ValueError("label indefinida")
                    inst = str(labels[inst])
            else:
                # utilizado no HALT e o byte anterior ao opcode.
                inst = str(mem - 2)
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            i += 1
        elif op == "MOVE":
            op = "XOR"
            inst = "0b" + intruções[op] + intruções[tokens[2]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            op = "OR"
            inst = "0b" + intruções[op] + intruções[tokens[1]] + intruções[tokens[2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            i+=1
        elif op == "CLR":
            op = "XOR"
            inst = "0b" + intruções[op] + intruções[tokens[1]] + intruções[tokens[1]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        else:
            caez = 0b0000
            f = tokens[0]
            for ch in f:
                if ch in jcaez:
                    caez += jcaez[ch]
            caez = bin(caez)
            inst = "0b" + "0101" + str(caez[2:])
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            inst = tokens[1]
            if not is_numero(inst):
                if inst not in labels:
                    raise ValueError("label indefinida")
                inst = str(labels[inst])
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            i += 1
                
    return

# Grava o arquivo
def escrever_saida(arquivo):
    with open(arquivo, "w") as f:
        f.write("v3.0 hex words plain\n")
        # grava apenas ate o ultimo endereco utilizado
        fim = 0
        for i, codigo in enumerate(memory):
            if codigo != "00":
                fim = i + 1
        for codigo in memory[:fim]:
            f.write(codigo.lower())
            f.write("\n")

# Processa argumentos e executa as etapas de montagem
def montador(argv=None):
    parser = argparse.ArgumentParser(description="Montador OC")
    parser.add_argument(
        "source",
        nargs="?",
        default="program.asm",
        help="Arquivo de entrada em assembly",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="program.txt",
        help="Arquivo de saída gerado",
    )
    args = parser.parse_args(argv)

    try:
        programa_asm = ler_arquivo_asm(args.source)
    except FileNotFoundError as e:
        print(e)
        return

    try:
        _, labels = primeira_passagem(programa_asm)
        global memory
        memory = 256*["00"]
        conversao(programa_asm, labels)
    except ValueError as e:
        print(f"Erro: {e}")
        return
    escrever_saida(args.output)
    

# Execucao direta
if __name__ == "__main__":
    montador()    

# Execucao direta
if __name__ == "__main__":
    montador()
