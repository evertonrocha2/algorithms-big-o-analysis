"""
Exercicio 10 - Bubble Sort para strings.

O mesmo algoritmo do Ex. 9. Muda so o criterio de comparacao:
  - versao "crua": compara as strings direto (ordem dos codigos Unicode);
  - versao "alfabetica": compara por uma chave normalizada (sem acento, minuscula),
    que e o que uma pessoa espera de "ordem alfabetica".
"""

import unicodedata


def bubble_sort(lista, chave=None):
    """Bubble Sort generico. `chave` transforma cada item antes de comparar."""
    resultado = lista[:]
    if chave is None:
        chave = lambda item: item
    n = len(resultado)
    for ultimo in range(n - 1, 0, -1):
        for i in range(ultimo):
            if chave(resultado[i]) > chave(resultado[i + 1]):
                resultado[i], resultado[i + 1] = resultado[i + 1], resultado[i]
    return resultado


def chave_alfabetica(palavra):
    """'Ábaco' -> 'abaco': remove acentos e ignora maiusculas/minusculas."""
    sem_acento = unicodedata.normalize("NFD", palavra)
    sem_acento = "".join(c for c in sem_acento if unicodedata.category(c) != "Mn")
    return sem_acento.casefold()


def esta_ordenada(lista, chave=lambda x: x):
    return all(chave(lista[i]) <= chave(lista[i + 1]) for i in range(len(lista) - 1))


def main():
    testes = {
        "simples": ["pera", "uva", "banana", "abacaxi", "manga"],
        "prefixos": ["casa", "cas", "casamento", "ca", "casal"],
        "maiusculas": ["banana", "Abacate", "cereja", "Banana", "abacate"],
        "acentos": ["zebra", "ábaco", "Ótimo", "ovo", "água", "agua"],
        "com numeros": ["item10", "item2", "item1", "item20"],
        "repetidas": ["sol", "lua", "sol", "mar", "lua"],
    }

    for nome, palavras in testes.items():
        crua = bubble_sort(palavras)
        alfabetica = bubble_sort(palavras, chave=chave_alfabetica)
        print(f"== {nome} ==")
        print(f"  entrada:              {palavras}")
        print(f"  comparacao crua:      {crua}  ordenada? {esta_ordenada(crua)}")
        print(f"  ordem alfabetica:     {alfabetica}  ordenada? {esta_ordenada(alfabetica, chave_alfabetica)}")
    print()

    # Por que a versao crua erra com maiusculas e acentos: ela compara codigos Unicode
    for letra in ["A", "Z", "a", "z", "á", "Ó"]:
        print(f"ord('{letra}') = {ord(letra)}")


if __name__ == "__main__":
    main()
