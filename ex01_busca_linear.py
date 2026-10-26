"""
Exercicio 1 - Busca linear instrumentada.

Gera um array NAO ordenado com 10.000 inteiros distintos, busca o elemento
da primeira posicao e conta quantas comparacoes foram feitas.
"""

import random

TAMANHO = 10_000
SEMENTE = 42  # semente fixa: toda execucao gera o mesmo array (reprodutivel)


def gerar_array_distinto(tamanho, semente):
    """Retorna uma lista embaralhada com `tamanho` inteiros distintos."""
    random.seed(semente)
    # random.sample sorteia sem repeticao, entao todos os valores sao distintos
    return random.sample(range(1, tamanho * 10), tamanho)


def busca_linear(arr, alvo):
    """
    Percorre o array da esquerda para a direita.
    Retorna (indice, comparacoes). Se nao achar, indice = -1.
    """
    comparacoes = 0
    for i in range(len(arr)):
        comparacoes += 1  # conta a comparacao arr[i] == alvo
        if arr[i] == alvo:
            return i, comparacoes
    return -1, comparacoes


def main():
    arr = gerar_array_distinto(TAMANHO, SEMENTE)

    print(f"Tamanho do array: {len(arr)}")
    print(f"Todos distintos? {len(set(arr)) == len(arr)}")
    print(f"Primeiros 10 elementos: {arr[:10]}")
    print()

    # Caso pedido no enunciado: elemento na primeira posicao (melhor caso)
    alvo = arr[0]
    indice, comparacoes = busca_linear(arr, alvo)
    print("== Caso pedido: alvo na PRIMEIRA posicao (melhor caso) ==")
    print(f"Alvo: {alvo} | indice encontrado: {indice} | comparacoes: {comparacoes}")
    print()

    # Casos extras para mostrar como o custo cresce com a posicao do alvo
    print("== Casos extras (para comparar) ==")
    cenarios = [
        ("meio do array", arr[TAMANHO // 2]),
        ("ultima posicao (pior caso com sucesso)", arr[-1]),
        ("elemento ausente (pior caso)", -1),
    ]
    for descricao, alvo in cenarios:
        indice, comparacoes = busca_linear(arr, alvo)
        print(f"{descricao:<40} indice={indice:>6} comparacoes={comparacoes:>6}")


if __name__ == "__main__":
    main()
