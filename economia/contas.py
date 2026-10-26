"""M3 (o tamanho do gasto) e M4 (o juro), pelas réguas do pré-registro e da emenda 1."""
from __future__ import annotations

import datetime as dt
import json
import statistics

from . import series as S

G20_EMERGENTES_SEM_BRASIL = ["ARG", "CHN", "IND", "IDN", "MEX", "RUS", "SAU", "ZAF", "TUR"]
LATAM_SEM_BRASIL = ["ARG", "CHL", "COL", "MEX", "PER", "URY"]


def comparar(nome: str, ano: int) -> dict:
    v = S.imf(nome)
    g20 = {p: v[p][ano] for p in G20_EMERGENTES_SEM_BRASIL if ano in v.get(p, {})}
    lat = {p: v[p][ano] for p in LATAM_SEM_BRASIL if ano in v.get(p, {})}
    return {
        "ano": ano, "brasil": v["BRA"][ano],
        "mediana_g20_emergentes": statistics.median(g20.values()), "paises_g20": g20,
        "media_fm_emg": v.get("FM_EMG", {}).get(ano),
        "mediana_america_latina": statistics.median(lat.values()), "paises_latam": lat,
        "media_avancados": v.get("ADVEC", {}).get(ano),
    }


def regua_a5(diferenca_pp: float) -> str:
    if diferenca_pp >= 5:
        return "confirmada"
    if diferenca_pp >= 0:
        return "confirmada em parte"
    return "não confirmada"


def gasto() -> dict:
    desp = {a: comparar("imf-fm-despesa", a) for a in (2019, 2022, 2025, 2026)}
    nom = {a: comparar("imf-fm-nominal", a) for a in (2025, 2026)}
    prim = {a: comparar("imf-fm-primario", a) for a in (2025, 2026)}
    d25 = desp[2025]
    dif = d25["brasil"] - d25["mediana_g20_emergentes"]
    juros = {a: nom[a]["brasil"] - prim[a]["brasil"] for a in nom}   # nominal - primário = - juros
    return {
        "despesa_total": desp, "resultado_nominal": nom, "resultado_primario": prim,
        "juros_liquidos_fmi_pct_pib": {a: -v for a, v in juros.items()},
        "diferenca_2025_contra_mediana_g20_pp": dif,
        "diferenca_2025_contra_fm_emg_pp": d25["brasil"] - d25["media_fm_emg"],
        "veredito_a5": regua_a5(dif),
    }


def contas_hoje() -> dict:
    """Banco Central: primário, juros e dívida, no último mês e em dezembro de anos de referência."""
    out = {}
    for nome in ["bcb-primario-12m", "bcb-juros-nominais-12m", "bcb-divida-bruta-gg", "bcb-divida-liquida-sp"]:
        s = S.sgs(nome)
        ult = s.index[-1]
        out[nome] = {"ultimo": {"mes": ult.isoformat(), "valor": float(s.iloc[-1])},
                     **{f"dez_{a}": float(s[dt.date(a, 12, 1)]) for a in (2014, 2018, 2022, 2025) if dt.date(a, 12, 1) in s.index}}
    # NFSP: valor positivo = déficit. O nominal é a soma.
    p, j = out["bcb-primario-12m"]["ultimo"]["valor"], out["bcb-juros-nominais-12m"]["ultimo"]["valor"]
    out["deficit_nominal_12m_pct_pib"] = p + j
    return out


def juro_real() -> dict:
    hoje = dt.date.today()
    selic_dia, selic = S.valor_em(S.sgs("bcb-selic-meta"), hoje)
    f12 = json.loads((S.SERIES / "focus-ipca-12m.json").read_text(encoding="utf-8"))
    f12 = sorted([x for x in f12 if x.get("Suavizada") == "S" and x.get("baseCalculo") == 0], key=lambda x: x["Data"])
    ipca12 = f12[-1]
    real = 100 * ((1 + selic / 100) / (1 + ipca12["Mediana"] / 100) - 1)
    return {"selic_meta": selic, "selic_em": selic_dia.isoformat(), "ipca_esperado_12m": ipca12["Mediana"],
            "focus_data": ipca12["Data"], "juro_real_ex_ante_pct": real}


def regua_a7(focus_fim_2027: float, curva_fim_2027: float | None, selic_atual: float, focus_trajetoria: list[float]) -> str:
    """Pré-registro M4: maior que a atual no fim de 2027 nas duas = confirmada; só uma = em parte;
    menor nas duas = não confirmada; queda em todos os anos nas duas = o dado diz o contrário."""
    sobe = [focus_fim_2027 > selic_atual] + ([curva_fim_2027 > selic_atual] if curva_fim_2027 is not None else [])
    if all(sobe):
        return "confirmada"
    if any(sobe):
        return "confirmada em parte"
    caindo = all(b < a for a, b in zip([selic_atual] + focus_trajetoria, focus_trajetoria))
    if caindo and (curva_fim_2027 is None or curva_fim_2027 < selic_atual):
        return "o dado diz o contrário"
    return "não confirmada"
