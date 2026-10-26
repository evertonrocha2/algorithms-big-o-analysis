"""
Exercicio 13 - Comparacao de estrategias de busca (linear x binaria).

Parte A: funcoes instrumentadas.
Parte B: 3 listas (ordenada, decrescente, embaralhada) com N = 31 e 3 alvos cada.
A conclusao (Parte C) esta em RESPOSTAS.md.
"""

import random

N = 31


# ---------------------------------------------------------------- Parte A

def linear_search_count(arr, target):
    """Retorna (index, comparisons). Conta cada teste arr[i] == target."""
    comparisons = 0
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            return i, comparisons
    return -1, comparisons


def binary_search_count(sorted_arr, target):
    """
    Assume lista em ordem crescente. Retorna (index, comparisons).
    Conta as comparacoes de chave entre target e o valor do meio:
    1 pelo teste de igualdade e, se nao achou, 1 pelo teste de menor
    (mesmo modelo de contagem do codigo do Ex. 14).
    """
    low, high = 0, len(sorted_arr) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if sorted_arr[mid] == target:
            return mid, comparisons
        comparisons += 1
        if target < sorted_arr[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1, comparisons


def bubble_sort_count(arr):
    """Ordena uma COPIA (Bubble Sort classico). Retorna (sorted_arr, comparisons)."""
    sorted_arr = arr[:]
    n = len(sorted_arr)
    comparisons = 0
    for last in range(n - 1, 0, -1):
        for i in range(last):
            comparisons += 1  # comparacao entre o par adjacente
            if sorted_arr[i] > sorted_arr[i + 1]:
                sorted_arr[i], sorted_arr[i + 1] = sorted_arr[i + 1], sorted_arr[i]
    return sorted_arr, comparisons


def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


# ---------------------------------------------------------------- Parte B

def build_lists():
    arr_sorted = list(range(1, N + 1))          # 1, 2, ..., 31
    arr_reverse = arr_sorted[::-1]              # 31, 30, ..., 1
    arr_random = arr_sorted[:]
    random.seed(42)
    random.shuffle(arr_random)
    return {"arr_sorted": arr_sorted, "arr_reverse": arr_reverse, "arr_random": arr_random}


def run_experiments():
    rows = []
    for name, arr in build_lists().items():
        targets = {
            "first": arr[0],
            "middle": arr[N // 2],
            "absent": -1,
        }
        already_sorted = is_sorted(arr)
        if already_sorted:
            sorted_arr, sort_comparisons = arr, 0
        else:
            sorted_arr, sort_comparisons = bubble_sort_count(arr)

        for label, target in targets.items():
            lin_index, lin_comp = linear_search_count(arr, target)
            bin_index, bin_comp = binary_search_count(sorted_arr, target)
            rows.append({
                "lista": name,
                "alvo": f"{label} ({target})",
                "linear_idx": lin_index,
                "linear": lin_comp,
                "binaria_idx": bin_index,
                "binaria": bin_comp,
                "bubble": sort_comparisons,
                "total": sort_comparisons + bin_comp,
            })
    return rows


def main():
    lists = build_lists()
    for name, arr in lists.items():
        print(f"{name:<12} {arr}")
    print()

    header = (
        f"{'lista':<12} {'alvo':<12} {'linear (idx)':>13} {'binaria (idx)':>14} "
        f"{'bubble':>7} {'bubble+binaria':>15}"
    )
    print(header)
    print("-" * len(header))
    for r in run_experiments():
        bubble = r["bubble"] if r["bubble"] else "-"
        total = r["total"] if r["bubble"] else "-"
        print(
            f"{r['lista']:<12} {r['alvo']:<12} "
            f"{r['linear']:>7} ({r['linear_idx']:>3}) {r['binaria']:>7} ({r['binaria_idx']:>3}) "
            f"{bubble:>7} {total:>15}"
        )
    print()
    print("Obs.: idx da binaria e a posicao na lista ORDENADA (copia), nao na original.")
    print()

    # Ponto de equilibrio no pior caso: 465 + 10k < 31k
    sort_cost = N * (N - 1) // 2
    _, worst_binary = binary_search_count(lists["arr_sorted"], -1)
    worst_linear = N
    k = 1
    while sort_cost + worst_binary * k >= worst_linear * k:
        k += 1
    print(f"Pior caso: ordenar custa {sort_cost}, cada binaria {worst_binary}, cada linear {worst_linear}.")
    print(f"Ordenar + binaria passa a compensar a partir de {k} buscas.")


if __name__ == "__main__":
    main()
