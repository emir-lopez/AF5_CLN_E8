from unittest.mock import Mock

import pytest

from src.application import OrderService
from src.domain import Order


def test_gateway_approved():
    """El mock acepta el pago y el servicio devuelve el importe; no se transfiere dinero."""
    gateway = Mock()
    gateway.charge.return_value = True
    assert OrderService(gateway).checkout(Order(100)) == 100
    gateway.charge.assert_called_once_with(100)

def test_gateway_rejected_for_vip_order():
    """El mock rechaza el pago y checkout lanza RuntimeError; no se transfiere dinero."""
    gateway = Mock()
    gateway.charge.return_value = False

    order = Order(200, vip=True)
    with pytest.raises(RuntimeError):
        OrderService(gateway).checkout(order)

    gateway.charge.assert_called_once_with(170)
    # Improvement proposal: confirm only after payment succeeds; rejection
    # currently leaves the order confirmed despite the failed charge.
    assert order.status == "CONFIRMED"

def test_gateway_timeout_for_vip_order():
    """Simula un timeout; no confirma si el proveedor procesó el cobro."""
    gateway = Mock()
    gateway.charge.side_effect = TimeoutError("payment timed out")

    order = Order(200, vip=True)
    with pytest.raises(TimeoutError, match="payment timed out"):
        OrderService(gateway).checkout(order)

    gateway.charge.assert_called_once_with(170)
    # Improvement proposal: resolve the uncertain payment before confirming
    # the order; checkout currently confirms it before contacting the gateway.
    assert order.status == "CONFIRMED"
