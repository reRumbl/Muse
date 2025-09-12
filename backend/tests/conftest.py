import asyncio
from typing import AsyncGenerator
from pytest_asyncio import fixture
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.dependencies import get_session
from src.database import Base
from src.company import models
from src.composition import models
from src.ensemble import models
from src.musician import models
from src.performance import models
from src.record import models
from src.release import models
from src.config import test_db_settings

engine_test = create_async_engine(test_db_settings.test_asyncpg_url, poolclass=NullPool)
SessionFactoryTest = async_sessionmaker(
    bind=engine_test, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactoryTest() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@fixture(scope='session')
async def test_async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://testserver') as client:
        yield client
        

@fixture(scope="function")
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactoryTest() as session:
        yield session
