"""
Exercicio 8 - Bubble Sort bidirecional (Cocktail Sort).

Cada rodada tem duas passadas:
  - ida (esquerda -> direita): leva o MAIOR elemento para a direita;
  - volta (direita -> esquerda): leva o MENOR elemento para a esquerda.
Os indices `esquerdo` e `direito` marcam a parte ainda nao ordenada.
"""

import random


def cocktail_sort(arr):
    """Retorna (lista_ordenada, comparacoes, rodadas). Nao altera a original."""
    lista = arr[:]
    esquerdo = 0
    direito = len(lista) - 1
    comparacoes = 0
    rodadas = 0

    while esquerdo < direito:
        rodadas += 1
        houve_troca = False

        # Ida: o maior da faixa [esquerdo, direito] termina em `direito`
        for i in range(esquerdo, direito):
            comparacoes += 1
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                houve_troca = True
        direito -= 1  # a ultima posicao ja esta no lugar certo

        if not houve_troca:
            break

        houve_troca = False
        # Volta: o menor da faixa [esquerdo, direito] termina em `esquerdo`
        for i in range(direito, esquerdo, -1):
            comparacoes += 1
            if lista[i - 1] > lista[i]:
                lista[i - 1], lista[i] = lista[i], lista[i - 1]
                houve_troca = True
        esquerdo += 1  # a primeira posicao ja esta no lugar certo

        if not houve_troca:
            break

    return lista, comparacoes, rodadas


def bubble_sort_otimizado(arr):
    """Bubble Sort tradicional (so ida) com parada antecipada, para comparar."""
    lista = arr[:]
    n = len(lista)
    comparacoes = 0
    passadas = 0
    for ultimo in range(n - 1, 0, -1):
        passadas += 1
        houve_troca = False
        for i in range(ultimo):
            comparacoes += 1
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                houve_troca = True
        if not houve_troca:
            break
    return lista, comparacoes, passadas


def esta_ordenada(lista):
    return all(lista[i] <= lista[i + 1] for i in range(len(lista) - 1))


def main():
    random.seed(42)
    testes = {
        "aleatorio": random.sample(range(1, 21), 10),
        "ja ordenado": [1, 2, 3, 4, 5, 6, 7, 8],
        "decrescente": [8, 7, 6, 5, 4, 3, 2, 1],
        "com repetidos": [5, 1, 4, 1, 5, 9, 2, 6, 5],
        "tartaruga (menor no fim)": [2, 3, 4, 5, 6, 7, 8, 1],
        "vazio": [],
        "um elemento": [42],
    }

    print("== Testes do Cocktail Sort ==")
    for nome, arr in testes.items():
        ordenada, comparacoes, rodadas = cocktail_sort(arr)
        ok = "OK" if esta_ordenada(ordenada) else "ERRO"
        print(f"{nome:<26} {str(arr):<32} -> {str(ordenada):<32} {ok}")
    print()

    print("== Cocktail x Bubble tradicional (ambos com parada antecipada) ==")
    print(f"{'caso':<26} {'bubble comp':>11} {'passadas':>8} | {'cocktail comp':>13} {'rodadas':>7}")
    for nome, arr in testes.items():
        _, comp_b, passadas = bubble_sort_otimizado(arr)
        _, comp_c, rodadas = cocktail_sort(arr)
        print(f"{nome:<26} {comp_b:>11} {passadas:>8} | {comp_c:>13} {rodadas:>7}")


if __name__ == "__main__":
    main()
