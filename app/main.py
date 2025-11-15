from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import status
from sqlmodel import SQLModel

from app.routes import router
from app.dependencies import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        raise
    yield


app = FastAPI(
    title="FastAPI CRUD Service",
    description="A simple and efficient CRUD API for managing tasks",
    version="0.1.0",
    lifespan=lifespan
)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "An unexpected error occurred",
            "path": request.url.path,
            "exception_type": type(exc).__name__
        }
    )


@app.get("/", tags=["health"])
async def health_check():
    return {
        "status": "healthy",
        "message": "FastAPI CRUD Service is running"
    }

# add routes
app.include_router(router)
