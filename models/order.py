import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    instrument: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(Enum("market", "limit", name="order_type"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    side: Mapped[str] = mapped_column(Enum("buy", "sell", name="order_side"), nullable=False)
    limit_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("pending", "placed", "failed", name="order_status"),
        default="pending",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
