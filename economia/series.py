"""Leitura das séries baixadas por ferramentas/coletar.py (dados/series/*.json)."""
from __future__ import annotations

import datetime as dt
import json
from functools import lru_cache
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
SERIES = RAIZ / "dados" / "series"


def _json(nome: str):
    return json.loads((SERIES / f"{nome}.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def sgs(nome: str) -> pd.Series:
    """Série do SGS indexada por data (valor float)."""
    linhas = _json(nome)
    s = pd.Series({dt.datetime.strptime(l["data"], "%d/%m/%Y").date(): float(l["valor"]) for l in linhas})
    return s.sort_index()


@lru_cache(maxsize=None)
def yahoo(nome: str) -> pd.Series:
    """Fechamento diário (data local da bolsa), sem dias vazios."""
    # a data vem do fuso do próprio mercado (o Yahoo grava moeda à meia-noite de Londres, e o horário de
    # verão de lá muda a hora UTC do candle; o deslocamento fixo do meta só vale para o dia da coleta)
    from zoneinfo import ZoneInfo
    j = _json(nome)
    fuso = ZoneInfo(j["meta"].get("exchangeTimezoneName") or "UTC")
    s = pd.Series({dt.datetime.fromtimestamp(l["t"], fuso).date(): l["fechamento"] for l in j["linhas"] if l["fechamento"] is not None})
    return s[~s.index.duplicated(keep="last")].sort_index()


@lru_cache(maxsize=None)
def imf(nome: str) -> dict[str, dict[int, float]]:
    """{país ou grupo: {ano: valor}}."""
    vals = _json(nome)["values"]
    (ind,) = [k for k in vals if vals[k]]
    return {p: {int(a): v for a, v in anos.items() if v is not None} for p, anos in vals[ind].items()}


@lru_cache(maxsize=None)
def focus(nome: str = "focus-recente") -> pd.DataFrame:
    df = pd.DataFrame(_json(nome))
    df["Data"] = pd.to_datetime(df["Data"]).dt.date
    df["DataReferencia"] = df["DataReferencia"].astype(int)
    return df[df["baseCalculo"] == 0]


def focus_mediana(indicador: str, ano: int, ate: dt.date, nome: str = "focus-recente") -> tuple[dt.date, float]:
    """Mediana mais recente (até a data `ate`) para o ano de referência."""
    df = focus(nome)
    df = df[(df["Indicador"] == indicador) & (df["DataReferencia"] == ano) & (df["Data"] <= ate)]
    if df.empty:
        raise KeyError((indicador, ano, ate))
    linha = df.sort_values("Data").iloc[-1]
    return linha["Data"], float(linha["Mediana"])


def valor_em(s: pd.Series, dia: dt.date, antes: bool = True) -> tuple[dt.date, float]:
    """Último valor até `dia` (antes=True) ou primeiro a partir de `dia` (antes=False)."""
    if antes:
        sub = s[s.index <= dia]
        return sub.index[-1], float(sub.iloc[-1])
    sub = s[s.index >= dia]
    return sub.index[0], float(sub.iloc[0])
