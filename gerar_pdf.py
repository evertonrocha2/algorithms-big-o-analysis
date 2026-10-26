"""Monta o PDF de entrega do TP1 no padrão Infnet (capa + texto ABNT + prints + link do código no GitHub).

Uso:
    python gerar_prints.py      (gera os prints a partir da execução real dos exercícios)
    python gerar_pdf.py
"""

import glob
import os
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(BASE, "screenshots")
LOGO = os.path.join(BASE, "assets", "logo_infnet.png")

ALUNO = "Everton da Rocha Silva"
LINK_VIDEO = "https://drive.google.com/drive/folders/1iToH65ab0lIRCsZB90hC3C7416fyAaI6"
REPO = "https://github.com/evertonrocha2/algorithms-big-o-analysis"
CAPA = {
    "instituicao": "INSTITUTO INFNET",
    "linhas": ["Faculdade de Engenharia de IA e Software", "Graduação em Engenharia de Software"],
    "disciplina": "Disciplina: Velocidade e Qualidade com Estruturas de Dados e Algoritmos [26E4_1]",
    "trabalho": "TP1",
    "titulo": "BUSCA, ORDENAÇÃO E ANÁLISE DE ALGORITMOS COM BIG O",
    "cidade": "Rio de Janeiro",
    "ano": "2026",
}
ARQUIVO_SAIDA = f"{ALUNO.replace(' ', '_')}_DR1_TP1.PDF"

INTRODUCAO = [
    "Este trabalho documenta a resolução dos catorze exercícios do Teste de Performance 1. O tema central é "
    "medir quantos passos um algoritmo executa quando o tamanho da entrada cresce e expressar esse "
    "crescimento com a notação Big O. Por isso, em vez de medir tempo em segundos, que depende da máquina, "
    "os algoritmos foram instrumentados com contadores de comparações, trocas e iterações.",
    "Todos os exercícios foram implementados em Python 3.14, um arquivo por exercício, e executados no "
    "PowerShell do Windows 11. Para cada exercício são apresentados a explicação do que foi feito, a análise "
    "de complexidade, a captura do terminal com o comando e a saída e o link para o código-fonte, que está completo no "
    "repositório do GitHub indicado ao final. As capturas foram geradas a partir da execução real de cada script. Os sorteios usam semente fixa (42), então "
    "qualquer nova execução produz os mesmos números.",
    "Na busca binária foi adotado o mesmo modelo de contagem do código fornecido no Exercício 14: cada "
    "iteração conta uma comparação pelo teste de igualdade com o elemento do meio e, se ele não for o alvo, "
    "mais uma pelo teste que decide qual metade descartar.",
]

CONSIDERACOES = [
    "Os exercícios mostraram, com números medidos, a diferença entre as principais classes de complexidade. "
    "A busca binária, O(log N), resolve o problema cortando o espaço de busca pela metade a cada passo. A "
    "busca linear, O(N), cresce na mesma proporção da entrada. O Bubble Sort e a versão original do maior "
    "número único, O(N²), quadruplicam o trabalho quando a entrada dobra.",
    "Em todos os casos os resultados empíricos confirmaram a análise assintótica: a busca linear fez "
    "exatamente N comparações no pior caso, o Bubble Sort fez exatamente N(N-1)/2 comparações e o número de "
    "voltas no tabuleiro de xadrez cresceu como log Q. Também ficou claro que o Big O descreve o pior caso e "
    "o crescimento, e não cada execução isolada, como mostrou a busca binária perdendo da linear no alvo da "
    "primeira posição. Por fim, a refatoração do Exercício 14 mostrou que é possível tornar o código legível "
    "sem alterar comportamento nem complexidade, desde que um teste comprove a equivalência.",
]

# Consolas cobre os acentos e símbolos do código; Courier é o fallback
MONO = "Courier"
if os.path.exists(r"C:\Windows\Fonts\consola.ttf"):
    pdfmetrics.registerFont(TTFont("Consolas", r"C:\Windows\Fonts\consola.ttf"))
    MONO = "Consolas"

SECAO = ParagraphStyle("Secao", fontName="Times-Bold", fontSize=12, leading=18, spaceBefore=6, spaceAfter=12)
CORPO = ParagraphStyle(
    "Corpo", fontName="Times-Roman", fontSize=12, leading=18, alignment=TA_JUSTIFY,
    firstLineIndent=1.25 * cm, spaceAfter=6,
)
ITEM = ParagraphStyle("Item", parent=CORPO, firstLineIndent=0, leftIndent=1.25 * cm, spaceAfter=3)
LEGENDA = ParagraphStyle("Legenda", fontName="Times-Roman", fontSize=10, leading=12, alignment=TA_CENTER, spaceAfter=4)
FONTE = ParagraphStyle("Fonte", parent=LEGENDA, spaceBefore=4, spaceAfter=14)
SUBTITULO = ParagraphStyle("Sub", fontName="Times-Bold", fontSize=12, leading=18, spaceBefore=6, spaceAfter=6)
CELULA = ParagraphStyle("Celula", fontName="Times-Roman", fontSize=10, leading=12)
CELULA_B = ParagraphStyle("CelulaB", parent=CELULA, fontName="Times-Bold")
FORMULA = ParagraphStyle("Formula", parent=CORPO, alignment=TA_CENTER, firstLineIndent=0, spaceBefore=4, spaceAfter=10)


