from abc import ABC, abstractmethod


class IExchangeClient(ABC):

    @abstractmethod
    def place_order(self, order_id: str) -> None:
        ...
