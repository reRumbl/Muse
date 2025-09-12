from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.composition.models import CompositionModel
from src.composition.schemas import CompositionCreate, CompositionUpdate, Composition


class CompositionService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, composition_data: CompositionCreate):
        composition_db = CompositionModel(**composition_data.model_dump())
        self.session.add(composition_db)
        await self.session.commit()
        await self.session.refresh(composition_db)
        composition_schema = Composition.model_validate(composition_db)
        return composition_schema
    
    async def get(self, composition_id: UUID):
        composition_db = await self.session.get(CompositionModel, composition_id)
        composition_schema = Composition.model_validate(composition_db)
        return composition_schema
    
    async def update(self, composition_id: UUID, composition_data: CompositionUpdate):
        composition_db = await self.session.get(CompositionModel, composition_id)
        
        for key, value in composition_data.model_dump(exclude_unset=True).items():
            setattr(composition_db, key, value)
            
        await self.session.commit()
        await self.session.refresh(composition_db)
        composition_schema = Composition.model_validate(composition_db)
        return composition_schema
    
    async def delete(self, composition_id: UUID):
        composition_db = await self.session.get(CompositionModel, composition_id)
        await self.session.delete(composition_db)
        await self.session.commit()
    