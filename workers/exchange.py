import random
import time

from interfaces.exchange_interface import IExchangeClient


class OrderPlacementError(Exception):
    pass


class ExchangeClient(IExchangeClient):
    def place_order(self, order_id: str) -> None:
        if random.random() < 0.1:
            raise OrderPlacementError(f"Failed to place order {order_id} at the exchange")
        time.sleep(0.5)
