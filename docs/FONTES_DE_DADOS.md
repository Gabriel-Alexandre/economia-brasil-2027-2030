# Fontes de dados

Toda série numérica entra por `ferramentas/coletar.py` e fica registrada em `dados/MANIFESTO.json` (endereço, hora, tamanho e sha256). Toda página de terceiros entra por `ferramentas/capturar.py` (ou `importar-achados.py`), com o texto extraído em `dados/capturas/` e a linha em `dados/MANIFESTO_CAPTURAS.csv`; o arquivo bruto (HTML ou PDF) fica fora do git, em `dados/brutos/`.

| Fonte | O que entra | Como |
|---|---|---|
| Banco Central, SGS | Selic meta (432), dívida bruta do governo geral (13762), dívida líquida do setor público (4513), resultado primário em 12 meses (5793), juros nominais em 12 meses (5727), IPCA (433, 13522), desemprego (24369), dólar PTAX (1) | API `api.bcb.gov.br/dados/serie` |
| Banco Central, Focus | medianas anuais de IPCA, PIB, Selic, câmbio, primário, nominal, dívidas; inflação para 12 meses | API Olinda `ExpectativasMercadoAnuais` e `ExpectativasMercadoInflacao12Meses` |
| FMI | WEO de out/2026 (dívida bruta, nominal, PIB real) e Fiscal Monitor (despesa, primário, nominal, dívida) do Brasil, dos emergentes do G20, da América Latina e dos grupos | datamapper `imf.org/external/datamapper/api/v1` |
| IFI (Senado) | cenários de jun/2026 (RAF 113), a revisão de set/2026 (RAF 116) | PDF capturado; tabelas lidas por `ferramentas/derivar-ifi.py` |
| Tesouro e Planejamento | PLOA 2027 (Mensagem Presidencial), Relatório de Projeções Fiscais, Relatório Mensal da Dívida | PDF capturado |
| Yahoo Finance | Ibovespa, EWZ, EEM, dólar contra real, peso mexicano, chileno, colombiano, rand, título de 10 anos dos EUA | API de gráfico diário |
| Leis, MPs e imprensa | as medidas de 2025 e 2026, as promessas, os temas do M8, a história | `dados/evidencias/ACHADOS.csv`, trecho conferido por `ferramentas/conferir-trechos.py` |

**Conceitos de dívida.** O Banco Central e a IFI usam a dívida bruta do governo geral sem os títulos do Tesouro que estão na carteira do Banco Central. O FMI soma esses títulos, por isso o número dele é maior (97% do PIB em 2026 contra 82,5% da IFI). O projeto usa o conceito do Banco Central na conta e mostra o do FMI ao lado.

**Vídeos do YouTube** entram só para mapear argumentos (achados `Y*`): a página carrega por JavaScript e o script não confere trecho deles. Nenhum número do relatório vem de vídeo.
