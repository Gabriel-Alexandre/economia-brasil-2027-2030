# CLAUDE.md: como operar neste repositório

Projeto aberto de dados do vídeo longo 18 de Gabriel Alexandre: o que esperar da economia do Brasil de 2027 a 2030 depois da eleição de 2026. **Comece pelo `ESTADO.md`.** A doutrina está em `.cursor/rules/economia-fundamentos.mdc` (leia à mão: o Claude Code não carrega `.cursor/rules` sozinho).

1. **O pré-registro manda** (`docs/PRE_REGISTRO.md`). Regra nova só por emenda na §12, datada, dizendo o que já tinha sido visto.
2. **Nenhum número à mão.** Série entra por `ferramentas/coletar.py` (com hash); página de terceiros por `ferramentas/importar-achados.py` e só vale se `ferramentas/conferir-trechos.py` achar o trecho; o relatório sai de `ferramentas/gerar-relatorio.py`.
3. **Não é recomendação de investimento**, não julga intenção, não diz se o governo é bom ou ruim.
4. Texto público em português, sem travessão, conferido por `ferramentas/conferir-linguagem.py`. Código e nomes no padrão português dos projetos de eleição do autor.
5. O roteiro do vídeo mora no repositório de documentação do autor (`referencias-conteudo/roteiros/videos-longos/VIDEO_018_...`), não aqui.
