"""Escreve docs/LEITURA_DA_IA.md e docs/REVISAO_ADVERSARIAL.md: a opinião do Claude, separada dos números.

Todo número sai de resultados/RESUMO.json, resultados/M1_MERCADO.json ou resultados/REVISAO.json.
O texto é a leitura da IA, com o raciocínio econômico por trás; não muda nenhuma régua.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RES = RAIZ / "resultados"


def br(x, casas: int = 1) -> str:
    if x is None:
        return "sem dado"
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def dados_extra() -> dict:
    import csv
    import re
    conf = {l["id"] for l in csv.DictReader((RES / "TRECHOS_CONFERIDOS.csv").open(encoding="utf-8")) if l["estado_a"].startswith("ok")}
    ach = {l["id"]: l for l in csv.DictReader((RAIZ / "dados" / "evidencias" / "ACHADOS.csv").open(encoding="utf-8")) if l["id"] in conf}
    med = {l["id"]: l for l in csv.DictReader((RAIZ / "dados" / "evidencias" / "MEDIDAS_E_PROMESSAS.csv").open(encoding="utf-8"))}
    ifi = json.loads((RAIZ / "dados" / "derivados" / "ifi_raf113.json").read_text(encoding="utf-8"))["base"]
    f42 = [float(x.replace(",", ".")) for x in re.findall(r"R\$ (\d+,\d) bilh", ach.get("F42", {}).get("trecho_a", ""))]
    return {"bf": float(med["M13"]["recorrente_a_partir_de_2027_rs_bi"]), "tarifa": float(med["P01"]["custo_informado_rs_bi"]),
            "pdm_univ": float(med["P02"]["custo_informado_rs_bi"]), "pib30": ifi["pib_nominal"]["2030"],
            "falta28": f42[4] - f42[1] if len(f42) >= 7 else None, "falta30": f42[6] - f42[3] if len(f42) >= 7 else None,
            "meta27": float(ach["F18"]["numero"]) if "F18" in ach else None}


def leitura(r: dict, rev: dict) -> str:
    x = dados_extra()
    m6, ch, jr, m5, v5 = r["M6_divida"], r["M3_contas_hoje"], r["M4_juro_real"], r["M5_medidas"], r["M5_vereditos"]
    m1 = r.get("M1_mercado") or {}
    g = r["M3_gasto"]
    sel = r["M4_focus_selic"]
    f = r["M4_focus_macro"]
    rz = r["M7_previsao_do_mercado_contra_o_realizado"]["resumo"]
    hist = {l["ano"]: l for l in r["M1_historico_eleicoes"]}
    selic = r.get("M4_custo_de_um_ponto_de_selic", {})
    pm = m1.get("polymarket") or {}
    dia = m1.get("dia") or {}
    s = ["# Leitura da IA\n",
         "Este arquivo é a opinião do Claude (IA da Anthropic) sobre os números do projeto. Os números estão em [`RELATORIO.md`](../RELATORIO.md); aqui está o que eles querem dizer, com o raciocínio da economia por trás. Não é recomendação de investimento.\n"]
    s.append("## 1. O que aconteceu no dia 26/out\n")
    if pm:
        s.append(f"Na véspera, o mercado de previsão dava {br(100 * pm['p'], 1)}% de chance para Lula (Polymarket, {pm['hora_brt'][11:16]} de 25/out, último registro antes do fim da votação). "
                 "A bolsa tinha subido no ano apostando no outro resultado e o dinheiro estrangeiro tinha entrado. A queda do dia, portanto, mede sobretudo a surpresa: "
                 f"como a vitória de Lula era vista como a menos provável, o preço tinha de andar {br(1 / (1 - pm['p']), 2)} vezes o que andaria se as chances fossem as mesmas de agora em diante.")
    if dia.get("ibovespa"):
        s.append(f" O Ibovespa variou {br(dia['ibovespa']['variacao_pct'], 2)}% e o dólar {br(dia['usdbrl_yahoo']['variacao_pct'], 2)}%.")
    s.append("\n")
    s.append(f"Na história, o dia seguinte não ensina muito sobre o mandato. Em 2002 a bolsa caiu {br(-hist[2002]['ibovespa_dia_pct'])}% e depois teve um dos melhores mandatos da série; em 2010 subiu e depois caiu quase pela metade. "
             "A queda de hoje é uma informação sobre o que o mercado teme, e o que ele teme é o fiscal. É esse o ponto que decide 2027 a 2030.\n")
    s.append("## 2. O problema principal é a conta de juros, e ela se alimenta sozinha\n")
    s.append(f"O déficit total do setor público é de {br(ch['deficit_nominal_12m_pct_pib'])}% do PIB em 12 meses, e {br(ch['bcb-juros-nominais-12m']['ultimo']['valor'], 2)} pontos disso são juros. "
             f"O juro real de {br(jr['juro_real_ex_ante_pct'])}% ao ano está entre os maiores do mundo. A conta que a economia usa para isso é simples: a dívida em relação ao PIB sobe quando o juro que se paga sobre ela é maior que o crescimento da economia e o governo não faz superávit para cobrir a diferença. "
             f"Com a dívida perto de {br(m6['S1_central']['2029'])}% do PIB em 2029 no cenário central, só para ela parar seria preciso um superávit de {br(m6['primario_que_estabiliza_em_2030_pct_pib'])}% do PIB por ano. "
             f"O previsto é {br(m6['primario_previsto_2030_base_ifi'])}%. A diferença, {br(m6['distancia_ate_estabilizar_pp'])} pontos do PIB, é do tamanho de R$ {br(m6['distancia_ate_estabilizar_pp'] / 100 * x['pib30'], 0)} bi por ano em valores de 2030.\n")
    if selic:
        s.append(f"Mais da metade da dívida federal acompanha a Selic ({br(selic['fatia_selic_pct'], 2)}%). Cada ponto de Selic a mais custa cerca de R$ {br(selic['rs_bi_por_ano'], 0)} bi por ano. "
                 "Por isso o fiscal e o juro andam juntos: se o mercado desconfia das contas, ele cobra mais nos títulos longos, o dólar sobe, a inflação vem atrás, o Banco Central segura a Selic, e a dívida cresce mais. "
                 "A economia chama o caso extremo disso de dominância fiscal (Blanchard, 2004, com o Brasil de 2002 como exemplo). O Brasil não está nesse caso extremo, mas a direção do risco é essa.\n")
    s.append("## 3. Como as medidas de 2025 e 2026 estão sendo pagas\n")
    cat = m5["por_categoria_fatia_pct"]
    s.append(f"O custo que se repete por ano, a partir de 2027, é de R$ {br(m5['total_recorrente_rs_bi'])} bi ({br(m5['total_recorrente_pct_pib_2027'], 2)}% do PIB). "
             f"Cerca de {br(cat.get('A', 0), 0)}% tem compensação escrita na própria lei (a isenção do IR, paga com o imposto mínimo de quem ganha mais, compensação que a Consultoria do Senado e a IFI acham que não fecha inteira). "
             f"Cerca de {br(cat.get('B', 0), 0)}% fica dentro do limite de gasto do arcabouço. Isso quer dizer que o dinheiro sai de outro lugar do Orçamento: as despesas livres do governo (custeio e investimento), que já estão no mínimo. "
             f"E cerca de {br(cat.get('D', 0), 0)}% sai fora do Orçamento, sobretudo pela conta de luz dos outros consumidores (a tarifa social) e por renúncia de imposto. "
             "Resposta direta à pergunta: as medidas não estão sendo pagas com dinheiro novo. Estão sendo pagas apertando o resto do Orçamento, com imposto de um grupo menor de pessoas e com a tarifa de energia de todo mundo. "
             f"O reajuste do Bolsa Família de setembro (R$ {br(x['bf'])} bi por ano a partir de 2027) ainda não está no Orçamento de 2027 enviado em agosto.\n")
    s.append("## 4. E as promessas\n")
    s.append(f"Das {v5['A4']['promessas']} promessas econômicas levantadas, {v5['A4']['sem_custo_ou_sem_fonte']} não têm custo publicado ou não dizem de onde vem o dinheiro. "
             f"As que têm custo são pequenas perto do Orçamento (a tarifa zero de fim de semana, cerca de R$ {br(x['tarifa'], 0)} bi, que o governo quer pagar com uma parte das emendas parlamentares; o Pé-de-Meia universitário, R$ {br(x['pdm_univ'])} bi pelo Fundo Social). "
             "O risco não está nelas, está nas que não têm número (escola integral, energia mais barata, ampliar a proteção social) e num Congresso de maioria de direita a partir de 2027 que precisa aprovar qualquer imposto novo.\n")
    s.append("## 5. O que esperar, ano a ano\n")
    s.append(f"- **2027: o ano do aperto.** O mercado esperava, antes da eleição, PIB de {br(f['PIB Total']['2027'])}%, inflação de {br(f['IPCA']['2027'], 2)}% e Selic terminando o ano em {br(sel['2027']['mediana'], 2)}%. "
             f"A meta fiscal do ano (superávit de R$ {br(x['meta27'])} bi) só fecha, pela IFI, com bloqueio de dezenas de bilhões. É o ano em que o governo terá de mostrar se ajusta, e os primeiros testes são a próxima reunião do Copom e o Orçamento de 2027 revisto.")
    s.append(f"- **2028: o limite do arcabouço deixa de caber.** Pelo próprio governo, faltam R$ {br(x['falta28'])} bi de despesa livre em 2028 e R$ {br(x['falta30'])} bi em 2030 para manter a máquina como está; a IFI fala em risco de paralisação. Ao mesmo tempo, os precatórios voltam aos poucos para dentro da meta. É aí que a regra fiscal provavelmente terá de ser mudada (mexendo nos pisos de saúde e educação, na regra do salário mínimo ou no próprio limite), e o tipo de mudança vai decidir o juro do resto do mandato.")
    s.append(f"- **2029 e 2030: a dívida perto de {br(m6['S1_central']['2030'], 0)}% do PIB** no cenário central, contra {br(m6['S0_base_ifi']['2030'])}% na base da IFI e {br(m6['focus_dbgg']['2030'])}% no Focus. Com o PIB um ponto abaixo, {br(m6['sensibilidade_2030']['pib_1_ponto_abaixo'])}%; um ponto acima, {br(m6['sensibilidade_2030']['pib_1_ponto_acima'])}%.\n")
    s.append("## 6. A minha conclusão\n")
    db_ifi = json.loads((RAIZ / "dados" / "derivados" / "ifi_raf113.json").read_text(encoding="utf-8"))["base"]["divida_bruta"]
    ano_ult = max(db_ifi, key=int)
    ifi36 = db_ifi[ano_ult]
    v = r["M6_variantes_revisao"]
    metas = v.get("p2_metas_do_pldo_cumpridas", {})
    s.append(f"**A dívida {m6['classificacao_S1']} até 2030, e o juro alto é a causa principal e a consequência ao mesmo tempo.** Isso já era verdade antes da eleição: a base da IFI de junho já tinha a dívida subindo todo ano, até {br(ifi36)}% do PIB em {ano_ult}. "
             "O que o resultado mudou foi o preço do risco: o mercado passou a cobrar mais para financiar o mesmo governo, e isso, se ficar, encarece a dívida por anos. "
             f"Ao mesmo tempo, o mercado costuma errar a dívida para pior ({rz['vezes_que_o_mercado_previu_divida_maior']} das {rz['n']} eleições desde 2002), e a economia real está melhor que a conta pública. "
             "O que separa os caminhos é uma decisão que ainda não foi tomada: "
             + (f"se o 2º mandato cumprir as metas que ele mesmo mandou ao Congresso, a dívida termina 2030 perto de {br(metas['divida_2030_com_premio'], 0)}% do PIB mesmo com o prêmio; " if metas else "")
             + f"se empurrar o problema para 2028, quando o limite de gasto deixa de caber, o prêmio fica e a dívida chega a {br(m6['S1_central']['2030'], 0)}% ou mais.\n")
    s.append("## 7. As duas premissas\n")
    s.append("A seção 11 do relatório toma como verdadeira, uma de cada vez, a premissa de que o mercado tem razão e a de que ele exagerou, com a conta de cada uma. "
             "A minha leitura: a P1 ganha no que importa para 2027 a 2030, porque a dívida sobe em todas as contas, inclusive nas mais favoráveis ao governo; "
             "a P2 ganha no tamanho do susto do dia, porque parte da queda é aposta desfeita e o mercado costuma errar a dívida para pior. "
             "As duas cabem juntas: o problema é real e vem de antes da eleição, e o preço do dia pode ter exagerado o tamanho dele.\n")
    return "\n".join(s)


def revisao(rev: dict) -> str:
    s = ["# Revisão adversarial\n", "Três leitores independentes (agentes de IA separados, sem acesso à conversa do autor) leram o repositório e procuraram o que estava errado, cada um de um lado. As objeções e o que o projeto fez com cada uma:\n"]
    for leitor in rev.get("leitores", []):
        s.append(f"## {leitor['nome']}\n")
        for o in leitor["objecoes"]:
            s.append(f"- **({o['gravidade']})** {o['texto']} **O que foi feito:** {o['feito']}")
        s.append("")
    return "\n".join(s)


def main() -> int:
    r = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))
    p = RES / "REVISAO.json"
    rev = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    (RAIZ / "docs" / "LEITURA_DA_IA.md").write_text(leitura(r, rev), encoding="utf-8")
    if rev:
        (RAIZ / "docs" / "REVISAO_ADVERSARIAL.md").write_text(revisao(rev), encoding="utf-8")
    print("leitura gravada")
    return 0


if __name__ == "__main__":
    sys.exit(main())
