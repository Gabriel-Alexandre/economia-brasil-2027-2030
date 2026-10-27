# Estado do projeto

**26/out/2026, noite. Primeira rodada fechada.** O pré-registro foi publicado antes de qualquer conta (07h16, commit `0e7620d`) e recebeu nove emendas, cada uma com o que já tinha sido visto (`docs/PRE_REGISTRO.md` §12). Já estão feitos: a coleta; o fechamento de 26/out (cotações da coleta das 18h16); os juros de 26/out pela imprensa (emenda 9); a análise; a validação independente (12 de 12); a revisão adversarial por três leitores; o relatório e a leitura por script; os 10 gráficos; e a conferência de linguagem (0 ocorrência). A cadeia inteira foi rodada de novo às 21h14 (`python ferramentas/rodar-tudo.py --sem-coleta`) e deu os mesmos números.

**O resultado em uma linha por afirmação:** bolsa caiu forte (A1 confirmada) · o dinheiro de fora fugiu (A2 não confirmada até 22/out) · muitas medidas sem dinheiro novo (A3 confirmada, 15 medidas e 75% sem compensação) · promessas sem fonte (A4 confirmada, 10 de 14) · gasto alto (A5 confirmada, 46,9% do PIB contra 31,1%) · juro alto (A6 confirmada, 1º de 40) · juro tende a subir (A7 em parte) · dívida de 82,5% a 105,4% do PIB em 2030 no cenário central, subindo nos 17 cenários.

## O que ainda vai mudar a conta (a atualização prometida no vídeo)

| O que falta | Quando sai | O que fazer |
|---|---|---|
| Curva DI x pré da B3 de 26/out (substitui o DI da imprensa da emenda 9; A7 e o prêmio) | o arquivo `TS261026` não saiu até as 21h de 26/out (22 bytes); costuma sair no dia útil seguinte | `python ferramentas/mercado-do-dia.py` baixa sozinho; depois `python ferramentas/rodar-tudo.py --sem-coleta` |
| Fluxo estrangeiro da B3 de 26/out (A2) | 28/out | atualizar os achados K04 e K09 e rodar de novo |
| O 1º Focus depois da eleição (A7 e o cenário de 2027) | segunda, 02/nov (o de 30/out, se sair na sexta) | `python ferramentas/coletar.py focus-recente focus-ipca-12m` |
| A semana inteira (23/out a 30/out) | sexta, 30/out, depois das 18h | trocar `D1` em `mercado-do-dia.py` por uma 2ª janela (pré-registro M1) |
| Copom de 3 e 4/nov | 04/nov à noite | o sinal 1 do relatório; registrar como fato, sem mudar régua |

**Não entregue nesta rodada (emenda 6):** a régua 2 do M3 (crescimento real da despesa do governo central de 2023 a 2026 contra 2015 a 2022). O Tesouro Transparente respondeu 429 em todas as tentativas de 26/out, até as 21h.

## Para continuar

Comece pelo `RESUMO_SIMPLES.md`, depois o `RELATORIO.md`, o `docs/LEITURA_DA_IA.md` e o `docs/REVISAO_ADVERSARIAL.md`. Qualquer mudança de régua entra como emenda nova no `docs/PRE_REGISTRO.md`, com o que já tinha sido visto.

O roteiro do vídeo mora no repositório de documentação: `referencias-conteudo/roteiros/videos-longos/VIDEO_018_ECONOMIA_BRASIL_2027_2030/`.
