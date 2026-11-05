import pytest

from src.domain import CalculadoraReembolso


# 1. Caso de Éxito: Más de 24 horas (Reembolso del 100%)
def test_reembolso_mas_de_24_horas():
    monto = 200.0
    reembolso = CalculadoraReembolso.calcular(monto, horas_anticipacion=48.0)
    assert reembolso == 200.0


# 2. Caso de Éxito: Entre 6 y 24 horas (Reembolso del 50%)
@pytest.mark.parametrize("horas", [24.0, 12.0, 6.0])
def test_reembolso_entre_6_y_24_horas(horas):
    monto = 200.0
    reembolso = CalculadoraReembolso.calcular(monto, horas_anticipacion=horas)
    assert reembolso == 100.0


# 3. Caso de Éxito: Menos de 6 horas (Sin reembolso)
def test_reembolso_menos_de_6_horas():
    monto = 200.0
    reembolso = CalculadoraReembolso.calcular(monto, horas_anticipacion=5.9)
    assert reembolso == 0.0