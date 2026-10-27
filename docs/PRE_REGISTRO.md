# Pré-registro: o que esperar da economia do Brasil de 2027 a 2030

**Escrito em 26/out/2026, às 07h30, antes de qualquer conta e antes da abertura da B3 (10h).** Este arquivo entra no primeiro commit do repositório. Tudo o que mudar depois entra na §12, com data e dizendo se veio antes ou depois de ver o número.

Análise feita pelo Claude (IA da Anthropic), a pedido de Gabriel Alexandre, para o vídeo longo 18 do canal dele.

---

## 1. A pergunta, nas palavras do pedido

> *"Baseado no resultado das eleições do Brasil, me fale o que esperar da economia para o próximo ano, para os próximos anos [...] esperando em que não aconteça nenhuma contestação de fraude [...] baseado no governo que a gente tem."*

O pedido traz afirmações que o projeto testa uma a uma, sem dar nenhuma por certa:

| Nº | Afirmação do pedido | Como é testada |
|---|---|---|
| A1 | *"a bolsa derreteu"* com a vitória de Lula | §4, M1 |
| A2 | *"vários investimentos que fortificavam a bolsa acabou fugindo do Brasil"* | §4, M2 |
| A3 | *"tiveram muitas medidas eleitoreiras do governo Lula"*: como vão ser pagas | §4, M5 |
| A4 | *"as coisas que o Lula prometeu, como vão ser pagas? De onde é que vai vir esse dinheiro"* | §4, M5 |
| A5 | *"a gastança do Brasil já está muito alta"* | §4, M3 |
| A6 | *"o juro já está muito alto"* | §4, M4 |
| A7 | *"e a tendência é apenas aumentar"* (o juro) | §4, M4 |

E a pergunta principal: **o que esperar da economia em 2027 e até 2030** (§4, M6), mais *"outras coisas importantes de ser analisadas"* (§4, M8).

## 2. O que já foi visto antes de escrever este arquivo

Declarado para que ninguém pense que uma regra foi feita sob medida para um número já conhecido.

- **Resultado do 2º turno (25/out):** Lula 51,78% e Flávio Bolsonaro 48,22% dos votos válidos, pela imprensa que cita a totalização do TSE (InfoMoney, Spacemoney, Mixvale). A conferência no arquivo do TSE entra na coleta.
- **Último pregão antes da eleição (sexta, 23/out):** Ibovespa fechou em 205.082,56 pontos (alta de 0,47%, pela InfoMoney e pelo Yahoo Finance); dólar perto de R$ 4,99.
- **O que os analistas esperavam para segunda, 26/out, antes da abertura:** queda forte da bolsa e alta do dólar e dos juros futuros (InfoMoney fala em risco de circuit breaker; a Oby Capital, citada pela InfoMoney, em queda de 6% a 10% da bolsa e dólar de R$ 5,50 a R$ 5,70; o economista Bruno Perri, no BPMoney, em dólar acima de R$ 5,20 e bolsa abaixo de 180 mil pontos). **Nada disso é dado realizado.** Na hora deste arquivo a B3 não tinha aberto.
- **Banco Central (SGS), olhado só para saber se as séries existem:** meta da Selic em 13,75% ao ano; resultado primário do setor público em 12 meses até ago/2026 com déficit de 0,62% do PIB (série 5793); juros nominais de 9,48% do PIB em 12 meses (série 5727); dívida líquida de 69,27% do PIB em ago/2026 (série 4513).
- **Projeto anterior do mesmo autor** (`simulacao-governos-eleicoes-2026`, público): simulação da dívida até 2030 sobre o cenário base da IFI de jun/2026 (dívida bruta de 95,7% do PIB em 2030) e um prêmio de juros de 2,05 pontos ao ano estimado pela reação do DI a uma pesquisa de mercado de previsão em 15/out. Os números de lá entram aqui só como cópia com hash, e a estimativa do prêmio é refeita com o dado da eleição (M1).

