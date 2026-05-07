from sqlalchemy.ext.asyncio import AsyncSession

from interfaces.order_repository_interface import IOrderRepository
from interfaces.order_service_interface import IOrderService
from models.order import Order
from repositories.order_repository import OrderRepository
from schemas.order import OrderCreate
from workers.celery_worker import place_order_task


class OrderService(IOrderService):
    def __init__(self, db: AsyncSession):
        self.repo: IOrderRepository = OrderRepository(db)

    async def create_order(self, payload: OrderCreate) -> Order:
        order = await self.repo.create(payload)
        place_order_task.delay(order.id)
        return order
