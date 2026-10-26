"""
Exercicio 14 - Refatoracao: mesma logica, mesmos contadores, codigo legivel.

Contem:
  - o codigo ORIGINAL (f e h), sem nenhuma alteracao, para servir de referencia;
  - a versao REFATORADA (binary_search_with_count e bubble_sort_with_count);
  - um teste que prova que as duas versoes devolvem exatamente o mesmo resultado.
"""

import random


# ===================================================== codigo original (nao mexer)

def f(a, t):
    c = 0
    i = 0
    j = len(a) - 1
    r = -1
    while i <= j:
        m = (i + j) // 2
        c = c + 1
        if a[m] == t:
            r = m
            break
        c = c + 1
        if t < a[m]:
            j = m - 1
        else:
            i = m + 1
    return r, c


def h(arr):
    b = arr[:]
    n = len(b)
    k = 0
    for last in range(n - 1, 0, -1):
        for p in range(last):
            k += 1
            if b[p] > b[p + 1]:
                tmp = b[p]
                b[p] = b[p + 1]
                b[p + 1] = tmp
    return b, k


# ===================================================== versao refatorada

NOT_FOUND = -1


def binary_search_with_count(sorted_values, target):
    """
    Busca binaria em uma lista em ordem crescente.

    Retorna (indice, comparacoes):
      - indice: posicao do alvo, ou NOT_FOUND (-1) se ele nao existir;
      - comparacoes: comparacoes de chave feitas (igualdade + menor que).

    Complexidade: O(log N), pois cada iteracao descarta metade do intervalo.
    """
    comparisons = 0
    low = 0
    high = len(sorted_values) - 1

    while low <= high:
        middle = (low + high) // 2

        comparisons += 1  # teste de igualdade com o elemento do meio
        if sorted_values[middle] == target:
            return middle, comparisons

        comparisons += 1  # teste que decide qual metade descartar
        if target < sorted_values[middle]:
            high = middle - 1  # alvo so pode estar a esquerda
        else:
            low = middle + 1  # alvo so pode estar a direita

    return NOT_FOUND, comparisons


def swap(values, i, j):
    """Troca dois elementos de posicao (in-place)."""
    values[i], values[j] = values[j], values[i]


def bubble_sort_with_count(values):
    """
    Bubble Sort classico sobre uma COPIA da lista (a original nao muda).

    Retorna (lista_ordenada, comparacoes) onde comparacoes conta cada
    comparacao entre pares adjacentes.

    Complexidade: O(N^2). Sempre faz N(N-1)/2 comparacoes, pois nao
    tem parada antecipada (igual ao original).
    """
    result = values[:]
    comparisons = 0

    # A cada passada o maior elemento restante vai para a posicao `last_unsorted`,
    # entao o trecho depois dela ja esta ordenado e nao precisa ser revisto.
    for last_unsorted in range(len(result) - 1, 0, -1):
        for position in range(last_unsorted):
            comparisons += 1
            if result[position] > result[position + 1]:
                swap(result, position, position + 1)

    return result, comparisons


# ===================================================== teste de equivalencia

def build_test_lists(seed=42):
    """Listas variadas: vazia, 1 elemento, repetidos, negativos e aleatorias."""
    random.seed(seed)
    fixed = [[], [1], [2, 1], [3, 3, 3], [5, -2, 0, -2, 9], list(range(10)), list(range(10, 0, -1))]
    randoms = [
        [random.randint(-50, 50) for _ in range(random.randint(0, 40))]
        for _ in range(300)
    ]
    return fixed + randoms


def test_equivalence():
    lists = build_test_lists()
    sort_checks = 0
    search_checks = 0

    for values in lists:
        original_input = values[:]

        # Bubble Sort: mesma lista e mesmo contador
        assert h(values) == bubble_sort_with_count(values)
        assert values == original_input  # nenhuma das versoes altera a entrada
        sort_checks += 1

        # Busca binaria: testa todos os valores presentes e alguns ausentes
        sorted_values, _ = h(values)
        targets = set(sorted_values) | {-999, 999, 0}
        for target in targets:
            assert f(sorted_values, target) == binary_search_with_count(sorted_values, target)
            search_checks += 1

    return sort_checks, search_checks


def main():
    exemplo = [29, 10, 14, 37, 13]
    print(f"Exemplo: {exemplo}")
    print(f"  original   h(arr) = {h(exemplo)}")
    print(f"  refatorado        = {bubble_sort_with_count(exemplo)}")
    ordenado, _ = h(exemplo)
    print(f"  original   f(arr, 14) = {f(ordenado, 14)}")
    print(f"  refatorado            = {binary_search_with_count(ordenado, 14)}")
    print(f"  original   f(arr, 99) = {f(ordenado, 99)}")
    print(f"  refatorado            = {binary_search_with_count(ordenado, 99)}")
    print()

    sort_checks, search_checks = test_equivalence()
    print(f"Bubble Sort: {sort_checks} listas comparadas, todas iguais.")
    print(f"Busca binaria: {search_checks} buscas comparadas, todas iguais.")
    print("Teste de equivalencia: PASSOU")


if __name__ == "__main__":
    main()
