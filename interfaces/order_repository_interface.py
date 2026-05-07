from abc import ABC, abstractmethod

from models.order import Order
from schemas.order import OrderCreate


class IOrderRepository(ABC):

    @abstractmethod
    async def create(self, payload: OrderCreate) -> Order:
        ...

    @abstractmethod
    async def update_status(self, order_id: str, status: str) -> None:
        ...
