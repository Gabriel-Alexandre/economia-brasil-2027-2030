"""Importa os achados da pesquisa (listas JSON), captura cada página com hash e grava dados/evidencias/ACHADOS.csv.

Cada achado tem a fonte principal (sufixo -a) e, quando houver, a segunda fonte (sufixo -b).
A captura passa por ferramentas/capturar.py; o trecho literal é conferido depois por
ferramentas/conferir-trechos.py. Uso: python ferramentas/importar-achados.py arquivo.json [...]
"""
from __future__ import annotations

import csv
import importlib.util
import json
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "dados" / "evidencias" / "ACHADOS.csv"
CAMPOS = ["id", "tema", "fato", "numero", "unidade", "data_da_fonte", "fonte_a", "url_a", "trecho_a",
          "fonte_b", "url_b", "trecho_b", "categoria_pagamento", "custo_anual_rs_bi", "implicacao", "origem"]

spec = importlib.util.spec_from_file_location("capturar", RAIZ / "ferramentas" / "capturar.py")
cap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cap)


def ler_existentes() -> dict[str, dict]:
    if not SAIDA.exists():
        return {}
    return {l["id"]: l for l in csv.DictReader(SAIDA.open(encoding="utf-8"))}


def tipo_de(url: str, tipo: str | None) -> str | None:
    if url.lower().split("?")[0].endswith(".pdf") or (tipo or "").lower() == "pdf":
        return "pdf"
    return None


def ja_capturado(url: str) -> str:
    """Id da captura que já tem este endereço (cada endereço se baixa uma vez só)."""
    for l in cap.ler_manifesto():
        if l["url"] == url and (RAIZ / l["arquivo_texto"]).exists():
            return l["id"]
    return ""


def capturar(ident: str, url: str, tipo: str | None) -> str:
    feito = ja_capturado(url)
    if feito:
        return feito
    try:
        cap.capturar(ident, url, tipo_de(url, tipo))
        time.sleep(1)
        return ident
    except Exception as e:  # noqa: BLE001
        print(f"{ident}: captura falhou ({e})", file=sys.stderr)
        return ""


def main(arquivos: list[str]) -> int:
    linhas = ler_existentes()
    for arq in arquivos:
        origem = Path(arq).parent.name
        for a in json.loads(Path(arq).read_text(encoding="utf-8")):
            if not isinstance(a, dict) or not a.get("url") or not a.get("trecho_literal"):
                continue
            ident = a["id"]
            if ident in linhas and linhas[ident].get("fonte_a"):
                continue
            fa = capturar(f"{ident}-a", a["url"], a.get("tipo"))
            fb = ""
            if a.get("segunda_fonte_url") and a.get("segunda_fonte_trecho"):
                fb = capturar(f"{ident}-b", a["segunda_fonte_url"], None)
            linhas[ident] = {
                "id": ident, "tema": a.get("tema") or a.get("nome", ""), "fato": a.get("fato") or a.get("descricao", ""),
                "numero": a.get("numero") or "", "unidade": a.get("unidade") or "",
                "data_da_fonte": a.get("data_da_fonte") or a.get("data_e_hora") or a.get("data") or "",
                "fonte_a": fa, "url_a": a["url"], "trecho_a": a["trecho_literal"],
                "fonte_b": fb, "url_b": a.get("segunda_fonte_url") or "", "trecho_b": a.get("segunda_fonte_trecho") or "",
                "categoria_pagamento": a.get("categoria_pagamento") or "", "custo_anual_rs_bi": a.get("custo_anual_rs_bi") or "",
                "implicacao": a.get("implicacao_2027_2030") or a.get("fonte_do_dinheiro") or "", "origem": origem,
            }
            SAIDA.parent.mkdir(parents=True, exist_ok=True)
            with SAIDA.open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=CAMPOS)
                w.writeheader()
                for k in sorted(linhas):
                    w.writerow({c: linhas[k].get(c, "") for c in CAMPOS})
    print(f"{len(linhas)} achados em {SAIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
