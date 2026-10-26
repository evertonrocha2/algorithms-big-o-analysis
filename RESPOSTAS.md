# DR1 TP1: Respostas escritas

Cada exercício tem um script `exNN_*.py`. Rode com `python exNN_*.py` ou tudo com `python rodar_todos.py`.
Modelo de contagem: na busca binária, cada iteração conta 1 comparação pelo teste `==` e, se não achou, mais 1 pelo teste `<` (mesmo modelo do código do Ex. 14).

---

## Exercício 1: Busca linear instrumentada

- Array: 10.000 inteiros distintos, não ordenados (`random.sample`, semente 42).
- Busca pelo elemento da primeira posição: **1 comparação**.
- Casos extras para análise: meio = 5.001, última posição = 10.000, ausente = 10.000 comparações.

**Análise:** o custo é igual à posição do alvo + 1. O caso pedido é o melhor caso, O(1). O pior caso (último ou ausente) faz N comparações, logo a busca linear é **O(N)**.

---

## Exercício 2: Ordenação das 13 cartas de espadas

**Restrições assumidas:** cartas viradas para cima em uma fileira; só é possível comparar duas cartas vizinhas e trocá-las de lugar; não há espaço auxiliar.

**Estado inicial:** 13 cartas (A=1 ... K=13) embaralhadas na fileira.
**Operações permitidas:** comparar duas vizinhas; trocar as duas.
**Estado final:** A 2 3 4 5 6 7 8 9 10 J Q K.

**Algoritmo:**
1. Comece pela carta mais à esquerda.
2. Compare com a vizinha da direita; se a da esquerda for maior, troque.
3. Avance uma posição e repita até o fim da parte não ordenada.
4. Ao fim da rodada a maior carta restante está no final; a próxima rodada para uma posição antes.
5. Se uma rodada inteira não teve trocas, pare: a fileira está ordenada.

**Algoritmo clássico:** Bubble Sort. A única operação é comparar e trocar vizinhos, e a cada rodada o maior elemento "borbulha" para o fim.

**Custo:** pior caso (N-1) + (N-2) + ... + 1 = N(N-1)/2 = 78 comparações para N = 13, ou seja **O(N²)**. Melhor caso (já ordenado, com parada antecipada): N-1 = 12 comparações, O(N). Simulação real: 77 comparações e 47 trocas.

---

## Exercício 3: Busca linear manual em [2, 4, 6, 8, 10, 12, 13], alvo 8

| Passo | Índice | Valor | 8 == valor? |
|---|---|---|---|
| 1 | 0 | 2 | não |
| 2 | 1 | 4 | não |
| 3 | 2 | 6 | não |
| 4 | 3 | 8 | sim |

**4 comparações.** O 8 está no índice 3; a linear verifica todos os anteriores, então faz índice + 1 comparações.
Para N = 7 a linear faz de 1 (melhor caso) a 7 (pior caso) comparações. O pior caso cresce na mesma proporção de N: **O(N)**. A linear não aproveita a ordenação do array.

---

## Exercício 4: Busca binária manual no mesmo array, alvo 8

| Passo | início | fim | meio | arr[meio] | Decisão |
|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 8 | 8 == 8, encontrado |

**1 comparação** (contra 4 da linear).
Pior caso com N = 7 (alvo ausente): 3 iterações (log₂ 8 = 3), 6 comparações, contra 7 da linear.
A binária descarta metade do intervalo a cada passo, logo **O(log N)**. Com N = 1.000.000 a linear pode fazer 1.000.000 comparações e a binária no máximo 20 iterações. Pré-requisito: lista ordenada.

---

## Exercício 5: Maior número único, O(N²) para O(N)

**Por que é O(N²):** para cada um dos N elementos, o laço interno percorre o array inteiro para contar ocorrências. São N × N = N² comparações, e valores repetidos são recontados várias vezes.

**Versão O(N):**
```python
def maior_unico_otimizado(arr):
    contagem = {}
    for valor in arr:
        contagem[valor] = contagem.get(valor, 0) + 1
    maior = None
    for valor, vezes in contagem.items():
        if vezes == 1 and (maior is None or valor > maior):
            maior = valor
    return maior
```

**Estratégia:** contar todas as ocorrências em uma única passada, guardando em um dicionário (tabela hash, acesso O(1) em média). Depois, uma segunda passada sobre as chaves escolhe o maior com contagem 1.

