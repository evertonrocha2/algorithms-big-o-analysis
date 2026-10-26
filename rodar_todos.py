"""Roda todos os exercicios em sequencia, com um cabecalho entre cada um."""

import subprocess
import sys
from pathlib import Path

PASTA = Path(__file__).parent

for script in sorted(PASTA.glob("ex*.py")):
    print("=" * 80)
    print(f">>> python {script.name}")
    print("=" * 80, flush=True)  # flush: o cabecalho sai antes da saida do script
    subprocess.run([sys.executable, str(script)], cwd=PASTA, check=True)
    print(flush=True)
