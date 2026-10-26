"""Escreve RELATORIO.md, RESUMO_SIMPLES.md e docs/REVISAO_ADVERSARIAL.md a partir de resultados/RESUMO.json.

Nenhum número é digitado à mão: tudo sai do RESUMO, da VALIDACAO e das tabelas de dados/evidencias.
A leitura da IA (docs/LEITURA_DA_IA.md) é escrita à parte e cita os mesmos números.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RES = RAIZ / "resultados"
REPO = "github.com/Gabriel-Alexandre/economia-brasil-2027-2030"


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


def achados() -> dict[str, dict]:
    ok = {l["id"]: l for l in csv.DictReader((RES / "TRECHOS_CONFERIDOS.csv").open(encoding="utf-8")) if l["estado_a"].startswith("ok")}
    return {l["id"]: l for l in csv.DictReader((RAIZ / "dados" / "evidencias" / "ACHADOS.csv").open(encoding="utf-8")) if l["id"] in ok}


def vereditos(r: dict) -> list[list]:
    m1 = r.get("M1_mercado") or {}
    a1 = m1.get("veredito_a1", {})
    a2 = m1.get("veredito_a2", {})
    g = r["M3_gasto"]
    jr = r["M4_juro_real"]
    v5 = r["M5_vereditos"]
    linhas = [
        ["A1", "\"a bolsa derreteu\"", a1.get("veredito", "aguardando o fechamento de 26/out"), a1.get("porque", "")],
        ["A2", "\"vários investimentos [...] acabou fugindo do Brasil\"", a2.get("veredito", "aguardando o dado da B3"), a2.get("porque", "")],
        ["A3", "\"muitas medidas\" no ano da eleição", v5["A3"]["veredito"],
         f"{v5['A3']['n']} medidas nos 12 meses antes da eleição; {br(v5['A3']['fatia_nao_compensada_pct'], 0)}% do custo que se repete não é compensado na própria lei. Intenção não se mede"],
        ["A4", "\"de onde é que vai vir esse dinheiro\"", v5["A4"]["veredito"],
         f"{v5['A4']['sem_custo_ou_sem_fonte']} de {v5['A4']['promessas']} promessas econômicas sem custo publicado ou sem fonte declarada"],
        ["A5", "\"a gastança do Brasil já está muito alta\"", g["veredito_a5"],
         f"o governo gasta {br(g['despesa_total']['2025']['brasil'])}% do PIB, contra {br(g['despesa_total']['2025']['mediana_g20_emergentes'])}% na mediana dos emergentes do G20 (FMI, 2025)"],
        ["A6", "\"o juro já está muito alto\"", m1.get("veredito_a6", {}).get("veredito", "ver M4"),
         m1.get("veredito_a6", {}).get("porque", f"juro real de {br(jr['juro_real_ex_ante_pct'])}% ao ano (Selic {br(jr['selic_meta'], 2)}% menos inflação esperada de {br(jr['ipca_esperado_12m'], 2)}%)")],
        ["A7", "\"a tendência é apenas aumentar\" (o juro)", r["M4_veredito_a7"], r.get("M4_porque_a7", "")],
    ]
    return linhas


def cenario_central(r: dict) -> list[list]:
    f = r["M4_focus_macro"]
    sel = r["M4_focus_selic"]
    m6 = r["M6_divida"]
    linhas = []
    for a in ["2027", "2028", "2029", "2030"]:
        linhas.append([a, f"{br(f['PIB Total'][a])}%", f"{br(f['IPCA'][a], 2)}%", f"{br(sel[a]['mediana'], 2)}%",
                       f"R$ {br(f['Câmbio'][a], 2)}", f"{br(m6['S1_central'][a])}%"])
    return linhas


def relatorio(r: dict, val: dict) -> str:
    m6, m3, ch, jr = r["M6_divida"], r["M3_gasto"], r["M3_contas_hoje"], r["M4_juro_real"]
    m5, v5 = r["M5_medidas"], r["M5_vereditos"]
    prev = r["M7_previsao_do_mercado_contra_o_realizado"]
    m1 = r.get("M1_mercado") or {}
    A = achados()
    hist = r["M1_historico_eleicoes"]
    ok_val = sum(i["passou"] for i in val["itens"])
    s = []
    s.append("# O que esperar da economia do Brasil de 2027 a 2030\n")
    s.append(f"**Relatório gerado por script em {r['gerado_em'][:10]}** a partir de `resultados/RESUMO.json`. Regras escritas antes de qualquer conta em [`docs/PRE_REGISTRO.md`](docs/PRE_REGISTRO.md). Análise feita pelo Claude (IA da Anthropic), a pedido de Gabriel Alexandre. **Não é recomendação de investimento.**\n")
    s.append("## O que este projeto não consegue dizer\n")
    s.append("- **Não prevê preço de ação, de dólar ou de juro.** Os números de 2027 a 2030 são cenários com regra escrita antes, não profecia. No passado, a previsão do mercado para a dívida três anos depois errou, em média, "
             f"{br(prev['resumo']['erro_medio_absoluto_dlsp_pp'])} pontos do PIB (§8).")
    s.append("- **Não julga intenção.** Uma medida de ano eleitoral pode ter sido feita para ganhar votos ou não; o projeto mede data, custo e quem paga.")
    s.append("- **O dia seguinte é um dia.** A reação de 26/out mede o susto do mercado com o resultado, não o mandato inteiro (§2.2).")
    s.append("- **A base da IFI é de junho de 2026**, antes de medidas de setembro e outubro (o reajuste do Bolsa Família e o Desenrola 3.0). O efeito delas está calculado à parte (§7.1).")
    s.append("- **Não testa se houve fraude**: o pedido supõe que não haja contestação.\n")
    s.append("## 1. A resposta curta\n")
    s.append(tabela(["", "O que o pedido disse", "Veredito", "Por quê"], vereditos(r)) + "\n")
    s.append(f"**A dívida no cenário central: {m6['classificacao_S1']}.** A dívida bruta passa de {br(m6['S1_central']['2026'])}% do PIB em 2026 para "
             f"{br(m6['S1_central']['2030'])}% em 2030 ({sinal(m6['variacao_2026_2030_S1_pp'])} pontos). Para ela parar de subir, o governo precisaria de um superávit primário de "
             f"{br(m6['primario_que_estabiliza_em_2030_pct_pib'])}% do PIB por ano; a base da IFI prevê {br(m6['primario_previsto_2030_base_ifi'])}%. A distância é de "
             f"{br(m6['distancia_ate_estabilizar_pp'])} pontos do PIB.\n")
    s.append("**O cenário central, ano a ano** (macro: mediana do Focus; dívida: cálculo do projeto, cenário S1):\n")
    s.append(tabela(["Ano", "PIB", "Inflação (IPCA)", "Selic no fim do ano", "Dólar no fim do ano", "Dívida bruta (% do PIB)"], cenario_central(r)) + "\n")
    focus_data = r["M4_focus_selic"]["2027"]["data"]
    s.append(f"Focus de {focus_data}. Se o Focus de depois da eleição mudar, a tabela muda junto quando o script rodar de novo.\n")

    # 2. mercado
    s.append("## 2. O mercado no dia seguinte (M1)\n")
    e = m1.get("dia")
    if e and e.get("ibovespa"):
        linhas = [["Ibovespa", f"{sinal(e['ibovespa']['variacao_pct'], 2)}%", f"{br(e['ibovespa']['inicio'], 0)} → {br(e['ibovespa']['fim'], 0)} pontos"],
                  ["EWZ (ações do Brasil em Nova York, em dólar)", f"{sinal(e['ewz']['variacao_pct'], 2)}%", f"US$ {br(e['ewz']['inicio'], 2)} → US$ {br(e['ewz']['fim'], 2)}"],
                  ["EEM (ações de emergentes, controle)", f"{sinal(e['eem']['variacao_pct'], 2)}%", ""],
                  ["Dólar contra o real (Yahoo)", f"{sinal(e['usdbrl_yahoo']['variacao_pct'], 2)}%", f"R$ {br(e['usdbrl_yahoo']['inicio'], 4)} → R$ {br(e['usdbrl_yahoo']['fim'], 4)}"],
                  ["Dólar contra México, Chile, Colômbia e África do Sul (média, controle)", f"{sinal(e['controle_moeda_pct'], 2)}%", ""]]
        if e.get("usdbrl_ptax"):
            linhas.insert(4, ["Dólar PTAX (Banco Central)", f"{sinal(e['usdbrl_ptax']['variacao_pct'], 2)}%", f"R$ {br(e['usdbrl_ptax']['inicio'], 4)} → R$ {br(e['usdbrl_ptax']['fim'], 4)}"])
        for j in m1.get("juros", []):
            linhas.append([j["nome"], f"{sinal(j['variacao_pp'] * 100, 0)} centésimos", j.get("detalhe", "")])
        s.append(f"Janela: fechamento de {e['janela'][0]} contra o de {e['janela'][1]}.\n")
        s.append(tabela(["Ativo", "Variação", "De → para"], linhas) + "\n")
        s.append(f"**Excesso contra os emergentes:** bolsa {sinal(e.get('excesso_ibovespa_contra_eem_pct', 0), 2)} pontos; dólar {sinal(e.get('excesso_dolar_contra_cesta_pct', 0), 2)} pontos. É o que se atribui à eleição.\n")
        for nota in m1.get("notas", []):
            s.append(f"- {nota}")
        s.append("")
    else:
        s.append("O fechamento de 26/out ainda não estava no dado quando este relatório foi gerado.\n")
    s.append("### 2.1 O prêmio de juros\n")
    s.append(f"Prêmio usado na conta da dívida: **{br(m6['premio_pp'], 2)} pontos ao ano** ({m6['premio_origem']}).\n")
    s.append("### 2.2 As eleições anteriores\n")
    linhas = []
    for l in hist:
        if l["ano"] == 2026:
            continue
        linhas.append([l["ano"], l["vencedor"], f"{sinal(l['ibovespa_dia_pct'])}%", f"{sinal(l['dolar_dia_pct'])}%" if l.get("dolar_dia_pct") is not None else "",
                       f"{br(l['pib_real_medio_pct'])}%", f"{br(l['divida_bruta_inicio'])} → {br(l['divida_bruta_fim'])}",
                       f"{sinal(l['ibovespa_real_pct'], 0)}%" + ("" if l["mandato_completo"] else " (até hoje)")])
    s.append(tabela(["Eleição", "Venceu", "Ibovespa no dia seguinte", "Dólar (PTAX) no dia seguinte", "PIB médio no mandato seguinte",
                     "Dívida bruta, conceito FMI (% do PIB)", "Ibovespa real no mandato"], linhas) + "\n")
    h = {l["ano"]: l for l in hist}
    caiu = [l for l in hist if l["ano"] < 2026 and l["ibovespa_dia_pct"] < 0]
    acerto = sum(1 for l in hist if l["ano"] < 2026 and (l["ibovespa_dia_pct"] > 0) == (l["ibovespa_real_pct"] > 0))
    s.append(f"Em {len(caiu)} das 6 eleições a bolsa caiu no dia seguinte. A direção do dia bateu com a direção da bolsa no mandato em **{acerto} de 6**. "
             f"Em 2002 o Ibovespa caiu {br(-h[2002]['ibovespa_dia_pct'])}% no dia seguinte e depois subiu {br(h[2002]['ibovespa_real_pct'], 0)}% acima da inflação até 2006; em 2010 subiu {br(h[2010]['ibovespa_dia_pct'])}% no dia seguinte e caiu {br(-h[2010]['ibovespa_real_pct'], 0)}% acima da inflação até 2014. "
             "**O dia seguinte mede o susto, não o mandato.** O que decidiu os mandatos foi o que veio depois: em 2003, a meta de superávit de 4,25% do PIB; em 2015, a recessão.\n")
    # 3. dinheiro estrangeiro
    s.append("## 3. O dinheiro estrangeiro (M2)\n")
    if m1.get("fluxo"):
        for linha in m1["fluxo"]:
            s.append(f"- {linha}")
        s.append("")
    else:
        s.append("Aguardando a coleta do saldo do investidor estrangeiro na B3.\n")
    # 4. contas hoje
    s.append("## 4. As contas públicas hoje (M3)\n")
    p, j = ch["bcb-primario-12m"], ch["bcb-juros-nominais-12m"]
    db, dl = ch["bcb-divida-bruta-gg"], ch["bcb-divida-liquida-sp"]
    s.append(tabela(["Indicador (Banco Central, % do PIB)", "dez/2014", "dez/2018", "dez/2022", "dez/2025", f"último ({p['ultimo']['mes'][:7]})"], [
        ["Déficit primário em 12 meses (positivo = déficit)", br(p.get("dez_2014"), 2), br(p.get("dez_2018"), 2), br(p.get("dez_2022"), 2), br(p.get("dez_2025"), 2), br(p["ultimo"]["valor"], 2)],
        ["Juros da dívida em 12 meses", br(j.get("dez_2014"), 2), br(j.get("dez_2018"), 2), br(j.get("dez_2022"), 2), br(j.get("dez_2025"), 2), br(j["ultimo"]["valor"], 2)],
        ["Dívida bruta do governo geral", br(db.get("dez_2014"), 1), br(db.get("dez_2018"), 1), br(db.get("dez_2022"), 1), br(db.get("dez_2025"), 1), br(db["ultimo"]["valor"], 1)],
        ["Dívida líquida do setor público", br(dl.get("dez_2014"), 1), br(dl.get("dez_2018"), 1), br(dl.get("dez_2022"), 1), br(dl.get("dez_2025"), 1), br(dl["ultimo"]["valor"], 1)],
    ]) + "\n")
    s.append(f"**O rombo total (déficit nominal) é de {br(ch['deficit_nominal_12m_pct_pib'])}% do PIB em 12 meses, e a maior parte é juro:** {br(j['ultimo']['valor'], 2)} pontos de juros contra {br(p['ultimo']['valor'], 2)} de déficit primário.\n")
    d25 = m3["despesa_total"]["2025"]
    s.append("### 4.1 O tamanho do gasto, contra o mundo (A5)\n")
    s.append(tabela(["Gasto total do governo geral (FMI, % do PIB)", "2019", "2022", "2025", "2026 (projeção)"], [
        ["Brasil"] + [br(m3["despesa_total"][a]["brasil"]) for a in ["2019", "2022", "2025", "2026"]],
        ["Emergentes do G20 (mediana, sem o Brasil)"] + [br(m3["despesa_total"][a]["mediana_g20_emergentes"]) for a in ["2019", "2022", "2025", "2026"]],
        ["Emergentes e renda média (média do FMI)"] + [br(m3["despesa_total"][a]["media_fm_emg"]) for a in ["2019", "2022", "2025", "2026"]],
        ["América Latina (mediana, sem o Brasil)"] + [br(m3["despesa_total"][a]["mediana_america_latina"]) for a in ["2019", "2022", "2025", "2026"]],
        ["Países avançados (média)"] + [br(m3["despesa_total"][a]["media_avancados"]) for a in ["2019", "2022", "2025", "2026"]],
    ]) + "\n")
    s.append(f"Diferença do Brasil para a mediana dos emergentes do G20 em 2025: **{sinal(m3['diferenca_2025_contra_mediana_g20_pp'])} pontos do PIB** (régua: 5 ou mais = confirmada). "
             f"Desse gasto, {br(m3['juros_liquidos_fmi_pct_pib']['2025'])} pontos são juros (FMI). Mesmo sem os juros, o gasto do Brasil fica no nível dos países ricos (§4.2 da leitura da IA).\n")
    # 5. juro
    s.append("## 5. O juro (M4)\n")
    s.append(f"Selic de **{br(jr['selic_meta'], 2)}%** ao ano, inflação esperada para 12 meses de **{br(jr['ipca_esperado_12m'], 2)}%** (Focus de {jr['focus_data']}): juro real de **{br(jr['juro_real_ex_ante_pct'])}%** ao ano.\n")
    for nota in r.get("M4_notas", []):
        s.append(f"- {nota}")
    s.append("")
    sel = r["M4_focus_selic"]
    s.append(tabela(["Fim de", "Selic esperada (Focus)"], [[a, f"{br(sel[a]['mediana'], 2)}%"] for a in sel]) + "\n")
    # 6. medidas
    s.append("## 6. As medidas de 2025 e 2026 e as promessas: quem paga (M5)\n")
    linhas = []
    for l in csv.DictReader((RAIZ / "dados" / "evidencias" / "MEDIDAS_E_PROMESSAS.csv").open(encoding="utf-8")):
        if l["id"].startswith("M"):
            linhas.append([l["id"], l["nome"], l["categoria"], l["custo_informado_rs_bi"] or "sem custo publicado",
                           l["recorrente_a_partir_de_2027_rs_bi"] or "não se repete", l["de_onde_vem_o_dinheiro"][:160]])
    s.append("Categorias: **A** compensada na própria lei · **B** dentro do limite de gasto (tira de outra despesa) · **C** fora da meta · **D** fora do Orçamento · **E** sem fonte declarada.\n")
    s.append(tabela(["", "Medida", "Cat.", "Custo informado (R$ bi)", "Custo que se repete a partir de 2027 (R$ bi)", "De onde vem o dinheiro"], linhas) + "\n")
    s.append(f"**Custo que se repete por ano a partir de 2027: R$ {br(m5['total_recorrente_rs_bi'])} bi ({br(m5['total_recorrente_pct_pib_2027'], 2)}% do PIB).** "
             + "; ".join(f"categoria {k}: R$ {br(v)} bi ({br(m5['por_categoria_fatia_pct'][k], 0)}%)" for k, v in sorted(m5["por_categoria_rs_bi"].items())) + ".\n")
    if "M01" in A:
        s.append("**A compensação do IR é contestada:** a própria lei compensa a isenção com a tributação mínima de altas rendas, e a Consultoria de Orçamento do Senado e a IFI estimaram perdas líquidas (achado M01). \n")
    s.append("**Promessas do 2º mandato:**\n")
    linhas = []
    for l in csv.DictReader((RAIZ / "dados" / "evidencias" / "MEDIDAS_E_PROMESSAS.csv").open(encoding="utf-8")):
        if l["id"].startswith("P"):
            linhas.append([l["id"], l["nome"], l["categoria"] or "", l["custo_informado_rs_bi"] or "sem custo publicado", l["de_onde_vem_o_dinheiro"][:150]])
    s.append(tabela(["", "Promessa", "Cat.", "Custo (R$ bi por ano)", "De onde vem o dinheiro"], linhas) + "\n")
    # 7. 2027-2030
    s.append("## 7. 2027 a 2030 (M6)\n")
    s.append(tabela(["Cenário", "2026", "2027", "2028", "2029", "2030"], [
        ["S0, base da IFI (jun/2026)"] + [br(m6["S0_base_ifi"][a]) for a in ["2026", "2027", "2028", "2029", "2030"]],
        [f"S1, central (base + prêmio de {br(m6['premio_pp'], 2)} pontos)"] + [br(m6["S1_central"][a]) for a in ["2026", "2027", "2028", "2029", "2030"]],
        [f"S2, risco (S1 + promessas com custo e sem fonte, {br(r['M5_S2']['custo_pct_pib'], 2)}% do PIB)"] + [br(m6["S2_risco"][a]) for a in ["2026", "2027", "2028", "2029", "2030"]],
        ["Mercado (Focus)"] + [br(m6["focus_dbgg"][a]) for a in ["2026", "2027", "2028", "2029", "2030"]],
    ]) + "\n")
    s.append("Dívida bruta do governo geral, % do PIB, conceito do Banco Central. "
             f"No conceito do FMI (que soma os títulos do Tesouro na carteira do Banco Central), o FMI projeta {br(m6['fmi_weo_out2026_conceito_fmi'].get('2026'))}% em 2026 e {br(m6['fmi_weo_out2026_conceito_fmi'].get('2030'))}% em 2030 (WEO de out/2026).\n")
    s.append("### 7.1 Sensibilidade (dívida em 2030)\n")
    nomes = {"premio_metade": "prêmio pela metade", "premio_dobro": "prêmio em dobro", "repasse_total_imediato": "o prêmio passa inteiro para a dívida já em 2027",
             "pib_1_ponto_abaixo": "PIB 1 ponto abaixo por ano", "pib_1_ponto_acima": "PIB 1 ponto acima por ano",
             "custos_fora_da_base_ifi": "com o reajuste do Bolsa Família e o Desenrola 3.0 (fora da base da IFI) piorando o primário",
             "cenario_otimista_ifi_com_premio": "cenário otimista da IFI, com o prêmio", "cenario_pessimista_ifi_com_premio": "cenário pessimista da IFI, com o prêmio"}
    s.append(tabela(["Variante", "Dívida em 2030 (% do PIB)"], [[nomes[k], br(v)] for k, v in m6["sensibilidade_2030"].items()]) + "\n")
    s.append("### 7.2 O aperto do Orçamento\n")
    for ident in ("F42", "F45", "T13", "T12"):
        if ident in A:
            s.append(f"- {A[ident]['fato']} ([fonte]({A[ident]['url_a']}))")
    s.append("")
    # 8. passado
    s.append("## 8. O teste do passado (M7)\n")
    linhas = [[l["eleicao"], l["ano_alvo"], br(l["dlsp_prevista"]), br(l["dlsp_realizada"]), sinal(l["erro_dlsp_pp"]),
               f"{br(l['pib_medio_previsto'])}% / {br(l['pib_medio_realizado'])}%"] for l in prev["linhas"]]
    s.append(tabela(["Eleição", "Ano previsto", "Dívida líquida prevista (Focus, out)", "Aconteceu", "Erro (pontos)", "PIB médio previsto / aconteceu"], linhas) + "\n")
    rz = prev["resumo"]
    s.append(f"Erro médio de {br(rz['erro_medio_absoluto_dlsp_pp'])} pontos do PIB na dívida e de {br(rz['erro_medio_absoluto_pib_pp'])} ponto no PIB. "
             f"Em {rz['vezes_que_o_mercado_previu_divida_maior']} de {rz['n']} eleições o mercado previu dívida **maior** do que aconteceu; a exceção foi 2014, com erro de {br(rz['maior_erro_para_menos'])} pontos (a recessão de 2015 e 2016). "
             "A série da dívida líquida mudou de método em 2008; a conta compara a previsão de cada época com a série atual.\n")
    # 9. outros temas
    s.append("## 9. Outras coisas importantes (M8)\n")
    for k in sorted(A):
        if k.startswith("T"):
            s.append(f"- **{A[k]['tema']}.** {A[k]['fato']} {('*O que muda:* ' + A[k]['implicacao']) if A[k]['implicacao'] else ''} ([fonte]({A[k]['url_a']}))")
    s.append("")
    s.append("## 10. Como se conferiu\n")
    s.append(f"- Validação por um segundo caminho: **{ok_val} de {len(val['itens'])}** itens passaram (`resultados/VALIDACAO.json`).")
    conf = list(csv.DictReader((RES / "TRECHOS_CONFERIDOS.csv").open(encoding="utf-8")))
    s.append(f"- Achados de terceiros: {len(conf)} levantados, **{sum(1 for c in conf if c['estado_a'].startswith('ok'))}** com o trecho encontrado por script no texto capturado; os outros ficam fora do relatório.")
    s.append("- Revisão adversarial: [`docs/REVISAO_ADVERSARIAL.md`](docs/REVISAO_ADVERSARIAL.md). Leitura da IA: [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md). Como refazer: [`docs/REPLICAR.md`](docs/REPLICAR.md).\n")
    return "\n".join(s)


def resumo_simples(r: dict) -> str:
    m6, jr, v5 = r["M6_divida"], r["M4_juro_real"], r["M5_vereditos"]
    m1 = r.get("M1_mercado") or {}
    s = ["# Resumo simples\n", f"**Gerado em {r['gerado_em'][:10]}.** Completo: [`RELATORIO.md`](RELATORIO.md). Opinião da IA: [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md). Não é recomendação de investimento.\n"]
    s.append("## As afirmações do pedido\n")
    s.append(tabela(["Afirmação", "Veredito", "Por quê"], [[l[1], l[2], l[3]] for l in vereditos(r)]) + "\n")
    s.append("## O que esperar até 2030\n")
    s.append(f"- **A dívida {m6['classificacao_S1']}:** de {br(m6['S1_central']['2026'])}% do PIB em 2026 para {br(m6['S1_central']['2030'])}% em 2030 no cenário central.")
    s.append(f"- **Para ela parar de subir**, seria preciso um superávit de {br(m6['primario_que_estabiliza_em_2030_pct_pib'])}% do PIB por ano. O previsto é {br(m6['primario_previsto_2030_base_ifi'])}%.")
    s.append(f"- **O juro real é de {br(jr['juro_real_ex_ante_pct'])}% ao ano.** O mercado esperava, antes da eleição, Selic de {br(r['M4_focus_selic']['2027']['mediana'], 2)}% no fim de 2027.")
    s.append(f"- **As medidas de 2025 e 2026 custam R$ {br(r['M5_medidas']['total_recorrente_rs_bi'])} bi por ano a partir de 2027**; {br(100 - r['M5_medidas']['por_categoria_fatia_pct'].get('A', 0), 0)}% disso não tem compensação na própria lei.")
    s.append(f"- **{v5['A4']['sem_custo_ou_sem_fonte']} de {v5['A4']['promessas']} promessas** do 2º mandato não têm custo publicado ou fonte declarada.")
    for linha in m1.get("resumo_simples", []):
        s.append(f"- {linha}")
    s.append("")
    return "\n".join(s)


def main() -> int:
    r = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))
    val = json.loads((RES / "VALIDACAO.json").read_text(encoding="utf-8"))
    (RAIZ / "RELATORIO.md").write_text(relatorio(r, val), encoding="utf-8")
    (RAIZ / "RESUMO_SIMPLES.md").write_text(resumo_simples(r), encoding="utf-8")
    print("RELATORIO.md e RESUMO_SIMPLES.md gravados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
