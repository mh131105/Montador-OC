# Montador OC

Este projeto contém um montador simples escrito em Python para a CPU descrita no livro **"But How Do It Know?: The Basic Principles of Computers for Everyone"** de J. Clark Scott.

![image](https://github.com/user-attachments/assets/2525d152-0dbe-43c1-af7a-a94bce82ac07)


O script `montador.py` converte um arquivo assembly em um arquivo `program.txt` no formato `v3.0 hex words plain` (usado em ferramentas como o Logisim para inicializar memória). Por padrão ele procura `program.asm`, mas é possível indicar qualquer arquivo de entrada pela linha de comando.

O montador faz duas passagens para resolver rótulos e inclui pseudo instruções como `HALT`, `MOVE` e `CLR` para facilitar a escrita de programas.

## Como usar

1. Crie um arquivo `program.asm` (ou outro nome de sua escolha) contendo o programa em assembly. Cada instrução pode ser separada por espaços ou vírgulas e os comentários começam com `;`.
2. Execute o montador indicando o arquivo de entrada e opcionalmente o de saída:

```bash
python3 montador.py seu_programa.asm -o resultado.txt
```

Se nenhum arquivo for informado, o montador usa `program.asm` e gera `program.txt`.

Endereços informados em decimal devem estar no intervalo de -128 a 255. Valores fora desse
intervalo resultarão em erro de conversão.

Antes de executar, é possível compilar os arquivos Python para verificar
erros de sintaxe utilizando `py_compile`:

```bash
python3 -m py_compile arquivo1.py montador.py
```

Em seguida rode o montador normalmente:

```bash
python3 montador.py seu_programa.asm -o resultado.txt
```

## Conjunto de Instruções

O montador reconhece as seguintes instruções (todas em letras maiúsculas):

- `LD RD RS`   – Carrega o conteúdo de `RS` em `RD`.
- `ST RD RS`   – Armazena o conteúdo de `RS` no endereço apontado por `RD`.
- `DATA RX VALOR` – Coloca o valor imediato após a instrução. Útil para definir constantes.
- `JMPR RX`    – Salta para o endereço contido em `RX`.
- `JMP END`    – Salto incondicional para `END`.
- `IN/OUT TIPO RX` – Operações de entrada/saída. `TIPO` pode ser `DATA` ou `ADDR`.
- `ADD`, `SHR`, `SHL`, `NOT`, `AND`, `OR`, `XOR`, `CMP` – Operações aritméticas ou lógicas entre registradores.
- `CLF`        – Limpa os registradores de flags.
- `HALT [END]` – Salta para `END` ou encerra caso nenhum endereço seja informado.
- `MOVE RD RS` – Copia o conteúdo de `RS` para `RD`.
- `CLR RX`     – Zera o registrador especificado.
- Saltos condicionais podem ser formados pelas letras `C`, `A`, `E` e/ou `Z` seguidas do endereço (por exemplo `JCZ 0x10`).

Cada instrução é convertida para um ou dois bytes de acordo com o formato definido no processador do livro.

O montador executa duas passagens para resolver rótulos. Qualquer palavra seguida de `:` define um rótulo que pode ser usado como destino de saltos ou no `HALT`.

## Exemplo simples

```
LD R0 R1      ; carrega R1 em R0
ADD R0 R2     ; soma R2 em R0
DATA R3 5     ; define o valor 5 logo apos
```

Executando `python3 montador.py` com o código acima gera `program.txt` contendo:

```
v3.0 hex words plain
01
82
23
05
```

O restante da memória é preenchido com `00`.

## Licença

Este projeto foi disponibilizado sem um arquivo de licença explícito. Consulte o autor original para mais informações.
