from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.performance.models import PerformanceModel
from src.performance.schemas import PerformanceCreate, PerformanceUpdate, Performance


class PerformanceService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, performance_data: PerformanceCreate):
        performance_db = PerformanceModel(**performance_data.model_dump())
        self.session.add(performance_db)
        await self.session.commit()
        await self.session.refresh(performance_db)
        performance_schema = Performance.model_validate(performance_db)
        return performance_schema
    
    async def get(self, performance_id: UUID):
        performance_db = await self.session.get(PerformanceModel, performance_id)
        performance_schema = Performance.model_validate(performance_db)
        return performance_schema
    
    async def update(self, performance_id: UUID, performance_data: PerformanceUpdate):
        performance_db = await self.session.get(PerformanceModel, performance_id)
        
        for key, value in performance_data.model_dump(exclude_unset=True).items():
            setattr(performance_db, key, value)
            
        await self.session.commit()
        await self.session.refresh(performance_db)
        performance_schema = Performance.model_validate(performance_db)
        return performance_schema
    
    async def delete(self, performance_id: UUID):
        performance_db = await self.session.get(PerformanceModel, performance_id)
        await self.session.delete(performance_db)
        await self.session.commit()
    