# Cada exercício é uma lista de blocos:
#   ("p", texto)                 parágrafo
#   ("i", texto)                 item de lista (recuado)
#   ("f", texto)                 fórmula centralizada
#   ("s", texto)                 subtítulo
#   ("t", legenda, linhas)       tabela (a primeira linha é o cabeçalho)
#   ("print", chave, legenda)    captura do terminal (screenshots/<chave>*.png)
#   ("codigo", arquivo)          link para o código-fonte do exercício no GitHub
EXERCICIOS = [
    (1, "Busca linear instrumentada", [
        ("p", "Foi gerado um array não ordenado com 10.000 números inteiros distintos, usando "
              "<i>random.sample</i>, que sorteia sem repetição. A semente fixa (42) faz o array ser sempre o "
              "mesmo. A função <i>busca_linear</i> percorre o array do início ao fim e soma 1 ao contador "
              "<b>antes</b> de cada comparação <i>arr[i] == alvo</i>, de modo que até a comparação que resulta "
              "em falso é contabilizada. Ela retorna o índice encontrado (ou -1) e o total de comparações."),
        ("p", "Na busca pelo elemento da primeira posição, como pede o enunciado, foram registradas "
              "<b>1 comparação</b>. Esse resultado, porém, é o melhor caso e não mostra o custo real do "
              "algoritmo. Por isso foram executados também três casos extras, apresentados na Tabela 1."),
        ("t", "Comparações da busca linear por posição do alvo (N = 10.000)", [
            ["Posição do alvo", "Índice", "Comparações", "Caso"],
            ["Primeira (pedido do enunciado)", "0", "1", "Melhor caso"],
            ["Meio do array", "5.000", "5.001", "Caso médio"],
            ["Última posição", "9.999", "10.000", "Pior caso com sucesso"],
            ["Elemento ausente", "-1", "10.000", "Pior caso"],
        ]),
        ("p", "O número de comparações é sempre a posição do alvo mais um. No pior caso ele é igual a N: com "
              "10.000 itens, 10.000 comparações. Se o array tivesse 1 milhão de itens, seriam até 1 milhão. "
              "O custo cresce na mesma proporção da entrada, logo a busca linear é <b>O(N)</b>."),
        ("print", "ex01", "Execução da busca linear instrumentada"),
        ("codigo", "ex01_busca_linear.py"),
    ]),
    (2, "Ordenação com cartas (algoritmo conceitual)", [
        ("p", "<b>Restrições consideradas.</b> As 13 cartas de espadas ficam viradas para cima, lado a lado, "
              "em uma fileira. Só é permitido comparar duas cartas <b>vizinhas</b> e trocá-las de lugar. Não "
              "há espaço auxiliar na mesa nem é permitido retirar uma carta do meio para encaixá-la em outro lugar."),
        ("p", "<b>Estado inicial:</b> as 13 cartas (A, 2, 3, ..., 10, J, Q, K) embaralhadas na fileira, com "
              "A = 1, J = 11, Q = 12 e K = 13. <b>Operações permitidas:</b> comparar duas cartas vizinhas e "
              "trocá-las. <b>Estado final:</b> a fileira em ordem crescente, de A até K."),
        ("s", "Algoritmo passo a passo"),
        ("i", "1. Comece pela carta mais à esquerda."),
        ("i", "2. Compare a carta atual com a vizinha da direita. Se a da esquerda for maior, troque as duas."),
        ("i", "3. Avance uma posição e repita o passo 2 até o fim da parte ainda não ordenada."),
        ("i", "4. Ao fim da rodada, a maior carta fora do lugar chegou ao final da fileira e não sai mais de lá. "
              "Na próxima rodada, pare uma posição antes."),
        ("i", "5. Se uma rodada inteira terminar sem nenhuma troca, a fileira está ordenada. Pare."),
        ("p", "<b>Algoritmo clássico:</b> o procedimento é o <b>Bubble Sort</b>. A justificativa está nas "
              "operações: a única ação possível é comparar e trocar elementos vizinhos, que é a definição do "
              "Bubble Sort, e a cada rodada o maior elemento restante sobe até o fim da fileira, como uma bolha. "
              "A parada quando uma rodada não faz trocas é a otimização clássica do algoritmo (Exercício 12)."),
        ("p", "<b>Custo:</b> na primeira rodada são 12 comparações, na segunda 11, e assim até 1. No pior caso:"),
        ("f", "(N - 1) + (N - 2) + ... + 1 = N(N - 1) / 2 = 13 × 12 / 2 = 78 comparações"),
        ("p", "O total cresce como N²/2. Descartando a constante, o custo é <b>O(N²)</b>. No melhor caso "
              "(cartas já ordenadas), a parada antecipada encerra após uma rodada de 12 comparações: O(N). A "
              "simulação abaixo embaralhou as cartas com semente 42 e ordenou com 77 comparações e 47 trocas. "
              "Ela mostra também a carta A, que estava perto do fim e andou só uma posição para a esquerda por "
              "rodada, levando 10 rodadas para chegar ao início."),
        ("print", "ex02", "Simulação do algoritmo das cartas, rodada por rodada"),
        ("codigo", "ex02_ordenacao_cartas.py"),
    ]),
    (3, "Busca linear: análise manual", [
        ("p", "Considerando o array ordenado [2, 4, 6, 8, 10, 12, 13] (N = 7), a busca linear pelo valor 8 "
              "compara os elementos um a um, a partir do índice 0, como mostra a Tabela {tab}."),
        ("t", "Simulação manual da busca linear pelo valor 8", [
            ["Passo", "Índice", "Valor", "8 == valor?"],
            ["1", "0", "2", "Não"],
            ["2", "1", "4", "Não"],
            ["3", "2", "6", "Não"],
            ["4", "3", "8", "Sim, encontrado"],
        ]),
        ("p", "Foram realizadas <b>4 comparações</b>. A justificativa é a posição do valor: o 8 está no índice "
              "3, e a busca linear precisa passar por todos os elementos anteriores a ele, ou seja, faz índice "
              "+ 1 comparações. A busca linear também não aproveita o fato de o array estar ordenado: faria as "
              "mesmas 4 comparações em um array desordenado com o 8 na mesma posição."),
        ("p", "Relacionando com o tamanho do array: com N = 7, a busca linear faz de 1 comparação (melhor caso) "
              "a 7 comparações (pior caso, valor ausente ou na última posição). O pior caso cresce junto com N, "
              "o que caracteriza O(N). A conferência desta simulação aparece na parte de cima da Figura {fig}."),
        ("print", "ex03", "Rastreio da busca linear e da busca binária (Exercícios 3 e 4)"),
        ("codigo", "ex03_ex04_busca_manual.py"),
    ]),
    (4, "Busca binária: análise manual", [
        ("p", "No mesmo array, a busca binária começa com o intervalo inteiro (início = 0, fim = 6) e compara o "
              "alvo com o elemento do meio. A Tabela {tab} mostra a simulação."),
        ("t", "Simulação manual da busca binária pelo valor 8", [
            ["Passo", "início", "fim", "meio = (início + fim) // 2", "arr[meio]", "Decisão"],
            ["1", "0", "6", "(0 + 6) // 2 = 3", "8", "8 == 8: encontrado"],
        ]),
        ("p", "Foi realizada <b>1 comparação</b>, contra 4 da busca linear. O 8 estava exatamente no meio do "
              "array. Para comparar os dois algoritmos sem depender da sorte, também foi simulado o pior caso, "
              "com um valor ausente (14). A Tabela {tab2} resume os resultados, conferidos na parte de baixo da "
              "Figura {fig03}."),
        ("t", "Busca linear x busca binária no array de 7 elementos", [
            ["Cenário", "Busca linear", "Busca binária"],
            ["Buscar o 8", "4 comparações", "1 comparação"],
            ["Pior caso (valor ausente)", "7 comparações", "3 iterações (6 comparações)"],
            ["Notação Big O", "O(N)", "O(log N)"],
        ]),
        ("p", "A diferença se explica pelo Big O. A busca binária descarta metade do intervalo a cada passo, "
              "então precisa de no máximo cerca de log<sub>2</sub> N iterações: com N = 7, 3 iterações (log<sub>2</sub> 8 = 3). A "
              "linear pode precisar de N. Com N pequeno a diferença parece modesta, mas com N = 1.000.000 a "
              "linear pode fazer 1.000.000 de comparações e a binária no máximo 20 iterações. Cada vez que N "
              "dobra, a linear dobra e a binária ganha apenas uma iteração. O pré-requisito da binária é o "
              "array estar ordenado; sem isso, ela descarta a metade errada."),
    ]),
    (5, "Otimização de O(N²) para O(N)", [
        ("p", "<b>Gargalo.</b> A função original tem um laço dentro de outro. Para cada um dos N elementos, o "
              "laço interno percorre o array inteiro de novo para contar quantas vezes aquele valor aparece. "
              "São N × N = N² comparações, e valores repetidos ainda são recontados várias vezes."),
        ("p", "<b>Estratégia.</b> Em vez de perguntar N vezes \"quantas vezes este valor aparece?\", a nova "
              "versão percorre o array <b>uma única vez</b> e anota a contagem de cada valor em um dicionário. "
              "Em seguida, uma segunda passada pelas chaves do dicionário escolhe o maior valor com contagem 1. "
              "O dicionário é uma tabela hash: consultar e atualizar uma chave custa O(1) em média."),
        ("p", "<b>Nova complexidade.</b> A primeira passada faz N iterações de custo O(1), ou seja, O(N). A "
              "segunda passada faz no máximo N iterações de custo O(1), também O(N). O total é O(2N) = "
              "<b>O(N)</b>, já que constantes são descartadas. O custo extra é a memória do dicionário, O(N): "
              "troca-se memória por velocidade."),
        ("p", "<b>Corretude.</b> As duas versões foram comparadas em 6 casos de borda (lista vazia, nenhum "
              "valor único, um único elemento, negativos e repetidos) e em 200 listas aleatórias, sempre com o "
              "mesmo resultado. A Tabela {tab} mostra o crescimento do trabalho."),
        ("t", "Iterações da versão original e da otimizada", [
            ["N", "Original (N²)", "Otimizada (~2N)"],
            ["10", "100", "20"],
            ["100", "10.000", "200"],
            ["1.000", "1.000.000", "2.000"],
            ["10.000", "100.000.000", "20.000"],
        ]),
        ("print", "ex05", "Comparação entre a versão original e a otimizada"),
        ("codigo", "ex05_maior_unico.py"),
    ]),
    (6, "Tabuleiro de xadrez e grãos de arroz", [
        ("p", "A função <i>menor_quadrado(qtd_graos)</i> recebe uma quantidade de grãos e devolve o primeiro "
              "quadrado que, sozinho, tem pelo menos essa quantidade. Ela valida a entrada (inteiro positivo), "
              "começa no quadrado 1 com 1 grão e, a cada volta, verifica se o quadrado atual já atende ao alvo; "
              "se não atende, dobra os grãos para o quadrado seguinte. Não é usada nenhuma fórmula pronta, como "
              "logaritmo: o cálculo é feito só por iteração, e um contador registra as voltas do laço."),
        ("p", "Se o laço passar pelos 64 quadrados sem alcançar o alvo, a função devolve a mensagem de que o "
              "valor excede o limite do tabuleiro. O total de grãos do tabuleiro, 2<super>64</super> - 1 = "
              "18.446.744.073.709.551.615, é calculado também por iteração e usado para montar o teste acima "
              "do limite. A Tabela {tab} resume os testes."),
        ("t", "Testes da função menor_quadrado", [
            ["qtd_graos", "Quadrado", "Iterações", "Tipo de teste"],
            ["1, 2, 4, 8", "1, 2, 3, 4", "1, 2, 3, 4", "Valores pequenos"],
            ["3, 5", "3, 4", "3, 4", "Entre potências de 2"],
            ["1.000", "11", "11", "Intermediário"],
            ["1.000.000", "21", "21", "Intermediário"],
            ["2^63 (grãos do quadrado 64)", "64", "64", "Limite exato"],
            ["Total do tabuleiro + 1", "Excede o limite", "64", "Acima do total"],
        ]),
        ("p", "<b>Complexidade.</b> O laço executa uma volta por quadrado até chegar à resposta, e como os "
              "grãos dobram a cada quadrado, o quadrado da resposta é aproximadamente log<sub>2</sub>(Q) + 1, em que Q é a "
              "quantidade pedida. Multiplicar o pedido por 1.000 (de 1.000 para 1.000.000) acrescentou apenas "
              "10 iterações (de 11 para 21). A complexidade é, portanto, <b>O(log Q)</b>. Como o tabuleiro tem "
              "64 quadrados, o laço nunca passa de 64 iterações, um teto constante."),
        ("p", "Observação: o quadrado 64 tem 2<super>63</super> grãos, mas o total do tabuleiro é quase o "
              "dobro. Um valor entre os dois não cabe em nenhum quadrado e também não ultrapassa o total; nesse "
              "caso a função devolve a mesma mensagem de limite, porque nenhum quadrado o alcança sozinho."),
        ("print", "ex06", "Testes do tabuleiro de xadrez"),
        ("codigo", "ex06_tabuleiro_xadrez.py"),
    ]),
    (7, "Notação Big O: análise de código", [
        ("p", "A função <i>only_a_strings</i> recebe uma lista de N strings e devolve apenas as que começam com "
              "a letra \"a\". A análise segue as premissas do enunciado: strings de tamanho constante e "
              "operações <i>len(s)</i>, <i>s[0] == \"a\"</i> e <i>append</i> de custo O(1)."),
        ("p", "<b>1. Execuções do laço.</b> O laço <i>for</i> executa exatamente <b>N vezes</b>, uma por "
              "elemento. Não há <i>break</i>, então ele sempre percorre a lista inteira."),
        ("p", "<b>2. Operações por iteração.</b> Em cada volta: <i>len(s) &gt; 0</i> sempre executa; "
              "<i>s[0] == \"a\"</i> só executa se a string não for vazia, pelo curto-circuito do <i>and</i>, o "
              "que também evita o erro de acessar a primeira letra de uma string vazia; <i>append</i> só "
              "executa se a string começar com \"a\". São de 1 a 3 operações constantes por volta."),
        ("p", "<b>3. Custo total.</b> T(N) = c<sub>1</sub> + c<sub>2</sub> · N, em que c<sub>1</sub> é o "
              "trabalho fixo (criar a lista de resultado e retorná-la) e c<sub>2</sub>, entre 1 e 3, é o "
              "trabalho constante de cada volta."),
        ("p", "<b>4. Big O.</b> <b>O(N)</b>."),
        ("p", "<b>5. Justificativa.</b> Há um único laço, não aninhado, que visita cada elemento uma vez, com "
              "trabalho constante dentro dele. Uma constante multiplicada por N cresce linearmente. O termo "
              "c<sub>1</sub> não depende de N e é descartado. Uma versão instrumentada confirmou a análise: a "
              "razão entre operações e N ficou estável em 2,33 de N = 100 até N = 100.000."),
        ("print", "ex07", "Confirmação empírica do custo linear de only_a_strings"),
        ("codigo", "ex07_only_a_strings.py"),
    ]),
    (8, "Bubble Sort bidirecional (Cocktail Sort)", [
        ("p", "O Cocktail Sort usa dois índices externos, <i>esquerdo</i> e <i>direito</i>, que delimitam a "
              "parte ainda não ordenada. Cada rodada tem duas passadas. Na ida, da esquerda para a direita, o "
              "<b>maior</b> elemento da faixa é levado até <i>direito</i>, que então diminui uma posição. Na "
              "volta, da direita para a esquerda, o <b>menor</b> elemento é levado até <i>esquerdo</i>, que "
              "então aumenta uma posição. O algoritmo para quando os índices se encontram ou quando uma passada "
              "não faz trocas."),
        ("p", "O algoritmo foi testado com arrays aleatório, já ordenado, decrescente, com repetidos, com um "
              "elemento pequeno no fim, vazio e com um único elemento, todos ordenados corretamente. A Tabela "
              "{tab} compara as comparações feitas pelo Cocktail e pelo Bubble Sort tradicional, ambos com "
              "parada antecipada."),
        ("t", "Comparações: Bubble Sort tradicional x Cocktail Sort", [
            ["Caso", "Bubble Sort", "Cocktail Sort"],
            ["Elemento pequeno no fim [2, 3, 4, 5, 6, 7, 8, 1]", "28", "18"],
            ["Aleatório (10 elementos)", "42", "35"],
            ["Com repetidos (9 elementos)", "30", "26"],
            ["Decrescente (8 elementos)", "28", "28"],
            ["Já ordenado (8 elementos)", "7", "7"],
        ]),
        ("p", "<b>Comparação conceitual.</b> No Bubble Sort tradicional, um elemento pequeno no fim da lista "
              "anda apenas uma posição para a esquerda por passada (as chamadas \"tartarugas\"). No Cocktail, a "
              "passada de volta leva esse elemento ao início de uma só vez, o que reduz o número de passadas: "
              "de 28 para 18 comparações no caso testado. Porém, no pior caso (lista decrescente) os dois "
              "empatam, com cerca de N²/2 comparações. O Cocktail melhora a constante e alguns cenários, mas "
              "continua <b>O(N²)</b> no pior caso e O(N) no melhor."),
        ("print", "ex08", "Testes do Cocktail Sort e comparação com o Bubble Sort"),
        ("codigo", "ex08_cocktail_sort.py"),
    ]),
    (9, "Bubble Sort numérico", [
        ("p", "O Bubble Sort compara pares vizinhos e troca os que estão fora de ordem. O laço externo, "
              "<i>for ultimo in range(n - 1, 0, -1)</i>, define até onde cada passada vai: como a cada passada "
              "o maior elemento restante chega ao fim, a passada seguinte pode parar uma posição antes. O laço "
              "interno percorre os pares até essa posição. A função ordena uma cópia, sem alterar a lista "
              "original."),
        ("p", "A corretude foi verificada sem usar <i>sorted()</i>, com duas funções: <i>esta_ordenada</i>, que "
              "confere se cada elemento é menor ou igual ao vizinho da direita, e <i>mesmos_elementos</i>, que "
              "confere com <i>Counter</i> se nenhum elemento foi perdido ou criado. Foram testadas listas já "
              "ordenadas e desordenadas, como pede o enunciado, e também decrescente, com repetidos, com "
              "negativos e zero, com decimais, com um único elemento e vazia. Os 8 testes passaram, e um "
              "<i>assert</i> interromperia a execução em caso de falha."),
        ("print", "ex09", "Evidência de execução do Bubble Sort numérico"),
        ("codigo", "ex09_bubble_sort_numerico.py"),
    ]),
    (10, "Bubble Sort para strings", [
        ("p", "O algoritmo é o mesmo do Exercício 9. A única mudança é o critério de comparação, que passou a "
              "ser uma função <i>chave</i> opcional. Sem chave, o Python compara as strings letra por letra pelo "
              "código Unicode de cada caractere, o que é chamado de ordem lexicográfica. A Tabela {tab} resume "
              "o comportamento observado nos testes."),
        ("t", "Comportamento observado na comparação direta de strings", [
            ["Comportamento", "Exemplo", "Motivo"],
            ["Maiúsculas vêm antes de minúsculas", "Banana antes de abacate", "ord('B') = 66 < ord('a') = 97"],
            ["Palavras acentuadas vão para o fim", "ábaco depois de zebra", "ord('á') = 225 > ord('z') = 122"],
            ["Prefixo vem antes da palavra maior", "ca < cas < casa", "a palavra menor termina primeiro"],
            ["Números são comparados como texto", "item10 antes de item2", "compara '1' com '2', não 10 com 2"],
        ]),
        ("p", "Para obter a ordem alfabética esperada por uma pessoa, foi criada a função "
              "<i>chave_alfabetica</i>, que normaliza a palavra apenas no momento da comparação: separa e remove "
              "os acentos com <i>unicodedata</i> e ignora maiúsculas com <i>casefold</i>. As palavras originais "
              "são mantidas na saída. Os resultados foram validados com a mesma chave usada na ordenação. A "
              "complexidade continua O(N²) em comparações; cada comparação de strings custa até o tamanho delas, "
              "que nos testes é pequeno e constante."),
        ("print", "ex10", "Ordenação de strings: comparação direta e ordem alfabética"),
        ("codigo", "ex10_bubble_sort_strings.py"),
    ]),
    (11, "Instrumentação do Bubble Sort", [
        ("p", "O Bubble Sort clássico, sem parada antecipada, recebeu dois contadores. O de comparações fica "
              "<b>fora</b> do <i>if</i>, para contar toda comparação entre vizinhos; o de trocas fica "
              "<b>dentro</b> do <i>if</i>, para contar só as trocas realizadas. O algoritmo foi executado para "
              "N = 25, 50, 100, 200, 400 e 800, cada tamanho o dobro do anterior, em três perfis de dados: "
              "aleatório, já ordenado e decrescente."),
        ("t", "Comparações e trocas do Bubble Sort clássico", [
            ["N", "Comparações (todos os perfis)", "Trocas: aleatório", "Trocas: ordenado", "Trocas: decrescente"],
            ["25", "300", "165", "0", "300"],
            ["50", "1.225", "582", "0", "1.225"],
            ["100", "4.950", "2.535", "0", "4.950"],
            ["200", "19.900", "10.124", "0", "19.900"],
            ["400", "79.800", "41.210", "0", "79.800"],
            ["800", "319.600", "156.792", "0", "319.600"],
        ]),
        ("p", "<b>Análise do crescimento.</b> As comparações não dependem dos dados: em todos os perfis foram "
              "exatamente N(N - 1)/2, porque o laço só termina quando os índices acabam. As trocas dependem dos "
              "dados, pois cada troca desfaz um par fora de ordem: zero na lista ordenada, cerca de N²/4 na "
              "aleatória e N(N - 1)/2 na decrescente. A cada vez que N dobrou, as comparações foram "
              "multiplicadas por 4,08, 4,04, 4,02, 4,01 e 4,01, valores que se aproximam de 4 porque "
              "(2N)² = 4N². Esse é o comportamento de um algoritmo <b>O(N²)</b>; se fosse O(N), a razão seria 2."),
        ("print", "ex11", "Contagem de comparações e trocas para diferentes tamanhos de entrada"),
        ("codigo", "ex11_bubble_sort_instrumentado.py"),
    ]),
    (12, "Bubble Sort otimizado", [
        ("p", "A otimização adiciona a variável <i>houve_troca</i>. Ela começa falsa em cada passada e vira "
              "verdadeira quando ocorre uma troca. Se uma passada inteira termina sem trocas, todos os vizinhos "
              "estão em ordem e o algoritmo para. O script importa o gerador de entradas do Exercício 11, então "
              "os dados são exatamente os mesmos, e confere que as duas versões produzem a mesma lista e o "
              "mesmo número de trocas."),
        ("t", "Bubble Sort clássico x otimizado, N = 800", [
            ["Perfil", "Comparações clássico", "Comparações otimizado", "Economia", "Passadas"],
            ["Já ordenado", "319.600", "799", "99,8%", "1"],
            ["Aleatório", "319.600", "319.600", "0%", "799"],
            ["Decrescente", "319.600", "319.600", "0%", "799"],
        ]),
        ("p", "<b>Ganho obtido.</b> O ganho foi grande apenas na lista já ordenada, em que uma única passada de "
              "N - 1 comparações bastou. Nas listas aleatórias o ganho foi pequeno (1,6% com N = 100) e "
              "desapareceu com N = 800, porque algum elemento pequeno perto do fim precisou de todas as passadas "
              "para chegar ao início. Na lista decrescente não houve ganho."),
        ("p", "<b>Relação com Big O.</b> O melhor caso caiu de O(N²) para <b>O(N)</b>. O caso médio e o pior "
              "caso continuam <b>O(N²)</b>. Como o Big O costuma expressar o pior caso, a complexidade do "
              "algoritmo não muda; a otimização é útil quando os dados chegam já ou quase ordenados."),
        ("print", "ex12", "Comparação entre o Bubble Sort clássico e o otimizado"),
        ("codigo", "ex12_bubble_sort_otimizado.py"),
    ]),
    (13, "Comparação de estratégias de busca", [
        ("s", "Parte A: implementação instrumentada"),
        ("p", "Foram implementadas as três funções pedidas. <i>linear_search_count(arr, target)</i> retorna "
              "(índice, comparações), contando cada <i>arr[i] == target</i>. <i>binary_search_count(sorted_arr, "
              "target)</i> assume o array ordenado e conta as comparações de chave com o elemento do meio. "
              "<i>bubble_sort_count(arr)</i> ordena uma cópia, sem alterar a lista original, e retorna (lista "
              "ordenada, comparações entre pares adjacentes). Foi usado o Bubble Sort clássico, o mesmo do "
              "Exercício 14, que sempre faz N(N - 1)/2 = 465 comparações com N = 31."),
        ("s", "Parte B: casos de teste controlados"),
        ("p", "Foram criadas três listas com N = 31: <i>arr_sorted</i> (1 a 31), <i>arr_reverse</i> (31 a 1) e "
              "<i>arr_random</i> (os mesmos números embaralhados com <i>random.seed(42)</i>). Em cada uma foram "
              "buscados o primeiro elemento, o elemento da posição N // 2 e o valor -1, que não existe nas "
              "listas. Nas listas não ordenadas, a busca binária foi feita sobre a cópia ordenada pelo Bubble "
              "Sort, e o custo da ordenação foi somado."),
        ("t", "Comparações das buscas (N = 31)", [
            ["Lista", "Alvo", "Linear", "Binária", "Bubble Sort", "Bubble + binária"],
            ["arr_sorted", "first (1)", "1", "9", "não precisa", "9"],
            ["arr_sorted", "middle (16)", "16", "1", "não precisa", "1"],
            ["arr_sorted", "absent (-1)", "31", "10", "não precisa", "10"],
            ["arr_reverse", "first (31)", "1", "9", "465", "474"],
            ["arr_reverse", "middle (16)", "16", "1", "465", "466"],
            ["arr_reverse", "absent (-1)", "31", "10", "465", "475"],
            ["arr_random", "first (20)", "1", "5", "465", "470"],
            ["arr_random", "middle (29)", "16", "9", "465", "474"],
            ["arr_random", "absent (-1)", "31", "10", "465", "475"],
        ]),
        ("print", "ex13", "Comparações da busca linear, da busca binária e do Bubble Sort"),
        ("s", "Parte C: interpretação e Big O"),
        ("p", "<b>Pré-requisitos.</b> A busca linear não exige nada: funciona em qualquer lista, ordenada ou "
              "não. A busca binária exige a lista ordenada; em uma lista desordenada ela descarta a metade "
              "errada e pode não encontrar um elemento que existe."),
        ("p", "<b>Big O.</b> A busca linear é O(N): fez exatamente 31 comparações no pior caso, com N = 31. A "
              "busca binária é O(log N): nunca passou de 5 iterações, ou 10 comparações, já que log<sub>2</sub> 32 = 5. O "
              "Bubble Sort é O(N²): fez exatamente 465 comparações. Assim, ordenar e buscar uma única vez custa "
              "O(N² + log N) = O(N²), que é pior do que O(N)."),
        ("p", "<b>Quando vale pagar o Bubble Sort.</b> A ordenação é um custo fixo, pago uma vez, e cada busca "
              "posterior fica mais barata. No pior caso, com k buscas, ordenar e usar a binária compensa quando "
              "465 + 10k &lt; 31k, isto é, a partir de <b>23 buscas</b> na mesma lista. No caso médio, com a "
              "linear em cerca de 16 comparações por busca, seriam necessárias 78 buscas. Para uma ou poucas "
              "buscas, a linear direta é sempre melhor: 31 comparações contra até 475. Com N maior a vantagem da "
              "linear cresce, porque o Bubble Sort cresce com N² e a linear com N; na prática, usaria-se uma "
              "ordenação O(N log N)."),
        ("p", "<b>Relação com os resultados.</b> Os números confirmam a análise: a linear só depende da posição "
              "do alvo (1, 16 e 31 em todas as listas), a binária ficou sempre em até 10 comparações e o Bubble "
              "Sort fez exatamente N(N - 1)/2. O alvo <i>first</i> mostra que a binária pode perder em um caso "
              "isolado (9 contra 1), porque o primeiro elemento é o melhor caso da linear e quase o pior da "
              "binária. O Big O descreve o crescimento no pior caso, e não cada execução."),
        ("codigo", "ex13_comparacao_buscas.py"),
    ]),
    (14, "Organização de código e qualidade (refatoração)", [
        ("p", "Antes de refatorar, o código foi interpretado: <i>f</i> é uma busca binária que conta "
              "comparações e <i>h</i> é um Bubble Sort clássico que conta comparações. A refatoração preservou "
              "a lógica, os contadores e os critérios de parada, e não usa <i>sorted</i>, <i>.sort()</i> nem "
              "bibliotecas externas. A Tabela {tab} mostra as principais mudanças."),
        ("t", "Principais mudanças da refatoração", [
            ["Original", "Refatorado", "Motivo"],
            ["f(a, t)", "binary_search_with_count(sorted_values, target)", "O nome diz o que a função faz e que a lista deve estar ordenada"],
            ["h(arr)", "bubble_sort_with_count(values)", "O nome diz o algoritmo e que ele conta comparações"],
            ["c, k", "comparisons", "Nome descritivo para o contador"],
            ["i, j, m", "low, high, middle", "Limites e meio do intervalo"],
            ["last, p, b", "last_unsorted, position, result", "Último índice não ordenado, posição e resultado"],
            ["r = m; break", "return middle, comparisons", "Mesmo resultado, com menos estado"],
            ["-1", "NOT_FOUND", "Constante nomeada no lugar de um número solto"],
            ["Troca com tmp (3 linhas)", "swap(values, i, j)", "Uma função que expressa a intenção"],
        ]),
        ("p", "Foram adicionadas docstrings com entradas, saídas e complexidade, e comentários que explicam o "
              "motivo de cada contador e de cada descarte. As complexidades foram mantidas: O(log N) na busca "
              "binária e O(N²) no Bubble Sort. O código original foi mantido no arquivo apenas como referência "
              "para o teste de equivalência."),
        ("p", "<b>Teste de equivalência.</b> O teste executa as duas versões lado a lado e compara as tuplas "
              "completas, com o resultado e o contador. Foram usadas 307 listas: 7 casos de borda (vazia, um "
              "elemento, dois elementos, todos iguais, negativos com repetidos, já ordenada e decrescente) e "
              "300 listas aleatórias com repetidos. Para cada lista foram buscados todos os valores presentes e "
              "três valores ausentes, totalizando 6.556 buscas. Todas as comparações foram iguais, e o teste "
              "também confirma que nenhuma versão altera a lista de entrada."),
        ("print", "ex14", "Teste de equivalência entre o código original e o refatorado"),
        ("codigo", "ex14_refatoracao.py"),
    ]),
]


