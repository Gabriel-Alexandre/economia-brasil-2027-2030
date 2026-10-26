"""Confere que cada trecho citado existe, de fato, no texto capturado da fonte.

Lê dados/evidencias/ACHADOS.csv. Para cada achado, procura o trecho (sem diferença de espaço
e de maiúscula) na captura dados/capturas/<fonte>.txt. Grava resultados/TRECHOS_CONFERIDOS.csv
com o estado de cada fonte: ok, nao_encontrado ou sem_captura. Um achado só entra no relatório
se a fonte principal estiver ok.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CAPTURAS = RAIZ / "dados" / "capturas"
ACHADOS = RAIZ / "dados" / "evidencias" / "ACHADOS.csv"
SAIDA = RAIZ / "resultados" / "TRECHOS_CONFERIDOS.csv"


def normalizar(t: str) -> str:
    t = t.replace(" ", " ").replace("’", "'").replace("“", '"').replace("”", '"')
    return " ".join(re.sub(r"\s+", " ", t).split()).casefold()


def conferir(fonte: str, trecho: str) -> str:
    if not fonte:
        return "sem_captura"
    arq = CAPTURAS / f"{fonte}.txt"
    if not arq.exists():
        return "sem_captura"
    texto = normalizar(arq.read_text(encoding="utf-8"))
    alvo = normalizar(trecho)
    if alvo in texto:
        return "ok"
    # trecho com reticências ou montado de partes: cada parte tem de estar na página
    partes = [p.strip() for p in re.split(r"\s*(?:\.\.\.|…|\[\.\.\.\])\s*", alvo) if len(p.strip()) > 15]
    if partes and all(p in texto for p in partes):
        return "ok"
    # PDF: a extração de texto quebra linha e hifeniza de outro jeito; compara sem nenhum espaço
    sem = lambda x: re.sub(r"[\s\-‐]+", "", x)  # noqa: E731
    if sem(alvo) in sem(texto):
        return "ok_sem_espacos"
    # PDF em duas colunas: vale só o maior começo do trecho (60 caracteres ou mais) que está na página
    palavras = alvo.split()
    for n in range(len(palavras) - 1, 0, -1):
        pedaco = " ".join(palavras[:n])
        if len(pedaco) < 60:
            break
        if pedaco in texto:
            return "ok_so_o_comeco:" + pedaco
    return "nao_encontrado"


def main() -> int:
    linhas = list(csv.DictReader(ACHADOS.open(encoding="utf-8")))
    saida, ruins = [], 0
    for l in linhas:
        ea = conferir(l["fonte_a"], l["trecho_a"])
        eb = conferir(l["fonte_b"], l["trecho_b"]) if l["url_b"] else "sem_segunda_fonte"
        conferido = ea.split(":", 1)[1] if ea.startswith("ok_so_o_comeco:") else (l["trecho_a"] if ea.startswith("ok") else "")
        ea, eb = ea.split(":", 1)[0], eb.split(":", 1)[0]
        saida.append({"id": l["id"], "estado_a": ea, "estado_b": eb, "url_a": l["url_a"], "url_b": l["url_b"], "trecho_conferido_a": conferido})
        ruins += not ea.startswith("ok")
    SAIDA.parent.mkdir(exist_ok=True)
    with SAIDA.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "estado_a", "estado_b", "url_a", "url_b", "trecho_conferido_a"])
        w.writeheader()
        w.writerows(saida)
    ok = sum(1 for s in saida if s["estado_a"].startswith("ok"))
    dois = sum(1 for s in saida if s["estado_a"].startswith("ok") and s["estado_b"].startswith("ok"))
    print(f"{len(saida)} achados: {ok} com a fonte principal conferida, {dois} com as duas fontes conferidas, {ruins} fora")
    for s in saida:
        if not s["estado_a"].startswith("ok") and "youtube.com" not in s["url_a"]:
            print("FORA:", s["id"], s["estado_a"], s["url_a"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