## 3. As saídas

1. **Um veredito para cada afirmação A1 a A7**, na régua de quatro níveis: **confirmada**, **confirmada em parte**, **não confirmada**, **o dado diz o contrário**. Sem "não dá para concluir": quando o dado ainda não saiu (ex.: o fluxo estrangeiro do dia 26/out sai na B3 com dois dias de atraso), o veredito se dá com o dado que existe e diz o que falta.
2. **O cenário central de 2027 a 2030**, com número: crescimento do PIB, inflação, Selic, resultado primário, dívida bruta do governo geral. Uma frase de classificação da trajetória da dívida (régua no M6).
3. **A tabela das medidas de 2025 e 2026 e das promessas do 2º mandato**: custo por ano, quem paga e de onde vem o dinheiro (categorias do M5).
4. **Os gatilhos**: o que, se acontecer, tira a economia do cenário central, para cima ou para baixo, com o tamanho de cada um.
5. **O que a IA acha** (`docs/LEITURA_DA_IA.md`), separado dos números.

## 4. Os métodos

### M1. A reação do mercado (A1)

**Estudo de evento.** Janela do dia: fechamento de **sexta, 23/out** contra o fechamento de **segunda, 26/out**. Janela da semana: 23/out contra **sexta, 30/out**, atualizada quando sair (até lá o relatório diz que é parcial).

**Ativos do Brasil:** Ibovespa; EWZ (o fundo de ações brasileiras negociado em Nova York); dólar contra o real; juros longos (taxa do Tesouro Prefixado e do Tesouro IPCA+ de prazo mais longo do Tesouro Direto e, se a B3 publicar, o DI futuro de janeiro de 2029 e de 2033); CDS de 5 anos, se houver fonte com dois registros.

**Controle:** o que os outros emergentes fizeram no mesmo dia. Bolsa: o EEM (fundo de ações de emergentes). Moeda: a média simples da variação do peso mexicano, do peso chileno, do peso colombiano e do rand sul-africano contra o dólar. **Excesso = variação do Brasil menos a do controle.** É o excesso que se atribui à eleição.

**Régua de A1 ("a bolsa derreteu"):** queda do Ibovespa no dia de **5% ou mais** = confirmada; de **2% a 5%** = confirmada em parte; **menos de 2%** = não confirmada; **alta** = o dado diz o contrário. A mesma régua vale para o excesso contra o EEM, e os dois vão publicados.

**Comparação com o passado:** a variação do Ibovespa e do dólar no primeiro pregão depois do 2º turno (ou do 1º, quando não houve 2º) em 2002, 2006, 2010, 2014, 2018 e 2022.

**Prêmio de juros de um governo contra o outro:** antes da eleição o mercado já dava uma chance para cada lado, então a reação de 26/out mede só a surpresa. Se a chance de Lula na véspera era *p*, a diferença inteira entre os dois resultados é **Δ excesso ÷ (1 − p)**. *p* sai de um mercado de previsão (Polymarket) no último registro antes do fim da votação, com segunda fonte; sem isso, *p* = a média das pesquisas registradas no TSE convertida em chance pela regra do projeto `previsao-segundo-turno-2026` (cópia com hash). Este prêmio é o que entra no M6.

### M2. O dinheiro estrangeiro (A2)

**Duas medidas, nas duas pontas:** (1) o saldo do investidor estrangeiro no mercado de ações da B3 (compras menos vendas), por mês em 2026 e no acumulado do ano até o último dado; (2) o investimento estrangeiro em carteira no balanço de pagamentos do Banco Central (ações e renda fixa), por mês. Dado de terceiros (B3 citada pela imprensa) só entra com duas fontes que batem.

**Régua de A2:** **confirmada** se o saldo acumulado de 2026 e o de outubro estiverem negativos; **em parte** se só um dos dois; **não confirmada** se os dois positivos; o dia 26/out entra quando a B3 publicar.

