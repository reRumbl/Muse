from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.release.models import ReleaseModel
from src.release.schemas import ReleaseCreate, ReleaseUpdate, Release


class ReleaseService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
    
    async def create(self, release_data: ReleaseCreate):
        async with self.session_factory() as session:
            release_db = ReleaseModel(**release_data.model_dump())
            session.add(release_db)
            await session.commit()
            await session.refresh(release_db)
            release_schema = Release.model_validate(release_db)
            return release_schema
    
    async def get(self, release_id: UUID):
        async with self.session_factory() as session:
            release_db = await session.get(ReleaseModel, release_id)
            release_schema = Release.model_validate(release_db)
            return release_schema
    
    async def update(self, release_id: UUID, release_data: ReleaseUpdate):
        async with self.session_factory() as session:
            release_db = await session.get(ReleaseModel, release_id)
            
            for key, value in release_data.model_dump(exclude_unset=True).items():
                setattr(release_db, key, value)
                
            await session.commit()
            await session.refresh(release_db)
            release_schema = Release.model_validate(release_db)
            return release_schema
    
    async def delete(self, release_id: UUID):
        async with self.session_factory() as session:
            release_db = await session.get(ReleaseModel, release_id)
            await session.delete(release_db)
            await session.commit()
