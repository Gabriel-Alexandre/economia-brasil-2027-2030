"""Confere a linguagem dos textos públicos do projeto (pré-registro §8).

Proibido na voz do projeto: travessão, "vai quebrar", "calote", "gastança", "derreteu",
"eleitoreira", "mentiu", "fraude" e qualquer recomendação de investimento. Citação do pedido
vale entre aspas (a linha precisa ter a palavra entre aspas). Sai com código 1 se achar algo.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVOS = ["RELATORIO.md", "RESUMO_SIMPLES.md", "README.md", "ESTADO.md", "docs/LEITURA_DA_IA.md",
            "docs/REVISAO_ADVERSARIAL.md", "docs/FONTES_DE_DADOS.md", "docs/REPLICAR.md"]
PROIBIDAS = [r"—", r"–", r"vai quebrar", r"\bcalote", r"gastan[çc]a", r"derreteu", r"eleitoreir",
             r"mentiu", r"mentiroso", r"\bfraude", r"\bcompre\b", r"\bvenda suas", r"recomendamos investir"]


def citado(linha: str, padrao: str) -> bool:
    """A palavra só vale se estiver dentro de aspas (citação do pedido)."""
    for trecho in re.findall(r"[\"“«*]([^\"”»*]+)[\"”»*]", linha):
        if re.search(padrao, trecho, re.I):
            return True
    return False


def main() -> int:
    achou = 0
    for nome in ARQUIVOS:
        p = RAIZ / nome
        if not p.exists():
            continue
        for i, linha in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for padrao in PROIBIDAS:
                if re.search(padrao, linha, re.I) and not citado(linha, padrao):
                    print(f"{nome}:{i}: '{padrao}' -> {linha.strip()[:140]}")
                    achou += 1
    print(f"{achou} ocorrência(s)")
    return 1 if achou else 0


if __name__ == "__main__":
    sys.exit(main())