### M3. O tamanho do gasto (A5)

**Três réguas, todas com dado público:**
1. **Gasto total do governo geral em % do PIB**, Brasil contra a mediana dos emergentes e da América Latina (FMI, *World Economic Outlook* mais recente, indicador `GGX_NGDP`). **Confirmada** se o Brasil estiver 5 pontos do PIB ou mais acima da mediana dos emergentes; **em parte** de 0 a 5; **não confirmada** abaixo.
2. **Crescimento real da despesa primária do governo central** de 2023 a 2026 contra o de 2015 a 2022 (Tesouro Nacional, Resultado do Tesouro).
3. **Déficit nominal** (primário mais juros) em % do PIB, contra os emergentes (FMI `GGXCNL_NGDP`).

O veredito de A5 é o da régua 1; as outras duas explicam de onde vem o número. O juro da dívida é separado do gasto com serviços e benefícios em toda tabela, porque são coisas diferentes.

### M4. O juro (A6 e A7)

- **A6 ("muito alto"):** juro real (Selic meta menos a inflação esperada para 12 meses no Boletim Focus) e a posição do Brasil no ranking de juro real entre as maiores economias (duas fontes). **Confirmada** se o Brasil estiver entre os três maiores juros reais; **em parte** entre o 4º e o 10º; **não confirmada** abaixo.
- **A7 ("tende apenas a aumentar"):** o que o Focus (mediana) e a curva de juros do mercado esperam para a Selic no fim de 2026, 2027 e 2028, antes e depois da eleição. **Confirmada** se as duas apontarem Selic maior que a atual no fim de 2027; **em parte** se só uma; **não confirmada** se as duas apontarem menor; **o dado diz o contrário** se as duas apontarem queda em todos os anos.
- **O que liga o juro às contas:** quanto cada ponto de Selic custa por ano em juros da dívida (pela fatia da dívida que acompanha a Selic, Tesouro, Relatório Mensal da Dívida).

### M5. Medidas de 2025 e 2026 e promessas (A3 e A4)

**Critério de inclusão das medidas:** medida federal anunciada, editada ou sancionada de **01/jan/2025 a 25/out/2026** que aumenta renda, reduz preço ou imposto, ou dá crédito com subsídio às famílias, com estimativa de custo publicada por órgão oficial (lei, medida provisória e exposição de motivos, PLOA, Tesouro, Receita) e uma segunda fonte (IFI, TCU ou imprensa). O projeto **não julga intenção**: a palavra *eleitoreira* só aparece como citação do pedido; a tabela traz a **data** de cada medida e a distância até a eleição, e o leitor tira a conclusão.

**Quem paga, em cinco categorias:**

| Cat. | Como é paga |
|---|---|
| **A** | compensação na própria lei (imposto novo ou maior para outra pessoa ou setor) |
| **B** | dentro do limite de gasto do arcabouço (tira de outra despesa) |
| **C** | fora da meta ou do limite (excepcionalizada por lei ou emenda) |
| **D** | fora do orçamento (fundo, estatal, banco público, tarifa de energia, crédito) |
| **E** | sem fonte declarada |

Para A, o projeto também diz se a compensação estimada pelo governo é contestada por órgão independente (IFI ou TCU), com o número dos dois.

**Promessas do 2º mandato:** o plano de governo registrado no TSE e as promessas feitas nos debates de 18/out (Band) e 23/out (Globo), já levantadas no projeto `analise-debates-eleicoes-2026` (cópia com hash). Para cada uma: custo publicado (oficial ou independente) ou "sem custo publicado"; fonte declarada ou não. **Só as promessas com custo de duas fontes entram na conta do M6** (cenário S2).

**Veredito de A3 e A4:** a fatia do custo anual em cada categoria. A pergunta "como vão ser pagas" se responde com essa fatia, em reais e em % do PIB.

