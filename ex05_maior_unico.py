"""
Exercicio 5 - Otimizacao de O(N^2) para O(N).

Problema: retornar o maior numero que aparece exatamente uma vez no array.
"""

import random


def maior_unico_original(arr):
    """Versao original fornecida: O(N^2). Mantida igual para comparar resultados."""
    maior = None
    for i in range(len(arr)):
        atual = arr[i]
        contador = 0
        # Gargalo: para CADA elemento, percorre o array INTEIRO de novo
        for j in range(len(arr)):
            if arr[j] == atual:
                contador += 1
        if contador == 1:
            if (maior is None) or (atual > maior):
                maior = atual
    return maior


def maior_unico_otimizado(arr):
    """
    Versao O(N) em duas passadas lineares:
      1) conta quantas vezes cada valor aparece (dicionario);
      2) entre os valores com contagem 1, guarda o maior.
    """
    contagem = {}
    for valor in arr:  # passada 1: N iteracoes, cada uma O(1) em media
        contagem[valor] = contagem.get(valor, 0) + 1

    maior = None
    for valor, vezes in contagem.items():  # passada 2: no maximo N iteracoes
        if vezes == 1 and (maior is None or valor > maior):
            maior = valor
    return maior


def contar_passos_original(arr):
    """Quantas vezes o laco interno roda na versao original."""
    return len(arr) * len(arr)


def contar_passos_otimizado(arr):
    """Quantas iteracoes as duas passadas da versao otimizada fazem."""
    return len(arr) + len(set(arr))


def main():
    casos = [
        [5, 3, 9, 3, 5, 7],      # unicos: 9 e 7 -> 9
        [4, 4, 2, 2],            # nenhum unico -> None
        [1],                     # um elemento -> 1
        [],                      # vazio -> None
        [-3, -1, -1, -7],        # negativos -> -3
        [10, 10, 8, 6, 8],       # unico: 6 -> 6
    ]

    print("== Corretude: original x otimizado ==")
    for arr in casos:
        a = maior_unico_original(arr)
        b = maior_unico_otimizado(arr)
        status = "OK" if a == b else "DIFERENTE"
        print(f"{str(arr):<26} original={str(a):<5} otimizado={str(b):<5} {status}")

    # Teste aleatorio extra: 200 listas sorteadas
    random.seed(42)
    iguais = all(
        maior_unico_original(lst) == maior_unico_otimizado(lst)
        for lst in ([random.randint(0, 20) for _ in range(random.randint(0, 30))] for _ in range(200))
    )
    print(f"200 listas aleatorias com o mesmo resultado? {iguais}")
    print()

    print("== Crescimento do trabalho (iteracoes) ==")
    print(f"{'N':>7} {'original (N^2)':>16} {'otimizado (~2N)':>16}")
    for n in [10, 100, 1_000, 10_000]:
        arr = list(range(n))  # todos distintos: pior caso da segunda passada
        print(f"{n:>7} {contar_passos_original(arr):>16,} {contar_passos_otimizado(arr):>16,}")


if __name__ == "__main__":
    main()
