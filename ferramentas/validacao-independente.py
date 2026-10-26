"""Refaz os números centrais por um segundo caminho, sem importar o pacote economia/ (pré-registro §6).

1. A dívida do S0 refeita com aritmética simples sobre a tabela da IFI, contra a própria IFI.
2. O S1 refeito com o prêmio do RESUMO, contra o RESUMO.
3. As séries do SGS baixadas de novo e comparadas com as do projeto (último valor de cada uma).
4. A variação do Ibovespa no dia seguinte às eleições (Yahoo) contra matérias da época (achados H05, H07, H10, H12).
5. A variação do dia 26/out (Yahoo) contra a segunda fonte do M1, quando houver.
Grava resultados/VALIDACAO.json e sai com erro se algum item não passar.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parents[1]
RES = RAIZ / "resultados"


def divida_simples(ifi: dict, premio: float = 0.0) -> dict:
    d, pib, s = ifi["divida_bruta"], ifi["pib_nominal"], ifi["primario_sp"]
    rep = {"2027": 0.45, "2028": 0.65, "2029": 0.80, "2030": 0.90}
    out = {"2025": d["2025"]}
    for a in ["2026", "2027", "2028", "2029", "2030"]:
        ant = str(int(a) - 1)
        cresc = pib[a] / pib[ant]
        juro = (d[a] + s[a]) * cresc / d[ant]          # (1 + i) que reproduz a IFI
        juro += rep.get(a, 0.0) * premio / 100
        out[a] = out[ant] * juro / cresc - s[a]
    return out


def main() -> int:
    itens = []
    ifi = json.loads((RAIZ / "dados" / "derivados" / "ifi_raf113.json").read_text(encoding="utf-8"))["base"]
    r = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))
    s0 = divida_simples(ifi)
    itens.append({"item": "S0 reproduz a dívida da IFI de 2026 a 2030", "passou": all(abs(s0[a] - ifi["divida_bruta"][a]) < 0.05 for a in s0)})
    premio = r["M6_divida"]["premio_pp"]
    s1 = divida_simples(ifi, premio)
    itens.append({"item": f"S1 (prêmio {premio:.2f}) igual nos dois caminhos", "passou": all(abs(s1[a] - r["M6_divida"]["S1_central"][a]) < 0.01 for a in s1),
                  "valor_2030": s1["2030"]})
    # 3. SGS de novo
    for nome, cod in [("bcb-divida-bruta-gg", 13762), ("bcb-primario-12m", 5793), ("bcb-juros-nominais-12m", 5727), ("bcb-divida-liquida-sp", 4513)]:
        nossa = json.loads((RAIZ / "dados" / "series" / f"{nome}.json").read_text(encoding="utf-8"))[-1]
        nova = None
        for _ in range(4):
            resp = requests.get(f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados?formato=json&dataInicial=01/01/2026&dataFinal=31/12/2026", timeout=60)
            if resp.ok and resp.text.startswith("["):
                nova = resp.json()[-1]
                break
            time.sleep(3)
        itens.append({"item": f"SGS {cod} baixada de novo", "passou": nossa == nova, "projeto": nossa, "de_novo": nova})
    # 4. eleições passadas contra matérias da época
    achados = {l["id"]: l for l in csv.DictReader((RAIZ / "dados" / "evidencias" / "ACHADOS.csv").open(encoding="utf-8"))}
    hist = {l["ano"]: l for l in r["M1_historico_eleicoes"]}
    for ano, ident in [(2010, "H05"), (2014, "H07"), (2018, "H10"), (2022, "H12")]:
        m = re.search(r"(sub\w+|baixa de|queda de)\s+(?:de\s+)?(\d+,\d+)%", achados[ident]["trecho_a"])
        materia = float(m.group(2).replace(",", ".")) * (-1 if m.group(1) in ("baixa de", "queda de") else 1)
        itens.append({"item": f"Ibovespa no dia seguinte a {ano}: Yahoo contra matéria ({ident})",
                      "passou": abs(hist[ano]["ibovespa_dia_pct"] - materia) < 0.02, "yahoo": round(hist[ano]["ibovespa_dia_pct"], 2), "materia": materia})
    # 5. o dia 26/out
    m1 = r.get("M1_mercado") or {}
    for c in m1.get("conferencia_segunda_fonte", []):
        itens.append({"item": c["item"], "passou": abs(c["projeto"] - c["segunda_fonte"]) <= c.get("tolerancia", 0.05), **c})
    RES.mkdir(exist_ok=True)
    (RES / "VALIDACAO.json").write_text(json.dumps({"em": dt.datetime.now().isoformat(timespec="minutes"), "itens": itens}, ensure_ascii=False, indent=1), encoding="utf-8")
    for i in itens:
        print("OK  " if i["passou"] else "FALHOU", i["item"])
    ok = sum(i["passou"] for i in itens)
    print(f"{ok} de {len(itens)} passaram")
    return 0 if ok == len(itens) else 1


if __name__ == "__main__":
    sys.exit(main())