### M6. 2027 a 2030 (a pergunta principal)

**Base fiscal:** o cenário base do Relatório de Acompanhamento Fiscal (RAF) mais recente da Instituição Fiscal Independente (IFI, Senado). **Segunda base:** a projeção do FMI (WEO mais recente) para a dívida bruta. **Macro:** a mediana do Focus mais recente para PIB, IPCA, Selic e câmbio.

**A conta da dívida:** `d_t = d_(t-1) × (1 + i_t) ÷ (1 + g_t) − s_t` (d = dívida bruta em % do PIB, i = juro nominal médio da dívida, g = crescimento nominal do PIB, s = resultado primário em % do PIB). Calibrada para reproduzir a base da IFI; o juro implícito sai da própria base.

**Cenários:**

| | O que é | Como entra |
|---|---|---|
| **S0** | base da IFI | como publicada |
| **S1 (central)** | S0 mais o prêmio de juros medido no M1 | repasse gradual para o juro médio da dívida: 45% em 2027, 65% em 2028, 80% em 2029 e 90% em 2030 (hipótese declarada, a mesma do projeto do vídeo 13, porque a dívida é rolada aos poucos) |
| **S2 (risco)** | S1 mais as promessas com custo e sem fonte (M5) | custo em % do PIB a partir de 2027, piorando o primário |
| **S3 (ajuste)** | o primário que **estabiliza** a dívida em 2030 | `s* = d × (i − g) ÷ (1 + g)` |

**Por que S1 é o central:** a base da IFI já supõe as regras e as despesas aprovadas; o prêmio é o que o próprio mercado cobrou no dia; as promessas sem fonte ainda dependem do Congresso eleito, então ficam no cenário de risco.

**Régua da trajetória (variação da dívida bruta de 2026 a 2030 no S1):** **menos de 2 pontos** = estabiliza; **de 2 a 8 pontos** = sobe devagar; **mais de 8 pontos** = sobe rápido.

**Sensibilidade:** prêmio pela metade e em dobro; repasse total imediato; PIB 1 ponto abaixo e acima; e a projeção do FMI no lugar da IFI.

### M7. Teste do passado

1. **A reação do dia diz o que vem depois?** Para 2002, 2006, 2010, 2014, 2018 e 2022: o sinal da variação do Ibovespa e do dólar no primeiro pregão depois da eleição contra o que aconteceu no mandato seguinte (PIB médio, dívida, Ibovespa real). Publicado mesmo que a resposta seja "não diz nada".
2. **A previsão de dívida costuma acertar?** A previsão do Focus para a dívida líquida feita no outubro de cada ano de eleição, para o fim do 3º ano seguinte, contra o que aconteceu. O erro médio vira a faixa do número central do M6.

### M8. Outras coisas importantes

Lista fechada na pesquisa, cada uma com duas fontes e uma linha sobre o que muda para 2027 a 2030, sem nota: reforma tributária (transição de 2026 a 2033); tarifas dos Estados Unidos e comércio; China e preço das commodities; juros e dólar no mundo; o Congresso eleito para 2027 (do projeto `congresso-e-governos-eleicoes-2026`, cópia com hash); precatórios e o fim da exceção na meta; previdência, salário mínimo e envelhecimento; endividamento e inadimplência das famílias; emprego e produtividade; o que as agências de risco dizem da nota do Brasil.

## 5. Fontes

Banco Central (SGS, Focus pela API Olinda, Relatório de Política Monetária, Notas de política fiscal), Tesouro Nacional (Resultado do Tesouro, Relatório Mensal da Dívida, Tesouro Direto), IBGE (SIDRA), IFI/Senado (RAF), FMI (WEO), B3, TSE (resultado e plano de governo), legislação (Planalto), Yahoo Finance (cotações diárias, com segunda fonte para o dia do evento). Imprensa e relatórios de bancos entram como fonte de terceiros, com captura do texto, hash e segunda fonte. Vídeos do YouTube entram para mapear argumentos (quem diz o quê), nunca como fonte de número.

