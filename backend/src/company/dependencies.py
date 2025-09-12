from typing import Annotated
from fastapi import Depends
from src.dependencies import SessionDep
from src.company.service import CompanyService


def get_company_service(session: SessionDep) -> CompanyService:
    return CompanyService(session)


CompanyServiceDep = Annotated[CompanyService, Depends(get_company_service)]
