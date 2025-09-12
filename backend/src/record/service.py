from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.record.models import RecordModel, RecordPerformanceModel
from src.record.schemas import RecordCreate, RecordUpdate, Record


class RecordService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, record_data: RecordCreate):
        record_db = RecordModel(**record_data.model_dump())
        self.session.add(record_db)
        await self.session.commit()
        await self.session.refresh(record_db)
        record_schema = Record.model_validate(record_db)
        return record_schema
    
    async def get(self, record_id: UUID):
        record_db = await self.session.get(RecordModel, record_id)
        record_schema = Record.model_validate(record_db)
        return record_schema
    
    async def update(self, record_id: UUID, record_data: RecordUpdate):
        record_db = await self.session.get(RecordModel, record_id)
        
        for key, value in record_data.model_dump(exclude_unset=True).items():
            setattr(record_db, key, value)
            
        await self.session.commit()
        await self.session.refresh(record_db)
        record_schema = Record.model_validate(record_db)
        return record_schema
    
    async def delete(self, record_id: UUID) -> None:
        record_db = await self.session.get(RecordModel, record_id)
        await self.session.delete(record_db)
        await self.session.commit()
            
    async def add_record_to_performance(self, record_id: UUID, performance_id: UUID) -> None:
        record_performance_db = RecordPerformanceModel(
            record_id=record_id, 
            performance_id=performance_id
        )
        self.session.add(record_performance_db)
        await self.session.commit()
        await self.session.refresh(record_performance_db)
    