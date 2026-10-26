"""M1 e M7.1: a reação do mercado à eleição e o que veio depois nas eleições anteriores."""
from __future__ import annotations

import datetime as dt

from . import series as S

D = dt.date

# eleição decisiva (2º turno, ou 1º quando não houve) -> (último pregão antes, primeiro pregão depois)
ELEICOES = {
    2002: (D(2002, 10, 25), D(2002, 10, 28)),
    2006: (D(2006, 10, 27), D(2006, 10, 30)),
    2010: (D(2010, 10, 29), D(2010, 11, 1)),
    2014: (D(2014, 10, 24), D(2014, 10, 27)),
    2018: (D(2018, 10, 26), D(2018, 10, 29)),
    2022: (D(2022, 10, 28), D(2022, 10, 31)),
    2026: (D(2026, 10, 23), D(2026, 10, 26)),
}
VENCEDOR = {2002: "Lula", 2006: "Lula", 2010: "Dilma", 2014: "Dilma", 2018: "Bolsonaro", 2022: "Lula", 2026: "Lula"}

MOEDAS_CONTROLE = ["yahoo-usdmxn", "yahoo-usdclp", "yahoo-usdcop", "yahoo-usdzar"]


def variacao(nome: str, d0: D, d1: D, fonte: str = "yahoo") -> dict | None:
    """Variação % do fechamento de d0 (ou o último antes) ao de d1 (exato). None se d1 não existe."""
    s = S.yahoo(nome) if fonte == "yahoo" else S.sgs(nome)
    if d1 not in s.index:
        return None
    a0, v0 = S.valor_em(s, d0)
    v1 = float(s[d1])
    return {"de": a0.isoformat(), "ate": d1.isoformat(), "inicio": v0, "fim": v1, "variacao_pct": 100 * (v1 / v0 - 1)}


def media(vals: list[float | None]) -> float | None:
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None


def evento(d0: D, d1: D) -> dict:
    """Brasil contra o controle de emergentes, em %. Moeda: alta = real (ou a moeda) mais fraca."""
    ibov = variacao("yahoo-ibovespa", d0, d1)
    ewz = variacao("yahoo-ewz", d0, d1)
    eem = variacao("yahoo-eem", d0, d1)
    brl = variacao("yahoo-usdbrl", d0, d1)
    ptax = variacao("bcb-ptax-venda", d0, d1, fonte="sgs")
    moedas = {m: variacao(m, d0, d1) for m in MOEDAS_CONTROLE}
    controle_moeda = media([v["variacao_pct"] if v else None for v in moedas.values()])
    out = {
        "janela": [d0.isoformat(), d1.isoformat()],
        "ibovespa": ibov, "ewz": ewz, "eem": eem, "usdbrl_yahoo": brl, "usdbrl_ptax": ptax,
        "moedas_controle": moedas, "controle_moeda_pct": controle_moeda,
    }
    if ibov and eem:
        out["excesso_ibovespa_contra_eem_pct"] = ibov["variacao_pct"] - eem["variacao_pct"]
    if ewz and eem:
        out["excesso_ewz_contra_eem_pct"] = ewz["variacao_pct"] - eem["variacao_pct"]
    if brl and controle_moeda is not None:
        out["excesso_dolar_contra_cesta_pct"] = brl["variacao_pct"] - controle_moeda
    return out


def regua_a1(queda_pct: float) -> str:
    """Pré-registro M1: queda de 5% ou mais = confirmada; 2 a 5 = em parte; menos de 2 = não; alta = contrário."""
    if queda_pct > 0:
        return "o dado diz o contrário"
    q = -queda_pct
    if q >= 5:
        return "confirmada"
    if q >= 2:
        return "confirmada em parte"
    return "não confirmada"


def ibovespa_real(d0: D, d1: D) -> float | None:
    """Retorno real (deflacionado pelo IPCA mensal) do Ibovespa de d0 a d1, em %."""
    s = S.yahoo("yahoo-ibovespa")
    if d1 < s.index[0]:
        return None
    a0, v0 = S.valor_em(s, d0)
    a1, v1 = S.valor_em(s, d1)
    ipca = S.sgs("bcb-ipca-mensal")
    meses = ipca[(ipca.index > D(a0.year, a0.month, 1)) & (ipca.index <= D(a1.year, a1.month, 1))]
    fator = 1.0
    for v in meses:
        fator *= 1 + v / 100
    return 100 * ((v1 / v0) / fator - 1)


def depois_do_mandato(ano: int) -> dict:
    """O que veio no mandato seguinte: PIB real médio (FMI), dívida bruta (FMI) e Ibovespa real."""
    pib = S.imf("imf-weo-pib-real")["BRA"]
    div = S.imf("imf-weo-divida-bruta")["BRA"]
    anos = list(range(ano + 1, ano + 5))
    pib_vals = [pib[a] for a in anos if a in pib]
    fim = D(ano + 4, 12, 31)
    hoje = S.yahoo("yahoo-ibovespa").index[-1]
    return {
        "anos": [anos[0], anos[-1]],
        "pib_real_medio_pct": sum(pib_vals) / len(pib_vals) if pib_vals else None,
        "pib_anos_com_dado": len(pib_vals),
        "divida_bruta_inicio": div.get(ano), "divida_bruta_fim": div.get(ano + 4),
        "ibovespa_real_pct": ibovespa_real(ELEICOES[ano][1], min(fim, hoje)),
        "mandato_completo": fim <= hoje,
    }


def historico() -> list[dict]:
    linhas = []
    for ano, (d0, d1) in ELEICOES.items():
        e = evento(d0, d1)
        linha = {"ano": ano, "vencedor": VENCEDOR[ano],
                 "ibovespa_dia_pct": e["ibovespa"]["variacao_pct"] if e["ibovespa"] else None,
                 "dolar_dia_pct": (e["usdbrl_ptax"] or e["usdbrl_yahoo"] or {}).get("variacao_pct"),
                 "excesso_ibovespa_pct": e.get("excesso_ibovespa_contra_eem_pct")}
        if ano < 2026:
            linha.update(depois_do_mandato(ano))
        linhas.append(linha)
    return linhas
