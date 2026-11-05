import pytest

from src.domain import CustomerHasDebt, Order, OrderAlreadyConfirmed


def test_vip_discount():
    o = Order(100, vip=True)
    assert o.confirm() == 85
    assert o.status == "CONFIRMED"

def test_regular_no_discount():
    assert Order(100).confirm() == 100

def test_customer_debt():
    with pytest.raises(CustomerHasDebt, match=r"deuda pendiente de \$50\.00"):
        Order(100).confirm(customer_debt=50)

@pytest.mark.parametrize("total", [0, -1])
def test_invalid_total(total):
    with pytest.raises(ValueError, match=r"debe ser mayor a \$0\.00"):
        Order(total).confirm()


# --- E2: pruebas agregadas (Integrante 1) ---
def test_vip_200_da_170():
    # Arrange
    o = Order(200, vip=True)
    # Act
    cobro = o.confirm()
    # Assert
    assert cobro == 170
    assert o.discount == 30
    assert o.status == "CONFIRMED"


def test_regular_200_da_200():
    # Arrange
    o = Order(200)
    # Act
    cobro = o.confirm()
    # Assert
    assert cobro == 200
    assert o.discount == 0
    assert o.status == "CONFIRMED"



# --- E3: TDD - regla nueva: no confirmar dos veces ---
def test_cannot_confirm_twice():
    order = Order(100)
    order.confirm()
    with pytest.raises(OrderAlreadyConfirmed, match="ya se encuentra confirmado"):
        order.confirm()
    assert order.status == "CONFIRMED"
