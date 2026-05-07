from abc import ABC, abstractmethod

from models.order import Order
from schemas.order import OrderCreate


class IOrderService(ABC):

    @abstractmethod
    async def create_order(self, payload: OrderCreate) -> Order:
        ...
