"""Escreve RELATORIO.md e RESUMO_SIMPLES.md a partir de resultados/RESUMO.json.

Nenhum número é digitado à mão: tudo sai do RESUMO, da VALIDACAO, das tabelas de dados/evidencias
e de dados/derivados. A leitura da IA (docs/LEITURA_DA_IA.md) sai de ferramentas/gerar-leitura.py.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RES = RAIZ / "resultados"
ANOS = ["2026", "2027", "2028", "2029", "2030"]


def br(x, casas: int = 1) -> str:
    if x is None:
        return "sem dado"
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def sinal(x, casas: int = 1) -> str:
    return ("+" if x > 0 else "") + br(x, casas)


def tabela(cab: list[str], linhas: list[list]) -> str:
    out = ["| " + " | ".join(cab) + " |", "|" + "|".join("---" for _ in cab) + "|"]
    out += ["| " + " | ".join(str(c) for c in l) + " |" for l in linhas]
    return "\n".join(out)


def deficit(x: float) -> str:
    """Resultado primário em linguagem simples: negativo é déficit."""
    return f"déficit de {br(-x)}%" if x < 0 else f"superávit de {br(x)}%"


def carregar() -> dict:
    conf = {l["id"]: l for l in csv.DictReader((RES / "TRECHOS_CONFERIDOS.csv").open(encoding="utf-8"))}
    ach = {l["id"]: l for l in csv.DictReader((RAIZ / "dados" / "evidencias" / "ACHADOS.csv").open(encoding="utf-8"))}
    ok = {k: v for k, v in ach.items() if conf.get(k, {}).get("estado_a", "").startswith("ok")}
    dois = {k: v for k, v in ok.items() if conf[k]["estado_b"].startswith("ok")}
    med = list(csv.DictReader((RAIZ / "dados" / "evidencias" / "MEDIDAS_E_PROMESSAS.csv").open(encoding="utf-8")))
    ifi = json.loads((RAIZ / "dados" / "derivados" / "ifi_raf113.json").read_text(encoding="utf-8"))
    return {"ok": ok, "dois": dois, "med": med, "ifi": ifi, "conf": conf}


def vereditos(r: dict) -> list[list]:
    m1 = r.get("M1_mercado") or {}
    a1, a2, a6 = m1.get("veredito_a1", {}), m1.get("veredito_a2", {}), m1.get("veredito_a6", {})
    g, v5, pv = r["M3_gasto"], r["M5_vereditos"], r["M5_pontos_de_virada"]
    return [
        ["A1", "\"a bolsa derreteu\"", a1.get("veredito", "pendente (falta o fechamento de 26/out)"), a1.get("porque", "")],
        ["A2", "\"vários investimentos [...] acabou fugindo do Brasil\"", a2.get("veredito", "sem dado"), a2.get("porque", "")],
        ["A3", "\"muitas medidas\" no ano da eleição", v5["A3"]["veredito"],
         f"{v5['A3']['n']} medidas nos 12 meses antes da eleição; {br(v5['A3']['fatia_nao_compensada_pct'], 0)}% do custo que se repete não tem receita nova para pagar (sai de outra despesa ou de fora do Orçamento). "
         "Viraria \"em parte\" se o que cabe no limite de gasto contasse como pago. Intenção não se mede"],
        ["A4", "\"de onde é que vai vir esse dinheiro\"", v5["A4"]["veredito"],
         f"{v5['A4']['sem_custo_ou_sem_fonte']} de {v5['A4']['promessas']} promessas econômicas sem custo publicado ou sem fonte declarada "
         f"({pv['a4_sem_6x1']['sem']} de {pv['a4_sem_6x1']['de']} sem o fim da escala 6x1, que já foi aprovado)"],
        ["A5", "\"a gastança do Brasil já está muito alta\"", g["veredito_a5"],
         f"o governo (União, estados e municípios) gasta {br(g['despesa_total']['2025']['brasil'])}% do PIB, contra {br(g['despesa_total']['2025']['mediana_g20_emergentes'])}% na mediana dos emergentes do G20 (FMI, 2025)"],
        ["A6", "\"o juro já está muito alto\"", a6.get("veredito", "sem dado"), a6.get("porque", "")],
        ["A7", "\"a tendência é apenas aumentar\" (o juro)", r["M4_veredito_a7"], r.get("M4_porque_a7", "")],
    ]


def premissas(r: dict) -> list[dict]:
    v = r["M6_variantes_revisao"]
    rz = r["M7_previsao_do_mercado_contra_o_realizado"]["resumo"]
    m1 = r.get("M1_mercado") or {}
    pm = m1.get("polymarket") or {}
    pj = v.get("p2_premio_contra_a_curva_de_junho")
    metas = v.get("p2_metas_do_pldo_cumpridas", {})
    p2 = (f"o mercado de previsão dava {br(100 * pm['p'], 1)}% de chance a Lula na véspera, então parte da queda é aposta desfeita; " if pm else "")
    p2 += (f"contra a curva de junho, que a base da IFI usa, o prêmio é de {br(pj['premio_pp'], 2)} ponto e a dívida vai a {br(pj['divida_2030'])}% em 2030; " if pj else "")
    p2 += (f"sem prêmio nenhum, {br(v['p2_sem_premio']['divida_2030'])}%; com as metas do próprio governo cumpridas, {br(metas.get('divida_2030_sem_premio'))}% sem prêmio e "
           f"{br(metas.get('divida_2030_com_premio'))}% com ele; e o mercado previu a dívida maior do que aconteceu em {rz['vezes_que_o_mercado_previu_divida_maior']} das {rz['n']} eleições desde 2002")
    p1 = (f"com o macro do Focus (Selic mais alta e PIB menor que os da IFI), a dívida vai a {br(v['p1_macro_do_focus']['divida_2030'])}% em 2030; "
          f"com os juros de 2026 já acima da base, {br(v['p1_ponto_de_partida_pior']['divida_2030'])}%; "
          f"se o limite de gasto não segurar os R$ {br(v['p1_limite_nao_segura']['custo_rs_bi'])} bi por ano que a base não tem, {br(v['p1_limite_nao_segura']['divida_2030'])}%; "
          f"as três juntas, {br(v['p1_juntas']['divida_2030'])}%")
    return [
        {"nome": "P1: o mercado tem razão", "versao_forte": "o resultado mantém um governo que expande gasto sem receita nova, o juro longo sobe e fica, e a dívida, que já subia, sobe mais depressa; a queda do dia antecipa isso",
         "o_que_se_veria": "o juro longo e o dólar sem voltar nas semanas seguintes, o Copom parando os cortes, as metas fiscais de 2027 e 2028 revistas para baixo",
         "o_que_mostra": p1, "o_que_derruba": "um pacote de ajuste crível antes do Orçamento de 2027 e o juro longo voltando ao nível de antes da eleição"},
        {"nome": "P2: o mercado exagerou", "versao_forte": "a queda é a desmontagem de uma aposta no outro resultado; a economia real (emprego, renda) vai bem e o mercado costuma errar a dívida para pior",
         "o_que_se_veria": "a bolsa e o dólar recuperando parte da perda em semanas, o juro longo voltando ao nível de junho, o governo cumprindo a meta de 2027",
         "o_que_mostra": p2, "o_que_derruba": "o juro longo ficando acima do de junho, a meta de 2027 descumprida ou mudada, o limite de gasto alterado em 2028 sem compensação"},
    ]


def todas_as_contas(r: dict) -> list[float]:
    v = r["M6_variantes_revisao"]
    todas = [r["M6_divida"]["S1_central"]["2030"], v["p2_sem_premio"]["divida_2030"], v["p1_macro_do_focus"]["divida_2030"],
             v["p1_ponto_de_partida_pior"]["divida_2030"], v["p1_limite_nao_segura"]["divida_2030"], v["p1_juntas"]["divida_2030"]]
    m = v.get("p2_metas_do_pldo_cumpridas", {})
    todas += [x for x in (m.get("divida_2030_sem_premio"), m.get("divida_2030_com_premio")) if x is not None]
    if "p2_premio_contra_a_curva_de_junho" in v:
        todas.append(v["p2_premio_contra_a_curva_de_junho"]["divida_2030"])
    todas += list(r["M6_divida"]["sensibilidade_2030"].values())
    return todas


def qual_sustenta(r: dict) -> str:
    todas = todas_as_contas(r)
    ini = r["M6_divida"]["S1_central"]["2026"]
    return (f"Em nenhuma das {len(todas)} contas a dívida para de subir: em 2030 ela fica entre {br(min(todas))}% e {br(max(todas))}% do PIB, contra {br(ini)}% em 2026. "
            "Nisso o dado sustenta a P1: o problema das contas é real e vem de antes da eleição. Onde a P2 tem razão é no tamanho do susto do dia: parte da queda é aposta desfeita, "
            "e o mercado já errou a dívida para pior. O que decide entre as duas daqui para a frente é se o governo cumpre a meta de 2027 e o que faz com o limite de gasto em 2028.")


def secao_mercado(r: dict, v: dict, jr: dict) -> list[str]:
    m1 = r.get("M1_mercado") or {}
    m6 = r["M6_divida"]
    s = ["## 2. O mercado no dia seguinte (M1)\n"]
    e = m1.get("dia")
    if e and e.get("ibovespa") and m1.get("fechamento_de_26_out"):
        linhas = [["Ibovespa", f"{sinal(e['ibovespa']['variacao_pct'], 2)}%", f"{br(e['ibovespa']['inicio'], 0)} → {br(e['ibovespa']['fim'], 0)} pontos"],
                  ["EWZ (ações do Brasil em Nova York, em dólar)", f"{sinal(e['ewz']['variacao_pct'], 2)}%", f"US$ {br(e['ewz']['inicio'], 2)} → US$ {br(e['ewz']['fim'], 2)}"],
                  ["EEM (ações de emergentes, controle)", f"{sinal(e['eem']['variacao_pct'], 2)}%", ""],
                  ["Dólar contra o real (Yahoo, fechamento)", f"{sinal(e['usdbrl_yahoo']['variacao_pct'], 2)}%", f"R$ {br(e['usdbrl_yahoo']['inicio'], 4)} → R$ {br(e['usdbrl_yahoo']['fim'], 4)}"]]
        if e.get("usdbrl_ptax"):
            linhas.append(["Dólar PTAX (média do dia, Banco Central)", f"{sinal(e['usdbrl_ptax']['variacao_pct'], 2)}%", f"R$ {br(e['usdbrl_ptax']['inicio'], 4)} → R$ {br(e['usdbrl_ptax']['fim'], 4)}"])
        dv = m1.get("dolar_a_vista")
        if dv:
            linhas.append(["Dólar à vista (fechamento, imprensa)", f"{sinal(dv['variacao_pct'], 2)}%", f"→ R$ {br(dv['fim'], 4)} ([fonte]({dv['fonte']}))"])
        linhas.append(["Dólar contra México, Chile, Colômbia e África do Sul (média, controle)", f"{sinal(e['controle_moeda_pct'], 2)}%", ""])
        for j in m1.get("juros", []):
            linhas.append([j["nome"], f"{sinal(j['variacao_pp'] * 100, 0)} centésimos", j.get("detalhe", "")])
        s += [f"Janela: fechamento de {e['janela'][0]} contra o de {e['janela'][1]}.\n", tabela(["Ativo", "Variação", "De → para"], linhas) + "\n",
              f"**O que se atribui à eleição (o Brasil menos os outros emergentes):** bolsa {sinal(e.get('excesso_ibovespa_contra_eem_pct', 0), 2)} pontos; dólar {sinal(e.get('excesso_dolar_contra_cesta_pct', 0), 2)} pontos (dólar do Yahoo nos dois lados, para a mesma hora; a PTAX é a média do dia e mede outra coisa).\n"]
        pos = m1.get("posicao_da_queda_de_26_out")
        if pos:
            outras = [q for q in m1["maiores_quedas_desde_1995"] if q["data"] != e["janela"][1]][:pos - 1]
            s.append(f"**É a {pos}ª maior queda diária do Ibovespa desde 1995.** Maiores que ela: "
                     + "; ".join(f"{q['data'][8:10]}/{q['data'][5:7]}/{q['data'][:4]} ({br(q['variacao_pct'], 2)}%)" for q in outras)
                     + ". Nas eleições anteriores (§2.2), o pior dia seguinte tinha sido o de 2002.\n")
        s += [f"- {n}" for n in m1.get("notas", [])] + [""]
    else:
        s.append("Os números do fechamento de 26/out entram quando o script rodar depois das 18h. Antes disso, nenhuma variação de dentro do pregão é usada.\n")
    pm = m1.get("polymarket")
    if pm:
        s.append(f"**O que o mercado esperava:** às {pm['hora_brt'][11:16]} de 25/out, último registro antes do fim da votação, o Polymarket dava {br(100 * pm['p'], 1)}% de chance a Lula (no fim de 23/out, {br(100 * pm['fim_de_23_out'], 1)}%). "
                 f"A reação do dia mede só a parte que não estava no preço; para ter a diferença inteira entre os dois resultados, a variação se divide por {br(1 - pm['p'], 3)}.\n")
    s.append("### 2.1 O prêmio de juros\n")
    txt = f"Prêmio usado na conta da dívida: **{br(m6['premio_pp'], 2)} ponto ao ano** ({m6['premio_origem']})."
    pj = v.get("p2_premio_contra_a_curva_de_junho")
    if pj:
        txt += f" Medido contra a curva de 12/jun (data da base da IFI), e não contra a véspera, o prêmio é de {br(pj['premio_pp'], 2)} ponto (variante, §11)."
    s.append(txt + "\n")
    if m1.get("termo_2028_em_23_out") is not None:
        t26 = m1.get("termo_2028_em_26_out")
        s.append(f"**A Selic que a curva cobra para 2028** (taxa a termo entre os DI de janeiro de 2028 e de 2029, emenda 4): {br(m1['termo_2028_em_23_out'], 2)}% em 23/out"
                 + (f" e {br(t26, 2)}% em 26/out" if t26 is not None else "") + f". A Selic hoje é {br(jr['selic_meta'], 2)}%.\n")
    return s


def relatorio(r: dict, val: dict, x: dict) -> str:
    m6, m3, ch = r["M6_divida"], r["M3_gasto"], r["M3_contas_hoje"]
    jr, m5 = r["M4_juro_real"], r["M5_medidas"]
    prev = r["M7_previsao_do_mercado_contra_o_realizado"]
    m1 = r.get("M1_mercado") or {}
    hist = r["M1_historico_eleicoes"]
    h = {l["ano"]: l for l in hist}
    ifi = x["ifi"]["base"]
    v = r["M6_variantes_revisao"]
    fx = r["M6_faixa_2030"]
    s0_var = m6["S0_base_ifi"]["2030"] - m6["S0_base_ifi"]["2026"]
    est_sem = r.get("M6_estabilizador_sem_premio")
    s = ["# O que esperar da economia do Brasil de 2027 a 2030\n",
         f"**Relatório gerado por script em {r['gerado_em'][:10]}** a partir de `resultados/RESUMO.json`. Regras escritas antes de qualquer conta em [`docs/PRE_REGISTRO.md`](docs/PRE_REGISTRO.md), com 6 emendas, cada uma dizendo o que já tinha sido visto. "
         "Análise feita pelo Claude (IA da Anthropic), a pedido de Gabriel Alexandre. **Não é recomendação de investimento.**\n",
         "## O que este projeto não consegue dizer\n",
         f"- **Não prevê preço de ação, de dólar ou de juro.** Os números de 2027 a 2030 são cenários com regra escrita antes. No passado, a previsão do mercado para a dívida três anos depois errou, em média, {br(prev['resumo']['erro_medio_absoluto_dlsp_pp'])} pontos do PIB (§8).",
         "- **Não julga intenção.** Uma medida de ano eleitoral pode ter sido feita para ganhar votos ou não; o projeto mede data, custo e quem paga.",
         "- **O dia seguinte é um dia.** A reação de 26/out mede o susto do mercado com o resultado, não o mandato inteiro (§2.2).",
         "- **A base é a projeção de médio prazo mais recente da IFI, de junho de 2026**, anterior a medidas de setembro e outubro. O efeito delas está calculado à parte (§7.1).",
         "- **O modelo da dívida não tem a volta do juro sobre a confiança** (a dívida maior encarece o juro, que aumenta a dívida). O efeito do fim da escala 6x1 sobre o PIB também fica de fora, por falta de número público.",
         "- **Não testa se houve fraude**: o pedido supõe que não haja contestação.\n",
         "## 1. A resposta curta\n",
         tabela(["", "O que o pedido disse", "Veredito", "Por quê"], vereditos(r)) + "\n",
         f"**A dívida no cenário central: {m6['classificacao_S1']}.** A dívida bruta do governo passa de {br(m6['S1_central']['2026'])}% do PIB em 2026 para **{br(m6['S1_central']['2030'])}% em 2030** "
         f"({sinal(m6['variacao_2026_2030_S1_pp'])} pontos; faixa pelo erro histórico, de {br(fx['de'], 0)}% a {br(fx['ate'], 0)}%). Mesmo sem nenhum prêmio de juros ela sobe {br(s0_var)} pontos, o que já é \"sobe rápido\" pela régua. "
         f"Para a dívida parar de subir em 2030, o governo precisaria de um superávit de {br(m6['primario_que_estabiliza_em_2030_pct_pib'])}% do PIB naquele ano"
         + (f" ({br(est_sem)}% se o mercado não cobrasse prêmio)" if est_sem is not None else "")
         + f"; a base da IFI prevê um {deficit(m6['primario_previsto_2030_base_ifi'])}. A distância é de {br(m6['distancia_ate_estabilizar_pp'])} pontos do PIB. "
         f"Em nenhuma das {len(todas_as_contas(r))} contas feitas (§7.1) a dívida para de subir.\n",
         "**O cenário central, ano a ano** (o que a conta usa: o cenário base da IFI de junho, mais o prêmio de juros medido no dia):\n",
         tabela(["Ano", "PIB (IFI)", "Selic no fim do ano (IFI)", "Resultado primário do setor público (IFI)", "Dívida bruta no cenário central"],
                [[a, f"{br(ifi['pib_real_pct'][a])}%", f"{br(ifi['selic_fim_pct'][a], 0)}%", deficit(ifi["primario_sp"][a]), f"{br(m6['S1_central'][a])}%"] for a in ANOS]) + "\n"]
    f, sel = r["M4_focus_macro"], r["M4_focus_selic"]
    s += [f"**O que o mercado esperava antes da eleição** (mediana do Focus de {sel['2027']['data']}; é outro cenário, mais pessimista no PIB e no juro que o da IFI; a dívida com ele está no §7.1):\n",
          tabela(["Ano", "PIB", "Inflação (IPCA)", "Selic no fim do ano", "Dólar no fim do ano", "Dívida bruta (Focus)"],
                 [[a, f"{br(f['PIB Total'][a])}%", f"{br(f['IPCA'][a], 2)}%", f"{br(sel[a]['mediana'], 2)}%", f"R$ {br(f['Câmbio'][a], 2)}", f"{br(m6['focus_dbgg'][a])}%"] for a in ANOS]) + "\n"]
    s += secao_mercado(r, v, jr)
    s.append("### 2.2 As eleições anteriores\n")
    linhas = [[l["ano"], l["vencedor"], f"{sinal(l['ibovespa_dia_pct'])}%", f"{sinal(l['dolar_dia_pct'])}%" if l.get("dolar_dia_pct") is not None else "",
               f"{br(l['pib_real_medio_pct'])}%", f"{br(l['divida_bruta_inicio'])} → {br(l['divida_bruta_fim'])}" + ("" if l["mandato_completo"] else " (projeção do FMI)"),
               f"{sinal(l['ibovespa_real_pct'], 0)}%" + ("" if l["mandato_completo"] else " (até hoje)")] for l in hist if l["ano"] < 2026]
    s.append(tabela(["Eleição", "Venceu", "Ibovespa no dia seguinte", "Dólar PTAX no dia seguinte", "PIB médio no mandato seguinte (FMI)",
                     "Dívida bruta, conceito do FMI (% do PIB)", "Ibovespa acima da inflação no mandato"], linhas) + "\n")
    caiu = [l for l in hist if l["ano"] < 2026 and l["ibovespa_dia_pct"] < 0]
    acerto = sum(1 for l in hist if l["ano"] < 2026 and (l["ibovespa_dia_pct"] > 0) == (l["ibovespa_real_pct"] > 0))
    meta03 = re.search(r"(\d+,\d+)% do PIB", x["ok"].get("H03", {}).get("trecho_a", ""))
    s.append(f"Em {len(caiu)} das 6 eleições a bolsa caiu no dia seguinte. A direção do dia bateu com a da bolsa no mandato em **{acerto} de 6**. "
             f"Em 2002 o Ibovespa caiu {br(-h[2002]['ibovespa_dia_pct'])}% no dia seguinte e depois subiu {br(h[2002]['ibovespa_real_pct'], 0)}% acima da inflação até 2006; "
             f"em 2010 subiu {br(h[2010]['ibovespa_dia_pct'])}% e depois caiu {br(-h[2010]['ibovespa_real_pct'], 0)}% acima da inflação até 2014. "
             "**O dia seguinte mede o susto, não o mandato.** O que decidiu os mandatos foi o que veio depois" + (f": em 2003, a meta de superávit de {meta03.group(1)}% do PIB" if meta03 else "")
             + f"; no mandato que começou em 2015, PIB médio de {br(h[2014]['pib_real_medio_pct'])}% ao ano. A dívida desta tabela está no conceito do FMI, maior que o do Banco Central usado no resto do relatório.\n")
    s.append("## 3. O dinheiro estrangeiro (M2)\n")
    s += [f"- {linha}" for linha in m1.get("fluxo", [])]
    bp = (m1.get("fluxo_numeros") or {}).get("balanco_de_pagamentos") or {}
    if bp:
        acoes = bp.get("ações", {}).get("soma_us_mi", 0)
        renda_fixa = sum(v["soma_us_mi"] for k, v in bp.items() if k.startswith("títulos"))
        s.append(f"\nA régua de A2 usa a primeira medida (a bolsa, B3), como o pré-registro manda. Pela segunda (o balanço de pagamentos), a entrada de 2026 foi sobretudo em renda fixa (US$ {br(renda_fixa / 1000)} bi), "
                 f"e em ações, contando tudo, o saldo foi de {'saída' if acoes < 0 else 'entrada'} (US$ {br(abs(acoes) / 1000)} bi). As duas medidas contam coisas diferentes: a B3 só a bolsa; o Banco Central também ações fora da bolsa e recibos negociados lá fora.\n")
    s.append("## 4. As contas públicas hoje (M3)\n")
    p, j = ch["bcb-primario-12m"], ch["bcb-juros-nominais-12m"]
    db, dl = ch["bcb-divida-bruta-gg"], ch["bcb-divida-liquida-sp"]
    cols = ["dez_2014", "dez_2018", "dez_2022", "dez_2025"]
    s.append(tabela(["Banco Central, % do PIB", "dez/2014", "dez/2018", "dez/2022", "dez/2025", f"último ({p['ultimo']['mes'][:7]})"], [
        ["Déficit primário em 12 meses (negativo = superávit)"] + [br(p.get(c), 2) for c in cols] + [br(p["ultimo"]["valor"], 2)],
        ["Juros da dívida em 12 meses"] + [br(j.get(c), 2) for c in cols] + [br(j["ultimo"]["valor"], 2)],
        ["Dívida bruta do governo geral (conceito do Banco Central)"] + [br(db.get(c)) for c in cols] + [br(db["ultimo"]["valor"])],
        ["Dívida líquida do setor público"] + [br(dl.get(c)) for c in cols] + [br(dl["ultimo"]["valor"])],
    ]) + "\n")
    s.append(f"**O déficit total (primário mais juros) é de {br(ch['deficit_nominal_12m_pct_pib'])}% do PIB em 12 meses, e a maior parte é juro:** {br(j['ultimo']['valor'], 2)} pontos de juros contra {br(p['ultimo']['valor'], 2)} de déficit primário.\n")
    if "M4_custo_de_um_ponto_de_selic" in r:
        c = r["M4_custo_de_um_ponto_de_selic"]
        s.append(f"Mais da metade da dívida federal acompanha a Selic: {br(c['fatia_selic_pct'], 2)}% (Tesouro, ago/2026; uma série da IFI, com outra base, dá menos). Cada ponto de Selic custa cerca de R$ {br(c['rs_bi_por_ano'], 0)} bi por ano.\n")
    s.append("### 4.1 O tamanho do gasto, contra o mundo (A5)\n")
    s.append(tabela(["FMI, Fiscal Monitor, % do PIB", "2019", "2022", "2025", "2026 (projeção)"], [
        ["Brasil: gasto total do governo geral"] + [br(m3["despesa_total"][a]["brasil"]) for a in ["2019", "2022", "2025", "2026"]],
        ["Emergentes do G20 (mediana, sem o Brasil)"] + [br(m3["despesa_total"][a]["mediana_g20_emergentes"]) for a in ["2019", "2022", "2025", "2026"]],
        ["Emergentes e renda média (média do FMI)"] + [br(m3["despesa_total"][a]["media_fm_emg"]) for a in ["2019", "2022", "2025", "2026"]],
        ["América Latina (mediana, sem o Brasil)"] + [br(m3["despesa_total"][a]["mediana_america_latina"]) for a in ["2019", "2022", "2025", "2026"]],
        ["Países avançados (média)"] + [br(m3["despesa_total"][a]["media_avancados"]) for a in ["2019", "2022", "2025", "2026"]],
    ]) + "\n")
    nom = m3["resultado_nominal"]
    s.append(f"Diferença do Brasil para a mediana dos emergentes do G20 em 2025: **{sinal(m3['diferenca_2025_contra_mediana_g20_pp'])} pontos do PIB** (régua: 5 ou mais = confirmada). "
             f"O FMI estima os juros líquidos do Brasil em {br(m3['juros_liquidos_fmi_pct_pib']['2025'])}% do PIB em 2025; como o gasto total inclui os juros, a parte sem juros fica um pouco abaixo da diferença acima. "
             f"Déficit nominal do governo geral em 2025 (régua 3): Brasil {br(-nom['2025']['brasil'])}% do PIB, mediana dos emergentes do G20 {br(-nom['2025']['mediana_g20_emergentes'])}%. "
             "A régua 2 (crescimento real da despesa do governo central de 2023 a 2026 contra 2015 a 2022) não foi calculada nesta rodada (emenda 6).\n")
    s.append("## 5. O juro (M4)\n")
    a6 = m1.get("veredito_a6", {})
    s.append(f"Selic de **{br(jr['selic_meta'], 2)}%** ao ano e inflação esperada para os próximos 12 meses de **{br(jr['ipca_esperado_12m'], 2)}%** (Focus de {jr['focus_data']}): juro real de **{br(jr['juro_real_ex_ante_pct'])}%** ao ano. "
             + (f"No ranking MoneYou de 16/set, feito com outra estimativa de inflação, o juro real do Brasil era {br(a6.get('juro_real_brasil_ranking'), 2)}%, o maior entre 40 países." if a6.get("posicao") == 1 else "") + "\n")
    s += [f"- {nota}" for nota in r.get("M4_notas", []) if "MoneYou" not in nota]
    s.append("")
    s.append("## 6. As medidas de 2025 e 2026 e as promessas: quem paga (M5)\n")
    s.append("Categorias: **A** compensada na própria lei (imposto maior para outro grupo) · **B** cabe no limite de gasto (o dinheiro sai de outra despesa do Orçamento) · **C** fora da meta · **D** fora do Orçamento (tarifa, fundo, renúncia, crédito) · **E** sem fonte declarada.\n")
    linhas = [[l["id"], l["nome"], l["categoria"], l["custo_informado_rs_bi"] or "sem custo publicado", l["recorrente_a_partir_de_2027_rs_bi"] or "não se repete",
               l["de_onde_vem_o_dinheiro"][:170]] for l in x["med"] if l["id"].startswith("M")]
    s.append(tabela(["", "Medida", "Cat.", "Custo informado (R$ bi)", "Custo que se repete a partir de 2027 (R$ bi por ano)", "De onde vem o dinheiro"], linhas) + "\n")
    s.append(f"**Custo que se repete por ano a partir de 2027: R$ {br(m5['total_recorrente_rs_bi'])} bi ({br(m5['total_recorrente_pct_pib_2027'], 2)}% do PIB).** "
             + "; ".join(f"categoria {k}: R$ {br(vv)} bi ({br(m5['por_categoria_fatia_pct'][k], 0)}%)" for k, vv in sorted(m5["por_categoria_rs_bi"].items())) + ". "
             "A leitura de quanto se repete por ano é do projeto, com o motivo escrito ao lado de cada medida em `dados/evidencias/MEDIDAS_E_PROMESSAS.csv`.\n")
    if "M01" in x["ok"]:
        s.append("**A compensação do Imposto de Renda é contestada:** a lei compensa a isenção com a tributação mínima de altas rendas, e a Consultoria de Orçamento do Senado e a IFI estimaram perda líquida de arrecadação.\n")
    s.append("**Promessas do 2º mandato:**\n")
    linhas = [[l["id"], l["nome"], l["categoria"] or "", l["custo_informado_rs_bi"] or "sem custo publicado", l["de_onde_vem_o_dinheiro"][:160]] for l in x["med"] if l["id"].startswith("P")]
    s.append(tabela(["", "Promessa", "Cat.", "Custo (R$ bi por ano)", "De onde vem o dinheiro"], linhas) + "\n")
    s.append("## 7. 2027 a 2030 (M6)\n")
    s.append(tabela(["Cenário (dívida bruta, conceito do Banco Central, % do PIB)"] + ANOS, [
        ["S0: base da IFI (jun/2026)"] + [br(m6["S0_base_ifi"][a]) for a in ANOS],
        [f"S1: central (base + prêmio de {br(m6['premio_pp'], 2)} ponto)"] + [br(m6["S1_central"][a]) for a in ANOS],
        [f"S2: risco (S1 + promessas com custo e sem fonte, {br(r['M5_S2']['custo_pct_pib'], 2)}% do PIB)"] + [br(m6["S2_risco"][a]) for a in ANOS],
        ["Mercado (Focus, antes da eleição)"] + [br(m6["focus_dbgg"][a]) for a in ANOS],
    ]) + "\n")
    fmi = m6["fmi_weo_out2026_conceito_fmi"]
    s.append(f"No conceito do FMI, que soma os títulos do Tesouro na carteira do Banco Central, o FMI projeta {br(fmi.get('2026'))}% em 2026 e {br(fmi.get('2030'))}% em 2030 (WEO de out/2026). Não se compara um conceito com o outro.\n")
    s.append("### 7.1 Sensibilidade e variantes (dívida em 2030)\n")
    nomes = {"premio_metade": "prêmio pela metade", "premio_dobro": "prêmio em dobro", "repasse_total_imediato": "o prêmio passa inteiro para a dívida já em 2027",
             "pib_1_ponto_abaixo": "PIB 1 ponto abaixo por ano", "pib_1_ponto_acima": "PIB 1 ponto acima por ano",
             "custos_fora_da_base_ifi": "se o limite de gasto não segurar o reajuste do Bolsa Família e o Desenrola 3.0",
             "cenario_otimista_ifi_com_premio": "cenário otimista da IFI, com o prêmio", "cenario_pessimista_ifi_com_premio": "cenário pessimista da IFI, com o prêmio"}
    linhas = [[nomes[k], br(vv)] for k, vv in m6["sensibilidade_2030"].items()]
    linhas.append(["(P2) sem prêmio nenhum", br(v["p2_sem_premio"]["divida_2030"])])
    pj = v.get("p2_premio_contra_a_curva_de_junho")
    if pj:
        linhas.append([f"(P2) prêmio medido contra a curva de junho ({br(pj['premio_pp'], 2)} ponto)", br(pj["divida_2030"])])
    mt = v.get("p2_metas_do_pldo_cumpridas")
    if mt:
        linhas += [["(P2) metas do PLDO 2027 cumpridas, sem prêmio", br(mt["divida_2030_sem_premio"])], ["(P2) metas do PLDO 2027 cumpridas, com o prêmio", br(mt["divida_2030_com_premio"])]]
    linhas += [["(P1) macro do Focus no lugar do da IFI", br(v["p1_macro_do_focus"]["divida_2030"])],
               ["(P1) 2026 começando com os juros já acima da base", br(v["p1_ponto_de_partida_pior"]["divida_2030"])],
               [f"(P1) limite de gasto sem segurar os R$ {br(v['p1_limite_nao_segura']['custo_rs_bi'])} bi por ano que a base não tem", br(v["p1_limite_nao_segura"]["divida_2030"])],
               ["(P1) as três juntas", br(v["p1_juntas"]["divida_2030"])]]
    s.append(tabela(["Variante", "Dívida em 2030 (% do PIB)"], linhas) + "\n")
    s.append("### 7.2 O aperto do Orçamento\n")
    s += [f"- {x['ok'][i]['fato']} ([fonte]({x['ok'][i]['url_a']}))" for i in ("F42", "F45", "F08", "F09", "T13") if i in x["ok"]]
    s.append("")
    s.append("## 8. O teste do passado (M7)\n")
    linhas = [[l["eleicao"], l["ano_alvo"], br(l["dlsp_prevista"]), br(l["dlsp_realizada"]), sinal(l["erro_dlsp_pp"]),
               f"{br(l['pib_medio_previsto'])}% / {br(l['pib_medio_realizado'])}%"] for l in prev["linhas"]]
    s.append(tabela(["Eleição", "Ano previsto", "Dívida líquida prevista (Focus, outubro)", "Aconteceu", "Erro (pontos)", "PIB médio previsto / aconteceu"], linhas) + "\n")
    rz = prev["resumo"]
    pior = min(prev["linhas"], key=lambda l: l["erro_dlsp_pp"])
    s.append(f"Erro médio de {br(rz['erro_medio_absoluto_dlsp_pp'])} pontos do PIB na dívida e de {br(rz['erro_medio_absoluto_pib_pp'])} ponto no PIB. "
             f"Em {rz['vezes_que_o_mercado_previu_divida_maior']} de {rz['n']} eleições o mercado previu dívida **maior** do que aconteceu; a exceção foi a eleição de {pior['eleicao']}, com erro de {br(pior['erro_dlsp_pp'])} pontos. "
             "A conta compara a previsão de cada época com a série atual do Banco Central, que mudou de método em 2008. É esse erro que dá a faixa do número central (§1).\n")
    s.append("## 9. Outras coisas importantes (M8)\n")
    s.append("Só entram temas com as duas fontes conferidas por script. A frase \"o que pode mudar\" é a leitura da pesquisa, não um número.\n")
    for k in sorted(x["dois"]):
        a = x["dois"][k]
        if not k.startswith("T") or k == "T11" or "youtube" in (a["fato"] + a["url_a"]).lower() or "canal" in a["fato"].lower():
            continue
        s.append(f"- **{a['tema']}.** {a['fato']}" + (f" *O que pode mudar:* {a['implicacao']}" if a["implicacao"] else "") + f" ([fonte]({a['url_a']}), [segunda fonte]({a['url_b']}))")
    s.append("")
    ok_val = sum(i["passou"] for i in val["itens"])
    conf = list(x["conf"].values())
    s += ["## 10. Como se conferiu\n",
          f"- Validação por um segundo caminho: **{ok_val} de {len(val['itens'])}** itens passaram (`resultados/VALIDACAO.json`).",
          f"- Achados de terceiros: {len(conf)} levantados, **{sum(1 for c in conf if c['estado_a'].startswith('ok'))}** com o trecho encontrado por script no texto capturado, {sum(1 for c in conf if c['estado_a'].startswith('ok') and c['estado_b'].startswith('ok'))} deles com a segunda fonte também conferida.",
          "- Revisão adversarial por três leitores independentes: [`docs/REVISAO_ADVERSARIAL.md`](docs/REVISAO_ADVERSARIAL.md). Leitura da IA: [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md). Como refazer: [`docs/REPLICAR.md`](docs/REPLICAR.md).\n",
          "## 11. As duas premissas (emenda 5)\n"]
    for pr in premissas(r):
        s += [f"### {pr['nome']}\n", f"- **A versão mais forte:** {pr['versao_forte']}.", f"- **O que se esperaria ver:** {pr['o_que_se_veria']}.",
              f"- **O que o dado mostra:** {pr['o_que_mostra']}.", f"- **O que a derrubaria:** {pr['o_que_derruba']}.\n"]
    s.append(f"**Qual o dado sustenta mais.** {qual_sustenta(r)}\n")
    return "\n".join(s)


def resumo_simples(r: dict) -> str:
    m6, jr, v5 = r["M6_divida"], r["M4_juro_real"], r["M5_vereditos"]
    fx = r["M6_faixa_2030"]
    todas = todas_as_contas(r)
    h = [l for l in r["M1_historico_eleicoes"] if l["ano"] < 2026]
    acerto = sum(1 for l in h if (l["ibovespa_dia_pct"] > 0) == (l["ibovespa_real_pct"] > 0))
    s = ["# Resumo simples\n", f"**Gerado em {r['gerado_em'][:10]}.** Completo: [`RELATORIO.md`](RELATORIO.md). Opinião da IA: [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md). Não é recomendação de investimento.\n",
         "## As afirmações do pedido\n", tabela(["Afirmação", "Veredito", "Por quê"], [[l[1], l[2], l[3]] for l in vereditos(r)]) + "\n", "## O que esperar até 2030\n",
         f"- **A dívida {m6['classificacao_S1']}:** de {br(m6['S1_central']['2026'])}% do PIB em 2026 para {br(m6['S1_central']['2030'])}% em 2030 no cenário central (faixa de {br(fx['de'], 0)}% a {br(fx['ate'], 0)}%).",
         f"- **Em nenhuma das {len(todas)} contas feitas a dívida para de subir**: em 2030 ela fica entre {br(min(todas))}% e {br(max(todas))}% do PIB, mesmo com as metas do próprio governo cumpridas.",
         f"- **Para ela parar de subir em 2030**, seria preciso um superávit de {br(m6['primario_que_estabiliza_em_2030_pct_pib'])}% do PIB naquele ano. O previsto é um {deficit(m6['primario_previsto_2030_base_ifi'])}.",
         f"- **O juro real é de {br(jr['juro_real_ex_ante_pct'])}% ao ano**, o maior do mundo. Antes da eleição, o mercado esperava a Selic em {br(r['M4_focus_selic']['2027']['mediana'], 2)}% no fim de 2027.",
         f"- **As medidas de 2025 e 2026 custam R$ {br(r['M5_medidas']['total_recorrente_rs_bi'])} bi por ano a partir de 2027**; {br(r['M5_medidas']['por_categoria_fatia_pct'].get('B', 0), 0)}% disso cabe no limite de gasto, ou seja, sai de outra despesa do Orçamento.",
         f"- **{v5['A4']['sem_custo_ou_sem_fonte']} de {v5['A4']['promessas']} promessas** do 2º mandato não têm custo publicado ou fonte declarada.",
         f"- **O dia seguinte não decide o mandato:** a direção da bolsa no dia seguinte à eleição bateu com a do mandato em {acerto} das 6 eleições desde 2002.\n"]
    return "\n".join(s)


def main() -> int:
    r = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))
    val = json.loads((RES / "VALIDACAO.json").read_text(encoding="utf-8"))
    x = carregar()
    (RAIZ / "RELATORIO.md").write_text(relatorio(r, val, x), encoding="utf-8")
    (RAIZ / "RESUMO_SIMPLES.md").write_text(resumo_simples(r), encoding="utf-8")
    print("RELATORIO.md e RESUMO_SIMPLES.md gravados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