## 6. Validação

- Os números centrais refeitos por um segundo caminho, sem importar o módulo do projeto (`ferramentas/validacao-independente.py`): a dívida do S0 reproduzida contra a IFI, a variação do dia refeita com outra fonte de cotação, as séries do SGS baixadas de novo e comparadas.
- Todo trecho citado de página é procurado, por script, no texto capturado (`ferramentas/conferir-trechos.py`). Trecho não encontrado sai.

## 7. Revisão adversarial

Três leitores: (1) quem acha que o mercado exagera contra Lula e que o país está melhor do que a bolsa diz; (2) quem acha que as contas estão fora de controle e que o projeto está sendo brando; (3) o auditor de método e de linguagem. A objeção mais forte de cada lado vira variante calculada e publicada.

## 8. Linguagem

Sem "vai quebrar", "calote", "gastança" ou "derreteu" na voz do projeto (só entre aspas, como citação do pedido); sem julgar intenção de ninguém; sem chamar ninguém de mentiroso; sem travessão. **Nada aqui é recomendação de investimento.**

## 9. O que o projeto não faz

Não prevê preço de ação nem diz onde investir. Não diz se Lula é bom ou ruim. Não testa se houve fraude (o pedido supõe que não haja contestação). Não faz previsão para além de 2030.

## 10. Prazo eleitoral

A eleição acabou em 25/out. A leitura dos projetos anteriores para a Res. TSE nº 23.755/2026 vai de 72 horas antes a 24 horas depois do pleito. Este projeto analisa o governo eleito, não compara candidatos, e só deve ser publicado depois do fim dessa janela (`docs/LIMITE_ELEITORAL.md`).

## 11. Ordem de execução

Pré-registro (este commit) → coleta com hash → derivados → M1 a M8 → validação → revisão adversarial → teste do passado → relatório por script → gráficos → conferência de linguagem e testes.

## 12. Emendas

### Emenda 1 (26/out, 08h, operacional, antes de qualquer conta do M3)

O indicador `GGX_NGDP` do WEO não está no serviço de dados do FMI (datamapper). O gasto total do governo geral passa a vir do **Fiscal Monitor** (`G_X_G01_GDP_PT`, mesma definição, mesma base de out/2026), com o primário (`GGXONLB_G01_GDP_PT`) e o nominal (`GGXCNL_G01_GDP_PT`) da mesma publicação. O serviço também não lista quais países formam o grupo "emergentes e de renda média" do Fiscal Monitor (`FM_EMG`), então a **mediana dos emergentes** da régua 1 do M3 passa a ser a mediana dos **emergentes do G20** (Argentina, Brasil, China, Índia, Indonésia, México, Rússia, Arábia Saudita, África do Sul e Turquia, sem o Brasil na mediana), e a **média ponderada do grupo FM_EMG**, que o FMI publica pronta, vai ao lado. O limite de 5 pontos do PIB não muda. **O que já tinha sido visto ao escrever esta emenda:** o valor de 2026 do Brasil (48,7% do PIB), do FM_EMG (32,4%), do México e da Índia, impressos na conferência do download. Com qualquer das duas réguas, essa diferença já passa de 5 pontos; a emenda não muda o veredito, só diz de onde ele sai.

### Emenda 2 (26/out, antes das 10h, antes da abertura da B3, operacional)

O M1 definiu o controle de emergentes para a bolsa e para a moeda, mas não para o juro. Fica definido agora, antes de qualquer dado do dia: **o controle do juro longo é a variação do juro do título de 10 anos dos Estados Unidos** no mesmo intervalo (Yahoo Finance, `^TNX`), e o excesso do juro é a variação brasileira menos essa. **A série de juro longo do Brasil**, em ordem de preferência: (1) a taxa de ajuste do DI futuro de janeiro de 2033 publicada pela B3; (2) a taxa de ajuste do DI de janeiro de 2031; (3) a taxa do Tesouro Prefixado de prazo mais longo do Tesouro Direto; (4) duas matérias que publiquem a taxa de fechamento do mesmo vencimento. Vale a primeira disponível; as outras vão como conferência. O prêmio que entra no M6 é o excesso desse juro dividido por (1 − *p*), como no M1.

