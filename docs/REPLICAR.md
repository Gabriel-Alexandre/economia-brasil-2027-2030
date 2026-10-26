# Como refazer tudo

```bash
pip install -r requirements.txt
python ferramentas/coletar.py                 # séries (BCB, Focus, FMI, Yahoo)
python ferramentas/importar-achados.py <listas.json>   # páginas de terceiros, com hash
python ferramentas/conferir-trechos.py        # cada trecho procurado no texto capturado
python ferramentas/derivar-ifi.py             # tabelas da IFI lidas do PDF
python ferramentas/medidas.py                 # medidas e promessas
python ferramentas/mercado-do-dia.py          # M1 e M2 (depois do fechamento)
python ferramentas/analise.py                 # M3 a M7 -> resultados/RESUMO.json
python ferramentas/validacao-independente.py  # segundo caminho
python ferramentas/gerar-relatorio.py         # RELATORIO.md e RESUMO_SIMPLES.md
python ferramentas/graficos.py                # resultados/figuras/
python ferramentas/conferir-linguagem.py
python -m pytest -q
```

As séries mudam com o tempo (o Banco Central revisa a dívida; o Focus sai toda segunda). Para refazer exatamente este relatório, use os arquivos de `dados/series/` deste repositório, que têm o sha256 no `dados/MANIFESTO.json`.
