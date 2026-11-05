from dataclasses import dataclass


class CustomerHasDebt(Exception):
    pass


@dataclass
class Order:
    total: float
    vip: bool = False
    status: str = "NEW"
    discount: float = 0.0

    def confirm(self, customer_debt=0):
        if self.total <= 0:
            raise ValueError("total must be positive")
        if customer_debt > 0:
            raise CustomerHasDebt("outstanding debt")
        self.discount = round(self.total * 0.15, 2) if self.vip else 0.0
        self.status = "CONFIRMED"
        return self.total - self.discount


class CalculadoraReembolso:
    """
    Domain Service para calcular el reembolso de una sesión cancelada (Regla R-06).
    Basado en el hallazgo H-05 del informe de arquitectura.
    """
    @staticmethod
    def calcular(monto_pagado: float, horas_anticipacion: float) -> float:
        if horas_anticipacion > 24.0:
            return monto_pagado  # 100% de reembolso
        elif 6.0 <= horas_anticipacion <= 24.0:
            return monto_pagado * 0.50  # 50% de reembolso
        else:
            return 0.0  # 0% de reembolso con menos de 6 horas