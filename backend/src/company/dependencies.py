from typing import Annotated
from fastapi import Depends
from src.database import SessionFactory
from src.company.service import CompanyService


def get_company_service() -> CompanyService:
    return CompanyService(SessionFactory)


CompanyServiceDep = Annotated[CompanyService, Depends(get_company_service)]
