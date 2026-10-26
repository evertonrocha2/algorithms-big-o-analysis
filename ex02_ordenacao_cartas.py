"""
Exercicio 2 - Ordenacao das 13 cartas de espadas (simulacao do algoritmo conceitual).

Restricoes assumidas (modelo de mesa):
  - As 13 cartas estao viradas para cima, lado a lado, em uma fileira.
  - So da para olhar e comparar DUAS cartas VIZINHAS por vez.
  - A unica movimentacao permitida e TROCAR essas duas vizinhas de lugar.
  - Nao existe espaco extra na mesa (sem pilha auxiliar).

Com essas restricoes o procedimento manual vira o Bubble Sort.
"""

import random

# Valor numerico de cada carta: A=1, J=11, Q=12, K=13
NOMES = {1: "A", 11: "J", 12: "Q", 13: "K"}


def nome(carta):
    return NOMES.get(carta, str(carta))


def mostrar(fileira):
    return " ".join(f"{nome(c):>2}" for c in fileira)


def ordenar_cartas(fileira):
    """Ordena a fileira trocando so cartas vizinhas. Mostra cada rodada."""
    cartas = fileira[:]
    n = len(cartas)
    comparacoes = 0
    trocas = 0

    for rodada in range(1, n):
        houve_troca = False
        # A cada rodada a maior carta ainda fora do lugar "borbulha" para a direita,
        # entao a parte final da fileira ja esta pronta e nao precisa ser revista.
        for i in range(n - rodada):
            comparacoes += 1
            if cartas[i] > cartas[i + 1]:
                cartas[i], cartas[i + 1] = cartas[i + 1], cartas[i]
                trocas += 1
                houve_troca = True
        print(f"Rodada {rodada:>2}: {mostrar(cartas)}")
        if not houve_troca:
            print("Nenhuma troca nesta rodada: a fileira ja esta ordenada.")
            break

    return cartas, comparacoes, trocas


def main():
    random.seed(42)
    fileira = list(range(1, 14))
    random.shuffle(fileira)

    print(f"Estado inicial: {mostrar(fileira)}")
    print()
    ordenadas, comparacoes, trocas = ordenar_cartas(fileira)
    print()
    print(f"Estado final:   {mostrar(ordenadas)}")
    print(f"Comparacoes: {comparacoes} | Trocas: {trocas}")
    print(f"Pior caso teorico com 13 cartas: 13*12/2 = {13 * 12 // 2} comparacoes")


if __name__ == "__main__":
    main()
