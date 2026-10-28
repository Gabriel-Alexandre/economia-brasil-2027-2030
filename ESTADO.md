# Estado do projeto

**26/out/2026, 23h30. Primeira versão fechada.** O pré-registro foi publicado antes de qualquer conta (07h16, commit `0e7620d`) e recebeu dez emendas, cada uma com o que já tinha sido visto (`docs/PRE_REGISTRO.md` §12). Já estão feitos: a coleta; o fechamento de 26/out (cotações da coleta das 18h16); os juros de 26/out pela curva da B3, que saiu às 23h e substituiu a da imprensa (emendas 9 e 10, sem mudar veredito); os 3 vídeos que circularam de manhã, conferidos afirmação por afirmação (`docs/VIDEOS_QUE_CIRCULARAM.md`, rodada 7: os números deles são do pior momento do dia, não do fechamento); a análise; a validação independente (12 de 12); a revisão adversarial por três leitores; o relatório e a leitura por script; os 10 gráficos; e a conferência de linguagem (0 ocorrência). A cadeia inteira foi rodada de novo às 23h25 (`python ferramentas/rodar-tudo.py --sem-coleta`): 243 achados, 217 com o trecho conferido.

**O resultado em uma linha por afirmação:** bolsa caiu forte (A1 confirmada) · o dinheiro de fora fugiu (A2 não confirmada até 26/out, rodada 9) · muitas medidas sem dinheiro novo (A3 confirmada, 15 medidas e 75% sem compensação) · promessas sem fonte (A4 confirmada, 10 de 14) · gasto alto (A5 confirmada, 46,9% do PIB contra 31,1%) · juro alto (A6 confirmada, 1º de 40) · juro tende a subir (A7 em parte) · dívida de 82,5% a 105,5% do PIB em 2030 no cenário central, subindo nos 17 cenários.

**27/out/2026, rodada 8 (o 2º dia depois da eleição).** Entraram como registro, sem mudar régua nem veredito, no §2.1.2 do relatório: o Tesouro sem nenhum leilão de venda na semana (o de LFT cancelado em 27/out, K51), o ministro da Fazenda, Dario Durigan, prometendo um projeto de lei complementar para buscar o centro da meta e dizendo que a queda não é de fundamento (K52), e a Fitch dizendo que o ajuste que ela espera não basta pra estabilizar a dívida, sem mudar a nota (K53). O fechamento de 27/out (K54) ficou para a rodada 9.

**28/out/2026, rodada 9 (o dado da B3 de 26/out e o 2º dia fechado).** Sete achados novos, todos com 2 fontes conferidas no texto capturado (K60 é a exceção, fonte única e preliminar): o fechamento de 27/out (K54: Ibovespa −0,51%, a 175.710,05; dólar à vista cerca de −1%, a R$ 5,35); o dinheiro de fora com o dado da B3 publicado em 28/out (K55 e K56: o estrangeiro vendeu R$ 2,94 bi em 23/out e R$ 2,85 bi em 26/out, e o saldo ficou em **R$ 13,34 bi em outubro e R$ 40,73 bi no ano, até 26/out**; o relatório e a régua de A2 passaram a usar esse saldo, e **A2 segue não confirmada**, porque os dois saldos continuam positivos); os juros de 27/out (K57: DI de janeiro de 2028 em 14,41%, devolvendo uma parte da alta da véspera; o prêmio da conta segue o de 26/out, como o pré-registro manda); as recompras do Tesouro (K58: R$ 31,6 bi em 2 dias; corrige o K43, que era só a operação da manhã de 26/out); a Moody's (K59: nota Ba1 mantida, superávit de 2% a 3% do PIB para estabilizar a dívida); e o fechamento preliminar de 28/out (K60). **Nenhum veredito mudou e a conta da dívida não mudou** (105,5% do PIB em 2030 no cenário central). Não achados com 2 fontes: um comentário da S&P depois da eleição e o painel das opções de Copom (só uma página de terceiros, citando o Valor Investe: 62% de chance de manutenção em 27/out). O fluxo de 27/out sai na B3 em 29/out.

## O que ainda vai mudar a conta (a atualização prometida no vídeo)

| O que falta | Quando sai | O que fazer |
|---|---|---|
| ~~Fluxo estrangeiro da B3 de 26/out (A2)~~ | ✅ feito na rodada 9 (K55 e K56) | o de 27/out em diante sai com 2 dias de defasagem; entra como achado novo e `fluxo()` em `mercado-do-dia.py` |
| O fechamento oficial de 28/out | 28/out à noite | trocar o K60 (preliminar) por um achado com 2 fontes |
| O 1º Focus depois da eleição (A7 e o cenário de 2027) | segunda, 02/nov (o de 30/out, se sair na sexta) | `python ferramentas/coletar.py focus-recente focus-ipca-12m` |
| A semana inteira (23/out a 30/out) | sexta, 30/out, depois das 18h | trocar `D1` em `mercado-do-dia.py` por uma 2ª janela (pré-registro M1) |
| Copom de 3 e 4/nov | 04/nov à noite | o sinal 1 do relatório; registrar como fato, sem mudar régua |

**Não entregue nesta rodada (emenda 6):** a régua 2 do M3 (crescimento real da despesa do governo central de 2023 a 2026 contra 2015 a 2022). O Tesouro Transparente respondeu 429 em todas as tentativas de 26/out, até as 21h.

## Para continuar

Comece pelo `RESUMO_SIMPLES.md`, depois o `RELATORIO.md`, o `docs/LEITURA_DA_IA.md` e o `docs/REVISAO_ADVERSARIAL.md`. Qualquer mudança de régua entra como emenda nova no `docs/PRE_REGISTRO.md`, com o que já tinha sido visto.

O roteiro do vídeo mora no repositório de documentação: `referencias-conteudo/roteiros/videos-longos/VIDEO_018_ECONOMIA_BRASIL_2027_2030/`.
