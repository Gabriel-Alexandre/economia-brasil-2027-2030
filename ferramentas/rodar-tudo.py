"""Roda a cadeia inteira na ordem do docs/REPLICAR.md e para no primeiro erro.

Uso: python ferramentas/rodar-tudo.py [--sem-coleta]
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PASSOS = [
    ["ferramentas/conferir-trechos.py"],
    ["ferramentas/medidas.py"],
    ["ferramentas/mercado-do-dia.py"],
    ["ferramentas/analise.py"],
    ["ferramentas/validacao-independente.py"],
    ["ferramentas/gerar-relatorio.py"],
    ["ferramentas/gerar-leitura.py"],
    ["ferramentas/graficos.py"],
    ["ferramentas/conferir-linguagem.py"],
]


def main() -> int:
    sem_coleta = "--sem-coleta" in sys.argv
    for passo in PASSOS:
        cmd = [sys.executable, *passo]
        if sem_coleta and passo[0].endswith("mercado-do-dia.py"):
            cmd.append("--sem-coleta")
        print(">>", " ".join(passo), flush=True)
        r = subprocess.run(cmd, cwd=RAIZ)
        if r.returncode != 0:
            print(f"PAROU em {passo[0]} (código {r.returncode})", flush=True)
            return r.returncode
    r = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=RAIZ)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
