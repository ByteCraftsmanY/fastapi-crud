import pytest
from httpx import AsyncClient, ASGITransport
from random import randint

from app.main import app


@pytest.mark.asyncio
async def test_health_check() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy", "message": "FastAPI CRUD Service is running"
    }


@pytest.mark.asyncio
async def test_create_task() -> None:
    payload = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": 1,
        "task_code": f"TEST-{randint(100, 999)}"
    }
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(url="/task/", json=payload)
    assert response.status_code == 201
    for key, value in payload.items():
        assert response.json().get(key) == value
