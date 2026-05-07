from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.database import Base, engine
from routes.order_routes import router as order_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="lemon.markets orders", lifespan=lifespan)
app.include_router(order_router)
