from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.musician.models import MusicianModel
from src.musician.schemas import MusicianCreate, MusicianUpdate, Musician


class MusicianService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
    
    async def create(self, musician_data: MusicianCreate):
        async with self.session_factory() as session:
            musician_db = MusicianModel(**musician_data.model_dump())
            session.add(musician_db)
            await session.commit()
            await session.refresh(musician_db)
            ensemble_schema = Musician.model_validate(musician_db)
            return ensemble_schema
    
    async def get(self, musician_id: UUID):
        async with self.session_factory() as session:
            musician_db = await session.get(MusicianModel, musician_id)
            musician_schema = Musician.model_validate(musician_db)
            return musician_schema
    
    async def update(self, musician_id: UUID, musician_data: MusicianUpdate):
        async with self.session_factory() as session:
            musician_db = await session.get(MusicianModel, musician_id)
            
            for key, value in musician_data.model_dump(exclude_unset=True).items():
                setattr(musician_db, key, value)
                
            await session.commit()
            await session.refresh(musician_db)
            ensemble_schema = Musician.model_validate(musician_db)
            return ensemble_schema
    
    async def delete(self, musician_id: UUID):
        async with self.session_factory() as session:
            ensemble_db = await session.get(MusicianModel, musician_id)
            await session.delete(ensemble_db)
            await session.commit()
    