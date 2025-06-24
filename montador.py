import argparse  # trata argumentos via linha de comando

memory = 256*["00"]  # memoria inicial preenchida com zeros

intruções = {  # codificação de registradores e instruções
            "R0" : "00",
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

jcaez = {  # bits das flags para saltos condicionais
        "C" : 0b1000,
        "A" : 0b0100,
        "E" : 0b0010,
        "Z" : 0b0001
       }

InOut = {"DATA" : "0", "ADDR" : "1"}  # tipo de operacao para IN/OUT

def hexa(bin_str):  # converte string binaria em byte hexadecimal
    if bin_str.lower().startswith("0b"):
        bin_str = bin_str[2:]
    value = int(bin_str, 2)
    return f"{value:02x}"[-2:]

def bin(n, width: int = 4, twos_complement: bool = False):  # formata numero em binario
    if twos_complement:
        n &= (1 << width) - 1
    return "0b" + format(n, f"0{width}b")

def decBin(n):  # decimal para binario de 8 bits validando intervalo
    n = int(n)
    if n < -128 or n > 255:
        raise ValueError("Valor decimal fora do intervalo permitido [-128, 255]")
    return "0b" + format(n & 0xFF, "08b")

def normalizaNumero (s):  # transforma decimal/binario/hex em byte hexadecimal
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

def removeListasVazias(list_of_lists: list[list]) -> list[list]:  # elimina sublistas vazias
    return [sub for sub in list_of_lists if sub]


def instr_size(tokens: list[str]) -> int:
    """Retorna o numero de bytes que a instrucao ou pseudo-instrucao gera."""
    op = tokens[0]
    if op == "DATA" or op == "JMP" or op.startswith("J") and len(op) > 1 and op != "JMPR":
        return 2
    if op == "HALT":
        return 2
    if op == "MOVE":
        return 3
    if op == "CLR":
        return 1
    return 1


def parse_labels(programa_asm: list[list[str]]):
    """Remove rotulos do codigo e retorna tabela de labels e instrucoes."""
    labels = {}
    cleaned = []
    mem = 0
    for line in programa_asm:
        tokens = line[:]
        while tokens and tokens[0].endswith(":"):
            label = tokens.pop(0)[:-1]
            labels[label] = mem
        if not tokens:
            continue
        cleaned.append(tokens)
        mem += instr_size(tokens)
    return cleaned, labels


def ler_arquivo_asm(arquivo):  # carrega e tokeniza o arquivo asm
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

def conversao(programa_asm):  # gera codigo de maquina na memoria
    programa, labels = parse_labels(programa_asm)
    tam = len(programa)
    mem = 0
    i = 0
    while i < tam:
        op = programa[i][0]
        if op == "HALT":
            inst = "0b" + intruções["JMP"]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            inst = normalizaNumero(str(mem - 1))
            memory[mem] = inst
            mem += 1
            i += 1
            continue
        elif op == "MOVE":
            ra, rb = programa[i][1], programa[i][2]
            seq = [(ra, rb), (rb, ra), (ra, rb)]
            for a, b in seq:
                inst = "0b" + intruções["XOR"] + intruções[a] + intruções[b]
                inst = normalizaNumero(inst)
                memory[mem] = inst
                mem += 1
            i += 1
            continue
        elif op == "CLR":
            ra = programa[i][1]
            inst = "0b" + intruções["XOR"] + intruções[ra] + intruções[ra]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            i += 1
            continue
        if op == "LD":  # operacao de carga
            inst = "0b" + intruções[op] + intruções[programa[i][1]] + intruções[programa[i][2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "ST":  # operacao de armazenamento
            inst = "0b" + intruções[op] + intruções[programa[i][1]] + intruções[programa[i][2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "DATA":  # diretiva para dado imediato
            inst = "0b" + intruções[op] + "00" + intruções[programa[i][1]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            operand = programa[i][2]
            if operand in labels:
                operand = str(labels[operand])
            inst = normalizaNumero(operand)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "JMPR":  # salto para registrador
            inst = "0b" + intruções[op] + "00" + intruções[programa[i][1]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            i += 1
        elif op == "JMP":  # salto absoluto
            inst = "0b" + intruções[op]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            operand = programa[i][1]
            if operand in labels:
                operand = str(labels[operand])
            inst = normalizaNumero(operand)
            memory[mem] = inst
            mem += 1
            i += 1
        elif op == "IN":  # instrucao de entrada
            inst = "0b" + intruções[op] + "0" + InOut[programa[i][1]] + intruções[programa[i][2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            i += 1
        elif op == "OUT":  # instrucao de saida
            inst = "0b" + intruções[op] + "1" + InOut[programa[i][1]] + intruções[programa[i][2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            i += 1
        elif op == "ADD":  # soma registradores
            inst = "0b" + intruções[op] + intruções[programa[i][1]] + intruções[programa[i][2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "SHR":  # desloca bits para direita
            inst = "0b" + intruções[op] + intruções[programa[i][1]] + intruções[programa[i][2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "SHL":  # desloca bits para esquerda
            inst = "0b" + intruções[op] + intruções[programa[i][1]] + intruções[programa[i][2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "NOT":  # inverte bits
            inst = "0b" + intruções[op] + intruções[programa[i][1]] + intruções[programa[i][2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "AND":  # operacao logica AND
            inst = "0b" + intruções[op] + intruções[programa[i][1]] + intruções[programa[i][2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "OR":  # operacao logica OR
            inst = "0b" + intruções[op] + intruções[programa[i][1]] + intruções[programa[i][2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "XOR":  # operacao logica XOR
            inst = "0b" + intruções[op] + intruções[programa[i][1]] + intruções[programa[i][2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "CMP":  # compara registradores
            inst = "0b" + intruções[op] + intruções[programa[i][1]] + intruções[programa[i][2]]
            inst = normalizaNumero(inst)
            memory[mem] = inst
            i += 1
            mem += 1
        elif op == "CLF":  # limpa flags
            memory[mem] = "60"
            mem += 1
            i += 1
        else:  # saltos condicionais
            caez = 0b0000
            f = programa[i][0]
            for ch in f:
                if ch in jcaez:
                    caez += jcaez[ch]
            caez = bin(caez)
            inst = "0b" + "0101" + str(caez[2:])
            inst = normalizaNumero(inst)
            memory[mem] = inst
            mem += 1
            operand = programa[i][1]
            if operand in labels:
                operand = str(labels[operand])
            inst = normalizaNumero(operand)
            memory[mem] = inst
            mem += 1
            i += 1
                
    return

def escrever_saida(arquivo):
    # grava o conteudo da memoria no arquivo
    with open(arquivo, "w") as f:
        f.write("v3.0 hex words plain\n")
        for codigo in memory:
            f.write(codigo)
            f.write("\n")

def montador(argv=None):
    # ponto de entrada: processa argumentos e executa montagem
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
        conversao(programa_asm)
    except ValueError as e:
        print(f"Erro: {e}")
        return
    escrever_saida(args.output)
    

if __name__ == "__main__":
    montador()
