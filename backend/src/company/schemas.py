from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CompanyBase(BaseModel):
    name: str
    address: str
    

class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    address: str | None = None


class Company(CompanyBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
