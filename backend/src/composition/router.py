from uuid import UUID
from fastapi import APIRouter
from src.auth.dependencies import OnlyAdminUserDep, CurrentUserDep
from src.composition.schemas import CompositionCreate, CompositionUpdate, Composition
from src.composition.dependencies import CompositionServiceDep
from src.schemas import SuccessResponse

router = APIRouter(prefix='/compositions', tags=['composition'])


@router.post('/', response_model=Composition)
async def create_composition(
    composition_data: CompositionCreate,
    service: CompositionServiceDep,
    user: OnlyAdminUserDep
):
    return await service.create(composition_data)


@router.get('/{composition_id}', response_model=Composition)
async def get_composition(
    composition_id: UUID,
    service: CompositionServiceDep,
    user: CurrentUserDep
):
    return await service.get(composition_id)


@router.put('/{composition_id}/update', response_model=Composition)
async def update_composition(
    composition_id: UUID,
    composition_data: CompositionUpdate,
    service: CompositionServiceDep,
    user: OnlyAdminUserDep
):
   
    return await service.update(composition_id, composition_data)


@router.delete('/{composition_id}', response_model=SuccessResponse)
async def delete_composition(
    composition_id: UUID,
    service: CompositionServiceDep,
    user: OnlyAdminUserDep
):
    await service.delete(composition_id)
    return SuccessResponse(message='Composition deleted')    
