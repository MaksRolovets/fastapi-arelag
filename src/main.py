
from fastapi import FastAPI

from routers.user import router as user_router
from routers.transaction import router as trans_router
from routers.analytics import router as anal_router

from schemas.user import *
from schemas.enums import *
from schemas.transaction import *

from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.kafka import start_kafka, stop_kafka


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_kafka()
    yield
    await stop_kafka()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(trans_router)
app.include_router(anal_router)

