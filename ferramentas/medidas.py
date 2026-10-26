"""M5: monta dados/evidencias/MEDIDAS_E_PROMESSAS.csv a partir dos achados conferidos.

O custo e a categoria de pagamento vêm de ACHADOS.csv (fonte com trecho conferido). O que este
script acrescenta, com o motivo escrito ao lado, é só a leitura de quanto do custo se repete por
ano a partir de 2027 (recorrente) e quanto foi de uma vez só. Essa leitura é do projeto, não da fonte.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ACHADOS = RAIZ / "dados" / "evidencias" / "ACHADOS.csv"
SAIDA = RAIZ / "dados" / "evidencias" / "MEDIDAS_E_PROMESSAS.csv"

# id -> (custo recorrente por ano a partir de 2027, em R$ bi, ou None; motivo)
LEITURA = {
    "M01": (27.72, "a lei vale todo ano; custo bruto de 2027 pela nota do Senado (R$ 27,72 bi), compensado na própria lei"),
    "M02": (4.7, "programa permanente; dotação de 2026 repetida"),
    "M03": (10.4, "gratuidade permanente na tarifa social; paga pela CDE, fora do Orçamento"),
    "M04": (None, "foi o modelo de 2025; em 2026 o programa entrou no Orçamento (M05)"),
    "M05": (11.47, "programa permanente; dotação de 2026 repetida"),
    "M06": (None, "crédito com garantia do FGTS do próprio trabalhador; sem custo fiscal publicado"),
    "M07": (None, "empréstimo do Fundo Social que volta ao fundo; sem custo fiscal publicado"),
    "M08": (None, "crédito extraordinário de 2026, uma vez só"),
    "M09": (None, "dinheiro do FGTS e de bancos; sem custo fiscal publicado"),
    "M10": (2.0, "renúncia com teto anual de R$ 2 bi, todo ano"),
    "M11": (None, "aporte de 2026 no fundo garantidor, uma vez só"),
    "M12": (5.0, "teto de R$ 15 bi de 2026 a 2028, dividido por 3 anos (a fonte não divide)"),
    "M13": (22.7, "reajuste permanente do benefício; custo anual a partir de 2027"),
    "M14": (39.1, "o salário mínimo maior vale para sempre na Previdência; custo de 2026 pelo Dieese"),
    "M15": (None, "medida de 2026 com prazo, uma vez só"),
    "M16": (None, "créditos extraordinários de 2026, uma vez só"),
    "M17": (None, "sem despesa pública; o custo é das empresas"),
    "M18": (None, "ressarcimento de 2025 e 2026, uma vez só"),
    "M19": (None, "sem custo publicado"),
    "M20": (1.01, "renúncia de R$ 3,04 bi de 2027 a 2029 pelo Poder360, dividida por 3 anos"),
    "M21": (None, "medida de 30 dias em out e nov/2026, uma vez só"),
}


def main() -> int:
    linhas = list(csv.DictReader(ACHADOS.open(encoding="utf-8")))
    conferidos = {l["id"] for l in csv.DictReader((RAIZ / "resultados" / "TRECHOS_CONFERIDOS.csv").open(encoding="utf-8"))
                  if l["estado_a"].startswith("ok")}
    saida = []
    for l in linhas:
        if not (l["id"].startswith("M") or l["id"].startswith("P")):
            continue
        rec, motivo = LEITURA.get(l["id"], (None, ""))
        if l["id"].startswith("P"):
            rec, motivo = None, "promessa: só entra no cenário S2 se tiver custo de duas fontes e nenhuma fonte de dinheiro declarada"
        saida.append({
            "id": l["id"], "nome": l["tema"], "data": l["data_da_fonte"], "categoria": l["categoria_pagamento"],
            "custo_informado_rs_bi": l["custo_anual_rs_bi"], "recorrente_a_partir_de_2027_rs_bi": "" if rec is None else rec,
            "motivo_da_leitura": motivo, "de_onde_vem_o_dinheiro": l["implicacao"],
            "fonte_principal_conferida": "sim" if l["id"] in conferidos else "não",
            "tem_segunda_fonte": "sim" if l["url_b"] else "não", "url": l["url_a"],
        })
    with SAIDA.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(saida[0]))
        w.writeheader()
        w.writerows(saida)
    print(f"{len(saida)} medidas e promessas em {SAIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
