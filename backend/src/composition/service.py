from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.composition.models import CompositionModel
from src.composition.schemas import CompositionCreate, CompositionUpdate, Composition


class CompositionService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
    
    async def create(self, composition_data: CompositionCreate):
        async with self.session_factory() as session:
            composition_db = CompositionModel(**composition_data.model_dump())
            session.add(composition_db)
            await session.commit()
            await session.refresh(composition_db)
            ensemble_schema = Composition.model_validate(composition_db)
            return ensemble_schema
    
    async def get(self, composition_id: UUID):
        async with self.session_factory() as session:
            composition_db = await session.get(CompositionModel, composition_id)
            composition_schema = Composition.model_validate(composition_db)
            return composition_schema
    
    async def update(self, composition_id: UUID, composition_data: CompositionUpdate):
        async with self.session_factory() as session:
            composition_db = await session.get(CompositionModel, composition_id)
            
            for key, value in composition_data.model_dump(exclude_unset=True).items():
                setattr(composition_db, key, value)
                
            await session.commit()
            await session.refresh(composition_db)
            ensemble_schema = Composition.model_validate(composition_db)
            return ensemble_schema
    
    async def delete(self, composition_id: UUID):
        async with self.session_factory() as session:
            ensemble_db = await session.get(CompositionModel, composition_id)
            await session.delete(ensemble_db)
            await session.commit()
    