from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.musician.models import MusicianModel
from src.musician.schemas import MusicianCreate, MusicianUpdate, Musician


class MusicianService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, musician_data: MusicianCreate):
        musician_db = MusicianModel(**musician_data.model_dump())
        self.session.add(musician_db)
        await self.session.commit()
        await self.session.refresh(musician_db)
        musician_schema = Musician.model_validate(musician_db)
        return musician_schema
    
    async def get(self, musician_id: UUID):
        musician_db = await self.session.get(MusicianModel, musician_id)
        musician_schema = Musician.model_validate(musician_db)
        return musician_schema
    
    async def update(self, musician_id: UUID, musician_data: MusicianUpdate):
        musician_db = await self.session.get(MusicianModel, musician_id)
        
        for key, value in musician_data.model_dump(exclude_unset=True).items():
            setattr(musician_db, key, value)
            
        await self.session.commit()
        await self.session.refresh(musician_db)
        musician_schema = Musician.model_validate(musician_db)
        return musician_schema
    
    async def delete(self, musician_id: UUID):
        musician_db = await self.session.get(MusicianModel, musician_id)
        await self.session.delete(musician_db)
        await self.session.commit()
    