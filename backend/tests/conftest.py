from uuid import UUID
from datetime import date
from typing import AsyncGenerator
from pytest_asyncio import fixture
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.dependencies import get_session
from src.database import Base
from src.company.service import CompanyService, CompanyCreate
from src.composition.service import CompositionService, CompositionCreate
from src.ensemble.service import EnsembleService, EnsembleCreate
from src.musician.service import MusicianService, MusicianCreate
from src.performance.service import PerformanceService, PerformanceCreate
from src.record.service import RecordService, RecordCreate
from src.release.service import ReleaseService, ReleaseCreate
from src.ensemble.models import EnsembleType
from src.musician.models import MusicianType
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
        

@fixture(scope='function')
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactoryTest() as session:
        yield session


@fixture(scope='function')
async def company_service(test_session: AsyncSession) -> CompanyService:
    return CompanyService(session=test_session)


@fixture(scope='function')
async def composition_service(test_session: AsyncSession) -> CompositionService:
    return CompositionService(session=test_session)


@fixture(scope='function')
async def ensemble_service(test_session: AsyncSession) -> EnsembleService:
    return EnsembleService(session=test_session)


@fixture(scope='function')
async def musician_service(test_session: AsyncSession) -> MusicianService:
    return MusicianService(session=test_session)


@fixture(scope='function')
async def performance_service(test_session: AsyncSession) -> PerformanceService:
    return PerformanceService(session=test_session)


@fixture(scope='function')
async def record_service(test_session: AsyncSession) -> RecordService:
    return RecordService(session=test_session)


@fixture(scope='function')
async def release_service(test_session: AsyncSession) -> ReleaseService:
    return ReleaseService(session=test_session)


@fixture(scope='function')
async def create_company_factory(company_service: CompanyService):
    async def _create_company(name: str = 'Test Company', address: str = 'Test Address'):
        return await company_service.create(CompanyCreate(name=name, address=address))
    return _create_company


@fixture(scope='function')
async def create_composition_factory(composition_service: CompositionService):
    async def _create_composition(composer_id: UUID, title: str = 'Test Composition'):
        return await composition_service.create(CompositionCreate(title=title, composer_id=composer_id))
    return _create_composition


@fixture(scope='function')
async def create_ensemble_factory(ensemble_service: EnsembleService):
    async def _create_ensemble(name: str = 'Test Ensemble', type: EnsembleType = EnsembleType.orchestra):
        return await ensemble_service.create(EnsembleCreate(name=name, type=type))
    return _create_ensemble


@fixture(scope='function')
async def add_member_to_ensemble_factory(ensemble_service: EnsembleService):
    async def _add_member_to_ensemble(musician_id: UUID, ensemble_id: UUID):
        return await ensemble_service.add_member_to_ensemble(musician_id=musician_id, ensemble_id=ensemble_id)
    return _add_member_to_ensemble


@fixture(scope='function')
async def create_musician_factory(musician_service: MusicianService):
    async def _create_musician(name: str = 'Test', surname: str = 'Musician', type: MusicianType = MusicianType.composer):
        return await musician_service.create(MusicianCreate(name=name, surname=surname, description='description', type=type))
    return _create_musician


@fixture(scope='function')
async def create_performance_factory(performance_service: PerformanceService):
    async def _create_performance(composition_id: UUID, ensemble_id: UUID):
        return await performance_service.create(PerformanceCreate(composition_id=composition_id, ensemble_id=ensemble_id))
    return _create_performance


@fixture(scope='function')
async def create_record_factory(record_service: RecordService):
    async def _create_record(manufacturer_id: UUID, title: str = 'Test Record'):
        return await record_service.create(RecordCreate(title=title, manufacturer_id=manufacturer_id))
    return _create_record


@fixture(scope='function')
async def add_record_to_performance_factory(record_service: RecordService):
    async def _add_record_to_performance(record_id: UUID, performance_id: UUID):
        return await record_service.add_record_to_performance(record_id=record_id, performance_id=performance_id)
    return _add_record_to_performance


@fixture(scope='function')
async def create_release_factory(release_service: ReleaseService):
    async def _create_release(
        record_id: UUID,
        wholesale_supplier_id: UUID,
        release_date: date = date.today(),
        wholesale_price: int = 100,
        retail_price: int = 100,
        last_year_sold: int = 1000,
        this_year_sold: int = 1000,
        in_stock: int = 100,
    ):
        return await release_service.create(ReleaseCreate(
            record_id=record_id,
            release_date=release_date,
            wholesale_supplier_id=wholesale_supplier_id,
            wholesale_price=wholesale_price,
            retail_price=retail_price,
            last_year_sold=last_year_sold,
            this_year_sold=this_year_sold,
            in_stock=in_stock
        ))
    return _create_release
