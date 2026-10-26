"""Baixa as séries numéricas do projeto para dados/series/ e registra cada uma em dados/MANIFESTO.json.

Fontes: Banco Central (SGS e Focus, API Olinda), FMI (datamapper, WEO e Fiscal Monitor),
IBGE (SIDRA) e Yahoo Finance (cotações diárias). Um download por vez, com pausa.

Uso: python ferramentas/coletar.py [nome ...]   (sem nome, baixa tudo)
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
import time
import urllib.parse
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parents[1]
SERIES = RAIZ / "dados" / "series"
MANIFESTO = RAIZ / "dados" / "MANIFESTO.json"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/129.0"}

SGS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{n}/dados?formato=json&dataInicial={ini}&dataFinal={fim}"
IMF = "https://www.imf.org/external/datamapper/api/v1/{ind}/{paises}"
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{sim}?period1={p1}&period2={p2}&interval=1d"
OLINDA = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoAnuais"

HOJE = dt.date.today()
FIM = HOJE.strftime("%d/%m/%Y")

# Séries mensais e diárias do SGS: nome -> (código, data inicial). Diária longa vai em blocos de 10 anos.
SGS_SERIES = {
    "bcb-divida-bruta-gg": (13762, "01/12/2006"),
    "bcb-divida-liquida-sp": (4513, "01/12/2001"),
    "bcb-primario-12m": (5793, "01/12/2002"),
    "bcb-juros-nominais-12m": (5727, "01/12/2002"),
    "bcb-ipca-mensal": (433, "01/01/1995"),
    "bcb-ipca-12m": (13522, "01/01/1995"),
    "bcb-desemprego-pnad": (24369, "01/03/2012"),
}
SGS_DIARIAS = {"bcb-ptax-venda": (1, 1995), "bcb-selic-meta": (432, 2000)}

YAHOO_TICKERS = {
    "yahoo-ibovespa": "^BVSP",
    "yahoo-ewz": "EWZ",
    "yahoo-eem": "EEM",
    "yahoo-usdbrl": "BRL=X",
    "yahoo-usdmxn": "MXN=X",
    "yahoo-usdclp": "CLP=X",
    "yahoo-usdcop": "COP=X",
    "yahoo-usdzar": "ZAR=X",
    "yahoo-us10y": "^TNX",
}

G20_EMERGENTES = ["ARG", "BRA", "CHN", "IND", "IDN", "MEX", "RUS", "SAU", "ZAF", "TUR"]
LATAM = ["ARG", "BRA", "CHL", "COL", "MEX", "PER", "URY"]
PAISES_FMI = "/".join(sorted(set(G20_EMERGENTES + LATAM)) + ["FM_EMG", "FAD_G20Emg", "OEMDC", "WE", "ADVEC"])
IMF_SERIES = {
    "imf-weo-divida-bruta": "GGXWDG_NGDP",
    "imf-weo-resultado-nominal": "GGXCNL_NGDP",
    "imf-weo-pib-real": "NGDP_RPCH",
    "imf-fm-despesa": "G_X_G01_GDP_PT",
    "imf-fm-primario": "GGXONLB_G01_GDP_PT",
    "imf-fm-nominal": "GGXCNL_G01_GDP_PT",
    "imf-fm-divida-bruta": "G_XWDG_G01_GDP_PT",
}

FOCUS_INDICADORES = ["IPCA", "PIB Total", "Selic", "Câmbio", "Resultado primário", "Resultado nominal",
                     "Dívida líquida do setor público", "Dívida bruta do governo geral"]


def manifesto() -> dict:
    return json.loads(MANIFESTO.read_text(encoding="utf-8")) if MANIFESTO.exists() else {}


def registrar(nome: str, urls: list[str], conteudo: bytes, arquivo: Path) -> None:
    m = manifesto()
    m[nome] = {
        "urls": urls,
        "baixado_em": dt.datetime.now().isoformat(timespec="seconds"),
        "bytes": len(conteudo),
        "sha256": hashlib.sha256(conteudo).hexdigest(),
        "arquivo": arquivo.relative_to(RAIZ).as_posix(),
    }
    MANIFESTO.write_text(json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")


def baixar(url: str, tentativas: int = 4) -> requests.Response:
    # o datamapper do FMI devolve 403 para identificação de navegador; aceita a do requests
    cab = {} if "imf.org" in url else UA
    for k in range(tentativas):
        r = requests.get(url, headers=cab, timeout=120)
        if r.status_code == 200:
            return r
        time.sleep(3 * (k + 1))
    r.raise_for_status()
    return r


def gravar(nome: str, dados, urls: list[str]) -> None:
    SERIES.mkdir(parents=True, exist_ok=True)
    arq = SERIES / f"{nome}.json"
    conteudo = json.dumps(dados, ensure_ascii=False, indent=0).encode("utf-8")
    arq.write_bytes(conteudo)
    registrar(nome, urls, conteudo, arq)
    print(f"{nome}: {len(conteudo)} bytes")


def coletar_sgs(nome: str) -> None:
    n, ini = SGS_SERIES[nome]
    url = SGS.format(n=n, ini=ini, fim=FIM)
    gravar(nome, baixar(url).json(), [url])


def coletar_sgs_diaria(nome: str) -> None:
    n, ano0 = SGS_DIARIAS[nome]
    linhas, urls = [], []
    for a in range(ano0, HOJE.year + 1, 5):
        fim = min(a + 4, HOJE.year)
        url = SGS.format(n=n, ini=f"01/01/{a}", fim=f"31/12/{fim}" if fim < HOJE.year else FIM)
        linhas += baixar(url).json()
        urls.append(url)
        time.sleep(1)
    gravar(nome, linhas, urls)


def coletar_yahoo(nome: str) -> None:
    sim = urllib.parse.quote(YAHOO_TICKERS[nome])
    p2 = int(time.time()) + 86400
    url = YAHOO.format(sim=sim, p1=int(dt.datetime(1993, 1, 1).timestamp()), p2=p2)
    j = baixar(url).json()["chart"]["result"][0]
    q = j["indicators"]["quote"][0]
    linhas = [{"t": t, "data": dt.datetime.utcfromtimestamp(t + j["meta"].get("gmtoffset", 0)).date().isoformat(),
               "abertura": o, "maxima": h, "minima": l, "fechamento": c}
              for t, o, h, l, c in zip(j["timestamp"], q["open"], q["high"], q["low"], q["close"])]
    gravar(nome, {"meta": j["meta"], "linhas": linhas}, [url])


def coletar_imf(nome: str) -> None:
    """Um país ou grupo por vez: o datamapper recusa (403) endereço com muitos países."""
    valores, urls = {}, []
    for pais in PAISES_FMI.split("/"):
        url = IMF.format(ind=IMF_SERIES[nome], paises=pais)
        j = baixar(url).json()
        for ind, por_pais in (j.get("values") or {}).items():
            valores.setdefault(ind, {}).update(por_pais or {})
        urls.append(url)
        time.sleep(1.5)
    gravar(nome, {"values": valores}, urls)


def coletar_focus(nome: str) -> None:
    """focus-recente: todas as datas de 2026-09-01 em diante. focus-historico: outubro dos anos de eleição."""
    linhas, urls = [], []
    if nome == "focus-recente":
        janelas = [("2026-09-01", HOJE.isoformat())]
    else:
        janelas = [(f"{a}-10-01", f"{a}-11-15") for a in (2002, 2006, 2010, 2014, 2018, 2022)]
    for ind in FOCUS_INDICADORES:
        for ini, fim in janelas:
            filtro = f"Indicador eq '{ind}' and Data ge '{ini}' and Data le '{fim}'"
            url = OLINDA + "?" + urllib.parse.urlencode({"$filter": filtro, "$format": "json", "$top": "100000"}, quote_via=urllib.parse.quote)
            linhas += baixar(url).json()["value"]
            urls.append(url)
            time.sleep(0.5)
    gravar(nome, linhas, urls)


def coletar_focus_12m(nome: str) -> None:
    """Inflação esperada para os próximos 12 meses (IPCA, suavizada), de 2026-09-01 em diante."""
    base = OLINDA.replace("ExpectativasMercadoAnuais", "ExpectativasMercadoInflacao12Meses")
    filtro = "Indicador eq 'IPCA' and Data ge '2026-09-01'"
    url = base + "?" + urllib.parse.urlencode({"$filter": filtro, "$format": "json", "$top": "10000"}, quote_via=urllib.parse.quote)
    gravar(nome, baixar(url).json()["value"], [url])


COLETORES = {**{k: coletar_sgs for k in SGS_SERIES}, **{k: coletar_sgs_diaria for k in SGS_DIARIAS},
             **{k: coletar_yahoo for k in YAHOO_TICKERS}, **{k: coletar_imf for k in IMF_SERIES},
             "focus-recente": coletar_focus, "focus-historico": coletar_focus, "focus-ipca-12m": coletar_focus_12m}


def main(nomes: list[str]) -> int:
    falhas = 0
    for nome in nomes or list(COLETORES):
        try:
            COLETORES[nome](nome)
        except Exception as e:  # noqa: BLE001
            print(f"{nome}: FALHOU ({e})", file=sys.stderr)
            falhas += 1
        time.sleep(1)
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
