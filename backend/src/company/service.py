from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.company.models import CompanyModel
from src.company.schemas import CompanyCreate, CompanyUpdate, Company


class CompanyService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, company_data: CompanyCreate):
        company_db = CompanyModel(**company_data.model_dump())
        self.session.add(company_db)
        await self.session.commit()
        await self.session.refresh(company_db)
        company_schema = Company.model_validate(company_db)
        return company_schema
    
    async def get(self, company_id: UUID):
        company_db = await self.session.get(CompanyModel, company_id)
        company_schema = Company.model_validate(company_db)
        return company_schema
    
    async def update(self, company_id: UUID, company_data: CompanyUpdate):
        company_db = await self.session.get(CompanyModel, company_id)
        
        for key, value in company_data.model_dump(exclude_unset=True).items():
            setattr(company_db, key, value)
            
        await self.session.commit()
        await self.session.refresh(company_db)
        company_schema = Company.model_validate(company_db)
        return company_schema
    
    async def delete(self, company_id: UUID):
        company_db = await self.session.get(CompanyModel, company_id)
        await self.session.delete(company_db)
        await self.session.commit()
    