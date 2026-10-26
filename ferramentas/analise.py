"""Roda M1 a M7 do pré-registro e grava resultados/RESUMO.json (fonte única do relatório).

Entradas: dados/series (coletar.py), dados/derivados/ifi_raf113.json (derivar-ifi.py),
dados/evidencias (importar-achados.py, medidas.py), resultados/M1_MERCADO.json (mercado-do-dia.py).
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from economia import contas, fiscal, mercado, passado  # noqa: E402
from economia import series as S  # noqa: E402

RES = RAIZ / "resultados"
PREMIO_VIDEO_13 = 0.266 / 0.13   # projeto simulacao-governos-eleicoes-2026, usado só até medir o do dia


def ler_json(p: Path, padrao=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else padrao


def base_ifi(cenario: str = "base") -> dict:
    ifi = ler_json(RAIZ / "dados" / "derivados" / "ifi_raf113.json")[cenario]
    anos = range(2025, 2031)
    conv = lambda d: {int(a): v for a, v in d.items() if int(a) in anos}  # noqa: E731
    return {"divida": conv(ifi["divida_bruta"]), "pib_nominal": conv(ifi["pib_nominal"]), "primario": conv(ifi["primario_sp"])}


def m6(premio: float, premio_origem: str, custo_s2_pct_pib: float, custos_fora_da_base_pct: float) -> dict:
    base = base_ifi()
    s0 = fiscal.trajetoria(base)
    s1 = fiscal.trajetoria(base, premio_pp=premio)
    piora = {a: custo_s2_pct_pib for a in range(2027, 2031)}
    s2 = fiscal.trajetoria(base, premio_pp=premio, piora_primario=piora)
    i = fiscal.juro_implicito(base["divida"], base["pib_nominal"], base["primario"])
    g30 = base["pib_nominal"][2030] / base["pib_nominal"][2029] - 1
    i30 = i[2030] + fiscal.REPASSE_GRADUAL[2030] * premio / 100
    estab = fiscal.primario_estabilizador(s1[2029], i30, g30)
    sens = {
        "premio_metade": fiscal.trajetoria(base, premio_pp=premio / 2)[2030],
        "premio_dobro": fiscal.trajetoria(base, premio_pp=premio * 2)[2030],
        "repasse_total_imediato": fiscal.trajetoria(base, premio_pp=premio, repasse=fiscal.REPASSE_TOTAL)[2030],
        "pib_1_ponto_abaixo": fiscal.trajetoria(base, premio_pp=premio, choque_pib_pp=-1)[2030],
        "pib_1_ponto_acima": fiscal.trajetoria(base, premio_pp=premio, choque_pib_pp=1)[2030],
        "custos_fora_da_base_ifi": fiscal.trajetoria(base, premio_pp=premio,
                                                     piora_primario={a: custos_fora_da_base_pct for a in range(2027, 2031)})[2030],
        "cenario_otimista_ifi_com_premio": fiscal.trajetoria(base_ifi("otimista"), premio_pp=premio)[2030],
        "cenario_pessimista_ifi_com_premio": fiscal.trajetoria(base_ifi("pessimista"), premio_pp=premio)[2030],
    }
    fmi = S.imf("imf-weo-divida-bruta")["BRA"]
    variacao = s1[2030] - s1[2026]
    return {
        "premio_pp": premio, "premio_origem": premio_origem,
        "S0_base_ifi": s0, "S1_central": s1, "S2_risco": s2, "custo_s2_pct_pib": custo_s2_pct_pib,
        "S0_reproduz_a_ifi": all(abs(s0[a] - base["divida"][a]) < 0.05 for a in base["divida"]),
        "variacao_2026_2030_S1_pp": variacao, "classificacao_S1": fiscal.regua_trajetoria(variacao),
        "primario_que_estabiliza_em_2030_pct_pib": estab,
        "primario_previsto_2030_base_ifi": base["primario"][2030],
        "distancia_ate_estabilizar_pp": estab - base["primario"][2030],
        "sensibilidade_2030": sens,
        "fmi_weo_out2026_conceito_fmi": {a: fmi[a] for a in range(2025, 2032) if a in fmi},
        "focus_dbgg": {a: S.focus_mediana("Dívida bruta do governo geral", a, dt.date.today())[1] for a in range(2026, 2031)},
    }


def m5() -> dict:
    p = RAIZ / "dados" / "evidencias" / "MEDIDAS_E_PROMESSAS.csv"
    linhas = list(csv.DictReader(p.open(encoding="utf-8")))
    pib27 = base_ifi()["pib_nominal"][2027] if 2027 in base_ifi()["pib_nominal"] else None
    pib27 = pib27 or ler_json(RAIZ / "dados" / "derivados" / "ifi_raf113.json")["base"]["pib_nominal"]["2027"]
    por_cat, itens = {}, []
    for l in linhas:
        if not l["id"].startswith("M") or not l["recorrente_a_partir_de_2027_rs_bi"]:
            continue
        v = float(l["recorrente_a_partir_de_2027_rs_bi"])
        por_cat[l["categoria"]] = por_cat.get(l["categoria"], 0.0) + v
        itens.append({"id": l["id"], "nome": l["nome"], "categoria": l["categoria"], "rs_bi": v})
    total = sum(por_cat.values())
    promessas = [l for l in linhas if l["id"].startswith("P")]
    com_custo = [l for l in promessas if l["custo_informado_rs_bi"]]
    return {
        "medidas_recorrentes": itens, "total_recorrente_rs_bi": total, "pib_nominal_2027_ifi": pib27,
        "total_recorrente_pct_pib_2027": 100 * total / pib27,
        "por_categoria_rs_bi": por_cat,
        "por_categoria_fatia_pct": {k: 100 * v / total for k, v in por_cat.items()},
        "promessas": len(promessas), "promessas_com_custo_publicado": len(com_custo),
        "promessas_sem_custo": [l["nome"] for l in promessas if not l["custo_informado_rs_bi"]],
    }


MESES = {m: i for i, m in enumerate(["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"], 1)}
JANELA = (dt.date(2025, 10, 26), dt.date(2026, 10, 25))


def datas_do_texto(t: str) -> list[dt.date]:
    """Datas escritas como 26/nov/2025, nov/2025 ou 2026-09-17 no campo de data da fonte."""
    out = []
    for d, m, a in re.findall(r"(\d{1,2})/(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)/(\d{4})", t):
        out.append(dt.date(int(a), MESES[m], int(d)))
    for m, a in re.findall(r"(?<!\d/)(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)/(\d{4})", t):
        out.append(dt.date(int(a), MESES[m], 15))
    for a, m, d in re.findall(r"(\d{4})-(\d{2})-(\d{2})", t):
        out.append(dt.date(int(a), int(m), int(d)))
    return out


def vereditos_a3_a4() -> dict:
    """Emenda 3."""
    linhas = list(csv.DictReader((RAIZ / "dados" / "evidencias" / "MEDIDAS_E_PROMESSAS.csv").open(encoding="utf-8")))
    medidas = [l for l in linhas if l["id"].startswith("M")]
    na_janela = [l for l in medidas if any(JANELA[0] <= d <= JANELA[1] for d in datas_do_texto(l["data"]))]
    rec = [l for l in na_janela if l["recorrente_a_partir_de_2027_rs_bi"]]
    total = sum(float(l["recorrente_a_partir_de_2027_rs_bi"]) for l in rec)
    nao_comp = sum(float(l["recorrente_a_partir_de_2027_rs_bi"]) for l in rec if l["categoria"] != "A")
    c1, c2 = len(na_janela) >= 5, total > 0 and nao_comp / total > 0.5
    a3 = "confirmada" if c1 and c2 else ("confirmada em parte" if c1 or c2 else "não confirmada")
    prom = [l for l in linhas if l["id"].startswith("P") and l["id"] != "P15"]
    sem = [l for l in prom if not l["custo_informado_rs_bi"] or l["categoria"] == "E"]
    f = len(sem) / len(prom)
    a4 = "confirmada" if f > 0.5 else ("confirmada em parte" if f >= 0.25 else "não confirmada")
    return {"A3": {"medidas_na_janela": [l["id"] for l in na_janela], "n": len(na_janela),
                   "custo_recorrente_delas_rs_bi": total, "nao_compensado_rs_bi": nao_comp,
                   "fatia_nao_compensada_pct": 100 * nao_comp / total if total else None, "veredito": a3},
            "A4": {"promessas": len(prom), "sem_custo_ou_sem_fonte": len(sem), "fatia_pct": 100 * f,
                   "lista_sem": [l["nome"] for l in sem], "veredito": a4}}


def main() -> int:
    hoje = dt.date.today()
    m1 = ler_json(RES / "M1_MERCADO.json", {})
    premio = m1.get("premio", {}).get("premio_pp")
    origem = m1.get("premio", {}).get("origem", "")
    if premio is None:
        premio, origem = PREMIO_VIDEO_13, "provisório: o do projeto do vídeo 13 (reação do DI de 15/out), até medir o do dia 26/out"
    medidas = m5()
    # S2: promessas com custo de duas fontes e sem fonte declarada (pré-registro M5)
    linhas = list(csv.DictReader((RAIZ / "dados" / "evidencias" / "MEDIDAS_E_PROMESSAS.csv").open(encoding="utf-8")))
    itens_s2 = [{"id": l["id"], "nome": l["nome"], "rs_bi": float(l["custo_informado_rs_bi"])} for l in linhas
                if l["id"].startswith("P") and l["categoria"] == "E" and l["custo_informado_rs_bi"]
                and l["fonte_principal_conferida"] == "sim" and l["tem_segunda_fonte"] == "sim"]
    s2 = {"itens": itens_s2, "custo_rs_bi": sum(x["rs_bi"] for x in itens_s2),
          "custo_pct_pib": 100 * sum(x["rs_bi"] for x in itens_s2) / medidas["pib_nominal_2027_ifi"]}
    # Variante (descoberta depois do pré-registro): custos recorrentes posteriores ao cenário da IFI de jun/2026
    pib27 = medidas["pib_nominal_2027_ifi"]
    fora_da_base = [x for x in medidas["medidas_recorrentes"] if x["id"] in ("M12", "M13")]
    fora_pct = 100 * sum(x["rs_bi"] for x in fora_da_base) / pib27
    hist = mercado.historico()
    prev = passado.previsao_contra_realizado()
    resumo = {
        "gerado_em": dt.datetime.now().isoformat(timespec="minutes"),
        "M1_mercado": m1,
        "M1_historico_eleicoes": hist,
        "M7_previsao_do_mercado_contra_o_realizado": {"linhas": prev, "resumo": passado.resumo_erros(prev)},
        "M3_gasto": contas.gasto(),
        "M3_contas_hoje": contas.contas_hoje(),
        "M4_juro_real": contas.juro_real(),
        "M4_focus_selic": {a: S.focus_mediana("Selic", a, hoje) for a in range(2026, 2031)},
        "M4_focus_macro": {ind: {a: S.focus_mediana(ind, a, hoje)[1] for a in range(2026, 2031)}
                           for ind in ["PIB Total", "IPCA", "Câmbio", "Resultado primário", "Dívida líquida do setor público"]},
        "M5_medidas": medidas,
        "M5_S2": s2,
        "M5_vereditos": vereditos_a3_a4(),
        "M6_divida": m6(premio, origem, s2["custo_pct_pib"], fora_pct),
        "M6_variante_custos_fora_da_base": {"itens": fora_da_base, "pct_pib": fora_pct},
    }
    sel = resumo["M4_focus_selic"]
    resumo["M4_focus_selic"] = {a: {"data": d.isoformat(), "mediana": v} for a, (d, v) in sel.items()}
    atual = resumo["M4_juro_real"]["selic_meta"]
    curva27 = m1.get("curva_selic_fim_2027")
    resumo["M4_veredito_a7"] = contas.regua_a7(sel[2027][1], curva27, atual, [sel[a][1] for a in range(2026, 2031)])
    RES.mkdir(exist_ok=True)
    (RES / "RESUMO.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("RESUMO.json gravado:", resumo["M6_divida"]["classificacao_S1"], round(resumo["M6_divida"]["S1_central"][2030], 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
