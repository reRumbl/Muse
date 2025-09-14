from uuid import UUID
from fastapi import APIRouter
from src.auth.dependencies import OnlyAdminUserDep, CurrentUserDep
from src.company.schemas import CompanyCreate, CompanyUpdate, Company
from src.company.dependencies import CompanyServiceDep
from src.schemas import SuccessResponse

router = APIRouter(prefix='/companies', tags=['company'])


@router.post('/', response_model=Company)
async def create_company(
    company_data: CompanyCreate,
    service: CompanyServiceDep,
    user: OnlyAdminUserDep
):
    return await service.create(company_data)


@router.get('/{company_id}', response_model=Company)
async def get_company(
    company_id: UUID,
    service: CompanyServiceDep,
    user: CurrentUserDep
):
    return await service.get(company_id)


@router.put('/{company_id}/update', response_model=Company)
async def update_company(
    company_id: UUID,
    company_data: CompanyUpdate,
    service: CompanyServiceDep,
    user: OnlyAdminUserDep
):
   
    return await service.update(company_id, company_data)


@router.delete('/{company_id}', response_model=SuccessResponse)
async def delete_company(
    company_id: UUID,
    service: CompanyServiceDep,
    user: OnlyAdminUserDep
):
    await service.delete(company_id)
    return SuccessResponse(message='Company deleted')    
