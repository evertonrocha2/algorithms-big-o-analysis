"""
Exercicio 12 - Bubble Sort otimizado (para quando uma passada nao faz trocas).

Usa exatamente os mesmos dados do Ex. 11 e compara as contagens.
"""

from ex11_bubble_sort_instrumentado import TAMANHOS, bubble_sort_instrumentado, gerar_entradas


def bubble_sort_otimizado(arr):
    """Retorna (lista_ordenada, comparacoes, trocas, passadas)."""
    lista = arr[:]
    n = len(lista)
    comparacoes = 0
    trocas = 0
    passadas = 0
    for ultimo in range(n - 1, 0, -1):
        passadas += 1
        houve_troca = False
        for i in range(ultimo):
            comparacoes += 1
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                trocas += 1
                houve_troca = True
        # Se ninguem trocou de lugar, todos os vizinhos estao em ordem: lista pronta
        if not houve_troca:
            break
    return lista, comparacoes, trocas, passadas


def main():
    print(f"{'N':>5} {'perfil':<12} {'comp. classico':>15} {'comp. otimizado':>16} {'economia':>9} {'trocas':>8} {'passadas':>9}")
    print("-" * 80)
    for n in TAMANHOS:
        for perfil, arr in gerar_entradas(n).items():
            ordenada_a, comp_classico, trocas_a = bubble_sort_instrumentado(arr)
            ordenada_b, comp_otimizado, trocas_b, passadas = bubble_sort_otimizado(arr)
            assert ordenada_a == ordenada_b and trocas_a == trocas_b  # mesmo resultado, mesmas trocas
            economia = 1 - comp_otimizado / comp_classico
            print(
                f"{n:>5} {perfil:<12} {comp_classico:>15,} {comp_otimizado:>16,} "
                f"{economia:>8.1%} {trocas_b:>8,} {passadas:>9}"
            )
        print()


if __name__ == "__main__":
    main()
