from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.routes import router
from app.dependencies import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="FastAPI CRUD Service",
    description="A simple and efficient CRUD API for managing tasks",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(router)
