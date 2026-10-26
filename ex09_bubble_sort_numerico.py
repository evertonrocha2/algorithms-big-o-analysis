"""
Exercicio 9 - Bubble Sort numerico (ordem crescente).

Compara pares vizinhos e troca quando estao fora de ordem. Ao fim de cada
passada o maior elemento restante "borbulha" para o final da lista.
"""

from collections import Counter


def bubble_sort(arr):
    """Retorna uma NOVA lista ordenada em ordem crescente."""
    lista = arr[:]  # copia: nao altera a lista original
    n = len(lista)
    for ultimo in range(n - 1, 0, -1):  # a cada passada a parte final ja esta pronta
        for i in range(ultimo):
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
    return lista


def esta_ordenada(lista):
    """Verifica a ordem sem usar sorted(): cada elemento <= seu vizinho da direita."""
    return all(lista[i] <= lista[i + 1] for i in range(len(lista) - 1))


def mesmos_elementos(a, b):
    """Garante que a ordenacao nao perdeu nem inventou elementos."""
    return Counter(a) == Counter(b)


def main():
    testes = {
        "ja ordenada": [1, 2, 3, 4, 5, 6],
        "desordenada": [64, 34, 25, 12, 22, 11, 90],
        "decrescente": [9, 7, 5, 3, 1],
        "com repetidos": [3, 1, 2, 3, 1, 2],
        "negativos e zero": [0, -5, 8, -1, 3],
        "decimais": [3.14, 2.71, 1.41, 1.73],
        "um elemento": [7],
        "vazia": [],
    }

    todos_ok = True
    for nome, arr in testes.items():
        resultado = bubble_sort(arr)
        ok = esta_ordenada(resultado) and mesmos_elementos(arr, resultado)
        todos_ok = todos_ok and ok
        print(f"{nome:<18} entrada={str(arr):<32} saida={str(resultado):<32} {'OK' if ok else 'ERRO'}")
        assert ok, f"Falha no caso: {nome}"

    print()
    print(f"Todos os {len(testes)} testes passaram: {todos_ok}")


if __name__ == "__main__":
    main()
