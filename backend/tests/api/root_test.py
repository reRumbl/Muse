import pytest
from httpx import AsyncClient
from tests.conftest import test_async_client


@pytest.mark.asyncio
async def test_root(test_async_client: AsyncClient):
    response = await test_async_client.get('/')
    assert response.status_code == 200
    assert response.json()['message'] == 'This is Muse API'
