"""
Exercicio 11 - Bubble Sort instrumentado (comparacoes e trocas).

Versao classica, SEM parada antecipada. Roda para varios tamanhos de entrada
e tres perfis de dados: aleatorio, ja ordenado e decrescente.
"""

import random

TAMANHOS = [25, 50, 100, 200, 400, 800]  # cada N e o dobro do anterior
SEMENTE = 42


def bubble_sort_instrumentado(arr):
    """Retorna (lista_ordenada, comparacoes, trocas)."""
    lista = arr[:]
    n = len(lista)
    comparacoes = 0
    trocas = 0
    for ultimo in range(n - 1, 0, -1):
        for i in range(ultimo):
            comparacoes += 1
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                trocas += 1
    return lista, comparacoes, trocas


def gerar_entradas(n, semente=SEMENTE):
    """Mesmos dados usados no Ex. 12 (por isso a semente e fixa)."""
    random.seed(semente + n)
    aleatorio = random.sample(range(n * 10), n)
    return {
        "aleatorio": aleatorio,
        "ordenado": list(range(n)),
        "decrescente": list(range(n, 0, -1)),
    }


def main():
    print(f"{'N':>5} {'perfil':<12} {'comparacoes':>12} {'trocas':>9} {'N(N-1)/2':>10}")
    print("-" * 52)
    for n in TAMANHOS:
        for perfil, arr in gerar_entradas(n).items():
            _, comparacoes, trocas = bubble_sort_instrumentado(arr)
            print(f"{n:>5} {perfil:<12} {comparacoes:>12,} {trocas:>9,} {n * (n - 1) // 2:>10,}")
        print()

    print("== Crescimento: o que acontece quando N dobra? ==")
    print(f"{'N':>5} {'comparacoes':>12} {'razao vs N anterior':>20}")
    anterior = None
    for n in TAMANHOS:
        _, comparacoes, _ = bubble_sort_instrumentado(gerar_entradas(n)["aleatorio"])
        razao = f"{comparacoes / anterior:.2f}x" if anterior else "-"
        print(f"{n:>5} {comparacoes:>12,} {razao:>20}")
        anterior = comparacoes


if __name__ == "__main__":
    main()