### Emenda 3 (26/out, manhã, antes de contar, régua que faltava)

O M5 diz o que medir em A3 e A4, mas não escreveu a régua de quatro níveis que o §3 pede para cada afirmação. Fica assim, igual para qualquer governo:

- **A3 (*"muitas medidas"* no ano da eleição):** **confirmada** se houver 5 medidas ou mais anunciadas, editadas ou sancionadas nos 12 meses antes da eleição (26/out/2025 a 25/out/2026) **e** mais da metade do custo recorrente delas não for compensada na própria lei (categorias B a E); **em parte** se só uma das duas; **não confirmada** se nenhuma. A intenção continua fora da conta.
- **A4 (*"de onde é que vai vir esse dinheiro"*):** conta-se a fatia das promessas econômicas do 2º mandato **sem custo publicado ou sem fonte do dinheiro declarada**. **Confirmada** (não se sabe de onde vem) se for mais da metade; **em parte** de um quarto à metade; **não confirmada** abaixo de um quarto.

**O que já foi visto:** a lista de medidas e de promessas com as datas, o custo e a categoria, que a pesquisa entregou antes desta emenda. As contagens ainda não foram feitas.

### Emenda 4 (26/out, antes das 10h, antes da abertura da B3, operacional)

A7 pede a Selic que **a curva** espera para o fim de 2027, sem dizer como lê-la. Fica definido: é a **taxa a termo de um ano entre os vértices de janeiro de 2028 e janeiro de 2029** da curva DI x pré da B3 (arquivo de taxas referenciais), no fechamento de 26/out. Essa taxa é o juro médio que o mercado cobra para 2028, que começa com a Selic do fim de 2027. Ela inclui um prêmio de prazo, então tende a ficar **acima** da Selic esperada; por isso, se mesmo ela ficar abaixo de 13,75%, a leitura de queda é forte, e se ficar acima, o relatório diz que parte é prêmio. A mesma conta no fechamento de 23/out vai ao lado, para mostrar o que a eleição mudou. **O que já tinha sido visto:** as taxas dos vértices de janeiro de 2027, 2029, 2031 e 2033 no fechamento de 23/out, trazidas pela pesquisa de mercado; nenhuma taxa de 26/out.

### Emenda 5 (26/out, manhã, antes do fechamento e antes da revisão adversarial voltar; regra do autor)

Regra do autor registrada hoje para todos os projetos dele: *"faça dos dois pontos de vista"*. O relatório ganha uma seção **"As duas premissas"**, cada uma tomada como verdadeira por vez: **P1, o mercado tem razão** (o resultado piora as contas e o juro, e a queda do dia antecipa isso) e **P2, o mercado exagerou** (a queda é a desmontagem de uma aposta, e a economia segue o caminho que já seguia). Para cada uma: a versão mais forte, o que se esperaria ver no dado, as implicações para 2027 a 2030 e o que a derrubaria. No fim, a seção diz qual das duas o dado sustenta mais, sem apagar a outra. A seção não muda nenhuma régua nem o cenário central; as objeções mais fortes da revisão adversarial entram nela como variantes calculadas.

### Emenda 6 (26/out, manhã, correções apontadas pela revisão adversarial de método)

