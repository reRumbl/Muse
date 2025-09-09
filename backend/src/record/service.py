from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.record.models import RecordModel
from src.record.schemas import RecordCreate, RecordUpdate, Record
from src.record.models import RecordReleaseModel
from src.record.schemas import RecordReleaseCreate, RecordReleaseUpdate, RecordRelease


class RecordService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
    
    async def create(self, record_data: RecordCreate):
        async with self.session_factory() as session:
            record_db = RecordModel(**record_data.model_dump())
            session.add(record_db)
            await session.commit()
            await session.refresh(record_db)
            record_schema = Record.model_validate(record_db)
            return record_schema
    
    async def get(self, record_id: UUID):
        async with self.session_factory() as session:
            record_db = await session.get(RecordModel, record_id)
            record_schema = Record.model_validate(record_db)
            return record_schema
    
    async def update(self, record_id: UUID, record_data: RecordUpdate):
        async with self.session_factory() as session:
            record_db = await session.get(RecordModel, record_id)
            
            for key, value in record_data.model_dump(exclude_unset=True).items():
                setattr(record_db, key, value)
                
            await session.commit()
            await session.refresh(record_db)
            record_schema = Record.model_validate(record_db)
            return record_schema
    
    async def delete(self, record_id: UUID):
        async with self.session_factory() as session:
            record_db = await session.get(RecordModel, record_id)
            await session.delete(record_db)
            await session.commit()


class RecordReleaseService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
    
    async def create(self, release_data: RecordReleaseCreate):
        async with self.session_factory() as session:
            release_db = RecordReleaseModel(**release_data.model_dump())
            session.add(release_db)
            await session.commit()
            await session.refresh(release_db)
            release_schema = RecordRelease.model_validate(release_db)
            return release_schema
    
    async def get(self, release_id: UUID):
        async with self.session_factory() as session:
            release_db = await session.get(RecordReleaseModel, release_id)
            release_schema = RecordRelease.model_validate(release_db)
            return release_schema
    
    async def update(self, release_id: UUID, release_data: RecordReleaseUpdate):
        async with self.session_factory() as session:
            release_db = await session.get(RecordReleaseModel, release_id)
            
            for key, value in release_data.model_dump(exclude_unset=True).items():
                setattr(release_db, key, value)
                
            await session.commit()
            await session.refresh(release_db)
            release_schema = RecordRelease.model_validate(release_db)
            return release_schema
    
    async def delete(self, release_id: UUID):
        async with self.session_factory() as session:
            release_db = await session.get(RecordReleaseModel, release_id)
            await session.delete(release_db)
            await session.commit()
    