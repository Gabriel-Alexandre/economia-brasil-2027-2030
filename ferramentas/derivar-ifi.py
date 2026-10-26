"""Lê as tabelas de cenário da IFI (RAF 113, jun/2026) direto do texto capturado do PDF.

Grava dados/derivados/ifi_raf113.json com, por cenário (base, otimista, pessimista):
PIB nominal (R$ bi), crescimento real, IPCA, Selic, dívida bruta (conceito BC, % do PIB) e
resultado primário, juros e nominal do setor público (% do PIB). Nenhum número é digitado à mão:
se uma linha não aparece no texto, o script para.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FONTE = RAIZ / "dados" / "capturas" / "F01-a.txt"
SAIDA = RAIZ / "dados" / "derivados" / "ifi_raf113.json"
ANOS_MACRO = list(range(2026, 2037))


def num(x: str) -> float:
    x = x.replace("%", "")
    if "," in x and "." not in x:
        x = x.replace(",", ".")
    return float(x)


def linhas_apos(texto: str, rotulo: str, n: int = 3) -> list[list[float]]:
    """As n primeiras ocorrências da linha que começa com `rotulo`, com os números dela."""
    out = []
    for m in re.finditer(re.escape(rotulo) + r"([^\n]*)", texto):
        vals = re.findall(r"-?\d+[.,]\d+%?", m.group(1))
        out.append(vals)
        if len(out) == n:
            break
    if len(out) < n:
        sys.exit(f"faltou a linha {rotulo!r}")
    return out


def main() -> int:
    t = FONTE.read_text(encoding="utf-8")
    cen = ["base", "otimista", "pessimista"]
    res = {c: {} for c in cen}
    for rot, chave, conv in [("PIB nominal (R$ bilhões)", "pib_nominal", lambda v: float(v.replace(",", ""))),
                             ("PIB - Crescimento real", "pib_real_pct", num),
                             ("IPCA", None, None),
                             ("Selic - final de período (a.a.)", "selic_fim_pct", num)]:
        if chave is None:
            continue
        for c, vals in zip(cen, linhas_apos(t, rot)):
            res[c][chave] = dict(zip(ANOS_MACRO, [conv(v) for v in vals[:11]]))
    # PIB nominal de 2025 (tabela de projeções com ponto de milhar)
    m = re.search(r"PIB . nominal \(R\$ bilhões\) (\d+\.\d{3}) 13\.667", t)
    if not m:
        sys.exit("faltou o PIB nominal de 2025")
    for c in cen:
        res[c]["pib_nominal"][2025] = float(m.group(1).replace(".", ""))
    # Tabela 13: dívida bruta, colunas dez/25 e jun/26 de cada cenário; vale a de jun/26
    div = {}
    for m in re.finditer(r"\n(20[23]\d) (\d+,\d)% (\d+,\d)% (\d+,\d)% (\d+,\d)% (\d+,\d)% (\d+,\d)%", t):
        a = int(m.group(1))
        if a not in div:
            div[a] = [num(m.group(k)) for k in range(2, 8)]
    for c, k in zip(cen, (1, 3, 5)):
        res[c]["divida_bruta"] = {a: v[k] for a, v in sorted(div.items())}
    # Tabela 15: nominal, primário e juros do setor público, em cada cenário
    sp = {}
    for m in re.finditer(r"\n(20[23]\d)((?: -?\d+,\d%){9})", t):
        a = int(m.group(1))
        if a not in sp and 2025 <= a <= 2036:
            sp[a] = [num(v) for v in m.group(2).split()]
    for c, k in zip(cen, (0, 3, 6)):
        res[c]["nominal_sp"] = {a: v[k] for a, v in sorted(sp.items())}
        res[c]["primario_sp"] = {a: v[k + 1] for a, v in sorted(sp.items())}
        res[c]["juros_sp"] = {a: v[k + 2] for a, v in sorted(sp.items())}
    res["fonte"] = {"documento": "IFI, Relatório de Acompanhamento Fiscal nº 113 (jun/2026), Tabelas 4, 5, 13 e 15",
                    "captura": "dados/capturas/F01-a.txt"}
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    b = res["base"]
    print("base: dívida", b["divida_bruta"].get(2026), "->", b["divida_bruta"].get(2030),
          "| primário SP 2027", b["primario_sp"].get(2027), "| PIB 2025", b["pib_nominal"][2025])
    return 0


if __name__ == "__main__":
    sys.exit(main())
