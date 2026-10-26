"""
Exercicio 6 - Tabuleiro de xadrez e graos de arroz.

Quadrado n tem 2^(n-1) graos. Dada uma quantidade alvo de graos, achar o
MENOR quadrado cujo proprio conteudo e >= alvo. Solucao iterativa (sem log).
"""

TOTAL_QUADRADOS = 64


def menor_quadrado(qtd_graos):
    """
    Retorna (quadrado, iteracoes) ou (mensagem, iteracoes) se nao couber no tabuleiro.
    Comeca no quadrado 1 com 1 grao e vai dobrando ate alcancar o alvo.
    """
    if not isinstance(qtd_graos, int) or qtd_graos <= 0:
        raise ValueError("qtd_graos deve ser um inteiro positivo")

    graos_no_quadrado = 1  # quadrado 1
    iteracoes = 0
    for quadrado in range(1, TOTAL_QUADRADOS + 1):
        iteracoes += 1
        if graos_no_quadrado >= qtd_graos:
            return quadrado, iteracoes
        graos_no_quadrado *= 2  # proximo quadrado tem o dobro

    return "Valor excede o limite do tabuleiro (64 quadrados)", iteracoes


def total_do_tabuleiro():
    """Soma os graos dos 64 quadrados por iteracao (= 2^64 - 1)."""
    total, graos = 0, 1
    for _ in range(TOTAL_QUADRADOS):
        total += graos
        graos *= 2
    return total


def main():
    total = total_do_tabuleiro()
    print(f"Total de graos no tabuleiro: {total:,}")
    print(f"Graos so no quadrado 64:     {2 ** 63:,}")
    print()

    testes = [
        1, 2, 4, 8,                 # pequenos
        3, 5,                       # entre potencias de 2
        1_000, 1_000_000,           # intermediarios
        2 ** 63,                    # exatamente o quadrado 64
        total + 1,                  # maior que o total do tabuleiro
    ]
    print(f"{'qtd_graos':>28} | {'resultado':<50} | iteracoes")
    print("-" * 95)
    for qtd in testes:
        resultado, iteracoes = menor_quadrado(qtd)
        print(f"{qtd:>28,} | {str(resultado):<50} | {iteracoes}")


if __name__ == "__main__":
    main()
