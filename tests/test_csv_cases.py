"""Prueba parametrizada que lee los casos del laboratorio desde CSV.

Los CSV no se cargan solos: aquí se leen con csv.DictReader, se une cada caso
(casos_de_prueba.csv) con su pedido (pedidos_prueba.csv) y se ejecuta la regla real.
"""

import csv
from pathlib import Path

import pytest

from src.domain import CustomerHasDebt, Order, OrderAlreadyConfirmed

DATA_DIR = Path(__file__).parent / "data"

EXCEPCIONES = {
    "ValueError": ValueError,
    "CustomerHasDebt": CustomerHasDebt,
    "OrderAlreadyConfirmed": OrderAlreadyConfirmed,
}


def leer_csv(nombre):
    # utf-8-sig: los CSV traen BOM (Excel) y sin esto la primera columna no se reconoce.
    with open(DATA_DIR / nombre, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def cargar_casos_confirmar():
    pedidos = {p["pedido_id"]: p for p in leer_csv("pedidos_prueba.csv")}
    casos = []
    for caso in leer_csv("casos_de_prueba.csv"):
        if caso["accion"] != "confirmar":
            continue  # CP13-CP15 son de mock y persistencia (Integrante 2)
        pedido = pedidos[caso["pedido_id"]]
        casos.append(pytest.param(pedido, caso["resultado_esperado"], id=caso["caso_id"]))
    return casos


CASOS = cargar_casos_confirmar()


def test_csv_tiene_los_12_casos_de_confirmacion():
    assert len(CASOS) == 12


@pytest.mark.parametrize("pedido, esperado", CASOS)
def test_caso_csv(pedido, esperado):
    # Arrange: construir el pedido con los datos del CSV
    order = Order(
        total=float(pedido["total"]),
        vip=pedido["es_vip"] == "1",
        status=pedido["estado_inicial"],
    )
    deuda = float(pedido["deuda_cliente"])

    # Act + Assert
    if esperado in EXCEPCIONES:
        with pytest.raises(EXCEPCIONES[esperado]):
            order.confirm(customer_debt=deuda)
    else:
        # formato esperado: "CONFIRMED, cobro 120.00"
        cobro_esperado = float(esperado.split("cobro")[1])
        cobro = order.confirm(customer_debt=deuda)
        assert cobro == pytest.approx(cobro_esperado)
        assert order.status == "CONFIRMED"
