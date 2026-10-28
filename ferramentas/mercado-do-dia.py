"""M1 e M2: a reação do mercado ao resultado (pré-registro M1, emendas 2 e 4) e o veredito de A1, A2 e A6.

Passos:
1. Baixa de novo as cotações (Yahoo, PTAX, título de 10 anos dos EUA) e o Focus.
2. Baixa a curva DI x pré da B3 (arquivo TaxaSwap) de 23/out e, quando sair, de 26/out.
3. Baixa a chance de Lula no Polymarket hora a hora em 25/out (o DNS do Brasil bloqueia o site;
   a consulta vai por DNS sobre HTTPS) e pega o último ponto antes das 19h de Brasília.
4. Calcula o evento, o excesso contra os emergentes, o prêmio e os vereditos.
Grava resultados/M1_MERCADO.json. Uso: python ferramentas/mercado-do-dia.py [--sem-coleta]
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from economia import mercado  # noqa: E402
from economia import series as S  # noqa: E402

RES = RAIZ / "resultados"
DERIV = RAIZ / "dados" / "derivados"
BRUTOS = RAIZ / "dados" / "brutos"
D0, D1 = dt.date(2026, 10, 23), dt.date(2026, 10, 26)
BRT = dt.timezone(dt.timedelta(hours=-3))
TOKEN_LULA_SIM = "30630994248667897740988010928640156931882346081873066002335460180076741328029"
VENCIMENTOS = {"jan/2027": dt.date(2027, 1, 4), "jan/2028": dt.date(2028, 1, 3), "jan/2029": dt.date(2029, 1, 2),
               "jan/2031": dt.date(2031, 1, 2), "jan/2033": dt.date(2033, 1, 3)}


def registrar(nome: str, url: str, conteudo: bytes, arquivo: Path) -> None:
    man = RAIZ / "dados" / "MANIFESTO.json"
    m = json.loads(man.read_text(encoding="utf-8")) if man.exists() else {}
    m[nome] = {"urls": [url], "baixado_em": dt.datetime.now().isoformat(timespec="seconds"), "bytes": len(conteudo),
               "sha256": hashlib.sha256(conteudo).hexdigest(), "arquivo": arquivo.relative_to(RAIZ).as_posix()}
    man.write_text(json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")


def curva_b3(dia: dt.date) -> dict | None:
    """Vértices da curva PRE (DI x pré) do arquivo TaxaSwap da B3: {dias corridos: (dias úteis, taxa %)}."""
    url = f"https://www.b3.com.br/pesquisapregao/download?filelist=TS{dia:%y%m%d}.ex_"
    pronto = DERIV / f"curva_pre_b3_{dia:%Y%m%d}.json"
    if pronto.exists():
        return {int(k): tuple(v) for k, v in json.loads(pronto.read_text(encoding="utf-8"))["vertices"].items()}
    r = None
    for _ in range(3):
        try:
            r = requests.get(url, timeout=180, headers={"User-Agent": "Mozilla/5.0"})
            break
        except requests.RequestException:
            continue
    if r is None or r.status_code != 200 or len(r.content) < 10000:
        return None
    BRUTOS.mkdir(parents=True, exist_ok=True)
    bruto = BRUTOS / f"TS{dia:%y%m%d}.zip"
    bruto.write_bytes(r.content)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["7z", "x", "-y", f"-o{tmp}", str(bruto)], capture_output=True, check=True)
        exe = next(Path(tmp).glob("*.ex_"))
        subprocess.run(["7z", "x", "-y", f"-o{tmp}", str(exe)], capture_output=True, check=True)
        texto = next(Path(tmp).rglob("TaxaSwap.txt")).read_text(encoding="latin-1")
    vert = {}
    for linha in texto.splitlines():
        if linha[21:26].strip() != "PRE" or linha[11:19] != f"{dia:%Y%m%d}":
            continue
        dc, du = int(linha[41:46]), int(linha[46:51])
        taxa = int(linha[52:66]) / 1e7 * (-1 if linha[51] == "-" else 1)
        vert[dc] = (du, taxa)
    if not vert:
        return None
    DERIV.mkdir(parents=True, exist_ok=True)
    arq = DERIV / f"curva_pre_b3_{dia:%Y%m%d}.json"
    conteudo = json.dumps({"data": dia.isoformat(), "fonte": url, "vertices": {str(k): v for k, v in sorted(vert.items())}}).encode()
    arq.write_bytes(conteudo)
    registrar(f"b3-curva-pre-{dia:%Y%m%d}", url, r.content, bruto)
    return vert


def taxa_em(vert: dict, dia: dt.date, venc: dt.date) -> tuple[float, int]:
    """Taxa do vértice do vencimento (dias corridos exatos), ou interpolação exponencial nos dias úteis."""
    dc = (venc - dia).days
    if dc in vert:
        return vert[dc][1], vert[dc][0]
    ks = sorted(vert)
    a = max(k for k in ks if k < dc)
    b = min(k for k in ks if k > dc)
    (dua, ta), (dub, tb) = vert[a], vert[b]
    dux = dua + (dub - dua) * (dc - a) / (b - a)
    fa, fb = (1 + ta / 100) ** (dua / 252), (1 + tb / 100) ** (dub / 252)
    fx = fa * (fb / fa) ** ((dux - dua) / (dub - dua))
    return 100 * (fx ** (252 / dux) - 1), round(dux)


def termo(vert: dict, dia: dt.date, v1: dt.date, v2: dt.date) -> float:
    t1, d1 = taxa_em(vert, dia, v1)
    t2, d2 = taxa_em(vert, dia, v2)
    f = (1 + t2 / 100) ** (d2 / 252) / (1 + t1 / 100) ** (d1 / 252)
    return 100 * (f ** (252 / (d2 - d1)) - 1)


def polymarket() -> dict | None:
    ini = int(dt.datetime(2026, 10, 23, 0, 0, tzinfo=BRT).timestamp())
    fim = int(dt.datetime(2026, 10, 26, 6, 0, tzinfo=BRT).timestamp())
    url = f"https://clob.polymarket.com/prices-history?market={TOKEN_LULA_SIM}&startTs={ini}&endTs={fim}&fidelity=60"
    try:
        out = subprocess.run(["curl", "-s", "--doh-url", "https://1.1.1.1/dns-query", url], capture_output=True, timeout=90, check=True).stdout
        hist = json.loads(out)["history"]
    except Exception as e:  # noqa: BLE001
        print("Polymarket falhou:", e, file=sys.stderr)
        return None
    arq = RAIZ / "dados" / "series" / "polymarket-lula.json"
    arq.write_bytes(out)
    registrar("polymarket-lula", url, out, arq)
    fecha = dt.datetime(2026, 10, 25, 19, 0, tzinfo=BRT).timestamp()
    antes = [h for h in hist if h["t"] < fecha]
    ult = antes[-1]
    return {"p": ult["p"], "hora_brt": dt.datetime.fromtimestamp(ult["t"], BRT).isoformat(timespec="minutes"),
            "fim_de_23_out": [h["p"] for h in hist if h["t"] < dt.datetime(2026, 10, 24, 0, 0, tzinfo=BRT).timestamp()][-1],
            "pontos": len(hist), "url": url}


def tnx(d0: dt.date, d1: dt.date) -> float | None:
    s = S.yahoo("yahoo-us10y")
    if d1 not in s.index:
        return None
    return (float(s[d1]) - S.valor_em(s, d0)[1]) / 100 if s[d1] > 20 else float(s[d1]) - S.valor_em(s, d0)[1]


def fluxo() -> tuple[dict, list[str]]:
    """M2 pelos achados de fluxo (K04 a K09), com os números lidos do trecho conferido."""
    conf = {l["id"]: l for l in csv.DictReader((RES / "TRECHOS_CONFERIDOS.csv").open(encoding="utf-8")) if l["estado_a"].startswith("ok")}
    ach = {l["id"]: l for l in csv.DictReader((RAIZ / "dados" / "evidencias" / "ACHADOS.csv").open(encoding="utf-8")) if l["id"] in conf}
    # rodada 9: com o dado da B3 publicado em 28/out (K55 e K56), o saldo vai até 26/out, o dia medido; sem eles, até 22/out (K04 e K09)
    k_ano, k_out, dia_fim = ("K56", "K55", 26) if "K56" in ach and "K55" in ach else ("K04", "K09", 22)
    ano = float(ach[k_ano]["numero"]) if k_ano in ach else None
    outubro = float(ach[k_out]["numero"]) if k_out in ach else None
    b = lambda x: f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")  # noqa: E731
    linhas = []
    if ano is not None:
        linhas.append(f"De janeiro a {dia_fim}/out de 2026, os estrangeiros compraram R$ {b(ano)} bi a mais do que venderam em ações na B3 (sem contar ofertas novas) ([fonte]({ach[k_ano]['url_a']})).")
    if outubro is not None:
        linhas.append(f"Só em outubro, até o dia {dia_fim}, a entrada foi de R$ {b(outubro)} bi ([fonte]({ach[k_out]['url_a']})).")
    if dia_fim == 26 and "K04" in ach and "K09" in ach:
        linhas.append(f"Até 22/out eram R$ {b(float(ach['K04']['numero']))} bi no ano e R$ {b(float(ach['K09']['numero']))} bi em outubro; a diferença saiu nos 2 pregões em volta do 2º turno ([fonte]({ach['K55']['url_b']})).")
    if "K08" in ach:
        linhas.append(f"No primeiro pregão depois do 1º turno (5/out) entraram R$ {b(float(ach['K08']['numero']))} bi num dia só, recorde ([fonte]({ach['K08']['url_a']})).")
    if "K06" in ach:
        linhas.append(f"O pior mês do ano foi agosto, com saída de R$ {b(-float(ach['K06']['numero']))} bi ([fonte]({ach['K06']['url_a']})).")
    if "K09" in ach:
        dias = re.findall(r"(\d{2}/10) ([+-][\d.]+,\d+) mi", ach["K09"]["fato"])
        if dia_fim == 26:
            dias += re.findall(r"(\d{2}/10) ([+-][\d.]+,\d+) mi", ach["K55"]["fato"])
        if dias:
            linhas.append("Nos dias em volta do 2º turno o saldo oscilou: " + ", ".join(f"{d}, R$ {v} mi" for d, v in dias) + ".")
    # medida 2 do M2: balanço de pagamentos (Banco Central), investimento estrangeiro em carteira no Brasil
    bp = {}
    for nome, rot in [("bcb-bp-acoes", "ações"), ("bcb-bp-fundos", "fundos de investimento"),
                      ("bcb-bp-titulos-no-pais", "títulos de dívida negociados no país"), ("bcb-bp-titulos-no-exterior", "títulos de dívida negociados no exterior")]:
        try:
            s = S.sgs(nome)
        except FileNotFoundError:
            continue
        a = s[s.index >= dt.date(2026, 1, 1)]
        bp[rot] = {"ate": a.index[-1].isoformat(), "soma_us_mi": float(a.sum()), "ultimo_mes_us_mi": float(a.iloc[-1])}
    if bp:
        ate = max(v["ate"] for v in bp.values())
        partes = "; ".join(f"{k}, US$ {b(v['soma_us_mi'] / 1000)} bi" for k, v in bp.items())
        linhas.append(f"Pelo balanço de pagamentos do Banco Central, que conta todo tipo de compra de ações (não só a bolsa) e também a renda fixa, o saldo do investimento estrangeiro em carteira no Brasil de janeiro até {ate[5:7]}/{ate[:4]} foi: {partes}.")
    if "K21" in ach:
        linhas.append(f"A imprensa registrou que os investidores estrangeiros estavam posicionados para a vitória do outro candidato ([fonte]({ach['K21']['url_a']})).")
    return {"ano_rs_bi": ano, "outubro_rs_bi": outubro, "ate_o_dia": f"{dia_fim}/out", "balanco_de_pagamentos": bp}, linhas


def regua_a2(ano: float | None, outubro: float | None) -> str:
    if ano is None or outubro is None:
        return "sem dado"
    neg = [ano < 0, outubro < 0]
    return "confirmada" if all(neg) else ("confirmada em parte" if any(neg) else "não confirmada")


def main(coletar: bool = True) -> int:
    if coletar:
        subprocess.run([sys.executable, str(RAIZ / "ferramentas" / "coletar.py"), *mercado.MOEDAS_CONTROLE,
                        "yahoo-ibovespa", "yahoo-ewz", "yahoo-eem", "yahoo-usdbrl", "yahoo-us10y", "bcb-ptax-venda",
                        "focus-recente", "focus-ipca-12m"], check=False)
        S.yahoo.cache_clear(), S.sgs.cache_clear(), S.focus.cache_clear()
    out: dict = {"gerado_em": dt.datetime.now(BRT).isoformat(timespec="minutes")}
    e = mercado.evento(D0, D1)
    fechado = e["ibovespa"] is not None and dt.datetime.now(BRT) >= dt.datetime(D1.year, D1.month, D1.day, 18, 0, tzinfo=BRT)
    out["fechamento_de_26_out"] = fechado
    out["dia"] = e if e["ibovespa"] else None
    if e["ibovespa"]:
        q = mercado.maiores_quedas()
        out["maiores_quedas_desde_1995"] = q
        out["posicao_da_queda_de_26_out"] = next((i + 1 for i, x in enumerate(q) if x["data"] == D1.isoformat()), None)
    notas = []
    if e["ibovespa"] and not fechado:
        notas.append(f"Números do dia 26/out parciais, coletados às {out['gerado_em'][11:16]}: o veredito de A1 só vale com o fechamento.")
    # curva
    c0, c1 = curva_b3(D0), curva_b3(D1)
    juros = []
    if c0:
        out["curva_23_out"] = {k: taxa_em(c0, D0, v)[0] for k, v in VENCIMENTOS.items()}
        out["termo_2028_em_23_out"] = termo(c0, D0, VENCIMENTOS["jan/2028"], VENCIMENTOS["jan/2029"])
    venc = "jan/2033"
    if c0 and c1:
        out["curva_26_out"] = {k: taxa_em(c1, D1, v)[0] for k, v in VENCIMENTOS.items()}
        out["termo_2028_em_26_out"] = termo(c1, D1, VENCIMENTOS["jan/2028"], VENCIMENTOS["jan/2029"])
        out["curva_selic_fim_2027"] = out["termo_2028_em_26_out"]
        out["fonte_curva_26_out"] = "B3, arquivo de taxas referenciais (emenda 4)"
        for k in VENCIMENTOS:
            juros.append({"nome": f"DI futuro {k} (B3)", "variacao_pp": out["curva_26_out"][k] - out["curva_23_out"][k],
                          "detalhe": f"{out['curva_23_out'][k]:.2f}% → {out['curva_26_out'][k]:.2f}%".replace(".", ",")})
    elif c0:
        # emenda 9: sem o arquivo da B3 de 26/out, a taxa de fechamento publicada (achado K45, texto da Reuters)
        k45 = {l["id"]: l for l in csv.DictReader((RAIZ / "dados" / "evidencias" / "ACHADOS.csv").open(encoding="utf-8"))}.get("K45")
        conf45 = {l["id"]: l for l in csv.DictReader((RES / "TRECHOS_CONFERIDOS.csv").open(encoding="utf-8"))}.get("K45", {})
        if k45 and conf45.get("estado_a", "").startswith("ok") and conf45.get("estado_b", "").startswith("ok"):
            t = k45["trecho_a"]
            m28 = re.search(r"janeiro de 2028 estava em (\d+,\d+)%", t)
            m31 = re.search(r"janeiro de 2031 estava em (\d+,\d+)%", t)
            num = lambda m: float(m.group(1).replace(",", "."))  # noqa: E731
            out["curva_26_out"] = {"jan/2028": num(m28), "jan/2031": num(m31)}
            out["curva_selic_fim_2027"] = num(m28)
            out["fonte_curva_26_out"] = "imprensa, texto da Reuters na CNN Brasil e no InfoMoney (achado K45; emenda 9)"
            venc = "jan/2031"
            for k in ("jan/2028", "jan/2031"):
                juros.append({"nome": f"DI futuro {k} (fechamento, Reuters)", "variacao_pp": out["curva_26_out"][k] - out["curva_23_out"][k],
                              "detalhe": f"{out['curva_23_out'][k]:.2f}% → {out['curva_26_out'][k]:.2f}%".replace(".", ",")})
    out["juros"] = juros
    out["vencimento_do_premio"] = venc
    # prêmio
    pm = polymarket()
    out["polymarket"] = pm
    dus = tnx(D0, D1)
    if pm and out.get("curva_26_out") and dus is not None:
        dbr = out["curva_26_out"][venc] - out["curva_23_out"][venc]
        exc = dbr - dus
        out["premio"] = {"premio_pp": exc / (1 - pm["p"]), "excesso_juro_pp": exc, "variacao_di_pp": dbr, "vencimento": venc,
                         "variacao_10_anos_eua_pp": dus, "p_lula_vespera": pm["p"],
                         "origem": f"excesso do DI {venc} contra o título de 10 anos dos EUA em 26/out ({exc:.2f} ponto), dividido pela surpresa (1 - {pm['p']:.3f})".replace(".", ",")}
    # variante da revisão adversarial: o juro longo de 26/out contra o da data da base da IFI (12/jun),
    # descontado o que o título de 10 anos dos EUA fez no mesmo intervalo; sem dividir pela surpresa,
    # porque compara dois níveis e não a reação a um resultado
    jun = dt.date(2026, 6, 12)
    cj = curva_b3(jun)
    dus_jun = tnx(jun, D1)
    if cj and out.get("curva_26_out") and dus_jun is not None:
        di_jun = taxa_em(cj, jun, VENCIMENTOS[venc])[0]
        out["premio_contra_base_ifi"] = {"premio_pp": (out["curva_26_out"][venc] - di_jun) - dus_jun, "vencimento": venc,
                                         "di_12_jun": di_jun, "variacao_10_anos_eua_pp": dus_jun}
    # vereditos
    if e["ibovespa"]:
        v = e["ibovespa"]["variacao_pct"]
        out["veredito_a1"] = {"veredito": mercado.regua_a1(v) + ("" if fechado else " (parcial)"),
                              "porque": f"Ibovespa {v:+.2f}% no dia; contra os emergentes (EEM), {e.get('excesso_ibovespa_contra_eem_pct', 0):+.2f} pontos".replace(".", ",")}
    f, linhas = fluxo()
    out["fluxo_numeros"], out["fluxo"] = f, linhas
    a2 = regua_a2(f["ano_rs_bi"], f["outubro_rs_bi"])
    resto = "; o dado de 26/out sai na B3 dois dias depois" if f["ate_o_dia"] != "26/out" else "; o dia 26/out, já publicado pela B3, foi de saída e não virou o saldo"
    out["veredito_a2"] = {"veredito": a2, "porque": (f"até {f['ate_o_dia']} entraram R$ {f['ano_rs_bi']:.1f} bi de estrangeiros na bolsa em 2026 e R$ {f['outubro_rs_bi']:.1f} bi em outubro".replace(".", ",") + resto) if a2 != "sem dado" else ""}
    conf = {l["id"]: l for l in csv.DictReader((RES / "TRECHOS_CONFERIDOS.csv").open(encoding="utf-8")) if l["estado_a"].startswith("ok")}
    ach = {l["id"]: l for l in csv.DictReader((RAIZ / "dados" / "evidencias" / "ACHADOS.csv").open(encoding="utf-8"))}
    if "K12" in conf and conf["K12"]["estado_b"].startswith("ok"):
        # ranking MoneYou e Lev Intelligence (16/set/2026): o Brasil na segunda fonte, os países seguintes na primeira
        k = ach["K12"]
        brasil = float(re.search(r"juro real do Brasil é de (\d+,\d+)%", k["trecho_b"]).group(1).replace(",", "."))
        texto_outros = k["trecho_a"].split("A média")[0]
        outros = [float(x.replace(",", ".")) for x in re.findall(r"(\d+,\d+)%", texto_outros)]
        posicao = 1 + sum(1 for x in outros if x > brasil)
        v = "confirmada" if posicao <= 3 else ("confirmada em parte" if posicao <= 10 else "não confirmada")
        out["veredito_a6"] = {"veredito": v, "posicao": posicao, "juro_real_brasil_ranking": brasil, "seguintes": outros,
                              "porque": (f"o Brasil tem o {'maior' if posicao == 1 else str(posicao) + 'º maior'} juro real entre 40 países no ranking MoneYou de 16/set/2026, com {brasil:.2f}% ao ano; "
                                         f"o segundo tem {max(outros):.2f}%").replace(".", ",")}
    # segunda fonte do fechamento (matérias do dia, achados K40 e K41) para a validação independente
    conferencia = []
    if "K40" in conf and e["ibovespa"]:
        k = ach["K40"]
        m_ib = re.search(r"queda de (\d+,\d+)%, aos ([\d.]+,\d+) pontos", k["trecho_a"])
        if m_ib:
            conferencia.append({"item": "Ibovespa de 26/out: Yahoo contra a matéria (K40)", "projeto": e["ibovespa"]["fim"],
                                "segunda_fonte": float(m_ib.group(2).replace(".", "").replace(",", ".")), "tolerancia": 1.0})
            conferencia.append({"item": "Queda do Ibovespa em 26/out: Yahoo contra a matéria (K40)", "projeto": -e["ibovespa"]["variacao_pct"],
                                "segunda_fonte": float(m_ib.group(1).replace(",", ".")), "tolerancia": 0.01})
        m_us = re.search(r"avançou (\d+,\d+)% e fechou cotado a R\$ (\d+,\d+)", k["trecho_b"])
        if m_us:
            out["dolar_a_vista"] = {"variacao_pct": float(m_us.group(1).replace(",", ".")), "fim": float(m_us.group(2).replace(",", ".")), "fonte": k["url_b"]}
    for k in ("K42", "K43"):
        if k in conf:
            notas.append(f"{ach[k]['fato']} ([fonte]({ach[k]['url_a']})" + (f", [segunda fonte]({ach[k]['url_b']}))" if ach[k]["url_b"] else ")"))
    if "K41" in conf:
        notas.append(f"{ach['K41']['fato']} ([fonte]({ach['K41']['url_a']}), [segunda fonte]({ach['K41']['url_b']}))")
    out["conferencia_segunda_fonte"] = conferencia
    notas.append("As cotações do Yahoo são as da coleta das 18h16 de 26/out, depois do fechamento de Nova York e com todas as moedas na mesma hora; a coleta das 21h devolveu o dia 26 vazio para o EWZ e os emergentes, e não foi usada.")
    out["notas"] = notas
    RES.mkdir(exist_ok=True)
    (RES / "M1_MERCADO.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: out.get(k) for k in ("fechamento_de_26_out", "veredito_a1", "veredito_a2", "premio", "termo_2028_em_23_out", "termo_2028_em_26_out")},
                     ensure_ascii=False, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main("--sem-coleta" not in sys.argv))
