import pytest

from src.domain import CustomerHasDebt, Order


# 1. Caso de Éxito: Cliente regular (No VIP) sin deuda
def test_order_regular_customer():
    order = Order(total=100.0)
    final_total = order.confirm(customer_debt=0)
    assert final_total == 100.0
    assert order.discount == 0.0
    assert order.status == "CONFIRMED"


# 2. Caso de Éxito: Cliente VIP sin deuda (Aplica descuento del 15%)
def test_order_vip_customer():
    order = Order(total=100.0, vip=True)
    final_total = order.confirm(customer_debt=0)
    assert final_total == 85.0
    assert order.discount == 15.0
    assert order.status == "CONFIRMED"


# 3. Caso Límite: Cliente VIP con decimales (Verifica el redondeo a 2 decimales)
def test_order_vip_rounding():
    order = Order(total=100.55, vip=True)
    # 100.55 * 0.15 = 15.0825 -> redondeado a 15.08
    final_total = order.confirm()
    assert order.discount == 15.08
    assert final_total == 100.55 - 15.08
    assert order.status == "CONFIRMED"


# 4. Caso de Error y Límite: Totales inválidos (0 o negativos)
@pytest.mark.parametrize("invalid_total", [0, -0.01, -50])
def test_order_invalid_total(invalid_total):
    order = Order(total=invalid_total)
    with pytest.raises(ValueError, match="total must be positive"):
        order.confirm()
    assert order.status == "NEW"  # El estado no debe cambiar


# 5. Caso de Error: Cliente con deuda pendiente
def test_order_with_customer_debt():
    order = Order(total=100.0)
    with pytest.raises(CustomerHasDebt, match="outstanding debt"):
        order.confirm(customer_debt=10.5)
    assert order.status == "NEW"


# 6. Caso Límite / Anomalía de Negocio: Deuda negativa
def test_order_negative_debt():
    order = Order(total=100.0)
    final_total = order.confirm(customer_debt=-5.0)
    assert final_total == 100.0
    assert order.status == "CONFIRMED"
