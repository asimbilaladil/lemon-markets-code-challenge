from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from interfaces.order_service_interface import IOrderService
from logger.logger import get_logger
from schemas.order import OrderCreate, OrderResponse
from services.order_service import OrderService

logger = get_logger(__name__)


async def create_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
) -> OrderResponse:
    service: IOrderService = OrderService(db)
    try:
        order = await service.create_order(payload)
        return OrderResponse.model_validate(order)
    except Exception:
        logger.exception("unexpected error while creating order")
        raise HTTPException(
            status_code=500,
            detail={"message": "Internal server error while placing the order"},
        )