def desenhar_capa(c, doc):
    largura, altura = A4
    meio = largura / 2

    def texto(y_topo, conteudo, fonte="Times-Roman", tamanho=12):
        c.setFont(fonte, tamanho)
        c.drawCentredString(meio, altura - y_topo - tamanho, conteudo)

    if os.path.exists(LOGO):
        c.drawImage(LOGO, meio - 51, altura - 187, width=102, height=102, mask="auto")
    texto(201, CAPA["instituicao"], "Times-Bold")
    y = 217
    for linha in CAPA["linhas"]:
        texto(y, linha)
        y += 16
    texto(277, CAPA["disciplina"])
    texto(400, CAPA["trabalho"], "Times-Bold", 14)
    texto(428, CAPA["titulo"], "Times-Bold", 14)
    texto(550, f"Aluno: {ALUNO}")

    def link(y_topo, rotulo, url):
        texto(y_topo, rotulo, "Times-Bold", 11)
        c.setFillColor(colors.blue)
        texto(y_topo + 14, url, tamanho=10)
        c.setFillColor(colors.black)
        w = c.stringWidth(url, "Times-Roman", 10)
        base = altura - y_topo - 14 - 10
        c.line(meio - w / 2, base - 1.5, meio + w / 2, base - 1.5)
        c.linkURL(url, (meio - w / 2, base - 3, meio + w / 2, base + 10), relative=0)

    link(588, "Vídeo de apresentação:", LINK_VIDEO)
    link(626, "Código-fonte:", REPO)
    texto(679, CAPA["cidade"])
    texto(695, CAPA["ano"])


