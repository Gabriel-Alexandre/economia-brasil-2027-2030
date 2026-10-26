"""M7.2: a previsão do mercado (Focus) feita em outubro de cada ano de eleição contra o que aconteceu."""
from __future__ import annotations

import datetime as dt

from . import series as S
from .mercado import ELEICOES


def previsao_contra_realizado(horizonte: int = 3) -> list[dict]:
    """Dívida líquida (Focus contra SGS 4513, dezembro) e PIB (Focus contra FMI) no ano eleição + horizonte."""
    dl = S.sgs("bcb-divida-liquida-sp")
    pib = S.imf("imf-weo-pib-real")["BRA"]
    linhas = []
    for ano, (d0, _) in ELEICOES.items():
        alvo = ano + horizonte
        if ano == 2026:
            continue
        dd, prev = S.focus_mediana("Dívida líquida do setor público", alvo, d0, "focus-historico")
        dreal, real = S.valor_em(dl, dt.date(alvo, 12, 1))
        prev_pib = [S.focus_mediana("PIB Total", ano + k, d0, "focus-historico")[1] for k in range(1, horizonte + 1)]
        real_pib = [pib[ano + k] for k in range(1, horizonte + 1)]
        linhas.append({
            "eleicao": ano, "previsao_feita_em": dd.isoformat(), "ano_alvo": alvo,
            "dlsp_prevista": prev, "dlsp_realizada": real, "dlsp_realizada_em": dreal.isoformat(),
            "erro_dlsp_pp": prev - real,
            "pib_medio_previsto": sum(prev_pib) / horizonte, "pib_medio_realizado": sum(real_pib) / horizonte,
            "erro_pib_pp": sum(prev_pib) / horizonte - sum(real_pib) / horizonte,
        })
    return linhas


def resumo_erros(linhas: list[dict]) -> dict:
    e = [l["erro_dlsp_pp"] for l in linhas]
    p = [l["erro_pib_pp"] for l in linhas]
    return {
        "erro_medio_absoluto_dlsp_pp": sum(abs(x) for x in e) / len(e),
        "vies_medio_dlsp_pp": sum(e) / len(e),
        "vezes_que_o_mercado_previu_divida_maior": sum(1 for x in e if x > 0),
        "maior_erro_para_menos": min(e),
        "erro_medio_absoluto_pib_pp": sum(abs(x) for x in p) / len(p),
        "vies_medio_pib_pp": sum(p) / len(p),
        "n": len(e),
    }