**Justificativa:** passada 1 = N × O(1) = O(N); passada 2 = até N × O(1) = O(N). Total O(2N) = **O(N)**. Custo extra de memória O(N) pelo dicionário.
**Evidência:** mesmo resultado da original em 6 casos de borda e 200 listas aleatórias. Com N = 10.000: 100.000.000 iterações (original) contra 20.000 (otimizada).

---

## Exercício 6: Tabuleiro de xadrez

Função `menor_quadrado(qtd_graos)`: começa no quadrado 1 com 1 grão e dobra a cada quadrado até alcançar o alvo. Sem fórmula pronta.

| qtd_graos | Quadrado | Iterações |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 4 | 3 | 3 |
| 8 | 4 | 4 |
| 1.000 | 11 | 11 |
| 1.000.000 | 21 | 21 |
| 2⁶³ | 64 | 64 |
| 2⁶⁴ (maior que o total 2⁶⁴ - 1) | "Valor excede o limite do tabuleiro" | 64 |

**Complexidade:** o laço roda até o quadrado da resposta, que é aproximadamente log₂(Q) + 1. Multiplicar Q por 1.000 (de 1.000 para 1.000.000) aumentou só 10 iterações: **O(log Q)**. Como o tabuleiro tem 64 quadrados, o laço nunca passa de 64 iterações (limite constante).

---

## Exercício 7: Análise de `only_a_strings`

1. O `for` executa **exatamente N vezes** (um por elemento, sem `break`).
2. Em cada iteração: `len(s) > 0` (sempre), `s[0] == "a"` (se a string não for vazia) e `append` (se começar com "a"). Entre 1 e 3 operações O(1).
3. Custo total: T(N) = c₁ + c₂·N, com c₁ = criar a lista e retornar, e 1 ≤ c₂ ≤ 3.
4. **O(N)**.
5. Há um único laço, não aninhado, com trabalho constante por iteração (premissas do enunciado). Constante × N cresce linearmente; c₁ não depende de N e é descartado. Confirmação empírica: operações/N fica em 2,33 de N = 100 a N = 100.000.

---

## Exercício 8: Cocktail Sort

Duas passadas por rodada: a ida leva o maior para `direito`; a volta leva o menor para `esquerdo`. Os índices se fecham a cada rodada. Testado com arrays aleatório, ordenado, decrescente, com repetidos, "tartaruga", vazio e unitário: todos corretos.

| Caso | Bubble (comparações) | Cocktail (comparações) |
|---|---|---|
| Tartaruga [2,3,4,5,6,7,8,1] | 28 | 18 |
| Aleatório (10) | 42 | 35 |
| Decrescente (8) | 28 | 28 |
| Já ordenado (8) | 7 | 7 |

**Comparação conceitual:** o Bubble move elementos pequenos só uma posição para a esquerda por passada ("tartarugas"). O Cocktail os traz de volta em uma passada de volta, reduzindo passadas. Porém o pior caso continua ~N²/2 comparações: **O(N²)**; melhor caso O(N).

---

## Exercício 9: Bubble Sort numérico

Implementado em ordem crescente sobre uma cópia da lista. Validação sem `sorted()`: `esta_ordenada` (cada elemento ≤ vizinho) e `mesmos_elementos` (`Counter`). 8 casos testados (ordenada, desordenada, decrescente, repetidos, negativos, decimais, unitária, vazia): todos OK.

---

## Exercício 10: Bubble Sort para strings

Mesmo algoritmo; muda só o critério de comparação. Comportamento observado com comparação direta (códigos Unicode):
- maiúsculas antes de minúsculas (`Banana` < `abacate`, pois 66 < 97);
- palavras acentuadas no fim (`ábaco` > `zebra`, pois 225 > 122);
- prefixo antes da palavra maior (`ca` < `cas` < `casa`);
- números comparados como texto (`item10` < `item2`).

Para ordem alfabética "humana", usei uma chave que remove acentos e ignora maiúsculas (`unicodedata` + `casefold`). Continua O(N²) comparações (cada comparação de strings custa até o tamanho delas).

---

## Exercício 11: Bubble Sort instrumentado

| N | Comparações (todos os perfis) | Trocas aleatório | Trocas ordenado | Trocas decrescente |
|---|---|---|---|---|
| 25 | 300 | 165 | 0 | 300 |
| 50 | 1.225 | 582 | 0 | 1.225 |
| 100 | 4.950 | 2.535 | 0 | 4.950 |
| 200 | 19.900 | 10.124 | 0 | 19.900 |
| 400 | 79.800 | 41.210 | 0 | 79.800 |
| 800 | 319.600 | 156.792 | 0 | 319.600 |

