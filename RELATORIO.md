# O que esperar da economia do Brasil de 2027 a 2030

**Relatório gerado por script em 2026-10-26** a partir de `resultados/RESUMO.json`. Regras escritas antes de qualquer conta em [`docs/PRE_REGISTRO.md`](docs/PRE_REGISTRO.md), com 6 emendas, cada uma dizendo o que já tinha sido visto. Análise feita pelo Claude (IA da Anthropic), a pedido de Gabriel Alexandre. **Não é recomendação de investimento.**

## O que este projeto não consegue dizer

- **Não prevê preço de ação, de dólar ou de juro.** Os números de 2027 a 2030 são cenários com regra escrita antes. No passado, a previsão do mercado para a dívida três anos depois errou, em média, 7,0 pontos do PIB (§8).
- **Não julga intenção.** Uma medida de ano eleitoral pode ter sido feita para ganhar votos ou não; o projeto mede data, custo e quem paga.
- **O dia seguinte é um dia.** A reação de 26/out mede o susto do mercado com o resultado, não o mandato inteiro (§2.2).
- **A base é a projeção de médio prazo mais recente da IFI, de junho de 2026**, anterior a medidas de setembro e outubro. O efeito delas está calculado à parte (§7.1).
- **O modelo da dívida não tem a volta do juro sobre a confiança** (a dívida maior encarece o juro, que aumenta a dívida). O efeito do fim da escala 6x1 sobre o PIB também fica de fora, por falta de número público.
- **Não testa se houve fraude**: o pedido supõe que não haja contestação.

## 1. A resposta curta

|  | O que o pedido disse | Veredito | Por quê |
|---|---|---|---|
| A1 | "a bolsa derreteu" | confirmada | Ibovespa -13,88% no dia; contra os emergentes (EEM), -13,58 pontos |
| A2 | "vários investimentos [...] acabou fugindo do Brasil" | não confirmada | até 22/out entraram R$ 46,5 bi de estrangeiros na bolsa em 2026 e R$ 19,1 bi em outubro; o dado de 26/out sai na B3 dois dias depois |
| A3 | "muitas medidas" no ano da eleição | confirmada | 15 medidas nos 12 meses antes da eleição; 75% do custo que se repete não tem receita nova para pagar (sai de outra despesa ou de fora do Orçamento). Viraria "em parte" se o que cabe no limite de gasto contasse como pago. Intenção não se mede |
| A4 | "de onde é que vai vir esse dinheiro" | confirmada | 10 de 14 promessas econômicas sem custo publicado ou sem fonte declarada (9 de 13 sem o fim da escala 6x1, que já foi aprovado) |
| A5 | "a gastança do Brasil já está muito alta" | confirmada | o governo (União, estados e municípios) gasta 46,9% do PIB, contra 31,1% na mediana dos emergentes do G20 (FMI, 2025) |
| A6 | "o juro já está muito alto" | confirmada | o Brasil tem o maior juro real entre 40 países no ranking MoneYou de 16/set/2026, com 8,45% ao ano; o segundo tem 6,79% |
| A7 | "a tendência é apenas aumentar" (o juro) | confirmada em parte | o Focus de 2026-10-23 esperava Selic de 11,75% no fim de 2027, abaixo dos 13,75% de hoje; a curva da B3 cobrava 12,38% para 2028 em 23/out; depois do resultado, o DI de janeiro de 2028 (o juro médio cobrado até lá) foi de 12,86% para 14,80%, acima da Selic de hoje (emenda 9) |

**A dívida no cenário central: sobe rápido.** A dívida bruta do governo passa de 82,5% do PIB em 2026 para **105,4% em 2030** (+22,9 pontos; faixa pelo erro histórico, de 98% a 112%). Mesmo sem nenhum prêmio de juros ela sobe 13,2 pontos, o que já é "sobe rápido" pela régua. Para a dívida parar de subir em 2030, o governo precisaria de um superávit de 5,3% do PIB naquele ano (1,9% se o mercado não cobrasse prêmio); a base da IFI prevê um déficit de 1,1%. A distância é de 6,4 pontos do PIB. Em nenhuma das 17 contas feitas (§7.1) a dívida para de subir.

**O cenário central, ano a ano** (o que a conta usa: o cenário base da IFI de junho, mais o prêmio de juros medido no dia):

| Ano | PIB (IFI) | Selic no fim do ano (IFI) | Resultado primário do setor público (IFI) | Dívida bruta no cenário central |
|---|---|---|---|---|
| 2026 | 2,0% | 14% | déficit de 0,5% | 82,5% |
| 2027 | 1,8% | 12% | déficit de 0,7% | 87,8% |
| 2028 | 2,3% | 10% | déficit de 0,6% | 93,6% |
| 2029 | 2,3% | 8% | déficit de 0,8% | 99,0% |
| 2030 | 2,3% | 8% | déficit de 1,1% | 105,4% |

**O que o mercado esperava antes da eleição** (mediana do Focus de 2026-10-23; é outro cenário, mais pessimista no PIB e no juro que o da IFI; a dívida com ele está no §7.1):

| Ano | PIB | Inflação (IPCA) | Selic no fim do ano | Dólar no fim do ano | Dívida bruta (Focus) |
|---|---|---|---|---|---|
| 2026 | 1,8% | 5,19% | 13,25% | R$ 5,05 | 83,5% |
| 2027 | 1,3% | 4,34% | 11,75% | R$ 5,15 | 87,2% |
| 2028 | 1,8% | 3,75% | 10,00% | R$ 5,20 | 90,1% |
| 2029 | 2,0% | 3,50% | 10,00% | R$ 5,28 | 92,7% |
| 2030 | 2,0% | 3,50% | 10,00% | R$ 5,30 | 95,0% |

## 2. O mercado no dia seguinte (M1)

Janela: fechamento de 2026-10-23 contra o de 2026-10-26.

