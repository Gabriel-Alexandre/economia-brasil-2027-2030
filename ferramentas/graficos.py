"""Gráficos 1920x1080 para o vídeo, todos lidos de resultados/RESUMO.json e de dados/ (nenhum número à mão).

Paleta categórica validada (ordem fixa): azul #2a78d6 (Brasil, cenário central), laranja #eb6834,
verde-água #1baf7a, amarelo #eda100; cinza #6B6B6B para base e comparação. Todo valor tem rótulo direto.
Uso: python ferramentas/graficos.py
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from economia import series as S  # noqa: E402

RES = RAIZ / "resultados"
FIG = RES / "figuras"
AZUL, LARANJA, VERDE, AMARELO, CINZA, CLARO = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#6B6B6B", "#BDBDBD"
TINTA, TINTA2 = "#0b0b0b", "#52514e"
RODAPE = "Projeto aberto: github.com/Gabriel-Alexandre/economia-brasil-2027-2030. Análise feita pelo Claude (IA da Anthropic). Não é recomendação de investimento"
plt.rcParams.update({"font.size": 18, "axes.titlesize": 28, "axes.titleweight": "bold", "axes.spines.top": False,
                     "axes.spines.right": False, "figure.facecolor": "white", "axes.facecolor": "white",
                     "axes.titlepad": 22, "axes.edgecolor": CLARO, "xtick.color": TINTA2, "ytick.color": TINTA2,
                     "axes.labelcolor": TINTA2, "axes.grid": False})


def br(x: float, casas: int = 1) -> str:
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def nova(titulo: str, fonte: str, subtitulo: str = ""):
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    fig.subplots_adjust(left=0.07, right=0.88, top=0.82, bottom=0.14)
    fig.text(0.07, 0.925, titulo, fontsize=30, fontweight="bold", color=TINTA)
    if subtitulo:
        fig.text(0.07, 0.875, subtitulo, fontsize=18, color=TINTA2)
    fig.text(0.01, 0.035, f"Fonte: {fonte}.", fontsize=12, color="#555555")
    fig.text(0.01, 0.012, f"{RODAPE}.", fontsize=12, color="#555555")
    return fig, ax


def salvar(fig, nome: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / nome)
    plt.close(fig)


def grade_y(ax):
    ax.yaxis.grid(True, color="#EEEEEE", lw=1)
    ax.set_axisbelow(True)


def g02_divida(r: dict) -> None:
    m = r["M6_divida"]
    db = S.sgs("bcb-divida-bruta-gg")
    hist = {d.year: v for d, v in db.items() if d.month == 12}
    fig, ax = nova("Dívida bruta do governo: o caminho até 2030", "Banco Central (histórico, dezembro), IFI RAF 113 (jun/2026), Boletim Focus, cálculo do projeto",
                   "% do PIB, conceito do Banco Central. Central = base da IFI mais o prêmio de juros cobrado pelo mercado")
    anos_h = sorted(a for a in hist if a >= 2010)
    ax.plot(anos_h, [hist[a] for a in anos_h], color=TINTA, lw=3)
    ax.text(anos_h[0], hist[anos_h[0]] + 2, "o que aconteceu", fontsize=16, color=TINTA)
    s0 = {int(a): v for a, v in m["S0_base_ifi"].items()}
    s1 = {int(a): v for a, v in m["S1_central"].items()}
    foc = {int(a): v for a, v in m["focus_dbgg"].items()}
    for serie, cor, nome, dy in ((s0, CINZA, "base da IFI", 4.0), (foc, VERDE, "mercado (Focus)", -6.0), (s1, AZUL, "cenário central", 2.0)):
        anos = sorted(a for a in serie if a >= 2025)
        ax.plot(anos, [serie[a] for a in anos], color=cor, lw=3.5 if cor == AZUL else 2.5, ls="-" if cor == AZUL else "--")
        ax.text(2030.15, serie[2030] + dy * 0.3, f"{nome}: {br(serie[2030])}%", fontsize=18, color=cor if cor != VERDE else "#0e7a54",
                fontweight="bold" if cor == AZUL else "normal", va="center")
    ax.set_xlim(2010, 2030.4)
    fig.subplots_adjust(right=0.79)
    ax.set_xticks(list(range(2010, 2031, 2)))
    ax.set_ylim(45, 110)
    ax.set_ylabel("% do PIB")
    grade_y(ax)
    salvar(fig, "g02_divida_ate_2030.png")


def g03_gasto(r: dict) -> None:
    g = r["M3_gasto"]
    d25 = g["despesa_total"]["2025"]
    juros = g["juros_liquidos_fmi_pct_pib"]["2025"]
    linhas = [("Brasil", d25["brasil"], AZUL), ("Países avançados (média)", d25["media_avancados"], CINZA),
              ("Emergentes do G20 (mediana)", d25["mediana_g20_emergentes"], CINZA),
              ("Emergentes e renda média (média FMI)", d25["media_fm_emg"], CINZA),
              ("América Latina (mediana)", d25["mediana_america_latina"], CINZA)]
    fig, ax = nova("Quanto o governo gasta, em % do PIB (2025)", "FMI, Fiscal Monitor de out/2026 (despesa total do governo geral, inclui juros)",
                   f"Governo geral: União, estados e municípios, com os juros da dívida (o FMI estima os juros líquidos do Brasil em {br(juros)}% do PIB)")
    for i, (nome, v, cor) in enumerate(linhas[::-1]):
        ax.barh(i, v, height=0.6, color=cor)
        ax.text(v + 0.6, i, f"{br(v)}%", va="center", fontsize=24, fontweight="bold", color=TINTA)
    ax.set_yticks(range(len(linhas)))
    ax.set_yticklabels([n for n, _, _ in linhas[::-1]], fontsize=20)
    ax.set_xlim(0, 58)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    fig.subplots_adjust(left=0.30)
    salvar(fig, "g03_gasto_do_governo.png")


def g04_juros_e_primario(r: dict) -> None:
    p = S.sgs("bcb-primario-12m")
    j = S.sgs("bcb-juros-nominais-12m")
    fig, ax = nova("O déficit das contas: a maior parte é juro", "Banco Central, necessidades de financiamento do setor público, acumulado em 12 meses",
                   "% do PIB. Acima de zero é déficit. Juros = o que a dívida custa; primário = o resto das contas")
    pd_ = [d for d in p.index if d >= dt.date(2010, 1, 1)]
    ax.plot(pd_, [j[d] for d in pd_], color=LARANJA, lw=3)
    ax.plot(pd_, [p[d] for d in pd_], color=AZUL, lw=3)
    ax.axhline(0, color=CINZA, lw=1)
    u = pd_[-1]
    ax.text(u, j[u] + 0.5, f"juros: {br(j[u], 2)}%", color="#b4451a", fontsize=20, fontweight="bold", ha="right")
    ax.text(u, p[u] + 0.7, f"primário: {br(p[u], 2)}%", color=AZUL, fontsize=20, fontweight="bold", ha="right")
    ax.set_ylabel("% do PIB")
    grade_y(ax)
    salvar(fig, "g04_juros_e_primario.png")


def g05_selic(r: dict) -> None:
    s = S.sgs("bcb-selic-meta")
    sub = s[s.index >= dt.date(2019, 1, 1)]
    foc = r["M4_focus_selic"]
    fig, ax = nova("Selic: onde está e para onde o mercado acha que vai", "Banco Central (meta da Selic) e Boletim Focus (mediana)",
                   "% ao ano. Linha tracejada: o que o mercado esperava antes da eleição para o fim de cada ano")
    ax.plot(list(sub.index), list(sub.values), color=TINTA, lw=3)
    xs = [dt.date(int(a), 12, 31) for a in foc]
    ys = [foc[a]["mediana"] for a in foc]
    ax.plot([sub.index[-1]] + xs, [float(sub.iloc[-1])] + ys, color=AZUL, lw=3, ls="--", marker="o", ms=10)
    for x, y in zip(xs, ys):
        ax.text(x, y + 0.6, f"{br(y, 2)}%", ha="center", color=AZUL, fontsize=18, fontweight="bold")
    ax.text(sub.index[-1], float(sub.iloc[-1]) + 0.8, f"hoje: {br(float(sub.iloc[-1]), 2)}%", ha="right", fontsize=20, fontweight="bold")
    ax.set_ylabel("% ao ano")
    ax.set_ylim(0, 17)
    grade_y(ax)
    salvar(fig, "g05_selic.png")


def g06_eleicoes_passadas(r: dict) -> None:
    h = [l for l in r["M1_historico_eleicoes"] if l["ano"] < 2026]
    fig, ax = nova("O dia seguinte não diz como vai ser o mandato", "Yahoo Finance (Ibovespa), Banco Central (IPCA), cálculo do projeto",
                   "Variação do Ibovespa no 1º pregão depois da eleição contra o ganho real da bolsa até o fim do mandato seguinte")
    x = range(len(h))
    w = 0.38
    dia = [l["ibovespa_dia_pct"] for l in h]
    man = [l["ibovespa_real_pct"] for l in h]
    ax.bar([i - w / 2 for i in x], dia, width=w, color=LARANJA, label="no dia seguinte")
    ax.bar([i + w / 2 for i in x], man, width=w, color=AZUL, label="real, no mandato seguinte")
    for i, (a, b) in enumerate(zip(dia, man)):
        ax.text(i - w / 2, a + (3 if a >= 0 else -9), f"{br(a)}%", ha="center", fontsize=17, color=TINTA)
        ax.text(i + w / 2, b + (3 if b >= 0 else -9), f"{br(b, 0)}%", ha="center", fontsize=17, color=TINTA, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{l['ano']}\n{l['vencedor']}" + ("\n(até hoje)" if not l["mandato_completo"] else "") for l in h], fontsize=18)
    ax.axhline(0, color=CINZA, lw=1)
    ax.set_ylabel("%")
    ax.legend(frameon=False, loc="upper right", fontsize=18)
    grade_y(ax)
    salvar(fig, "g06_dia_seguinte_e_mandato.png")


def g07_previsao_divida(r: dict) -> None:
    L = r["M7_previsao_do_mercado_contra_o_realizado"]["linhas"]
    fig, ax = nova("O mercado costuma errar a dívida, e quase sempre para pior", "Boletim Focus (mediana de outubro do ano da eleição) e Banco Central (dívida líquida, dezembro)",
                   "Dívida líquida 3 anos depois da eleição: o que o mercado previa contra o que aconteceu (% do PIB)")
    x = range(len(L))
    w = 0.38
    ax.bar([i - w / 2 for i in x], [l["dlsp_prevista"] for l in L], width=w, color=CINZA, label="previsto")
    ax.bar([i + w / 2 for i in x], [l["dlsp_realizada"] for l in L], width=w, color=AZUL, label="aconteceu")
    for i, l in enumerate(L):
        ax.text(i - w / 2, l["dlsp_prevista"] + 1, br(l["dlsp_prevista"]), ha="center", fontsize=16, color=TINTA2)
        ax.text(i + w / 2, l["dlsp_realizada"] + 1, br(l["dlsp_realizada"]), ha="center", fontsize=16, color=TINTA, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"eleição de {l['eleicao']}\n(para {l['ano_alvo']})" for l in L], fontsize=16)
    ax.legend(frameon=False, fontsize=18, loc="upper left")
    ax.set_ylim(0, 80)
    grade_y(ax)
    salvar(fig, "g07_previsao_da_divida.png")


def g08_medidas(r: dict) -> None:
    m = r["M5_medidas"]
    nomes = {"A": "compensada na própria lei\n(imposto maior para outro grupo)", "B": "dentro do limite de gasto\n(tira de outra despesa)",
             "C": "fora da meta", "D": "fora do Orçamento\n(tarifa de luz, renúncia)", "E": "sem fonte declarada"}
    cats = [c for c in "ABCDE" if c in m["por_categoria_rs_bi"]]
    vals = [m["por_categoria_rs_bi"][c] for c in cats]
    cores = {"A": VERDE, "B": AZUL, "C": LARANJA, "D": AMARELO, "E": CINZA}
    fig, ax = nova("As medidas de 2025 e 2026: quem paga, por ano", "Leis, MPs, LOA e PLOA 2027, Consultoria do Senado, IFI e imprensa (dados/evidencias/MEDIDAS_E_PROMESSAS.csv)",
                   f"Custo que se repete a partir de 2027: R$ {br(m['total_recorrente_rs_bi'], 1)} bi por ano ({br(m['total_recorrente_pct_pib_2027'], 2)}% do PIB)")
    for i, (c, v) in enumerate(zip(cats[::-1], vals[::-1])):
        ax.barh(i, v, height=0.6, color=cores[c])
        ax.text(v + 1, i, f"R$ {br(v)} bi ({br(m['por_categoria_fatia_pct'][c], 0)}%)", va="center", fontsize=22, fontweight="bold", color=TINTA)
    ax.set_yticks(range(len(cats)))
    ax.set_yticklabels([nomes[c] for c in cats[::-1]], fontsize=19)
    ax.set_xlim(0, max(vals) * 1.45)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    fig.subplots_adjust(left=0.27)
    salvar(fig, "g08_medidas_quem_paga.png")


def g09_discricionarias(r: dict) -> None:
    linhas = {l["id"]: l for l in csv.DictReader((RAIZ / "dados" / "evidencias" / "ACHADOS.csv").open(encoding="utf-8"))}
    t = linhas.get("F42", {}).get("trecho_a", "")
    nums = [float(x.replace(".", "").replace(",", ".")) for x in re.findall(r"R\$ (\d+,\d) bilh", t)]
    if len(nums) < 7:
        return
    espaco, base = nums[:4], [None] + nums[4:7]
    anos = [2027, 2028, 2029, 2030]
    fig, ax = nova("O aperto: o dinheiro livre do governo encolhe", "Ministério do Planejamento, Mensagem Presidencial do PLOA 2027 (cap. 2)",
                   "Despesas discricionárias do Executivo (custeio e investimento), R$ bilhões: o espaço do limite contra o que seria preciso")
    w = 0.38
    ax.bar([a - w / 2 for a in anos], espaco, width=w, color=AZUL, label="espaço no limite")
    ax.bar([a + w / 2 for a in anos[1:]], base[1:], width=w, color=CINZA, label="o que mantém a máquina como está")
    for a, v in zip(anos, espaco):
        ax.text(a - w / 2, v + 2, br(v), ha="center", fontsize=19, fontweight="bold")
    for a, v, e in zip(anos[1:], base[1:], espaco[1:]):
        ax.text(a + w / 2, v + 2, br(v), ha="center", fontsize=19, color=TINTA2)
        ax.text(a, max(v, e) + 12, f"faltam R$ {br(v - e)} bi", ha="center", fontsize=19, color="#b4451a", fontweight="bold")
    ax.set_xticks(anos)
    ax.set_ylim(150, 260)
    ax.legend(frameon=False, fontsize=18, loc="upper left")
    grade_y(ax)
    salvar(fig, "g09_discricionarias.png")


def g10_estabilizar(r: dict) -> None:
    m = r["M6_divida"]
    fig, ax = nova("Quanto falta para a dívida parar de subir", "IFI RAF 113 (primário previsto), cálculo do projeto (primário que estabiliza)",
                   "Resultado primário do setor público em 2030, % do PIB")
    v = [("previsto (base da IFI)", m["primario_previsto_2030_base_ifi"], CINZA),
         ("necessário para estabilizar", m["primario_que_estabiliza_em_2030_pct_pib"], AZUL)]
    for i, (n, x, c) in enumerate(v):
        ax.bar(i, x, width=0.55, color=c)
        ax.text(i, x + (0.2 if x >= 0 else -0.45), f"{br(x)}%", ha="center", fontsize=34, fontweight="bold")
    ax.axhline(0, color=CINZA, lw=1)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([n for n, _, _ in v], fontsize=22)
    ax.set_ylim(-2.5, 5)
    ax.text(0.5, 4.4, f"distância: {br(m['distancia_ate_estabilizar_pp'])} pontos do PIB", ha="center", fontsize=24, color="#b4451a", fontweight="bold")
    grade_y(ax)
    salvar(fig, "g10_quanto_falta.png")


def g01_mercado(r: dict) -> None:
    m = r.get("M1_mercado", {})
    e = m.get("dia")
    if not e or not e.get("ibovespa"):
        return
    itens = [("Ibovespa", e["ibovespa"]["variacao_pct"], AZUL), ("EWZ (Brasil em Nova York, em US$)", e["ewz"]["variacao_pct"], AZUL),
             ("Emergentes (EEM)", e["eem"]["variacao_pct"], CINZA), ("Dólar contra o real (PTAX)", e["usdbrl_ptax"]["variacao_pct"] if e.get("usdbrl_ptax") else e["usdbrl_yahoo"]["variacao_pct"], LARANJA),
             ("Dólar contra outros emergentes (média)", e["controle_moeda_pct"], CINZA)]
    fig, ax = nova(f"O mercado no dia seguinte: {dt.date.fromisoformat(e['janela'][1]).strftime('%d/%m')} contra {dt.date.fromisoformat(e['janela'][0]).strftime('%d/%m')}",
                   "Yahoo Finance e Banco Central (PTAX), fechamento", "Variação em %. Cinza = o que os outros emergentes fizeram no mesmo dia")
    for i, (n, v, c) in enumerate(itens[::-1]):
        ax.barh(i, v, height=0.6, color=c)
        ax.text(v + (0.4 if v >= 0 else -0.4), i, f"{'+' if v > 0 else ''}{br(v)}%", va="center", ha="left" if v >= 0 else "right", fontsize=24, fontweight="bold")
    ax.axvline(0, color=TINTA, lw=1)
    ax.set_yticks(range(len(itens)))
    ax.set_yticklabels([n for n, _, _ in itens[::-1]], fontsize=18)
    lim = max(abs(v) for _, v, _ in itens) * 1.6
    ax.set_xlim(-lim, lim)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    fig.subplots_adjust(left=0.30)
    fig.text(0.07, 0.07, "Outros emergentes: peso mexicano, chileno e colombiano e rand sul-africano. EWZ e EEM são fundos negociados em Nova York.", fontsize=14, color=TINTA2)
    salvar(fig, "g01_mercado_no_dia.png")


def main() -> int:
    r = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))
    for g in (g01_mercado, g02_divida, g03_gasto, g04_juros_e_primario, g05_selic, g06_eleicoes_passadas,
              g07_previsao_divida, g08_medidas, g09_discricionarias, g10_estabilizar):
        g(r)
    print("gráficos:", sorted(p.name for p in FIG.glob("*.png")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
