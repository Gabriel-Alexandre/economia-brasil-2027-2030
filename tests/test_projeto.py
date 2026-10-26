"""Testes do método: a conta da dívida, as réguas e a leitura das séries."""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from economia import contas, fiscal, mercado  # noqa: E402


def base_ifi():
    ifi = json.loads((RAIZ / "dados" / "derivados" / "ifi_raf113.json").read_text(encoding="utf-8"))["base"]
    conv = lambda d: {int(a): v for a, v in d.items() if 2025 <= int(a) <= 2030}  # noqa: E731
    return {"divida": conv(ifi["divida_bruta"]), "pib_nominal": conv(ifi["pib_nominal"]), "primario": conv(ifi["primario_sp"])}


def test_sem_premio_reproduz_a_ifi():
    b = base_ifi()
    d = fiscal.trajetoria(b)
    assert all(abs(d[a] - b["divida"][a]) < 1e-9 for a in b["divida"])


def test_premio_aumenta_a_divida_e_repasse_total_aumenta_mais():
    b = base_ifi()
    g = fiscal.trajetoria(b, premio_pp=2)[2030]
    t = fiscal.trajetoria(b, premio_pp=2, repasse=fiscal.REPASSE_TOTAL)[2030]
    assert b["divida"][2030] < g < t


def test_primario_estabilizador():
    # com juro igual ao crescimento, qualquer dívida fica parada sem superávit
    assert abs(fiscal.primario_estabilizador(90, 0.06, 0.06)) < 1e-12
    assert fiscal.primario_estabilizador(90, 0.09, 0.06) > 0


def test_reguas():
    assert fiscal.regua_trajetoria(1.9) == "estabiliza"
    assert fiscal.regua_trajetoria(8) == "sobe devagar"
    assert fiscal.regua_trajetoria(8.1) == "sobe rápido"
    assert mercado.regua_a1(-5) == "confirmada"
    assert mercado.regua_a1(-3) == "confirmada em parte"
    assert mercado.regua_a1(-1) == "não confirmada"
    assert mercado.regua_a1(0.5) == "o dado diz o contrário"
    assert contas.regua_a5(5) == "confirmada"
    assert contas.regua_a7(12, 11, 13.75, [13.25, 12, 10.5]) == "o dado diz o contrário"
    assert contas.regua_a7(12, None, 13.75, [13.25, 12, 10.5]).startswith("pendente")
    assert contas.regua_a7(14, 11, 13.75, [13.25, 14]) == "confirmada em parte"
    assert contas.regua_a7(14, 14.5, 13.75, [13.25, 14]) == "confirmada"


def test_eleicoes_conhecidas_batem_com_a_imprensa():
    h = {l["ano"]: l for l in mercado.historico()}
    assert round(h[2014]["ibovespa_dia_pct"], 2) == -2.77
    assert round(h[2022]["ibovespa_dia_pct"], 2) == 1.31
