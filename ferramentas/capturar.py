"""Captura uma fonte (página, PDF ou série), guarda o bruto com sha256 e extrai o texto.

Uso:
    python ferramentas/capturar.py <id> <url> [--tipo html|pdf|json|csv] [--forcar]

O bruto vai para dados/brutos/ (fora do git quando é HTML ou PDF), o texto extraído
para dados/capturas/<id>.txt (no git) e a linha para dados/MANIFESTO_CAPTURAS.csv.
Nenhum número do projeto sai de página que não passou por aqui.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import re
import sys
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parents[1]
BRUTOS = RAIZ / "dados" / "brutos"
CAPTURAS = RAIZ / "dados" / "capturas"
MANIFESTO = RAIZ / "dados" / "MANIFESTO_CAPTURAS.csv"
CAMPOS = ["id", "url", "tipo", "capturado_em", "bytes", "sha256", "arquivo_bruto", "arquivo_texto"]
CABECALHOS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/129.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}


def texto_de_html(conteudo: bytes) -> str:
    from bs4 import BeautifulSoup

    m = re.search(rb"charset=[\"']?([A-Za-z0-9_-]+)", conteudo[:4000])
    cod = m.group(1).decode() if m else None
    if cod and cod.lower() in ("iso-8859-1", "latin-1", "latin1"):
        cod = "windows-1252"
    if cod is None:
        try:
            conteudo.decode("utf-8")
            cod = "utf-8"
        except UnicodeDecodeError:
            cod = "windows-1252"
    sopa = BeautifulSoup(conteudo, "lxml", from_encoding=cod)
    for marca in sopa(["script", "style", "noscript", "svg", "iframe"]):
        marca.decompose()
    texto = sopa.get_text("\n")
    linhas = [re.sub(r"[ \t\xa0]+", " ", l).strip() for l in texto.splitlines()]
    return "\n".join(l for l in linhas if l)


def texto_de_pdf(conteudo: bytes) -> str:
    import pdfplumber

    partes = []
    with pdfplumber.open(io.BytesIO(conteudo)) as pdf:
        for n, pagina in enumerate(pdf.pages, 1):
            partes.append(f"\n=== página {n} ===\n{pagina.extract_text() or ''}")
    return "\n".join(partes)


def ler_manifesto() -> list[dict]:
    if not MANIFESTO.exists():
        return []
    with MANIFESTO.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def gravar_manifesto(linhas: list[dict]) -> None:
    with MANIFESTO.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for l in sorted(linhas, key=lambda x: x["id"]):
            w.writerow(l)


def capturar(ident: str, url: str, tipo: str | None = None, forcar: bool = False) -> Path:
    linhas = ler_manifesto()
    if any(l["id"] == ident for l in linhas) and not forcar:
        print(f"{ident}: já capturado (use --forcar)")
        return CAPTURAS / f"{ident}.txt"
    resp = requests.get(url, headers=CABECALHOS, timeout=90)
    resp.raise_for_status()
    conteudo = resp.content
    if tipo is None:
        ctype = resp.headers.get("content-type", "")
        tipo = "pdf" if ("pdf" in ctype or url.lower().endswith(".pdf")) else (
            "json" if "json" in ctype else "html")
    ext = {"html": "html", "pdf": "pdf", "json": "json", "csv": "csv"}[tipo]
    BRUTOS.mkdir(parents=True, exist_ok=True)
    CAPTURAS.mkdir(parents=True, exist_ok=True)
    bruto = BRUTOS / f"{ident}.{ext}"
    bruto.write_bytes(conteudo)
    if tipo == "html":
        texto = texto_de_html(conteudo)
    elif tipo == "pdf":
        texto = texto_de_pdf(conteudo)
    else:
        texto = conteudo.decode("utf-8", errors="replace")
    alvo = CAPTURAS / f"{ident}.txt"
    alvo.write_text(f"# fonte: {url}\n# capturado em: {dt.date.today().isoformat()}\n\n{texto}", encoding="utf-8")
    linhas = [l for l in linhas if l["id"] != ident]
    linhas.append({
        "id": ident,
        "url": url,
        "tipo": tipo,
        "capturado_em": dt.date.today().isoformat(),
        "bytes": len(conteudo),
        "sha256": hashlib.sha256(conteudo).hexdigest(),
        "arquivo_bruto": bruto.relative_to(RAIZ).as_posix(),
        "arquivo_texto": alvo.relative_to(RAIZ).as_posix(),
    })
    gravar_manifesto(linhas)
    print(f"{ident}: {len(conteudo)} bytes, {len(texto)} caracteres de texto")
    return alvo


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("id")
    p.add_argument("url")
    p.add_argument("--tipo", choices=["html", "pdf", "json", "csv"])
    p.add_argument("--forcar", action="store_true")
    a = p.parse_args()
    try:
        capturar(a.id, a.url, a.tipo, a.forcar)
    except Exception as e:  # noqa: BLE001
        print(f"{a.id}: FALHOU ({e})", file=sys.stderr)
        sys.exit(1)
