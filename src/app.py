from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from src.database.database import engine
from src.api import admin_router, bot_router
from src.utils.fill_rooms import fill_rooms


@asynccontextmanager
async def lifespan(_):
    SQLModel.metadata.create_all(engine)
    fill_rooms()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(admin_router)
app.include_router(bot_router)
