# O que esperar da economia do Brasil de 2027 a 2030

Projeto aberto de dados: o que o resultado da eleição de 2026 muda na economia do Brasil, com mercado, contas públicas, juros, dívida, as medidas de 2025 e 2026 e as promessas do 2º mandato, e de onde vem o dinheiro de cada uma.

**Comece por:** [`RESUMO_SIMPLES.md`](RESUMO_SIMPLES.md) (o resultado em uma página) · [`RELATORIO.md`](RELATORIO.md) (completo) · [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md) (a opinião da IA, separada dos números) · [`docs/REVISAO_ADVERSARIAL.md`](docs/REVISAO_ADVERSARIAL.md) · [`resultados/figuras/`](resultados/figuras/).

**Como foi feito:** as regras de todas as contas foram escritas e publicadas antes de qualquer número e antes da abertura da bolsa no dia seguinte à eleição ([`docs/PRE_REGISTRO.md`](docs/PRE_REGISTRO.md), commit `0e7620d`); o que mudou depois está nas emendas, cada uma dizendo o que já tinha sido visto. Toda série tem hash em `dados/MANIFESTO.json`; toda página de terceiros tem o texto capturado e o trecho conferido por script; o relatório é escrito por script a partir de `resultados/RESUMO.json`. Para refazer: [`docs/REPLICAR.md`](docs/REPLICAR.md). O que ainda depende do mercado: [`ESTADO.md`](ESTADO.md).

Análise feita pelo Claude (IA da Anthropic), a pedido de Gabriel Alexandre. **Não é recomendação de investimento.**
