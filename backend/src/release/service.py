from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.release.models import ReleaseModel
from src.release.schemas import ReleaseCreate, ReleaseUpdate, Release


class ReleaseService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, release_data: ReleaseCreate):
        release_db = ReleaseModel(**release_data.model_dump())
        self.session.add(release_db)
        await self.session.commit()
        await self.session.refresh(release_db)
        release_schema = Release.model_validate(release_db)
        return release_schema
    
    async def get(self, release_id: UUID):
        release_db = await self.session.get(ReleaseModel, release_id)
        release_schema = Release.model_validate(release_db)
        return release_schema
    
    async def update(self, release_id: UUID, release_data: ReleaseUpdate):
        release_db = await self.session.get(ReleaseModel, release_id)
        
        for key, value in release_data.model_dump(exclude_unset=True).items():
            setattr(release_db, key, value)
            
        await self.session.commit()
        await self.session.refresh(release_db)
        release_schema = Release.model_validate(release_db)
        return release_schema
    
    async def delete(self, release_id: UUID):
        release_db = await self.session.get(ReleaseModel, release_id)
        await self.session.delete(release_db)
        await self.session.commit()
