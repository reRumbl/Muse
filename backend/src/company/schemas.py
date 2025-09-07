from uuid import UUID
from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    address: str
    

class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    address: str | None = None


class Company(CompanyBase):
    id: UUID
