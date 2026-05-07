from celery import Celery
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from config.settings import settings
from interfaces.exchange_interface import IExchangeClient
from logger.logger import get_logger
from workers.exchange import ExchangeClient, OrderPlacementError

logger = get_logger(__name__)

celery = Celery("orders", broker=settings.redis_url, backend=settings.redis_url)
celery.conf.task_acks_late = True  # re-queue if the worker crashes mid-task

_engine = create_engine(settings.sync_database_url, pool_pre_ping=True)
_Session = sessionmaker(_engine)

# swap this out for any IExchangeClient implementation
_exchange: IExchangeClient = ExchangeClient()


@celery.task(
    bind=True,
    autoretry_for=(OrderPlacementError,),
    max_retries=5,
    retry_backoff=True,
    retry_jitter=True,
    name="workers.place_order",
)
def place_order_task(self, order_id: str) -> None:
    from models.order import Order

    try:
        _exchange.place_order(order_id)
        status = "placed"
    except OrderPlacementError:
        if self.request.retries >= self.max_retries:
            logger.error("order %s failed after %d retries", order_id, self.max_retries)
            status = "failed"
        else:
            raise

    with _Session() as session:
        session.execute(update(Order).where(Order.id == order_id).values(status=status))
        session.commit()
