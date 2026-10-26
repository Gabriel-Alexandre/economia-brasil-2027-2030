# Estado do projeto

**26/out/2026, manhã.** Pré-registro publicado antes de qualquer conta (07h16, commit `0e7620d`) e seis emendas, cada uma com o que já tinha sido visto (`docs/PRE_REGISTRO.md` §12). Coleta, análise, validação (10 de 10), revisão adversarial por três leitores e relatório por script feitos. O que falta é o dado do próprio dia:

| O que falta | Quando sai | O que fazer |
|---|---|---|
| Fechamento de 26/out (Ibovespa, EWZ, dólar, emergentes) | depois das 18h | `python ferramentas/mercado-do-dia.py`, depois `analise.py`, `validacao-independente.py`, `gerar-relatorio.py`, `gerar-leitura.py`, `graficos.py` |
| Curva DI x pré da B3 de 26/out (A7 e o prêmio de juros) | o arquivo de taxas referenciais sai por volta das 20h | o mesmo comando; `mercado-do-dia.py` baixa sozinho |
| Fluxo estrangeiro da B3 de 26/out | dois dias depois (28/out) | atualizar o achado K04/K09 e rodar de novo |
| Focus de 23/out e o primeiro depois da eleição (30/out) | segundas, de manhã | `python ferramentas/coletar.py focus-recente focus-ipca-12m` |
| A semana (23/out a 30/out) | sexta, 30/out, depois das 18h | trocar `D1` em `mercado-do-dia.py` por uma segunda janela (pré-registro M1) |

**Não entregue nesta rodada (emenda 6):** a régua 2 do M3 (crescimento real da despesa do governo central de 2023 a 2026 contra 2015 a 2022).

**Para continuar:** comece pelo `RESUMO_SIMPLES.md`, depois `RELATORIO.md`, `docs/LEITURA_DA_IA.md` e `docs/REVISAO_ADVERSARIAL.md`.
