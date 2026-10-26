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
    ano = float(ach["K04"]["numero"]) if "K04" in ach else None
    outubro = float(ach["K09"]["numero"]) if "K09" in ach else None
    b = lambda x: f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")  # noqa: E731
    linhas = []
    if ano is not None:
        linhas.append(f"De janeiro a 22/out de 2026, os estrangeiros compraram R$ {b(ano)} bi a mais do que venderam em ações na B3 (sem contar ofertas novas) ([fonte]({ach['K04']['url_a']})).")
    if outubro is not None:
        linhas.append(f"Só em outubro, até o dia 22, a entrada foi de R$ {b(outubro)} bi ([fonte]({ach['K09']['url_a']})).")
    if "K08" in ach:
        linhas.append(f"No primeiro pregão depois do 1º turno (5/out) entraram R$ {b(float(ach['K08']['numero']))} bi num dia só, recorde ([fonte]({ach['K08']['url_a']})).")
    if "K06" in ach:
        linhas.append(f"O pior mês do ano foi agosto, com saída de R$ {b(-float(ach['K06']['numero']))} bi ([fonte]({ach['K06']['url_a']})).")
    if "K09" in ach:
        dias = re.findall(r"(\d{2}/10) ([+-][\d.]+,\d+) mi", ach["K09"]["fato"])
        if dias:
            linhas.append("Nos dias antes do 2º turno o saldo já oscilava: " + ", ".join(f"{d}, R$ {v} mi" for d, v in dias) + ".")
    if "K21" in ach:
        linhas.append(f"A imprensa registrou que os investidores estrangeiros estavam posicionados para a vitória do outro candidato ([fonte]({ach['K21']['url_a']})).")
    return {"ano_ate_22_out_rs_bi": ano, "outubro_ate_22_out_rs_bi": outubro}, linhas


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
    fechado = e["ibovespa"] is not None and dt.datetime.now(BRT).hour >= 18
    out["fechamento_de_26_out"] = fechado
    out["dia"] = e if e["ibovespa"] else None
    notas = []
    if e["ibovespa"] and not fechado:
        notas.append(f"Números do dia 26/out parciais, coletados às {out['gerado_em'][11:16]}: o veredito de A1 só vale com o fechamento.")
    # curva
    c0, c1 = curva_b3(D0), curva_b3(D1)
    juros = []
    if c0:
        out["curva_23_out"] = {k: taxa_em(c0, D0, v)[0] for k, v in VENCIMENTOS.items()}
        out["termo_2028_em_23_out"] = termo(c0, D0, VENCIMENTOS["jan/2028"], VENCIMENTOS["jan/2029"])
    if c0 and c1:
        out["curva_26_out"] = {k: taxa_em(c1, D1, v)[0] for k, v in VENCIMENTOS.items()}
        out["termo_2028_em_26_out"] = termo(c1, D1, VENCIMENTOS["jan/2028"], VENCIMENTOS["jan/2029"])
        out["curva_selic_fim_2027"] = out["termo_2028_em_26_out"]
        for k in VENCIMENTOS:
            juros.append({"nome": f"DI futuro {k} (B3)", "variacao_pp": out["curva_26_out"][k] - out["curva_23_out"][k],
                          "detalhe": f"{out['curva_23_out'][k]:.2f}% → {out['curva_26_out'][k]:.2f}%".replace(".", ",")})
    out["juros"] = juros
    # prêmio
    pm = polymarket()
    out["polymarket"] = pm
    dus = tnx(D0, D1)
    if pm and c0 and c1 and dus is not None:
        dbr = out["curva_26_out"]["jan/2033"] - out["curva_23_out"]["jan/2033"]
        exc = dbr - dus
        out["premio"] = {"premio_pp": exc / (1 - pm["p"]), "excesso_juro_jan2033_pp": exc, "variacao_di_jan2033_pp": dbr,
                         "variacao_10_anos_eua_pp": dus, "p_lula_vespera": pm["p"],
                         "origem": f"excesso do DI jan/2033 contra o título de 10 anos dos EUA em 26/out ({exc:.2f} ponto), dividido pela surpresa (1 - {pm['p']:.3f})".replace(".", ",")}
    # variante da revisão adversarial: o juro longo de 26/out contra o da data da base da IFI (12/jun),
    # descontado o que o título de 10 anos dos EUA fez no mesmo intervalo; sem dividir pela surpresa,
    # porque compara dois níveis e não a reação a um resultado
    jun = dt.date(2026, 6, 12)
    cj = curva_b3(jun)
    dus_jun = tnx(jun, D1)
    if cj and c1 and dus_jun is not None:
        di_jun = taxa_em(cj, jun, VENCIMENTOS["jan/2033"])[0]
        out["premio_contra_base_ifi"] = {"premio_pp": (out["curva_26_out"]["jan/2033"] - di_jun) - dus_jun,
                                         "di_jan2033_12_jun": di_jun, "variacao_10_anos_eua_pp": dus_jun}
    # vereditos
    if e["ibovespa"]:
        v = e["ibovespa"]["variacao_pct"]
        out["veredito_a1"] = {"veredito": mercado.regua_a1(v) + ("" if fechado else " (parcial)"),
                              "porque": f"Ibovespa {v:+.2f}% no dia; contra os emergentes (EEM), {e.get('excesso_ibovespa_contra_eem_pct', 0):+.2f} pontos".replace(".", ",")}
    f, linhas = fluxo()
    out["fluxo_numeros"], out["fluxo"] = f, linhas
    a2 = regua_a2(f["ano_ate_22_out_rs_bi"], f["outubro_ate_22_out_rs_bi"])
    out["veredito_a2"] = {"veredito": a2, "porque": (f"até 22/out entraram R$ {f['ano_ate_22_out_rs_bi']:.1f} bi de estrangeiros na bolsa em 2026 e R$ {f['outubro_ate_22_out_rs_bi']:.1f} bi em outubro; o dado de 26/out sai na B3 dois dias depois".replace(".", ",")) if a2 != "sem dado" else ""}
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
                              "porque": (f"o Brasil é o {'maior' if posicao == 1 else str(posicao) + 'º maior'} juro real entre 40 países no ranking MoneYou de 16/set/2026, com {brasil:.2f}% ao ano; "
                                         f"o segundo tem {max(outros):.2f}%").replace(".", ",")}
    out["notas"] = notas
    RES.mkdir(exist_ok=True)
    (RES / "M1_MERCADO.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: out.get(k) for k in ("fechamento_de_26_out", "veredito_a1", "veredito_a2", "premio", "termo_2028_em_23_out", "termo_2028_em_26_out")},
                     ensure_ascii=False, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main("--sem-coleta" not in sys.argv))
