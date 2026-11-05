class OrderService:
    def __init__(self, gateway):
        self.gateway = gateway

    def checkout(self, order):
        amount = order.confirm()
        if not self.gateway.charge(amount):
            raise RuntimeError(
                f"El pago de ${amount:.2f} fue rechazado por la pasarela de pago. "
                "No se realizó ningún cobro."
            )
        return amount
