"""
Exercicio 7 - Analise de complexidade de only_a_strings.

A funcao original fica igual. A versao instrumentada so conta as iteracoes do
laco e as operacoes O(1) feitas em cada uma, para confirmar a analise O(N).
"""

import random
import string


def only_a_strings(strings):
    result = []
    for s in strings:
        if len(s) > 0 and s[0] == "a":
            result.append(s)
    return result


def only_a_strings_instrumentada(strings):
    result = []
    iteracoes = 0
    operacoes = 0
    for s in strings:
        iteracoes += 1
        operacoes += 1  # len(s) > 0
        if len(s) > 0:
            operacoes += 1  # s[0] == "a" (so roda se a string nao for vazia)
            if s[0] == "a":
                operacoes += 1  # append
                result.append(s)
    return result, iteracoes, operacoes


def gerar_strings(n):
    """Strings de tamanho pequeno e constante (premissa do enunciado)."""
    return ["".join(random.choices(string.ascii_lowercase[:3], k=5)) for _ in range(n)]


def main():
    exemplo = ["abacaxi", "banana", "", "amora", "uva", "a"]
    print(f"Exemplo: {exemplo}")
    print(f"Resultado: {only_a_strings(exemplo)}")
    print()

    random.seed(42)
    print(f"{'N':>9} {'iteracoes':>10} {'operacoes':>10} {'operacoes/N':>12}")
    for n in [10, 100, 1_000, 10_000, 100_000]:
        _, iteracoes, operacoes = only_a_strings_instrumentada(gerar_strings(n))
        print(f"{n:>9,} {iteracoes:>10,} {operacoes:>10,} {operacoes / n:>12.2f}")
    print()
    print("Iteracoes = N sempre. Operacoes/N fica entre 1 e 3 (constante), logo custo total O(N).")


if __name__ == "__main__":
    main()
