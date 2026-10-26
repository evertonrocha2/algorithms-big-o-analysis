"""
Exercicios 3 e 4 - Rastreio passo a passo da busca linear e da busca binaria.

Array: [2, 4, 6, 8, 10, 12, 13]  |  Alvo: 8
Serve para conferir a simulacao manual feita no papel.
"""

ARRAY = [2, 4, 6, 8, 10, 12, 13]
ALVO = 8


def busca_linear_rastreada(arr, alvo):
    comparacoes = 0
    for i, valor in enumerate(arr):
        comparacoes += 1
        achou = valor == alvo
        print(f"  Passo {comparacoes}: arr[{i}] = {valor:>2} == {alvo}? {'SIM' if achou else 'nao'}")
        if achou:
            return i, comparacoes
    return -1, comparacoes


def busca_binaria_rastreada(arr, alvo):
    """Conta 1 comparacao por teste de igualdade e 1 pelo teste de menor (mesmo modelo do Ex. 14)."""
    inicio, fim = 0, len(arr) - 1
    comparacoes = 0
    passo = 0
    while inicio <= fim:
        passo += 1
        meio = (inicio + fim) // 2
        print(f"  Passo {passo}: inicio={inicio}, fim={fim}, meio=({inicio}+{fim})//2={meio}, arr[{meio}]={arr[meio]}")
        comparacoes += 1
        if arr[meio] == alvo:
            print(f"           {arr[meio]} == {alvo}? SIM -> encontrado no indice {meio}")
            return meio, comparacoes
        comparacoes += 1
        if alvo < arr[meio]:
            print(f"           {alvo} < {arr[meio]}? sim -> descarta a metade direita")
            fim = meio - 1
        else:
            print(f"           {alvo} < {arr[meio]}? nao -> descarta a metade esquerda")
            inicio = meio + 1
    return -1, comparacoes


def main():
    print(f"Array: {ARRAY} (N = {len(ARRAY)}) | Alvo: {ALVO}")
    print()

    print("== Exercicio 3: busca linear ==")
    indice, comp_linear = busca_linear_rastreada(ARRAY, ALVO)
    print(f"Resultado: indice {indice}, {comp_linear} comparacoes")
    print()

    print("== Exercicio 4: busca binaria ==")
    indice, comp_binaria = busca_binaria_rastreada(ARRAY, ALVO)
    print(f"Resultado: indice {indice}, {comp_binaria} comparacao(oes)")
    print()

    print("== Pior caso para N = 7 (alvo ausente, ex.: 14) ==")
    _, pior_linear = busca_linear_rastreada(ARRAY, 14)
    print(f"Linear: {pior_linear} comparacoes (= N)")
    _, pior_binaria = busca_binaria_rastreada(ARRAY, 14)
    print(f"Binaria: {pior_binaria} comparacoes (3 iteracoes = log2(8), 2 comparacoes cada)")


if __name__ == "__main__":
    main()
