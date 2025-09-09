from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.performance.models import PerformanceModel
from src.performance.schemas import PerformanceCreate, PerformanceUpdate, Performance


class PerformanceService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
    
    async def create(self, performance_data: PerformanceCreate):
        async with self.session_factory() as session:
            performance_db = PerformanceModel(**performance_data.model_dump())
            session.add(performance_db)
            await session.commit()
            await session.refresh(performance_db)
            performance_schema = Performance.model_validate(performance_db)
            return performance_schema
    
    async def get(self, performance_id: UUID):
        async with self.session_factory() as session:
            performance_db = await session.get(PerformanceModel, performance_id)
            performance_schema = Performance.model_validate(performance_db)
            return performance_schema
    
    async def update(self, performance_id: UUID, performance_data: PerformanceUpdate):
        async with self.session_factory() as session:
            performance_db = await session.get(PerformanceModel, performance_id)
            
            for key, value in performance_data.model_dump(exclude_unset=True).items():
                setattr(performance_db, key, value)
                
            await session.commit()
            await session.refresh(performance_db)
            performance_schema = Performance.model_validate(performance_db)
            return performance_schema
    
    async def delete(self, performance_id: UUID):
        async with self.session_factory() as session:
            performance_db = await session.get(PerformanceModel, performance_id)
            await session.delete(performance_db)
            await session.commit()
    