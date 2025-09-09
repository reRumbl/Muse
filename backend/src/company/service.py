from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.company.models import CompanyModel
from src.company.schemas import CompanyCreate, CompanyUpdate, Company


class CompanyService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
    
    async def create(self, company_data: CompanyCreate):
        async with self.session_factory() as session:
            company_db = CompanyModel(**company_data.model_dump())
            session.add(company_db)
            await session.commit()
            await session.refresh(company_db)
            company_schema = Company.model_validate(company_db)
            return company_schema
    
    async def get(self, company_id: UUID):
        async with self.session_factory() as session:
            company_db = await session.get(CompanyModel, company_id)
            company_schema = Company.model_validate(company_db)
            return company_schema
    
    async def update(self, company_id: UUID, company_data: CompanyUpdate):
        async with self.session_factory() as session:
            company_db = await session.get(CompanyModel, company_id)
            
            for key, value in company_data.model_dump(exclude_unset=True).items():
                setattr(company_db, key, value)
                
            await session.commit()
            await session.refresh(company_db)
            company_schema = Company.model_validate(company_db)
            return company_schema
    
    async def delete(self, company_id: UUID):
        async with self.session_factory() as session:
            company_db = await session.get(CompanyModel, company_id)
            await session.delete(company_db)
            await session.commit()
    