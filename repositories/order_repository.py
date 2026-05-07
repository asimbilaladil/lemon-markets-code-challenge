from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces.order_repository_interface import IOrderRepository
from models.order import Order
from schemas.order import OrderCreate


class OrderRepository(IOrderRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload: OrderCreate) -> Order:
        order = Order(**payload.model_dump())
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def update_status(self, order_id: str, status: str) -> None:
        await self.db.execute(
            update(Order).where(Order.id == order_id).values(status=status)
        )
        await self.db.commit()
