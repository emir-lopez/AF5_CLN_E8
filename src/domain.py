from dataclasses import dataclass

class CustomerHasDebt(Exception):
    pass

class OrderAlreadyConfirmed(ValueError):
    """El pedido ya fue confirmado y no puede confirmarse otra vez."""

@dataclass
class Order:
    total: float
    vip: bool = False
    status: str = "NEW"
    discount: float = 0.0

    def confirm(self, customer_debt=0):
        self._ensure_not_confirmed()
        if self.total <= 0:
            raise ValueError(
                f"El total del pedido debe ser mayor a $0.00 (recibido: ${self.total:.2f}). "
                "Revisa el monto antes de confirmar."
            )
        if customer_debt > 0:
            raise CustomerHasDebt(
                f"El cliente tiene una deuda pendiente de ${customer_debt:.2f}. "
                "Debe liquidarla antes de confirmar el pedido."
            )
        self.discount = round(self.total * 0.15, 2) if self.vip else 0.0
        self.status = "CONFIRMED"
        return self.total - self.discount

    def _ensure_not_confirmed(self):
        if self.status == "CONFIRMED":
            raise OrderAlreadyConfirmed(
                f"El pedido por ${self.total:.2f} ya se encuentra confirmado "
                f"(estatus actual: {self.status}). No se puede confirmar dos veces."
            )

class CalculadoraReembolso:
    """
    Domain Service para calcular el reembolso de una sesión cancelada (Regla R-06).
    Basado en el hallazgo H-05 del informe de arquitectura.
    """
    @staticmethod
    def calcular(monto_pagado: float, horas_anticipacion: float) -> float:
        if monto_pagado < 0 or horas_anticipacion < 0:
            raise ValueError("El monto y las horas de anticipación no pueden ser negativos.")
            
        if horas_anticipacion > 24.0:
            return monto_pagado  # 100% de reembolso
        elif 6.0 <= horas_anticipacion <= 24.0:
            return monto_pagado * 0.50  # 50% de reembolso
        else:
            return 0.0  # 0% de reembolso con menos de 6 horas