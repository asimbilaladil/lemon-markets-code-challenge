from fastapi import APIRouter

from controllers.order_controller import create_order
from schemas.order import OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])

router.post("", response_model=OrderResponse, status_code=201)(create_order)