| Ativo | Variação | De → para |
|---|---|---|
| Ibovespa | -13,88% | 205.083 → 176.608 pontos |
| EWZ (ações do Brasil em Nova York, em dólar) | -19,82% | US$ 42,59 → US$ 34,15 |
| EEM (ações de emergentes, controle) | -0,31% |  |
| Dólar contra o real (Yahoo, fechamento) | +6,59% | R$ 5,0499 → R$ 5,3829 |
| Dólar PTAX (média do dia, Banco Central) | +9,19% | R$ 5,0377 → R$ 5,5007 |
| Dólar à vista (fechamento, imprensa) | +8,21% | → R$ 5,4029 ([fonte](https://euqueroinvestir.com/acoes/ibovespa-hoje-reage-a-eleicao-e-derrete-mais-de-1388)) |
| Dólar contra México, Chile, Colômbia e África do Sul (média, controle) | -0,33% |  |
| DI futuro jan/2028 (fechamento, Reuters) | +194 centésimos | 12,86% → 14,80% |
| DI futuro jan/2031 (fechamento, Reuters) | +254 centésimos | 12,64% → 15,19% |

**O que se atribui à eleição (o Brasil menos os outros emergentes):** bolsa -13,58 pontos; dólar +6,92 pontos (dólar do Yahoo nos dois lados, para a mesma hora; a PTAX é a média do dia e mede outra coisa).

**É a 5ª maior queda diária do Ibovespa desde 1995.** Maiores que ela: 10/09/1998 (-15,81%); 27/10/1997 (-14,97%); 12/03/2020 (-14,78%); 16/03/2020 (-13,92%). Nas eleições anteriores (§2.2), o pior dia seguinte tinha sido o de 2002.

- Em 26/out o Tesouro cancelou o leilão de títulos atrelados à inflação (NTN-B) de 27/out e o de prefixados (LTN e NTN-F) de 29/out, e manteve o de títulos ligados à Selic (LFT). ([fonte](https://exame.com/invest/mercados/tesouro-suspende-leiloes-de-titulos-prefixados-e-atrelados-a-inflacao-apos-vitoria-de-lula/), [segunda fonte](https://www.suno.com.br/noticias/tesouro-nacional-suspende-leiloes-ipca-prefixados-2026/))
- Uma fonte registra que o Tesouro recomprou R$ 7,1 bilhões em títulos em 26/out (uma fonte só; fica como registro, sem entrar na conta). ([fonte](https://gazetadoparana.com.br/publico/apos-reeleicao-de-lula-tesouro-cancela-leiloes-de-titulos-publicos-e-recompra-r-71-bilhoes-para))
- Às 10h05 de 26/out a B3 acionou o circuit breaker (queda de 10% do Ibovespa) e suspendeu os negócios à vista por 30 minutos, a primeira vez desde a pandemia. ([fonte](https://www.infomoney.com.br/mercados/circuit-breaker-por-que-bolsa-suspendeu-negociacoes-veja-quando-ela-volta/), [segunda fonte](https://investalk.bb.com.br/noticias/mercado/b3-aciona-circuit-break-pela-1-vez-desde-pandemia-e-suspende-negociacoes-a-vista-por-30-minutos))
- As cotações do Yahoo são as da coleta das 18h16 de 26/out, depois do fechamento de Nova York e com todas as moedas na mesma hora; a coleta das 21h devolveu o dia 26 vazio para o EWZ e os emergentes, e não foi usada.

**O que o mercado esperava:** às 18:00 de 25/out, último registro antes do fim da votação, o Polymarket dava 34,5% de chance a Lula (no fim de 23/out, 22,5%). A reação do dia mede só a parte que não estava no preço; para ter a diferença inteira entre os dois resultados, a variação se divide por 0,655.

### 2.1 O prêmio de juros

Prêmio usado na conta da dívida: **3,89 pontos ao ano** (excesso do DI jan/2031 contra o título de 10 anos dos EUA em 26/out (2,54 ponto), dividido pela surpresa (1 - 0,345)). Medido contra a curva de 12/jun (data da base da IFI), e não contra a véspera, o prêmio é de 0,36 ponto ao ano (variante, §11).

**A Selic que a curva cobra para 2028** (taxa a termo entre os DI de janeiro de 2028 e de 2029, emenda 4): 12,38% em 23/out. A Selic hoje é 13,75%.

### 2.2 As eleições anteriores

| Eleição | Venceu | Ibovespa no dia seguinte | Dólar PTAX no dia seguinte | PIB médio no mandato seguinte (FMI) | Dívida bruta, conceito do FMI (% do PIB) | Ibovespa acima da inflação no mandato |
|---|---|---|---|---|---|---|
| 2002 | Lula | -4,4% | -1,6% | 3,5% | 76,1 → 64,6 | +244% |
| 2006 | Lula | -1,1% | +0,4% | 4,7% | 64,6 → 62,4 | +45% |
| 2010 | Dilma | +1,3% | +0,2% | 2,4% | 62,4 → 61,6 | -45% |
| 2014 | Dilma | -2,8% | +2,2% | -0,9% | 61,6 → 84,8 | +37% |
| 2018 | Bolsonaro | -2,2% | -1,0% | 1,4% | 84,8 → 83,9 | +4% |
| 2022 | Lula | +1,3% | -1,7% | 2,8% | 83,9 → 97,0 (projeção do FMI) | +27% (até hoje) |

Em 4 das 6 eleições a bolsa caiu no dia seguinte. A direção do dia bateu com a da bolsa no mandato em **1 de 6**. Em 2002 o Ibovespa caiu 4,4% no dia seguinte e depois subiu 244% acima da inflação até 2006; em 2010 subiu 1,3% e depois caiu 45% acima da inflação até 2014. **O dia seguinte mede o susto, não o mandato.** O que decidiu os mandatos foi o que veio depois: em 2003, a meta de superávit de 4,25% do PIB; no mandato que começou em 2015, PIB médio de -0,9% ao ano. A dívida desta tabela está no conceito do FMI, maior que o do Banco Central usado no resto do relatório.

## 3. O dinheiro estrangeiro (M2)

- De janeiro a 22/out de 2026, os estrangeiros compraram R$ 46,5 bi a mais do que venderam em ações na B3 (sem contar ofertas novas) ([fonte](https://www.dadosdemercado.com.br/fluxo)).
- Só em outubro, até o dia 22, a entrada foi de R$ 19,1 bi ([fonte](https://www.dadosdemercado.com.br/fluxo)).
- No primeiro pregão depois do 1º turno (5/out) entraram R$ 10,1 bi num dia só, recorde ([fonte](https://www.dadosdemercado.com.br/fluxo)).
- O pior mês do ano foi agosto, com saída de R$ 18,1 bi ([fonte](https://trademap.com.br/noticias/news-8266222)).
- Nos dias antes do 2º turno o saldo já oscilava: 19/10, R$ -1.008,76 mi, 20/10, R$ +17,64 mi, 21/10, R$ +156,88 mi, 22/10, R$ -1.030,50 mi.
- Pelo balanço de pagamentos do Banco Central, que conta todo tipo de compra de ações (não só a bolsa) e também a renda fixa, o saldo do investimento estrangeiro em carteira no Brasil de janeiro até 09/2026 foi: ações, US$ -3,4 bi; fundos de investimento, US$ -2,1 bi; títulos de dívida negociados no país, US$ 5,7 bi; títulos de dívida negociados no exterior, US$ 9,6 bi.
- A imprensa registrou que os investidores estrangeiros estavam posicionados para a vitória do outro candidato ([fonte](https://www.infomoney.com.br/mercados/ibovespa-em-alta-dolar-em-queda-a-reacao-do-mercado-entre-1o-e-2o-turno-da-eleicao/)).

A régua de A2 usa a primeira medida (a bolsa, B3), como o pré-registro manda. Pela segunda (o balanço de pagamentos), a entrada de 2026 foi sobretudo em renda fixa (US$ 15,3 bi), e em ações, contando tudo, o saldo foi de saída (US$ 3,4 bi). As duas medidas contam coisas diferentes: a B3 só a bolsa; o Banco Central também ações fora da bolsa e recibos negociados lá fora.

## 4. As contas públicas hoje (M3)

| Banco Central, % do PIB | dez/2014 | dez/2018 | dez/2022 | dez/2025 | último (2026-08) |
|---|---|---|---|---|---|
| Déficit primário em 12 meses (negativo = superávit) | 0,56 | 1,55 | -1,25 | 0,43 | 0,62 |
| Juros da dívida em 12 meses | 5,95 | 6,96 | 4,57 | 8,34 | 9,48 |
| Dívida bruta do governo geral (conceito do Banco Central) | 56,3 | 75,3 | 71,7 | 78,6 | 82,9 |
| Dívida líquida do setor público | 32,6 | 52,8 | 56,1 | 65,2 | 69,3 |

**O déficit total (primário mais juros) é de 10,1% do PIB em 12 meses, e a maior parte é juro:** 9,48 pontos de juros contra 0,62 de déficit primário.

Mais da metade da dívida federal acompanha a Selic: 52,74% (Tesouro, ago/2026; uma série da IFI, com outra base, dá menos). Cada ponto de Selic custa cerca de R$ 49 bi por ano.

### 4.1 O tamanho do gasto, contra o mundo (A5)

| FMI, Fiscal Monitor, % do PIB | 2019 | 2022 | 2025 | 2026 (projeção) |
|---|---|---|---|---|
| Brasil: gasto total do governo geral | 43,0 | 43,4 | 46,9 | 48,7 |
| Emergentes do G20 (mediana, sem o Brasil) | 31,8 | 29,9 | 31,1 | 30,5 |
| Emergentes e renda média (média do FMI) | 31,6 | 31,2 | 32,3 | 32,4 |
| América Latina (mediana, sem o Brasil) | 28,5 | 29,1 | 30,5 | 29,8 |
| Países avançados (média) | 38,7 | 40,3 | 40,9 | 41,4 |

Diferença do Brasil para a mediana dos emergentes do G20 em 2025: **+15,8 pontos do PIB** (régua: 5 ou mais = confirmada). O FMI estima os juros líquidos do Brasil em 7,3% do PIB em 2025; como o gasto total inclui os juros, a parte sem juros fica um pouco abaixo da diferença acima. Déficit nominal do governo geral em 2025 (régua 3): Brasil 7,4% do PIB, mediana dos emergentes do G20 4,9%. A régua 2 (crescimento real da despesa do governo central de 2023 a 2026 contra 2015 a 2022) não foi calculada nesta rodada (emenda 6).

## 5. O juro (M4)

Selic de **13,75%** ao ano e inflação esperada para os próximos 12 meses de **4,53%** (Focus de 2026-10-23): juro real de **8,8%** ao ano. No ranking MoneYou de 16/set, feito com outra estimativa de inflação, o juro real do Brasil era 8,45%, o maior entre 40 países.

- Cada ponto de Selic a mais custa cerca de R$ 49 bi por ano só na parte da dívida federal atrelada à Selic (52,74% de R$ 9.293 bi. Tesouro. ago/2026). ou 0,36% do PIB; sem contar as operações compromissadas do Banco Central
- Última decisão do Copom em 2026 (281ª reunião, 16/09/2026): Selic cortada para 13,75% a.a. Orientação: 'a magnitude total do ciclo de calibração será estabelecida à luz de novas informações'; cenário com 'desancoragem das expectativas'; projeção de IPCA 3,2% no 1º tri de 2028; Focus 4,9% (2026) e 4,3% (2027). Cortes anteriores: 14,25% (17/06) e 14,00% (05/08). ([fonte](https://www.bcb.gov.br/api/servico/sitebcb/copom/comunicados_detalhes?nro_reuniao=281))
- Próxima reunião do Copom: 4 de novembro de 2026, dez dias depois da eleição (InfoMoney). Bruno Corano (Corano Capital), opinião: alta probabilidade de o BC interromper o ciclo de cortes. ([fonte](https://www.infomoney.com.br/onde-investir/tesouro-direto-abertura-fechamento-26102026/))

## 6. As medidas de 2025 e 2026 e as promessas: quem paga (M5)

Categorias: **A** compensada na própria lei (imposto maior para outro grupo) · **B** cabe no limite de gasto (o dinheiro sai de outra despesa do Orçamento) · **C** fora da meta · **D** fora do Orçamento (tarifa, fundo, renúncia, crédito) · **E** sem fonte declarada.

|  | Medida | Cat. | Custo informado (R$ bi) | Custo que se repete a partir de 2027 (R$ bi por ano) | De onde vem o dinheiro |
|---|---|---|---|---|---|
| M01 | Isenção do IR até R$ 5 mil e redução até R$ 7.350 (Lei 15.270/2025), com tributação mínima de altas rendas | A | 25.84 | 27.72 | Compensação na própria lei: tributação mínima de altas rendas (estimada em R$ 25,22 bi em 2026) e tributação de dividendos remetidos ao exterior (R$ 8,90 bi), pela estima |
| M02 | Gás do Povo (recarga gratuita do botijão de 13 kg) | B | 4.7 | 4.7 | Dotações do Ministério do Desenvolvimento e Assistência Social no Orçamento, despesa discricionária sujeita à disponibilidade (LOA 2026: mais de R$ 4,7 bi; o PLOA tinha R |
| M03 | Luz do Povo: tarifa social com gratuidade até 80 kWh/mês e isenção da CDE até 120 kWh | D | 10.4 | 10.4 | Conta de Desenvolvimento Energético (CDE), encargo cobrado na tarifa dos demais consumidores de energia; não passa pelo Orçamento da União. |
| M04 | Pé-de-Meia em 2025 (pago via fundo Fipem, fora do Orçamento) | D | 12.5 | não se repete | Fundo privado Fipem (Caixa), integralizado com recursos de outros fundos (FGO, Fgeduc); só ~R$ 1 bi estava na LOA 2025. |
| M05 | Pé-de-Meia em 2026 (dentro da LOA) | B | 11.47 | 11.47 | Dotação do MEC na LOA 2026, dentro do limite de despesas. |
| M06 | Crédito do Trabalhador (consignado para empregados do setor privado) | D | sem custo publicado | não se repete | Crédito de bancos privados e públicos, com garantia do FGTS do próprio trabalhador; não há despesa orçamentária declarada. |
| M07 | Reforma Casa Brasil (crédito para reforma de moradias) | D | sem custo publicado | não se repete | R$ 30 bi do Fundo Social do pré-sal (empréstimo, retorna ao fundo) e R$ 10 bi do SBPE da Caixa; ver M08 para o aporte em fundo garantidor por crédito extraordinário. |
| M08 | MP 1.385/2026: crédito extraordinário de R$ 3,5 bi para fundos garantidores de crédito (inclui o da habitação popular) | C | 3.5 | não se repete | Crédito extraordinário (art. 167, §3º da Constituição), fora do limite de despesas; segundo a Agência Câmara, não afeta a meta fiscal, mas aumenta a dívida. |
| M09 | Minha Casa Minha Vida, Faixa 4 (renda até R$ 12 mil, depois R$ 13 mil) | D | sem custo publicado | não se repete | R$ 15 bi do FGTS mais R$ 15 bi captados por instituições financeiras; a MP 1.291 permitiu usar o Fundo Social do pré-sal em habitação. |
| M10 | Agora Tem Especialistas (atendimento do SUS em hospitais privados pago com crédito tributário) | D | 2.0 | 2.0 | Renúncia de receita: o crédito abate tributos federais, com limite anual de R$ 2 bi; a lei manda incluir a renúncia na estimativa de receita da LOA (art. 14 da LRF), sem  |
| M11 | Novo Desenrola Brasil (renegociação de dívidas com juros até 1,99% ao mês e aporte no FGO) | B | 5.0 | não se repete | Aporte da União no FGO de até R$ 5 bi em 2026, declarado na exposição de motivos como compatível com a meta e sujeito à disponibilidade orçamentária. |
| M12 | Desenrola Brasil 3.0: compra de carteiras de dívidas pela União em leilão (MP 1.393/2026) | B | 15.0 | 5.0 | Dotações do Ministério da Fazenda, despesa discricionária sujeita à disponibilidade orçamentária, com teto de R$ 15 bi. |
| M13 | Reajuste do Bolsa Família em 15,04% (piso de R$ 600 para R$ 691) | B | 22.7 | 22.7 | Segundo a equipe econômica, cabe no limite de gastos de 2026 sem crédito extraordinário (R$ 5,8 bi de out a dez/2026). |
| M14 | Salário mínimo de 2026: R$ 1.621 (alta de 6,79%, com ganho real de 2,5%) | B | 39.1 | 39.1 | Despesa obrigatória (Previdência, BPC, abono, seguro-desemprego) dentro do limite do arcabouço; a Lei 15.077/2024 limita o ganho real ao crescimento permitido das despesa |
| M15 | Subvenção ao diesel e PIS/Cofins zero, compensados por imposto de exportação de petróleo (MP 1.340/2026) | A | 10.0 | não se repete | Na própria MP: imposto de exportação sobre petróleo bruto e diesel, com arrecadação estimada em R$ 15,6 bi em quatro meses (Brent a US$ 90), parte para compensar o PIS/Co |
| M16 | Subvenções a gasolina e diesel por crédito extraordinário (MPs 1.358 e 1.363/2026) | C | 11.0 | não se repete | Créditos extraordinários: a IFI registra R$ 6,8 bi de créditos extraordinários para subvenção a combustíveis (MPs 1.358 e 1.363) na avaliação do 3º bimestre de 2026. |
| M17 | Fim da escala 6x1 e jornada de 40 horas sem redução salarial (Emenda Constitucional 141) | D | sem custo publicado | não se repete | Sem despesa pública: o custo recai sobre os empregadores. A EC permite lei complementar com medidas transitórias para MEI, micro e pequenas empresas, sem fonte definida. |
| M18 | Ressarcimento de descontos indevidos nos benefícios do INSS | C | 3.2 | não se repete | Crédito extraordinário (a IFI lista a MP 1.378 entre os créditos extraordinários: R$ 547 mi). |
| M19 | Farmácia Popular 100% gratuito (todos os 41 itens) | E | sem custo publicado | não se repete | Nenhuma estimativa de custo adicional nem fonte específica foi localizada; o programa é executado com dotação do Ministério da Saúde. |
| M20 | Prospera MEI: perdão de dívidas de MEIs com a União (anunciado em 13/out, entre os turnos; vale a partir de 1º/jan/2027) | E | 1.12 | 1.01 | Renúncia de receita sem compensação: o projeto dispensa a compensação da Lei de Responsabilidade Fiscal. |
| M21 | Gasolina com PIS/Pasep, Cofins e Cide zerados por 30 dias e mais subsídio ao diesel (09/out, entre os turnos) | C | 5.2 | não se repete | Crédito extraordinário (MP 1.395), fora do limite de gasto, e renúncia de tributos por 30 dias. |

**Custo que se repete por ano a partir de 2027: R$ 124,1 bi (0,85% do PIB).** categoria A: R$ 27,7 bi (22%); categoria B: R$ 83,0 bi (67%); categoria D: R$ 12,4 bi (10%); categoria E: R$ 1,0 bi (1%). A leitura de quanto se repete por ano é do projeto, com o motivo escrito ao lado de cada medida em `dados/evidencias/MEDIDAS_E_PROMESSAS.csv`.

**O tamanho do pacote de 2026 pela IFI:** A IFI estimou que as medidas do governo em 2026 mobilizaram R$ 298,4 bilhões: R$ 93,8 bilhões com impacto nas contas (primário) e R$ 185,7 bilhões em crédito com juros subsidiados, que deve voltar à União. ([fonte](https://timesbrasil.com.br/eleicoes-2026/bondades-governo-298-bilhoes-ifi-contas-2027/), [segunda fonte](https://boca.com.br/economia/instituicao-alerta-sobre-necessidade-de-ajuste-fiscal)). A conta acima, de quanto se repete a partir de 2027, é outra medida: ela não soma o crédito que volta à União nem o que foi de uma vez só.

**A compensação do Imposto de Renda é contestada:** a lei compensa a isenção com a tributação mínima de altas rendas, e a Consultoria de Orçamento do Senado e a IFI estimaram perda líquida de arrecadação.

**Promessas do 2º mandato:**

|  | Promessa | Cat. | Custo (R$ bi por ano) | De onde vem o dinheiro |
|---|---|---|---|---|
| P01 | Tarifa zero no transporte coletivo aos fins de semana e feriados (PEC 18/2026) | B | 12.0 | Declarada: remanejamento de 26,8% das emendas parlamentares de execução obrigatória (R$ 44,8 bi no PLOA 2027), dentro do Orçamento. |
| P02 | Pé-de-Meia universitário (R$ 700 por mês e poupança de R$ 2.500 por ano) | D | 4.6 | Declarada pela campanha (Camilo Santana): Fundo Social do Pré-Sal. |
| P03 | Universalizar o Pé-de-Meia no ensino médio público | E | 5.0 | Sem fonte declarada nas falas; em jul/2025 o MEC dizia depender de ampliação orçamentária negociada com o Congresso. |
| P04 | Universalizar a escola de tempo integral até o ensino médio | E | sem custo publicado | Sem fonte declarada e sem custo publicado localizado. |
| P05 | Continuar a valorização do salário mínimo acima da inflação | B | sem custo publicado | Despesa obrigatória dentro do limite; o ganho real está limitado pela Lei 15.077/2024. Cada R$ 1 no mínimo custa cerca de R$ 380,5 mi por ano à Previdência (Die |
| P06 | Comprar dívidas das famílias em leilão com deságio de 90% ou mais (Desenrola 3.0) | B | 15.0 | Declarada na MP: dotações do Ministério da Fazenda, discricionárias, com teto de R$ 15 bi. |
| P07 | Fim da escala 6x1 e jornada de 40 horas (promessa do plano, já cumprida pela EC 141) | D | sem custo publicado | Sem despesa pública; custo com os empregadores (ver M17). |
| P08 | Manter a Farmácia Popular 100% gratuita (e incluir exames, segundo a seleção do projeto de simulação) | E | sem custo publicado | Sem custo publicado e sem fonte declarada. |
| P09 | Manter, aperfeiçoar e ampliar a proteção social e a transferência de renda | E | sem custo publicado | Sem custo publicado e sem fonte declarada. |
| P10 | Manter e ampliar o Minha Casa Minha Vida para todas as faixas | E | sem custo publicado | Sem custo publicado e sem fonte declarada no plano. |
| P11 | Seguir mitigando a volatilidade dos preços de combustíveis | E | sem custo publicado | Sem custo publicado e sem fonte declarada; em 2026 as medidas custaram até R$ 10 bi (M15) e R$ 11 bi (M16). |
| P12 | Impulsionar o Agora Tem Especialistas e o diagnóstico e tratamento de câncer em 30 dias | D | 2.0 | O programa vigente é pago com renúncia de tributos (até R$ 2 bi por ano, M10); a ampliação prometida não tem custo nem fonte declarados. |
| P13 | Debater o barateamento da energia elétrica para residências e empresas | E | sem custo publicado | Sem custo publicado e sem fonte declarada. |
| P14 | Pé-de-Meia Licenciatura / Pé-de-Meia Professor | E | sem custo publicado | Sem custo publicado e sem fonte declarada nas fontes lidas. |
| P15 | Manter o arcabouço fiscal (restrição declarada para as promessas) |  | sem custo publicado | Não se aplica. |

## 7. 2027 a 2030 (M6)

| Cenário (dívida bruta, conceito do Banco Central, % do PIB) | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|---|
| S0: base da IFI (jun/2026) | 82,5 | 86,4 | 90,1 | 92,7 | 95,7 |
| S1: central (base + prêmio de 3,89 pontos) | 82,5 | 87,8 | 93,6 | 99,0 | 105,4 |
| S2: risco (S1 + promessas com custo e sem fonte, 0,03% do PIB) | 82,5 | 87,8 | 93,7 | 99,1 | 105,6 |
| Mercado (Focus, antes da eleição) | 83,5 | 87,2 | 90,1 | 92,7 | 95,0 |

No conceito do FMI, que soma os títulos do Tesouro na carteira do Banco Central, o FMI projeta 97,0% em 2026 e 104,5% em 2030 (WEO de out/2026). Não se compara um conceito com o outro.

### 7.1 Sensibilidade e variantes (dívida em 2030)

| Variante | Dívida em 2030 (% do PIB) |
|---|---|
| prêmio pela metade | 100,5 |
| prêmio em dobro | 115,8 |
| o prêmio passa inteiro para a dívida já em 2027 | 109,7 |
| PIB 1 ponto abaixo por ano | 109,4 |
| PIB 1 ponto acima por ano | 101,6 |
| se o limite de gasto não segurar o reajuste do Bolsa Família e o Desenrola 3.0 | 106,2 |
| cenário otimista da IFI, com o prêmio | 94,3 |
| cenário pessimista da IFI, com o prêmio | 116,6 |
| (P2) sem prêmio nenhum | 95,7 |
| (P2) prêmio medido contra a curva de junho (0,36 ponto) | 96,6 |
| (P2) metas do PLDO 2027 cumpridas, sem prêmio | 88,0 |
| (P2) metas do PLDO 2027 cumpridas, com o prêmio | 97,5 |
| (P1) macro do Focus no lugar do da IFI | 108,5 |
| (P1) 2026 começando com os juros já acima da base | 111,3 |
| (P1) limite de gasto sem segurar os R$ 51,3 bi por ano que a base não tem | 106,8 |
| (P1) as três juntas | 116,0 |

### 7.2 O aperto do Orçamento

- Governo (MOMP do PLOA 2027): o espaço para discricionárias do Executivo cai de R$ 222,1 bi (2027) para R$ 208,4 bi (2028), abaixo da linha de base de R$ 224,2 bi. ([fonte](https://www.gov.br/planejamento/pt-br/assuntos/orcamento/orcamentos-anuais/2027/ploa-2027/mensagem-presidencial.pdf/@@display-file/file))
- Precatórios e RPVs: incorporação à meta de 39,4% em 2027, 55,7% em 2028, 61,5% em 2029 e 67,7% em 2030; fora da meta: R$ 59,2 bi, 52,6 bi, 46,0 bi e 39,4 bi. ([fonte](https://www.gov.br/planejamento/pt-br/assuntos/orcamento/orcamentos-anuais/2027/ploa-2027/mensagem-presidencial.pdf/@@display-file/file))
- IFI, cenário base: meta de 2026 atingida no limite inferior; para 2027, contingenciamento de R$ 35,7 bilhões. ([fonte](https://www12.senado.leg.br/ifi/pdf/raf113_jun2026.pdf))
- IFI: a partir de 2028, mantidas as metas, o Executivo precisará de novas medidas de receita ou de corte para evitar a interrupção da máquina pública. ([fonte](https://www12.senado.leg.br/ifi/pdf/raf113_jun2026.pdf))
- Segundo a IFI, as despesas obrigatórias sujeitas ao limite crescem R$ 131,4 bi de 2026 para 2027; o PLOA 2027 prevê R$ 1,169 trilhão em benefícios previdenciários e R$ 145,1 bi para o BPC. ([fonte](https://www12.senado.leg.br/ifi/pdf/raf116_set2026.pdf))

## 8. O teste do passado (M7)

| Eleição | Ano previsto | Dívida líquida prevista (Focus, outubro) | Aconteceu | Erro (pontos) | PIB médio previsto / aconteceu |
|---|---|---|---|---|---|
| 2002 | 2005 | 56,2 | 47,9 | +8,3 | 3,0% / 3,4% |
| 2006 | 2009 | 45,3 | 40,9 | +4,4 | 3,5% / 3,7% |
| 2010 | 2013 | 37,0 | 30,5 | +6,5 | 4,5% / 3,0% |
| 2014 | 2017 | 35,0 | 51,4 | -16,4 | 2,1% / -1,8% |
| 2018 | 2021 | 60,5 | 55,1 | +5,4 | 2,5% / 0,9% |
| 2022 | 2025 | 66,5 | 65,2 | +1,3 | 1,5% / 3,0% |

Erro médio de 7,0 pontos do PIB na dívida e de 1,5 ponto no PIB. Em 5 de 6 eleições o mercado previu dívida **maior** do que aconteceu; a exceção foi a eleição de 2014, com erro de -16,4 pontos. A conta compara a previsão de cada época com a série atual do Banco Central, que mudou de método em 2008. É esse erro que dá a faixa do número central (§1).

## 9. Outras coisas importantes (M8)

Só entram temas com as duas fontes conferidas por script. A frase "o que pode mudar" é a leitura da pesquisa, não um número.

- **Reforma tributária: 2026 é ano de teste.** Em 2026 a CBS (0,9%) e o IBS (0,1%) aparecem em nota fiscal só como teste, sem recolhimento efetivo. *O que pode mudar:* O ano de teste acaba em 2026; o mandato de 2027 a 2030 pega o começo da cobrança real e o grosso da transição. ([fonte](https://www.poder360.com.br/poder-economia/reforma-tributaria-saiba-como-sera-o-cronograma-ate-2033/), [segunda fonte](https://www.contabeis.com.br/noticias/73889/reforma-tributaria-2026-veja-o-que-muda-na-fase-de-transicao/))
- **Reforma tributária: 2027 a 2033.** Em 2027 PIS e Cofins são extintos, a CBS passa a ser cobrada (alíquota estimada 8,7%, a confirmar) e entra o Imposto Seletivo; de 2029 a 2032 ICMS e ISS caem para 90%, 80%, 70% e 60% e o IBS sobe; 2033 é o modelo pleno. *O que pode mudar:* Todo o mandato 2027 a 2030 acontece dentro da transição: CBS cheia desde 2027 e troca do ICMS/ISS a partir de 2029; alíquota final e neutralidade da arrecadação são riscos de receita do período. A segunda fonte é o mesmo site (não achei outra conferível). ([fonte](https://www.contabeis.com.br/noticias/73889/reforma-tributaria-2026-veja-o-que-muda-na-fase-de-transicao/), [segunda fonte](https://www.contabeis.com.br/noticias/73889/reforma-tributaria-2026-veja-o-que-muda-na-fase-de-transicao/))
- **Tarifas dos EUA sobre o Brasil.** Desde 22/jul/2026 vale tarifa adicional de 25% (Seção 301) sobre parte das exportações brasileiras; o ministro do Comércio estimou cerca de 18% das vendas aos EUA (quase US$ 7 bi); a Suprema Corte dos EUA derrubou em fevereiro as tarifas anteriores de até 50%. *O que pode mudar:* A tarifa é estrutural (Seção 301, não emergencial) e entra no mandato; o tamanho afetado diverge entre fontes (18% pelo ministro, 23,1% pelo MDIC). Não achei texto conferível sobre o estado da negociação em out/2026. ([fonte](https://profit.pakistantoday.com.pk/2026/07/17/us-imposes-25percent-tariffs-on-brazilian-goods-keeps-exemptions-for-beef-coffee-and-aircraft), [segunda fonte](https://www.opovo.com.br/noticias/economia/2026/07/24/mdic-aponta-que-231-das-exportacoes-brasileiras-aos-eua-estao-sujeitas-a-novas-tarifas.html))
- **Exportações aos EUA em 2026.** Exportações para os EUA caíram 12,4% de janeiro a julho de 2026 (perda de US$ 2,9 bi); em setembro subiram 31,9% (US$ 3,5 bi) sobre base fraca, mas o acumulado do ano ainda cai 6,5%. *O que pode mudar:* O choque é concentrado em setores (madeira, máquinas, calçados, móveis) e parcialmente redirecionado. A manchete da Poder360 diz 12,4% (o endereço diz 12,2%: página atualizada). ([fonte](https://www.poder360.com.br/poder-economia/exportacao-do-brasil-para-os-eua-cai-122-no-acumulado-de-2026/), [segunda fonte](https://www.diariodepernambuco.com.br/colunas/diario-economico/2026/10/11726401-exportacoes-brasileiras-para-os-estados-unidos-cresceram-319-em-setembro.html))
- **Efeito das tarifas no PIB.** O Daycoval estimou o impacto das tarifas de 25% em 0,03 ponto do PIB de 2026; o FMI, em janeiro de 2026, cortou o PIB do Brasil de 2026 para 1,6% citando as tarifas. *O que pode mudar:* Estimativas de efeito direto são pequenas (centésimos a décimos de ponto); o risco para 2027 a 2030 é escalada ou retaliação, não a tarifa atual. ([fonte](https://monitordomercado.com.br/noticias/408942-impacto-das-tarifas-no-pib-brasileiro-sera-de-apenas-003-projeta-daycoval/), [segunda fonte](https://jovempan.com.br/noticias/economia/fmi-reduz-previsao-de-crescimento-do-pib-do-brasil-para-16-em-2026.html))
- **China.** O PIB da China cresceu 4,5% no 3º trimestre de 2026 (4,3% no 2º); o FMI, em julho, projetou 4,6% em 2026 e 4,1% em 2027, citando petróleo caro. *O que pode mudar:* China desacelerando para perto de 4% reduz o impulso de demanda por minério e soja no mandato. ([fonte](https://timesbrasil.com.br/mundo/pib-china-cresce-4-5-terceiro-trimestre-2026/), [segunda fonte](https://www.dgabc.com.br/Noticia/4333971/fmi-eleva-previsao-do-pib-da-china-em-2026-e-2027-mas-alerta-para-dificuldades-na-economia))
- **Minério de ferro em 2026.** Em 24/jul/2026 o minério fechou a 746 iuanes (US$ 110,11) em Dalian e a US$ 98,1 em Cingapura, com demanda fraca por aço na China. *O que pode mudar:* Com Simandou entrando e a China desacelerando, o consenso é de minério perto ou abaixo de US$ 100 no mandato. A segunda fonte é de dez/2025 (Bloomberg Línea), não de 2026; não achei cotação de outubro. ([fonte](https://www.noticiasagricolas.com.br/noticias/politica-economia/425270-minerio-de-ferro-recua-em-dalian-em-meio-a-demanda-fraca-e-oferta-abundante.amp.html), [segunda fonte](https://www.bloomberglinea.com.br/negocios/vale-reduz-estimativa-de-producao-de-minerio-de-ferro-para-2026/))
- **Juros nos EUA (Fed).** O Fed SUBIU os juros em 16/set/2026, por 12 a 0, para 3,75% a 4,00%; em julho tinha mantido 3,50% a 3,75% com 3 votos por alta; a ata indica que a maioria espera nova alta até o fim de 2026. *O que pode mudar:* Fed em alta, e não em corte, reduz o espaço para a Selic cair rápido e encarece o financiamento externo no começo do mandato. Não achei número conferível do índice DXY de out/2026. ([fonte](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm), [segunda fonte](https://bpmoney.com.br/economia/ata-do-fed-indica-nova-alta-de-juros-nos-eua-ainda-em-2026/))
- **Precatórios: volta para dentro da meta.** Pela PLDO 2027, 39,4% dos precatórios de 2027 entram na meta (o mínimo constitucional é 10%) e R$ 57,8 bi ficam fora; o Tesouro (jan/2026) projetava R$ 96 bi fora da meta em 2027 e pico de R$ 98,7 bi em 2028, caindo até 2036. *O que pode mudar:* A EC 136/2025 obriga incorporar ao menos 10 pontos por ano até 2036: a cada ano do mandato dezenas de bilhões passam a disputar espaço dentro do limite. A Consultoria da Câmara cita R$ 59,2 bi fora no PLOA (não conferido: PDF bloqueado). ([fonte](https://www12.senado.leg.br/noticias/materias/2026/04/15/lei-de-diretrizes-orcamentarias-preve-salario-minimo-de-r-1-717-em-2027), [segunda fonte](https://timesbrasil.com.br/brasil/economia-brasileira/precatorios-fora-da-meta-chegarao-a-rs-98-7-bilhoes-em-2028/))
- **Despesas obrigatórias, previdência e BPC.** Segundo a IFI, as despesas obrigatórias sujeitas ao limite crescem R$ 131,4 bi de 2026 para 2027; o PLOA 2027 prevê R$ 1,169 trilhão em benefícios previdenciários e R$ 145,1 bi para o BPC. *O que pode mudar:* Obrigatórias crescendo acima do limite de 2,5% real espremem a despesa discricionária ano a ano; a IFI duvida das economias com revisão de benefícios previdenciários e do BPC que o PLOA conta. ([fonte](https://www12.senado.leg.br/ifi/pdf/raf116_set2026.pdf), [segunda fonte](https://www.acessa.com/economia/2026/09/338457-no-ploa-projecao-de-despesa-previdenciaria-e-de-rs-1169-tri-para-2027.html))
- **Salário mínimo 2027.** O PLOA 2027 prevê salário mínimo de R$ 1.741 (alta de R$ 120 sobre R$ 1.621); em abril, a PLDO previa R$ 1.717. *O que pode mudar:* Cada real do mínimo reajusta previdência, BPC e abono: é a correia que liga a política de valorização ao crescimento das obrigatórias. ([fonte](https://meutudo.com.br/blog/noticias/2026/09/14/aposentados-e-beneficiarios-do-bpc-vao-receber-mais-com-o-novo-salario-de-2027-confira/), [segunda fonte](https://www12.senado.leg.br/noticias/materias/2026/04/15/lei-de-diretrizes-orcamentarias-preve-salario-minimo-de-r-1-717-em-2027))
- **Inadimplência das famílias (Serasa).** A Serasa contou 81,7 milhões de inadimplentes em fevereiro de 2026, recorde da série, alta de 38,1% em dez anos. *O que pode mudar:* Metade dos adultos negativada limita o consumo a crédito e explica a pressão por programas como o Desenrola; a queda da Selic demora a chegar ao crédito pessoal. ([fonte](https://www.serasa.com.br/imprensa/10-anos-do-mapa-de-inadimplencia/), [segunda fonte](https://timesbrasil.com.br/brasil/economia-brasileira/brasil-atinge-817-milhoes-de-inadimplentes-em-fevereiro-de-2026-maior-nivel-da-serie-diz-serasa/))
- **Endividamento das famílias (BCB).** Em maio de 2026 o endividamento das famílias era 49,8% da renda (recorde de 49,9% em fev/2026), o comprometimento da renda 28,5% e o juro médio do crédito livre a pessoas físicas 64% ao ano (junho). *O que pode mudar:* Com quase 30% da renda indo para dívida, o consumo das famílias tem pouco espaço para puxar o crescimento no começo do mandato. ([fonte](https://www.diariodepernambuco.com.br/economia/2026/07/11719918-juros-das-familias-seguem-elevados-e-chegam-a-64-ao-ano-diz-bc.html), [segunda fonte](https://www.poder360.com.br/poder-economia/bc-alerta-para-endividamento-alto-e-risco-no-credito/))
- **Recuperações judiciais de empresas.** Recorde de 7.980 empresas em recuperação judicial no fim de junho de 2026 (RGF Bizdoc), alta de 21,2% em um ano; em 2025 a Serasa contou 2.466 empresas pedindo RJ, maior número desde 2012. *O que pode mudar:* Juro alto por muito tempo aparece em quebra de empresa (o agro lidera o crescimento); a carteira de crédito ruim é herança para 2027. ([fonte](https://www.revistaoeste.com/economia/brasil-chega-a-quase-8-mil-empresas-em-recuperacao-judicial/), [segunda fonte](https://www.infomoney.com.br/business/serasa-experian-recuperacao-judicial-cresce-em-2025-e-atinge-maior-no-desde-2012/))
- **Emprego e renda.** Desemprego de 5,3% no trimestre jun-ago/2026; população ocupada de 103,5 milhões e massa de renda real de R$ 385,6 bi, as maiores da série (desde 2012); rendimento médio de R$ 3.777 (+3,7% em 12 meses). *O que pode mudar:* Mercado de trabalho apertado sustenta renda, mas também inflação de serviços. Não achei texto que diga com todas as letras 'menor taxa da série' para os 5,3% (um portal deu 5,4% em junho como mínima da série). ([fonte](https://agenciagov.ebc.com.br/noticias/202609/desemprego-cai-no-trimestre-e-numero-de-pessoas-ocupadas-e-o-maior-da-serie-historica), [segunda fonte](https://viva.com.br/dinheiro/taxa-de-desemprego-fica-em-53-no-trimestre-ate-agosto.html))
- **Produtividade.** Produtividade por hora efetiva cresceu 1,0% no 2T26 (FGV IBRE), depois de cair 0,5% no 1T26; desde 2019 oscila entre queda e ligeira alta. *O que pode mudar:* Crescer acima de ~2% no mandato sem produtividade depende de mais gente ocupada, que já está em recorde. A própria página do IBRE traz 0,9% em outro trecho. ([fonte](https://blogdoibre.fgv.br/node/2400), [segunda fonte](https://www.portaltela.com/economia/2026/06/16/produtividade-do-trabalho-cai-no-brasil-no-1o-trimestre/))
- **Inflação de 2026.** IPCA de setembro de 2026: 0,82% no mês, 3,95% no ano e 4,58% em 12 meses, acima do teto de 4,5%; habitação subiu 2,31% (energia). *O que pode mudar:* Começar o mandato com inflação no teto e petróleo alto limita o ritmo de corte da Selic em 2027. ([fonte](https://static.poder360.com.br/uploads/2026/10/inpc_ipca_2026_set.pdf), [segunda fonte](https://bpmoney.com.br/?p=425837))
- **Selic e expectativas.** Em 16/set/2026 o Copom cortou a Selic de 14% para 13,75% (unânime), com Focus em 4,9% (2026) e 4,3% (2027); a IFI projeta Selic de 14,0% no fim de 2026 e 12,0% no fim de 2027, com juro real ex ante caindo de 7,5% para 5,4%. *O que pode mudar:* Mesmo com cortes, o juro real fica perto de 5% em 2027: é o principal custo da dívida no mandato. A IFI escreve 14,0% para o fim de 2026 apesar da Selic já em 13,75% em setembro (provável premissa anterior ao corte). ([fonte](https://atlaspublico.com.br/bcb/noticias/copom-reduz-selic-para-13-75pct-ao-ano-em-decisao-unanime-87748), [segunda fonte](https://www12.senado.leg.br/ifi/pdf/raf116_set2026.pdf))
- **Margem Equatorial / Petrobras.** A Petrobras achou hidrocarbonetos no poço Morpho (bloco FZA-M-59, a 175 km do Amapá, lâmina d'água de 2.886 m) em agosto de 2026 e anunciou nova descoberta no mesmo poço em 2/out; volume, viabilidade comercial e cronograma ainda não foram divulgados. *O que pode mudar:* Receita de royalties da Margem Equatorial dentro do mandato 2027 a 2030 é improvável: não há volume declarado e o prazo típico entre descoberta e produção em águas ultraprofundas é longo. ([fonte](https://www.seudinheiro.com/2026/bolsa-dolar/mais-petroleo-na-margem-equatorial-petrobras-petr4-anuncia-nova-descoberta-e-confirma-boa-qualidade-do-oleo-encontrado-em-agosto/), [segunda fonte](https://www.jb.com.br/economia/2026/08/1060596-petrobras-encontra-hidrocarbonetos-em-poco-no-amapa.html))
- **Emendas parlamentares.** O PLOA 2027 reserva R$ 44,8 bi para emendas individuais e de bancada (impositivas), R$ 4 bi a mais que os R$ 40,8 bi do projeto de 2026; emendas de comissão têm teto de R$ 12,9 bi; o Congresso aprovou R$ 53 bi em 2025 e R$ 61 bi em 2026. *O que pode mudar:* Com um Congresso mais à direita a partir de 2027, a disputa por emendas tende a subir o valor aprovado acima do projeto, como em 2025 e 2026. ([fonte](https://www.acessa.com/economia/2026/08/338425-orcamento-de-2027-reserva-rs-448-bilhoes-para-emendas-impositivas.html), [segunda fonte](https://sbtnews.sbt.com.br/noticia/politica/governo-guarda-r-44-8-bi-para-emendas-parlamentares-em-2027))
- **Dívida bruta e composição.** A dívida bruta do governo geral chegou a 82,5% do PIB em julho de 2026; os títulos atrelados à Selic subiram de 35,7% (dez/2023) para 46,4% (jul/2026) da Dívida Pública Federal. *O que pode mudar:* Quase metade da dívida reage na hora à Selic: cada ponto de juro vira custo fiscal rápido. A segunda fonte é o mesmo relatório. ([fonte](https://www12.senado.leg.br/ifi/pdf/raf116_set2026.pdf), [segunda fonte](https://www12.senado.leg.br/ifi/pdf/raf116_set2026.pdf))
- **Juro real longo e esforço para estabilizar a dívida.** O juro real de longo prazo foi de cerca de 5% (2018) para 8,3% em setembro de 2026 (IFI); o UBS calcula superávit primário estabilizador de 2,2% a 4,0% do PIB, cerca de 3,4% com juros nominais de 12%. *O que pode mudar:* É a conta central do mandato: o PLOA prevê superávit de 0,13% do PIB e a dívida só para de subir com algo perto de 3% do PIB. ([fonte](https://www12.senado.leg.br/ifi/pdf/raf116_set2026.pdf), [segunda fonte](https://www.infomoney.com.br/economia/esforco-fiscal-para-estabilizar-divida-pode-chegar-a-4-do-pib-diz-ubs/))
- **PLOA 2027 x IFI.** O PLOA 2027 prevê superávit primário de R$ 18,6 bi; a IFI projeta déficit de R$ 86,1 bi (diferença de R$ 104,8 bi), com PIB de 2,5% no PLOA contra 1,8% na IFI e 1,5% no Focus, e aponta contingenciamento necessário de R$ 35,7 bi. *O que pode mudar:* O primeiro ano do novo mandato começa com risco de contingenciamento ou de mudança de meta; a credibilidade da meta de 2027 é o primeiro teste. ([fonte](https://www12.senado.leg.br/ifi/pdf/raf116_set2026.pdf), [segunda fonte](https://www.canalrural.com.br/economia/ploa-de-2027-preve-superavit-primario-de-r-186-bilhoes/))

## 10. Como se conferiu

- Validação por um segundo caminho: **12 de 12** itens passaram (`resultados/VALIDACAO.json`).
- Achados de terceiros: 238 levantados, **212** com o trecho encontrado por script no texto capturado, 88 deles com a segunda fonte também conferida.
- Revisão adversarial por três leitores independentes: [`docs/REVISAO_ADVERSARIAL.md`](docs/REVISAO_ADVERSARIAL.md). Leitura da IA: [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md). Como refazer: [`docs/REPLICAR.md`](docs/REPLICAR.md).

## 11. As duas premissas (emenda 5)

### P1: o mercado tem razão

- **A versão mais forte:** o resultado mantém um governo que expande gasto sem receita nova, o juro longo sobe e fica, e a dívida, que já subia, sobe mais depressa; a queda do dia antecipa isso.
- **O que se esperaria ver:** o juro longo e o dólar sem voltar nas semanas seguintes, o Copom parando os cortes, as metas fiscais de 2027 e 2028 revistas para baixo.
- **O que o dado mostra:** com o macro do Focus (Selic mais alta e PIB menor que os da IFI), a dívida vai a 108,5% em 2030; com os juros de 2026 já acima da base, 111,3%; se o limite de gasto não segurar os R$ 51,3 bi por ano que a base não tem, 106,8%; as três juntas, 116,0%.
- **O que a derrubaria:** um pacote de ajuste crível antes do Orçamento de 2027 e o juro longo voltando ao nível de antes da eleição.

### P2: o mercado exagerou

- **A versão mais forte:** a queda é a desmontagem de uma aposta no outro resultado; a economia real (emprego, renda) vai bem e o mercado costuma errar a dívida para pior.
- **O que se esperaria ver:** a bolsa e o dólar recuperando parte da perda em semanas, o juro longo voltando ao nível de junho, o governo cumprindo a meta de 2027.
- **O que o dado mostra:** o mercado de previsão dava 34,5% de chance a Lula na véspera, então parte da queda é aposta desfeita; contra a curva de junho, que a base da IFI usa, o prêmio é de 0,36 ponto e a dívida vai a 96,6% em 2030; sem prêmio nenhum, 95,7%; com as metas do próprio governo cumpridas, 88,0% sem prêmio e 97,5% com ele; e o mercado previu a dívida maior do que aconteceu em 5 das 6 eleições desde 2002.
- **O que a derrubaria:** o juro longo ficando acima do de junho, a meta de 2027 descumprida ou mudada, o limite de gasto alterado em 2028 sem compensação.

**Qual o dado sustenta mais.** Em nenhuma das 17 contas a dívida para de subir: em 2030 ela fica entre 88,0% e 116,6% do PIB, contra 82,5% em 2026. Nisso o dado sustenta a P1: o problema das contas é real e vem de antes da eleição. Onde a P2 tem razão é no tamanho do susto do dia: parte da queda é aposta desfeita, e o mercado já errou a dívida para pior. O que decide entre as duas daqui para a frente é se o governo cumpre a meta de 2027 e o que faz com o limite de gasto em 2028.
