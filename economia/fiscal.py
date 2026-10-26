"""M6: a conta da dívida, d_t = d_(t-1) (1 + i_t) / (1 + g_t) - s_t (pré-registro §4, M6).

d = dívida bruta em % do PIB, i = juro nominal médio implícito, g = crescimento do PIB nominal,
s = resultado primário em % do PIB (positivo = superávit). A conta se calibra na base: o juro
implícito de cada ano sai da própria base, e os cenários mexem só no que o pré-registro manda.
"""
from __future__ import annotations

REPASSE_GRADUAL = {2027: 0.45, 2028: 0.65, 2029: 0.80, 2030: 0.90}
REPASSE_TOTAL = {2027: 1.0, 2028: 1.0, 2029: 1.0, 2030: 1.0}


def juro_implicito(divida: dict[int, float], pib_nominal: dict[int, float], primario: dict[int, float]) -> dict[int, float]:
    """i_t que faz a equação reproduzir a base, ano a ano."""
    i = {}
    for t in sorted(divida):
        if t - 1 not in divida:
            continue
        g = pib_nominal[t] / pib_nominal[t - 1] - 1
        i[t] = (divida[t] + primario[t]) * (1 + g) / divida[t - 1] - 1
    return i


def trajetoria(base: dict, premio_pp: float = 0.0, repasse: dict[int, float] | None = None,
               piora_primario: dict[int, float] | None = None, choque_pib_pp: float = 0.0,
               ano_inicio: int = 2027) -> dict[int, float]:
    """Dívida ano a ano. base = {"divida", "pib_nominal", "primario"} com os mesmos anos.

    premio_pp: pontos ao ano a mais no juro de mercado, repassados ao juro médio pela tabela `repasse`.
    piora_primario: pontos do PIB a menos no primário, por ano (custo de promessas sem fonte).
    choque_pib_pp: pontos ao ano a mais (ou a menos) no crescimento nominal a partir de ano_inicio.
    """
    repasse = repasse if repasse is not None else REPASSE_GRADUAL
    piora_primario = piora_primario or {}
    div, pib, prim = base["divida"], base["pib_nominal"], base["primario"]
    i = juro_implicito(div, pib, prim)
    anos = sorted(i)
    d = {anos[0] - 1: div[anos[0] - 1]}
    for t in anos:
        g = pib[t] / pib[t - 1] - 1
        it = i[t]
        if t >= ano_inicio:
            it += repasse.get(t, 0.0) * premio_pp / 100
            g += choque_pib_pp / 100
        s = prim[t] - (piora_primario.get(t, 0.0) if t >= ano_inicio else 0.0)
        d[t] = d[t - 1] * (1 + it) / (1 + g) - s
    return d


def primario_estabilizador(d: float, i: float, g: float) -> float:
    """s* = d (i - g) / (1 + g): o primário (% do PIB) que mantém a dívida parada."""
    return d * (i - g) / (1 + g)


def regua_trajetoria(variacao_pp: float) -> str:
    """Pré-registro M6: menos de 2 pontos = estabiliza; 2 a 8 = sobe devagar; mais de 8 = sobe rápido."""
    if variacao_pp < 2:
        return "estabiliza"
    if variacao_pp <= 8:
        return "sobe devagar"
    return "sobe rápido"


def trajetoria_geral(base: dict, juro_extra_pp: dict[int, float] | None = None,
                     piora_primario: dict[int, float] | None = None,
                     choque_pib_pp: dict[int, float] | None = None) -> dict[int, float]:
    """Como trajetoria, mas com o acréscimo de juro, a piora do primário e o choque no PIB dados ano a ano.

    Serve às variantes da revisão adversarial (docs/REVISAO_ADVERSARIAL.md), que mexem em anos diferentes.
    Valores negativos em piora_primario são melhora (superávit maior que o da base).
    """
    juro_extra_pp, piora_primario, choque_pib_pp = juro_extra_pp or {}, piora_primario or {}, choque_pib_pp or {}
    div, pib, prim = base["divida"], base["pib_nominal"], base["primario"]
    i = juro_implicito(div, pib, prim)
    anos = sorted(i)
    d = {anos[0] - 1: div[anos[0] - 1]}
    for t in anos:
        g = pib[t] / pib[t - 1] - 1 + choque_pib_pp.get(t, 0.0) / 100
        it = i[t] + juro_extra_pp.get(t, 0.0) / 100
        d[t] = d[t - 1] * (1 + it) / (1 + g) - (prim[t] - piora_primario.get(t, 0.0))
    return d
