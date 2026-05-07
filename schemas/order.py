from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class OrderCreate(BaseModel):
    instrument: str
    type: str
    quantity: int
    side: str
    limit_price: Optional[float] = None

    @model_validator(mode="after")
    def validate_fields(self):
        if self.type not in ("market", "limit"):
            raise ValueError("type must be 'market' or 'limit'")
        if self.side not in ("buy", "sell"):
            raise ValueError("side must be 'buy' or 'sell'")
        if self.type == "limit" and self.limit_price is None:
            raise ValueError("limit_price is required for limit orders")
        if self.type == "market" and self.limit_price is not None:
            raise ValueError("limit_price should not be set for market orders")
        return self


class OrderResponse(BaseModel):
    id: str
    instrument: str
    type: str
    quantity: int
    side: str
    limit_price: Optional[float]
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
