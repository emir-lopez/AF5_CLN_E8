import pytest

from src.domain import CalculadoraReembolso


def test_reembolso_mas_de_24_horas():
    monto = 200.0
    reembolso = CalculadoraReembolso.calcular(monto, horas_anticipacion=48.0)
    assert reembolso == 200.0


@pytest.mark.parametrize("horas", [24.0, 12.0, 6.0])
def test_reembolso_entre_6_y_24_horas(horas):
    monto = 200.0
    reembolso = CalculadoraReembolso.calcular(monto, horas_anticipacion=horas)
    assert reembolso == 100.0


def test_reembolso_menos_de_6_horas():
    monto = 200.0
    reembolso = CalculadoraReembolso.calcular(monto, horas_anticipacion=5.9)
    assert reembolso == 0.0


# 4. Caso de Error: montos u horas negativas (valores inválidos)
@pytest.mark.parametrize("monto, horas", [(200.0, -5.0), (-200.0, 48.0)])
def test_reembolso_error(monto, horas):
    with pytest.raises(ValueError, match="no pueden ser negativos"):
        CalculadoraReembolso.calcular(monto, horas_anticipacion=horas)