def numerar_pagina(c, doc):
    c.setFont("Times-Roman", 10)
    c.drawRightString(A4[0] - 2 * cm, A4[1] - 1.5 * cm, str(doc.page))


def screenshots(chave):
    return sorted(glob.glob(os.path.join(SHOTS, f"{chave}*.png")))


def imagem(caminho, largura_max, altura_max):
    w, h = ImageReader(caminho).getSize()
    escala = min(largura_max / w, altura_max / h, 1)
    return Image(caminho, width=w * escala, height=h * escala)


def tabela(linhas, largura):
    dados = [[Paragraph(str(c), CELULA_B if i == 0 else CELULA) for c in linha] for i, linha in enumerate(linhas)]
    t = Table(dados, colWidths=[largura / len(linhas[0])] * len(linhas[0]), repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#888888")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def main():
    saida = os.path.join(BASE, ARQUIVO_SAIDA)
    doc = SimpleDocTemplate(
        saida, pagesize=A4, title=f"{CAPA['trabalho']} - {CAPA['titulo'].title()}", author=ALUNO,
        leftMargin=3 * cm, rightMargin=2 * cm, topMargin=3 * cm, bottomMargin=2 * cm,
    )
    largura = doc.width
    story = [PageBreak()]  # página 1 é a capa, desenhada direto no canvas

    story.append(Paragraph("1 INTRODUÇÃO", SECAO))
    story += [Paragraph(p, CORPO) for p in INTRODUCAO]

    figura = 0
    num_tabela = 0
    figura_do_print = {}
    faltando = []
    for secao, (num, titulo, blocos) in enumerate(EXERCICIOS, start=2):
        story.append(PageBreak())
        story.append(Paragraph(f"{secao} EXERCÍCIO {num}: {titulo.upper()}", SECAO))

        # Números que o texto cita antes de a tabela/figura aparecer
        tabelas_da_secao = [num_tabela + k + 1 for k, b in enumerate(b for b in blocos if b[0] == "t")]
        proxima_figura = figura + 1
        refs = {
            "tab": tabelas_da_secao[0] if tabelas_da_secao else "",
            "tab2": tabelas_da_secao[1] if len(tabelas_da_secao) > 1 else "",
            "fig": proxima_figura,
            "fig03": figura_do_print.get("ex03", ""),
        }

        for bloco in blocos:
            tipo = bloco[0]
            if tipo == "p":
                story.append(Paragraph(bloco[1].format(**refs), CORPO))
            elif tipo == "i":
                story.append(Paragraph(bloco[1], ITEM))
            elif tipo == "f":
                story.append(Paragraph(bloco[1], FORMULA))
            elif tipo == "s":
                story.append(Paragraph(bloco[1], SUBTITULO))
            elif tipo == "t":
                num_tabela += 1
                story.append(KeepTogether([
                    Spacer(1, 4),
                    Paragraph(f"Tabela {num_tabela}: {escape(bloco[1])}", LEGENDA),
                    tabela(bloco[2], largura),
                    Paragraph("Fonte: o autor (2026).", FONTE),
                ]))
            elif tipo == "print":
                chave, legenda = bloco[1], bloco[2]
                shots = screenshots(chave)
                if not shots:
                    faltando.append(chave)
                for parte, s in enumerate(shots):
                    figura += 1
                    if parte == 0:
                        figura_do_print[chave] = figura
                    sufixo = "" if parte == 0 else " (continuação)"
                    story.append(KeepTogether([
                        Spacer(1, 6),
                        Paragraph(f"Figura {figura}: {escape(legenda)}{sufixo}", LEGENDA),
                        imagem(s, largura, doc.height * 0.8),
                        Paragraph("Fonte: o autor (2026).", FONTE),
                    ]))
            elif tipo == "codigo":
                arquivo = bloco[1]
                url = f"{REPO}/blob/main/{arquivo}"
                story.append(Paragraph(
                    f"Código-fonte: <link href=\"{url}\" color='blue'><u><font face='{MONO}'>{arquivo}</font></u></link>",
                    CORPO,
                ))

    story.append(PageBreak())
    story.append(Paragraph(f"{len(EXERCICIOS) + 2} CONSIDERAÇÕES FINAIS", SECAO))
    story += [Paragraph(p, CORPO) for p in CONSIDERACOES]
    story.append(Spacer(1, 12))
    url = escape(LINK_VIDEO, {'"': "&quot;"})
    story.append(Paragraph("VÍDEO DE APRESENTAÇÃO", SUBTITULO))
    story.append(Paragraph(f"<link href=\"{url}\" color='blue'><u>{escape(LINK_VIDEO)}</u></link>", CORPO))
    story.append(Paragraph("CÓDIGO-FONTE", SUBTITULO))
    story.append(Paragraph(f"<link href=\"{REPO}\" color='blue'><u>{REPO}</u></link>", CORPO))

    doc.build(story, onFirstPage=desenhar_capa, onLaterPages=numerar_pagina)
    print(f"PDF gerado: {saida}")
    if faltando:
        print(f"Atenção: sem prints para {faltando} (rode: python gerar_prints.py)")


if __name__ == "__main__":
    main()