**Análise:** comparações = N(N-1)/2 sempre, independentemente dos dados. Trocas = número de inversões: 0 (ordenado), ~N²/4 (aleatório), N(N-1)/2 (decrescente). Quando N dobra, as comparações multiplicam por ~4,0: crescimento quadrático, **O(N²)**.

---

## Exercício 12: Bubble Sort otimizado (parada sem trocas)

| N = 800 | Clássico | Otimizado | Economia | Passadas |
|---|---|---|---|---|
| Ordenado | 319.600 | 799 | 99,8% | 1 |
| Aleatório | 319.600 | 319.600 | 0% | 799 |
| Decrescente | 319.600 | 319.600 | 0% | 799 |

(Aleatório com N = 100: 4.950 para 4.872, 1,6% de economia.) Trocas idênticas nas duas versões.
**Relação com Big O:** melhor caso cai de O(N²) para **O(N)** (uma passada). Pior caso (decrescente) e caso médio continuam **O(N²)**. O ganho só é relevante em dados já ou quase ordenados.

---

## Exercício 13: Comparação de estratégias de busca

### Parte B: resultados (N = 31)

| Lista | Alvo | Linear | Binária | Bubble | Bubble + binária |
|---|---|---|---|---|---|
| arr_sorted | first (1) | 1 | 9 | - | 9 |
| arr_sorted | middle (16) | 16 | 1 | - | 1 |
| arr_sorted | absent (-1) | 31 | 10 | - | 10 |
| arr_reverse | first (31) | 1 | 9 | 465 | 474 |
| arr_reverse | middle (16) | 16 | 1 | 465 | 466 |
| arr_reverse | absent (-1) | 31 | 10 | 465 | 475 |
| arr_random | first (20) | 1 | 5 | 465 | 470 |
| arr_random | middle (29) | 16 | 9 | 465 | 474 |
| arr_random | absent (-1) | 31 | 10 | 465 | 475 |

### Parte C: conclusão técnica

**Pré-requisitos.** A busca linear funciona em qualquer lista, ordenada ou não. A busca binária exige lista ordenada; sem isso ela descarta a metade errada e pode não encontrar um elemento que existe.

**Big O.** Busca linear: O(N) no pior caso (31 comparações com N = 31). Busca binária: O(log N) (no máximo 5 iterações, 10 comparações). Bubble Sort: O(N²) (465 = 31·30/2 comparações). Ordenar e buscar uma vez custa O(N² + log N) = O(N²), pior que a linear.

**Quando vale pagar o Bubble Sort.** Ordenar é um custo fixo pago uma vez. Compensa quando há muitas buscas na mesma lista: 465 + 10k < 31k quando k > 22,1, ou seja, a partir de **23 buscas** no pior caso (no caso médio, com a linear em ~16 comparações, a partir de 78). Para uma ou poucas buscas, a linear é sempre melhor (31 contra 475). Para N maior, o Bubble piora mais rápido (N² contra N); na prática usaria-se uma ordenação O(N log N).

**Relação com os resultados.** A linear fez exatamente N = 31 no pior caso e só depende da posição do alvo. A binária nunca passou de 10 = 2·log₂(32). O Bubble fez exatamente N(N-1)/2 = 465. O alvo "first" mostra que a binária pode perder num caso individual (9 contra 1), pois o primeiro elemento é o melhor caso da linear e quase o pior da binária: Big O descreve crescimento e pior caso, não cada execução.

---

## Exercício 14: Refatoração

- `f` virou `binary_search_with_count(sorted_values, target)`; `h` virou `bubble_sort_with_count(values)`.
- Variáveis de uma letra trocadas por nomes descritivos (`comparisons`, `low`, `high`, `middle`, `last_unsorted`, `position`).
- `r = m; break` virou `return` direto; constante `NOT_FOUND = -1`; troca manual com `tmp` virou a função `swap`.
- Docstrings com entrada, saída e Big O; comentários explicam o porquê.
- Contadores e critérios de parada intactos; sem `sorted`/`.sort()`; complexidades mantidas (O(log N) e O(N²)).

**Teste de equivalência:** o arquivo mantém `f` e `h` originais e compara as tuplas completas (resultado + contador) em 307 listas (7 de borda + 300 aleatórias) e 6.556 buscas (valores presentes e ausentes). Todas idênticas: **PASSOU**.

---

**Link do vídeo:** _(colar aqui)_
