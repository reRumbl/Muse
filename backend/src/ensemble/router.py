from uuid import UUID
from fastapi import APIRouter
from src.auth.dependencies import OnlyAdminUserDep, CurrentUserDep
from src.ensemble.dependencies import EnsembleServiceDep
from src.ensemble.schemas import EnsembleCreate, EnsembleUpdate, Ensemble
from src.composition.schemas import Composition
from src.record.schemas import Record
from src.schemas import SuccessResponse, CountResponse

router = APIRouter(prefix='/ensembles', tags=['ensemble'])


@router.post('/', response_model=Ensemble)
async def create_ensemble(
    ensemble_data: EnsembleCreate, 
    service: EnsembleServiceDep,
    user: OnlyAdminUserDep
):
    return await service.create(ensemble_data)


@router.post('/{ensemble_id}/musicians/{musician_id}', response_model=SuccessResponse)
async def add_member_to_ensemble(
    ensemble_id: UUID, 
    musician_id: UUID,
    service: EnsembleServiceDep,
    user: OnlyAdminUserDep
):
    await service.add_member_to_ensemble(ensemble_id, musician_id)
    return SuccessResponse(message='Member added to ensemble') 


@router.get('/{ensemble_id}', response_model=Ensemble)
async def get_ensemble(
    ensemble_id: UUID,
    service: EnsembleServiceDep,
    user: CurrentUserDep
):
    return await service.get(ensemble_id)


@router.get('/{ensemble_id}/compositions', response_model=list[Composition])
async def get_ensemble_compositions(
    ensemble_id: UUID,
    service: EnsembleServiceDep,
    user: CurrentUserDep
):
    return await service.get_all_compositions(ensemble_id)


@router.get('/{ensemble_id}/compositions/count', response_model=CountResponse)
async def get_ensemble_compositions_count(
    ensemble_id: UUID,
    service: EnsembleServiceDep,
    user: CurrentUserDep
):
    compositions = await service.get_all_compositions(ensemble_id)
    return CountResponse(count=len(compositions))


@router.get('/{ensemble_id}/records', response_model=list[Record])
async def get_ensemble_records(
    ensemble_id: UUID,
    service: EnsembleServiceDep,
    user: CurrentUserDep
):
    return await service.get_all_records(ensemble_id)
    

@router.put('/{ensemble_id}/update', response_model=Ensemble)
async def update_ensemble(
    ensemble_id: UUID,
    ensemble_data: EnsembleUpdate,
    service: EnsembleServiceDep,
    user: OnlyAdminUserDep
):
    return await service.update(ensemble_id, ensemble_data)


@router.delete('/{ensemble_id}/delete', response_model=SuccessResponse)
async def delete_ensemble(
    ensemble_id: UUID,
    service: EnsembleServiceDep,
    user: OnlyAdminUserDep
):
    await service.delete(ensemble_id)
    return SuccessResponse(message='Ensemble deleted')