**1. A emenda 3 foi escrita depois de um dado que ela não declarou.** O texto dela diz que *"as contagens ainda não foram feitas"*. Não é inteiramente verdade: o commit `f026935` (08h00), anterior à emenda (`086ddaf`, 08h05), já trazia em `resultados/RESUMO.json` o custo recorrente de todas as medidas por categoria (A: R$ 27,7 bi; B: R$ 83,0 bi; D: R$ 12,4 bi) e quantas promessas tinham custo publicado. O que não tinha sido feito era o recorte da janela de 12 meses e a contagem de A4 pela régua. Por isso as duas réguas da emenda 3 passam a valer **com este aviso**, e o relatório publica, ao lado de cada veredito, **a partir de quando ele mudaria**:
- A3 depende de como se lê a categoria B. Se o que cabe no limite de gasto contar como pago (porque sai de outra despesa), a fatia não compensada cai para perto de zero e A3 vira **"confirmada em parte"** (continua com 5 medidas ou mais na janela). Sem o salário mínimo, que segue uma regra anual, a fatia continua acima da metade.
- A4 muda de "confirmada" se três promessas a mais tiverem custo e fonte publicados. Sem o fim da escala 6x1, que já foi aprovado e não tem despesa pública, fica em 9 de 13.

**2. A régua de A7 olha 2026, 2027 e 2028.** O código passava a trajetória do Focus até 2030 e, com a Selic esperada igual em 2029 e 2030, o veredito saía "não confirmada" em vez de "o dado diz o contrário". Corrigido para os três anos do texto do M4. E o veredito de A7 **só sai com a curva de 26/out**, como o M4 manda; até lá, o relatório diz que está pendente.

**3. Horários.** As horas escritas nos títulos eram estimativas. Valem as dos commits: pré-registro às 07h16 (`0e7620d`), emenda 1 às 07h37, emenda 2 às 07h54, emenda 3 às 08h05, emenda 4 às 08h08, emenda 5 às 08h25. A B3 abriu às 10h; nenhuma regra de mercado foi escrita depois disso.

**4. A base é a IFI de junho (RAF 113), não a de setembro (RAF 116).** O RAF 116 é o mais recente, mas só revisou 2026 e 2027; a última projeção de médio prazo, que o M6 exige até 2030, é a do RAF 113. Declarado agora porque o M6 dizia "o mais recente".

**5. A tabela do cenário central.** A dívida do S1 é calculada com o PIB e a Selic da IFI; o M6 punha ao lado o macro do Focus, que é outro cenário. O relatório passa a mostrar as duas coisas em tabelas separadas, e o cenário com o macro do Focus vira variante calculada (revisão adversarial).

**6. O que o pré-registro prometeu e não foi entregue, dito aqui:** o investimento estrangeiro em carteira do balanço de pagamentos (M2, medida 2) e o crescimento real da despesa do governo central de 2023 a 2026 contra 2015 a 2022 (M3, régua 2), se a coleta não conseguir os arquivos; o relatório diz o que faltou. O M8 só mostra tema com duas fontes conferidas, como o M8 exige.

### Emenda 7 (26/out, manhã, antes de abrir a planilha do Tesouro; régua 2 do M3)

A série histórica do Resultado do Tesouro Nacional disponível vai até julho de 2026. A régua 2 do M3 fica assim: despesa total do governo central (linha "Despesa Total" da série mensal), cada mês corrigido pelo IPCA para reais de julho de 2026 e somado em 12 meses; **crescimento real médio por ano de 2023 a 2026** = do total de 2022 ao dos 12 meses até julho de 2026 (3 anos e 7 meses); **de 2015 a 2022** = do total de 2014 ao de 2022 (8 anos). A régua é só descritiva (o veredito de A5 é o da régua 1), e vai ao lado: a mesma conta para a despesa sem a Previdência e sem as transferências a estados e municípios, se a planilha tiver as linhas. **O que já foi visto:** só os nomes dos arquivos do conjunto de dados; nenhum valor.

### Emenda 8 (26/out, noite, depois do fechamento; o que entrou pela leitura dos projetos dos vídeos 16, 17 e 19)

