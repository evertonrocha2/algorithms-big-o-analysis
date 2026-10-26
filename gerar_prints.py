"""Roda cada exercício de verdade e desenha o print do terminal (PowerShell) com o comando e a saída.

Uso:
    python gerar_prints.py

Gera screenshots/exNN*.png. Saídas longas viram mais de um print (_b, _c...), como se a tela rolasse.
"""

import glob
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(BASE, "screenshots")
COLS = 120
MAX_LINHAS = 46

# Paleta "Campbell" do Windows Terminal
BG, FG, AMARELO = "#0C0C0C", "#CCCCCC", "#F9F1A5"
FONTE = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 16)
FONTE_TITULO = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 13)
CW = FONTE.getlength("M")
LH = 20
PAD = 12
BARRA = 34


def plano(texto, cor=FG):
    return [(c, cor) for c in texto]


def quebrar(linha):
    """Quebra uma linha em pedaços de COLS colunas, como o terminal faz."""
    if not linha:
        return [[]]
    return [linha[i:i + COLS] for i in range(0, len(linha), COLS)]


def prompt(comando=None):
    linha = plano(f"PS {BASE}> ")
    if comando is None:
        return linha + [("█", FG)]
    nome, _, resto = comando.partition(" ")
    return linha + plano(nome, AMARELO) + plano(" " + resto)


def desenhar(linhas, caminho):
    largura = int(PAD * 2 + COLS * CW)
    altura = BARRA + PAD * 2 + LH * len(linhas)
    img = Image.new("RGB", (largura, altura), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, largura, BARRA], fill="#202020")
    d.rounded_rectangle([8, 6, 300, BARRA + 4], radius=6, fill=BG)
    d.text((20, 10), "Windows PowerShell", font=FONTE_TITULO, fill="#FFFFFF")
    x = largura - 30
    d.line([x - 6, 11, x + 6, 23], fill="#FFFFFF")
    d.line([x - 6, 23, x + 6, 11], fill="#FFFFFF")
    d.rectangle([x - 52, 11, x - 40, 23], outline="#FFFFFF")
    d.line([x - 98, 17, x - 86, 17], fill="#FFFFFF")

    y = BARRA + PAD
    for linha in linhas:
        xpos = PAD
        for c, cor in linha:
            if c != " ":
                d.text((xpos, y + 1), c, font=FONTE, fill=cor)
            xpos += CW
        y += LH
    img.save(caminho)


def executar(script):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, script], cwd=BASE, capture_output=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"{script} falhou:\n{r.stderr.decode('utf-8', 'replace')}")
    return r.stdout.decode("utf-8").replace("\r\n", "\n").rstrip("\n")


def main():
    os.makedirs(SHOTS, exist_ok=True)
    for antigo in glob.glob(os.path.join(SHOTS, "ex*.png")):
        os.remove(antigo)

    scripts = sorted(os.path.basename(p) for p in glob.glob(os.path.join(BASE, "ex[0-9][0-9]_*.py")))
    for script in scripts:
        saida = executar(script)
        linhas = []
        for pedaco in quebrar(prompt(f"python {script}")):
            linhas.append(pedaco)
        for texto in saida.split("\n"):
            linhas += quebrar(plano(texto.expandtabs(8)))
        linhas.append([])
        linhas.append(prompt())

        nome = script[:4]  # ex01, ex02, ...
        partes = [linhas[i:i + MAX_LINHAS] for i in range(0, len(linhas), MAX_LINHAS)]
        for n, parte in enumerate(partes):
            sufixo = "" if n == 0 else "_" + "bcdefg"[n - 1]
            desenhar(parte, os.path.join(SHOTS, f"{nome}{sufixo}.png"))
        print(f"{script}: {len(partes)} print(s)")


if __name__ == "__main__":
    main()
