# algorithms-big-o-analysis

TP1 da disciplina **Velocidade e Qualidade com Estruturas de Dados e Algoritmos [26E4_1]**, Instituto Infnet.

Busca linear e binária, Bubble Sort (numérico, strings, instrumentado e otimizado), Cocktail Sort e análise de complexidade com Big O. Os algoritmos são instrumentados com contadores de comparações e trocas.

## Como rodar

Python 3.10+ e nenhuma dependência para os exercícios.

```bash
python ex01_busca_linear.py   # um exercício
python rodar_todos.py         # todos em sequência
```

Os sorteios usam semente fixa (42), então a saída é sempre a mesma.

## Exercícios

| # | Arquivo | Tema |
|---|---------|------|
| 1 | `ex01_busca_linear.py` | Busca linear instrumentada |
| 2 | `ex02_ordenacao_cartas.py` | Ordenação de cartas |
| 3 e 4 | `ex03_ex04_busca_manual.py` | Busca linear e binária passo a passo |
| 5 | `ex05_maior_unico.py` | De O(N²) para O(N) |
| 6 | `ex06_tabuleiro_xadrez.py` | Grãos no tabuleiro, O(log Q) |
| 7 | `ex07_only_a_strings.py` | Análise de `only_a_strings` |
| 8 | `ex08_cocktail_sort.py` | Bubble Sort bidirecional |
| 9 | `ex09_bubble_sort_numerico.py` | Bubble Sort numérico |
| 10 | `ex10_bubble_sort_strings.py` | Bubble Sort de strings |
| 11 | `ex11_bubble_sort_instrumentado.py` | Contagem de comparações e trocas |
| 12 | `ex12_bubble_sort_otimizado.py` | Parada antecipada |
| 13 | `ex13_comparacao_buscas.py` | Linear vs binária com testes |
| 14 | `ex14_refatoracao.py` | Refatoração com teste de equivalência |

Respostas escritas: [RESPOSTAS.md](RESPOSTAS.md). Os scripts `gerar_prints.py` e `gerar_pdf.py` montam o PDF de entrega (precisam de `pillow` e `reportlab`).
