from pytest_asyncio import fixture
from httpx import AsyncClient, ASGITransport
from src.main import app


@fixture(scope='session')
async def test_async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://testserver') as client:
        yield client
