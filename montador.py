import argparse

memory = 256*["00"]

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

jcaez = {"C" : 0b1000,
         "A" : 0b0100,
         "E" : 0b0010,
         "Z" : 0b0001
        }

InOut = {"DATA" : "0",
         "ADDR" : "1"
}

def hexa(bin_str):
    if bin_str.lower().startswith("0b"):
        bin_str = bin_str[2:]
    value = int(bin_str, 2)
    return f"{value:02x}"[-2:]

def bin(n, width: int = 4, twos_complement: bool = False):
    if twos_complement:
        n &= (1 << width) - 1
    return "0b" + format(n, f"0{width}b")

def decBin(n):
    n = int(n)
    if n < -128 or n > 255:
        raise ValueError("Valor decimal fora do intervalo permitido [-128, 255]")
    return "0b" + format(n & 0xFF, "08b")

def normalizaNumero(s, line_index=None, programa=None):
    try:
        if s[0] == "-":
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
    except ValueError as e:
        if line_index is not None and programa is not None:
            line_text = " ".join(programa[line_index])
            raise ValueError(f"{e} na linha {line_index + 1}: {line_text}") from None
        raise

def removeListasVazias(list_of_lists: list[list]) -> list[list]:
    return [sub for sub in list_of_lists if sub]


def ler_arquivo_asm(arquivo):
    with open(arquivo, "r") as f:
        content = f.read()
    programa_asm = content.upper().split("\n")
    for i in range(len(programa_asm)):
        programa_asm[i] = programa_asm[i].rstrip("\n").split(";", 1)[0].strip()
        programa_asm[i] = programa_asm[i].replace(","," ")
        programa_asm[i] = programa_asm[i].split()
    programa_asm = list(filter(bool, programa_asm))
    return programa_asm

def conversao(programa_asm):
    tam = len(programa_asm)
    mem = 0
    i = 0
    while(i < tam):
        match programa_asm[i][0]:
            case("LD"):
                inst = "0b" + intruções[programa_asm[i][0]] + intruções[programa_asm[i][1]] + intruções[programa_asm[i][2]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                i += 1
                mem += 1
            case("ST"):
                inst = "0b" + intruções[programa_asm[i][0]] + intruções[programa_asm[i][1]] + intruções[programa_asm[i][2]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                i += 1
                mem += 1
            case("DATA"):
                inst = "0b" + intruções[programa_asm[i][0]] + "00" + intruções[programa_asm[i][1]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                mem += 1
                inst = programa_asm[i][2]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                i += 1 
                mem += 1
            case("JMPR"):
                inst = "0b" + intruções[programa_asm[i][0]] + "00" + intruções[programa_asm[i][1]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                mem += 1
                i += 1
            case("JMP"):
                inst = "0b" + intruções[programa_asm[i][0]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                mem += 1
                inst = programa_asm[i][1]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                mem += 1
                i += 1
            case("IN"):
                inst = "0b" + intruções[programa_asm[i][0]] + "0" + InOut[programa_asm[i][1]] + intruções[programa_asm[i][2]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                mem += 1
                i += 1
            case("OUT"):
                inst = "0b" + intruções[programa_asm[i][0]] + "1" + InOut[programa_asm[i][1]] + intruções[programa_asm[i][2]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                mem += 1
                i += 1
            case("ADD"):
                inst = "0b" + intruções[programa_asm[i][0]] + intruções[programa_asm[i][1]] + intruções[programa_asm[i][2]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                i += 1
                mem += 1
            case("SHR"):
                inst = "0b" + intruções[programa_asm[i][0]] + intruções[programa_asm[i][1]] + intruções[programa_asm[i][2]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                i += 1
                mem += 1
            case("SHL"):
                inst = "0b" + intruções[programa_asm[i][0]] + intruções[programa_asm[i][1]] + intruções[programa_asm[i][2]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                i += 1
                mem += 1
            case("NOT"):
                inst = "0b" + intruções[programa_asm[i][0]] + intruções[programa_asm[i][1]] + intruções[programa_asm[i][2]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                i += 1
                mem += 1
            case("AND"):
                inst = "0b" + intruções[programa_asm[i][0]] + intruções[programa_asm[i][1]] + intruções[programa_asm[i][2]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                i += 1
                mem += 1
            case("OR"):
                inst = "0b" + intruções[programa_asm[i][0]] + intruções[programa_asm[i][1]] + intruções[programa_asm[i][2]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                i += 1
                mem += 1
            case("XOR"):
                inst = "0b" + intruções[programa_asm[i][0]] + intruções[programa_asm[i][1]] + intruções[programa_asm[i][2]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                i += 1
                mem += 1
            case("CMP"):
                inst = "0b" + intruções[programa_asm[i][0]] + intruções[programa_asm[i][1]] + intruções[programa_asm[i][2]]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                i += 1
                mem += 1
            case("CLF"):
                memory[mem] = "60"
                mem +=1
                i += 1
            case (_):
                caez = 0b0000
                f = programa_asm[i][0]
                f = list(f)
                for j in range(len(f)):
                    match f[j]:
                        case("C"):
                            jcaez[f[j]]
                            caez = caez + jcaez[f[j]]
                        case("A"):
                            jcaez[f[j]]
                            caez = caez + jcaez[f[j]]
                        case("E"):
                            jcaez[f[j]]
                            caez = caez + jcaez[f[j]]
                        case("Z"):
                            caez = caez + jcaez[f[j]]
                caez = bin(caez)
                inst = "0b" + "0101" + str(caez[2:])
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                mem += 1
                inst = programa_asm[i][1]
                inst = normalizaNumero(inst, i, programa_asm)
                memory[mem] = inst
                mem += 1
                i += 1
                
    return

def escrever_saida(arquivo):
    with open(arquivo, "w") as f:
        f.write("v3.0 hex words plain\n")
        for codigo in memory:
            f.write(codigo)
            f.write("\n")

def montador(argv=None):
    """Executa o montador utilizando argumentos de linha de comando."""
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

    programa_asm = ler_arquivo_asm(args.source)
    try:
        conversao(programa_asm)
    except ValueError as e:
        print(f"Erro: {e}")
        return
    escrever_saida(args.output)
    

if __name__ == "__main__":
    montador()