A pedido do autor, o projeto leu o que foi levantado hoje nos projetos dos vídeos 16, 17 e 19 (`investigacao-segundo-turno-2026`, `geopolitica-eleicao-2026`, `pesquisas-e-resultado-segundo-turno-2026`). Entraram, sem mudar nenhuma régua: **duas medidas que a pesquisa da manhã não tinha achado e que cabem no critério do M5** (o perdão de dívidas dos MEIs, anunciado em 13/out, e a gasolina com tributos zerados por 30 dias, em 09/out), com captura e trecho conferido; **o que o Tesouro fez no dia** (cancelou os leilões de títulos prefixados e atrelados à inflação da semana); **a estimativa da IFI do tamanho do pacote de 2026** (R$ 298,4 bilhões, a soma que circulou como *"R$ 300 bilhões"*); e **os números de comércio do projeto do vídeo 17**, como contexto do M8. **O que já se sabia:** A3 já estava confirmada antes dessas duas medidas; com elas, a contagem e a fatia não compensada sobem, e o veredito não muda.

### Emenda 9 (26/out, 21h, antes de calcular; a curva da B3 de 26/out não saiu)

Até as 20h52 o arquivo de taxas referenciais da B3 de 26/out não tinha sido publicado (as tentativas de 19h54 a 20h45 devolveram 22 bytes). Vale então a 4ª opção da emenda 2: **a taxa de fechamento publicada pela imprensa para o mesmo vencimento.** O vencimento mais longo publicado é o **DI de janeiro de 2031**, que é a 2ª opção da emenda 2, e o valor de sexta que as matérias citam (12,642%) é idêntico ao da curva da B3 que o projeto baixou. As 4 matérias capturadas (CNN Brasil, InfoMoney, BPMoney e SpaceMoney) **reproduzem o mesmo texto da Reuters**; contam como 2 publicações conferidas, com a ressalva de que a apuração é uma só.

**A7 sem o vértice de 2029.** A emenda 4 pede a taxa a termo entre janeiro de 2028 e janeiro de 2029; nenhuma matéria publicou janeiro de 2029. Enquanto o arquivo da B3 não sai, a leitura da curva para A7 passa a ser **o DI de janeiro de 2028**: ele é o juro médio que o mercado cobra de hoje até o começo de 2028, e se ele ficar acima da Selic atual, o mercado cobra uma Selic acima da de hoje em algum momento até lá. Quando o arquivo da B3 de 26/out sair, a conta da emenda 4 roda de novo e substitui esta. **O que já tinha sido visto:** as taxas de fechamento de janeiro de 2028 (14,8%) e de janeiro de 2031 (15,185%), na matéria da CNN, antes de escrever esta emenda.


### Emenda 10 (26/out, 23h, a curva da B3 de 26/out saiu; registro, sem régua nova)

O arquivo de taxas referenciais da B3 de 26/out saiu à noite (334 KB, baixado às 23h20 e registrado no `dados/MANIFESTO.json`). Como a emenda 9 previa, a conta da emenda 4 rodou de novo e **substituiu a da imprensa**: o prêmio volta a ser medido no DI de janeiro de 2033 (1ª opção da emenda 2) e A7 volta a usar a taxa a termo entre janeiro de 2028 e janeiro de 2029. Nenhuma régua mudou. **A comparação, para quem quiser conferir que a troca não mexeu no resultado:** DI jan/2028 14,8% (imprensa) contra 14,822% (B3); DI jan/2031 15,185% contra 15,277%; prêmio 3,89 contra 3,91 pontos; dívida no cenário central em 2030, 105,41% contra 105,46% do PIB (o arredondamento de uma casa passa de 105,4 para 105,5); contra a curva de junho, prêmio 0,36 contra 0,49 ponto; A7 segue **em parte** (a termo de 2028 foi de 12,38% para 15,70%). **O que já tinha sido visto:** todo o resultado da noite, com a curva da imprensa, publicado em `fd2db33`.
